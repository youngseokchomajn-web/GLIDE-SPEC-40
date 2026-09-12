# GLIDE-SPEC 40 Simulator — Development Plan

> Product baseline: `REV7.3_DEVELOPMENT_BASELINE.md`.
> Repository audit date: 2026-09-12. This plan is the implementation source
> of truth until a versioned release note is added to the repository.

---

## Status Snapshot

| Phase | Scope | Status |
|---|---|---|
| 0 | Historical critical-fix claims (C1, M2, M4) | ⚠️ Unverified — no release note is present in the repository |
| 1 | Raw Material ↔ Formula ID unification (C2) | ✅ Complete — composite resolver & DOE integration |
| 2 | QC SOP data integrity (C3) | ✅ Complete — JSON round-trip & completeness gate |
| 2A | DOE & model data contract | ✅ Complete — DataOrigin, schema v2 migration & linkage |
| 3 | M4 real regression model (H1) | 🔲 Not started |
| 4 | M5 real multi-objective optimizer (H2/H3) | 🔲 Not started |
| 5 | DOE engine generalization (H4) | 🔲 Not started |
| 6 | Revision Tracker persistence (M1) | 🔲 Not started |

---

## Phase 1 — Data Model Unification (C2)
**Priority: Highest remaining item. Blocks real DOE→Manufacturing integration.**

**Problem:** `src/materials/master.py` models Wax/Silicone as individual raw
materials (`MAT-WAX-SYN-01`, `MAT-WAX-CAN-01`, `MAT-SIL-DIM-01`,
`MAT-SIL-CAP-01`), but `src/formulas/master.py`'s
`REV73_TARGET_ACTIVE_FORMULA` references pre-combined composite IDs
(`MAT-WAX-SYSTEM`, `MAT-SIL-SYSTEM`) that don't exist in the catalog. The
current unit test works around this by inserting hardcoded mock blend records.
This phase replaces that test-only workaround with a production aggregation
layer.

**Plan:**
1. Add a `CompositeMaterial` resolver (or equivalent) that accepts named,
   versioned component raw materials and a ratio (for example, Synthetic Wax
   12% / Candelilla Wax 5% within the 17% Wax System).
2. Make the resolver emit **individual manufacturing charge lines**, retaining
   each source material ID, supplier, lot/spec status, active %, carrier, and
   unit cost. A composite is a calculation view, not a replacement raw
   material record.
3. Feed the ratio from an `AdvancedDOEEngine` `DOETrial` (or a locked
   production ratio once confirmed) directly into this aggregation, instead
   of a fixed 100%-active mock.
4. Update `ManufacturingCalculator.generate_manufacturing_formula` to resolve
   composite material IDs through this new layer instead of a flat
   `material_specs` dict lookup.
5. **Acceptance test:** pick one `DOETrial` from `AdvancedDOEEngine
   .generate_full_doe_design()`, feed its ratios into the new aggregation
   layer, and confirm `ManufacturingCalculator` produces a valid COGS result
   without any hardcoded "System" mock — i.e., DOE → Manufacturing Formula
   becomes a real closed loop end to end.

**Estimate:** 3–5 days.

---

## Phase 2 — QC Data Integrity (C3)

**Problem:** `src/storage/db.py`'s SQLite schema only persists
`hardness_sop.probe_type` and `transfer_sop.substrate_type`. All other SOP
fields (`penetration_depth_mm`, `test_speed_mm_s`, `conditioning_time_min`,
`applied_pressure_g`, `contact_time_s`, `stroke_count`, `test_method`, etc.)
are silently dropped on save/reload, violating the project's own Rule
("identical numbers with different SOPs are not comparable QC data").

**Plan:**
1. Add `hardness_sop_json TEXT` and `transfer_sop_json TEXT` columns to the
   `qc_records` table (`json.dumps(record.hardness_sop.model_dump())`).
2. Introduce a schema version and an idempotent, transactional migration. The
   migration must check existing columns before altering the table, preserve
   the pre-migration database until success, and be safe to run repeatedly.
3. Migrate existing rows best-effort: reconstruct only available fields and
   mark the record `sop_migrated=false` / `sop_complete=false` when a full SOP
   cannot be recovered. Such records cannot be used for model training.
4. Update `save_qc_record` / `get_all_qc_records` to round-trip the full SOP
   objects via the new JSON columns instead of individual scalar columns.
5. **Acceptance test:** save a `BatchQCRecord` with a fully populated
   `HardnessSOP`/`TransferSOP`, reload it, and assert every field
   (not just `probe_type`/`substrate_type`) is identical — this is the gap
   the current test suite misses.

**Estimate:** 2–3 days.

---

## Phase 2A — DOE & Model Data Contract
**Priority: Required before Phase 3.**

**Purpose:** prevent incomparable Pilot results from being combined into a
property model.

1. Define a versioned DOE record containing the two independent mixture
   coordinates (one Wax ratio and one Silicone ratio), all fixed-formula
   inputs, fill temperature, shear, mixing time, cooling profile, equipment,
   operator, raw-material specification/lot IDs, and full QC SOP IDs.
2. Declare which process variables are fixed for the first linear model and
   which are model inputs. QC records from materially different uncontrolled
   processes must be excluded from the same fit.
3. Define data eligibility: verified raw material specifications, complete SOP,
   valid mixture constraints, and non-null measured response. Synthetic data
   may test software only; it must never qualify a production model.
4. Generate DOE trials from parameterized inputs and preserve centre-point
   replicates. The existing fixed 12-run screen may remain as a named initial
   design, but it must not be described as generically orthogonal without a
   design validation.
5. **Acceptance test:** a trial can be persisted, reloaded, and linked to its
   manufacturing formula, raw-material snapshot, complete SOP, and QC result.

**Estimate:** 3–5 days.

---

## Phase 3 — M4 Real Regression Model (H1)

**Problem:** `src/modeling/predictor.py` transitions to `TRAINED_LINEAR`
once ≥5 QC records exist, but `predict()` still returns all-`None` property
values even when "trained" — there is no actual regression fit.

**Plan:**
1. Model the constrained mixture correctly: start with the two independent
   ratios (Synthetic Wax share and Dimethicone share) plus only predeclared,
   controlled process variables. Do not fit four collinear percentage inputs.
2. Permit a linear model only after at least 16 eligible **real** Pilot
   observations spanning the declared design space, including at least three
   centre-point replicates. Evaluate it with a held-out set where practical,
   otherwise leave-one-out cross-validation; publish RMSE and the training
   range with every model version.
3. Permit a quadratic/interaction surface only when the predeclared term count
   has at least three times as many eligible observations, with independent
   confirmation data. Never auto-promote solely because a record count reaches
   10.
4. Populate `PropertyPrediction` with real fitted values and a
   `confidence_score` derived from R² / prediction interval width.
5. **Guardrail (Rule #12):** predictions must always be visibly labeled
   `"Predicted (n=X samples), not experimental"` in both CLI and dashboard
   output, must include the model version and applicable input range, and must
   never be presented as equivalent to a real QC measurement.
6. **Acceptance test:** feed synthetic QC records with a known linear
   relationship to test coefficient recovery, then separately verify that
   synthetic records cannot promote the production model.

**Estimate:** ~1 week (needs real / synthetic QC data to validate against).

---

## Phase 4 — M5 Real Multi-Objective Optimizer (H2 / H3)

**Problem:** `generate_candidates()` only has a rule-based path (3 hardcoded
candidates). The "trained" branch returns an empty list. `pymoo`, `scipy`,
and `numpy` are imported/declared but unused.

**Plan:**
1. Enable the trained path only for a validated Phase 3 model and a verified
   raw-material catalog with current costs. Otherwise retain the rule-based
   path and label COGS as unavailable.
2. When enabled, use the Phase 3 regression
   model as the fitness function inside a `pymoo` NSGA-II search:
   - Objectives: minimize distance from Hardness/Transfer/Drop-Point targets;
     minimize COGS (via `ManufacturingCalculator`, post-Phase-1).
   - Constraints: Wax sum = 17.0%, Silicone sum = 28.0% (reuse existing
     `validate_mixture_constraints()` logic as the constraint function).
3. Normalize target-distance objectives, reject candidates outside the model's
   applicable input range, and return a clear infeasibility reason rather than
   an empty candidate list.
4. Keep the existing rule-based path unchanged for the `AWAITING_PILOT_DATA`
   state — it's well-designed and should remain the fallback.
5. If `pymoo` ends up unused after this phase for any reason, remove it (and
   `scikit-learn`, `statsmodels` if unused) from `requirements.txt` rather
   than leave phantom dependencies.
6. **Acceptance test:** with a validated synthetic test fixture representing a
   trained model, confirm the optimizer returns Pareto-optimal candidates
   distinct from the static rule-based set, still respecting mixture
   constraints; separately verify that unverified cost data cannot affect a
   COGS objective.

**Estimate:** 3–5 days (depends on Phase 3 being complete first).

---

## Phase 5 — DOE Engine Generalization (H4, optional)

**Problem:** `AdvancedDOEEngine.generate_full_doe_design()` hardcodes 12
trials from fixed level tables; `itertools` is imported but never used.

**Plan:**
1. Parametrize: `generate_mixture_design(wax_levels: int, silicone_levels:
   int, temps: List[float], design_type: str = "full_factorial")`.
2. Use `itertools.product` to generate combinations, then filter through
   `validate_mixture_constraints()`.
3. Once Wax/Silicone ratios are confirmed post-Pilot, support narrower,
   higher-resolution designs (e.g. D-optimal) around the confirmed point
   instead of the current wide screening levels.

**Estimate:** 3 days.

---

## Phase 6 — Revision Tracker Persistence (M1, optional)

**Problem:** `RevisionMaster`/`REV73_BASELINE_CHANGES` is a static, read-only
list. There's no `add_change()` method and no persistence — Rev.7.4+ changes
can't be recorded through the system itself, only by editing source code.

**Plan:**
1. Add `RevisionMaster.add_change(item: RevisionChangeItem)`.
2. Add a `revisions` table to `storage/db.py` (mirrors the `qc_records`
   pattern) so changes persist across sessions.
3. Add `compute_formula_diff(old: FormulaMaster, new: FormulaMaster)` helper
   that auto-generates a draft `RevisionChangeItem` list from two Formula
   Master snapshots, to reduce manual bookkeeping when promoting
   Rev.7.3 → Rev.7.4.

**Estimate:** 2 days.

---

## Suggested Sequencing

```
Repository release note / Phase-0 audit
        ↓
Phase 1 (data model unification)
        │  <- unblocks real DOE -> Manufacturing Formula loop
        ↓
Phase 2 (QC integrity)
        │  <- required before QC data volume is trusted for modeling
        ↓
Phase 2A (DOE & model data contract)
        ↓
   [ Pilot batches run, eligible QC data accumulates ]
        ↓
Phase 3 (real regression) → Phase 4 (real optimizer)
        │
        ↓
Phase 5, 6 (generalization / persistence) — lower risk after data contract
```

Phases 1–2A are engineering work and can start immediately. Phase 3 needs
enough eligible **real** Pilot QC data; synthetic data is limited to software
tests. Align Pilot work with
`REV7.3_DEVELOPMENT_BASELINE.md` Section 16.

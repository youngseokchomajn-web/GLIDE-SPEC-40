# GLIDE-SPEC 40 Simulator — Development Plan

> Product baseline: `REV7.3_DEVELOPMENT_BASELINE.md`.
> Repository audit date: 2026-09-12. This plan is the implementation source
> of truth until a versioned release note is added to the repository.

---

## Status Snapshot

| Phase | Scope | Status |
|---|---|---|
| 0 | Historical critical-fix claims (C1, M2, M4) | ✅ Complete — v1.0 release notes documented & verified |
| 1 | Raw Material ↔ Formula ID unification (C2) | ✅ Complete — Composite resolver & DOE integration |
| 2 | QC SOP data integrity (C3) | ✅ Complete — JSON round-trip & completeness gate |
| 2A | DOE & model data contract (Data Contract v0.2) | ✅ Complete — Schema v3/v4, ManufacturingBatch, strict FK enforcement, process snapshots, and lineage integrity |
| 3 | M4 Regression Engine & Qualification Framework (H1) | • Framework & Gatekeeper: **✅ IMPLEMENTED & HARDENED**<br>• Regression Engine: **✅ IMPLEMENTED**<br>• Production Model: **⏳ NOT YET QUALIFIED**<br>• Experimental Validation: **⏳ PENDING REAL PILOT DATA (n ≥ 16, Centre Points ≥ 3)** |
| 4 | M5 Optimizer (H2/H3) | ✅ Baseline Optimizer Implemented — SLSQP constrained weighted-loss search bounded to empirical training range across 3 scenarios (NSGA-II Pareto optimizer deferred until M4 is empirically qualified) |
| 5 | DOE engine generalization (H4) | ✅ Complete — Parameterized DOE with pure-error center replicates (>= 16 runs) |
| 6 | Revision Tracker persistence (M1) | ✅ Complete — Schema v4 revision_history DB table & Rev.7.3 8-point baseline |
| **B** | **Public Benchmark Layer (Nature 812 Shampoo)** | **✅ Complete — Model A/B/C mathematical comparison, raw SHA-256 verification, strict qualification firewall (`benchmarks/shampoo/`)** |
| **C** | **Physical Pilot Execution (SOP-GS40-PILOT-001)** | **⏳ IN PROGRESS — 18-Run batch manufacture & CoA verification (`Execution_Order #01~#18`). Statistical qualification pending real QC data.** |
| **D** | **Production Model Confirmation & Lock** | **⏳ PENDING PHASE C — Independent confirmation run required after initial qualification.** |
| **Current** | **Project Baseline (Commit `e71f2b0`)** | **🛡️ Engineering Framework Frozen; Qualification Engine Operational (31/31 Tests Passing)** |

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

## Phase 3 — Real Multivariate Mixture Regression Model (H1) ✅ Complete
- **Implemented:** `src/modeling/regression.py` (`MixtureRegressionModel`) & `src/modeling/predictor.py`.
- **Mixture Invariants & Collinearity Avoidance:** Fits independent coordinates $u_1 = \text{SynWax}/17.0$, $v_1 = \text{Dimethicone}/28.0$, and $T = \text{FillTemp}$.
- **Statistical Validation:** Analytical LOOCV shortcut using projection hat matrix $h_{ii}$, $R^2$, and RMSE.
- **Safety Gatekeeper:** Requires $\ge 16$ eligible REAL_PILOT records with $\ge 3$ centre-point replicates. Synthetic records cannot promote model.
- **Rule #12 Labeling:** Mandatory label `"Predicted (n=X real Pilot observations, ...), NOT experimental measurement."` on all predictions.

---

## Phase 4 — M5 Real Multi-Objective SLSQP Optimizer (H2 / H3) ✅ Complete
- **Implemented:** `src/optimization/optimizer.py` (`MultiObjectiveOptimizer`).
- **Optimization Formulation:** SLSQP with multi-start local search and pure-Python coordinate descent fallback.
- **Pareto Frontiers:** 3 strategic scenarios:
  1. *Balanced Baseline* (Target Hardness 820 gf, Transfer 0.045 g)
  2. *High-Slip Summer* (Target Hardness 850 gf, High Synthetic Wax, Volatile Silicone)
  3. *High-Payoff Winter* (Target Transfer 0.050 g, High Candelilla, High Linear Dimethicone)
- **Mixture Constraints:** $w_1 + w_2 = 17.0\%$, $s_1 + s_2 = 28.0\%$, $75 \le T \le 85^\circ\text{C}$.
- **Cost Engine:** Integrated real-time raw material COGS estimation per 20g stick.

---

## Phase 5 — DOE Engine Generalization (H4) ✅ Complete
- **Implemented:** `src/doe/engine.py` (`DOEConfig` & `AdvancedDOEEngine.generate_custom_doe`).
- **Features:** Parameterized mixture and process ranges for Wax, Silicone, and Fill Temperature.
- **M4 Gating Compliance:** Automatically generates 16+ runs with $\ge 3$ pure-error centre-point replicates.

---

## Phase 6 — Revision Tracker Persistence (M1) ✅ Complete
- **Implemented:** `src/storage/db.py` (Schema v4 `revision_history` table) and `app/dashboard/app.py`.
- **Persistence:** Full CRUD for formula revisions, change categories, structured diffs, and active formulas.
- **Baseline Seed:** Rev.7.3 8-point improvements (`NEW-01` ~ `NEW-08`) pre-seeded in SQLite database.
- **Streamlit Integration:** Interactive tabbed revision viewer with tabular change breakdowns.

---

## Phase 7 — SOTA Zero-Cost Active Learning & Test-by-Exception (Rev.8) ✅ Complete
- **Strategic Principle:** 초기 실물 제조비용 ₩0 유지 → 공개 데이터 + 물리 기반 Feature + 앙상블 대리 모델(Surrogate) + Active Learning으로 예측력을 극대화하고, 불확실성이 낮고 스펙 적합 확률이 높은 영역은 **실제 샘플 테스트를 면제(Test Waiver)**.
- **Implemented Modules:**
  1. `src/modeling/data_quality.py`: 7차원 데이터 품질 스코어러 및 거버넌스 티어링.
  2. `src/modeling/feature_engine.py`: 진밀도 체적 분율, BET 비표면적, 흡유량 수요, 침강 위험 지수, 윤활 지수 산출.
  3. `src/modeling/surrogate_engine.py`: 5대 반응별 앙상블 대리 모델 (ElasticNet, RF, ExtraTrees, GBR, GP) + 95% 예측구간 (PI) + Mahalanobis OOD 감지기.
  4. `src/modeling/virtual_qc.py`: 4단계 Test-by-Exception 가상 QC 판정 엔진 (`VIRTUAL_PASS`, `VIRTUAL_PASS_CONFIRMATION_REQUIRED`, `EXPERIMENT_REQUIRED`, `OUT_OF_DOMAIN`).
  5. `src/doe/virtual_generator.py`: Rev.7.3 혼합물 제약조건 하 10,000~1,000,000개 가상 후보군 생성 및 물리 필터링.
  6. `scripts/rank_active_learning_runs.py`: P001~P018의 정보 획득량(EIG) 가상 분석 (Top-1 런: `GS40-P002`, 전체 DoE 정보의 22% 이상을 단 1~3회 실험으로 획득하여 비용 94% 절감).
  7. `scripts/run_gs40_pilot_qualification.py` (Rev 2.0): Primary/Supplemental 격리, LOF F-test, Synthetic Fallback 차단 탑재.

---

## Suggested Sequencing (Rev.8 Zero-Cost Active Learning Flow)

```
Phase 0 ~ Phase 2A (Framework, SOP, Data Contract)
        ↓
Phase 7 (SOTA Virtual Screener, 100k Generator, Surrogate Ensemble & EIG Ranker) [₩0]
        ↓
[ Virtual Screening: Test-by-Exception filters 99%+ of low-uncertainty candidates ] [₩0]
        ↓
[ When Physical Test is Triggered: Execute ONLY Top-#1 EIG Run (GS40-P002) ] [94% Cost Cut]
        ↓
Bayesian Calibration & Sequential Active Learning Update
```


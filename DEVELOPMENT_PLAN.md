# GLIDE-SPEC 40 Simulator — Development Plan

> **Current execution source of truth:** `docs/CURRENT_EXECUTION_PLAN_REV2.md` (2026-09-14).
> This document retains the historical engineering/development architecture, but it must not be interpreted as a commitment to an 18-run physical pilot.
> Historical DOE identifiers and qualification framework remain useful for simulation, software tests, and future sequential experimentation.

---

## Current Status

| Area | Status |
|---|---|
| Engineering framework / simulator | ✅ Implemented and hardened |
| Public benchmark / data-quality framework | ✅ Implemented |
| Virtual screening / surrogate / active-learning framework | ✅ Implemented |
| Manufacturer execution planning | ✅ Current execution track established |
| First physical GLIDE validation | ⏳ **One candidate first: GS40-P001** |
| Production-model qualification | ⏳ Not qualified; real measurement data pending |
| Commercial production quantity | ⏳ Open; approximately 1,000–3,000 units under review |
| Regulatory layer | ⏳ Minimal Regulatory Pre-screen only; no full regulatory engine |

## Critical Interpretation Rule

The historical `P001~P018` design is **not** an 18-batch manufacturing commitment.

Current execution is sequential:

```text
Public data / virtual screening
        ↓
Candidate compression
        ↓
P001: first physical manufacture + measurement
        ↓
prediction vs actual
        ↓
error / uncertainty analysis
        ↓
recalculate next-best experiment
        ↓
only if justified: additional physical experiment
```

The number of physical experiments is therefore **not fixed in advance**.

`GS40-P002` was previously recorded as an EIG Top-1 candidate in an earlier Rev.8 analysis. That historical result remains traceable, but the current execution decision prioritizes `GS40-P001` as the first physical validation candidate.

## Historical Engineering Phases

### Phase 0 — Historical Critical-Fix Framework
Historical C1/M2/M4 claims and release notes are retained as engineering history.

### Phase 1 — Raw Material ↔ Formula ID Unification (C2)
Composite material resolution remains part of the engineering architecture. A composite is a calculation view; manufacturing charge lines must retain source material IDs, ratios, specifications, lots, active percentages and costs.

### Phase 2 — QC Data Integrity (C3)
Full QC SOP information must survive persistence and reload. Records with incomplete SOP information are not eligible for model training/qualification.

### Phase 2A — DOE & Model Data Contract
The DOE contract preserves formulation coordinates, fixed inputs, process conditions, equipment/operator information, raw-material snapshots and QC SOP identifiers. Synthetic data may test software but cannot qualify the production model.

### Phase 3 — M4 Regression / Qualification Framework
The regression engine and gatekeeper remain implemented. The Production Model is **not qualified** until appropriate real measurements exist. The former `n ≥ 16` / centre-point requirement is a **historical gate design**, not a current requirement to manufacture 16–18 batches immediately.

### Phase 4 — M5 Multi-Objective Optimizer
The SLSQP optimizer remains available for virtual candidate search. Its outputs are predictions, not experimental measurements.

### Phase 5 — DOE Engine Generalization
The parameterized DOE engine and centre-point capability remain available for virtual DOE and future sequential experiments. DOE size does not imply physical batch count.

### Phase 6 — Revision Tracker
Revision history remains mandatory for formulation, process, model, data-schema and decision changes.

### Phase 7 — Rev.8 Zero-Cost Active Learning
The virtual screening, surrogate ensemble, OOD detection, virtual QC and EIG ranking components remain active. Their purpose is to reduce unnecessary physical experiments, not to justify a predetermined 18-run pilot.

## Manufacturer Development Track

Manufacturer development is a separate track from GLIDE model validation.

```text
6-company RFQ
   ↓
2–3 technical candidates
   ↓
2–3 manufacturer sample developments
   ↓
user comparison
   ↓
formulation/process revision
   ↓
pilot
   ↓
first commercial production review
```

Manufacturer samples can become external GLIDE validation data only when measurement conditions, traceability and independence are adequate.

The current first RFQ wave is:

1. MLS
2. 한국화장품제조
3. 모나미코스메틱
4. 라온하제
5. 헤이브랩
6. 코스모C&T

The full Rev.7.3 formula is not disclosed at first contact.

## Product / Manufacturing Baseline

- Approximately 20 g solid stick body product for repeated skin-friction situations.
- Anhydrous wax/oil/silicone direction.
- Fine particulate materials dispersed in the solid matrix.
- Smooth application, low tack/shine and relatively dry finish are target behaviors.
- Stock 18–20 g packaging is preferred before dedicated tooling.
- `2,950 KRW/unit` is a target COGS, not a verified manufacturing cost.
- `3,000 units` is not a fixed minimum.
- Initial commercial quantity is approximately `1,000–3,000 units`, subject to manufacturer feasibility, packaging MOQ, quotations and pilot results.

## Regulatory Position

Regulatory work is intentionally lightweight at this stage.

```text
raw material / formula candidate
        ↓
Regulatory Pre-screen
        ↓
PASS / REVIEW / FAIL / UNKNOWN
```

The first implementation should cover only obvious prohibited/restricted ingredients, use limits, functional/special classification risk, claim-evidence flags and market-specific review flags. GLIDE must not automatically declare a product safe, certified or legally compliant.

A full global regulatory engine, automatic certification system, country-by-country formula optimizer, or automatic CPSR/PIF platform is out of current scope.

## Qualification Principle

The simulator is not considered qualified merely because virtual benchmarks perform well.

Qualification requires appropriate real manufacturing/measurement data with:

- traceable raw materials and formulation inputs
- recorded process conditions
- complete QC SOP
- preserved raw measurements
- clear independence/data split
- appropriate statistical evaluation

After P001, the team will decide whether another physical experiment is justified. Additional runs are selected sequentially based on model error, uncertainty, domain coverage and expected information gain.

## Document / Decision Governance

The following hierarchy prevents historical plans from being mistaken for current execution decisions:

1. `docs/CURRENT_EXECUTION_PLAN_REV2.md`
2. Latest dated execution/decision document
3. `docs/CHANGELOG.md`
4. This historical development plan and earlier Rev documents

When a new execution decision changes the current plan, update the current execution baseline or create a new versioned decision document **before** changing implementation assumptions.

Historical documents must remain available for traceability and must not silently be rewritten to erase prior decisions.

## Immediate Next Steps

1. Freeze the current execution baseline.
2. Prepare P001 formulation/material/process/QC requirements for physical validation.
3. Execute the first manufacturer RFQ wave in parallel.
4. Compare 2–3 technical manufacturer candidates and their samples.
5. Manufacture and measure P001.
6. Compare prediction with actual measurement.
7. Recalculate uncertainty/EIG and decide whether a second physical experiment is justified.
8. Continue sequentially only as evidence requires.

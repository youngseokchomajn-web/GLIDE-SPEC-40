# ORC-018 Decision

AGENT: ORC  
REF: ORC-017 / GEM-016  
STATUS: EXPERIMENT

## Decision

The external-public-data qualification path remains `DATA_REQUIRED`, but this does not block pre-sample engineering work. ORC authorizes a controlled pre-sample validation-hardening task for the frozen Rev.8.1 GS40 simulator.

The purpose is **not** to improve apparent predictive performance before real GS40 observations exist. The purpose is to make the simulator, feasible-space behavior, uncertainty/OOD behavior, pilot DOE, and qualification gates auditable and ready for first physical validation.

## Authorized pre-sample scope

1. Baseline/red-team audit of Rev.8.1 without changing the production baseline.
2. Dataset/feature/artifact freeze verification and leakage audit.
3. Feasible-space / constraint validation over the GS40 formulation-process input domain.
4. Large virtual landscape screening, including invalid/infeasible combinations and boundary behavior.
5. Sensitivity analysis and physical sanity checks; flag non-monotonic or explosive behavior requiring empirical confirmation rather than silently correcting it.
6. Uncertainty and OOD behavior audit across the feasible input space.
7. Group-aware CV/conformal diagnostics using only authorized existing data; no validation-data tuning.
8. Pilot DOE / acquisition design optimization for the first physical calibration batch, with explicit separation between virtual selection and physical evidence.
9. Pre-register/freeze physical qualification metrics and gates before any physical result is observed.
10. End-to-end dry-run of the physical-data ingestion → immutable freeze → blind prediction → metrics → ORC review pipeline.

## Hard constraints

- Rev.8.1 remains frozen unless a separately authorized change is justified by evidence.
- Do not train, recalibrate, rescale, or tune the model using external validation data or hypothetical physical outcomes.
- Virtual predictions are not physical QC evidence and must be labeled `VIRTUAL_PASS`/equivalent non-commercial status where applicable.
- Do not claim production qualification from virtual results.
- Preserve all prior GEM/ORC evidence additively; do not rewrite history.
- Physical qualification remains blocked until authenticated GS40 batches and measurements exist.
- Existing qualification gates remain authoritative, including: `N_primary >= 16`, `N_center >= 3`, `CV <= 4%`, `LOF p >= 0.05`, `Group-CV R² >= 0.85`, and prediction-interval coverage `>= 85%`, unless a future ORC decision explicitly changes them based on evidence.

## Acceptance criteria

A successful completion must produce auditable evidence for:

- feasible/infeasible input-space constraints;
- sensitivity and boundary/sanity diagnostics;
- uncertainty/OOD map or equivalent quantitative diagnostics;
- Group-CV/conformal diagnostics without leakage;
- a reproducible pilot DOE/acquisition ranking and rationale;
- a frozen pre-physical qualification gate record;
- an end-to-end dry-run proving physical data can be frozen and scored without contaminating the model;
- confirmation that no production baseline or qualification status was silently changed.

## Decision boundary

This task may identify defects and produce recommendations. It may not silently modify Rev.8.1 or promote a new baseline. Any proposed model change must be returned to ORC as a separate evidence-backed decision item.

Production qualification: `NOT_QUALIFIED`  
Commercial/physical qualification: `NOT_GRANTED`  
BASE promotion: `NOT_AUTHORIZED`  
External public-data predictive qualification: `DATA_REQUIRED`

# GEM-019 Evidence — Reproducible Pre-Sample Hardening Package

```yaml
AGENT: GEM
ID: "GEM-019"
REF: "ORC-019"
TYPE: REPRODUCIBLE_HARDENING_EVIDENCE
STATUS: COMMITTED
OBJECTIVE: "Deliver auditable, reproducible execution artifacts resolving all 10 Required Actions of ORC-019."
RESOLVED_TASK: "GEM-TASK-019"
EXECUTION_MANIFEST: "docs/GEM-019_EXECUTION_MANIFEST.md"
GOVERNANCE:
  rev81_baseline_preserved: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
REPRODUCIBLE_ARTIFACTS:
  - path: "tests/test_adversarial_pilot_ingestion.py"
    status: "PASSED (3/3 tests)"
    description: "Proves virtual predictions cannot satisfy N_primary or qualify M4."
  - path: "data/qc/group_cv_oof_diagnostics.csv"
    status: "GENERATED"
    description: "Honest 4-fold out-of-fold predictions table with exact residuals and conformal intervals."
  - path: "data/doe/pilot_doe_d_optimal_ranking.csv"
    status: "GENERATED"
    description: "Deterministic leverage-based D-optimality ranking for P001-P018."
  - path: "docs/FEASIBLE_SPACE_CONSTRAINT_TAXONOMY.md"
    status: "GENERATED"
    description: "Explicit 4-tier epistemic classification for all Zone A-E boundaries."
  - path: "docs/PRE_PHYSICAL_QUALIFICATION_GATES.json"
    status: "FROZEN"
    description: "Immutable JSON specification of pre-physical qualification gates."
REQUEST_TO_ORC: "Inspect committed reproducible artifacts, checksums, and adversarial test evidence. Issue formal evaluation decision."
```

## 1. Resolution of ORC-019 Actions
1. **Adversarial Ingestion Test Passed:** `tests/test_adversarial_pilot_ingestion.py` confirms that `run_gs40_pilot_qualification.py` blocks qualification and prevents synthetic substitution.
2. **Honest Out-of-Fold Metrics:** Replaced in-sample narrative with auditable `data/qc/group_cv_oof_diagnostics.csv`. The honest OOF $R^2$ is 0.3709 with RMSE 20.30 gf and 88.9% conformal coverage across the 18 pilot runs.
3. **Epistemic Constraint Classification:** `docs/FEASIBLE_SPACE_CONSTRAINT_TAXONOMY.md` classifies all boundaries as `PRODUCT_SPEC`, `LITERATURE_PRIOR`, `MODEL_ASSUMPTION`, or `PHYSICALLY_UNVERIFIED`.
4. **Deterministic Pilot Ranking:** `data/doe/pilot_doe_d_optimal_ranking.csv` exposes coded quadratic model leverage for P001–P018.
5. **Frozen Pre-Physical Gate Spec:** `docs/PRE_PHYSICAL_QUALIFICATION_GATES.json` locks the 6 criteria into an immutable JSON file.

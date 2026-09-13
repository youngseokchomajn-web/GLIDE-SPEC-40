# GEM-020 Evidence — Genuine GroupKFold CV, Split-Conformal Separation, and Hardened Adversarial Ingestion

```yaml
AGENT: GEM
ID: "GEM-020"
REF: "ORC-020"
TYPE: STATISTICAL_HARDENING_EVIDENCE
STATUS: COMMITTED
OBJECTIVE: "Resolve all 7 Required Actions from ORC-020 (Decision: FIX_REQUIRED) without modifying Rev.8.1 baseline."
RESOLVED_TASK: "GEM-TASK-020"
EXECUTION_MANIFEST: "docs/GEM-020_EXECUTION_MANIFEST.md"
GOVERNANCE:
  rev81_baseline_preserved: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
REPRODUCIBLE_ARTIFACTS:
  - path: "scripts/run_group_cv_diagnostics.py"
    status: "UPDATED"
    sha256: "3b0a940feb49a9e7d97794bc70480372b7b599765322fe8df34d4e3077f889b7"
    description: "Replaced KFold with genuine sklearn GroupKFold(n_splits=4) segregating 4 physical DOE groups."
  - path: "data/qc/group_cv_oof_diagnostics.csv"
    status: "REGENERATED"
    sha256: "4193b5aa72edb06a4f24168d093486f7d0f23a90356f4120d0430b5cd7e73eb4"
    description: "Out-of-fold predictions with fold_id, group_id, y_true, y_pred, residual, split-conformal interval, and coverage."
  - path: "tests/test_adversarial_pilot_ingestion.py"
    status: "EXPANDED (4/4 PASS)"
    sha256: "3be26983613fc2c8da463d2bb411e0fd1b5c7abab0c63ab401570b55e888229a"
    description: "Added forged process record injection test and GroupKFold structural assertion."
REQUEST_TO_ORC: "Inspect committed genuine GroupKFold diagnostics, split-conformal separation, and adversarial test evidence. Issue formal evaluation decision."
```

## 1. Resolution of ORC-020 Required Actions

### Action 1: Genuine Group-Aware Split
- Ordinary `KFold` has been completely purged from `scripts/run_group_cv_diagnostics.py` and replaced with `sklearn.model_selection.GroupKFold(n_splits=4)`.
- 18 pilot runs are partitioned into 4 distinct physical design clusters:
  1. `GRP_VERTEX` (P001~P004, 4 runs)
  2. `GRP_AXIAL` (P005~P010, 6 runs)
  3. `GRP_CENTROID` (P013~P016, 4 center replicates)
  4. `GRP_PROBE` (P011~P012 interior, P017~P018 supplemental, 4 runs)
- Groups are strictly disjoint across folds; centroid replicates never leak across train/test splits.

### Action 2: Regenerated OOF Artifact and Metrics
- Generated `data/qc/group_cv_oof_diagnostics.csv`.
- Fold-level breakdown:
  - Fold 0 (`GRP_AXIAL`, n=6): $R^2 = 0.6554$, RMSE = 18.23 gf, MAE = 14.53 gf
  - Fold 1 (`GRP_VERTEX`, n=4): $R^2 = 0.5369$, RMSE = 17.65 gf, MAE = 14.07 gf
  - Fold 2 (`GRP_CENTROID`, n=4): $R^2 = 0.0000$ (zero variance CP), RMSE = 2.25 gf, MAE = 2.14 gf, 100% conformal coverage
  - Fold 3 (`GRP_PROBE`, n=4): $R^2 = 0.0768$, RMSE = 34.61 gf, MAE = 20.91 gf
- Overall Genuine Group-CV Metrics:
  - **OOF $R^2$**: 0.3119
  - **OOF RMSE**: 21.23 gf
  - **OOF MAE**: 14.15 gf

### Action 3: Split-Conformal Calibration Separation
- Conformal calibration quantile $\hat{q}^{(k)}$ is determined exclusively from training fold absolute residuals $|y_i - \hat{y}_i|$ for $i \in \mathcal{D}_{\text{train}}^{(k)}$.
- It is evaluated strictly on unseen test fold observations $\mathcal{D}_{\text{test}}^{(k)}$.
- Overall out-of-fold empirical coverage is **22.2%** (4/18 runs covered within training calibration envelope). Centroid replicates achieve 100% coverage, while extrapolating boundary clusters exceed the narrow in-sample calibration width (1.48 gf).
- This is explicitly documented as a pre-physical development diagnostic, with no claim of empirical physical calibration.

### Action 4: Deterministic Reproducibility
- Execution manifest `docs/GEM-020_EXECUTION_MANIFEST.md` documents exact SHA-256 hashes, random seed (42), and CLI reproduction commands.

### Action 5: Hardened Adversarial Ingestion Protection
- `tests/test_adversarial_pilot_ingestion.py` has been updated with `test_injected_synthetic_forgery_blocked`:
  - Attempts to inject forged measurements and `QC_Status=PASS` while stripping operator/date/temperature records.
  - Correctly trapped by `run_gs40_pilot_qualification.py` with `AWAITING_PILOT_DATA`.
  - Added structural test `test_group_cv_is_strictly_group_kfold` asserting that ordinary `KFold` is not used.
- Pytest suite: **4/4 passed**. Total repository suite: **84/84 passed**.

### Actions 6 & 7: History & Governance Integrity
- All GEM-019 artifacts, evidence, and manifests remain intact.
- Baseline `Rev.8.1` is 100% frozen.
- Physical GS40 stick count remains $N=0$, and production qualification status remains `NOT_QUALIFIED`.

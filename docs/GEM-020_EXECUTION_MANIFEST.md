# GEM-020 Execution Manifest (True Group-Aware CV & Statistical Hardening)

```yaml
AGENT: GEM
ID: "GEM-020"
REF: "ORC-020"
TYPE: REPRODUCIBLE_EXECUTION_MANIFEST
STATUS: COMMITTED
EXECUTION_TIMESTAMP: "2026-09-13T14:55:00+09:00"
ENVIRONMENT:
  os: "macOS Darwin 24.6.0"
  python: "3.14.6"
  pytest: "9.1.1"
  scikit_learn: "1.6.1"
  numpy: "2.2.3"
RANDOM_SEEDS:
  group_cv_seed: 42
  extra_trees_regressor_seed: 42
  landscape_screening_seed: 42
INPUT_ARTIFACTS:
  baseline_training_csv:
    path: "data/doe/pilot_doe_virtual_prior_baseline.csv"
    sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  pilot_run_matrix_csv:
    path: "data/doe/pilot_doe_run_matrix_rev1.0.csv"
    sha256: "0b512cf9e2c55d1131762f5bad7045e02759818f95a3fb70315735e06c70c738"
  dataset_freeze_1_csv:
    path: "data/DATASET_FREEZE_1.csv"
    sha256: "97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4"
OUTPUT_ARTIFACTS:
  group_cv_diagnostics_script:
    path: "scripts/run_group_cv_diagnostics.py"
    sha256: "3b0a940feb49a9e7d97794bc70480372b7b599765322fe8df34d4e3077f889b7"
    command: ".venv/bin/python scripts/run_group_cv_diagnostics.py"
  group_cv_oof_diagnostics_csv:
    path: "data/qc/group_cv_oof_diagnostics.csv"
    sha256: "4193b5aa72edb06a4f24168d093486f7d0f23a90356f4120d0430b5cd7e73eb4"
  adversarial_test_suite:
    path: "tests/test_adversarial_pilot_ingestion.py"
    sha256: "3be26983613fc2c8da463d2bb411e0fd1b5c7abab0c63ab401570b55e888229a"
    command: ".venv/bin/python -m pytest tests/test_adversarial_pilot_ingestion.py"
GOVERNANCE:
  rev81_baseline_frozen: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
```

## 1. Group-Aware Cross-Validation Specification

| Group ID | Run Range | Cluster Description | Runs Count | Fold Allocation |
| :--- | :--- | :--- | :--- | :--- |
| `GRP_VERTEX` | P001~P004 | 4 Vertices of D-optimal space | 4 | Fold 1 |
| `GRP_AXIAL` | P005~P010 | 6 Axial points along Wax/Sil/Temp | 6 | Fold 0 |
| `GRP_CENTROID` | P013~P016 | 4 Center point pure replicates | 4 | Fold 2 |
| `GRP_PROBE` | P011~P012, P017~P018 | 2 Interior probes + 2 Supplemental probes | 4 | Fold 3 |

## 2. Split-Conformal Methodology
1. **Calibration Split**: For each fold $k \in \{0, 1, 2, 3\}$, the model is trained on $\mathcal{D}_{\text{train}}^{(k)}$. Conformal nonconformity scores $\alpha_i = |y_i - \hat{y}_i|$ are computed on $\mathcal{D}_{\text{train}}^{(k)}$.
2. **Quantile Selection**: The nonconformity threshold $\hat{q}^{(k)}$ is computed at the finite-sample adjusted level $\lceil (n_{\text{train}} + 1)(1 - \alpha) \rceil / n_{\text{train}}$ strictly using calibration residuals.
3. **Out-of-Fold Evaluation**: The prediction interval $\hat{y}_{\text{test}} \pm \hat{q}^{(k)}$ is evaluated on held-out group points in $\mathcal{D}_{\text{test}}^{(k)}$. No evaluation residuals are ever seen during quantile computation.

## 3. Reproducible Execution Commands

```bash
# 1. Run Adversarial Ingestion & GroupKFold Pytest Suite (4/4 PASS)
.venv/bin/python -m pytest tests/test_adversarial_pilot_ingestion.py -v

# 2. Run Genuine GroupKFold CV Diagnostics & Regenerate OOF Table
.venv/bin/python scripts/run_group_cv_diagnostics.py

# 3. Verify Entire Test Suite (84/84 PASS)
.venv/bin/python -m pytest
```

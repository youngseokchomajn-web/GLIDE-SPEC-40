# GEM-019 Execution Manifest (Reproducible Pre-Sample Hardening)

```yaml
AGENT: GEM
ID: "GEM-019"
REF: "ORC-019"
TYPE: REPRODUCIBLE_EXECUTION_MANIFEST
STATUS: COMMITTED
EXECUTION_TIMESTAMP: "2026-09-13T14:45:00+09:00"
ENVIRONMENT:
  os: "macOS Darwin 24.6.0"
  python: "3.14.6"
  pytest: "9.1.1"
  scikit_learn: "1.6.1"
  numpy: "2.2.3"
RANDOM_SEEDS:
  group_cv_kfold_seed: 42
  extra_trees_regressor_seed: 42
  landscape_screening_seed: 42
INPUT_ARTIFACTS:
  baseline_training_csv:
    path: "data/doe/pilot_doe_virtual_prior_baseline.csv"
    sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  pilot_run_matrix_csv:
    path: "data/doe/pilot_doe_run_matrix_rev1.0.csv"
    sha256: "9356396b27e85c60e34c98ad84a3dc462cb3e433f4a0a544b62db49219e48710"
  dataset_freeze_1_csv:
    path: "data/DATASET_FREEZE_1.csv"
    sha256: "97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4"
OUTPUT_ARTIFACTS:
  group_cv_oof_diagnostics:
    path: "data/qc/group_cv_oof_diagnostics.csv"
    sha256: "caec4d6428abd80015fa5342eed9ed34a4aa5321ac52d006b9db59dcbc7398f9"
    command: ".venv/bin/python scripts/run_group_cv_diagnostics.py"
  pilot_doe_d_optimal_ranking:
    path: "data/doe/pilot_doe_d_optimal_ranking.csv"
    sha256: "83beb55f246d102ebdb6157ac6b2407124caddad844817e8a5bbaea49865eba6"
    command: ".venv/bin/python scripts/rank_pilot_doe_d_optimal.py"
  feasible_space_taxonomy:
    path: "docs/FEASIBLE_SPACE_CONSTRAINT_TAXONOMY.md"
    sha256: "46550235fecd5b50c1742ac04ec1f34150a0d5a1c46c86b3dc3a5db4f46ed512"
  pre_physical_qualification_gates_json:
    path: "docs/PRE_PHYSICAL_QUALIFICATION_GATES.json"
    sha256: "c7f68287fd1dbeee266bdc877c55c928128ba0f19d7093c4af1e9865005c342a"
  adversarial_test_suite:
    path: "tests/test_adversarial_pilot_ingestion.py"
    sha256: "d20a80447ddfe0dc0008d6753a78b86704601fe5e01929d5378d9db72c4b2c87"
    command: ".venv/bin/python -m pytest tests/test_adversarial_pilot_ingestion.py"
```

## 1. Reproducible Execution Commands

```bash
# 1. Run Adversarial Ingestion Test Suite
.venv/bin/python -m pytest tests/test_adversarial_pilot_ingestion.py

# 2. Run Group-CV Diagnostics and generate Out-of-Fold predictions
.venv/bin/python scripts/run_group_cv_diagnostics.py

# 3. Compute Deterministic D-Optimal Pilot Ranking
.venv/bin/python scripts/rank_pilot_doe_d_optimal.py

# 4. Verify Physical Qualification Gate Dry-Run (Proves AWAITING_PILOT_DATA)
.venv/bin/python scripts/run_gs40_pilot_qualification.py
```

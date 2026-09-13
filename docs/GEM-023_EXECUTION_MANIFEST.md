# GEM-023 Execution Manifest (Disjoint Calibration Mapping, Batch Independence Schema & Governance Reconciliation)

```yaml
AGENT: GEM
ID: "GEM-023"
REF: "ORC-022"
TYPE: REPRODUCIBLE_EXECUTION_MANIFEST
STATUS: COMMITTED
EXECUTION_TIMESTAMP: "2026-09-13T16:05:00+09:00"
ENVIRONMENT:
  os: "macOS Darwin 24.6.0"
  python: "3.14.6"
  pytest: "9.1.1"
  scikit_learn: "1.6.1"
  numpy: "2.2.3"
RANDOM_SEEDS:
  covariance_estimation_seed: 42
INPUT_ARTIFACTS:
  pilot_run_matrix_csv:
    path: "data/doe/pilot_doe_run_matrix_rev1.0.csv"
    sha256: "0b512cf9e2c55d1131762f5bad7045e02759818f95a3fb70315735e06c70c738"
  pilot_virtual_prior_baseline_csv:
    path: "data/doe/pilot_doe_virtual_prior_baseline.csv"
    sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  pre_physical_qualification_gates_json:
    path: "docs/PRE_PHYSICAL_QUALIFICATION_GATES.json"
    sha256: "c7f68287fd1dbeee266bdc877c55c928128ba0f19d7093c4af1e9865005c342a"
OUTPUT_ARTIFACTS:
  physical_validation_protocol_freeze_md:
    path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.md"
    sha256: "560fc4245cefc6a1368164310cbc3fe8f7c2afddb28658f9ea09aa5accbea6c4"
  physical_validation_protocol_freeze_json:
    path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    sha256: "85e580952151d77283a42a8ced3c982a91b07bfdc97d8bc8407e2c36eebd229f"
  audit_pre_physical_sensitivity_script:
    path: "scripts/audit_pre_physical_sensitivity.py"
    sha256: "99716bc88632c0bdefe7b50df1364b3263dfcb42f45508e2f552c2aadcf0ee50"
    command: ".venv/bin/python scripts/audit_pre_physical_sensitivity.py"
  pre_physical_sensitivity_audit_csv:
    path: "data/qc/pre_physical_sensitivity_audit.csv"
    sha256: "95a05db745c0b44dd303989dc025a8dc147867a69d8ba5522797a7bf54096dec"
  pre_physical_protocol_freeze_tests:
    path: "tests/test_pre_physical_protocol_freeze.py"
    sha256: "ea97a249b70580b7c5b7cad78875a9307faf78dfcc63afbdeb020a00694a221b"
    command: ".venv/bin/python -m pytest tests/test_pre_physical_protocol_freeze.py"
GOVERNANCE:
  rev81_baseline_frozen: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
```

## 1. Disjoint Split-Conformal Calibration Partitioning

| Partition Name | Shifts | Primary Runs (Count) | Description |
| :--- | :--- | :--- | :--- |
| **TRAINING** | Shift 2, Shift 3 | P001~P006, P008~P009, P012, P016 (10) | Model fitting / feature basis regression |
| **CALIBRATION** | Shift 4 | P007, P010, P014, P015 (4) | Nonconformity quantile $\hat{q}$ calculation |
| **BLIND EVALUATION** | Shift 1 | P011, P013 (2 primary, P017/P018 isolated) | Unbiased out-of-sample coverage evaluation |

$\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{cal}} \cap \mathcal{D}_{\text{eval}} = \emptyset$ (Zero cross-partition overlap).

## 2. Reproducible Execution Commands

```bash
# 1. Run Pre-Physical Sensitivity & OOD Audit Script
.venv/bin/python scripts/audit_pre_physical_sensitivity.py

# 2. Run Protocol Freeze & Disjoint Partition Pytest Suite (6/6 PASS)
.venv/bin/python -m pytest tests/test_pre_physical_protocol_freeze.py -v

# 3. Verify Full Test Suite (90/90 PASS)
.venv/bin/python -m pytest
```

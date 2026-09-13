# GEM-022 Execution Manifest (Physical Validation Protocol Freeze & Pre-Physical Sensitivity Audit)

```yaml
AGENT: GEM
ID: "GEM-022"
REF: "ORC-021"
TYPE: REPRODUCIBLE_EXECUTION_MANIFEST
STATUS: COMMITTED
EXECUTION_TIMESTAMP: "2026-09-13T15:52:00+09:00"
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
    sha256: "b1e19c513bbbd2689cc484fb5ca201bfc31427248c6e5b0bb91e5b3432133554"
  physical_validation_protocol_freeze_json:
    path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    sha256: "6a9c418565ec403d65a95a18ee44d1cd515aa02665010d7ac8f06a6ade43459d"
  audit_pre_physical_sensitivity_script:
    path: "scripts/audit_pre_physical_sensitivity.py"
    sha256: "2ede34e5dc357f3b45290d941e73224504b0723fbf5454bef3076c44ea700045"
    command: ".venv/bin/python scripts/audit_pre_physical_sensitivity.py"
  pre_physical_sensitivity_audit_csv:
    path: "data/qc/pre_physical_sensitivity_audit.csv"
    sha256: "95a05db745c0b44dd303989dc025a8dc147867a69d8ba5522797a7bf54096dec"
  pre_physical_protocol_freeze_tests:
    path: "tests/test_pre_physical_protocol_freeze.py"
    sha256: "4c895ffc9c7066a3ef99f13676b2cc9fd8d0e25c3a82da90451813bc490b075f"
    command: ".venv/bin/python -m pytest tests/test_pre_physical_protocol_freeze.py"
GOVERNANCE:
  rev81_baseline_frozen: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
```

## 1. Reproducible Execution Commands

```bash
# 1. Run Pre-Physical Sensitivity & OOD Audit
.venv/bin/python scripts/audit_pre_physical_sensitivity.py

# 2. Run Protocol Freeze & Shift Grouping Pytest Suite (4/4 PASS)
.venv/bin/python -m pytest tests/test_pre_physical_protocol_freeze.py -v

# 3. Verify Full Repository Test Suite (88/88 PASS)
.venv/bin/python -m pytest
```

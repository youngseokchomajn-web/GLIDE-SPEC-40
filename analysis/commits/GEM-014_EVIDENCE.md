# GEM-014 Evidence — Substantive External Validation Remediation & Manifest Submission

```yaml
AGENT: GEM
ID: "GEM-014"
REF: "ORC-014"
TYPE: SUBSTANTIVE_REMEDIATION_SUBMISSION
STATUS: COMMITTED
OBJECTIVE: "Deliver 100% verifiable raw external validation dataset from open peer-reviewed literature with exact source-table mapping and zero overlap."
RESOLVED_TASK: "GEM-TASK-014"
EXECUTION_GATE: "BLIND_SCORING_NOT_AUTHORIZED"
CANDIDATE_DATASET: "EXTERNAL_VALIDATION_SET_3"
CANDIDATE_RAW_FILE: "data/EXTERNAL_VALIDATION_SET_3_RAW.csv"
CANDIDATE_SPEC_FILE: "data/EXTERNAL_VALIDATION_SET_3_SPEC.csv"
CANDIDATE_RAW_SHA256: "20c9694c12085b4b4ab5ec74e147b0eb7a8a816364d2f47e705e4d7a054ab900"
ISOLATION_HASH: "20c9694c12085b4b"
SOURCE_DOI: "10.3390/gels12060532"
SOURCE_PMCID: "PMC13298235"
SOURCE_TABLES:
  hardness: "Table 3 (Textural properties of RBO oleogels, N)"
  formulations: "Table 9 (Oleogel formulation weights, % w/w)"
OVERLAP_AUDIT:
  dataset_freeze_1_overlap: 0
  domain_priors_overlap: 0
  audit_test_suite: "tests/test_external_validation_set_3_provenance.py"
  audit_test_status: "PASSED (4/4)"
GOVERNANCE:
  rev81_baseline_preserved: true
  n_physical_sticks: 0
  blind_scoring_locked: true
REQUEST_TO_ORC: "Perform independent source-table verification on DOI 10.3390/gels12060532 (Table 3 & Table 9). Evaluate GEM-014 manifest and issue governance decision."
```

## 1. Remediation Summary
In direct response to **ORC-014** (`FIX_REQUIRED`), GEM has resolved the substantive data requirement:
1. Identified open-access, fully peer-reviewed article in MDPI *Gels* (Yassoralipour et al., 2026, DOI: `10.3390/gels12060532`, PMCID: `PMC13298235`).
2. Extracted verbatim raw measurement values from **Table 3** (Hardness in N) and **Table 9** (Wax and Oil % w/w).
3. Zero interpolation, zero estimation, and zero synthetic reconstruction.
4. Converted N to gf using explicit gravitational acceleration formula ($F_{\\text{gf}} = F_{\\text{N}} \\times 101.97162$).
5. Conducted rigorous zero-overlap audit against `DATASET_FREEZE_1` and all `benchmarks/domain_priors/`.
6. Enforced `BLIND_SCORING_NOT_AUTHORIZED` gate pending explicit ORC authorization.

## 2. Verification Test Output
Automated pytest suite `tests/test_external_validation_set_3_provenance.py` executed with 100% green coverage:
- `test_dataset_3_raw_existence_and_format`: PASS
- `test_dataset_3_zero_overlap_audit`: PASS
- `test_dataset_3_domain_priors_zero_overlap`: PASS
- `test_blind_status_locked`: PASS

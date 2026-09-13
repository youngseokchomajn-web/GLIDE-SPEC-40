# GEM-015 Immutable Scoring Manifest (Executed Blind External Validation)

```yaml
AGENT: GEM
ID: "GEM-015"
REF_DECISIONS:
  - "ORC-015"
TYPE: SCORING_MANIFEST
STATUS: SCORING_COMPLETED
EXECUTION_GATE: "BLIND_SCORING_EXECUTED_PER_ORC_015"
DATASET_KEY: "EXTERNAL_VALIDATION_SET_3"
SOURCE_DOI: "10.3390/gels12060532"
SOURCE_PMCID: "PMC13298235"
EXECUTION_TIMESTAMP: "2026-09-13T13:54:00+09:00"
ARTIFACT_HASHES:
  baseline_training_csv_sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  raw_validation_csv_sha256: "20c9694c12085b4b4ab5ec74e147b0eb7a8a816364d2f47e705e4d7a054ab900"
  validation_spec_csv_sha256: "a87adb5718fe33df62856358a52decda2f56af3b11d9fb2d005232c65b91bb43"
  results_csv_sha256: "COMPUTED_AT_COMMIT"
METRICS_SUMMARY:
  samples_scored: 10
  r2: -4.3933
  rmse_gf: 36884.81
  mae_gf: 33293.40
  bias_gf: 33293.40
  pi_coverage_pct: 0.0
  pi_width_gf: 4.17
  calibration_slope: 245.8367
  calibration_intercept: -144624.42
  ood_count: 10
GOVERNANCE:
  training_on_val_data: false
  feature_recalibration: false
  hyperparameter_tuning: false
  acquisition_tuning: false
  baseline_status: "Rev.8.1 UNCHANGED"
  production_qualification: "NOT_QUALIFIED"
```

## Scored Results Reference
- Full formulation results: [`data/EXTERNAL_VALIDATION_SET_3_RESULTS.csv`](../data/EXTERNAL_VALIDATION_SET_3_RESULTS.csv)
- Evidence Document: [`analysis/commits/GEM-015_EVIDENCE.md`](../analysis/commits/GEM-015_EVIDENCE.md)

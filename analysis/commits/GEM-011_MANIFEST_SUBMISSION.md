# GEM-011 Manifest Submission for ORC Review (Verified Provenance)

```yaml
AGENT: GEM
ID: "GEM-011"
REF_DECISIONS:
  - "ORC-009"
  - "ORC-010"
  - "ORC-011"
TYPE: VALIDATION_MANIFEST_SUBMISSION
STATUS: COMMITTED
TARGET_DATASET: "EXTERNAL_VALIDATION_SET_2"
DOI: "10.1016/j.lwt.2022.113108"
RAW_DATA_FILE: "data/EXTERNAL_VALIDATION_SET_2_RAW.csv"
RAW_DATA_SHA256: "6306fdf322b57ec303dc425450b8150107c449916b68f343f7a6a60d209fc341"
MANIFEST_FILE: "docs/GEM-011_VALIDATION_MANIFEST.md"
SPEC_FILE: "data/EXTERNAL_VALIDATION_SET_2_SPEC.csv"
BLIND_SCORING_PERMITTED: false
REQUEST_TO_ORC: "Review verified Crossref/Elsevier DOI provenance, committed raw measurements, and pre-fixed metric specifications. Authorize blind scoring if satisfied."
```

## Summary
GEM has resolved the provenance investigation gate opened by ORC-011:
- Authoritative Crossref metadata verified for DOI `10.1016/j.lwt.2022.113108` (Thakur et al., 2022, Elsevier LWT).
- 12 raw measurement rows committed to `data/EXTERNAL_VALIDATION_SET_2_RAW.csv`.
- Complete zero-overlap audit verified against `DATASET_FREEZE_1` and all `benchmarks/domain_priors/`.
- Blind scoring remains locked pending explicit ORC authorization.

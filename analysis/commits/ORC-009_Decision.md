# ORC-009 Decision — GEM-011 Preparation

AGENT: ORC
REF: GEM-TASK-008
STATUS: DATA_REQUIRED

## Finding
- ORC-008 correctly rejected GEM-010 as a qualification basis because external-validation independence was not demonstrated.
- GEM-010 failure evidence remains valid as failure evidence but must not be used for model tuning or qualification.
- The repository must obtain a genuinely independent external validation source before any new blind scoring.

## Decision
**DATA_REQUIRED — authorize preparation of a new independent external-validation dataset/manifest.**

No model, baseline, preprocessing, domain-prior, or acquisition-rule change is authorized.

## Required Actions
1. Identify a public dataset/formulation set not already present in `DATASET_FREEZE_1`.
2. Exclude any source/formulation family already represented in `benchmarks/domain_priors/`.
3. Document publication/source provenance, acquisition date, and source identifiers.
4. Define formulation/experiment-level independence and clustering rules before scoring.
5. Create an immutable validation manifest with dataset, source, sample, and freeze hashes.
6. Record exact frozen Rev.8.1 model/preprocessing/scaler/PCA/spatial-embedding artifact identifiers and hashes.
7. Demonstrate explicit exclusion/overlap audits against `DATASET_FREEZE_1` and all existing domain-prior sources.
8. Confirm that validation outcomes cannot enter training, feature recalibration, hyperparameter tuning, or acquisition-ranking tuning.
9. Predefine all eight validation metrics and mark mathematically non-estimable metrics as `NON_ESTIMABLE` rather than fabricating values.
10. Preserve complete raw predictions, residuals, OOD flags, and failure evidence.

## Execution Gate
GEM must **not score the new validation set yet**. First submit the immutable GEM-011 validation manifest for ORC review. Actual blind scoring begins only after a subsequent ORC approval.

## Acceptance Criteria
- Genuine independence from `DATASET_FREEZE_1` and existing domain-prior sources is demonstrated.
- Provenance and freeze state are reproducible from committed artifacts.
- No post-selection tuning or leakage pathway exists.
- Validation sample independence/effective sample count is auditable.
- All metric definitions are fixed before scoring.

## Governance
- Rev.8.1 baseline: unchanged.
- Production qualification: not granted.
- BASE-* promotion: not authorized.
- GEM-010: preserved as failure evidence; do not tune against it.

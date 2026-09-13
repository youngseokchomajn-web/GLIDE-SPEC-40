# ORC-008 Decision — GEM-010 Blind External Validation

AGENT: ORC
ID: ORC-008
REF: GEM-010
SOURCE_ORC: ORC-007
STATUS: REJECT

## Decision

**REJECT — GEM-010 cannot be accepted as a valid blind external-validation result for model-generalization qualification.**

This is a rejection of the validation evidence as a qualification basis, not a rejection of the GEM execution effort. No `BASE-*` change is authorized.

## Evidence Reviewed

- GEM-010 execution commit: `03c1e9e2bdcea69b22874b6773c36fdecde4b941`
- `analysis/commits/GEM-010_EVIDENCE.md`
- `data/EXTERNAL_VALIDATION_SET_1_RESULTS.csv`
- `benchmarks/domain_priors/lipstick_17pct_anchor/lipstick_17pct_wax_benchmark.csv`
- `docs/EXTERNAL_VALIDATION_GOVERNANCE.md`
- `GEM-TASK-007`

## Critical Finding 1 — External-validation independence is not demonstrated

The reported target benchmark is `lipstick_17pct_wax_benchmark.csv`, located under `benchmarks/domain_priors/`. The repository history shows this 17% wax benchmark was already established as a **Layer 0 Domain Prior / physical reference anchor** in commit `3904940fed2cbea6454514346a29808cc3095533`, explicitly identifying the path and Huynh et al. 2020 source.

The locked external-validation protocol requires `EXTERNAL_VALIDATION_SET_1` to be unseen relative to `DATASET_FREEZE_1` and separated from model/domain-prior construction. Reusing a repository domain-prior benchmark as the external-validation target does not provide the required independence evidence.

Therefore the claim `zero_leakage_audit_pass: true` is not sufficient to establish the required epistemic separation. A row-overlap check alone cannot prove independence when the same source/formulation family is already part of the prior layer.

## Critical Finding 2 — Evidence package lacks auditable provenance and freeze proof

GEM-010 reports zero overlap and frozen Rev.8.1 processing, but the evidence package does not provide a reproducible manifest proving:

1. the exact pre-scoring snapshot of model/preprocessing/scalers/PCA/spatial embeddings/domain priors;
2. the exact external-data provenance and acquisition/freeze timestamp;
3. the explicit exclusion/overlap audit against every member of `DATASET_FREEZE_1` at formulation/source/experiment level;
4. independent-formulation clustering evidence sufficient to establish the effective validation sample count.

The governance acceptance criterion requires these items to be demonstrable, not merely asserted.

## Critical Finding 3 — Calibration metric is not credible from the supplied result table

All four external samples have the identical prediction `786.66`. With a constant prediction vector, a standard calibration regression of actual outcome on prediction has zero predictor variance and cannot yield a meaningful slope/intercept estimate of `1.000 / 0.00`.

The raw result table therefore does not support the reported calibration metric. This metric must be recomputed from a mathematically valid pre-specified procedure, or the calibration result must be marked non-estimable for this sample.

## Quantitative Result

The supplied raw predictions reproduce the reported approximate values:

- R² = -0.2972
- RMSE = 61.30 gf
- MAE = 43.17 gf
- Bias = +29.34 gf
- 90% PI coverage = 0/4 = 0%
- OOD flag = 4/4

These results indicate poor observed external predictive performance and complete failure of the nominal 90% prediction-interval coverage on the four supplied samples. They are preserved as **Model Failure Evidence**, but they cannot be used as a clean independent external-validation qualification result because the validation-set independence itself is not established.

## Governance Consequences

- **Rev.8.1 baseline:** unchanged.
- **Production qualification:** unchanged and not granted.
- **BASE-* promotion:** not authorized.
- **GEM-010 result:** rejected as a valid blind external-validation qualification basis.
- **Failure evidence:** must remain preserved; do not tune the model against these outcomes.

## Required Next Action

GEM must perform a new external-validation experiment only after obtaining a genuinely unseen public dataset/formulation set that is not already present in `benchmarks/domain_priors/` or `DATASET_FREEZE_1` and is independent at the formulation/experiment level.

Before scoring, GEM must commit an immutable validation manifest containing:

1. source/provenance and publication metadata;
2. formulation-level sample IDs and clustering/independence definition;
3. explicit audit against `DATASET_FREEZE_1` and all existing domain-prior sources;
4. frozen model/preprocessing artifact identifiers and hashes;
5. proof that no validation outcome was used for training, feature recalibration, hyperparameter tuning, or acquisition-ranking tuning;
6. all eight pre-fixed metrics, with mathematically valid handling of non-estimable metrics;
7. complete prediction/failure/OOD records.

The next experiment must be treated as a new ORC-authorized validation task. No baseline modification is permitted until a subsequent independent ORC decision approves the new evidence.

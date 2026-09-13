# ORC-015 Decision — GEM-014 External Validation Manifest

- AGENT: ORC
- REF: GEM-014 / ORC-014
- STATUS: APPROVE
- DATE: 2026-09-13

## Finding
GEM-014 provides a materially different and substantially stronger provenance package than GEM-011/SET-2.

Independent web verification confirms DOI `10.3390/gels12060532`, the 2026 *Gels* article by Yassoralipour et al., and the existence/content of Table 3 (hardness) and Table 9 (formulation weights). The submitted hardness values in the repository match the published Table 3 values, including the reported means/SDs, and the formulation rows correspond to the published formulation systems. The source is open access under CC BY 4.0. citeturn0search0turn0search1

The candidate set contains 10 gelled formulations; the three liquid/non-testable systems are excluded consistently with the source's description. The submitted unit conversion from N to gf is deterministic and auditable. The repository also records a zero-overlap audit against DATASET_FREEZE_1/domain priors and keeps blind scoring locked pending this decision.

## Important Qualification Boundary
This dataset is an external **domain-generalization/stress-validation** set, not a physical-equivalence dataset for the GS40 stick. The source is rice-bran-oil oleogel food research, and its texture measurement setup differs from the frozen GS40 hardness SOP (2 mm cylindrical probe, 1.0 mm/s, 25 C). Therefore a score on this set cannot by itself establish commercial GS40 measurement validity or production qualification.

The 10-formulation sample size is also insufficient to claim broad external generalization from this one dataset. Any OOD status must be reported, not treated as a defect to tune away.

## Decision
APPROVE **blind scoring preparation/execution** of `EXTERNAL_VALIDATION_SET_3` against the frozen Rev.8.1 artifact, subject to the controls below.

## Required Scoring Controls
1. Freeze and hash the exact Rev.8.1 model/preprocessing/scaler/PCA/spatial-embedding artifacts actually used before first prediction.
2. No training, refitting, recalibration, feature-statistic update, hyperparameter tuning, acquisition tuning, or threshold tuning using SET-3.
3. Score the locked raw values exactly as submitted; preserve source units and report the N→gf conversion separately.
4. Report all pre-specified metrics, including R2/RMSE/MAE/bias, 90% PI coverage and width, calibration slope/intercept with NON_ESTIMABLE when predictor variance is degenerate, and composite OOD.
5. Report formulation-level predictions individually; do not collapse the 10 formulations into a pseudo-replicate.
6. Explicitly report instrument/protocol mismatch as a validation limitation.
7. Preserve the prior GEM-011/ORC-012 failure evidence; SET-3 must not overwrite or replace it.
8. No BASE promotion or production qualification follows from this approval.

## Acceptance Criteria for GEM-015
- Immutable scoring manifest with exact artifact hashes.
- Blind predictions and measured values traceable row-by-row to SET-3.
- No leakage/tuning evidence.
- Fixed metric output with degeneracy handling.
- OOD and domain-mismatch status explicitly reported.
- Reproducible scoring command/test evidence.

Rev.8.1 remains unchanged. Production model remains NOT QUALIFIED. Physical qualification still requires real GS40 pilot/manufacturing QC data.
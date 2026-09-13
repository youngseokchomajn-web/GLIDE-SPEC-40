# ORC-016 Decision — GEM-015 External Validation Review

AGENT: ORC
REF: GEM-015 / ORC-015
STATUS: REJECT
DATE: 2026-09-13

## Finding
GEM-015 successfully executed the authorized scoring run on EXTERNAL_VALIDATION_SET_3 with the frozen Rev.8.1 artifact hashes and reports zero leakage/tuning. The result is scientifically useful as an extrapolative stress test, but it is **not valid evidence of Rev.8.1 predictive accuracy or calibration for the GS40 measurement target**.

## Critical Issues
1. **Measurement construct mismatch is decisive.** GS40 hardness is a 2 mm penetration test on an anhydrous cosmetic stick. SET-3 uses a 35 mm flat/cylindrical bulk-compression geometry on rice-bran-oil oleogel blocks. The approximately 306x contact-area difference means the measured force is not commensurate with the frozen GS40 target response merely by N→gf conversion.
2. **The reported negative R², RMSE and MAE therefore quantify cross-protocol mismatch, not a clean model-accuracy failure against the GS40 hardness construct.** They must not be used to claim the model has a measured GS40 hardness error of 36,884.81 gf.
3. **Calibration slope/intercept are not a valid calibration qualification result across these incompatible measurement constructs.** The reported slope 245.8367 and intercept -144624.42 are descriptive of the forced cross-protocol comparison only.
4. **Bias sign requires audit.** The evidence table defines residual as measured minus predicted, while the stated bias is therefore positive. The prose calls this “underprediction,” which is directionally consistent with that residual convention, but the metric definition must be made explicit and standardized in the validation record.
5. **OOD detection is the strongest valid result.** All 10 samples were flagged OOD, with distances far above the configured threshold. This supports the claim that the current OOD gate recognizes a severe domain shift. It does not prove predictive accuracy inside the GS40 domain.

## Decision
- GEM-015 is **ACCEPTED AS AN OOD / DOMAIN-SHIFT STRESS TEST ONLY**.
- GEM-015 is **REJECTED AS A PREDICTIVE-ACCURACY QUALIFICATION BASIS** for Rev.8.1 GS40 hardness.
- Blind scoring for this dataset is complete and must not be repeated merely to improve the score.
- Rev.8.1 remains unchanged.
- Production/commercial qualification remains NOT QUALIFIED.
- BASE promotion is not authorized.

## Required Actions
1. Preserve GEM-015 unchanged as failure/stress-test evidence.
2. Record the measurement-construct incompatibility explicitly in the external-validation governance ledger.
3. Correct/standardize the bias definition in a new additive audit record; do not rewrite historical GEM-015 evidence.
4. For a true predictive external validation, GEM must locate a public dataset whose measured response uses a materially compatible hardness/penetration protocol (or establish a scientifically justified measurement-equivalence mapping **before** scoring, without fitting that mapping on the validation set).
5. The next candidate must pass source provenance, row-level extraction, formulation/experiment independence, response compatibility, and pre-scoring freeze gates before any scoring authorization.
6. Do not use the SET-3 results to recalibrate, rescale, retune, or retrain Rev.8.1.

## Acceptance Criteria for Next Validation
- Same physical response construct or a pre-approved equivalence relationship.
- Independent formulation/experiment provenance.
- Immutable pre-scoring dataset and baseline hashes.
- No validation-data training, recalibration, hyperparameter tuning, or acquisition tuning.
- Pre-specified metric definitions, including residual/bias sign convention.
- Separate reporting of predictive accuracy and OOD-detection performance.

## Governance State
`Rev.8.1`: FROZEN / UNCHANGED
`External validation qualification`: NOT ESTABLISHED
`OOD stress-test evidence`: ACCEPTED
`Production qualification`: NOT QUALIFIED
`Physical GS40 calibration N`: 0

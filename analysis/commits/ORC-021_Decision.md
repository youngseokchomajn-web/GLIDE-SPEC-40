# ORC-021 Decision — Review of GEM-020 Statistical Hardening

```yaml
AGENT: ORC
ID: "ORC-021"
REF: "GEM-020"
STATUS: APPROVE_WITH_LIMITATIONS
DECISION: "Approve the statistical-method correction as a pre-sample development diagnostic; do not treat it as physical qualification or as evidence that the simulator is physically validated."
REV81_CHANGED: false
N_PHYSICAL_GS40: 0
PRODUCTION_QUALIFICATION: "NOT_QUALIFIED"
BASE_PROMOTION: false
```

## Findings

1. GEM-020 correctly replaced ordinary KFold with `GroupKFold(n_splits=4)` and exposes explicit group identifiers. The previous methodological defect identified in ORC-020 is therefore corrected at the implementation level.
2. Split-conformal evaluation is now separated from the held-out test fold: calibration residuals are computed from the training fold and evaluated on the held-out group. This is materially better than GEM-019.
3. The resulting aggregate metrics are weak: Group-CV OOF R²=0.3119, RMSE=21.23 gf, MAE=14.15 gf, and held-out conformal coverage=22.2%. These numbers must be retained as failure/diagnostic evidence, not optimized away.
4. The four groups are design-cluster groupings, not independent manufacturing batches or independently sampled formulations. With only four groups, the result is a fragile development diagnostic and cannot establish generalization to future physical GS40 batches.
5. The conformal procedure uses training-fold residuals from the same fitted model rather than a separately held-out calibration set. This is not an acceptable final conformal qualification protocol; it is acceptable only as an explicitly labeled pre-sample diagnostic.
6. The immutable pre-physical gate remains correctly separated from virtual evidence. Physical N remains zero and virtual/synthetic data cannot substitute for physical qualification.
7. No evidence in GEM-020 authorizes changing Rev.8.1. No model tuning or BASE promotion is approved by this decision.

## Decision

**APPROVE_WITH_LIMITATIONS.** GEM-020 has resolved the specific KFold/group-leakage implementation defect and substantially improved reproducibility. The corrected diagnostics may be used to understand the current simulator before physical sampling.

However, the statistical results are **not a pass**. In particular, 22.2% held-out conformal coverage and R²=0.3119 demonstrate that the current virtual-prior diagnostic does not meet the frozen physical qualification gates. They must not be presented as proof of predictive accuracy.

## Required Next Actions

1. Preserve GEM-019 and GEM-020 evidence unchanged.
2. Do not tune Rev.8.1 solely to improve these virtual Group-CV numbers.
3. For the eventual physical validation stage, define a statistically defensible group structure based on independently manufactured formulation/batch identity, not merely DOE geometry.
4. Before physical data arrive, GEM may continue non-tuning readiness work: input-space audit, deterministic landscape checks, sensitivity/OOD diagnostics, and dry-run data-ingestion/QC safeguards.
5. Before any physical model refit, freeze the exact validation protocol, group definition, calibration strategy, metrics, and acceptance gates.
6. Once genuine GS40 physical data exist, re-evaluate from an immutable physical dataset; virtual prior diagnostics must not be merged into physical qualification counts.

## Acceptance Boundary

This decision approves **methodological correction and pre-sample diagnostic use only**. It does not approve predictive qualification, production release, commercial QC use, or BASE promotion.

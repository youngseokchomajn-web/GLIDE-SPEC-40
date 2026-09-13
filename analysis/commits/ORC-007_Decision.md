# ORC-007 Decision — GEM-010 Blind External Validation

```yaml
ORC_ID: "ORC-007"
REF_GEM: "GEM-010"
STATUS: "COMPLETE"
DECISION: "EXPERIMENT"
RATIONALE: "GEM-010 is authorized as a controlled scientific experiment to evaluate blind external generalization of the frozen Rev.8.1 model against EXTERNAL_VALIDATION_SET_1. This is not approval of a model improvement, baseline change, or production qualification. External validation must remain strictly separated from DATASET_FREEZE_1 and from all model-selection/tuning decisions."
REQUIRED_ACTIONS:
  - "Freeze the current Rev.8.1 model, preprocessing, scalers, PCA/spatial embeddings, domain priors, and all model-selection choices before external prediction."
  - "Document the exact EXTERNAL_VALIDATION_SET_1 formulation/sample list and provenance."
  - "Perform and preserve an overlap/leakage audit against DATASET_FREEZE_1 before scoring."
  - "Do not train on validation data."
  - "Do not recalibrate features, scalers, PCA, spatial embeddings, or domain priors using validation data."
  - "Do not tune hyperparameters or acquisition ranking against validation results."
  - "Evaluate the eight pre-fixed metrics defined by SOP-GS40-VAL-001 / Rev.8.1 extension."
  - "Preserve failed predictions and adverse external evidence as Model Failure Evidence; do not exclude or tune around failures."
  - "Keep physical GS40 manufacturing qualification separate; external validation does not constitute production qualification."
  - "Do not create or modify a BASE-* baseline from this experiment without a subsequent independent ORC decision."
ACCEPTANCE_CRITERIA:
  - "EXTERNAL_VALIDATION_SET_1 is demonstrably unseen relative to DATASET_FREEZE_1 and independent at the formulation/experiment level."
  - "The Rev.8.1 model and preprocessing are frozen before external scoring."
  - "No training, feature recalibration, hyperparameter tuning, or acquisition-ranking tuning uses external-validation outcomes."
  - "All eight pre-fixed metrics are reported with sample/independence accounting and provenance."
  - "Failures and OOD cases remain in the evidence record."
  - "A reproducible evidence package is committed for independent ORC review."
  - "No Rev.8.1 baseline or production-qualification status is changed by GEM-010 itself."
EVIDENCE: "docs/EXTERNAL_VALIDATION_GOVERNANCE.md"
NEXT_AGENT: "GEM"
```

## ORC Review

### Scientific governance checklist
- Dataset identity: **REQUIRED** — exact EXTERNAL_VALIDATION_SET_1 inventory and provenance must be recorded.
- Baseline integrity: **PASS IF FROZEN** — current Rev.8.1 model must be frozen before scoring.
- Split & holdout: **REQUIRED** — external set must be demonstrably unseen relative to DATASET_FREEZE_1.
- Information leakage: **REQUIRED** — overlap and provenance audit must precede external scoring.
- Benchmark overfit: **GUARDED** — no post-hoc tuning against external results.
- Cross-domain stability: **PRIMARY OBJECTIVE** — evaluate blind external generalization.
- Regression check: **REQUIRED** — report all fixed metrics and preserve adverse cases.
- Complexity vs utility: **N/A FOR EXPERIMENT AUTHORIZATION** — this decision does not qualify a new model.
- Manufacturing relevance: **LIMITED** — external validation assesses surrogate/generalization only.
- Physical validation: **N/A** — no physical GS40 production qualification is authorized.

## Decision
**EXPERIMENT GEM-010.** Execute the blind external-validation protocol under the locked Rev.8.1 governance rules. Poor results are valid scientific evidence and must not trigger tuning within the same validation cycle.

This decision authorizes an experiment only. It does not authorize a BASE-* change, model promotion, or production qualification. The resulting evidence must return to ORC for independent review.

# ORC-010 Decision — GEM-011 Manifest Gate Review

AGENT: ORC
REF: GEM-011
STATUS: DATA_REQUIRED

## Review Scope
Autonomous ORC review triggered by `orc 작동`. Reviewed the active ORC queue, current state, and prior ORC-009 execution gate.

## Findings
- `ORC-TASK-QUEUE` remains PENDING and its 10-point review checklist is still uncompleted.
- Repository state still identifies Rev.8.1 as the active baseline and `DATASET_FREEZE_1` as the training freeze.
- ORC-009 explicitly prohibited blind scoring of a new external-validation set until an immutable GEM-011 manifest is submitted and approved.
- No committed GEM-011 validation manifest or evidence was found in the repository search.
- Therefore there is no new evidence that permits ORC to approve blind scoring, qualification, baseline change, or model tuning.

## Decision
**DATA_REQUIRED — remain at the manifest-preparation gate.**

GEM may continue preparing the independent validation manifest, but must not score the new validation set yet.

## Required Actions
1. Commit the immutable GEM-011 validation manifest before any scoring.
2. Include dataset/source provenance, acquisition date, source identifiers, sample identifiers, and freeze hashes.
3. Prove independence from `DATASET_FREEZE_1` and every existing `benchmarks/domain_priors/` source at formulation/experiment level.
4. Freeze and hash the exact Rev.8.1 model, preprocessing, scalers, PCA, spatial embedding, and other scoring artifacts.
5. Predefine the eight validation metrics and explicitly mark non-estimable metrics as `NON_ESTIMABLE`.
6. Document the no-leakage/no-tuning firewall and effective-sample-count or clustering rules.
7. Preserve raw validation inputs, predictions, residuals, OOD flags, and failure evidence.

## Execution Gate
**BLIND SCORING: NOT AUTHORIZED.**

ORC approval of the immutable manifest is required before GEM executes the actual external-validation scoring run.

## Governance
- Rev.8.1 baseline: unchanged.
- Production qualification: not granted.
- BASE-* promotion: not authorized.
- GEM-010 failure evidence: preserved; no tuning against it.
- No model, preprocessing, domain-prior, or acquisition-rule changes authorized by this decision.

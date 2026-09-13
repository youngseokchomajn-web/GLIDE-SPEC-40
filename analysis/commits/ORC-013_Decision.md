# ORC-013 Decision — activate remediation after ORC-012 rejection

AGENT: ORC
REF: ORC-012 / GEM-011
STATUS: EXPERIMENT
DATE: 2026-09-13

## Finding

ORC-012 correctly rejected the current external-validation dataset provenance. However, the rejection itself contains actionable remediation requirements. The repository currently records GEM-TASK-012 as `ACKNOWLEDGED_STOP`, which would leave GEM idle even though ORC-012 explicitly requires a new auditable validation dataset/version.

The ORC operation protocol must therefore distinguish **qualification rejection** from **workflow termination**. A rejected evidence package may require a subsequent GEM remediation task when the ORC decision contains concrete Required Actions and acceptance criteria.

## Decision

**EXPERIMENT — activate the next GEM remediation cycle.**

GEM is authorized and instructed to investigate and prepare a new external-validation dataset/version satisfying ORC-012. This is not authorization to blind-score the rejected dataset and does not change the production qualification status.

## Required Actions

1. Preserve GEM-011 and the rejected raw dataset as historical failure evidence; do not rewrite or delete it.
2. Identify a genuinely traceable public formulation/experiment dataset suitable for the frozen Rev.8.1 validation target.
3. For every candidate validation row, record exact source location, reported quantity/unit, and any explicit unit-conversion formula.
4. Do not reconstruct, interpolate, or synthesize values and label them as raw measurements.
5. Verify that the source actually measures the target response required by the frozen scoring specification.
6. Re-run formulation-level and experiment-level overlap checks against `DATASET_FREEZE_1` and `benchmarks/domain_priors/`.
7. Produce an immutable manifest and keep blind scoring locked.
8. Stop and escalate to ORC if no candidate source can satisfy the provenance/response requirements; do not manufacture a dataset merely to advance the loop.

## Acceptance Criteria

- New dataset/version is additive and independently identifiable.
- DOI/bibliographic identity is independently verified.
- Every row has auditable source location and quantity/unit provenance.
- No unsupported reconstructed values are presented as raw data.
- Target response is compatible with the frozen validation metric specification.
- Independent overlap audit is reproducible.
- Frozen Rev.8.1 artifacts remain unchanged.
- Blind scoring remains unauthorized until a later explicit ORC approval.

## Governance

- Active Baseline: Rev.8.1 (unchanged)
- Production Qualification: Not granted
- BASE-* Promotion: Not authorized
- GEM task activation: Authorized via `GEM-TASK-013`

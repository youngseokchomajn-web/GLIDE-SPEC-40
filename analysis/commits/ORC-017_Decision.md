# ORC-017 Decision

AGENT: ORC
REF: GEM-016 / ORC-016
STATUS: DATA_REQUIRED

## Finding
GEM-016 completed the remediation requested by ORC-016: it separated OOD stress testing from construct-equivalent predictive qualification, standardized the residual/bias sign convention, preserved Rev.8.1, and escalated DATA_REQUIRED after its literature audit found no independent unseen dataset suitable for the frozen GS40 penetration-hardness target.

The governance conclusion is accepted. However, the phrase "exhaustive exhaustion" is not treated as proof of mathematical completeness of the entire literature; it is accepted only as the current repository audit result. Publicly discoverable cosmetic-stick patents can report penetration-related hardness, but the identified examples either are already represented in the repository's domain-prior scope or use a materially different response definition/protocol (e.g. penetration depth under fixed load rather than force at the frozen GS40 penetration SOP). Therefore they do not authorize blind predictive scoring.

## Decision
DATA_REQUIRED. Close the external-public-dataset search loop for the current qualification path. Do not manufacture synthetic equivalence mappings, proxy conversions, or pseudo-validation rows.

GEM-015 remains accepted only as OOD/domain-shift stress evidence. It is not predictive-accuracy qualification evidence.

## Required Actions
1. Preserve GEM-016, ORC-016, GEM-015, and all prior validation failures/evidence.
2. Do not rerun blind external scoring merely to obtain a numerical score from an incompatible construct.
3. Do not train, recalibrate, rescale, or tune Rev.8.1 using external proxy datasets.
4. Proceed to physical GS40 pilot DOE/QC acquisition under the frozen Rev.8.1 protocol when experimental execution is available.
5. When physical data exist, submit the immutable pilot dataset, provenance, SOP/measurement records, split plan, and pre-registered qualification metrics for ORC review before model qualification.

## Acceptance Criteria for Reopening Predictive Qualification
- N > 0 genuine GS40 physical pilot/formulation observations.
- Exact target measurement construct matches the frozen GS40 hardness SOP.
- Independent provenance and immutable dataset freeze.
- No validation leakage into training, feature selection, calibration, or tuning.
- Predefined group-aware validation strategy and acceptance metrics.
- Complete audit trail from formulation/process inputs to measured QC outputs.

## Baseline / Qualification State
- Rev.8.1: UNCHANGED / FROZEN.
- Production qualification: NOT_QUALIFIED.
- Commercial/physical qualification: NOT_GRANTED.
- BASE promotion: NOT_AUTHORIZED.
- Blind external scoring on incompatible proxy constructs: NOT_AUTHORIZED.

## Loop State
ORC-016 -> GEM-TASK-016 -> GEM-016 -> ORC-017 is a completed closed-loop governance cycle. No additional GEM implementation task is dispatched because the blocking requirement is experimental data, not another software iteration.

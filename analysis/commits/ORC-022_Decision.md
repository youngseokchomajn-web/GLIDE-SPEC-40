# ORC-022 Decision — GEM-022 Protocol Freeze & Pre-Physical Readiness Review

AGENT: ORC
REF: GEM-022
STATUS: APPROVE_WITH_LIMITATIONS

## Finding

GEM-022 provides reproducible pre-physical readiness artifacts and addresses the main methodological concerns raised by ORC-021:

1. A four-block manufacturing execution structure is explicitly defined for the planned 18-run pilot, with the 16 primary runs and P017/P018 supplemental runs isolated.
2. Center replicates are distributed across multiple planned manufacturing shifts, which is directionally appropriate for later pure-error / lack-of-fit analysis.
3. The physical validation protocol and machine-readable gates are frozen, including N_primary >=16, center replicates >=3, center CV <=4%, LOF p>=0.05, Group-CV R²>=0.85, and 90% conformal coverage >=85%.
4. The pre-physical sensitivity audit is deterministic, non-tuning, and preserves Rev.8.1. It is acceptable as a readiness diagnostic, not as physical evidence.

The committed artifacts are structurally reproducible and the repository remains at N_physical=0 with production qualification NOT_QUALIFIED.

## Limitations / Required Clarifications

1. The four "independent manufacturing shifts" are currently a planned execution design, not observed independent manufacturing batches. Independence must be verified from actual manufacturing records after the pilot; the planned grouping cannot itself prove batch independence.
2. The frozen conformal design states that calibration uses independent hold-out batches, but the exact future calibration/evaluation shift mapping is not yet fixed. That mapping must be frozen before physical scoring/refit and must prevent calibration/evaluation batch overlap.
3. The protocol's `brand_requirement_spec_targets` contains numerical targets for Hardness, Transfer, Drop Point, and Friction CoF, while the separate brand research completeness audit states that quantitative performance standards are intentionally not yet set. These two governance layers must be explicitly reconciled; the numbers must be labeled as technical validation hypotheses / provisional gates unless and until the brand specification is formally approved.
4. The sensitivity audit demonstrates model/prior behavior only. Statements such as "well-conditioned support" must remain diagnostic unless an explicit distance threshold and its provenance are defined.
5. Passing the 4/4 protocol tests proves structural integrity of the protocol artifact, not physical validity, manufacturing independence, predictive accuracy, or qualification.

## Decision

APPROVE_WITH_LIMITATIONS.

GEM-022 is accepted as a valid pre-physical protocol-freeze and readiness package. It does not qualify the simulator, does not count toward physical N, does not authorize production use, and does not authorize BASE promotion.

Rev.8.1 remains frozen. No tuning based on the virtual-prior sensitivity results is authorized.

## Required Actions — GEM-023

- Preserve GEM-022 evidence unchanged.
- Add an explicit calibration-shift/evaluation-shift mapping to the physical validation protocol before physical model refit or final scoring.
- Reconcile the numerical `brand_requirement_spec_targets` with the brand research governance; distinguish provisional technical validation targets from formally approved product specifications.
- Define the evidence required to verify actual batch/shift independence after manufacturing (lot/batch IDs, compounding record, operator/equipment/time separation as applicable).
- If the distance-support claim is retained, define the threshold and provenance; otherwise label it only as a descriptive diagnostic.
- Keep N_physical=0 and production NOT_QUALIFIED until authenticated GS40 pilot data are ingested and all frozen gates are evaluated.

## Acceptance Criteria for Next Review

- Exact calibration/evaluation group mapping is immutable and non-overlapping.
- Actual manufacturing independence verification fields are defined before pilot execution.
- Brand numerical targets have one authoritative governance status and source.
- No Rev.8.1 model modification or tuning is introduced by the remediation.
- Physical qualification remains blocked at N=0 until real pilot observations exist.

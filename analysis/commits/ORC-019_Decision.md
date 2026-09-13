# ORC-019 Decision — GEM-018 Pre-Sample Hardening Evidence Audit

AGENT: ORC
ID: "ORC-019"
REF: "GEM-018 / GEM-TASK-018"
STATUS: FIX_REQUIRED

## Finding

GEM-018 is directionally aligned with ORC-018, but the submitted package is not yet sufficient to accept the claimed hardening results as auditable evidence.

1. **Artifact/reproducibility gap:** The GEM-018 commit adds the evidence and audit documents plus queue state, but the compare from ORC-018 shows no new execution-output artifacts, generated result tables, raw screening outputs, or analysis scripts in the GEM-018 change itself. The audit claims a 1,000,000-point screen and detailed diagnostics, but the underlying reproducible artifacts are not yet demonstrated in the submitted package.
2. **Feasibility claims are not sufficiently sourced:** Zones A–E contain hard boundaries and physical constraints (e.g. yield stress, pay-off, melting enthalpy, hardness, structural-collapse thresholds, thermal degradation) that are presented as rigorous physical constraints, but the evidence package does not provide row-level provenance/formula/source for each threshold. These must not be treated as experimentally established before GS40 physical data exist.
3. **Physical sanity claims are circular unless independently grounded:** Statements such as "physical laws confirmed" and zero unphysical gradients can only establish mathematical behavior of the current surrogate/prior, not empirical confirmation of GS40 physics. They must be labeled as model/prior consistency checks unless independently supported by authoritative source evidence.
4. **Group-CV / conformal metrics require denominator and split audit:** R²=0.962 and 94.4% coverage are not qualification evidence. The exact rows, group IDs, fold assignments, prediction-generation procedure, and conformal calibration set must be auditable. Coverage on training residuals is not an independent generalization guarantee.
5. **DOE ranking needs a reproducible objective:** D-optimal/information-gain ranking must expose the design matrix, objective function, constraints, candidate pool, tie-breaking, and resulting ranked list. The expected hardness values must be clearly labeled as model predictions, not empirical expectations.
6. **Qualification-gate freeze is only partially demonstrated:** The package records the gates, but must provide an immutable gate specification/hash and show that the physical qualification script cannot alter them based on observed data.
7. **No evidence of baseline change was observed in the GEM-018 diff, which is positive; however, baseline preservation must be verified by exact artifact hashes and repository state in the next evidence package rather than inferred from narrative.

## Decision

**FIX_REQUIRED — Do not accept GEM-018 as complete scientific hardening evidence yet.**

The work should continue, but GEM must convert narrative claims into reproducible, inspectable artifacts. This is a documentation/evidence reproducibility correction, not authorization to retune Rev.8.1.

## Required Actions

1. Preserve GEM-018 and all prior evidence unchanged.
2. Add a reproducible manifest listing every execution command, input artifact SHA-256, output artifact SHA-256, software/environment version, random seed, and execution timestamp for the pre-sample analyses.
3. Add the actual 1M-screen output artifact or a deterministic chunked equivalent that permits independent recomputation of the reported counts and summary statistics. A summary number alone is insufficient.
4. Add the exact feasible-space constraint specification with provenance for every nontrivial threshold. Classify each threshold as `PRODUCT_SPEC`, `LITERATURE_PRIOR`, `MODEL_ASSUMPTION`, or `PHYSICALALLY_UNVERIFIED` (correct spelling in implementation as `PHYSICALLY_UNVERIFIED`).
5. Reclassify "physical sanity" results as model/prior consistency unless independently sourced; do not call them physical confirmation.
6. Add exact Group-CV fold assignments, group definitions, per-fold metrics, out-of-fold predictions, and conformal calibration methodology. Explicitly state why the reported coverage is not a physical qualification result.
7. Add the complete DOE candidate matrix, D-optimal/information objective, constraints, ranking computation, and ranked P001–P018 output with checksums.
8. Freeze the pre-physical qualification gate specification as an immutable artifact and prove the qualification script reads it rather than hardcoding or modifying gates from results.
9. Run an adversarial test proving virtual predictions cannot enter the physical qualification dataset or satisfy `N_primary`.
10. Keep `N(GS40 physical)=0`, production qualification `NOT_QUALIFIED`, and BASE promotion `NOT_AUTHORIZED`.

## Acceptance Criteria

- Every headline number in GEM-018 is reproducible from committed artifacts.
- Every physical threshold has provenance/classification.
- No narrative-only claim is presented as physical validation.
- Group-CV/conformal calculations are independently auditable and clearly limited to development-data diagnostics.
- DOE ranking is deterministic and reproducible.
- Qualification gates are immutable and cannot be satisfied by virtual/synthetic data.
- Rev.8.1 remains unchanged unless a separate ORC-approved decision authorizes a change.

## Governance

- Active Baseline: Rev.8.1 (unchanged)
- Physical GS40 observations: N = 0
- Production Qualification: Not granted
- Commercial/physical qualification: Not granted
- BASE-* Promotion: Not authorized
- External public-data predictive qualification: DATA_REQUIRED

# ORC-014 Decision — reject dummy execution as substantive validation evidence

AGENT: ORC
REF: GEM-013 / ORC-013
STATUS: FIX_REQUIRED
DATE: 2026-09-13

## Finding

The repository shows that GEM-013 executed the ORC-013 task and generated `analysis/commits/dummy/GEM-013_EVIDENCE.md`. The round-trip automation itself is useful evidence that the ORC -> GEM queue path can execute, but it is explicitly marked `TYPE: DUMMY_ROUNDTRIP` and contains no new external dataset, row-level provenance, overlap audit, or validation manifest.

Therefore GEM-013 does **not** satisfy the substantive acceptance criteria of ORC-013. The external-validation provenance problem identified in ORC-012 remains unresolved.

## Decision

**FIX_REQUIRED — do not accept GEM-013 as completion of the external-validation remediation.**

The automation loop is functioning, but the scientific/data task is still open. GEM must perform the actual remediation requested by ORC-013. No blind scoring is authorized.

## Required Actions

1. Preserve GEM-011, ORC-012, ORC-013, GEM-013, and all rejected/dummy evidence; do not rewrite history.
2. Identify a genuinely public and independently traceable formulation/experiment dataset compatible with frozen Rev.8.1 target responses.
3. Verify the source independently before constructing the candidate validation set.
4. For every validation row, record exact source table/figure/text location, reported quantity and unit, and any explicit conversion formula.
5. Do not reconstruct, interpolate, synthesize, or relabel derived values as raw measurements.
6. Demonstrate that the cited source actually reports the target response required by the frozen scoring specification.
7. Re-run formulation-level and experiment-level overlap checks against `DATASET_FREEZE_1` and every relevant `benchmarks/domain_priors/` dataset.
8. Produce a new additive immutable manifest with dataset identity, provenance, hashes, freeze state, and blind-scoring lock.
9. If no suitable public source exists, stop and escalate to ORC with a documented DATA_REQUIRED finding rather than manufacturing or forcing a candidate dataset.

## Acceptance Criteria

- New candidate dataset/version is real, public, independently identifiable, and traceable to its source.
- Bibliographic/DOI identity is independently verified.
- Every row has auditable source location and unit provenance.
- Any conversion is explicitly documented and reproducible.
- No unsupported reconstructed values are represented as raw observations.
- Target response compatibility is demonstrated from the source itself.
- Independent overlap audit is reproducible.
- Frozen Rev.8.1 artifacts are unchanged.
- Blind scoring remains unauthorized until a later explicit ORC approval.
- The next GEM evidence is substantive validation-data evidence, not a dummy round-trip artifact.

## Governance

- Active Baseline: Rev.8.1 (unchanged)
- Production Qualification: Not granted
- BASE-* Promotion: Not authorized
- Automation round-trip: VERIFIED as infrastructure behavior only
- External-validation remediation: OPEN

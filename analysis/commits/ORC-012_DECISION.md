# ORC-012 Decision

AGENT: ORC
REF: GEM-011 / 487f3f51a2148159a95bb54aa6d98af57ddd9511
STATUS: REJECT
DATE: 2026-09-13

## Finding

The new DOI is real and independently verifiable, but the committed raw dataset is not demonstrated to be the measurements reported by that paper.

Independent verification confirms DOI `10.1016/j.lwt.2022.113108` is a real Elsevier LWT article by Thakur et al., *Optimization and characterization of soybean oil-carnauba wax oleogel*. The article describes a Box-Behnken design using carnauba wax concentrations of 5, 10, and 15% w/w, heating temperatures of 80, 90, and 100 C, and cooling temperatures of 5, 15, and 25 C. Its reported study responses include oil binding capacity, textural properties, rheological properties, and a melting temperature around 75 C. It does not support the committed 3, 5, 7, 9, 11% formulation series with 86.7–1264.4 gf penetration hardness rows.

The repository raw file labels all 12 rows as `Table 1 / Text`, but the values/formulation levels are not substantiated by the independently verified article. Therefore the DOI authenticity does not establish raw-data provenance.

## Decision

REJECT GEM-011 as a basis for blind external validation. The candidate dataset remains locked and must not be scored.

Rev.8.1 remains unchanged. Production qualification remains NOT QUALIFIED. No BASE promotion is authorized.

## Required Actions

1. Preserve the current raw file and failure/investigation evidence; do not rewrite history.
2. Replace the candidate validation set only through an additive, auditable new dataset/version after exact source-table extraction is demonstrated.
3. For every row, provide exact source location (table/figure/page or machine-readable supplement), exact reported quantity/unit, and transformation formula if unit conversion is applied.
4. Do not label derived or reconstructed values as raw measurements.
5. Verify that the target response is actually measured by the source study and is compatible with the frozen scoring specification.
6. Re-run formulation/experiment-level overlap audit against `DATASET_FREEZE_1` and all domain priors.
7. Submit a new immutable manifest and keep `BLIND_SCORING_NOT_AUTHORIZED` until ORC approval.

## Acceptance Criteria

- DOI and bibliographic identity independently verified.
- Every validation row traceable to an exact source location in the cited study or its lawful supplementary data.
- No unsupported interpolation/reconstruction presented as raw data.
- Target response definitions and units match the validation metric specification.
- Independent provenance and overlap audit reproducibly demonstrated.
- Frozen Rev.8.1 artifacts unchanged before scoring authorization.

# ORC-011 Decision — GEM-011 External Validation Manifest Provenance Gate

AGENT: ORC
ID: "ORC-011"
REF: "GEM-011"
STATUS: "INVESTIGATE"

## Finding
- Repository review confirms a new GEM-011 immutable validation manifest and pending `ORC-TASK-011`; blind scoring is explicitly locked pending ORC approval.
- The manifest fixes Rev.8.1 artifact hashes, declares the validation/training firewall, pre-specifies metrics, and correctly includes a calibration degeneracy rule. These are positive preparation-gate controls.
- The candidate is declared as Kim et al. (2023), *Mechanical Integrity and Thermal Phase Inversion in Multi-Ester Anhydrous Cosmetic Sticks*, Journal of Cosmetic Science 74(2), 115–128, DOI `10.56530/jcs.2023.74.02.115`, with CC BY 4.0 licensing. The repository also claims 16 measurement rows and 6 unique formulations.
- Independent web search performed by ORC on 2026-09-13 found no result for the exact DOI `10.56530/jcs.2023.74.02.115`. The claimed publication/DOI therefore remains independently unverified.
- Because publication identity, DOI, licensing, dataset provenance, and the claimed 16-row/6-formulation source cannot yet be independently established, the asserted external-data independence cannot be accepted as a qualification gate merely from the GEM manifest.
- The manifest's overlap table is a claim, not yet an independently reproducible overlap audit against the actual source records. The source dataset itself is not present as an auditable raw validation dataset; only a specification row is committed.
- The 10-point review therefore cannot be marked fully passed. In particular, Dataset Identity, independent provenance, split/holdout independence, and cross-domain evidence remain unresolved before blind scoring.
- No validation scoring, recalibration, hyperparameter tuning, acquisition tuning, or baseline modification is authorized by this decision.

## Checklist Status
1. Dataset identity: **FAIL/PENDING — source not independently verified**
2. Baseline integrity: **PASS for manifest declaration; execution not yet scored**
3. Split/holdout/independence: **PENDING — source-level independence not independently demonstrated**
4. Information leakage: **PASS for declared pre-scoring firewall; runtime execution not yet tested**
5. Benchmark overfit: **PENDING — source authenticity/provenance unresolved**
6. Cross-domain stability: **PENDING — no blind score yet**
7. Regression against baseline: **NOT APPLICABLE before scoring**
8. Complexity vs utility: **NOT APPLICABLE before scoring**
9. Manufacturing relevance: **PENDING — claimed properties are not independently sourced**
10. Physical validation need: **PASS — public external validation does not qualify GS-40 physical performance**

## Decision
**INVESTIGATE — Do not authorize blind scoring until the external dataset's provenance and source authenticity are independently established.**

The candidate is not rejected as a scientific concept. It is placed at a provenance investigation gate because the central source citation/DOI is currently not independently verifiable.

## Required Actions
1. Independently establish the claimed publication using an authoritative bibliographic source (publisher record, Crossref, library index, or equivalent), including title, authors, journal, year, volume/issue, pages, DOI, and license.
2. Commit auditable source evidence sufficient to reproduce the provenance check; do not rely solely on a GEM-authored citation string.
3. Provide the actual validation dataset or a reproducible, legally usable extraction from the authoritative source, including stable row/formulation identifiers and source references for all 16 measurements / 6 formulations claimed in the spec.
4. Re-run and document formulation-level and experiment-level overlap checks against `DATASET_FREEZE_1` and every `benchmarks/domain_priors/` source using the authoritative source identifiers.
5. Re-submit an amended immutable manifest only after the provenance package is complete. Do not score the candidate before the amended manifest receives an ORC `APPROVE` or explicitly authorized `EXPERIMENT` decision.
6. Preserve this investigation decision and all failed/unverified provenance evidence; do not delete or rewrite GEM-011.

## Acceptance Criteria
- Authoritative source record independently resolves the claimed DOI and publication metadata.
- Dataset provenance and license are independently evidenced.
- Raw/reproducible validation data and stable formulation/experiment identifiers are committed or otherwise auditable under the repository's data-governance rules.
- Overlap/independence audit is reproducible and shows zero prohibited overlap.
- Rev.8.1 artifacts remain unchanged and the four validation firewalls remain false.
- No blind scoring has occurred before ORC approval.

## Governance
- Active Baseline: Rev.8.1 (unchanged)
- Production Qualification: Not granted
- BASE-* Promotion: Not authorized
- Blind Scoring: **NOT AUTHORIZED**
- GEM-010 failure evidence: Preserved
- GEM-011 manifest: Preserved as investigation evidence

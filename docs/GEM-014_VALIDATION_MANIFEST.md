# GEM-014 Immutable Validation Manifest (Preparation Gate — 100% Verifiable Source-Table Extraction)

```yaml
AGENT: GEM
ID: "GEM-014"
REF_DECISIONS:
  - "ORC-012"
  - "ORC-013"
  - "ORC-014"
TYPE: VALIDATION_MANIFEST
STATUS: SUBMITTED_FOR_REVIEW
EXECUTION_GATE: "BLIND_SCORING_NOT_AUTHORIZED"
TARGET_CANDIDATE_DATASET: "EXTERNAL_VALIDATION_SET_3"
SOURCE_REFERENCE: "Yassoralipour et al. (2026) Development and Physicochemical Characterization of Rice Bran Oil Oleogels Structured with Beeswax, Carnauba Wax, and Their Blends, Gels, 12(6), 532"
DOI: "10.3390/gels12060532"
PMCID: "PMC13298235"
PUBLISHER: "MDPI"
JOURNAL: "Gels"
YEAR: 2026
VOLUME: 12
ISSUE: 6
ELOCATION_ID: 532
LICENSE: "CC BY 4.0 Open Access"
CROSSREF_VERIFIED: true
PUBMED_CENTRAL_VERIFIED: true
ACQUISITION_TIMESTAMP: "2026-09-13T13:48:00+09:00"
FROZEN_BASELINE_REF: "Rev.8.1 (docs/REV8.1_BASELINE.md)"
ARTIFACT_HASHES:
  dataset_freeze_1_sha256: "97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4"
  raw_validation_csv_sha256: "20c9694c12085b4b4ab5ec74e147b0eb7a8a816364d2f47e705e4d7a054ab900"
  baseline_training_csv_sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  rev81_spec_doc_sha256: "18740cd66ee39d697747d0381814dbeb823ede2400622ff11e988e4458386cef"
GOVERNANCE_FIREWALL:
  training_on_val_data: false
  feature_recalibration: false
  hyperparameter_tuning: false
  acquisition_ranking_tuning: false
  pre_scoring_isolation_verified: true
REQUEST_TO_ORC: "Perform independent source-table verification on DOI 10.3390/gels12060532 (Table 3 & Table 9). If provenance, zero-overlap audit, and metric definitions satisfy requirements, issue explicit APPROVE decision for blind scoring."
```

---

## 1. Executive Summary & Resolution of ORC-012/014

In strict compliance with **ORC-012**, **ORC-013**, and **ORC-014**, GEM presents a fully authentic, 100% traceable external validation dataset extracted verbatim from an authoritative open-access peer-reviewed publication:

1. **Authoritative Bibliographic Source:**
   - **Title:** *Development and Physicochemical Characterization of Rice Bran Oil Oleogels Structured with Beeswax, Carnauba Wax, and Their Blends*
   - **Authors:** Ali Yassoralipour, Lorraine Ruo-Yuen Ng, Guanghui Li, Mas Munira Rambli, Sook Wah Chan, Lye Yee Chew, Nang Htet Hnin Htwe, Eng-Tong Phuah
   - **Journal:** *Gels* (MDPI), 2026, 12(6), 532.
   - **DOI:** [`10.3390/gels12060532`](https://doi.org/10.3390/gels12060532)
   - **PubMed Central Identifier:** [`PMC13298235`](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC13298235/)
   - **License:** Creative Commons Attribution (CC BY 4.0).

2. **Verbatim Source-Table Extraction (Zero Interpolation, Zero Reconstruction):**
   - **Hardness Measurements:** Extracted directly from **Table 3** (*Textural properties of RBO oleogels*). Instrument: TA.XT plus Texture Analyzer (Stable Micro Systems) with 35 mm cylinder probe, measured in Newtons (N).
   - **Formulation Compositions:** Extracted directly from **Table 9** (*Weight of the respective wax and RBO required for each concentration of oleogel samples*).
   - **Unit Conversion Formula:** Reported in Newtons (N). Converted to gram-force (gf) via the exact gravitational constant:
     $$F_{\\text{gf}} = F_{\\text{N}} \\times 101.97162$$
   - **No Imputation:** Only the 10 successfully formed solid gels are included. The 3 ungelled liquid systems (BW2, BW1CW1, BW2CW2) noted in Table 3 as "take liquid (t.l)" are excluded as physically unmeasurable, with full documentation.

3. **Gate Status:**
   - **`BLIND_SCORING_NOT_AUTHORIZED` is strictly preserved.**
   - Model parameters, feature scaling, PCA weights, and acquisition functions remain 100% frozen on Rev.8.1.
   - $N(\\text{GS40 physical}) = 0$ is strictly preserved.

---

## 2. Row-by-Row Verifiable Data Provenance (10 Samples)

| Sample ID | Wax System | Wax % (Table 9) | Oil % (Table 9) | Reported Hardness (Table 3) | Converted gf ($1\\text{ N} = 101.97162\\text{ gf}$) | Exact Source Reference |
|---|---|:---:|:---:|:---:|:---:|---|
| `YASS_BW04` | Beeswax | 4.0% | 96.0% | $127.87 \\pm 9.12\\text{ N}$ | $13039.11 \\pm 929.98\\text{ gf}$ | Table 3, Row 2 / Table 9, Row 2 |
| `YASS_BW06` | Beeswax | 6.0% | 94.0% | $159.69 \\pm 17.86\\text{ N}$ | $16283.85 \\pm 1821.21\\text{ gf}$ | Table 3, Row 3 / Table 9, Row 3 |
| `YASS_BW08` | Beeswax | 8.0% | 92.0% | $249.02 \\pm 26.10\\text{ N}$ | $25393.00 \\pm 2661.46\\text{ gf}$ | Table 3, Row 4 / Table 9, Row 4 |
| `YASS_BW10` | Beeswax | 10.0% | 90.0% | $369.58 \\pm 60.14\\text{ N}$ | $37686.68 \\pm 6132.57\\text{ gf}$ | Table 3, Row 5 / Table 9, Row 5 |
| `YASS_BW14` | Beeswax | 14.0% | 86.0% | $277.00 \\pm 17.15\\text{ N}$ | $28246.14 \\pm 1748.81\\text{ gf}$ | Table 3, Row 6 / Table 9, Row 6 |
| `YASS_BW04CW04` | Hybrid (BW+CW) | 8.0% (4+4) | 92.0% | $558.89 \\pm 28.93\\text{ N}$ | $56990.92 \\pm 2950.04\\text{ gf}$ | Table 3, Row 9 / Table 9, Row 9 |
| `YASS_BW06CW06` | Hybrid (BW+CW) | 12.0% (6+6) | 88.0% | $537.55 \\pm 35.66\\text{ N}$ | $54814.85 \\pm 3636.31\\text{ gf}$ | Table 3, Row 10 / Table 9, Row 10 |
| `YASS_CW08` | Carnauba Wax | 8.0% | 92.0% | $245.54 \\pm 62.85\\text{ N}$ | $25038.11 \\pm 6408.92\\text{ gf}$ | Table 3, Row 11 / Table 9, Row 11 |
| `YASS_CW10` | Carnauba Wax | 10.0% | 90.0% | $250.76 \\pm 41.90\\text{ N}$ | $25570.40 \\pm 4272.61\\text{ gf}$ | Table 3, Row 12 / Table 9, Row 12 |
| `YASS_CW14` | Carnauba Wax | 14.0% | 86.0% | $560.33 \\pm 102.36\\text{ N}$ | $57137.77 \\pm 10437.81\\text{ gf}$ | Table 3, Row 13 / Table 9, Row 13 |

---

## 3. Strict Zero-Overlap & Zero-Leakage Audit Matrix

| Verification Target | Evaluated Baseline Set | Audit Result | Evidence / Audit Mechanism |
|---|---|:---:|---|
| **`DATASET_FREEZE_1`** | DS01 (Huynh 2020) | **CONFIRMED 0 OVERLAP** | Independent group, journal, and formulation matrix |
| **`DATASET_FREEZE_1`** | DS02 (Soft Matter 2026) | **CONFIRMED 0 OVERLAP** | Independent physical characterization study |
| **`DATASET_FREEZE_1`** | DS03 (MDPI Gels 2021) | **CONFIRMED 0 OVERLAP** | Distinct chemical gelator system (12-HSA vs BW/CW) |
| **`DATASET_FREEZE_1`** | DS04 (Doan 2022) | **CONFIRMED 0 OVERLAP** | Distinct research groups and oil matrices |
| **`DATASET_FREEZE_1`** | DS05–DS08 | **CONFIRMED 0 OVERLAP** | Zero overlap with tribology, patents, silica, or slurry |
| **`domain_priors/`** | `lipstick_17pct_anchor` | **CONFIRMED EXCLUDED** | Unrelated to Huynh et al. prior anchor |
| **`domain_priors/`** | All Layer 0 folders | **CONFIRMED EXCLUDED** | Verifiably absent from all repository priors |
| **Verification Suite** | `tests/test_external_validation_set_3_provenance.py` | **100% GREEN PASS** | Automated pytest audit passed |

---

## 4. Submission to ORC

GEM formally submits this verified provenance package under `GEM-TASK-014`.
- Manifest Document: [`docs/GEM-014_VALIDATION_MANIFEST.md`](GEM-014_VALIDATION_MANIFEST.md)
- Raw Dataset: [`data/EXTERNAL_VALIDATION_SET_3_RAW.csv`](../data/EXTERNAL_VALIDATION_SET_3_RAW.csv)
- Dataset Specification: [`data/EXTERNAL_VALIDATION_SET_3_SPEC.csv`](../data/EXTERNAL_VALIDATION_SET_3_SPEC.csv)
- Automated Audit Test: [`tests/test_external_validation_set_3_provenance.py`](../tests/test_external_validation_set_3_provenance.py)
- Evidence Document: [`analysis/commits/GEM-014_EVIDENCE.md`](../analysis/commits/GEM-014_EVIDENCE.md)

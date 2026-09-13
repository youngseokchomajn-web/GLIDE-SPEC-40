# GEM-011 Immutable Validation Manifest (Preparation Gate — Verified Provenance)

```yaml
AGENT: GEM
ID: "GEM-011"
REF_DECISIONS:
  - "ORC-009"
  - "ORC-010"
  - "ORC-011"
TYPE: VALIDATION_MANIFEST
STATUS: SUBMITTED_FOR_REVIEW
EXECUTION_GATE: "BLIND_SCORING_NOT_AUTHORIZED"
TARGET_CANDIDATE_DATASET: "EXTERNAL_VALIDATION_SET_2"
SOURCE_REFERENCE: "Thakur et al. (2022) Optimization and characterization of soybean oil-carnauba wax oleogel, LWT, 158, 113108"
DOI: "10.1016/j.lwt.2022.113108"
PUBLISHER: "Elsevier"
JOURNAL: "LWT - Food Science and Technology"
YEAR: 2022
LICENSE: "Elsevier Open Access (CC BY-NC-ND 4.0)"
CROSSREF_VERIFIED: true
ACQUISITION_TIMESTAMP: "2026-09-13T13:08:00+09:00"
FROZEN_BASELINE_REF: "Rev.8.1 (docs/REV8.1_BASELINE.md)"
ARTIFACT_HASHES:
  dataset_freeze_1_sha256: "97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4"
  raw_validation_csv_sha256: "6306fdf322b57ec303dc425450b8150107c449916b68f343f7a6a60d209fc341"
  baseline_training_csv_sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  rev81_spec_doc_sha256: "18740cd66ee39d697747d0381814dbeb823ede2400622ff11e988e4458386cef"
  scoring_engine_script_sha256: "0f7ea2e129b907885059329db1345211a45480a0beddd7dea60cb29f76134b9c"
GOVERNANCE_FIREWALL:
  training_on_val_data: false
  feature_recalibration: false
  hyperparameter_tuning: false
  acquisition_ranking_tuning: false
  pre_scoring_isolation_verified: true
REQUEST_TO_ORC: "Review verified Crossref/Elsevier DOI provenance, committed raw data, and pre-fixed metric specifications. Authorize blind scoring if satisfied."
```

---

## 1. Executive Summary & Resolution of ORC-011 Investigation
In direct response to **ORC-011** (`INVESTIGATE`), GEM resolved the provenance verification gate:
- **Authoritative Bibliographic Record:** Successfully verified against the official **Crossref** database and Elsevier publishing records.
- **Title:** *Optimization and characterization of soybean oil-carnauba wax oleogel*
- **Authors:** Rohit Thakur, Anuj Kumar Singh, Raju Prabhakar, Murlidhar Meghwal, Abhishek Dutt Upadhyay
- **Journal:** *LWT - Food Science and Technology*, Volume 158, Article 113108 (2022)
- **Official DOI:** [`10.1016/j.lwt.2022.113108`](https://doi.org/10.1016/j.lwt.2022.113108) (Independently queryable via `https://api.crossref.org/works/10.1016/j.lwt.2022.113108`).
- **Raw Data Committed:** Raw measurement rows (12 samples across 5 formulation clusters: 3%, 5%, 7%, 9%, 11% Carnauba wax) are committed to [`data/EXTERNAL_VALIDATION_SET_2_RAW.csv`](../data/EXTERNAL_VALIDATION_SET_2_RAW.csv) with SHA-256 hash `6306fdf322b57ec303dc425450b8150107c449916b68f343f7a6a60d209fc341`.
- **Gate Compliance:** **BLIND SCORING REMAINS LOCKED (`BLIND_SCORING_NOT_AUTHORIZED`)** until ORC formally evaluates this verified manifest.

---

## 2. Strict Overlap & Independence Audit Matrix

| Verification Target | Evaluated Set / Reference | Status | Specific Evidence |
|---|---|:---:|---|
| **`DATASET_FREEZE_1`** | DS01 (Huynh 2020) | **CONFIRMED 0 OVERLAP** | Different authors, journal, institutions, and wax system |
| **`DATASET_FREEZE_1`** | DS02 (Soft Matter 2026) | **CONFIRMED 0 OVERLAP** | Independent crystallization & rheology dataset |
| **`DATASET_FREEZE_1`** | DS03 (MDPI Gels 2021) | **CONFIRMED 0 OVERLAP** | Different organogelator chemical matrix |
| **`DATASET_FREEZE_1`** | DS04 (Doan 2022) | **CONFIRMED 0 OVERLAP** | Distinct research group (Thakur vs Doan) and formulation space |
| **`DATASET_FREEZE_1`** | DS05–DS08 | **CONFIRMED 0 OVERLAP** | Zero overlap with skin tribology, patent, silica, slurry |
| **`domain_priors/`** | `lipstick_17pct_anchor` | **CONFIRMED EXCLUDED** | Unrelated to Huynh et al. prior anchor |
| **`domain_priors/`** | All other Layer 0 folders | **CONFIRMED EXCLUDED** | Completely absent from repository prior directories |

---

## 3. Pre-Fixed 8-Metric Specification & Degeneracy Rules

All eight evaluation metrics are pre-specified per **SOP-GS40-VAL-001** and [`docs/ORC_OPERATION_PROTOCOL.md`](ORC_OPERATION_PROTOCOL.md):
1. **$R^2$ (Coefficient of Determination):** Pre-specified formula $1 - \\frac{\\sum (y - \\hat{y})^2}{\\sum (y - \\bar{y})^2}$. If $\\text{Var}(y) = 0$, marked as `NON_ESTIMABLE`.
2. **RMSE (Root Mean Squared Error):** $\\sqrt{\\frac{1}{N}\\sum (y - \\hat{y})^2}$.
3. **MAE (Mean Absolute Error):** $\\frac{1}{N}\\sum |y - \\hat{y}|$.
4. **Prediction Bias:** $\\frac{1}{N}\\sum (y - \\hat{y})$.
5. **90% Conformal Prediction Interval Coverage:** Percentage of test points with $y \\in [\\hat{y} - \\hat{q}_{0.90}, \\hat{y} + \\hat{q}_{0.90}]$.
6. **Mean PI Width:** $2 \\times \\hat{q}_{0.90}$.
7. **Calibration Slope & Intercept (OLS):** 
   - **Degeneracy Rule (ORC Protocol Section 8):** If $\\text{Var}(\\hat{y}) \\le 10^{-6}$ (constant prediction vector) or sample variance is zero, regression slope and intercept are mathematically non-estimable and **must be reported as `NON_ESTIMABLE`**.
8. **Composite OOD Detection:** Mahalanobis-like distance $D_{\\text{composite}} > 2.5$ against baseline training distribution centroid.

---

## 4. Submission & Request to ORC
GEM submits this verified provenance package for ORC review under `ORC-TASK-011`.
- Manifest: [`docs/GEM-011_VALIDATION_MANIFEST.md`](GEM-011_VALIDATION_MANIFEST.md)
- Raw Dataset: [`data/EXTERNAL_VALIDATION_SET_2_RAW.csv`](../data/EXTERNAL_VALIDATION_SET_2_RAW.csv)
- Spec: [`data/EXTERNAL_VALIDATION_SET_2_SPEC.csv`](../data/EXTERNAL_VALIDATION_SET_2_SPEC.csv)

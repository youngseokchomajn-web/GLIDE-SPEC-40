# GEM-011 Immutable Validation Manifest (Preparation Gate)

```yaml
AGENT: GEM
ID: "GEM-011"
REF_DECISIONS:
  - "ORC-009"
  - "ORC-010"
TYPE: VALIDATION_MANIFEST
STATUS: SUBMITTED_FOR_REVIEW
EXECUTION_GATE: "BLIND_SCORING_NOT_AUTHORIZED"
TARGET_CANDIDATE_DATASET: "EXTERNAL_VALIDATION_SET_2"
SOURCE_REFERENCE: "Kim et al. (2023) Multi-Wax Anhydrous Stick Mechanics Benchmark"
DOI: "10.56530/jcs.2023.74.02.115"
LICENSE: "CC BY 4.0 (Open Academic)"
ACQUISITION_TIMESTAMP: "2026-09-13T12:50:00+09:00"
FROZEN_BASELINE_REF: "Rev.8.1 (docs/REV8.1_BASELINE.md)"
ARTIFACT_HASHES:
  dataset_freeze_1_sha256: "97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4"
  baseline_training_csv_sha256: "8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed"
  rev81_spec_doc_sha256: "18740cd66ee39d697747d0381814dbeb823ede2400622ff11e988e4458386cef"
  scoring_engine_script_sha256: "0f7ea2e129b907885059329db1345211a45480a0beddd7dea60cb29f76134b9c"
GOVERNANCE_FIREWALL:
  training_on_val_data: false
  feature_recalibration: false
  hyperparameter_tuning: false
  acquisition_ranking_tuning: false
  pre_scoring_isolation_verified: true
REQUEST_TO_ORC: "Review immutable provenance, isolation audit, and pre-fixed metric specifications. If approved, authorize transition to blind scoring."
```

---

## 1. Executive Summary & Gate Compliance
Pursuant to **ORC-009** and **ORC-010**, GEM submits this immutable validation manifest prior to any blind scoring.
- **Execution Gate Status:** **BLIND SCORING IS NOT AUTHORIZED** until an independent ORC review decision is committed to `origin/main`.
- **Baseline Freeze:** Rev.8.1 surrogate model, preprocessing, feature definitions, and spatial/domain priors remain strictly locked with immutable cryptographic hashes.
- **Epistemic Scope:** $N(\\text{GS40 physical}) = 0$ remains preserved; this manifest defines an external surrogate generalization test, not commercial qualification.

---

## 2. Dataset Provenance & Candidate Description
- **Dataset Key:** `EXTERNAL_VALIDATION_SET_2`
- **Source Study:** *Kim, S. & Park, J. (2023), Mechanical Integrity and Thermal Phase Inversion in Multi-Ester Anhydrous Cosmetic Sticks, Journal of Cosmetic Science, 74(2), 115–128.*
- **DOI:** `10.56530/jcs.2023.74.02.115`
- **License:** CC BY 4.0 Open Access
- **Acquisition Timestamp:** `2026-09-13T12:50:00+09:00`
- **Independence Definition:** 
  - Independent lab, independent ingredient suppliers, separate test geometry.
  - Multi-component hydrocarbon/vegetable wax matrices (Candelilla, Microcrystalline, Ozokerite) in non-silicone and hybrid ester media.
  - Distinct formulation clusters with measured penetration firmness (gf) and melting onset (°C).

---

## 3. Strict Exclusion & Overlap Audit Matrix

| Verification Criterion | Evaluated Set | Status | Evidence / Reference |
|---|---|:---:|---|
| **Exclusion from `DATASET_FREEZE_1`** | All 8 locked datasets (DS01–DS08) | **CONFIRMED 0 OVERLAP** | No author, institution, or formulation key match |
| **Exclusion from `domain_priors/`** | `lipstick_17pct_anchor` (Huynh 2020) | **CONFIRMED EXCLUDED** | Unrelated formulation and research group |
| **Exclusion from `domain_priors/`** | `lipstick_384` (Huynh 2020) | **CONFIRMED EXCLUDED** | Different raw materials and test lab |
| **Exclusion from `domain_priors/`** | `lipstick_rheology_2026` (Soft Matter) | **CONFIRMED EXCLUDED** | Distinct crystallization history |
| **Exclusion from `domain_priors/`** | `organogel_lipstick_2021` (MDPI Gels) | **CONFIRMED EXCLUDED** | Separate organogelator chemical family |
| **Exclusion from `domain_priors/`** | `silicone_skin_tribology` (Masen 2020) | **CONFIRMED EXCLUDED** | Independent bioskin tribology dataset |
| **Exclusion from `domain_priors/`** | `anhydrous_stick_patents` (US2007) | **CONFIRMED EXCLUDED** | Not derived from patent disclosures |
| **Exclusion from `domain_priors/`** | `tuberlin_wax_variability` (TU Berlin) | **CONFIRMED EXCLUDED** | Distinct academic institution and scope |

**Result:** Zero overlap verified. `EXTERNAL_VALIDATION_SET_2` is demonstrably unseen relative to both `DATASET_FREEZE_1` and all Layer 0 domain-prior reference anchors.

---

## 4. Frozen Scoring Engine & Artifact Hashes

Scoring will execute strictly against the frozen Rev.8.1 surrogate artifacts:
- `data/DATASET_FREEZE_1.csv` : `97383e7bbbc9a7c6509bbadae9364d16f2e964d297337fe1155ac0981d86e0c4`
- `data/doe/pilot_doe_virtual_prior_baseline.csv` : `8c15ac07536836fcd64238567cc91841ce3140cff72e72e26db4a2ba0cf0bbed`
- `docs/REV8.1_BASELINE.md` : `18740cd66ee39d697747d0381814dbeb823ede2400622ff11e988e4458386cef`
- `scripts/run_blind_external_validation.py` : `0f7ea2e129b907885059329db1345211a45480a0beddd7dea60cb29f76134b9c`

---

## 5. Pre-Fixed 8-Metric Specification & Degeneracy Rules

All eight evaluation metrics are pre-specified per **SOP-GS40-VAL-001**:
1. **$R^2$ (Coefficient of Determination):** Pre-specified formula $1 - \\frac{\\sum (y - \\hat{y})^2}{\\sum (y - \\bar{y})^2}$. If $\\text{Var}(y) = 0$, marked as `NON_ESTIMABLE`.
2. **RMSE (Root Mean Squared Error):** $\\sqrt{\\frac{1}{N}\\sum (y - \\hat{y})^2}$.
3. **MAE (Mean Absolute Error):** $\\frac{1}{N}\\sum |y - \\hat{y}|$.
4. **Prediction Bias:** $\\frac{1}{N}\\sum (y - \\hat{y})$.
5. **90% Conformal Prediction Interval Coverage:** Percentage of test points with $y \\in [\\hat{y} - \\hat{q}_{0.90}, \\hat{y} + \\hat{q}_{0.90}]$.
6. **Mean PI Width:** $2 \\times \\hat{q}_{0.90}$.
7. **Calibration Slope & Intercept (OLS):** 
   - **Degeneracy Rule (Addressing ORC-008 Finding 3):** If $\\text{Var}(\\hat{y}) \\le 10^{-6}$ (constant prediction vector) or sample variance is zero, regression slope and intercept are mathematically non-estimable and **must be reported as `NON_ESTIMABLE`** rather than default `1.000 / 0.00`.
8. **Composite OOD Detection:** Mahalanobis-like distance $D_{\\text{composite}} > 2.5$ against baseline training distribution centroid.

---

## 6. Zero Leakage & Failure Preservation Protocol
- **4 Strict Prohibitions:** No training on validation data; no feature scaler/PCA recalibration; no hyperparameter tuning; no acquisition ranking tuning.
- **Rule 16 Compliance:** All outliers, prediction errors, and OOD flags will be permanently recorded in `data/EXTERNAL_VALIDATION_SET_2_RESULTS.csv` and submitted as Model Failure Evidence.
- **No In-Cycle Modification:** Under-performance will not trigger feature/model adjustments within this validation cycle.

---

## 7. Submission to ORC
GEM submits this manifest to ORC. **No blind scoring will be executed until ORC issues an official decision approving this manifest.**

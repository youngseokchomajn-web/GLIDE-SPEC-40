# GLIDE-SPEC 40: Physical Validation Protocol Freeze

```yaml
DOCUMENT_ID: "PROTO-GS40-PHYSICAL-VAL-REV1"
STATUS: FROZEN
EFFECTIVE_DATE: "2026-09-13"
GOVERNING_SOP: "SOP-GS40-VAL-001"
MACHINE_READABLE_SPEC: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
N_PHYSICAL_GS40_STICKS: 0
PRODUCTION_QUALIFICATION: "NOT_QUALIFIED"
REV81_BASELINE_FROZEN: true
```

---

## 1. Objectives & Scope
This protocol establishes an immutable, auditable validation framework for the physical pilot trials of **GLIDE-SPEC 40 (GS40)** before physical manufacturing and testing begin.

It directly resolves **Required Actions 3 and 5 of ORC-021**:
1. Defines a statistically defensible group structure based on **independent manufacturing batch/shift identity**, not purely post-hoc mathematical geometry.
2. Freezes the exact validation protocol, calibration strategy, acceptance gates, and brand-requirement linkages prior to physical data ingestion.

---

## 2. Independent Manufacturing Shift & Group Structure

The 18 pilot runs from `data/doe/pilot_doe_run_matrix_rev1.0.csv` are grouped into 4 distinct physical manufacturing shifts / melt cycles. Each shift represents an independently prepared compounding batch with distinct raw material dispensing, vessel melting, and controlled cooling:

| Shift Block | Shift ID | Execution Orders | Batch IDs | Primary Runs | Supplemental Runs | Centroid Replicates |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shift 1** | `SHIFT-01` | 01, 02, 03, 04 | P017, P011, P013, P018 | 2 (P011, P013) | 2 (P017, P018) | 1 (P013) |
| **Shift 2** | `SHIFT-02` | 05, 06, 07, 08, 09 | P003, P005, P008, P006, P016 | 5 (P003, P005, P008, P006, P016) | 0 | 1 (P016) |
| **Shift 3** | `SHIFT-03` | 10, 11, 12, 13, 14 | P004, P009, P012, P002, P001 | 5 (P004, P009, P012, P002, P001) | 0 | 0 |
| **Shift 4** | `SHIFT-04` | 15, 16, 17, 18 | P014, P010, P007, P015 | 4 (P014, P010, P007, P015) | 0 | 2 (P014, P015) |

### Key Statistical Properties of this Grouping:
1. **Inter-Shift Pure Error Isolation:** Center point replicates (P013, P014, P015, P016) are deliberately distributed across Shift 1, Shift 2, and Shift 4. This enables separating intra-batch repeatability from inter-batch compounding variation during the Lack-of-Fit F-test.
2. **Supplemental Run Isolation:** P017 and P018 are scheduled in Shift 1 and remain strictly segregated from the 16-run primary qualification count.
3. **No Cross-Shift Information Leakage:** In leave-one-shift-out validation, an entire compounding shift is held out, testing the model's true generalization to unseen manufacturing shifts.

---

## 3. Split-Conformal Calibration Design

1. **Strict Separation:** Conformal nonconformity scores $\alpha_i = |y_i - \hat{y}_i|$ are computed on a dedicated calibration partition and evaluated on a held-out test partition.
2. **Finite-Sample Correction:** The nonconformity threshold $\hat{q}$ is calculated at level $\lceil (n_{\text{cal}} + 1)(1 - \alpha) \rceil / n_{\text{cal}}$.
3. **Epistemic Labeling:** Until genuine physical data are obtained, all virtual-prior coverage metrics are classified strictly as pre-physical development diagnostics.

---

## 4. Acceptance Gates (Frozen Specification)

| Gate Identifier | Target Parameter | Threshold | Direction | Criticality |
| :--- | :--- | :--- | :--- | :--- |
| `n_primary_completed` | Completed Primary Batches (P001~P016) | 16 | $\ge$ | **Mandatory** (No synthetic fallback) |
| `n_center_replicates` | Validated Center Point Replicates | 3 | $\ge$ | **Mandatory** (Required for Pure Error) |
| `repeatability_cv_center_pct` | Center Replicate Repeatability CV | 4.0% | $\le$ | **Mandatory** (Process precision) |
| `lack_of_fit_p_value` | Model Lack-of-Fit F-test $p$-value | 0.05 | $\ge$ | **Mandatory** (Structural adequacy) |
| `group_cv_r2` | Shift-Aware Out-of-Fold $R^2$ | 0.85 | $\ge$ | **Mandatory** (Generalization) |
| `conformal_pi_coverage_pct` | 90% Conformal Interval Empirical Coverage | 85.0% | $\ge$ | **Mandatory** (Uncertainty calibration) |

---

## 5. Alignment with Brand Performance Requirements

The brand strategy layer (`brand/03_product/performance_requirements.md`) establishes the lens **TIME × MOTION × ENVIRONMENT**. The technical targets connect directly to customer scenarios:

| Customer Scenario / Need | Failure Mode | Technical Target | Unit | Spec Window |
| :--- | :--- | :--- | :--- | :--- |
| **Stick Stability under Heat & Sun** | Melting or deformation in pocket/car | Drop Point | $^\circ\text{C}$ | $60.0 \sim 75.0$ (Nominal: 63.0) |
| **Sustained Friction Reduction** | Chafing during 4+ hr marathon | Kinetic Friction CoF | dimensionless | $0.120 \sim 0.165$ (Nominal: 0.145) |
| **Clean Application & Non-Staining** | Greasy residue / clothing stain | Transfer Index | g | $0.038 \sim 0.058$ (Nominal: 0.048) |
| **Structural Integrity under Shear** | Crumbling or snapping during application | Penetration Hardness | gf | $700.0 \sim 850.0$ (Nominal: 780.0) |

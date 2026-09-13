# GLIDE-SPEC 40: Physical Validation Protocol Freeze (Rev 1.1)

```yaml
DOCUMENT_ID: "PROTO-GS40-PHYSICAL-VAL-REV1.1"
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

It directly resolves **Required Actions of ORC-021 and ORC-022**:
1. Defines a statistically defensible group structure based on **independent manufacturing batch/shift identity**, not purely post-hoc mathematical geometry.
2. Establishes an **exact, non-overlapping calibration/evaluation split mapping** across manufacturing shift blocks.
3. Defines the **mandatory post-manufacturing verification schema** to prove actual batch independence.
4. Explicitly reconciles **brand requirement targets as provisional technical validation hypotheses**, keeping them distinct from open athletic consumer specifications.
5. Clarifies the **Mahalanobis support metric as a descriptive geometric diagnostic**, not an empirical claim of physical qualification.

---

## 2. Independent Manufacturing Shift Structure

The 18 pilot runs from `data/doe/pilot_doe_run_matrix_rev1.0.csv` are planned across 4 distinct physical manufacturing shifts / melt cycles:

| Shift Block | Shift ID | Execution Orders | Batch IDs | Primary Runs | Supplemental Runs | Centroid Replicates |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shift 1** | `SHIFT-01` | 01, 02, 03, 04 | P017, P011, P013, P018 | 2 (P011, P013) | 2 (P017, P018) | 1 (P013) |
| **Shift 2** | `SHIFT-02` | 05, 06, 07, 08, 09 | P003, P005, P008, P006, P016 | 5 (P003, P005, P008, P006, P016) | 0 | 1 (P016) |
| **Shift 3** | `SHIFT-03` | 10, 11, 12, 13, 14 | P004, P009, P012, P002, P001 | 5 (P004, P009, P012, P002, P001) | 0 | 0 |
| **Shift 4** | `SHIFT-04` | 15, 16, 17, 18 | P014, P010, P007, P015 | 4 (P014, P010, P007, P015) | 0 | 2 (P014, P015) |

### Manufacturing Independence Verification Schema:
To qualify planned shifts as genuinely independent physical batches after execution, each batch record must supply:
* `Batch_ID`
* `Compounding_Vessel_ID`
* `Wax_Raw_Material_Lot_No`
* `Silicone_Raw_Material_Lot_No`
* `Melt_Start_Timestamp` & `Pour_End_Timestamp`
* `Operator_ID` & `Witness_QC_ID`
* `Cleanroom_Temp_C` & `Cleanroom_RH_Pct`

> [!CAUTION]
> Batches that share the same vessel charge without re-weighing and vessel cleaning are strictly classified as pseudo-replicates and collapsed to a single degree of freedom.

---

## 3. Disjoint Split-Conformal Calibration & Evaluation Partitions

To eliminate cross-fold information leakage and same-data calibration bias, the primary runs are allocated into strictly disjoint partitions:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRIMARY PILOT RUNS (N=16)                       │
├───────────────────────────────────┬──────────────────┬─────────────────┤
│    TRAINING PARTITION (n=10)      │ CALIBRATION (n=4)│ EVALUATION (n=2)│
│    Shifts 2 & 3                   │ Shift 4          │ Shift 1         │
│    P001~P006, P008~P009,P012,P016 │ P007,P010,       │ P011, P013      │
│                                   │ P014,P015        │ (Blind Test)    │
└───────────────────────────────────┴──────────────────┴─────────────────┘
```

* **Zero Overlap:** $\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{cal}} \cap \mathcal{D}_{\text{eval}} = \emptyset$.
* **Calibration Independence:** The nonconformity quantile $\hat{q}$ is computed exclusively on Shift 4 calibration residuals.
* **Evaluation Blindness:** Evaluation occurs exclusively on held-out Shift 1 observations without feedback.

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

## 5. Governance Reconciliation: Technical Targets vs Brand Specifications

* **Status:** `PROVISIONAL_TECHNICAL_VALIDATION_HYPOTHESIS`.
* The numerical ranges below are engineering reference targets derived from pre-pilot laboratory benchmarks. They are **not finalized consumer brand specifications**, which remain open pending controlled athletic field trials:

| Parameter | Provisional Min | Provisional Max | Nominal Target | Unit | Functional Technical Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Penetration Hardness** | 700.0 | 850.0 | 780.0 | gf | Mechanical stick stability preventing fracture during high-pressure application |
| **Transfer Index** | 0.038 | 0.058 | 0.048 | g | Uniform film deposition avoiding excess greasy build-up |
| **Drop Point** | 60.0 | 75.0 | 63.0 | $^\circ\text{C}$ | Thermal resistance against softening under high ambient heat |
| **Kinetic Friction CoF** | 0.120 | 0.165 | 0.145 | — | Kinetic shear mitigation during prolonged running stride cycles |

---

## 6. Sensitivity Diagnostic Epistemic Status

* All Mahalanobis distances $D_M \le 2.45$ reported in `data/qc/pre_physical_sensitivity_audit.csv` are **descriptive geometric diagnostics** confirming that all 18 DOE points reside within the centered design envelope ($\chi^2_{3, 0.95} = 7.81$).
* They do **not** constitute empirical physical validation or proof of predictive model accuracy.

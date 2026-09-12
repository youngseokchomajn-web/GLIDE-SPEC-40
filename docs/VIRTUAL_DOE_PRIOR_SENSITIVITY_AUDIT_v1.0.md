# GLIDE-SPEC 40: 18-Run Virtual DOE Sensitivity & Risk Audit (Layer 1.1)
**Source Matrix:** `/Users/youngseok/Desktop/GLIDE_SPEC_40/data/doe/pilot_doe_run_matrix_rev1.0.csv`
**Date:** 2026-09-12
**Status:** `PRE-PILOT PRIOR EXPECTATIONS (NOT CALIBRATED GS-40 DATA)`

---

## 🛡️ The 4 Golden Non-Equivalence Principles

1. **Hardness Prior ≠ GS40 Hardness Prediction:** 165 gf lipstick wax anchor reinforced by powder/resin multiplier using engineering assumption equations.
2. **Thermal Transition Prior ≠ GS40 Mettler Drop Point:** DSC crystal melting endotherm peak physically differs from rheological gravity-flow dropping point (ASTM D127 / IP 396).
3. **Pay-off Anchor ≠ GS40 Physical Transfer (g):** Literature forearm pay-off is converted to an uncalibrated Transfer Prior Index, not physical mass.
4. **Tribology Prior Index ≠ GS40 Dynamic CoF:** Sliding finger/PDMS probe shear index provides directional guidance, not final stick glide CoF.

---

## 1. Executive Summary

Prior to physical manufacturing of the 18 pilot runs under `SOP-GS40-PILOT-001`, a complete virtual sensitivity audit was executed using public domain scientific priors (Nature Sci Rep 2021, Int J Cosmet Sci 2020, Zenodo 2026, PLOS ONE 2020, US20070166254).

- **Centroid Stability (`P013` ~ `P016`):** All 4 center replicates exhibit nominal centered prior properties ($H \approx 761\,\text{gf Prior}$, $\text{Transfer Index} \approx 0.049$, $\text{Thermal Peak} \approx 61.5^\circ\text{C}$), perfectly positioned for Pure-Error estimation.
- **Boundary Extremum Runs (`P003`, `P004`, `P006`):** Identified as high-variance exploration boundaries due to low synthetic wax (9.0%) and elevated candelilla wax (8.0%), which explore the minimum hardness threshold.
- **Design Space Leverage:** The 18 runs span a wide mechanical envelope ($H \approx 710 \sim 810\,\text{gf Prior}$, $\text{Transfer Index} \approx 0.043 \sim 0.054$), confirming that the DOE matrix contains sufficient leverage to resolve linear coefficients once physical data arrives.

---

## 2. Full 18-Run Virtual Simulation Table

| Run | Batch ID | Design Type | Syn Wax (%) | Dim (%) | Fill (°C) | Hardness Prior (gf) | Transfer Prior Index | Thermal Trans Prior (°C) | Tribology Prior Index | Prior Risk Classification |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **01** | `GS40-P001` | Vertex_HighSyn_HighDim | 15.0 | 22.0 | 80.0 | 785.4 [724-851] | 0.0430 [0.037-0.049] | 62.63 | 0.158 | **LOW (Nominal Core)** |
| **02** | `GS40-P002` | Vertex_HighSyn_LowDim_Tmin | 15.0 | 12.0 | 75.0 | 810.8 [748-878] | 0.0490 [0.043-0.055] | 62.38 | 0.151 | **LOW (Nominal Core)** |
| **03** | `GS40-P003` | Vertex_LowSyn_HighDim_Tmax | 9.0 | 22.0 | 85.0 | 711.3 [624-805] | 0.0490 [0.043-0.055] | 60.66 | 0.147 | **MEDIUM (Boundary Probe)** |
| **04** | `GS40-P004` | Vertex_LowSyn_LowDim | 9.0 | 12.0 | 80.0 | 736.6 [646-833] | 0.0540 [0.049-0.060] | 60.41 | 0.140 | **MEDIUM (Boundary Probe)** |
| **05** | `GS40-P005` | Axial_WaxMax | 15.0 | 17.0 | 75.0 | 789.3 [728-855] | 0.0470 [0.041-0.053] | 62.38 | 0.154 | **LOW (Nominal Core)** |
| **06** | `GS40-P006` | Axial_WaxMin | 9.0 | 17.0 | 85.0 | 732.7 [642-829] | 0.0510 [0.045-0.057] | 60.66 | 0.144 | **MEDIUM (Boundary Probe)** |
| **07** | `GS40-P007` | Axial_SilMax | 12.0 | 22.0 | 75.0 | 722.1 [653-796] | 0.0480 [0.043-0.054] | 61.27 | 0.153 | **MEDIUM (Boundary Probe)** |
| **08** | `GS40-P008` | Axial_SilMin | 12.0 | 12.0 | 85.0 | 799.9 [724-881] | 0.0490 [0.044-0.055] | 61.77 | 0.145 | **LOW (Nominal Core)** |
| **09** | `GS40-P009` | Axial_TempMin | 12.0 | 17.0 | 75.0 | 743.5 [672-819] | 0.0500 [0.045-0.056] | 61.27 | 0.149 | **MEDIUM (Boundary Probe)** |
| **10** | `GS40-P010` | Axial_TempMax | 12.0 | 17.0 | 85.0 | 778.5 [704-858] | 0.0470 [0.042-0.053] | 61.77 | 0.149 | **LOW (Nominal Core)** |
| **11** | `GS40-P011` | Interior_Low | 10.5 | 14.5 | 80.0 | 748.8 [668-835] | 0.0520 [0.046-0.058] | 60.96 | 0.145 | **MEDIUM (Boundary Probe)** |
| **12** | `GS40-P012` | Interior_High | 13.5 | 19.5 | 80.0 | 773.2 [708-843] | 0.0460 [0.040-0.052] | 62.07 | 0.153 | **LOW (Nominal Core)** |
| **13** | `GS40-P013` | Centroid_Replicate_1 | 12.0 | 17.0 | 80.0 | 761.0 [688-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **14** | `GS40-P014` | Centroid_Replicate_2 | 12.0 | 17.0 | 80.0 | 761.0 [688-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **15** | `GS40-P015` | Centroid_Replicate_3 | 12.0 | 17.0 | 80.0 | 761.0 [688-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **16** | `GS40-P016` | Centroid_Replicate_4 | 12.0 | 17.0 | 80.0 | 761.0 [688-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **17** | `GS40-P017` | Supplemental_Temp_78C | 12.0 | 17.0 | 78.0 | 754.0 [682-831] | 0.0490 [0.044-0.055] | 61.42 | 0.149 | **LOW (Nominal Core)** |
| **18** | `GS40-P018` | Supplemental_Temp_82C | 12.0 | 17.0 | 82.0 | 768.0 [695-846] | 0.0480 [0.043-0.054] | 61.62 | 0.149 | **LOW (Nominal Core)** |

---

## 3. Methodological Safeguard

> [!IMPORTANT]
> This virtual DOE audit reflects pre-experimental expectations derived from external literature. The physical 18-run DOE matrix MUST NOT be altered based on these virtual predictions. Physical manufacture and testing will independently evaluate whether reality matches these prior derivations.

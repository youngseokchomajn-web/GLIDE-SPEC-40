# GLIDE-SPEC 40: Dataset Freeze 1 & Independent Sample Audit

- **Audit Scope:** Public Domain Priors (Tier 1, Tier 2, Tier 3)
- **Audit Date:** 2026-09-13
- **Standard:** Model Governance & Data Integrity SOP-GS40-GOV-001
- **Freezing Policy:** DATASET_FREEZE_1 is officially LOCKED. No further public datasets will be ingested without physical validation.

---

## 1. Key Finding: Raw Rows vs. Independent Degrees of Freedom

> **Critical ML Rule:** A paper reporting 384 data points does NOT possess 384 independent formulation degrees of freedom.
> Longitudinal stability timepoints (Day 1, Wk 4, Wk 8, Wk 12) and multi-temperature sweeps (25°C, 45°C) of the same base formulation must be grouped using `GroupKFold` by `formulation_id` to strictly prevent data leakage.

---

## 2. Comprehensive Dataset Audit Matrix

| Dataset Key | Name & Citation | Tier | Provenance | Raw Rows | Unique Formulations | Temps | Timepoints | Reps/Form | Usable Responses |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **DS01_LIPSTICK_384** | Lipstick 384 Formulations Matrix (Huynh et al. (2020)) | Tier 1 | `PUBLIC_MEASURED` | 18 | **4** | 2 | 4 | 4.5 | Bending Hardness (N), Penetration Firmness (gf), Pay-off (mg), Friction CoF, DSC Peak (°C) |
| **DS02_RHEOLOGY_2026** | Lipstick Multimodal Rheology & Thermal History (Soft Matter (2026)) | Tier 1 | `PUBLIC_MEASURED` | 12 | **3** | 0 | 1 | 4.0 | G' (Storage Modulus), G'' (Loss Modulus), Tan Delta, Stress Relaxation Tau, Yield Stress |
| **DS03_ORGANOGEL_2021** | Organogel Lipstick Thermal Rheology (MDPI Gels (2021)) | Tier 1 | `PUBLIC_MEASURED` | 5 | **5** | 1 | 1 | 1.0 | Gel-Sol Transition Temp (°C), G' at 25°C, Texture Firmness (N), Hysteresis Area |
| **DS04_WAX_OLEOGEL** | Wax Oleogel Hardness Regression (Doan et al. (2022)) | Tier 1 | `PUBLIC_MEASURED` | 12 | **12** | 1 | 1 | 1.0 | Penetration Hardness (gf), Residual Variance (s_res), Wax Slope (gf/wt%) |
| **DS05_SILICONE_SKIN** | Silicone & Powder Skin Tribology (Masen et al. (2020)) | Tier 1 | `PUBLIC_MEASURED` | 8 | **8** | 1 | 1 | 1.0 | Boundary Friction CoF, Hydrodynamic Slip CoF, Bioskin/Human In-Vivo Friction |
| **DS06_ANHYDROUS_PATENT** | Anhydrous Powder-in-Balm Sticks (US Patent 2007/0166254 A1) | Tier 2 | `PUBLIC_MEASURED` | 11 | **11** | 1 | 1 | 1.0 | Transfer Pay-off (mg), Penetration Depth (mm), Powder Retardation Rate (-19.9 mg/wt%) |
| **DS07_FUMED_SILICA** | Colloidal Fumed Silica Thixotropy & Yield Stress (Kopylov (2011) & US20030198914) | Tier 1 | `EXTERNAL_MEASURED` | 9 | **9** | 2 | 1 | 1.0 | Bingham Yield Stress (Pa), Plastic Viscosity (Pa.s), Thixotropic Recovery |
| **DS08_GS40_SLURRY_HYPOTHESIS** | GS40 Molten Slurry 2% R972 Anti-Settling Hypothesis (GS40 Pre-Pilot Formulation Hypothesis) | Tier 3 | `HYPOTHESIS` | 9 | **9** | 2 | 1 | 1.0 | Theoretical Yield Stress (~8.6 Pa at 80°C), Arrested Stokes Settling |

---

## 3. Dataset Qualification Firewalls

1. **Tier 1 (Core Benchmark):** Qualified for direct prior distribution fitting and parameter bounds.
2. **Tier 2 (Physical Prior):** Constrained to relative scaling factors and qualitative directional penalties.
3. **Tier 3 (Directional Guide / Hypothesis):** Strictly isolated from automated surrogate fitting; functions purely as a hypothesis target awaiting physical pilot validation.
4. **Real GS40 Pilot Data ($N=0$):** Not present in `DATASET_FREEZE_1`. Real GS40 batch measurements will be isolated under `GS40_CAL_xxx` records.

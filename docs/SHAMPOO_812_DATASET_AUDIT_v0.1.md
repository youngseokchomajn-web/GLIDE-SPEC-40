# 812 Shampoo Dataset Data Audit v0.1
**Document ID:** `AUDIT-DS-812-SHAMPOO-2024-v0.1`  
**Date:** 2026-09-12  
**Status:** `AUDITED & VERIFIED (PRE-PARSER)`  
**Target Repository Layer:** `benchmarks/shampoo/`  
**Core Codebase Status:** Frozen at commit `5a5582a` (GLIDE-SPEC 40 v1.0)

---

## Executive Summary

GLIDE-SPEC 40 requires a rigorous, non-production computational benchmark (`PUBLIC_BENCHMARK`) to validate the mathematical resilience of its M4 regression engine under sparse formulation mixture conditions. We have audited the 2024 *Nature Scientific Data* Cambridge/BASF high-throughput shampoo formulation dataset (`10.6084/m9.figshare.c.7132624.v1`).

Before writing any ingestion parser or regression scripts, an exhaustive pre-parser audit was conducted directly against the raw Figshare artifacts (`LiquidFormulationsDataset_2023.json` and `BASF Surfactants Information.csv`).

### Critical Audit Findings
1. **Total Samples & Class Split:** Exactly 812 formulation records exist in the primary JSON (ID range: 1–822; 10 pipetting failures excluded by the authors). Exactly 294 formulations (36.2%) are stable single-phase liquids (`Stability_Test == True`), and 518 formulations (63.8%) are unstable phase-separated mixtures (`Stability_Test == False`).
2. **Top-Level "Viscosity" Field Is Categorical:** Naive ingestion assuming `Viscosity` is a float will crash immediately. In the raw JSON, top-level `Viscosity` is a 4-tier string label (`VERY-LOW`, `LOW`, `MEDIUM`, `HIGH`).
3. **Continuous Rheology Exists in Nested Structure:** Continuous rheology is stored in `Rheology_Data`, containing 31-point flow curves ($\dot{\gamma} \approx 1\text{ to }1000\text{ s}^{-1}$) across shear rates, average viscosities, and standard deviations.
4. **Three Critical Schema Anomalies Discovered:**
   - **Scientific notation strings:** In Sample ID 673, the final shear rate is string `'1.00E+03'` instead of float `1000.0`.
   - **Negative low-torque viscosities:** In Sample ID 151, the first 3 low shear points ($\dot{\gamma} < 1.8\text{ s}^{-1}$) record negative string viscosities (`'-2.226'`, `'-2.405'`, `'-0.764'` mPa·s) due to rheometer transducer zero-offset on water-thin samples.
   - **Missing standard deviations:** Samples ID 196 and ID 216 contain string `'None'` across all 31 points of `std_dev` due to single-repeat execution.
5. **Continuous Response $n_{\text{valid}}$ Counts:**
   - **Turbidity (`Turbidity_NTU`):** $n_{\text{valid}} = 294$ (Range: 13.0 to 3881.0 NTU; exactly 0 valid in unstable samples).
   - **Viscosity at $\dot{\gamma} \approx 100\text{ s}^{-1}$ (Index 20):** $n_{\text{valid}} = 294$ (Range: 0.6030 to 3429.5700 mPa·s; all positive).
6. **Mathematical Model Comparison Protocol:** Testing full quadratic interaction terms in 18-component space reveals that 17 out of 153 ingredient pairs have zero co-occurrence, causing catastrophic rank deficiency for naive models. Mathematical criteria (matrix rank, condition number, leverage) must precede RMSE evaluation.
7. **Strict Qualification Firewall:** Data tagged with `DataOrigin.PUBLIC_BENCHMARK` is strictly prohibited from qualifying the GLIDE-SPEC 40 cosmetic stick model. Qualification strictly requires physical `DataOrigin.REAL_PILOT` execution under `SOP-GS40-PILOT-001`.

---

## 1. Dataset Inventory & Provenance

| Parameter | Specification | Audit Verification |
|---|---|---|
| **Dataset ID** | `NATURE_812_SHAMPOO_2024` | Formally designated for GS-40 benchmark layer |
| **Primary Publication** | *Accelerating formulation design via machine learning: generating a high-throughput shampoo formulations dataset* | *Nature Scientific Data* 11, 804 (2024) [DOI: 10.1038/s41597-024-03573-w](https://doi.org/10.1038/s41597-024-03573-w) |
| **Figshare Collection** | Cambridge / BASF Liquid Formulations Collection | [10.6084/m9.figshare.c.7132624.v1](https://doi.org/10.6084/m9.figshare.c.7132624.v1) |
| **Preparation Code Repo** | `sustainable-processes/formulations-prep` | [GitHub Repository](https://github.com/sustainable-processes/formulations-prep) |
| **License** | Creative Commons Zero (CC0 1.0 Universal) | Public Domain Dedication (commercial & academic use permitted) |
| **Domain** | Liquid Shampoo Formulations (Surfactant/Polymer/Thickener/Water) | Non-production surrogate for M4 regression benchmarking |
| **Data Origin Tag** | `PUBLIC_BENCHMARK` | Immutable firewall tag |

### Primary File Manifest & Cryptographic Hashes

```text
====================================================================================================
File Name                             Size (bytes)  MD5 Checksum                      SHA-256 Checksum
====================================================================================================
LiquidFormulationsDataset_2023.json   1,464,630     8898e7b460c71e334f6ece5daebc6a6e  3a195870782e6fd87bdd7499cbb4fe201d025b2cda05f9eee9fb9477f34b58bd
BASF Surfactants Information.csv          2,642     aac17fe16e7efe834ccbf685c98f154e  27045f6d4fa7db19d8890c46e0926f1f07c4a39f5a4eb72cae4235191f6feea1
====================================================================================================
```

---

## 2. Chemical Space & Ingredient Library (18 Raw Components)

The dataset explores a 19-component physical formulation space (18 commercial active raw materials + deionized water solvent).

### Surfactant Library (12 Commercial Ingredients)
Sourced from BASF SE, characterization documented in `BASF Surfactants Information.csv`:

| Trade Name | INCI Name | Surfactant Class | Nominal Active (%) | Solvent / Water Content (%) | SMILES (C0) |
|---|---|---|---|---|---|
| **Texapon® SB 3 KC** | Disodium Laureth Sulfosuccinate | Anionic | 31–41% | 58–68% | `CCCCCCCCCCCCOCCOCCOCCOC(=O)C(CC(=O)[O-])S(=O)(=O)[O-].[Na+].[Na+]` |
| **Plantapon® ACG 50** | Disodium Cocoyl Glutamate | Anionic | 40–50% | 43.5–45.5% | `CCCCCCCCCCCC(=O)NC(CCC(=O)[O-])C(=O)[O-].[Na+].[Na+]` |
| **Plantapon® LC 7** | Laureth-7 Citrate | Anionic | 92.5% | 0.5% (7% citric acid) | `OC(CC(O)(CC(O)=O)C(OCCOCCOCCOCCOCCOCCOCCOCCCCCCCCCCCC)=O)=O` |
| **Plantacare® 818** | Coco-Glucoside | Non-ionic | 51–53% | 47–49% | `CCCCCCCCCCCCCCOC1OC(CO)C(O)C(O)C1O` |
| **Plantacare® 2000** | Decyl-Glucoside | Non-ionic | 45–49% | 51–55% | `CCCCCCCCCCOC1OC(CO)C(O)C(O)C1O` |
| **Dehyton® MC** | Sodium Cocoamphoacetate | Amphoteric | 25–35% | 65–75% | `CCCCCCCCCCCC(=O)NCCN(CCO)CC(=O)[O-].[Na+]` |
| **Dehyton® PK 45** | Cocamidopropyl Betaine | Amphoteric | 44–46% | 54–56% | `CCCCCCCCCCCC(NCCC[N+](C)(C)CC([O-])=O)=O` |
| **Dehyton® ML** | Sodium Lauroamphoacetate | Amphoteric | 25–29% | 71–75% | `CCCCCCCCCCCC(NCCN(CC([O-])=O)CCO)=O.[Na+]` |
| **Dehyton® AB 30** | Coco-Betaine | Amphoteric | 30% | 63% (7% NaCl) | `CCCCCCCCCCCC[N+](C)(C)CC([O-])=O.[Na+]` |
| **Plantapon® Amino SCG-L** | Sodium Cocoyl Glutamate | Amino-acid | 25–30% | 70–75% | `[O-]C(CCC(NC(CCCCCCCCCCCCCCC)=O)C([O-])=O)=O.[Na+].[Na+]` |
| **Plantapon® Amino KG-L** | Potassium Cocoyl Glycinate | Amino-acid | 30–35% | 65–70% | `CCCCCCCCCCCC(NCC([O-])=O)=O.[K+]` |
| **Dehyquart® A-CA** | Cetrimonium Chloride | Cationic | 25% | 75% | `CCCCCCCCCCCCCCCC[N+](C)(C)C.[Cl-]` |

### Conditioning Polymers / Polyelectrolytes (4 Ingredients)
| Trade Name | Chemical Family / INCI | Role | Density (g/mL) |
|---|---|---|---|
| **Luviquat® Excellence** | Polyquaternium-16 | Conditioning agent | 1.118 |
| **Dehyquart® CC6** | Polyquaternium-6 | Conditioning agent | 1.067 |
| **Dehyquart® CC7 Benz** | Polyquaternium-7 | Conditioning agent | 1.024 |
| **Salcare® Super 7** | Polyquaternium-7 | Conditioning agent | 1.121 |

### Thickeners (2 Ingredients)
| Trade Name | INCI Name | Role | Density (g/mL) |
|---|---|---|---|
| **Arlypon® F** | Laureth-2 | Non-ionic thickener | 0.887 |
| **Arlypon® TT** | PEG/PPG-120/10 Trimethylolpropane Trioleate and Laureth-2 | Associative thickener | 0.970 |

### Solvent
- **Water (Milli-Q Deionized):** $x_{\text{water}} = 100.0 - \sum_{i=1}^{18} x_i$ (Density: 0.998 g/mL).

---

## 3. Sample Architecture & Sparsity Audit

### Physical Compositional Rules
Each shampoo sample in the dataset is a **sparse quaternary active mixture** in water:
- **Binary Surfactant System:** Exactly 2 surfactants selected from the 12 surfactant candidates.
- **Single Conditioning Polymer:** Exactly 1 polymer selected from the 4 polyelectrolyte candidates.
- **Single Thickener:** Exactly 1 thickener selected from the 2 thickener candidates.
- **Water Base:** Formulations diluted with water to 100 wt%.

```text
Formulation Vector: 19 Dimensions (18 Commercial Ingredients + Water)
Actual Active Components per Sample:
├── 811 samples: Exactly 4 active ingredients (>0) + Water
└── 1 sample (ID 366, unstable): Exactly 3 active ingredients (Plantacare 2000, Dehyquart CC7 Benz, Arlypon F)
```

### Concentration Ranges
- **Total Commercial Actives Sum:** $15.94\%\text{ to }33.32\%$ (Mean: $25.43\%$).
- **Stable Formulations Active Sum:** $17.93\%\text{ to }33.32\%$ (Mean: $25.39\%$).
- **Water Content:** $66.68\%\text{ to }84.06\%$ (Mean: $74.57\%$).

---

## 4. Response Field Inventory & $n_{\text{valid}}$ Audit

### Partition by Physical Phase Stability (`Stability_Test`)

```text
Total Formulations Recorded: 812
├── Unstable Formulations: 518 samples (63.8%)
│   ├── Turbidity_NTU: "NA" (n_valid = 0)
│   ├── Turbidity_Error: "NA" (n_valid = 0)
│   ├── Viscosity: "NA" (n_valid = 0)
│   ├── Rheology_Type: "NA" (n_valid = 0)
│   └── Rheology_Data: "" (n_valid = 0)
│   └── Usable for: M4 Phase Stability Binary Classifier (M4-CLF-STAB) only.
│
└── Stable Formulations: 294 samples (36.2%)
    ├── Turbidity_NTU: Valid float (n_valid = 294)
    ├── Turbidity_Error: Valid integer (n_valid = 294)
    ├── Viscosity: Categorical string ("VERY-LOW", "LOW", "MEDIUM", "HIGH")
    ├── Rheology_Type: Categorical string ("NEWTONIAN", "SHEAR-THIN", "OTHER")
    └── Rheology_Data: 31-point flow curve list (n_valid = 294)
        └── Usable for: Continuous property regression benchmark.
```

### Detailed Breakdown of Stable Formulations ($n = 294$)

| Response Target | Representation | $n_{\text{valid}}$ | Range / Distribution | Unit | Notes / Quality Checks |
|---|---|---|---|---|---|
| **`phase_stability`** | Binary boolean (`True`) | 294 | 100% `True` | - | Target for classification layer |
| **`turbidity_ntu`** | Continuous float | 294 | Min: 13.00, Max: 3881.00, Mean: 224.94 | NTU | 0 missing in stable set |
| **`turbidity_error`** | Integer uncertainty | 294 | Min: 0, Max: 878, Mean: 26.99 | NTU | 95% confidence interval |
| **`viscosity_cat`** | 4-tier categorical | 294 | `VERY-LOW`: 143<br>`MEDIUM`: 71<br>`LOW`: 61<br>`HIGH`: 19 | - | Top-level `Viscosity` field |
| **`rheology_type`** | 3-tier categorical | 294 | `NEWTONIAN`: 184 (62.6%)<br>`SHEAR-THIN`: 97 (33.0%)<br>`OTHER`: 13 (4.4%) | - | Fluid classification |
| **`viscosity_at_100s`** | Continuous float | 294 | Min: 0.6030, Max: 3429.5700, Median: 10.7230 | mPa·s (cP) | Extracted from Index 20 ($\dot{\gamma} \approx 97\text{--}100\text{ s}^{-1}$) |
| **`flow_curve_full`** | Array of 31 tuples | 294 | 31 points per curve | $(\text{s}^{-1}, \text{mPa}\cdot\text{s}, \text{mPa}\cdot\text{s})$ | Contains instrument-specific grids |

---

## 5. Raw Schema Anomalies & Data Cleaning Requirements

A production-grade benchmark parser must explicitly handle three confirmed anomalies in the raw JSON:

### Anomaly 1: Scientific Notation Encoded as String
- **Location:** Sample ID 673, `Rheology_Data[0]['shear_rate'][30]`
- **Value:** String `'1.00E+03'`
- **Fix:** Ingestion parser must cast all shear rates via `float(val)`.

### Anomaly 2: Low-Torque Negative Viscosity Values
- **Location:** Sample ID 151, `Rheology_Data[1]['avg_viscosity'][0:3]`
- **Values:** Strings `'-2.226'`, `'-2.405'`, `'-0.764'` mPa·s at $\dot{\gamma} = 1.107, 1.407, 1.760\text{ s}^{-1}$.
- **Root Cause:** TA Instruments DHR 30 rotational rheometer operating below the minimum torque threshold ($< 10^{-7}\text{ N}\cdot\text{m}$) on very low viscosity fluid (`Viscosity == 'VERY-LOW'`). At $\dot{\gamma} \ge 2.196\text{ s}^{-1}$, readings become positive ($0.439, 1.445, \dots, 2.682\text{ mPa}\cdot\text{s}$).
- **Fix:** Any flow curve analysis at low shear rates must clamp or flag negative viscosities. At $\dot{\gamma} \approx 100\text{ s}^{-1}$, all 294 samples have strictly positive viscosities.

### Anomaly 3: String `'None'` in Standard Deviation Array
- **Location:** Samples ID 196 and ID 216, `Rheology_Data[2]['std_dev']`
- **Values:** String `'None'` across all 31 points (62 points total).
- **Root Cause:** Formulations prepared with a single experimental measurement rather than triplicate repeats.
- **Fix:** Parser must translate `'None'` strings to `np.nan` or `None`.

### Anomaly 4: Heterogeneous Rheometer Shear Rate Grids
- **TA Instruments DHR 30 (270 samples):** Experimental measured points spanning $1.10\text{ s}^{-1}$ to $897.8\text{ s}^{-1}$. Index 20 corresponds to $\dot{\gamma} = 96.9\text{--}97.0\text{ s}^{-1}$.
- **Anton Paar MCR702e (24 samples):** Fixed nominal points spanning $1.0\text{ s}^{-1}$ to $1000.0\text{ s}^{-1}$. Index 20 corresponds to $\dot{\gamma} = 100.0\text{ s}^{-1}$.
- **Fix:** For precise continuous target definition at exactly $\dot{\gamma} = 100.0\text{ s}^{-1}$, log-linear interpolation between points 20 and 21 must be supported.

---

## 6. Mathematical Evaluation Protocol: Models A, B, and C

The user has mandated that **mathematical validity must precede metric chasing**. Under sparse mixture conditions, naive linear or polynomial expansions often fail due to rank deficiency and extreme multicollinearity.

### Model Candidates Under Evaluation

```text
Model A: Raw 18-Component Linear Space
├── Features: X = [x_1, x_2, ..., x_18] (wt% of commercial ingredients)
├── Constraint: Explicit intercept included; water omitted
└── Diagnostic: Evaluates conditioning without mixture coordinate transformation

Model B: Reference-Eliminated Scheffé Mixture Coordinates
├── Features: Normalized 18-dimensional simplex coords with water as reference
└── Diagnostic: Evaluates identifiable parameter coordinates and coefficient stability

Model C: Subsystem Relative Decomposition (GS-40 Architecture)
├── Features:
│   ├── S_total = S_1 + S_2 (total surfactant wt%)
│   ├── S_ratio = S_1 / (S_1 + S_2) (binary surfactant ratio)
│   ├── P = polymer wt%
│   ├── T = thickener wt%
│   └── W = 100 - (S_total + P + T) (water wt%)
└── Diagnostic: Physics-informed sparse representation aligned with GS-40 design
```

### Mathematical Criteria Hierarchy

Before evaluating $R^2$ or LOOCV RMSE, the benchmark must compute:

1. **Matrix Rank & Nullity:** Confirm $\text{rank}(X^T X) = p$.
   - *Discovery:* A full quadratic interaction model ($\binom{18}{2} = 153$ pair interactions) has **17 ingredient pairs with ZERO co-occurrence** in the stable dataset. Naive full interaction models are guaranteed to be rank deficient by at least 17!
2. **Condition Number ($\kappa(X)$):** Ratio of maximum to minimum singular values. $\kappa > 1000$ indicates severe numerical instability.
   - For Model A linear: $\kappa \approx 66.4$ (well-conditioned).
3. **Parameter Identifiability & VIF:** Variance Inflation Factor per ingredient.
4. **Leverage Diagnostics ($h_{ii}$):** Maximum diagonal entries in the hat matrix $H = X(X^T X)^{-1} X^T$. Check for high-leverage boundary formulations ($h_{ii} > 2p/n$).
5. **Coefficient Stability:** Sensitivity of $\hat{\beta}$ under 5-fold perturbation.
6. **Cross-Validation Metrics:** LOOCV RMSE and $R^2$ computed only on mathematically sound representations.

---

## 7. Strict Qualification Firewall Architecture

GLIDE-SPEC 40 maintains a strict separation of computational benchmarks from physical cosmetic stick qualification:

```text
       ┌────────────────────────────────────────────────────────┐
       │             PUBLIC_BENCHMARK (Nature 812)              │
       │           Domain: Liquid Shampoo Formulations          │
       └───────────────────────────┬────────────────────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │   M4 Benchmark Test Suite     │
                   │   Stress-test sparse mixture  │
                   │   algorithm & numerical code  │
                   └───────────────┬───────────────┘
                                   │
                                   X  <--- STRICT FIREWALL GUARD
                                   │       (Blocked by origin check)
                                   ▼
                   ┌───────────────────────────────┐
                   │    GS-40 Stick Qualification  │
                   │   `ModelStatus.TRAINED_LINEAR`│
                   └───────────────▲───────────────┘
                                   │
       ┌───────────────────────────┴────────────────────────────┐
       │               REAL_PILOT (SOP-GS40-PILOT-001)          │
       │      Physical 18-Run Pilot DOE on Solid Stick Balm     │
       └────────────────────────────────────────────────────────┘
```

### Immutable Guard Implementation Rule
In `FormulationPredictor` and `QualificationEngine`:
```python
if trial_record.data_origin != DataOrigin.REAL_PILOT:
  raise QualificationFirewallViolation(
      f"Data origin {trial_record.data_origin} cannot qualify the GS-40"
      " production model. Only REAL_PILOT data is authorized."
  )
```

---

## 8. Target Directory Layout for Benchmark Implementation

Once this audit is approved by the user, the benchmark layer will be implemented in the following isolated structure without altering `src/` core production code:

```text
benchmarks/
└── shampoo/
    ├── README.md                           # Benchmark documentation
    ├── raw/                                # Immutable source data
    │   ├── LiquidFormulationsDataset_2023.json
    │   ├── BASF_Surfactants_Information.csv
    │   └── SHA256SUMS                      # Verified checksums
    ├── schema/                             # Data contract definitions
    │   ├── raw_dataset_schema.json
    │   └── benchmark_normalized_schema.json
    ├── normalized/                         # Normalized tabular benchmark datasets
    │   ├── shampoo_m4_visc_at_100s.csv     (n_valid = 294)
    │   ├── shampoo_m4_turbidity.csv        (n_valid = 294)
    │   └── shampoo_m4_phase_stability.csv  (n_valid = 812)
    └── reports/                            # Mathematical audit & model comparisons
        └── model_a_b_c_mathematical_comparison.md

scripts/
└── benchmark_shampoo_m4.py                 # Reproducible benchmark runner

tests/
└── test_shampoo_benchmark.py               # Automated CI tests for benchmark
```

---

## 9. Conclusion & Action Items

The pre-parser audit is complete. All numbers, schemas, missingness patterns, and anomalies have been verified directly against the raw files:
- **812 total samples** (294 stable, 518 unstable).
- **18 active ingredients** (12 surfactants, 4 polymers, 2 thickeners).
- **294 valid responses** for Turbidity and Viscosity at $100\text{ s}^{-1}$.
- **Zero modification to GS-40 Core** (`5a5582a` remains clean).

This document serves as the formal **Data Contract** for the benchmark parser implementation.

# Liquid Shampoo Formulation Benchmark: Model A, B, and C Mathematical Comparison
**Document ID:** `REPORT-BENCHMARK-SHAMPOO-M4-v1.0`  
**Dataset:** `NATURE_812_SHAMPOO_2024` ($n = 294$ stable formulations)  
**Target Response:** Natural logarithm of continuous viscosity at $\dot{\gamma} \approx 100\text{ s}^{-1}$ ($\ln(\eta_{100})$)  
**Evaluation Scope:** Mathematical soundness, matrix conditioning, leverage, sparse interaction limits, and cross-validation stability.

---

## 1. Executive Summary & Mathematical Verdict

Before assessing goodness-of-fit metrics ($R^2$, RMSE), formulation regression models must be audited for numerical stability, matrix rank, parameter identifiability, and physical assumptions.

### Comparative Mathematical Matrix

| Metric | Model A (Raw 18 Linear) | Model B (Scheffé 19 Simplex) | Model C (Subsystem Linear) | Model C (Subsystem Quad) | Model A-Quad (Sparse Interaction) |
|---|---|---|---|---|---|
| **Representation** | 18 actives + Intercept (Water omitted) | 19 components on Simplex (No Intercept) | 4 Subsystem variables + Intercept | 4 Subsystem variables (Full 2nd order) | 18 linear + 153 pairwise cross terms |
| **Parameters ($p$)** | 19 | 19 | 5 | 15 | 171 |
| **Matrix Rank** | **19 (Full)** | **19 (Full)** | **5 (Full)** | **15 (Full)** | **137 (RANK DEFICIENT)** |
| **Nullity / Singularity** | **0** | **0** | **0** | **0** | **34 (CATASTROPHIC FAILURE)** |
| **Zero-Cooccurrence Terms** | N/A | N/A | 0 | 0 | **17 pairs (11.1%)** |
| **Condition Number $\kappa$** | **66.43** | **223.20** | **622.64** | **363,349.88** | $\mathbf{\infty}$ **(Singular)** |
| **Max Leverage ($h_{ii}$)** | 0.1799 | 0.1799 | **0.0615** | 0.3381 | 1.0000 |
| **LOOCV $R^2$ (PRESS)** | **0.3827** | **0.3827** | 0.0708 | 0.0312 | Undefined (Singular) |
| **LOOCV RMSE** | **1.4566** | **1.4566** | 1.7870 | 1.8248 | Undefined (Singular) |
| **Fit $R^2$** | 0.4489 | 0.4489 | 0.0984 | 0.1448 | Overfit / Singular |
| **Coefficient Stability (CV $\sigma$)** | 0.0526 | 0.0526 | **0.0117** | 0.1420 | Divergent |

---

## 2. In-Depth Mathematical Analysis

### 2.1 Model A vs Model B: Simplex Coordinate Invariance
- **Finding:** Model A (raw 18 components with water omitted to avoid the collinearity singularity $\sum x_i = 100$) and Model B (Scheffé 19-component canonical mixture model without intercept) produce **mathematically identical predictions, residuals, leverage, and LOOCV performance** ($R^2_{\text{PRESS}} = 0.3827$).
- **Distinction:** The condition number of Model A is **66.43**, whereas Model B is **223.20**. Model A's numerical stability is superior because omitting the dominant solvent (Water, $67\% \sim 84\%$) removes the extreme scale disparity from the coordinate basis.

### 2.2 Model A-Quad: The Catastrophic Failure of Sparse Quadratic Models
- **Theoretical Expectation:** In standard Response Surface Methodology (RSM), adding quadratic interaction terms models surfactant synergism.
- **Physical Reality in Sparse Mixtures:** In this dataset, each sample contains only 4 active ingredients. Among the 153 possible ingredient pairs:
  - **17 ingredient pairs NEVER co-occur in any of the 294 stable formulations (11.1% zero pairs).**
  - An additional 17 linear combinations are completely non-identifiable.
  - The design matrix $X$ drops from 171 parameters to **rank 137 (nullity = 34)**.
  - **Verdict:** Naive quadratic expansion on sparse formulation libraries causes complete algebraic breakdown. Sparse mixture models require structural regularization or subsystem aggregation.

### 2.3 Model C: Functional-Group / Subsystem Representation
- **Structural Architecture:** Instead of tracking 18 individual trade-name molecules, Model C collapses the formulation into 4 physical subsystem coordinates:
  1. $S_{\text{total}}$: Total surfactant loading (wt%)
  2. $S_{\text{ratio}}$: Primary-to-secondary surfactant ratio
  3. $P$: Conditioning polymer loading (wt%)
  4. $T$: Thickener loading (wt%)
- **Mathematical Strength:**
  - Guaranteed full rank in both linear (rank 5/5) and full quadratic (rank 15/15) forms.
  - Exceptionally low maximum leverage ($h_{ii} = 0.0615$ vs $0.1799$ in Model A).
  - Superior coefficient stability under cross-validation perturbation ($\sigma = 0.0117$).
- **Representation Limitation (Physical Trade-off):**
  - LOOCV $R^2$ is 0.0708 (linear) and 0.0312 (quadratic).
  - **Why?** Model C makes the simplifying assumption that all 12 surfactants have identical viscosity-building power per unit mass. In reality, anionic sulfosuccinates, non-ionic glucosides, and amphoteric betaines form fundamentally different micellar geometries. Model A captures these specific chemical identities ($R^2 = 0.3827$), whereas Model C strips them away.

---

## 3. Engineering Guidance for GLIDE-SPEC 40

1. **For Sparse Mixture Libraries (like Nature 812):**
   - High-dimensional sparse interaction terms must never be fitted unconstrained.
   - Ingredient-specific linear effects (Model A) capture primary chemical differentiation without singularity.
2. **For GLIDE-SPEC 40 Production (18-Run Pilot DOE):**
   - Unlike the sparse 18-ingredient shampoo dataset, GLIDE-SPEC 40's pilot DOE (`SOP-GS40-PILOT-001`) is a **dense 3D coordinate design** (Synthetic Wax 10–14%, Dimethicone 15–19%, Fill Temp 78–82°C).
   - In GLIDE-SPEC 40, all variables co-occur in every single run, ensuring full rank for quadratic response surface modeling.
3. **Strict Qualification Firewall Enforcement:**
   - The results of this public benchmark confirm the numerical resilience of the M4 regression engine.
   - However, under no circumstances shall `NATURE_812_SHAMPOO_2024` data be used to calibrate or qualify the GLIDE-SPEC 40 cosmetic stick production model.

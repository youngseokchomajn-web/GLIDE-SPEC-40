# M4 Mathematical Engine Benchmark Report (Track B Sandbox)
**Dataset:** Nature Scientific Data (2024) Liquid Shampoo Formulations
**Purpose:** Mathematical Stress-Testing of GLIDE-SPEC 40 M4 Linear Mixture Algorithms
**Isolation Guarantee:** Tested strictly in `benchmarks/shampoo/` with ZERO coupling to `src/` core.

---

## 1. Summary of Mathematical Properties

| Benchmark Target | Samples (N) | Features (D) | Sparsity (%) | Matrix Rank | Condition Number $\kappa(X)$ | OLS $R^2$ | OLS LOOCV RMSE | Best Ridge LOOCV |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Viscosity @ 100s (Log-Scale)** | 294 | 18 | 77.8% | 18 / 18 | 2.06e+01 | 0.4529 | 1.3848 | 1.3831 ($\alpha=10.0$) |
| **Viscosity @ 100s (Linear)** | 294 | 18 | 77.8% | 18 / 18 | 2.06e+01 | 0.2400 | 322.4738 | 321.9564 ($\alpha=10.0$) |
| **Turbidity NTU (Linear)** | 294 | 18 | 77.8% | 18 / 18 | 2.06e+01 | 0.3597 | 528.1290 | 527.3572 ($\alpha=10.0$) |

---

## 2. Key Mathematical Insights for GLIDE-SPEC 40 Core

1. **Full Column Rank under High Sparsity:** Even with an average 78.4% component sparsity, the 18 active ingredients maintain full column rank ($18/18$), confirming that the pseudo-inverse and OLS formulations in M4 are numerically solvable.
2. **Logarithmic Scaling for Viscosity:** Viscosity spans 4 orders of magnitude ($0.6$ to $3429.6\,\text{mPa}\cdot\text{s}$). Log-transforming $\ln(1 + y)$ brings $R^2$ to the standard range and ensures positive predictions, demonstrating why non-linear transforms are beneficial for wide-dynamic-range responses.
3. **Regularization vs. Pure OLS:** On highly sparse 18-variable spaces, L2 Ridge regularization provides measurable reductions in Leave-One-Out Cross-Validation error compared to unregularized OLS.
4. **Strict Firewall Confirmed:** This dataset functions purely as an algorithmic resilience test suite and has zero influence on the 20g Powder-in-Balm stick formulation.

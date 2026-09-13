# GLIDE-SPEC 40: Model Governance & Qualification Framework

- **Standard Authority:** SOP-GS40-GOV-001
- **Effective Version:** Rev.8.1
- **Status:** Mandatory Enforcement

---

## 1. Fundamental Principles

### Principle 1: Real GS40 Empirical Status
As of Rev.8.1, the number of physically measured GS40 production or pilot batches is **$N = 0$**.
- No automated pipeline or documentation may state or imply that the GLIDE-SPEC 40 model has completed empirical physical qualification.
- All qualification gates require physical experimental verification before production release.

### Principle 2: Definition & Scope of `VIRTUAL_PASS`
`VIRTUAL_PASS` is strictly an internal active-learning screening verdict:
- **What it means:** The candidate formulation is predicted within Rev.7.3 specifications with high statistical confidence ($\ge 90\%$ Conformal Coverage) and low Out-of-Domain distance ($D_{\text{composite}} \le 1.0$) based on available domain priors. It is eligible for physical testing deferral (**Test Waiver Candidate**).
- **What it DOES NOT mean:** It is NOT a finished product release approval, NOT a Certificate of Analysis (CoA), and NOT an FDA/KFDA/ISO regulatory qualification.

### Principle 3: Zero Synthetic Data Fallbacks in Qualification
- Qualification of the production response surrogate cannot be achieved using synthetic, simulated, or pseudo-random data.
- The qualification engine (`src/modeling/qualification_gate.py`) strictly enforces that all $N \ge 16$ required calibration runs originate from authenticated physical pilot batch records.

---

## 2. Statistical Qualification Gatekeeper (Rev 2.0 Gate)

To unlock production model status, a physical pilot dataset must pass four sequential criteria without exception:

```text
                                  REV 2.0 QUALIFICATION FIREWALL
┌────────────────────────────────────────┐
│  Gate 1: Experimental Sample Size      │  Pass: N_primary >= 16 batches, N_center >= 3 replicates
└───────────────────┬────────────────────┘
                    ▼
┌────────────────────────────────────────┐
│  Gate 2: Pure-Error Repeatability      │  Pass: Center point CV <= 4.0%
└───────────────────┬────────────────────┘
                    ▼
┌────────────────────────────────────────┐
│  Gate 3: Exact Lack-of-Fit F-Test      │  Pass: F_calc < F_crit (p-value >= 0.05)
└───────────────────┬────────────────────┘
                    ▼
┌────────────────────────────────────────┐
│  Gate 4: Predictive Accuracy           │  Pass: Cross-validated R^2 >= 0.85, 90% PI Coverage >= 85%
└───────────────────┬────────────────────┘
                    ▼
          [PRODUCTION QUALIFIED]
```

---

## 3. Active Learning Stopping Rule

Physical testing cycles must automatically cease when all of the following conditions are met:
1. **Conformal Empirical Coverage:** $\ge 90.0\%$ on out-of-fold validation sets.
2. **Conformal Prediction Interval Width:** Hardness PI width $\le 100.0\text{ gf}$, Transfer PI width $\le 0.008\text{ g}$.
3. **Composite Domain Coverage:** Formulation resides safely within the empirical hyperbox and Mahalanobis domain ($D_{\text{composite}} \le 1.0$).
4. **Acquisition Utility Threshold:** Expected Information Gain score of the next candidate falls below the cost threshold ($\text{Utility} < 1.0$).

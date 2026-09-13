# GLIDE-SPEC 40: Model Governance & Qualification Framework

- **Standard Authority:** SOP-GS40-GOV-001
- **Effective Version:** Rev.8.1
- **Status:** Mandatory Enforcement

---

## 1. Fundamental Principles

### Principle 1: Real GS40 Empirical Status & Red-Team Audit
As of Rev.8.1, the number of physically measured GS40 production or pilot batches is strictly **$N = 0$**.

| Red-Team Audit Item | Current System Status | Scientific Truth / Interpretation |
|---|:---:|---|
| **Dataset Freeze** | COMPLETED | 8 public peer-reviewed datasets frozen with DOI/license |
| **Data Provenance** | COMPLETED | 30 features mapped to 4 explicit provenance levels |
| **Git Baseline & Tag** | COMPLETED | Committed and tagged at `Rev8.1-precalibration` |
| **1M Virtual Landscape** | COMPLETED | 1,000,000 candidates screened into 5 zones |
| **Unit Test Suite** | COMPLETED (55/55) | 100% test pass on physics and calibration pipelines |
| **Public-Data Group-CV** | IMPLEMENTED | ElasticNet $R^2=1.000$, GP $R^2=0.967$ on public domain priors |
| **Conformal Coverage** | IMPLEMENTED | 94.4% ~ 100.0% coverage on held-out public folds |
| **GS40 Empirical Validation** | **NONE (N=0)** | **Zero physical batches fabricated or measured to date** |
| **Real Stick Conformal Coverage** | **NONE (N=0)** | **No physical prediction intervals confirmed on stick** |
| **Real Stick OOD Validation** | **UNVERIFIED** | **Behavior on real 28% powder / 17% wax unconfirmed** |
| **Real Formulation Prediction** | **UNVERIFIED** | **Empirical formulation accuracy pending GS40-CAL-001** |

> [!CAUTION]
> **MANDATORY SCIENTIFIC FIREWALL:**
> $R^2 = +1.000$ and $94.4\% \sim 100.0\%$ Conformal Coverage represent mathematical consistency checks on **Public Domain Priors and virtual baselines only**.
> They MUST NEVER be presented, interpreted, or cited as "GS40 product performance" or "manufacturing success". Empirical physical accuracy remains completely unvalidated until `GS40-CAL-001` is fabricated and measured.

### Principle 2: Definition & Scope of `VIRTUAL_PASS` and Zone A Evolution
`VIRTUAL_PASS` is strictly an internal computational screening verdict:
- **Canonical Definition:**
  > **Internal computational screening pass; not a product release or regulatory qualification.**
- **Scope & Operational Role:** Eligible as an internal **Test Waiver Candidate** for computational testing deferral under verified prior assumptions.
- **It DOES NOT mean:** It is NOT a finished product release approval, NOT a Certificate of Analysis (CoA), NOT a release specification QC pass, and NOT an FDA/KFDA/ISO regulatory qualification.

#### Zone A Evolutionary Lifecycle
To prevent premature release claims, Zone A follows a strict 3-stage evolutionary classification:
1. **Pre-Calibration Stage (Current, $N=0$):**
   - Designation: **`Zone A — Virtual Target Zone`**
   - Meaning: Computational target satisfying Rev.7.3 specs under public prior assumptions. Requires first physical batch calibration.
2. **Post-First-Calibration Stage ($N=1$, after `GS40-CAL-001`):**
   - Designation: **`Zone A — Confirmation Candidate`**
   - Meaning: Formulation bias-corrected by real GS40 residual data; candidate for empirical confirmation test.
3. **Multi-Batch Validated Stage ($N \ge 16$, post Rev 2.0 Gate):**
   - Designation: **`Test-by-Exception Eligible`**
   - Meaning: High empirical confidence established across pilot matrix; physical batch testing may be legally deferred.

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

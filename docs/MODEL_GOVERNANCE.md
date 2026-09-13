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

### Principle 4: Six-Stage Model Qualification Lifecycle
A single physical batch (`GS40-CAL-001`) does NOT qualify the model as "Calibrated".
Model evolution must strictly adhere to the following 6-stage lifecycle progression:

```text
1. [Prior Model] (N = 0, Pre-Calibration Baseline)
   └─ Public literature + domain priors. All predictions are virtual hypotheses.
        │
        ▼
2. [CAL-001 Domain Anchor] (N = 1, Single-Batch Baseline)
   └─ P001 manufactured and measured. Serves as first empirical anchor point.
        │
        ▼
3. [Residual Domain Adaptation] (N = 1)
   └─ Residual = Actual - Prior calculated. Empirical bias and spatial shrinkage applied.
        │
        ▼
4. [Adaptive Run #2 Selection] (N = 1 ➔ 2)
   └─ Dynamic active learning re-ranks remaining candidates to select next non-redundant test.
        │
        ▼
5. [Domain Adapted Model] (N = 2 ~ 15)
   └─ Sequential active learning batches accumulated. Spatial uncertainty progressively reduced.
        │
        ▼
6. [Production Qualification] (N >= 16)
   └─ Mandatory Rev 2.0 Gatekeeper verification (Repeatability CV <= 4%, Lack-of-Fit p >= 0.05).
```

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

---

## 4. Locked Blind External Validation Governance (`EXTERNAL_VALIDATION_SET_1`)

- **Governing Specification:** [`docs/EXTERNAL_VALIDATION_GOVERNANCE.md`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/docs/EXTERNAL_VALIDATION_GOVERNANCE.md) (SOP-GS40-VAL-001)
- **Candidate Registry:** [`data/EXTERNAL_VALIDATION_SET_1_SPEC.csv`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/data/EXTERNAL_VALIDATION_SET_1_SPEC.csv)

### Rev.8.1 Version & Dataset Topology
기존 Rev.8.1 Freeze를 임의 변경하지 않고, 아래의 엄격한 2원화 거버넌스 분기 구조를 유지합니다:

```text
Rev.8.1
  │
  ├─ DATASET_FREEZE_1
  │    └─ Purpose: Model & Domain Prior Construction (Training / Feature Scaling)
  │    └─ Status: 8 Public Datasets Frozen
  │
  └─ EXTERNAL_VALIDATION_SET_1
       └─ Purpose: Locked Blind External Generalization Testing
       └─ Status: Strictly Blind / Zero Information Leakage
```

### Core Enforcement Rules:
1. **완전한 분리 (Complete Segregation):** `DATASET_FREEZE_1`과 원천 격리되며, 현재 모델 fitting에 일체 사용되지 않은 신규 미공개/사후 공개 문헌 데이터만 후보로 등록 가능.
2. **4대 금지 (Zero Leakage):** Training 금지, Feature calibration 금지, Hyperparameter tuning 금지, Acquisition ranking tuning 금지.
3. **표본 독립성 (Formulation-Level Independence):** 행(Row) 수가 아닌 독자 배합/실험 클러스터 단위로 자유도 및 독립성 산정.
4. **사전 고정 지표 (Pre-Fixed Metrics):** $R^2$, $\text{RMSE}$, $\text{MAE}$, $\text{bias}$, $90\%$ Prediction-Interval Coverage, PI Width, OOD Classification 정합성, Calibration 기울기/절편 사전 고정.
5. **응답별 검증 분리:** Hardness/Rheology 우선 검증, Payoff/CoF는 SOP 완전 일치 시 조건부 검증, Sedimentation 별도 검증.
6. **인식론적 한계 불변:** 모델 일반화 성능 검증용이며 GS40 완제품 합격 판정이 아님. $N(\text{GS40 physical}) = 0$ 유지.
7. **실패 증거 영구 보존 (Model Failure Evidence):** 외부 검증 결과가 불량하더라도 은폐하거나 모델에 재투입하지 않고 모델의 물리적 한계 증거로 영구 보존.


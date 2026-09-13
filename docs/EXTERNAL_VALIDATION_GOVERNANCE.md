# GLIDE-SPEC 40: Locked Blind External Validation Governance

- **Standard Authority:** SOP-GS40-VAL-001
- **Effective Version:** Rev.8.1 (Extension)
- **Status:** Mandatory Enforcement / Locked Protocol
- **Target Specification:** `EXTERNAL_VALIDATION_SET_1`

---

## 1. Governance Architecture & Version Hierarchy

`EXTERNAL_VALIDATION_SET_1`은 기존 Rev.8.1의 사전 모델 학습 데이터셋(`DATASET_FREEZE_1`)과 엄격히 분리된 **블라인드 외부 검증 거버넌스(Locked Blind External Validation Governance)**입니다.

기존 Rev.8.1 Freeze의 기본 골격을 훼손하지 않으며, 아래와 같은 명확한 계층 구조를 가집니다:

```text
Rev.8.1
  │
  ├─ DATASET_FREEZE_1 (Frozen)
  │    └─ Purpose: Model / Domain Prior Construction
  │    └─ Scope: 8 Audited Public Datasets (Huynh 2020, Soft Matter 2026, etc.)
  │    └─ Status: Locked for Training & Spatial Prior Fitting
  │
  └─ EXTERNAL_VALIDATION_SET_1 (Locked Protocol)
       └─ Purpose: Locked Blind External Generalization Testing
       └─ Scope: Unseen Public Formulations & Literature Post-Freeze
       └─ Status: Strictly Blind / Zero Information Leakage
```

---

## 2. 엄격한 4대 금지 규정 (Mandatory Blind Constraints)

`EXTERNAL_VALIDATION_SET_1`에 등록되는 모든 데이터는 모델 파이프라인과의 접촉이 엄격히 차단됩니다:

1. **학습 절대 금지 (Training Prohibited):**
   - 어떠한 대리 모델(ElasticNet, RF, ET, GBR, GP 등)의 학습 세트(Fit set)에 포함되어서는 안 됨.
2. **피처 캘리브레이션 금지 (Feature Calibration Prohibited):**
   - 입력 피처 스케일러(MinMax, StandardScaler), PCA, 공간 임베딩 파라미터 갱신에 사용 불가.
3. **하이퍼파라미터 튜닝 금지 (Hyperparameter Tuning Prohibited):**
   - Cross-validation 탐색, 정규화 파라미터($\alpha$, $\lambda$), 트리 깊이, RBF 커널 길이 스케일($\ell=12.0$) 결정 등에 사용 불가.
4. **획득 랭킹 튜닝 금지 (Acquisition Ranking Tuning Prohibited):**
   - 능동학습 유틸리티 가중치, Pareto 최적화 기준, EIG(Expected Information Gain) 함수 튜닝에 사용 불가.

---

## 3. 표본 독립성 평가 원칙 (Independent Formulation Principle)

- **평가 단위의 원칙:**
  - 데이터의 독립성은 **단순 Raw Row(측정 행) 수가 아니라 독립 제형(Unique Formulation) 및 독립 실험(Independent Experiment) 단위**로 판정합니다.
- **다중 온도/노화 데이터의 격리:**
  - 단일 제형의 다중 온도 스캔이나 노화 시계열 데이터가 다수 존재하더라도, 모델의 자유도($df$) 계산 및 검증 가중치 부여 시 독립 샘플 1개(Formulation Cluster 1개)로 클러스터링하여 취급합니다.

---

## 4. 사전 고정 평가 지표 (Pre-Fixed Evaluation Metrics)

검증 결과의 체리피킹(Cherry-picking) 및 사후 지표 수정을 원천 차단하기 위해 평가 지표를 사전에 완전히 고정합니다:

| 카테고리 | 평가 지표 | 수학적 정의 / 기준 | 합격/평가 가이드라인 |
|---|---|---|---|
| **결정 계수** | $R^2$ | $1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$ | 모델의 설명력 및 상관성 평가 (타깃 $\ge 0.70$) |
| **평균 제곱근 오차** | $\text{RMSE}$ | $\sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2}$ | 이상치 민감 예측 오차 절대 크기 |
| **평균 절대 오차** | $\text{MAE}$ | $\frac{1}{n} \sum |y_i - \hat{y}_i|$ | 일반적 예측 오차 크기 |
| **예측 편향** | $\text{Bias}$ | $\frac{1}{n} \sum (y_i - \hat{y}_i)$ | Systematic Over/Under-prediction 방향성 분석 |
| **컨포멀 신뢰구간 포괄률**| **90% PI Coverage** | $\frac{1}{n} \sum \mathbf{1}[y_i \in \hat{C}_{0.90}(x_i)]$ | 공칭 90% 신뢰구간의 실제 적중률 (목표 $\ge 85.0\%$) |
| **신뢰구간 폭** | **PI Width** | $\frac{1}{n} \sum (\hat{y}_{\text{upper}} - \hat{y}_{\text{lower}})$ | 불확실성의 선명도 (과도하게 넓은 무의미한 구간 감지) |
| **OOD 분류 정합성** | **OOD Classification** | $D_{\text{composite}}(x_i) \text{ vs. Error Outlier}$ | 모델이 OOD로 경고한 샘플에서 실제 큰 오차가 발생하는지 검증 |
| **캘리브레이션 성능** | **Calibration Slope/Intercept** | $y_{\text{actual}} = \alpha + \beta \hat{y}_{\text{prior}}$ | 기울기 $\beta \approx 1.0$, 절편 $\alpha \approx 0.0$ 정합성 점검 |

---

## 5. 응답(Response)별 검증 가능성 분리 원칙

모든 물성이 동일한 신뢰 수준으로 외부 검증될 수 없으므로, 물리적 특성에 따라 3단계로 검증 가능성을 분리합니다:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [우선 검증 그룹] Hardness / Rheology / Wax-Gel Network Behavior         │
│  - 바늘 관통 경도, 항복응력, 겔-졸 전이 온도는 물리적 상동성이 높아   │
│    신규 외부 공개 데이터셋과 즉시 정량 비교 가능.                      │
├─────────────────────────────────────────────────────────────────────────┤
│ [조건부 검증 그룹] Payoff / Friction (CoF)                              │
│  - 인공피부(BioSkin) 규격, 수직 하중, 도포 속도, 온도가 당사 표준 SOP  │
│    (SOP-QC-TRSF-001, SOP-QC-COF-001)와 엄격히 호환될 때만 비교 인정.   │
├─────────────────────────────────────────────────────────────────────────┤
│ [별도 검증 그룹] Sedimentation / Anti-Settling                          │
│  - 2% 에어로실 망상구조에 의한 고온 슬러리 침강 방지는 제형 고유 물성  │
│    특성이 강하므로 일반 외부 데이터와 단순 비교 불가, 별도 프로토콜 검증│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. 과학적 방화벽 및 인식론적 한계 (Epistemic Firewall)

1. **모델 성능 검증과 제품 성능 검증의 엄격한 분리:**
   - `EXTERNAL_VALIDATION_SET_1`의 결과는 **"사전 대리 모델의 일반화 능력 및 물리학적 일관성 검증"**에만 국한됩니다.
   - 이 결과가 아무리 우수하더라도 **"GLIDE-SPEC 40 실제 스틱 제품의 성능 검증"이나 "양산 합격"으로 확대 해석하는 것을 법적/품질적으로 엄격히 금지**합니다.
2. **물리적 데이터 기준 불변:**
   - 외부 공개 데이터를 아무리 많이 검증하더라도 **$N(\text{GS40 physical}) = 0$ 상태는 100% 동일하게 유지**됩니다.
3. **CAL-001과의 관계:**
   - 외부 검증과 무관하게, 실제 `GS40-CAL-001` 제조 후에는 **오직 실제 GS40 측정값에 기반한 전용 잔차(Residual) 도메인 적응**이 독립적으로 수행됩니다.

---

## 7. 실패 데이터 보존 원칙 (Model Failure Evidence Preservation)

> [!IMPORTANT]
> **실패의 투명한 보존 (No Hiding, No Leakage):**
> 만약 `EXTERNAL_VALIDATION_SET_1`에서 특정 제형에 대해 모델의 예측 오차가 크게 발생하거나 컨포멀 커버리지가 붕괴하더라도:
> 1. 해당 데이터를 **절대로 은폐하거나 통계에서 제외하지 않습니다.**
> 2. 해당 데이터를 맞추기 위해 **모델의 가중치나 피처 구조에 즉각 재투입(Leakage)하지 않습니다.**
> 3. 이를 **"모델 실패 증거(Model Failure Evidence)"**로 영구 보존하고, 모델의 물리적 한계점(Boundary Limit)을 규명하는 핵심 자산으로 기록합니다.

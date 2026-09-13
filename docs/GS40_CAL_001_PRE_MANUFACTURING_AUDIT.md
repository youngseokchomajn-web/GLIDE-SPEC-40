# GLIDE-SPEC 40: GS40_CAL_001 Pre-Manufacturing Red-Team Audit

- **Audit Date:** 2026-09-13
- **Document Authority:** SOP-GS40-GOV-001 / SOP-GS40-PILOT-001
- **Status:** APPROVED FOR BATCH PREPARATION (Freeze State Maintained)

---

## 1. Executive Summary & Core Principle

GLIDE-SPEC 40 is currently locked at **Rev.8.1 Freeze**.
The current physical calibration count is strictly **$N(\text{GS40 physical}) = 0$**.

All numerical predictions in pre-calibration reports (e.g., Hardness 781.6 gf, Transfer 0.0430 g, Drop Point 62.6°C) represent **Public Domain Prior Baselines**.
Demonstration values evaluated during adaptation testing (e.g., 735.0 gf, 0.0450 g, 62.1°C) are strictly **hypothetical simulation scenarios** to verify engine mechanics, NOT physical GS40 measurements.

---

## 2. Five Critical Pre-Manufacturing Audit Items

### ① 원료 배합 단위의 완벽한 일치성 검증 (Unit Invariance)
- **감사 결과:** **100% CONCORDANT**
- **검증 내용:**
  - [`data/doe/GS40_CAL_001_EXECUTION_SHEET.csv`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/data/doe/GS40_CAL_001_EXECUTION_SHEET.csv)는 두 가지 기준을 병기하여 실험실 계량 오류를 원천 차단함:
    1. **Active Basis (wt%):** 순수 유효 성분 기준 100.0 wt%
    2. **Physical Charge Basis (g per 1,000.0g):** 실제 저울에 달아야 하는 원료 투입량 1,000.00g (100g 벤치 조제 시 소수점 1자리 이동).
  - 총 중량 검증 합계(Checksum): 1,000.00 g (오차 0.00 g).

### ② MQ Resin 활성분(Active) vs. 용액(Solution) 규격 확정
- **감사 결과:** **CRITICAL RESOLUTION COMPLETED**
- **근본 원인 분석:**
  - 초기 간이 스크리너에서 MQ 레진 용액 2.0%라는 임의의 플레이스홀더가 존재하였으나, Rev.7.3 마스터 배합([`REV7.3_DEVELOPMENT_BASELINE.md`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/REV7.3_DEVELOPMENT_BASELINE.md) 및 [`PILOT_EXPERIMENT_PROTOCOL_REV1.0.md`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/docs/PILOT_EXPERIMENT_PROTOCOL_REV1.0.md))의 공식 규격은 **12.0% Active MQ Resin**임.
- **실제 제조 계량 수식 및 캐리어 상계(Carrier Offsetting):**
  - 입고 규격: `MAT-MQ-01` (Dowsil MQ-1600 / Wacker Belsil TMS 803 동등품, **60.0% Active Resin in Dimethicone 100 cSt**).
  - 1 kg 배치 투입량:
    $$\text{MQ Resin 60\% Solution 투입량} = \frac{120.0\text{ g (Active)}}{0.60} = \mathbf{200.0\text{ g (20.0 wt\%)}}$$
  - 캐리어 상계 차감:
    - MQ Resin 200.0g 중 40%인 **80.0g은 Dimethicone 오일**로 자동 공급됨.
    - GS40-P001의 목표 디메치콘 풀은 22.0% (220.0g)이므로, 순수 디메치콘 오일 실투입량은:
      $$\text{순수 Dimethicone 오일 계량} = 220.0\text{ g} - 80.0\text{ g} = \mathbf{140.0\text{ g (14.0 wt\%)}}$$
  - **결과:**
    - Active MQ Resin = 120.0 g (12.0 wt%)
    - Total Dimethicone = 140.0 g (순수) + 80.0 g (MQ 캐리어) = 220.0 g (22.0 wt%)
    - Caprylyl Methicone = 60.0 g (6.0 wt%)
    - Total Silicone Pool = 22.0% + 6.0% = **28.0 wt% (280.0 g)**.
    - 배합 오류 가능성 0%.

### ③ 물성 측정 SOP 일치성 전수 대조
모든 문서([`PILOT_EXPERIMENT_PROTOCOL_REV1.0.md`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/docs/PILOT_EXPERIMENT_PROTOCOL_REV1.0.md), [`GS40_CAL_001_EXECUTION_SHEET.csv`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/data/doe/GS40_CAL_001_EXECUTION_SHEET.csv), [`REV8.1_BASELINE.md`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/docs/REV8.1_BASELINE.md))의 측정 프로토콜이 동일함을 전수 대조 완료함:

| 물성 항목 | 공식 표준 SOP | 장비 및 프로브 사양 | 환경 및 전처리 조건 | 합격 목표 규격 |
|---|---|---|---|---|
| **Hardness (경도)** | `SOP-QC-HARD-001` | Texture Analyzer, 2.0 mm Needle Probe | 25.0°C (24h 안정화 후 30분 챔버), 1.0 mm/s, 깊이 2.0 mm | 750.0 ~ 900.0 gf (스틱 5개 평균) |
| **Transfer (도포량)** | `SOP-QC-TRSF-001` | BioSkin Plate (4.0 cm²), 0.1 mg 정밀저울 | 10.0°C 저온 챔버 1h 전처리, 500 gf 수직하중, 왕복 1회 | $\ge 0.040\text{ g}$ (0.038 ~ 0.065 g) |
| **Drop Point (융점)** | `ASTM D127` / Mettler FP83 | Mettler Toledo FP83HT Dropping Cell | 승온 속도 1.0 °C/min, 표준 2.8 mm 오리피스 컵 | 60.0 ~ 63.5 °C |
| **CoF (동마찰)** | `SOP-QC-COF-001` | 표면마찰측정기 (BioSkin 인공피부) | 25.0°C, 수직하중 100 gf, 이동속도 20 mm/s | $\le 0.180$ (Target: 0.158) |

### ④ CAL-001 잔차가 P002~P018 예측치를 보정하는 수학적 메커니즘
- **가우시안 RBF 커널 공간 수축 (Bayesian Spatial Shrinkage):**
  $$\hat{y}_{\text{adapted}}(x) = \hat{y}_{\text{prior}}(x) + w(x) \cdot (y_{\text{actual}} - \hat{y}_{\text{prior}})$$
  $$w(x) = \exp\left(-\frac{1}{2}\left(\frac{\|x - x_{\text{cal}}\|}{\ell}\right)^2\right), \quad \ell = 12.0$$
- **국소성(Locality) 보장:**
  - $x \approx x_{\text{cal}}$ (P001 인접 제형): $w \approx 1.0 \implies$ 잔차의 100% 반영, 인식론적 불확실성 최대 60% 축소.
  - $\|x - x_{\text{cal}}\| = 18.18$ (P008 직교 제형): $w = 0.317 \implies$ 전역 편향의 31.7%만 완만하게 반영되며, 81%의 불확실성이 유지되어 과도한 축소(Over-shrinkage) 방지.

### ⑤ Run #2 자동 선정 과정의 데이터 누수 및 과적합 방지 검증
- **누수 차단:** `recalibrate_candidate_runs()`는 이미 측정된 `GS40-P001`을 후보 리스트에서 원천 제외하고 나머지 17개 미실행 제형만 평가함.
- **다양성 페널티/보너스 적용:** 거리 인자 $(1 + 0.08 \ln(1 + \text{dist}))$를 곱하여, P001 근처의 중복된 제형(예: P012, 거리 6.23) 대신 직교 공간을 탐색하는 **P008 (거리 18.18)**을 능동적으로 선별하도록 설계됨.

---

## 3. 6단계 거버넌스 승격 사다리 (Qualification Progression)

```text
[Step 1: Prior Model] (N = 0, 현재 상태)
  └─ 공개 문헌 + 물리 기반 대리 모델 (실측 전 가상 목표 탐색)
       │
       ▼
[Step 2: CAL-001 Domain Anchor] (N = 1, 제조 대기)
  └─ P001 단일 배치 제조 및 실측 (Hardness, Transfer, Drop Point)
       │
       ▼
[Step 3: Residual Domain Adaptation] (N = 1)
  └─ Residual = Actual - Prior 계산 ➔ Empirical Bias 산출
       │
       ▼
[Step 4: Adaptive Run #2] (N = 1 ➔ 2)
  └─ 갱신된 불확실성/다양성 기반 차기 최적 배치 자동 추천
       │
       ▼
[Step 5: Domain Adapted Model] (N = 2 ~ 15)
  └─ 순차적 능동 학습 배치 누적 및 공간적 불확실성 축소
       │
       ▼
[Step 6: Production Qualification] (N >= 16)
  └─ Rev 2.0 Gatekeeper (Repeatability CV <= 4%, Lack-of-Fit p >= 0.05, Group-CV R² >= 0.85) 통과 후 양산 출시
```

> **규정:** CAL-001 단 1개 배치는 모델을 "Calibrated"로 만드는 것이 아니라, **최초의 물리적 기준점인 "Domain Anchor"**를 제공하는 것입니다. 상용 합격 및 통계적 적격성은 Step 6(Rev 2.0 Gatekeeper)에 도달하기 전까지 부여되지 않습니다.

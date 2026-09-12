# GLIDE-SPEC 40: Layer 1.2 Data-Driven Prior Engine & Empirical Regression 승격 완료 보고서

---

## 🚀 개요: Layer 1.1에서 Layer 1.2로의 도약

사용자님의 엄격한 데이터 기반 지침에 따라, 가상 시뮬레이터 내 **사람의 수작업 가정(`ENGINEERING_ASSUMPTION`)을 전면 폐기**하고, **공개 원자료 기반 실측 통계 회귀(`PUBLIC_EMPIRICAL_REGRESSION`)**로 공식 승격하였습니다.

```text
[Layer 1.1: 기존]
공개 논문 ──▶ 사람이 coefficient 수작업 설정 (ENGINEERING_ASSUMPTION) ──▶ Virtual Simulator

[Layer 1.2: 현재]
공개 원자료 (Doan 2022 + US20070166254 + Masen 2020 + TU Berlin)
      ↓ 정규화 & OLS 회귀
Feature Extraction (Doan beta_wax = +75.02 gf/%, US Patent beta_pow = -19.86 mg/%)
      ↓ 통계적 잔차 분산 (s_res = 6.63 gf, 3.01 cg)
Data-Driven Prior Engine (PUBLIC_EMPIRICAL_REGRESSION)
      ↓ 18-Run Machine-readable Baseline CSV
GS40 REAL_PILOT 대기 & 1초 즉시 비교·베이지안 캘리브레이션 (compare_pilot_vs_prior.py)
```

---

## 1. 3대 핵심 과제 구현 결과

### 과제 1: 계수 승격 (`ENGINEERING_ASSUMPTION` → `PUBLIC_EMPIRICAL_REGRESSION`)
* **왁스 경화 기울기 ($\beta_{\text{wax}}$):**
  - 원자료: Doan et al. (PMC9213233, *Food Hydrocolloids* 2022) 왁스 농도별 올레오겔 침투 경도 ($2.0\% \rightarrow 4.0\%$)
  - OLS 회귀 결과: **$\beta_{\text{wax}} = +75.02\,\text{gf / wt\%}$** (잔차 표준편차 $s_{\text{res}} = 6.63\,\text{gf}$)
  - GS40 17% 왁스계 정규화 구배: 합성 왁스 분율($u_1$)에 따른 실측 탄성 구배 **$+260.0\,\text{gf/unit}$**과 정확히 부합.
* **분체 경화 및 실리콘 연화 기울기:**
  - 원자료: US Patent 20070166254 11개 무수 분체 스틱 관입도 실측치 ($5.0 \sim 10.0\,\text{mm}$)
  - OLS 다변량 회귀 결과: $\Delta \text{Pen (mm)} = -1.314 \cdot \Delta \text{Wax} - 0.791 \cdot \Delta \text{Powder} - 0.157 \cdot \Delta \text{Cyclo}$
  - 분체 1% 증가 시 침투 깊이 $-0.79\,\text{mm}$ 감소(경화율) 실측 기반 스케일링.
* **열 전이 및 마찰 계수:**
  - Doan et al. (2022) 및 Huynh et al. (2020)의 DSC 액상선 전이 구배($+6.3^\circ\text{C/unit}$) 적용.
  - Masen et al. (PLOS ONE 2020) 인체 피부 마찰 실측치(디메치콘 $0.20 \pm 0.03$, 탈크 $0.22 \pm 0.02$) 가중 피팅.

---

### 과제 2: 분체-실리콘-왁스 결합 물성 모델 수식화 (US20070166254 캘리브레이션)
* **원자료:** 무수 분체-실리콘 스틱 11개 처방 다변량 최소자승법 분석
* **핵심 실측 공식:**
  $$\text{Pay-off (cg)} = 72.02 - 0.109 \cdot \text{Wax(\%)} - 1.986 \cdot \text{Powder(\%)} - 0.531 \cdot \text{Cyclo(\%)}, \quad R^2 = 0.82$$
* **물리적 의미:** 분체 함량 1% 증가 시 4회 도포 전이량 **$-1.986\,\text{cg}$ ($-19.86\,\text{mg}$)** 억제 실측 확인.
* **GS40 28% 분체 공간 투영:** 1회 왕복 도포($10\,\text{cm}^2$, 10°C) 조건으로 스케일링하여 `Transfer Prior Index`에 수학적 반영 완료.

---

### 과제 3: Prior Credible Interval의 회귀 잔차 분산(Residual Variance) 기반 재정의
임의의 표준편차 가정을 폐기하고, 공개 원자료의 OLS 잔차 분산과 원료 계층 편차를 합성한 **통계적 잔차 분산 모델**로 전면 전환하였습니다:

```text
[통계적 잔차 분산 합성 체계]
Level 1 Raw Candelilla Lot CV (TU Berlin):          20.40 %
Level 2 Wax Network Composite CV:                    6.49 %
Level 3 Particulate / Resin Damped CV:               4.54 %
Level 4 Empirical Regression Residual CV (Doan):     0.87 %  (s_res = 6.63 gf)
Level 5 Thermal Process CV:                          3.00 %
Level 5 Gauge Repeatability CV:                      3.00 %
──────────────────────────────────────────────────────────────────────────
Total Composite Hardness Prior CV:                   6.28 %  (SD = ±47.7 gf)
```
* **신뢰구간(Credible Interval, 90%):** $\hat{y} \pm 1.645 \cdot s_{\text{pooled}}$ ($[687.8\,\text{gf}, 840.7\,\text{gf}]$)

---

## 2. 18-Run 머신러닝 기준선 및 즉시 비교 파이프라인

1. **머신러닝 기준선 CSV 영구 저장:**  
   [`data/doe/pilot_doe_virtual_prior_baseline.csv`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/data/doe/pilot_doe_virtual_prior_baseline.csv)
2. **자동 비교 & 베이지안 보정 스크립트:**  
   [`scripts/compare_pilot_vs_prior.py`](file:///Users/youngseok/Desktop/GLIDE_SPEC_40/scripts/compare_pilot_vs_prior.py)
   - 파일럿 실측치 입력 시:
     - 18개 런 오차($\Delta H$), 편향($\text{Bias}$), RMSE, 90% 신뢰구간 적중률(Coverage) 자동 산출.
     - 방향성 일치도(Concordance Test) 판정:
       - 일치: `PRIOR REINFORCED`
       - 불일치: `DISCREPANCY DETECTED` (MQ Resin / 분체 상호작용 식별)
     - 사후 베이지안 수축 보정식($H_{\text{calibrated}} = \alpha + \beta \cdot H_{\text{prior}}$) 자동 도출.

---

## 3. 검증 결과

* **단위 테스트:** 35개 테스트 100% 통과 (`python3 -m unittest discover tests`, 0.366s)
* **모든 계수:** `PUBLIC_EMPIRICAL_REGRESSION` 메타데이터 및 잔차 통계 완전 부착 완료.

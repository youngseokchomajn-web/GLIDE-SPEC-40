# GLIDE-SPEC 40 Pilot Experiment Protocol (Rev.1.0)
**문서 번호:** `SOP-GS40-PILOT-001`  
**제정 일자:** 2026-09-12  
**적용 대상:** GLIDE-SPEC 40 파일럿 제조, QC 시험실, 제형 연구원 및 생산 현장 작업자  
**제품 규격:** 20g Anhydrous Powder-in-Balm Solid Stick (Rev.7.3 기준)  
**목적:** M4 다변량 처방 회귀 모델의 실험적 적격성(Qualification) 획득을 위한 18개 파일럿 배치 제조 및 QC 실측 데이터 수집 표준 지침

---

## 1. 개요 및 실험 철학 (Principles & Objectives)

본 프로토콜은 GLIDE-SPEC 40 처방 시뮬레이터의 **M4 회귀 모델을 실제 물리 데이터로 검증(Empirical Qualification)**하기 위한 공식 파일럿 실험 지침서입니다.

### 🛡️ 핵심 원칙 (Non-negotiable Rules)
1. **Strict Rule #6 (No Synthetic Substitution):** 모델 적격성 평가에는 오직 실제 파일럿 제조(`REAL_PILOT`) 및 실측 QC 데이터만 사용합니다. 가상값이나 시뮬레이션 예측값의 임의 대입은 엄격히 금지됩니다.
2. **Pure-Error Replicates (3D 물리 중심점):** 실험 오차(Pure Error)와 모델 결함(Lack-of-Fit)을 통계적으로 분리하기 위해, **동일한 중심점 좌표(Synthetic Wax 12.0%, Dimethicone 17.0%, Fill Temp 80.0°C)**에서 최소 3회 이상(본 프로토콜은 4회)의 **독립적인 배치 제조 및 측정**을 수행합니다.
3. **End-to-End Lineage Traceability:** 모든 QC 레코드는 반드시 실존하는 `DOETrial`과 `ManufacturingBatch`를 참조해야 하며, 사용된 원료의 입고 Lot 및 CoA 정보가 결합되어야 합니다.

---

## 2. 실제 원료 수불 및 Lot 관리 마스터 (Raw Material Sourcing)

각 Run 제조 전, 아래 14종 원료의 시험 성적서(CoA) 및 Lot 번호를 확인하고 입고 검수를 완료해야 합니다.

| 원료 코드 | 성분명 (INCI / Trade Name) | 순도/Active | 용매/Carrier | 공급사 | 실측 Lot No. | 단가 (원/kg) | 비고 |
|:---|:---|:---:|:---:|:---|:---:|:---:|:---|
| **MAT-WAX-SYN-01** | Synthetic Wax (Microcrystalline Sub.) | 100.0% | - | Koster Keunen | *기록 요망* | ₩18,000 | 경도 지지체 |
| **MAT-WAX-CAN-01** | Candelilla Wax (Refined) | 100.0% | - | Strahl & Pitsch | *기록 요망* | ₩26,000 | 유연성 & 도포감 |
| **MAT-WAX-PEG-01** | PEG-8 Beeswax | 100.0% | - | Gattefossé | *기록 요망* | ₩35,000 | 워시오프 기능성 |
| **MAT-SIL-DIM-01** | Dimethicone (100 cSt) | 100.0% | - | Dow Corning | *기록 요망* | ₩14,000 | 베이스 실리콘 |
| **MAT-SIL-CAP-01** | Caprylyl Methicone | 100.0% | - | Siltech | *기록 요망* | ₩28,000 | 휘발성 유사 슬립 |
| **MAT-MQ-01** | Trimethylsiloxysilicate Solution | 60.0% | Dimethicone 40% | Shin-Etsu | *기록 요망* | ₩65,000 | **고형분 환산 필수** |
| **MAT-OIL-C1215-01** | C12-15 Alkyl Benzoate | 100.0% | - | Innospec | *기록 요망* | ₩12,000 | 분산제 / 가소제 |
| **MAT-POW-BN-01** | Boron Nitride (Grade CC6004) | 100.0% | - | 3M / Momentive | *기록 요망* | ₩120,000 | 고윤활 슬립 파우더 |
| **MAT-POW-SIL-01** | Porous Spherical Silica (Sunsil-130) | 100.0% | - | Sunjin Beauty | *기록 요망* | ₩45,000 | 오일/땀 흡착 |
| **MAT-POW-AER-01** | Silica Dimethyl Silylate (Aerosil R972) | 100.0% | - | Evonik | *기록 요망* | ₩55,000 | 침전 방지 요변제 |
| **MAT-POW-PMS-01** | Polymethylsilsesquioxane (Tospearl) | 100.0% | - | Kobo Products | *기록 요망* | ₩85,000 | 마이크로 볼베어링 |
| **MAT-ACT-ZNO-01** | Triethoxycaprylylsilane Zinc Oxide | 100.0% | - | Kobo Products | *기록 요망* | ₩38,000 | 소수성 표면처리 징크 |
| **MAT-ACT-EHG-01** | Ethylhexylglycerin (Sensiva SC 50) | 100.0% | - | Schülke | *기록 요망* | ₩32,000 | 체취 방어 부스터 |
| **MAT-ACT-SOOTH-01** | Soothing Blend (Bisabolol+Tocopherol) | 100.0% | - | BASF / DSM | *기록 요망* | ₩95,000 | 산패 방지 & 피부 진정 |

> [!IMPORTANT]
> **MQ Resin 투입량 환산 주의:**  
> `Target Active Formula`의 MQ Resin 유효성분은 **12.0%**입니다. 원료가 60% 솔루션(`Dimethicone 40%`)인 경우 실제 투입량은 **20.0%**이며, 이때 동반 투입되는 8.0%의 Dimethicone은 실리콘 오일 투입량에서 **자동 차감(Offset)**되어 제조 계산됩니다.

---

## 3. 표준 파일럿 제조 공정 절차 (Pilot Manufacturing SOP)

- **표준 배치 크기:** **1.0 kg (1,000.0 g)** / Run (20g 스틱 약 50개 생산)
- **QC 시편 소요량:** Run당 15개 (경도 5개, 전이량 5개, 적점 2개, 예비/보관 3개)

```
[Phase A: 왁스 용융]
Synthetic Wax + Candelilla Wax + PEG-8 Beeswax + C12-15 Alkyl Benzoate
➔ 85~90°C 가열 용융 (투명 균질상)
         ↓
[Phase B: 실리콘 & 수지 프리믹스]
Dimethicone (Offset 반영량) + Caprylyl Methicone + MQ Resin Solution
➔ 70~75°C 보온 교반
         ↓
[Phase C: 파우더 슬러리 고전단 분산]
Boron Nitride + Sunsil Silica + Aerosil + Tospearl PMSSQ + Treated ZnO
➔ Phase B에 서서히 투입 후 호모믹서 3,000 RPM × 20분 전단 분산
         ↓
[Phase D: 메인 블렌딩 & 진정 복합체 투입]
Phase A(용융 왁스)에 Phase C(파우더-실리콘 슬러리) 투입
➔ 80°C 유지 교반 10분 ➔ Ethylhexylglycerin + Soothing Blend 투입 후 탈포
         ↓
[Phase E: 지정 온도 충진 & 3단계 제어 냉각]
각 DOE Run 지정 충진 온도 (75.0°C / 80.0°C / 85.0°C ± 1°C) 도달 확인
➔ 스틱 용기에 정량 디스펜싱 ➔ 3-Step Gradual Cooling:
   ① 25°C 상온 터널: 15분 (초기 고형화)
   ② 15°C 냉각 챔버: 20분 (결정 구조 안정화)
   ③ 5°C 저온 챔버: 10분 (수축 및 이형성 확보)
```

---

## 4. 18-Run Pilot DOE Execution Matrix (실제 작업자용 제조·실험표)

모든 Run은 독립된 1.0 kg 배치로 개별 제조됩니다.

| Run No | Batch ID | DOE Trial ID | 설계 유형 | Center Point | Syn Wax (%) | Can Wax (%) | Dimethicone (%) | Caprylyl (%) | Fill Temp (°C) | 제조 상태 | 작업자 서명 |
|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **01** | `GS40-P001` | `DOE-EXP-001` | Vertex_HighSyn_HighDim | **FALSE** | 15.0 | 2.0 | 22.0 | 6.0 | **80.0** | 대기 | |
| **02** | `GS40-P002` | `DOE-EXP-002` | Vertex_HighSyn_LowDim_Tmin | **FALSE** | 15.0 | 2.0 | 12.0 | 16.0 | **75.0** | 대기 | |
| **03** | `GS40-P003` | `DOE-EXP-003` | Vertex_LowSyn_HighDim_Tmax | **FALSE** | 9.0 | 8.0 | 22.0 | 6.0 | **85.0** | 대기 | |
| **04** | `GS40-P004` | `DOE-EXP-004` | Vertex_LowSyn_LowDim | **FALSE** | 9.0 | 8.0 | 12.0 | 16.0 | **80.0** | 대기 | |
| **05** | `GS40-P005` | `DOE-EXP-005` | Axial_WaxMax | **FALSE** | 15.0 | 2.0 | 17.0 | 11.0 | **75.0** | 대기 | |
| **06** | `GS40-P006` | `DOE-EXP-006` | Axial_WaxMin | **FALSE** | 9.0 | 8.0 | 17.0 | 11.0 | **85.0** | 대기 | |
| **07** | `GS40-P007` | `DOE-EXP-007` | Axial_SilMax | **FALSE** | 12.0 | 5.0 | 22.0 | 6.0 | **75.0** | 대기 | |
| **08** | `GS40-P008` | `DOE-EXP-008` | Axial_SilMin | **FALSE** | 12.0 | 5.0 | 12.0 | 16.0 | **85.0** | 대기 | |
| **09** | `GS40-P009` | `DOE-EXP-009` | Axial_TempMin | **FALSE** | 12.0 | 5.0 | 17.0 | 11.0 | **75.0** | 대기 | |
| **10** | `GS40-P010` | `DOE-EXP-010` | Axial_TempMax | **FALSE** | 12.0 | 5.0 | 17.0 | 11.0 | **85.0** | 대기 | |
| **11** | `GS40-P011` | `DOE-EXP-011` | Interior_Low | **FALSE** | 10.5 | 6.5 | 14.5 | 13.5 | **80.0** | 대기 | |
| **12** | `GS40-P012` | `DOE-EXP-012` | Interior_High | **FALSE** | 13.5 | 3.5 | 19.5 | 8.5 | **80.0** | 대기 | |
| **13** | `GS40-P013` | `DOE-EXP-013` | **Centroid_Replicate_1** | **TRUE** | **12.0** | **5.0** | **17.0** | **11.0** | **80.0** | 대기 | |
| **14** | `GS40-P014` | `DOE-EXP-014` | **Centroid_Replicate_2** | **TRUE** | **12.0** | **5.0** | **17.0** | **11.0** | **80.0** | 대기 | |
| **15** | `GS40-P015` | `DOE-EXP-015` | **Centroid_Replicate_3** | **TRUE** | **12.0** | **5.0** | **17.0** | **11.0** | **80.0** | 대기 | |
| **16** | `GS40-P016` | `DOE-EXP-016` | **Centroid_Replicate_4** | **TRUE** | **12.0** | **5.0** | **17.0** | **11.0** | **80.0** | 대기 | |
| **17** | `GS40-P017` | `DOE-EXP-017` | Confirmation_Run_1 | **FALSE** | 12.0 | 5.0 | 17.0 | 11.0 | **78.0** | 대기 | |
| **18** | `GS40-P018` | `DOE-EXP-018` | Confirmation_Run_2 | **FALSE** | 12.0 | 5.0 | 17.0 | 11.0 | **82.0** | 대기 | |

> [!NOTE]
> - **불변 혼합비 조건(Mixture Invariants):** 모든 Run에서 Wax 합계는 **17.0%**, Silicone 합계는 **28.0%**로 고정됩니다.
> - **중심점 반복(Pure Error Replicates):** Run 13, 14, 15, 16번은 동일 처방/조건이지만 **반드시 서로 다른 날짜/교반기에서 완전히 독립된 4개 배치로 개별 제조**해야 합니다. (동일 배치를 나누어 담는 행위는 순수 오차 검증을 무효화함)

---

## 5. 1.0 kg 배치 실 투입 중량표 (Batch Weight Sheet)

Run별 고정 원료 및 가변 원료의 1,000.0g 투입 레시피입니다. (단위: g)

### ① 모든 Run 공통 고정 원료 (총 550.0 g)
- `MAT-POW-BN-01` (Boron Nitride): **30.0 g** (3.0%)
- `MAT-POW-SIL-01` (Porous Spherical Silica): **100.0 g** (10.0%)
- `MAT-POW-AER-01` (Aerosil R972): **20.0 g** (2.0%)
- `MAT-POW-PMS-01` (Tospearl PMSSQ): **80.0 g** (8.0%)
- `MAT-ACT-ZNO-01` (Treated Zinc Oxide): **50.0 g** (5.0%)
- `MAT-WAX-PEG-01` (PEG-8 Beeswax): **30.0 g** (3.0%)
- `MAT-MQ-01` (MQ Resin 60% Solution): **200.0 g** (20.0% 투입 ➔ Active 12.0% + Carrier Dimethicone 8.0%)
- `MAT-OIL-C1215-01` (C12-15 Alkyl Benzoate): **95.0 g** (9.5%)
- `MAT-ACT-EHG-01` (Ethylhexylglycerin): **5.0 g** (0.5%)
- `MAT-ACT-SOOTH-01` (Soothing Blend): **20.0 g** (2.0%)

### ② 가변 원료 투입량 (총 450.0 g) — Carrier Offset 차감 반영
*MQ Resin 200g에서 이미 80.0g의 Dimethicone이 투입되므로, 순수 Dimethicone 오일 투입량은 `(목표 Dimethicone % - 8.0%) × 10`으로 계산됩니다.*

| Run 그룹 | Syn Wax 투입(g) | Candelilla Wax 투입(g) | 순수 Dimethicone 투입(g) | Caprylyl Methicone 투입(g) | 가변 소계 (g) |
|:---|:---:|:---:|:---:|:---:|:---:|
| **01 (Vertex High/High)** | 150.0 | 20.0 | 140.0 (22.0-8.0) | 60.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **02 (Vertex High/Low)** | 150.0 | 20.0 | 40.0 (12.0-8.0) | 160.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **03 (Vertex Low/High)** | 90.0 | 80.0 | 140.0 (22.0-8.0) | 60.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **04 (Vertex Low/Low)** | 90.0 | 80.0 | 40.0 (12.0-8.0) | 160.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **05 (Axial WaxMax)** | 150.0 | 20.0 | 90.0 (17.0-8.0) | 110.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **06 (Axial WaxMin)** | 90.0 | 80.0 | 90.0 (17.0-8.0) | 110.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **07 (Axial SilMax)** | 120.0 | 50.0 | 140.0 (22.0-8.0) | 60.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **08 (Axial SilMin)** | 120.0 | 50.0 | 40.0 (12.0-8.0) | 160.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **09~10 (Axial Temp)** | 120.0 | 50.0 | 90.0 (17.0-8.0) | 110.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **11 (Interior Low)** | 105.0 | 65.0 | 65.0 (14.5-8.0) | 135.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **12 (Interior High)** | 135.0 | 35.0 | 115.0 (19.5-8.0) | 85.0 | **370.0** + 80.0(수지캐리어) = 450.0 |
| **13~16 (Centroid CP)** | **120.0** | **50.0** | **90.0 (17.0-8.0)** | **110.0** | **370.0** + 80.0(수지캐리어) = 450.0 |
| **17~18 (Confirmation)** | **120.0** | **50.0** | **90.0 (17.0-8.0)** | **110.0** | **370.0** + 80.0(수지캐리어) = 450.0 |

---

## 6. 표준 QC 물성 측정 절차서 (QC Testing SOPs)

모든 시편은 제조 후 **상온(25°C, 습도 50±5%)에서 24시간 동안 경화 안정화**를 거친 뒤 측정합니다.

### ① Hardness @ 25°C (경도 시험)
- **시험 규격:** `SOP-QC-HARD-001`
- **측정 장비:** Rheometer / Texture Analyzer (선단 지름 2.0 mm Needle Probe)
- **시험 조건:**
  - 관통 깊이(Penetration Depth): **2.0 mm**
  - 시험 속도(Test Speed): **1.0 mm/s**
  - 사전 항온 시간(Conditioning): 25.0°C 챔버에서 **30분**
- **시편당 측정 횟수:** 배치당 스틱 5개 × 각 스틱 중앙부 1회 측정 (총 5회)
- **합격 기준:** **750.0 ~ 900.0 gf** (평균값 기준)

### ② Transfer / Pay-off @ 10°C (저온 전이량 시험)
- **시험 규격:** `SOP-QC-TRSF-001`
- **시험 기재:** 인공 피부 시트 (Bio-skin substrate, 거칠기 표준화)
- **시험 조건:**
  - 도포 면적: **4.0 cm²** (2.0 cm × 2.0 cm)
  - 인가 하중: **500.0 g** 수직 하중
  - 접촉 마찰 시간: **3.0초**
  - 시험 방식: **Two-stroke 왕복 도포 (왕복 1회)**
  - 환경 챔버: **10.0°C 저온 챔버**에서 시편 1시간 전처리 후 즉시 측정
- **측정 방법:** 도포 전/후 인공 피부의 무게를 정밀 전자저울(0.1 mg 감도)로 측정하여 차이 계산
- **합격 기준:** **$\ge 0.040\text{ g}$** (저온 발림성 보장)

### ③ Drop Point (적점 시험)
- **시험 규격:** `ASTM D127` 또는 Mettler FP83 Drop Point Apparatus
- **시험 조건:** 승온 속도 **1.0°C/min**
- **목표 기준:** **60.0 ~ 63.0°C**
- *주의: 장비 사정상 미측정 시 임의의 상수를 입력하지 말고 비워둡니다 (Null 유지).*

---

## 7. 대시보드 데이터 인입 및 품질 검수 (Data Ingestion & Gate)

실험 완료 후 Streamlit 대시보드(`app/dashboard/app.py`)를 통해 데이터베이스에 등록합니다.

```
[Step 1] Tab 4: DOE Mixture Matrix
➔ 18개 DOETrial 등록 확인 (DOE-EXP-001 ~ DOE-EXP-018)
         ↓
[Step 2] Tab 3: Manufacturing Calculator & COGS
➔ Batch ID (GS40-P001 ~ P018) 생성 및 실제 계량/공정조건 커밋
         ↓
[Step 3] Tab 5: QC & SOP Station
➔ Data Origin을 반드시 [REAL_PILOT]으로 선택
➔ Hardness, Transfer, Drop Point 실측치 및 SOP 파라미터 입력 후 DB 저장
```

### ✅ 데이터 품질 검수 체크리스트 (Data Eligibility Gate)
- [ ] 1. 모든 레코드의 `data_origin == DataOrigin.REAL_PILOT` 여부
- [ ] 2. `trial_id`가 `doe_trials` 테이블에 물리적으로 존재하는지 확인
- [ ] 3. `batch_id`가 `manufacturing_batches` 테이블에 유효하게 링크되어 있는지 확인
- [ ] 4. 사용된 원료의 입고 Lot No. 및 CoA 점검이 완료되었는지 확인
- [ ] 5. 경도 SOP(프로브 2mm, 침투 2mm, 속도 1mm/s, 25°C)가 완전히 기록되었는지 확인
- [ ] 6. 전이량 SOP(인공피부, 500g, 3초, Two-stroke, 10°C)가 완전히 기록되었는지 확인
- [ ] 7. **중심점 좌표 일치 확인:** `GS40-P013 ~ P016`의 실측 좌표가 `SynWax 12.0±0.2%`, `Dim 17.0±0.2%`, `FillTemp 80.0±1.0°C` 내에 존재하는지 독립 검증

---

## 8. M4 통계적 적격성 판정 기준 (Statistical Acceptance Criteria)

18개 유효 파일럿 레코드가 인입되면, 시뮬레이터가 OLS 회귀 모델 적합 및 통계 검증을 수행합니다.

### ① 모델 적합성 지표 기준
- **결정계수 ($R^2$):** $\ge 0.85$ (물성 분산의 85% 이상 설명)
- **LOOCV RMSE (Leave-One-Out Cross-Validation):**
  - Hardness: $\le 30.0\text{ gf}$
  - Transfer: $\le 0.003\text{ g}$
- **잔차 정규성 및 등분산성:** 잔차 플롯 상 특정 패턴이 없어야 함.

### ② 중심점 기반 순수 오차(Pure Error) 및 적합 결여(Lack-of-Fit) 분리 검정
4개의 독립 중심점(`GS40-P013` ~ `GS40-P016`)으로부터 순수 실험 분산을 산출합니다:
\[
SS_{PE} = \sum_{i=1}^{n_{cp}} (y_{cp, i} - \bar{y}_{cp})^2, \quad df_{PE} = n_{cp} - 1 = 3
\]
\[
MS_{PE} = \frac{SS_{PE}}{3} \quad (\text{순수 오차 분산})
\]
모델의 잔차 제곱합($SS_E$)에서 순수 오차를 감하여 적합 결여($SS_{LOF}$)를 산출:
\[
SS_{LOF} = SS_E - SS_{PE}, \quad df_{LOF} = df_E - df_{PE}
\]
\[
F_{LOF} = \frac{MS_{LOF}}{MS_{PE}}
\]
- **판정 기준:** $p\text{-value} > 0.05$ (적합 결여가 유의하지 않아야 함 ➔ 1차 다변량 혼합 회귀 모델이 물리 현상을 왜곡 없이 타당하게 설명함을 증명).

### ③ 최종 확인 실험 (Confirmation Runs)
Run 17, 18번(`GS40-P017`, `GS40-P018`)의 실제 측정값이 M4 모델이 제시한 **95% 예측 신뢰 구간(Prediction Interval) 내에 안착**하면, 비로소:
> **`M4 Production Model: OFFICIALLY QUALIFIED`**

로 공식 승격 판정을 내리고, 다음 단계인 **M5 다목적 파레토 프론티어(NSGA-II) 최적화기** 개발로 전환합니다.

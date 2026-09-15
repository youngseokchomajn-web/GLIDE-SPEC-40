# GLIDE-SPEC 40 (초경량 테크니컬 건식 윤활 밤)
## Physical Product Development & Qualification System

> **PRODUCT DEFINITION LOCK — DO NOT MISCLASSIFY**  
> **GLIDE-SPEC 40은 소프트웨어가 아니라 실제 판매를 위한 물리적 소비자 제품입니다.**  
> **제품:** 20 g Powder-in-Balm Technical Anti-Chafing Stick  
> **주기능:** 장시간 신체활동 중 마찰 감소 및 쓸림(Chafing) 방지  
> **주요 사용:** 러닝·마라톤/트레일 및 군장 행군 등 장시간 활동  
> **초기 생산 목표:** 3,000개  
> **명시적 제외:** Simulator / Simulation Software / Simulation Service / Formulation-Prediction SaaS / AI Formulation Platform  
> 저장소의 시뮬레이터·회귀·DOE·벤치마크·Qualification 코드는 **물리 제품을 개발·최적화·검증하기 위한 개발 도구**이며 상용 제품 자체가 아닙니다. 상세 정의는 [`PRODUCT_DEFINITION_LOCK.md`](./PRODUCT_DEFINITION_LOCK.md)를 기준으로 합니다.

> **Official Project Stage:** `Phase C — Physical Pilot Execution / Statistical Qualification Pending`  
> **Engineering Framework Status:** `Frozen at Commit e71f2b0; Qualification Engine Operational`  
> **Production Model Status:** `NOT QUALIFIED (Awaiting Real Pilot Experimental Data)`  
> **Product Baseline:** Rev.7.3 (원료 선정 · 생산배합 · QC 개발 기준서)  
> **Target Application:** 20kg 완전군장 40km 행군 장병 및 42.195km 풀코스/트레일 마라토너 (사타구니/겨드랑이/발바닥 쓸림 원천 방어)  
> **Product Architecture:** 20g Powder-in-Balm Technical Anti-Chafing Stick  
> **Target COGS:** ₩2,950 / 20g 완제품 (현재 벌크 원료 원가: 약 ₩815 ~ ₩2,610 / 스틱)  
> **Test Suite Coverage:** **31 Unit Tests 100% Pass** (`Ran 31 tests in 0.34s - OK`)

---

## 📂 프로젝트 핵심 문서 및 데이터 자산

| 구분 | 문서/자산 | 파일 경로 | 설명 |
|---|:---|:---|:---|
| **제품 실험** | **파일럿 18-Run 실험 프로토콜 Rev.1.0** | [`docs/PILOT_EXPERIMENT_PROTOCOL_REV1.0.md`](./docs/PILOT_EXPERIMENT_PROTOCOL_REV1.0.md) | `SOP-GS40-PILOT-001`. 18개 배치 제조/QC 공식 작업지침서 |
| **제품 실험** | **파일럿 18-Run 실행 매트릭스 CSV** | [`data/doe/pilot_doe_run_matrix_rev1.0.csv`](./data/doe/pilot_doe_run_matrix_rev1.0.csv) | 무작위 제조 순서(`Execution_Order #01~#18`) 및 실측치 기록 시트 |
| **벤치마크** | **Nature 812 샴푸 데이터 전수 감사록 v0.1** | [`docs/SHAMPOO_812_DATASET_AUDIT_v0.1.md`](./docs/SHAMPOO_812_DATASET_AUDIT_v0.1.md) | 원본 해시, $n_{\text{valid}}$, 이상치, 수리 모델 비교 데이터 계약서 |
| **벤치마크** | **공개 벤치마크 레이어 개요** | [`benchmarks/shampoo/README.md`](./benchmarks/shampoo/README.md) | 812 데이터 불변 저장소, 정규화 CSV 및 방화벽 선언 |
| **벤치마크** | **Model A/B/C 수리 비교 보고서** | [`benchmarks/shampoo/reports/model_a_b_c_mathematical_comparison.md`](./benchmarks/shampoo/reports/model_a_b_c_mathematical_comparison.md) | 18성분 심플렉스/희소 교호작용 파탄 및 기능군 축소 비교 |
| **엔지니어링** | **개발 로드맵 및 상태 스냅샷** | [`DEVELOPMENT_PLAN.md`](./DEVELOPMENT_PLAN.md) | Phase 0 ~ Phase C 단계별 자격 승격 기준 및 이력 관리 |
| **공정 스펙** | **원료사 스펙 공식 요청서** | [`docs/MATERIAL_SPEC_REQUEST_SHEET.md`](./docs/MATERIAL_SPEC_REQUEST_SHEET.md) | OEM 및 원료 공급사에 발송 가능한 공식 스펙 요청서 |
| **공정 스펙** | **원료사 회신용 CSV 템플릿** | [`data/raw_materials/supplier_spec_template.csv`](./data/raw_materials/supplier_spec_template.csv) | Active %, Carrier, 단가, 입도 회신용 표준 스프레드시트 |
| **제품 기준** | **Rev.7.3 개발 기준서** | [`REV7.3_DEVELOPMENT_BASELINE.md`](./REV7.3_DEVELOPMENT_BASELINE.md) | 공식 Baseline. Target Active Formula 및 QC SOP 요건 |

---

## 🛡️ 시스템 검증 구조 및 자격 방화벽 (Qualification Firewall)

GLIDE-SPEC 40은 **공개 벤치마크 데이터**와 **실제 제품 자격 데이터**를 엄격히 분리합니다:

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
                                   │       (Blocked by DataOrigin check)
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

### 공개 벤치마크 (Phase B) 핵심 결론
- **샴푸 데이터로 GS-40 스틱 모델을 학습하거나 처방을 유도할 수 없음:**
  - Model A (Raw 18-Component Linear): LOOCV $R^2 \approx 0.383$ (주효과 모델링 가능)
  - Model C (Subsystem 4-dim): LOOCV $R^2 \approx 0.071$ (화학적 특이성 손실)
  - Raw 18-Component Quadratic: 17개 미발생 성분쌍으로 인해 행렬이 완전 결손(Singular)되어 계산 불가
- **역할 정의:** 812 데이터는 알고리즘/회귀 엔진의 수치 안정성 검증용 시험장일 뿐이며, 제품 생산 모델의 훈련 데이터로 사용할 수 없습니다.

---

## 🏭 Phase C: 연구실 물리 제조 및 통계적 승격 가이드라인

### 1. 원료 Lot 및 실측 CoA 전수 추적
단순히 MQ 수지만 확인하는 것이 아니라, 제조에 투입되는 모든 원료의 Lot 및 실측치를 기록합니다:
- **MQ Resin Solution:** 실측 불휘발분(Solids %), 캐리어 순도/점도, Lot No., CoA No.
- **Dimethicone:** 실제 투입 Grade(동점도 cSt), 수분 함량, Lot No.
- **Synthetic Wax:** 융점(Melting Point 실측치), Lot No., CoA No.
- **Candelilla Wax & 고정 원료:** 유효 활성도 및 공급사 성적서 일련번호
- **실제 칭량값(Actual Charge g):** 1,000.0g 조제 시 소수점 둘째 자리(0.01g) 실측 계량값

### 2. 목표값과 실제값의 이중 보존 (Target vs. Actual Split)
장비 오버슈트나 믹싱 편차를 감추지 않고 독립 보존합니다:
- `Fill_Temp_Target`: DOE 설계 의도 온도 (예: 80.0°C)
- `Fill_Temp_Actual`: 몰드 주입 직전 열전대 실측 온도 (예: 81.7°C, 편차 +1.7°C 기록 보존)
- *통계적 목적:* 설계상의 온도 주효과와 공정 노이즈의 영향을 분리 추정하기 위함.

### 3. 무작위 제조 순서(`Execution_Order`) 준수
- `Run_No`(P001~P018)와 `Execution_Order`(#01~#18)를 혼동하지 않고 제조합니다.
- **중심점 4회(`P013`~`P016`) 독립 분산 제조:**
  - `P013` (제조 순서 **#03**)
  - `P014` (제조 순서 **#09**)
  - `P015` (제조 순서 **#15**)
  - `P016` (제조 순서 **#18**)
  - 단일 1kg 배치를 소분하는 것을 엄격히 금지하며, 일자별/작업자별 **순수오차(Pure Error)**를 산출하기 위해 반드시 4회의 독립 1.0kg 조제 공정을 수행합니다.

### 4. Phase C 데이터 수집 5대 불변 원칙 (Immutable Rules)
1. **새로운 모델을 만들지 않는다.** (추가 코드 작성 및 조기 튜닝 일체 중단)
2. **공개 데이터를 GS-40 모델에 섞지 않는다.** (812 샴푸 데이터는 방화벽 너머에 격리)
3. **실제 데이터를 좋게 보이도록 수정하지 않는다.** (측정 이상치, 편차 원형 보존)
4. **DOE에서 발생한 실제 편차를 삭제하지 않는다.** (Target vs. Actual 완벽 분리 기록)
5. **Qualification을 미리 가정하지 않는다.** (18개 Run이 입력되었다고 자동 승격되지 않음)

---

## 📊 실측 데이터 입고 시 통계 심사 파이프라인

[`scripts/run_gs40_pilot_qualification.py`](./scripts/run_gs40_pilot_qualification.py) 실행 시 다음 다차원 통계 심사를 거쳐 최종 PASS/FAIL을 판정합니다:

```text
실측 18-Run QC 데이터 (CSV)
            ↓
scripts/run_gs40_pilot_qualification.py
            ↓
[1. 원자료 무결성 & Lineage]  DOETrial ➔ ManufacturingBatch ➔ BatchQCRecord 참조 제약
            ↓
[2. Pure Error 분석]         중심점 4회(P013~P016) 독립 배치의 공정/측정 변동량(MS_PE) 산출
            ↓
[3. Lack-of-Fit 검정]        잔여 분산과 순수오차 분산 비교 (F = MS_LOF / MS_PE)
            ↓
[4. 다변량 선형 회귀]         혼합비 좌표계(u1, v1, T) 기반 유효 모수 추정
            ↓
[5. LOOCV & 잔차 진단]       R², R²_adj, PRESS, 레버리지(h_ii), 이상치 진단
            ↓
     [PASS / FAIL 판정]
            ├── FAIL: 모델 미승격 (AWAITING_PILOT_DATA 유지, 편차 원인 규명)
            └── PASS: 1차 자격 획득 (TRAINED_LINEAR)
                     ↓
          [6. Confirmation Run] 독립 검증 배치 1회 수행
                     ↓
          GS-40 Production Model 최종 승격 (Production Qualified)
```

---

## 🚀 실행 및 테스트 가이드

### 1. 전체 단위 테스트 스위트 (31개 100% Pass)
```bash
python3 -m unittest discover -s tests -v
```
- Core Unit Tests (26개) + Public Benchmark & Firewall Tests (5개) = **31/31 통과**

### 2. 샴푸 공개 벤치마크 러너 실행
```bash
python3 scripts/benchmark_shampoo_m4.py
```
- 812개 JSON 무결성 검증, 정규화 CSV 3종 생성, Model A/B/C 수리 진단 리포트 자동 생성.

### 3. 파일럿 QC 데이터 투입 및 자격 심사 러너 실행
```bash
python3 scripts/run_gs40_pilot_qualification.py --matrix data/doe/pilot_doe_run_matrix_rev1.0.csv
```
- 물리 데이터 미입력 시: `STATUS: AWAITING_PILOT_DATA (0/16 required)` 보고 및 자동 승격 차단.
- 물리 데이터 입력 완료 시: 순수오차, Lineage, 회귀, LOOCV 종합 PASS/FAIL 심사 수행.

### 4. 대시보드 구동
```bash
streamlit run app/dashboard/app.py
```

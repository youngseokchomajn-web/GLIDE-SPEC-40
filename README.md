# GLIDE-SPEC 40 (초경량 테크니컬 건식 윤활 밤)
## Formulation Simulator & Development System (v1.0 Production Release)

> **Current Product Baseline:** Rev.7.3 (원료 선정 · 생산배합 · QC 개발 기준서)  
> **Simulator Version:** v1.0 Production Release (Full Architecture M0 ~ M6 Complete)  
> **Target Application:** 20kg 완전군장 40km 행군 장병 및 42.195km 풀코스/트레일 마라토너 (사타구니/겨드랑이/발바닥 쓸림 원천 방어)  
> **Product Architecture:** 20g Powder-in-Balm Technical Anti-Chafing Stick  
> **Target COGS:** ₩2,950 / 20g 완제품 (현재 벌크 원료 원가: 약 ₩815 ~ ₩2,610 / 스틱)  
> **Test Coverage:** 23 Unit Tests 100% Pass (`tests/test_simulator_core.py`)

---

## 📂 프로젝트 문서 및 데이터 자산

| 문서/자산 | 파일 경로 | 설명 |
| :--- | :--- | :--- |
| **개발 로드맵 및 최종 감사록** | [`DEVELOPMENT_PLAN.md`](./DEVELOPMENT_PLAN.md) | Phase 0 ~ Phase 6 전 단계 완료 기록 및 데이터 무결성 보증서 |
| **원료사 기술스펙(TDS/CoA) 공식 요청서** | [`docs/MATERIAL_SPEC_REQUEST_SHEET.md`](./docs/MATERIAL_SPEC_REQUEST_SHEET.md) | OEM 및 원료 공급사에 즉시 발송 가능한 공식 스펙 요청서 |
| **원료사 회신용 CSV 템플릿** | [`data/raw_materials/supplier_spec_template.csv`](./data/raw_materials/supplier_spec_template.csv) | Active %, Carrier, 단가, 입도 회신용 표준 스프레드시트 |
| **Rev.7.3 개발 기준서** | [`REV7.3_DEVELOPMENT_BASELINE.md`](./REV7.3_DEVELOPMENT_BASELINE.md) | 공식 Baseline. Target Active Formula 및 QC SOP 요건 |
| **Rev.7.1 기술이전 마스터** | [`PROJECT_HANDOVER_MASTER_Rev7.1.md`](./PROJECT_HANDOVER_MASTER_Rev7.1.md) | 초기 컨셉 및 공학적 기초 사양 요약서 |

---

## ⚙️ 시뮬레이터 시스템 아키텍처 (M0 ~ M6)

```text
                        GLIDE-SPEC 40 (Rev.7.3 Baseline)
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           │                                                       │
    RAW MATERIAL MASTER                                     FORMULA MASTER
   (src/materials/master.py)                              (src/formulas/master.py)
    • TBD Gatekeeper (미확정 원료 차단)                    • Rev.7.3 Target Active (100.0%)
    • Active %, Carrier, 단가, CoA 검증                   • Powder System 28.0% 로딩 관리
           │                                                       │
           └───────────────────────────┬───────────────────────────┘
                                       ↓
                         MANUFACTURING CALCULATOR & COGS
                        (src/manufacturing/calculator.py)
    • CompositeMaterial Aggregation Layer (혼합물 왁스/실리콘을 개별 원료 투입비율로 지능형 분해)
    • Active% -> Manufacturing Charge% 자동 변환 (MQ 12% @ 60% active -> 20%)
    • 지능형 Carrier Offsetting (MQ 용매 실리콘을 메인 실리콘 캐리어에서 자동 차감)
    • Batch Scaler (100g Lab ~ 66kg Initial Charge Pilot Batch)
    • 실시간 COGS 및 견적 상태(quote_status, cogs_basis) 추적
                                       │
           ┌───────────────────────────┴───────────────────────────┐
           ↓                                                       ↓
   ADVANCED MIXTURE DOE                                       QC & SOP SYSTEM
    (src/doe/engine.py)                                     (src/qc/models.py)
    • Parameterized DOE Engine (DOEConfig)                  • Hardness @25C (750~900 gf)
    • Mixture Invariants: Wax 17%, Silicone 28%             • Pay-off @10C (>= 0.040 g)
    • Vertices, Axials, Interiors & Centre-points           • 2mm 니들 침투 & 인공피부 마찰 SOP 영구 결합
    • 순수오차 검증용 중심점(>= 3 replicates) 자동 배치    • Pass / Fail / Marginal 자동 판정
           │                                                       │
           └───────────────────────────┬───────────────────────────┘
                                       ↓
                    SQLITE REPOSITORY & REVISION PERSISTENCE
                              (src/storage/db.py)
    • Schema v4 트랜잭션 테이블 마이그레이션 (Physical Foreign Keys: ON CONFLICT DO UPDATE)
    • 완결된 디지털 계보 추적: DOETrial ➔ ManufacturingBatch ➔ BatchQCRecord
    • Formula Revision History 영구 보존 및 Rev.7.3 8대 핵심 변경점(NEW-01 ~ NEW-08) 사전 시딩
                                       ↓
                  MULTIVARIATE REGRESSION ENGINE (M4) & OPTIMIZER (M5)
                  (src/modeling/regression.py & src/optimization/optimizer.py)
    • OLS 다변량 회귀 및 투영 행렬 기반 LOOCV RMSE / R² 실시간 산출
    • 공선성 방지 혼합비 좌표계: u1 = SynWax/17.0, v1 = Dimethicone/28.0, T = FillTemp
    • 엄격한 ML 승격 안전 게이트: >= 16개 유효 실측 파일럿 데이터 + >= 3개 중심점 충족 시에만 TRAINED_LINEAR 전환
    • Rule #12 필수 준수: "Predicted (n=X samples), NOT experimental measurement" 명시
    • SLSQP 기반 3대 Pareto Frontier 전략 시나리오 (Balanced, High-Slip Summer, High-Payoff Winter)
                                       ↓
                             STREAMLIT WEB DASHBOARD
                              (app/dashboard/app.py)
    • 브라우저 기반 GUI: Formula, 원료 Spec 수정, 배치 생산 커밋, DOE 생성, QC Station, SLSQP 최적화 & Revision 추적
```

---

## 🛡️ 품질 보증 & 안전 철학 (Core Principles)

1. **Rule #6 (Strict Grounding):** 실제 파일럿 QC 실측 데이터가 충족되기 전까지는 어떠한 기계학습 물성 예측도 임의로 가정하지 않습니다 (16개 미만 시 `AWAITING_PILOT_DATA` 상태 유지 및 물리적 경계 기반 Rule-based 후보 제시).
2. **Rule #12 (Explicit Labeling):** 모델이 승격된 후 출력되는 모든 예측값은 반드시 `"Predicted (n=X real Pilot observations, LOOCV RMSE: ...), NOT experimental measurement."` 라벨을 동반합니다.
3. **Lineage Referential Integrity:** 제조 배치(`ManufacturingBatch`)는 반드시 설계 시험(`DOETrial`)을 참조해야 하며, 품질 기록(`BatchQCRecord`)은 반드시 실존하는 제조 배치를 참조해야만 영구 저장됩니다.

---

## 🚀 실행 및 사용 가이드

### 1. 전체 단위 테스트 스위트 실행
```bash
python3 -m unittest discover tests
```
* **23개 핵심 단위 테스트 100% 정상 통과 (Ran 23 tests in ~0.12s - OK)**

### 2. 통합 CLI 시뮬레이션 데모 실행
```bash
python3 scripts/run_rev73_calculator.py
```
* 66kg 파일럿 배치 원료 투입표, 20g 스틱당 원가(₩815.0), 16개 DOE 매트릭스, SQLite 완결 계보 저장, SLSQP 최적화 후보 출력.

### 3. 브라우저 기반 Streamlit 대시보드 구동
```bash
streamlit run app/dashboard/app.py
```
* 웹 브라우저(`http://localhost:8501`)에서 대화형 대시보드 실행:
  - 1. Target Active Formula
  - 2. Raw Material Master (TBD Gate)
  - 3. Manufacturing Calculator & COGS (Batch Commit to DB)
  - 4. DOE Mixture Matrix
  - 5. QC & SOP Test Station
  - 6. SLSQP Optimizer & Revision Tracker (Schema v4 DB Viewer)

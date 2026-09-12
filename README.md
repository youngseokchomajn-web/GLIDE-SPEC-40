# GLIDE-SPEC 40 (초경량 테크니컬 건식 윤활 밤)
## Formulation Simulator & Development System (v0.2 Full Suite)

> **Current Product Baseline:** Rev.7.3 (원료 선정 · 생산배합 · QC 개발 기준서)  
> **Simulator Version:** v0.2 (Complete Engine Suite: M0 ~ M6)  
> **Target Application:** 20kg 완전군장 행군 장병 및 42.195km 풀코스/트레일 러너  
> **Product Architecture:** 20g Powder-in-Balm Technical Anti-Chafing Stick  
> **Target COGS:** ₩2,950 / 20g 완제품 (현재 Bulk 원료 원가: 약 ₩815.0 / 27.6% 예산 소진)

---

## 📂 프로젝트 문서 및 데이터 자산

| 문서/자산 | 파일 경로 | 설명 |
| :--- | :--- | :--- |
| **원료사 기술스펙(TDS/CoA) 공식 요청서** | [`docs/MATERIAL_SPEC_REQUEST_SHEET.md`](./docs/MATERIAL_SPEC_REQUEST_SHEET.md) | **OEM 및 원료 공급사에 즉시 발송 가능한 공식 스펙 요청서** |
| **원료사 회신용 CSV 템플릿** | [`data/raw_materials/supplier_spec_template.csv`](./data/raw_materials/supplier_spec_template.csv) | Active %, Carrier, 단가, 입도 회신용 스프레드시트 |
| **시뮬레이터 개발 명세서 (Handoff)** | [`docs/FORMULATION_SIMULATOR_SPEC_v0.1.md`](./docs/FORMULATION_SIMULATOR_SPEC_v0.1.md) | 시스템 아키텍처, 14대 절대 금기, 개발 철학 |
| **Rev.7.3 개발 기준서** | [`REV7.3_DEVELOPMENT_BASELINE.md`](./REV7.3_DEVELOPMENT_BASELINE.md) | 공식 Baseline. Target Active Formula, QC SOP 요건 |
| **Rev.7.1 기술이전 마스터** | [`PROJECT_HANDOVER_MASTER_Rev7.1.md`](./PROJECT_HANDOVER_MASTER_Rev7.1.md) | 초기 컨셉 및 공학적 기초 사양 요약서 |

---

## ⚙️ 시뮬레이터 시스템 모듈 구조 (M0 ~ M6)

```text
                    GLIDE-SPEC 40 (Rev.7.3 Baseline)
                                  │
          ┌───────────────────────┴───────────────────────┐
          │                                               │
   RAW MATERIAL MASTER                             FORMULA MASTER
  (src/materials/master.py)                      (src/formulas/master.py)
   • TBD Gatekeeper (미확정 원료 차단)           • Rev.7.3 Target Active (100.0%)
   • Active %, Carrier, 단가, CoA                • Powder System 28.0% 로딩 관리
          │                                               │
          └───────────────────────┬───────────────────────┘
                                  ↓
                     MANUFACTURING CALCULATOR & COGS
                   (src/manufacturing/calculator.py)
   • Active% -> Manufacturing Charge% 자동 변환 (MQ 12% @ 60% active -> 20%)
   • 지능형 Carrier Offsetting (MQ 용매 실리콘을 메인 실리콘 캐리어에서 자동 차감)
   • Batch Scaler (100g Lab ~ 66kg Initial Charge Candidate)
   • 실시간 COGS 계산 (20g 스틱당 내용물 원가 및 ₩2,950 예산 대비 소진율 추적)
                                  │
          ┌───────────────────────┴───────────────────────┐
          ↓                                               ↓
  ADVANCED MIXTURE DOE                                QC & SOP SYSTEM
   (src/doe/engine.py)                             (src/qc/models.py)
   • Wax Mixture (Syn + Can = 17%)                 • Hardness @25C (750~900 gf)
   • Silicone Mixture (Dim + Cap = 28%)            • Pay-off @10C (>= 0.040 g)
   • Process Candidates (75, 80, 85°C)             • 필수 SOP 측정 조건 영구 결합
   • 12개 직교 파일럿 실험 매트릭스               • Pass / Fail / Marginal 자동 판정
          │                                               │
          └───────────────────────┬───────────────────────┘
                                  ↓
                    SQLITE PERSISTENCE & REPOSITORY
                        (src/storage/db.py)
   • 원료 카탈로그 JSON 및 시험 이력 SQLite DB (qc_records) 관리
                                  ↓
                    MULTI-OBJECTIVE OPTIMIZER
                   (src/optimization/optimizer.py)
   • Rule-based & Pareto 최적화 후보 제형 생성 (Rev.7.4 Candidate 01~03)
                                  ↓
                      STREAMLIT WEB DASHBOARD
                      (app/dashboard/app.py)
   • 브라우저 기반 GUI: Formula, 원료 Spec 수정, 배치 계산, DOE, QC Station
```

---

## 🚀 실행 및 사용 가이드

### 1. 전체 엔진 검증 테스트 (Unit Test Suite)
```bash
python3 -m unittest discover tests
```
* 7개 핵심 단위 테스트 100% 정상 통과 (Formula Sum, Charge 변환, TBD Gatekeeper, COGS, DOE 제약식, SQLite 저장, Optimizer).

### 2. 통합 CLI 시뮬레이션 데모 실행
```bash
python3 scripts/run_rev73_calculator.py
```
* 66kg 배치 투입량, 20g 스틱당 원가(₩815.0), 12개 직교 DOE 매트릭스, SQLite 시험 기록, Rev.7.4 최적화 후보 출력.

### 3. 브라우저 기반 Streamlit 웹 GUI 실행
```bash
python3 -m pip install streamlit pandas  # (필요 시 패키지 설치)
streamlit run app/dashboard/app.py
```
* 포트 `http://localhost:8501`에서 대화형 대시보드 구동.

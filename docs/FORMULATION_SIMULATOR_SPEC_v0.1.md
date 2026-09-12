# GLIDE-SPEC 40 Formulation Simulator

## Development Handoff / Project Continuation Document

**Project:** GLIDE-SPEC 40  
**Current Product Revision:** Rev.7.3  
**Simulator Development Version:** v0.1 — Development Preparation  
**Purpose:** 화장품/기술성 스틱 제형의 원료 선정 → 제조배합 계산 → DOE → QC 결과 → 물성 모델링 → 최적화 → Revision 관리

---

# 1. 프로젝트 목적

GLIDE-SPEC 40은 다음 구조의 기술성 스틱 제품이다.

* 20 g Stick
* Anhydrous 계열 Powder-in-Balm Stick
* 마찰 감소 및 피부 쓸림 방지 목적
* 주요 타깃: 러너 / 장거리 활동 / 군장 행군
* 목표 특성:
  * 저마찰
  * 보송한 마무리
  * 지속성
  * 전이 억제
  * 적절한 저온 Pay-off
  * 생산 안정성

현재 Rev.7.3은 제품 구조를 새로 설계하는 단계가 아니다.
**실제 원료와 제조공정으로 연결하기 위한 기준선**이다.

따라서 Simulator도 제품을 임의로 재설계하는 AI가 아니라,

> **Rev.7.3 기준 → 실제 원료 데이터 → Manufacturing Formula → 실험 → QC → 모델 → 최적화 → 다음 Revision**

의 폐루프를 구축하는 것이 목적이다.

---

# 2. 가장 중요한 개발 원칙

## 2.1 Active Formula와 Manufacturing Formula를 반드시 분리한다.
예:
* MQ Resin 목표 active = 12%
* 실제 원료가 60% active라면: $12 \div 0.60 = 20\%$
* 따라서 Manufacturing Formula에는 실제 원료를 20% 투입한다.
* Simulator는 이 계산을 자동화해야 한다.

## 2.2 실제 원료 Spec이 없는 상태에서 Manufacturing Formula를 확정하지 않는다.
다음 정보가 확보되어야 한다:
* Supplier, Trade Name, Grade, INCI, Active %, Carrier, Solvent, Moisture, Density, Viscosity, Particle Size, Surface Treatment, TDS, SDS, CoA, 제조사 권장 사용량.
* 정보가 없는 원료는 `TBD` 상태로 유지한다.

## 2.3 목표값과 확정값을 구분한다.
* 예: 80°C 충전은 현재 확정값이 아님 $\rightarrow$ `80°C = Initial Process Candidate`
* Simulator에서도 이를 확정값으로 취급하면 안 된다.

## 2.4 모든 Revision 변경을 기록한다.
* 반드시 다음 흐름을 유지한다: `Rev.7.3 → 실험 → 결과 → 변경 이유 → Rev.7.4`
* 변경된 항목은 최소한 다음을 기록한다: Added, Modified, Deleted, Previous Value, New Value, Reason, Experimental Evidence, Date, Related Batch.

---

# 3. Rev.7.3 Target Active Formula

| 원료군 | Target | 비고 |
| :--- | :---: | :--- |
| **Boron Nitride** | 3.0% | 판상 윤활 |
| **Porous Spherical Silica** | 10.0% | 피지/땀 흡착 |
| **Silica Dimethyl Silylate** | 2.0% | 침전 방지/요변성 |
| **Polymethylsilsesquioxane** | 8.0% | 볼베어링 하중 분산 |
| **Treated Zinc Oxide** | 5.0% | 무기 피막 |
| **Synthetic Wax + Candelilla Wax** | 17.0% | 하드 왁스 시스템 |
| **PEG-8 Beeswax** | 3.0% | 이지 워시오프 |
| **Dimethicone + Caprylyl Methicone** | 28.0% | 경량 실리콘 캐리어 |
| **MQ Resin** | **12.0% active** | 초강력 방수 피막 |
| **C12-15 Alkyl Benzoate** | 9.5% | 분산제/가소제 |
| **Ethylhexylglycerin** | 0.5% | 데오 부스터 |
| **Bisabolol + Stearyl Glycyrrhetinate + Tocopherol + Rosemary Extract** | 2.0% | 진정/산패방지 |
| **Total** | **100.0%** | |

---

# 4. 현재 미확정 원료군

## 4.1 Wax — 17%
* `Synthetic Wax + Candelilla Wax = 17%` (세부 비율 미확정)
* 목적: 25°C Hardness, 저온 Pay-off, Transfer, Stick integrity 균형 확보.

## 4.2 Silicone — 28%
* `Dimethicone + Caprylyl Methicone = 28%` (세부 비율 미확정)
* Simulator에서는 향후 다음 변수를 허용해야 한다: Silicone ratio, Dimethicone viscosity, Grade, Purity.

## 4.3 MQ Resin — 12% active
* 필수 데이터: Active %, Carrier, Solvent, INCI, Supplier, Trade Name, Grade, 권장 사용량.

## 4.4 Functional/Auxiliary Blend — 2%
* Bisabolol, Stearyl Glycyrrhetinate, Tocopherol, Rosemary Extract (총 2%, 세부 함량 미확정).

---

# 5. Powder System (총 약 28%)
* BN 3% + Porous Silica 10% + Fumed Silica 2% + PMSSQ 8% + Treated ZnO 5%
* 검증 항목: 1. Powder wetting, 2. Agglomeration, 3. Air entrapment, 4. Powder bloom, 5. Low-temperature Pay-off, 6. White cast, 7. Powder feel, 8. Scale-up dispersion consistency.

---

# 6. 원료 Master Database Schema

```text
material_id, INCI, trade_name, supplier, grade, material_type, active_pct,
carrier, carrier_pct, solvent, moisture, density, viscosity, particle_size,
D50, D90, BET, oil_absorption, surface_treatment, purity, cost_per_kg,
recommended_use_min, recommended_use_max, TDS_reference, SDS_reference,
CoA_reference, status, notes
```
* `TBD`를 허용해야 한다. 정보가 없다고 임의의 값을 넣으면 안 된다.

---

# 7. Formula Database Schema

* Formula Master: `formula_id, product_id, revision, formula_type, status, created_date, approved_date, notes`
* Formula Component: `formula_id, material_id, target_active_pct, raw_material_active_pct, calculated_charge_pct, actual_charge_kg`
* Formula Type: `target_active, manufacturing, pilot, engineering, production_master`

---

# 8. Manufacturing Formula Calculator

* 기본 공식:
  $$\text{Manufacturing Charge \%} = \frac{\text{Target Active \%}}{\text{Raw Material Active \%} / 100}$$
* Batch scaling:
  $$\text{Actual kg} = \frac{\text{Batch Size kg} \times \text{Charge \%}}{100}$$

---

# 9. Batch Size

* $100\,\text{g Lab} \rightarrow 1\,\text{kg Confirmation} \rightarrow 3\sim 5\,\text{kg Pilot} \rightarrow 10\sim 20\,\text{kg Engineering} \rightarrow 60\,\text{kg Net Production}$
* $66\,\text{kg} = \text{Initial Charge Candidate}$ (실제 손실률은 Pilot 이후 산출).

---

# 10. QC Target & Conditions

| Test | Target | 확정 필요 SOP 조건 |
| :--- | :---: | :--- |
| **Hardness** | $750 \sim 900\,\text{gf @25}^\circ\text{C}$ | Probe, Penetration depth, Speed, Conditioning time, Sample geometry, Location, Replicates |
| **Transfer** | $\ge 0.04\,\text{g @10}^\circ\text{C}$ | Applied amount, Substrate, Pressure, Contact area, Contact time, Temperature, Method |
| **Density** | $1.08 \pm 0.04\,\text{g/cm}^3$ | Pycnometer or specific volume |
| **Drop Point** | $61.5 \pm 1.5^\circ\text{C}$ | Mettler Drop point or manual |

---

# 11. Stability & 12. Package Compatibility
* Stability: RT, 40°C, 45°C, 5°C, Freeze-Thaw (-15 ↔ 45°C 3 cycles). 45°C 4주만으로 shelf life 확정 금지.
* Package: All-PP 호환성, 45/65°C 누액, 낙하, 래칫, 푸시백, 하단 누액, 흡착/이행 독립 검증.

---

# 13. Simulator 개발 아키텍처

```text
                    GLIDE-SPEC 40
                          │
          ┌───────────────┴───────────────┐
          │                               │
   RAW MATERIAL MASTER              FORMULA MASTER
          │                               │
 Supplier / Grade                  Rev.7.3
 Active / Carrier                  Rev.7.4
 TDS / SDS / CoA                   Rev.8.0
 Particle Data
          │                               │
          └───────────────┬───────────────┘
                          ↓
              MANUFACTURING CALCULATOR
                          ↓
                     DOE ENGINE
                          ↓
                  PILOT / QC DATA
                          ↓
               REGRESSION / ML MODEL
                          ↓
                   DESIGN SPACE
                          ↓
              MULTI-OBJECTIVE OPTIMIZER
                          ↓
                  FORMULA CANDIDATE
                          ↓
                    REV.7.4
```

---

# 14 ~ 29. 개발 로드맵 및 개발자 핵심 수칙

1. M0: Data Model (Material, Formula, QC, Revision)
2. M1: Formula Calculator & Batch Scaling (100g, 1kg, 5kg, 20kg, 66kg)
3. M2: DOE Engine (Wax/Silicone mixture design)
4. M3: QC Data & Target Tracking
5. M4: Response Modeling (Data 축적 전까지 "미학습 상태" 유지)
6. M5: Multi-Objective Optimization (pymoo 기반)
7. M6: Web GUI (Streamlit)

### 절대 금지 수칙 (14대 금기)
1. 실제 원료 Spec 없이 Manufacturing Formula 확정
2. MQ Resin 12%를 무조건 raw material 12%로 계산
3. Carrier를 무시
4. Active %를 무시
5. Supplier Grade 차이를 무시
6. 실제 QC 데이터 없이 AI가 물성을 안다고 가정
7. Hardness 시험조건을 무시
8. Transfer 시험조건을 무시
9. 80°C를 확정 공정으로 취급
10. 66 kg을 확정 생산량으로 취급
11. 45°C 4주를 shelf life로 단정
12. Simulation 결과를 실제 실험 결과처럼 취급
13. Revision 변경사항을 삭제하거나 덮어쓰기
14. 기존 Rev.7.3 값을 개발자가 임의로 수정

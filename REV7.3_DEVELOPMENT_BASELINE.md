# GLIDE-SPEC 40

## Rev.7.3
### 원료 선정 · 생산배합 · QC 개발 기준서

---

## 0. Rev.7.3의 정의

Rev.7.3은 **제품 구조를 다시 설계하는 단계가 아니다.**

현재 제품 컨셉과 후보 배합 구조를 유지하면서,

> **원료 Spec → Manufacturing Formula → Pilot → QC → Scale-up**

으로 연결하기 위한 **개발 기준선(Baseline)**이다.

따라서 Rev.7.3의 배합 수치는 최종 생산 Formula가 아니라 **Target Active Formula**를 중심으로 관리한다.

---

# 1. 제품 기본 사양

| 항목 | Rev.7.3 기준 |
| :--- | :--- |
| **제품명** | GLIDE-SPEC 40 |
| **제형** | Anhydrous 계열 Powder-in-Balm Stick |
| **내용량** | 20 g |
| **용도** | 마찰 감소 및 피부 쓸림 방지용 기술성 스틱 |
| **주요 타깃** | 러너 / 장거리 활동 / 군장 행군 |
| **초기 생산 목표** | 3,000개 |
| **제형 방향** | 저마찰 + 보송한 마무리 + 지속성 + 전이 억제 |
| **향료** | 미사용 방향 |
| **유기 자외선차단제** | 의도적으로 미첨가 |
| **ZnO** | 5% 유지, 용도 및 규제 포지션 별도 관리 |

### 중요
`Anhydrous`는 현재 최종 확정 표현이 아니다.  
실제 원료의 수분, Carrier, Solvent 등을 확인한 후 확정한다.

---

# 2. Target Active Formula

| 원료군 | 목표 함량 | 비고 |
| :--- | :---: | :--- |
| **Boron Nitride** | 3.0% | 전단 미끄럼 슬립성 |
| **Porous Spherical Silica** | 10.0% | 점도 안정화, 땀/피지 흡착 |
| **Silica Dimethyl Silylate** | 2.0% | 훈증 실리카, 침전 방지/요변성 |
| **Polymethylsilsesquioxane (PMSSQ)** | 8.0% | 마이크로 볼베어링 하중 분산, 실키감 |
| **Treated Zinc Oxide** | 5.0% | 표면처리 징크 (백탁 전이 억제) |
| **Synthetic Wax + Candelilla Wax** | 17.0% | 왁스 시스템 총량 |
| **PEG-8 Beeswax** | 3.0% | 이지 워시오프 기능성 왁스 |
| **Dimethicone + Caprylyl Methicone** | 28.0% | 경량 실리콘 캐리어 총량 |
| **MQ Resin** | **12.0% active** | 순수 고형분 기준 (용매 함량에 따라 투입량 환산) |
| **C12-15 Alkyl Benzoate** | 9.5% | 분산제 및 피막 가소제 |
| **Ethylhexylglycerin** | 0.5% | 데오 부스터 (악취 방어) |
| **Bisabolol + Stearyl Glycyrrhetinate + Tocopherol + Rosemary Extract** | 2.0% | 진정/산패 방지 블렌드 총량 |
| **합계** | **100.0%** | **Target Active Formula** |

### 핵심 원칙
위 표는 **Target Active Formula**이다. 실제 제조에 사용하는 Formula가 아니다.  
* **예시:** MQ Resin이 60% active 원료라면 $\rightarrow 12 \div 0.60 = 20\%$ 투입. (용매로 사용된 실리콘 비율만큼 실리콘 캐리어 투입량에서 상계 차감 계산 필요)

---

# 3. 현재 미확정 배합

## 3.1 Wax System — 총 17%
* 현재: `Synthetic Wax + Candelilla Wax = 17%` (세부 비율 미확정)
* 목적:
  * 25°C Hardness
  * 저온 Pay-off
  * Stick integrity
  * Transfer의 균형 확보
* 목표:
  * $\text{Hardness } 750 \sim 900\,\text{gf} \text{ @25}^\circ\text{C}$
  * $10^\circ\text{C} \text{ Transfer} \ge 0.04\,\text{g}$

## 3.2 Silicone System — 총 28%
* 현재: `Dimethicone + Caprylyl Methicone = 28%` (세부 비율 미확정)
* Dimethicone 확인 항목:
  * Viscosity (점도 cSt)
  * Grade
  * Purity
  * Supplier
  * Trade Name

## 3.3 MQ Resin — 12% Active
가장 중요한 확인 항목 중 하나.  
* **필수 확인:**
  * 실제 active %
  * Carrier 종류
  * Solvent/Carrier 함량
  * 실제 INCI
  * 제조사 및 Trade Name / Grade
  * 권장 사용량
* **주의:** Active 12%를 실제 원료 12%로 간주하면 안 됨.

## 3.4 Functional/Auxiliary Blend — 2%
* 현재 구성: Bisabolol, Stearyl Glycyrrhetinate, Tocopherol, Rosemary Extract (총 2%, 개별 함량 미확정)
* 특히 **Rosemary Extract**:
  * 정확한 INCI
  * Carrier
  * 수분 함량
  * Extract 함량
  * 색상 및 냄새 확인 필수

---

# 4. 원료 선정 기준

실제 원료 선정은 단순 INCI 기준이 아니라 **Grade 기준**으로 한다.

* **Boron Nitride:** Purity, Particle size ($D_{50}$), Morphology, Surface treatment
* **Porous Spherical Silica:** $D_{50}$, $D_{90}$, BET (비표면적), Oil absorption, Moisture, Bulk density
* **Silica Dimethyl Silylate:** BET, Particle size, Oil absorption, Moisture, Dispersion
* **PMSSQ:** Particle size, Spherical morphology, Agglomeration, Purity
* **ZnO:** 정확한 INCI, ZnO active %, Surface treatment, Particle size, Heavy metal specification

---

# 5. 핵심 Powder System

* **구성:** BN 3% + Porous Spherical Silica 10% + Silica Dimethyl Silylate 2% + PMSSQ 8% + Treated ZnO 5% = **총 약 28%**
* 이 시스템은 GLIDE-SPEC 40의 핵심 차별점인 동시에 가장 큰 제조 리스크다.
* **반드시 검증:**
  1. Powder wetting
  2. Agglomeration (뭉침)
  3. Air entrapment (기포 혼입)
  4. Powder bloom (표면 백화)
  5. 10°C Pay-off (저온 전사)
  6. White cast (백탁)
  7. Powder feel (도포감)
  8. Scale-up dispersion consistency (스케일업 분산 균일성)

---

# 6. QC 목표

| 시험 | 목표 | 비고 |
| :--- | :---: | :--- |
| **Drop Point (융점)** | $61.5 \pm 1.5^\circ\text{C}$ | |
| **Hardness (경도)** | $750 \sim 900\,\text{gf} \text{ @25}^\circ\text{C}$ | |
| **10°C Transfer (전사량)** | $\ge 0.04\,\text{g}$ | 피부 1회 왕복 기준 |
| **Density (비중)** | $1.08 \pm 0.04\,\text{g/cm}^3$ | |

> **[주의] 현재 숫자만 확정된 상태이며, 시험 SOP는 미확정이다.**

---

# 7. QC SOP에서 확정해야 할 사항

* **Hardness:**
  * Probe 규격
  * Penetration depth (침투 깊이)
  * Speed (진입 속도)
  * Conditioning time (시료 항온 시간)
  * Sample shape (시료 형상)
  * Measurement location (측정 부위)
  * Replicate number (반복 측정 수)
* **Transfer:**
  * 도포량 / 도포면적
  * Substrate (측정 대상 기질 - 인조가죽, 피부 등)
  * Pressure (인가 하중)
  * Contact time (접촉 시간)
  * Temperature (온도)
  * 측정방법

> **동일한 숫자라도 시험방법(SOP)이 다르면 QC 기준으로 사용할 수 없다.**

---

# 8. Stability (안정성 시험)

* **최소 시험 조건:**
  * **기본:** Room temperature, 40°C, 45°C, 5°C, (필요 시 0°C)
  * **Freeze-Thaw:** $-15^\circ\text{C} \leftrightarrow 45^\circ\text{C}$, 3 cycles
* **확인 항목:**
  * Sweating (발한)
  * Syneresis (이장/분리)
  * Cracking (균열)
  * Deformation (변형)
  * Powder bloom (분말 석출)
  * Color (변색)
  * Odor (이취/원료취)
  * Hardness (경도 변화)
  * Pay-off (전사량 변화)
  * Stick mechanism (용기 구동성)

> **45°C 4주만으로 최종 유통기한을 확정하지 않는다.**

---

# 9. Washability (세정성 평가)

* 기존의 *"1회 세정으로 100% 제거"* 같은 절대 표현은 사용하지 않는다.
* **시험법을 먼저 수립:**
  1. 일정량 도포
  2. 일정 시간 방치
  3. 표준 세정제 적용
  4. 일정 온도/시간 세정
  5. 잔류량 측정
* 시험 결과 데이터에 근거하여 외부 표현을 결정한다.

---

# 10. 인체 및 실사용 검증

* **안전성:**
  * 48h Patch Test
  * 반복 사용 적합성
  * 민감 부위 사용성
* **감각 평가:**
  * 미끄러움, 끈적임, 보송함, 백탁, 잔여감, 옷 전이
* **Running 실사용 검증:**
  * 10 km, 20–30 km, 장거리
* **Marching (행군) 실사용 검증:**
  * 장시간 보행, 고온·다습 환경
  * 허벅지, 사타구니, 겨드랑이, 발, 군장 스트랩 접촉 부위
* **비교군 설정:**
  * GLIDE-SPEC 40 vs Vaseline 계열 vs 기존 Anti-chafing 시판 제품

---

# 11. 제조 Scale-up

```text
100 g Lab
  ↓
1 kg Confirmation
  ↓
3–5 kg Pilot
  ↓
10–20 kg Engineering
  ↓
60 kg Net Production
```

### 11.1 66 kg 배치 정의
* 기존의 "60 kg 생산 + 10% 손실 = 66 kg"이라는 고정 개념 폐기.
* 현재 정의: **66 kg = Initial Charge Candidate** (실제 손실률은 Pilot 이후 계산).

### 11.2 80°C 충전 정의
* 80°C는 고정값이 아님.
* 현재 정의: **80°C = Initial Process Candidate**
* Pilot에서 확인: 충전성, 분산 안정성, 기포, 표면, 수축, 용기 변형, 원료 열 안정성 $\rightarrow$ 이후 실제 Fill Temperature 확정.

---

# 12. Package Validation

내용물 QC와 패키지 QC를 명확히 분리한다.

* **확인 항목:**
  * PP compatibility
  * 45°C / 65°C 내열 시험
  * Leakage (누액)
  * Drop test (낙하 충격)
  * Cap retention (캡 체결력)
  * Ratchet 작동 (래칫 기어감)
  * Push-back (후퇴 방지 내하중)
  * Bottom leakage (하단 축 누액)
  * Retraction (스틱 복귀)
  * 반복 사용 내구성
  * 장기 보관 안정성
  * Stick/Package 간 이행 및 흡착 여부

---

# 13. 규제 및 표시 방향

* 기능성화장품으로 표현하지 않음
* 자외선 차단 효능 주장하지 않음
* ZnO는 배합상 유지하되 용도 및 규제 포지션 관리
* 방수 등 절대 표현은 검증 후 판단
* “100% 제거” 표현 보류
* “무자극” 표현 보류
* “오염 Zero” 같은 절대 표현 보류
* “Anhydrous”는 원료 Carrier/수분 확인 후 확정
* 전성분 표시는 규정상 가능한 범위와 별개로 **가능하면 자발적으로 투명하게 표시하는 방향** 검토

---

# 14. 현재 상태 요약

### A. 확정에 가까운 것
* GLIDE-SPEC 40 제품 컨셉
* 20 g Stick 규격
* Powder-in-Balm 제형 구조
* 기본 후보 배합 구조
* 물성 목표 수치
* Pilot → Scale-up 5단계 구조
* Package QC 분리 원칙
* Powder system (28%)을 핵심 검증 대상으로 유지

### B. 조건부
* ZnO 5%
* MQ Resin 12% active
* Wax 17%
* Silicone 28%
* Functional/Auxiliary blend 2%
* 80°C Fill
* 66 kg Initial Charge
* 초기 3,000개 생산 목표
* 2,950원 Target COGS

### C. 미완성 (OEM 및 Pilot 단계에서 확보할 항목)
* 실제 원료 제조사, Trade Name, Grade, TDS, SDS, CoA
* 실제 INCI, Active %, Carrier, Moisture
* Manufacturing Formula 산출
* Wax 세부 비율, Silicone 세부 비율, Functional blend 세부 비율
* MQ 실제 투입량 계산
* QC SOP (측정 조건/장비 표준화)
* Stability 시험 결과
* Package Compatibility 시험 결과
* 인체시험, Running 시험, Marching 시험
* 실제 OEM 견적

---

# 15. Rev.7.3 변경 이력

| ID | 변경사항 | 유형 |
| :--- | :--- | :---: |
| **NEW-01** | Active Formula / Manufacturing Formula 분리 | Added |
| **NEW-02** | “Anhydrous”를 원료 확인 후 확정 | Modified |
| **NEW-03** | 80°C 충전을 고정값 → 공정 후보값(Candidate)으로 변경 | Modified |
| **NEW-04** | 66 kg을 고정 손실량 → Initial Charge Candidate로 변경 | Modified |
| **NEW-05** | Package Compatibility를 별도 독립 검증 항목으로 승격 | Added |
| **NEW-06** | 실제 원료 Spec 없는 상태에서 Production Formula 확정 금지 | Added |
| **NEW-07** | 28% Powder System의 분산성을 핵심 검증 대상으로 지정 | Added |
| **NEW-08** | MQ Resin 실제 active/charge 계산을 생산 전 필수화 | Added |

---

# 16. Rev.7.3 다음 단계

```text
① Rev.7.3 Baseline 동결
        ↓
② OEM에 원료 Spec 요청
        ↓
③ 후보 원료 비교표
        ↓
④ Manufacturing Formula 계산
        ↓
⑤ 100 g 시제품
        ↓
⑥ 1 kg Confirmation
        ↓
⑦ 3–5 kg Pilot
        ↓
⑧ 물성 / QC 측정
        ↓
⑨ 결과 분석
        ↓
⑩ Rev.7.4
        ↓
⑪ 10–20 kg Engineering
        ↓
⑫ 최종 Production Formula
        ↓
⑬ Rev.8.0 Production Master
```

---

# 17. Rev.7.3의 핵심 판단

**지금은 배합을 임의로 수정할 단계가 아니다.**

현재 가장 중요한 것은:

> **원료 Spec → Manufacturing Formula → Pilot → QC**

이다. 특히 다음 세 가지를 먼저 확보해야 한다:
1. **실제 원료 Spec (TDS, CoA, Active %, Carrier)**
2. **Active → Manufacturing Formula 변환**
3. **실제 Pilot QC 데이터**

그 이후에야 Wax ratio, Silicone ratio, Powder system 등의 최적화를 본격적으로 진행한다.

---

# 18. Rev.7.3 Baseline 선언

**GLIDE-SPEC 40 Rev.7.3은 현재 개발의 기준선으로 사용한다.**

Rev.7.3의 값을 임의로 덮어쓰지 않는다.

변경이 필요한 경우:
```text
실험 → 결과 → 변경 근거 → Rev.7.4
```
의 절차를 따른다. 따라서 Rev.7.3과 Rev.7.4 이후의 배합, 공정, QC 기준은 항상 별도의 Revision으로 추적한다.

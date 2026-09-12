# Solid Stick & Wax-Balm Domain Dataset Survey (Rev.1.0)
**Document ID:** `SURVEY-SOLID-STICK-WXP-2026-v1.0`  
**Date:** 2026-09-12  
**Target Product:** GLIDE-SPEC 40 (20g Powder-in-Balm Stick, Rev.7.3)  
**Track:** Track A-2 (Domain-Relevant Literature & Benchmark Dataset Survey)  

---

## 1. 서론 및 도메인 데이터 선별 배경

GLIDE-SPEC 40의 M4 회귀 엔진과 처방 최적화는 **수용성 액상 샴푸 데이터**로는 물리적 전이(Domain Transfer)가 불가능합니다.  
스틱 제형의 품질과 사용성은 **(1) 3차원 왁스 미세결정 네트워크**, **(2) 고함량 분체(28%)의 전단 분산**, **(3) 오일/실리콘 캐리어의 계면 윤활**이라는 고유한 유변학적 메커니즘에 의해 결정됩니다.

본 서베이는 샴푸 대신 **고체 스틱(Stick), 밤(Balm), 왁스 올레오겔(Wax Oleogel), 립스틱(Lipstick)** 등 물리화학적 구조가 상용되는 최근 공인 연구 논문 및 데이터셋을 발굴하고, GLIDE-SPEC 40의 3대 핵심 물성(Hardness, Pay-off/Transfer, Drop Point)과의 수리학적 매핑 관계를 확립하기 위해 수행되었습니다.

---

## 2. 주요 발굴 선행 연구 및 물리 데이터 요약

### [문헌 1] 지속가능 왁스-오일 스틱 제형의 물성 및 도포 거동 (2026)
- **논문명:** *Sustainable cosmetic ingredient alternatives to replace conventional ingredients: Case studies in moisturizers and lipsticks*
- **출처:** *International Journal of Cosmetic Science* / PMC12877994 (2026 Feb)
- **주요 원료 구성:**
  - **Wax Matrix:** Microcrystalline Wax (2.0%), Synthetic Wax/Beeswax (15.0%), Candelilla Wax (12.0%), Carnauba Wax (5.0%)
  - **Oils/Emollients:** Ethylhexyl Palmitate, Caprylic/Capric Triglyceride, Triheptanoin, Heptyl Undecylenate (총 ~45%)
  - **Pigment/Slurry:** 30% Dispersion (Castor oil + Lake)
- **GLIDE-SPEC 40 핵심 매핑 물성치:**
  1. **Hardness (Needle Penetration Test, gf):**
     - 측정치: **$136.3 \sim 184.5\,\text{gf}$** (침투 침 깊이 하중)
     - 특성: 왁스 네트워크 형성 후 6주 동안 유의미한 경도 저하 없이 균일 유지.
  2. **Pay-off / Transfer (3-cycle deposition on fabric, mg):**
     - 측정치: **$27.0 \sim 63.0\,\text{mg}$** (3회 왕복 도포)
     - 특성: 왁스 결정도 및 가소제 오일 종류에 따라 최대 2.3배의 도포량 편차 발생.
  3. **Friction & Glide Transition (Dynamic Resistance, gf):**
     - Cycle 1 피크 마찰: **$70 \sim 80.2\,\text{gf}$**
     - Cycle 2~3 윤활 마찰: **$57.5 \sim 61.9\,\text{gf}$** (1차 도포막 형성 후 슬라이딩 저항 감소)
  4. **Melting Peak / Drop Point (DSC, °C):**
     - 실측 적점: **$42.82 \pm 2.97^\circ\text{C} \sim 48.30 \pm 6.97^\circ\text{C}$**

---

### [문헌 2] 합성 왁스 대체에 따른 립스틱 경도 및 발한 안정성 (2022)
- **논문명:** *Substitution of synthetic waxes by plant-based waxes in lipsticks*
- **출처:** *OCL (Oilseeds and fats, Crops and Lipids)*, DOI: [10.1051/ocl/2022010](https://doi.org/10.1051/ocl/2022010)
- **핵심 통찰:**
  - Synthetic Wax 단독 사용 시 결정 구조가 지나치게 조밀해져 저온 취성(Brittleness) 및 낮은 전이량(Pay-off 저하) 초래.
  - Candelilla Wax를 $30 \sim 40\%$ 비율로 복합 적용할 때, 이종 탄화수소 사슬 간 얽힘(Entanglement)으로 인해 연성(Plasticity)이 증가하고 $10^\circ\text{C}$ 저온 발림성이 회복됨.
  - GLIDE-SPEC 40의 `Synthetic Wax (12.0%) : Candelilla Wax (5.0%)` 중심점 비율 ($u_1 \approx 0.706$)은 취성과 연성의 이상적 타협점임을 뒷받침함.

---

### [문헌 3] 천연/합성 왁스 이원계 올레오겔의 경도 및 소성 거동 (2022)
- **논문명:** *Hardness, plasticity, and oil binding capacity of binary mixtures of natural waxes in olive oil*
- **출처:** *Current Research in Food Science*, DOI: [10.1016/j.crfs.2022.06.002](https://doi.org/10.1016/j.crfs.2022.06.002)
- **수학적 모델링 시사점:**
  - 단일 왁스 대비 이원계 왁스 블렌드는 경도(Back Extrusion Hardness)에서 **강한 비선형 시너지(Synergistic Hardness Enhancement)**를 나타냄.
  - 단순 선형 1차식 $y = \beta_0 + \beta_1 u_1$에 더해, $u_1(1-u_1)$ 형태의 Scheffé 혼합물 2차 상호작용 항이 경도 피크를 예측하는 데 통계적으로 유의미함을 검증함.

---

## 3. GLIDE-SPEC 40 M4 회귀 모델 적용 전략

| 타깃 물성 | 도메인 연구 데이터 기준치 | GS40 파일럿 목표 규격 | M4 회귀 주영향 인자 |
|---|:---:|:---:|:---|
| **Hardness (경도)** | 136 ~ 185 gf (무들러/침투 침) | **$750 \sim 900\,\text{gf}$** (피크 압축 하중) | $u_1$ (Syn Wax 분율), Fill Temp ($T$) |
| **Transfer / Pay-off** | 27 ~ 63 mg (3-cycle 패브릭) | **$\ge 40\,\text{mg}$** ($10^\circ\text{C}$ 피부 1회 왕복) | $v_1$ (Dimethicone 분율), Candelilla Wax |
| **Drop Point (융점)** | 43 ~ 48 °C (DSC 피크) | **$61.5 \pm 1.5^\circ\text{C}$** (Mettler 적점) | Wax Total (17%), Synthetic Wax Ratio |

### 결론
선행 연구 데이터는 **"왁스 비율의 미세 변화가 경도와 전이량 간의 Trade-off를 지배한다"**는 물리적 원리를 명확히 입증합니다.  
따라서 GLIDE-SPEC 40의 실제 18-Run Pilot 실험(Track A-1) 데이터가 확보되었을 때, 선행 연구의 물리적 경향성(Synergistic Hardness & Friction Transition)을 참조 앵커로 삼아 이상치 검출 및 모델 타당성을 교차 검증할 수 있습니다.

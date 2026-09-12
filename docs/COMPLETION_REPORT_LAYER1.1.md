# GLIDE-SPEC 40: Layer 1.1 Virtual Mechanistic Simulator & Public Domain Prior 정밀 체계화 보고서

---

## 🛡️ 4대 황금 비동등성 원칙 (The 4 Golden Non-Equivalence Principles)

시뮬레이터의 과학적 무결성과 오해 방지를 위해, 외부 공개 데이터로부터 도출된 사전 수치와 실제 GS-40 물리 측정값 간의 비동등성을 코드 및 출력 레벨에 영구 확립하였습니다:

1. **Hardness Prior ≠ GS40 Hardness Prediction**  
   - 17% 왁스 립스틱 기준 경도(165 gf)에 28% 고함량 분체 및 MQ 레진 보강 계수를 공학적 가정을 통해 투영한 사전 지표입니다.
2. **Thermal Transition Prior ≠ GS40 Mettler Drop Point**  
   - DSC 흡열 용융 피크(Thermodynamic phase change, $\approx 61.5^\circ\text{C}$)는 중력 하 전단 유동을 측정하는 Mettler Drop Point(ASTM D127 / IP 396)와 물리화학적으로 상이합니다.
3. **Pay-off Anchor ≠ GS40 Physical Transfer (g)**  
   - 전완부 1회 도포 문헌값(14 mg) 및 특허 4회 마찰 손실량(29~46 mg/stroke)은 기판, 하중(100g vs 200g), 도포 속도, 온도(20°C 상온 vs 10°C 저온)가 완전히 다르므로, 그램 단위의 실측치가 아닌 무차원 `Transfer Prior Index`로만 다룹니다.
4. **Tribology Prior Index ≠ GS40 Dynamic CoF**  
   - PDMS 및 피부 접촉 마찰계수 경향은 GS-40의 표면 마찰 지수를 안내하는 사전 지수일 뿐, 완제 스틱의 실제 동마찰계수 실측치가 아닙니다.

---

## 🏛️ Public Domain 4대 마스터 분류 체계

```text
PUBLIC DOMAIN
│
├── A. FORMULATION → RESPONSE
│   ├── P&G Anhydrous Stick (US20070166254: 20-25% 분체, 실리콘, 왁스)
│   ├── Lipstick 17% Wax Benchmark (Huynh et al. 2020: 17% 왁스, DSC, pay-off)
│   └── Commercial Lip Balm SLA (Cosmetics 2024: 7종 Brookfield 텍스처 벤치마크)
│
├── B. TRIBOLOGY
│   ├── Imperial Wax-Oil (Yap et al. 2021: 왁스-오일 피부 CoF 0.16~0.29)
│   └── Silicone & Powder Tribology (Masen et al. 2020 / Carr et al. 2024: 디메치콘 CoF 0.20, 탈크 CoF 0.22)
│
├── C. RAW MATERIAL VARIABILITY
│   └── TU Berlin Wax Lots (Zenodo 2026: 칸데릴라 왁스 Lot별 G* CV 20.4%)
│
└── D. GENERAL FORMULATION ML QA
    └── Nature Shampoo 812 (Nature 2023: 머신러닝 회귀 엔진 수학 검증)
```

---

## 1. 경도(Hardness) 도출 공식의 근거 및 계수 출처 투명화

```text
PUBLIC EMPIRICAL DATA
  ├─ Huynh et al. (2020): 17.0% Wax Cosmetic Stick Firmness = 165.0 gf
  └─ US Patent 20070166254: 20~25% Talc/Silica Particulate Reinforcement (~1.8-2.2x stiffening)
        ↓
EMPIRICAL ANCHOR
  └─ Base wax matrix firmness = 165.0 gf
        ↓
ENGINEERING TRANSFORMATION
  ├─ Baseline Intercept = 650.0 gf (165 gf * 3.94x particulate scaffold & MQ resin multiplier)
  ├─ beta_wax_stiffness = +260.0 gf/unit (Synthetic Wax crystal fraction u1)
  ├─ beta_silicone_softener = -120.0 gf/unit (Dimethicone fluid plasticizing v1)
  └─ beta_thermal_quenching = +3.5 gf/°C (Pour temperature crystal nucleation dT)
  └─ [COEFFICIENT_SOURCE = ENGINEERING_ASSUMPTION]
        ↓
GS40 PRIOR
  └─ H_prior = 650.0 + 260.0 * u1 - 120.0 * v1 + 3.5 * dT
```
* **신뢰도 보증:** 본 수식은 머신러닝 피팅이 아닌 **공학적 가정에 기반한 변환(Engineering Transformation with Assumptions)**임을 코드의 메타데이터 및 CLI 출력에 100% 명시하였습니다.

---

## 2. 열 전이(Thermal Transition Prior) 및 전이 지수(Transfer Prior Index) 정밀화

### A. 열 전이 지표 (Thermal Transition Prior)
* **원자료 앵커:** Huynh et al. (2020) 17% 왁스계 DSC 흡열 용융 피크 = $60.3^\circ\text{C}$
* **공학 변환식:** $T_{\text{thermal}} = 57.0 + 6.3 \cdot u_1 + 0.05 \cdot dT$ (`coefficient_source = ENGINEERING_ASSUMPTION`)
* **물리적 분리:** ASTM D127 / IP 396 규격의 Mettler Drop Point 실측 변수(`GS40_QC_METTLER_DROP_POINT`)와 완전히 독립된 가상 사전 지표로 보존.

### B. 전이 지표 (Transfer Prior Index)
* **원자료 앵커:** 립스틱 L1 인체 피부 전이량 14 mg & 무수 분체 스틱 4회 마찰 손실 29~46 mg/stroke
* **공학 변환식:** $\text{Transfer\_Index} = 0.058 - 0.020 \cdot u_1 + 0.012 \cdot (1.0 - v_1) - 0.0003 \cdot dT$ (`coefficient_source = ENGINEERING_ASSUMPTION`)
* **물리적 분리:** 실측 규격(`SOP-GS40-PILOT-001` 10°C 인공피부 왕복 마찰 질량 측정값)과 혼동되지 않도록 명목 중심점 $\approx 0.049$를 기준으로 하는 지수 단위로 표기.

---

## 3. TU Berlin 칸데릴라 편차의 계층적 불확실성 전파 모델 구축

TU Berlin의 10 wt% 올레오겔 측정 편차(CV = 20.4%)를 GS40 완제 경도에 직접 1:1 대입하는 오류를 제거하고, 다성분계의 물리적 감쇠 구조를 반영한 **계층적 불확실성 전파(Hierarchical Uncertainty Transmission Layer)**를 구현하였습니다:

```text
[Level 1: Raw Material Lot Variability Prior]
  └─ TU Berlin Candelilla lot shear modulus G* CV = 20.40%
        ↓
[Level 2: Matrix Network-Strength Transmission]
  ├─ GS40 Wax Phase: Candelilla 5.0% (fraction 0.294) + Synthetic Wax 12.0% (fraction 0.706, CV ~ 3.5%)
  └─ Composite Wax Network CV = sqrt((0.294*0.204)^2 + (0.706*0.035)^2) = 6.49%
        ↓
[Level 3: Particulate Scaffold & Resin Damping]
  ├─ 28% Powder (PMMA, Silica, Al-Starch) + MQ Resin rigid skeleton buffers wax variation (Damping factor = 0.70)
  └─ Damped Raw Material Prior CV = 6.49% * 0.70 = 4.54%
        ↓
[Level 4: Thermal Processing & Gauge Compounding]
  ├─ Process Thermal Quenching Variance CV = 3.00%
  ├─ Texture Analyzer Gauge Repeatability CV = 3.00%
  └─ Total Composite Hardness Prior CV = sqrt(4.54^2 + 3.00^2 + 3.00^2) = 6.22%
        ↓
[Resulting GS40 Hardness Prior Monte Carlo SD]
  └─ 761.6 gf * 6.22% = ±47.3 gf (90% CI: [688.5 gf, 840.0 gf])
```

---

## 4. 실리콘 전용 생체 마찰 데이터셋 추가 (Category B)

* **출처:** Masen et al., *PLOS ONE* (2020) [PMC7514078](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514078/) & Southampton 연구팀 (2024) [PMC11318204](https://pmc.ncbi.nlm.nih.gov/articles/PMC11318204/)
* **데이터셋:** `benchmarks/domain_priors/silicone_skin_tribology/silicone_powder_skin_tribology_benchmark.csv`
* **관측 수치:**
  - 디메치콘/디메치코놀 오일 도포 직후 동마찰계수: **$\text{CoF} \approx 0.20 \pm 0.03$** (무도포 피부 대비 20% 수준)
  - 탈크 분체 도포 마찰계수: **$\text{CoF} \approx 0.22 \pm 0.02$** (4시간 이상 안정적인 지속 윤활성)
  - 실리콘 박막 배리어 필름 (Hexamethyldisiloxane / Polyphenylmethylsiloxane): **$\text{CoF} \approx 0.38 \sim 0.55$**
  - 무도포 피부 마찰계수: **$\text{CoF} \approx 0.92 \pm 0.14$**
* **역할:** GS40의 디메치콘/카프릴릴메치콘 및 실리카/탈크 분체 윤활 거동의 실험적 참조 앵커로 편입.

---

## 5. 18-Run Virtual DOE Prior Audit 재산출 결과

| Run | Batch ID | Design Type | Syn Wax (%) | Dim (%) | Fill (°C) | Hardness Prior (gf) | Transfer Prior Index | Thermal Trans Prior (°C) | Tribology Prior Index | Prior Risk Classification |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **01** | `GS40-P001` | Vertex_HighSyn_HighDim | 15.0 | 21.0 | 80.0 | 785.4 [725-850] | 0.0430 [0.037-0.049] | 62.63 | 0.158 | **LOW (Nominal Core)** |
| **02** | `GS40-P002` | Vertex_HighSyn_LowDim_Tmin | 15.0 | 13.0 | 75.0 | 810.8 [748-877] | 0.0490 [0.043-0.055] | 62.38 | 0.150 | **LOW (Nominal Core)** |
| **03** | `GS40-P003` | Vertex_LowSyn_HighDim_Tmax | 9.0 | 21.0 | 85.0 | 711.3 [624-804] | 0.0490 [0.043-0.055] | 60.66 | 0.147 | **MEDIUM (Boundary Probe)** |
| **04** | `GS40-P004` | Vertex_LowSyn_LowDim | 9.0 | 13.0 | 80.0 | 736.6 [646-833] | 0.0540 [0.049-0.060] | 60.41 | 0.140 | **MEDIUM (Boundary Probe)** |
| **05** | `GS40-P005` | Axial_WaxMax | 15.0 | 17.0 | 80.0 | 789.3 [729-854] | 0.0470 [0.041-0.053] | 62.38 | 0.154 | **LOW (Nominal Core)** |
| **06** | `GS40-P006` | Axial_WaxMin | 9.0 | 17.0 | 80.0 | 732.7 [643-828] | 0.0510 [0.045-0.057] | 60.66 | 0.143 | **MEDIUM (Boundary Probe)** |
| **07** | `GS40-P007` | Axial_SilMax | 12.0 | 21.0 | 80.0 | 722.0 [654-795] | 0.0480 [0.043-0.054] | 61.27 | 0.152 | **MEDIUM (Boundary Probe)** |
| **08** | `GS40-P008` | Axial_SilMin | 12.0 | 13.0 | 80.0 | 799.9 [724-881] | 0.0490 [0.044-0.055] | 61.77 | 0.145 | **LOW (Nominal Core)** |
| **09** | `GS40-P009` | Axial_TempMin | 12.0 | 17.0 | 75.0 | 743.5 [673-818] | 0.0500 [0.045-0.056] | 61.27 | 0.149 | **MEDIUM (Boundary Probe)** |
| **10** | `GS40-P010` | Axial_TempMax | 12.0 | 17.0 | 85.0 | 778.5 [705-857] | 0.0470 [0.042-0.053] | 61.77 | 0.149 | **LOW (Nominal Core)** |
| **11** | `GS40-P011` | Interior_Low | 10.5 | 15.0 | 77.5 | 748.8 [668-835] | 0.0520 [0.046-0.058] | 60.96 | 0.144 | **MEDIUM (Boundary Probe)** |
| **12** | `GS40-P012` | Interior_High | 13.5 | 19.0 | 82.5 | 773.2 [708-842] | 0.0460 [0.040-0.052] | 62.07 | 0.153 | **LOW (Nominal Core)** |
| **13** | `GS40-P013` | Centroid_Replicate_1 | 12.0 | 17.0 | 80.0 | 761.0 [689-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **14** | `GS40-P014` | Centroid_Replicate_2 | 12.0 | 17.0 | 80.0 | 761.0 [689-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **15** | `GS40-P015` | Centroid_Replicate_3 | 12.0 | 17.0 | 80.0 | 761.0 [689-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **16** | `GS40-P016` | Centroid_Replicate_4 | 12.0 | 17.0 | 80.0 | 761.0 [689-838] | 0.0490 [0.043-0.055] | 61.52 | 0.149 | **LOW (Centroid Calibration)** |
| **17** | `GS40-P017` | Supplemental_Temp_78C | 12.0 | 17.0 | 78.0 | 754.0 [683-830] | 0.0490 [0.044-0.055] | 61.42 | 0.149 | **LOW (Nominal Core)** |
| **18** | `GS40-P018` | Supplemental_Temp_82C | 12.0 | 17.0 | 82.0 | 768.0 [695-845] | 0.0480 [0.043-0.054] | 61.62 | 0.149 | **LOW (Nominal Core)** |

---

## 6. 테스트 및 검증 결과

* **단위 테스트 스위트:** 34개 테스트 100% 통과 (`python3 -m unittest discover tests`, `0.334s`)
* **방화벽 보증:** `VirtualSimulationResult.data_origin == "VIRTUAL_DOMAIN_PRIOR"`, `is_empirical_gs40 == False` 엄격 유지.

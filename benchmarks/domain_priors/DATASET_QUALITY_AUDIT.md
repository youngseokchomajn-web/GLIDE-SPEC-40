# GLIDE-SPEC 40: Public Domain & Prior Dataset Quality Audit

이 문서는 GLIDE-SPEC 40의 7차원 데이터 품질 루브릭(`src/modeling/data_quality.py`)에 따라 모든 공개 벤치마크 및 도메인 Prior 데이터셋을 정량 감사한 결과입니다.

---

## 📊 7차원 품질 평가 기준 (Weight Total: 100%)
- **Formulation Completeness (20%):** 100% 질량 완결성 및 원료 식별성
- **Measurement Quality (20%):** 표준 시험법(ASTM/ISO) 및 계측기 정밀도
- **Replicate Availability (15%):** 반복 측정($n \ge 2$) 및 표준편차 존재 여부
- **Method Completeness (15%):** 전단속도, 온도, 시간 등 공정 SOP 명시도
- **Feature Overlap (15%):** GS-40 제형 공간과의 물리화학적 유사도
- **License Integrity (10%):** CC BY, CC BY-NC, Patent 등 개방형 라이선스 준수
- **Provenance Traceability (5%):** DOI, 특허번호 등 원문 추적성

---

## 🏛️ 데이터셋 품질 평가 결과 요약

| 데이터셋 명칭 | 품질 점수 | 품질 티어 | 데이터 계보 (Provenance) | 대리 모델 Prior 허용 | 핵심 내용 |
|---|:---:|:---:|:---:|:---:|---|
| **Lipstick 384 Formulations (Huynh 2020)** | **95.1%** | Tier 1: CORE_BENCHMARK | `MEASURED` | ✅ **허용 (Prior)** | 384 longitudinal cosmetic stick matrix with 17% wax, 12-week aging stability, and penetration hardness. |
| **Lipstick Multimodal Rheology (Soft Matter 2026)** | **94.15%** | Tier 1: CORE_BENCHMARK | `MEASURED` | ✅ **허용 (Prior)** | SAOS/LAOS oscillatory sweeps, stress relaxation, creep, and LC-PolScope cooling rate crystallization. |
| **Organogel Lipstick Thermal Rheology (MDPI Gels 2021)** | **88.0%** | Tier 1: CORE_BENCHMARK | `MEASURED` | ✅ **허용 (Prior)** | Temperature ramp G'/G'', gel-sol transition temperature (63.8 C), and cooling hysteresis. |
| **Wax Oleogel Hardness Regression (Doan 2022)** | **95.25%** | Tier 1: CORE_BENCHMARK | `MEASURED` | ✅ **허용 (Prior)** | Wax concentration vs. penetration firmness OLS regression (beta_wax = +75.02 gf/wt%, s_res = 6.63 gf). |
| **Silicone & Powder Skin Tribology (Masen 2020)** | **94.8%** | Tier 1: CORE_BENCHMARK | `MEASURED` | ✅ **허용 (Prior)** | In-vivo human skin & bioskin friction measurements for pure Dimethicone 100 cSt and cosmetic talc. |
| **Anhydrous Powder Stick (US Patent 20070166254)** | **78.2%** | Tier 2: PHYSICAL_PRIOR | `MEASURED` | ✅ **허용 (Prior)** | 11 anhydrous silicone-wax stick formulations with 20-25% powder loading, pay-off, and penetration depth. |
| **Fumed Silica Yield Stress (Kopylov 2011 & US20030198914)** | **84.85%** | Tier 1: CORE_BENCHMARK | `MEASURED_IN_EXTERNAL_SYSTEM` | ✅ **허용 (Prior)** | Concentration series of Aerosil R 972 in colloidal fluids (6% -> 122 Pa, 8% -> 190 Pa, 10% -> 365 Pa, 12% -> 545 Pa). |
| **GS-40 Molten Slurry 2% R972 Yield Stress & Zero Settling** | **64.0%** | Tier 3: DIRECTIONAL_GUIDE | `PRE_PILOT_HYPOTHESIS` | ⚠️ **격리 (가설/검증대기)** | Theoretical Stokes-Bingham anti-settling extrapolation (~8.6 Pa at 80 C). Pending physical verification in P001-P018. |

---

## 🛡️ 거버넌스 및 방화벽 규칙
1. **`TIER_1_CORE_BENCHMARK` (Score >= 80%):** 대리 모델(Surrogate Engine)의 정량적 사전 분포(Prior) 학습에 직접 투입 가능.
2. **`TIER_2_PHYSICAL_PRIOR` (Score 65~79%):** 정성적 스케일링 파라미터 또는 보조 사전 분포로만 활용.
3. **`PRE_PILOT_HYPOTHESIS` 및 `UNQUALIFIED` (<65%):** 정량적 사전 확률에 절대 혼입할 수 없으며, **P001~P018 물리 파일럿에서 직접 검증해야 할 가설 대상**으로만 엄격 격리.

# GLIDE-SPEC 40: System Changelog

All notable changes to the GLIDE-SPEC 40 simulation, modeling, and active learning engines are documented herein.

---

## [Product/Manufacturing Clarification] - 2026-09-14
### Changed
- Added `docs/PRODUCT_FORM_FACTOR_AND_MANUFACTURING_ASSUMPTIONS_REV1.md` to clarify the physical product definition and manufacturing assumptions.
- **“Powder-in-Balm Stick” is no longer treated as a confirmed commercial category name.** It is retained only as a shorthand for the intended balm-to-powder-like physical behavior.
- Adopted **20 g solid stick-format skin anti-chafing product** as the clearer product-form description.
- Identified NUDESTIX Blot & Blur Matte Primer Stick as a **formulation/texture reference only** because its balm-to-powder stick behavior is useful as a market analogue; it is not a GLIDE-SPEC 40 competitor or equivalent product.
- Manufacturer-facing description now emphasizes a wax/oil/silicone solid matrix with dispersed fine particulate materials, smooth application, relatively dry/powdery surface film, reduced friction and controlled transfer.
- Removed the assumption that **3,000 units is the minimum production quantity**.
- Initial production planning is now **approximately 1,000–3,000 units**, subject to manufacturer MOQ, formulation feasibility, stock-package availability and actual quotations. Smaller technical/pilot quantities may be evaluated separately.
- **2,950 KRW/unit remains a target COGS only**, not a verified manufacturing cost.
- Dedicated package tooling is not locked; **stock 18–20 g stick packaging is the first-choice path**.
- Manufacturer screening is now focused on solid stick filling, anhydrous/oil-phase balm/stick systems, balm-to-powder/matte stick experience, fine-powder dispersion and pilot filling capability.

### Rationale
- Publicly available small-batch manufacturing examples show that MOQ varies materially by manufacturer, formulation and package; therefore a fixed 3,000-unit minimum is not sufficiently supported.
- GLIDE-SPEC 40's specific powder-loaded stick formulation must be validated directly with manufacturers before MOQ, production cost or final manufacturing terminology is fixed.

---

## [Rev.8.1] - 2026-09-13 (Commit `5749cc0` / Tag `Rev8.1-precalibration`)
### Added
- **Dataset Freeze 1 & Independent Sample Audit (`data/DATASET_FREEZE_1.csv`, `docs/DATASET_INDEPENDENT_SAMPLE_AUDIT.md`):**
  - Audited 8 public peer-reviewed datasets isolating raw longitudinal/thermal rows from independent formulation clusters.
  - Clarified that 384 data points in Huynh (2020) correspond to repeated aging/thermal sweeps, mathematically justifying `GroupKFold`.
- **Feature Engineering v2 & 3-Tier Feasibility Engine (`src/modeling/feature_engine.py`):**
  - Mapped all 30 features to 4 explicit provenance levels (`MEASURED`, `DERIVED_PHYSICAL`, `DERIVED_EMPIRICAL`, `HYPOTHESIS`).
  - Added strict 3-tier boundary checking: Composition (Tier 1), Manufacturing (Tier 2), Physical mechanics (Tier 3).
- **1,000,000 Virtual Candidate Landscape Engine (`scripts/run_1m_virtual_landscape.py`, `virtual_landscape/`):**
  - Fully vectorized candidate generation and 3-tier physical screening running at 2,094,649 formulations/sec (0.48s total).
  - Screened 1,000,000 candidates: 640,822 feasible (64.1%), 359,178 rejected into Zone E by physical constraints.
  - Partitioned evaluated candidates into 5 landscape zones: Zone A (Sweet Spot, 260), Zone B (Boundary, 7,598), Zone C (High Uncertainty, 224), Zone D (OOD Extrapolation, 6,918), Zone E (Infeasible, 359,178).
  - Exported persistent Parquet datasets and summary report to `virtual_landscape/`.
- **Multi-Model Benchmark & Group-CV Cross-Validation (`docs/MODEL_BENCHMARK_REPORT.md`):**
  - Benchmarked ElasticNet, RF, ExtraTrees, GBR, HistGB, GP across 4 folds with zero cross-formulation data leakage.
  - Validated out-of-fold Conformal Prediction coverage: 80% nominal -> 94.4%, 90% nominal -> 100.0%, 95% nominal -> 100.0%.
- **Active Learning Information Diversity & Pareto Selection (`scripts/rank_active_learning_runs.py`):**
  - Computed 30-dimensional normalized Euclidean distance matrix: revealed severe redundancy between `GS40-P004` and `GS40-P011` (distance 2.66), vs. orthogonal exploration between `GS40-P001` and `GS40-P004` (distance 10.63).
  - Derived 6 non-dominated Pareto front runs.
  - Formally selected **`GS40-P001` as `GS40_CAL_001`** (Total Utility = 8.77, Rank #1) for single-batch priority manufacturing.
- **External Validation Governance 도입 (`EXTERNAL_VALIDATION_SET_1`, `docs/EXTERNAL_VALIDATION_GOVERNANCE.md`):**
  - Rev.8.1 하위 거버넌스로 `DATASET_FREEZE_1`(학습/사전모델 구축용)과 완전히 분리된 `EXTERNAL_VALIDATION_SET_1`(블라인드 외부 일반화 검증) 체계 수립.
  - 4대 엄격 금지 규정 수립: 모델 학습 금지, 피처 캘리브레이션 금지, 하이퍼파라미터 튜닝 금지, 능동학습 획득 랭킹 튜닝 금지.
  - 표본 독립성을 raw row 수가 아닌 독립 formulation / experiment 단위로 판정.
  - 사전에 8대 평가 지표 고정: $R^2$, $\text{RMSE}$, $\text{MAE}$, $\text{bias}$, 90% Prediction-Interval Coverage, PI Width, OOD Classification, Calibration Slope/Intercept.
  - 응답별 검증 가능성 3단계 분리: Hardness/Rheology 우선 검증, Payoff/CoF SOP 일치 시 조건부 검증, Sedimentation 별도 프로토콜 분리.
  - 인식론적 한계 고정: 모델 검증용이며 GS40 제품 출시 적격성으로 해석 불가 ($N(\text{GS40 physical}) = 0$ 유지).
  - 실패 데이터 영구 보존: 외부 검증 결과가 불량하더라도 은폐하거나 모델에 재투입하지 않고 Model Failure Evidence로 영구 보존.
- **Automated Testing Suite:**
  - Added `tests/test_audit_governance_and_provenance.py` and `tests/test_1m_landscape_pipeline.py`.
  - Full suite expanded to 55 tests passing 100% green in 4.08s.

### Fixed
- **GaussianProcess Target Scaling Bug (`src/modeling/surrogate_engine.py`):**
  - Added `normalize_y=True` to `GaussianProcessRegressor` inside `ResponseEnsemble`, resolving an unscaled target collapse where GP predicted 114 gf and dragged ensemble hardness mean down from 785 gf to 647 gf. Ensemble hardness now accurately predicts **781.6 gf** (centered in Rev.7.3 750–900 gf spec).
- **Composite OOD Hyperbox Robust Normalization (`src/modeling/composite_ood.py`):**
  - Normalized hyperbox bounding ranges using feature standard deviations and means, preventing zero-variance overflow.
- **Virtual Candidate Formulation Ratio Alignment:**
  - Corrected silicone ratio calculation so Total Silicone strictly equals 30.0 wt% (28% Dimethicone/Caprylyl + 2% MQ Resin), matching GS40 pilot DoE center.

---

## [Rev.8.0] - 2026-09-12
### Added
- Feature engine calculating true-density volume fractions, BET surface area, and sedimentation risk.
- 5-Surrogate ensemble (ElasticNet, RF, ExtraTrees, GBR, GP).
- 7-Dimension data quality auditor (`src/modeling/data_quality.py`).
- Nature 812 Shampoo benchmark firewall.

---

## [Rev.7.3] - 2026-09-11
### Baseline
- 18-Run DOE pilot matrix (`data/doe/pilot_doe_run_matrix_rev1.0.csv`).
- Target active formulation baseline (`src/formulas/master.py`).
- SQLite Schema v4 and M4 regression engine framework.

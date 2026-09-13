# GLIDE-SPEC 40: System Changelog

All notable changes to the GLIDE-SPEC 40 simulation, modeling, and active learning engines are documented herein.

---

## [Rev.8.1] - 2026-09-13 (Commit `bdad5ac` / Tag `Rev8.1-precalibration`)
### Added
- **Group Conformal Prediction Engine (`src/modeling/uncertainty_calibration.py`):**
  - Implemented `GroupKFold` split ensuring zero data leakage between formulation groups.
  - Implemented locally adaptive non-conformity scores ($s_i = |e_i| / \hat{\sigma}_i$) and finite-sample adaptive quantile computation for guaranteed 90% prediction intervals.
- **4-Signal Composite Out-of-Domain (OOD) Detector (`src/modeling/composite_ood.py`):**
  - Integrated Mahalanobis distance ($D_M$), kNN local density, ensemble model disagreement ($CV$), and hyperbox feature bounds violations into a unified index.
- **Multi-Objective Calibrated Acquisition Engine (`src/modeling/calibrated_acquisition.py`):**
  - Tri-criteria utility: $\text{Acquisition Score} = \text{InfoGain} \times \text{SpecRelevance} \times \text{DomainCoverage}$.
  - Corrected classification of `GS40-P002` (Hardness 668.4 gf) from unverified "top winner" to "Boundary Probe".
  - Identified `GS40-P001` as optimal safe-domain calibration candidate.
- **100k/1M Virtual Formulation Landscape Mapper (`scripts/run_1m_virtual_landscape.py`):**
  - Monte Carlo candidate generator across Rev.7.3 mixture space with percolation, solid fraction, and binder checks.
  - Partitioning into Target Sweet Spot, Specification Boundary, High Uncertainty, and OOD Extrapolation zones.
- **Automated Testing:** Added `tests/test_conformal_and_composite_ood.py` (47/47 repository tests passing).

### Changed
- Refactored `VirtualFormulationGenerator` to support `fixed_powder=True` for pilot subspace alignment.
- Refined CN102341090B artificial leather CoF and Aerosil R972 yield stress attributions.

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

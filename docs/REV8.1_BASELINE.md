# GLIDE-SPEC 40: Rev.8.1 Technical Baseline Specification

- **Baseline Freeze Tag:** `Rev8.1-precalibration` (Commit `bdad5ac`)
- **Audit Date:** 2026-09-13
- **Classification:** Controlled Technical Baseline
- **Product Scope:** 20g Anhydrous Powder-in-Balm High-Adhesion Stick
- **Hardware/Software Cost Target:** ₩0 Pure Simulation & Test-by-Exception Architecture

---

## 1. Executive Summary & Architecture State

GLIDE-SPEC 40 Rev.8.1 establishes an active learning simulation pipeline designed to minimize physical prototyping costs (reducing standard 18-run upfront manufacture of ₩2.5M~₩4.0M down to targeted single-batch executions).

```text
                                  REV.8.1 SYSTEM TOPOLOGY
┌────────────────────────────────┐       ┌────────────────────────────────┐
│      PUBLIC DATASETS (₩0)      │       │     RAW MATERIAL DB (15 Mat)   │
│  8 Curated External Datasets   │       │  Densities, BET, Oil Demands   │
└───────────────┬────────────────┘       └───────────────┬────────────────┘
                │                                        │
                └───────────────────┬────────────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │     FEATURE ONTOLOGY v2     │
                     │  28-dim Latent Descriptors  │
                     │  Volume Frac, Stokes Risk   │
                     └──────────────┬──────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │    5-SURROGATE ENSEMBLE     │
                     │  ElasticNet, RF, ET, GBR, GP│
                     │  Hardness, Transfer, DropPt │
                     └──────────────┬──────────────┘
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          ▼                                                   ▼
┌─────────────────────────────┐                     ┌─────────────────────────────┐
│  GROUP CONFORMAL CALIBRATOR │                     │    COMPOSITE OOD DETECTOR   │
│  Locally Adaptive Residuals │                     │  Mahalanobis + kNN +        │
│  Finite-Sample 90% Coverage │                     │  Disagreement + Hyperbox    │
└──────────────┬──────────────┘                     └──────────────┬──────────────┘
               │                                                   │
               └──────────────────────────┬────────────────────────┘
                                          ▼
                     ┌────────────────────────────────────────┐
                     │   CALIBRATED ACQUISITION ENGINE v2     │
                     │   Tri-Criteria Utility Function:       │
                     │   InfoGain × SpecRel × DomainCov       │
                     └────────────────────┬───────────────────┘
                                          ▼
                     ┌────────────────────────────────────────┐
                     │       PHYSICAL PILOT EXECUTION         │
                     │   Targeted Calibration: N=1 Batch      │
                     │   Strict Lineage: GS40_CAL_001         │
                     └────────────────────────────────────────┘
```

---

## 2. Core Modules & Component Inventory

| Component | Source Path | Description | Status |
|---|---|---|---|
| **Feature Engine** | `src/modeling/feature_engine.py` | Calculates true-density volume fractions ($\phi$), BET powder surface area, Stokes-Bingham sedimentation risk | Operational |
| **Multi-Surrogate** | `src/modeling/surrogate_engine.py` | 5 response ensembles (Hardness, Transfer, Drop Point, Settling Risk, Glide CoF) | Operational |
| **Conformal Calibrator**| `src/modeling/uncertainty_calibration.py` | Group K-Fold split & finite-sample adaptive conformal non-conformity quantiles ($s_i = \|e_i\| / \sigma_i$) | Operational |
| **Composite OOD** | `src/modeling/composite_ood.py` | 4 orthogonal signals: Mahalanobis ($D_M$), kNN density, ensemble $CV$, hyperbox range | Operational |
| **Acquisition Utility** | `src/modeling/calibrated_acquisition.py`| Multi-objective utility: $\text{InfoGain} \times \text{SpecRelevance} \times \text{DomainCoverage}$ | Operational |
| **Candidate Generator** | `src/doe/virtual_generator.py` | Vectorized Monte Carlo generator with percolation, solid fraction, and binder constraints | Operational |
| **Pilot Matrix** | `data/doe/pilot_doe_run_matrix_rev1.0.csv` | 18 planned DOE trials (16 Primary orthogonal + 2 Supplemental temperature probes) | Frozen |
| **Gatekeeper** | `src/modeling/qualification_gate.py` | Rev 2.0 qualification firewall enforcing Zero Synthetic Fallbacks & Exact LOF $F$-test | Operational |

---

## 3. Product Specification Baselines (Rev.7.3)

| Performance Attribute | Target Nominal | Specification Acceptance Window | Primary Measurement SOP |
|---|---|---|---|
| **Hardness ($H$)** | 800 gf | **750.0 ~ 900.0 gf** | 2mm cylindrical needle probe, 1.0 mm/s, 25.0°C |
| **Pay-off / Transfer ($T$)** | 0.048 g | **$\ge 0.0400\text{ g}$** | Artificial bioskin / rough card substrate, 100g load |
| **Drop Point ($T_{\text{drop}}$)** | 61.5 °C | **60.0 ~ 63.5 °C** | Mettler Drop Point / DSC onset |
| **Sedimentation Risk** | Low (< 1.0) | **$\le 1.50$ (Arrested settling)**| Stokes-Bingham network calculation & 24h scan |
| **Dynamic Glide CoF** | 0.145 | **0.130 ~ 0.160** | Universal friction analyzer, 100g load, 25°C |

---

## 4. Current State Limitations & Invariants

1. **Current Physical GS40 Calibration Count: $N = 0$.**
   No commercial GS40 stick has yet been manufactured or measured. All current model predictions reflect public literature priors combined with empirical physics assumptions.
2. **`VIRTUAL_PASS` Scope:**
   `VIRTUAL_PASS` denotes high confidence and in-spec behavior under current domain priors. It acts as an internal **physical test waiver candidate**, NOT a commercial release certification.
3. **P002 Boundary Nature:**
   Run `GS40-P002` possesses the highest raw prediction variance but predicts hardness at 668.4 gf (below specification). It functions as a **Boundary Probe**, while `GS40-P001` serves as the primary safe-domain calibration candidate.

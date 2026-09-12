# GLIDE-SPEC 40 - Domain Priors & Mechanistic Datasets (Layer 0)

This directory contains public domain scientific benchmark datasets and raw measurement tables for solid sticks, wax-oil lubricants, and natural wax batch variability.

## 🛡️ Strict Qualification Firewall Rule

All data residing in `benchmarks/domain_priors/` is tagged as `DataOrigin.PUBLIC_BENCHMARK`.  
It is **STRICTLY PROHIBITED** from qualifying or training the final GS-40 production model.  
Production qualification is governed solely by `SOP-GS40-PILOT-001` (`DataOrigin.REAL_PILOT`).

These datasets serve exclusively as **Layer 0 Domain Priors** to inform the **Layer 1 Virtual Mechanistic Simulator** before physical pilot data arrives.

---

## 1. Inventory of Domain Prior Datasets

### A. Imperial College London — Wax-Oil Lubricants (Nature Sci. Rep. 2021)
- **Directory:** `benchmarks/domain_priors/imperial_friction/`
- **Source:** *Wax-oil lubricants to reduce the shear between skin and PPE*, *Nature Sci. Rep.* 11, 11756 (2021). [PMC8173004](https://pmc.ncbi.nlm.nih.gov/articles/PMC8173004/)
- **Target Metrics:**
  - In-vivo human skin vs. PDMS dynamic coefficient of friction (CoF @ 2000 Hz)
  - Instantaneous CoF vs. 4-hour sustained wear CoF
  - Wax ratio ($0 \sim 30\%$) and oil polarity (polar triglyceride vs. non-polar mineral hydrocarbon)
- **GS-40 Application:** Calibrates the virtual slip & dynamic friction model at the skin interface.

### B. 17% Wax System Cosmetic Stick Benchmark (Int. J. Cosmet. Sci. 2020)
- **Directory:** `benchmarks/domain_priors/lipstick_17pct_anchor/`
- **Source:** *Evaluation of alkenones, a renewably sourced, plant-derived wax as a structuring agent for lipsticks*, *Int. J. Cosmet. Sci.* 42, 292–302 (2020). [PMC9291794](https://pmc.ncbi.nlm.nih.gov/articles/PMC9291794/)
- **Target Metrics:**
  - Wax matrix total: **Exact 17.0 wt%** (Microcrystalline 3.5%, Ozokerite 3.5%, Candelilla 7.0%, Carnauba 3.0%)
  - Thermal Drop Point (DSC peak): **$60.3^\circ\text{C}$**
  - Pay-off to human skin: **$14 \pm 2\,\text{mg}$** (3 strokes)
  - Pay-off to fabric: **$61 \pm 3\,\text{mg}$**
  - Needle penetration firmness ($gf$) & 3-point bending hardness
- **GS-40 Application:** Serves as the primary physical reference anchor for the 17% wax formulation space.

### C. TU Berlin — Natural Wax Batch-to-Batch Variability (Zenodo 2026)
- **Directory:** `benchmarks/domain_priors/tuberlin_wax_variability/`
- **Source:** *Natural wax batch-to-batch variability – Implications for oleogel application*, TU Berlin. [DOI: 10.5281/zenodo.18458747](https://doi.org/10.5281/zenodo.18458747)
- **Target Metrics:**
  - Candelilla wax (CLX), Beeswax (BWX), Carnauba (CRX), Rice Bran (RBX) supplier lot variability
  - Complex shear modulus ($G^*_{\max}$ at $5^\circ\text{C}$) and gelation temperatures ($T_{\text{gel start}}$, $T_{\text{gel end}}$)
  - Chemical constituent distributions (alkanes, wax esters, free fatty acids)
- **GS-40 Application:** Supplies real-world coefficient of variation ($\text{CV} \approx 15 \sim 25\%$) for the Monte Carlo raw material tolerance simulator.

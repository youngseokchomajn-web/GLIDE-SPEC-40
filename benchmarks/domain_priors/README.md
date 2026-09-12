# GLIDE-SPEC 40 - Domain Priors & Mechanistic Datasets (Layer 0)

This directory contains public domain scientific benchmark datasets and raw measurement tables for solid sticks, wax-oil lubricants, anhydrous powder-in-sticks, and natural wax batch variability.

## 🛡️ Strict Qualification Firewall Rule

All data residing in `benchmarks/domain_priors/` is tagged as `DataOrigin.PUBLIC_BENCHMARK`.  
It is **STRICTLY PROHIBITED** from qualifying or training the final GS-40 production model.  
Production qualification is governed solely by `SOP-GS40-PILOT-001` (`DataOrigin.REAL_PILOT`).

These datasets serve exclusively as **Layer 0 Domain Priors** to inform the **Layer 1 Virtual Mechanistic Simulator** before physical pilot data arrives.

---

## 1. Inventory of Domain Prior Datasets (5 Scientific Assets)

### A. Imperial College London — Wax-Oil Lubricants (Nature Sci. Rep. 2021)
- **Directory:** `benchmarks/domain_priors/imperial_friction/`
- **File:** `wax_oil_friction_data.csv`
- **Source:** *Wax-oil lubricants to reduce the shear between skin and PPE*, *Nature Sci. Rep.* 11, 11756 (2021). [PMC8173004](https://pmc.ncbi.nlm.nih.gov/articles/PMC8173004/)
- **Target Metrics:**
  - In-vivo human skin vs. PDMS dynamic coefficient of friction (CoF @ 2000 Hz)
  - Instantaneous CoF vs. 4-hour sustained wear CoF
  - Wax ratio ($0 \sim 30\%$) and oil polarity (polar triglyceride vs. non-polar mineral hydrocarbon)
- **GS-40 Role:** Calibrates the virtual slip & dynamic friction model at the skin interface.

### B. 17% Wax System Cosmetic Stick Benchmark (Int. J. Cosmet. Sci. 2020)
- **Directory:** `benchmarks/domain_priors/lipstick_17pct_anchor/`
- **File:** `lipstick_17pct_wax_benchmark.csv`
- **Source:** *Evaluation of alkenones, a renewably sourced, plant-derived wax as a structuring agent for lipsticks*, *Int. J. Cosmet. Sci.* 42, 292–302 (2020). [PMC9291794](https://pmc.ncbi.nlm.nih.gov/articles/PMC9291794/)
- **Target Metrics:**
  - Wax matrix total: **Exact 17.0 wt%** (Microcrystalline 3.5%, Ozokerite 3.5%, Candelilla 7.0%, Carnauba 3.0%)
  - Thermal Drop Point (DSC peak): **$60.3^\circ\text{C}$**
  - Pay-off to human skin: **$14 \pm 2\,\text{mg}$** (3 strokes)
  - Pay-off to fabric: **$61 \pm 3\,\text{mg}$**
  - Needle penetration firmness ($gf$) & 3-point bending hardness
- **GS-40 Role:** Serves as the primary physical reference anchor for the 17% wax formulation space.

### C. TU Berlin — Natural Wax Batch-to-Batch Variability (Zenodo 2026)
- **Directory:** `benchmarks/domain_priors/tuberlin_wax_variability/`
- **Files:** `natural_wax_batch_variability_summary.csv`, `Rheology.xlsx`, `LC_mass_percentages.xlsx`
- **Source:** *Natural wax batch-to-batch variability – Implications for oleogel application*, TU Berlin. [DOI: 10.5281/zenodo.18458747](https://doi.org/10.5281/zenodo.18458747)
- **Target Metrics:**
  - Candelilla wax (CLX), Beeswax (BWX), Carnauba (CRX), Rice Bran (RBX) supplier lot variability
  - Complex shear modulus ($G^*_{\max}$ at $5^\circ\text{C}$) and gelation temperatures ($T_{\text{gel start}}$, $T_{\text{gel end}}$)
  - Chemical constituent distributions (alkanes, wax esters, free fatty acids)
- **GS-40 Role:** Supplies real-world coefficient of variation ($\text{CV} \approx 15 \sim 25\%$) for the Monte Carlo raw material tolerance simulator.

### D. Anhydrous Powder-in-Stick Formulation Matrix (US Patent 20070166254)
- **Directory:** `benchmarks/domain_priors/anhydrous_stick_patents/`
- **File:** `us20070166254_anhydrous_powder_stick.csv`
- **Source:** *Anhydrous antiperspirant stick composition*, US Patent 20070166254A1 (Procter & Gamble / Gillette).
- **Target Metrics:**
  - 11 formulations combining solidifying waxes (Castor wax, stearyl alcohol, PE wax, 21~24%), volatile silicone (cyclomethicone, 8~30%), Dimethicone (50 cSt, 1%), C12-15 Alkyl Benzoate (5~31%), and **high particulate powder loading (20~25% AAZG, Talc, Silica)**.
  - Penetration hardness ($mm$ and $gf$), 4-stroke pay-off weight loss ($cg = 10\,\text{mg}$), and fabric whiteness transfer.
- **GS-40 Role:** Provides real formulation $\rightarrow$ hardness & transfer curves for 20~25% powder-loaded anhydrous sticks with volatile silicone and C12-15 alkyl benzoate.

### E. Commercial Lip Balm Structural Lipid Architecture (MDPI Cosmetics 2024)
- **Directory:** `benchmarks/domain_priors/commercial_stick_benchmark/`
- **File:** `mdpi_commercial_lipbalm_texture_sla.csv`
- **Source:** *Beyond Brand Popularity: Decoding Lip Balm Performance Through Lipid Structural Architecture*, *Cosmetics* 13(4), 200 (2024). [DOI: 10.3390/cosmetics13040200](https://doi.org/10.3390/cosmetics13040200)
- **Target Metrics:**
  - 7 commercial benchmark sticks analyzed by Brookfield CT3 texture analyzer.
  - Hardness-mechanical work correlation ($r = 0.950, p = 0.001$).
  - Structural failure rates (76.9% consumer fracture rate in single-wax systems vs. superior cohesion in complementary multi-wax systems).
- **GS-40 Role:** Validates that multi-wax systems (Synthetic Wax + Candelilla) are structurally necessary to prevent shear fracture.

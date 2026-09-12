# GLIDE-SPEC 40 - Public Domain Priors & Scientific Benchmark Base (Layer 0)

This directory houses the curated scientific datasets, patent matrices, and raw rheological measurements used as **Layer 0 Domain Priors** to guide the **Layer 1 Virtual Mechanistic Simulator** prior to physical GS-40 pilot manufacturing.

---

## 🛡️ Strict Qualification Firewall & Non-Equivalence Principles

All records in `benchmarks/domain_priors/` are tagged as `DataOrigin.PUBLIC_BENCHMARK`.  
They are **STRICTLY PROHIBITED** from qualifying, training, or modifying the production M4 empirical model. Production qualification is governed solely by `SOP-GS40-PILOT-001` (`DataOrigin.REAL_PILOT`).

### The 4 Golden Non-Equivalence Principles:
1. **Hardness Prior ≠ GS40 Hardness Prediction**  
   (Wax/powder base scaled by engineering transformation; not a calibrated physical test value).
2. **Thermal Transition Prior ≠ GS40 Mettler Drop Point**  
   (Thermodynamic DSC melting endotherm peak is physical-chemically distinct from gravity dripping flow under ASTM D127 / IP 396).
3. **Pay-off Anchor ≠ GS40 Physical Transfer (g)**  
   (Literature stroke, substrate, load, and ambient temperature differ from GS-40 SOP-001 10°C synthetic skin protocol).
4. **Tribology Prior Index ≠ GS40 Dynamic CoF**  
   (Friction index reflects external PDMS-skin shear trends, not direct GS-40 stick surface friction).

---

## 🏛️ Public Domain Prior 4-Category Architecture

```text
PUBLIC DOMAIN
│
├── A. FORMULATION → RESPONSE
│   ├── P&G Anhydrous Powder Stick (US20070166254: 20-25% powder, silicone, wax)
│   ├── Lipstick 17% Wax Benchmark (Huynh et al. 2020: 17% wax, DSC, pay-off)
│   └── Commercial Lip Balm SLA (Cosmetics 2024: 7 stick texture benchmark)
│
├── B. TRIBOLOGY
│   ├── Imperial Wax-Oil Friction (Yap et al. 2021: wax-oil skin CoF 0.16-0.29)
│   └── Silicone & Powder Skin Tribology (Masen et al. 2020: Dimethicone CoF 0.20, Talc CoF 0.22)
│
├── C. RAW MATERIAL VARIABILITY
│   └── TU Berlin Wax Lots (Zenodo 2026: Candelilla G* CV 20.4%)
│
└── D. GENERAL FORMULATION ML QA
    └── Nature Shampoo 812 (Nature 2023: ML benchmark)
```

---

## 1. Category A: Formulation → Response Benchmarks

### 1. P&G Anhydrous Powder-in-Stick (US Patent 20070166254)
- **Path:** `benchmarks/domain_priors/anhydrous_stick_patents/us20070166254_anhydrous_powder_stick.csv`
- **Citation:** US Patent 20070166254A1 (Procter & Gamble / Gillette).
- **Key Metrics:** 11 formulations combining 21~24% waxes, volatile silicone (cyclomethicone 8~30%), Dimethicone 50 cSt, C12-15 Alkyl Benzoate, and **20~25% particulate powder (AAZG, Talc, Silica)**.
- **GS-40 Role:** Formulation-space nearest neighbor providing empirical evidence for particulate-induced stiffening (~1.8-2.2x) and pay-off control.

### 2. 17% Wax System Cosmetic Stick Anchor (Int. J. Cosmet. Sci. 2020)
- **Path:** `benchmarks/domain_priors/lipstick_17pct_anchor/lipstick_17pct_wax_benchmark.csv`
- **Citation:** Huynh et al., *Int. J. Cosmet. Sci.* 42, 292–302 (2020). [PMC9291794](https://pmc.ncbi.nlm.nih.gov/articles/PMC9291794/)
- **Key Metrics:** **Exact 17.0 wt% wax** matrix, DSC melting peak at **$60.3^\circ\text{C}$**, human skin pay-off **$14 \pm 2\,\text{mg}$**, base wax needle firmness 165 gf.
- **GS-40 Role:** Physical reference anchor for the 17% wax backbone.

### 3. Commercial Lip Balm Structural Lipid Architecture (MDPI Cosmetics 2024)
- **Path:** `benchmarks/domain_priors/commercial_stick_benchmark/mdpi_commercial_lipbalm_texture_sla.csv`
- **Citation:** *Cosmetics* 13(4), 200 (2024). [DOI: 10.3390/cosmetics13040200](https://doi.org/10.3390/cosmetics13040200)
- **Key Metrics:** 7 commercial benchmark sticks analyzed by Brookfield CT3 texture analyzer ($r = 0.950$ work-hardness correlation).
- **GS-40 Role:** External commercial reality benchmark confirming multi-wax synergy (Synthetic Wax + Candelilla).

---

## 2. Category B: Tribology Benchmarks

### 1. Imperial College Wax-Oil Skin Tribology (Nature Sci. Rep. 2021)
- **Path:** `benchmarks/domain_priors/imperial_friction/wax_oil_friction_data.csv`
- **Citation:** Yap et al., *Nature Sci. Rep.* 11, 11756 (2021). [PMC8173004](https://pmc.ncbi.nlm.nih.gov/articles/PMC8173004/)
- **Key Metrics:** In-vivo human skin vs. PDMS dynamic friction ($\text{CoF} \approx 0.16 \sim 0.29$), 4-hour durability.
- **GS-40 Role:** Boundary lubrication model for wax-oil skin contact.

### 2. Silicone & Powder Skin Tribology (PLOS ONE 2020 / Southampton 2024)
- **Path:** `benchmarks/domain_priors/silicone_skin_tribology/silicone_powder_skin_tribology_benchmark.csv`
- **Citation:** Masen et al., *PLOS ONE* 15(9), e0239363 (2020) [PMC7514078](https://pmc.ncbi.nlm.nih.gov/articles/PMC7514078/) & Carr et al., *Proc. Inst. Mech. Eng. H* (2024) [PMC11318204](https://pmc.ncbi.nlm.nih.gov/articles/PMC11318204/).
- **Key Metrics:** In-vivo human skin friction under Dimethicone/Dimethiconol lube ($\text{CoF} \approx 0.20$), Talcum powder ($\text{CoF} \approx 0.22$), and silicone barrier films ($\text{CoF} \approx 0.38 \sim 0.55$) vs. unlubricated skin ($\text{CoF} \approx 0.92$).
- **GS-40 Role:** Bridges the silicone fluid and inorganic powder tribological lubrication mechanism directly to human skin.

---

## 3. Category C: Raw Material Lot Variability

### 1. TU Berlin Natural Wax Lot-to-Lot Variability (Zenodo 2026)
- **Path:** `benchmarks/domain_priors/tuberlin_wax_variability/`
- **Citation:** TU Berlin (2026). [DOI: 10.5281/zenodo.18458747](https://doi.org/10.5281/zenodo.18458747)
- **Key Metrics:** Candelilla wax Lot-to-Lot shear modulus variability ($\text{CV} \approx 20.4\%$).
- **GS-40 Role:** Supplies raw material lot variance prior, transmitted hierarchically through the composite wax-powder-resin network.

---

## 4. Category D: General Formulation ML QA

### 1. Nature Shampoo 812 ML Benchmark
- **Path:** `benchmarks/shampoo/`
- **Citation:** *Nature Machine Intelligence* (2023).
- **GS-40 Role:** Mathematical regression engine qualification and ANOVA lack-of-fit validation testing ground.

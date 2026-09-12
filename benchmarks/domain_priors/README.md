# GLIDE-SPEC 40 - Public Domain Priors & Scientific Benchmark Base (Layer 0)

This directory houses curated scientific datasets, patent formulation matrices, multimodal rheological sweeps, and thermal crystallization profiles used as **Layer 0 Domain Priors** to guide the **Layer 1 Virtual Mechanistic Simulator** prior to physical GS-40 pilot manufacturing.

---

## 🛡️ Strict Qualification Firewall & Non-Equivalence Principles

All records in `benchmarks/domain_priors/` are tagged as `DataOrigin.PUBLIC_BENCHMARK`.  
They are **STRICTLY PROHIBITED** from qualifying, training, or modifying the production M4 empirical model. Production qualification is governed solely by `SOP-GS40-PILOT-001` (`DataOrigin.REAL_PILOT`).

### The 4 Golden Non-Equivalence Principles:
1. **Hardness Prior ≠ GS40 Hardness Prediction** (Wax/powder base scaled by empirical regression; not a calibrated physical test value).
2. **Thermal Transition Prior ≠ GS40 Mettler Drop Point** (DSC crystal melting endotherm physically differs from gravity dripping under ASTM D127 / IP 396).
3. **Pay-off Anchor ≠ GS40 Physical Transfer (g)** (Literature forearm pay-off is an uncalibrated Prior Transfer Index, not physical mass).
4. **Tribology Prior Index ≠ GS40 Dynamic CoF** (Sliding finger/PDMS probe shear index provides directional guidance, not final stick glide CoF).

---

## 🏛️ Public Domain Prior 4-Category Architecture

```text
PUBLIC DOMAIN
│
├── A. FORMULATION → RESPONSE & STABILITY
│   ├── P&G Anhydrous Powder Stick (US20070166254: 20-25% powder, silicone, wax)
│   ├── Lipstick 384 Longitudinal Matrix (Huynh et al. 2020: 17% wax, 25/45°C 12-week aging)
│   ├── Commercial Lip Balm SLA (Cosmetics 2024: 7 stick texture benchmark)
│   └── Wax Oleogel Hardness (Doan et al. 2022: concentration vs. firmness)
│
├── B. MULTIMODAL RHEOLOGY & TRIBOLOGY
│   ├── 2026 Lipstick Multimodal Rheology (Soft Matter 2026: SAOS, LAOS, creep, relaxation, cooling rate)
│   ├── 2021 Organogel Lipstick (MDPI Gels 2021: G'/G'' thermal ramp, gel-sol crossover)
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

## 🔄 4-Tier Data Pipeline Architecture

```text
Tier 1: SOURCE_RAW        ──▶ Original papers, patent specs, and SI raw text data
Tier 2: NORMALIZED        ──▶ Standardized tabular CSVs matching schema.json units
Tier 3: DOMAIN_PRIOR      ──▶ Cross-domain scaling equations and parameter bounds
Tier 4: DERIVED_FEATURE   ──▶ Crossover temps (T_gel-sol), relaxation time (tau=10s), cooling sensitivity
```

---

## ⚖️ Intellectual Property & Licensing Safeguards

| Directory | Primary Publication & DOI | License | Usage Boundary |
|---|---|---|---|
| `lipstick_rheology_2026/` | *Soft Matter* (2026), 10.1039/D5SM01032B | **CC BY-NC 3.0** | Research, feature extraction & physical prior only. No commercial distribution. |
| `organogel_lipstick_2021/` | *Gels* (2021), 10.3390/gels7030097 | **CC BY 4.0** | Unrestricted open access for academic & commercial development. |
| `lipstick_384/` | *Int. J. Cosmet. Sci.* (2020), 10.1111/ics.12597 | **CC BY-NC-ND 4.0** | Non-commercial prior benchmarking & feature extraction. |
| `wax_oleogel_hardness/` | *Food Hydrocolloids* (2022), 10.1016/j.foodhyd.2022.107794 | Open Archive | Concentration regression & modulus scaling. |
| `silicone_skin_tribology/` | *PLOS ONE* (2020), 10.1371/journal.pone.0239363 | **CC BY 4.0** | Open access biotribology benchmark. |

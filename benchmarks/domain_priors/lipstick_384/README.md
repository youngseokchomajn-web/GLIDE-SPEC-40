# 384 Specimen Lipstick Benchmark & 12-Week Stability Matrix

This directory documents the 384-specimen longitudinal cosmetic stick dataset from:

> **Huynh, Sharma, O'Neil, et al. (2020)**  
> *Evaluation of alkenones, a renewably sourced, plant-derived wax as a structuring agent for lipsticks*  
> *Int. J. Cosmet. Sci.* 42, 292–302. DOI: [10.1111/ics.12597](https://doi.org/10.1111/ics.12597) / [PMC9291794](https://pmc.ncbi.nlm.nih.gov/articles/PMC9291794/)

---

## 🔍 Dataset Truth & Clarification Notice

As verified in the study text, **384 lipsticks were manufactured across an experimental design of 4 formulations (L1, L2, L3, L4), 2 temperatures (25°C, 45°C), 4 aging timepoints (Day 1, Week 4, Week 8, Week 12), and replicate specimens ($N=12$)**:
$$4 \text{ formulations} \times 2 \text{ temperatures} \times 4 \text{ timepoints} \times 12 \text{ replicates} = 384 \text{ tested lipstick sticks}$$

This dataset provides the most comprehensive physical longitudinal data available in the cosmetic stick domain for:
- 3-point bending hardness ($N$)
- Bending stiffness ($N/mm$)
- Needle penetration firmness ($gf$)
- Skin pay-off & fabric transfer ($mg$)
- 3-cycle kinetic friction traces
- 25°C vs. 45°C 12-week aging kinetics

---

## 🛡️ STRICT FIREWALL & USAGE SCOPE

```text
DOMAIN PRIOR ONLY
These datasets are NOT GS40 production training data.
They serve exclusively as Layer 0 priors for:
  - 17% wax substitution mechanics (Ozokerite vs Candelilla vs Microcrystalline vs Alkenone)
  - Longitudinal aging degradation rates (Day 1 → W4 → W8 → W12)
  - Thermal acceleration factors (45°C stress vs 25°C nominal)
```

---

## 📂 Subdirectory Structure
- `source.md`: Primary reference and experimental protocol details.
- `license.md`: CC BY-NC-ND 4.0 open access terms.
- `raw/`: Direct text and tabular extractions from PMC9291794.
- `normalized/`: Cleaned tabular dataset of the 4 formulations across all stability timepoints and mechanical tests.
- `mapping/`: Mathematical feature mapping to GS-40 coordinates.

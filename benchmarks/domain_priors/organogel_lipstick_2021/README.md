# Organogel-Based Lipstick Benchmark (MDPI Gels 2021)

This directory contains standardized thermal-rheology sweeps ($G', G'', \tan\delta$ vs. temperature), gel-sol transition temperatures ($T_{\text{gel-sol}}$ at $G'=G''$), and texture analyzer physical metrics from:

> **MDPI Gels (2021), 7(3), 97**  
> *Preparation, Characterization and Evaluation of Organogel-Based Lipstick Formulations: Application in Cosmetics*  
> DOI: [10.3390/gels7030097](https://doi.org/10.3390/gels7030097)

---

## 🛡️ STRICT FIREWALL & USAGE SCOPE

```text
DOMAIN PRIOR ONLY
These datasets are NOT GS40 production training data.
They serve exclusively as Layer 0 priors for:
  - G' / G'' thermal ramp profiles (20°C to 150°C at 1°C/min)
  - Gel-sol crossover temperature determination (G' = G'')
  - Heating vs. cooling thermal hysteresis modeling
  - Needle penetration firmness vs. bending stiffness correlations
```

---

## ⚖️ License Notice
Open access under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE.md`](./LICENSE.md).

---

## 📂 Subdirectory Structure
- `SOURCE.md`: Experimental instrument parameters (TA AR1000, parallel plate 8 mm, gap 0.7 mm, 1 Hz, 1% strain).
- `LICENSE.md`: CC BY 4.0 license text.
- `raw/`: Raw supplementary table extracts and temperature sweep traces.
- `normalized/`: 5 organogel lipstick formulations (F1 to F5) with mechanical firmness, bending stiffness, pay-off, and sensory ratings.
- `derived_features/`: Extracted $T_{\text{gel-sol}}$, thermal hysteresis $\Delta T_{\text{hyst}}$, and plateau modulus $G'_0$.

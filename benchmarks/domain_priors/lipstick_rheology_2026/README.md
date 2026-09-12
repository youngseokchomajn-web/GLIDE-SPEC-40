# Lipstick Multimodal Rheology & Microstructure Benchmark (Soft Matter 2026)

This directory contains curated rheological datasets, cooling-rate microstructural metrics, and nonlinear viscoelastic response tables from the 2026 landmark study on lipstick physics:

> **Gautier, To, Botte, Dupire, Rouxel, & Artzner (2026)**  
> *Lipstick structure revealed by multimodal strain- and time-dependent rheology*  
> **Soft Matter** (Royal Society of Chemistry). DOI: [10.1039/D5SM01032B](https://doi.org/10.1039/D5SM01032B)

---

## 🛡️ STRICT FIREWALL & USAGE SCOPE

```text
DOMAIN PRIOR ONLY
These datasets are NOT GS40 production training data.
They may be used for:
  - physical prior construction (viscoelastic bounds)
  - cooling rate sensitivity modeling (0.1 vs 1 vs 10 °C/min)
  - relaxation regime feature extraction (short-term vs long-term decay)
  - surrogate-model initialization
They must NOT be used as evidence of GS40 production qualification.
```

---

## ⚖️ License Notice

This dataset is derived from an open access publication licensed under **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)**.  
See [`LICENSE.md`](./LICENSE.md) and [`SOURCE.md`](./SOURCE.md) for details.

---

## 📂 Subdirectory Structure

- `SOURCE.md`: Complete citation, DOI, author affiliation, and experimental instrument metadata.
- `LICENSE.md`: CC BY-NC 3.0 terms and commercial boundary conditions.
- `schema.json`: Unified 35-field data schema for multimodal rheology.
- `raw/`: Metadata and instructions for downloading the full 26.9 MB Supplementary Information ZIP.
- `normalized/`: Normalized CSV tables of linear/nonlinear rheology ($G', G'', \tan\delta$, creep, LAOS).
- `thermal_history/`: Cooling rate ($0.1, 1.0, 10.0^\circ\text{C/min}$) vs. crystal size, birefringence, and wax network rigidity.
- `derived_features/`: Extracted physical features for GLIDE-SPEC 40 (yield stress, 10-second relaxation inflection, thermal modulus transition).

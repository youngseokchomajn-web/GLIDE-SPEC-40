# GLIDE-SPEC 40: Data Provenance & Provenance Tagging Policy

- **Standard Authority:** SOP-GS40-DAT-001
- **Effective Version:** Rev.8.1
- **Status:** Mandatory Enforcement

---

## 1. Data Classification Taxonomy

All feature descriptors, training inputs, and model outputs must be explicitly tagged with one of the following 6 provenance categories:

```text
                               DATA PROVENANCE HIERARCHY
┌────────────────────────────────────────────────────────────────────────┐
│  1. GS40 MEASURED (Gold Standard, Highest Priority)                    │
│     - Physical measurements conducted directly on GLIDE-SPEC 40        │
│     - Strict batch, lot, operator, and raw material CoA lineage        │
│     - Current Status: N = 0                                            │
├────────────────────────────────────────────────────────────────────────┤
│  2. PUBLIC MEASURED (High Reliability Baseline)                         │
│     - Empirical data extracted from peer-reviewed literature or patents│
│     - Identical chemical system under documented ASTM/ISO SOPs         │
├────────────────────────────────────────────────────────────────────────┤
│  3. EXTERNAL MEASURED (Domain Cross-Reference)                         │
│     - Measurements on analogous cosmetic/stick systems                 │
│     - Example: CN102341090B artificial leather CoF                     │
├────────────────────────────────────────────────────────────────────────┤
│  4. DERIVED PHYSICAL (First-Principles Calculation)                    │
│     - Computed using deterministic physical/geometric equations        │
│     - Examples: True density volume fractions (phi), Stokes settling   │
├────────────────────────────────────────────────────────────────────────┤
│  5. DERIVED EMPIRICAL (Statistical Regression / Surrogate)             │
│     - Fitted statistical regression models                             │
│     - Example: Power-law shear thinning, lubricity synergism           │
├────────────────────────────────────────────────────────────────────────┤
│  6. HYPOTHESIS (Design Assumption, Subject to Falsification)           │
│     - Engineering assumptions awaiting empirical pilot validation      │
│     - Example: Fumed silica percolation threshold c* = 1.5 wt%         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Provenance Tagging Invariants

1. **No Data Without Lineage:**
   Any data row added to training matrices must reference a source DOI, Patent Number, Laboratory Notebook entry, or Manufacturing Batch ID.
2. **Replicate vs. Independent Formulation Transparency:**
   Multi-temperature sweeps (e.g. 25°C, 40°C, 45°C) and stability timepoints (1w, 4w, 12w) of a single base formulation must NOT be counted as independent formulation samples in model degrees-of-freedom calculations.
3. **Hypothesis Demotion Rule:**
   Any parameter tagged as `HYPOTHESIS` that exhibits discordance during physical pilot testing is automatically flagged for elimination or empirical replacement.

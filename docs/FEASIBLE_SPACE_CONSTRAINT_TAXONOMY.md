# GS40 Feasible Space Constraint & Threshold Taxonomy

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-13  
**Governing Decision:** ORC-019 / GEM-TASK-019  
**Status:** ACTIVE & BINDING  

In strict compliance with **ORC-019 Action 4**, every threshold and boundary defining Zones A through E is categorized under one of four rigorous epistemic classifications:
1. `PRODUCT_SPEC`: Defined by commercial finished good product performance requirements.
2. `LITERATURE_PRIOR`: Grounded in published, peer-reviewed physical/rheological literature.
3. `MODEL_ASSUMPTION`: Theoretical surrogate boundary or interpolation support limit.
4. `PHYSICALLY_UNVERIFIED`: Working hypothesis requiring physical GS40 pilot confirmation.

---

## 1. Parameter & Threshold Epistemic Classification Table

| Zone | Parameter / Boundary | Value / Range | Epistemic Classification | Provenance & Justification |
|---|---|:---:|:---:|---|
| **Zone A (Nominal Core)** | Total Wax Concentration | $11.0–13.0\\%$ | `PRODUCT_SPEC` | Target hardness design envelope for optimal stick pay-off without breakage. |
| **Zone A (Nominal Core)** | Dimethicone Concentration | $15.0–19.0\\%$ | `PRODUCT_SPEC` | Cosmetic slip and non-greasy sensory specification. |
| **Zone A (Nominal Core)** | Pour / Fill Temperature | $78.0–82.0\\text{ °C}$ | `LITERATURE_PRIOR` | Complete wax dissolution temperature reported in Doan (2022) & MDPI Gels (2021). |
| **Zone A (Nominal Core)** | Slurry Yield Stress ($S_y$) | $\\ge 8.5\\text{ Pa}$ | `PHYSICALLY_UNVERIFIED` | Stokes-Bingham anti-settling hypothesis (Pre-pilot hypothesis in Layer 0 priors). |
| **Zone A (Nominal Core)** | Friction Pay-off | $10.0–18.0\\text{ mg}$ | `PRODUCT_SPEC` | Target deposition mass per 2-stroke application on human skin / bioskin. |
| **Zone B (Design Space)** | Minimum Wax Concentration | $9.0\\%$ | `LITERATURE_PRIOR` | Critical gelation concentration threshold ($C_g$) for synthetic/carnauba wax oleogels. |
| **Zone B (Design Space)** | Maximum Wax Concentration | $15.0\\%$ | `PRODUCT_SPEC` | Upper hardness boundary to prevent brittle stick fracture during drop tests. |
| **Zone B (Design Space)** | Hardness Design Acceptance | $650–900\\text{ gf}$ | `PRODUCT_SPEC` | Target 2mm needle penetration resistance window at 25 °C. |
| **Zone B (Design Space)** | Melting Transition Peak ($T_m$) | $\\ge 60.0\\text{ °C}$ | `LITERATURE_PRIOR` | Thermal stability threshold preventing stick softening in 45 °C hot-stability storage (Soft Matter 2026). |
| **Zone C (Process Marginal)** | Low Fill Temperature | $< 75.0\\text{ °C}$ | `MODEL_ASSUMPTION` | Risk of premature crystallization in dispensing nozzles causing bulk voids. |
| **Zone C (Process Marginal)** | High Fill Temperature | $> 85.0\\text{ °C}$ | `MODEL_ASSUMPTION` | Risk of volatile silicone loss and oxidative thermal stress. |
| **Zone D (Extrapolative)** | Wax Exploration Buffer | $[7.0, 9.0)\\% \\cup (15.0, 17.0]\\%$ | `MODEL_ASSUMPTION` | Boundary exploration region flagged with elevated composite OOD distance ($1.5 < D \\le 2.5$). |
| **Zone E (Strictly Infeasible)**| Structural Collapse Floor | $< 7.0\\%$ Total Wax | `PHYSICALLY_UNVERIFIED` | Insufficient crystalline network density to support freestanding stick geometry. |
| **Zone E (Strictly Infeasible)**| Extreme Brittleness Ceiling | $> 18.0\\%$ Total Wax | `PHYSICALLY_UNVERIFIED` | High crystalline wax density leading to catastrophic fracture under 150g lateral shear. |
| **Zone E (Strictly Infeasible)**| Mass Balance Integrity | $\\sum m_i \\ne 100.0\\%$ | `PRODUCT_SPEC` | Conservation of formulation mass requirement. |

---

## 2. Governance Rule: Non-Substitution
No threshold marked `PHYSICALLY_UNVERIFIED` or `MODEL_ASSUMPTION` may be treated as empirically established prior to observing physical GS40 pilot batch measurements ($N \\ge 16$).

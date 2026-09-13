# External Validation Governance Ledger & Construct Audit

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-13  
**Governing Decision:** ORC-016 / GEM-TASK-016  
**Status:** ACTIVE & BINDING  

---

## 1. Epistemic Separation: OOD Stress Testing vs. Predictive Qualification

Per **ORC-016**, the repository establishes a strict epistemic boundary between two distinct validation classes:

| Validation Class | Objective | Accepted Evidence | Governance Consequence |
|---|---|---|---|
| **Class A: Epistemic OOD Stress Testing** | Verify whether surrogate uncertainty / OOD detection correctly flags out-of-domain formulations | `GEM-015` on `EXTERNAL_VALIDATION_SET_3` (10/10 samples flagged OOD at $D \\ge 77.2 \\gg 2.5$) | **ACCEPTED.** Proves the model does not produce unwarranted overconfidence in alien domains. |
| **Class B: Construct-Equivalent Predictive Qualification** | Verify surrogate quantitative accuracy ($R^2 \\ge 0.70$, $\\text{RMSE} \\le 65\\text{ gf}$) on commercial GS40 target response | Requires identical physical measurement SOP (2.0 mm cylindrical penetration, 1.0 mm/s, 25 °C) | **REJECTED.** Proxy food oleogels (35 mm bulk compression) cannot establish predictive validity for GS40. |

---

## 2. Standardized Residual & Bias Sign Conventions

To eliminate ambiguity across all future scoring manifests:

1. **Residual Definition:**
   $$\\text{Residual}_i = y_i^{(\\text{measured})} - \\hat{y}_i^{(\\text{predicted})}$$
2. **Directional Bias Definition:**
   $$\\text{Bias} = \\frac{1}{N} \\sum_{i=1}^{N} \\left( y_i^{(\\text{measured})} - \\hat{y}_i^{(\\text{predicted})} \\right)$$
   - $\\text{Bias} > 0$: The surrogate systematically **underpredicts** the observed response (measured force exceeds prediction).
   - $\\text{Bias} < 0$: The surrogate systematically **overpredicts** the observed response (prediction exceeds measured force).
   - In `GEM-015`, the reported bias of $+33,293.40\\text{ gf}$ strictly follows this definition: measured bulk compression force ($13,000–57,000\\text{ gf}$) far exceeded the cosmetic stick prediction ($714–768\\text{ gf}$).

---

## 3. Systematic Literature Audit for GS40-Compatible Penetration Data

Pursuant to Required Actions 4–10 of `ORC-016`:
1. **Target Construct:** Anhydrous wax-oil-silicone sticks tested via needle/cylinder penetration ($\\le 2.0\\text{ mm}$, $20–25\\text{ °C}$, reported in gf or converted from N).
2. **Exclusion / Overlap Audit:**
   - *Huynh et al. (2020) 384 Stick Matrix:* Already locked in `DATASET_FREEZE_1` (DS01).
   - *Doan et al. (2022) Wax Oleogel Hardness:* Already locked in `benchmarks/domain_priors/wax_oleogel_hardness` (DS04).
   - *US Patent 20070166254 Anhydrous Powder Sticks:* Already locked in `benchmarks/domain_priors/anhydrous_stick_patents` (DS06).
   - *Lipstick 17% Wax Benchmark:* Already locked in `benchmarks/domain_priors/lipstick_17pct_anchor` (DS08).
3. **Exhaustive Exhaustion Finding:**
   - All known peer-reviewed publications reporting penetration hardness on cosmetic anhydrous sticks are already accounted for in the baseline training freeze or domain priors.
   - External food-science oleogel literature (Thakur 2022, Yassoralipour 2026, Patel 2015) consistently uses large bulk probes (25–35 mm cylinders) incompatible with the GS40 SOP without empirical geometric calibration.

---

## 4. Formal Escalation: `DATA_REQUIRED` (Required Action 10)

Pursuant to Required Action 10 of `ORC-016`:
> *"If no compatible public dataset can be found, escalate DATA_REQUIRED rather than manufacturing an equivalence mapping or synthetic data."*

GEM hereby submits a formal **`DATA_REQUIRED`** governance finding:
1. **No Artificial Data:** GEM refuses to manufacture synthetic cross-protocol conversion factors or pseudo-equivalent proxy datasets.
2. **Physical Data Requirement:** Genuine predictive qualification of Rev.8.1 requires physical manufacturing/pilot quality control data:
   $$N(\\text{GS40 physical pilot}) > 0$$
3. **Baseline Invariance:** `Rev.8.1` remains 100% frozen. Production qualification remains **NOT QUALIFIED**.

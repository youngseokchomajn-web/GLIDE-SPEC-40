# GS-40 28% Particulate Powder System & Tribology Prior

This directory houses domain prior data, qualitative mechanisms, and external rheology benchmarks for the **28.0 wt% multi-particulate inorganic/silicone powder system** of GLIDE-SPEC 40.

---

## 🛡️ STRICT DATA PROVENANCE & ISOLATION NOTICE

```text
========================================================================================
CRITICAL AUDIT NOTICE: EXTERNAL DATA VS. GS-40 PILOT HYPOTHESIS
========================================================================================
1. FRICTION ATTRIBUTION (CN102341090B Table 11):
   - CoF values (0.138, 0.155) are MEASURED ON FINISHED COSMETIC FORMULATIONS applied
     to artificial leather under a 100 g normal load.
   - They are NOT neat/intrinsic friction coefficients of isolated BN or PMSSQ raw powders.
   - Isolated raw material CoF is tagged as UNSUPPORTED / PENDING_PILOT_MEASUREMENT.

2. R972 YIELD STRESS ATTRIBUTION (Kopylov 2011 & US20030198914):
   - Direct measurements exist for external colloidal suspensions (Kopylov 2011:
     6% -> 122 Pa, 8% -> 190 Pa, 10% -> 365 Pa, 12% -> 545 Pa; US20030198914: 0.5% static onset).
   - The GS-40 condition (2.0 wt% R972 in molten balm matrix yielding ~8.6 Pa at 80°C) is
     a DERIVED_ESTIMATE / PRE-PILOT HYPOTHESIS, NOT an empirical measurement.
   - The assertion of "ZnO zero sedimentation" is a theoretical calculation that MUST
     be verified via physical testing in P001–P018.
========================================================================================
```

---

## 🔄 Prior-to-Pilot Verification Lineage

```text
PUBLIC SCIENTIFIC DATA
  │
  ├── External R972 Rheology: Kopylov (2011), US20030198914, Addit. Manuf. (2026)
  └── Biotribology & Formulation Benchmarks: CN102341090B Table 11, Masen et al. (2020)
       │
       ▼
GS40 DOMAIN PRIOR MODEL (PRE-PILOT HYPOTHESIS)
  │
  ├── Qualitative mechanism: R972 forms thixotropic network to retard ZnO settling
  └── Directional expectation: BN & PMSSQ reduce stick application glide friction
       │
       ▼
GS40 PHYSICAL PILOT EXECUTION (P001 ~ P018)
  │
  ├── 30-min molten holding test: Visual pelleting & Top vs. Bottom ZnO concentration
  └── Stick surface tribology: Bioskin / artificial leather dynamic CoF measurement
       │
       ▼
BAYESIAN CALIBRATION & PRODUCTION QUALIFICATION (Level 4 & 5)
```

---

## 📂 File Inventory

- `powder_system_specs_and_rheology.csv`: Physical specifications ($D_{50}$, BET, density, oil absorption) of the 5 GS-40 functional powders and 3 benchmarks.
- `fumed_silica_thixotropic_yield_stress.csv`: External suspension yield stress measurements (Kopylov 2011, US20030198914) contrasted with the GS-40 pre-pilot hypothesis and pilot verification protocol.
- `powder_friction_and_slip_benchmarks.csv`: Formulation-level artificial leather friction (CN102341090B) and peer-reviewed skin biotribology (Masen 2020), strictly isolated from neat powder properties.

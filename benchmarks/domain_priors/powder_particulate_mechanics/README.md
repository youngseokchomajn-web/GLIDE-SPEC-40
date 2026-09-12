# GS-40 28% Particulate Powder System & Tribology Benchmark

This directory provides the missing physical link for GLIDE-SPEC 40: **the 28% multi-particulate inorganic/silicone powder system**.

While typical lipstick benchmarks only evaluate wax + liquid oil matrices, GLIDE-SPEC 40 incorporates 5 distinct functional powders:
1. **Boron Nitride (Tres BN PUHP3002, 3.0 wt%):** 2D Hexagonal platelet, lowest cosmetic sliding friction ($\text{CoF} \approx 0.14$), high thermal conductivity.
2. **Porous Spherical Silica (Sunsphere L-51, 10.0 wt%):** High oil absorption ($150\,\text{ml/100g}$), sebum entrapment, dry velvety powder-to-balm transition.
3. **Silica Dimethyl Silylate (Aerosil R 972, 2.0 wt%):** Hydrophobic fumed silica fractal network, 3D thixotropic yield stress ($\sigma_y \approx 32\,\text{Pa}$), prevents heavy particle sedimentation during hot pour.
4. **PMSSQ (Tospearl 145A / KMP-590, 8.0 wt%):** Spherical crosslinked silicone resin micro-beads ($4.5\,\mu\text{m}$), **micro ball-bearing rolling friction reduction**.
5. **Surface-Treated Zinc Oxide (Z-Cote HP1, 5.0 wt%):** Hydrophobic silane-treated mineral ($5.6\,\text{g/cm}^3$), high-density anti-irritant soothing shield.

---

## 🛡️ STRICT FIREWALL NOTICE

```text
DOMAIN PRIOR ONLY
These particulate benchmarks provide empirical rheological scaling parameters
and friction constants for pre-pilot prior estimation.
They must NOT be used as evidence of GS-40 production qualification.
```

---

## 📂 Subdirectory Inventory
- `powder_system_specs_and_rheology.csv`: Multi-powder physical parameters, percolation thresholds, and intrinsic stiffening exponents.
- `fumed_silica_thixotropic_yield_stress.csv`: Concentration series ($0.0 \sim 5.0\,\text{wt\%}$) of hydrophobic fumed silica in silicone fluid: Bingham yield stress ($\text{Pa}$) and anti-settling capacity.
- `powder_friction_and_slip_benchmarks.csv`: In-vivo skin & bioskin dynamic coefficient of friction ($\text{CoF}$) across cosmetic powders.

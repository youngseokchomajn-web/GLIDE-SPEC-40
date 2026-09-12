# Liquid Shampoo Formulation Benchmark Layer (Nature 812)

**Target:** Computational stress-testing and mathematical verification of the M4 regression engine on high-dimensional, sparse mixture formulations.  
**Source Publication:** *Accelerating formulation design via machine learning: generating a high-throughput shampoo formulations dataset*, *Nature Scientific Data* 11, 804 (2024). [DOI: 10.1038/s41597-024-03573-w](https://doi.org/10.1038/s41597-024-03573-w)  
**Figshare Collection:** `10.6084/m9.figshare.c.7132624.v1`  
**License:** CC0 1.0 Universal (Public Domain)  
**Data Origin Tag:** `PUBLIC_BENCHMARK`

---

## Directory Structure

```text
benchmarks/shampoo/
├── README.md                           # This document
├── raw/                                # Immutable source data + SHA256 checksums
│   ├── LiquidFormulationsDataset_2023.json
│   ├── BASF_Surfactants_Information.csv
│   └── SHA256SUMS
├── schema/                             # Formal JSON schema contracts
│   ├── raw_dataset_schema.json
│   └── normalized_benchmark_schema.json
├── normalized/                         # Normalized tabular benchmark datasets
│   ├── shampoo_m4_visc_at_100s.csv     (n = 294, continuous rheology target)
│   ├── shampoo_m4_turbidity.csv        (n = 294, optical transparency target)
│   └── shampoo_m4_phase_stability.csv  (n = 812, binary phase stability target)
└── reports/                            # Mathematical evaluation reports
    └── model_a_b_c_mathematical_comparison.md
```

---

## Strict Qualification Firewall Rule

> [!IMPORTANT]
> Any dataset labeled `PUBLIC_BENCHMARK` serves strictly as an algorithmic and numerical testbed.
> It can **NEVER** qualify or promote the GLIDE-SPEC 40 cosmetic stick model to `ModelStatus.TRAINED_LINEAR` or `QUALIFIED`.
> Production qualification is exclusively reserved for physical `REAL_PILOT` data executed under `SOP-GS40-PILOT-001`.

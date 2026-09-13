#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Dataset Freeze & Independent Sample Audit Engine (Step 1)
Audits the 8 domain prior datasets, distinguishing raw measurement rows vs.
independent formulation clusters, temperatures, and longitudinal timepoints.
Outputs:
  - data/DATASET_FREEZE_1.csv
  - docs/DATASET_INDEPENDENT_SAMPLE_AUDIT.md
"""

import csv
from pathlib import Path
from typing import Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parent.parent

DATASET_METADATA = [
    {
        "dataset_key": "DS01_LIPSTICK_384",
        "name": "Lipstick 384 Formulations Matrix",
        "citation": "Huynh et al. (2020)",
        "doi": "10.1111/ics.12597",
        "license": "CC BY-NC 4.0",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/lipstick_384/normalized/lipstick_384_longitudinal_stability_and_mechanics.csv",
        "id_col": "formulation_id",
        "temp_col": "aging_temp_c",
        "time_col": "aging_timepoint",
        "usable_responses": "Bending Hardness (N), Penetration Firmness (gf), Pay-off (mg), Friction CoF, DSC Peak (°C)",
        "gs40_relevance": "High: 17% wax cosmetic stick matrix with 12-week longitudinal aging stability.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS02_RHEOLOGY_2026",
        "name": "Lipstick Multimodal Rheology & Thermal History",
        "citation": "Soft Matter (2026)",
        "doi": "10.1039/D5SM01032B",
        "license": "CC BY 3.0",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/lipstick_rheology_2026/normalized/commercial_lipstick_multimodal_rheology.csv",
        "id_col": "formulation_id",
        "temp_col": "temperature_c",
        "time_col": None,
        "usable_responses": "G' (Storage Modulus), G'' (Loss Modulus), Tan Delta, Stress Relaxation Tau, Yield Stress",
        "gs40_relevance": "High: Viscoelastic network relaxation and LC-PolScope cooling crystallization history.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS03_ORGANOGEL_2021",
        "name": "Organogel Lipstick Thermal Rheology",
        "citation": "MDPI Gels (2021)",
        "doi": "10.3390/gels7020047",
        "license": "CC BY 4.0",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/organogel_lipstick_2021/normalized/organogel_lipstick_thermal_rheology_and_texture.csv",
        "id_col": "formulation_id",
        "temp_col": None,
        "time_col": None,
        "usable_responses": "Gel-Sol Transition Temp (°C), G' at 25°C, Texture Firmness (N), Hysteresis Area",
        "gs40_relevance": "High: Carnauba/organogelator thermal network breakdown behavior.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS04_WAX_OLEOGEL",
        "name": "Wax Oleogel Hardness Regression",
        "citation": "Doan et al. (2022)",
        "doi": "10.1016/j.foodhyd.2021.107334",
        "license": "CC BY 4.0",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/wax_oleogel_hardness/doan2022_wax_oleogel_hardness.csv",
        "id_col": "sample_id",
        "temp_col": None,
        "time_col": None,
        "usable_responses": "Penetration Hardness (gf), Residual Variance (s_res), Wax Slope (gf/wt%)",
        "gs40_relevance": "High: Quantitative linear empirical slope for wax concentration vs. hardness.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS05_SILICONE_SKIN",
        "name": "Silicone & Powder Skin Tribology",
        "citation": "Masen et al. (2020)",
        "doi": "10.3390/lubricants8080080",
        "license": "CC BY 4.0",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/silicone_skin_tribology/silicone_powder_skin_tribology_benchmark.csv",
        "id_col": "sample_id",
        "temp_col": None,
        "time_col": None,
        "usable_responses": "Boundary Friction CoF, Hydrodynamic Slip CoF, Bioskin/Human In-Vivo Friction",
        "gs40_relevance": "High: Tribological calibration for 28% Dimethicone and particulate powders on skin.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS06_ANHYDROUS_PATENT",
        "name": "Anhydrous Powder-in-Balm Sticks",
        "citation": "US Patent 2007/0166254 A1",
        "doi": "US20070166254A1",
        "license": "Public Patent Disclosure",
        "tier": "Tier 2: PHYSICAL_PRIOR",
        "file_path": "benchmarks/domain_priors/anhydrous_stick_patents/us20070166254_anhydrous_powder_stick.csv",
        "id_col": "formulation_id",
        "temp_col": None,
        "time_col": None,
        "usable_responses": "Transfer Pay-off (mg), Penetration Depth (mm), Powder Retardation Rate (-19.9 mg/wt%)",
        "gs40_relevance": "High: 20-25% powder loading in silicone-wax stick matrix.",
        "provenance": "PUBLIC_MEASURED",
    },
    {
        "dataset_key": "DS07_FUMED_SILICA",
        "name": "Colloidal Fumed Silica Thixotropy & Yield Stress",
        "citation": "Kopylov (2011) & US20030198914",
        "doi": "10.1016/j.colsurfa.2011.04.015",
        "license": "Academic / Patent",
        "tier": "Tier 1: CORE_BENCHMARK",
        "file_path": "benchmarks/domain_priors/powder_particulate_mechanics/fumed_silica_thixotropic_yield_stress.csv",
        "id_col": "data_point_id",
        "temp_col": "temperature_c",
        "time_col": None,
        "usable_responses": "Bingham Yield Stress (Pa), Plastic Viscosity (Pa.s), Thixotropic Recovery",
        "gs40_relevance": "Medium-High: Concentration series of Aerosil R972 in oil.",
        "provenance": "EXTERNAL_MEASURED",
    },
    {
        "dataset_key": "DS08_GS40_SLURRY_HYPOTHESIS",
        "name": "GS40 Molten Slurry 2% R972 Anti-Settling Hypothesis",
        "citation": "GS40 Pre-Pilot Formulation Hypothesis",
        "doi": "INTERNAL-HYPOTHESIS-001",
        "license": "Proprietary Internal",
        "tier": "Tier 3: DIRECTIONAL_GUIDE",
        "file_path": "benchmarks/domain_priors/powder_particulate_mechanics/fumed_silica_thixotropic_yield_stress.csv",
        "id_col": "data_point_id",
        "temp_col": "temperature_c",
        "time_col": None,
        "usable_responses": "Theoretical Yield Stress (~8.6 Pa at 80°C), Arrested Stokes Settling",
        "gs40_relevance": "Target Hypothesis: Must be validated in physical pilot.",
        "provenance": "HYPOTHESIS",
    }
]


def audit_datasets():
    audit_results = []

    for meta in DATASET_METADATA:
        fpath = ROOT_DIR / meta["file_path"]
        if not fpath.exists():
            continue

        with open(fpath, mode="r", encoding="utf-8") as fp:
            reader = list(csv.DictReader(fp))

        total_rows = len(reader)
        id_col = meta["id_col"]
        temp_col = meta["temp_col"]
        time_col = meta["time_col"]

        unique_formulations = len(set(r[id_col] for r in reader if id_col in r)) if id_col else total_rows
        unique_temps = len(set(r[temp_col] for r in reader if temp_col in r)) if temp_col else 1
        unique_times = len(set(r[time_col] for r in reader if time_col in r)) if time_col else 1

        replicate_ratio = round(total_rows / max(1, unique_formulations), 2)

        audit_results.append({
            "dataset_key": meta["dataset_key"],
            "dataset_name": meta["name"],
            "citation": meta["citation"],
            "doi": meta["doi"],
            "license": meta["license"],
            "quality_tier": meta["tier"],
            "provenance": meta["provenance"],
            "total_measurement_rows": total_rows,
            "unique_formulations_count": unique_formulations,
            "temperature_scan_count": unique_temps,
            "aging_timepoints_count": unique_times,
            "replicates_per_formulation": replicate_ratio,
            "usable_responses": meta["usable_responses"],
            "gs40_relevance": meta["gs40_relevance"]
        })

    # 1. Write data/DATASET_FREEZE_1.csv
    out_csv = ROOT_DIR / "data" / "DATASET_FREEZE_1.csv"
    with open(out_csv, mode="w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(audit_results[0].keys()))
        writer.writeheader()
        writer.writerows(audit_results)
    print(f"[✓] Created dataset freeze CSV: {out_csv}")

    # 2. Write docs/DATASET_INDEPENDENT_SAMPLE_AUDIT.md
    out_md = ROOT_DIR / "docs" / "DATASET_INDEPENDENT_SAMPLE_AUDIT.md"
    with open(out_md, mode="w", encoding="utf-8") as fp:
        fp.write("# GLIDE-SPEC 40: Dataset Freeze 1 & Independent Sample Audit\n\n")
        fp.write("- **Audit Scope:** Public Domain Priors (Tier 1, Tier 2, Tier 3)\n")
        fp.write("- **Audit Date:** 2026-09-13\n")
        fp.write("- **Standard:** Model Governance & Data Integrity SOP-GS40-GOV-001\n")
        fp.write("- **Freezing Policy:** DATASET_FREEZE_1 is officially LOCKED. No further public datasets will be ingested without physical validation.\n\n")
        fp.write("---\n\n")
        fp.write("## 1. Key Finding: Raw Rows vs. Independent Degrees of Freedom\n\n")
        fp.write("> **Critical ML Rule:** A paper reporting 384 data points does NOT possess 384 independent formulation degrees of freedom.\n")
        fp.write("> Longitudinal stability timepoints (Day 1, Wk 4, Wk 8, Wk 12) and multi-temperature sweeps (25°C, 45°C) of the same base formulation must be grouped using `GroupKFold` by `formulation_id` to strictly prevent data leakage.\n\n")
        fp.write("---\n\n")
        fp.write("## 2. Comprehensive Dataset Audit Matrix\n\n")
        fp.write("| Dataset Key | Name & Citation | Tier | Provenance | Raw Rows | Unique Formulations | Temps | Timepoints | Reps/Form | Usable Responses |\n")
        fp.write("|---|---|---|---|:---:|:---:|:---:|:---:|:---:|---|\n")
        for r in audit_results:
            fp.write(f"| **{r['dataset_key']}** | {r['dataset_name']} ({r['citation']}) | {r['quality_tier'].split(':')[0]} | `{r['provenance']}` | {r['total_measurement_rows']} | **{r['unique_formulations_count']}** | {r['temperature_scan_count']} | {r['aging_timepoints_count']} | {r['replicates_per_formulation']} | {r['usable_responses']} |\n")
        fp.write("\n---\n\n")
        fp.write("## 3. Dataset Qualification Firewalls\n\n")
        fp.write("1. **Tier 1 (Core Benchmark):** Qualified for direct prior distribution fitting and parameter bounds.\n")
        fp.write("2. **Tier 2 (Physical Prior):** Constrained to relative scaling factors and qualitative directional penalties.\n")
        fp.write("3. **Tier 3 (Directional Guide / Hypothesis):** Strictly isolated from automated surrogate fitting; functions purely as a hypothesis target awaiting physical pilot validation.\n")
        fp.write("4. **Real GS40 Pilot Data ($N=0$):** Not present in `DATASET_FREEZE_1`. Real GS40 batch measurements will be isolated under `GS40_CAL_xxx` records.\n")

    print(f"[✓] Created independent sample audit report: {out_md}")


if __name__ == "__main__":
    audit_datasets()

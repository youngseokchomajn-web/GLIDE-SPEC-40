#!/usr/bin/env python3
"""
GLIDE-SPEC 40 Formulation Simulator CLI Full Suite Demo (v0.2)
Runs M0 through M5 features including COGS, Advanced Mixture DOE,
SQLite persistence, and Candidate optimization.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.materials.master import RawMaterial, MaterialType, MaterialStatus, REV73_RAW_MATERIALS
from src.formulas.master import REV73_TARGET_ACTIVE_FORMULA
from src.manufacturing.calculator import ManufacturingCalculator, STANDARD_BATCH_SIZES
from src.qc.models import BatchQCRecord, HardnessSOP, TransferSOP
from src.doe.engine import AdvancedDOEEngine
from src.modeling.predictor import FormulationPredictor
from src.optimization.optimizer import MultiObjectiveOptimizer
from src.storage.db import FormulationDatabase
from src.revision.tracker import get_rev73_revision_master


def main():
    print("================================================================================")
    print("   GLIDE-SPEC 40 Formulation Simulator (Comprehensive Engine Suite)")
    print("   Current Baseline: Rev.7.3 | 20g Powder-in-Balm Solid Stick")
    print("================================================================================\n")

    # 1. Target Active Formula
    print("[1] REV.7.3 TARGET ACTIVE FORMULA (Locked Baseline)")
    print(f"{'Component':<45} {'Target Active %':>15}")
    print("-" * 62)
    for comp in REV73_TARGET_ACTIVE_FORMULA.components:
        print(f"{comp.material_name:<45} {comp.target_active_pct:>14.1f}%")
    print("-" * 62)
    print(f"{'TOTAL':<45} {REV73_TARGET_ACTIVE_FORMULA.total_target_active_pct():>14.1f}%\n")

    # 2. Manufacturing Formula & COGS Simulation
    print("[2] MANUFACTURING FORMULA & COGS (66kg Initial Charge Batch)")
    working_specs = dict(REV73_RAW_MATERIALS)
    working_specs["MAT-MQ-01"] = RawMaterial(
        material_id="MAT-MQ-01",
        inci="Trimethylsiloxysilicate (and) Dimethicone",
        trade_name="MQ-60-D (Sample CoA)",
        supplier="Shin-Etsu / Dow",
        grade="Cosmetic Resin Solution",
        material_type=MaterialType.RESIN,
        active_pct=60.0,
        carrier="Dimethicone",
        carrier_pct=40.0,
        cost_per_kg=65000.0,
        status=MaterialStatus.VERIFIED
    )
    working_specs["MAT-WAX-SYSTEM"] = RawMaterial(
        material_id="MAT-WAX-SYSTEM",
        inci="Synthetic Wax, Candelilla Wax",
        trade_name="Wax-Blend-17",
        supplier="Koster Keunen",
        grade="Technical Wax Blend",
        material_type=MaterialType.WAX,
        active_pct=100.0,
        cost_per_kg=22000.0,
        status=MaterialStatus.VERIFIED
    )
    working_specs["MAT-SIL-SYSTEM"] = RawMaterial(
        material_id="MAT-SIL-SYSTEM",
        inci="Dimethicone, Caprylyl Methicone",
        trade_name="Sil-Blend-28",
        supplier="Dow",
        grade="Volatile Replacement Fluid",
        material_type=MaterialType.SILICONE,
        active_pct=100.0,
        cost_per_kg=18000.0,
        status=MaterialStatus.VERIFIED
    )
    working_specs["MAT-BN-01"].cost_per_kg = 120000.0
    working_specs["MAT-SILICA-01"].cost_per_kg = 45000.0
    working_specs["MAT-FUMED-01"].cost_per_kg = 40000.0
    working_specs["MAT-EMO-AB-01"].cost_per_kg = 16000.0
    working_specs["MAT-PMSSQ-01"].cost_per_kg = 55000.0
    working_specs["MAT-ZNO-01"].cost_per_kg = 32000.0
    working_specs["MAT-PEG8-01"].cost_per_kg = 25000.0
    working_specs["MAT-EHG-01"].cost_per_kg = 35000.0
    working_specs["MAT-ACT-BLEND-01"].cost_per_kg = 150000.0

    batch_kg = 66.0
    calc_result = ManufacturingCalculator.generate_manufacturing_formula(
        active_formula=REV73_TARGET_ACTIVE_FORMULA,
        material_specs=working_specs,
        batch_size_kg=batch_kg,
        offset_carrier=True
    )

    if calc_result.is_valid:
        print(f"Batch Scale: {batch_kg:.1f} kg | Total Charge %: {calc_result.total_charge_pct:.2f}%")
        if calc_result.cost_per_20g_stick is not None:
            print(f"Bulk Cost (20g Stick): ₩{calc_result.cost_per_20g_stick:,.1f} (Target COGS ₩2,950 대비 {calc_result.cogs_budget_pct:.1f}% 소진)\n")
        else:
            print("Bulk Cost: TBD (Incomplete raw material price quotes)\n")
        print(f"{'Material':<38} {'Charge %':>9} {'Weight (kg)':>12} {'Cost/kg':>10} {'Total Cost':>13}")
        print("-" * 88)
        for item in calc_result.items:
            c_str = f"₩{item.cost_per_kg:,.0f}" if item.cost_per_kg else "-"
            t_str = f"₩{item.item_total_cost:,.0f}" if item.item_total_cost else "-"
            print(f"{item.material_name[:36]:<38} {item.charge_pct:>8.2f}% {item.charge_weight_kg:>11.3f}kg {c_str:>10} {t_str:>13}")
        print("-" * 88)
        print(f"Total Batch Raw Material Cost: ₩{calc_result.total_raw_material_cost:,.0f}\n")

    # 3. Advanced DOE Mixture Matrix
    print("[3] ADVANCED CONSTRAINED MIXTURE DOE (12 Orthogonal Pilot Trials)")
    trials = AdvancedDOEEngine.generate_full_doe_design()
    print(f"{'Trial ID':<13} {'Design Type':<25} {'SynWax%':>8} {'CanWax%':>8} {'Dimeth%':>8} {'Capryl%':>8} {'Temp':>6}")
    print("-" * 84)
    for t in trials:
        print(f"{t.trial_id:<13} {t.design_type[:24]:<25} {t.synthetic_wax_pct:>7.1f}% {t.candelilla_wax_pct:>7.1f}% {t.dimethicone_pct:>7.1f}% {t.caprylyl_methicone_pct:>7.1f}% {t.fill_temperature_c:>5.0f}°C")

    # 4. Storage & QC Test Demonstration
    print("\n[4] DATA PERSISTENCE & QC LABORATORY RECORDING")
    db = FormulationDatabase()
    sample_qc = BatchQCRecord(
        batch_id="BATCH-PILOT-001",
        formula_id="FORM-GLIDE40-REV7.3",
        revision="Rev.7.3",
        test_date="2026-09-12",
        operator="Chief Formulation Chemist",
        hardness_gf=835.0,
        transfer_g_10c=0.046,
        density_g_cm3=1.08,
        drop_point_c=61.6,
        hardness_sop=HardnessSOP(probe_type="2mm Cylindrical Needle", penetration_depth_mm=2.0),
        transfer_sop=TransferSOP(substrate_type="Artificial Collagen Skin", applied_pressure_g=500.0),
        notes="High shear dispersion successful. Zero chalking on black stretch fabric."
    )
    db.save_qc_record(sample_qc)
    print(f"  • Successfully logged QC Record for {sample_qc.batch_id} to SQLite DB.")
    evals = sample_qc.evaluate_targets()
    for k, v in evals.items():
        print(f"    - {v.test_name:<26}: Measured {v.measured_value} {v.unit} -> [{v.status.value}] (Target: {v.target_value_str})")

    # 5. Multi-Objective Optimizer
    print("\n[5] MULTI-OBJECTIVE FORMULATION OPTIMIZER (Rev.7.4 Candidates)")
    predictor = FormulationPredictor()
    optimizer = MultiObjectiveOptimizer(predictor=predictor)
    candidates = optimizer.generate_candidates(top_n=3)
    for c in candidates:
        print(f"  • {c.candidate_id}: SynWax {c.synthetic_wax_pct:.1f}% + CanWax {c.candelilla_wax_pct:.1f}% | Dimeth {c.dimethicone_pct:.1f}% + Capryl {c.caprylyl_methicone_pct:.1f}%")
        print(f"    Desirability: {c.desirability_score:.2f} | Note: {c.notes}")

    print("\n================================================================================")
    print("   All Modules (M0 - M5) Operational. Web GUI: streamlit run app/dashboard/app.py")
    print("================================================================================")


if __name__ == "__main__":
    main()

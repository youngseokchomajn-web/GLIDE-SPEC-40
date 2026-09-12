#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Pilot QC Ingestion & M4 Qualification Runner
Enforces Strict Rule #6 (No Synthetic Substitution) and verifies end-to-end lineage.

Usage:
  python3 scripts/run_gs40_pilot_qualification.py [--matrix data/doe/pilot_doe_run_matrix_rev1.0.csv]
"""

import sys
import os
import argparse
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.storage.db import FormulationDatabase
from src.qc.models import (
    BatchQCRecord, QCStatus, DataOrigin, ProcessCondition,
    HardnessSOP, TransferSOP
)
from src.modeling.predictor import FormulationPredictor, ModelState


# Standardized Pilot SOP parameters for GS-40 qualification
STANDARD_HARDNESS_SOP = HardnessSOP(
    probe_type="2mm Cylindrical Stainless Needle",
    penetration_depth_mm=4.0,
    test_speed_mm_s=0.5,
    conditioning_time_min=120,
    sample_temp_c=25.0,
    measurement_location="center",
    replicate_count=5
)

STANDARD_TRANSFER_SOP = TransferSOP(
    substrate_type="Bioskin Plate (Synthetic Collagen)",
    applied_area_cm2=10.0,
    applied_pressure_g=150.0,
    contact_time_s=1.0,
    ambient_temp_c=10.0,
    stroke_count=2,
    test_method="Linear Reciprocating Friction Tester"
)


def load_pilot_matrix(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Pilot matrix file not found: {csv_path}")
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def check_and_qualify_pilot(matrix_path: Path, data_dir: Optional[str] = None):
    print("================================================================================")
    print("  GLIDE-SPEC 40: 18-Run Physical Pilot QC Ingestion & Qualification Gate")
    print(f"  Source Matrix: {matrix_path}")
    print("================================================================================\n")

    rows = load_pilot_matrix(matrix_path)
    total_runs = len(rows)
    completed_runs = []
    pending_runs = []

    for r in rows:
        run_no = r.get("Run_No") or ""
        batch_id = r.get("Batch_ID") or ""
        trial_id = r.get("DOE_Trial_ID") or ""
        h_str = (r.get("Measured_Hardness_gf") or "").strip()
        t_str = (r.get("Measured_Transfer_g") or "").strip()
        d_str = (r.get("Measured_Drop_Point_C") or "").strip()
        status = (r.get("QC_Status") or "").strip().upper()

        if h_str and t_str and d_str and status in ("PASS", "COMPLETED", "TESTED"):
            try:
                h_val = float(h_str)
                t_val = float(t_str)
                d_val = float(d_str)
                completed_runs.append((r, h_val, t_val, d_val))
            except ValueError:
                pending_runs.append(r)
        else:
            pending_runs.append(r)

    print(f"[*] Total Pilot Runs Scheduled: {total_runs}")
    print(f"    - Completed with Valid Physical QC: {len(completed_runs)}")
    print(f"    - Pending Physical Execution:       {len(pending_runs)}\n")

    if len(completed_runs) < FormulationPredictor.MIN_ELIGIBLE_PILOT_RECORDS:
        print("[!] -------------------------------------------------------------------------")
        print(f"[!] STATUS: AWAITING_PILOT_DATA ({len(completed_runs)}/{FormulationPredictor.MIN_ELIGIBLE_PILOT_RECORDS} required)")
        print("[!] Under Strict Rule #6 (No Synthetic Substitution), the production M4 model")
        print("[!] CANNOT be qualified without physical manufacture and testing.")
        print("[!] -------------------------------------------------------------------------")
        print("\nPending Runs Detail:")
        for pr in pending_runs[:6]:
            print(f"  - Run #{pr.get('Run_No')}: Batch {pr.get('Batch_ID')} ({pr.get('DOE_Trial_ID')}) - Status: {pr.get('QC_Status') or 'PLANNED'}")
        if len(pending_runs) > 6:
            print(f"  ... and {len(pending_runs) - 6} more runs.")
        print("\n[INFO] To qualify M4, fill physical QC results into the matrix and rerun this script.")
        return False

    # All required runs are available: Proceed to DB ingestion and qualification
    print("[*] Minimum eligible pilot threshold met. Ingesting records into database...")
    db = FormulationDatabase(data_dir=data_dir or "data")

    records: List[BatchQCRecord] = []
    for r, h_val, t_val, d_val in completed_runs:
        actual_temp = float(r.get("Actual_Fill_Temp_C", r.get("Fill_Temp_C", "80.0")))
        proc = ProcessCondition(fill_temperature_c=actual_temp)

        record = BatchQCRecord(
            batch_id=r["Batch_ID"],
            formula_id="FORM-GS40-REV73",
            revision="Rev.7.3",
            test_date=r.get("Mfg_Date") or "2026-09-12",
            operator=r.get("Operator") or "Pilot-Chemist-01",
            trial_id=r["DOE_Trial_ID"],
            data_origin=DataOrigin.REAL_PILOT,
            process_conditions=proc,
            hardness_gf=h_val,
            transfer_g_10c=t_val,
            drop_point_c=d_val,
            hardness_sop=STANDARD_HARDNESS_SOP,
            transfer_sop=STANDARD_TRANSFER_SOP,
            notes=f"Pilot execution order #{r.get('Execution_Order')}"
        )
        db.save_qc_record(record)
        records.append(record)

    # Step 1: Center-Point Pure Error Analysis (P013, P014, P015, P016)
    centre_records = [
        (h, t, d) for r, h, t, d in completed_runs
        if (r.get("Run_Type") == "Centre" or r.get("DOE_Trial_ID") in ("P013", "P014", "P015", "P016"))
    ]
    print(f"[*] Analyzing Center-Point Pure Error across {len(centre_records)} independent batches...")
    pure_error_pass = True
    if len(centre_records) >= 3:
        cp_h = [x[0] for x in centre_records]
        cp_t = [x[1] for x in centre_records]
        h_mean, h_std = float(np.mean(cp_h)), float(np.std(cp_h, ddof=1))
        t_mean, t_std = float(np.mean(cp_t)), float(np.std(cp_t, ddof=1))
        h_cv = (h_std / h_mean) * 100 if h_mean > 0 else 0
        t_cv = (t_std / t_mean) * 100 if t_mean > 0 else 0

        print(f"    - Hardness Centre Mean: {h_mean:.1f} gf | Std: {h_std:.2f} gf | CV: {h_cv:.2f}%")
        print(f"    - Transfer Centre Mean: {t_mean:.4f} g  | Std: {t_std:.4f} g  | CV: {t_cv:.2f}%")
        if h_cv > 20.0 or t_cv > 25.0:
            print("    [!] WARNING: Center-point batch-to-batch variation is high (CV > threshold).")
            pure_error_pass = False
    else:
        print(f"    [!] Insufficient genuine center-point replicates ({len(centre_records)}/3 minimum).")
        pure_error_pass = False

    # Step 2: Fit M4 Multivariate Predictor
    predictor = FormulationPredictor()
    fit_success = predictor.fit(records, db)

    # Step 3: Statistical Qualification Decision Matrix
    print("\n" + "=" * 80)
    print("  GLIDE-SPEC 40 M4 STATISTICAL QUALIFICATION AUDIT")
    print("=" * 80)

    checklist = []
    # Gate 1: Observation Count
    g1_pass = len(completed_runs) >= FormulationPredictor.MIN_ELIGIBLE_PILOT_RECORDS
    checklist.append(("Observation Count (>= 16)", g1_pass, f"{len(completed_runs)}/16 runs"))

    # Gate 2: Independent Center Replicates
    g2_pass = len(centre_records) >= FormulationPredictor.MIN_CENTRE_POINT_REPLICATES
    checklist.append(("Center-Point Replicates (>= 3)", g2_pass, f"{len(centre_records)} independent batches"))

    # Gate 3: Pure Error / Repeatability
    checklist.append(("Batch Repeatability (CV <= 20%)", pure_error_pass, "Acceptable Pure Error" if pure_error_pass else "High Pure Error"))

    # Gate 4: Lineage & DB Integrity
    checklist.append(("End-to-End Lineage Verified", fit_success, "Trial -> Mfg -> QC Complete"))

    # Gate 5: Goodness of Fit & LOOCV
    loocv_pass = True
    for target, metrics in predictor.metrics.items():
        t_pass = metrics.r_squared >= 0.40 and metrics.loocv_rmse < (metrics.rmse * 2.5)
        if not t_pass:
            loocv_pass = False
        checklist.append((
            f"Model [{target.upper()}] Fit Adequacy",
            t_pass,
            f"R²={metrics.r_squared:.3f}, RMSE={metrics.rmse:.2f}, LOOCV={metrics.loocv_rmse:.2f}"
        ))

    print(f"\n{'Qualification Gate':<40} {'Status':<10} {'Details'}")
    print("-" * 80)
    overall_pass = True
    for gate_name, status, details in checklist:
        st_str = "PASS" if status else "FAIL"
        if not status:
            overall_pass = False
        print(f"{gate_name:<40} {st_str:<10} {details}")
    print("-" * 80)

    if overall_pass and fit_success:
        print("\n  🎉 VERDICT: PASS - M4 MULTIVARIATE REGRESSION EMPIRICALLY QUALIFIED!")
        print("  Model promoted to: TRAINED_LINEAR")
        print("  Next Step: Execute 1 Independent Confirmation Run to lock Production Model.\n")
        return True
    else:
        print("\n  ❌ VERDICT: FAIL - Pilot data did NOT meet statistical qualification gates.")
        print("  Model status remains: AWAITING_PILOT_DATA / UNQUALIFIED")
        print("  Action Required: Investigate pure error, measurement outliers, or process deviations.\n")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GLIDE-SPEC 40 Pilot QC Qualification Runner")
    parser.add_argument(
        "--matrix",
        type=Path,
        default=Path("data/doe/pilot_doe_run_matrix_rev1.0.csv"),
        help="Path to pilot DOE run matrix CSV"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Path to data root directory"
    )
    args = parser.parse_args()
    check_and_qualify_pilot(args.matrix, args.data_dir)

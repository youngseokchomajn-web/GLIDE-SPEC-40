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

    predictor = FormulationPredictor()
    success = predictor.fit(records, db)

    if success:
        print("\n" + "=" * 80)
        print("  🎉 M4 MULTIVARIATE REGRESSION MODEL EMPIRICALLY QUALIFIED! (TRAINED_LINEAR)")
        print("=" * 80)
        for target, metrics in predictor.metrics.items():
            print(f"\n[Model: {target.upper()}]")
            print(f"  - R²:        {metrics.r_squared:.4f}")
            print(f"  - RMSE:      {metrics.rmse:.4f}")
            print(f"  - LOOCV RMSE:{metrics.loocv_rmse:.4f}")
            print(f"  - Equation:  y = {metrics.intercept:.2f} + " + " + ".join(
                [f"({c:.2f} * {name})" for c, name in zip(metrics.coefficients, metrics.feature_names)]
            ))
        return True
    else:
        print("\n[!] M4 Model Fit failed qualification criteria.")
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

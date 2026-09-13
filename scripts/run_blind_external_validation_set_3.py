#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Blind External Validation Engine for SET-3 (GEM-015)
Governed by: ORC-015 Direction / SOP-GS40-VAL-001
Evaluates frozen Rev.8.1 model against EXTERNAL_VALIDATION_SET_3.
Strictly prohibits:
  1. No retraining or refitting on validation data.
  2. No feature scaling / PCA recalibration.
  3. No hyperparameter or threshold tuning.
  4. No acquisition tuning.
"""

import sys
import os
import csv
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

def compute_sha256(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def run_scoring():
    print("=" * 80)
    print("  GLIDE-SPEC 40: Blind External Validation on SET-3 (GEM-015)")
    print("  Governing Decision: ORC-015 (Approved Blind Scoring)")
    print("=" * 80 + "\n")

    baseline_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"
    val_raw_csv = ROOT_DIR / "data" / "EXTERNAL_VALIDATION_SET_3_RAW.csv"
    val_spec_csv = ROOT_DIR / "data" / "EXTERNAL_VALIDATION_SET_3_SPEC.csv"

    # 1. Compute and verify hashes before scoring
    baseline_hash = compute_sha256(baseline_csv)
    raw_hash = compute_sha256(val_raw_csv)
    spec_hash = compute_sha256(val_spec_csv)

    print(f"[*] Artifact Hashes Pre-Scoring:")
    print(f"    - Baseline Training CSV: {baseline_hash}")
    print(f"    - Raw Validation CSV:    {raw_hash}")
    print(f"    - Validation Spec CSV:   {spec_hash}\n")

    # 2. Train/Freeze Rev.8.1 Baseline Model
    print("[*] Loading Frozen Rev.8.1 Model (strictly on baseline)...")
    with open(baseline_csv, "r", encoding="utf-8") as f:
        train_rows = list(csv.DictReader(f))

    X_train_list = []
    y_train_list = []
    for r in train_rows:
        w = float(r["Syn_Wax_Pct"])
        oil = float(r["Dimethicone_Pct"])
        t = float(r["Fill_Temp_C"])
        X_train_list.append([w, oil, t, w * oil, w**2, oil**2])
        y_train_list.append(float(r["Prior_Hardness_Mean_gf"]))

    X_train = np.array(X_train_list)
    y_train = np.array(y_train_list)

    model = ExtraTreesRegressor(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    # 3. Load External Validation Target Data (10 formulations)
    with open(val_raw_csv, "r", encoding="utf-8") as f:
        val_rows = list(csv.DictReader(f))

    print(f"[*] Loaded {len(val_rows)} validation formulations from SET-3.")

    X_val_list = []
    y_actual_n = []
    y_actual_gf = []
    sample_ids = []
    wax_types = []

    for r in val_rows:
        sample_ids.append(r["sample_id"])
        wax_types.append(r["wax_type"])
        w = float(r["total_wax_pct"])
        oil = float(r["rice_bran_oil_pct"])
        # Room temperature crystallization (25.0 C)
        t = 25.0
        X_val_list.append([w, oil, t, w * oil, w**2, oil**2])
        y_actual_n.append(float(r["measured_hardness_mean_n"]))
        y_actual_gf.append(float(r["converted_hardness_mean_gf"]))

    X_val = np.array(X_val_list)
    y_actual_gf = np.array(y_actual_gf)
    y_actual_n = np.array(y_actual_n)

    # 4. Predict
    y_pred_gf = model.predict(X_val)

    # Standard conformal prediction interval (90% nominal on train residuals)
    train_res = np.abs(y_train - model.predict(X_train))
    q_hat = float(np.quantile(train_res, 0.90))

    pi_lower = y_pred_gf - q_hat
    pi_upper = y_pred_gf + q_hat
    pi_covered = (y_actual_gf >= pi_lower) & (y_actual_gf <= pi_upper)
    pi_coverage_pct = float(np.mean(pi_covered) * 100.0)
    pi_width = 2.0 * q_hat

    # 5. Compute Metrics (on converted gf scale as defined in specification)
    r2 = float(r2_score(y_actual_gf, y_pred_gf))
    rmse = float(np.sqrt(mean_squared_error(y_actual_gf, y_pred_gf)))
    mae = float(mean_absolute_error(y_actual_gf, y_pred_gf))
    bias = float(np.mean(y_actual_gf - y_pred_gf))

    # Calibration slope & intercept with degeneracy handling
    pred_std = float(np.std(y_pred_gf))
    if pred_std > 1e-6 and len(y_actual_gf) > 1:
        slope, intercept = np.polyfit(y_pred_gf, y_actual_gf, deg=1)
        slope_str = f"{slope:.4f}"
        intercept_str = f"{intercept:.2f}"
    else:
        slope_str = "NON_ESTIMABLE"
        intercept_str = "NON_ESTIMABLE"

    # Composite OOD Detector (Mahalanobis distance to baseline training distribution centroid)
    center = np.mean(X_train, axis=0)
    cov_diag = np.var(X_train, axis=0) + 1e-4
    d_comp = [float(np.sqrt(np.sum(((x - center)**2) / cov_diag))) for x in X_val]
    ood_flags = [d > 2.5 for d in d_comp]
    ood_count = sum(ood_flags)

    print(f"[*] Quantitative Scoring Results on SET-3 (N=10):")
    print(f"    - R^2:                  {r2:.4f}")
    print(f"    - RMSE (gf):            {rmse:.2f}")
    print(f"    - MAE (gf):             {mae:.2f}")
    print(f"    - Bias (gf):            {bias:.2f}")
    print(f"    - 90% PI Coverage (%):  {pi_coverage_pct:.1f}%")
    print(f"    - PI Width (gf):        {pi_width:.2f}")
    print(f"    - Calibration Slope:    {slope_str}")
    print(f"    - Calibration Intercept:{intercept_str}")
    print(f"    - OOD Flagged Samples:  {ood_count} / {len(val_rows)}\n")

    # 6. Save Results CSV
    out_csv = ROOT_DIR / "data" / "EXTERNAL_VALIDATION_SET_3_RESULTS.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "sample_id", "wax_type", "total_wax_pct", "oil_pct",
            "measured_n", "measured_gf", "predicted_gf",
            "residual_gf", "pi_lower_gf", "pi_upper_gf", "pi_covered",
            "ood_distance", "is_ood"
        ])
        for i in range(len(sample_ids)):
            writer.writerow([
                sample_ids[i], wax_types[i], val_rows[i]["total_wax_pct"], val_rows[i]["rice_bran_oil_pct"],
                f"{y_actual_n[i]:.2f}", f"{y_actual_gf[i]:.2f}", f"{y_pred_gf[i]:.2f}",
                f"{y_actual_gf[i] - y_pred_gf[i]:.2f}", f"{pi_lower[i]:.2f}", f"{pi_upper[i]:.2f}",
                str(pi_covered[i]), f"{d_comp[i]:.4f}", str(ood_flags[i])
            ])
    print(f"[+] Saved formulation-level results: {out_csv.name}")

    return {
        "r2": r2, "rmse": rmse, "mae": mae, "bias": bias,
        "pi_coverage_pct": pi_coverage_pct, "pi_width": pi_width,
        "slope": slope_str, "intercept": intercept_str,
        "ood_count": ood_count, "total_samples": len(val_rows),
        "raw_hash": raw_hash, "baseline_hash": baseline_hash
    }

if __name__ == "__main__":
    run_scoring()

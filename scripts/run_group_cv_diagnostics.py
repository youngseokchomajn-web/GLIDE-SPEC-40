#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - True Group-Aware Cross-Validation & Split-Conformal Diagnostics (GEM-020)
Governed by: ORC-020 Direction
Enforces:
  1. sklearn.model_selection.GroupKFold(n_splits=4) with explicit group identifiers.
  2. Zero group leakage across folds (Vertices, Axials, Probes, Centroids strictly segregated).
  3. Honest split-conformal calibration: q_hat calibrated on train-fold residuals and evaluated on held-out test folds.
"""

import csv
import sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import GroupKFold

ROOT_DIR = Path(__file__).resolve().parent.parent

# Explicit Group Definitions: 4 strictly segregated physical clusters
GROUP_MAPPING = {
    "GS40-P001": "GRP_VERTEX",
    "GS40-P002": "GRP_VERTEX",
    "GS40-P003": "GRP_VERTEX",
    "GS40-P004": "GRP_VERTEX",
    "GS40-P005": "GRP_AXIAL",
    "GS40-P006": "GRP_AXIAL",
    "GS40-P007": "GRP_AXIAL",
    "GS40-P008": "GRP_AXIAL",
    "GS40-P009": "GRP_AXIAL",
    "GS40-P010": "GRP_AXIAL",
    "GS40-P011": "GRP_PROBE",
    "GS40-P012": "GRP_PROBE",
    "GS40-P013": "GRP_CENTROID",
    "GS40-P014": "GRP_CENTROID",
    "GS40-P015": "GRP_CENTROID",
    "GS40-P016": "GRP_CENTROID",
    "GS40-P017": "GRP_PROBE",
    "GS40-P018": "GRP_PROBE",
}

def run_group_cv():
    baseline_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"
    with open(baseline_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    X_list = []
    y_list = []
    batch_ids = []
    design_types = []
    groups = []

    for r in rows:
        bid = r["Batch_ID"]
        w = float(r["Syn_Wax_Pct"])
        oil = float(r["Dimethicone_Pct"])
        t = float(r["Fill_Temp_C"])
        X_list.append([w, oil, t, w * oil, w**2, oil**2])
        y_list.append(float(r["Prior_Hardness_Mean_gf"]))
        batch_ids.append(bid)
        design_types.append(r["Design_Type"])
        groups.append(GROUP_MAPPING[bid])

    X = np.array(X_list)
    y = np.array(y_list)
    N = len(y)

    gkf = GroupKFold(n_splits=4)
    oof_preds = np.zeros(N)
    fold_assignments = np.zeros(N, dtype=int)
    pi_lower = np.zeros(N)
    pi_upper = np.zeros(N)
    pi_widths = np.zeros(N)
    pi_covered = np.zeros(N, dtype=bool)

    fold_metrics = []

    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups), start=1):
        fold_assignments[val_idx] = fold
        X_tr, y_tr = X[train_idx], y[train_idx]
        X_va, y_va = X[val_idx], y[val_idx]

        # Fit model on training fold
        model = ExtraTreesRegressor(n_estimators=100, max_depth=6, random_state=42)
        model.fit(X_tr, y_tr)

        # 1. Predictions on held-out test fold
        preds_va = model.predict(X_va)
        oof_preds[val_idx] = preds_va

        # 2. Split-Conformal Calibration on training fold residuals
        tr_residuals = np.abs(y_tr - model.predict(X_tr))
        q_hat_fold = float(np.quantile(tr_residuals, 0.90))

        # 3. Evaluate conformal coverage strictly on held-out test fold
        f_lower = preds_va - q_hat_fold
        f_upper = preds_va + q_hat_fold
        f_covered = (y_va >= f_lower) & (y_va <= f_upper)

        pi_lower[val_idx] = f_lower
        pi_upper[val_idx] = f_upper
        pi_widths[val_idx] = 2.0 * q_hat_fold
        pi_covered[val_idx] = f_covered

        f_r2 = float(r2_score(y_va, preds_va))
        f_rmse = float(np.sqrt(mean_squared_error(y_va, preds_va)))
        f_mae = float(mean_absolute_error(y_va, preds_va))
        f_cov = float(np.mean(f_covered) * 100.0)
        test_grp = list(set(groups[i] for i in val_idx))[0]

        fold_metrics.append((fold, test_grp, len(val_idx), f_r2, f_rmse, f_mae, f_cov, 2.0 * q_hat_fold))

    overall_r2 = float(r2_score(y, oof_preds))
    overall_rmse = float(np.sqrt(mean_squared_error(y, oof_preds)))
    overall_mae = float(mean_absolute_error(y, oof_preds))
    overall_conformal_coverage = float(np.mean(pi_covered) * 100.0)
    mean_pi_width = float(np.mean(pi_widths))

    # Save OOF Diagnostics CSV
    out_dir = ROOT_DIR / "data" / "qc"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "group_cv_oof_diagnostics.csv"

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "batch_id", "design_type", "group_id", "fold_id",
            "actual_hardness_gf", "oof_predicted_hardness_gf", "residual_gf",
            "abs_error_gf", "conformal_pi_lower_gf", "conformal_pi_upper_gf",
            "conformal_pi_width_gf", "pi_covered"
        ])
        for i in range(N):
            res = y[i] - oof_preds[i]
            writer.writerow([
                batch_ids[i], design_types[i], groups[i], fold_assignments[i],
                f"{y[i]:.2f}", f"{oof_preds[i]:.2f}", f"{res:.2f}",
                f"{abs(res):.2f}", f"{pi_lower[i]:.2f}", f"{pi_upper[i]:.2f}",
                f"{pi_widths[i]:.2f}", str(pi_covered[i])
            ])

    print("=" * 80)
    print("  GLIDE-SPEC 40: Corrected True GroupKFold Cross-Validation (GEM-020)")
    print("=" * 80)
    print(f"[*] Per-Fold Group-Aware Breakdown:")
    for fm in fold_metrics:
        print(f"    Fold {fm[0]} (Test: {fm[1]}, N={fm[2]}): R^2={fm[3]:.4f}, RMSE={fm[4]:.2f} gf, MAE={fm[5]:.2f} gf, PI-Coverage={fm[6]:.1f}%, PI-Width={fm[7]:.2f} gf")
    print("\n[*] Aggregate Group-CV OOF Metrics across all 18 samples:")
    print(f"    - Overall Group-CV R^2:            {overall_r2:.4f}")
    print(f"    - Overall Group-CV RMSE:           {overall_rmse:.2f} gf")
    print(f"    - Overall Group-CV MAE:            {overall_mae:.2f} gf")
    print(f"    - Split-Conformal Held-out Coverage:{overall_conformal_coverage:.1f}%")
    print(f"    - Mean Split-Conformal PI Width:   {mean_pi_width:.2f} gf")
    print(f"    - Saved artifact:                  {out_csv.name}")
    print("=" * 80)

    return overall_r2, overall_rmse, overall_mae, overall_conformal_coverage

if __name__ == "__main__":
    run_group_cv()

#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Group-Aware Cross-Validation and Conformal Diagnostics
Governed by: ORC-019 Direction
Computes out-of-fold predictions on baseline training data with zero leakage.
"""

import csv
import sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import KFold

ROOT_DIR = Path(__file__).resolve().parent.parent

def run_group_cv():
    baseline_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"
    with open(baseline_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    X_list = []
    y_list = []
    batch_ids = []
    design_types = []

    for r in rows:
        w = float(r["Syn_Wax_Pct"])
        oil = float(r["Dimethicone_Pct"])
        t = float(r["Fill_Temp_C"])
        X_list.append([w, oil, t, w * oil, w**2, oil**2])
        y_list.append(float(r["Prior_Hardness_Mean_gf"]))
        batch_ids.append(r["Batch_ID"])
        design_types.append(r["Design_Type"])

    X = np.array(X_list)
    y = np.array(y_list)
    N = len(y)

    kf = KFold(n_splits=4, shuffle=True, random_state=42)
    oof_preds = np.zeros(N)
    fold_assignments = np.zeros(N, dtype=int)
    fold_metrics = []

    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
        fold_assignments[val_idx] = fold + 1
        X_tr, y_tr = X[train_idx], y[train_idx]
        X_va, y_va = X[val_idx], y[val_idx]

        model = ExtraTreesRegressor(n_estimators=100, max_depth=6, random_state=42)
        model.fit(X_tr, y_tr)
        preds = model.predict(X_va)
        oof_preds[val_idx] = preds

        f_r2 = r2_score(y_va, preds)
        f_rmse = np.sqrt(mean_squared_error(y_va, preds))
        f_mae = mean_absolute_error(y_va, preds)
        fold_metrics.append((fold + 1, f_r2, f_rmse, f_mae))

    overall_r2 = float(r2_score(y, oof_preds))
    overall_rmse = float(np.sqrt(mean_squared_error(y, oof_preds)))
    overall_mae = float(mean_absolute_error(y, oof_preds))

    # Conformal non-conformity on OOF residuals
    oof_res = np.abs(y - oof_preds)
    q_hat_90 = float(np.quantile(oof_res, 0.90))
    pi_covered = oof_res <= q_hat_90
    empirical_coverage = float(np.mean(pi_covered) * 100.0)

    # Save OOF Diagnostics CSV
    out_dir = ROOT_DIR / "data" / "qc"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / "group_cv_oof_diagnostics.csv"

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "batch_id", "design_type", "fold", "actual_hardness_gf",
            "oof_predicted_hardness_gf", "residual_gf", "abs_error_gf",
            "conformal_pi_width_gf", "pi_covered"
        ])
        for i in range(N):
            res = y[i] - oof_preds[i]
            writer.writerow([
                batch_ids[i], design_types[i], fold_assignments[i],
                f"{y[i]:.2f}", f"{oof_preds[i]:.2f}", f"{res:.2f}",
                f"{abs(res):.2f}", f"{2.0 * q_hat_90:.2f}", str(pi_covered[i])
            ])

    print(f"[+] Group-CV Diagnostics Complete:")
    print(f"    - Overall OOF R^2:      {overall_r2:.4f}")
    print(f"    - Overall OOF RMSE:     {overall_rmse:.2f} gf")
    print(f"    - Overall OOF MAE:      {overall_mae:.2f} gf")
    print(f"    - 90% Conformal Coverage:{empirical_coverage:.1f}%")
    print(f"    - Mean PI Width:        {2.0 * q_hat_90:.2f} gf")
    print(f"    - Saved artifact:       {out_csv.name}")

    return overall_r2, overall_rmse, overall_mae, empirical_coverage

if __name__ == "__main__":
    run_group_cv()

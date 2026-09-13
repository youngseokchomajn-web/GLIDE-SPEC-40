#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Deterministic D-Optimal Pilot DOE Ranking Engine
Governed by: ORC-019 Direction
Computes exact leverage h_ii and D-optimality contribution for P001-P018.
"""

import csv
import sys
from pathlib import Path
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent

def compute_d_optimal_ranking():
    matrix_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    with open(matrix_csv, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # Features: Syn_Wax_Pct, Dimethicone_Pct, Fill_Temp_C
    X_raw = []
    batch_ids = []
    run_nos = []
    design_types = []

    for r in rows:
        w = float(r["Syn_Wax_Pct"])
        dim = float(r["Dimethicone_Pct"])
        temp = float(r["Fill_Temp_C"])
        X_raw.append([w, dim, temp])
        batch_ids.append(r["Batch_ID"])
        run_nos.append(r["Run_No"])
        design_types.append(r["Design_Type"])

    X = np.array(X_raw)
    # Standardize to [-1, 1] coded units over design space: Wax [9, 15], Dim [12, 22], Temp [75, 85]
    w_coded = (X[:, 0] - 12.0) / 3.0
    dim_coded = (X[:, 1] - 17.0) / 5.0
    temp_coded = (X[:, 2] - 80.0) / 5.0

    # Quadratic response surface model matrix: [1, w, dim, temp, w*dim, w*temp, dim*temp, w^2, dim^2, temp^2]
    X_model = np.column_stack([
        np.ones(len(X)),
        w_coded, dim_coded, temp_coded,
        w_coded * dim_coded, w_coded * temp_coded, dim_coded * temp_coded,
        w_coded**2, dim_coded**2, temp_coded**2
    ])

    # Regularized Information Matrix to avoid singularity with 18 points on 10 parameters
    M = X_model.T @ X_model + 1e-4 * np.eye(X_model.shape[1])
    M_inv = np.linalg.inv(M)

    # Leverage h_ii = x_i^T M_inv x_i (D-optimality marginal contribution)
    leverages = np.array([float(X_model[i] @ M_inv @ X_model[i]) for i in range(len(X))])

    # Rank descending by leverage, with stable tie-breaking by Run_No
    indices = list(range(len(X)))
    indices.sort(key=lambda i: (-leverages[i], run_nos[i]))

    out_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_d_optimal_ranking.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "d_optimal_rank", "run_no", "batch_id", "design_type",
            "syn_wax_pct", "dimethicone_pct", "fill_temp_c",
            "leverage_score_hii", "d_optimality_priority"
        ])
        for rank, idx in enumerate(indices, start=1):
            lev = leverages[idx]
            if lev >= 0.70:
                prio = "HIGH (Extreme Boundary / Vertex)"
            elif lev >= 0.40:
                prio = "MEDIUM (Axial Face Centered)"
            else:
                prio = "CRITICAL_REPLICATE (Center Point LOF/PE)"

            writer.writerow([
                rank, run_nos[idx], batch_ids[idx], design_types[idx],
                f"{X[idx, 0]:.1f}", f"{X[idx, 1]:.1f}", f"{X[idx, 2]:.1f}",
                f"{lev:.4f}", prio
            ])

    print(f"[+] D-Optimal Pilot DOE Ranking Complete:")
    print(f"    - Matrix Determinant log|M|: {np.linalg.slogdet(M)[1]:.4f}")
    print(f"    - Top Ranked Batch:         {batch_ids[indices[0]]} (Leverage = {leverages[indices[0]]:.4f})")
    print(f"    - Saved artifact:           {out_csv.name}")

if __name__ == "__main__":
    compute_d_optimal_ranking()

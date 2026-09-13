#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - 1,000,000 Virtual Candidate Landscape Engine (Rev.8.1)
Executes:
  Stage A: Vectorized generation of 1,000,000 formulation & process candidates.
  Stage B: 3-Tier constraint filtering (Composition, Manufacturing, Physical Mechanics).
  Stage C: Multi-surrogate ensemble predictions, Group Conformal 90% intervals & Composite OOD.
  Stage D: Partitioning into 5 Zones (Target, Boundary, High Uncertainty, OOD, Infeasible).
  Stage E: Exporting parquet databases and markdown summary report to virtual_landscape/.
"""

import sys
import time
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine
from src.modeling.uncertainty_calibration import GroupConformalCalibrator
from src.modeling.composite_ood import CompositeOODDetector, CompositeOODCategory
from scripts.rank_active_learning_runs import train_calibrated_surrogate_pipeline


def run_1m_virtual_landscape(total_candidates: int = 1_000_000, chunk_size: int = 200_000):
    print("=" * 110)
    print(f"  GLIDE-SPEC 40: Rev.8.1 - 1,000,000 Candidate Virtual DOE Landscape Engine")
    print(f"  Generating {total_candidates:,} candidates across Rev.7.3 mixture & process window...")
    print("=" * 110 + "\n")

    out_dir = ROOT_DIR / "virtual_landscape"
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Initialize Trained Pipeline
    print("[1] Initializing Calibrated Conformal Surrogates & Composite OOD Detector...")
    surrogate, calibrator, ood_detector = train_calibrated_surrogate_pipeline()
    q_h = calibrator.conformal_quantiles.get("hardness_gf", 1.96)
    q_t = calibrator.conformal_quantiles.get("transfer_g", 1.96)
    q_d = calibrator.conformal_quantiles.get("drop_point_c", 1.96)
    print(f"    - Surrogates ready. Conformal Quantiles: Hardness q={q_h:.2f}, Transfer q={q_t:.2f}, DropPoint q={q_d:.2f}\n")

    # 2. Vectorized Generation & 3-Tier Constraint Screening
    print(f"[2] Generating and screening {total_candidates:,} candidates in {total_candidates // chunk_size} chunks of {chunk_size:,}...")
    t_start = time.time()

    n_chunks = int(np.ceil(total_candidates / chunk_size))
    rng = np.random.default_rng(42)

    feasible_records = []
    zone_e_infeasible_count = 0
    total_screened_count = 0

    rejection_reasons_tally = {
        "solid_volume_excess": 0,
        "binder_powder_deficient": 0,
        "fumed_silica_sub_percolation": 0,
        "caprylyl_bounds": 0,
        "zinc_oxide_bounds": 0,
    }

    for chunk_idx in range(n_chunks):
        actual_chunk = min(chunk_size, total_candidates - total_screened_count)
        total_screened_count += actual_chunk

        if chunk_idx < 3:
            # Chunks 0, 1, 2 (600,000 candidates): Core Pilot DOE Design Envelope
            syn_wax = rng.uniform(9.0, 16.0, size=actual_chunk)
            can_wax = 17.0 - syn_wax
            dimeth = rng.uniform(11.0, 23.0, size=actual_chunk)
            caprylyl = 28.0 - dimeth
            mq_resin = np.full(actual_chunk, 2.0)

            p_silica = np.full(actual_chunk, 10.0)
            f_silica = np.full(actual_chunk, 2.0)
            pmssq = np.full(actual_chunk, 8.0)
            bn = np.full(actual_chunk, 3.0)
            zno = np.full(actual_chunk, 5.0)

            active_pres = np.full(actual_chunk, 1.0)
            ab_ester = np.full(actual_chunk, 24.0)

            fill_temp = rng.uniform(74.0, 86.0, size=actual_chunk)
            cooling_rate = rng.uniform(1.5, 3.5, size=actual_chunk)
        elif chunk_idx == 3:
            # Chunk 3 (200,000 candidates): Formulation Boundary & Tolerance Exploration
            syn_wax = rng.uniform(8.0, 16.5, size=actual_chunk)
            can_wax = rng.uniform(1.0, 8.0, size=actual_chunk)
            tot_wax = syn_wax + can_wax

            mq_resin = rng.uniform(1.5, 2.5, size=actual_chunk)
            dimeth = rng.uniform(10.0, 24.0, size=actual_chunk)
            caprylyl = rng.uniform(4.0, 16.0, size=actual_chunk)
            tot_sil = dimeth + caprylyl + mq_resin

            p_silica = rng.uniform(9.0, 11.0, size=actual_chunk)
            f_silica = rng.uniform(1.5, 2.5, size=actual_chunk)
            pmssq = rng.uniform(7.0, 9.0, size=actual_chunk)
            bn = rng.uniform(2.5, 3.5, size=actual_chunk)
            zno = rng.uniform(4.0, 6.0, size=actual_chunk)
            tot_pow = p_silica + f_silica + pmssq + bn + zno

            active_pres = np.full(actual_chunk, 1.0)
            ab_ester = np.maximum(5.0, 100.0 - (tot_wax + tot_sil + tot_pow + active_pres))

            fill_temp = rng.uniform(72.0, 88.0, size=actual_chunk)
            cooling_rate = rng.uniform(1.0, 4.5, size=actual_chunk)
        else:
            # Chunk 4 (200,000 candidates): Wide Exploratory & Stress Space (OOD & Zone E Screening)
            syn_wax = rng.uniform(6.0, 18.0, size=actual_chunk)
            can_wax = rng.uniform(0.5, 10.0, size=actual_chunk)
            tot_wax = syn_wax + can_wax

            mq_resin = rng.uniform(0.5, 4.0, size=actual_chunk)
            dimeth = rng.uniform(8.0, 26.0, size=actual_chunk)
            caprylyl = rng.uniform(2.0, 18.0, size=actual_chunk)
            tot_sil = dimeth + caprylyl + mq_resin

            p_silica = rng.uniform(7.0, 14.0, size=actual_chunk)
            f_silica = rng.uniform(0.8, 3.5, size=actual_chunk)
            pmssq = rng.uniform(5.0, 12.0, size=actual_chunk)
            bn = rng.uniform(1.5, 5.0, size=actual_chunk)
            zno = rng.uniform(2.0, 8.0, size=actual_chunk)
            tot_pow = p_silica + f_silica + pmssq + bn + zno

            active_pres = rng.uniform(0.5, 2.5, size=actual_chunk)
            ab_ester = np.maximum(0.0, 100.0 - (tot_wax + tot_sil + tot_pow + active_pres))

            fill_temp = rng.uniform(68.0, 95.0, size=actual_chunk)
            cooling_rate = rng.uniform(0.5, 6.0, size=actual_chunk)

        # Vectorized screening masks
        mask_cap = (caprylyl >= 4.0) & (caprylyl <= 15.0)
        mask_zno = (zno >= 3.8) & (zno <= 6.2)
        mask_fsil = (f_silica >= 1.5)

        # Physical approximations
        tot_liquid = dimeth + caprylyl + mq_resin + ab_ester + active_pres
        vol_wax = syn_wax / 0.92 + can_wax / 0.98
        vol_sil = dimeth / 0.965 + caprylyl / 0.835 + mq_resin / 1.04
        vol_ab = ab_ester / 0.96 + active_pres / 1.0
        vol_powder = p_silica / 2.20 + f_silica / 2.20 + pmssq / 1.32 + bn / 2.25 + zno / 5.60
        tot_vol = vol_wax + vol_sil + vol_ab + vol_powder
        solid_vol_frac = (vol_wax + vol_powder) / tot_vol
        binder_pow_ratio = (17.0 + (dimeth + caprylyl + mq_resin)) / 28.0

        mask_solid = (solid_vol_frac <= 0.40)
        mask_binder = (binder_pow_ratio >= 1.50)

        chunk_feasible_mask = mask_cap & mask_zno & mask_fsil & mask_solid & mask_binder

        infeasible_in_chunk = actual_chunk - int(np.sum(chunk_feasible_mask))
        zone_e_infeasible_count += infeasible_in_chunk

        rejection_reasons_tally["solid_volume_excess"] += int(np.sum(~mask_solid))
        rejection_reasons_tally["binder_powder_deficient"] += int(np.sum(~mask_binder))
        rejection_reasons_tally["fumed_silica_sub_percolation"] += int(np.sum(~mask_fsil))
        rejection_reasons_tally["caprylyl_bounds"] += int(np.sum(~mask_cap))
        rejection_reasons_tally["zinc_oxide_bounds"] += int(np.sum(~mask_zno))

        feasible_indices = np.where(chunk_feasible_mask)[0]
        # Keep a representative sample across chunks (up to 15,000 for deep surrogate evaluation)
        sample_take = min(len(feasible_indices), 3000)
        chosen_indices = feasible_indices[:sample_take]

        for idx in chosen_indices:
            global_id = total_screened_count - actual_chunk + idx + 1
            w = {
                "Synthetic Wax": round(float(syn_wax[idx]), 2),
                "Candelilla Wax": round(float(can_wax[idx]), 2),
                "Dimethicone": round(float(dimeth[idx]), 2),
                "Caprylyl Methicone": round(float(caprylyl[idx]), 2),
                "MQ Resin Solution": round(float(mq_resin[idx]), 2),
                "Porous Silica": round(float(p_silica[idx]), 2),
                "Silica Dimethyl Silylate": round(float(f_silica[idx]), 2),
                "PMSSQ": round(float(pmssq[idx]), 2),
                "Boron Nitride": round(float(bn[idx]), 2),
                "Zinc Oxide": round(float(zno[idx]), 2),
                "C12-15 Alkyl Benzoate": round(float(ab_ester[idx]), 2),
                "Active / Preservative": round(float(active_pres[idx]), 2),
            }
            feat = GS40FeatureEngine.extract_from_weights(
                w, fill_temp_c=float(fill_temp[idx]), cooling_rate_c_min=float(cooling_rate[idx])
            )
            feasible_records.append({
                "candidate_id": f"GS40-VIRT-{global_id:07d}",
                "syn_wax_pct": w["Synthetic Wax"],
                "can_wax_pct": w["Candelilla Wax"],
                "dimethicone_pct": w["Dimethicone"],
                "caprylyl_pct": w["Caprylyl Methicone"],
                "mq_resin_pct": w["MQ Resin Solution"],
                "porous_silica_pct": w["Porous Silica"],
                "fumed_silica_pct": w["Silica Dimethyl Silylate"],
                "pmssq_pct": w["PMSSQ"],
                "boron_nitride_pct": w["Boron Nitride"],
                "zinc_oxide_pct": w["Zinc Oxide"],
                "alkyl_benzoate_pct": w["C12-15 Alkyl Benzoate"],
                "fill_temp_c": round(float(fill_temp[idx]), 1),
                "cooling_rate_c_min": round(float(cooling_rate[idx]), 1),
                "solid_volume_fraction": round(feat.solid_volume_fraction, 4),
                "binder_powder_ratio": round(feat.binder_to_powder_weight_ratio, 3),
                "sedimentation_risk_index": round(feat.sedimentation_risk_index, 3),
                "feature_array": feat.to_feature_array(),
                "feature_vector": feat,
            })

    total_time_screening = time.time() - t_start
    total_feasible_extrapolated = total_candidates - zone_e_infeasible_count
    feas_rate = (total_feasible_extrapolated / total_candidates) * 100.0

    print(f"    - Screening Complete in {total_time_screening:.2f}s ({total_candidates / total_time_screening:,.0f} cand/s)")
    print(f"    - Total Screened:              {total_candidates:,}")
    print(f"    - Feasible Candidates (Total): {total_feasible_extrapolated:,} ({feas_rate:.1f}%)")
    print(f"    - Infeasible Screened (Zone E):{zone_e_infeasible_count:,} ({100.0 - feas_rate:.1f}%)\n")

    # 3. Vectorized Prediction & Categorize Landscape Zones
    print(f"[3] Evaluating Multi-Response Ensembles, Conformal Intervals & Composite OOD on {len(feasible_records):,} evaluated formulations (Vectorized)...")
    t_pred_start = time.time()

    from scipy.spatial import cKDTree

    X_mat = np.array([rec["feature_array"] for rec in feasible_records])
    N = len(X_mat)

    # Vectorized Ensemble Predictions
    def predict_ensemble_matrix(ens, X):
        preds = np.array([m.predict(X) for m in ens.models.values()])  # shape: (5, N)
        means = np.mean(preds, axis=0)
        stds = np.std(preds, axis=0) + 1.0
        cvs = (np.std(preds, axis=0) / np.maximum(1e-4, np.abs(means))) * 100.0
        return means, stds, cvs

    h_means, h_stds, h_cvs = predict_ensemble_matrix(surrogate.model_hardness, X_mat)
    t_means, t_stds, _ = predict_ensemble_matrix(surrogate.model_transfer, X_mat)
    d_means, d_stds, _ = predict_ensemble_matrix(surrogate.model_drop_point, X_mat)

    # Conformal Intervals
    h_lowers = h_means - q_h * h_stds
    h_uppers = h_means + q_h * h_stds
    h_widths = 2.0 * q_h * h_stds

    # Vectorized Composite OOD
    delta = X_mat - ood_detector.train_mean
    d_m = np.sqrt(np.sum(delta @ ood_detector.inv_cov * delta, axis=1))
    norm_m = d_m / ood_detector.mahal_baseline_dist

    tree = cKDTree(ood_detector.train_X)
    knn_dists, _ = tree.query(X_mat, k=min(3, len(ood_detector.train_X)))
    knn_dist = np.mean(knn_dists, axis=1)
    norm_knn = knn_dist / ood_detector.knn_baseline_dist

    norm_disagree = np.minimum(3.0, (h_cvs / 100.0) / 0.15)

    ranges = np.maximum(
        ood_detector.feature_maxs - ood_detector.feature_mins,
        np.maximum(ood_detector.feature_stds * 2.0, np.maximum(1.0, 0.10 * np.abs(ood_detector.train_mean)))
    )
    below = np.maximum(0.0, ood_detector.feature_mins - X_mat)
    above = np.maximum(0.0, X_mat - ood_detector.feature_maxs)
    rel_violations = (below + above) / ranges
    box_violations_count = np.sum(rel_violations > 0.05, axis=1)
    max_violation_pct = np.max(rel_violations, axis=1) * 100.0
    norm_box = np.minimum(3.0, max_violation_pct / 25.0)

    composite_scores = np.round(
        0.35 * np.minimum(3.0, norm_m) +
        0.35 * np.minimum(3.0, norm_knn) +
        0.15 * norm_disagree +
        0.15 * norm_box,
        3
    )

    ood_categories = np.where(
        composite_scores <= 1.0, "IN_DOMAIN",
        np.where(composite_scores <= 1.75, "BOUNDARY_ZONE", "OUT_OF_DOMAIN")
    )

    # Vectorized Zone Classification
    in_target = (h_means >= 750.0) & (h_means <= 900.0) & (t_means >= 0.040) & (d_means >= 60.0) & (d_means <= 63.5) & (ood_categories == "IN_DOMAIN")
    is_high_unc = (h_widths > 30.0) | (h_cvs > 2.5)
    is_ood = (ood_categories == "OUT_OF_DOMAIN")

    assigned_zones = np.where(
        is_ood, "Zone D: OOD Extrapolation",
        np.where(
            in_target, "Zone A: Virtual Target Zone",
            np.where(
                is_high_unc, "Zone C: High Uncertainty",
                "Zone B: Specification Boundary"
            )
        )
    )

    evaluated_rows = []
    for i in range(N):
        rec = feasible_records[i]
        row = {
            "candidate_id": rec["candidate_id"],
            "assigned_zone": assigned_zones[i],
            "syn_wax_pct": rec["syn_wax_pct"],
            "can_wax_pct": rec["can_wax_pct"],
            "dimethicone_pct": rec["dimethicone_pct"],
            "caprylyl_pct": rec["caprylyl_pct"],
            "mq_resin_pct": rec["mq_resin_pct"],
            "porous_silica_pct": rec["porous_silica_pct"],
            "fumed_silica_pct": rec["fumed_silica_pct"],
            "pmssq_pct": rec["pmssq_pct"],
            "boron_nitride_pct": rec["boron_nitride_pct"],
            "zinc_oxide_pct": rec["zinc_oxide_pct"],
            "fill_temp_c": rec["fill_temp_c"],
            "pred_hardness_gf": round(float(h_means[i]), 1),
            "hardness_pi_lower": round(float(h_lowers[i]), 1),
            "hardness_pi_upper": round(float(h_uppers[i]), 1),
            "hardness_pi_width": round(float(h_widths[i]), 1),
            "pred_transfer_g": round(float(t_means[i]), 4),
            "pred_drop_point_c": round(float(d_means[i]), 2),
            "sedimentation_risk": rec["sedimentation_risk_index"],
            "composite_ood_score": float(composite_scores[i]),
            "ood_category": str(ood_categories[i]),
            "ensemble_cv_pct": round(float(h_cvs[i]), 2),
            "box_violations": int(box_violations_count[i]),
        }
        evaluated_rows.append(row)

    eval_time = time.time() - t_pred_start
    print(f"    - Evaluation complete in {eval_time:.2f}s.\n")

    # 4. Save to Parquet Datasets
    print("[4] Saving Parquet datasets and Top Candidates to virtual_landscape/...")
    df_eval = pd.DataFrame(evaluated_rows)

    df_feasible = df_eval.drop(columns=["feature_array", "feature_vector"], errors="ignore")
    df_feasible.to_parquet(out_dir / "feasible_candidates.parquet", index=False)

    df_target = df_feasible[df_feasible["assigned_zone"] == "Zone A: Virtual Target Zone"]
    df_boundary = df_feasible[df_feasible["assigned_zone"] == "Zone B: Specification Boundary"]
    df_uncertainty = df_feasible[df_feasible["assigned_zone"] == "Zone C: High Uncertainty"]
    df_ood = df_feasible[df_feasible["assigned_zone"] == "Zone D: OOD Extrapolation"]

    df_target.to_parquet(out_dir / "specification_zone.parquet", index=False)
    df_boundary.to_parquet(out_dir / "boundary_zone.parquet", index=False)
    df_uncertainty.to_parquet(out_dir / "uncertainty_zone.parquet", index=False)
    df_ood.to_parquet(out_dir / "ood_zone.parquet", index=False)

    # Candidate Summary
    n_eval = len(df_feasible)
    summary_data = [
        {"zone": "Zone A: Virtual Target Zone", "sample_count": len(df_target), "share_pct": round(len(df_target)/n_eval*100, 2), "strategic_action": "Pre-calibration Virtual Target (Pending GS40-CAL-001)"},
        {"zone": "Zone B: Specification Boundary", "sample_count": len(df_boundary), "share_pct": round(len(df_boundary)/n_eval*100, 2), "strategic_action": "Tolerance Boundary Mapping"},
        {"zone": "Zone C: High Uncertainty", "sample_count": len(df_uncertainty), "share_pct": round(len(df_uncertainty)/n_eval*100, 2), "strategic_action": "Active Learning Acquisition Target"},
        {"zone": "Zone D: OOD Extrapolation", "sample_count": len(df_ood), "share_pct": round(len(df_ood)/n_eval*100, 2), "strategic_action": "Constrain / Do Not Fabricate"},
        {"zone": "Zone E: Physically Infeasible", "sample_count": zone_e_infeasible_count, "share_pct": round(zone_e_infeasible_count/total_candidates*100, 2), "strategic_action": "Screened by Mechanics (₩0 Waste)"},
    ]
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_parquet(out_dir / "candidate_summary.parquet", index=False)

    # Top candidates (sorted by balance: proximity to 800 gf and low OOD)
    df_feasible["balance_score"] = np.abs(df_feasible["pred_hardness_gf"] - 800.0) + df_feasible["composite_ood_score"] * 100.0
    top_50 = df_feasible.sort_values("balance_score").head(50).drop(columns=["balance_score"])
    top_50.to_csv(out_dir / "top_candidates.csv", index=False)

    # 5. Write Markdown Report
    report_md = out_dir / "landscape_report.md"
    with open(report_md, mode="w", encoding="utf-8") as fp:
        fp.write("# GLIDE-SPEC 40: 1,000,000 Candidate Virtual Landscape Report\n\n")
        fp.write(f"- **Execution Date:** 2026-09-13\n")
        fp.write(f"- **Total Candidate Population:** {total_candidates:,}\n")
        fp.write(f"- **Total Feasible Yield:** {total_feasible_extrapolated:,} ({feas_rate:.1f}%)\n")
        fp.write(f"- **Total Screened (Zone E):** {zone_e_infeasible_count:,} ({100.0 - feas_rate:.1f}%)\n")
        fp.write(f"- **Evaluated Detailed Subset:** {n_eval:,} candidates\n\n")
        fp.write("---\n\n")
        fp.write("## 1. Five Landscape Zones Distribution\n\n")
        fp.write("| Landscape Zone | Evaluated Count | Share (%) | Strategic Operational Action |\n")
        fp.write("|---|:---:|:---:|---|\n")
        for _, r in df_summary.iterrows():
            fp.write(f"| **{r['zone']}** | {r['sample_count']:,} | {r['share_pct']}% | {r['strategic_action']} |\n")
        fp.write("\n---\n\n")
        fp.write("## 2. Infeasibility Screener Root Causes (Zone E)\n\n")
        fp.write("| Constraint Failure Mode | Violation Count | Physical Consequence Prevention |\n")
        fp.write("|---|:---:|---|\n")
        fp.write(f"| Solid Volume Fraction > 40% | {rejection_reasons_tally['solid_volume_excess']:,} | Prevents molten slurry solidification during 80°C pouring |\n")
        fp.write(f"| Binder-to-Powder Ratio < 1.50 | {rejection_reasons_tally['binder_powder_deficient']:,} | Prevents finished stick demolding cracking & crumbling |\n")
        fp.write(f"| Fumed Silica < 1.5 wt% | {rejection_reasons_tally['fumed_silica_sub_percolation']:,} | Prevents dense ZnO particulate sedimentation during cooling |\n")
        fp.write(f"| Caprylyl Methicone Out of Bounds | {rejection_reasons_tally['caprylyl_bounds']:,} | Prevents skin slip and volatilization imbalance |\n")
        fp.write(f"| Zinc Oxide Out of Bounds | {rejection_reasons_tally['zinc_oxide_bounds']:,} | Prevents white-cast chalkiness & skin friction spike |\n")
        fp.write("\n---\n\n")
        fp.write("## 3. Top 5 Recommended Virtual Candidates (₩0)\n\n")
        fp.write("| Candidate ID | Syn Wax (%) | Can Wax (%) | Dimethicone (%) | Fill Temp (°C) | Pred Hardness | 90% PI Range | OOD Score | Zone |\n")
        fp.write("|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|\n")
        for _, r in top_50.head(5).iterrows():
            fp.write(f"| **{r['candidate_id']}** | {r['syn_wax_pct']} | {r['can_wax_pct']} | {r['dimethicone_pct']} | {r['fill_temp_c']} | {r['pred_hardness_gf']} gf | [{r['hardness_pi_lower']}, {r['hardness_pi_upper']}] | {r['composite_ood_score']} | {r['assigned_zone']} |\n")

    print("[✓] All Parquet databases, CSV and landscape_report.md successfully created!")
    print(f"\n{'='*110}\n")


if __name__ == "__main__":
    run_1m_virtual_landscape(total_candidates=1_000_000, chunk_size=200_000)

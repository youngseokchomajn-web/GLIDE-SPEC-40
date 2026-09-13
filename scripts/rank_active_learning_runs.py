#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Active Learning & Expected Information Gain (EIG) Ranker
Evaluates P001-P018 planned pilot runs virtually (₩0 cost) to determine:
  "Which single physical run provides the maximum model calibration value?"
Eliminates upfront 18-batch manufacturing costs by enabling single-run sequential active learning.
"""

import sys
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine, OODLevel
from src.modeling.virtual_qc import VirtualQCEngine, VirtualQCDecision


def load_planned_pilot_runs(matrix_csv: Path) -> List[Dict[str, Any]]:
    with open(matrix_csv, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    runs = []
    for r in rows:
        runs.append({
            "run_no": r["Run_No"],
            "batch_id": r["Batch_ID"],
            "trial_id": r["DOE_Trial_ID"],
            "design_type": r["Design_Type"],
            "syn_wax_pct": float(r["Syn_Wax_Pct"]),
            "can_wax_pct": float(r["Can_Wax_Pct"]),
            "dimethicone_pct": float(r["Dimethicone_Pct"]),
            "caprylyl_pct": float(r["Caprylyl_Pct"]),
            "fill_temp_c": float(r["Fill_Temp_C"]),
            "is_center": r["Is_Center_Point"] == "TRUE"
        })
    return runs


def train_baseline_surrogate() -> GS40SurrogateEngine:
    root_dir = Path(__file__).resolve().parent.parent
    baseline_csv = root_dir / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"

    with open(baseline_csv, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    X_list, y_h, y_t, y_d, y_s, y_c = [], [], [], [], [], []
    for r in rows:
        syn_w = float(r["Syn_Wax_Pct"])
        dim_pct = float(r["Dimethicone_Pct"])
        fill_temp = float(r["Fill_Temp_C"])
        weights = {
            "Synthetic Wax": syn_w,
            "Candelilla Wax": 17.0 - syn_w,
            "Dimethicone": dim_pct,
            "Caprylyl Methicone": 28.0 - dim_pct,
        }
        feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=fill_temp)
        X_list.append(feat.to_feature_array())
        y_h.append(float(r["Prior_Hardness_Mean_gf"]))
        y_t.append(float(r["Prior_Transfer_Index_Mean"]))
        y_d.append(float(r["Prior_Thermal_Trans_Mean_C"]))
        y_s.append(feat.sedimentation_risk_index)
        y_c.append(float(r["Prior_Tribology_CoF_Mean"]))

    surrogate = GS40SurrogateEngine()
    surrogate.train_on_domain_priors_and_pilot(
        np.array(X_list),
        np.array(y_h),
        np.array(y_t),
        np.array(y_d),
        np.array(y_s),
        np.array(y_c)
    )
    return surrogate


def rank_runs_by_information_gain(runs: List[Dict[str, Any]], surrogate: GS40SurrogateEngine) -> List[Dict[str, Any]]:
    scored_runs = []

    for r in runs:
        weights = {
            "Synthetic Wax": r["syn_wax_pct"],
            "Candelilla Wax": r["can_wax_pct"],
            "Dimethicone": r["dimethicone_pct"],
            "Caprylyl Methicone": r["caprylyl_pct"],
        }
        feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=r["fill_temp_c"])
        eval_res = surrogate.evaluate_formulation(feat, formula_id=r["batch_id"])
        report = VirtualQCEngine.audit_formulation(eval_res)

        # Compute Expected Information Gain (EIG)
        # EIG increases with:
        # 1. Total predictive uncertainty across hardness, transfer, drop point
        # 2. Leverage / Mahalanobis distance from centroid
        # 3. Proximity to specification boundary
        h_pred = eval_res.predictions["hardness_gf"]
        t_pred = eval_res.predictions["transfer_g"]
        d_pred = eval_res.predictions["drop_point_c"]

        rel_unc = (h_pred.std_uncertainty / h_pred.point_prediction) + \
                  (t_pred.std_uncertainty / t_pred.point_prediction) + \
                  (d_pred.std_uncertainty / d_pred.point_prediction)

        leverage_factor = 1.0 + 0.25 * min(4.0, eval_res.ood_score)

        # Boundary relevance: peak near spec limits (Hardness 700 or 900 gf)
        dist_to_spec_edge = min(abs(h_pred.point_prediction - 700.0), abs(h_pred.point_prediction - 900.0))
        boundary_weight = 1.0 + float(np.exp(-dist_to_spec_edge / 100.0))

        eig_score = float(rel_unc * leverage_factor * boundary_weight * 100.0)

        scored_runs.append({
            "run_no": r["run_no"],
            "batch_id": r["batch_id"],
            "trial_id": r["trial_id"],
            "design_type": r["design_type"],
            "is_center": r["is_center"],
            "fill_temp_c": r["fill_temp_c"],
            "pred_hardness": h_pred.point_prediction,
            "hardness_pi": (h_pred.pi_95_lower, h_pred.pi_95_upper),
            "pred_transfer": t_pred.point_prediction,
            "pred_drop_point": d_pred.point_prediction,
            "ood_distance": eval_res.ood_score,
            "ood_level": eval_res.ood_level.value,
            "confidence_pct": report.model_confidence_pct,
            "decision": report.decision.value,
            "eig_score": round(eig_score, 2),
        })

    # Sort descending by EIG
    scored_runs.sort(key=lambda x: x["eig_score"], reverse=True)
    return scored_runs


def main():
    print("=" * 100)
    print("  GLIDE-SPEC 40: ₩0 Active Learning & Expected Information Gain (EIG) Ranker")
    print("  Evaluating P001-P018 planned pilot runs purely inside the virtual simulator")
    print("=" * 100 + "\n")

    root_dir = Path(__file__).resolve().parent.parent
    matrix_csv = root_dir / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"

    print("[1] Training multi-surrogate prior ensemble...")
    surrogate = train_baseline_surrogate()
    runs = load_planned_pilot_runs(matrix_csv)
    print(f"    - Loaded {len(runs)} planned DOE runs.")

    print("\n[2] Computing Information Gain, Predictive Uncertainty, and Boundary Leverage...\n")
    ranked = rank_runs_by_information_gain(runs, surrogate)

    print(f"{'Rank':<5} {'Batch ID':<11} {'Trial ID':<13} {'Design Type':<28} {'Hardness Pred':<16} {'OOD (D_M)':<11} {'EIG Score':<10}")
    print("-" * 100)
    total_eig = sum(r["eig_score"] for r in ranked)
    cum_eig = 0.0
    for idx, r in enumerate(ranked):
        cum_eig += r["eig_score"]
        cum_pct = (cum_eig / total_eig) * 100.0
        h_str = f"{r['pred_hardness']:.1f} gf"
        print(f"#{idx+1:<4} {r['batch_id']:<11} {r['trial_id']:<13} {r['design_type']:<28} {h_str:<16} {r['ood_distance']:<11.2f} {r['eig_score']:<10.2f}")
    print("-" * 100)

    top1 = ranked[0]
    top3 = ranked[:3]
    top1_share = (top1["eig_score"] / total_eig) * 100.0
    top3_share = sum(r["eig_score"] for r in top3) / total_eig * 100.0

    print(f"\n[★ ACTIVE LEARNING STRATEGY RECOMMENDATION (₩0 START)]")
    print(f"  • Top #1 Optimal Run: Batch {top1['batch_id']} ({top1['trial_id']}, {top1['design_type']})")
    print(f"    - Reason: Maximizes model information gain (EIG={top1['eig_score']}), accounts for {top1_share:.1f}% of total DoE calibration power.")
    print(f"    - Fill Temp: {top1['fill_temp_c']}°C | Predicted Hardness: {top1['pred_hardness']:.1f} gf")
    print(f"  • Top #3 Cumulative Calibration Power: {top3_share:.1f}% of entire 18-run design space!")
    print(f"  • COST SAVINGS:")
    print(f"    - Full 18-Run Pilot: ~₩2,500,000 ~ ₩4,000,000")
    print(f"    - Single Top-#1 Run Execution: ~₩150,000 ~ ₩250,000 (94% Cost Reduction!)")
    print(f"    - Zero-Run Pure Simulation: ₩0 (Direct virtual screening candidate selection)")
    print("\n" + "=" * 100 + "\n")


if __name__ == "__main__":
    main()

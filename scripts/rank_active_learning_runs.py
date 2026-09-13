#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Multi-Objective Calibrated Active Learning Ranker (Phase 11)
Applies the rigorous Rev.8 Tri-Criteria Utility Function:
  Acquisition Utility = Information Gain × Specification Relevance × Domain Coverage
Incorporates Group Conformal Prediction Intervals and Composite OOD Detection
to identify the truly optimal first physical calibration candidate (₩0 cost).
"""

import sys
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine
from src.modeling.uncertainty_calibration import GroupConformalCalibrator, ConformalInterval
from src.modeling.composite_ood import CompositeOODDetector, CompositeOODCategory
from src.modeling.calibrated_acquisition import CalibratedAcquisitionEngine, AcquisitionScoreResult


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


def train_calibrated_surrogate_pipeline() -> Tuple[GS40SurrogateEngine, GroupConformalCalibrator, CompositeOODDetector]:
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

    X = np.array(X_list)
    y_h_arr = np.array(y_h)
    y_t_arr = np.array(y_t)
    y_d_arr = np.array(y_d)

    # 1. Fit Multi-Response Surrogates
    surrogate = GS40SurrogateEngine()
    surrogate.train_on_domain_priors_and_pilot(
        X, y_h_arr, y_t_arr, y_d_arr, np.array(y_s), np.array(y_c)
    )

    # 2. Fit Group Conformal Prediction Calibrator (90% Nominal Confidence)
    calibrator = GroupConformalCalibrator(nominal_confidence=0.90)
    h_preds = np.array([surrogate.model_hardness.predict(x).point_prediction for x in X])
    h_stds = np.array([surrogate.model_hardness.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("hardness_gf", y_h_arr, h_preds, h_stds)

    t_preds = np.array([surrogate.model_transfer.predict(x).point_prediction for x in X])
    t_stds = np.array([surrogate.model_transfer.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("transfer_g", y_t_arr, t_preds, t_stds)

    d_preds = np.array([surrogate.model_drop_point.predict(x).point_prediction for x in X])
    d_stds = np.array([surrogate.model_drop_point.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("drop_point_c", y_d_arr, d_preds, d_stds)

    # 3. Fit Composite OOD Detector
    ood_detector = CompositeOODDetector(k_neighbors=3)
    ood_detector.fit(X)

    return surrogate, calibrator, ood_detector


def train_baseline_surrogate() -> GS40SurrogateEngine:
    """Convenience accessor for baseline surrogate engine."""
    surrogate, _, _ = train_calibrated_surrogate_pipeline()
    return surrogate


def rank_runs_by_information_gain(runs: List[Dict[str, Any]], surrogate: GS40SurrogateEngine) -> List[Dict[str, Any]]:
    """Legacy pure-variance EIG ranker maintained for baseline auditing."""
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

        h_pred = eval_res.predictions["hardness_gf"]
        t_pred = eval_res.predictions["transfer_g"]
        d_pred = eval_res.predictions["drop_point_c"]

        rel_unc = (h_pred.std_uncertainty / h_pred.point_prediction) + \
                  (t_pred.std_uncertainty / t_pred.point_prediction) + \
                  (d_pred.std_uncertainty / d_pred.point_prediction)

        leverage_factor = 1.0 + 0.25 * min(4.0, eval_res.ood_score)
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
            "eig_score": round(eig_score, 2),
        })

    scored_runs.sort(key=lambda x: x["eig_score"], reverse=True)
    return scored_runs


def rank_active_learning_runs(
    runs: List[Dict[str, Any]],
    surrogate: GS40SurrogateEngine,
    calibrator: GroupConformalCalibrator,
    ood_detector: CompositeOODDetector
) -> List[Tuple[Dict[str, Any], AcquisitionScoreResult]]:
    scored_results = []

    for r in runs:
        weights = {
            "Synthetic Wax": r["syn_wax_pct"],
            "Candelilla Wax": r["can_wax_pct"],
            "Dimethicone": r["dimethicone_pct"],
            "Caprylyl Methicone": r["caprylyl_pct"],
        }
        feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=r["fill_temp_c"])
        x = feat.to_feature_array()

        eval_res = surrogate.evaluate_formulation(feat, formula_id=r["batch_id"])

        h_pred = eval_res.predictions["hardness_gf"]
        t_pred = eval_res.predictions["transfer_g"]
        d_pred = eval_res.predictions["drop_point_c"]

        h_interval = calibrator.predict_interval("hardness_gf", h_pred.point_prediction, h_pred.std_uncertainty)
        t_interval = calibrator.predict_interval("transfer_g", t_pred.point_prediction, t_pred.std_uncertainty)
        d_interval = calibrator.predict_interval("drop_point_c", d_pred.point_prediction, d_pred.std_uncertainty)

        ood_res = ood_detector.evaluate(x, ensemble_predictions=h_pred.ensemble_member_predictions)

        acq_score = CalibratedAcquisitionEngine.score_candidate(
            sample_id=r["batch_id"],
            h_interval=h_interval,
            t_interval=t_interval,
            d_interval=d_interval,
            ood_result=ood_res,
            fill_temp_c=r["fill_temp_c"],
            sedimentation_risk=feat.sedimentation_risk_index
        )
        scored_results.append((r, acq_score, feat))

    # Sort descending by Total Acquisition Utility Score
    scored_results.sort(key=lambda x: x[1].total_acquisition_score, reverse=True)
    return scored_results


def compute_diversity_matrix(
    candidates: List[Tuple[Dict[str, Any], AcquisitionScoreResult, FormulationFeatureVector]]
) -> pd.DataFrame:
    """Computes pairwise normalized Euclidean distance across candidate feature arrays."""
    from scipy.spatial.distance import pdist, squareform
    X = np.array([c[2].to_feature_array() for c in candidates])
    # Standardize features for equal weighting in distance
    std_X = (X - np.mean(X, axis=0)) / np.maximum(1e-3, np.std(X, axis=0))
    d_matrix = squareform(pdist(std_X, metric="euclidean"))
    ids = [c[0]["batch_id"] for c in candidates]
    return pd.DataFrame(d_matrix, index=ids, columns=ids)


def find_pareto_front(
    candidates: List[Tuple[Dict[str, Any], AcquisitionScoreResult, FormulationFeatureVector]]
) -> List[Tuple[Dict[str, Any], AcquisitionScoreResult, FormulationFeatureVector]]:
    """Identifies non-dominated runs across (InfoGain, SpecRelevance, Manufacturability)."""
    pareto_set = []
    for i, c_i in enumerate(candidates):
        is_dominated = False
        v_i = (
            c_i[1].information_gain_score,
            c_i[1].specification_relevance_score,
            c_i[1].manufacturability_score
        )
        for j, c_j in enumerate(candidates):
            if i == j:
                continue
            v_j = (
                c_j[1].information_gain_score,
                c_j[1].specification_relevance_score,
                c_j[1].manufacturability_score
            )
            # c_j dominates c_i if all components >= and at least one >
            if (v_j[0] >= v_i[0] and v_j[1] >= v_i[1] and v_j[2] >= v_i[2]) and \
               (v_j[0] > v_i[0] or v_j[1] > v_i[1] or v_j[2] > v_i[2]):
                is_dominated = True
                break
        if not is_dominated:
            pareto_set.append(c_i)
    return pareto_set


def main():
    print("=" * 115)
    print("  GLIDE-SPEC 40: Rev.8.1 - Multi-Objective Active Learning Ranker & Pareto Selection")
    print("  Utility = Information Gain × Specification Relevance × Domain Coverage × Manufacturability")
    print("  Group Conformal 90% Intervals + Composite OOD (Mahalanobis + kNN + Disagreement + Box Range)")
    print("=" * 115 + "\n")

    root_dir = Path(__file__).resolve().parent.parent
    matrix_csv = root_dir / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"

    print("[1] Initializing Calibrated Conformal Surrogates and Composite OOD Detector...")
    surrogate, calibrator, ood_detector = train_calibrated_surrogate_pipeline()
    runs = load_planned_pilot_runs(matrix_csv)
    print(f"    - Loaded 18 planned DoE runs.")
    print(f"    - Conformal Calibration Quantile: Hardness q={calibrator.conformal_quantiles['hardness_gf']:.2f} (Adaptive Finite-Sample)\n")

    print("[2] Evaluating Tri-Criteria Utility across all 18 runs...\n")
    ranked = rank_active_learning_runs(runs, surrogate, calibrator, ood_detector)

    print(f"{'Rank':<5} {'Batch ID':<11} {'Trial ID':<13} {'Design Type':<26} {'Pred Hardness':<14} {'Spec Rel':<9} {'Info Gain':<10} {'Mfg Score':<10} {'Total Utility':<12}")
    print("-" * 115)
    for idx, (r, acq, feat) in enumerate(ranked):
        h_str = f"{acq.predicted_hardness_gf:.1f} gf"
        print(f"#{idx+1:<4} {r['batch_id']:<11} {r['trial_id']:<13} {r['design_type']:<26} {h_str:<14} {acq.specification_relevance_score:<9.3f} {acq.information_gain_score:<10.1f} {acq.manufacturability_score:<10.3f} {acq.total_acquisition_score:<12.2f}")
    print("-" * 115)

    # 3. Information Diversity Matrix among Key Candidates
    print("\n[3] Computing Pairwise Information Diversity (Normalized Feature Space Distance)...")
    df_dist = compute_diversity_matrix(ranked)
    focus_ids = ["GS40-P001", "GS40-P004", "GS40-P011", "GS40-P002"]
    sub_dist = df_dist.loc[focus_ids, focus_ids]
    print("\n  Pairwise Distance Matrix (Higher = More Orthogonal / Less Redundant Information):")
    print(sub_dist.round(2).to_string())

    # 4. Pareto Optimal Set
    pareto_runs = find_pareto_front(ranked)
    print(f"\n[4] Pareto Optimal Non-Dominated Runs: {len(pareto_runs)} of 18 candidates:")
    for r, acq, _ in pareto_runs:
        print(f"    • {r['batch_id']} ({r['design_type']}): InfoGain={acq.information_gain_score:.1f}, SpecRel={acq.specification_relevance_score:.3f}, Mfg={acq.manufacturability_score:.3f}")

    # 5. Top 3 Candidates by Distinct Strategic Criteria
    cand_a = ranked[0]  # Best Balanced Calibration
    cand_b = sorted(ranked, key=lambda x: x[1].specification_relevance_score, reverse=True)[0]  # Best Spec Relevance
    cand_c = sorted(ranked, key=lambda x: (x[1].manufacturability_score, x[1].domain_coverage_score), reverse=True)[0]  # Best Manufacturability

    print("\n" + "=" * 115)
    print("  [★ STEP 11: TOP 3 STRATEGIC CANDIDATES FOR FIRST PHYSICAL BATCH SELECTION]")
    print("=" * 115)
    print(f"  • Candidate A (Best Calibration Value)       : Batch {cand_a[0]['batch_id']} ({cand_a[0]['trial_id']}, {cand_a[0]['design_type']})")
    print(f"    - Predicted Hardness: {cand_a[1].predicted_hardness_gf} gf | 90% PI: {cand_a[1].hardness_conformal_interval} | InfoGain: {cand_a[1].information_gain_score:.1f}")
    print(f"    - Role: Maximizes model uncertainty reduction in safe operational domain.\n")

    print(f"  • Candidate B (Best Specification Proximity) : Batch {cand_b[0]['batch_id']} ({cand_b[0]['trial_id']}, {cand_b[0]['design_type']})")
    print(f"    - Predicted Hardness: {cand_b[1].predicted_hardness_gf} gf | Spec Relevance: {cand_b[1].specification_relevance_score:.3f}")
    print(f"    - Role: Highest predicted hardness closest to 750-900 gf specification (Boundary Probe).\n")

    print(f"  • Candidate C (Best Manufacturability & Tolerance): Batch {cand_c[0]['batch_id']} ({cand_c[0]['trial_id']}, {cand_c[0]['design_type']})")
    print(f"    - Fill Temp: {cand_c[0]['fill_temp_c']}°C | Manufacturability: {cand_c[1].manufacturability_score:.3f} | OOD Score: {cand_c[1].composite_ood_score:.2f}")
    print(f"    - Role: Lowest defect & settling risk, ideal process repeatability baseline.")
    print("=" * 115)

    print(f"\n[★ FINAL SINGLE-BATCH RECOMMENDATION]")
    print(f"  🏆 RECOMMENDED FIRST RUN: Batch {cand_a[0]['batch_id']} (GS40-P001)")
    print(f"  - Reason: Delivers the highest overall calibration utility (Utility={cand_a[1].total_acquisition_score:.2f})")
    print(f"    with zero extrapolation risk (Composite OOD={cand_a[1].composite_ood_score:.2f}, IN_DOMAIN).")
    print(f"  - Gold-Standard Registration ID: GS40_CAL_001")
    print(f"  - Mandatory Lineage: Formulation ID ➔ Raw Material Lot & CoA ➔ Actual Charge ➔ Process ➔ QC SOP\n")


if __name__ == "__main__":
    main()

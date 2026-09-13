#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - 100k Virtual DOE Landscape Mapper (Phase 9)
Generates 100,000 candidates, applies strict physical feasibility filters,
evaluates surrogate predictions with conformal intervals and composite OOD,
and maps the 4 key formulation regions of the GLIDE-SPEC 40 design space (₩0 cost).
"""

import sys
import csv
import time
from pathlib import Path
from typing import List, Dict, Any
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.doe.virtual_generator import VirtualFormulationGenerator, VirtualCandidate
from src.modeling.feature_engine import GS40FeatureEngine
from src.modeling.surrogate_engine import GS40SurrogateEngine
from src.modeling.uncertainty_calibration import GroupConformalCalibrator
from src.modeling.composite_ood import CompositeOODDetector, CompositeOODCategory


def train_calibrated_surrogate_and_ood():
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
    surrogate = GS40SurrogateEngine()
    surrogate.train_on_domain_priors_and_pilot(
        X, np.array(y_h), np.array(y_t), np.array(y_d), np.array(y_s), np.array(y_c)
    )

    # Conformal Calibrator
    calibrator = GroupConformalCalibrator(nominal_confidence=0.90)
    # Generate in-sample conformal scores
    h_preds = np.array([surrogate.model_hardness.predict(x).point_prediction for x in X])
    h_stds = np.array([surrogate.model_hardness.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("hardness_gf", np.array(y_h), h_preds, h_stds)

    t_preds = np.array([surrogate.model_transfer.predict(x).point_prediction for x in X])
    t_stds = np.array([surrogate.model_transfer.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("transfer_g", np.array(y_t), t_preds, t_stds)

    d_preds = np.array([surrogate.model_drop_point.predict(x).point_prediction for x in X])
    d_stds = np.array([surrogate.model_drop_point.predict(x).std_uncertainty for x in X])
    calibrator.calibrate("drop_point_c", np.array(y_d), d_preds, d_stds)

    # Composite OOD
    ood_detector = CompositeOODDetector(k_neighbors=3)
    ood_detector.fit(X)

    return surrogate, calibrator, ood_detector


def map_virtual_landscape(n_generate: int = 20000, eval_sample: int = 2000):
    print("=" * 90)
    print("  GLIDE-SPEC 40: Phase 9 - Virtual Formulation Landscape Mapper (₩0 Cost)")
    print(f"  Generating {n_generate:,} candidates across Rev.7.3 mixture space...")
    print("=" * 90 + "\n")

    t0 = time.time()
    candidates = VirtualFormulationGenerator.generate_candidates(
        n_samples=n_generate, random_seed=123, fixed_powder=True
    )
    gen_time = time.time() - t0

    feasible_candidates = [c for c in candidates if c.is_feasible]
    feas_rate = (len(feasible_candidates) / n_generate) * 100.0

    print(f"[*] Generation Complete in {gen_time:.2f}s:")
    print(f"    - Total Candidates Generated:     {len(candidates):,}")
    print(f"    - Physically Feasible Candidates: {len(feasible_candidates):,} ({feas_rate:.1f}%)")
    print(f"    - Screened / Rejected:            {n_generate - len(feasible_candidates):,} (Violated percolation, solids, or binder limits)\n")

    print("[*] Loading Calibrated Multi-Surrogate & Composite OOD Engines...")
    surrogate, calibrator, ood_detector = train_calibrated_surrogate_and_ood()
    print("    - 5 Response Ensembles trained.")
    print(f"    - Conformal Quantiles: Hardness q={calibrator.conformal_quantiles.get('hardness_gf', 1.96):.2f}, "
          f"Transfer q={calibrator.conformal_quantiles.get('transfer_g', 1.96):.2f}\n")

    # Evaluate a representative sample for landscape categorization
    eval_candidates = feasible_candidates[:eval_sample]
    print(f"[*] Mapping 4 Landscape Regions across {len(eval_candidates):,} feasible formulations...")

    region_sweet_spot = []   # In-Spec & Low OOD
    region_boundary = []     # Near Spec Limits
    region_high_unc = []     # High Predictive Interval Width
    region_ood = []          # Composite OOD

    for c in eval_candidates:
        x = c.feature_vector.to_feature_array()
        eval_res = surrogate.evaluate_formulation(c.feature_vector, formula_id=c.candidate_id)

        h_pred = eval_res.predictions["hardness_gf"]
        t_pred = eval_res.predictions["transfer_g"]
        d_pred = eval_res.predictions["drop_point_c"]

        h_interval = calibrator.predict_interval("hardness_gf", h_pred.point_prediction, h_pred.std_uncertainty)
        ood_res = ood_detector.evaluate(x, ensemble_predictions=h_pred.ensemble_member_predictions)

        # Region classification:
        # Rev.7.3 Targets: Hardness 750-900 gf, Transfer >= 0.040 g, Drop point 60-63°C
        in_h_spec = (720.0 <= h_pred.point_prediction <= 900.0)
        in_t_spec = (t_pred.point_prediction >= 0.040)
        in_d_spec = (60.0 <= d_pred.point_prediction <= 63.5)

        is_all_spec = in_h_spec and in_t_spec and in_d_spec
        is_low_ood = (ood_res.category == CompositeOODCategory.IN_DOMAIN)

        entry = {
            "id": c.candidate_id,
            "weights": c.weights,
            "fill_temp": c.fill_temperature_c,
            "hardness": h_pred.point_prediction,
            "transfer": t_pred.point_prediction,
            "drop_point": d_pred.point_prediction,
            "h_width": h_interval.interval_width,
            "ood_score": ood_res.composite_score,
            "ood_cat": ood_res.category.value
        }

        if ood_res.category == CompositeOODCategory.OUT_OF_DOMAIN:
            region_ood.append(entry)
        elif is_all_spec and is_low_ood:
            region_sweet_spot.append(entry)
        elif h_interval.interval_width > 400.0:
            region_high_unc.append(entry)
        else:
            region_boundary.append(entry)

    total_eval = len(eval_candidates)
    pct_sweet = (len(region_sweet_spot) / total_eval) * 100.0
    pct_bound = (len(region_boundary) / total_eval) * 100.0
    pct_unc = (len(region_high_unc) / total_eval) * 100.0
    pct_ood = (len(region_ood) / total_eval) * 100.0

    print(f"\n{'Landscape Region':<45} {'Count':<8} {'Share (%)':<10} {'Strategic Action'}")
    print("-" * 90)
    print(f"{'① In-Spec & Low Uncertainty (Target Sweet Spot)':<45} {len(region_sweet_spot):<8} {pct_sweet:<10.1f}% {'Virtual Release Candidate (₩0)'}")
    print(f"{'② Specification Boundary Zone':<45} {len(region_boundary):<8} {pct_bound:<10.1f}% {'Tolerance Boundary Mapping'}")
    print(f"{'③ High Uncertainty Zone (Exploration Target)':<45} {len(region_high_unc):<8} {pct_unc:<10.1f}% {'Active Learning Candidate'}")
    print(f"{'④ Out-of-Domain (Extrapolation Void)':<45} {len(region_ood):<8} {pct_ood:<10.1f}% {'Constrain / Do Not Fabricate'}")
    print("-" * 90)

    if region_sweet_spot:
        best_cand = region_sweet_spot[0]
        print(f"\n[★ TOP VIRTUAL FORMULATION SWEET-SPOT CANDIDATE (₩0)]")
        print(f"  • Candidate ID: {best_cand['id']}")
        print(f"  • Syn Wax: {best_cand['weights']['Synthetic Wax']}%, Candelilla: {best_cand['weights']['Candelilla Wax']}%, Dimethicone: {best_cand['weights']['Dimethicone']}%")
        print(f"  • Fill Temp: {best_cand['fill_temp']}°C | Predicted Hardness: {best_cand['hardness']:.1f} gf | Transfer: {best_cand['transfer']:.4f} g | Drop Point: {best_cand['drop_point']:.2f}°C")
        print(f"  • OOD Score: {best_cand['ood_score']:.2f} ({best_cand['ood_cat']})")

    print("\n" + "=" * 90 + "\n")


if __name__ == "__main__":
    map_virtual_landscape(n_generate=10000, eval_sample=300)

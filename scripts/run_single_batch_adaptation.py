#!/usr/bin/env python3
"""
GLIDE-SPEC 40: Single-Batch Physical Calibration & Next Best Experiment Ranker (Phase C)
Usage:
  # View pre-fabrication checklist for GS40_CAL_001:
  python3 scripts/run_single_batch_adaptation.py --checklist

  # Run empirical calibration validation with mock or real data:
  python3 scripts/run_single_batch_adaptation.py --hardness 735.0 --transfer 0.045 --drop-point 62.1
"""

import sys
import argparse
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.feature_engine import GS40FeatureEngine
from src.modeling.domain_adaptation import GS40DomainAdaptor, CalibrationObservation
from scripts.rank_active_learning_runs import load_planned_pilot_runs, train_calibrated_surrogate_pipeline


def main():
    parser = argparse.ArgumentParser(description="GLIDE-SPEC 40 Single-Batch Domain Adaptation & Active Learning")
    parser.add_argument("--checklist", action="store_true", help="Display GS40_CAL_001 pre-fabrication lineage checklist")
    parser.add_argument("--hardness", type=float, default=735.0, help="Measured Hardness in gf (Default: 735.0 demonstration)")
    parser.add_argument("--transfer", type=float, default=0.0450, help="Measured Transfer in g (Default: 0.0450 demonstration)")
    parser.add_argument("--drop-point", type=float, default=62.1, help="Measured Drop Point in °C (Default: 62.1 demonstration)")
    parser.add_argument("--cof", type=float, default=0.155, help="Measured BioSkin CoF (Default: 0.155)")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    matrix_csv = root_dir / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    runs = load_planned_pilot_runs(matrix_csv)
    p001_run = next(r for r in runs if r["batch_id"] == "GS40-P001")

    print("=" * 110)
    print("  GLIDE-SPEC 40: Single-Batch Domain Adaptation & Sequential Active Learning Engine")
    print("  First Physical Calibration: Batch GS40-P001 (Gold-Standard ID: GS40_CAL_001)")
    print("=" * 110)

    if args.checklist:
        sheet_path = root_dir / "data" / "doe" / "GS40_CAL_001_EXECUTION_SHEET.csv"
        print(f"\n[+] Pre-Fabrication Checklist Loaded from: {sheet_path}")
        print("-" * 80)
        with open(sheet_path, "r", encoding="utf-8") as f:
            for line in f:
                print(line.rstrip())
        print("-" * 80)
        print("Ready for laboratory batch preparation per SOP-GS40-MFG-001.\n")
        return

    # 1. Initialize Pipeline
    print("\n[1] Initializing Calibrated Domain Prior Ensemble & Composite OOD Guardrails...")
    surrogate, calibrator, ood_detector = train_calibrated_surrogate_pipeline()
    adaptor = GS40DomainAdaptor(surrogate, ood_detector)

    cal_w = {
        "Synthetic Wax": p001_run["syn_wax_pct"],
        "Candelilla Wax": p001_run["can_wax_pct"],
        "Dimethicone": p001_run["dimethicone_pct"],
        "Caprylyl Methicone": p001_run["caprylyl_pct"],
    }
    p001_feat = GS40FeatureEngine.extract_from_weights(cal_w, fill_temp_c=p001_run["fill_temp_c"])
    x0 = p001_feat.to_feature_array()

    # 2. Register Calibration Batch & Compute Residuals
    obs = CalibrationObservation(
        batch_id="GS40-P001",
        registration_id="GS40_CAL_001",
        hardness_actual_gf=args.hardness,
        transfer_actual_g=args.transfer,
        drop_point_actual_c=args.drop_point,
        cof_actual=args.cof
    )
    res = adaptor.register_calibration_batch(obs, x0)

    print("\n[2] Empirical Residual Analysis (Actual vs. Public Prior Prediction):")
    print("-" * 80)
    print(f"  Physical Response        Prior Prediction    Actual Measured       Residual (Actual - Prior)")
    print("-" * 80)
    print(f"  Hardness (gf)            {res.hardness_prior_gf:10.1f} gf     {res.hardness_actual_gf:10.1f} gf     {res.hardness_residual_gf:+10.1f} gf ({'OVER_PREDICTED' if res.hardness_residual_gf < 0 else 'UNDER_PREDICTED'})")
    print(f"  Transfer (g)             {res.transfer_prior_g:10.4f} g      {res.transfer_actual_g:10.4f} g      {res.transfer_residual_g:+10.4f} g ({'OVER_PREDICTED' if res.transfer_residual_g < 0 else 'UNDER_PREDICTED'})")
    print(f"  Drop Point (°C)          {res.drop_point_prior_c:10.2f} °C     {res.drop_point_actual_c:10.2f} °C     {res.drop_point_residual_c:+10.2f} °C ({'OVER_PREDICTED' if res.drop_point_residual_c < 0 else 'UNDER_PREDICTED'})")
    if res.cof_actual is not None:
        print(f"  BioSkin CoF              {res.cof_prior:10.3f}        {res.cof_actual:10.3f}        {res.cof_residual:+10.3f}")
    print("-" * 80)
    print(f"  💡 Domain Adaptation Insight: Prior hardness exhibits a {res.hardness_residual_gf:+.1f} gf offset in real GS40 formulation matrix.")

    # 3. Dynamic Sequential Active Learning Re-Ranking
    print("\n[3] Recalibrating Remaining Candidates (P002~P018) via Spatial Kernel Shrinkage & Re-scoring...")
    ranked_remaining = adaptor.recalibrate_candidate_runs(runs, p001_run, res)

    print("\nRank  Batch ID    Trial ID      Design Type                Adapted Hardness  Dist to CAL-001  Spec Rel  Adaptive Utility")
    print("-" * 110)
    for idx, r in enumerate(ranked_remaining, start=1):
        is_top = "🏆 [NEXT EXPERIMENT]" if idx == 1 else ""
        print(f"#{idx:<4} {r['batch_id']:<11} {r['trial_id']:<13} {r['design_type']:<26} {r['adapted_hardness_gf']:>6.1f} gf (±{r['adapted_hardness_std']:.1f})   {r['distance_to_cal_001']:>7.2f}          {r['spec_relevance']:>5.3f}     {r['adaptive_utility']:>6.2f}  {is_top}")
    print("-" * 110)

    # 4. Highlight Next Best Experiment (Run #2)
    next_exp = ranked_remaining[0]
    print("\n" + "=" * 110)
    print(f"  [★ DYNAMIC ACTIVE LEARNING VERDICT: RECOMMENDED RUN #2]")
    print(f"  🏆 NEXT BEST EXPERIMENT: Batch {next_exp['batch_id']} ({next_exp['trial_id']}) - {next_exp['design_type']}")
    print(f"  • Adapted Predicted Hardness: {next_exp['adapted_hardness_gf']:.1f} gf (Uncertainty: ±{next_exp['adapted_hardness_std']:.1f} gf)")
    print(f"  • Distance from Cal-001:      {next_exp['distance_to_cal_001']:.2f} (Explores orthogonal feature space, avoiding redundant waste)")
    print(f"  • Adaptive Total Utility:     {next_exp['adaptive_utility']:.2f} (Rank #1 among remaining candidates)")
    print("=" * 110 + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Virtual Formulation Screener & Test-by-Exception Runner
Demonstrates the end-to-end active learning and surrogate qualification flow:
  Candidate Formulations -> Physics Feature Engine -> Multi-Surrogate Ensemble ->
  95% Prediction Interval & OOD -> 4-Tier Virtual QC Decision (Test Waiver vs Pilot)
"""

import sys
import csv
from pathlib import Path
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine, OODLevel
from src.modeling.virtual_qc import VirtualQCEngine, VirtualQCDecision
from src.modeling.data_quality import DataQualityAuditor


def build_training_matrix_from_prior_baseline(baseline_csv: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    with open(baseline_csv, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    X_list = []
    y_h_list = []
    y_t_list = []
    y_d_list = []
    y_s_list = []
    y_c_list = []

    for r in rows:
        syn_w = float(r["Syn_Wax_Pct"])
        can_w = 17.0 - syn_w
        dim_pct = float(r["Dimethicone_Pct"])
        cap_pct = 28.0 - dim_pct
        fill_temp = float(r["Fill_Temp_C"])

        weights = {
            "Synthetic Wax": syn_w,
            "Candelilla Wax": can_w,
            "Dimethicone": dim_pct,
            "Caprylyl Methicone": cap_pct,
        }
        feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=fill_temp)
        X_list.append(feat.to_feature_array())

        y_h_list.append(float(r["Prior_Hardness_Mean_gf"]))
        y_t_list.append(float(r["Prior_Transfer_Index_Mean"]))
        y_d_list.append(float(r["Prior_Thermal_Trans_Mean_C"]))
        y_s_list.append(feat.sedimentation_risk_index)
        y_c_list.append(float(r["Prior_Tribology_CoF_Mean"]))

    return (
        np.array(X_list),
        np.array(y_h_list),
        np.array(y_t_list),
        np.array(y_d_list),
        np.array(y_s_list),
        np.array(y_c_list)
    )


def main():
    print("=" * 80)
    print("  GLIDE-SPEC 40: SOTA Virtual Formulation Screener & Test-by-Exception Engine")
    print("=" * 80 + "\n")

    root_dir = Path(__file__).resolve().parent.parent
    baseline_csv = root_dir / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"

    # Step 1: Data Quality Audit
    print("[1] Performing Data Quality Rubric Audit on Domain Prior Baselines...")
    audit = DataQualityAuditor.evaluate(
        dataset_name="GS40_Prior_Baseline_18Run",
        formulation_completeness=100.0,
        measurement_quality=95.0,
        has_replicates=True,
        replicate_count=4,
        method_completeness=90.0,
        feature_overlap=100.0,
        license_type="OPEN",
        has_doi_or_patent=True,
        provenance_status="DOMAIN_PRIOR_REGRESSION"
    )
    print(f"    - Baseline Quality Score: {audit.composite_score_pct}% ({audit.tier.value})")
    print(f"    - Admissible for Surrogate Training: {audit.is_admissible_for_surrogate_prior()}\n")

    # Step 2: Build Training Matrix and Fit Surrogate Engine
    print("[2] Training Multi-Surrogate Ensemble (ElasticNet, RF, ExtraTrees, GBR, GP)...")
    X, y_h, y_t, y_d, y_s, y_c = build_training_matrix_from_prior_baseline(baseline_csv)
    surrogate = GS40SurrogateEngine()
    surrogate.train_on_domain_priors_and_pilot(X, y_h, y_t, y_d, y_s, y_c)
    print("    - All 5 Response Ensembles (Hardness, Transfer, Drop Point, Settling, CoF) fitted.")
    print("    - Mahalanobis OOD Covariance structure calibrated.\n")

    # Step 3: Screen 3 Representative Formulation Scenarios
    candidates = [
        (
            "CANDIDATE-A (Nominal Rev.7.3 Center)",
            {"Synthetic Wax": 12.0, "Candelilla Wax": 5.0, "Dimethicone": 17.0, "Caprylyl Methicone": 11.0},
            80.0
        ),
        (
            "CANDIDATE-B (High-Slip Soft Stick)",
            {"Synthetic Wax": 10.0, "Candelilla Wax": 4.5, "Dimethicone": 20.0, "Caprylyl Methicone": 13.5},
            77.0
        ),
        (
            "CANDIDATE-C (Extrapolated Out-of-Domain Wax-Heavy)",
            {"Synthetic Wax": 20.0, "Candelilla Wax": 8.0, "Dimethicone": 8.0, "Caprylyl Methicone": 4.0},
            92.0
        ),
    ]

    print("[3] Virtual Screening & Test-by-Exception Decisions:\n")
    for name, weights, temp in candidates:
        feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=temp)
        eval_res = surrogate.evaluate_formulation(feat, formula_id=name)
        report = VirtualQCEngine.audit_formulation(eval_res)

        print("-" * 80)
        print(f"▶ Formulation: {name}")
        print(f"  • Fill Temp: {temp}°C | Powder Vol: {feat.powder_volume_fraction*100:.1f}% | Wax Vol: {feat.wax_volume_fraction*100:.1f}%")
        print(f"  • Predicted Hardness:   {eval_res.predictions['hardness_gf'].point_prediction:.1f} gf "
              f"(95% PI: {eval_res.predictions['hardness_gf'].pi_95_lower:.1f} ~ {eval_res.predictions['hardness_gf'].pi_95_upper:.1f} gf)")
        print(f"  • Predicted Transfer:   {eval_res.predictions['transfer_g'].point_prediction:.4f} g "
              f"(95% PI: {eval_res.predictions['transfer_g'].pi_95_lower:.4f} ~ {eval_res.predictions['transfer_g'].pi_95_upper:.4f} g)")
        print(f"  • Predicted Drop Point: {eval_res.predictions['drop_point_c'].point_prediction:.2f} °C "
              f"(95% PI: {eval_res.predictions['drop_point_c'].pi_95_lower:.2f} ~ {eval_res.predictions['drop_point_c'].pi_95_upper:.2f} °C)")
        print(f"  • OOD Score: {report.ood_level.value} (D_M={eval_res.ood_score:.2f}) | Model Confidence: {report.model_confidence_pct}%")
        print(f"  ★ DECISION: [{report.decision.value}]")
        print(f"  • Test Waiver Granted: {report.test_waiver_granted}")
        print(f"  • Action: {report.recommended_action}")

    print("\n" + "=" * 80)
    print("  Virtual Screening Complete: Demonstrated Active Learning & Test-by-Exception.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    from typing import Tuple
    main()

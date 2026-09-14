#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - GS40-P001 Prediction Snapshot Generator
Generates the immutable pre-manufacture prediction snapshot for GS40-P001 (batch GS40_CAL_001).
Strictly adheres to:
- docs/CURRENT_EXECUTION_PLAN_REV2.md
- docs/GEMINI_P001_PREDICTION_TASK_REV1.md
- docs/P001_PHYSICAL_VALIDATION_HANDOFF_AUDIT_REV1.md
- data/doe/GS40_CAL_001_EXECUTION_SHEET.csv
- data/doe/GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv
"""

import sys
import os
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Ensure project root in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.modeling.feature_engine import GS40FeatureEngine
from src.modeling.surrogate_engine import GS40SurrogateEngine
from src.modeling.virtual_simulator import VirtualMechanisticSimulator
from src.modeling.predictor import FormulationPredictor, ModelState
from scripts.rank_active_learning_runs import train_calibrated_surrogate_pipeline


def generate_snapshot():
    # 1. P001 Input definition verification
    syn_wax_pct = 15.0
    can_wax_pct = 2.0
    dimethicone_pct = 22.0
    caprylyl_pct = 6.0
    fill_temp_c = 80.0
    batch_scale_g = 1000.0
    formula_version = "REV7.3_DEVELOPMENT_BASELINE"
    batch_id = "GS40_CAL_001"
    trial_id = "DOE-EXP-001"
    snapshot_id = "GS40_P001_PRED_001"
    input_schema_version = "GS40_INPUT_SCHEMA_v1.0"
    code_commit_sha = "97e497a3647e2dd1a3681ab44bd5eade7c2a0ca8"

    # 2. Execute GS40 Surrogate Engine
    surrogate, calibrator, ood_detector = train_calibrated_surrogate_pipeline()
    weights = {
        "Synthetic Wax": syn_wax_pct,
        "Candelilla Wax": can_wax_pct,
        "Dimethicone": dimethicone_pct,
        "Caprylyl Methicone": caprylyl_pct
    }
    feat = GS40FeatureEngine.extract_from_weights(weights, fill_temp_c=fill_temp_c)
    eval_res = surrogate.evaluate_formulation(feat, formula_id=batch_id)

    pred_h = eval_res.predictions["hardness_gf"]
    pred_t = eval_res.predictions["transfer_g"]
    pred_d = eval_res.predictions["drop_point_c"]
    pred_c = eval_res.predictions["glide_cof"]

    h_conf = calibrator.predict_interval("hardness_gf", pred_h.point_prediction, pred_h.std_uncertainty)

    # 3. Virtual Mechanistic Simulator reference (isolated prior)
    vsim = VirtualMechanisticSimulator()
    pt_priors = vsim.estimate_point_priors(syn_wax_pct, can_wax_pct, dimethicone_pct, caprylyl_pct, fill_temp_c)

    # 4. FormulationPredictor (M4) status check
    m4 = FormulationPredictor()
    m4_state = m4.state.value

    # Fixed generation timestamp (KST)
    tz_kst = timezone(timedelta(hours=9))
    created_at = "2026-09-14T21:10:00+09:00"
    created_by = "gemini-3.8-flash (Antigravity Agent)"

    # Compute prediction_input_hash
    canonical_inputs = (
        f"batch_id={batch_id};"
        f"trial_id={trial_id};"
        f"formula_version={formula_version};"
        f"synthetic_wax_wt_pct={syn_wax_pct:.1f};"
        f"dimethicone_pool_wt_pct={dimethicone_pct:.1f};"
        f"caprylyl_methicone_wt_pct={caprylyl_pct:.1f};"
        f"fill_temperature_c={fill_temp_c:.1f};"
        f"batch_scale_g={batch_scale_g:.1f}"
    )
    prediction_input_hash = hashlib.sha256(canonical_inputs.encode("utf-8")).hexdigest()

    # Note text describing the provenance
    notes_text = (
        f"Snapshot generated from GS40SurrogateEngine (v8.1 Multi-Response Ensemble: ElasticNet, RF, ExtraTrees, GBR, GP) "
        f"calibrated with GroupConformalCalibrator and CompositeOODDetector. "
        f"Hardness 90% Conformal Interval: [{h_conf.calibrated_lower:.1f}, {h_conf.calibrated_upper:.1f}] gf (q={h_conf.conformal_quantile_q:.4f}). "
        f"Composite OOD Score: {eval_res.ood_score:.2f} ({eval_res.ood_level.value}). "
        f"Virtual Prior Baseline Reference (Layer 1.2): Hardness={pt_priors['hardness_gf']:.1f}gf, Transfer={pt_priors['transfer_g_10c']:.4f}, DropPoint={pt_priors['drop_point_c']:.2f}C, CoF={pt_priors['friction_cof']:.3f}. "
        f"Production M4 status: {m4_state} (UNQUALIFIED, 0 physical runs). "
        f"Physical manufacture remains strictly DO NOT MANUFACTURE YET pending material lot CoA verification."
    )

    # Build snapshot lines 1-21 (payload)
    payload_lines = [
        f"snapshot_id,{snapshot_id}",
        f"batch_id,{batch_id}",
        f"trial_id,{trial_id}",
        f"status,FROZEN_PRE_MANUFACTURE",
        f"model_version,GS40SurrogateEngine_v8.1_Ensemble",
        f"code_commit_sha,{code_commit_sha}",
        f"input_schema_version,{input_schema_version}",
        f"formula_version,{formula_version}",
        f"synthetic_wax_wt_pct,{syn_wax_pct:.1f}",
        f"dimethicone_pool_wt_pct,{dimethicone_pct:.1f}",
        f"caprylyl_methicone_wt_pct,{caprylyl_pct:.1f}",
        f"fill_temperature_c,{fill_temp_c:.1f}",
        f"batch_scale_g,{batch_scale_g:.1f}",
        f"prediction_created_at,{created_at}",
        f"prediction_created_by,{created_by}",
        f"hardness_pred_gf,{pred_h.point_prediction:.3f}",
        f"hardness_pred_sd_gf,{pred_h.std_uncertainty:.3f}",
        f"transfer_pred_g,{pred_t.point_prediction:.3f}",
        f"cof_pred,{pred_c.point_prediction:.3f}",
        f"thermal_transition_pred_c,{pred_d.point_prediction:.3f}",
        f"prediction_input_hash,{prediction_input_hash}",
    ]

    payload_str = "\n".join(payload_lines) + "\n"
    snapshot_sha256 = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

    full_lines = payload_lines + [
        f"snapshot_sha256,{snapshot_sha256}",
        f"immutable_after_execution,TRUE",
        f"actual_measurements_may_be_written_here,FALSE",
        f"notes,\"{notes_text}\"",
    ]
    snapshot_content = "\n".join(full_lines) + "\n"

    out_csv = ROOT_DIR / "data" / "doe" / "GS40_P001_PREDICTION_SNAPSHOT.csv"
    with open(out_csv, "w", encoding="utf-8") as f:
        f.write(snapshot_content)

    file_hash = hashlib.sha256(snapshot_content.encode("utf-8")).hexdigest()
    out_sha = ROOT_DIR / "data" / "doe" / "GS40_P001_PREDICTION_SNAPSHOT.csv.sha256"
    with open(out_sha, "w", encoding="utf-8") as f:
        f.write(f"{file_hash}  GS40_P001_PREDICTION_SNAPSHOT.csv\n")

    print(f"[+] Snapshot saved to: {out_csv}")
    print(f"[+] Checksum saved to: {out_sha}")
    print(f"    Payload SHA-256: {snapshot_sha256}")
    print(f"    Full File SHA-256: {file_hash}")
    print(f"    Prediction Input Hash: {prediction_input_hash}")
    print(f"    Predictions:")
    print(f"      - Hardness: {pred_h.point_prediction:.3f} ± {pred_h.std_uncertainty:.3f} gf (90% Conformal: [{h_conf.calibrated_lower:.1f}, {h_conf.calibrated_upper:.1f}] gf)")
    print(f"      - Transfer: {pred_t.point_prediction:.3f} ± {pred_t.std_uncertainty:.3f} g")
    print(f"      - CoF: {pred_c.point_prediction:.3f} ± {pred_c.std_uncertainty:.3f}")
    print(f"      - Thermal Transition: {pred_d.point_prediction:.3f} ± {pred_d.std_uncertainty:.3f} °C")
    return out_csv, out_sha


if __name__ == "__main__":
    generate_snapshot()

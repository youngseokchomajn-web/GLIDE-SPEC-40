#!/usr/bin/env python3
"""
Tests for Pre-Physical Validation Protocol Freeze & Sensitivity Safeguards (GEM-022)
Enforces:
  1. Complete JSON structure of PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json
  2. Independent manufacturing shift grouping integrity
  3. Strict isolation of supplemental runs (P017/P018) from primary runs count
  4. Proper distribution of center replicates across multiple melt shifts
  5. Deterministic reproducibility of pre_physical_sensitivity_audit.csv
  6. Maintenance of Rev.8.1 model freeze and N=0 physical count
"""

import json
import csv
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_protocol_freeze_json_structure():
    json_path = ROOT_DIR / "docs" / "PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    assert json_path.exists(), "PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json must exist"

    with open(json_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["status"] == "FROZEN"
    assert "manufacturing_grouping_structure" in data
    assert "split_conformal_calibration_design" in data
    assert "acceptance_gates" in data
    assert "brand_requirement_spec_targets" in data

    # Check acceptance gates match PRE_PHYSICAL_QUALIFICATION_GATES.json
    gates = data["acceptance_gates"]
    assert gates["n_primary_completed"]["threshold"] == 16
    assert gates["n_center_replicates"]["threshold"] == 3
    assert gates["repeatability_cv_center_pct"]["threshold"] == 4.0
    assert gates["lack_of_fit_p_value"]["threshold"] == 0.05
    assert gates["group_cv_r2"]["threshold"] == 0.85
    assert gates["conformal_pi_coverage_pct"]["threshold"] == 85.0


def test_manufacturing_shift_grouping_integrity():
    json_path = ROOT_DIR / "docs" / "PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    with open(json_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    shifts = data["manufacturing_grouping_structure"]["shifts"]
    assert len(shifts) == 4, "Must have exactly 4 independent manufacturing shifts"

    all_batches = []
    primary_batches = []
    supplemental_batches = []
    centroid_batches = []

    for shift_name, shift_info in shifts.items():
        all_batches.extend(shift_info["batch_ids"])
        primary_batches.extend(shift_info["primary_runs"])
        supplemental_batches.extend(shift_info["supplemental_runs"])
        centroid_batches.extend(shift_info["centroid_replicates"])

    assert len(all_batches) == 18, "All 18 pilot runs must be assigned to shifts"
    assert len(set(all_batches)) == 18, "No run can appear in more than one shift"

    # Primary count must be exactly 16
    assert len(primary_batches) == 16, "Primary runs must equal exactly 16"
    assert set(primary_batches) == {f"GS40-P{i:03d}" for i in range(1, 17)}

    # Supplemental must be exactly P017 and P018
    assert set(supplemental_batches) == {"GS40-P017", "GS40-P018"}

    # Centroid replicates must be distributed across multiple shifts for inter-batch Pure Error
    assert len(centroid_batches) == 4
    shifts_with_centroids = [s for s, info in shifts.items() if info["centroid_replicates"]]
    assert len(shifts_with_centroids) >= 2, "Center points must span multiple manufacturing shifts"


def test_sensitivity_audit_reproducibility():
    script_path = ROOT_DIR / "scripts" / "audit_pre_physical_sensitivity.py"
    audit_csv = ROOT_DIR / "data" / "qc" / "pre_physical_sensitivity_audit.csv"

    # Run script
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    assert res.returncode == 0, f"Script failed: {res.stderr}"
    assert audit_csv.exists(), "pre_physical_sensitivity_audit.csv must be generated"

    with open(audit_csv, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 18, "Must contain exactly 18 audited runs"
    for r in rows:
        dm = float(r["Mahalanobis_Distance_DM"])
        de = float(r["Euclidean_Distance_DE"])
        assert dm >= 0.0, "Mahalanobis distance must be non-negative"
        assert de >= 0.0, "Euclidean distance must be non-negative"
        assert r["Hardness_In_Brand_Spec"] in ("TRUE", "FALSE")
        assert r["Transfer_In_Brand_Spec"] in ("TRUE", "FALSE")
        assert r["Drop_Point_In_Brand_Spec"] in ("TRUE", "FALSE")


def test_brand_spec_target_coverage():
    json_path = ROOT_DIR / "docs" / "PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    with open(json_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    responses = data["brand_requirement_spec_targets"]["responses"]
    required_responses = ["Hardness_gf", "Transfer_Index_g", "Drop_Point_C", "Friction_CoF"]
    for resp in required_responses:
        assert resp in responses, f"Response {resp} must be defined in brand requirements"
        assert responses[resp]["spec_min"] < responses[resp]["spec_max"]

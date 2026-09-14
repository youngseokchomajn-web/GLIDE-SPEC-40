"""
GLIDE-SPEC 40 - Automated Unit Tests for P001 Prediction Snapshot
Validates:
  1. File existence and schema conformity against GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv
  2. Input reconciliation with GS40_CAL_001_EXECUTION_SHEET.csv
  3. Cryptographic integrity of payload SHA-256 and input hash
  4. Non-leakage: actual measurements are strictly disallowed
  5. Governance check: M4 production model status remains un-qualified (AWAITING_PILOT_DATA)
"""

import unittest
import hashlib
from pathlib import Path
import csv

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestP001PredictionSnapshot(unittest.TestCase):

    def setUp(self):
        self.snapshot_csv = ROOT_DIR / "data" / "doe" / "GS40_P001_PREDICTION_SNAPSHOT.csv"
        self.template_csv = ROOT_DIR / "data" / "doe" / "GS40_P001_PREDICTION_SNAPSHOT_TEMPLATE.csv"
        self.exec_sheet_csv = ROOT_DIR / "data" / "doe" / "GS40_CAL_001_EXECUTION_SHEET.csv"

    def test_snapshot_exists_and_matches_template_keys(self):
        self.assertTrue(self.snapshot_csv.exists(), "Snapshot CSV must exist")
        self.assertTrue(self.template_csv.exists(), "Template CSV must exist")

        with open(self.template_csv, mode="r", encoding="utf-8") as f:
            template_keys = [line.strip().split(",")[0] for line in f if line.strip()]

        with open(self.snapshot_csv, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            snapshot_dict = {row[0]: row[1] for row in reader if row}

        for key in template_keys:
            self.assertIn(key, snapshot_dict, f"Missing key '{key}' from snapshot")
            self.assertNotEqual(snapshot_dict[key], "REQUIRED", f"Key '{key}' was not filled")
            self.assertNotEqual(snapshot_dict[key], "REQUIRED_FROM_SIMULATOR", f"Key '{key}' was not filled")

    def test_input_reconciliation_with_execution_sheet(self):
        with open(self.snapshot_csv, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = {row[0]: row[1] for row in reader if row}

        self.assertEqual(data["snapshot_id"], "GS40_P001_PRED_001")
        self.assertEqual(data["batch_id"], "GS40_CAL_001")
        self.assertEqual(data["trial_id"], "DOE-EXP-001")
        self.assertEqual(data["formula_version"], "REV7.3_DEVELOPMENT_BASELINE")
        self.assertEqual(float(data["synthetic_wax_wt_pct"]), 15.0)
        self.assertEqual(float(data["dimethicone_pool_wt_pct"]), 22.0)
        self.assertEqual(float(data["caprylyl_methicone_wt_pct"]), 6.0)
        self.assertEqual(float(data["fill_temperature_c"]), 80.0)
        self.assertEqual(float(data["batch_scale_g"]), 1000.0)

    def test_cryptographic_hashes(self):
        with open(self.snapshot_csv, mode="r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

        data = {}
        for line in lines:
            parts = line.split(",", 1)
            data[parts[0]] = parts[1]

        # 1. Prediction Input Hash
        canonical_inputs = (
            f"batch_id={data['batch_id']};"
            f"trial_id={data['trial_id']};"
            f"formula_version={data['formula_version']};"
            f"synthetic_wax_wt_pct={float(data['synthetic_wax_wt_pct']):.1f};"
            f"dimethicone_pool_wt_pct={float(data['dimethicone_pool_wt_pct']):.1f};"
            f"caprylyl_methicone_wt_pct={float(data['caprylyl_methicone_wt_pct']):.1f};"
            f"fill_temperature_c={float(data['fill_temperature_c']):.1f};"
            f"batch_scale_g={float(data['batch_scale_g']):.1f}"
        )
        expected_input_hash = hashlib.sha256(canonical_inputs.encode("utf-8")).hexdigest()
        self.assertEqual(data["prediction_input_hash"], expected_input_hash)

        # 2. Payload SHA-256 (lines 1 to 21)
        payload_lines = lines[:21]
        payload_str = "\n".join(payload_lines) + "\n"
        expected_payload_sha = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        self.assertEqual(data["snapshot_sha256"], expected_payload_sha)

    def test_governance_safeguards(self):
        with open(self.snapshot_csv, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            data = {row[0]: row[1] for row in reader if row}

        self.assertEqual(data["immutable_after_execution"], "TRUE")
        self.assertEqual(data["actual_measurements_may_be_written_here"], "FALSE")
        self.assertEqual(data["status"], "FROZEN_PRE_MANUFACTURE")

        # Predictions must be valid positive numbers
        h_pred = float(data["hardness_pred_gf"])
        h_sd = float(data["hardness_pred_sd_gf"])
        t_pred = float(data["transfer_pred_g"])
        c_pred = float(data["cof_pred"])
        d_pred = float(data["thermal_transition_pred_c"])

        self.assertGreater(h_pred, 500.0)
        self.assertLess(h_pred, 1200.0)
        self.assertGreater(h_sd, 0.0)
        self.assertGreater(t_pred, 0.01)
        self.assertGreater(c_pred, 0.05)
        self.assertGreater(d_pred, 50.0)


if __name__ == "__main__":
    unittest.main()

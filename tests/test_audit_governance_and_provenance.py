"""
GLIDE-SPEC 40 - Automated Unit Tests for Rev.8.1 Governance, Provenance & Pareto Ranking
Verifies:
  1. Rev.8.1 Governance documents and N=0 physical pilot invariants.
  2. Dataset Freeze 1 audit file and independent formulation sample counts.
  3. Feature Engine v2 3-tier feasibility evaluation and Provenance tagging.
  4. Active Learning Diversity matrix and Pareto front identification.
"""

import unittest
from pathlib import Path
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

from src.modeling.feature_engine import (
    GS40FeatureEngine, FormulationFeatureVector, FeatureProvenance, FEATURE_PROVENANCE_MAP
)
from src.modeling.uncertainty_calibration import GroupConformalCalibrator
from src.modeling.composite_ood import CompositeOODDetector
from src.modeling.calibrated_acquisition import CalibratedAcquisitionEngine
from scripts.rank_active_learning_runs import (
    load_planned_pilot_runs, train_calibrated_surrogate_pipeline,
    rank_active_learning_runs, compute_diversity_matrix, find_pareto_front
)


class TestAuditGovernanceAndProvenance(unittest.TestCase):

    def test_governance_documents_and_invariants(self):
        """Verify presence of Rev.8.1 governance documentation and N=0 declaration."""
        gov_doc = ROOT_DIR / "docs" / "MODEL_GOVERNANCE.md"
        base_doc = ROOT_DIR / "docs" / "REV8.1_BASELINE.md"
        prov_doc = ROOT_DIR / "docs" / "DATA_PROVENANCE_POLICY.md"
        change_doc = ROOT_DIR / "docs" / "CHANGELOG.md"
        audit_md = ROOT_DIR / "docs" / "DATASET_INDEPENDENT_SAMPLE_AUDIT.md"
        freeze_csv = ROOT_DIR / "data" / "DATASET_FREEZE_1.csv"

        for p in [gov_doc, base_doc, prov_doc, change_doc, audit_md, freeze_csv]:
            self.assertTrue(p.exists(), f"Missing required governance file: {p}")

        # Check N = 0 invariant in MODEL_GOVERNANCE.md
        content = gov_doc.read_text(encoding="utf-8")
        self.assertIn("N = 0", content, "MODEL_GOVERNANCE.md must explicitly declare physical GS40 N=0")
        self.assertIn("VIRTUAL_PASS", content, "MODEL_GOVERNANCE.md must document VIRTUAL_PASS scope")
        self.assertIn("Test Waiver Candidate", content)

    def test_dataset_freeze_1_structure(self):
        """Verify DATASET_FREEZE_1 contains 8 audited datasets with independent formulation counts."""
        freeze_csv = ROOT_DIR / "data" / "DATASET_FREEZE_1.csv"
        df = pd.read_csv(freeze_csv)

        self.assertEqual(len(df), 8)
        self.assertIn("dataset_key", df.columns)
        self.assertIn("unique_formulations_count", df.columns)
        self.assertIn("provenance", df.columns)

        # Verify Huynh dataset separates raw rows from unique formulations
        huynh_row = df[df["dataset_key"] == "DS01_LIPSTICK_384"].iloc[0]
        self.assertGreater(huynh_row["temperature_scan_count"], 1)
        self.assertGreater(huynh_row["aging_timepoints_count"], 1)

    def test_feature_engine_v2_provenance_and_feasibility(self):
        """Verify FeatureProvenance tagging and 3-tier feasibility evaluation."""
        feature_names = FormulationFeatureVector.feature_names()
        self.assertEqual(len(feature_names), 30)

        # Every feature must have a defined provenance
        for fn in feature_names:
            self.assertIn(fn, FEATURE_PROVENANCE_MAP, f"Feature {fn} missing provenance tag")
            self.assertIsInstance(FEATURE_PROVENANCE_MAP[fn], FeatureProvenance)

        # Test 3-Tier Feasibility on standard Rev.7.3 formulation
        valid_weights = {
            "Synthetic Wax": 12.0, "Candelilla Wax": 5.0, "PEG-8 Beeswax": 0.0,
            "Dimethicone": 17.0, "Caprylyl Methicone": 9.0, "MQ Resin Solution": 2.0,
            "C12-15 Alkyl Benzoate": 26.0, "Active / Preservative": 1.0,
            "Porous Silica": 10.0, "Silica Dimethyl Silylate": 2.0, "PMSSQ": 8.0,
            "Boron Nitride": 3.0, "Zinc Oxide": 5.0
        }
        feat_valid = GS40FeatureEngine.extract_from_weights(valid_weights, fill_temp_c=80.0)
        is_feas, rejections = feat_valid.evaluate_3tier_feasibility()
        self.assertTrue(is_feas, f"Valid formulation rejected: {rejections}")

        # Test invalid: Fumed silica below percolation threshold (1.0% < 1.5%)
        invalid_weights = dict(valid_weights)
        invalid_weights["Silica Dimethyl Silylate"] = 1.0
        invalid_weights["Porous Silica"] = 11.0  # keep powder sum 28%
        feat_invalid = GS40FeatureEngine.extract_from_weights(invalid_weights, fill_temp_c=80.0)
        is_feas_inv, rejections_inv = feat_invalid.evaluate_3tier_feasibility()
        self.assertFalse(is_feas_inv)
        self.assertTrue(any("percolation" in r for r in rejections_inv))

    def test_pareto_front_and_diversity(self):
        """Verify Active Learning Pareto front and information diversity calculation."""
        matrix_csv = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
        runs = load_planned_pilot_runs(matrix_csv)
        surrogate, calibrator, ood_detector = train_calibrated_surrogate_pipeline()

        ranked = rank_active_learning_runs(runs, surrogate, calibrator, ood_detector)
        self.assertEqual(len(ranked), 18)

        # Check diversity distance matrix
        df_dist = compute_diversity_matrix(ranked)
        # P001 and P004 explore opposite vertices -> large distance
        dist_p1_p4 = df_dist.loc["GS40-P001", "GS40-P004"]
        dist_p4_p11 = df_dist.loc["GS40-P004", "GS40-P011"]
        self.assertGreater(dist_p1_p4, dist_p4_p11, "P001 and P004 must be more orthogonal than P004 and P011")

        # Check Pareto Front contains P001
        pareto_runs = find_pareto_front(ranked)
        pareto_ids = [r[0]["batch_id"] for r in pareto_runs]
        self.assertIn("GS40-P001", pareto_ids, "GS40-P001 must be on the non-dominated Pareto front")


if __name__ == "__main__":
    unittest.main()

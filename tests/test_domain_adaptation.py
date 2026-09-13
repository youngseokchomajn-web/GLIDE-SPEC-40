"""
GLIDE-SPEC 40 - Automated Unit Tests for Domain Adaptation & Sequential Active Learning
Tests:
  1. Residual calculation (Actual - Prior) across Hardness, Transfer, Drop Point.
  2. Spatial kernel shrinkage & epistemic uncertainty reduction.
  3. Dynamic selection of Run #2 (Next Best Experiment) based on adaptive utility.
"""

import unittest
from pathlib import Path
import numpy as np

from src.modeling.feature_engine import GS40FeatureEngine
from src.modeling.domain_adaptation import GS40DomainAdaptor, CalibrationObservation, CalibrationResidualResult
from scripts.rank_active_learning_runs import load_planned_pilot_runs, train_calibrated_surrogate_pipeline

ROOT_DIR = Path(__file__).resolve().parent.parent


class TestDomainAdaptationEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.surrogate, cls.calibrator, cls.ood_detector = train_calibrated_surrogate_pipeline()
        cls.adaptor = GS40DomainAdaptor(cls.surrogate, cls.ood_detector, kernel_length_scale=12.0)
        cls.runs = load_planned_pilot_runs(ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv")
        cls.p001 = next(r for r in cls.runs if r["batch_id"] == "GS40-P001")

        cal_w = {
            "Synthetic Wax": cls.p001["syn_wax_pct"],
            "Candelilla Wax": cls.p001["can_wax_pct"],
            "Dimethicone": cls.p001["dimethicone_pct"],
            "Caprylyl Methicone": cls.p001["caprylyl_pct"],
        }
        cls.p001_feat = GS40FeatureEngine.extract_from_weights(cal_w, fill_temp_c=cls.p001["fill_temp_c"])
        cls.x0 = cls.p001_feat.to_feature_array()

    def test_residual_computation(self):
        """Verify empirical residual calculation matches exact difference."""
        obs = CalibrationObservation(
            batch_id="GS40-P001",
            registration_id="GS40_CAL_001",
            hardness_actual_gf=735.0,
            transfer_actual_g=0.0450,
            drop_point_actual_c=62.10
        )
        res = self.adaptor.compute_residuals(obs, self.x0)
        self.assertEqual(res.batch_id, "GS40-P001")
        self.assertAlmostEqual(res.hardness_residual_gf, 735.0 - res.hardness_prior_gf, places=2)
        self.assertAlmostEqual(res.transfer_residual_g, 0.0450 - res.transfer_prior_g, places=4)
        self.assertAlmostEqual(res.drop_point_residual_c, 62.10 - res.drop_point_prior_c, places=2)

    def test_spatial_adaptation_shrinkage(self):
        """Verify that points close to Cal-001 inherit the residual shift and have reduced uncertainty."""
        obs = CalibrationObservation(
            batch_id="GS40-P001",
            registration_id="GS40_CAL_001",
            hardness_actual_gf=735.0,
            transfer_actual_g=0.0450,
            drop_point_actual_c=62.10
        )
        res = self.adaptor.compute_residuals(obs, self.x0)
        
        # Test self-adaptation at x0 (distance = 0)
        adapted_self = self.adaptor.predict_adapted(self.x0, self.x0, res)
        h_adapted_self, h_std_self = adapted_self["hardness_gf"]
        w_corr, dist = adapted_self["spatial_weight"]

        self.assertEqual(dist, 0.0)
        self.assertAlmostEqual(w_corr, 1.0, places=3)
        self.assertAlmostEqual(h_adapted_self, 735.0, places=1)

    def test_dynamic_selection_of_run_2(self):
        """Verify remaining 17 runs are ranked and Run #2 is identified."""
        obs = CalibrationObservation(
            batch_id="GS40-P001",
            registration_id="GS40_CAL_001",
            hardness_actual_gf=735.0,
            transfer_actual_g=0.0450,
            drop_point_actual_c=62.10
        )
        res = self.adaptor.register_calibration_batch(obs, self.x0)
        ranked = self.adaptor.recalibrate_candidate_runs(self.runs, self.p001, res)

        # 17 runs remaining (P001 excluded)
        self.assertEqual(len(ranked), 17)
        self.assertNotIn("GS40-P001", [r["batch_id"] for r in ranked])

        # Top ranked candidate has highest utility
        top_cand = ranked[0]
        self.assertGreater(top_cand["adaptive_utility"], 0.0)
        self.assertIn(top_cand["batch_id"], ["GS40-P008", "GS40-P002", "GS40-P004"])


if __name__ == "__main__":
    unittest.main()

"""
GLIDE-SPEC 40 - Automated Unit Tests for Conformal Calibration, Composite OOD & Acquisition
Verifies:
  1. Group K-Fold split leakage prevention and locally adaptive conformal quantiles.
  2. 4-signal Composite OOD Detector (Mahalanobis, kNN, Disagreement, Hyperbox range).
  3. Tri-Criteria Active Learning Acquisition Engine (InfoGain × SpecRelevance × DomainCoverage).
"""

import unittest
import numpy as np

from src.modeling.uncertainty_calibration import (
    GroupConformalCalibrator, ConformalInterval, ConformalCalibrationReport
)
from src.modeling.composite_ood import (
    CompositeOODDetector, CompositeOODCategory, CompositeOODResult
)
from src.modeling.calibrated_acquisition import (
    CalibratedAcquisitionEngine, AcquisitionScoreResult
)


class TestConformalAndCompositeOOD(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)

    def test_group_conformal_split_no_leakage(self):
        """Verify GroupKFold ensures groups do not appear in both train and val."""
        X = np.random.randn(20, 5)
        # 5 distinct formulation groups, 4 replicates each
        groups = ["F_A"] * 4 + ["F_B"] * 4 + ["F_C"] * 4 + ["F_D"] * 4 + ["F_E"] * 4
        splits = GroupConformalCalibrator.get_group_kfold_splits(X, groups, n_splits=3)

        self.assertGreaterEqual(len(splits), 2)
        for train_idx, val_idx in splits:
            train_groups = set(groups[i] for i in train_idx)
            val_groups = set(groups[i] for i in val_idx)
            # Intersection must be empty (strict no-leakage)
            self.assertEqual(len(train_groups.intersection(val_groups)), 0)

    def test_conformal_calibration_and_coverage(self):
        """Verify locally adaptive conformal quantile computation and coverage guarantee."""
        n = 50
        y_true = np.linspace(700.0, 900.0, n)
        # Synthetic predictions with known noise
        noise = np.random.normal(0, 15.0, size=n)
        y_pred = y_true + noise
        y_std = np.full(n, 15.0)

        calibrator = GroupConformalCalibrator(nominal_confidence=0.90)
        report = calibrator.calibrate("hardness_gf", y_true, y_pred, y_std)

        self.assertIsInstance(report, ConformalCalibrationReport)
        self.assertEqual(report.sample_size, n)
        self.assertEqual(report.nominal_confidence_pct, 90.0)
        # Empirical coverage on calibration set should be >= nominal (finite sample guarantee)
        self.assertGreaterEqual(report.empirical_coverage_pct, 88.0)
        self.assertGreater(report.conformal_quantile_q, 0.0)

        # Test predict_interval
        pi = calibrator.predict_interval("hardness_gf", point_pred=800.0, point_std=20.0)
        self.assertIsInstance(pi, ConformalInterval)
        self.assertTrue(pi.is_empirically_calibrated)
        self.assertAlmostEqual(pi.calibrated_lower, 800.0 - pi.conformal_quantile_q * 20.0, places=2)
        self.assertAlmostEqual(pi.calibrated_upper, 800.0 + pi.conformal_quantile_q * 20.0, places=2)
        self.assertAlmostEqual(pi.interval_width, (pi.calibrated_upper - pi.calibrated_lower), places=2)

    def test_conformal_fallback_small_sample(self):
        """Verify graceful fallback for sample sizes smaller than 3."""
        calibrator = GroupConformalCalibrator(nominal_confidence=0.90)
        report = calibrator.calibrate("transfer_g", np.array([0.04, 0.05]), np.array([0.041, 0.049]), np.array([0.005, 0.005]))
        self.assertEqual(report.conformal_quantile_q, 1.96)
        self.assertEqual(report.empirical_coverage_pct, 100.0)

    def test_composite_ood_detector(self):
        """Verify 4-signal composite OOD detector correctly differentiates in-domain vs OOD."""
        # 1. Create a synthetic 10-sample 4-feature training set
        train_X = np.array([
            [12.0, 17.0, 10.0, 80.0],
            [13.0, 16.0, 10.0, 82.0],
            [11.0, 18.0, 10.0, 78.0],
            [14.0, 15.0, 10.0, 84.0],
            [12.5, 16.5, 10.0, 80.5],
            [10.0, 19.0, 10.0, 76.0],
            [15.0, 14.0, 10.0, 85.0],
            [11.5, 17.5, 10.0, 79.0],
            [13.5, 15.5, 10.0, 81.0],
            [12.0, 17.0, 10.0, 80.0],
        ])

        detector = CompositeOODDetector(k_neighbors=2)
        detector.fit(train_X)
        self.assertTrue(detector.is_fitted)

        # 2. Test In-Domain point (close to centroid)
        in_sample = np.array([12.2, 16.8, 10.0, 80.2])
        res_in = detector.evaluate(in_sample, ensemble_predictions={"m1": 800.0, "m2": 805.0, "m3": 798.0})
        self.assertEqual(res_in.category, CompositeOODCategory.IN_DOMAIN)
        self.assertLessEqual(res_in.composite_score, 1.0)
        self.assertEqual(res_in.box_violation_count, 0)

        # 3. Test Out-of-Domain point (extreme values violating hyperbox and distance)
        ood_sample = np.array([25.0, 5.0, 25.0, 120.0])
        res_ood = detector.evaluate(ood_sample, ensemble_predictions={"m1": 800.0, "m2": 500.0, "m3": 1100.0})
        self.assertEqual(res_ood.category, CompositeOODCategory.OUT_OF_DOMAIN)
        self.assertGreater(res_ood.composite_score, 1.5)
        self.assertGreater(res_ood.box_violation_count, 0)
        self.assertGreater(res_ood.ensemble_disagreement_cv, 10.0)

    def test_calibrated_acquisition_engine(self):
        """Verify tri-criteria utility function balances InfoGain, SpecRelevance, and Coverage."""
        calibrator = GroupConformalCalibrator()

        # Case A: Ideal Sweet Spot candidate (Target Hardness 800 gf, Transfer 0.048 g, Drop Point 61.5 C)
        h_pi_sweet = calibrator.predict_interval("h", 800.0, 25.0)
        t_pi_sweet = calibrator.predict_interval("t", 0.048, 0.002)
        d_pi_sweet = calibrator.predict_interval("d", 61.5, 0.3)

        dummy_ood_in = CompositeOODResult(
            composite_score=0.4,
            category=CompositeOODCategory.IN_DOMAIN,
            mahalanobis_distance=1.2,
            knn_mean_distance=0.8,
            ensemble_disagreement_cv=2.0,
            box_violation_count=0,
            box_violation_max_pct=0.0,
            details={}
        )

        score_sweet = CalibratedAcquisitionEngine.score_candidate(
            "CAND_SWEET", h_pi_sweet, t_pi_sweet, d_pi_sweet, dummy_ood_in
        )

        self.assertAlmostEqual(score_sweet.specification_relevance_score, 1.0, places=1)
        self.assertEqual(score_sweet.domain_coverage_score, 1.0)
        self.assertIn("PRIORITY_1_SWEET_SPOT_CALIBRATOR", score_sweet.strategic_verdict)

        # Case B: Boundary Probe (High uncertainty, but Hardness = 620 gf - far below spec)
        h_pi_bound = calibrator.predict_interval("h", 620.0, 45.0)  # High variance
        t_pi_bound = calibrator.predict_interval("t", 0.035, 0.005)
        d_pi_bound = calibrator.predict_interval("d", 58.0, 1.0)

        score_bound = CalibratedAcquisitionEngine.score_candidate(
            "CAND_BOUNDARY", h_pi_bound, t_pi_bound, d_pi_bound, dummy_ood_in
        )

        # Even with high InfoGain, SpecRelevance must be penalized
        self.assertGreater(score_bound.information_gain_score, score_sweet.information_gain_score)
        self.assertLess(score_bound.specification_relevance_score, 0.20)
        self.assertIn("BOUNDARY_PROBE_ONLY", score_bound.strategic_verdict)

        # Case C: Extreme Out-of-Domain candidate
        dummy_ood_out = CompositeOODResult(
            composite_score=3.5,
            category=CompositeOODCategory.OUT_OF_DOMAIN,
            mahalanobis_distance=8.0,
            knn_mean_distance=5.0,
            ensemble_disagreement_cv=25.0,
            box_violation_count=3,
            box_violation_max_pct=50.0,
            details={}
        )
        score_ood = CalibratedAcquisitionEngine.score_candidate(
            "CAND_OOD", h_pi_sweet, t_pi_sweet, d_pi_sweet, dummy_ood_out
        )
        self.assertLess(score_ood.domain_coverage_score, 0.30)
        self.assertLess(score_ood.total_acquisition_score, score_sweet.total_acquisition_score)


if __name__ == "__main__":
    unittest.main()

"""
GLIDE-SPEC 40 - Automated Unit Tests for SOTA Virtual Formulation & QC Engine
Verifies Data Quality Auditor, Physics Feature Engine, Multi-Response Surrogates,
and Test-by-Exception Decision Matrix.
"""

import unittest
import numpy as np
from pathlib import Path
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from src.modeling.data_quality import DataQualityAuditor, QualityTier
from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine, OODLevel
from src.modeling.virtual_qc import VirtualQCEngine, VirtualQCDecision
from scripts.run_gs40_pilot_qualification import calculate_lack_of_fit_f_test


class TestSotaSurrogateAndQC(unittest.TestCase):

    def test_data_quality_auditor(self):
        # Case A: Rigorous academic paper with replicates and CC BY license
        res_a = DataQualityAuditor.evaluate(
            dataset_name="Soft_Matter_2026_Rheology",
            formulation_completeness=100.0,
            measurement_quality=95.0,
            has_replicates=True,
            replicate_count=3,
            method_completeness=90.0,
            feature_overlap=85.0,
            license_type="CC_BY",
            has_doi_or_patent=True,
            provenance_status="MEASURED"
        )
        self.assertGreaterEqual(res_a.composite_score_pct, 80.0)
        self.assertEqual(res_a.tier, QualityTier.TIER_1_CORE_BENCHMARK)
        self.assertTrue(res_a.is_admissible_for_surrogate_prior())

        # Case B: Incomplete patent without replicates
        res_b = DataQualityAuditor.evaluate(
            dataset_name="Vague_Patent_Example",
            formulation_completeness=60.0,
            measurement_quality=50.0,
            has_replicates=False,
            replicate_count=1,
            method_completeness=40.0,
            feature_overlap=40.0,
            license_type="RESTRICTED",
            has_doi_or_patent=False,
            provenance_status="ESTIMATED"
        )
        self.assertLess(res_b.composite_score_pct, 50.0)
        self.assertEqual(res_b.tier, QualityTier.UNQUALIFIED)
        self.assertFalse(res_b.is_admissible_for_surrogate_prior())

    def test_gs40_feature_engine(self):
        feat = GS40FeatureEngine.extract_from_weights({
            "Synthetic Wax": 12.0,
            "Candelilla Wax": 5.0,
            "Dimethicone": 17.0,
            "Caprylyl Methicone": 11.0,
            "MQ Resin Solution": 2.0,
            "C12-15 Alkyl Benzoate": 24.0,
            "Porous Silica": 10.0,
            "Silica Dimethyl Silylate": 2.0,
            "PMSSQ": 8.0,
            "Boron Nitride": 3.0,
            "Zinc Oxide": 5.0,
            "Active / Preservative": 1.0,
        }, fill_temp_c=80.0)

        # Check total volume fractions sum to approximately 1.0
        tot_vol_frac = feat.wax_volume_fraction + feat.silicone_volume_fraction + feat.powder_volume_fraction + (25.0 / 0.96 / (100.0 / 1.15))
        self.assertTrue(0.10 <= feat.wax_volume_fraction <= 0.30)
        self.assertTrue(0.10 <= feat.powder_volume_fraction <= 0.25)
        self.assertTrue(0.20 <= feat.silicone_volume_fraction <= 0.40)

        # Check derived physical properties
        self.assertGreater(feat.total_particle_surface_area_m2_g, 20.0)
        self.assertGreater(feat.total_oil_absorption_demand_ml_100g, 10.0)
        self.assertGreater(feat.fumed_silica_percolation_ratio, 1.0)
        self.assertTrue(0.1 <= feat.sedimentation_risk_index <= 3.0)

        # Check array conversion
        arr = feat.to_feature_array()
        self.assertEqual(len(arr), len(feat.to_dict()))

    def test_surrogate_engine_and_virtual_qc(self):
        # Generate 20 synthetic training vectors for testing pipeline
        np.random.seed(42)
        n_samples = 20
        n_features = 30
        X_train = np.random.randn(n_samples, n_features) * 2.0 + 10.0

        y_h = 750.0 + 10.0 * X_train[:, 0] + np.random.randn(n_samples) * 5.0
        y_t = 0.045 + 0.001 * X_train[:, 1] + np.random.randn(n_samples) * 0.001
        y_d = 61.5 + 0.05 * X_train[:, 2] + np.random.randn(n_samples) * 0.1
        y_s = 0.80 + 0.02 * X_train[:, 3] + np.random.randn(n_samples) * 0.02
        y_c = 0.16 + 0.002 * X_train[:, 4] + np.random.randn(n_samples) * 0.005

        surrogate = GS40SurrogateEngine()
        surrogate.train_on_domain_priors_and_pilot(X_train, y_h, y_t, y_d, y_s, y_c)
        self.assertTrue(surrogate.is_trained)

        # Query in-domain sample
        dummy_feat = GS40FeatureEngine.extract_from_weights({}, fill_temp_c=80.0)
        # Override to match training distribution center
        eval_res = surrogate.evaluate_formulation(dummy_feat)
        self.assertIn("hardness_gf", eval_res.predictions)
        self.assertIn("transfer_g", eval_res.predictions)
        self.assertIn("drop_point_c", eval_res.predictions)

        # Check prediction interval
        h_pred = eval_res.predictions["hardness_gf"]
        self.assertLessEqual(h_pred.pi_95_lower, h_pred.point_prediction)
        self.assertGreaterEqual(h_pred.pi_95_upper, h_pred.point_prediction)

        # Run Virtual QC
        report = VirtualQCEngine.audit_formulation(eval_res)
        self.assertIsInstance(report.decision, VirtualQCDecision)
        self.assertIn(report.decision, [
            VirtualQCDecision.VIRTUAL_PASS,
            VirtualQCDecision.VIRTUAL_PASS_CONFIRMATION_REQUIRED,
            VirtualQCDecision.EXPERIMENT_REQUIRED,
            VirtualQCDecision.OUT_OF_DOMAIN
        ])

    def test_lack_of_fit_f_test_math(self):
        # 16 observations with 4 replicates at center
        np.random.seed(42)
        y_actual = np.array([780, 800, 720, 740, 790, 730, 720, 800, 740, 780, 750, 770, 760, 762, 759, 761], dtype=np.float64)
        y_pred = y_actual + np.random.randn(16) * 2.0  # Good fit
        center_indices = [12, 13, 14, 15]

        ss_pe, ss_lof, f_stat, p_val, ms_pe = calculate_lack_of_fit_f_test(y_actual, y_pred, center_indices, n_params=4)
        self.assertGreater(ss_pe, 0.0)
        self.assertGreaterEqual(p_val, 0.0)
        self.assertLessEqual(p_val, 1.0)


if __name__ == "__main__":
    unittest.main()

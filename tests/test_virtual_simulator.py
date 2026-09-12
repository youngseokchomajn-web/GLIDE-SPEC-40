"""
GLIDE-SPEC 40 - Automated Tests for Layer 1.1 Virtual Mechanistic Simulator
Verifies prior estimations, provenance attribution (ENGINEERING_ASSUMPTION),
hierarchical Monte Carlo bounds, and strict firewall flags.
"""

from pathlib import Path
import unittest
import numpy as np

from src.modeling.virtual_simulator import VirtualMechanisticSimulator, VirtualSimulationResult


class TestVirtualSimulator(unittest.TestCase):

    def setUp(self):
        self.simulator = VirtualMechanisticSimulator()
        self.domain_priors_dir = Path(__file__).resolve().parent.parent / "benchmarks" / "domain_priors"

    def test_domain_prior_files_exist(self):
        fric_csv = self.domain_priors_dir / "imperial_friction" / "wax_oil_friction_data.csv"
        stick_csv = self.domain_priors_dir / "lipstick_17pct_anchor" / "lipstick_17pct_wax_benchmark.csv"
        wax_csv = self.domain_priors_dir / "tuberlin_wax_variability" / "natural_wax_batch_variability_summary.csv"
        pat_csv = self.domain_priors_dir / "anhydrous_stick_patents" / "us20070166254_anhydrous_powder_stick.csv"
        sla_csv = self.domain_priors_dir / "commercial_stick_benchmark" / "mdpi_commercial_lipbalm_texture_sla.csv"
        sili_csv = self.domain_priors_dir / "silicone_skin_tribology" / "silicone_powder_skin_tribology_benchmark.csv"

        self.assertTrue(fric_csv.exists(), "Imperial friction CSV must exist")
        self.assertTrue(stick_csv.exists(), "Lipstick 17% anchor CSV must exist")
        self.assertTrue(wax_csv.exists(), "TU Berlin wax variability CSV must exist")
        self.assertTrue(pat_csv.exists(), "Patent anhydrous stick CSV must exist")
        self.assertTrue(sla_csv.exists(), "Commercial lip balm SLA benchmark CSV must exist")
        self.assertTrue(sili_csv.exists(), "Silicone skin tribology benchmark CSV must exist")

    def test_virtual_simulator_center_point_priors(self):
        # Test center point: SynWax 12%, CanWax 5%, Dimethicone 17%, Caprylyl 11%, Fill 80C
        priors = self.simulator.estimate_point_priors(
            syn_wax_pct=12.0,
            candelilla_wax_pct=5.0,
            dimethicone_pct=17.0,
            caprylyl_pct=11.0,
            fill_temp_c=80.0
        )

        # Thermal transition should be close to Rev.7.3 target (~61.5°C)
        self.assertTrue(60.0 <= priors["thermal_transition_c"] <= 63.0)
        self.assertTrue(60.0 <= priors["drop_point_c"] <= 63.0)

        # Hardness prior should be within plausible cosmetic stick range
        self.assertTrue(650.0 <= priors["hardness_gf"] <= 900.0)

        # Transfer prior index should be around 0.04 to 0.06
        self.assertTrue(0.035 <= priors["transfer_prior_index"] <= 0.065)
        self.assertTrue(0.035 <= priors["transfer_g_10c"] <= 0.065)

        # Tribology prior index should be in low lubricious range
        self.assertTrue(0.10 <= priors["tribology_prior_index"] <= 0.20)
        self.assertTrue(0.10 <= priors["friction_cof"] <= 0.20)

    def test_virtual_simulator_monte_carlo_distribution_and_provenance(self):
        result = self.simulator.simulate(
            syn_wax_pct=12.0,
            candelilla_wax_pct=5.0,
            dimethicone_pct=17.0,
            caprylyl_pct=11.0,
            fill_temp_c=80.0,
            n_monte_carlo=500,
            random_seed=123
        )

        self.assertIsInstance(result, VirtualSimulationResult)
        # STRICT FIREWALL CHECK
        self.assertEqual(result.data_origin, "VIRTUAL_DOMAIN_PRIOR")
        self.assertFalse(result.is_empirical_gs40)
        self.assertIn("PRE-PILOT ESTIMATE", result.warning_notice)

        # Check distribution statistics
        self.assertTrue(result.predicted_hardness_prior_gf.p05 < result.predicted_hardness_prior_gf.mean < result.predicted_hardness_prior_gf.p95)
        self.assertTrue(result.predicted_transfer_prior_index.p05 < result.predicted_transfer_prior_index.mean < result.predicted_transfer_prior_index.p95)
        self.assertTrue(result.predicted_thermal_transition_c.p05 < result.predicted_thermal_transition_c.mean < result.predicted_thermal_transition_c.p95)
        self.assertTrue(result.predicted_tribology_prior_index.p05 < result.predicted_tribology_prior_index.mean < result.predicted_tribology_prior_index.p95)

        # Check backwards-compatible properties
        self.assertEqual(result.predicted_hardness_gf.mean, result.predicted_hardness_prior_gf.mean)
        self.assertEqual(result.predicted_transfer_g_10c.mean, result.predicted_transfer_prior_index.mean)
        self.assertEqual(result.predicted_drop_point_c.mean, result.predicted_thermal_transition_c.mean)
        self.assertEqual(result.predicted_friction_index.mean, result.predicted_tribology_prior_index.mean)

        # Check Provenance & Explicit Coefficient Source (ENGINEERING_ASSUMPTION)
        h_prov = result.predicted_hardness_prior_gf.provenance
        self.assertIn("ENGINEERING_ASSUMPTION", h_prov.coefficient_source)
        self.assertIn("Hardness Prior ≠ GS40 Hardness Prediction", h_prov.golden_principle_warning)

        t_prov = result.predicted_thermal_transition_c.provenance
        self.assertIn("ENGINEERING_ASSUMPTION", t_prov.coefficient_source)
        self.assertIn("Thermal Transition Prior ≠ GS40 Mettler Drop Point", t_prov.golden_principle_warning)

        trans_prov = result.predicted_transfer_prior_index.provenance
        self.assertIn("ENGINEERING_ASSUMPTION", trans_prov.coefficient_source)
        self.assertIn("Pay-off Anchor ≠ GS40 Physical Transfer (g)", trans_prov.golden_principle_warning)

        trib_prov = result.predicted_tribology_prior_index.provenance
        self.assertIn("ENGINEERING_ASSUMPTION", trib_prov.coefficient_source)
        self.assertIn("Tribology Prior Index ≠ GS40 Dynamic CoF", trib_prov.golden_principle_warning)

        # Check Hierarchical Uncertainty Breakdown
        bd = result.hierarchical_uncertainty_breakdown
        self.assertGreaterEqual(bd["level1_candelilla_raw_cv_pct"], 15.0)
        self.assertLess(bd["level2_wax_network_cv_pct"], bd["level1_candelilla_raw_cv_pct"])
        self.assertLess(bd["level3_powder_damped_cv_pct"], bd["level2_wax_network_cv_pct"])
        self.assertTrue(4.0 <= bd["composite_total_hardness_cv_pct"] <= 10.0)


if __name__ == "__main__":
    unittest.main()

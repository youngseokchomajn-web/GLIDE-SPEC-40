"""
GLIDE-SPEC 40 - Automated Tests for Layer 1.1 Virtual Mechanistic Simulator
Verifies prior estimations, provenance attribution (ENGINEERING_ASSUMPTION),
hierarchical Monte Carlo bounds, and strict firewall flags.
"""

from pathlib import Path
import csv
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
        doan_csv = self.domain_priors_dir / "wax_oleogel_hardness" / "doan2022_wax_oleogel_hardness.csv"

        self.assertTrue(fric_csv.exists(), "Imperial friction CSV must exist")
        self.assertTrue(stick_csv.exists(), "Lipstick 17% anchor CSV must exist")
        self.assertTrue(wax_csv.exists(), "TU Berlin wax variability CSV must exist")
        self.assertTrue(pat_csv.exists(), "Patent anhydrous stick CSV must exist")
        self.assertTrue(sla_csv.exists(), "Commercial lip balm SLA benchmark CSV must exist")
        self.assertTrue(sili_csv.exists(), "Silicone skin tribology benchmark CSV must exist")
        self.assertTrue(doan_csv.exists(), "Doan 2022 oleogel hardness CSV must exist")

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

        # Check Provenance & Explicit Coefficient Source (PUBLIC_EMPIRICAL_REGRESSION)
        h_prov = result.predicted_hardness_prior_gf.provenance
        self.assertIn("PUBLIC_EMPIRICAL_REGRESSION", h_prov.coefficient_source)
        self.assertIn("Hardness Prior ≠ GS40 Hardness Prediction", h_prov.golden_principle_warning)
        self.assertTrue(len(h_prov.residual_variance_stats) > 0)

        t_prov = result.predicted_thermal_transition_c.provenance
        self.assertIn("PUBLIC_EMPIRICAL_REGRESSION", t_prov.coefficient_source)
        self.assertIn("Thermal Transition Prior ≠ GS40 Mettler Drop Point", t_prov.golden_principle_warning)

        trans_prov = result.predicted_transfer_prior_index.provenance
        self.assertIn("PUBLIC_EMPIRICAL_REGRESSION", trans_prov.coefficient_source)
        self.assertIn("Pay-off Anchor ≠ GS40 Physical Transfer (g)", trans_prov.golden_principle_warning)

        trib_prov = result.predicted_tribology_prior_index.provenance
        self.assertIn("PUBLIC_EMPIRICAL_REGRESSION", trib_prov.coefficient_source)
        self.assertIn("Tribology Prior Index ≠ GS40 Dynamic CoF", trib_prov.golden_principle_warning)

        # Check Hierarchical Uncertainty Breakdown
        bd = result.hierarchical_uncertainty_breakdown
        self.assertGreaterEqual(bd["level1_candelilla_raw_cv_pct"], 15.0)
        self.assertLess(bd["level2_wax_network_cv_pct"], bd["level1_candelilla_raw_cv_pct"])
        self.assertLess(bd["level3_powder_damped_cv_pct"], bd["level2_wax_network_cv_pct"])
        self.assertIn("level4_empirical_regression_residual_cv_pct", bd)
        self.assertTrue(4.0 <= bd["composite_total_hardness_cv_pct"] <= 10.0)

    def test_virtual_prior_baseline_csv_and_comparator(self):
        root_dir = Path(__file__).resolve().parent.parent
        baseline_csv = root_dir / "data" / "doe" / "pilot_doe_virtual_prior_baseline.csv"
        matrix_csv = root_dir / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"

        self.assertTrue(baseline_csv.exists(), "pilot_doe_virtual_prior_baseline.csv must exist")

        with open(baseline_csv, mode="r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 18, "Prior baseline must contain exactly 18 runs")

        # Test comparator execution in mock mode
        from scripts.compare_pilot_vs_prior import run_comparison
        # Should execute cleanly without error
        run_comparison(matrix_csv, baseline_csv, mock_mode=True)

    def test_powder_particulate_mechanics_and_raw_materials_db(self):
        root_dir = Path(__file__).resolve().parent.parent
        powder_dir = root_dir / "benchmarks" / "domain_priors" / "powder_particulate_mechanics"
        raw_mat_csv = root_dir / "data" / "raw_materials" / "gs40_raw_material_property_db.csv"
        exec_sheet_csv = root_dir / "data" / "doe" / "pilot_process_execution_sheet_template.csv"

        # 1. Powder specs & rheology
        specs_csv = powder_dir / "powder_system_specs_and_rheology.csv"
        self.assertTrue(specs_csv.exists(), "powder_system_specs_and_rheology.csv must exist")
        with open(specs_csv, mode="r", encoding="utf-8") as f:
            specs = list(csv.DictReader(f))
        self.assertGreaterEqual(len(specs), 5)
        powder_ids = {r["powder_id"] for r in specs}
        gs40_powders = {"POW-BN-01", "POW-SIL-POR-01", "POW-SIL-FUM-01", "POW-PMSSQ-01", "POW-ZNO-TR-01"}
        self.assertTrue(gs40_powders.issubset(powder_ids))
        total_powder_wt = sum(float(r["gs40_target_wt_pct"]) for r in specs if r["powder_id"] in gs40_powders)
        self.assertAlmostEqual(total_powder_wt, 28.0, places=2)

        # 2. Fumed silica thixotropic yield stress
        thixo_csv = powder_dir / "fumed_silica_thixotropic_yield_stress.csv"
        self.assertTrue(thixo_csv.exists(), "fumed_silica_thixotropic_yield_stress.csv must exist")
        with open(thixo_csv, mode="r", encoding="utf-8") as f:
            thixo = list(csv.DictReader(f))
        self.assertGreaterEqual(len(thixo), 10)
        # Check 2.0% Aerosil R 972 at 80°C hot fill
        target_run = [r for r in thixo if float(r["fumed_silica_wt_pct"]) == 2.0 and float(r["temperature_c"]) == 80.0][0]
        self.assertGreater(float(target_run["bingham_yield_stress_pa"]), 5.0)
        self.assertEqual(float(target_run["zno_settling_velocity_um_min"]), 0.0)
        self.assertEqual(target_run["anti_settling_stability_30min_hot_hold"], "STABLE_SUSPENSION")

        # 3. Powder friction & slip benchmarks
        fric_csv = powder_dir / "powder_friction_and_slip_benchmarks.csv"
        self.assertTrue(fric_csv.exists(), "powder_friction_and_slip_benchmarks.csv must exist")
        with open(fric_csv, mode="r", encoding="utf-8") as f:
            frics = list(csv.DictReader(f))
        self.assertGreaterEqual(len(frics), 8)
        bn_run = [r for r in frics if "BN" in r["powder_trade_name"] and "Bioskin" in r["test_substrate"]][0]
        self.assertLess(float(bn_run["dynamic_friction_cof"]), 0.15)

        # 4. Raw Material Property DB
        self.assertTrue(raw_mat_csv.exists(), "gs40_raw_material_property_db.csv must exist")
        with open(raw_mat_csv, mode="r", encoding="utf-8") as f:
            materials = list(csv.DictReader(f))
        self.assertEqual(len(materials), 15)
        for mat in materials:
            self.assertEqual(mat["status"], "SPEC_LOCKED")
            self.assertIn("crystallization_enthalpy_j_g", mat)
            self.assertIn("cooling_behavior", mat)
            self.assertIn("surface_area_bet_m2_g", mat)
            self.assertIn("yield_stress_contribution_pa", mat)
            self.assertIn("neat_dynamic_cof", mat)

        # 5. Pilot process execution sheet template
        self.assertTrue(exec_sheet_csv.exists(), "pilot_process_execution_sheet_template.csv must exist")
        with open(exec_sheet_csv, mode="r", encoding="utf-8") as f:
            exec_rows = list(csv.DictReader(f))
        self.assertEqual(len(exec_rows), 18)


if __name__ == "__main__":
    unittest.main()


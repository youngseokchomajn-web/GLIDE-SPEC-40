"""
Unit tests for GLIDE-SPEC 40 Formulation Simulator Core
Validates STEP 1 ~ 11, M0 ~ M5 modules using standard unittest.
"""

import unittest
import os
import shutil
from src.materials.master import RawMaterial, MaterialType, MaterialStatus, REV73_RAW_MATERIALS
from src.formulas.master import REV73_TARGET_ACTIVE_FORMULA
from src.manufacturing.calculator import ManufacturingCalculator, STANDARD_BATCH_SIZES
from src.qc.models import BatchQCRecord, QCStatus, HardnessSOP, TransferSOP
from src.revision.tracker import get_rev73_revision_master
from src.doe.engine import AdvancedDOEEngine
from src.modeling.predictor import FormulationPredictor, ModelState
from src.optimization.optimizer import MultiObjectiveOptimizer
from src.storage.db import FormulationDatabase


class TestGLIDESpec40Simulator(unittest.TestCase):

    def test_rev73_target_active_formula_sum(self):
        """Rev.7.3 Target Active Formula must sum up to exactly 100.0%."""
        total = REV73_TARGET_ACTIVE_FORMULA.total_target_active_pct()
        self.assertAlmostEqual(total, 100.0, places=4, msg=f"Expected 100.0%, got {total}")

    def test_mq_resin_charge_calculation_step7(self):
        """
        Step 7 requirement:
        Target active = 12%, Raw material active = 60%
        Expected manufacturing charge = 20%
        """
        target_active = 12.0
        raw_active = 60.0
        charge_pct = ManufacturingCalculator.calculate_single_charge_pct(target_active, raw_active)
        self.assertAlmostEqual(charge_pct, 20.0, places=4)

    def test_tbd_spec_gatekeeper_blocks_final_manufacturing_formula(self):
        """
        Step 5 & Rule 2.2:
        When a material has active_pct = None (TBD), manufacturing formula generation must fail gracefully.
        """
        result = ManufacturingCalculator.generate_manufacturing_formula(
            active_formula=REV73_TARGET_ACTIVE_FORMULA,
            material_specs=REV73_RAW_MATERIALS,
            batch_size_kg=1.0
        )
        self.assertFalse(result.is_valid, "Formula generation should be invalid when raw material specs are TBD")
        self.assertTrue(any("MAT-MQ-01" in item for item in result.missing_specs))

    def test_manufacturing_formula_with_cogs_and_carrier_offset(self):
        """
        Validates manufacturing calculation when specs are confirmed by supplier CoA,
        including MQ carrier offset and bulk COGS cost calculation.
        """
        mock_specs = dict(REV73_RAW_MATERIALS)

        # Mock confirmed MQ resin: 60% solid in Dimethicone carrier
        mock_specs["MAT-MQ-01"] = RawMaterial(
            material_id="MAT-MQ-01",
            inci="Trimethylsiloxysilicate (and) Dimethicone",
            trade_name="MQ-60-D",
            supplier="Shin-Etsu / Dow",
            grade="Cosmetic Resin Solution",
            material_type=MaterialType.RESIN,
            active_pct=60.0,
            carrier="Dimethicone",
            carrier_pct=40.0,
            cost_per_kg=60000.0,
            status=MaterialStatus.VERIFIED
        )
        mock_specs["MAT-WAX-SYSTEM"] = RawMaterial(
            material_id="MAT-WAX-SYSTEM",
            inci="Synthetic Wax, Candelilla Wax",
            trade_name="Wax-Blend-17",
            supplier="Koster Keunen",
            grade="Technical Wax Blend",
            material_type=MaterialType.WAX,
            active_pct=100.0,
            cost_per_kg=20000.0,
            status=MaterialStatus.VERIFIED
        )
        mock_specs["MAT-SIL-SYSTEM"] = RawMaterial(
            material_id="MAT-SIL-SYSTEM",
            inci="Dimethicone, Caprylyl Methicone",
            trade_name="Sil-Blend-28",
            supplier="Dow",
            grade="Volatile Replacement Fluid",
            material_type=MaterialType.SILICONE,
            active_pct=100.0,
            cost_per_kg=15000.0,
            status=MaterialStatus.VERIFIED
        )

        batch_size = 66.0  # Initial Charge Candidate
        calc_result = ManufacturingCalculator.generate_manufacturing_formula(
            active_formula=REV73_TARGET_ACTIVE_FORMULA,
            material_specs=mock_specs,
            batch_size_kg=batch_size,
            offset_carrier=True
        )

        self.assertTrue(calc_result.is_valid)
        self.assertEqual(len(calc_result.missing_specs), 0)

        # MQ charge should be 20.0% (12 / 0.60)
        mq_item = next(i for i in calc_result.items if i.material_id == "MAT-MQ-01")
        self.assertAlmostEqual(mq_item.charge_pct, 20.0, places=3)
        self.assertAlmostEqual(mq_item.charge_weight_kg, 13.2, places=2)  # 66 * 0.20 = 13.2 kg

        # Silicone carrier charge should be offset by 8% (20% * 40% = 8% carrier introduced)
        sil_item = next(i for i in calc_result.items if i.material_id == "MAT-SIL-SYSTEM")
        self.assertAlmostEqual(sil_item.charge_pct, 20.0, places=3)
        self.assertTrue(len(calc_result.carrier_offsets_applied) > 0)

    def test_doe_ratios_resolve_blends_to_traceable_raw_materials(self):
        """DOE ratios must replace blend placeholders, not require blend mocks."""
        specs = dict(REV73_RAW_MATERIALS)
        specs["MAT-MQ-01"] = RawMaterial(
            material_id="MAT-MQ-01", inci="MQ Resin", trade_name="MQ-60",
            supplier="Supplier", grade="Cosmetic", material_type=MaterialType.RESIN,
            active_pct=60.0, carrier="Dimethicone", carrier_pct=40.0,
            status=MaterialStatus.VERIFIED,
        )
        trial = AdvancedDOEEngine.generate_full_doe_design()[8]
        result = ManufacturingCalculator.generate_manufacturing_formula(
            active_formula=REV73_TARGET_ACTIVE_FORMULA,
            material_specs=specs,
            batch_size_kg=1.0,
            component_ratios={
                "MAT-WAX-SYSTEM": {
                    "MAT-WAX-SYN-01": trial.synthetic_wax_pct,
                    "MAT-WAX-CAN-01": trial.candelilla_wax_pct,
                },
                "MAT-SIL-SYSTEM": {
                    "MAT-SIL-DIM-01": trial.dimethicone_pct,
                    "MAT-SIL-CAP-01": trial.caprylyl_methicone_pct,
                },
            },
        )
        self.assertTrue(result.is_valid)
        ids = {item.material_id for item in result.items}
        self.assertNotIn("MAT-WAX-SYSTEM", ids)
        self.assertNotIn("MAT-SIL-SYSTEM", ids)
        self.assertIn("MAT-WAX-SYN-01", ids)
        dim = next(item for item in result.items if item.material_id == "MAT-SIL-DIM-01")
        self.assertAlmostEqual(dim.charge_pct, 9.0, places=3)

    def test_doe_to_manufacturing_to_cogs(self):
        """A DOE trial deterministically resolves to raw charges and COGS."""
        specs = {key: value.model_copy(deep=True) for key, value in REV73_RAW_MATERIALS.items()}
        for index, material in enumerate(specs.values(), start=1):
            material.cost_per_kg = float(index * 1000)
        specs["MAT-MQ-01"] = RawMaterial(
            material_id="MAT-MQ-01", inci="MQ Resin", trade_name="MQ-60", supplier="Supplier",
            grade="Cosmetic", material_type=MaterialType.RESIN, active_pct=60.0,
            carrier="Dimethicone", carrier_pct=40.0, cost_per_kg=10000.0,
            status=MaterialStatus.VERIFIED,
        )
        trial = AdvancedDOEEngine.generate_full_doe_design()[8]
        ratios = {
            "MAT-WAX-SYSTEM": {"MAT-WAX-SYN-01": trial.synthetic_wax_pct, "MAT-WAX-CAN-01": trial.candelilla_wax_pct},
            "MAT-SIL-SYSTEM": {"MAT-SIL-DIM-01": trial.dimethicone_pct, "MAT-SIL-CAP-01": trial.caprylyl_methicone_pct},
        }
        first = ManufacturingCalculator.generate_manufacturing_formula(REV73_TARGET_ACTIVE_FORMULA, specs, 1.0, component_ratios=ratios)
        second = ManufacturingCalculator.generate_manufacturing_formula(REV73_TARGET_ACTIVE_FORMULA, specs, 1.0, component_ratios=ratios)
        self.assertTrue(first.is_valid)
        self.assertIsNotNone(first.cost_per_20g_stick)
        self.assertEqual(first.model_dump(), second.model_dump())
        self.assertAlmostEqual(sum(i.charge_weight_kg for i in first.items), first.total_charge_pct / 100, places=4)

    def test_advanced_doe_matrix_constraints(self):
        """Validates that Advanced DOE Engine adheres to mixture boundaries."""
        trials = AdvancedDOEEngine.generate_full_doe_design()
        self.assertGreaterEqual(len(trials), 10)
        for t in trials:
            self.assertTrue(t.validate_mixture_constraints(), f"Trial {t.trial_id} violated mixture constraints")

    def test_database_persistence_and_qc(self):
        """Checks DB SQLite storage for QC records."""
        test_dir = "data/test_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        sample_record = BatchQCRecord(
            batch_id="BATCH-TEST-SQLITE-01",
            formula_id="FORM-TEST",
            revision="Rev.7.3",
            test_date="2026-09-12",
            operator="Chemist",
            hardness_gf=830.0,
            transfer_g_10c=0.045,
            density_g_cm3=1.08,
            drop_point_c=61.5,
            hardness_sop=HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30),
            transfer_sop=TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")
        )

        db.save_qc_record(sample_record)
        records = db.get_all_qc_records()
        self.assertTrue(any(r.batch_id == "BATCH-TEST-SQLITE-01" for r in records))
        restored = next(r for r in records if r.batch_id == "BATCH-TEST-SQLITE-01")
        self.assertEqual(restored.hardness_sop, sample_record.hardness_sop)
        self.assertEqual(restored.transfer_sop, sample_record.transfer_sop)
        self.assertTrue(restored.is_sop_complete())

        # Cleanup tmp test directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_optimizer_candidate_generation(self):
        """Optimizer generates valid candidate formulations conforming to constraints."""
        predictor = FormulationPredictor()
        optimizer = MultiObjectiveOptimizer(predictor=predictor)
        candidates = optimizer.generate_candidates(top_n=3)
        self.assertEqual(len(candidates), 3)
        for c in candidates:
            wax_sum = c.synthetic_wax_pct + c.candelilla_wax_pct
            sil_sum = c.dimethicone_pct + c.caprylyl_methicone_pct
            self.assertAlmostEqual(wax_sum, 17.0, places=2)
            self.assertAlmostEqual(sil_sum, 28.0, places=2)


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for GLIDE-SPEC 40 Formulation Simulator Core
Validates STEP 1 ~ 11, M0 ~ M5 modules using standard unittest.
"""

import unittest
import os
import shutil
import sqlite3
from src.materials.master import RawMaterial, MaterialType, MaterialStatus, REV73_RAW_MATERIALS
from src.formulas.master import REV73_TARGET_ACTIVE_FORMULA
from src.manufacturing.calculator import ManufacturingCalculator, STANDARD_BATCH_SIZES
from src.manufacturing.models import ManufacturingBatch
from src.qc.models import BatchQCRecord, QCStatus, HardnessSOP, TransferSOP, DataOrigin, ProcessCondition
from src.revision.tracker import get_rev73_revision_master
from src.doe.engine import AdvancedDOEEngine, DOETrial
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
        """Checks DB SQLite storage for QC records with valid parent ManufacturingBatch."""
        test_dir = "data/test_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        # 1. Create and persist parent ManufacturingBatch first (Foreign Key requirement)
        parent_batch = ManufacturingBatch(
            batch_id="BATCH-TEST-SQLITE-01",
            trial_id=None,
            formula_id="FORM-TEST",
            revision="Rev.7.3",
            created_date="2026-09-12",
            operator="Chemist",
            batch_size_kg=1.0,
            total_charge_pct=100.0,
            items=[],
            process_conditions=ProcessCondition(),
            total_raw_material_cost=20000.0,
            cost_per_20g_stick=400.0
        )
        db.save_manufacturing_batch(parent_batch)

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

    def test_qc_requires_existing_manufacturing_batch(self):
        """Phase 2A [P1 Fix]: QC record MUST reject orphan batch_id not existing in manufacturing_batches."""
        test_dir = "data/test_batch_fk_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        orphan_batch_qc = BatchQCRecord(
            batch_id="BATCH-NON-EXISTENT-XYZ",
            trial_id=None,
            formula_id="FORM-TEST",
            revision="Rev.7.3",
            test_date="2026-09-12",
            operator="Tester",
            hardness_gf=820.0,
            transfer_g_10c=0.045,
            hardness_sop=complete_hardness,
            transfer_sop=complete_transfer
        )

        with self.assertRaises(sqlite3.IntegrityError):
            db.save_qc_record(orphan_batch_qc)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_cogs_basis_and_quote_status_snapshot(self):
        """Phase 2A [P2 Fix]: Verifies COGS status, price source, and calculation timestamp snapshots."""
        test_dir = "data/test_cogs_status_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        batch = ManufacturingBatch(
            batch_id="BATCH-COGS-TEST-01",
            trial_id=None,
            formula_id="FORM-REV7.3",
            revision="Rev.7.3",
            created_date="2026-09-12",
            operator="Cost Engineer",
            batch_size_kg=66.0,
            total_charge_pct=100.21,
            items=[],
            process_conditions=ProcessCondition(),
            total_raw_material_cost=2689610.0,
            cost_per_20g_stick=815.0,
            cogs_basis="ESTIMATED_SIMULATION",
            material_price_source="Supplier Quote REQ-GLIDE40-MAT-202609",
            quote_status="PENDING_FORMAL_QUOTES",
            calculated_at="2026-09-12T16:00:00"
        )
        db.save_manufacturing_batch(batch)

        reloaded = db.get_manufacturing_batch("BATCH-COGS-TEST-01")
        self.assertIsNotNone(reloaded)
        self.assertEqual(reloaded.cogs_basis, "ESTIMATED_SIMULATION")
        self.assertEqual(reloaded.quote_status, "PENDING_FORMAL_QUOTES")
        self.assertFalse(reloaded.is_cogs_confirmed())

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_predictor_fit_checks_persisted_db_lineage(self):
        """Phase 2A [P2 Fix]: Predictor checks DB existence to reject memory-forged orphan lineage records."""
        test_dir = "data/test_predictor_db_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        # Create real trial & batch in DB
        trial = DOETrial(trial_id="DOE-REAL-01", synthetic_wax_pct=12.0, candelilla_wax_pct=5.0, dimethicone_pct=18.0, caprylyl_methicone_pct=10.0)
        db.save_doe_trial(trial)
        batch = ManufacturingBatch(
            batch_id="BATCH-REAL-01", trial_id=trial.trial_id, formula_id="FORM-REV7.3", revision="Rev.7.3",
            created_date="2026-09-12", operator="Lead", batch_size_kg=1.0, total_charge_pct=100.0,
            items=[], process_conditions=trial.to_process_condition()
        )
        db.save_manufacturing_batch(batch)

        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        # 1. Real record matching DB records
        real_qc = BatchQCRecord(
            batch_id=batch.batch_id, trial_id=trial.trial_id, formula_id="FORM-REV7.3", revision="Rev.7.3",
            test_date="2026-09-12", operator="Tester", hardness_gf=820.0, transfer_g_10c=0.045,
            data_origin=DataOrigin.REAL_PILOT, process_conditions=batch.process_conditions,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )

        # 2. Forged record with non-existent trial/batch
        forged_qc = BatchQCRecord(
            batch_id="BATCH-FORGED-99", trial_id="DOE-FORGED-99", formula_id="FORM-REV7.3", revision="Rev.7.3",
            test_date="2026-09-12", operator="Tester", hardness_gf=820.0, transfer_g_10c=0.045,
            data_origin=DataOrigin.REAL_PILOT, process_conditions=batch.process_conditions,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )

        predictor = FormulationPredictor()
        predictor.fit([real_qc, forged_qc], db=db)
        # Only the real_qc should be accepted into training_records; forged_qc must be dropped
        self.assertEqual(len(predictor.training_records), 1)
        self.assertEqual(predictor.training_records[0].batch_id, "BATCH-REAL-01")

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

    def test_schema_migration_idempotency(self):
        """Phase 2A: Verifies schema versioning table and idempotent migrations to Schema v3."""
        test_dir = "data/test_migration_tmp"
        db = FormulationDatabase(data_dir=test_dir)
        self.assertEqual(db.get_current_schema_version(), 3)

        # Run init again to test idempotency
        db._init_sqlite()
        self.assertEqual(db.get_current_schema_version(), 3)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_foreign_key_violation_raises_error(self):
        """Phase 2A [P1 Fix]: Verifies that unlinked/invalid trial_id violates Foreign Key integrity."""
        test_dir = "data/test_fk_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        # 1. Create valid parent batch so batch_id is valid
        parent_batch = ManufacturingBatch(
            batch_id="BATCH-ORPHAN-01", trial_id=None, formula_id="FORM-TEST", revision="Rev.7.3",
            created_date="2026-09-12", operator="Tester", batch_size_kg=1.0, total_charge_pct=100.0,
            items=[], process_conditions=ProcessCondition()
        )
        db.save_manufacturing_batch(parent_batch)

        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        orphan_qc = BatchQCRecord(
            batch_id="BATCH-ORPHAN-01",
            trial_id="DOE-NON-EXISTENT-999",  # Does NOT exist in doe_trials!
            formula_id="FORM-TEST", revision="Rev.7.3",
            test_date="2026-09-12", operator="Tester",
            hardness_gf=820.0, transfer_g_10c=0.045,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )

        with self.assertRaises(sqlite3.IntegrityError):
            db.save_qc_record(orphan_qc)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_data_eligibility_gate_rejects_synthetic_and_incomplete(self):
        """Phase 2A [P1 Fix]: Data Contract gate verifies lineage, complete SOPs, and blocks premature ML promotion."""
        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        # 1. Real Pilot with linked trial_id and complete SOP -> Eligible
        real_record = BatchQCRecord(
            batch_id="BATCH-REAL-01", trial_id="DOE-EXP-001", formula_id="FORM-TEST", revision="Rev.7.3",
            test_date="2026-09-12", operator="Chemist",
            hardness_gf=820.0, transfer_g_10c=0.045,
            data_origin=DataOrigin.REAL_PILOT,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )
        self.assertTrue(real_record.is_training_eligible())

        # 2. Unlinked record (trial_id is None) -> Lineage violation, rejected
        unlinked_record = BatchQCRecord(
            batch_id="BATCH-UNLINKED-01", trial_id=None, formula_id="FORM-TEST", revision="Rev.7.3",
            test_date="2026-09-12", operator="Chemist",
            hardness_gf=820.0, transfer_g_10c=0.045,
            data_origin=DataOrigin.REAL_PILOT,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )
        self.assertFalse(unlinked_record.is_training_eligible())

        # 3. Synthetic Test data -> Strictly rejected from training
        synthetic_record = BatchQCRecord(
            batch_id="BATCH-SYNTH-01", trial_id="DOE-EXP-001", formula_id="FORM-TEST", revision="Rev.7.3",
            test_date="2026-09-12", operator="Simulation Engine",
            hardness_gf=820.0, transfer_g_10c=0.045,
            data_origin=DataOrigin.SYNTHETIC_TEST,
            hardness_sop=complete_hardness, transfer_sop=complete_transfer
        )
        self.assertFalse(synthetic_record.is_training_eligible())

        # 4. Predictor does NOT promote with synthetic records or fewer than 16 records
        predictor = FormulationPredictor()
        promoted_synth = predictor.fit([synthetic_record] * 20)
        self.assertFalse(promoted_synth, "Model must never promote to TRAINED_LINEAR with synthetic records")
        self.assertEqual(predictor.state, ModelState.AWAITING_PILOT_DATA)

        promoted_under_threshold = predictor.fit([real_record] * 10)
        self.assertFalse(promoted_under_threshold, "Model must not promote with < 16 eligible records")
        self.assertEqual(predictor.state, ModelState.AWAITING_PILOT_DATA)

    def test_doe_batch_qc_complete_linkage(self):
        """Phase 2A [P1/P2 Fix]: Full End-to-End Lineage: DOETrial (75C) -> ManufacturingBatch -> QC Record."""
        test_dir = "data/test_linkage_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        # 1. Save DOE Trial with non-default fill temperature (75.0C, 3200 RPM)
        trial = DOETrial(
            trial_id="DOE-EXP-LINK-01", design_type="Vertex",
            synthetic_wax_pct=13.0, candelilla_wax_pct=4.0,
            dimethicone_pct=16.0, caprylyl_methicone_pct=12.0,
            fill_temperature_c=75.0, shear_speed_rpm=3200.0,
            mixing_time_min=25.0
        )
        db.save_doe_trial(trial)
        reloaded_trial = db.get_doe_trial("DOE-EXP-LINK-01")
        self.assertIsNotNone(reloaded_trial)
        self.assertEqual(reloaded_trial.fill_temperature_c, 75.0)

        # 2. Generate Manufacturing Charges from Trial Ratios using verified mock specs
        component_ratios = trial.to_component_ratios()
        verified_specs = dict(REV73_RAW_MATERIALS)
        verified_specs["MAT-MQ-01"] = RawMaterial(
            material_id="MAT-MQ-01", inci="Trimethylsiloxysilicate (and) Dimethicone",
            trade_name="MQ-60-D", supplier="Shin-Etsu", grade="Resin Solution",
            material_type=MaterialType.RESIN, active_pct=60.0, carrier="Dimethicone", carrier_pct=40.0,
            cost_per_kg=60000.0, status=MaterialStatus.VERIFIED
        )
        calc_result = ManufacturingCalculator.generate_manufacturing_formula(
            active_formula=REV73_TARGET_ACTIVE_FORMULA,
            material_specs=verified_specs,
            batch_size_kg=5.0,
            component_ratios=component_ratios
        )
        self.assertTrue(calc_result.is_valid)

        # 3. Create and persist ManufacturingBatch with real process conditions snapshot
        mfg_batch = ManufacturingBatch(
            batch_id="BATCH-PILOT-LINK-01",
            trial_id=trial.trial_id,
            formula_id=calc_result.formula_id,
            revision="Rev.7.3",
            created_date="2026-09-12",
            operator="Pilot Lead",
            batch_size_kg=calc_result.batch_size_kg,
            total_charge_pct=calc_result.total_charge_pct,
            items=calc_result.items,
            process_conditions=trial.to_process_condition(),
            total_raw_material_cost=calc_result.total_raw_material_cost,
            cost_per_20g_stick=calc_result.cost_per_20g_stick
        )
        db.save_manufacturing_batch(mfg_batch)

        reloaded_batch = db.get_manufacturing_batch("BATCH-PILOT-LINK-01")
        self.assertIsNotNone(reloaded_batch)
        self.assertEqual(reloaded_batch.process_conditions.fill_temperature_c, 75.0)
        self.assertEqual(reloaded_batch.process_conditions.shear_speed_rpm, 3200.0)

        # 4. Link QC Record: explicitly snapshots process conditions from the batch
        qc_record = BatchQCRecord(
            batch_id=mfg_batch.batch_id,
            trial_id=trial.trial_id,
            formula_id=mfg_batch.formula_id,
            revision=mfg_batch.revision,
            test_date="2026-09-12",
            operator="QC Specialist",
            process_conditions=mfg_batch.process_conditions,
            hardness_gf=810.0,
            transfer_g_10c=0.046,
            hardness_sop=HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30),
            transfer_sop=TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")
        )
        db.save_qc_record(qc_record)

        reloaded_qc = db.get_all_qc_records()
        linked = next(r for r in reloaded_qc if r.batch_id == "BATCH-PILOT-LINK-01")
        self.assertEqual(linked.trial_id, "DOE-EXP-LINK-01")
        self.assertEqual(linked.process_conditions.fill_temperature_c, 75.0)
        self.assertEqual(linked.process_conditions.shear_speed_rpm, 3200.0)
        self.assertTrue(linked.is_training_eligible(verified_raw_materials=True))

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_synthetic_coefficient_recovery(self):
        """Phase 3 [M4 Engine]: Verify OLS recovers known linear response coefficients within 1e-3."""
        from src.modeling.regression import MixtureRegressionModel
        import numpy as np

        model = MixtureRegressionModel("Test Hardness")
        # True equation: y = 800.0 + 50.0*u1 - 30.0*v1 - 2.0*T
        # Generate 16 sample grid
        u1_vals = [0.6, 0.7, 0.8, 0.7]
        v1_vals = [0.5, 0.6, 0.7, 0.6]
        t_vals = [75.0, 80.0, 85.0, 80.0]

        X_rows = []
        y_rows = []
        for i in range(4):
            for j in range(4):
                u = u1_vals[i]
                v = v1_vals[j]
                t = t_vals[(i + j) % 4]
                y = 800.0 + 50.0 * u - 30.0 * v - 2.0 * t
                X_rows.append([u, v, t])
                y_rows.append(y)

        X = np.array(X_rows)
        y = np.array(y_rows)

        metrics = model.fit(X, y)
        self.assertAlmostEqual(metrics.intercept, 800.0, places=2)
        self.assertAlmostEqual(metrics.coefficients[0], 50.0, places=2)
        self.assertAlmostEqual(metrics.coefficients[1], -30.0, places=2)
        self.assertAlmostEqual(metrics.coefficients[2], -2.0, places=2)
        self.assertGreaterEqual(metrics.r_squared, 0.999)
        self.assertLess(metrics.loocv_rmse, 0.05)

        # Test prediction method
        pred_val, margin = model.predict(syn_wax=17.0 * 0.7, dimethicone=28.0 * 0.6, fill_temp=80.0)
        expected = 800.0 + 50.0 * 0.7 - 30.0 * 0.6 - 2.0 * 80.0
        self.assertAlmostEqual(pred_val, expected, places=1)

    def test_synthetic_data_cannot_promote_production_model(self):
        """Phase 3 [Safety Gate]: Synthetic test records cannot promote model to TRAINED_LINEAR."""
        predictor = FormulationPredictor()
        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        synthetic_records = [
            BatchQCRecord(
                batch_id=f"SYNTH-BATCH-{i:02d}",
                trial_id=f"DOE-EXP-{i:02d}",
                formula_id="GLIDE-REV73-PILOT",
                revision="Rev.7.3",
                test_date="2026-09-12",
                operator="Simulator",
                hardness_gf=820.0,
                transfer_g_10c=0.045,
                data_origin=DataOrigin.SYNTHETIC_TEST,
                hardness_sop=complete_hardness,
                transfer_sop=complete_transfer
            )
            for i in range(20)
        ]

        promoted = predictor.fit(synthetic_records)
        self.assertFalse(promoted)
        self.assertEqual(predictor.state, ModelState.AWAITING_PILOT_DATA)

        # Calling predict() must return None with Rule #6 warning
        pred = predictor.predict(12.0, 5.0, 17.0, 11.0, 80.0)
        self.assertIsNone(pred.hardness_gf)
        self.assertIsNone(pred.transfer_g)
        self.assertIn("Property prediction locked", pred.message)

    def test_trained_linear_prediction_output_and_labeling(self):
        """Phase 3 [M4 & Rule #12]: 16 eligible records with 3 centre-points promote to TRAINED_LINEAR and output mandatory label."""
        test_dir = "data/test_phase3_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        records = []
        for i in range(16):
            trial_id = f"DOE-P3-{i:02d}"
            batch_id = f"BATCH-P3-{i:02d}"
            # Ensure at least 4 centre points at 80°C
            fill_t = 80.0 if i < 4 else (75.0 if i % 2 == 0 else 85.0)
            syn_w = 12.0 if i < 4 else (10.0 + (i % 6) * 0.8)
            dim = 17.0 if i < 4 else (14.0 + (i % 5) * 1.5)

            trial = DOETrial(
                trial_id=trial_id, design_type="Custom",
                synthetic_wax_pct=syn_w, candelilla_wax_pct=17.0 - syn_w,
                dimethicone_pct=dim, caprylyl_methicone_pct=28.0 - dim,
                fill_temperature_c=fill_t, shear_speed_rpm=3000.0, mixing_time_min=20.0
            )
            db.save_doe_trial(trial)

            calc = ManufacturingCalculator.generate_manufacturing_formula(
                active_formula=REV73_TARGET_ACTIVE_FORMULA,
                material_specs=REV73_RAW_MATERIALS,
                batch_size_kg=5.0,
                component_ratios=trial.to_component_ratios()
            )
            mfg = ManufacturingBatch(
                batch_id=batch_id,
                trial_id=trial_id,
                formula_id="GLIDE-REV73-PILOT",
                revision="Rev.7.3",
                created_date="2026-09-12",
                operator="Pilot Lead",
                batch_size_kg=calc.batch_size_kg,
                total_charge_pct=calc.total_charge_pct,
                items=calc.items,
                process_conditions=trial.to_process_condition()
            )
            db.save_manufacturing_batch(mfg)

            qc = BatchQCRecord(
                batch_id=batch_id, trial_id=trial_id, formula_id="GLIDE-REV73-PILOT", revision="Rev.7.3",
                test_date="2026-09-12", operator="Pilot QC",
                process_conditions=trial.to_process_condition(),
                hardness_gf=800.0 + 10.0 * (syn_w - 12.0) - 1.5 * (fill_t - 80.0),
                transfer_g_10c=0.045 - 0.001 * (syn_w - 12.0) + 0.0005 * (dim - 17.0),
                drop_point_c=61.5 + 0.2 * (syn_w - 12.0),
                data_origin=DataOrigin.REAL_PILOT,
                hardness_sop=complete_hardness,
                transfer_sop=complete_transfer
            )
            db.save_qc_record(qc)
            records.append(qc)

        predictor = FormulationPredictor()
        promoted = predictor.fit(records, verified_raw_materials=True, db=db)
        self.assertTrue(promoted, "Should promote to TRAINED_LINEAR with 16 eligible records and >= 3 centre points")
        self.assertEqual(predictor.state, ModelState.TRAINED_LINEAR)

        # Run prediction
        pred = predictor.predict(12.0, 5.0, 17.0, 11.0, 80.0)
        self.assertIsNotNone(pred.hardness_gf)
        self.assertIsNotNone(pred.transfer_g)
        self.assertGreater(pred.confidence_score, 0.5)

        # Rule #12 verification
        self.assertIn("Predicted", pred.message)
        self.assertIn("NOT experimental measurement", pred.message)
        self.assertIn("LOOCV RMSE", pred.message)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_optimizer_uncalibrated_returns_rule_candidates(self):
        """Phase 4 [M5 Optimizer]: Uncalibrated predictor returns rule-based boundary candidates without predictions."""
        from src.optimization.optimizer import MultiObjectiveOptimizer

        predictor = FormulationPredictor()
        optimizer = MultiObjectiveOptimizer(predictor=predictor)
        candidates = optimizer.generate_candidates(top_n=3)

        self.assertEqual(len(candidates), 3)
        for c in candidates:
            # Check mixture invariants
            self.assertAlmostEqual(c.synthetic_wax_pct + c.candelilla_wax_pct, 17.0, places=2)
            self.assertAlmostEqual(c.dimethicone_pct + c.caprylyl_methicone_pct, 28.0, places=2)
            # Property predictions must remain None
            self.assertIsNone(c.predicted_hardness_gf)
            self.assertIsNone(c.predicted_transfer_g)
            self.assertGreater(c.estimated_cogs_krw, 0.0)
            self.assertIn("Uncalibrated", c.prediction_label)

    def test_optimizer_slsqp_convergence_on_trained_model(self):
        """Phase 4 [M5 Optimizer]: Trained regression model enables SLSQP Pareto search across 3 strategic scenarios."""
        from src.optimization.optimizer import MultiObjectiveOptimizer

        test_dir = "data/test_phase4_tmp"
        db = FormulationDatabase(data_dir=test_dir)

        complete_hardness = HardnessSOP(probe_type="2mm Needle", penetration_depth_mm=2.0, test_speed_mm_s=1.0, conditioning_time_min=30)
        complete_transfer = TransferSOP(substrate_type="Artificial Skin", applied_area_cm2=4.0, applied_pressure_g=500.0, contact_time_s=3.0, test_method="Two stroke")

        records = []
        for i in range(16):
            trial_id = f"DOE-P4-{i:02d}"
            batch_id = f"BATCH-P4-{i:02d}"
            fill_t = 80.0 if i < 4 else (76.0 if i % 2 == 0 else 84.0)
            syn_w = 12.0 if i < 4 else (10.0 + (i % 6) * 0.8)
            dim = 17.0 if i < 4 else (14.0 + (i % 5) * 1.5)

            trial = DOETrial(
                trial_id=trial_id, design_type="Custom",
                synthetic_wax_pct=syn_w, candelilla_wax_pct=17.0 - syn_w,
                dimethicone_pct=dim, caprylyl_methicone_pct=28.0 - dim,
                fill_temperature_c=fill_t, shear_speed_rpm=3000.0, mixing_time_min=20.0
            )
            db.save_doe_trial(trial)

            calc = ManufacturingCalculator.generate_manufacturing_formula(
                active_formula=REV73_TARGET_ACTIVE_FORMULA,
                material_specs=REV73_RAW_MATERIALS,
                batch_size_kg=5.0,
                component_ratios=trial.to_component_ratios()
            )
            mfg = ManufacturingBatch(
                batch_id=batch_id, trial_id=trial_id, formula_id="GLIDE-REV73-PILOT", revision="Rev.7.3",
                created_date="2026-09-12", operator="Pilot Lead",
                batch_size_kg=calc.batch_size_kg, total_charge_pct=calc.total_charge_pct,
                items=calc.items, process_conditions=trial.to_process_condition()
            )
            db.save_manufacturing_batch(mfg)

            qc = BatchQCRecord(
                batch_id=batch_id, trial_id=trial_id, formula_id="GLIDE-REV73-PILOT", revision="Rev.7.3",
                test_date="2026-09-12", operator="Pilot QC",
                process_conditions=trial.to_process_condition(),
                hardness_gf=810.0 + 8.0 * (syn_w - 12.0) - 1.2 * (fill_t - 80.0),
                transfer_g_10c=0.046 - 0.0008 * (syn_w - 12.0) + 0.0004 * (dim - 17.0),
                drop_point_c=61.8 + 0.15 * (syn_w - 12.0),
                data_origin=DataOrigin.REAL_PILOT,
                hardness_sop=complete_hardness, transfer_sop=complete_transfer
            )
            db.save_qc_record(qc)
            records.append(qc)

        predictor = FormulationPredictor()
        predictor.fit(records, verified_raw_materials=True, db=db)
        self.assertEqual(predictor.state, ModelState.TRAINED_LINEAR)

        optimizer = MultiObjectiveOptimizer(predictor=predictor)
        candidates = optimizer.generate_candidates(top_n=3)

        self.assertEqual(len(candidates), 3)
        scenario_names = [c.scenario_name for c in candidates]
        self.assertIn("Balanced Baseline", scenario_names)
        self.assertIn("High-Slip Summer", scenario_names)
        self.assertIn("High-Payoff Winter", scenario_names)

        for c in candidates:
            # 1. Mixture constraints
            self.assertAlmostEqual(c.synthetic_wax_pct + c.candelilla_wax_pct, 17.0, places=2)
            self.assertAlmostEqual(c.dimethicone_pct + c.caprylyl_methicone_pct, 28.0, places=2)
            self.assertTrue(75.0 <= c.fill_temperature_c <= 85.0)

            # 2. Predicted values
            self.assertIsNotNone(c.predicted_hardness_gf)
            self.assertIsNotNone(c.predicted_transfer_g)
            self.assertGreater(c.confidence_score, 0.5)
            self.assertGreater(c.desirability_score, 0.0)
            self.assertGreater(c.estimated_cogs_krw, 0.0)

            # 3. Rule #12 compliance
            self.assertIn("Predicted", c.prediction_label)
            self.assertIn("NOT experimental measurement", c.prediction_label)

        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

    def test_parameterized_doe_generation(self):
        """Phase 5 [DOE Engine]: Parameterized DOE produces >= 16 runs with >= 3 centre-points and valid mixture invariants."""
        from src.doe.engine import AdvancedDOEEngine, DOEConfig

        cfg = DOEConfig(
            total_wax_pct=17.0,
            syn_wax_min=10.0,
            syn_wax_max=14.0,
            syn_wax_center=12.0,
            total_silicone_pct=28.0,
            dimethicone_min=14.0,
            dimethicone_max=20.0,
            dimethicone_center=17.0,
            fill_temp_min=76.0,
            fill_temp_max=84.0,
            fill_temp_center=80.0,
            centre_point_replicates=5
        )

        trials = AdvancedDOEEngine.generate_custom_doe(cfg)

        # 1. Total runs count >= 16 (4 vertex + 6 axial + 2 interior + 5 centre = 17 runs)
        self.assertGreaterEqual(len(trials), 16)
        self.assertEqual(len(trials), 17)

        # 2. Centre points count >= 5
        centre_trials = [t for t in trials if "Centroid" in t.design_type]
        self.assertEqual(len(centre_trials), 5)

        # 3. Verify mixture invariants on every trial
        for t in trials:
            self.assertTrue(t.validate_mixture_constraints(), f"Mixture constraint failed on {t.trial_id}")
            self.assertAlmostEqual(t.synthetic_wax_pct + t.candelilla_wax_pct, 17.0, places=2)
            self.assertAlmostEqual(t.dimethicone_pct + t.caprylyl_methicone_pct, 28.0, places=2)
            self.assertTrue(76.0 <= t.fill_temperature_c <= 84.0)

        # 4. Default generator also produces >= 16 runs
        default_trials = AdvancedDOEEngine.generate_full_doe_design()
        self.assertGreaterEqual(len(default_trials), 16)


if __name__ == "__main__":
    unittest.main()


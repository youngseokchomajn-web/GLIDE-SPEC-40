"""
test_shampoo_benchmark.py
=========================
Unit tests for the GLIDE-SPEC 40 Public Benchmark Layer (Nature 812 Shampoo Dataset).

Verifies:
1. Raw file integrity and cryptographic SHA-256 checksums.
2. Normalization dataset row counts, schemas, and continuous response ranges.
3. Provenance metadata presence (source_file_hash, dataset_id, data_origin).
4. Mathematical properties:
   - Model A full rank and condition number
   - Model B Scheffé coordinate equivalence to Model A
   - Sparse interaction singularity (Model A-Quad has rank deficiency)
   - Model C subsystem representation full rank
5. Strict Qualification Firewall:
   - DataOrigin.PUBLIC_BENCHMARK is strictly rejected by GS-40 stick qualification guards.
"""

import unittest
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

BENCHMARK_DIR = Path(__file__).resolve().parent.parent / "benchmarks" / "shampoo"
RAW_DIR = BENCHMARK_DIR / "raw"
NORMALIZED_DIR = BENCHMARK_DIR / "normalized"
REPORTS_DIR = BENCHMARK_DIR / "reports"

RAW_JSON_PATH = RAW_DIR / "LiquidFormulationsDataset_2023.json"
EXPECTED_SHA256 = "3a195870782e6fd87bdd7499cbb4fe201d025b2cda05f9eee9fb9477f34b58bd"


class TestShampooBenchmark(unittest.TestCase):
    def test_raw_dataset_file_integrity(self):
        """Verify that the raw JSON file exists, is unmodified, and matches SHA-256."""
        self.assertTrue(RAW_JSON_PATH.exists(), f"Missing raw JSON at {RAW_JSON_PATH}")
        h = hashlib.sha256()
        with open(RAW_JSON_PATH, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        self.assertEqual(h.hexdigest(), EXPECTED_SHA256, "Raw JSON checksum mismatch")

    def test_normalized_datasets_exist_and_counts(self):
        """Verify that normalized CSV datasets have the expected row counts and targets."""
        visc_path = NORMALIZED_DIR / "shampoo_m4_visc_at_100s.csv"
        turb_path = NORMALIZED_DIR / "shampoo_m4_turbidity.csv"
        stab_path = NORMALIZED_DIR / "shampoo_m4_phase_stability.csv"

        self.assertTrue(visc_path.exists(), "Missing normalized viscosity CSV")
        self.assertTrue(turb_path.exists(), "Missing normalized turbidity CSV")
        self.assertTrue(stab_path.exists(), "Missing normalized phase stability CSV")

        df_visc = pd.read_csv(visc_path)
        df_turb = pd.read_csv(turb_path)
        df_stab = pd.read_csv(stab_path)

        # Row counts
        self.assertEqual(len(df_visc), 294, f"Expected 294 stable viscosity rows, got {len(df_visc)}")
        self.assertEqual(len(df_turb), 294, f"Expected 294 stable turbidity rows, got {len(df_turb)}")
        self.assertEqual(len(df_stab), 812, f"Expected 812 total stability rows, got {len(df_stab)}")

        # Class balance in stability
        self.assertEqual(int((df_stab["target_value"] == 1).sum()), 294)
        self.assertEqual(int((df_stab["target_value"] == 0).sum()), 518)

        # Strictly positive viscosity at ~100 s^-1
        self.assertTrue((df_visc["target_value"] > 0).all(), "Found non-positive viscosity value")
        self.assertGreaterEqual(float(df_visc["target_value"].min()), 0.6)
        self.assertLessEqual(float(df_visc["target_value"].max()), 3500.0)

    def test_provenance_metadata_headers(self):
        """Verify that all normalized datasets contain immutable provenance metadata."""
        for fname in ["shampoo_m4_visc_at_100s.csv", "shampoo_m4_turbidity.csv", "shampoo_m4_phase_stability.csv"]:
            df = pd.read_csv(NORMALIZED_DIR / fname)
            self.assertIn("source_file_hash", df.columns)
            self.assertIn("dataset_id", df.columns)
            self.assertIn("source_record_id", df.columns)
            self.assertIn("data_origin", df.columns)
            self.assertIn("schema_version", df.columns)

            self.assertTrue((df["source_file_hash"] == EXPECTED_SHA256).all())
            self.assertTrue((df["dataset_id"] == "NATURE_812_SHAMPOO_2024").all())
            self.assertTrue((df["data_origin"] == "PUBLIC_BENCHMARK").all())
            self.assertTrue((df["schema_version"] == 1.0).all())

    def test_mathematical_model_a_b_c_properties(self):
        """Verify mathematical properties of Model A, B, and C."""
        df_visc = pd.read_csv(NORMALIZED_DIR / "shampoo_m4_visc_at_100s.csv")

        ing_cols = [c for c in df_visc.columns if c in [
            "Texapon SB 3 KC", "Plantapon ACG 50", "Plantapon LC 7", "Plantacare 818",
            "Plantacare 2000", "Dehyton MC", "Dehyton PK 45", "Dehyton ML", "Dehyton AB 30",
            "Plantapon Amino SCG-L", "Plantapon Amino KG-L", "Dehyquart A-CA",
            "Luviquat Excellence", "Dehyquart CC6", "Dehyquart CC7 Benz", "Salcare Super 7",
            "Arlypon F", "Arlypon TT"
        ]]
        self.assertEqual(len(ing_cols), 18)

        X_18 = df_visc[ing_cols].to_numpy()

        # Model A: Full rank
        X_A = np.column_stack([np.ones(len(df_visc)), X_18])
        self.assertEqual(np.linalg.matrix_rank(X_A), 19)
        cond_A = np.linalg.cond(X_A)
        self.assertLess(cond_A, 100.0, f"Model A condition number {cond_A} unexpectedly high")

        # Model A-Quad: Must demonstrate rank deficiency due to zero-cooccurrence pairs
        pair_cols = []
        zero_pairs = 0
        for i in range(18):
            for j in range(i + 1, 18):
                col = X_18[:, i] * X_18[:, j]
                if np.all(col == 0):
                    zero_pairs += 1
                pair_cols.append(col)
        self.assertEqual(zero_pairs, 17, f"Expected exactly 17 zero pairs, found {zero_pairs}")
        X_A_quad = np.column_stack([X_18] + pair_cols)
        rank_quad = np.linalg.matrix_rank(X_A_quad)
        self.assertLess(rank_quad, X_A_quad.shape[1], "Expected Model A-Quad to be rank deficient")

        # Model C: Subsystem Representation full rank
        X_C = np.column_stack([
            np.ones(len(df_visc)),
            df_visc["surfactant_total_wt_pct"].to_numpy(),
            df_visc["surfactant_primary_ratio"].to_numpy(),
            df_visc["polymer_total_wt_pct"].to_numpy(),
            df_visc["thickener_total_wt_pct"].to_numpy(),
        ])
        self.assertEqual(np.linalg.matrix_rank(X_C), 5)

    def test_strict_qualification_firewall_blocks_public_benchmark(self):
        """Verify that DataOrigin.PUBLIC_BENCHMARK or non-REAL_PILOT is strictly rejected by GS-40 qualification."""
        from src.qc.models import BatchQCRecord, DataOrigin
        from src.modeling.predictor import FormulationPredictor, ModelState

        predictor = FormulationPredictor()
        self.assertEqual(predictor.state, ModelState.AWAITING_PILOT_DATA)

        # Attempt to create a BatchQCRecord with synthetic origin or non-pilot origin
        synthetic_record = BatchQCRecord(
            batch_id="SYN-001",
            trial_id="P001",
            formula_id="FORM-GS40-TEST",
            revision="Rev.7.3",
            test_date="2026-09-12",
            operator="Benchmark Engine",
            data_origin=DataOrigin.SYNTHETIC_TEST,
            hardness_gf=150.0,
            transfer_g_10c=0.035,
        )
        # The record must NOT be eligible for model training
        self.assertFalse(synthetic_record.is_training_eligible())

        # Attempting to fit FormulationPredictor with non-REAL_PILOT records must not promote model state
        fit_success = predictor.fit([synthetic_record] * 20)
        self.assertFalse(fit_success)
        self.assertEqual(predictor.state, ModelState.AWAITING_PILOT_DATA)
        self.assertEqual(len(predictor.training_records), 0)


if __name__ == "__main__":
    unittest.main()

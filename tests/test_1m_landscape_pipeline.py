"""
GLIDE-SPEC 40 - Automated Unit Tests for 1M Virtual Landscape Parquet Datasets
Verifies:
  1. Existence and schema consistency of all 5 Parquet datasets in virtual_landscape/.
  2. Zone partitioning consistency (Zone A Target, Zone B Boundary, Zone C Uncertainty, Zone D OOD, Zone E Infeasible).
  3. Top 50 candidates CSV export and landscape report Markdown generation.
"""

import unittest
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
VL_DIR = ROOT_DIR / "virtual_landscape"


class Test1MVirtualLandscapePipeline(unittest.TestCase):

    def test_landscape_artifacts_exist(self):
        """Verify all expected parquet datasets and summary report exist."""
        expected_files = [
            VL_DIR / "candidate_summary.parquet",
            VL_DIR / "feasible_candidates.parquet",
            VL_DIR / "specification_zone.parquet",
            VL_DIR / "boundary_zone.parquet",
            VL_DIR / "uncertainty_zone.parquet",
            VL_DIR / "ood_zone.parquet",
            VL_DIR / "top_candidates.csv",
            VL_DIR / "landscape_report.md"
        ]
        for f in expected_files:
            self.assertTrue(f.exists(), f"Missing landscape artifact: {f}")

    def test_candidate_summary_zones(self):
        """Verify candidate_summary.parquet covers all 5 zones."""
        df_sum = pd.read_parquet(VL_DIR / "candidate_summary.parquet")
        self.assertEqual(len(df_sum), 5)
        self.assertIn("zone", df_sum.columns)
        self.assertIn("sample_count", df_sum.columns)
        self.assertIn("share_pct", df_sum.columns)

        zones = df_sum["zone"].tolist()
        self.assertTrue(any("Zone A" in z for z in zones))
        self.assertTrue(any("Zone B" in z for z in zones))
        self.assertTrue(any("Zone C" in z for z in zones))
        self.assertTrue(any("Zone D" in z for z in zones))
        self.assertTrue(any("Zone E" in z for z in zones))

    def test_feasible_candidates_schema(self):
        """Verify feasible_candidates.parquet has all required prediction & OOD fields."""
        df_feas = pd.read_parquet(VL_DIR / "feasible_candidates.parquet")
        self.assertGreater(len(df_feas), 100)

        required_cols = [
            "candidate_id", "syn_wax_pct", "can_wax_pct", "dimethicone_pct",
            "pred_hardness_gf", "hardness_pi_lower", "hardness_pi_upper",
            "pred_transfer_g", "pred_drop_point_c", "composite_ood_score", "assigned_zone"
        ]
        for col in required_cols:
            self.assertIn(col, df_feas.columns, f"Missing required column: {col}")

    def test_top_candidates_csv(self):
        """Verify top_candidates.csv contains 50 ranked candidates."""
        df_top = pd.read_csv(VL_DIR / "top_candidates.csv")
        self.assertEqual(len(df_top), 50)
        self.assertIn("candidate_id", df_top.columns)
        self.assertIn("pred_hardness_gf", df_top.columns)


if __name__ == "__main__":
    unittest.main()

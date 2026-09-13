"""
GLIDE-SPEC 40 - Automated Unit Tests for Virtual Generator & Active Learning EIG Ranker
Verifies 10,000-candidate virtual generation, mixture mass balance,
physical feasibility filters, and EIG utility ranking.
"""

import unittest
from pathlib import Path
import numpy as np

from src.doe.virtual_generator import VirtualFormulationGenerator, VirtualCandidate
from scripts.rank_active_learning_runs import (
    load_planned_pilot_runs, train_baseline_surrogate, rank_runs_by_information_gain
)


class TestVirtualGeneratorAndActiveLearning(unittest.TestCase):

    def test_virtual_formulation_generator(self):
        # Generate 500 candidates
        candidates = VirtualFormulationGenerator.generate_candidates(n_samples=500, random_seed=42)
        self.assertEqual(len(candidates), 500)

        # Verify mass balance and constraints on feasible candidates
        feasible_count = sum(1 for c in candidates if c.is_feasible)
        self.assertGreater(feasible_count, 100, "Should have a healthy yield of physically feasible candidates")

        for c in candidates:
            w = c.weights
            total_mass = sum(w.values())
            self.assertAlmostEqual(total_mass, 100.0, places=1, msg="Formulation total mass must sum to 100%")

            wax_sum = w["Synthetic Wax"] + w["Candelilla Wax"]
            self.assertAlmostEqual(wax_sum, 17.0, places=1, msg="Wax sum must be 17.0%")

            if c.is_feasible:
                # Feasible checks
                self.assertGreaterEqual(w["Silica Dimethyl Silylate"], 1.5)
                self.assertLessEqual(c.feature_vector.solid_volume_fraction, 0.40)
                self.assertGreaterEqual(c.feature_vector.binder_to_powder_weight_ratio, 1.50)

    def test_active_learning_eig_ranking(self):
        root_dir = Path(__file__).resolve().parent.parent
        matrix_csv = root_dir / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"

        runs = load_planned_pilot_runs(matrix_csv)
        self.assertEqual(len(runs), 18)

        surrogate = train_baseline_surrogate()
        ranked = rank_runs_by_information_gain(runs, surrogate)
        self.assertEqual(len(ranked), 18)

        # Highest EIG run should be at the top
        self.assertGreaterEqual(ranked[0]["eig_score"], ranked[-1]["eig_score"])
        # Center points should have lower leverage/EIG than boundary vertices
        center_scores = [r["eig_score"] for r in ranked if r["is_center"]]
        vertex_scores = [r["eig_score"] for r in ranked if "Vertex" in r["design_type"]]
        self.assertLess(np.mean(center_scores), np.mean(vertex_scores))


if __name__ == "__main__":
    unittest.main()

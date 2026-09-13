"""
GLIDE-SPEC 40 - Composite Out-of-Domain (OOD) Detection Engine
Combines 4 orthogonal domain boundary signals:
  1. Mahalanobis Distance (Covariance-adjusted global distance)
  2. k-Nearest Neighbors (kNN) Local Density Distance
  3. Ensemble Model Disagreement (Epistemic uncertainty across surrogate architectures)
  4. Hyperbox Bounding Range Violations (Extrapolation beyond empirical feature limits)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional
import numpy as np
from scipy.spatial.distance import mahalanobis, cdist


class CompositeOODCategory(str, Enum):
    IN_DOMAIN = "IN_DOMAIN"             # High confidence, safe for virtual screening
    BOUNDARY_ZONE = "BOUNDARY_ZONE"     # Specification edge or moderate extrapolation
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"     # Significant extrapolation, mandatory testing


@dataclass
class CompositeOODResult:
    composite_score: float              # Normalized index: 0.0 (center) to 1.0+ (extreme OOD)
    category: CompositeOODCategory
    mahalanobis_distance: float
    knn_mean_distance: float
    ensemble_disagreement_cv: float
    box_violation_count: int
    box_violation_max_pct: float
    details: Dict[str, Any]


class CompositeOODDetector:
    """
    Evaluates new formulations against empirical training envelope across 4 dimensions.
    """

    def __init__(self, k_neighbors: int = 3):
        self.k_neighbors = k_neighbors
        self.train_X: Optional[np.ndarray] = None
        self.train_mean: Optional[np.ndarray] = None
        self.inv_cov: Optional[np.ndarray] = None
        self.feature_mins: Optional[np.ndarray] = None
        self.feature_maxs: Optional[np.ndarray] = None
        self.knn_baseline_dist: float = 1.0
        self.mahal_baseline_dist: float = 1.0
        self.is_fitted = False

    def fit(self, X: np.ndarray):
        """Calibrates distance baselines and covariance structure from training data."""
        self.train_X = np.copy(X)
        self.train_mean = np.mean(X, axis=0)
        self.feature_mins = np.min(X, axis=0)
        self.feature_maxs = np.max(X, axis=0)
        self.feature_stds = np.std(X, axis=0)

        cov = np.cov(X, rowvar=False)
        cov_reg = cov + np.eye(cov.shape[0]) * 1e-4
        self.inv_cov = np.linalg.pinv(cov_reg)

        # Baseline Mahalanobis 90th percentile
        m_dists = [mahalanobis(x, self.train_mean, self.inv_cov) for x in X]
        self.mahal_baseline_dist = float(np.percentile(m_dists, 90)) if len(m_dists) > 0 else 1.0
        if self.mahal_baseline_dist <= 0:
            self.mahal_baseline_dist = 1.0

        # Baseline kNN distances within training data
        pw_dists = cdist(X, X, metric="euclidean")
        np.fill_diagonal(pw_dists, np.inf)
        k = min(self.k_neighbors, len(X) - 1)
        knn_dists = [np.mean(np.sort(row)[:k]) for row in pw_dists]
        self.knn_baseline_dist = float(np.percentile(knn_dists, 90)) if len(knn_dists) > 0 else 1.0
        if self.knn_baseline_dist <= 0:
            self.knn_baseline_dist = 1.0

        self.is_fitted = True

    def evaluate(
        self,
        x_feature_array: np.ndarray,
        ensemble_predictions: Optional[Dict[str, float]] = None
    ) -> CompositeOODResult:
        if not self.is_fitted:
            raise RuntimeError("CompositeOODDetector must be fitted before evaluation.")

        x = x_feature_array.flatten()

        # 1. Mahalanobis Distance
        d_m = float(mahalanobis(x, self.train_mean, self.inv_cov))
        norm_m = d_m / self.mahal_baseline_dist

        # 2. kNN Distance
        dists = cdist(x.reshape(1, -1), self.train_X, metric="euclidean")[0]
        k = min(self.k_neighbors, len(self.train_X))
        knn_dist = float(np.mean(np.sort(dists)[:k]))
        norm_knn = knn_dist / self.knn_baseline_dist

        # 3. Ensemble Model Disagreement
        if ensemble_predictions and len(ensemble_predictions) > 1:
            vals = list(ensemble_predictions.values())
            m_val = float(np.mean(vals))
            s_val = float(np.std(vals, ddof=1))
            disagreement_cv = (s_val / abs(m_val)) if abs(m_val) > 1e-4 else 0.0
        else:
            disagreement_cv = 0.0
        norm_disagree = min(3.0, disagreement_cv / 0.15)  # 15% CV considered high disagreement

        # 4. Hyperbox Bounding Range Violations (Physically Normalized)
        below = np.maximum(0.0, self.feature_mins - x)
        above = np.maximum(0.0, x - self.feature_maxs)
        ranges = np.maximum(
            self.feature_maxs - self.feature_mins,
            np.maximum(self.feature_stds * 2.0, np.maximum(1.0, 0.10 * np.abs(self.train_mean)))
        )
        rel_violations = (below + above) / ranges
        box_violations_count = int(np.sum(rel_violations > 0.05))
        max_violation_pct = float(np.max(rel_violations)) * 100.0 if len(rel_violations) > 0 else 0.0
        norm_box = min(3.0, max_violation_pct / 25.0)

        # Composite Score (weighted combination)
        # Weights: Mahalanobis 35%, kNN 35%, Disagreement 15%, Box 15%
        composite = (
            0.35 * min(3.0, norm_m) +
            0.35 * min(3.0, norm_knn) +
            0.15 * norm_disagree +
            0.15 * norm_box
        )
        # Scale into normalized index (1.0 = baseline 90th percentile)
        composite_index = round(float(composite), 3)

        if composite_index <= 1.0:
            category = CompositeOODCategory.IN_DOMAIN
        elif composite_index <= 1.75:
            category = CompositeOODCategory.BOUNDARY_ZONE
        else:
            category = CompositeOODCategory.OUT_OF_DOMAIN

        return CompositeOODResult(
            composite_score=composite_index,
            category=category,
            mahalanobis_distance=round(d_m, 2),
            knn_mean_distance=round(knn_dist, 2),
            ensemble_disagreement_cv=round(disagreement_cv * 100.0, 2),
            box_violation_count=box_violations_count,
            box_violation_max_pct=round(max_violation_pct, 1),
            details={
                "norm_mahalanobis": round(norm_m, 2),
                "norm_knn": round(norm_knn, 2),
                "norm_disagreement": round(norm_disagree, 2),
                "norm_box_violation": round(norm_box, 2)
            }
        )

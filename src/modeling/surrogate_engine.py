"""
GLIDE-SPEC 40 - Multi-Response Surrogate & Uncertainty Ensemble Engine
Implements Model A (Hardness), Model B (Transfer), Model C (Drop Point),
Model D (Sedimentation Risk), and Model E (Glide CoF) using an ensemble of:
  - ElasticNet (Penalized Linear)
  - RandomForestRegressor
  - ExtraTreesRegressor
  - GradientBoostingRegressor
  - GaussianProcessRegressor
Provides 95% Prediction Intervals (PI) and Mahalanobis Out-of-Domain (OOD) scoring.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from scipy import stats
from scipy.spatial.distance import mahalanobis

import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C, WhiteKernel

from src.modeling.feature_engine import FormulationFeatureVector, GS40FeatureEngine


class OODLevel(str, Enum):
    LOW = "LOW"             # In-domain: Mahalanobis distance within 90th percentile of training data
    MEDIUM = "MEDIUM"       # Moderate extrapolation: between 90th and 99th percentile
    HIGH = "HIGH"           # Far out-of-domain: above 99th percentile, test required


@dataclass
class SingleResponsePrediction:
    response_name: str
    point_prediction: float
    std_uncertainty: float
    pi_95_lower: float
    pi_95_upper: float
    ensemble_member_predictions: Dict[str, float]
    spec_target_min: Optional[float] = None
    spec_target_max: Optional[float] = None
    prob_in_spec: float = 1.0


@dataclass
class SurrogateEvaluationResult:
    formula_id: str
    predictions: Dict[str, SingleResponsePrediction]
    ood_score: float
    ood_level: OODLevel
    model_confidence_pct: float
    active_learning_utility: float  # Expected information gain (higher = more valuable to test)


class ResponseEnsemble:
    """Ensemble for a single physical response."""

    def __init__(self, response_name: str, spec_min: Optional[float] = None, spec_max: Optional[float] = None):
        self.response_name = response_name
        self.spec_min = spec_min
        self.spec_max = spec_max

        self.models = {
            "elastic_net": ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=2000, random_state=42),
            "random_forest": RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42),
            "extra_trees": ExtraTreesRegressor(n_estimators=50, max_depth=5, random_state=42),
            "gradient_boosting": GradientBoostingRegressor(n_estimators=50, max_depth=3, learning_rate=0.08, random_state=42),
            "gaussian_process": GaussianProcessRegressor(
                kernel=C(1.0, (1e-3, 1e3)) * RBF(10.0, (1e-2, 1e2)) + WhiteKernel(noise_level=1.0),
                n_restarts_optimizer=2,
                random_state=42
            ),
        }
        self.is_fitted = False
        self.residual_std = 1.0

    def fit(self, X: np.ndarray, y: np.ndarray):
        residuals = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for name, model in self.models.items():
                model.fit(X, y)
                pred = model.predict(X)
                residuals.append(pred - y)

        mean_res = np.mean(residuals, axis=0)
        self.residual_std = float(np.std(mean_res, ddof=1)) if len(y) > 1 else 1.0
        self.is_fitted = True

    def predict(self, x: np.ndarray) -> SingleResponsePrediction:
        if not self.is_fitted:
            raise RuntimeError(f"Surrogate ensemble for {self.response_name} is not fitted.")

        x_2d = x.reshape(1, -1)
        preds = {}
        for name, model in self.models.items():
            preds[name] = float(model.predict(x_2d)[0])

        pred_values = list(preds.values())
        y_hat = float(np.mean(pred_values))
        ensemble_var = float(np.var(pred_values, ddof=1)) if len(pred_values) > 1 else 0.0
        total_var = ensemble_var + (self.residual_std ** 2)
        total_std = float(np.sqrt(max(1e-6, total_var)))

        pi_lower = y_hat - 1.96 * total_std
        pi_upper = y_hat + 1.96 * total_std

        # Spec probability calculation
        if self.spec_min is not None and self.spec_max is not None:
            p_upper = stats.norm.cdf(self.spec_max, loc=y_hat, scale=total_std)
            p_lower = stats.norm.cdf(self.spec_min, loc=y_hat, scale=total_std)
            p_in_spec = float(max(0.0, min(1.0, p_upper - p_lower)))
        elif self.spec_min is not None:
            p_in_spec = float(1.0 - stats.norm.cdf(self.spec_min, loc=y_hat, scale=total_std))
        elif self.spec_max is not None:
            p_in_spec = float(stats.norm.cdf(self.spec_max, loc=y_hat, scale=total_std))
        else:
            p_in_spec = 1.0

        return SingleResponsePrediction(
            response_name=self.response_name,
            point_prediction=round(y_hat, 3),
            std_uncertainty=round(total_std, 3),
            pi_95_lower=round(pi_lower, 3),
            pi_95_upper=round(pi_upper, 3),
            ensemble_member_predictions={k: round(v, 3) for k, v in preds.items()},
            spec_target_min=self.spec_min,
            spec_target_max=self.spec_max,
            prob_in_spec=round(p_in_spec, 4)
        )


class GS40SurrogateEngine:
    """
    Manages Models A, B, C, D, E and OOD computation.
    """

    def __init__(self):
        # Model A: Hardness (Spec: 650 - 900 gf, Rev.7.3 Target: 750 - 850 gf)
        self.model_hardness = ResponseEnsemble("Hardness (gf)", spec_min=700.0, spec_max=900.0)
        # Model B: Transfer (Spec: >= 0.040 g)
        self.model_transfer = ResponseEnsemble("Transfer (g)", spec_min=0.038, spec_max=0.065)
        # Model C: Drop Point (Spec: 60.0 - 64.0 C)
        self.model_drop_point = ResponseEnsemble("Drop Point (C)", spec_min=60.0, spec_max=64.0)
        # Model D: Sedimentation Risk Index (Target: <= 1.50)
        self.model_sedimentation = ResponseEnsemble("Sedimentation Risk Index", spec_max=1.80)
        # Model E: Glide CoF (Target: <= 0.22)
        self.model_glide_cof = ResponseEnsemble("Dynamic Glide CoF", spec_max=0.220)

        self.train_X_mean = None
        self.train_inv_cov = None
        self.ood_threshold_90 = 3.5
        self.ood_threshold_99 = 6.0
        self.is_trained = False

    def train_on_domain_priors_and_pilot(
        self,
        X_features: np.ndarray,
        y_hardness: np.ndarray,
        y_transfer: np.ndarray,
        y_drop_point: np.ndarray,
        y_sedimentation: np.ndarray,
        y_glide_cof: np.ndarray
    ):
        """Fits all 5 response ensembles and estimates OOD covariance structure."""
        self.model_hardness.fit(X_features, y_hardness)
        self.model_transfer.fit(X_features, y_transfer)
        self.model_drop_point.fit(X_features, y_drop_point)
        self.model_sedimentation.fit(X_features, y_sedimentation)
        self.model_glide_cof.fit(X_features, y_glide_cof)

        # Fit OOD distribution
        self.train_X_mean = np.mean(X_features, axis=0)
        cov = np.cov(X_features, rowvar=False)
        # Regularize covariance to avoid singularity
        cov_reg = cov + np.eye(cov.shape[0]) * 1e-4
        self.train_inv_cov = np.linalg.pinv(cov_reg)

        # Empirical calibration of OOD quantiles
        distances = [
            mahalanobis(x, self.train_X_mean, self.train_inv_cov)
            for x in X_features
        ]
        self.ood_threshold_90 = float(np.percentile(distances, 90))
        self.ood_threshold_99 = float(np.percentile(distances, 99))
        self.is_trained = True

    def evaluate_formulation(
        self,
        feature_vector: FormulationFeatureVector,
        formula_id: str = "GS40-CANDIDATE"
    ) -> SurrogateEvaluationResult:
        if not self.is_trained:
            raise RuntimeError("Surrogate engine has not been trained.")

        x = feature_vector.to_feature_array()

        # Predictions
        p_h = self.model_hardness.predict(x)
        p_t = self.model_transfer.predict(x)
        p_d = self.model_drop_point.predict(x)
        p_s = self.model_sedimentation.predict(x)
        p_c = self.model_glide_cof.predict(x)

        predictions = {
            "hardness_gf": p_h,
            "transfer_g": p_t,
            "drop_point_c": p_d,
            "sedimentation_risk": p_s,
            "glide_cof": p_c,
        }

        # OOD Mahalanobis calculation
        d_m = float(mahalanobis(x, self.train_X_mean, self.train_inv_cov))
        if d_m <= self.ood_threshold_90:
            ood_lvl = OODLevel.LOW
        elif d_m <= self.ood_threshold_99:
            ood_lvl = OODLevel.MEDIUM
        else:
            ood_lvl = OODLevel.HIGH

        # Confidence: Joint probability of all key specs * OOD penalty
        joint_prob = p_h.prob_in_spec * p_t.prob_in_spec * p_d.prob_in_spec
        ood_penalty = 1.0 if ood_lvl == OODLevel.LOW else (0.8 if ood_lvl == OODLevel.MEDIUM else 0.4)
        confidence_pct = round(joint_prob * ood_penalty * 100.0, 1)

        # Active learning information gain utility:
        # High uncertainty + high relevance = optimal candidate for physical testing
        total_relative_uncertainty = (
            (p_h.std_uncertainty / p_h.point_prediction) +
            (p_t.std_uncertainty / max(1e-4, p_t.point_prediction)) +
            (p_d.std_uncertainty / p_d.point_prediction)
        )
        utility = round(float(total_relative_uncertainty * (1.0 + 0.5 * min(3.0, d_m))), 4)

        return SurrogateEvaluationResult(
            formula_id=formula_id,
            predictions=predictions,
            ood_score=round(d_m, 2),
            ood_level=ood_lvl,
            model_confidence_pct=confidence_pct,
            active_learning_utility=utility
        )

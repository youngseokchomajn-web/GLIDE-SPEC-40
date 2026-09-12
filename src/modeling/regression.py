"""
GLIDE-SPEC 40 - Multivariate Mixture & Process Regression Engine (M4)
Fits empirical response surfaces for constrained Wax-Silicone mixture systems
and process conditions using Ordinary Least Squares (OLS) with LOOCV validation.
"""

from typing import List, Dict, Tuple, Optional
import numpy as np
from pydantic import BaseModel


class RegressionMetrics(BaseModel):
    r_squared: float
    rmse: float
    loocv_rmse: float
    sample_count: int
    feature_names: List[str]
    coefficients: List[float]
    intercept: float
    u1_range: Tuple[float, float]
    v1_range: Tuple[float, float]
    temp_range: Tuple[float, float]


class MixtureRegressionModel:
    """
    Multivariate OLS Regression for GLIDE-SPEC 40 formulation space:
    Inputs:
      - u1: Synthetic Wax share in Wax System = SynWax% / 17.0 (range ~ [0.529, 0.882])
      - v1: Dimethicone share in Silicone System = Dimethicone% / 28.0 (range ~ [0.428, 0.786])
      - T: Fill Temperature (°C) (range ~ [70.0, 90.0])
    Avoids collinearity of fitting all 4 percentage terms directly.
    """

    def __init__(self, target_name: str):
        self.target_name = target_name
        self.metrics: Optional[RegressionMetrics] = None
        self._beta: Optional[np.ndarray] = None
        self._residual_variance: float = 0.0

    @classmethod
    def extract_features(cls, syn_wax: float, dimethicone: float, fill_temp: float) -> Tuple[float, float, float]:
        u1 = syn_wax / 17.0
        v1 = dimethicone / 28.0
        return u1, v1, fill_temp

    def fit(self, X: np.ndarray, y: np.ndarray) -> RegressionMetrics:
        """
        Fits linear model: y = b0 + b1*u1 + b2*v1 + b3*T
        X shape: (N, 3), y shape: (N,)
        Computes R2, RMSE, and Leave-One-Out Cross-Validation (LOOCV).
        """
        N = X.shape[0]
        if N < 4:
            raise ValueError(f"At least 4 observations required to fit linear model with 3 features, got {N}")

        # Design matrix with intercept column
        X_design = np.column_stack([np.ones(N), X])  # shape: (N, 4)

        # OLS fit via pseudo-inverse/least squares
        beta, residuals, rank, s = np.linalg.lstsq(X_design, y, rcond=None)
        self._beta = beta

        # Predictions on training data
        y_pred = X_design @ beta
        errors = y - y_pred
        sse = float(np.sum(errors ** 2))
        sst = float(np.sum((y - np.mean(y)) ** 2))
        r2 = 1.0 - (sse / sst) if sst > 1e-12 else 0.0
        rmse = float(np.sqrt(sse / N))
        self._residual_variance = sse / max(1, N - 4)

        # Leave-One-Out Cross-Validation (LOOCV) analytical shortcut using hat matrix
        # e_loo_i = e_i / (1 - h_ii)
        H = X_design @ np.linalg.pinv(X_design.T @ X_design) @ X_design.T
        h_ii = np.diag(H)
        loo_errors = errors / np.clip(1.0 - h_ii, 1e-6, 1.0)
        loocv_rmse = float(np.sqrt(np.mean(loo_errors ** 2)))

        self.metrics = RegressionMetrics(
            r_squared=round(r2, 4),
            rmse=round(rmse, 4),
            loocv_rmse=round(loocv_rmse, 4),
            sample_count=N,
            feature_names=["u1_syn_wax_share", "v1_dimethicone_share", "fill_temp_c"],
            coefficients=[round(float(b), 4) for b in beta[1:]],
            intercept=round(float(beta[0]), 4),
            u1_range=(round(float(np.min(X[:, 0])), 3), round(float(np.max(X[:, 0])), 3)),
            v1_range=(round(float(np.min(X[:, 1])), 3), round(float(np.max(X[:, 1])), 3)),
            temp_range=(round(float(np.min(X[:, 2])), 1), round(float(np.max(X[:, 2])), 1))
        )
        return self.metrics

    def predict(self, syn_wax: float, dimethicone: float, fill_temp: float) -> Tuple[float, float]:
        """Returns (predicted_value, 95% prediction interval half-width)."""
        if self._beta is None:
            raise RuntimeError("Model is not fitted.")

        u1, v1, T = self.extract_features(syn_wax, dimethicone, fill_temp)
        x_vec = np.array([1.0, u1, v1, T])
        pred_val = float(x_vec @ self._beta)

        # 95% prediction interval approximation (1.96 * sqrt(s2))
        margin = 1.96 * np.sqrt(self._residual_variance)
        return round(pred_val, 3), round(margin, 3)

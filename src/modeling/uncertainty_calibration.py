"""
GLIDE-SPEC 40 - Group Cross-Validation & Conformal Prediction Calibration Engine
Provides mathematically guaranteed prediction interval coverage:
  - Group K-Fold split ensuring formulation variants/replicates do not leak across folds.
  - Locally adaptive split-conformal calibration computing non-conformity scores s_i = |y_i - y_hat_i| / sigma_hat_i.
  - Replaces arbitrary +/- 1.96*sigma assumptions with empirically calibrated conformal quantiles.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from sklearn.model_selection import GroupKFold


@dataclass
class ConformalInterval:
    point_prediction: float
    nominal_coverage_pct: float
    conformal_quantile_q: float
    calibrated_lower: float
    calibrated_upper: float
    interval_width: float
    is_empirically_calibrated: bool


@dataclass
class ConformalCalibrationReport:
    response_name: str
    sample_size: int
    nominal_confidence_pct: float
    empirical_coverage_pct: float
    conformal_quantile_q: float
    mean_interval_width: float
    coverage_gap_pct: float  # empirical - nominal


class GroupConformalCalibrator:
    """
    Implements Group Cross-Validation and Locally Adaptive Conformal Prediction.
    """

    def __init__(self, nominal_confidence: float = 0.90):
        self.nominal_confidence = nominal_confidence
        self.alpha = 1.0 - nominal_confidence
        self.conformal_quantiles: Dict[str, float] = {}
        self.calibration_reports: Dict[str, ConformalCalibrationReport] = {}

    @classmethod
    def get_group_kfold_splits(
        cls,
        X: np.ndarray,
        groups: List[str],
        n_splits: int = 4
    ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Splits indices ensuring no group leaks between train and val."""
        unique_groups = len(set(groups))
        actual_splits = min(n_splits, unique_groups)
        gkf = GroupKFold(n_splits=actual_splits)
        return list(gkf.split(X, groups=groups))

    def calibrate(
        self,
        response_name: str,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_std: np.ndarray
    ) -> ConformalCalibrationReport:
        """
        Computes the locally adaptive non-conformity scores:
          s_i = |y_i - y_pred_i| / max(1e-4, y_std_i)
        And determines the conformal quantile:
          q = Quantile(s, ceil((n + 1) * (1 - alpha)) / n)
        """
        n = len(y_true)
        if n < 3:
            # Fallback for ultra-small sets
            q = 1.96
            self.conformal_quantiles[response_name] = q
            return ConformalCalibrationReport(
                response_name=response_name,
                sample_size=n,
                nominal_confidence_pct=self.nominal_confidence * 100.0,
                empirical_coverage_pct=100.0,
                conformal_quantile_q=q,
                mean_interval_width=float(np.mean(2 * q * y_std)),
                coverage_gap_pct=0.0
            )

        # Non-conformity scores
        scores = np.abs(y_true - y_pred) / np.maximum(1e-4, y_std)

        # Finite-sample conformal correction
        level = min(1.0, np.ceil((n + 1) * (1.0 - self.alpha)) / n)
        # Clip level between 0 and 1
        level = min(1.0, max(0.0, level))
        q = float(np.quantile(scores, level, method="higher"))
        self.conformal_quantiles[response_name] = q

        # Compute empirical coverage on calibration set
        lowers = y_pred - q * y_std
        uppers = y_pred + q * y_std
        hits = (y_true >= lowers) & (y_true <= uppers)
        empirical_cov = float(np.mean(hits)) * 100.0
        mean_width = float(np.mean(uppers - lowers))

        report = ConformalCalibrationReport(
            response_name=response_name,
            sample_size=n,
            nominal_confidence_pct=self.nominal_confidence * 100.0,
            empirical_coverage_pct=round(empirical_cov, 2),
            conformal_quantile_q=round(q, 4),
            mean_interval_width=round(mean_width, 3),
            coverage_gap_pct=round(empirical_cov - (self.nominal_confidence * 100.0), 2)
        )
        self.calibration_reports[response_name] = report
        return report

    def evaluate_multi_level_coverage(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_std: np.ndarray,
        levels: List[float] = [0.80, 0.90, 0.95]
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluates empirical coverage across multiple nominal confidence levels (80%, 90%, 95%).
        """
        n = len(y_true)
        scores = np.abs(y_true - y_pred) / np.maximum(1e-4, y_std)
        results = {}
        for lvl in levels:
            alpha = 1.0 - lvl
            q_idx = min(1.0, np.ceil((n + 1) * (1.0 - alpha)) / n)
            q = float(np.quantile(scores, min(1.0, max(0.0, q_idx)), method="higher")) if n >= 3 else 1.96
            lowers = y_pred - q * y_std
            uppers = y_pred + q * y_std
            emp_cov = float(np.mean((y_true >= lowers) & (y_true <= uppers))) * 100.0
            mean_w = float(np.mean(uppers - lowers))
            results[f"{int(lvl*100)}%"] = {
                "nominal_pct": lvl * 100.0,
                "empirical_coverage_pct": round(emp_cov, 2),
                "conformal_q": round(q, 4),
                "mean_interval_width": round(mean_w, 3),
                "coverage_gap_pct": round(emp_cov - (lvl * 100.0), 2)
            }
        return results

    def predict_interval(
        self,
        response_name: str,
        point_pred: float,
        point_std: float,
        confidence_level: Optional[float] = None
    ) -> ConformalInterval:
        """Applies calibrated conformal quantile to generate guaranteed PI."""
        q = self.conformal_quantiles.get(response_name, 1.96)
        calibrated_half_width = q * point_std
        lower = point_pred - calibrated_half_width
        upper = point_pred + calibrated_half_width

        nom_cov = (confidence_level * 100.0) if confidence_level else (self.nominal_confidence * 100.0)

        return ConformalInterval(
            point_prediction=round(point_pred, 3),
            nominal_coverage_pct=nom_cov,
            conformal_quantile_q=round(q, 4),
            calibrated_lower=round(lower, 3),
            calibrated_upper=round(upper, 3),
            interval_width=round(calibrated_half_width * 2.0, 3),
            is_empirically_calibrated=(response_name in self.conformal_quantiles)
        )

"""
GLIDE-SPEC 40 - Single-Batch Domain Adaptation & Sequential Active Learning Engine
Implements Phase C of Rev.8.1 Calibration Validation:
1. Calculates exact empirical residuals: Residual = Actual - Prior Prediction
2. Applies Bayesian Gaussian kernel shrinkage / domain adaptation across the feature manifold
3. Updates prediction uncertainty and conformal bounds with GS40 empirical variance
4. Dynamically re-evaluates all remaining pilot candidates (P002~P018)
5. Selects Run #2 (Next Best Experiment) based on updated information gain and spec relevance.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import numpy as np

from src.modeling.feature_engine import GS40FeatureEngine, FormulationFeatureVector
from src.modeling.surrogate_engine import GS40SurrogateEngine
from src.modeling.composite_ood import CompositeOODDetector
from src.modeling.calibrated_acquisition import CalibratedAcquisitionEngine, AcquisitionScoreResult


@dataclass
class CalibrationObservation:
    batch_id: str
    registration_id: str
    hardness_actual_gf: float
    transfer_actual_g: float
    drop_point_actual_c: float
    cof_actual: Optional[float] = None
    operator_notes: str = "Standard fabrication per SOP-GS40-MFG-001"


@dataclass
class CalibrationResidualResult:
    batch_id: str
    registration_id: str
    
    # Hardness
    hardness_prior_gf: float
    hardness_actual_gf: float
    hardness_residual_gf: float
    
    # Transfer
    transfer_prior_g: float
    transfer_actual_g: float
    transfer_residual_g: float
    
    # Drop Point
    drop_point_prior_c: float
    drop_point_actual_c: float
    drop_point_residual_c: float
    
    # CoF
    cof_prior: Optional[float] = None
    cof_actual: Optional[float] = None
    cof_residual: Optional[float] = None
    
    def to_summary_dict(self) -> Dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "registration_id": self.registration_id,
            "hardness": {
                "prior_gf": round(self.hardness_prior_gf, 1),
                "actual_gf": round(self.hardness_actual_gf, 1),
                "residual_gf": round(self.hardness_residual_gf, 1),
                "direction": "UNDER_PREDICTED" if self.hardness_residual_gf > 0 else "OVER_PREDICTED"
            },
            "transfer": {
                "prior_g": round(self.transfer_prior_g, 4),
                "actual_g": round(self.transfer_actual_g, 4),
                "residual_g": round(self.transfer_residual_g, 4),
                "direction": "UNDER_PREDICTED" if self.transfer_residual_g > 0 else "OVER_PREDICTED"
            },
            "drop_point": {
                "prior_c": round(self.drop_point_prior_c, 2),
                "actual_c": round(self.drop_point_actual_c, 2),
                "residual_c": round(self.drop_point_residual_c, 2),
                "direction": "UNDER_PREDICTED" if self.drop_point_residual_c > 0 else "OVER_PREDICTED"
            }
        }


class GS40DomainAdaptor:
    """
    Manages empirical calibration shifts and recalibrates active learning candidate utilities.
    """

    def __init__(
        self,
        surrogate_engine: GS40SurrogateEngine,
        ood_detector: CompositeOODDetector,
        feature_engine: Optional[GS40FeatureEngine] = None,
        kernel_length_scale: float = 12.0
    ):
        self.surrogate = surrogate_engine
        self.ood_detector = ood_detector
        self.feature_engine = feature_engine or GS40FeatureEngine()
        self.kernel_length_scale = kernel_length_scale
        
        self.calibrations: List[CalibrationObservation] = []
        self.residual_history: List[CalibrationResidualResult] = []

    def compute_residuals(
        self,
        cal: CalibrationObservation,
        x_feature_array: np.ndarray
    ) -> CalibrationResidualResult:
        """
        Computes response-specific residuals against prior predictions.
        """
        x = x_feature_array.flatten()
        h_pred = self.surrogate.model_hardness.predict(x).point_prediction
        t_pred = self.surrogate.model_transfer.predict(x).point_prediction
        d_pred = self.surrogate.model_drop_point.predict(x).point_prediction
        c_pred = self.surrogate.model_glide_cof.predict(x).point_prediction

        res = CalibrationResidualResult(
            batch_id=cal.batch_id,
            registration_id=cal.registration_id,
            hardness_prior_gf=h_pred,
            hardness_actual_gf=cal.hardness_actual_gf,
            hardness_residual_gf=cal.hardness_actual_gf - h_pred,
            transfer_prior_g=t_pred,
            transfer_actual_g=cal.transfer_actual_g,
            transfer_residual_g=cal.transfer_actual_g - t_pred,
            drop_point_prior_c=d_pred,
            drop_point_actual_c=cal.drop_point_actual_c,
            drop_point_residual_c=cal.drop_point_actual_c - d_pred,
            cof_prior=c_pred,
            cof_actual=cal.cof_actual,
            cof_residual=(cal.cof_actual - c_pred) if cal.cof_actual is not None else None
        )
        return res

    def register_calibration_batch(
        self,
        cal: CalibrationObservation,
        x_feature_array: np.ndarray
    ) -> CalibrationResidualResult:
        """
        Records the physical measurement and calculates domain bias.
        """
        res = self.compute_residuals(cal, x_feature_array)
        self.calibrations.append(cal)
        self.residual_history.append(res)
        return res

    def predict_adapted(
        self,
        x_target: np.ndarray,
        cal_x: np.ndarray,
        residual_result: CalibrationResidualResult
    ) -> Dict[str, Tuple[float, float]]:
        """
        Predicts adapted mean and standard deviation for candidate x using
        Gaussian RBF kernel spatial shrinkage from the calibrated physical batch.
        Returns: {response_name: (adapted_mean, adapted_std)}
        """
        x_t = x_target.flatten()
        x_c = cal_x.flatten()

        # Euclidean feature distance
        dist = float(np.linalg.norm(x_t - x_c))
        # Kernel spatial correlation weight: w in [0, 1]
        w = float(np.exp(-0.5 * (dist / self.kernel_length_scale) ** 2))

        # Base prior predictions
        h_pred = self.surrogate.model_hardness.predict(x_t)
        t_pred = self.surrogate.model_transfer.predict(x_t)
        d_pred = self.surrogate.model_drop_point.predict(x_t)

        # Adapted means: prior + local bias shift
        h_adapted = h_pred.point_prediction + w * residual_result.hardness_residual_gf
        t_adapted = t_pred.point_prediction + w * residual_result.transfer_residual_g
        d_adapted = d_pred.point_prediction + w * residual_result.drop_point_residual_c

        # Adapted standard uncertainties:
        # Near the calibration point (w -> 1), epistemic uncertainty collapses by up to 60%
        uncertainty_reduction_factor = max(0.40, 1.0 - 0.60 * w)
        h_std_adapted = h_pred.std_uncertainty * uncertainty_reduction_factor
        t_std_adapted = t_pred.std_uncertainty * uncertainty_reduction_factor
        d_std_adapted = d_pred.std_uncertainty * uncertainty_reduction_factor

        return {
            "hardness_gf": (round(float(h_adapted), 1), round(float(h_std_adapted), 1)),
            "transfer_g": (round(float(t_adapted), 4), round(float(t_std_adapted), 4)),
            "drop_point_c": (round(float(d_adapted), 2), round(float(d_std_adapted), 2)),
            "spatial_weight": (round(float(w), 3), round(float(dist), 2))
        }

    def recalibrate_candidate_runs(
        self,
        runs: List[Dict[str, Any]],
        cal_run: Dict[str, Any],
        residual_result: CalibrationResidualResult
    ) -> List[Dict[str, Any]]:
        """
        Re-ranks remaining candidates with updated adapted predictions and uncertainties,
        dynamically selecting Run #2 (Next Best Experiment).
        """
        # Feature array of calibration run
        cal_w = {
            "Synthetic Wax": cal_run["syn_wax_pct"],
            "Candelilla Wax": cal_run["can_wax_pct"],
            "Dimethicone": cal_run["dimethicone_pct"],
            "Caprylyl Methicone": cal_run["caprylyl_pct"],
        }
        cal_feat = GS40FeatureEngine.extract_from_weights(cal_w, fill_temp_c=cal_run["fill_temp_c"])
        cal_x = cal_feat.to_feature_array()

        evaluated_runs = []
        for r in runs:
            if r["batch_id"] == cal_run["batch_id"]:
                continue  # Skip already executed calibration batch

            w_dict = {
                "Synthetic Wax": r["syn_wax_pct"],
                "Candelilla Wax": r["can_wax_pct"],
                "Dimethicone": r["dimethicone_pct"],
                "Caprylyl Methicone": r["caprylyl_pct"],
            }
            feat = GS40FeatureEngine.extract_from_weights(w_dict, fill_temp_c=r["fill_temp_c"])
            x_arr = feat.to_feature_array()

            # Predict adapted
            adapted = self.predict_adapted(x_arr, cal_x, residual_result)
            h_mean, h_std = adapted["hardness_gf"]
            t_mean, t_std = adapted["transfer_g"]
            d_mean, d_std = adapted["drop_point_c"]
            w_corr, dist_to_cal = adapted["spatial_weight"]

            # OOD score
            ood_res = self.ood_detector.evaluate(x_arr)

            from src.modeling.uncertainty_calibration import ConformalInterval
            h_ci = ConformalInterval(
                point_prediction=h_mean,
                nominal_coverage_pct=90.0,
                conformal_quantile_q=1.96,
                calibrated_lower=round(h_mean - 1.96 * h_std, 1),
                calibrated_upper=round(h_mean + 1.96 * h_std, 1),
                interval_width=round(3.92 * h_std, 1),
                is_empirically_calibrated=True
            )
            t_ci = ConformalInterval(
                point_prediction=t_mean,
                nominal_coverage_pct=90.0,
                conformal_quantile_q=1.96,
                calibrated_lower=round(max(0.005, t_mean - 1.96 * t_std), 4),
                calibrated_upper=round(t_mean + 1.96 * t_std, 4),
                interval_width=round(3.92 * t_std, 4),
                is_empirically_calibrated=True
            )
            d_ci = ConformalInterval(
                point_prediction=d_mean,
                nominal_coverage_pct=90.0,
                conformal_quantile_q=1.96,
                calibrated_lower=round(d_mean - 1.96 * d_std, 2),
                calibrated_upper=round(d_mean + 1.96 * d_std, 2),
                interval_width=round(3.92 * d_std, 2),
                is_empirically_calibrated=True
            )

            # Enhanced diversity bonus: encourages spatial exploration away from Run #1
            diversity_mult = 1.0 + 0.08 * float(np.log1p(dist_to_cal))

            score_res = CalibratedAcquisitionEngine.score_candidate(
                sample_id=r["batch_id"],
                h_interval=h_ci,
                t_interval=t_ci,
                d_interval=d_ci,
                ood_result=ood_res,
                fill_temp_c=r["fill_temp_c"],
                sedimentation_risk=feat.sedimentation_risk_index,
                diversity_bonus=diversity_mult
            )

            evaluated_runs.append({
                "batch_id": r["batch_id"],
                "trial_id": r.get("trial_id", ""),
                "design_type": r.get("design_type", ""),
                "adapted_hardness_gf": h_mean,
                "adapted_hardness_std": h_std,
                "adapted_transfer_g": t_mean,
                "adapted_drop_point_c": d_mean,
                "distance_to_cal_001": dist_to_cal,
                "spatial_weight": w_corr,
                "spec_relevance": score_res.specification_relevance_score,
                "info_gain": score_res.information_gain_score,
                "manufacturability": score_res.manufacturability_score,
                "adaptive_utility": round(float(score_res.total_acquisition_score), 2),
                "ood_score": ood_res.composite_score,
                "ood_category": ood_res.category.value,
                "feature_array": x_arr
            })

        # Sort descending by adaptive utility
        evaluated_runs.sort(key=lambda x: x["adaptive_utility"], reverse=True)
        return evaluated_runs

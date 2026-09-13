"""
GLIDE-SPEC 40 - Multi-Objective Calibrated Active Learning Acquisition Engine
Evaluates candidate formulations and DoE runs using the tri-criteria utility function:
  Acquisition Utility = Information Gain × Specification Relevance × Domain Coverage
Prevents wasting physical testing budget on extreme outlier runs (e.g. P002 which has high
variance but falls far below the target 750-900 gf specification).
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from src.modeling.uncertainty_calibration import ConformalInterval
from src.modeling.composite_ood import CompositeOODResult, CompositeOODCategory


@dataclass
class AcquisitionScoreResult:
    sample_id: str
    total_acquisition_score: float
    information_gain_score: float
    specification_relevance_score: float
    domain_coverage_score: float
    predicted_hardness_gf: float
    hardness_conformal_interval: Tuple[float, float]
    predicted_transfer_g: float
    predicted_drop_point_c: float
    composite_ood_score: float
    composite_ood_category: str
    strategic_verdict: str


class CalibratedAcquisitionEngine:
    """
    Ranks experimental candidates for physical execution selection.
    """

    # Rev.7.3 Target Center and Desired Tolerance
    TARGET_HARDNESS_GF = 800.0
    TOLERANCE_HARDNESS_GF = 80.0  # 720 ~ 880 gf is prime specification sweet-spot

    TARGET_TRANSFER_G = 0.048
    TOLERANCE_TRANSFER_G = 0.007

    TARGET_DROP_POINT_C = 61.5
    TOLERANCE_DROP_POINT_C = 1.2

    @classmethod
    def score_candidate(
        cls,
        sample_id: str,
        h_interval: ConformalInterval,
        t_interval: ConformalInterval,
        d_interval: ConformalInterval,
        ood_result: CompositeOODResult
    ) -> AcquisitionScoreResult:
        # 1. Information Gain Component (Total Conformal Uncertainty Width)
        # Wider conformal width = higher potential model reduction upon physical feedback
        rel_w_h = h_interval.interval_width / max(10.0, h_interval.point_prediction)
        rel_w_t = t_interval.interval_width / max(0.005, t_interval.point_prediction)
        rel_w_d = d_interval.interval_width / max(10.0, d_interval.point_prediction)
        info_gain = float(rel_w_h + rel_w_t + rel_w_d) * 100.0

        # 2. Specification Relevance Component (Gaussian Proximity to Rev.7.3 Sweet Spot)
        # Penalizes runs whose prediction is far below/above spec (e.g. Hardness < 700 gf)
        h_dev = (h_interval.point_prediction - cls.TARGET_HARDNESS_GF) / cls.TOLERANCE_HARDNESS_GF
        t_dev = (t_interval.point_prediction - cls.TARGET_TRANSFER_G) / cls.TOLERANCE_TRANSFER_G
        d_dev = (d_interval.point_prediction - cls.TARGET_DROP_POINT_C) / cls.TOLERANCE_DROP_POINT_C

        # Scaled between 0.05 and 1.0
        # Hardness is prioritized (weight 2.0 in distance)
        dist_sq = 2.0 * (h_dev ** 2) + 1.0 * (t_dev ** 2) + 1.0 * (d_dev ** 2)
        spec_relevance = float(np.exp(-0.5 * dist_sq))
        # Ensure minimum baseline relevance so boundary runs still carry some value
        spec_relevance = max(0.05, min(1.0, spec_relevance))

        # 3. Domain Coverage Component (OOD Decay Factor)
        # If deeply Out-of-Domain, domain coverage penalty reduces utility
        ood_score = ood_result.composite_score
        if ood_result.category == CompositeOODCategory.IN_DOMAIN:
            domain_cov = 1.0
        elif ood_result.category == CompositeOODCategory.BOUNDARY_ZONE:
            domain_cov = float(np.exp(-0.4 * (ood_score - 1.0)))
        else:
            domain_cov = float(np.exp(-1.0 * (ood_score - 1.0)))
        domain_cov = max(0.10, min(1.0, domain_cov))

        # Total Acquisition Utility = InfoGain * SpecRelevance * DomainCoverage
        total_utility = info_gain * spec_relevance * domain_cov

        # Strategic Evaluation Verdict
        if spec_relevance >= 0.60 and info_gain >= 30.0 and domain_cov >= 0.70:
            verdict = "PRIORITY_1_SWEET_SPOT_CALIBRATOR (Balances high info gain with target spec relevance)"
        elif spec_relevance < 0.20:
            verdict = "BOUNDARY_PROBE_ONLY (High uncertainty but predicted off-target; secondary calibration)"
        elif domain_cov < 0.30:
            verdict = "EXTREME_EXTRAPOLATION (Too distant from empirical envelope; defer physical test)"
        else:
            verdict = "SECONDARY_CONFIRMATION_CANDIDATE"

        return AcquisitionScoreResult(
            sample_id=sample_id,
            total_acquisition_score=round(total_utility, 2),
            information_gain_score=round(info_gain, 2),
            specification_relevance_score=round(spec_relevance, 3),
            domain_coverage_score=round(domain_cov, 3),
            predicted_hardness_gf=round(h_interval.point_prediction, 1),
            hardness_conformal_interval=(round(h_interval.calibrated_lower, 1), round(h_interval.calibrated_upper, 1)),
            predicted_transfer_g=round(t_interval.point_prediction, 4),
            predicted_drop_point_c=round(d_interval.point_prediction, 2),
            composite_ood_score=round(ood_score, 2),
            composite_ood_category=ood_result.category.value,
            strategic_verdict=verdict
        )

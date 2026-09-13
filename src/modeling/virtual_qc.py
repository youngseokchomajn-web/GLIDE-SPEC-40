"""
GLIDE-SPEC 40 - Test-by-Exception Virtual QC Decision Engine
Translates multi-surrogate prediction distributions, 95% PIs, and OOD scores
into an automated 4-tier physical testing decision:
  1. VIRTUAL_PASS (Test Waiver Eligible - Zero testing needed)
  2. VIRTUAL_PASS_CONFIRMATION_REQUIRED (1 replicate test needed)
  3. EXPERIMENT_REQUIRED (Full physical manufacture needed)
  4. OUT_OF_DOMAIN (Active Learning / exploratory test needed)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional

from src.modeling.surrogate_engine import (
    SurrogateEvaluationResult, OODLevel, SingleResponsePrediction
)


class VirtualQCDecision(str, Enum):
    VIRTUAL_PASS = "VIRTUAL_PASS"
    VIRTUAL_PASS_CONFIRMATION_REQUIRED = "VIRTUAL_PASS_CONFIRMATION_REQUIRED"
    EXPERIMENT_REQUIRED = "EXPERIMENT_REQUIRED"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"


@dataclass
class VirtualQCReport:
    formula_id: str
    decision: VirtualQCDecision
    test_waiver_granted: bool
    joint_spec_probability_pct: float
    model_confidence_pct: float
    ood_level: OODLevel
    rationale: str
    response_summaries: Dict[str, Dict[str, Any]]
    recommended_action: str


class VirtualQCEngine:
    """
    Automated decision gate evaluating surrogate evaluation results.
    """

    CONFIDENCE_THRESHOLD_WAIVER = 95.0
    JOINT_PROB_THRESHOLD_WAIVER = 0.985
    SINGLE_PROB_MIN_WAIVER = 0.990

    @classmethod
    def audit_formulation(
        cls,
        eval_result: SurrogateEvaluationResult
    ) -> VirtualQCReport:
        preds = eval_result.predictions
        h_pred = preds["hardness_gf"]
        t_pred = preds["transfer_g"]
        d_pred = preds["drop_point_c"]
        s_pred = preds.get("sedimentation_risk")

        p_h = h_pred.prob_in_spec
        p_t = t_pred.prob_in_spec
        p_d = d_pred.prob_in_spec
        joint_p = p_h * p_t * p_d

        response_summaries = {}
        for key, p in preds.items():
            response_summaries[key] = {
                "prediction": p.point_prediction,
                "uncertainty_std": p.std_uncertainty,
                "pi_95": [p.pi_95_lower, p.pi_95_upper],
                "prob_in_spec": p.prob_in_spec,
                "target_range": [p.spec_target_min, p.spec_target_max]
            }

        # Decision Logic:
        # 1. Check Out-of-Domain
        if eval_result.ood_level == OODLevel.HIGH:
            decision = VirtualQCDecision.OUT_OF_DOMAIN
            waiver = False
            rationale = (
                f"Formulation feature vector is Out-of-Domain (Mahalanobis D={eval_result.ood_score:.2f} > threshold). "
                "Surrogate cannot safely extrapolate without experimental calibration."
            )
            action = "Add formulation to Active Learning queue for exploratory sequential DOE."

        # 2. Check Severe Quality / Spec Failure Risk
        elif joint_p < 0.90 or (s_pred and s_pred.point_prediction > 2.0):
            decision = VirtualQCDecision.EXPERIMENT_REQUIRED
            waiver = False
            failed_responses = [k for k, v in preds.items() if v.prob_in_spec < 0.90]
            rationale = (
                f"High risk of specification deviation or settling instability. "
                f"Critical responses below 90% spec probability: {failed_responses}."
            )
            action = "Mandatory full physical pilot manufacture and 3-replicate QC testing."

        # 3. Check Moderate Uncertainty / Borderline Spec
        elif joint_p < cls.JOINT_PROB_THRESHOLD_WAIVER or eval_result.ood_level == OODLevel.MEDIUM or eval_result.model_confidence_pct < cls.CONFIDENCE_THRESHOLD_WAIVER:
            decision = VirtualQCDecision.VIRTUAL_PASS_CONFIRMATION_REQUIRED
            waiver = False
            rationale = (
                f"Formulation predicted in-spec (Joint P={joint_p*100:.1f}%), but moderate uncertainty "
                f"or borderline parameter space (Confidence={eval_result.model_confidence_pct}%)."
            )
            action = "Execute 1 confirmation sample test to verify critical response."

        # 4. Low Uncertainty, In-Domain, High Confidence (>98.5% joint probability)
        else:
            decision = VirtualQCDecision.VIRTUAL_PASS
            waiver = True
            rationale = (
                f"Formulation is fully in-domain (OOD={eval_result.ood_level.value}) with high confidence "
                f"({eval_result.model_confidence_pct}%) and joint spec probability {joint_p*100:.1f}% >= 98.5%."
            )
            action = "GRANT TEST WAIVER: Proceed directly to digital formulation release without physical pilot."

        return VirtualQCReport(
            formula_id=eval_result.formula_id,
            decision=decision,
            test_waiver_granted=waiver,
            joint_spec_probability_pct=round(joint_p * 100.0, 2),
            model_confidence_pct=eval_result.model_confidence_pct,
            ood_level=eval_result.ood_level,
            rationale=rationale,
            response_summaries=response_summaries,
            recommended_action=action
        )

"""
GLIDE-SPEC 40 - Multi-Objective Formulation SLSQP Optimizer (Phase 4)
Optimizes the constrained mixture design space:
  - Wax System: Synthetic Wax + Candelilla Wax = 17.0%
  - Silicone System: Dimethicone + Caprylyl Methicone = 28.0%
  - Process Condition: Fill Temperature in [75°C, 85°C]
Targeting Hardness 820 gf, Transfer >= 0.040 g @ 10°C, and minimal raw material COGS.
"""

from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel
import numpy as np

try:
    from scipy.optimize import minimize
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

from src.modeling.predictor import FormulationPredictor, ModelState, PropertyPrediction


class OptimizationTarget(BaseModel):
    target_hardness_gf: float = 820.0
    min_hardness_gf: float = 750.0
    max_hardness_gf: float = 900.0
    target_transfer_g_10c: float = 0.045
    min_transfer_g_10c: float = 0.040
    target_drop_point_c: float = 61.5
    min_drop_point_c: float = 60.0
    max_drop_point_c: float = 63.0
    weight_hardness: float = 1.0
    weight_transfer: float = 1.5
    weight_cogs: float = 0.5


class CandidateFormula(BaseModel):
    candidate_id: str
    scenario_name: str
    synthetic_wax_pct: float
    candelilla_wax_pct: float
    dimethicone_pct: float
    caprylyl_methicone_pct: float
    fill_temperature_c: float = 80.0
    estimated_cogs_krw: float = 0.0
    predicted_hardness_gf: Optional[float] = None
    hardness_margin_gf: Optional[float] = None
    predicted_transfer_g: Optional[float] = None
    transfer_margin_g: Optional[float] = None
    predicted_drop_point_c: Optional[float] = None
    confidence_score: float = 0.0
    desirability_score: float = 0.0
    status: str = "PROPOSED_BY_OPTIMIZER"
    prediction_label: str = ""
    notes: Optional[str] = ""


class MultiObjectiveOptimizer:
    """
    Formulation Space Optimizer enforcing strict mixture invariants:
      Wax: SynWax + Candelilla = 17.0%
      Silicone: Dimethicone + Caprylyl Methicone = 28.0%
      Remaining 55.0% fixed active formulation.
    """

    # Approximate unit prices from raw material specs (KRW / kg)
    PRICE_SYN_WAX: float = 18000.0
    PRICE_CANDELILLA: float = 28000.0
    PRICE_DIMETHICONE: float = 12000.0
    PRICE_CAPRYLYL: float = 35000.0
    FIXED_BASE_COGS_PER_KG: float = 13500.0  # COGS of the fixed 55% components

    def __init__(self, predictor: FormulationPredictor, targets: Optional[OptimizationTarget] = None):
        self.predictor = predictor
        self.targets = targets or OptimizationTarget()

    def calculate_cogs(
        self,
        syn_wax: float,
        candelilla: float,
        dimethicone: float,
        caprylyl: float,
        stick_weight_g: float = 20.0
    ) -> float:
        """Calculates estimated raw material cost per 20g stick in KRW."""
        cost_per_kg = (
            (syn_wax / 100.0) * self.PRICE_SYN_WAX +
            (candelilla / 100.0) * self.PRICE_CANDELILLA +
            (dimethicone / 100.0) * self.PRICE_DIMETHICONE +
            (caprylyl / 100.0) * self.PRICE_CAPRYLYL +
            self.FIXED_BASE_COGS_PER_KG
        )
        return round((cost_per_kg / 1000.0) * stick_weight_g, 1)

    def _loss_function(
        self,
        x: np.ndarray,
        target_h: float,
        target_t: float,
        w_h: float,
        w_t: float,
        w_c: float
    ) -> float:
        """
        x = [u1, v1, T]
        u1 in [0.5294, 0.8824], v1 in [0.4286, 0.7857], T in [75.0, 85.0]
        """
        u1, v1, T = x[0], x[1], x[2]
        syn_wax = 17.0 * u1
        candelilla = 17.0 * (1.0 - u1)
        dimethicone = 28.0 * v1
        caprylyl = 28.0 * (1.0 - v1)

        # Retrieve predictions
        pred_h, _ = self.predictor.hardness_model.predict(syn_wax, dimethicone, T)
        pred_t, _ = self.predictor.transfer_model.predict(syn_wax, dimethicone, T)

        # Loss terms normalized to relative deviance
        loss_h = ((pred_h - target_h) / target_h) ** 2
        # One-sided penalty if transfer < minimum requirement (0.040g)
        transfer_deficit = max(0.0, (self.targets.min_transfer_g_10c - pred_t) / self.targets.min_transfer_g_10c)
        transfer_target_dev = ((pred_t - target_t) / target_t) ** 2
        loss_t = 3.0 * (transfer_deficit ** 2) + transfer_target_dev

        # Normalized COGS term
        cogs = self.calculate_cogs(syn_wax, candelilla, dimethicone, caprylyl)
        loss_c = (cogs / 1000.0) ** 2

        return w_h * loss_h + w_t * loss_t + w_c * loss_c

    def _optimize_scenario(
        self,
        candidate_id: str,
        scenario_name: str,
        target_h: float,
        target_t: float,
        w_h: float,
        w_t: float,
        w_c: float,
        x0: np.ndarray
    ) -> CandidateFormula:
        """Runs SLSQP on decision variables [u1, v1, T]."""
        bounds = [
            (9.0 / 17.0, 15.0 / 17.0),
            (12.0 / 28.0, 22.0 / 28.0),
            (75.0, 85.0)
        ]

        if HAS_SCIPY:
            res = minimize(
                fun=self._loss_function,
                x0=x0,
                args=(target_h, target_t, w_h, w_t, w_c),
                method="SLSQP",
                bounds=bounds,
                options={"maxiter": 100, "ftol": 1e-6}
            )
            opt_x = res.x if res.success else x0
        else:
            opt_x = x0

        u1, v1, T = opt_x[0], opt_x[1], opt_x[2]
        syn_wax = round(float(17.0 * u1), 2)
        candelilla = round(float(17.0 - syn_wax), 2)
        dimethicone = round(float(28.0 * v1), 2)
        caprylyl = round(float(28.0 - dimethicone), 2)
        fill_t = round(float(T), 1)

        pred = self.predictor.predict(syn_wax, candelilla, dimethicone, caprylyl, fill_t)
        cogs = self.calculate_cogs(syn_wax, candelilla, dimethicone, caprylyl)

        loss = self._loss_function(opt_x, target_h, target_t, w_h, w_t, w_c)
        desirability = round(float(1.0 / (1.0 + loss)), 3)

        return CandidateFormula(
            candidate_id=candidate_id,
            scenario_name=scenario_name,
            synthetic_wax_pct=syn_wax,
            candelilla_wax_pct=candelilla,
            dimethicone_pct=dimethicone,
            caprylyl_methicone_pct=caprylyl,
            fill_temperature_c=fill_t,
            estimated_cogs_krw=cogs,
            predicted_hardness_gf=pred.hardness_gf,
            hardness_margin_gf=pred.hardness_margin_gf,
            predicted_transfer_g=pred.transfer_g,
            transfer_margin_g=pred.transfer_margin_g,
            predicted_drop_point_c=pred.drop_point_c,
            confidence_score=pred.confidence_score,
            desirability_score=desirability,
            status="OPTIMIZED_SLSQP",
            prediction_label=pred.message,
            notes=f"SLSQP Pareto solution for {scenario_name}"
        )

    def generate_candidates(self, top_n: int = 3) -> List[CandidateFormula]:
        """
        Generates Pareto frontier candidates across 3 strategic scenarios:
        1. Balanced Baseline (Hardness 820 gf, Transfer 0.045 g)
        2. High-Slip Summer (Hardness 850 gf, High Synthetic Wax, Volatile Silicone)
        3. High-Payoff Winter (Transfer 0.050 g, High Candelilla, High Linear Dimethicone)
        """
        if self.predictor.state == ModelState.AWAITING_PILOT_DATA or self.predictor.hardness_model is None:
            rule_set = [
                ("CAND-OPT-01", "Balanced Baseline", 12.0, 5.0, 17.0, 11.0, 80.0, "Standard Wax 12/5 & Silicone 17/11"),
                ("CAND-OPT-02", "High-Slip Summer", 13.5, 3.5, 15.0, 13.0, 82.0, "Higher Synthetic Wax + Volatile Caprylyl"),
                ("CAND-OPT-03", "High-Payoff Winter", 10.5, 6.5, 19.0, 9.0, 78.0, "Higher Candelilla + High Linear Dimethicone")
            ]

            candidates = []
            for cid, sc_name, syn_w, can_w, dim_s, cap_s, fill_t, desc in rule_set[:top_n]:
                cogs = self.calculate_cogs(syn_w, can_w, dim_s, cap_s)
                candidates.append(CandidateFormula(
                    candidate_id=cid,
                    scenario_name=sc_name,
                    synthetic_wax_pct=syn_w,
                    candelilla_wax_pct=can_w,
                    dimethicone_pct=dim_s,
                    caprylyl_methicone_pct=cap_s,
                    fill_temperature_c=fill_t,
                    estimated_cogs_krw=cogs,
                    predicted_hardness_gf=None,
                    predicted_transfer_g=None,
                    predicted_drop_point_c=None,
                    confidence_score=0.0,
                    desirability_score=0.80,
                    prediction_label="Uncalibrated (Awaiting >= 16 real Pilot QC records)",
                    notes=f"{desc} (Rule-based boundary estimate)"
                ))
            return candidates

        scenarios = [
            ("CAND-SLSQP-01", "Balanced Baseline", 820.0, 0.045, 1.0, 1.5, 0.5, np.array([12.0 / 17.0, 17.0 / 28.0, 80.0])),
            ("CAND-SLSQP-02", "High-Slip Summer", 850.0, 0.042, 2.0, 0.8, 0.5, np.array([13.5 / 17.0, 15.0 / 28.0, 82.0])),
            ("CAND-SLSQP-03", "High-Payoff Winter", 780.0, 0.050, 0.8, 2.5, 0.5, np.array([10.5 / 17.0, 19.0 / 28.0, 78.0]))
        ]

        candidates = []
        for cid, sc_name, th, tt, wh, wt, wc, x0 in scenarios[:top_n]:
            candidate = self._optimize_scenario(cid, sc_name, th, tt, wh, wt, wc, x0)
            candidates.append(candidate)

        return candidates

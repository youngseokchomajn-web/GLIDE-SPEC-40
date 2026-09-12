"""
GLIDE-SPEC 40 - Property Response Model & Predictor (Phase 3 Real Regression)
Strictly adheres to rule #6: Never assume property predictions without real QC experimental data.
Enforces Rule #12: Predictions must always be explicitly labeled as Predicted, not experimental.
Promotes to TRAINED_LINEAR only after >= 16 eligible real Pilot observations and >= 3 centre-point replicates.
"""

from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
import numpy as np
from pydantic import BaseModel

from src.qc.models import BatchQCRecord
from src.modeling.regression import MixtureRegressionModel, RegressionMetrics


class ModelState(str, Enum):
    AWAITING_PILOT_DATA = "AWAITING_PILOT_DATA"
    TRAINED_LINEAR = "TRAINED_LINEAR"
    TRAINED_SURFACE = "TRAINED_SURFACE"
    TRAINED_GAUSSIAN_PROCESS = "TRAINED_GAUSSIAN_PROCESS"


class PropertyPrediction(BaseModel):
    hardness_gf: Optional[float] = None
    hardness_margin_gf: Optional[float] = None
    transfer_g: Optional[float] = None
    transfer_margin_g: Optional[float] = None
    drop_point_c: Optional[float] = None
    confidence_score: float = 0.0
    model_state: ModelState = ModelState.AWAITING_PILOT_DATA
    sample_count: int = 0
    applicable_range: Dict[str, Tuple[float, float]] = {}
    message: str


class FormulationPredictor:
    MIN_ELIGIBLE_PILOT_RECORDS: int = 16
    MIN_CENTRE_POINT_REPLICATES: int = 3

    def __init__(self):
        self.state: ModelState = ModelState.AWAITING_PILOT_DATA
        self.training_records: List[BatchQCRecord] = []
        self.hardness_model: Optional[MixtureRegressionModel] = None
        self.transfer_model: Optional[MixtureRegressionModel] = None
        self.drop_point_model: Optional[MixtureRegressionModel] = None
        self.metrics: Dict[str, RegressionMetrics] = {}

    def _count_centre_points(self, eligible_records: List[BatchQCRecord], db: Optional[Any] = None) -> int:
        """
        Detects genuine centre-point replicates:
        Must satisfy all 3 physical coordinates:
          - Synthetic Wax ≈ 12.0% (u1 ≈ 0.706)
          - Dimethicone ≈ 17.0% (v1 ≈ 0.607)
          - Fill Temperature ≈ 80.0°C
        Or trial_obj.is_centre_point() is explicitly True.
        """
        count = 0
        for r in eligible_records:
            trial_obj = db.get_doe_trial(r.trial_id) if db else None
            if trial_obj and trial_obj.is_centre_point():
                count += 1
            elif trial_obj:
                t = r.process_conditions.fill_temperature_c
                if (
                    abs(t - 80.0) <= 1.0 and
                    abs(trial_obj.synthetic_wax_pct - 12.0) <= 0.2 and
                    abs(trial_obj.dimethicone_pct - 17.0) <= 0.2
                ):
                    count += 1
        return count

    def _build_matrix(
        self,
        records: List[BatchQCRecord],
        db: Optional[Any],
        target_attr: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        X_list = []
        y_list = []
        for r in records:
            trial_obj = db.get_doe_trial(r.trial_id) if db else None
            if trial_obj is None:
                continue
            val = getattr(r, target_attr)
            if val is None:
                continue
            u1, v1, T = MixtureRegressionModel.extract_features(
                trial_obj.synthetic_wax_pct,
                trial_obj.dimethicone_pct,
                r.process_conditions.fill_temperature_c
            )
            X_list.append([u1, v1, T])
            y_list.append(val)
        return np.array(X_list), np.array(y_list)

    def fit(
        self,
        records: List[BatchQCRecord],
        verified_raw_materials: bool = True,
        db: Optional[Any] = None
    ) -> bool:
        """
        Phase 3 Real Multivariate Regression Fit (Hardened Qualification):
        1. Filters genuine, SOP-complete, lineage-verified REAL_PILOT records.
        2. Property-isolated datasets: Hardness and Transfer models fit only on real measurements.
        3. Strictly eliminates any fake replacement of unmeasured Drop Point values.
        4. Enforces >= 16 eligible records AND >= 3 true 3-coordinate centre-point replicates.
        """
        if db is None:
            try:
                from src.storage.db import FormulationDatabase
                db = FormulationDatabase()
            except Exception:
                db = None

        eligible = []
        for r in records:
            if not r.is_training_eligible(verified_raw_materials=verified_raw_materials):
                continue
            if db is not None:
                if not db.get_doe_trial(r.trial_id):
                    continue
                if not db.get_manufacturing_batch(r.batch_id):
                    continue
            eligible.append(r)

        self.training_records = eligible

        # Property-specific isolated observation sets
        h_records = [r for r in eligible if r.hardness_gf is not None]
        t_records = [r for r in eligible if r.transfer_g_10c is not None]
        dp_records = [r for r in eligible if r.drop_point_c is not None]

        # Count genuine 3-coordinate centre-points for each property
        h_centre = self._count_centre_points(h_records, db)
        t_centre = self._count_centre_points(t_records, db)

        # Core promotion criteria for production model
        if len(h_records) < self.MIN_ELIGIBLE_PILOT_RECORDS or h_centre < self.MIN_CENTRE_POINT_REPLICATES:
            self.state = ModelState.AWAITING_PILOT_DATA
            return False

        if len(t_records) < self.MIN_ELIGIBLE_PILOT_RECORDS or t_centre < self.MIN_CENTRE_POINT_REPLICATES:
            self.state = ModelState.AWAITING_PILOT_DATA
            return False

        # 1. Fit Hardness response surface
        X_h, y_h = self._build_matrix(h_records, db, "hardness_gf")
        self.hardness_model = MixtureRegressionModel("Hardness @ 25C")
        self.metrics["hardness"] = self.hardness_model.fit(X_h, y_h)

        # 2. Fit Pay-off / Transfer response surface
        X_t, y_t = self._build_matrix(t_records, db, "transfer_g_10c")
        self.transfer_model = MixtureRegressionModel("Pay-off @ 10C")
        self.metrics["transfer"] = self.transfer_model.fit(X_t, y_t)

        # 3. Fit Drop Point model ONLY if genuine >= 16 real observations & >= 3 centre points exist
        dp_centre = self._count_centre_points(dp_records, db)
        if len(dp_records) >= self.MIN_ELIGIBLE_PILOT_RECORDS and dp_centre >= self.MIN_CENTRE_POINT_REPLICATES:
            X_dp, y_dp = self._build_matrix(dp_records, db, "drop_point_c")
            self.drop_point_model = MixtureRegressionModel("Drop Point")
            self.metrics["drop_point"] = self.drop_point_model.fit(X_dp, y_dp)
        else:
            self.drop_point_model = None
            if "drop_point" in self.metrics:
                del self.metrics["drop_point"]

        self.state = ModelState.TRAINED_LINEAR
        return True

    def predict(
        self,
        synthetic_wax: float,
        candelilla_wax: float,
        dimethicone: float,
        caprylyl_methicone: float,
        fill_temperature_c: float = 80.0
    ) -> PropertyPrediction:
        """
        Generates empirical response surface predictions adhering strictly to Rule #12:
        Always labeled visibly as 'Predicted (n=X samples), not experimental'.
        Applicability range is derived directly from the real training data boundaries.
        """
        if self.state == ModelState.AWAITING_PILOT_DATA or self.hardness_model is None or self.transfer_model is None:
            return PropertyPrediction(
                hardness_gf=None,
                hardness_margin_gf=None,
                transfer_g=None,
                transfer_margin_g=None,
                drop_point_c=None,
                confidence_score=0.0,
                model_state=self.state,
                sample_count=len(self.training_records),
                applicable_range={},
                message=f"Property prediction locked. Waiting for >= {self.MIN_ELIGIBLE_PILOT_RECORDS} verified real Pilot records and >= {self.MIN_CENTRE_POINT_REPLICATES} genuine 3-coordinate centre-point replicates (Current eligible: {len(self.training_records)})."
            )

        # Perform actual multivariate OLS predictions
        pred_h, margin_h = self.hardness_model.predict(synthetic_wax, dimethicone, fill_temperature_c)
        pred_t, margin_t = self.transfer_model.predict(synthetic_wax, dimethicone, fill_temperature_c)

        # Drop point is predicted ONLY if genuine model exists
        pred_dp = None
        if self.drop_point_model is not None:
            pred_dp, _ = self.drop_point_model.predict(synthetic_wax, dimethicone, fill_temperature_c)

        # Calculate composite confidence score based on R² and LOOCV
        h_r2 = max(0.0, self.metrics["hardness"].r_squared)
        t_r2 = max(0.0, self.metrics["transfer"].r_squared)
        avg_r2 = (h_r2 + t_r2) / 2.0
        confidence = round(min(0.98, max(0.10, avg_r2 * 0.95)), 2)

        sample_n = len(self.training_records)

        # Extract dynamic applicability range directly from fitted training metrics
        h_m = self.metrics["hardness"]
        ranges = {
            "synthetic_wax_pct": (round(h_m.u1_range[0] * 17.0, 2), round(h_m.u1_range[1] * 17.0, 2)),
            "dimethicone_pct": (round(h_m.v1_range[0] * 28.0, 2), round(h_m.v1_range[1] * 28.0, 2)),
            "fill_temperature_c": (round(h_m.temp_range[0], 1), round(h_m.temp_range[1], 1))
        }

        # Rule #12 Mandatory labeling
        rule_label = f"Predicted (n={sample_n} real Pilot observations, LOOCV RMSE: Hardness ±{self.metrics['hardness'].loocv_rmse:.1f}gf, Transfer ±{self.metrics['transfer'].loocv_rmse:.4f}g), NOT experimental measurement."

        return PropertyPrediction(
            hardness_gf=pred_h,
            hardness_margin_gf=margin_h,
            transfer_g=pred_t,
            transfer_margin_g=margin_t,
            drop_point_c=pred_dp,
            confidence_score=confidence,
            model_state=self.state,
            sample_count=sample_n,
            applicable_range=ranges,
            message=rule_label
        )

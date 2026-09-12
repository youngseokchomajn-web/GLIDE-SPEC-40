"""
GLIDE-SPEC 40 - Property Response Model & Predictor
Strictly adheres to rule #6: Never assume property predictions without real QC experimental data.
Starts in UNTRAINED state and only trains when verified QC records are provided.
"""

from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel

from src.qc.models import BatchQCRecord


class ModelState(str, Enum):
    AWAITING_PILOT_DATA = "AWAITING_PILOT_DATA"
    TRAINED_LINEAR = "TRAINED_LINEAR"
    TRAINED_SURFACE = "TRAINED_SURFACE"
    TRAINED_GAUSSIAN_PROCESS = "TRAINED_GAUSSIAN_PROCESS"


class PropertyPrediction(BaseModel):
    hardness_gf: Optional[float] = None
    transfer_g: Optional[float] = None
    drop_point_c: Optional[float] = None
    density_g_cm3: Optional[float] = None
    confidence_score: float = 0.0
    model_state: ModelState = ModelState.AWAITING_PILOT_DATA
    message: str


class FormulationPredictor:
    def __init__(self):
        self.state: ModelState = ModelState.AWAITING_PILOT_DATA
        self.training_records: List[BatchQCRecord] = []

    def fit(self, records: List[BatchQCRecord]):
        """Trains empirical response surface models once sufficient experimental data exists."""
        valid_records = [
            r for r in records
            if r.hardness_gf is not None and r.transfer_g_10c is not None
        ]
        if len(valid_records) < 5:
            self.state = ModelState.AWAITING_PILOT_DATA
            self.training_records = valid_records
            return False

        # In v0.1, we acknowledge data but require more points for robust response surface
        self.training_records = valid_records
        self.state = ModelState.TRAINED_LINEAR
        return True

    def predict(self, synthetic_wax: float, candelilla_wax: float, dimethicone: float, caprylyl_methicone: float) -> PropertyPrediction:
        if self.state == ModelState.AWAITING_PILOT_DATA:
            return PropertyPrediction(
                hardness_gf=None,
                transfer_g=None,
                drop_point_c=None,
                density_g_cm3=None,
                confidence_score=0.0,
                model_state=self.state,
                message="[RULE ENFORCED] Model is in AWAITING_PILOT_DATA state. Predictions will NOT be generated until real QC laboratory data is fed."
            )

        # Once trained, regression calculation will take place here
        return PropertyPrediction(
            confidence_score=0.5,
            model_state=self.state,
            message="Preliminary empirical estimate"
        )

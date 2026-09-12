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

    MIN_ELIGIBLE_PILOT_RECORDS: int = 16

    def fit(self, records: List[BatchQCRecord], verified_raw_materials: bool = True) -> bool:
        """
        Phase 2A & 3 Data Contract Enforced:
        Accepts only genuine REAL_PILOT records with complete SOP, verified materials, and DOE lineage.
        Synthetic records or incomplete SOP records are strictly rejected.
        Requires >= 16 eligible real Pilot observations.
        IMPORTANT: In Phase 2A, promotion to TRAINED_LINEAR is blocked until Phase 3 implements
        the actual mathematical multivariate regression coefficients fit.
        """
        eligible_records = [
            r for r in records
            if r.is_training_eligible(verified_raw_materials=verified_raw_materials)
        ]
        self.training_records = eligible_records

        if len(eligible_records) < self.MIN_ELIGIBLE_PILOT_RECORDS:
            self.state = ModelState.AWAITING_PILOT_DATA
            return False

        # Gatekeeper: Do NOT promote to TRAINED_LINEAR without Phase 3 regression engine!
        self.state = ModelState.AWAITING_PILOT_DATA
        return False

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

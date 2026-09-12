"""
GLIDE-SPEC 40 - QC Data Models & Test SOP Conditions
Tracks QC measurements along with strict SOP environmental & equipment parameters.
"""

from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class QCStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    MARGINAL = "MARGINAL"
    PENDING_SOP = "PENDING_SOP"


class DataOrigin(str, Enum):
    REAL_PILOT = "REAL_PILOT"
    SYNTHETIC_TEST = "SYNTHETIC_TEST"


class ProcessCondition(BaseModel):
    fill_temperature_c: float = 80.0
    shear_speed_rpm: float = 3000.0
    mixing_time_min: float = 20.0
    cooling_profile: str = "3-Step Gradual (25->15->5C)"


class HardnessSOP(BaseModel):
    probe_type: str = "TBD"  # e.g., 2mm needle, conical 45 deg, spherical
    penetration_depth_mm: Optional[float] = None
    test_speed_mm_s: Optional[float] = None
    conditioning_time_min: Optional[int] = None
    sample_temp_c: float = 25.0
    measurement_location: str = "center"
    replicate_count: int = 5


class TransferSOP(BaseModel):
    substrate_type: str = "TBD"  # e.g., synthetic leather, collagen sheet, human skin
    applied_area_cm2: Optional[float] = None
    applied_pressure_g: Optional[float] = None
    contact_time_s: Optional[float] = None
    ambient_temp_c: float = 10.0
    stroke_count: int = 2  # 1 round-trip
    test_method: str = "TBD"


class QCTestResult(BaseModel):
    test_name: str
    target_value_str: str
    measured_value: Optional[float]
    unit: str
    status: QCStatus
    notes: Optional[str] = ""


class BatchQCRecord(BaseModel):
    batch_id: str
    formula_id: str
    revision: str
    test_date: str
    operator: str

    # Linkage to DOE & Execution Contract
    trial_id: Optional[str] = None
    data_origin: DataOrigin = DataOrigin.REAL_PILOT
    process_conditions: ProcessCondition = Field(default_factory=ProcessCondition)

    # Measurements
    hardness_gf: Optional[float] = None
    transfer_g_10c: Optional[float] = None
    density_g_cm3: Optional[float] = None
    drop_point_c: Optional[float] = None

    # Mandatory SOP tracking
    hardness_sop: HardnessSOP = Field(default_factory=HardnessSOP)
    transfer_sop: TransferSOP = Field(default_factory=TransferSOP)

    # Secondary observations
    powder_bloom_observed: bool = False
    white_cast_score: Optional[int] = None  # 0 to 5
    sweating_syneresis_observed: bool = False
    stick_mechanism_smoothness: Optional[int] = None  # 1 to 5

    notes: Optional[str] = ""

    def is_sop_complete(self) -> bool:
        hardness = self.hardness_sop
        transfer = self.transfer_sop
        return all([
            hardness.probe_type != "TBD", hardness.penetration_depth_mm is not None,
            hardness.test_speed_mm_s is not None, hardness.conditioning_time_min is not None,
            transfer.substrate_type != "TBD", transfer.applied_area_cm2 is not None,
            transfer.applied_pressure_g is not None, transfer.contact_time_s is not None,
            transfer.test_method != "TBD",
        ])

    def is_training_eligible(self, verified_raw_materials: bool = True) -> bool:
        """
        Phase 2A Data Contract Gate:
        A record is eligible for model training ONLY if:
        1. It is genuine real pilot data (synthetic data strictly excluded).
        2. trial_id is linked (full lineage to DOE specification required).
        3. SOP is complete without any missing parameters.
        4. Raw material specifications are verified.
        5. Core measured properties (hardness & transfer) are non-null and positive.
        6. Process conditions are within controlled pilot screening bounds (e.g. 70~90°C fill).
        """
        if self.data_origin != DataOrigin.REAL_PILOT:
            return False
        if not self.trial_id:
            return False
        if not self.is_sop_complete():
            return False
        if not verified_raw_materials:
            return False
        if self.hardness_gf is None or self.hardness_gf <= 0:
            return False
        if self.transfer_g_10c is None or self.transfer_g_10c <= 0:
            return False
        # Controlled process space check
        fill_t = self.process_conditions.fill_temperature_c
        if fill_t < 70.0 or fill_t > 90.0:
            return False
        return True

    def evaluate_targets(self) -> Dict[str, QCTestResult]:
        results = {}

        # 1. Hardness: Target 750 ~ 900 gf @ 25C
        if self.hardness_gf is None:
            h_status = QCStatus.PENDING_SOP
        elif 750.0 <= self.hardness_gf <= 900.0:
            h_status = QCStatus.PASS
        elif 700.0 <= self.hardness_gf < 750.0 or 900.0 < self.hardness_gf <= 950.0:
            h_status = QCStatus.MARGINAL
        else:
            h_status = QCStatus.FAIL

        results["hardness"] = QCTestResult(
            test_name="Hardness @25C",
            target_value_str="750 - 900 gf",
            measured_value=self.hardness_gf,
            unit="gf",
            status=h_status,
            notes="Requires validated probe depth and speed SOP"
        )

        # 2. Transfer: Target >= 0.04 g @ 10C
        if self.transfer_g_10c is None:
            t_status = QCStatus.PENDING_SOP
        elif self.transfer_g_10c >= 0.04:
            t_status = QCStatus.PASS
        elif 0.035 <= self.transfer_g_10c < 0.04:
            t_status = QCStatus.MARGINAL
        else:
            t_status = QCStatus.FAIL

        results["transfer"] = QCTestResult(
            test_name="Low-Temp Transfer @10C",
            target_value_str=">= 0.04 g",
            measured_value=self.transfer_g_10c,
            unit="g",
            status=t_status,
            notes="Requires standardized substrate and contact pressure SOP"
        )

        # 3. Density: Target 1.08 +- 0.04 (1.04 ~ 1.12 g/cm3)
        if self.density_g_cm3 is None:
            d_status = QCStatus.PENDING_SOP
        elif 1.04 <= self.density_g_cm3 <= 1.12:
            d_status = QCStatus.PASS
        else:
            d_status = QCStatus.FAIL

        results["density"] = QCTestResult(
            test_name="Density",
            target_value_str="1.08 +- 0.04 g/cm3",
            measured_value=self.density_g_cm3,
            unit="g/cm3",
            status=d_status
        )

        # 4. Drop Point: Target 61.5 +- 1.5 C (60.0 ~ 63.0 C)
        if self.drop_point_c is None:
            dp_status = QCStatus.PENDING_SOP
        elif 60.0 <= self.drop_point_c <= 63.0:
            dp_status = QCStatus.PASS
        elif 59.0 <= self.drop_point_c < 60.0 or 63.0 < self.drop_point_c <= 64.0:
            dp_status = QCStatus.MARGINAL
        else:
            dp_status = QCStatus.FAIL

        results["drop_point"] = QCTestResult(
            test_name="Drop Point (Melting)",
            target_value_str="61.5 +- 1.5 C",
            measured_value=self.drop_point_c,
            unit="deg C",
            status=dp_status
        )

        return results

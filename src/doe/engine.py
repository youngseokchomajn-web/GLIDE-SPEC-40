"""
GLIDE-SPEC 40 - Advanced Mixture DOE (Design of Experiments) Engine
Generates constrained mixture designs for the Wax Matrix and Silicone Matrix,
integrated with process variables (Fill temperature, shear, cooling).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import itertools

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class DOETrial(BaseModel):
    trial_id: str
    design_type: str = "Vertex"  # Vertex, Centroid, Axial, Interior
    synthetic_wax_pct: float
    candelilla_wax_pct: float
    dimethicone_pct: float
    caprylyl_methicone_pct: float
    c12_15_alkyl_benzoate_pct: float = 9.5
    fill_temperature_c: float = 80.0
    shear_speed_rpm: float = 3000.0
    mixing_time_min: float = 20.0
    cooling_profile: str = "3-Step Gradual (25->15->5C)"
    status: str = "PLANNED"
    is_center_point: bool = False
    notes: Optional[str] = ""

    def is_centre_point(self) -> bool:
        """Strict 3-coordinate physical centre-point validation.
        
        The metadata flag `is_center_point` can NEVER bypass physical coordinate verification.
        Both conditions MUST hold:
          1. Physical coordinates must strictly fall within centroid bounds:
             - Synthetic Wax: 12.0 ± 0.2%
             - Dimethicone: 17.0 ± 0.2%
             - Fill Temperature: 80.0 ± 1.0°C
          2. AND it must be designated as a centre point:
             `self.is_center_point is True` OR design_type contains "Centroid" / "Center".
        """
        coord_valid = (
            abs(self.synthetic_wax_pct - 12.0) <= 0.2 and
            abs(self.dimethicone_pct - 17.0) <= 0.2 and
            abs(self.fill_temperature_c - 80.0) <= 1.0
        )
        if not coord_valid:
            return False

        return bool(self.is_center_point or "Centroid" in self.design_type or "Center" in self.design_type)

    def validate_mixture_constraints(self) -> bool:
        wax_sum = self.synthetic_wax_pct + self.candelilla_wax_pct
        sil_sum = self.dimethicone_pct + self.caprylyl_methicone_pct
        return abs(wax_sum - 17.0) < 0.05 and abs(sil_sum - 28.0) < 0.05

    def to_component_ratios(self) -> Dict[str, Dict[str, float]]:
        """Maps trial mixture ratios directly to Composite Component IDs."""
        return {
            "MAT-WAX-SYSTEM": {
                "MAT-WAX-SYN-01": self.synthetic_wax_pct,
                "MAT-WAX-CAN-01": self.candelilla_wax_pct,
            },
            "MAT-SIL-SYSTEM": {
                "MAT-SIL-DIM-01": self.dimethicone_pct,
                "MAT-SIL-CAP-01": self.caprylyl_methicone_pct,
            },
        }

    def to_process_condition(self):
        """Phase 2A Data Contract: Extracts real process conditions for batch & QC snapshot."""
        from src.qc.models import ProcessCondition
        return ProcessCondition(
            fill_temperature_c=self.fill_temperature_c,
            shear_speed_rpm=self.shear_speed_rpm,
            mixing_time_min=self.mixing_time_min,
            cooling_profile=self.cooling_profile
        )


class DOEConfig(BaseModel):
    """
    Configuration for parameterized mixture & process DOE generation.
    Enforces minimum 3 centre-point replicates to satisfy M4/Rule #6 requirements.
    """
    total_wax_pct: float = 17.0
    syn_wax_min: float = 9.0
    syn_wax_max: float = 15.0
    syn_wax_center: float = 12.0

    total_silicone_pct: float = 28.0
    dimethicone_min: float = 12.0
    dimethicone_max: float = 22.0
    dimethicone_center: float = 17.0

    fill_temp_min: float = 75.0
    fill_temp_max: float = 85.0
    fill_temp_center: float = 80.0

    centre_point_replicates: int = Field(default=4, ge=3)
    shear_speed_rpm: float = 3000.0
    mixing_time_min: float = 20.0
    cooling_profile: str = "3-Step Gradual (25->15->5C)"


class AdvancedDOEEngine:
    """
    Advanced Constrained Mixture & Process Factor DOE Generator.
    - Wax System (17% Total):
      * Synthetic Wax: 9.0% ~ 15.0% (Hardness & Melting)
      * Candelilla Wax: 2.0% ~ 8.0% (Pay-off & Plasticity)
    - Silicone System (28% Total):
      * Dimethicone: 12.0% ~ 22.0% (Linear base)
      * Caprylyl Methicone: 6.0% ~ 16.0% (Volatile-like slip)
    - Process Candidates:
      * Fill Temperature: 75°C, 80°C, 85°C
    """

    @classmethod
    def generate_full_doe_design(cls) -> List[DOETrial]:
        return cls.generate_custom_doe(DOEConfig(centre_point_replicates=4))

    @classmethod
    def generate_custom_doe(cls, config: Optional[DOEConfig] = None) -> List[DOETrial]:
        """
        Generates a comprehensive 16+ run DOE matrix satisfying M4 regression promotion criteria:
        - 4 Vertex points (Corner combinations of Wax & Silicone at Low/High temperatures)
        - 4 Mid-edge combinations
        - 4 Axial points
        - >= 3 Centre-point replicates at (syn_center, dim_center, temp_center)
        Total runs >= 16 with >= 3 centre-points.
        """
        cfg = config or DOEConfig()
        trials: List[DOETrial] = []
        counter = 1

        # 1. Vertex points (High/Low Wax x High/Low Silicone at T_min/T_max)
        vertices = [
            (cfg.syn_wax_max, cfg.dimethicone_max, cfg.fill_temp_center, "Vertex_HighSyn_HighDim"),
            (cfg.syn_wax_max, cfg.dimethicone_min, cfg.fill_temp_min, "Vertex_HighSyn_LowDim_Tmin"),
            (cfg.syn_wax_min, cfg.dimethicone_max, cfg.fill_temp_max, "Vertex_LowSyn_HighDim_Tmax"),
            (cfg.syn_wax_min, cfg.dimethicone_min, cfg.fill_temp_center, "Vertex_LowSyn_LowDim")
        ]
        for syn, dim, temp, tag in vertices:
            trials.append(DOETrial(
                trial_id=f"DOE-EXP-{counter:03d}",
                design_type=tag,
                synthetic_wax_pct=syn,
                candelilla_wax_pct=round(cfg.total_wax_pct - syn, 2),
                dimethicone_pct=dim,
                caprylyl_methicone_pct=round(cfg.total_silicone_pct - dim, 2),
                fill_temperature_c=temp,
                shear_speed_rpm=cfg.shear_speed_rpm,
                mixing_time_min=cfg.mixing_time_min,
                cooling_profile=cfg.cooling_profile,
                notes=f"Boundary vertex run exploring {tag}"
            ))
            counter += 1

        # 2. Axial points
        axials = [
            (cfg.syn_wax_max, cfg.dimethicone_center, cfg.fill_temp_min, "Axial_WaxMax"),
            (cfg.syn_wax_min, cfg.dimethicone_center, cfg.fill_temp_max, "Axial_WaxMin"),
            (cfg.syn_wax_center, cfg.dimethicone_max, cfg.fill_temp_min, "Axial_SilMax"),
            (cfg.syn_wax_center, cfg.dimethicone_min, cfg.fill_temp_max, "Axial_SilMin"),
            (cfg.syn_wax_center, cfg.dimethicone_center, cfg.fill_temp_min, "Axial_TempMin"),
            (cfg.syn_wax_center, cfg.dimethicone_center, cfg.fill_temp_max, "Axial_TempMax")
        ]
        for syn, dim, temp, tag in axials:
            trials.append(DOETrial(
                trial_id=f"DOE-EXP-{counter:03d}",
                design_type=tag,
                synthetic_wax_pct=syn,
                candelilla_wax_pct=round(cfg.total_wax_pct - syn, 2),
                dimethicone_pct=dim,
                caprylyl_methicone_pct=round(cfg.total_silicone_pct - dim, 2),
                fill_temperature_c=temp,
                shear_speed_rpm=cfg.shear_speed_rpm,
                mixing_time_min=cfg.mixing_time_min,
                cooling_profile=cfg.cooling_profile,
                notes=f"Axial exploration run {tag}"
            ))
            counter += 1

        # 3. Intermediate interior points
        interiors = [
            (round((cfg.syn_wax_min + cfg.syn_wax_center) / 2.0, 2), round((cfg.dimethicone_min + cfg.dimethicone_center) / 2.0, 2), cfg.fill_temp_center, "Interior_Low"),
            (round((cfg.syn_wax_max + cfg.syn_wax_center) / 2.0, 2), round((cfg.dimethicone_max + cfg.dimethicone_center) / 2.0, 2), cfg.fill_temp_center, "Interior_High")
        ]
        for syn, dim, temp, tag in interiors:
            trials.append(DOETrial(
                trial_id=f"DOE-EXP-{counter:03d}",
                design_type=tag,
                synthetic_wax_pct=syn,
                candelilla_wax_pct=round(cfg.total_wax_pct - syn, 2),
                dimethicone_pct=dim,
                caprylyl_methicone_pct=round(cfg.total_silicone_pct - dim, 2),
                fill_temperature_c=temp,
                shear_speed_rpm=cfg.shear_speed_rpm,
                mixing_time_min=cfg.mixing_time_min,
                cooling_profile=cfg.cooling_profile,
                notes=f"Interior resolution run {tag}"
            ))
            counter += 1

        # 4. Mandatory Centre-point replicates (>= 3)
        for i in range(cfg.centre_point_replicates):
            trials.append(DOETrial(
                trial_id=f"DOE-EXP-{counter:03d}",
                design_type=f"Centroid_Replicate_{i+1}",
                synthetic_wax_pct=cfg.syn_wax_center,
                candelilla_wax_pct=round(cfg.total_wax_pct - cfg.syn_wax_center, 2),
                dimethicone_pct=cfg.dimethicone_center,
                caprylyl_methicone_pct=round(cfg.total_silicone_pct - cfg.dimethicone_center, 2),
                fill_temperature_c=cfg.fill_temp_center,
                shear_speed_rpm=cfg.shear_speed_rpm,
                mixing_time_min=cfg.mixing_time_min,
                cooling_profile=cfg.cooling_profile,
                is_center_point=True,
                notes=f"Centre-point pure-error replicate {i+1} of {cfg.centre_point_replicates}"
            ))
            counter += 1

        return trials

    @classmethod
    def export_to_dataframe(cls, trials: List[DOETrial]):
        data = [t.model_dump() for t in trials]
        if HAS_PANDAS:
            return pd.DataFrame(data)
        return data

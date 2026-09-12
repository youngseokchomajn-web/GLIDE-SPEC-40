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
    notes: Optional[str] = ""

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
        # Wax mixture levels (Sum = 17.0)
        wax_levels = [
            ("Vertex_HighSyn", 15.0, 2.0),
            ("Vertex_LowSyn", 9.0, 8.0),
            ("Centroid_Wax", 12.0, 5.0),
            ("Axial_Wax1", 13.5, 3.5),
            ("Axial_Wax2", 10.5, 6.5)
        ]

        # Silicone mixture levels (Sum = 28.0)
        silicone_levels = [
            ("Vertex_HighDim", 22.0, 6.0),
            ("Vertex_LowDim", 12.0, 16.0),
            ("Centroid_Sil", 17.0, 11.0),
            ("Axial_Sil1", 19.5, 8.5),
            ("Axial_Sil2", 14.5, 13.5)
        ]

        fill_temps = [75.0, 80.0, 85.0]

        trials: List[DOETrial] = []
        trial_id_counter = 1

        # 1. Core Orthogonal Screening Matrix (12 runs)
        core_combos = [
            (wax_levels[0], silicone_levels[0], 80.0),  # HighSyn + HighDim @ 80C
            (wax_levels[0], silicone_levels[1], 75.0),  # HighSyn + LowDim  @ 75C
            (wax_levels[0], silicone_levels[2], 85.0),  # HighSyn + Centroid @ 85C
            (wax_levels[1], silicone_levels[0], 85.0),  # LowSyn  + HighDim @ 85C
            (wax_levels[1], silicone_levels[1], 80.0),  # LowSyn  + LowDim  @ 80C
            (wax_levels[1], silicone_levels[2], 75.0),  # LowSyn  + Centroid @ 75C
            (wax_levels[2], silicone_levels[0], 75.0),  # Centroid + HighDim @ 75C
            (wax_levels[2], silicone_levels[1], 85.0),  # Centroid + LowDim  @ 85C
            (wax_levels[2], silicone_levels[2], 80.0),  # Center Point Run 1 @ 80C
            (wax_levels[2], silicone_levels[2], 80.0),  # Center Point Replicate @ 80C
            (wax_levels[3], silicone_levels[3], 80.0),  # Axial 1
            (wax_levels[4], silicone_levels[4], 80.0),  # Axial 2
        ]

        for wax_item, sil_item, temp in core_combos:
            wax_name, syn_wax, can_wax = wax_item
            sil_name, dim, cap = sil_item

            t = DOETrial(
                trial_id=f"DOE-EXP-{trial_id_counter:03d}",
                design_type=f"{wax_name} x {sil_name}",
                synthetic_wax_pct=syn_wax,
                candelilla_wax_pct=can_wax,
                dimethicone_pct=dim,
                caprylyl_methicone_pct=cap,
                c12_15_alkyl_benzoate_pct=9.5,
                fill_temperature_c=temp,
                shear_speed_rpm=3000.0,
                mixing_time_min=20.0,
                cooling_profile="3-Step Gradual (25->15->5C)",
                status="PLANNED",
                notes=f"Pilot Run exploring {wax_name} and {sil_name} at {temp}C"
            )
            trials.append(t)
            trial_id_counter += 1

        return trials

    @classmethod
    def export_to_dataframe(cls, trials: List[DOETrial]):
        data = [t.model_dump() for t in trials]
        if HAS_PANDAS:
            return pd.DataFrame(data)
        return data

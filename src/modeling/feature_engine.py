"""
GLIDE-SPEC 40 - Physics-Informed Feature Ontology & Engine
Transforms raw formulation weight percentages and process parameters into
latent physical descriptors (volume fractions, surface area, network indices,
sedimentation risk, and thermal crystallization features).
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import csv
import numpy as np


class FeatureProvenance(str, Enum):
    MEASURED = "MEASURED"
    DERIVED_PHYSICAL = "DERIVED_PHYSICAL"
    DERIVED_EMPIRICAL = "DERIVED_EMPIRICAL"
    HYPOTHESIS = "HYPOTHESIS"


@dataclass
class FormulationFeatureVector:
    # 1. Raw Formulation Input Features (MEASURED)
    syn_wax_pct: float
    candelilla_wax_pct: float
    peg8_beeswax_pct: float
    dimethicone_pct: float
    caprylyl_methicone_pct: float
    mq_resin_solution_pct: float
    alkyl_benzoate_pct: float
    porous_silica_pct: float
    fumed_silica_pct: float
    pmssq_pct: float
    boron_nitride_pct: float
    zinc_oxide_pct: float
    active_preservative_pct: float

    # 2. Process & Thermal History Features (MEASURED)
    fill_temperature_c: float
    cooling_rate_c_min: float
    homogenizer_shear_rpm: float

    # 3. Derived Physical Volume Fractions
    total_powder_wt_pct: float
    total_wax_wt_pct: float
    total_silicone_wt_pct: float
    total_liquid_wt_pct: float

    wax_volume_fraction: float
    silicone_volume_fraction: float
    powder_volume_fraction: float
    solid_volume_fraction: float

    # 4. Surface Area, Oil Demand & Binder Dynamics
    total_particle_surface_area_m2_g: float
    total_oil_absorption_demand_ml_100g: float
    liquid_to_surface_area_ratio: float
    binder_to_powder_weight_ratio: float

    # 5. Latent Network & Structural Mechanics
    wax_crystallization_enthalpy_composite_j_g: float
    fumed_silica_percolation_ratio: float
    sedimentation_risk_index: float
    slip_lubricity_index: float

    # 6. Extended Manufacturing Parameters (Defaults)
    mixing_temperature_c: float = 88.0
    hold_time_min: float = 20.0

    # Raw dictionary representation for ML tabular models
    def to_dict(self) -> Dict[str, float]:
        return {
            "syn_wax_pct": self.syn_wax_pct,
            "candelilla_wax_pct": self.candelilla_wax_pct,
            "peg8_beeswax_pct": self.peg8_beeswax_pct,
            "dimethicone_pct": self.dimethicone_pct,
            "caprylyl_methicone_pct": self.caprylyl_methicone_pct,
            "mq_resin_solution_pct": self.mq_resin_solution_pct,
            "alkyl_benzoate_pct": self.alkyl_benzoate_pct,
            "porous_silica_pct": self.porous_silica_pct,
            "fumed_silica_pct": self.fumed_silica_pct,
            "pmssq_pct": self.pmssq_pct,
            "boron_nitride_pct": self.boron_nitride_pct,
            "zinc_oxide_pct": self.zinc_oxide_pct,
            "fill_temperature_c": self.fill_temperature_c,
            "cooling_rate_c_min": self.cooling_rate_c_min,
            "homogenizer_shear_rpm": self.homogenizer_shear_rpm,
            "total_powder_wt_pct": self.total_powder_wt_pct,
            "total_wax_wt_pct": self.total_wax_wt_pct,
            "total_silicone_wt_pct": self.total_silicone_wt_pct,
            "wax_volume_fraction": self.wax_volume_fraction,
            "silicone_volume_fraction": self.silicone_volume_fraction,
            "powder_volume_fraction": self.powder_volume_fraction,
            "solid_volume_fraction": self.solid_volume_fraction,
            "total_particle_surface_area_m2_g": self.total_particle_surface_area_m2_g,
            "total_oil_absorption_demand_ml_100g": self.total_oil_absorption_demand_ml_100g,
            "liquid_to_surface_area_ratio": self.liquid_to_surface_area_ratio,
            "binder_to_powder_weight_ratio": self.binder_to_powder_weight_ratio,
            "wax_crystallization_enthalpy_composite_j_g": self.wax_crystallization_enthalpy_composite_j_g,
            "fumed_silica_percolation_ratio": self.fumed_silica_percolation_ratio,
            "sedimentation_risk_index": self.sedimentation_risk_index,
            "slip_lubricity_index": self.slip_lubricity_index,
        }

    def to_feature_array(self) -> np.ndarray:
        d = self.to_dict()
        return np.array(list(d.values()), dtype=np.float64)

    @classmethod
    def feature_names(cls) -> List[str]:
        dummy = GS40FeatureEngine.extract_from_weights({}, 80.0, 2.5, 2500.0)
        return list(dummy.to_dict().keys())

    def evaluate_3tier_feasibility(self) -> Tuple[bool, List[str]]:
        """
        Evaluates formulation against Rev.7.3 3-tier constraints:
          Tier 1: Composition (Mass balance & component sub-system limits)
          Tier 2: Manufacturing (Fill temp, mixing temp, cooling rate, hold time)
          Tier 3: Physical Mechanics (Solid fraction, binder demand, percolation, sedimentation)
        """
        rejections = []

        # Tier 1: Composition Constraints
        tot_mass = (
            self.syn_wax_pct + self.candelilla_wax_pct + self.peg8_beeswax_pct +
            self.dimethicone_pct + self.caprylyl_methicone_pct + self.mq_resin_solution_pct +
            self.alkyl_benzoate_pct + self.porous_silica_pct + self.fumed_silica_pct +
            self.pmssq_pct + self.boron_nitride_pct + self.zinc_oxide_pct +
            self.active_preservative_pct
        )
        if abs(tot_mass - 100.0) > 0.5:
            rejections.append(f"Composition: Total formulation mass {tot_mass:.2f}% deviates from 100.0%")
        if not (16.0 <= self.total_wax_wt_pct <= 18.0):
            rejections.append(f"Composition: Total wax {self.total_wax_wt_pct:.1f}% outside Rev.7.3 16-18% range")
        if not (26.0 <= self.total_silicone_wt_pct <= 30.0):
            rejections.append(f"Composition: Total silicone {self.total_silicone_wt_pct:.1f}% outside Rev.7.3 26-30% range")
        if not (26.0 <= self.total_powder_wt_pct <= 30.0):
            rejections.append(f"Composition: Total powder {self.total_powder_wt_pct:.1f}% outside Rev.7.3 26-30% range")

        # Tier 2: Manufacturing Constraints
        if not (74.0 <= self.fill_temperature_c <= 86.0):
            rejections.append(f"Manufacturing: Fill temperature {self.fill_temperature_c:.1f}°C outside 74-86°C window")
        if not (83.0 <= self.mixing_temperature_c <= 92.0):
            rejections.append(f"Manufacturing: Mixing temperature {self.mixing_temperature_c:.1f}°C outside 83-92°C window")
        if not (0.5 <= self.cooling_rate_c_min <= 6.0):
            rejections.append(f"Manufacturing: Cooling rate {self.cooling_rate_c_min:.1f}°C/min outside 0.5-6.0°C/min range")
        if self.hold_time_min > 60.0:
            rejections.append(f"Manufacturing: Hold time {self.hold_time_min:.1f} min exceeds maximum 60.0 min")

        # Tier 3: Physical Mechanics Constraints
        if self.solid_volume_fraction > 0.40:
            rejections.append(f"Physical: Solid volume fraction excessive ({self.solid_volume_fraction*100:.1f}% > 40.0%)")
        if self.binder_to_powder_weight_ratio < 1.50:
            rejections.append(f"Physical: Binder/powder ratio deficient ({self.binder_to_powder_weight_ratio:.2f} < 1.50)")
        if self.fumed_silica_pct < 1.5:
            rejections.append(f"Physical: Fumed silica {self.fumed_silica_pct:.1f}% below percolation threshold (>=1.5%)")
        if self.sedimentation_risk_index > 2.0:
            rejections.append(f"Physical: Stokes-Bingham sedimentation risk {self.sedimentation_risk_index:.2f} exceeds threshold (<=2.0)")

        return (len(rejections) == 0, rejections)


FEATURE_PROVENANCE_MAP: Dict[str, FeatureProvenance] = {
    "syn_wax_pct": FeatureProvenance.MEASURED,
    "candelilla_wax_pct": FeatureProvenance.MEASURED,
    "peg8_beeswax_pct": FeatureProvenance.MEASURED,
    "dimethicone_pct": FeatureProvenance.MEASURED,
    "caprylyl_methicone_pct": FeatureProvenance.MEASURED,
    "mq_resin_solution_pct": FeatureProvenance.MEASURED,
    "alkyl_benzoate_pct": FeatureProvenance.MEASURED,
    "porous_silica_pct": FeatureProvenance.MEASURED,
    "fumed_silica_pct": FeatureProvenance.MEASURED,
    "pmssq_pct": FeatureProvenance.MEASURED,
    "boron_nitride_pct": FeatureProvenance.MEASURED,
    "zinc_oxide_pct": FeatureProvenance.MEASURED,
    "fill_temperature_c": FeatureProvenance.MEASURED,
    "cooling_rate_c_min": FeatureProvenance.MEASURED,
    "homogenizer_shear_rpm": FeatureProvenance.MEASURED,
    "total_powder_wt_pct": FeatureProvenance.DERIVED_PHYSICAL,
    "total_wax_wt_pct": FeatureProvenance.DERIVED_PHYSICAL,
    "total_silicone_wt_pct": FeatureProvenance.DERIVED_PHYSICAL,
    "wax_volume_fraction": FeatureProvenance.DERIVED_PHYSICAL,
    "silicone_volume_fraction": FeatureProvenance.DERIVED_PHYSICAL,
    "powder_volume_fraction": FeatureProvenance.DERIVED_PHYSICAL,
    "solid_volume_fraction": FeatureProvenance.DERIVED_PHYSICAL,
    "total_particle_surface_area_m2_g": FeatureProvenance.DERIVED_PHYSICAL,
    "total_oil_absorption_demand_ml_100g": FeatureProvenance.DERIVED_EMPIRICAL,
    "liquid_to_surface_area_ratio": FeatureProvenance.DERIVED_PHYSICAL,
    "binder_to_powder_weight_ratio": FeatureProvenance.DERIVED_EMPIRICAL,
    "wax_crystallization_enthalpy_composite_j_g": FeatureProvenance.HYPOTHESIS,
    "fumed_silica_percolation_ratio": FeatureProvenance.HYPOTHESIS,
    "sedimentation_risk_index": FeatureProvenance.DERIVED_PHYSICAL,
    "slip_lubricity_index": FeatureProvenance.DERIVED_EMPIRICAL,
}


class GS40FeatureEngine:
    """
    Computes physics-informed feature vectors from raw material database and formulation specs.
    """

    DEFAULT_DENSITIES = {
        "Synthetic Wax": 0.92,
        "Candelilla Wax": 0.98,
        "PEG-8 Beeswax": 0.96,
        "Dimethicone": 0.965,
        "Caprylyl Methicone": 0.835,
        "MQ Resin Solution": 1.04,
        "C12-15 Alkyl Benzoate": 0.96,
        "Porous Silica": 2.20,
        "Silica Dimethyl Silylate": 2.20,
        "PMSSQ": 1.32,
        "Boron Nitride": 2.25,
        "Zinc Oxide": 5.60,
        "Preservative / Active": 0.98,
    }

    DEFAULT_BET = {
        "Porous Silica": 350.0,
        "Silica Dimethyl Silylate": 110.0,
        "PMSSQ": 25.0,
        "Boron Nitride": 4.5,
        "Zinc Oxide": 18.0,
    }

    DEFAULT_OIL_ABSORPTION = {
        "Porous Silica": 150.0,
        "Silica Dimethyl Silylate": 280.0,
        "PMSSQ": 45.0,
        "Boron Nitride": 65.0,
        "Zinc Oxide": 30.0,
    }

    @classmethod
    def extract_from_weights(
        cls,
        weights: Dict[str, float],
        fill_temp_c: float = 80.0,
        cooling_rate_c_min: float = 2.5,
        shear_rpm: float = 2500.0,
        raw_materials_db_path: Optional[Path] = None
    ) -> FormulationFeatureVector:
        # 1. Resolve raw weight percentages (defaults aligned with GS40 Rev.7.3 center)
        syn_wax = float(weights.get("Synthetic Wax", weights.get("syn_wax_pct", 12.0)))
        can_wax = float(weights.get("Candelilla Wax", weights.get("candelilla_wax_pct", 5.0)))
        peg8 = float(weights.get("PEG-8 Beeswax", weights.get("peg8_beeswax_pct", 0.0)))

        dimeth = float(weights.get("Dimethicone", weights.get("dimethicone_pct", 17.0)))
        caprylyl = float(weights.get("Caprylyl Methicone", weights.get("caprylyl_methicone_pct", 11.0)))
        mq_resin = float(weights.get("MQ Resin Solution", weights.get("mq_resin_solution_pct", 2.0)))
        ab_ester = float(weights.get("C12-15 Alkyl Benzoate", weights.get("alkyl_benzoate_pct", 24.0)))

        porous_silica = float(weights.get("Porous Silica", weights.get("porous_silica_pct", 10.0)))
        fumed_silica = float(weights.get("Silica Dimethyl Silylate", weights.get("fumed_silica_pct", 2.0)))
        pmssq = float(weights.get("PMSSQ", weights.get("pmssq_pct", 8.0)))
        bn = float(weights.get("Boron Nitride", weights.get("boron_nitride_pct", 3.0)))
        zno = float(weights.get("Zinc Oxide", weights.get("zinc_oxide_pct", 5.0)))
        active_pres = float(weights.get("Active / Preservative", weights.get("active_preservative_pct", 1.0)))

        # 2. Aggregations
        tot_wax = syn_wax + can_wax + peg8
        tot_silicone = dimeth + caprylyl + mq_resin
        tot_liquid = dimeth + caprylyl + mq_resin + ab_ester + active_pres
        tot_powder = porous_silica + fumed_silica + pmssq + bn + zno

        # 3. Volume Calculations
        vol_syn_wax = syn_wax / cls.DEFAULT_DENSITIES["Synthetic Wax"]
        vol_can_wax = can_wax / cls.DEFAULT_DENSITIES["Candelilla Wax"]
        vol_peg8 = peg8 / cls.DEFAULT_DENSITIES["PEG-8 Beeswax"]
        vol_wax = vol_syn_wax + vol_can_wax + vol_peg8

        vol_dimeth = dimeth / cls.DEFAULT_DENSITIES["Dimethicone"]
        vol_cap = caprylyl / cls.DEFAULT_DENSITIES["Caprylyl Methicone"]
        vol_mq = mq_resin / cls.DEFAULT_DENSITIES["MQ Resin Solution"]
        vol_ab = ab_ester / cls.DEFAULT_DENSITIES["C12-15 Alkyl Benzoate"]
        vol_pres = active_pres / cls.DEFAULT_DENSITIES["Preservative / Active"]
        vol_silicone = vol_dimeth + vol_cap + vol_mq
        vol_liquid = vol_silicone + vol_ab + vol_pres

        vol_psil = porous_silica / cls.DEFAULT_DENSITIES["Porous Silica"]
        vol_fsil = fumed_silica / cls.DEFAULT_DENSITIES["Silica Dimethyl Silylate"]
        vol_pmssq = pmssq / cls.DEFAULT_DENSITIES["PMSSQ"]
        vol_bn = bn / cls.DEFAULT_DENSITIES["Boron Nitride"]
        vol_zno = zno / cls.DEFAULT_DENSITIES["Zinc Oxide"]
        vol_powder = vol_psil + vol_fsil + vol_pmssq + vol_bn + vol_zno

        total_vol = vol_wax + vol_liquid + vol_powder

        phi_wax = vol_wax / total_vol if total_vol > 0 else 0.0
        phi_silicone = vol_silicone / total_vol if total_vol > 0 else 0.0
        phi_powder = vol_powder / total_vol if total_vol > 0 else 0.0
        phi_solid = (vol_wax + vol_powder) / total_vol if total_vol > 0 else 0.0

        # 4. Surface Area & Oil Demand
        bet_sum = (
            porous_silica * cls.DEFAULT_BET["Porous Silica"] +
            fumed_silica * cls.DEFAULT_BET["Silica Dimethyl Silylate"] +
            pmssq * cls.DEFAULT_BET["PMSSQ"] +
            bn * cls.DEFAULT_BET["Boron Nitride"] +
            zno * cls.DEFAULT_BET["Zinc Oxide"]
        ) / 100.0  # m2 per gram of total formula

        oa_sum = (
            porous_silica * cls.DEFAULT_OIL_ABSORPTION["Porous Silica"] +
            fumed_silica * cls.DEFAULT_OIL_ABSORPTION["Silica Dimethyl Silylate"] +
            pmssq * cls.DEFAULT_OIL_ABSORPTION["PMSSQ"] +
            bn * cls.DEFAULT_OIL_ABSORPTION["Boron Nitride"] +
            zno * cls.DEFAULT_OIL_ABSORPTION["Zinc Oxide"]
        ) / 100.0  # ml oil demand per 100g formula

        liq_to_sa = (tot_liquid / bet_sum) if bet_sum > 0 else 1.0
        binder_to_pow = (tot_wax + tot_silicone) / tot_powder if tot_powder > 0 else 1.0

        # 5. Network & Crystallization Mechanics
        # SynWax: 195 J/g, Candelilla: 142 J/g
        wax_enthalpy = (syn_wax * 195.0 + can_wax * 142.0) / (tot_wax if tot_wax > 0 else 1.0)
        
        # Fumed silica percolation ratio (percolation threshold c* ~ 1.5 wt%)
        percolation_ratio = fumed_silica / 1.5

        # Stokes-Bingham sedimentation risk of dense ZnO (density 5.6 g/cm3 vs oil 0.9 g/cm3)
        # Higher temperature reduces viscosity -> higher settling risk; higher R972 -> network yield arrests settling
        temp_factor = (fill_temp_c - 70.0) / 15.0  # Normalized around 70-85°C
        network_retardation = 1.0 + (fumed_silica / 1.5) ** 2.0
        sedimentation_risk = float(np.clip((zno / 5.0) * (1.0 + 0.5 * temp_factor) / network_retardation, 0.05, 5.0))

        # Lubricity Index: Synergistic sliding (BN) + rolling (PMSSQ)
        slip_lubricity = (bn * 1.5 + pmssq * 1.0) / 10.0

        return FormulationFeatureVector(
            syn_wax_pct=syn_wax,
            candelilla_wax_pct=can_wax,
            peg8_beeswax_pct=peg8,
            dimethicone_pct=dimeth,
            caprylyl_methicone_pct=caprylyl,
            mq_resin_solution_pct=mq_resin,
            alkyl_benzoate_pct=ab_ester,
            porous_silica_pct=porous_silica,
            fumed_silica_pct=fumed_silica,
            pmssq_pct=pmssq,
            boron_nitride_pct=bn,
            zinc_oxide_pct=zno,
            active_preservative_pct=active_pres,
            fill_temperature_c=fill_temp_c,
            cooling_rate_c_min=cooling_rate_c_min,
            homogenizer_shear_rpm=shear_rpm,
            total_powder_wt_pct=tot_powder,
            total_wax_wt_pct=tot_wax,
            total_silicone_wt_pct=tot_silicone,
            total_liquid_wt_pct=tot_liquid,
            wax_volume_fraction=round(phi_wax, 4),
            silicone_volume_fraction=round(phi_silicone, 4),
            powder_volume_fraction=round(phi_powder, 4),
            solid_volume_fraction=round(phi_solid, 4),
            total_particle_surface_area_m2_g=round(bet_sum, 2),
            total_oil_absorption_demand_ml_100g=round(oa_sum, 2),
            liquid_to_surface_area_ratio=round(liq_to_sa, 4),
            binder_to_powder_weight_ratio=round(binder_to_pow, 4),
            wax_crystallization_enthalpy_composite_j_g=round(wax_enthalpy, 2),
            fumed_silica_percolation_ratio=round(percolation_ratio, 3),
            sedimentation_risk_index=round(sedimentation_risk, 3),
            slip_lubricity_index=round(slip_lubricity, 3),
        )

"""
GLIDE-SPEC 40 - Raw Material Master Schema & Catalog
Manages raw material specifications with explicit TBD tracking and strict validation.
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class MaterialType(str, Enum):
    POWDER = "POWDER"
    WAX = "WAX"
    SILICONE = "SILICONE"
    RESIN = "RESIN"
    EMOLLIENT = "EMOLLIENT"
    ACTIVE = "ACTIVE"
    PRESERVATIVE_BOOSTER = "PRESERVATIVE_BOOSTER"


class MaterialStatus(str, Enum):
    TBD = "TBD"
    CANDIDATE = "CANDIDATE"
    VERIFIED = "VERIFIED"
    LOCKED = "LOCKED"


class RatioType(str, Enum):
    ABSOLUTE_ACTIVE_PERCENT = "ABSOLUTE_ACTIVE_PERCENT"
    RELATIVE_RATIO = "RELATIVE_RATIO"


class CompositeComponent(BaseModel):
    material_id: str
    ratio: Optional[float] = None


class CompositeMaterial(BaseModel):
    """Versioned blend definition; DOE supplies ratios when they are unlocked."""
    material_id: str
    material_name: str
    components: List[CompositeComponent]
    ratio_type: RatioType = RatioType.ABSOLUTE_ACTIVE_PERCENT
    version: str = "Rev.7.3"
    notes: str = ""


class RawMaterial(BaseModel):
    material_id: str
    inci: str
    trade_name: Optional[str] = "TBD"
    supplier: Optional[str] = "TBD"
    grade: Optional[str] = "TBD"
    material_type: MaterialType
    active_pct: Optional[float] = None  # None indicates TBD
    carrier: Optional[str] = "TBD"
    carrier_pct: Optional[float] = None
    solvent: Optional[str] = "TBD"
    moisture: Optional[float] = None
    density: Optional[float] = None
    viscosity: Optional[float] = None
    particle_size: Optional[str] = "TBD"
    d50: Optional[float] = None  # in micrometers
    d90: Optional[float] = None  # in micrometers
    bet: Optional[float] = None  # m^2/g
    oil_absorption: Optional[float] = None  # g/100g
    surface_treatment: Optional[str] = "TBD"
    purity: Optional[str] = "TBD"
    cost_per_kg: Optional[float] = None
    recommended_use_min: Optional[float] = None
    recommended_use_max: Optional[float] = None
    tds_reference: Optional[str] = "TBD"
    sds_reference: Optional[str] = "TBD"
    coa_reference: Optional[str] = "TBD"
    status: MaterialStatus = MaterialStatus.TBD
    notes: Optional[str] = ""

    def is_specification_complete(self) -> bool:
        """Returns True only when all mandatory specs for manufacturing are present."""
        if self.active_pct is None:
            return False
        if self.trade_name == "TBD" or self.supplier == "TBD":
            return False
        return True


# Predefined baseline raw material groups for Rev.7.3 (with explicit TBD state)
REV73_RAW_MATERIALS = {
    "MAT-BN-01": RawMaterial(
        material_id="MAT-BN-01",
        inci="Boron Nitride",
        trade_name="TBD",
        supplier="TBD",
        grade="Cosmetic h-BN (Platelet)",
        material_type=MaterialType.POWDER,
        active_pct=100.0,
        d50=10.0,
        surface_treatment="Untreated",
        status=MaterialStatus.TBD,
        notes="Platelet dry lubricant, D50 <= 10 um"
    ),
    "MAT-SILICA-01": RawMaterial(
        material_id="MAT-SILICA-01",
        inci="Silica",
        trade_name="TBD",
        supplier="TBD",
        grade="Porous Spherical Silica",
        material_type=MaterialType.POWDER,
        active_pct=100.0,
        d50=10.0,
        status=MaterialStatus.TBD,
        notes="Porous spherical silica, sebum/sweat absorption"
    ),
    "MAT-FUMED-01": RawMaterial(
        material_id="MAT-FUMED-01",
        inci="Silica Dimethyl Silylate",
        trade_name="TBD",
        supplier="TBD",
        grade="Fumed Silica (Hydrophobic)",
        material_type=MaterialType.POWDER,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Thixotropic anti-settling agent"
    ),
    "MAT-PMSSQ-01": RawMaterial(
        material_id="MAT-PMSSQ-01",
        inci="Polymethylsilsesquioxane",
        trade_name="TBD",
        supplier="TBD",
        grade="Spherical Elastic Powder",
        material_type=MaterialType.POWDER,
        active_pct=100.0,
        d50=10.0,
        status=MaterialStatus.TBD,
        notes="Ball-bearing load distribution, velvety finish"
    ),
    "MAT-ZNO-01": RawMaterial(
        material_id="MAT-ZNO-01",
        inci="Zinc Oxide, Triethoxycaprylylsilane",
        trade_name="TBD",
        supplier="TBD",
        grade="Silane-Treated Zinc Oxide",
        material_type=MaterialType.POWDER,
        active_pct=96.0,  # Example: 96% ZnO active + 4% silane coat
        surface_treatment="Triethoxycaprylylsilane",
        d50=10.0,
        status=MaterialStatus.TBD,
        notes="Hydrophobic inorganic coating, zero chalking"
    ),
    "MAT-WAX-SYN-01": RawMaterial(
        material_id="MAT-WAX-SYN-01",
        inci="Synthetic Wax",
        trade_name="TBD",
        supplier="TBD",
        grade="High-melt Synthetic Wax",
        material_type=MaterialType.WAX,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Hardness structure matrix (Combined with Candelilla = 17%)"
    ),
    "MAT-WAX-CAN-01": RawMaterial(
        material_id="MAT-WAX-CAN-01",
        inci="Euphorbia Cerifera (Candelilla) Wax",
        trade_name="TBD",
        supplier="TBD",
        grade="Deodorized Purified Candelilla Wax",
        material_type=MaterialType.WAX,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Deodorized Candelilla Wax, pay-off balance"
    ),
    "MAT-PEG8-01": RawMaterial(
        material_id="MAT-PEG8-01",
        inci="PEG-8 Beeswax",
        trade_name="TBD",
        supplier="TBD",
        grade="Cosmetic Functional Emulsifying Wax",
        material_type=MaterialType.WAX,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Easy wash-off switch, detergent-sensitive emulsification"
    ),
    "MAT-SIL-DIM-01": RawMaterial(
        material_id="MAT-SIL-DIM-01",
        inci="Dimethicone",
        trade_name="TBD",
        supplier="TBD",
        grade="Low-viscosity Linear Dimethicone",
        material_type=MaterialType.SILICONE,
        active_pct=100.0,
        viscosity=None,  # TBD: 2 cSt, 5 cSt etc.
        status=MaterialStatus.TBD,
        notes="D4/D5/D6 Free linear silicone carrier"
    ),
    "MAT-SIL-CAP-01": RawMaterial(
        material_id="MAT-SIL-CAP-01",
        inci="Caprylyl Methicone",
        trade_name="TBD",
        supplier="TBD",
        grade="Volatile-like Alkyl Methicone",
        material_type=MaterialType.SILICONE,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Light silky slip carrier, D4/D5/D6 Free"
    ),
    "MAT-MQ-01": RawMaterial(
        material_id="MAT-MQ-01",
        inci="Trimethylsiloxysilicate",
        trade_name="TBD",
        supplier="TBD",
        grade="MQ Resin Premix Solution",
        material_type=MaterialType.RESIN,
        active_pct=None,  # TBD! Must be confirmed from CoA (e.g. 50~70% solid in solvent)
        carrier="TBD",    # e.g., Dimethicone or Isododecane
        carrier_pct=None,
        status=MaterialStatus.TBD,
        notes="Waterproof film former. 12.0% Active required in finished formula"
    ),
    "MAT-EMO-AB-01": RawMaterial(
        material_id="MAT-EMO-AB-01",
        inci="C12-15 Alkyl Benzoate",
        trade_name="TBD",
        supplier="TBD",
        grade="Ester Emollient & Powder Wetting Agent",
        material_type=MaterialType.EMOLLIENT,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Powder dispersion wetting and cold film plasticizer"
    ),
    "MAT-EHG-01": RawMaterial(
        material_id="MAT-EHG-01",
        inci="Ethylhexylglycerin",
        trade_name="TBD",
        supplier="TBD",
        grade="Deodorant Booster & Skin Conditioning",
        material_type=MaterialType.PRESERVATIVE_BOOSTER,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="Gram-positive bacterial inhibitor, sweat odor blocker"
    ),
    "MAT-ACT-BLEND-01": RawMaterial(
        material_id="MAT-ACT-BLEND-01",
        inci="Bisabolol, Stearyl Glycyrrhetinate, Tocopherol, Rosmarinus Officinalis Extract",
        trade_name="TBD",
        supplier="TBD",
        grade="Anhydrous Soothing & Anti-oxidation Blend",
        material_type=MaterialType.ACTIVE,
        active_pct=100.0,
        status=MaterialStatus.TBD,
        notes="2.0% total active soothing and rancidity defense blend"
    ),
}

# Composite membership belongs to the Material Master, not calculator code.
# Ratios stay unset until a DOE trial or a locked manufacturing formula supplies
# absolute target-active percentages.
REV73_COMPOSITE_MATERIALS = {
    "MAT-WAX-SYSTEM": CompositeMaterial(
        material_id="MAT-WAX-SYSTEM", material_name="Synthetic Wax + Candelilla Wax Blend",
        components=[CompositeComponent(material_id="MAT-WAX-SYN-01"), CompositeComponent(material_id="MAT-WAX-CAN-01")],
        notes="17% wax system; detailed ratio is DOE/production-formula controlled.",
    ),
    "MAT-SIL-SYSTEM": CompositeMaterial(
        material_id="MAT-SIL-SYSTEM", material_name="Dimethicone + Caprylyl Methicone Blend",
        components=[CompositeComponent(material_id="MAT-SIL-DIM-01"), CompositeComponent(material_id="MAT-SIL-CAP-01")],
        notes="28% silicone system; detailed ratio is DOE/production-formula controlled.",
    ),
}

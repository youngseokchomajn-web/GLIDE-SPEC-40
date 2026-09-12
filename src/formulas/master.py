"""
GLIDE-SPEC 40 - Formula Master Schema & Rev.7.3 Baseline Formula
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class FormulaType(str, Enum):
    TARGET_ACTIVE = "target_active"
    MANUFACTURING = "manufacturing"
    PILOT = "pilot"
    ENGINEERING = "engineering"
    PRODUCTION_MASTER = "production_master"


class FormulaStatus(str, Enum):
    DRAFT = "draft"
    CANDIDATE = "candidate"
    APPROVED = "approved"
    LOCKED = "locked"
    ARCHIVED = "archived"


class FormulaComponent(BaseModel):
    material_id: str
    material_name: str
    target_active_pct: float = Field(..., ge=0.0, le=100.0)
    raw_material_active_pct: Optional[float] = None
    calculated_charge_pct: Optional[float] = None
    notes: Optional[str] = ""


class FormulaMaster(BaseModel):
    formula_id: str
    product_id: str = "GLIDE-SPEC 40"
    revision: str = "Rev.7.3"
    formula_type: FormulaType
    status: FormulaStatus = FormulaStatus.LOCKED
    components: List[FormulaComponent]
    created_date: str = "2026-09-12"
    approved_date: Optional[str] = None
    notes: Optional[str] = ""

    def total_target_active_pct(self) -> float:
        return sum(c.target_active_pct for c in self.components)

    def total_charge_pct(self) -> Optional[float]:
        if any(c.calculated_charge_pct is None for c in self.components):
            return None
        return sum(c.calculated_charge_pct for c in self.components)


# Rev.7.3 Immutable Target Active Baseline Formula
REV73_TARGET_ACTIVE_FORMULA = FormulaMaster(
    formula_id="FORM-GLIDE40-REV7.3-ACTIVE",
    product_id="GLIDE-SPEC 40",
    revision="Rev.7.3",
    formula_type=FormulaType.TARGET_ACTIVE,
    status=FormulaStatus.LOCKED,
    components=[
        FormulaComponent(
            material_id="MAT-BN-01",
            material_name="Boron Nitride (Platelet h-BN)",
            target_active_pct=3.0,
            notes="Dry shear lubricant"
        ),
        FormulaComponent(
            material_id="MAT-SILICA-01",
            material_name="Porous Spherical Silica",
            target_active_pct=10.0,
            notes="Sebum/sweat absorption, texture"
        ),
        FormulaComponent(
            material_id="MAT-FUMED-01",
            material_name="Silica Dimethyl Silylate",
            target_active_pct=2.0,
            notes="Thixotropic anti-settling"
        ),
        FormulaComponent(
            material_id="MAT-PMSSQ-01",
            material_name="Polymethylsilsesquioxane (PMSSQ)",
            target_active_pct=8.0,
            notes="Micro ball-bearing load distribution"
        ),
        FormulaComponent(
            material_id="MAT-ZNO-01",
            material_name="Treated Zinc Oxide",
            target_active_pct=5.0,
            notes="Hydrophobic inorganic shield, zero chalking"
        ),
        FormulaComponent(
            material_id="MAT-WAX-SYSTEM",
            material_name="Synthetic Wax + Candelilla Wax Blend",
            target_active_pct=17.0,
            notes="Hardness matrix (detailed ratio TBD in pilot)"
        ),
        FormulaComponent(
            material_id="MAT-PEG8-01",
            material_name="PEG-8 Beeswax",
            target_active_pct=3.0,
            notes="Easy wash-off trigger wax"
        ),
        FormulaComponent(
            material_id="MAT-SIL-SYSTEM",
            material_name="Dimethicone + Caprylyl Methicone Blend",
            target_active_pct=28.0,
            notes="Carrier system (D4/D5/D6 Free, detailed ratio TBD)"
        ),
        FormulaComponent(
            material_id="MAT-MQ-01",
            material_name="MQ Resin (Trimethylsiloxysilicate)",
            target_active_pct=12.0,
            notes="Waterproof film active 12.0% (Charge % depends on supplier active %)"
        ),
        FormulaComponent(
            material_id="MAT-EMO-AB-01",
            material_name="C12-15 Alkyl Benzoate",
            target_active_pct=9.5,
            notes="Powder wetting and anti-crack plasticizer"
        ),
        FormulaComponent(
            material_id="MAT-EHG-01",
            material_name="Ethylhexylglycerin",
            target_active_pct=0.5,
            notes="Gram-positive bacterial inhibitor"
        ),
        FormulaComponent(
            material_id="MAT-ACT-BLEND-01",
            material_name="Bisabolol + Stearyl Glycyrrhetinate + Tocopherol + Rosemary",
            target_active_pct=2.0,
            notes="Soothing & rancidity defense blend"
        ),
    ],
    created_date="2026-09-12",
    notes="Official Rev.7.3 Target Active Baseline Formula (Sum = 100.0%). Immutable."
)

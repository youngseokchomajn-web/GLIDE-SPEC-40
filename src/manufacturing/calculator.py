"""
GLIDE-SPEC 40 - Manufacturing Formula Calculator & Batch Scaler
Implements active-to-manufacturing conversion, carrier solvent offsetting,
batch weight scaling, and specification completeness gating.
"""

from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.materials.master import RawMaterial, MaterialStatus
from src.formulas.master import FormulaMaster, FormulaComponent, FormulaType, FormulaStatus


class BatchScaleSpec(BaseModel):
    batch_name: str
    target_weight_kg: float
    description: str


STANDARD_BATCH_SIZES: Dict[str, BatchScaleSpec] = {
    "100g_lab": BatchScaleSpec(batch_name="100g Lab", target_weight_kg=0.1, description="Initial bench beaker sample"),
    "1kg_confirm": BatchScaleSpec(batch_name="1kg Confirmation", target_weight_kg=1.0, description="Pre-pilot homogeneity check"),
    "3kg_pilot": BatchScaleSpec(batch_name="3kg Pilot", target_weight_kg=3.0, description="Small pilot dispersion & fill trial"),
    "5kg_pilot": BatchScaleSpec(batch_name="5kg Pilot", target_weight_kg=5.0, description="Standard pilot batch"),
    "10kg_eng": BatchScaleSpec(batch_name="10kg Engineering", target_weight_kg=10.0, description="Equipment parameter validation"),
    "20kg_eng": BatchScaleSpec(batch_name="20kg Engineering", target_weight_kg=20.0, description="Pre-production hot-melt check"),
    "66kg_initial_charge": BatchScaleSpec(batch_name="66kg Initial Charge", target_weight_kg=66.0, description="Production candidate charge (3000 pcs target)")
}


class BatchChargeItem(BaseModel):
    material_id: str
    material_name: str
    inci: str
    charge_pct: float
    charge_weight_g: float
    charge_weight_kg: float
    active_contribution_pct: float
    cost_per_kg: Optional[float] = None
    item_total_cost: Optional[float] = None
    notes: Optional[str] = ""


class ManufacturingCalculationResult(BaseModel):
    is_valid: bool
    formula_id: str
    revision: str
    batch_size_kg: float
    total_charge_pct: float
    items: List[BatchChargeItem]
    missing_specs: List[str]
    carrier_offsets_applied: List[str]
    total_raw_material_cost: Optional[float] = None
    cost_per_20g_stick: Optional[float] = None
    target_cogs_per_stick: float = 2950.0  # KRW
    cogs_budget_pct: Optional[float] = None
    warnings: List[str]


class ManufacturingCalculator:
    """
    Computes real production charge percentages and weights from target active formulas.
    """

    @staticmethod
    def calculate_single_charge_pct(target_active_pct: float, raw_active_pct: float) -> float:
        """
        Charge % = Target Active % / (Raw Material Active % / 100)
        Example: 12% active from 60% active raw material = 12 / 0.60 = 20.0%
        """
        if raw_active_pct <= 0:
            raise ValueError(f"Raw material active % must be positive, got {raw_active_pct}")
        return target_active_pct / (raw_active_pct / 100.0)

    @classmethod
    def generate_manufacturing_formula(
        cls,
        active_formula: FormulaMaster,
        material_specs: Dict[str, RawMaterial],
        batch_size_kg: float,
        offset_carrier: bool = True
    ) -> ManufacturingCalculationResult:
        missing_specs: List[str] = []
        warnings: List[str] = []
        carrier_offsets_applied: List[str] = []
        items: List[BatchChargeItem] = []

        total_target = active_formula.total_target_active_pct()
        if abs(total_target - 100.0) > 0.001:
            warnings.append(f"Target active formula total is {total_target:.2f}%, expected 100.0%")

        # First pass: check specs and compute nominal charges
        nominal_charges: Dict[str, float] = {}
        for comp in active_formula.components:
            mat = material_specs.get(comp.material_id)
            if not mat:
                missing_specs.append(f"Material {comp.material_id} ({comp.material_name}) missing from Raw Material Master.")
                continue

            if mat.active_pct is None:
                missing_specs.append(f"Material {comp.material_id} active_pct is TBD/Unconfirmed.")
                continue

            charge_pct = cls.calculate_single_charge_pct(comp.target_active_pct, mat.active_pct)
            nominal_charges[comp.material_id] = charge_pct

        if missing_specs:
            return ManufacturingCalculationResult(
                is_valid=False,
                formula_id=f"MFG-{active_formula.formula_id}",
                revision=active_formula.revision,
                batch_size_kg=batch_size_kg,
                total_charge_pct=0.0,
                items=[],
                missing_specs=missing_specs,
                carrier_offsets_applied=[],
                warnings=warnings + ["Manufacturing Formula CANNOT be finalized without confirmed raw material specs."]
            )

        # Second pass: Carrier Solvent Offsetting (e.g. MQ Resin carrier offset against Silicone carrier pool)
        final_charges = dict(nominal_charges)
        if offset_carrier:
            for comp in active_formula.components:
                mat = material_specs[comp.material_id]
                # If raw material is a solution/premix with a known carrier
                if mat.active_pct < 100.0 and mat.carrier and mat.carrier != "TBD":
                    solvent_pct_in_raw = 100.0 - mat.active_pct
                    actual_solvent_introduced_pct = final_charges[comp.material_id] * (solvent_pct_in_raw / 100.0)

                    # Look for corresponding carrier recipient in formula (e.g., silicone blend)
                    carrier_recipient_id = None
                    if "dimethicone" in mat.carrier.lower() or "silicone" in mat.carrier.lower():
                        carrier_recipient_id = "MAT-SIL-SYSTEM"

                    if carrier_recipient_id and carrier_recipient_id in final_charges:
                        previous_carrier_charge = final_charges[carrier_recipient_id]
                        new_carrier_charge = max(0.0, previous_carrier_charge - actual_solvent_introduced_pct)
                        final_charges[carrier_recipient_id] = new_carrier_charge
                        carrier_offsets_applied.append(
                            f"Subtracted {actual_solvent_introduced_pct:.2f}% from {carrier_recipient_id} "
                            f"due to {mat.carrier} solvent introduced by {comp.material_name} "
                            f"({previous_carrier_charge:.2f}% -> {new_carrier_charge:.2f}%)"
                        )

        total_charge_pct = sum(final_charges.values())
        total_cost: float = 0.0
        has_cost_data = True

        for comp in active_formula.components:
            mat = material_specs[comp.material_id]
            charge_pct = final_charges[comp.material_id]
            weight_kg = (batch_size_kg * charge_pct) / 100.0
            weight_g = weight_kg * 1000.0

            item_cost = None
            if mat.cost_per_kg is not None:
                item_cost = weight_kg * mat.cost_per_kg
                total_cost += item_cost
            else:
                has_cost_data = False

            items.append(BatchChargeItem(
                material_id=comp.material_id,
                material_name=comp.material_name,
                inci=mat.inci,
                charge_pct=round(charge_pct, 4),
                charge_weight_g=round(weight_g, 3),
                charge_weight_kg=round(weight_kg, 4),
                active_contribution_pct=comp.target_active_pct,
                cost_per_kg=mat.cost_per_kg,
                item_total_cost=round(item_cost, 2) if item_cost is not None else None,
                notes=comp.notes or ""
            ))

        cost_per_stick = None
        cogs_budget_pct = None
        if has_cost_data and batch_size_kg > 0:
            # 20g stick net weight = 0.02 kg
            cost_per_kg_bulk = total_cost / batch_size_kg
            cost_per_stick = round(cost_per_kg_bulk * 0.02, 2)
            cogs_budget_pct = round((cost_per_stick / 2950.0) * 100.0, 1)

        return ManufacturingCalculationResult(
            is_valid=True,
            formula_id=f"MFG-{active_formula.formula_id}",
            revision=active_formula.revision,
            batch_size_kg=batch_size_kg,
            total_charge_pct=round(total_charge_pct, 4),
            items=items,
            missing_specs=[],
            carrier_offsets_applied=carrier_offsets_applied,
            total_raw_material_cost=round(total_cost, 2) if has_cost_data else None,
            cost_per_20g_stick=cost_per_stick,
            target_cogs_per_stick=2950.0,
            cogs_budget_pct=cogs_budget_pct,
            warnings=warnings
        )

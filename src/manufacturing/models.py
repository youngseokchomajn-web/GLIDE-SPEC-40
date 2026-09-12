"""
GLIDE-SPEC 40 - Manufacturing Batch Model & Snapshot
Represents an executed production batch with frozen formulation charges,
material lot/cost snapshots, process parameters, and formal COGS quote status.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from src.manufacturing.calculator import BatchChargeItem
from src.qc.models import ProcessCondition


class ManufacturingBatch(BaseModel):
    batch_id: str
    trial_id: Optional[str] = None  # Link to DOETrial if executed under DOE
    formula_id: str
    revision: str = "Rev.7.3"
    created_date: str
    operator: str
    batch_size_kg: float
    total_charge_pct: float
    items: List[BatchChargeItem]
    process_conditions: ProcessCondition
    total_raw_material_cost: Optional[float] = None
    cost_per_20g_stick: Optional[float] = None
    target_cogs_per_stick: float = 2950.0

    # Phase 2A Data Contract: Explicit COGS quote status & price source tracking
    cogs_basis: str = "ESTIMATED_SIMULATION"  # "ESTIMATED_SIMULATION" vs "CONFIRMED_SUPPLIER_QUOTES"
    material_price_source: str = "Baseline Simulation Fixture"  # e.g., "Supplier Quote REQ-GLIDE40-MAT-202609"
    quote_status: str = "PENDING_FORMAL_QUOTES"  # "PENDING_FORMAL_QUOTES" vs "LOCKED_PRODUCTION_QUOTES"
    calculated_at: Optional[str] = None  # ISO timestamp of cost computation

    notes: Optional[str] = ""

    def get_charge_for_material(self, material_id: str) -> Optional[float]:
        for item in self.items:
            if item.material_id == material_id:
                return item.charge_pct
        return None

    def is_cogs_confirmed(self) -> bool:
        return self.cogs_basis == "CONFIRMED_SUPPLIER_QUOTES" and self.quote_status == "LOCKED_PRODUCTION_QUOTES"

"""
GLIDE-SPEC 40 - Revision Tracker & Change Control System
Enforces immutable revision baselines and auditable change logs.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    ADDED = "Added"
    MODIFIED = "Modified"
    DELETED = "Deleted"


class RevisionChangeItem(BaseModel):
    change_id: str
    revision: str
    change_type: ChangeType
    item: str
    previous_value: Optional[str]
    new_value: str
    reason: str
    experimental_evidence: str = "TBD / Theoretical baseline"
    date: str = "2026-09-12"
    related_batch_id: Optional[str] = None


class RevisionMaster(BaseModel):
    product_name: str = "GLIDE-SPEC 40"
    baseline_revision: str = "Rev.7.3"
    current_revision: str = "Rev.7.3"
    is_locked: bool = True
    changes: List[RevisionChangeItem] = Field(default_factory=list)


# Rev.7.3 Baseline Formal Change Log Register
REV73_BASELINE_CHANGES: List[RevisionChangeItem] = [
    RevisionChangeItem(
        change_id="NEW-01",
        revision="Rev.7.3",
        change_type=ChangeType.ADDED,
        item="Active / Manufacturing Formula Separation",
        previous_value="Unified 100% Locked Formula",
        new_value="Target Active Formula vs Manufacturing Formula Separated",
        reason="Account for raw material active concentrations (e.g. MQ resin solutions) and carrier dilution",
        experimental_evidence="Engineering baseline definition"
    ),
    RevisionChangeItem(
        change_id="NEW-02",
        revision="Rev.7.3",
        change_type=ChangeType.MODIFIED,
        item="Anhydrous Claim Status",
        previous_value="100% Anhydrous (Fixed)",
        new_value="Conditional (Pending raw material moisture & carrier verification)",
        reason="Avoid premature legal compliance risk before raw material CoA check",
        experimental_evidence="Regulatory compliance review"
    ),
    RevisionChangeItem(
        change_id="NEW-03",
        revision="Rev.7.3",
        change_type=ChangeType.MODIFIED,
        item="Fill Temperature Specification",
        previous_value="80 deg C (Fixed)",
        new_value="80 deg C (Initial Process Candidate)",
        reason="Prevent silicone carrier evaporation or sink mark prior to pilot rheology test",
        experimental_evidence="Process engineering baseline"
    ),
    RevisionChangeItem(
        change_id="NEW-04",
        revision="Rev.7.3",
        change_type=ChangeType.MODIFIED,
        item="66 kg Batch Charge Definition",
        previous_value="60 kg + 10% Fixed Loss = 66 kg (Fixed)",
        new_value="66 kg = Initial Charge Candidate",
        reason="Actual pipeline and filling nozzle dead-volume losses must be calculated empirically in pilot",
        experimental_evidence="Pilot scale-up validation requirement"
    ),
    RevisionChangeItem(
        change_id="NEW-05",
        revision="Rev.7.3",
        change_type=ChangeType.ADDED,
        item="Package Validation Independence",
        previous_value="Integrated into general QC",
        new_value="Separated into independent package qualification protocol",
        reason="100% All-PP ESC resistance, ratchet torque, and anti-pushback require distinct mechanical testing",
        experimental_evidence="Packaging mechanics risk mitigation"
    ),
    RevisionChangeItem(
        change_id="NEW-06",
        revision="Rev.7.3",
        change_type=ChangeType.ADDED,
        item="Raw Material Spec Gatekeeper",
        previous_value="None",
        new_value="Mandatory TDS/CoA/Active% spec before production formula lock",
        reason="Prevent batch failure caused by unknown solvent or particle size differences",
        experimental_evidence="QC risk prevention"
    ),
    RevisionChangeItem(
        change_id="NEW-07",
        revision="Rev.7.3",
        change_type=ChangeType.ADDED,
        item="28% Powder System Dispersion Gate",
        previous_value="Standard powder addition",
        new_value="Core validation target (Agglomeration, wetting, air entrapment)",
        reason="High solids loading (28%) is the primary source of process failure and chalking",
        experimental_evidence="Rheological stability assessment"
    ),
    RevisionChangeItem(
        change_id="NEW-08",
        revision="Rev.7.3",
        change_type=ChangeType.ADDED,
        item="MQ Resin Active Calculation Mandatory",
        previous_value="Manual / Assumed 12%",
        new_value="Mandatory automated charge formula conversion",
        reason="MQ resin is typically supplied as 50~70% solid in solvent carrier",
        experimental_evidence="Polymer resin chemistry requirements"
    ),
]


def get_rev73_revision_master() -> RevisionMaster:
    return RevisionMaster(
        product_name="GLIDE-SPEC 40",
        baseline_revision="Rev.7.3",
        current_revision="Rev.7.3",
        is_locked=True,
        changes=REV73_BASELINE_CHANGES
    )

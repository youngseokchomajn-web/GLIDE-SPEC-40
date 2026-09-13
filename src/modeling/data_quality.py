"""
GLIDE-SPEC 40 - Data Quality Scoring & Provenance Rubric
Evaluates public domain benchmarks and internal data across 7 dimensions
to ensure only high-fidelity datasets inform physical surrogate priors.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class QualityTier(str, Enum):
    TIER_1_CORE_BENCHMARK = "TIER_1_CORE_BENCHMARK"         # Score >= 80%: Rigorous benchmark with replicates
    TIER_2_PHYSICAL_PRIOR = "TIER_2_PHYSICAL_PRIOR"         # Score 65-79%: Useful rheology/thermal prior
    TIER_3_DIRECTIONAL_GUIDE = "TIER_3_DIRECTIONAL_GUIDE"   # Score 50-64%: Directional guidance only
    UNQUALIFIED = "UNQUALIFIED"                             # Score < 50%: Excluded from quantitative prior


@dataclass
class QualityScoreResult:
    dataset_name: str
    composite_score_pct: float
    tier: QualityTier
    dimension_scores: Dict[str, float]  # Score out of 100 for each dimension
    dimension_weights: Dict[str, float]
    provenance_tag: str
    audit_notes: List[str] = field(default_factory=list)

    def is_admissible_for_surrogate_prior(self) -> bool:
        return self.tier in (QualityTier.TIER_1_CORE_BENCHMARK, QualityTier.TIER_2_PHYSICAL_PRIOR)


class DataQualityAuditor:
    """
    7-Dimensional Scientific Quality Rubric:
      1. Formulation Completeness (Weight: 20%)
      2. Measurement Quality (Weight: 20%)
      3. Replicate Availability (Weight: 15%)
      4. Method Completeness (Weight: 15%)
      5. Feature Overlap with GS-40 (Weight: 15%)
      6. License Integrity (Weight: 10%)
      7. Provenance Traceability (Weight: 5%)
    """

    WEIGHTS = {
        "formulation_completeness": 0.20,
        "measurement_quality": 0.20,
        "replicate_availability": 0.15,
        "method_completeness": 0.15,
        "feature_overlap": 0.15,
        "license_integrity": 0.10,
        "provenance_traceability": 0.05,
    }

    @classmethod
    def evaluate(
        cls,
        dataset_name: str,
        formulation_completeness: float,   # 0.0 to 100.0
        measurement_quality: float,        # 0.0 to 100.0
        has_replicates: bool,
        replicate_count: int = 1,
        method_completeness: float = 80.0, # 0.0 to 100.0
        feature_overlap: float = 75.0,     # 0.0 to 100.0
        license_type: str = "OPEN",        # "CC_BY", "CC_BY_NC", "PATENT", "RESTRICTED"
        has_doi_or_patent: bool = True,
        provenance_status: str = "MEASURED"
    ) -> QualityScoreResult:
        notes = []

        # 1. Formulation Completeness
        f_score = max(0.0, min(100.0, float(formulation_completeness)))
        if f_score < 80.0:
            notes.append("Incomplete formulation mass balance (<80%).")

        # 2. Measurement Quality
        m_score = max(0.0, min(100.0, float(measurement_quality)))

        # 3. Replicate Availability
        if has_replicates and replicate_count >= 3:
            r_score = 100.0
        elif has_replicates and replicate_count == 2:
            r_score = 75.0
        elif has_replicates:
            r_score = 50.0
        else:
            r_score = 20.0
            notes.append("No experimental replicates reported (n=1 single point).")

        # 4. Method Completeness
        meth_score = max(0.0, min(100.0, float(method_completeness)))

        # 5. Feature Overlap
        ov_score = max(0.0, min(100.0, float(feature_overlap)))

        # 6. License Integrity
        lic = license_type.upper()
        if "CC_BY" in lic or "CC-BY" in lic or "OPEN" in lic:
            lic_score = 100.0
        elif "PATENT" in lic:
            lic_score = 90.0
        elif "CC_BY_NC" in lic or "CC-BY-NC" in lic:
            lic_score = 80.0
        else:
            lic_score = 30.0
            notes.append("Restricted or ambiguous data license.")

        # 7. Provenance
        prov_score = 100.0 if has_doi_or_patent else 40.0
        if not has_doi_or_patent:
            notes.append("Missing peer-reviewed DOI or patent identifier.")

        dim_scores = {
            "formulation_completeness": f_score,
            "measurement_quality": m_score,
            "replicate_availability": r_score,
            "method_completeness": meth_score,
            "feature_overlap": ov_score,
            "license_integrity": lic_score,
            "provenance_traceability": prov_score,
        }

        composite = sum(dim_scores[k] * cls.WEIGHTS[k] for k in cls.WEIGHTS)

        if composite >= 80.0:
            tier = QualityTier.TIER_1_CORE_BENCHMARK
        elif composite >= 65.0:
            tier = QualityTier.TIER_2_PHYSICAL_PRIOR
        elif composite >= 50.0:
            tier = QualityTier.TIER_3_DIRECTIONAL_GUIDE
        else:
            tier = QualityTier.UNQUALIFIED

        return QualityScoreResult(
            dataset_name=dataset_name,
            composite_score_pct=round(composite, 2),
            tier=tier,
            dimension_scores=dim_scores,
            dimension_weights=cls.WEIGHTS,
            provenance_tag=provenance_status,
            audit_notes=notes
        )

#!/usr/bin/env python3
"""
GLIDE-SPEC 40 - Domain Prior Quality Audit & Governance Generator
Runs the 7-Dimensional Data Quality Rubric across all public domain datasets,
evaluates provenance levels (MEASURED vs DERIVED vs ESTIMATED vs HYPOTHESIS),
and generates a machine-readable governance report.
"""

import sys
from pathlib import Path
from typing import List

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.modeling.data_quality import DataQualityAuditor, QualityScoreResult, QualityTier


DATASET_CATALOG = [
    {
        "name": "Lipstick 384 Formulations (Huynh 2020)",
        "formulation_completeness": 100.0,
        "measurement_quality": 92.0,
        "has_replicates": True,
        "replicate_count": 3,
        "method_completeness": 90.0,
        "feature_overlap": 88.0,
        "license_type": "CC_BY_NC",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "384 longitudinal cosmetic stick matrix with 17% wax, 12-week aging stability, and penetration hardness."
    },
    {
        "name": "Lipstick Multimodal Rheology (Soft Matter 2026)",
        "formulation_completeness": 90.0,
        "measurement_quality": 98.0,
        "has_replicates": True,
        "replicate_count": 3,
        "method_completeness": 95.0,
        "feature_overlap": 82.0,
        "license_type": "CC_BY_NC",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "SAOS/LAOS oscillatory sweeps, stress relaxation, creep, and LC-PolScope cooling rate crystallization."
    },
    {
        "name": "Organogel Lipstick Thermal Rheology (MDPI Gels 2021)",
        "formulation_completeness": 95.0,
        "measurement_quality": 90.0,
        "has_replicates": True,
        "replicate_count": 2,
        "method_completeness": 85.0,
        "feature_overlap": 80.0,
        "license_type": "CC_BY",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "Temperature ramp G'/G'', gel-sol transition temperature (63.8 C), and cooling hysteresis."
    },
    {
        "name": "Wax Oleogel Hardness Regression (Doan 2022)",
        "formulation_completeness": 100.0,
        "measurement_quality": 95.0,
        "has_replicates": True,
        "replicate_count": 3,
        "method_completeness": 90.0,
        "feature_overlap": 85.0,
        "license_type": "OPEN",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "Wax concentration vs. penetration firmness OLS regression (beta_wax = +75.02 gf/wt%, s_res = 6.63 gf)."
    },
    {
        "name": "Silicone & Powder Skin Tribology (Masen 2020)",
        "formulation_completeness": 100.0,
        "measurement_quality": 95.0,
        "has_replicates": True,
        "replicate_count": 5,
        "method_completeness": 92.0,
        "feature_overlap": 80.0,
        "license_type": "CC_BY",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "In-vivo human skin & bioskin friction measurements for pure Dimethicone 100 cSt and cosmetic talc."
    },
    {
        "name": "Anhydrous Powder Stick (US Patent 20070166254)",
        "formulation_completeness": 95.0,
        "measurement_quality": 82.0,
        "has_replicates": False,
        "replicate_count": 1,
        "method_completeness": 80.0,
        "feature_overlap": 92.0,
        "license_type": "PATENT",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED",
        "description": "11 anhydrous silicone-wax stick formulations with 20-25% powder loading, pay-off, and penetration depth."
    },
    {
        "name": "Fumed Silica Yield Stress (Kopylov 2011 & US20030198914)",
        "formulation_completeness": 85.0,
        "measurement_quality": 88.0,
        "has_replicates": True,
        "replicate_count": 2,
        "method_completeness": 82.0,
        "feature_overlap": 78.0,
        "license_type": "OPEN",
        "has_doi_or_patent": True,
        "provenance_status": "MEASURED_IN_EXTERNAL_SYSTEM",
        "description": "Concentration series of Aerosil R 972 in colloidal fluids (6% -> 122 Pa, 8% -> 190 Pa, 10% -> 365 Pa, 12% -> 545 Pa)."
    },
    {
        "name": "GS-40 Molten Slurry 2% R972 Yield Stress & Zero Settling",
        "formulation_completeness": 100.0,
        "measurement_quality": 60.0,
        "has_replicates": False,
        "replicate_count": 1,
        "method_completeness": 60.0,
        "feature_overlap": 100.0,
        "license_type": "INTERNAL",
        "has_doi_or_patent": False,
        "provenance_status": "PRE_PILOT_HYPOTHESIS",
        "description": "Theoretical Stokes-Bingham anti-settling extrapolation (~8.6 Pa at 80 C). Pending physical verification in P001-P018."
    },
]


def run_audit() -> List[QualityScoreResult]:
    results = []
    for item in DATASET_CATALOG:
        res = DataQualityAuditor.evaluate(
            dataset_name=item["name"],
            formulation_completeness=item["formulation_completeness"],
            measurement_quality=item["measurement_quality"],
            has_replicates=item["has_replicates"],
            replicate_count=item["replicate_count"],
            method_completeness=item["method_completeness"],
            feature_overlap=item["feature_overlap"],
            license_type=item["license_type"],
            has_doi_or_patent=item["has_doi_or_patent"],
            provenance_status=item["provenance_status"]
        )
        results.append((res, item["description"]))
    return results


def generate_markdown_report(results: List[Tuple[QualityScoreResult, str]], output_path: Path):
    lines = [
        "# GLIDE-SPEC 40: Public Domain & Prior Dataset Quality Audit",
        "",
        "이 문서는 GLIDE-SPEC 40의 7차원 데이터 품질 루브릭(`src/modeling/data_quality.py`)에 따라 모든 공개 벤치마크 및 도메인 Prior 데이터셋을 정량 감사한 결과입니다.",
        "",
        "---",
        "",
        "## 📊 7차원 품질 평가 기준 (Weight Total: 100%)",
        "- **Formulation Completeness (20%):** 100% 질량 완결성 및 원료 식별성",
        "- **Measurement Quality (20%):** 표준 시험법(ASTM/ISO) 및 계측기 정밀도",
        r"- **Replicate Availability (15%):** 반복 측정($n \ge 2$) 및 표준편차 존재 여부",
        "- **Method Completeness (15%):** 전단속도, 온도, 시간 등 공정 SOP 명시도",
        "- **Feature Overlap (15%):** GS-40 제형 공간과의 물리화학적 유사도",
        "- **License Integrity (10%):** CC BY, CC BY-NC, Patent 등 개방형 라이선스 준수",
        "- **Provenance Traceability (5%):** DOI, 특허번호 등 원문 추적성",
        "",
        "---",
        "",
        "## 🏛️ 데이터셋 품질 평가 결과 요약",
        "",
        "| 데이터셋 명칭 | 품질 점수 | 품질 티어 | 데이터 계보 (Provenance) | 대리 모델 Prior 허용 | 핵심 내용 |",
        "|---|:---:|:---:|:---:|:---:|---|"
    ]

    for res, desc in results:
        tier_str = res.tier.value.replace("TIER_1_", "Tier 1: ").replace("TIER_2_", "Tier 2: ").replace("TIER_3_", "Tier 3: ")
        admissible_str = "✅ **허용 (Prior)**" if res.is_admissible_for_surrogate_prior() else "⚠️ **격리 (가설/검증대기)**"
        lines.append(
            f"| **{res.dataset_name}** | **{res.composite_score_pct}%** | {tier_str} | `{res.provenance_tag}` | {admissible_str} | {desc} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 🛡️ 거버넌스 및 방화벽 규칙",
        "1. **`TIER_1_CORE_BENCHMARK` (Score >= 80%):** 대리 모델(Surrogate Engine)의 정량적 사전 분포(Prior) 학습에 직접 투입 가능.",
        "2. **`TIER_2_PHYSICAL_PRIOR` (Score 65~79%):** 정성적 스케일링 파라미터 또는 보조 사전 분포로만 활용.",
        "3. **`PRE_PILOT_HYPOTHESIS` 및 `UNQUALIFIED` (<65%):** 정량적 사전 확률에 절대 혼입할 수 없으며, **P001~P018 물리 파일럿에서 직접 검증해야 할 가설 대상**으로만 엄격 격리.",
        ""
    ])

    with open(output_path, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[+] Quality audit report generated at: {output_path}")


def main():
    print("================================================================================")
    print("  GLIDE-SPEC 40: Public Domain Prior Quality Audit & Governance Runner")
    print("================================================================================\n")
    results = run_audit()

    print(f"{'Dataset Name':<45} {'Score':<8} {'Tier':<25} {'Provenance':<22} {'Admissible'}")
    print("-" * 115)
    for res, _ in results:
        admissible = "YES" if res.is_admissible_for_surrogate_prior() else "NO (Isolated)"
        print(f"{res.dataset_name:<45} {res.composite_score_pct:<8}% {res.tier.value:<25} {res.provenance_tag:<22} {admissible}")
    print("-" * 115)

    root_dir = Path(__file__).resolve().parent.parent
    report_path = root_dir / "benchmarks" / "domain_priors" / "DATASET_QUALITY_AUDIT.md"
    generate_markdown_report(results, report_path)


if __name__ == "__main__":
    from typing import Tuple
    main()

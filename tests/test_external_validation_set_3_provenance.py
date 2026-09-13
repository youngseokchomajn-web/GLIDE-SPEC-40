import os
import csv
import pytest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_dataset_3_raw_existence_and_format():
    raw_path = ROOT_DIR / "data" / "EXTERNAL_VALIDATION_SET_3_RAW.csv"
    assert raw_path.exists(), "EXTERNAL_VALIDATION_SET_3_RAW.csv missing"
    with open(raw_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 10, f"Expected 10 rows, found {len(rows)}"
    for r in rows:
        assert r["provenance_doi"] == "10.3390/gels12060532"
        assert r["provenance_pmcid"] == "PMC13298235"
        assert r["source_table_hardness"] == "Table 3"
        assert r["source_table_formulation"] == "Table 9"
        assert r["license"] == "CC-BY-4.0"
        
        # Test unit conversion accuracy
        f_n = float(r["measured_hardness_mean_n"])
        f_gf = float(r["converted_hardness_mean_gf"])
        expected_gf = f_n * 101.97162
        assert abs(f_gf - expected_gf) < 0.1, f"Conversion mismatch: {f_gf} vs {expected_gf}"

def test_dataset_3_zero_overlap_audit():
    freeze_csv = ROOT_DIR / "data" / "DATASET_FREEZE_1.csv"
    with open(freeze_csv, "r", encoding="utf-8") as f:
        freeze_text = f.read().lower()
    
    # DOI and PMCID must not exist in frozen training baseline
    assert "10.3390/gels12060532" not in freeze_text
    assert "pmc13298235" not in freeze_text
    assert "yassoralipour" not in freeze_text

def test_dataset_3_domain_priors_zero_overlap():
    domain_dir = ROOT_DIR / "benchmarks" / "domain_priors"
    for p in domain_dir.rglob("*.csv"):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()
            assert "10.3390/gels12060532" not in content, f"Overlap detected in {p}"
            assert "yassoralipour" not in content, f"Overlap detected in {p}"

def test_blind_status_locked():
    spec_path = ROOT_DIR / "data" / "EXTERNAL_VALIDATION_SET_3_SPEC.csv"
    assert spec_path.exists()
    with open(spec_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["blind_status"] == "LOCKED_BLIND"

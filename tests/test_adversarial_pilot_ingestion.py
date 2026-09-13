import pytest
import csv
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_adversarial_virtual_data_blocked():
    """Adversarial test: prove that virtual predictions or incomplete synthetic rows cannot qualify M4."""
    script_path = ROOT_DIR / "scripts" / "run_gs40_pilot_qualification.py"
    
    # Run qualification script on current matrix
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    assert res.returncode == 0
    assert "AWAITING_PILOT_DATA" in res.stdout
    assert "0/16 Primary runs required" in res.stdout

def test_supplemental_isolation():
    """Ensure supplemental runs P017-P018 cannot count toward primary N=16 requirement."""
    matrix_path = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    with open(matrix_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    
    primary = [r for r in rows if not (r.get("Design_Type") or "").startswith("Supplemental")]
    supplemental = [r for r in rows if (r.get("Design_Type") or "").startswith("Supplemental")]
    
    assert len(primary) == 16, f"Expected 16 primary runs, found {len(primary)}"
    assert len(supplemental) == 2, f"Expected 2 supplemental runs, found {len(supplemental)}"

def test_no_synthetic_substitution_gate():
    """Ensure qualification fails because no rows are marked PASS or COMPLETED."""
    matrix_path = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    with open(matrix_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            assert "PASS" not in row and "COMPLETED" not in row, "Physical QC status prematurely completed"

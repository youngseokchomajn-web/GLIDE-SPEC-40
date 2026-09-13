import pytest
import csv
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def test_adversarial_virtual_data_blocked():
    """Adversarial test: prove that virtual predictions cannot qualify M4 on current matrix."""
    script_path = ROOT_DIR / "scripts" / "run_gs40_pilot_qualification.py"
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    assert res.returncode == 0
    assert "AWAITING_PILOT_DATA" in res.stdout
    assert "0/16 Primary runs required" in res.stdout

def test_supplemental_isolation():
    """Ensure supplemental runs P017-P018 cannot count toward primary N=16 requirement."""
    matrix_path = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    with open(matrix_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    primary = [r for r in rows if not (r.get("Design_Type") or "").startswith("Supplemental")]
    supplemental = [r for r in rows if (r.get("Design_Type") or "").startswith("Supplemental")]
    
    assert len(primary) == 16, f"Expected 16 primary runs, found {len(primary)}"
    assert len(supplemental) == 2, f"Expected 2 supplemental runs, found {len(supplemental)}"

def test_injected_synthetic_forgery_blocked():
    """Adversarial injection: inject 16 rows with forged QC_Status=PASS but missing real process operator/date."""
    script_path = ROOT_DIR / "scripts" / "run_gs40_pilot_qualification.py"
    matrix_path = ROOT_DIR / "data" / "doe" / "pilot_doe_run_matrix_rev1.0.csv"
    
    with open(matrix_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Construct forged matrix in a temporary file
    with tempfile.NamedTemporaryFile("w", newline="", suffix=".csv", delete=False) as tmp:
        tmp_path = Path(tmp.name)
        writer = csv.DictWriter(tmp, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            forged_r = dict(r)
            # Try to forge completion without real operator/date
            forged_r["Measured_Hardness_gf"] = "145.0"
            forged_r["Measured_Transfer_g"] = "0.045"
            forged_r["Measured_Drop_Point_C"] = "68.0"
            forged_r["QC_Status"] = "PASS"
            forged_r["Operator"] = ""  # Missing operator
            forged_r["Mfg_Date"] = ""  # Missing date
            writer.writerow(forged_r)

    try:
        # Run qualification script pointing to forged matrix
        res = subprocess.run([sys.executable, str(script_path), "--matrix", str(tmp_path)], capture_output=True, text=True)
        assert "AWAITING_PILOT_DATA" in res.stdout
        assert "Incomplete Process Records:         18" in res.stdout or "Incomplete Process Records:" in res.stdout
        assert "Missing actual_fill_temp, operator, or mfg_date" in res.stdout
    finally:
        tmp_path.unlink(missing_ok=True)

def test_group_cv_is_strictly_group_kfold():
    """Ensure run_group_cv_diagnostics.py uses GroupKFold and does NOT import KFold without group aware."""
    script_path = ROOT_DIR / "scripts" / "run_group_cv_diagnostics.py"
    with open(script_path, "r", encoding="utf-8") as f:
        code = f.read()
    assert "GroupKFold" in code, "GroupKFold missing from diagnostics script"
    assert "from sklearn.model_selection import KFold" not in code, "Ordinary KFold must not be used"

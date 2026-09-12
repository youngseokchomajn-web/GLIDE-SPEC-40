"""
GLIDE-SPEC 40 - 812 Shampoo Dataset Normalized Parser (Track B Engine Benchmark)
Implements data ingestion according to AUDIT-DS-812-SHAMPOO-2024-v0.1.
Zero dependencies on src/ core production logic.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple


INGREDIENTS_18 = [
    "Texapon SB 3 KC",
    "Plantapon ACG 50",
    "Plantapon LC 7",
    "Plantacare 818",
    "Plantacare 2000",
    "Dehyton MC",
    "Dehyton PK 45",
    "Dehyton ML",
    "Dehyton AB 30",
    "Plantapon Amino SCG-L",
    "Plantapon Amino KG-L",
    "Dehyquart A-CA",
    "Luviquat Excellence",
    "Dehyquart CC6",
    "Dehyquart CC7 Benz",
    "Salcare Super 7",
    "Arlypon F",
    "Arlypon TT"
]


def clean_float(val: Any) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if s.upper() in ("NA", "NONE", "NULL", ""):
        return None
    try:
        return float(s)
    except ValueError:
        return None


class ShampooDatasetParser:
    def __init__(self, raw_json_path: Path, raw_csv_path: Optional[Path] = None):
        self.raw_json_path = Path(raw_json_path)
        self.raw_csv_path = Path(raw_csv_path) if raw_csv_path else None
        self.samples: List[Dict[str, Any]] = []

    def load(self) -> List[Dict[str, Any]]:
        if not self.raw_json_path.exists():
            raise FileNotFoundError(f"Raw json not found at {self.raw_json_path}")
        with open(self.raw_json_path, mode="r", encoding="utf-8") as f:
            self.samples = json.load(f)
        return self.samples

    def parse_all(self) -> Dict[str, List[Dict[str, Any]]]:
        if not self.samples:
            self.load()

        visc_rows = []
        turb_rows = []
        stability_rows = []

        for sample in self.samples:
            sample_id = sample.get("ID")
            is_stable = bool(sample.get("Stability_Test", False))

            # Build ingredient compositions (percentage sum to ~ active + water)
            comp = {}
            total_active = 0.0
            for ing in INGREDIENTS_18:
                pct = clean_float(sample.get(ing, 0.0)) or 0.0
                comp[ing] = pct
                total_active += pct
            water_pct = round(max(0.0, 100.0 - total_active), 4)
            comp["Water"] = water_pct

            # 1. Phase Stability Dataset (All 812)
            stab_record = {
                "sample_id": sample_id,
                **comp,
                "stability_pass": 1 if is_stable else 0,
                "viscosity_class": sample.get("Viscosity", "UNKNOWN"),
                "rheology_type": sample.get("Rheology_Type", "UNKNOWN")
            }
            stability_rows.append(stab_record)

            # 2. Continuous Responses (Only for stable samples n=294)
            if is_stable:
                # Turbidity
                turb_val = clean_float(sample.get("Turbidity_NTU"))
                if turb_val is not None:
                    turb_rows.append({
                        "sample_id": sample_id,
                        **comp,
                        "turbidity_ntu": turb_val,
                        "turbidity_error": clean_float(sample.get("Turbidity_Error"))
                    })

                # Viscosity at shear rate index 20 (~97 to 100 s^-1)
                rd = sample.get("Rheology_Data")
                if rd and isinstance(rd, list) and len(rd) >= 2:
                    shear_rates = rd[0].get("shear_rate", [])
                    viscosities = rd[1].get("avg_viscosity", [])
                    std_devs = rd[2].get("std_dev", []) if len(rd) > 2 else []

                    # Index 20 corresponds to ~100 s^-1
                    idx = 20 if len(viscosities) > 20 else -1
                    if idx >= 0:
                        shear_at_idx = clean_float(shear_rates[idx])
                        visc_at_idx = clean_float(viscosities[idx])
                        std_at_idx = clean_float(std_devs[idx]) if idx < len(std_devs) else None

                        if visc_at_idx is not None and visc_at_idx > 0:
                            visc_rows.append({
                                "sample_id": sample_id,
                                **comp,
                                "shear_rate_s1": shear_at_idx,
                                "viscosity_100s_mPas": visc_at_idx,
                                "viscosity_std_mPas": std_at_idx
                            })

        return {
            "phase_stability": stability_rows,
            "turbidity": turb_rows,
            "viscosity_100s": visc_rows
        }

    def export_normalized(self, output_dir: Path):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        datasets = self.parse_all()

        for name, rows in datasets.items():
            if not rows:
                continue
            out_file = output_dir / f"shampoo_m4_{name}.csv"
            fieldnames = list(rows[0].keys())
            with open(out_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print(f"[+] Exported {len(rows)} records to {out_file}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    raw_json = base_dir / "raw" / "LiquidFormulationsDataset_2023.json"
    raw_csv = base_dir / "raw" / "BASF_Surfactants_Information.csv"
    out_dir = base_dir / "normalized"

    parser = ShampooDatasetParser(raw_json, raw_csv)
    parser.export_normalized(out_dir)

"""
GLIDE-SPEC 40 - 812 Shampoo Dataset Normalized Parser (Track B Engine Benchmark)
Implements data ingestion according to AUDIT-DS-812-SHAMPOO-2024-v0.1.
Adheres strictly to benchmarks/shampoo/schema/normalized_benchmark_schema.json.
"""

import hashlib
import json
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional

DATASET_ID = "NATURE_812_SHAMPOO_2024"
DATA_ORIGIN = "PUBLIC_BENCHMARK"
SCHEMA_VERSION = 1.0
EXPECTED_SHA256 = "3a195870782e6fd87bdd7499cbb4fe201d025b2cda05f9eee9fb9477f34b58bd"

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
    if s == "" or s.upper() in ("NA", "NONE", "NULL"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


class ShampooDatasetParser:
    def __init__(self, raw_json_path: Path, raw_surfactant_csv: Optional[Path] = None):
        self.raw_json_path = Path(raw_json_path)
        self.raw_surfactant_csv = Path(raw_surfactant_csv) if raw_surfactant_csv else None
        self.file_hash = self._compute_hash(self.raw_json_path)

    @staticmethod
    def _compute_hash(path: Path) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def parse_all(self) -> Dict[str, List[Dict[str, Any]]]:
        with open(self.raw_json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        visc_rows = []
        turb_rows = []
        stability_rows = []

        for sample in raw_data:
            rec_id = int(sample["ID"])
            is_stable = bool(sample.get("Stability_Test", False))

            comp = {ing: clean_float(sample.get(ing, 0.0)) or 0.0 for ing in INGREDIENTS_18}
            active_sum = sum(comp.values())
            water = round(100.0 - active_sum, 4)

            # Subsystem groupings
            surf_vals = [comp[ing] for ing in INGREDIENTS_18[:12]]
            poly_vals = [comp[ing] for ing in INGREDIENTS_18[12:16]]
            thick_vals = [comp[ing] for ing in INGREDIENTS_18[16:18]]

            surf_total = sum(surf_vals)
            surf_max = max(surf_vals) if surf_total > 0 else 0.0
            surf_ratio = (surf_max / surf_total) if surf_total > 0 else 0.0
            poly_total = sum(poly_vals)
            thick_total = sum(thick_vals)

            base_row = {
                "source_file_hash": self.file_hash,
                "dataset_id": DATASET_ID,
                "source_record_id": rec_id,
                "data_origin": DATA_ORIGIN,
                "schema_version": SCHEMA_VERSION,
                **comp,
                "water_wt_pct": water,
                "surfactant_total_wt_pct": round(surf_total, 4),
                "surfactant_primary_ratio": round(surf_ratio, 4),
                "polymer_total_wt_pct": round(poly_total, 4),
                "thickener_total_wt_pct": round(thick_total, 4),
            }

            # 1. Phase Stability (All 812)
            stab_row = dict(base_row)
            stab_row["target_name"] = "phase_stability"
            stab_row["target_value"] = 1 if is_stable else 0
            stab_row["target_error"] = None
            stab_row["target_unit"] = "binary"
            stability_rows.append(stab_row)

            # 2. Continuous Responses (Only for stable samples n=294)
            if is_stable:
                # Turbidity
                turb_val = clean_float(sample.get("Turbidity_NTU"))
                if turb_val is not None:
                    t_row = dict(base_row)
                    t_row["target_name"] = "turbidity_ntu"
                    t_row["target_value"] = round(turb_val, 2)
                    t_row["target_error"] = clean_float(sample.get("Turbidity_Error"))
                    t_row["target_unit"] = "NTU"
                    turb_rows.append(t_row)

                # Viscosity at shear rate index 20 (~97 to 100 s^-1)
                rd = sample.get("Rheology_Data")
                if rd and isinstance(rd, list) and len(rd) >= 2:
                    shear_rates = rd[0].get("shear_rate", [])
                    viscosities = rd[1].get("avg_viscosity", [])
                    std_devs = rd[2].get("std_dev", []) if len(rd) > 2 else []

                    idx = 20 if len(viscosities) > 20 else -1
                    if idx >= 0:
                        shear_at_idx = clean_float(shear_rates[idx])
                        visc_at_idx = clean_float(viscosities[idx])
                        std_at_idx = clean_float(std_devs[idx]) if idx < len(std_devs) else None

                        if visc_at_idx is not None and visc_at_idx > 0:
                            v_row = dict(base_row)
                            v_row["target_name"] = "viscosity_at_100s"
                            v_row["target_value"] = round(visc_at_idx, 4)
                            v_row["target_error"] = round(std_at_idx, 4) if std_at_idx is not None else None
                            v_row["target_unit"] = "mPa.s"
                            v_row["measured_shear_rate_s_minus_1"] = round(shear_at_idx, 3)
                            v_row["rheology_type"] = sample.get("Rheology_Type")
                            v_row["viscosity_category"] = sample.get("Viscosity")
                            visc_rows.append(v_row)

        return {
            "phase_stability": stability_rows,
            "turbidity": turb_rows,
            "visc_at_100s": visc_rows
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

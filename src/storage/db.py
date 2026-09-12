"""
GLIDE-SPEC 40 - Data Storage & Repository Layer
Manages persistence of raw materials, formula revisions, DOE trials, and QC records
using structured JSON and lightweight SQLite database.
"""

import json
import os
import sqlite3
from typing import Dict, List, Optional
from pathlib import Path

from src.materials.master import RawMaterial, REV73_RAW_MATERIALS
from src.formulas.master import FormulaMaster, REV73_TARGET_ACTIVE_FORMULA
from src.qc.models import BatchQCRecord, HardnessSOP, TransferSOP
from src.doe.engine import DOETrial


class FormulationDatabase:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.materials_file = self.data_dir / "raw_materials" / "catalog.json"
        self.qc_db_path = self.data_dir / "qc" / "qc_history.db"

        self._init_directories()
        self._init_sqlite()

    def _init_directories(self):
        (self.data_dir / "raw_materials").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "formulas").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "qc").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "doe").mkdir(parents=True, exist_ok=True)

    def _init_sqlite(self):
        with sqlite3.connect(self.qc_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS qc_records (
                batch_id TEXT PRIMARY KEY,
                formula_id TEXT,
                revision TEXT,
                test_date TEXT,
                operator TEXT,
                hardness_gf REAL,
                transfer_g_10c REAL,
                density_g_cm3 REAL,
                drop_point_c REAL,
                hardness_probe TEXT,
                transfer_substrate TEXT,
                powder_bloom INTEGER,
                white_cast_score INTEGER,
                sweating_syneresis INTEGER,
                notes TEXT,
                hardness_sop_json TEXT,
                transfer_sop_json TEXT,
                sop_complete INTEGER NOT NULL DEFAULT 0
            )
            """)
            columns = {row[1] for row in cursor.execute("PRAGMA table_info(qc_records)")}
            for name, definition in {
                "hardness_sop_json": "TEXT", "transfer_sop_json": "TEXT",
                "sop_complete": "INTEGER NOT NULL DEFAULT 0",
            }.items():
                if name not in columns:
                    cursor.execute(f"ALTER TABLE qc_records ADD COLUMN {name} {definition}")
            conn.commit()

    def load_materials_catalog(self) -> Dict[str, RawMaterial]:
        if not self.materials_file.exists():
            # Seed with baseline REV73_RAW_MATERIALS
            self.save_materials_catalog(REV73_RAW_MATERIALS)
            return dict(REV73_RAW_MATERIALS)

        with open(self.materials_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return {k: RawMaterial.model_validate(v) for k, v in raw_data.items()}

    def save_materials_catalog(self, materials: Dict[str, RawMaterial]):
        dump_data = {k: v.model_dump() for k, v in materials.items()}
        with open(self.materials_file, "w", encoding="utf-8") as f:
            json.dump(dump_data, f, ensure_ascii=False, indent=2)

    def save_qc_record(self, record: BatchQCRecord):
        with sqlite3.connect(self.qc_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO qc_records (
                batch_id, formula_id, revision, test_date, operator, hardness_gf,
                transfer_g_10c, density_g_cm3, drop_point_c, hardness_probe,
                transfer_substrate, powder_bloom, white_cast_score, sweating_syneresis,
                notes, hardness_sop_json, transfer_sop_json, sop_complete
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.batch_id,
                record.formula_id,
                record.revision,
                record.test_date,
                record.operator,
                record.hardness_gf,
                record.transfer_g_10c,
                record.density_g_cm3,
                record.drop_point_c,
                record.hardness_sop.probe_type,
                record.transfer_sop.substrate_type,
                1 if record.powder_bloom_observed else 0,
                record.white_cast_score,
                1 if record.sweating_syneresis_observed else 0,
                record.notes,
                json.dumps(record.hardness_sop.model_dump()),
                json.dumps(record.transfer_sop.model_dump()),
                1 if record.is_sop_complete() else 0,
            ))
            conn.commit()

    def get_all_qc_records(self) -> List[BatchQCRecord]:
        records: List[BatchQCRecord] = []
        with sqlite3.connect(self.qc_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM qc_records ORDER BY test_date DESC")
            rows = cursor.fetchall()
            for r in rows:
                record = BatchQCRecord(
                    batch_id=r[0],
                    formula_id=r[1],
                    revision=r[2],
                    test_date=r[3],
                    operator=r[4],
                    hardness_gf=r[5],
                    transfer_g_10c=r[6],
                    density_g_cm3=r[7],
                    drop_point_c=r[8],
                    hardness_sop=HardnessSOP(**json.loads(r[15])) if r[15] else HardnessSOP(probe_type=r[9]),
                    transfer_sop=TransferSOP(**json.loads(r[16])) if r[16] else TransferSOP(substrate_type=r[10]),
                    powder_bloom_observed=bool(r[11]),
                    white_cast_score=r[12],
                    sweating_syneresis_observed=bool(r[13]),
                    notes=r[14]
                )
                records.append(record)
        return records

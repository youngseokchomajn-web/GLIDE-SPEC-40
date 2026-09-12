"""
GLIDE-SPEC 40 - Data Storage & Repository Layer (Schema v3)
Manages persistence of raw materials, formula revisions, DOE trials,
manufacturing batches, and QC records with strict Foreign Key enforcement,
idempotent migrations, and full DOE -> Batch -> QC lineage.
"""

import json
import os
import sqlite3
from typing import Dict, List, Optional
from pathlib import Path

from src.materials.master import RawMaterial, REV73_RAW_MATERIALS
from src.formulas.master import FormulaMaster, REV73_TARGET_ACTIVE_FORMULA
from src.qc.models import BatchQCRecord, HardnessSOP, TransferSOP, DataOrigin, ProcessCondition
from src.doe.engine import DOETrial
from src.manufacturing.models import ManufacturingBatch
from src.manufacturing.calculator import BatchChargeItem

CURRENT_SCHEMA_VERSION = 3


class FormulationDatabase:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.materials_file = self.data_dir / "raw_materials" / "catalog.json"
        self.qc_db_path = self.data_dir / "qc" / "qc_history.db"

        self._init_directories()
        self._init_sqlite()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.qc_db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_directories(self):
        (self.data_dir / "raw_materials").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "formulas").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "qc").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "doe").mkdir(parents=True, exist_ok=True)

    def _init_sqlite(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. Schema versioning tracking table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_versions (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL,
                description TEXT NOT NULL
            )
            """)

            # 2. DOE Trials table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doe_trials (
                trial_id TEXT PRIMARY KEY,
                design_type TEXT,
                synthetic_wax_pct REAL,
                candelilla_wax_pct REAL,
                dimethicone_pct REAL,
                caprylyl_methicone_pct REAL,
                c12_15_alkyl_benzoate_pct REAL,
                fill_temperature_c REAL,
                shear_speed_rpm REAL,
                mixing_time_min REAL,
                cooling_profile TEXT,
                status TEXT,
                notes TEXT
            )
            """)

            # 3. Manufacturing Batches table (Phase 2A Data Contract v0.2)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS manufacturing_batches (
                batch_id TEXT PRIMARY KEY,
                trial_id TEXT,
                formula_id TEXT NOT NULL,
                revision TEXT NOT NULL,
                created_date TEXT NOT NULL,
                operator TEXT NOT NULL,
                batch_size_kg REAL NOT NULL,
                total_charge_pct REAL NOT NULL,
                items_json TEXT NOT NULL,
                process_conditions_json TEXT NOT NULL,
                total_raw_material_cost REAL,
                cost_per_20g_stick REAL,
                target_cogs_per_stick REAL NOT NULL DEFAULT 2950.0,
                notes TEXT,
                FOREIGN KEY (trial_id) REFERENCES doe_trials(trial_id) ON DELETE SET NULL
            )
            """)

            # 4. Base QC Records table with Foreign Key to doe_trials
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
                sop_complete INTEGER NOT NULL DEFAULT 0,
                trial_id TEXT,
                data_origin TEXT NOT NULL DEFAULT 'REAL_PILOT',
                process_conditions_json TEXT,
                FOREIGN KEY (trial_id) REFERENCES doe_trials(trial_id) ON DELETE RESTRICT
            )
            """)

            # 5. Idempotent column migrations for qc_records
            columns = {row[1] for row in cursor.execute("PRAGMA table_info(qc_records)")}
            migrations = {
                "hardness_sop_json": "TEXT",
                "transfer_sop_json": "TEXT",
                "sop_complete": "INTEGER NOT NULL DEFAULT 0",
                "trial_id": "TEXT",
                "data_origin": "TEXT NOT NULL DEFAULT 'REAL_PILOT'",
                "process_conditions_json": "TEXT",
            }
            for name, definition in migrations.items():
                if name not in columns:
                    cursor.execute(f"ALTER TABLE qc_records ADD COLUMN {name} {definition}")

            # Record schema version v3
            cursor.execute("SELECT version FROM schema_versions WHERE version = ?", (CURRENT_SCHEMA_VERSION,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO schema_versions (version, applied_at, description) VALUES (?, datetime('now'), ?)",
                    (CURRENT_SCHEMA_VERSION, "Phase 2A Data Contract v0.2: ManufacturingBatch, Foreign Key enforcement, and Lineage")
                )

            conn.commit()

    def get_current_schema_version(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(version) FROM schema_versions")
            row = cursor.fetchone()
            return row[0] if row and row[0] is not None else 0

    def load_materials_catalog(self) -> Dict[str, RawMaterial]:
        if not self.materials_file.exists():
            self.save_materials_catalog(REV73_RAW_MATERIALS)
            return dict(REV73_RAW_MATERIALS)

        with open(self.materials_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return {k: RawMaterial.model_validate(v) for k, v in raw_data.items()}

    def save_materials_catalog(self, materials: Dict[str, RawMaterial]):
        dump_data = {k: v.model_dump() for k, v in materials.items()}
        with open(self.materials_file, "w", encoding="utf-8") as f:
            json.dump(dump_data, f, ensure_ascii=False, indent=2)

    # --------------------------------------------------------------------------
    # DOE Trials
    # --------------------------------------------------------------------------
    def save_doe_trial(self, trial: DOETrial):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO doe_trials (
                trial_id, design_type, synthetic_wax_pct, candelilla_wax_pct,
                dimethicone_pct, caprylyl_methicone_pct, c12_15_alkyl_benzoate_pct,
                fill_temperature_c, shear_speed_rpm, mixing_time_min,
                cooling_profile, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trial.trial_id, trial.design_type, trial.synthetic_wax_pct, trial.candelilla_wax_pct,
                trial.dimethicone_pct, trial.caprylyl_methicone_pct, trial.c12_15_alkyl_benzoate_pct,
                trial.fill_temperature_c, trial.shear_speed_rpm, trial.mixing_time_min,
                trial.cooling_profile, trial.status, trial.notes
            ))
            conn.commit()

    def get_doe_trial(self, trial_id: str) -> Optional[DOETrial]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doe_trials WHERE trial_id = ?", (trial_id,))
            r = cursor.fetchone()
            if not r:
                return None
            return DOETrial(
                trial_id=r[0], design_type=r[1], synthetic_wax_pct=r[2], candelilla_wax_pct=r[3],
                dimethicone_pct=r[4], caprylyl_methicone_pct=r[5], c12_15_alkyl_benzoate_pct=r[6],
                fill_temperature_c=r[7], shear_speed_rpm=r[8], mixing_time_min=r[9],
                cooling_profile=r[10], status=r[11], notes=r[12]
            )

    def get_all_doe_trials(self) -> List[DOETrial]:
        trials: List[DOETrial] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doe_trials ORDER BY trial_id ASC")
            for r in cursor.fetchall():
                trials.append(DOETrial(
                    trial_id=r[0], design_type=r[1], synthetic_wax_pct=r[2], candelilla_wax_pct=r[3],
                    dimethicone_pct=r[4], caprylyl_methicone_pct=r[5], c12_15_alkyl_benzoate_pct=r[6],
                    fill_temperature_c=r[7], shear_speed_rpm=r[8], mixing_time_min=r[9],
                    cooling_profile=r[10], status=r[11], notes=r[12]
                ))
        return trials

    # --------------------------------------------------------------------------
    # Manufacturing Batches
    # --------------------------------------------------------------------------
    def save_manufacturing_batch(self, batch: ManufacturingBatch):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # If trial_id is specified, verify its existence to enforce referential integrity
            if batch.trial_id:
                cursor.execute("SELECT 1 FROM doe_trials WHERE trial_id = ?", (batch.trial_id,))
                if not cursor.fetchone():
                    raise sqlite3.IntegrityError(f"Foreign Key violation: trial_id '{batch.trial_id}' does not exist in doe_trials.")

            items_json = json.dumps([item.model_dump() for item in batch.items])
            proc_json = json.dumps(batch.process_conditions.model_dump())

            cursor.execute("""
            INSERT OR REPLACE INTO manufacturing_batches (
                batch_id, trial_id, formula_id, revision, created_date, operator,
                batch_size_kg, total_charge_pct, items_json, process_conditions_json,
                total_raw_material_cost, cost_per_20g_stick, target_cogs_per_stick, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                batch.batch_id, batch.trial_id, batch.formula_id, batch.revision,
                batch.created_date, batch.operator, batch.batch_size_kg, batch.total_charge_pct,
                items_json, proc_json, batch.total_raw_material_cost,
                batch.cost_per_20g_stick, batch.target_cogs_per_stick, batch.notes
            ))
            conn.commit()

    def get_manufacturing_batch(self, batch_id: str) -> Optional[ManufacturingBatch]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM manufacturing_batches WHERE batch_id = ?", (batch_id,))
            r = cursor.fetchone()
            if not r:
                return None
            items = [BatchChargeItem(**i) for i in json.loads(r[8])]
            proc_cond = ProcessCondition(**json.loads(r[9]))
            return ManufacturingBatch(
                batch_id=r[0], trial_id=r[1], formula_id=r[2], revision=r[3],
                created_date=r[4], operator=r[5], batch_size_kg=r[6], total_charge_pct=r[7],
                items=items, process_conditions=proc_cond,
                total_raw_material_cost=r[10], cost_per_20g_stick=r[11],
                target_cogs_per_stick=r[12], notes=r[13]
            )

    # --------------------------------------------------------------------------
    # QC Records
    # --------------------------------------------------------------------------
    def save_qc_record(self, record: BatchQCRecord):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Strict Referential Integrity Gate:
            # If trial_id is provided, it MUST exist in doe_trials.
            if record.trial_id:
                cursor.execute("SELECT 1 FROM doe_trials WHERE trial_id = ?", (record.trial_id,))
                if not cursor.fetchone():
                    raise sqlite3.IntegrityError(
                        f"Foreign Key violation: trial_id '{record.trial_id}' does not exist in doe_trials table."
                    )

            cursor.execute("""
            INSERT OR REPLACE INTO qc_records (
                batch_id, formula_id, revision, test_date, operator, hardness_gf,
                transfer_g_10c, density_g_cm3, drop_point_c, hardness_probe,
                transfer_substrate, powder_bloom, white_cast_score, sweating_syneresis,
                notes, hardness_sop_json, transfer_sop_json, sop_complete,
                trial_id, data_origin, process_conditions_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                record.trial_id,
                record.data_origin.value,
                json.dumps(record.process_conditions.model_dump()),
            ))
            conn.commit()

    def get_all_qc_records(self) -> List[BatchQCRecord]:
        records: List[BatchQCRecord] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                batch_id, formula_id, revision, test_date, operator,
                hardness_gf, transfer_g_10c, density_g_cm3, drop_point_c,
                hardness_probe, transfer_substrate, powder_bloom,
                white_cast_score, sweating_syneresis, notes,
                hardness_sop_json, transfer_sop_json, sop_complete,
                trial_id, data_origin, process_conditions_json
            FROM qc_records
            ORDER BY test_date DESC
            """)
            rows = cursor.fetchall()
            for r in rows:
                hardness_sop = (
                    HardnessSOP(**json.loads(r[15]))
                    if r[15]
                    else HardnessSOP(probe_type=r[9])
                )
                transfer_sop = (
                    TransferSOP(**json.loads(r[16]))
                    if r[16]
                    else TransferSOP(substrate_type=r[10])
                )
                trial_id = r[18]
                data_origin = DataOrigin(r[19]) if r[19] else DataOrigin.REAL_PILOT
                proc_cond = (
                    ProcessCondition(**json.loads(r[20]))
                    if r[20]
                    else ProcessCondition()
                )

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
                    hardness_sop=hardness_sop,
                    transfer_sop=transfer_sop,
                    powder_bloom_observed=bool(r[11]),
                    white_cast_score=r[12],
                    sweating_syneresis_observed=bool(r[13]),
                    notes=r[14],
                    trial_id=trial_id,
                    data_origin=data_origin,
                    process_conditions=proc_cond,
                )
                records.append(record)
        return records

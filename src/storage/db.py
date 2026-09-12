"""
GLIDE-SPEC 40 - Data Storage & Repository Layer (Schema v3 with Table Rebuild Migration)
Manages persistence of raw materials, formula revisions, DOE trials,
manufacturing batches, and QC records with strict Foreign Key enforcement,
transactional table rebuild migrations, and full DOE -> Batch -> QC lineage.
"""

import json
import os
import sqlite3
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

from src.materials.master import RawMaterial, REV73_RAW_MATERIALS
from src.formulas.master import FormulaMaster, REV73_TARGET_ACTIVE_FORMULA
from src.qc.models import BatchQCRecord, HardnessSOP, TransferSOP, DataOrigin, ProcessCondition
from src.doe.engine import DOETrial
from src.manufacturing.models import ManufacturingBatch
from src.manufacturing.calculator import BatchChargeItem

CURRENT_SCHEMA_VERSION = 4


class FormulationDatabase:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.materials_file = self.data_dir / "raw_materials" / "catalog.json"
        self.qc_db_path = self.data_dir / "qc" / "qc_history.db"

        self._init_directories()
        self._init_sqlite()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.qc_db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()

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

            # 3. Manufacturing Batches table (Phase 2A Lineage)
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
                cogs_basis TEXT NOT NULL DEFAULT 'ESTIMATED_SIMULATION',
                material_price_source TEXT NOT NULL DEFAULT 'Baseline Simulation Fixture',
                quote_status TEXT NOT NULL DEFAULT 'PENDING_FORMAL_QUOTES',
                calculated_at TEXT,
                notes TEXT,
                FOREIGN KEY (trial_id) REFERENCES doe_trials(trial_id) ON DELETE SET NULL
            )
            """)

            # Idempotent column migrations for manufacturing_batches
            mfg_cols = {row[1] for row in cursor.execute("PRAGMA table_info(manufacturing_batches)").fetchall()}
            mfg_migrations = {
                "cogs_basis": "TEXT NOT NULL DEFAULT 'ESTIMATED_SIMULATION'",
                "material_price_source": "TEXT NOT NULL DEFAULT 'Baseline Simulation Fixture'",
                "quote_status": "TEXT NOT NULL DEFAULT 'PENDING_FORMAL_QUOTES'",
                "calculated_at": "TEXT",
            }
            for name, definition in mfg_migrations.items():
                if name not in mfg_cols:
                    cursor.execute(f"ALTER TABLE manufacturing_batches ADD COLUMN {name} {definition}")

            # 4. Check if qc_records exists and has required FK constraints
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='qc_records'")
            qc_table_exists = cursor.fetchone() is not None

            needs_rebuild = False
            if qc_table_exists:
                # Inspect foreign keys on qc_records
                fks = cursor.execute("PRAGMA foreign_key_list(qc_records)").fetchall()
                # Each fk row: (id, seq, table, from, to, on_update, on_delete, match)
                fk_tables = {row[2] for row in fks}
                if "doe_trials" not in fk_tables or "manufacturing_batches" not in fk_tables:
                    needs_rebuild = True

            if not qc_table_exists:
                # Brand new table with full FK constraints
                cursor.execute("""
                CREATE TABLE qc_records (
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
                    FOREIGN KEY (batch_id) REFERENCES manufacturing_batches(batch_id) ON DELETE RESTRICT,
                    FOREIGN KEY (trial_id) REFERENCES doe_trials(trial_id) ON DELETE RESTRICT
                )
                """)
            elif needs_rebuild:
                # Transactional table rebuild to enforce Foreign Keys on existing tables
                cursor.execute("PRAGMA foreign_keys = OFF;")
                cursor.execute("""
                CREATE TABLE qc_records_v3_new (
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
                    FOREIGN KEY (batch_id) REFERENCES manufacturing_batches(batch_id) ON DELETE RESTRICT,
                    FOREIGN KEY (trial_id) REFERENCES doe_trials(trial_id) ON DELETE RESTRICT
                )
                """)
                # Check existing columns in qc_records to migrate safely
                existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(qc_records)").fetchall()]
                common_cols = [
                    c for c in [
                        "batch_id", "formula_id", "revision", "test_date", "operator",
                        "hardness_gf", "transfer_g_10c", "density_g_cm3", "drop_point_c",
                        "hardness_probe", "transfer_substrate", "powder_bloom", "white_cast_score",
                        "sweating_syneresis", "notes", "hardness_sop_json", "transfer_sop_json",
                        "sop_complete", "trial_id", "data_origin", "process_conditions_json"
                    ] if c in existing_cols
                ]
                cols_str = ", ".join(common_cols)
                cursor.execute(f"INSERT INTO qc_records_v3_new ({cols_str}) SELECT {cols_str} FROM qc_records")
                cursor.execute("DROP TABLE qc_records")
                cursor.execute("ALTER TABLE qc_records_v3_new RENAME TO qc_records")
                cursor.execute("PRAGMA foreign_keys = ON;")

            # 5. Revision History table (Phase 6)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS revision_history (
                revision_id TEXT PRIMARY KEY,
                release_date TEXT NOT NULL,
                status TEXT NOT NULL,
                change_summary TEXT NOT NULL,
                changes_json TEXT NOT NULL,
                active_formula_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)

            # Seed Rev.7.3 baseline revision if not present
            cursor.execute("SELECT revision_id FROM revision_history WHERE revision_id = 'Rev.7.3'")
            if not cursor.fetchone():
                rev73_changes = [
                    {
                        "change_id": "NEW-01",
                        "category": "Wax System",
                        "title": "합성 왁스 비중 상향 (10% -> 12%) 및 칸데릴라 왁스 비율 조정 (7% -> 5%)",
                        "description": "융점 및 스틱 골격 안정성 향상, 30°C 이상 하절기 및 체온에 의한 유동 붕괴/스틱 꺾임 방지"
                    },
                    {
                        "change_id": "NEW-02",
                        "category": "Silicone System",
                        "title": "Dimethicone 17.0% + Caprylyl Methicone 11.0% 고정 배합 확립",
                        "description": "선형 실리콘의 마찰 방지 지속성과 휘발성 알킬 실리콘의 도포 시 끈적임 없는 실키 슬립 밸런스 달성"
                    },
                    {
                        "change_id": "NEW-03",
                        "category": "Dispersant",
                        "title": "C12-15 Alkyl Benzoate 9.5% 분산상 시스템 적용",
                        "description": "실리카 및 PMMA 파우더 입자의 균일 분산 촉진 및 도포 후 백탁 0% 투명 밀착막 형성"
                    },
                    {
                        "change_id": "NEW-04",
                        "category": "Powder Complex",
                        "title": "PMMA + Silica 구상 파우더 13.0% 복합 파우더 시스템 완성",
                        "description": "볼베어링 효과에 의한 동마찰 계수 mu < 0.15 극저마찰막 형성 및 과도한 유분감 흡착"
                    },
                    {
                        "change_id": "NEW-05",
                        "category": "Barrier Film",
                        "title": "Trimethylsiloxysilicate (MQ 레진) 2.0% 유효 성분 도입",
                        "description": "40km 행군/마라톤 땀(Sweat-washout) 및 연속 마찰에 견디는 고밀착 내수성 방수막 구현"
                    },
                    {
                        "change_id": "NEW-06",
                        "category": "Process SOP",
                        "title": "3단계 점진 냉각 공정 (25°C -> 15°C -> 5°C) SOP 확립",
                        "description": "왁스-실리콘 급랭 수축 균열 및 표면 오일 석출(Sweating/Syneresis) 현상 원천 억제"
                    },
                    {
                        "change_id": "NEW-07",
                        "category": "Cost & Supply",
                        "title": "원자재 제조 원가(COGS) 목표 달성: 2,610원 / 20g 스틱",
                        "description": "양산 목표치 2,950원/스틱 대비 11.5% 원가 절감 달성 및 안정적 공급망 확보"
                    },
                    {
                        "change_id": "NEW-08",
                        "category": "Quality Contract",
                        "title": "표준화된 QC SOP 검사 프로토콜(Data Contract v0.2) 수립",
                        "description": "2mm 니들 침투 경도 820±50gf 및 10°C 인공피부 2-stroke pay-off >= 0.040g 측정 규격화"
                    }
                ]
                active_formula_dict = {
                    "synthetic_wax_pct": 12.0,
                    "candelilla_wax_pct": 5.0,
                    "dimethicone_pct": 17.0,
                    "caprylyl_methicone_pct": 11.0,
                    "c12_15_alkyl_benzoate_pct": 9.5,
                    "pmma_silica_powder_pct": 13.0,
                    "trimethylsiloxysilicate_pct": 2.0,
                    "other_excipients_pct": 30.5
                }
                cursor.execute("""
                INSERT INTO revision_history (
                    revision_id, release_date, status, change_summary, changes_json, active_formula_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                """, (
                    "Rev.7.3",
                    "2026-09-12",
                    "PRODUCTION_BASELINE",
                    "Baseline 20g Anhydrous Powder-in-Balm formulation for 40km military march chafing defense.",
                    json.dumps(rev73_changes, ensure_ascii=False),
                    json.dumps(active_formula_dict, ensure_ascii=False)
                ))

            # Record schema versions
            cursor.execute("SELECT version FROM schema_versions WHERE version = 3")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO schema_versions (version, applied_at, description) VALUES (3, datetime('now'), ?)",
                    ("Phase 2A Data Contract v0.2: Table rebuild migration, batch FK, and COGS status",)
                )

            cursor.execute("SELECT version FROM schema_versions WHERE version = 4")
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO schema_versions (version, applied_at, description) VALUES (4, datetime('now'), ?)",
                    ("Phase 6 Revision DB Persistence: revision_history table and Rev.7.3 8-point baseline seed",)
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
            INSERT INTO doe_trials (
                trial_id, design_type, synthetic_wax_pct, candelilla_wax_pct,
                dimethicone_pct, caprylyl_methicone_pct, c12_15_alkyl_benzoate_pct,
                fill_temperature_c, shear_speed_rpm, mixing_time_min,
                cooling_profile, status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(trial_id) DO UPDATE SET
                design_type = excluded.design_type,
                synthetic_wax_pct = excluded.synthetic_wax_pct,
                candelilla_wax_pct = excluded.candelilla_wax_pct,
                dimethicone_pct = excluded.dimethicone_pct,
                caprylyl_methicone_pct = excluded.caprylyl_methicone_pct,
                c12_15_alkyl_benzoate_pct = excluded.c12_15_alkyl_benzoate_pct,
                fill_temperature_c = excluded.fill_temperature_c,
                shear_speed_rpm = excluded.shear_speed_rpm,
                mixing_time_min = excluded.mixing_time_min,
                cooling_profile = excluded.cooling_profile,
                status = excluded.status,
                notes = excluded.notes
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
            calc_time = batch.calculated_at or datetime.now().isoformat()

            cursor.execute("""
            INSERT INTO manufacturing_batches (
                batch_id, trial_id, formula_id, revision, created_date, operator,
                batch_size_kg, total_charge_pct, items_json, process_conditions_json,
                total_raw_material_cost, cost_per_20g_stick, target_cogs_per_stick,
                cogs_basis, material_price_source, quote_status, calculated_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(batch_id) DO UPDATE SET
                trial_id = excluded.trial_id,
                formula_id = excluded.formula_id,
                revision = excluded.revision,
                created_date = excluded.created_date,
                operator = excluded.operator,
                batch_size_kg = excluded.batch_size_kg,
                total_charge_pct = excluded.total_charge_pct,
                items_json = excluded.items_json,
                process_conditions_json = excluded.process_conditions_json,
                total_raw_material_cost = excluded.total_raw_material_cost,
                cost_per_20g_stick = excluded.cost_per_20g_stick,
                target_cogs_per_stick = excluded.target_cogs_per_stick,
                cogs_basis = excluded.cogs_basis,
                material_price_source = excluded.material_price_source,
                quote_status = excluded.quote_status,
                calculated_at = excluded.calculated_at,
                notes = excluded.notes
            """, (
                batch.batch_id, batch.trial_id, batch.formula_id, batch.revision,
                batch.created_date, batch.operator, batch.batch_size_kg, batch.total_charge_pct,
                items_json, proc_json, batch.total_raw_material_cost,
                batch.cost_per_20g_stick, batch.target_cogs_per_stick,
                batch.cogs_basis, batch.material_price_source, batch.quote_status,
                calc_time, batch.notes
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
                target_cogs_per_stick=r[12],
                cogs_basis=r[13] if len(r) > 13 else "ESTIMATED_SIMULATION",
                material_price_source=r[14] if len(r) > 14 else "Baseline Simulation Fixture",
                quote_status=r[15] if len(r) > 15 else "PENDING_FORMAL_QUOTES",
                calculated_at=r[16] if len(r) > 16 else None,
                notes=r[17] if len(r) > 17 else ""
            )

    def get_all_manufacturing_batches(self) -> List[ManufacturingBatch]:
        batches: List[ManufacturingBatch] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM manufacturing_batches ORDER BY created_date DESC")
            for r in cursor.fetchall():
                items = [BatchChargeItem(**i) for i in json.loads(r[8])]
                proc_cond = ProcessCondition(**json.loads(r[9]))
                batches.append(ManufacturingBatch(
                    batch_id=r[0], trial_id=r[1], formula_id=r[2], revision=r[3],
                    created_date=r[4], operator=r[5], batch_size_kg=r[6], total_charge_pct=r[7],
                    items=items, process_conditions=proc_cond,
                    total_raw_material_cost=r[10], cost_per_20g_stick=r[11],
                    target_cogs_per_stick=r[12],
                    cogs_basis=r[13] if len(r) > 13 else "ESTIMATED_SIMULATION",
                    material_price_source=r[14] if len(r) > 14 else "Baseline Simulation Fixture",
                    quote_status=r[15] if len(r) > 15 else "PENDING_FORMAL_QUOTES",
                    calculated_at=r[16] if len(r) > 16 else None,
                    notes=r[17] if len(r) > 17 else ""
                ))
        return batches

    # --------------------------------------------------------------------------
    # QC Records
    # --------------------------------------------------------------------------
    def save_qc_record(self, record: BatchQCRecord):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Strict Referential Integrity Gate 1: batch_id MUST exist in manufacturing_batches
            cursor.execute("SELECT 1 FROM manufacturing_batches WHERE batch_id = ?", (record.batch_id,))
            if not cursor.fetchone():
                raise sqlite3.IntegrityError(
                    f"Foreign Key violation: batch_id '{record.batch_id}' does not exist in manufacturing_batches table."
                )

            # Strict Referential Integrity Gate 2: trial_id MUST exist in doe_trials
            if record.trial_id:
                cursor.execute("SELECT 1 FROM doe_trials WHERE trial_id = ?", (record.trial_id,))
                if not cursor.fetchone():
                    raise sqlite3.IntegrityError(
                        f"Foreign Key violation: trial_id '{record.trial_id}' does not exist in doe_trials table."
                    )

            cursor.execute("""
            INSERT INTO qc_records (
                batch_id, formula_id, revision, test_date, operator, hardness_gf,
                transfer_g_10c, density_g_cm3, drop_point_c, hardness_probe,
                transfer_substrate, powder_bloom, white_cast_score, sweating_syneresis,
                notes, hardness_sop_json, transfer_sop_json, sop_complete,
                trial_id, data_origin, process_conditions_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(batch_id) DO UPDATE SET
                formula_id = excluded.formula_id,
                revision = excluded.revision,
                test_date = excluded.test_date,
                operator = excluded.operator,
                hardness_gf = excluded.hardness_gf,
                transfer_g_10c = excluded.transfer_g_10c,
                density_g_cm3 = excluded.density_g_cm3,
                drop_point_c = excluded.drop_point_c,
                hardness_probe = excluded.hardness_probe,
                transfer_substrate = excluded.transfer_substrate,
                powder_bloom = excluded.powder_bloom,
                white_cast_score = excluded.white_cast_score,
                sweating_syneresis = excluded.sweating_syneresis,
                notes = excluded.notes,
                hardness_sop_json = excluded.hardness_sop_json,
                transfer_sop_json = excluded.transfer_sop_json,
                sop_complete = excluded.sop_complete,
                trial_id = excluded.trial_id,
                data_origin = excluded.data_origin,
                process_conditions_json = excluded.process_conditions_json
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

    # --------------------------------------------------------------------------
    # Formula Revision Persistence (Phase 6)
    # --------------------------------------------------------------------------
    def save_revision(
        self,
        revision_id: str,
        release_date: str,
        status: str,
        change_summary: str,
        changes: List[Dict[str, Any]],
        active_formula: Dict[str, Any]
    ):
        """Persists or updates a Formula Revision with structured change logs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO revision_history (
                revision_id, release_date, status, change_summary,
                changes_json, active_formula_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(revision_id) DO UPDATE SET
                release_date = excluded.release_date,
                status = excluded.status,
                change_summary = excluded.change_summary,
                changes_json = excluded.changes_json,
                active_formula_json = excluded.active_formula_json
            """, (
                revision_id,
                release_date,
                status,
                change_summary,
                json.dumps(changes, ensure_ascii=False),
                json.dumps(active_formula, ensure_ascii=False)
            ))
            conn.commit()

    def get_all_revisions(self) -> List[Dict[str, Any]]:
        """Retrieves all tracked revisions ordered by release_date DESC."""
        revisions = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT revision_id, release_date, status, change_summary,
                   changes_json, active_formula_json, created_at
            FROM revision_history
            ORDER BY release_date DESC
            """)
            rows = cursor.fetchall()
            for r in rows:
                revisions.append({
                    "revision_id": r[0],
                    "release_date": r[1],
                    "status": r[2],
                    "change_summary": r[3],
                    "changes": json.loads(r[4]) if r[4] else [],
                    "active_formula": json.loads(r[5]) if r[5] else {},
                    "created_at": r[6]
                })
        return revisions

    def get_revision(self, revision_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a specific revision by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT revision_id, release_date, status, change_summary,
                   changes_json, active_formula_json, created_at
            FROM revision_history
            WHERE revision_id = ?
            """, (revision_id,))
            r = cursor.fetchone()
            if not r:
                return None
            return {
                "revision_id": r[0],
                "release_date": r[1],
                "status": r[2],
                "change_summary": r[3],
                "changes": json.loads(r[4]) if r[4] else [],
                "active_formula": json.loads(r[5]) if r[5] else {},
                "created_at": r[6]
            }

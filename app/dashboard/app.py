"""
GLIDE-SPEC 40 - Formulation Simulator Interactive Dashboard (M6)
Runs via: streamlit run app/dashboard/app.py
"""

import sys
import os
import streamlit as st
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.materials.master import RawMaterial, MaterialType, MaterialStatus, REV73_RAW_MATERIALS
from src.formulas.master import REV73_TARGET_ACTIVE_FORMULA
from src.manufacturing.calculator import ManufacturingCalculator, STANDARD_BATCH_SIZES
from src.manufacturing.models import ManufacturingBatch
from src.qc.models import BatchQCRecord, QCStatus, HardnessSOP, TransferSOP, DataOrigin, ProcessCondition
from src.doe.engine import AdvancedDOEEngine
from src.modeling.predictor import FormulationPredictor, ModelState
from src.optimization.optimizer import MultiObjectiveOptimizer
from src.revision.tracker import get_rev73_revision_master
from src.storage.db import FormulationDatabase

# Page config
st.set_page_config(
    page_title="GLIDE-SPEC 40 Simulator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header
st.markdown("""
<div style="background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); padding: 22px; border-radius: 10px; color: white; margin-bottom: 25px;">
    <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: 0.5px;">GLIDE-SPEC 40 : Formulation Digital Twin</h1>
    <p style="margin: 5px 0 0 0; opacity: 0.85; font-size: 15px;">Rev.7.3 Development Baseline | 20g Technical Solid Anti-Chafing Stick</p>
</div>
""", unsafe_allow_html=True)

# Initialize DB and Session State
db = FormulationDatabase()
if "materials" not in st.session_state:
    st.session_state.materials = db.load_materials_catalog()

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Modules",
    [
        "1. Target Active Formula",
        "2. Raw Material Master (TBD Gate)",
        "3. Manufacturing Calculator & COGS",
        "4. DOE Mixture Matrix",
        "5. QC & SOP Test Station",
        "6. Optimizer & Revision Tracker"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Core Principle:** Never finalize manufacturing formulas without verified raw material CoA. Prediction requires real QC data.")

# ==============================================================================
# 1. Target Active Formula
# ==============================================================================
if menu == "1. Target Active Formula":
    st.subheader("🎯 Rev.7.3 Target Active Formula (Locked Baseline)")
    st.caption("유효 활성 성분 100% 기준 개발 목표선. 임의 변경이 불가하며 실험 결과에 의해서만 다음 Revision으로 진화합니다.")

    comps = REV73_TARGET_ACTIVE_FORMULA.components
    data = [{
        "Material ID": c.material_id,
        "Component Name": c.material_name,
        "Target Active %": f"{c.target_active_pct:.1f}%",
        "Engineering Role / Notes": c.notes
    } for c in comps]

    df_formula = pd.DataFrame(data)
    st.dataframe(df_formula, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Target Active", "100.0%", "Balanced")
    with col2:
        st.metric("Powder System Loading", "28.0%", "BN + Silicas + PMSSQ + ZnO")
    with col3:
        st.metric("Carrier + Resin Matrix", "40.0%", "Silicone (28%) + MQ Resin (12%)")

# ==============================================================================
# 2. Raw Material Master (TBD Gate)
# ==============================================================================
elif menu == "2. Raw Material Master (TBD Gate)":
    st.subheader("📋 Raw Material Master & Specification Gatekeeper")
    st.write("공급사 성적서(TDS/CoA)를 통해 확인된 원료 스펙을 관리합니다. 필수 값이 `TBD` 상태인 원료는 생산 배합 계산에서 자동 차단됩니다.")

    materials = st.session_state.materials

    # Quick summary metric
    total_mats = len(materials)
    verified_mats = sum(1 for m in materials.values() if m.status == MaterialStatus.VERIFIED)
    tbd_mats = sum(1 for m in materials.values() if m.status == MaterialStatus.TBD)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Raw Materials", total_mats)
    m2.metric("Verified Specs (Ready)", verified_mats)
    m3.metric("Pending Specs (TBD Gate Blocked)", tbd_mats)

    st.markdown("### Material Specification Catalog")
    table_rows = []
    for mid, m in materials.items():
        table_rows.append({
            "ID": m.material_id,
            "INCI": m.inci,
            "Trade Name": m.trade_name,
            "Supplier": m.supplier,
            "Active %": f"{m.active_pct:.1f}%" if m.active_pct is not None else "TBD",
            "Carrier": m.carrier,
            "Cost/kg (KRW)": f"{m.cost_per_kg:,.0f}" if m.cost_per_kg else "TBD",
            "Status": m.status.value
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Update Material Spec (Simulate Supplier CoA Input)")
    with st.form("update_material_form"):
        sel_mat_id = st.selectbox("Select Material ID to Update", list(materials.keys()))
        current_mat = materials[sel_mat_id]

        c1, c2, c3 = st.columns(3)
        with c1:
            new_trade = st.text_input("Trade Name", current_mat.trade_name or "TBD")
            new_supplier = st.text_input("Supplier", current_mat.supplier or "TBD")
        with c2:
            new_active = st.number_input("Active %", min_value=1.0, max_value=100.0, value=float(current_mat.active_pct or 100.0))
            new_carrier = st.text_input("Carrier / Solvent", current_mat.carrier or "None")
        with c3:
            new_cost = st.number_input("Cost per kg (KRW)", min_value=0.0, value=float(current_mat.cost_per_kg or 0.0), step=1000.0)
            new_status = st.selectbox("Status", [s.value for s in MaterialStatus], index=2 if current_mat.status == MaterialStatus.VERIFIED else 0)

        submitted = st.form_submit_button("Save Material Specification")
        if submitted:
            current_mat.trade_name = new_trade
            current_mat.supplier = new_supplier
            current_mat.active_pct = new_active
            current_mat.carrier = new_carrier
            current_mat.cost_per_kg = new_cost if new_cost > 0 else None
            current_mat.status = MaterialStatus(new_status)
            materials[sel_mat_id] = current_mat
            st.session_state.materials = materials
            db.save_materials_catalog(materials)
            st.success(f"Updated {sel_mat_id} successfully!")
            st.rerun()

# ==============================================================================
# 3. Manufacturing Calculator & COGS
# ==============================================================================
elif menu == "3. Manufacturing Calculator & COGS":
    st.subheader("⚙️ Manufacturing Formula & Batch Scaler (M1)")
    st.write("Active Formula로부터 원료별 실제 투입 비율(Charge %)과 배치 중량을 역산하고 캐리어 용매를 상계 처리합니다.")

    c1, c2 = st.columns([1, 1])
    with c1:
        batch_preset = st.selectbox("Batch Scale Preset", list(STANDARD_BATCH_SIZES.keys()), index=6)
        preset_spec = STANDARD_BATCH_SIZES[batch_preset]
        batch_weight_kg = st.number_input("Batch Size (kg)", min_value=0.01, max_value=500.0, value=float(preset_spec.target_weight_kg), step=1.0)
    with c2:
        offset_carrier = st.toggle("Enable Carrier Offsetting", value=True, help="MQ Resin 등에 포함된 실리콘 용매를 메인 실리콘 캐리어(28%)에서 자동 차감")
        use_sample_mock = st.toggle("Simulate with Confirmed Specs (Demo Mode)", value=True, help="TBD 원료를 모의 확정 스펙으로 채워 계산기 동작 시연")

    working_materials = dict(st.session_state.materials)
    if use_sample_mock:
        # Provide sample verified specs
        working_materials["MAT-MQ-01"] = RawMaterial(
            material_id="MAT-MQ-01",
            inci="Trimethylsiloxysilicate (and) Dimethicone",
            trade_name="MQ-60-D",
            supplier="Shin-Etsu",
            grade="Resin Premix",
            material_type=MaterialType.RESIN,
            active_pct=60.0,
            carrier="Dimethicone",
            carrier_pct=40.0,
            cost_per_kg=65000.0,
            status=MaterialStatus.VERIFIED
        )
        working_materials["MAT-WAX-SYN-01"].cost_per_kg = 18000.0
        working_materials["MAT-WAX-CAN-01"].cost_per_kg = 28000.0
        working_materials["MAT-BN-01"].cost_per_kg = 120000.0
        working_materials["MAT-SILICA-01"].cost_per_kg = 45000.0
        working_materials["MAT-SIL-DIM-01"].cost_per_kg = 15000.0
        working_materials["MAT-EMO-AB-01"].cost_per_kg = 16000.0

    calc_res = ManufacturingCalculator.generate_manufacturing_formula(
        active_formula=REV73_TARGET_ACTIVE_FORMULA,
        material_specs=working_materials,
        batch_size_kg=batch_weight_kg,
        offset_carrier=offset_carrier
    )

    if not calc_res.is_valid:
        st.error("🚫 Manufacturing Formula Generation Blocked by Gatekeeper")
        st.write("**Missing or Incomplete Raw Material Specifications:**")
        for miss in calc_res.missing_specs:
            st.warning(f"• {miss}")
    else:
        st.success(f"✅ Manufacturing Formula Calculated for {batch_weight_kg:.2f} kg Batch")

        # Metric cards
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Charge %", f"{calc_res.total_charge_pct:.2f}%")
        m2.metric("Total Batch Weight", f"{batch_weight_kg:.2f} kg")
        if calc_res.cost_per_20g_stick:
            m3.metric("Bulk Cost (20g Stick)", f"₩{calc_res.cost_per_20g_stick:,.1f}")
            m4.metric("COGS Budget Utilization", f"{calc_res.cogs_budget_pct:.1f}%", delta=f"Target: ₩2,950")

        if calc_res.carrier_offsets_applied:
            st.info("🔄 **Carrier Offsetting Applied:** " + " | ".join(calc_res.carrier_offsets_applied))

        # Items table
        items_data = [{
            "Material": item.material_name,
            "INCI": item.inci,
            "Target Active %": f"{item.active_contribution_pct:.1f}%",
            "Charge %": f"{item.charge_pct:.2f}%",
            "Weight (kg)": f"{item.charge_weight_kg:.3f}",
            "Weight (g)": f"{item.charge_weight_g:.1f}",
            "Cost/kg (KRW)": f"₩{item.cost_per_kg:,.0f}" if item.cost_per_kg else "-",
            "Item Total (KRW)": f"₩{item.item_total_cost:,.0f}" if item.item_total_cost else "-"
        } for item in calc_res.items]

        df_items = pd.DataFrame(items_data)
        st.dataframe(df_items, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 💾 Commit Calculation to Manufacturing Batch Record (Phase 2A)")
        with st.form("commit_batch_form"):
            cb1, cb2, cb3 = st.columns(3)
            with cb1:
                new_batch_id = st.text_input("New Batch ID to Commit", value=f"BATCH-MFG-{preset_spec.batch_name.split()[0]}-001")
            with cb2:
                batch_operator = st.text_input("Production / Pilot Lead", value="Chief Compounder")
            with cb3:
                all_trials_mfg = db.get_all_doe_trials()
                mfg_trial_opts = ["None (Standard Scale-up)"] + [t.trial_id for t in all_trials_mfg]
                sel_mfg_trial = st.selectbox("Associated DOE Trial ID", mfg_trial_opts, index=0)
                actual_mfg_trial_id = None if sel_mfg_trial.startswith("None") else sel_mfg_trial

            batch_commit_btn = st.form_submit_button("Commit & Persist Manufacturing Batch")
            if batch_commit_btn:
                # Resolve process condition from trial or standard
                batch_proc = ProcessCondition()
                if actual_mfg_trial_id:
                    trial_found = db.get_doe_trial(actual_mfg_trial_id)
                    if trial_found:
                        batch_proc = trial_found.to_process_condition()

                mfg_batch_record = ManufacturingBatch(
                    batch_id=new_batch_id,
                    trial_id=actual_mfg_trial_id,
                    formula_id=calc_res.formula_id,
                    revision=calc_res.revision,
                    created_date="2026-09-12",
                    operator=batch_operator,
                    batch_size_kg=calc_res.batch_size_kg,
                    total_charge_pct=calc_res.total_charge_pct,
                    items=calc_res.items,
                    process_conditions=batch_proc,
                    total_raw_material_cost=calc_res.total_raw_material_cost,
                    cost_per_20g_stick=calc_res.cost_per_20g_stick,
                    target_cogs_per_stick=calc_res.target_cogs_per_stick,
                    notes=f"Generated from {batch_preset} preset ({batch_weight_kg} kg)."
                )
                db.save_manufacturing_batch(mfg_batch_record)
                st.success(f"✅ Manufacturing Batch '{new_batch_id}' successfully saved to SQLite database with full material & cost snapshots!")

# ==============================================================================
# 4. DOE Mixture Matrix
# ==============================================================================
elif menu == "4. DOE Mixture Matrix":
    st.subheader("🧪 Advanced Constrained Mixture DOE Engine (M2)")
    st.write("왁스 시스템(17%)과 실리콘 시스템(28%)의 미확정 세부 비율 및 충전 공정 후보값(75~85°C)을 탐색하기 위한 직교 파일럿 실험 계획입니다.")

    trials = AdvancedDOEEngine.generate_full_doe_design()
    df_doe = AdvancedDOEEngine.export_to_dataframe(trials)

    st.write(f"Generated **{len(trials)} Orthogonal Pilot Experimental Runs**:")
    st.dataframe(df_doe, use_container_width=True, hide_index=True)

    csv_data = df_doe.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Download DOE Matrix as CSV",
        data=csv_data,
        file_name="GLIDE_SPEC_40_Rev7.3_Pilot_DOE_Matrix.csv",
        mime="text/csv"
    )

# ==============================================================================
# 5. QC & SOP Test Station
# ==============================================================================
elif menu == "5. QC & SOP Test Station":
    st.subheader("🔬 QC Test Station & Laboratory SOP Records (M3)")
    st.write("동일한 수치라도 시험 방법(SOP)이 다르면 QC로 인정하지 않습니다. 측정값과 시험 장비/환경 조건을 함께 기록합니다.")

    with st.form("qc_entry_form"):
        st.markdown("#### 1. Batch Identification & Data Contract (Phase 2A)")
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            batch_id = st.text_input("Batch ID", value="BATCH-PILOT-001")
        with b2:
            formula_id = st.text_input("Formula ID", value="FORM-GLIDE40-REV7.3")
        with b3:
            operator = st.text_input("Operator / Lab Engineer", value="Lead Chemist")
        with b4:
            data_origin_val = st.selectbox("Data Origin", ["REAL_PILOT", "SYNTHETIC_TEST"], index=0, help="REAL_PILOT만 머신러닝 학습 세트에 편입됩니다.")

        st.markdown("#### 2. Linked DOE Trial & Process Conditions")
        all_trials = db.get_all_doe_trials()
        trial_options = ["None (Unlinked Manual Batch)"] + [t.trial_id for t in all_trials]
        selected_trial = st.selectbox("Linked DOE Trial ID", trial_options, index=0)
        actual_trial_id = None if selected_trial.startswith("None") else selected_trial

        st.markdown("#### 3. Core QC Measurements & Mandatory SOP Tracking")
        q1, q2 = st.columns(2)
        with q1:
            meas_hardness = st.number_input("Hardness @ 25°C (gf) [Target: 750~900]", min_value=0.0, max_value=2000.0, value=820.0)
            probe_type = st.selectbox("Hardness Probe Type", ["2mm Cylindrical Needle", "45 deg Conical", "10mm Sphere"])
            depth_mm = st.number_input("Penetration Depth (mm)", value=2.0)
            test_speed = st.number_input("Test Speed (mm/s)", value=1.0)
            cond_time = st.number_input("Conditioning Time (min)", value=30)
        with q2:
            meas_transfer = st.number_input("Pay-off / Transfer @ 10°C (g) [Target: >= 0.040]", min_value=0.0, max_value=1.0, value=0.048, format="%.3f")
            substrate = st.selectbox("Transfer Substrate", ["Artificial Collagen Skin", "Textured Polyurethane Leather", "Human Forearm"])
            applied_area = st.number_input("Applied Area (cm²)", value=4.0)
            pressure_g = st.number_input("Applied Contact Pressure (g)", value=500.0)
            contact_time = st.number_input("Contact Time (s)", value=3.0)
            test_method = st.text_input("Test Method / SOP Code", value="Two-stroke standardized friction SOP")

        q3, q4 = st.columns(2)
        with q3:
            meas_density = st.number_input("Density (g/cm³) [Target: 1.04~1.12]", min_value=0.5, max_value=2.0, value=1.08, format="%.2f")
        with q4:
            meas_drop_point = st.number_input("Drop Point (°C) [Target: 60.0~63.0]", min_value=30.0, max_value=100.0, value=61.8)

        qc_notes = st.text_area("Lab Observations (Powder Bloom, White Cast, Stick Glide etc.)", "Smooth pay-off, zero chalking on black fabric, no syneresis observed.")

        qc_submit = st.form_submit_button("Record QC Laboratory Result")
        if qc_submit:
            # Phase 2A Data Contract v0.2: Snapshot real process conditions from linked DOE Trial
            proc_cond = ProcessCondition()
            if actual_trial_id:
                linked_trial_obj = db.get_doe_trial(actual_trial_id)
                if linked_trial_obj:
                    proc_cond = linked_trial_obj.to_process_condition()

            new_record = BatchQCRecord(
                batch_id=batch_id,
                formula_id=formula_id,
                revision="Rev.7.3",
                test_date="2026-09-12",
                operator=operator,
                trial_id=actual_trial_id,
                data_origin=DataOrigin(data_origin_val),
                process_conditions=proc_cond,
                hardness_gf=meas_hardness,
                transfer_g_10c=meas_transfer,
                density_g_cm3=meas_density,
                drop_point_c=meas_drop_point,
                hardness_sop=HardnessSOP(
                    probe_type=probe_type,
                    penetration_depth_mm=depth_mm,
                    test_speed_mm_s=test_speed,
                    conditioning_time_min=int(cond_time)
                ),
                transfer_sop=TransferSOP(
                    substrate_type=substrate,
                    applied_area_cm2=applied_area,
                    applied_pressure_g=pressure_g,
                    contact_time_s=contact_time,
                    test_method=test_method
                ),
                notes=qc_notes
            )
            db.save_qc_record(new_record)
            if new_record.is_sop_complete():
                st.success(f"✅ QC Record for {batch_id} successfully persisted! (SOP Complete & Training Eligible)")
            else:
                st.warning(f"⚠️ QC Record for {batch_id} saved, but SOP is INCOMPLETE (cannot be used for model training).")

    st.markdown("---")
    st.markdown("### QC Test History & Target Pass/Fail Analysis")
    all_qc = db.get_all_qc_records()
    if all_qc:
        eval_list = []
        for r in all_qc:
            evals = r.evaluate_targets()
            eval_list.append({
                "Batch ID": r.batch_id,
                "Linked Trial": r.trial_id or "-",
                "Origin": r.data_origin.value,
                "SOP Status": "COMPLETE" if r.is_sop_complete() else "INCOMPLETE",
                "Hardness": f"{r.hardness_gf:.0f} gf ({evals['hardness'].status.value})",
                "Transfer": f"{r.transfer_g_10c:.3f} g ({evals['transfer'].status.value})",
                "Density": f"{r.density_g_cm3:.2f} ({evals['density'].status.value})",
                "Drop Point": f"{r.drop_point_c:.1f}°C ({evals['drop_point'].status.value})",
                "Notes": r.notes
            })
        st.dataframe(pd.DataFrame(eval_list), use_container_width=True, hide_index=True)
    else:
        st.info("No QC test records currently logged in database.")

# ==============================================================================
# 6. Optimizer & Revision Tracker
# ==============================================================================
elif menu == "6. Optimizer & Revision Tracker":
    st.subheader("🔮 Multi-Objective SLSQP Optimizer & Revision History (Phase 4 ~ Phase 6)")

    predictor = FormulationPredictor()
    all_qc = db.get_all_qc_records()
    predictor.fit(all_qc, verified_raw_materials=True, db=db)

    col_state1, col_state2 = st.columns([1, 2])
    with col_state1:
        st.write(f"**ML Property Predictor State:** `{predictor.state.value}`")
    with col_state2:
        if predictor.state == ModelState.TRAINED_LINEAR:
            st.success("✅ **Calibrated Linear Model:** Real pilot observations threshold achieved. Full SLSQP Multi-Objective Optimization enabled.")
        else:
            st.warning(f"⚠️ **[RULE #6 LOCKED]:** Waiting for $\\ge {FormulationPredictor.MIN_ELIGIBLE_PILOT_RECORDS}$ real Pilot records with $\\ge {FormulationPredictor.MIN_CENTRE_POINT_REPLICATES}$ centre-points. Using rule-based boundary candidates.")

    if predictor.state == ModelState.TRAINED_LINEAR and predictor.metrics:
        with st.expander("📈 Multivariate Mixture Regression Model Metrics (M4 Engine)", expanded=False):
            m_cols = st.columns(3)
            with m_cols[0]:
                st.metric("Hardness R²", f"{predictor.metrics['hardness'].r_squared:.3f}", f"LOOCV: ±{predictor.metrics['hardness'].loocv_rmse:.1f} gf")
            with m_cols[1]:
                st.metric("Transfer R²", f"{predictor.metrics['transfer'].r_squared:.3f}", f"LOOCV: ±{predictor.metrics['transfer'].loocv_rmse:.4f} g")
            with m_cols[2]:
                st.metric("Training Observations", f"{predictor.metrics['hardness'].sample_count} samples", "Real Pilot Data")

    optimizer = MultiObjectiveOptimizer(predictor=predictor)
    candidates = optimizer.generate_candidates(top_n=3)

    st.markdown("#### 🎯 SLSQP Pareto Frontier Candidates (Rev.7.4 Candidates)")
    cand_data = []
    for c in candidates:
        cand_data.append({
            "Candidate ID": c.candidate_id,
            "Scenario": c.scenario_name,
            "Syn Wax %": f"{c.synthetic_wax_pct:.1f}%",
            "Can Wax %": f"{c.candelilla_wax_pct:.1f}%",
            "Dimethicone %": f"{c.dimethicone_pct:.1f}%",
            "Caprylyl %": f"{c.caprylyl_methicone_pct:.1f}%",
            "Fill Temp": f"{c.fill_temperature_c:.1f}°C",
            "Est. COGS": f"{c.estimated_cogs_krw:,.0f} ₩",
            "Pred. Hardness": f"{c.predicted_hardness_gf:.0f} gf" if c.predicted_hardness_gf is not None else "Pending QC",
            "Pred. Transfer": f"{c.predicted_transfer_g:.4f} g" if c.predicted_transfer_g is not None else "Pending QC",
            "Desirability": f"{c.desirability_score:.2f}",
            "Rule #12 Label / Note": c.prediction_label or c.notes
        })
    st.dataframe(pd.DataFrame(cand_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 📜 Database-Backed Formula Revision History (Schema v4)")
    db_revisions = db.get_all_revisions()

    if db_revisions:
        rev_tabs = st.tabs([f"{r['revision_id']} ({r['status']})" for r in db_revisions])
        for tab, rev in zip(rev_tabs, db_revisions):
            with tab:
                st.write(f"**Release Date:** `{rev['release_date']}` | **Status:** `{rev['status']}`")
                st.write(f"**Summary:** {rev['change_summary']}")

                st.markdown("##### 8 Key Engineering Improvements (NEW-01 ~ NEW-08)")
                ch_list = rev.get("changes", [])
                if ch_list:
                    ch_df = pd.DataFrame([{
                        "Item ID": item.get("change_id", "-"),
                        "Category": item.get("category", "-"),
                        "Title": item.get("title", "-"),
                        "Detailed Rationale": item.get("description", "-")
                    } for item in ch_list])
                    st.dataframe(ch_df, use_container_width=True, hide_index=True)

                st.markdown("##### Active Target Formulation Breakdown")
                formula_dict = rev.get("active_formula", {})
                if formula_dict:
                    f_df = pd.DataFrame([{"Component": k, "Target Share %": f"{v:.1f}%"} for k, v in formula_dict.items()])
                    st.dataframe(f_df, use_container_width=True, hide_index=True)
    else:
        st.info("No persisted revisions found in database.")

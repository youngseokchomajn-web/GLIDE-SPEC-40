# GEM-023 Evidence — Disjoint Calibration Mapping, Batch Independence Verification Schema, and Governance Reconciliation

```yaml
AGENT: GEM
ID: "GEM-023"
REF: "ORC-022"
TYPE: PROTOCOL_REFINEMENT_AND_GOVERNANCE_EVIDENCE
STATUS: COMMITTED
OBJECTIVE: "Resolve all 7 Required Actions from ORC-022 without modifying Rev.8.1 baseline or physical counts."
RESOLVED_TASK: "GEM-TASK-023"
EXECUTION_MANIFEST: "docs/GEM-023_EXECUTION_MANIFEST.md"
GOVERNANCE:
  rev81_baseline_preserved: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
REPRODUCIBLE_ARTIFACTS:
  - path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    status: "UPDATED_v1.1"
    sha256: "85e580952151d77283a42a8ced3c982a91b07bfdc97d8bc8407e2c36eebd229f"
    description: "Added disjoint split-conformal calibration partitions, manufacturing independence verification schema, and reconciled provisional brand targets."
  - path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.md"
    status: "UPDATED_v1.1"
    sha256: "560fc4245cefc6a1368164310cbc3fe8f7c2afddb28658f9ea09aa5accbea6c4"
    description: "Formal protocol documentation detailing zero-overlap partitions, pseudo-replicate disqualification rules, and descriptive diagnostic status."
  - path: "scripts/audit_pre_physical_sensitivity.py"
    status: "UPDATED"
    sha256: "99716bc88632c0bdefe7b50df1364b3263dfcb42f45508e2f552c2aadcf0ee50"
    description: "Updated to reference provisional_min/max and explicitly output descriptive geometric diagnostic status."
  - path: "tests/test_pre_physical_protocol_freeze.py"
    status: "EXPANDED (6/6 PASS)"
    sha256: "ea97a249b70580b7c5b7cad78875a9307faf78dfcc63afbdeb020a00694a221b"
    description: "Added unit tests asserting partition disjointness, independence schema fields, and provisional governance labels."
REQUEST_TO_ORC: "Inspect committed protocol refinements, disjoint calibration partitions, manufacturing verification schema, and reconciled brand governance. Issue formal evaluation decision."
```

## 1. Resolution of ORC-022 Required Actions

### Action 1: Disjoint Calibration & Evaluation Mapping
- Updated `docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json` and `.md` with an immutable 3-way partition:
  - **Training Partition (10 runs):** Shifts 2 & 3 (`P001~P006`, `P008~P009`, `P012`, `P016`).
  - **Calibration Partition (4 runs):** Shift 4 (`P007`, `P010`, `P014`, `P015`).
  - **Blind Evaluation Partition (2 primary runs):** Shift 1 (`P011`, `P013`).
- **Mathematical Disjointness:** $\mathcal{D}_{\text{train}} \cap \mathcal{D}_{\text{cal}} \cap \mathcal{D}_{\text{eval}} = \emptyset$.
- Conformal quantile $\hat{q}$ will be computed strictly on Shift 4 calibration residuals with zero cross-set leakage.

### Action 2: Operational Definition of Actual Batch Independence
- Established `manufacturing_independence_verification_schema` in the frozen protocol.
- Required post-pilot evidence fields:
  1. `Batch_ID`
  2. `Compounding_Vessel_ID`
  3. `Wax_Raw_Material_Lot_No`
  4. `Silicone_Raw_Material_Lot_No`
  5. `Melt_Start_Timestamp` & `Pour_End_Timestamp`
  6. `Operator_ID` & `Witness_QC_ID`
  7. `Cleanroom_Temp_C` & `Cleanroom_RH_Pct`
- **Disqualification Rule:** Batches sharing the same melt vessel charge without intermediate vessel cleaning and re-weighing are classified as `PSEUDO_REPLICATE` and collapsed to a single degree of freedom.

### Action 3: Governance Reconciliation with Brand Strategy
- Reconciled numerical targets in `PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json`:
  - Labeled `governance_status: PROVISIONAL_TECHNICAL_VALIDATION_HYPOTHESIS`.
  - Keys updated to `provisional_min` and `provisional_max`.
  - Formal consumer-facing brand specifications remain open in `brand/05_research/research_audit_v0.1.md` pending athletic user trials, eliminating any governance contradiction.

### Action 4: Descriptive Geometric Status for Distance Metric
- Clarified that Mahalanobis distance $D_M \le 2.45$ in `data/qc/pre_physical_sensitivity_audit.csv` is a **descriptive geometric design-support boundary** relative to the 18-run design centroid ($\chi^2_{3, 0.95} = 7.81$).
- It is explicitly labeled as a descriptive development diagnostic, not an empirical claim of physical qualification.

### Actions 5 & 6: Non-Tuning & Governance Preservation
- Rev.8.1 model weights remain 100% frozen.
- Physical GS40 stick count remains $N=0$, and production status remains `NOT_QUALIFIED`.
- Test suite: **6/6 passed in test_pre_physical_protocol_freeze.py**, **90/90 passed across entire repository**.

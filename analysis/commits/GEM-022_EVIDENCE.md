# GEM-022 Evidence — Physical Validation Protocol Freeze, Independent Manufacturing Group Structure, and Pre-Physical Sensitivity Audit

```yaml
AGENT: GEM
ID: "GEM-022"
REF: "ORC-021"
TYPE: PROTOCOL_FREEZE_AND_READINESS_EVIDENCE
STATUS: COMMITTED
OBJECTIVE: "Deliver frozen validation protocol, independent manufacturing shift structure, and pre-physical sensitivity audit fulfilling ORC-021 Actions 3, 4, 5."
RESOLVED_TASK: "GEM-TASK-022"
EXECUTION_MANIFEST: "docs/GEM-022_EXECUTION_MANIFEST.md"
GOVERNANCE:
  rev81_baseline_preserved: true
  n_physical_gs40_sticks: 0
  production_qualification: "NOT_QUALIFIED"
REPRODUCIBLE_ARTIFACTS:
  - path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.md"
    status: "FROZEN"
    description: "Detailed protocol defining 4 physical manufacturing shifts, pure error isolation, and brand target alignment."
  - path: "docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json"
    status: "FROZEN"
    description: "Machine-readable specification locking shift block mapping, conformal split rules, and acceptance gates."
  - path: "scripts/audit_pre_physical_sensitivity.py"
    status: "COMMITTED"
    description: "Deterministic non-tuning script auditing local response sensitivities and Mahalanobis distances."
  - path: "data/qc/pre_physical_sensitivity_audit.csv"
    status: "GENERATED"
    description: "Audit table for 18 pilot runs with finite difference sensitivities and brand spec compliance checks."
  - path: "tests/test_pre_physical_protocol_freeze.py"
    status: "PASSED (4/4 tests)"
    description: "Automated test suite asserting JSON integrity, shift grouping structure, and deterministic reproducibility."
REQUEST_TO_ORC: "Inspect committed protocol freeze, manufacturing shift structure, and pre-physical sensitivity audit evidence. Issue formal evaluation decision."
```

## 1. Resolution of ORC-021 Required Actions

### Action 3: Statistically Defensible Group Structure Based on Manufacturing Identity
- Rather than relying on purely post-hoc geometric clusters (Vertex vs Axial), `docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.md` establishes **4 independent compounding shifts / melt cycles** (`SHIFT_BLOCK_1` through `SHIFT_BLOCK_4`):
  - **Shift 1 (Orders 01~04):** P017 (Supplemental), P011 (Interior), P013 (Centroid Replicate 1), P018 (Supplemental).
  - **Shift 2 (Orders 05~09):** P003 (Vertex), P005 (Axial), P008 (Axial), P006 (Axial), P016 (Centroid Replicate 4).
  - **Shift 3 (Orders 10~14):** P004 (Vertex), P009 (Axial), P012 (Interior), P002 (Vertex), P001 (Vertex).
  - **Shift 4 (Orders 15~18):** P014 (Centroid Replicate 2), P010 (Axial), P007 (Axial), P015 (Centroid Replicate 3).
- **Inter-Shift Pure Error Isolation:** Center points are deliberately spread across Shift 1, Shift 2, and Shift 4. This enables separating compounding batch error from intra-batch testing repeatability during the Lack-of-Fit F-test.
- **Supplemental Isolation:** P017 and P018 remain strictly isolated from the 16-run primary qualification count.

### Action 4: Non-Tuning Readiness & Sensitivity Audit
- Created `scripts/audit_pre_physical_sensitivity.py` and generated `data/qc/pre_physical_sensitivity_audit.csv`.
- Audited all 18 pilot runs without modifying any Rev.8.1 model weights:
  - Local gradient sensitivities:
    - $\frac{\partial \text{Hardness}}{\partial \text{Wax}} \approx +12.35\text{ gf/\%}$
    - $\frac{\partial \text{Hardness}}{\partial \text{Silicone}} \approx -8.45\text{ gf/\%}$
    - $\frac{\partial \text{Hardness}}{\partial \text{Temp}} \approx +1.82\text{ gf/}^\circ\text{C}$
  - Mahalanobis distances $D_M$ range from $0.0000$ (Centroid) to $2.4474$ (extrema vertices), confirming that all 18 runs lie within the well-conditioned support of the design space.

### Action 5: Validation Protocol, Calibration Strategy, and Acceptance Gates Frozen
- Fully locked into `docs/PHYSICAL_VALIDATION_PROTOCOL_FREEZE.json`:
  - Split-conformal calibration design requires independent calibration batches without in-sample leakage.
  - Acceptance gates: $N_{\text{primary}} \ge 16$, $N_{\text{CP}} \ge 3$, Repeatability $\text{CV} \le 4.0\%$, Lack-of-Fit $p \ge 0.05$, Group-CV $R^2 \ge 0.85$, Conformal coverage $\ge 85.0\%$.

### Brand Requirement Integration
- Seamlessly connects with `brand/03_product/performance_requirements.md`:
  - **Drop Point ($60.0 \sim 75.0^\circ\text{C}$):** Thermal endurance in hot running conditions.
  - **Transfer Index ($0.038 \sim 0.058\text{ g}$):** Friction barrier film without clothing staining.
  - **Hardness ($700 \sim 850\text{ gf}$):** Mechanical integrity preventing stick fracture during motion.
  - **Kinetic CoF ($0.120 \sim 0.165$):** Kinetic shear reduction across marathon duration.

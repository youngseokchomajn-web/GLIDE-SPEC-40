# GLIDE-SPEC 40: System Changelog

All notable changes to the GLIDE-SPEC 40 simulation, modeling, and active learning engines are documented herein.

---

## [P001 Physical Validation Handoff Audit] - 2026-09-14
### Changed
- Added `docs/P001_PHYSICAL_VALIDATION_HANDOFF_AUDIT_REV1.md` as the current P001 manufacturing handoff gate.
- Reclassified P001 as `CONDITIONAL READY / DO NOT MANUFACTURE YET` until material specifications, Formula version, prediction snapshot, QC SOP and manufacturing setup are frozen.
- Corrected the physical-sheet shorthand for the 2% Soothing Blend: Rev.7.3 lists Bisabolol + Stearyl Glycyrrhetinate + Tocopherol + Rosemary Extract, so the two-component shorthand is no longer treated as the physical formula.
- Added explicit MQ Resin CoA/solids/carrier gate and required recalculation of the Dimethicone carrier offset from the actual lot.
- Clarified that P001 process values are initial process candidates and that Target vs Actual must remain separate.
- Clarified that historical 18-run randomization `Execution_Order #14` is not the current P001 execution order; P001 is the first physical validation batch under the current sequential plan.
- Added minimum raw QC linkage for hardness, transfer, drop point, friction/CoF, appearance and density, with test-condition capture requirements.
- Added manufacturer handoff controls for substitutions, scale changes, equipment changes, yield/loss and deviations.

### Decision
- Do not manufacture P001 until all pre-manufacture gates in the handoff audit are passed.
- P001 remains the first and only currently authorized GLIDE physical validation candidate; P002-P018 remain virtual/historical candidate identifiers unless a later decision authorizes another physical run.
- No P001 result can be used to claim Production Model qualification.

---

## [P001 Execution Sheet Provenance Fix] - 2026-09-14
### Changed
- Updated `data/doe/GS40_CAL_001_EXECUTION_SHEET.csv` so the physical P001 execution sheet contains only execution targets and REAL_PILOT actual-measurement fields.
- Removed historical `Prior:` values from physical QC measurement rows to prevent virtual predictions from being mistaken for measured results.
- Kept virtual prior predictions isolated in `data/doe/pilot_doe_virtual_prior_baseline.csv`.
- Added explicit model-linkage fields for virtual prior, immutable prediction snapshot and post-measurement residual/error.
- Clarified that P001 is a first physical validation anchor and is not, by itself, Production Model qualification.
- Clarified that the registered P001 batch is a 1.0 kg pilot batch; any different physical scale requires explicit new batch registration rather than silently changing P001.

### Decision
- P001 actual measurements must be entered only after physical execution and must preserve raw replicates and test conditions.
- Virtual prior values may inform prediction and experiment selection but must never populate REAL_PILOT actual fields.
- After P001 actual data are available, model error/uncertainty and EIG will be recalculated before deciding whether another physical experiment is justified.

---

## [Manufacturer-Simulator Data Interface] - 2026-09-14
### Added
- Added `docs/MANUFACTURER_SIMULATOR_DATA_INTERFACE_REV1.md`.

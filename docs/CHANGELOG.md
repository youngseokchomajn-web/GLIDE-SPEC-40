# GLIDE-SPEC 40: System Changelog

All notable changes to the GLIDE-SPEC 40 simulation, modeling, and active learning engines are documented herein.

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
- Defined a common data boundary between manufacturer sample development and the GLIDE simulator.
- Added identifiers for sample, formulation, batch, manufacturer, package and process so formulation changes and manufacturing repeats remain traceable.
- Defined priority formulation, powder-loading, process, physical-property, friction/use-feel and environmental fields for sample data collection.
- Defined the intended linkage `sample_id → formulation/process inputs → GLIDE prediction → actual measurement → residual/error`.
- Separated development data, independent validation data and later real-use data to reduce leakage and preserve credible model evaluation.
- Required raw measurements and test conditions to be preserved where available rather than storing only summarized scores.
- Added a minimum executable dataset for the first manufacturer samples without requiring an unnecessarily large data package.
- Added version-control rules linking formulation, test-method, data-schema and model versions.

### Decision
- Manufacturer samples will be treated as potential external validation data for GLIDE, not merely as product-development artifacts.
- No calibration or qualification claim will be made until sufficient real measurements are available and the relevant data split is explicitly defined.
- The actual code input schema is not assumed to be identical to this planning interface; implementation changes require separate version tracking.

---

## [Manufacturer Execution Plan] - 2026-09-14
### Added
- Added `docs/MANUFACTURER_EXECUTION_PLAN_REV1.md`.
- Converted the manufacturer work from public-web screening to an execution sequence: **6-company RFQ → comparable response collection → 2–3 technical candidates → 2–3 sample developments → user testing → formulation/process revision → pilot → first commercial production review**.
- Defined the first RFQ disclosure boundary: 20 g solid stick, anti-chafing use case, anhydrous wax/oil/silicone direction, dispersed fine particulate materials, smooth glide and relatively dry finish; detailed formulation/batch composition remains withheld until basic feasibility is confirmed.
- Added separate checks for **content MOQ vs. package/component MOQ**, rather than treating a single advertised MOQ as the actual launch constraint.
- Added a requirement to identify **1–3 previous products closest in physical behavior** to GLIDE-SPEC 40 as stronger evidence than a generic claim of manufacturing capability.
- Defined sample evaluation criteria covering glide, friction, sweat/moisture, transfer to clothing, residue, tack/shine, powderiness, whitening, agglomeration, stick hardness and mechanical integrity.
- Defined pilot/first-production sequence and retained flexibility to use approximately 1,000 units as the first commercial batch if 500-unit production is impractical.
- Connected manufacturer development with the parallel GLIDE simulator validation track: public data → prediction → independent validation → error analysis → model improvement; actual sample measurements may later be used for calibration/qualification where appropriate.
- Added manufacturer exclusion criteria covering weak technical evidence, infeasible sampling, excessive package MOQ, inadequate sample quality/repeatability and incompatible IP/ownership terms.

### Decision
- Stop expanding the manufacturer list unless new evidence materially changes the candidate pool; **execute the first RFQ wave first**.
- Do not disclose the full Rev.7.3 formulation in the first contact.
- Do not lock the final manufacturer or first-production quantity from website claims or quotations alone; require technical review and sample evidence first.

---

## [Manufacturer Candidate Screening] - 2026-09-14
### Added
- Added `docs/MANUFACTURER_CANDIDATE_SCREENING_REV1.md`.
- Completed a first public-evidence screening of domestic OEM/ODM candidates for the 20 g solid-stick anti-chafing product.
- Prioritized **Laonhase, Heib Lab, Hankook Cosmetics Manufacturing, Monami Cosmetics, MLS and Cosmo C&T** for first-round technical/RFQ contact.
- Added secondary candidates including Hankook Cosmo, Jeongin, Oxygen Development/Eyesome and Hanform.
- Added large ODM technology references **Kolmar Korea** and **COSMAX** as technical-capability references, not assumed low-MOQ suppliers.
- Explicitly separated direct manufacturers from sourcing/matching platforms.
- Recorded negative evidence where a public MOQ is materially above the current 1,000–3,000 unit launch strategy.
- Added a standardized RFQ checklist covering 20 g stick filling, fine-powder dispersion, anhydrous/oil/wax/silicone systems, pilot production, stock packaging, development cost, 500/1,000/2,000/3,000/5,000-unit pricing and lead time.

### Decision
- The first RFQ wave will focus on technical feasibility, not advertised MOQ or headline unit price.
- Public claims remain **unverified until the manufacturer confirms them for GLIDE-SPEC 40**.
- The first production quantity remains open pending technical review, pilot samples and comparable quotations.

---

## [Manufacturer Sourcing Plan] - 2026-09-14
### Added
- Added `docs/MANUFACTURER_SOURCING_PLAN_REV1.md`.
- Established a manufacturer-screening funnel: **10–15 initial candidates → 5–7 RFQs → 3 technical candidates → 2–3 pilots → 1–2 final manufacturers**.
- Defined manufacturer-facing product brief around a **20 g solid stick anti-chafing product**, rather than treating “Powder-in-Balm Stick” as a standardized category.
- Standardized RFQ quantities at **500 (if pilot possible), 1,000, 2,000 and 3,000 units**.
- Added technical screening criteria for solid-stick filling, anhydrous/oil/wax/silicone systems, fine-powder dispersion, pilot capability and stock 18–20 g packaging.
- Added a 100-point manufacturer scorecard with technical feasibility weighted above price.
- Added evidence discipline: public MOQ/product claims must be separated from direct manufacturer confirmation and pilot/quotation results.
- Added an initial candidate set including Laonhase, Heib Lab, Ladyhouse, COSMEDIQUE, The One Cosmetic, Korea Cosmetic Manufacturing, Hanform, BouncyLab, HWAJAE and Selfcos, with explicit distinction between direct manufacturers and sourcing/matching platforms.
- Recorded higher-MOQ stick examples as negative evidence against assuming universal 1,000-unit stick production.

### Decision
- Manufacturer selection will **not** be based on advertised MOQ alone.
- Final first-production quantity remains open until technical feasibility, pilot behavior and comparable quotations are obtained.

---

## [Product/Manufacturing Clarification] - 2026-09-14
### Changed
- Added `docs/PRODUCT_FORM_FACTOR_AND_MANUFACTURING_ASSUMPTIONS_REV1.md` to clarify the physical product definition and manufacturing assumptions.
- **“Powder-in-Balm Stick” is no longer treated as a confirmed commercial category name.** It is retained only as a shorthand for the intended balm-to-powder-like physical behavior.
- Adopted **20 g solid stick-format skin anti-chafing product** as the clearer product-form description.
- Identified NUDESTIX Blot & Blur Matte Primer Stick as a **formulation/texture reference only** because its balm-to-powder stick behavior is useful as a market analogue; it is not a GLIDE-SPEC 40 competitor or equivalent product.
- Manufacturer-facing description now emphasizes a wax/oil/silicone solid matrix with dispersed fine particulate materials, smooth application, relatively dry/powdery surface film, reduced friction and controlled transfer.
- Removed the assumption that **3,000 units is the minimum production quantity**.
- Initial production planning is now **approximately 1,000–3,000 units**, subject to manufacturer MOQ, formulation feasibility, stock-package availability and actual quotations. Smaller technical/pilot quantities may be evaluated separately.
- **2,950 KRW/unit remains a target COGS only**, not a verified manufacturing cost.
- Dedicated package tooling is not locked; **stock 18–20 g stick packaging is the first-choice path**.
- Manufacturer screening is now focused on solid stick filling, anhydrous/oil-phase balm/stick systems, balm-to-powder/matte stick experience, fine-powder dispersion and pilot filling capability.

### Rationale
- Publicly available small-batch manufacturing examples show that MOQ varies materially by manufacturer, formulation and package; therefore a fixed 3,000-unit minimum is not sufficiently supported.
- GLIDE-SPEC 40's specific powder-loaded stick formulation must be validated directly with manufacturers before MOQ, production cost or final manufacturing terminology is fixed.

---

## [Rev.8.1] - 2026-09-13 (Commit `5749cc0` / Tag `Rev8.1-precalibration`)
### Added
- **Dataset Freeze 1 & Independent Sample Audit (`data/DATASET_FREEZE_1.csv`, `docs/DATASET_INDEPENDENT_SAMPLE_AUDIT.md`):**
  - Audited 8 public peer-reviewed datasets isolating raw longitudinal/thermal rows from independent formulation clusters.
  - Clarified that 384 data points in Huynh (2020) correspond to repeated aging/thermal sweeps, mathematically justifying `GroupKFold`.
  - Preserved the historical Rev.8.1 engineering record below unchanged for traceability.

# GLIDE-SPEC 40: System Changelog

All notable changes to the GLIDE-SPEC 40 simulation, modeling, and active learning engines are documented herein.

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
  - ...

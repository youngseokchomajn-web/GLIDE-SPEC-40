# GLIDE-SPEC 40 — Rev.7.4-alpha Change Log

## Baseline

- Product baseline: Rev.7.3
- Git baseline: `be39b42`

## Changes

### ADD

- `CompositeMaterial`, `CompositeComponent`, and explicit `RatioType` in the Material Master.
- DOE → resolved raw-material charges → COGS integration coverage.
- Full QC SOP SQLite round-trip coverage and `is_sop_complete()` gate.

### MODIFY

- Manufacturing calculation resolves composite membership from the Material Master; calculator code no longer owns blend definitions.
- A Dimethicone carrier introduced by MQ resin offsets the resolved Dimethicone charge while retaining raw-material traceability.

### BUGFIX

- QC persistence now stores and restores complete Hardness and Transfer SOP objects instead of only one field from each.

### TEST

- `python3 -m unittest discover tests` passes (9 tests).

## Scope boundary

This alpha does not promote the model to `TRAINED_LINEAR`, generate production predictions, or alter the locked Rev.7.3 target-active formula.

# Brand Research Audit — v0.1

Date: 2026-09-13

## Purpose

Check whether the current brand-planning evidence chain is missing a material category before moving from research into product-definition decisions.

## Current coverage

| Area | Status | Note |
|---|---|---|
| Brand origin | Covered | Runner + Vaseline observation preserved as origin hypothesis |
| Positioning | Covered | Performance/endurance skin direction; not finalized |
| Target beachhead | Covered | Marathon / ultra runners as working beachhead |
| Runner journey | Covered | Preparation → running → late-stage → finish/recovery |
| Market/competitor landscape | Covered | Multiple incumbent anti-chafe solutions recognized |
| Community evidence schema | Covered | Context-preserving registry exists |
| Individual community evidence | Added v0.1 | 10 cases entered in community_cases_v0.1.md |
| Contradictory reports | Added | Persistence and reapplication conflicts intentionally preserved |
| Body-area differences | Added | Nipples, inner thighs, groin, armpits, sports-bra/equipment interface |
| Weather/environment | Added | Heat, sweat, wet conditions, cold, humid/wet regional context where reported |
| Clothing/equipment interaction | Added | Garment fit, hydration vest, sports bra, shirt movement |
| Reapplication behavior | Added | Explicitly captured where reported; contradictory intervals retained |
| Application format | Added | Stick/balm, wipes, roll-on, tape/band-aid alternatives |
| Residue/clothing transfer | Added | Staining/greasy tradeoff captured |
| Price/value | Partial | Some community signals exist, but not enough structured cases yet |
| Gender/anatomy segmentation | Partial | Male-specific and sports-bra/nipple cases present; broader sex/body/anatomy segmentation still needed |
| Climate segmentation | Partial | Heat/wet/cold signals present; dry/cold/hot-humid matrix not yet balanced |
| Distance/time segmentation | Partial | 14.5 mi, 15 mi, 24 mi, 50K, marathon/ultra context; controlled time-to-failure still absent |
| Recovery/post-run | Missing | Community evidence currently focuses mainly on prevention/protection |
| Skin compatibility/adverse reactions | Missing | Needs dedicated evidence pass; do not infer from “works/doesn't work” |
| Sensory UX | Partial | Greasy/dry/brittle/smell signals present; texture, spreadability, cleanup need more evidence |
| Packaging/carryability | Partial | Wipes/roll-on/carrying small container mentioned; broader pack/aid-station workflow missing |
| Regulatory/claim boundary | Covered as constraint | Community reports are not treated as regulatory evidence |
| Controlled performance standards | Missing by design | Must be established through technical/R&D work, not community anecdotes |

## Important missing research passes

### 1. Body-area matrix

Need balanced cases for:
- inner thigh
- groin
- buttocks/gluteal cleft
- nipples
- underarms
- sports-bra contact
- waistband/pack contact
- feet/toes/shoe interface

For each, record the same fields and identify whether formulation, clothing, tape, or equipment is the dominant intervention.

### 2. Condition matrix

Build evidence across:
- dry/cool
- hot/dry
- hot/humid
- rain/wet
- cold
- sweat-heavy indoor/treadmill if relevant

Do not infer missing cells from adjacent conditions.

### 3. Distance/time matrix

Separate:
- 5–10K
- half marathon
- marathon
- 50K
- 100K+

Capture time-to-first-symptom and time-to-failure whenever users report it.

### 4. User-behavior matrix

Capture:
- initial application amount
- application timing before start
- reapplication timing
- whether product is carried
- aid-station/drop-bag behavior
- whether user changes clothing or tape instead of product
- why they stay with an imperfect incumbent

### 5. Failure taxonomy

Do not use “doesn't work” as a single label. Classify failure as:
- friction breakthrough
- product migration
- sweat dilution/wash-off
- water exposure
- heat softening/melting
- cold hardening/brittleness
- residue/grease
- clothing staining/transfer
- odor/sensory issue
- application difficulty
- reapplication difficulty
- skin irritation/compatibility
- equipment/garment interaction

### 6. Recovery evidence

The current brand architecture includes PROTECT → PERFORM → RECOVER → OPTIMIZE, but the community evidence collected so far is overwhelmingly about protection. Recovery should be researched separately rather than assumed from the protection problem.

## Decision integrity check

The following conclusions remain valid as working hypotheses, but none should be upgraded to product claims solely from community evidence:

- Do not position the brand simply as “sports Vaseline.”
- Endurance runners remain a useful beachhead because duration, repetitive motion, sweat/moisture and equipment interactions create observable skin-use scenarios.
- TIME × MOTION × ENVIRONMENT is a useful abstraction, but clothing/equipment and body area must remain explicit sub-variables.
- The opportunity may be a scenario-based skin system rather than another generic anti-chafe product, but this requires validation.
- Duration superiority is not established; persistence must be tested comparatively.

## Gate before product lock

Before locking the first-product specification, require:

1. More individual community cases, especially missing body-area/condition cells.
2. Structured user interviews or survey work to estimate prevalence and willingness-to-pay.
3. Controlled technical tests translating recurring failure modes into measurable requirements.
4. Competitive product testing under matched conditions.
5. Clear separation between user-reported benefit, measured performance, and regulatory claim language.
6. Explicit linkage from each major product requirement back to evidence IDs and/or controlled test results.

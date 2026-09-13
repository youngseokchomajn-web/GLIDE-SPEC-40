# Technical Validation Matrix — v0.1

Date: 2026-09-13

## Purpose

Translate recurring community/user failure modes into measurable technical questions before formula, format, numerical thresholds, or first-product SKU are locked.

This document defines the test architecture. It does not establish any performance claim or final acceptance threshold.

## Core system model

The test unit is not the cosmetic alone. The working system is:

`skin × product × garment × equipment × motion × sweat/water × time`

Primary controlled variables should include:

- body-area/interface type
- application amount per unit area
- garment/textile or equipment material
- moisture condition
- temperature
- mechanical motion/load
- elapsed time
- reapplication condition

## Failure-mode → measurement map

| Failure mode | Technical question | Candidate measurement | Main controlled variables |
|---|---|---|---|
| friction breakthrough | Does protection reduce skin/interface friction under repeated motion? | friction/tribology metric | load, speed, textile, moisture, temperature, cycles |
| time-dependent loss | How does protection change with repeated motion/time? | friction + film/presence proxy over time | same as above + elapsed time |
| sweat dilution/wash-off | Does simulated sweat reduce protective function? | pre/post moisture exposure performance | sweat composition/volume, temperature, exposure time |
| water exposure | Does rain/water contact change performance? | pre/post water exposure friction/persistence | water volume, exposure, drying condition |
| heat softening/migration | Does heat alter placement or protection? | migration/flow + friction | temperature, orientation, motion |
| cold hardening | Does cold reduce spread/application consistency? | application force/spread uniformity | temperature, format, storage conditioning |
| garment transfer/staining | Does product transfer excessively to textile? | transfer mass/visual grading | textile, amount, pressure, motion, time |
| residue/sensory burden | Does protection create unacceptable residue or wet/greasy feel? | standardized sensory panel/structured scoring | amount, textile, time, wash/cleanup condition |
| application/reapplication | Can the intended user apply/reapply reliably? | task success, time, amount variance, mess score | body site, format, gloves/wet hands, visibility |
| reachability | Can users reach critical sites during realistic use? | successful coverage rate/time | body site, posture, format |
| skin compatibility | Does repeated topical exposure create unacceptable irritation signals? | qualified compatibility/patch testing | intended population, exposure protocol |
| equipment interaction | Does pack/bra/waistband motion alter protection? | localized friction/persistence | equipment fit, motion, moisture, time |

## Required benchmark set

At minimum, compare:

1. petroleum jelly / petrolatum benchmark
2. at least one leading specialized anti-chafe stick
3. at least one specialized balm/ointment format
4. candidate GLIDE-SPEC formulation(s)

Do not select a benchmark because it is assumed to be inferior. Benchmark selection should reflect actual incumbent use in the target scenario.

## Condition matrix

### Time

Use staged measurements rather than assuming a universal duration claim. Candidate observation points may include:

- baseline / immediately after application
- early-use
- mid-use
- late-use
- post-moisture exposure
- post-reapplication

Exact timepoints and thresholds must be established during method development.

### Temperature / moisture

At minimum, method development should consider:

- cool/dry
- warm/dry
- warm/humid/sweat
- wet/rain exposure

Cold-state application should be tested separately where the chosen format is plausibly temperature-sensitive.

### Interface

Prioritize interfaces represented in user evidence:

- skin-to-skin / inner thigh
- skin-to-waistband/groin garment
- skin-to-sports-bra/under-bra
- skin-to-hydration-vest/pack
- skin-to-seam/textile edge
- other high-friction sites identified by Korean survey data

## Test hierarchy

### Level 1 — Bench method development

Goal: establish repeatable measurement methods and variance.

Outputs:
- method definition
- equipment/setup
- sample conditioning
- application protocol
- replicate count
- measurement uncertainty

### Level 2 — Matched incumbent comparison

Goal: determine whether candidate formulations produce reproducible differences under the same conditions.

Outputs:
- raw measurements
- mean/dispersion
- failure curves where appropriate
- operator notes
- blind/randomized sample coding where feasible

### Level 3 — Application/UX validation

Goal: determine whether technical performance survives realistic application and reapplication behavior.

Outputs:
- successful coverage
- application time
- amount variability
- reachability
- reapplication burden
- transfer/cleanup observations

### Level 4 — Field validation

Goal: test whether controlled findings remain relevant in actual running scenarios.

Field testing should be hypothesis-confirmatory, not used to replace controlled comparison.

## Acceptance-threshold rule

Do not invent numerical thresholds before baseline variance and incumbent performance are known.

A requirement becomes eligible for numerical specification only after:

1. failure scenario is supported by user evidence;
2. measurement method is repeatable;
3. incumbent baseline is measured;
4. candidate performance distribution is available;
5. the threshold has a documented decision rationale.

## Evidence linkage

Every final product requirement should point to one or more of:

- community evidence ID
- Korean survey finding ID
- controlled technical test ID
- skin compatibility result
- regulatory/claim substantiation source

No requirement should enter the final product specification solely because it is conventional, fashionable, or preferred by the development team.

## Explicit non-claims

This matrix does not yet establish:

- a specific formulation
- a specific ingredient as superior
- exact hours of protection
- medical prevention or treatment
- universal superiority over incumbents
- final packaging or format
- final launch price

Those decisions remain gated by evidence and testing.

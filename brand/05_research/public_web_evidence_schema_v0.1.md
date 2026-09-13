# Public Web Evidence Schema v0.1

## Purpose

Create a repeatable structure for scaling public-web runner evidence without turning anecdotal reports into unsupported quantitative claims.

## Required fields

- `Evidence ID`: stable identifier such as PW7-016
- `Source type`: Reddit / forum / review / blog / retailer / other
- `Source`: exact page reference
- `Publication date`: when available
- `Context`: runner/event/environment context
- `Distance`: exact or approximate, if reported
- `Duration`: exact or approximate, if reported
- `Body area`: anatomical interface
- `Interface`: skin-skin / skin-garment / skin-equipment / mixed
- `Motion`: repetitive running / static pressure / equipment movement / unknown
- `Temperature`: if reported
- `Humidity/water`: if reported
- `Sweat`: low / moderate / heavy / unknown, only when explicitly supported
- `Garment`: type, fit, seam, migration, material when available
- `Equipment`: vest/pack/strap/etc. when relevant
- `Product/solution`: exact product or solution class
- `Application`: timing, amount, location, reapplication if reported
- `Outcome`: success / failure / partial / conditional / unknown
- `Failure mode`: controlled vocabulary below
- `Switching`: prior solution → new solution, when available
- `Reason for switching`: persistence / feel / staining / application / fit / reachability / cost / other
- `Positive signal`
- `Negative signal`
- `Contradiction group`: identifier when another case reports the opposite outcome
- `Evidence boundary`: what the case cannot establish
- `Strategic implication`: hypothesis only

## Failure-mode vocabulary

- friction breakthrough
- migration
- sweat wash-off
- water/rain failure
- heat softening
- cold hardening
- residue/greasiness
- textile transfer/staining
- odor/sensory issue
- application difficulty
- reapplication difficulty
- reachability
- skin compatibility/irritation
- garment interaction
- equipment interaction
- adhesive failure
- unknown

## Outcome coding

Do not reduce all reports to binary success/failure.

Use:

- `success`: user explicitly reports satisfactory outcome in the described context
- `failure`: user explicitly reports unacceptable outcome
- `partial`: some sites/conditions work and others do not
- `conditional`: outcome is explicitly dependent on environment, duration, body area, garment, or application
- `unknown`: insufficient outcome information

## Contradiction handling

Contradictory cases must remain separate.

Example:

- Case A: Vaseline satisfactory for long run.
- Case B: Vaseline washes off during shorter hot run.

Do not average these into “Vaseline lasts X hours.” Instead record the conditions and create a contradiction group for later hypothesis testing.

## Deduplication rules

- Same source/page and same underlying event = one case.
- Multiple comments describing the same original event should not be counted as independent runner cases.
- A commenter describing their own separate experience may be a separate case.
- Reposts or syndicated copies should be linked to the earliest identifiable source where possible.

## Evidence hierarchy for interpretation

### Level A — controlled/observed measurement
Not created by community testimony. Reserved for later technical testing.

### Level B — structured human research
Survey/interview data collected under a defined protocol.

### Level C — public user report
Useful for failure discovery, hypothesis generation, and UX signals.

### Level D — commercial/marketing statement
Useful for competitor positioning only; never treated as independent efficacy evidence.

## Aggregation rules

Public-web cases may be aggregated for:

- failure-mode discovery
- solution switching patterns
- condition/body-area hypothesis generation
- competitor UX themes
- research-priority setting

Public-web cases must **not** alone be aggregated into claims of:

- market prevalence
- objective efficacy
- duration thresholds
- comparative superiority
- clinical benefit
- regulatory eligibility

## Research pipeline

`discover → verify source → extract case → code variables → preserve contradiction → cluster hypotheses → identify gaps → design controlled test/survey`

## Quality-control checklist

Before adding a case:

1. Is this a distinct underlying experience?
2. Is the source traceable?
3. Are reported facts separated from interpretation?
4. Are missing variables marked unknown rather than guessed?
5. Is the exact product/solution distinguished from the category?
6. Is the context preserved?
7. Is any contradiction retained?
8. Is the evidence boundary explicit?
9. Is the strategic implication phrased as a hypothesis rather than a fact?

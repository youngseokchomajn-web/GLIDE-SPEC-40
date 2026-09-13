# GLIDE-SPEC 40 Technical Test Protocol — v0.1

Date: 2026-09-13
Status: Method-development draft; not a product specification

## 1. Purpose

Convert the READY_FOR_TEST cells in the public-web saturation matrix and technical validation matrix into a reproducible first test program.

The immediate objective is **not** to prove that GLIDE-SPEC is superior. It is to establish a repeatable measurement method, measure real incumbent baselines, and identify which failure contexts produce meaningful differences between candidates.

The working test unit is:

`skin surrogate / interface × product × garment/equipment × motion × sweat/water × temperature × time`

## 2. Evidence basis

Public and scientific literature supports treating skin–textile friction as a measurable tribological interaction and shows that moisture, skin condition, textile properties, load, speed, anatomical site and contact conditions can change measured friction. Repeatable surrogate-skin/textile friction testing has also been demonstrated in laboratory work. These sources support the **method architecture**, not a numerical performance target or a claim for any product.

Key references:

- Temel, Lloyd & Johnson (2021), *Tribology Letters*, “Evaluating the Design and Repeatability of a Novel Device to Measure Friction of Mechanical Surrogate Skins in Contact with Cotton Textiles.” DOI: 10.1007/s11249-021-01502-1.
- MacFarlane et al. (2021), *Biosurface and Biotribology*, “Skin tribology in sport.” DOI: 10.1049/bsb2.12015.
- Gerhardt et al. (2007), *Wear*, “Tribology of human skin and mechanical skin equivalents in contact with textiles.” DOI: 10.1016/j.wear.2006.11.031.

The literature indicates that friction measurement should control moisture, contact conditions and material pairing rather than treating “friction” as a single universal number.

## 3. Benchmark set

Use the same coded, blinded sample IDs across the first matched comparison.

Minimum benchmark set:

1. Petrolatum / petroleum jelly benchmark.
2. One leading anti-chafe stick.
3. One specialized balm/ointment benchmark.
4. GLIDE-SPEC candidate formulation(s), once testable prototypes exist.

Benchmark products should be selected because they are actually used in the target scenarios, not because they are presumed weak or strong.

Record for every benchmark:

- commercial product name and variant
- batch/lot where available
- purchase date/source
- package size
- stated ingredients/format
- storage condition
- sample preparation
- any manufacturer application guidance used

## 4. Test program overview

### T1 — Friction / tribology method development

Question:

> Under controlled repeated motion, how does each product alter interface friction compared with the untreated control?

Primary output:

- static friction metric where measurable
- dynamic friction metric
- variability across repeated measurements
- effect of moisture condition
- effect of repeated cycles

Do not convert the result directly into “hours of protection.”

### T2 — Persistence under sweat/water exposure

Question:

> How does measured protection change after controlled moisture exposure and repeated motion?

Conditions to develop:

- dry baseline
- simulated sweat exposure
- higher-moisture/wet condition
- water exposure followed by controlled motion

Outputs:

- pre-exposure measurement
- post-exposure measurement
- relative change from baseline
- visible migration/film loss notes

Exact sweat composition, volume, temperature and exposure duration must be fixed during method development and then held constant for comparison.

### T3 — Garment/system interaction

Question:

> Does the candidate remain functional when paired with representative textiles and realistic garment motion?

Priority interfaces:

- inner-thigh / skin-to-skin plus adjacent garment
- groin/waistband
- sports-bra / under-bra textile
- seam/edge interface
- hydration-vest/pack contact textile

Outputs:

- friction/persistence change by textile
- migration/coverage change
- transfer to textile
- qualitative surface condition

The product is evaluated as part of the interface system, not as a free-standing balm.

### T4 — Reapplication / application UX

Question:

> Can the intended user apply and reapply the product consistently at realistic sites and conditions?

Measure:

- task completion rate
- application time
- amount used
- coverage consistency
- reapplication time
- hand contamination/mess score
- reachability
- wet/sweaty-hand usability
- visibility/precision where relevant

This is a separate validation layer from laboratory friction performance.

### T5 — Transfer / staining

Question:

> How much material transfers from treated interface to representative textile under pressure and repeated motion?

Measure:

- textile mass change where feasible
- standardized visual grading
- transfer area
- qualitative residue description

Use identical textile type, pressure, motion and elapsed time when comparing products.

### T6 — Heat / temperature conditioning

Question:

> Does temperature change application consistency, migration, or measured protection?

At minimum consider:

- cool/dry
- room/reference
- warm/dry
- warm/humid

Cold-state testing is added if the chosen prototype format is plausibly temperature-sensitive.

Temperature values must be selected from realistic target-use conditions during method development; they are not product requirements at this stage.

## 5. First method-development matrix

| Variable | Initial levels | Purpose |
|---|---|---|
| Product | untreated + benchmark set + candidate | comparator structure |
| Interface | surrogate skin + representative textile | system realism |
| Moisture | dry / sweat-conditioned / wet | wash-off and friction effects |
| Motion | controlled reciprocating motion | repeatability |
| Time | staged cycles rather than claimed hours | persistence trajectory |
| Temperature | reference / warm; cold if format-sensitive | rheology/migration |
| Textile | at least 2 representative constructions | garment dependency |
| Replicate | determine during pilot from variance | statistical reliability |

The pilot must establish measurement variance before any acceptance threshold is proposed.

## 6. Sample preparation rules

Before testing:

1. Randomize/counterbalance product order where feasible.
2. Condition all products and textiles to the same documented environment.
3. Use a defined application mass or mass-per-area.
4. Record application operator and method.
5. Record application-to-test waiting time.
6. Use fresh or explicitly conditioned textile samples according to the method.
7. Clean/prepare surrogate surfaces using one fixed protocol.
8. Record deviations immediately rather than correcting them retrospectively.

## 7. Data capture

Every run should retain raw data, not only averages.

Minimum record:

- Test ID
- Date/time
- Operator
- Product code
- Product batch/lot
- Interface/body-area proxy
- Textile/equipment code
- Application mass
- Application area
- Moisture condition
- Temperature/humidity
- Motion/load/speed settings
- Conditioning time
- Cycle/time point
- Raw measurement
- Replicate number
- Visible migration/transfer notes
- Equipment/calibration status
- Deviations

## 8. Analysis rules

### 8.1 Do not pool unlike interfaces

Do not average inner-thigh, sports-bra, waistband and hydration-vest results into one universal product score if the underlying mechanisms differ.

### 8.2 Do not infer field duration directly

A laboratory time/cycle curve is evidence about the tested condition. It is not automatically an “X-hour protection” claim.

### 8.3 Preserve contradictions

If petrolatum performs well in one condition and poorly in another, retain both results and identify the condition that separates them.

### 8.4 Separate product effects from system effects

A failed condition may originate from:

- product film loss
- textile migration
- garment movement
- equipment pressure
- excessive moisture
- application error
- anatomical/interface geometry

The test report must identify the most plausible failure mechanism without overstating causality.

### 8.5 Thresholds come last

No pass/fail threshold is established in v0.1.

A numerical product requirement can only be proposed after:

1. repeatability is demonstrated;
2. incumbent variance is known;
3. the failure scenario has user/evidence support;
4. candidate distributions are available;
5. the decision rationale is documented.

## 9. Pilot sequence

### Phase A — T1 pilot

Start with one representative textile and one surrogate-skin/interface condition.

Goals:

- establish repeatability
- determine useful load/speed/cycle range
- identify measurement floor/ceiling
- estimate replicate count
- identify operator-sensitive steps

### Phase B — T1 matched incumbent baseline

Run untreated control + petrolatum + specialized stick + specialized balm.

Do not include candidate formulation until the method is stable enough to distinguish known incumbent samples reproducibly.

### Phase C — T2 moisture challenge

Use the selected T1 configuration and add controlled sweat/water exposure.

### Phase D — T3 system interfaces

Expand only after the base method is stable:

1. inner-thigh/garment
2. waistband/groin
3. sports-bra/under-bra
4. seam/edge
5. hydration-vest/pack

### Phase E — T4/T5 UX and transfer

Run in parallel with prototype-format development rather than waiting for a final formula.

## 10. Decision gates

### Gate T0 — Method ready

Pass when:

- protocol is executable by another operator;
- sample conditioning is documented;
- repeatability is characterized;
- raw data are retained;
- major sources of variance are known.

### Gate T1 — Incumbent baseline ready

Pass when:

- all minimum benchmarks have been measured under the same conditions;
- between-product differences can be distinguished from method noise;
- no benchmark is excluded because of an assumed ranking.

### Gate T2 — Candidate comparison ready

Pass when:

- candidate prototypes are stable enough for matched testing;
- application mass/area is defined;
- candidate and benchmark results are directly comparable.

### Gate T3 — Scenario validation ready

Pass when:

- the candidate is tested in at least one evidence-supported failure scenario;
- garment/equipment interaction is represented where relevant;
- technical findings can be linked back to evidence IDs.

## 11. Explicit non-claims

This protocol does not establish:

- medical prevention or treatment
- universal anti-chafe efficacy
- exact duration of protection
- superiority over petrolatum or any named competitor
- suitability for every anatomical site
- final formula
- final format
- final price
- regulatory claim eligibility

Those require separate evidence and decision gates.

## 12. Immediate next action

Do **not** start with a large human field trial.

First execute the method-development sequence:

`T1 friction pilot → incumbent baseline → T2 sweat/water challenge → T3 system interfaces → T4/T5 UX & transfer`

The first deliverable should be a repeatable incumbent baseline dataset. Only then should numerical product requirements be considered.

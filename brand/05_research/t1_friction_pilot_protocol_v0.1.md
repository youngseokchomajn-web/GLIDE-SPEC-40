# GLIDE-SPEC 40 T1 Friction Pilot Protocol — v0.1

Date: 2026-09-13  
Status: Method-development pilot; not a product specification

## 1. Purpose

T1 is the first controlled bench experiment in the GLIDE-SPEC 40 technical validation program.

The purpose is to determine whether a skin-surrogate/textile reciprocating-friction method can:

1. produce repeatable measurements;
2. distinguish untreated interface from incumbent anti-chafe products;
3. detect changes caused by moisture and repeated motion;
4. provide a stable method for later candidate-formulation comparison.

T1 is **not** intended to establish clinical efficacy, exact protection duration, universal superiority, or a final product requirement.

## 2. Why this method architecture

Skin–textile friction is a measurable tribological interaction. Published work has demonstrated repeatable static and dynamic friction measurements using surrogate skin and linearly moving textile interfaces. One 2021 study reported excellent repeatability for static and dynamic friction measurements and showed that the surrogate material itself materially affects the measured coefficient of friction. A 2022 follow-up also found repeatable measurements across human body regions and significant regional differences. These findings support controlled surrogate/interface testing, while also requiring GLIDE-SPEC to avoid treating one friction number as universal across all body areas. citeturn0search0turn0search3

Moisture must be treated as an explicit factor. Human skin hydration has been associated with increased skin–textile friction, and completely wet fabric conditions can produce substantially higher friction than dry textile conditions. citeturn0search10

Therefore the T1 pilot deliberately separates:

`product × interface × textile × moisture × motion × time/cycles`

rather than testing product performance in a single dry condition.

## 3. Primary endpoints

### 3.1 Primary

- Dynamic coefficient of friction (dynamic COF), where the apparatus supports a valid calculation.
- Static coefficient of friction (static COF), where the apparatus supports a valid calculation.
- Within-condition measurement variability.
- Change in friction across repeated motion/cycles.

### 3.2 Secondary

- Pre/post moisture-condition change.
- Visible film loss, migration, pooling, or transfer.
- Textile surface change.
- Operator/application variability.

The primary decision is whether the method is sufficiently repeatable and discriminating to proceed to matched incumbent testing.

## 4. Test architecture

### 4.1 Interface

Start with **one surrogate-skin material** and one controlled textile interface.

Do not assume that any commercial surrogate material reproduces human skin. The chosen material must be documented by supplier/specification and retained as a fixed method component once selected.

A second surrogate material may be added later if the first material produces floor/ceiling effects or unrealistic ranking behaviour.

### 4.2 Textile

T1 starts with one representative textile construction to minimize variance while the method is being stabilized.

The textile must be:

- reproducibly cut to a fixed specimen size;
- from the same material lot for a pilot batch where possible;
- washed/conditioned by one documented procedure if preconditioning is required;
- mounted using a fixed attachment method that prevents uncontrolled wrinkling or slippage.

After T1 method stabilization, representative textiles should be added for evidence-supported interfaces such as inner thigh, waistband, sports-bra/under-bra and hydration-vest/pack contact.

### 4.3 Product conditions

Initial pilot conditions:

1. untreated control;
2. petrolatum benchmark;
3. specialized anti-chafe stick benchmark;
4. specialized balm/ointment benchmark.

Candidate GLIDE-SPEC formulations are excluded from the first method-stability run. They enter only after the method can reproducibly distinguish incumbent samples from untreated control.

All products are coded before measurement where feasible so the operator does not know product identity during the measurement run.

## 5. Application normalization

Product application is normalized by **mass per unit area (mg/cm²)** rather than by an informal swipe count.

The exact application loading is a pilot variable and must be empirically selected. It must not be copied from a commercial product's marketing language or treated as a final consumer dosage.

For each condition record:

- application mass before/after application;
- application area;
- calculated mass/area;
- operator;
- application technique;
- application-to-test waiting time.

For stick products, record both mass loss and the defined application area. If direct mass measurement is impractical, document the validated alternative method before comparing products.

## 6. Motion variables

Use a **linear reciprocating motion** because this provides a controlled repeated interface rather than the changing contact velocity associated with uncontrolled rotational movement. Published surrogate-skin/textile work has successfully used linearly moving interfaces and adjustable normal load/velocity. citeturn0search0

The following are method-development variables, not product specifications:

- normal load;
- stroke length;
- reciprocating speed;
- cycle count;
- dwell/rest interval, if any.

Select initial levels from the capability and validated operating range of the available tribometer. Do not invent a universal running-equivalent load, speed, or cycle count.

For each selected setting record the instrument configuration exactly so that another operator can reproduce it.

## 7. Environmental conditions

The first pilot uses two moisture states:

### M0 — Dry/reference

- controlled ambient condition;
- documented temperature and relative humidity;
- no intentional moisture added to the interface immediately before measurement.

### M1 — Sweat-simulated/moist

- defined artificial sweat or saline formulation;
- defined application method;
- defined moisture loading;
- fixed conditioning interval before measurement.

A third **M2 — wet/water-exposed** condition should be added after M0/M1 repeatability is established.

The exact sweat composition, volume, temperature, humidity and conditioning time are method-development parameters. They must be fixed before comparative product testing and then held constant.

The rationale for separating dry and moist states is supported by skin–textile friction literature showing strong dependence of friction on hydration/moisture. citeturn0search10turn0search9

## 8. Pilot sequence

### Phase 1 — Untreated control repeatability

Run the untreated interface repeatedly before introducing products.

Objectives:

- identify instrument noise;
- identify specimen-to-specimen variation;
- identify drift over a run;
- determine whether the selected interface has sufficient measurement range.

### Phase 2 — Benchmark discrimination

Run:

`untreated → petrolatum → specialized stick → specialized balm`

Use randomized/counterbalanced order where practical.

The question is not which product wins. The question is whether the method can detect reproducible differences without method noise overwhelming the signal.

### Phase 3 — Repeated-motion trajectory

For each selected product/condition, retain measurements at staged cycle points.

Do not translate cycle count into hours of protection.

The output is a **friction trajectory under the tested laboratory condition**.

### Phase 4 — Moisture challenge

Repeat the stable configuration under M1 sweat-simulated moisture.

Compare:

- untreated M0 vs untreated M1;
- each benchmark M0 vs its M1 condition;
- ranking changes, if any;
- variance changes.

If M1 creates uncontrolled specimen pooling or run-to-run instability, stop and redesign the moisture application method before product ranking.

## 9. Replicate structure

The pilot should contain three variance layers:

1. repeated measurements within a specimen/run;
2. independent specimens within a test day;
3. repeat testing on a separate day.

The final replicate count is determined from observed variance and the ability to distinguish incumbent differences, rather than from an arbitrary fixed N.

A practical pilot may begin with multiple repeated measurements per condition and then expand between-day replication after the operating window is identified.

The exact N is therefore a **method-development output**.

## 10. Randomization and blinding

Where practical:

- assign anonymous product codes;
- randomize product order;
- randomize specimen order;
- keep the operator blind to product identity during measurement;
- keep analysis files linked to the code key separately until the primary calculations are complete.

Record any unavoidable unblinding.

## 11. Instrument checks

Before each measurement block:

- verify instrument status/calibration according to manufacturer or laboratory SOP;
- verify load and motion settings;
- inspect textile mounting;
- inspect surrogate surface condition;
- verify data acquisition;
- record environmental conditions.

If calibration status or specimen condition is outside the predefined operating window, mark the run as a deviation rather than silently replacing the data.

## 12. Raw data capture

Each measurement record must retain:

| Field | Required |
|---|---|
| Test ID | Yes |
| Date/time | Yes |
| Operator | Yes |
| Blind product code | Yes |
| Actual product identity | analysis key only |
| Product lot/batch | Yes when available |
| Interface/surrogate code | Yes |
| Textile code/lot | Yes |
| Application mass | Yes |
| Application area | Yes |
| mg/cm² | Yes |
| Waiting/conditioning time | Yes |
| Moisture condition | Yes |
| Temperature/RH | Yes |
| Normal load | Yes |
| Stroke length | Yes |
| Speed | Yes |
| Cycle/time point | Yes |
| Raw force trace | Yes where instrument supports it |
| Static COF | If measurable |
| Dynamic COF | If measurable |
| Replicate ID | Yes |
| Visible migration/transfer | Yes |
| Deviation | Yes |
| Calibration status | Yes |

Do not retain only means and standard deviations. Raw traces and individual replicate values must remain available for audit.

## 13. Analysis plan

### 13.1 Repeatability

Estimate within-run, within-day and between-day variability.

Possible outputs include:

- coefficient of variation;
- relative pooled standard deviation;
- intraclass correlation where the experimental design supports it;
- variance components;
- control-chart style run monitoring where useful.

The literature demonstrates that high repeatability is achievable in controlled skin–textile friction measurement, including ICC values around 0.9 or higher in published systems. This is evidence that repeatability should be measured, not evidence that GLIDE-SPEC must adopt a specific ICC cutoff before pilot data exist. citeturn0search0turn0search3

### 13.2 Discrimination

Determine whether benchmark-vs-control differences are larger than method variability.

Do not rank products solely on a single mean COF.

Inspect:

- effect size relative to variance;
- overlap of replicate distributions;
- friction trajectory over cycles;
- moisture-induced changes;
- anomalous runs;
- visible film failure.

### 13.3 Static vs dynamic friction

Report static and dynamic friction separately when both are validly measurable. Published work shows that their relationship can depend on the interacting surface material, so they should not automatically be collapsed into one score. citeturn0search0

## 14. Method-readiness gates

### T1-P0 — Executability

Pass when another trained operator can reproduce the setup from the written protocol without relying on undocumented decisions.

### T1-P1 — Repeatability

Pass when within-run and between-day variance are characterized and are small enough to support comparative testing.

No universal numerical cutoff is imposed at v0.1; the acceptable variance must be justified against the expected incumbent effect size and intended decision use.

### T1-P2 — Discrimination

Pass when at least one known incumbent/control contrast can be detected consistently across independent replicates without being explained by measurement noise alone.

### T1-P3 — Moisture robustness

Pass when the dry and sweat-simulated methods remain executable and the moisture condition does not introduce uncontrolled variability.

### T1-P4 — Ready for candidate comparison

Pass when:

- the interface and textile are fixed;
- application loading is fixed;
- motion settings are fixed;
- moisture protocol is fixed;
- replicate structure is fixed;
- raw-data schema is locked;
- benchmark baseline is complete.

Only then should GLIDE-SPEC candidate formulations enter matched comparison.

## 15. Failure handling

Stop and redesign the method if any of the following occurs:

- untreated control drifts materially within a measurement block;
- textile slips or wrinkles unpredictably;
- surrogate surface is damaged or contaminated;
- moisture pooling causes uncontrolled hydrodynamic/slip behaviour;
- force signal saturates or reaches the instrument floor;
- product application cannot be normalized across formats;
- repeated measurements cannot distinguish benchmark signal from method noise.

A failed method is not a failed product. It is a method-development result and must be recorded as such.

## 16. Expected outputs

T1 should produce five concrete artifacts:

1. **T1 raw dataset** — individual force/friction measurements and metadata.
2. **T1 repeatability report** — variance by layer and identified sources of variation.
3. **Incumbent baseline table** — untreated, petrolatum, specialized stick, specialized balm.
4. **Moisture sensitivity report** — dry vs sweat-simulated changes.
5. **Method decision memo** — continue, modify, or stop, with reasons.

## 17. Decision linkage to GLIDE-SPEC 40

Each T1 finding should be linked to:

- technical validation matrix failure mode;
- public-web evidence ID(s);
- later Korean survey finding ID, if applicable;
- candidate formulation/prototype ID once prototypes exist;
- downstream T2/T3 test decision.

Example linkage structure:

`P8-03 reapplication / time-dependent failure → T1 cycle trajectory → T2 moisture challenge → T3 representative garment interface`

This prevents a laboratory measurement from becoming an isolated number with no connection to the original user problem.

## 18. Explicit non-claims

T1 does not establish:

- medical prevention or treatment;
- exact hours of anti-chafe protection;
- superiority over petrolatum or named competitors;
- universal suitability across anatomy, climate or sport;
- clinical efficacy;
- final formula or ingredient choice;
- final product format;
- final consumer dosage;
- final price;
- regulatory claim eligibility.

## 19. Next step after T1

If T1-P4 is passed:

`T1 stable method → complete incumbent baseline → T2 sweat/water persistence → T3 representative system interfaces`

If T1-P1 or T1-P2 fails:

`diagnose variance → modify method → repeat pilot`

Do not proceed to candidate-formulation optimization merely because a first measurement was obtained.

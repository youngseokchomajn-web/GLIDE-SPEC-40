# ORC-024 — DIY Friction Test Rig Decision Log

Date: 2026-09-19
Repository: youngseokchomajn-web/GLIDE-SPEC-40
Status: DECISION LOG / V1 HARDWARE DESIGN FREEZE (except NF302 mounting dimensions)

## 1. Why this work started

GLIDE-SPEC 40 is a physical 20 g Powder-in-Balm technical anti-chafing stick intended for actual sale. The simulator/software is supporting development infrastructure, not the product itself.

A physical friction test is needed to:
- benchmark existing anti-chafing references before interpreting GLIDE-SPEC 40 performance;
- identify concrete failure modes of reference products under controlled conditions;
- create repeatable internal data that can later be connected to formulation development;
- avoid relying only on subjective feel or community reviews.

Reference products selected:
- Squirrel's Saddle Butter 48 g — purchased for KRW 26,180 including shipping;
- BodyGlide 42.5 g — purchased for KRW 27,710 including KRW 5,000 shipping; delivery expected 2026-10-02.

These purchases are for engineering benchmarking, not resale.

## 2. Failure modes to test

Prior community/review research was used to define the minimum useful engineering questions.

Priority failure modes:
1. friction reduction that deteriorates during prolonged/repeated rubbing;
2. performance degradation under sweat/moisture/heat-like conditions;
3. need for frequent reapplication;
4. product migration/transfer or residue on contacting clothing/equipment;
5. secondary observations such as feel/odor are recorded but are not the primary V1 engineering metric.

The rig therefore needs to capture both initial friction and change with repeated/wet exposure.

## 3. Measurement principle selected

A horizontal sled is pulled at controlled speed over a fixed test surface.

Measured force:
- initial peak force = static friction force, Fmax;
- stable moving force = kinetic friction force, Favg.

Calculated:
- μs = Fmax / N
- μk = Favg / N

One horizontal sled system therefore measures both static and kinetic friction. A separate incline-plane apparatus is unnecessary for V1.

The method is described internally as an “ASTM D1894-style/internal comparative method.” It must NOT be described as ASTM-certified or as a skin-specific ASTM pass/fail test.

ASTM D1894 was used as a methodological reference because weighted sled, controlled speed, continuous force recording, and separation of static/kinetic friction are directly relevant. It is not a skin-specific standard.

## 4. Why a physical sled instead of a simpler test

Rejected/avoided:
- subjective hand-rub testing: too operator-dependent;
- spring scale alone: difficult to obtain clean static/kinetic traces and repeatability;
- incline-plane only: less convenient for continuous force recording and repeated-friction testing;
- motorized commercial tribometer: unnecessary cost and complexity at V1.

Selected:
- motorized horizontal sled + inline load cell.

Reason:
- directly measures the quantity needed;
- mechanically simple;
- supports repeated friction, wet conditions, and controlled speed;
- can be upgraded without replacing the basic architecture.

## 5. Skin-side surrogate decision

Candidate surfaces considered:
- real human skin;
- Dragon Skin 10;
- Dragon Skin 20;
- Dragon Skin 30;
- synthetic leather/other skin substitutes.

Real human skin was not selected for V1 because:
- site-to-site and person-to-person variability is high;
- moisture, pressure, speed, roughness and biological condition change the result;
- reproducibility and repeated testing are poor for a DIY benchmark;
- ethical/practical issues make it unsuitable as the primary engineering reference.

Dragon Skin was selected as a repeatable artificial skin-side surface.

Important limitation:
No Dragon Skin grade is claimed to be “human skin equivalent.” The goal is repeatability and controlled comparison.

### Dragon Skin grade decision

Dragon Skin 10:
- softer;
- literature shows useful skin-like tribological behavior in some contexts;
- retained as a future sensitivity condition.

Dragon Skin 20:
- moderate stiffness;
- Shore A 20;
- used as a skin substitute in recent surface-characterization literature;
- recent 2026 skin-surrogate tribology work used Dragon Skin at 3.5 mm with a sled test at 150 mm/min;
- selected as V1 standard/reference surface.

Dragon Skin 30:
- harder;
- useful as a future robustness/harder-counterface sensitivity condition;
- not necessary for V1.

Final V1:
**Dragon Skin 20, 3.5 mm.**

## 6. Why 3.5 mm

A recent 2026 skin-surrogate tribology study used Dragon Skin silicone elastomer cast to 3.5 mm and a sled-based test at 150 mm/min. This provides a useful literature anchor for a repeatable internal method.

3.5 mm is therefore a practical V1 thickness, not a claim that human skin has an equivalent 3.5 mm tribological layer.

## 7. Counterface/contact pad decision

The product film is placed on the Dragon Skin surface and the sled contacts it through a fixed counterface.

Candidate contactor sizes considered:
- 10 x 10 mm;
- 20 x 20 mm.

10 x 10 mm was initially considered because an anti-chafing patent friction test used a 10 x 10 mm contactor.

After review, 10 x 10 mm was NOT frozen for V1 because the smaller contact area can make local pressure, film thickness, squeeze-out and local surface effects dominate the measurement.

Selected:
**20 x 20 mm flat replaceable 316L stainless-steel pad.**

Reason:
- stable, hard, flat counterface;
- easy to manufacture and replace;
- larger controlled area;
- less sensitive to local defects than a very small contactor.

10 x 10 mm remains a possible later sensitivity comparison.

## 8. Product loading decision

An earlier 0.10 g proposal was rejected.

Literature/research found product application ranges in the approximate 1–6 mg/cm² region in anti-chafing contexts, an actual skin lubricant friction test using 120 mg over 15 cm² (~8 mg/cm²), and an anti-chafing friction patent using 1 g over 20 x 20 cm (~2.5 mg/cm²).

Because the methods are not identical, no single literature value was treated as a universal correct dose.

V1 nominal controlled-film loading:
**5 mg/cm².**

For the 20 x 20 mm contact area (4 cm²):
**20 mg product.**

Important:
20 mg / 4 cm² is a controlled laboratory loading for comparison, NOT a claimed consumer application dose.

Application must be uniform. A blob placed under the sled is not acceptable.

Conditioning:
**5 minutes** after application before measurement.

Later sensitivity:
- 2.5 mg/cm² = 10 mg;
- 5 mg/cm² = 20 mg;
- 8 mg/cm² = 32 mg.

V1 uses only 20 mg to avoid unnecessary variables.

## 9. Two-stage product application plan

TEST A — controlled film:
- 20 x 20 mm area;
- 20 mg;
- uniform application;
- fixed Dragon Skin 20;
- 200 g sled;
- 150 mm/min;
- dry first, wet later.

Purpose:
compare intrinsic friction behavior under controlled loading.

TEST B — real stick application:
- apply each commercial stick using controlled stroke count/pressure;
- weigh stick before and after;
- determine actual transferred mass per area.

Purpose:
separate formulation-level behavior from real stick-transfer/application behavior.

This distinction is important because a product may perform well as a uniform film but transfer poorly from the package, or vice versa.

## 10. Normal load and sled mass decision

Selected total sled mass:
**200 g.**

Normal force:
N ≈ 0.200 × 9.81 = 1.96 N.

Approximate friction forces:
- μ = 0.2 -> 0.39 N
- μ = 0.5 -> 0.98 N
- μ = 1 -> 1.96 N
- μ = 2 -> 3.92 N
- μ = 3 -> 5.89 N
- μ = 4 -> 7.85 N
- μ = 5 -> 9.81 N

This range makes a 10 N load cell appropriate for the expected measurement region.

A much larger-capacity 5 kg/10 kg load cell was rejected because its full-scale range is unnecessarily large for low-force friction measurements and can reduce useful resolution.

A 5 N load cell was not selected because it leaves too little margin if wet/high-friction conditions produce larger forces.

## 11. Load-cell decision

Selected first choice:
**Naturoll NF302, 10 N S-type tension/compression load cell.**

Officially reported family characteristics include:
- 10 N capacity available;
- rated output 2.0 ± 10% mV/V;
- stainless steel;
- IP65;
- 0.05% FS nonlinearity;
- 0.05% FS hysteresis;
- 0.05% FS repeatability;
- 350/650 ±5 ohm input/output impedance;
- recommended excitation 5–12 V;
- safe overload 150% FS;
- ultimate overload 200% FS.

Why selected:
- capacity is well matched to the 200 g sled;
- S-type/in-line geometry fits the motor → sensor → sled architecture;
- threaded axial installation is convenient;
- substantially less overkill than laboratory load cells.

Alternatives:
- Omega 10 N load cells exist but were judged economically excessive for V1;
- domestic 10 kg S-type cells are cheaper but have too-large a capacity;
- Naturoll NF301 10 N exists and is more miniature, but NF302 is the more natural fit for an inline threaded V1 assembly.

### Critical unresolved item

Do NOT invent the exact mounting dimensions or thread size for NF302 10 N.

Naturoll documentation states that NF302 uses M3/M4 depending on capacity, but the publicly exposed text does not establish the exact 10 N thread size. The manufacturer mounting drawing must be obtained before final bracket dimensions are frozen.

Therefore:
**NF302 10 N is selected, but its exact 10 N mounting drawing/thread specification remains an open procurement check.**

## 12. Mechanical architecture

V1 architecture:

NEMA17
  ↓
Ø20 mm constant-radius drum
  ↓
wire
  ↓
NF302 10 N
  ↓
short rigid axial connection
  ↓
200 g sled
  ↓
20 x 20 mm 316L flat pad
  ↓
product film
  ↓
Dragon Skin 20, 3.5 mm
  ↓
rigid base

Target base size:
approximately **400 x 150 mm** as a provisional envelope.

Final bracket dimensions must wait for the actual NF302 10 N drawing.

## 13. Rail decision

**No rail, LM guide, wheels, or rolling support under the sled in V1.**

Reason:
Any guide friction or constraint can contaminate the measured friction force.

The sled should slide directly on the fixed test surface.

A later non-contact side guide may be considered only if needed to prevent gross lateral drift, but it must not introduce meaningful friction or vertical force.

## 14. Pull-line alignment

The tow line must:
- remain horizontal;
- pass through/near the sled centerline;
- align with the NF302 measurement axis;
- avoid vertical force components;
- avoid side load, bending moment and torque on the load cell.

A pulley may be used only as a low-friction direction guide if geometry requires it, and its influence must not enter the measured axis.

The sled's center of mass and 20 x 20 mm contact pad should be positioned as close to vertically aligned as practical to minimize pitching/tilting.

## 15. Motor/drum decision

Motor:
**NEMA17 stepper.**

Drum:
**Ø20 mm, constant radius, single-layer winding.**

At 150 mm/min:
drum speed ≈ 150 / (π × 20) ≈ **2.39 rpm**.

Reason for fixed single-layer drum:
if the line winds in multiple layers, effective radius changes and the actual pulling speed changes.

V1 therefore uses a constant-radius single-layer arrangement.

## 16. Speed decision

Selected:
**150 mm/min.**

Reason:
- directly aligned with ASTM D1894-style testing;
- also matches the recent 2026 skin-surrogate sled literature reference;
- slow enough for stable force acquisition;
- fast enough for practical repeated tests.

Target stroke:
**100–150 mm.**

## 17. Electronics decision

V1 electronics:
- ESP32;
- HX711 ADC;
- NEMA17;
- stepper driver;
- suitable power supply;
- wiring/connectors.

HX711 is sufficient as a low-cost acquisition front end for V1, provided the assembled system is calibrated and noise-tested.

Do not treat the HX711 “24-bit” marketing figure as actual effective measurement resolution.

## 18. Calibration and error philosophy

The load-cell datasheet specifications do NOT equal total rig accuracy.

System-level uncertainty can be dominated by:
- HX711 noise;
- mechanical vibration;
- wire tension variation;
- motor stepping irregularity;
- sled wobble/pitch;
- Dragon Skin surface variation;
- product application variation;
- pad flatness;
- temperature/moisture condition.

Before product testing:
- zero the system;
- calibrate at representative forces such as 1 N, 2 N and 5 N;
- verify repeatability;
- check force trace stability;
- confirm actual travel speed.

## 19. V1 experimental matrix

Initial dry controlled-film matrix:

- No treatment × 6
- Squirrel's × 6
- BodyGlide × 6
- GLIDE-SPEC 40 × 6

Total:
**24 dry runs.**

Record:
- force-time trace;
- Fmax;
- Favg;
- μs;
- μk;
- visible residue/transfer observations.

After dry apparatus stability is established:
- Wet condition using 0.9% saline as a simple sweat/moisture model;
- repeated-friction testing;
- transfer/residue observations.

Dragon Skin 10/30 sensitivity testing is deferred until V1 data exists.

## 20. Why n=6

n=6 was selected as a practical V1 compromise:
- more robust than very small n;
- still manageable for a DIY rig;
- sufficient to estimate repeatability and expose obvious failure modes before scaling the experiment.

It is not being presented as a formal regulatory/statistical qualification sample size.

## 21. Wet-condition decision

Selected wet model:
**0.9% isotonic saline.**

Reason:
simple and reproducible approximation for a sweat/moisture condition.

The exact application amount was intentionally NOT frozen yet because a balm film can respond differently from a liquid dressing or aqueous lubricant. The 2026 literature's moisture protocol should inform, not be copied blindly.

Sequence:
1. dry baseline first;
2. verify apparatus;
3. then introduce wet condition.

## 22. Absolute target-value decision

No absolute “skin friction coefficient target” is being frozen.

Reasons:
- skin friction varies strongly with moisture, site, pressure, speed, roughness and counterface;
- no single universal skin μ pass/fail value is appropriate for this DIY setup;
- Dragon Skin is a surrogate, not human skin;
- patent values and literature values are development/reference data, not official universal standards.

Therefore V1 is a **comparative benchmark**:
same apparatus + same surface + same load + same speed + same product loading.

The objective is to identify relative differences and failure behavior, then establish GLIDE-specific engineering targets from actual data.

## 23. Reference evidence used in the decision

The research chain included:
- ASTM D1894-style sled methodology;
- ASTM G115 as a general friction-measurement/reporting guide rather than a skin pass/fail standard;
- skin tribology literature showing wide variation in measured μ;
- University of Wisconsin work on skin tissues/equivalents and Dragon Skin behavior;
- anti-chafing patent friction methodology and its 1 g / 20 x 20 cm / 200 g / 10 x 10 mm setup;
- recent 2026 International Wound Journal work using Dragon Skin, 3.5 mm and 150 mm/min sled testing;
- 2025 Skin Research and Technology surface characterization including Dragon Skin 20.

The evidence supports the architecture as a reasonable internal comparative setup, but does not establish it as a standardized skin tribometer.

## 24. Important corrections made during this session

1. **Dragon Skin 20 was not declared “optimal human skin.”**
   Earlier reasoning was too strong. V1 selection is based on repeatability, moderate stiffness, literature use and practical availability.

2. **10 x 10 mm contact pad was not frozen.**
   It was initially suggested from a patent but rejected as the V1 default because local pressure/film effects could dominate.

3. **0.10 g product loading was rejected.**
   V1 is now 5 mg/cm² = 20 mg over 4 cm².

4. **NF302 exact 10 N thread size was not guessed.**
   M3/M4 varies by capacity in the family; the 10 N drawing must be confirmed.

5. **No sled rail.**
   A rail would introduce unwanted friction/constraint.

6. **The rig is not intended to reproduce human skin absolutely.**
   It is an internal comparative benchmark.

7. **The GLIDE product definition remains physical-product-first.**
   The simulator is supporting infrastructure and must not be confused with the product.

## 25. Current V1 specification freeze

| Item | V1 decision |
|---|---|
| Product benchmark | Squirrel's + BodyGlide + GLIDE-SPEC 40 |
| Method | Horizontal motorized sled |
| Reporting | ASTM D1894-style/internal comparative |
| Skin-side surface | Dragon Skin 20 |
| Skin-side thickness | 3.5 mm |
| Sled mass | 200 g |
| Load cell | Naturoll NF302 10 N |
| ADC | HX711 |
| MCU | ESP32 |
| Motor | NEMA17 stepper |
| Drum | Ø20 mm constant-radius, single layer |
| Speed | 150 mm/min |
| Stroke | 100–150 mm |
| Counterface | 316L stainless flat pad |
| Counterface size | 20 × 20 mm |
| Controlled product loading | 5 mg/cm² |
| Product mass for 4 cm² | 20 mg |
| Conditioning | 5 min |
| Replicates | n=6 |
| First condition | Dry |
| Later wet model | 0.9% saline |
| Primary outputs | μs, μk, force-time curve |
| Secondary output | transfer/residue |
| Absolute μ target | none |
| Rail | none |
| NF302 exact mounting dimensions | OPEN until manufacturer drawing |

## 26. Immediate next actions

1. Obtain NF302 10 N exact mounting drawing and thread size from supplier/manufacturer.
2. Freeze sled dimensions around the confirmed load-cell interface.
3. Design the 400 x 150 mm-class base and motor/load-cell centerline.
4. Build BOM and purchase only V1-essential parts.
5. Assemble the empty rig.
6. Calibrate and characterize noise/repeatability.
7. Test no-treatment control.
8. Test Squirrel's and BodyGlide dry.
9. Test GLIDE-SPEC 40.
10. Only after dry stability is demonstrated, add wet/repeated-friction conditions.
11. Use the resulting reference-product failure modes to define the next GLIDE formulation/physical prototype iteration.

## 27. Decision status

**FROZEN:** test principle, Dragon Skin 20 / 3.5 mm, 200 g sled, 10 N NF302 selection, 150 mm/min, Ø20 mm constant-radius drum, no sled rail, 20 x 20 mm 316L pad, 20 mg controlled loading, 5 min conditioning, n=6, dry-first sequence.

**OPEN:** exact NF302 10 N mounting dimensions/thread; final bracket dimensions; exact wet-fluid application amount; real-stick transfer protocol details.

**DO NOT REGRESS:** do not replace the physical-product definition with a simulator/service interpretation; do not claim ASTM certification; do not claim Dragon Skin is equivalent to human skin; do not invent load-cell dimensions.


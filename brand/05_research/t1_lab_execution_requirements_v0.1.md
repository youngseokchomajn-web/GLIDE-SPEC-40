# GLIDE-SPEC 40 T1 Lab Execution Requirements — v0.1

Date: 2026-09-13  
Status: Vendor/lab briefing draft; not a final procurement specification

## 1. Purpose

This document converts the T1 friction pilot into a practical brief for contacting external testing laboratories, tribology laboratories, textile-testing laboratories, or universities with suitable friction-testing equipment.

The goal is **not** to purchase a machine immediately. The first objective is to determine whether an external laboratory can execute the method reproducibly and provide raw data suitable for GLIDE-SPEC development.

## 2. What GLIDE-SPEC needs from the laboratory

The laboratory should be able to support, directly or through a validated setup:

1. skin-surrogate / textile contact testing;
2. controlled linear reciprocating motion;
3. controlled normal load;
4. measurement of friction force and calculation of static/dynamic COF where valid;
5. controlled or documented temperature and relative humidity;
6. controlled dry/moist conditions;
7. repeated-cycle measurements;
8. raw-data export rather than averages only;
9. repeat testing across specimens and preferably across days;
10. documented calibration/instrument status.

Published work demonstrates that linearly moving skin-surrogate/textile friction devices can achieve high repeatability, including repeated measurements over multiple days. The studies also show that surrogate material and body region can materially change friction results. Therefore the laboratory's exact apparatus and surface materials must be documented rather than treated as interchangeable. DOI references: https://doi.org/10.1007/s11249-021-01502-1 and https://doi.org/10.1007/s11249-021-01560-5.

## 3. Minimum equipment capability

### Required

- tribometer or equivalent force-measurement apparatus capable of linear reciprocating contact;
- measurable/controlled normal load;
- adjustable reciprocating speed and stroke length;
- force acquisition sufficient to derive friction force;
- fixed textile mounting;
- specimen temperature/RH documentation;
- raw force/time data export;
- calibration or verification procedure.

### Strongly preferred

- programmable cycle count;
- interchangeable contact/surrogate-skin specimens;
- controlled environmental chamber or enclosure;
- automated data logging;
- ability to repeat a programmed method without manual timing;
- independent measurement of static and dynamic friction where appropriate.

### Not required at T1

- a device marketed specifically for cosmetics;
- a human clinical laboratory;
- a finished-product certification test;
- a machine that claims to simulate running exactly;
- a universal "anti-chafe" test standard.

T1 is a method-development exercise, not a certification test.

## 4. Surrogate-skin requirements

The laboratory must identify:

- supplier/manufacturer;
- material type;
- surface finish/roughness where available;
- thickness and backing;
- conditioning/storage method;
- expected service life or replacement rule;
- cleaning/preparation method;
- whether the material is intended for textile/skin-friction research.

Do not accept a statement such as "skin-like material" as sufficient documentation.

A published study found materially different friction coefficients across surrogate surfaces, including silicon and Lorica-type surrogate materials. This means changing surrogate material can change the measured result even when the textile is unchanged.

## 5. Textile specimen requirements

The laboratory should be able to mount a defined textile specimen consistently.

For T1 method development, one textile construction is preferred to reduce variance. Later phases will add representative constructions for:

- inner-thigh/groin interfaces;
- waistband;
- sports-bra/under-bra;
- seam/edge interfaces;
- hydration-vest/pack contact.

The laboratory should record:

- fiber/material description;
- knit/woven construction where known;
- fabric mass or thickness where available;
- supplier/lot;
- washing/preconditioning procedure;
- specimen dimensions;
- mounting orientation.

## 6. Product handling

The first benchmark set is:

1. untreated control;
2. petrolatum;
3. specialized anti-chafe stick;
4. specialized balm/ointment.

The laboratory must be able to apply each product to a defined area using a documented mass-per-area procedure.

Do not allow the laboratory to substitute a swipe-count-only application method unless the method is itself being evaluated and separately documented.

For each product record:

- commercial name and variant;
- lot/batch if available;
- format;
- purchase source/date;
- storage condition;
- application mass;
- application area;
- waiting/conditioning time.

GLIDE-SPEC candidate formulations should be introduced only after T1 method stability is demonstrated.

## 7. Moisture requirements

The laboratory must be able to create at least two controlled states:

- dry/reference;
- defined moist/sweat-simulated.

A later water-exposure condition may be added.

The laboratory should document:

- liquid composition;
- concentration where applicable;
- application volume or loading;
- application method;
- specimen conditioning time;
- temperature;
- ambient RH;
- whether liquid is absorbed, pooled, or remains on the surface.

Wet-state literature demonstrates that moisture can materially change skin–textile friction. Exact literature wet-state timings should not be copied into the GLIDE-SPEC method without pilot validation.

## 8. Data deliverables

The preferred deliverable is:

### Raw data

- force vs time/cycle data;
- static/dynamic COF calculation data;
- individual replicate results;
- environmental metadata;
- application metadata;
- instrument settings;
- calibration/verification record;
- deviations.

### Process documentation

- exact test method;
- apparatus model;
- surrogate-skin specification;
- textile specification;
- product application method;
- moisture method;
- operator information;
- test dates.

### Summary

- repeatability/variance analysis;
- untreated baseline;
- benchmark comparison;
- dry vs moist comparison;
- method limitations;
- recommendation to continue/modify/stop.

A report containing only a final ranking or averaged COF values is insufficient for GLIDE-SPEC evidence provenance.

## 9. Questions to ask a prospective laboratory

Before commissioning work, ask:

1. Do you have a tribometer or equivalent system capable of linear reciprocating skin/textile friction testing?
2. Can normal load, stroke length and speed be controlled and recorded?
3. Can you export raw force/time data?
4. Can you calculate static and dynamic COF separately?
5. Can the same textile specimen be mounted reproducibly?
6. Can you use a specified surrogate-skin material supplied or approved by us?
7. Can you control or document temperature and RH?
8. Can you create a repeatable moist/sweat-simulated condition?
9. Can you run repeated measurements within a day and on separate days?
10. What calibration/verification procedure is used?
11. What is the smallest practical sample size and specimen size?
12. What is the expected measurement uncertainty or repeatability from comparable work?
13. Can the operator be blinded to product identity?
14. Can the laboratory retain and deliver raw data and method metadata?
15. Can the laboratory execute a small method-development pilot before a larger benchmark study?

## 10. Procurement principle

Do **not** buy a tribometer solely because it can output a coefficient of friction.

The relevant capability is:

`repeatable interface + controlled motion + controlled moisture + raw force data + documented specimen preparation + reproducible application`

A technically sophisticated instrument can still produce weak product-development evidence if specimen preparation, application loading, moisture, or textile mounting are uncontrolled.

## 11. Recommended engagement structure

### Stage A — Capability call

Provide the laboratory with:

- T1 protocol;
- this requirements sheet;
- intended benchmark categories;
- requirement for raw data;
- statement that the method is still under development.

Ask whether their existing equipment can execute the architecture without forcing GLIDE-SPEC into an unrelated standard test.

### Stage B — Small pilot quote

Request a small pilot rather than immediately ordering a large comparative study.

The pilot should answer:

- Is the interface stable?
- Is the force signal usable?
- Is the textile mounting reproducible?
- Can the method distinguish untreated from at least one benchmark?
- Can dry and moist conditions be repeated?
- What is the observed variance?

### Stage C — Method lock

Only after reviewing pilot data should the following be fixed:

- surrogate material;
- textile;
- application loading;
- motion settings;
- moisture protocol;
- replicate structure;
- analysis method.

### Stage D — Matched incumbent baseline

Then execute the full benchmark set under identical conditions.

### Stage E — Candidate comparison

Only after the incumbent baseline is stable should GLIDE-SPEC candidate formulations be introduced.

## 12. Evidence boundary

A successful tribology test does not automatically prove:

- clinical prevention of chafing;
- exact hours of protection;
- superiority in real-world running;
- suitability for all anatomical sites;
- safety/skin compatibility;
- regulatory claim eligibility.

Those require separate validation tracks.

## 13. Decision rule for laboratory selection

Prefer the laboratory that can provide the strongest combination of:

1. method reproducibility;
2. relevant skin/textile tribology experience;
3. controlled moisture capability;
4. raw-data access;
5. transparent calibration/uncertainty information;
6. repeat testing across days;
7. willingness to run a small method-development pilot;
8. clear separation between measured result and interpretation.

The lowest quote is not automatically the best choice if it produces only a black-box final score.

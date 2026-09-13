# Brand Planning Changelog

## v0.9 — 2026-09-13

The Korean runner research protocol was converted into a field-ready survey instrument so the next step can be actual data collection rather than further informal question design.

### Added

- `brand/05_research/korean_runner_survey_field_instrument_v0.1.md`
  - screening and runner-profile questions
  - body-area frequency capture
  - reconstruction of the most recent meaningful failure event
  - separate symptom-onset and unacceptable-protection/failure timing
  - skin/product/garment/equipment/motion/sweat-water variables
  - reapplication, carryability, reachability, and switching behavior
  - failure-mode taxonomy derived from five community evidence passes
  - actual category-spend questions
  - neutral concept-card price sensitivity exercise
  - randomized concept trade-off structure with a keep-current option
  - open-ended diagnostic questions for qualitative interpretation
  - explicit data-quality and evidence-boundary rules

### Changed

- The project now has a separation between:
  1. research protocol — what must be learned;
  2. field instrument — the exact questions used to learn it;
  3. technical validation matrix — how recurring failures will later be measured objectively.
- The survey deliberately avoids unsupported numerical duration/performance claims.
- Non-topical substitutes such as clothing, tape, and equipment changes remain inside the choice architecture instead of treating topical cosmetics as the only category.

### Decision impact

The Korean/local evidence gate can now move from **instrument design** to **field execution**.

However, product specification remains locked. Survey results must still be combined with matched technical testing, skin compatibility evidence, and regulatory mapping before product claims or final formula/format decisions.

### Next gate

1. Pilot the questionnaire with approximately 5–10 qualified runners.
2. Check comprehension, completion time, response-option gaps, and leading-question risk.
3. Revise the instrument if pilot data reveal ambiguity.
4. Field the larger quantitative sample and recruit 20–30 qualitative interviews from variation cells.
5. Analyze the results against the pre-defined gate criteria.

## v0.8 — 2026-09-13

Round 5 findings were converted from research observations into a preliminary technical-validation architecture and the gate-closure sequence was updated accordingly.

### Added

- `brand/05_research/technical_validation_matrix_v0.1.md`
  - maps recurring failure modes to measurable technical questions
  - defines the working system as `skin × product × garment × equipment × motion × sweat/water × time`
  - separates bench method development, matched incumbent comparison, UX validation, and field validation
  - prohibits numerical thresholds until method variance and incumbent baselines are known
  - requires every final product requirement to link to evidence IDs and/or controlled test IDs

### Changed

- `brand/05_research/gate_closure_plan_v0.1.md` upgraded in place to v0.2
  - Round 5 variables incorporated into the gate sequence
  - technical validation matrix added as the starting architecture for incumbent/candidate testing
  - benchmark measurements expanded beyond friction to persistence, migration, transfer, sensory/application and reapplication burden where justified
  - numerical acceptance thresholds explicitly deferred until baseline data exist
- `brand/05_research/research_audit_v0.1.md` upgraded in place to v0.3
  - controlled performance architecture is now tracked as an explicit research category
  - Round 5 system-level findings and remaining gates updated

### Decision impact

The project is now ready to move from broad community discovery toward two parallel evidence tracks:

1. **Human evidence:** Korean runner survey + qualitative interviews to establish prevalence, failure context, switching, spend and price sensitivity.
2. **Technical evidence:** repeatable bench methods and matched incumbent testing derived from the failure taxonomy.

Neither track alone is sufficient for product lock.

### Evidence interpretation

The technical matrix is a test architecture, not a claim of efficacy. It intentionally leaves formulation, format, duration thresholds, superiority claims, price and SKU open until measurements and user evidence support them.

### Remaining gates

1. Field Korean runner survey and 20–30 qualitative interviews.
2. Structured price/value and willingness-to-pay analysis.
3. Bench method development and matched incumbent comparison.
4. Skin compatibility testing.
5. Controlled temperature/moisture/friction/persistence matrix.
6. Application-format and reachability validation.
7. Independent recovery evidence.
8. Korean regulatory classification and claim mapping.

## v0.7 — 2026-09-13

Community Evidence Round 5 was incorporated into the brand research decision chain, and the Korean runner survey protocol was upgraded before fielding.

### Added / incorporated

- `brand/05_research/community_round5_2026-09.md`
  - 16 individually preserved failure-context cases
  - Korean sweat/wash-off, garment migration, and distance/time reports
  - global heat/humidity, sports-bra, hydration-vest, pack, sensory, reapplication, and non-topical substitution cases
- `brand/05_research/korean_runner_interview_survey_v0.1.md` updated in place to v0.2
  - primary failure unit expanded to `skin × product × garment × equipment × motion × sweat/water × time`
  - separate capture of symptom onset vs unacceptable protection/failure
  - explicit garment migration, seams, straps, bra bands, vest/pack contact, and reachability variables
  - explicit topical vs adhesive vs apparel vs equipment substitution measurement
  - sensory/cleanup and carry/reapplication variables strengthened
  - non-topical/keep-current option added to concept trade-off design
  - community-derived failure taxonomy explicitly separated from prevalence or efficacy claims
  - v0.1 citation placeholder removed

### New evidence signals

- The most useful unit of analysis is increasingly the **system interaction**, not the topical product alone.
- Mileage is an insufficient standalone durability variable; time, sweat/water, temperature, motion, garment migration, and equipment contact can change the failure context.
- High-shear anatomical interfaces may lead users to adhesive, clothing, or equipment solutions rather than another topical product.
- Sensory attributes such as grease/wet feel, odor, staining, and cleanup can drive switching even when users perceive protection as adequate.
- Reachability and reapplication opportunity are functional constraints, especially for long events.
- Female-specific bra/waistband and hydration-vest interfaces warrant explicit cells rather than being pooled into generic body-area data.

### Changed

- The Korean runner evidence gate is still **open**, but the next survey/interview instrument now directly measures the highest-value failure-system variables surfaced by five community passes.
- Survey analysis will distinguish product failure from clothing/fit failure, equipment interaction, application/reapplication failure, skin compatibility, and sensory/cleanup objections.
- Non-topical substitutes are treated as real alternatives in product-choice and price/value research.
- No new numerical duration, superiority, medical, or regulatory claim has been adopted.

### Evidence interpretation

The fifth pass strengthens the working hypothesis that GLIDE-SPEC 40 should be designed and validated around the **skin–clothing–equipment–environment system**. It does not establish prevalence, objective friction reduction, exact persistence, comparative superiority, clinical benefit, or regulatory claim eligibility.

### Remaining gates

1. Balanced Korean/local runner survey and interviews.
2. Structured price/value and willingness-to-pay evidence.
3. Matched objective testing against petroleum jelly and leading specialized formats.
4. Skin compatibility testing.
5. Temperature/humidity friction and persistence testing.
6. Application-format prototypes and reachability testing.
7. Independent recovery evidence.
8. Korean regulatory classification and claim mapping.

## v0.6 — 2026-09-13

A fourth community-evidence pass expanded Korean and global runner discovery before the structured survey is fielded.

### Added

- `brand/05_research/community_round4_2026-09.md`
  - 18 individually preserved community cases
  - Korean 10 km, 20 km/2 h, 30 km+, wet-weather, garment-migration, and apparel-substitution reports
  - global ultrarunning cases covering sports-bra friction, tape switching, carryability, reapplication, heat-dependent handling, residue/staining, and contradictory incumbent experiences

### New evidence signals

- Garment migration can reintroduce skin-to-skin friction even when topical protection is applied.
- Apparel and adhesive barriers are direct substitutes/competitors for topical anti-chafe products.
- Long-event logistics make carryability, reachability, and reapplication part of functional product performance.
- Heat and sweat can change both perceived persistence and application/rheology.
- Anatomical site can determine which solution works; one product need not solve all sites.
- Users may accept premium apparel or specialized products when they solve several problems simultaneously.
- Contradictory reports remain substantial across Vaseline, Body Glide, Squirrel's Nut Butter, 2Toms, tape, and apparel.

### Changed

- Korean/local evidence gate is now richer but still not closed; structured prevalence and balanced sampling remain required.
- Survey requirements should explicitly measure substitute behavior, garment migration, reapplication logistics, and body-area-specific solution switching.

### Evidence interpretation

The new pass strengthens the hypothesis that the product problem is a **skin–clothing–equipment–environment system problem**, not merely a lubricant-selection problem. It does not establish prevalence, objective performance, superiority, exact duration, medical benefit, or regulatory claim eligibility.

### Remaining gates

1. Balanced Korean/local runner interviews or survey.
2. Structured price/value and willingness-to-pay evidence.
3. Matched objective testing against petroleum jelly and leading specialized formats.
4. Skin compatibility testing.
5. Temperature/humidity friction and persistence testing.
6. Application-format prototypes and reachability testing.
7. Independent recovery evidence.
8. Korean regulatory classification and claim mapping.

## v0.5 — 2026-09-13

The first Korean/local runner evidence pass was completed and the remaining pre-product-lock gates were converted into a concrete closure plan.

### Added

- `brand/05_research/korean_runner_evidence_round1_2026-09.md`
  - 4 individually traceable Korean/local signals
  - sweat-related Vaseline wash-off
  - clothing-motion interaction in groin/thigh friction
  - perceived duration limitation around 20 km / 2 h in one report
  - Korean marathon guidance recommending Vaseline for chafing prevention
- `brand/05_research/gate_closure_plan_v0.1.md`
  - gate-by-gate status
  - recommended study sequence
  - competitive benchmark structure
  - application-format prototype plan
  - skin compatibility/recovery separation
  - Korean regulatory/claim mapping requirement

### Changed

- `brand/05_research/research_audit_v0.1.md` upgraded to v0.2.
- Korean/local evidence is no longer a completely empty gate, but it remains insufficient for prevalence or product decisions.
- Distance/time coverage now includes Korean 10K and ~20 km/2 h reports, while controlled time-to-failure remains open.

### Evidence interpretation

- Korean community reports reproduce several international hypotheses: sweat-related wash-off, garment-motion contribution, and distance/time-dependent failure.
- A Korean marathon organizer guide confirms Vaseline is already a locally familiar chafing-prevention recommendation.
- These signals strengthen problem relevance but do not establish prevalence, objective performance limits, superiority, willingness-to-pay, or regulatory efficacy claims.

### Remaining gates

1. Balanced Korean/local runner interviews or survey.
2. Structured price/value and willingness-to-pay evidence.
3. Matched objective testing against petroleum jelly and leading specialized formats.
4. Skin compatibility testing.
5. Temperature/humidity friction and persistence testing.
6. Application-format prototypes and reachability testing.
7. Independent recovery evidence.
8. Korean regulatory classification and claim mapping.

## v0.4 — 2026-09-13

A third community-evidence pass was completed against the remaining gaps from v0.3. The evidence registry was upgraded to 40 individually preserved cases across three passes.

### Added

- `brand/05_research/community_round3_2026-09.md`
  - 15 individually preserved community/retailer cases
  - female-specific bra/waistband interfaces
  - hydration-vest interaction
  - sensitive skin and contradictory reactions
  - cold-state texture/application
  - rain/high-humidity behavior
  - post-chafe protection vs prevention
  - price/value
  - packaging/reachability
  - topical vs adhesive barrier switching

### Changed

- `brand/05_research/community_evidence_registry.md` upgraded to v0.3.
- Evidence IDs and explicit `What it does NOT prove` fields are now required for traceability.
- Registry now records 40 individual cases across Pass 1, Pass 2, and Pass 3.
- Evidence gaps were narrowed and converted into explicit pre-product-specification gates.

### New evidence signals

- Skin sensitivity can reverse product preference; contradictory reactions must be preserved.
- Temperature can change formulation usability, not merely protection performance.
- Female bra/waistband interfaces and hydration-vest interactions create distinct friction systems.
- Adhesive barriers can become preferred after repeated topical failure.
- Prevention and post-chafe recovery are separate jobs-to-be-done.
- Packaging geometry/reachability can limit an otherwise effective product.
- Price/value is evaluated against clothing, tape, and inexpensive incumbents, not only other cosmetic products.
- Retailer reviews show strong positive and negative outliers for the same incumbent product, reinforcing the need for controlled testing.

### Strategic status

- D008 (format/application UX as a first-class performance variable): **candidate, not yet formalized**.
- D009 (validate topical protection within the skin–clothing–environment system): **candidate, not yet formalized**.
- No new universal product-performance claim has been adopted.

## v0.3 — 2026-09-13

A second community-evidence pass was completed and stored as individually traceable cases, followed by pattern extraction and an evidence-to-decision audit.

### Added

- `brand/05_research/community_round2_2026-09.md`
  - 15 individually preserved community/retailer evidence cases
  - source URL, context, body area, distance/time, conditions, product/solution, positive/negative signals, strategic implication, and limitations
  - contradictions retained instead of averaged away
  - pattern extraction and new research hypotheses

### New evidence signals

- persistence is conditional rather than a single universal duration
- reapplication is a normal operating behavior in long-distance use
- body-area differences are substantial
- clothing/equipment changes can substitute for or complement topical products
- format affects application and perceived performance
- cold-state usability/rheology may matter
- heat/humidity may alter product behavior
- odor/product interaction surfaced as a niche sensory hypothesis
- incumbent products have meaningful strengths; no universal winner is established

### New candidate decisions

- D008 candidate: treat format/application UX as a first-class performance variable
- D009 candidate: validate topical protection within the full skin–clothing–environment system

These remain candidate decisions until balanced evidence and controlled testing support formal adoption into the main decision log.

### Still provisional

- marathon/ultra beachhead
- Endurance / Performance Skin Care working category
- TIME × MOTION × ENVIRONMENT abstraction
- PROTECT → PERFORM → RECOVER → OPTIMIZE architecture
- first-product performance requirements
- brand name, slogan, final target segment, formula, numerical thresholds, regulatory claims, packaging, pricing

## v0.2 — 2026-09-13

A community evidence set and completeness audit were added.

## v0.1 — 2026-09-13

Initial brand-planning workspace created inside the GLIDE-SPEC-40 repository.

## Versioning rule

Future changes to brand strategy should document:

1. what changed
2. why it changed
3. what evidence caused the change
4. what downstream product or GLIDE-SPEC 40 requirements may be affected

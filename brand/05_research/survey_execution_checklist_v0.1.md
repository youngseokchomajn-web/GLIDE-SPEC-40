# Survey Execution Checklist — v0.1

Date: 2026-09-13

## Before fielding

- [ ] Finalize respondent screener.
- [ ] Randomize answer choices where order effects are possible.
- [ ] Separate observed behavior from opinion questions.
- [ ] Show product concept before price questions.
- [ ] Do not use unsupported numerical performance claims.
- [ ] Keep male/female and anatomical-interface variables explicit.
- [ ] Pilot with 5–10 runners and remove ambiguous questions.

## Data quality

- [ ] Remove respondents failing the running screener.
- [ ] Flag impossible distance/time combinations.
- [ ] Flag contradictory price thresholds for review rather than silently correcting.
- [ ] Preserve raw responses.
- [ ] Preserve survey version and field dates.
- [ ] Record recruitment source.
- [ ] Do not deduplicate contradictory respondents merely because their answers look inconvenient.

## Analysis

- [ ] Report n for every segment.
- [ ] Report missing data.
- [ ] Show distributions, not only means.
- [ ] Preserve outliers where they may represent a meaningful user segment.
- [ ] Compare actual spend with stated price sensitivity.
- [ ] Compare price sensitivity with current solution type.
- [ ] Compare recurrent-failure users with no/low-problem users.
- [ ] Cross-tab body area and conditions where sample size permits.

## Evidence storage

For each major finding record:

- Finding ID
- survey version
- sample definition
- n
- exact question(s)
- result
- uncertainty/limitation
- whether it is descriptive, hypothesis-generating, or decision-supporting
- downstream product implication

## No-go conditions

Do not use the survey to claim:

- objective product superiority
- exact duration of protection
- medical treatment/prevention
- regulatory approval/eligibility
- universal runner preference
- market-wide prevalence from a convenience sample

## Recommended next step after survey

Select the top 2–3 failure scenarios from the survey and move them into matched incumbent testing. The survey identifies where to test; it does not replace the test.

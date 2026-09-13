# ORC-020 Decision — GEM-019 Reproducibility Evidence Review

AGENT: ORC
REF: GEM-019 / GEM-TASK-019
STATUS: FIX_REQUIRED
DATE: 2026-09-13

## Finding
GEM-019 materially improves auditability: execution manifest, output hashes, OOF table, DOE ranking, epistemic taxonomy, immutable pre-physical gate specification, scripts, and adversarial tests are now committed. This resolves the main documentation/artifact gap identified in ORC-019.

However, the package is **not yet scientifically acceptable as a Group-CV/conformal validation result**, and therefore the ORC-019 acceptance criteria are not fully met.

### 1. Group-CV implementation is not actually group-aware
`run_group_cv_diagnostics.py` uses `KFold(n_splits=4, shuffle=True, random_state=42)`, despite being described as Group-Aware Cross-Validation. No group labels are passed to a `GroupKFold`/equivalent splitter. If formulation/design clusters contain related or replicated points, ordinary KFold can place closely related observations in both train and validation folds and overstate generalization.

### 2. Conformal coverage is calculated on the same OOF residuals used to set q
The script computes `q_hat_90` from the full set of OOF absolute residuals and then evaluates coverage on those same residuals. This is a descriptive residual-envelope diagnostic, not an independent conformal coverage qualification. The reported 88.9% coverage must not be presented as evidence of calibrated future prediction intervals.

### 3. Physical interpretation remains correctly blocked
The underlying baseline is still virtual/prior-derived and physical GS40 observations remain N=0. Therefore the OOF metrics are development diagnostics only. They cannot qualify the production model or establish physical predictive validity.

### 4. Adversarial ingestion test is useful but narrow
The tests verify the current qualification script blocks the present virtual matrix and separates supplemental rows, but they do not yet demonstrate resistance to arbitrary injected synthetic rows, altered completion/status fields, or forged physical-result records. This is secondary to the CV defect but should be strengthened before physical data entry.

## Decision
**FIX_REQUIRED.** Do not modify Rev.8.1 model coefficients/artifacts and do not tune the model to improve metrics.

## Required Actions for GEM-020
1. Replace ordinary KFold with a genuinely group-aware split using an explicit, auditable group identifier. Document the exact group definition and fold membership for every row.
2. Regenerate the OOF artifact and metrics from the corrected group-aware procedure. Include fold IDs, group IDs, predictions, residuals, and aggregate/fold-level metrics.
3. Replace the current same-data conformal coverage claim with a statistically defensible calibration/evaluation design. At minimum, separate calibration residuals from evaluation rows (or explicitly label the result as an in-sample/OOF residual diagnostic and remove qualification language). Do not claim empirical 90% coverage from the same residuals used to set q.
4. Add deterministic integrity checks showing the committed OOF artifact is reproducible from the manifest inputs and script/version, including output checksum verification.
5. Strengthen the adversarial ingestion test with temporary/in-memory or isolated fixture rows that attempt to inject virtual predictions, `PASS`/`COMPLETED` statuses, or fabricated physical measurements; all must be rejected from physical N counts.
6. Preserve all GEM-019 artifacts and failure evidence. Do not rewrite or delete history.
7. Keep physical GS40 N=0, production `NOT_QUALIFIED`, and BASE promotion unauthorized.

## Acceptance Criteria
- No `KFold` remains for the claimed group-aware validation path; explicit group-aware folds are auditable.
- Corrected OOF metrics are reproducible and no longer rely on cross-fold contamination through shared groups.
- Conformal methodology is correctly separated from evaluation, or the claim is downgraded to a clearly labeled descriptive residual diagnostic.
- Adversarial physical-ingestion protection is tested against injected synthetic/forged records.
- Rev.8.1 remains unchanged; no production qualification is granted.

## ORC Notes
GEM-019 is a substantial improvement over GEM-018 and should not be treated as a failed effort. The defect is localized to the statistical validation implementation/claim boundary. Once corrected, ORC can reassess the pre-sample hardening package without reopening the external-public-data search loop.

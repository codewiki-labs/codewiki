# Model And Usage Governance

## Feature Coverage

### Feature: `provider-usage-accounting`

- Spec Basis: `MU-USAGE-001`, `MU-USAGE-002`, `MU-USAGE-003`, `MU-USAGE-004`.
- Surface: administrator usage reporting and pre-call limit checks consume the normalized usage ledger rather than provider-specific response shapes.
- API or Event: model calls deliver terminal provider usage to the normalization boundary before the result is returned to callers.
- Authorization and Limits: per-user limits are evaluated before billable calls; detailed ledger access remains an administrator boundary.
- Service and Provider: `normalizeGeminiUsage` in `src/usage/provider-usage.ts` subtracts cached tokens and separates image modalities before `computeCostBreakdown` applies configured price units.
- Persistence and Lifecycle: normalized counts and cost components are stored as an immutable event in `llm_usage_events`; display copies do not replace the ledger.
- Usage, Cost and Audit: cache read, cache write, image input, and image output counts remain independent; configured image-token pricing excludes duplicate per-image charging.
- Failure and Recovery: terminal usage is recorded when available on failed or interrupted calls, while a ledger write failure is reported separately from provider-call success.
- Exact Tests: `tests/provider-usage.test.ts` covers provider mappings, cache subtraction, image separation, pricing exclusivity, and event persistence.

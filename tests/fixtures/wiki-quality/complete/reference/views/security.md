# Security View

## Feature Coverage

### Feature: `security-enforcement-view`

- Spec Basis: `SEC-R001`.
- Surface: authenticated administrator requests cross the shared security logging boundary.
- API or Event: protected handlers under `src/auth/guards.ts` attach verified identity before request logging.
- Authorization and Limits: guards reject missing identity and the logger applies `redactSensitiveHeaders` before emitting request metadata.
- Service and Provider: the shared logging configuration receives only bounded headers after guard processing.
- Persistence and Lifecycle: emitted logs retain request outcome metadata without persisting authentication secrets.
- Usage, Cost and Audit: redacted authentication outcomes remain available for operational audit with no model usage or cost effect.
- Failure and Recovery: malformed or missing credentials are rejected and still pass through the same redacted failure logging boundary.
- Exact Tests: `tests/require-menu-stepup.test.ts` covers protected success and failure requests without exposing authentication secrets.

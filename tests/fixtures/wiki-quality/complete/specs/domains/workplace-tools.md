# Workplace Tools

## Requirements

### Requirement: `WT-POSTER-001`

Poster generation must use an enabled poster type and an allowed configured image provider.
A completed poster generation must preserve the request inputs, model, and policy version as an auditable snapshot.

## Acceptance Criteria

- A disabled poster type or disallowed provider is rejected before generation.
- A completed generation can be audited from its preserved request and policy snapshot.

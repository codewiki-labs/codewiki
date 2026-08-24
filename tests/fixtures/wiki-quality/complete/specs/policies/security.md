# Security Policy

## Requirements

### Requirement: `SEC-R001`

Authentication secrets must never be written to application logs.

## Acceptance Criteria

- Protected request logs redact authentication secrets while retaining bounded diagnostic metadata.

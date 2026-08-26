# Security Policy

## Requirements

### `SEC-R001`

Authentication secrets must never be written to application logs.

## Acceptance Criteria

### `SEC-AC001`

Protected request logs redact authentication secrets while retaining bounded diagnostic metadata.

# Model And Usage Governance

## Requirements

### Requirement: `MU-USAGE-001`

Canonical usage dimensions must keep general, cache, and image tokens non-overlapping.
General input excludes cache-read, cache-write, and image-input tokens.

### Requirement: `MU-USAGE-002`

Token costs divide each token count by 1,000,000 before applying its configured price.
Web-search and image-generation counts use per-request prices.

### Requirement: `MU-USAGE-003`

Configured image-token pricing excludes duplicate per-image charging.

### Requirement: `MU-USAGE-004`

Terminal usage from failed or interrupted calls must remain auditable.

## Acceptance Criteria

- 300 cache-write tokens at 1 USD per million cost 0.0003 USD.
- Two generated images at 0.04 USD each cost 0.08 USD when image-token prices are absent.
- The same request has zero per-image cost when either image-token price is configured.

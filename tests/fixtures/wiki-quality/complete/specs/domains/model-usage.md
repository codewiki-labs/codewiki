# Model And Usage Governance

## Requirements

### `MU-USAGE-R001`

Canonical usage dimensions must keep general, cache, and image tokens non-overlapping.
General input excludes cache-read, cache-write, and image-input tokens.

### `MU-USAGE-R002`

Token costs divide each token count by 1,000,000 before applying its configured price.
Web-search and image-generation counts use per-request prices.

### `MU-USAGE-R003`

Configured image-token pricing excludes duplicate per-image charging.

### `MU-USAGE-R004`

Terminal usage from failed or interrupted calls must remain auditable.

## Acceptance Criteria

### `MU-USAGE-AC001`

300 cache-write tokens at 1 USD per million cost 0.0003 USD.

### `MU-USAGE-AC002`

Two generated images at 0.04 USD each cost 0.08 USD when image-token prices are absent.

### `MU-USAGE-AC003`

The same request has zero per-image cost when either image-token price is configured.

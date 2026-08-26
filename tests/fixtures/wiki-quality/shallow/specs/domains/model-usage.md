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

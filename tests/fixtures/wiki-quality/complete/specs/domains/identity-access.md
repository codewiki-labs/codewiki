# Identity And Access

## Requirements

### `IA-AUTH-R001`

A MANAGER may access only explicitly assigned, non-administrator-only menus.
A USER cannot access administrator routes.

### `IA-AUTH-R002`

Every protected administrator operation requires step-up authentication.

## Acceptance Criteria

### `IA-AUTH-AC001`

An assigned MANAGER can access the matching protected menu after step-up.

### `IA-AUTH-AC002`

A MANAGER without the assignment, a MANAGER targeting an administrator-only menu, and a USER are rejected.

# Identity And Access

## Requirements

### Requirement: `IA-AUTH-001`

A MANAGER may access only explicitly assigned, non-administrator-only menus.
A USER cannot access administrator routes.

### Requirement: `IA-AUTH-002`

Every protected administrator operation requires step-up authentication.

## Acceptance Criteria

- An assigned MANAGER can access the matching protected menu after step-up.
- A MANAGER without the assignment, a MANAGER targeting an administrator-only menu, and a USER are rejected.

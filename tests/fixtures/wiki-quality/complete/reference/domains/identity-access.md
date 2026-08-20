# Identity And Access

## Feature Coverage

### Feature: `admin-menu-authorization`

- Surface: administrator routes and menu navigation expose only the management areas allowed for the current actor.
- API or Event: protected route handlers attach `requireMenuStepup` from `src/auth/guards.ts` with the exact menu key they enforce.
- Authorization and Limits: the guard verifies JWT identity, reloads the active user, grants all known menus to ADMIN, checks MANAGER `menuPermissions`, rejects administrator-only menus, and verifies `X-Admin-Stepup` for the same user.
- Service and Provider: menu assignments are sanitized before persistence so unknown, duplicate, and administrator-only keys cannot grant access.
- Persistence and Lifecycle: current role, active state, and `menuPermissions` are read from durable user state on each protected request rather than trusted from stale frontend visibility.
- Usage, Cost and Audit: this feature has no model usage or cost effect; security audit requirements are represented by the protected route and authentication logs.
- Failure and Recovery: missing identity returns unauthorized, disallowed role or menu returns forbidden, and missing or invalid step-up requires a new challenge without invoking the handler.
- Exact Tests: `tests/require-menu-stepup.test.ts` covers ADMIN, allowed MANAGER, disallowed MANAGER, administrator-only menu, USER, and missing step-up behavior.

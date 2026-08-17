---
name: updating-code-wiki
description: Use before completing project-related work when approved intent changed, implementation navigation changed, or Code-Wiki content became stale.
---

# Updating Code-Wiki

Update normative Specs and descriptive Reference through separate authority paths. Code changes may require a Reference refresh, but they never silently rewrite Specs.

## Decide What Changed

### Durable intent

Store durable user intent when it should govern future sessions: final behavior, project direction, long-lived constraints, architecture or security invariants, important rationale, non-goals, and Acceptance Criteria.

Do not store one-off debugging requests, temporary test instructions, transient workarounds, implementation plans, or raw conversation history.

### Current implementation

Refresh Reference when verified source code, configuration, runtime flow, entry points, symbols, models, APIs, commands, dependencies, tests, security behavior, or gotchas change.

## Updating Specs

Canonical Specs contain current approved intent only.

1. Identify affected project, architecture, security, or domain Specs.
2. Draft the exact semantic change: current behavior, proposed behavior, constraints, important rationale, non-goals, Acceptance Criteria, and Related Domains.
3. Obtain user approval before editing canonical Specs or implementing a new requirement. Exact Spec content explicitly supplied with an implementation instruction is already approved.
4. Apply semantic compaction: replace superseded requirements with the current approved intent and retain only rationale still useful for understanding it.
5. Update `wiki/specs/index.md` when the domain registry changes.
6. Create or rename the paired Reference domain at the same relative path whenever a Spec domain is created or renamed.
7. Verify implementation against the updated Acceptance Criteria.

Do not add draft status machinery inside canonical Specs. Keep drafts in the active design or approval conversation until approved. Do not append a chronological transcript; Git preserves history.

## Updating Reference

Update Reference from verified source code and observed runtime state:

1. Start from changed source, configuration, tests, and runtime evidence.
2. Map them to affected paired domain pages and Reference-only cross-cutting pages.
3. Verify paths, symbols, routes, models, commands, flows, and test locations before writing.
4. Keep pages concise and navigation-oriented.
5. Update `wiki/reference/index.md` when pages are added, removed, split, merged, or renamed.
6. Preserve the domain taxonomy shared with Specs.

If implementation changed but violates an approved Spec, document the verified mismatch for the task; do not normalize either the Spec or Reference into a false statement. The Spec continues to describe the desired state, and Reference may accurately describe the nonconforming current state.

## Pairing And Cross-Cutting Pages

- Every Spec has a corresponding Reference: project-to-overview, index-to-index, same-named architecture and security pages when their Specs exist, and exact relative paths for domains.
- Reference-only domain files are invalid. The Spec and Reference domain trees must contain identical relative file sets.
- Reference-only pages such as data flow, data models, API surface, configuration, dependencies, commands, testing, gotchas, and glossary do not need Specs.
- A logical domain may navigate to many source modules; do not rename domains merely to mirror folders.

## Closeout

State separately:

- which Specs changed and where user approval came from
- which old intent was semantically compacted
- which Reference pages changed from verified implementation evidence
- which Acceptance Criteria were verified
- any remaining Spec/code nonconformance, stale Reference, or missing pair

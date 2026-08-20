---
name: reading-code-wiki
description: Use when starting project-related work in a repository that has a code-wiki, to recover approved intent and select minimal implementation context.
---

# Reading Code-Wiki

Recover durable project intent before navigating toward implementation. Specs are normative; Reference is descriptive. Specs are the behaviorally complete user-facing contract; Reference is the agent-facing implementation map.

## Read Order

1. Read `wiki/index.md` to recover authority, approval, and navigation rules.
2. Always read `wiki/specs/project.md` in full. It is the concise global memory for purpose, priorities, global intent, constraints, and non-goals.
3. Read `wiki/specs/index.md` and match the task to one or more domain responsibilities.
4. For an architecture task or a permission or security task, always select the relevant cross-cutting Reference page whether or not the corresponding Spec exists; also select the approved Spec when present. Architecture work selects `wiki/reference/architecture.md`; permission or security work selects `wiki/reference/security.md`.
5. Read every selected Spec in full, including Intent, Requirements, Constraints, Rationale, Non-goals, Acceptance Criteria, and `Related Domains`.
   - Capture the stable requirement IDs and Acceptance Criterion IDs that define correctness.
6. Recursively follow `Related Domains`, deduplicate cycles, and read the resulting closure in full.
7. For every selected Spec domain, read the paired Reference domain at the same relative path under `wiki/reference/domains/`.
8. For every selected cross-cutting Spec, confirm that its paired Reference page is selected before source inspection: `wiki/specs/architecture.md` pairs with `wiki/reference/architecture.md`, and `wiki/specs/security.md` pairs with `wiki/reference/security.md`.
9. Read Reference-only pages such as commands, configuration, testing, data flow, dependencies, models, API surface, gotchas, or glossary only when the task needs them. For an implementation or bug-fix task, include `wiki/reference/testing.md` unless the selected domain pages already provide complete verification paths.

Do not read all domains or all Reference pages by default. Completeness applies to the selected requirement closure, not the entire Wiki.

## Interpret Each Layer Correctly

- `wiki/specs/project.md` explains why the project exists and where it is going.
- Specs state what should be true even when code currently differs.
- Reference states where and how the implementation was organized when verified.
- Source code and observed runtime state determine what is currently implemented.

The user does not need to read Reference. Agents read it to accelerate source verification, then present desired behavior and Spec conformance from Specs. If a Spec cannot determine an actor permission, calculation result, policy decision, invariant, lifecycle or failure outcome, retention rule, audit meaning, or testable result without Reference, report a Spec sufficiency defect.

Do not weaken a requirement because Reference or code describes a different state. Do not cite Reference alone as proof of current behavior.

## Missing Or Ambiguous Context

- Missing `wiki/index.md` or `wiki/specs/project.md`: report that persistent memory is incomplete.
- Missing matched domain: inspect the registry and source, then propose a new paired domain if durable intent warrants it.
- Missing Reference counterpart: report a domain-pairing violation and use targeted source search.
- Ambiguous or conflicting Specs: do not choose silently. Present the conflict for user resolution.
- Stale Reference: switch to `exploring-code-with-wiki`, verify source, and record a Reference refresh need.

## Output

Before planning or editing, be able to state concisely:

- project-level intent and constraints that apply
- directly matched and related Specs read
- approved requirements and Acceptance Criteria
- stable requirement IDs used for implementation and verification mapping
- paired Reference pages to follow
- source claims still requiring verification
- whether the request needs a Proposed Spec Change and user approval

For user-facing review, summarize the applicable Spec and eventual Spec conformance. Include Reference navigation details only when the user requests implementation evidence or when they are necessary to explain a mismatch.

Use `exploring-code-with-wiki` for implementation tracing and `updating-code-wiki` for approved canonical changes or descriptive refreshes.

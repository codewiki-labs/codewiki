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
4. Read `wiki/reference/coverage.json` when the task concerns feature coverage, architecture, authentication, permission, security, ownership, public access, sensitive data, secrets, or other trust boundaries. Use it to identify source-derived concern applicability, owning domains, policy paths, and view paths.
5. Read every selected Spec in full, including Intent, Requirements, Constraints, Rationale, Non-goals, Acceptance Criteria, `Required Context`, and `See Also`.
   - Capture the stable requirement IDs and Acceptance Criterion IDs that define correctness.
6. Recursively follow `Required Context`, deduplicate cycles, and read that closure in full. Follow `See Also` only when directly relevant; never recurse through it.
7. For every selected Spec domain, read the paired Reference domain at the same relative path under `wiki/reference/domains/`.
8. Select a policy Spec under `wiki/specs/policies/` when its approved cross-domain rule applies. Every selected policy must have the same-named view under `wiki/reference/views/`.
9. Select `wiki/reference/views/architecture.md` or `wiki/reference/views/security.md` when the coverage manifest lists it and the task needs its cross-domain source map. A permission or security task does not make a missing security view an error when `security.applicability` is evidence-backed `not_applicable`; domain-owned security may also be fully navigable through its paired domain Reference.
10. Read Reference-only pages such as commands, configuration, testing, data flow, dependencies, models, API surface, gotchas, or glossary only when the task needs them. For an implementation or bug-fix task, include `wiki/reference/testing.md` unless the selected domain pages already provide complete verification paths.

Do not read all domains or all Reference pages by default. Completeness applies to the selected requirement closure, not the entire Wiki.

Legacy `Related Domains` is migration input, not a recursive retrieval contract. Until it is migrated, follow each legacy link at most one hop, classify it as `Required Context` or `See Also`, and report the stale representation.

## Interpret Each Layer Correctly

- `wiki/specs/project.md` explains why the project exists and where it is going.
- Specs state what should be true even when code currently differs.
- Reference states where and how the implementation was organized when verified.
- `wiki/reference/coverage.json` states which source features and concerns were accounted for at its recorded revision; it does not approve behavior.
- Source code and observed runtime state determine what is currently implemented.

The user does not need to read Reference. Agents read it to accelerate source verification, then present desired behavior and Spec conformance from Specs. If a Spec cannot determine an actor permission, calculation result, policy decision, invariant, lifecycle or failure outcome, retention rule, audit meaning, or testable result without Reference, report a Spec sufficiency defect.

Do not weaken a requirement because Reference or code describes a different state. Do not cite Reference alone as proof of current behavior.

## Missing Or Ambiguous Context

- Missing `wiki/index.md` or `wiki/specs/project.md`: report that persistent memory is incomplete.
- Missing matched domain: inspect the registry and source, then propose a new paired domain if durable intent warrants it.
- Missing Reference counterpart: report a domain-pairing violation and use targeted source search.
- Missing policy view: report a policy-and-view pairing violation. A view without a policy is valid only when the coverage manifest lists it and its durable behavior is grounded in domain Specs or explicitly descriptive.
- Missing security or architecture view with evidence-backed `not_applicable`: do not invent or require a placeholder page.
- Ambiguous or conflicting Specs: do not choose silently. Present the conflict for user resolution.
- Stale Reference: switch to `exploring-code-with-wiki`, verify source, and record a Reference refresh need.

## Output

Before planning or editing, be able to state concisely:

- project-level intent and constraints that apply
- directly matched and required Specs read
- recursively required Specs and any directly selected See Also pages
- approved requirements and Acceptance Criteria
- stable requirement IDs used for implementation and verification mapping
- paired Reference pages to follow
- source claims still requiring verification
- applicable coverage-manifest concerns and any policy/view pairing issue
- whether the request needs a Proposed Spec Change and user approval

For user-facing review, summarize the applicable Spec and eventual Spec conformance. Include Reference navigation details only when the user requests implementation evidence or when they are necessary to explain a mismatch.

If any page you actually read is larger than 200 lines, always end your response with a one-line oversize note naming the page and its line count, even when the user asked for a short answer. Do not start compacting; repair goes through the `updating-code-wiki` oversize flow only when the user asks.

Use `exploring-code-with-wiki` for implementation tracing and `updating-code-wiki` for approved canonical changes or descriptive refreshes.

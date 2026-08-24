---
name: exploring-code-with-wiki
description: Use when source-code inspection is needed and a code-wiki exists, especially for implementation tracing or Spec and Reference verification.
---

# Exploring Code With Wiki

Use approved Specs as the desired-state contract and agent-facing Reference as a navigation map into current source. Reference narrows inspection; it never replaces it or becomes part of the user's review burden.

## Preconditions

Use `reading-code-wiki` first so project memory, matched Specs, their recursive `Required Context` closure, any directly relevant nonrecursive `See Also` pages, and paired Reference pages are already known.

## Inspection Process

1. Extract every selected stable requirement ID and Acceptance Criterion from the Spec.
2. Extract the paired Reference domain's Feature Coverage, `Spec Basis`, Spec Implementation Map, entry points, paths, routes, events, symbols, models, jobs, tests, dependencies, and Contract Artifacts. When relevant, use `reference/coverage.json` and a manifest-listed concern view to find cross-domain evidence.
3. Use Authorization Enforcement, Invariant Enforcement, Lifecycle Implementation, Failure Implementation, and Usage, Cost And Audit Implementation to choose the smallest complete source trace.
4. Inspect every cited production path and exact focused test before relying on the Reference claim.
5. Trace only named callers, dependencies, schemas, generated artifacts, events, jobs, storage layers, and runtime composition needed to establish behavior.
6. Use broad repository search only when Reference is missing, paths no longer exist, a feature trace is incomplete, `Spec Basis` is absent, or the task crosses an undocumented boundary.
7. Compare verified implementation and test results with each affected Spec requirement and Acceptance Criterion.
8. Build a Spec conformance matrix: `requirement ID → implementation evidence → verification result → pass or mismatch`.

If tracing reveals an undocumented logical domain, pause before making decisions in that domain, load its Spec if one exists, and record the missing `Required Context`, `See Also`, coverage-manifest assignment, or Reference link. If no approved Spec exists and durable intent is needed, use the approval gate instead of inferring it from source.

For security or architecture work, start with the concern's owning domains in `reference/coverage.json`. A missing global policy or view is not itself a gap when the concern is evidence-backed `not_applicable`, or when applicable behavior is fully owned and traced by domains. If a policy exists, verify its paired view; if a view exists without a policy, keep its source observations descriptive and map durable behavior to domain requirement IDs.

## Mismatch Rules

- **Spec differs from code:** the approved Spec remains the desired state. Report nonconformance and change the implementation to conform when the user requested implementation.
- **Reference differs from code:** source remains the observed-state authority. Record the verified paths and refresh Reference.
- **User request differs from a Spec:** propose the exact Spec change and obtain approval before changing canonical intent or implementing the new requirement.

Never infer a Spec change from code, tests, Reference, runtime drift, or an implementation shortcut. Never refresh a Spec merely to describe what code happens to do.

The repair direction does not expand the user's requested scope. For read-only audits, reviews, explanations, or diagnoses, report nonconformance and stale Reference without editing them.

## Evidence Discipline

- Verify implementation claims in active code, configuration, manifests, schemas, routes, or observed runtime state.
- Use tests as supporting evidence for verification paths and regression coverage, while checking the production path they exercise.
- Treat prose docs and comments as discovery hints unless the user has approved them as normative content.
- Keep uncertainty explicit when runtime behavior or dynamic configuration cannot be verified.

## Output

Lead with:

- the applicable approved requirements and Acceptance Criteria
- the Spec conformance matrix
- any Spec/code nonconformance or remaining uncertainty

Do not require the user to read Reference. Provide the following agent evidence only when useful or requested:

- Reference pages used as navigation
- source and test files inspected
- verified current behavior
- stale or missing Reference
- missing Feature Coverage, incomplete feature traces, or vague evidence
- exact verification commands or remaining uncertainty

After implementation, use `updating-code-wiki` to refresh descriptive navigation without silently changing approved intent.

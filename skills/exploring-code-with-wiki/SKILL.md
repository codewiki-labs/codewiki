---
name: exploring-code-with-wiki
description: Use when source-code inspection is needed and a code-wiki exists, especially for implementation tracing or Spec and Reference verification.
---

# Exploring Code With Wiki

Use approved Specs as the desired-state contract and Reference as a navigation map into current source. Reference narrows inspection; it never replaces it.

## Preconditions

Use `reading-code-wiki` first so project memory, matched Specs, their `Related Domains` closure, and paired Reference pages are already known.

## Inspection Process

1. Extract concrete entry points, source paths, routes, symbols, models, jobs, tests, commands, dependencies, and gotchas from the paired Reference pages.
2. Inspect those source locations and nearby tests first.
3. Trace only named callers, dependencies, schemas, generated artifacts, events, jobs, storage layers, and runtime composition needed to establish behavior.
4. Use broad repository search only when Reference is missing, paths no longer exist, or the task crosses an undocumented boundary.
5. Compare the verified implementation with each affected Spec requirement and Acceptance Criteria.

If tracing reveals an undocumented logical domain, pause before making decisions in that domain, load its Spec if one exists, and record the missing Related Domains or Reference link. If no approved Spec exists and durable intent is needed, use the approval gate instead of inferring it from source.

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

Report:

- Specs and Acceptance Criteria used as the contract
- Reference pages used as navigation
- source and test files inspected
- verified current behavior
- Spec/code nonconformance
- stale or missing Reference
- exact verification commands or remaining uncertainty

After implementation, use `updating-code-wiki` to refresh descriptive navigation without silently changing approved intent.

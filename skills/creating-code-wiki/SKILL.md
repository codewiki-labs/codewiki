---
name: creating-code-wiki
description: Use when initializing or substantially regenerating a repository-local Code-Wiki for persistent project memory.
---

# Creating Code-Wiki

Create a V2 Wiki whose Specs are a behaviorally complete user-facing contract and whose Reference is an agent-facing implementation map. Users approve Specs and taxonomy, not Reference content.

## Separate The Evidence

Use different evidence for different questions:

- Specs describe desired state, contain only user-approved intent, and must let a reviewer determine correct behavior without reading Reference.
- Reference describes the current implementation for agents and must be grounded in source code, configuration, manifests, schemas, routes, runtime composition, or runtime evidence observed during the task.
- Tests support verification paths and expected behavior candidates, but do not override active source or runtime evidence.
- Existing prose docs, comments, and an older Wiki are discovery hints. They are not automatically approved requirements or confirmed implementation facts.

Mark uncertain descriptive claims as `Confirm needed`. Do not use that label to place unapproved requirements in canonical Specs.

Use the replaceability test for every detail:

- If changing the detail would change an actor's allowed behavior, a calculation result, a policy decision, an invariant, a lifecycle outcome, failure handling, retention, audit meaning, or an observable Acceptance Criterion, it belongs in Spec.
- If the implementation can replace the detail while preserving all approved outcomes, it belongs in Reference. Typical examples are internal function and type names, source paths, provider SDK field paths, table and column names, call graphs, and exact test locations.

## Canonical Structure

Create the core structure below. Architecture and security Specs are optional until corresponding global intent is approved; when present, pair them with Reference pages.

```text
wiki/
├── index.md
├── specs/
│   ├── index.md
│   ├── project.md
│   ├── architecture.md        # when approved
│   ├── security.md            # when approved
│   └── domains/
│       └── <domain>.md
└── reference/
    ├── index.md
    ├── overview.md
    ├── architecture.md
    ├── data-flow.md
    ├── data-models.md
    ├── api-surface.md
    ├── configuration.md
    ├── dependencies.md
    ├── commands.md
    ├── testing.md
    ├── security.md
    ├── gotchas.md
    ├── glossary.md
    └── domains/
        └── <domain>.md
```

Every Spec has a corresponding Reference, but only domain pairs require identical relative paths. `wiki/specs/project.md` is paired with `wiki/reference/overview.md`; `wiki/specs/index.md` is paired with `wiki/reference/index.md`; architecture and security Specs pair with the same-named Reference pages when those Specs exist. Other useful Reference-only pages do not require Specs.

**Every Spec domain has exactly one Reference domain with the same relative path.** For example, `wiki/specs/domains/search.md` pairs with `wiki/reference/domains/search.md`.

Reference-only domain files are invalid. The two domain trees must have identical relative file sets; the Reference-only allowance applies to cross-cutting operational pages outside `domains/`.

The generic pair is `wiki/specs/domains/<domain>.md` and `wiki/reference/domains/<domain>.md`.

Do not create a chronological history file or a standalone decision store. Git retains detailed history; important reasons stay in the relevant Spec's Intent or Rationale.

## Router And Registries

`wiki/index.md` is a short router. It must explain:

- Specs are normative and Reference is descriptive.
- Approved Spec versus code means code must change.
- Reference versus code means Reference must change.
- A new durable request requires a proposed Spec change and user approval before canonical update and implementation.
- The retrieval order starts with project memory, moves through domains and Reference, and ends at source.

`wiki/specs/index.md` is the domain registry. Give each logical domain a short responsibility. `wiki/reference/index.md` links the implementation maps and clearly identifies the paired domain directory.

## Feature Surface Inventory

Before finalizing domain candidates, build a noncanonical Feature Surface Inventory from the current checkout. Inspect:

- active user and operator UI, catalogs, commands, public APIs, routes, events, and jobs
- service branches, provider adapters, schemas, generated contracts, storage, and lifecycle state
- configuration defaults, persisted overrides, feature flags, limits, retention, and cleanup
- authentication, roles, permissions, ownership, public boundaries, audit, usage, and cost
- success, failure, interruption, cancellation, retry, and deletion paths
- exact focused tests and code-backed contract artifacts

Classify each surface as `important`, `supporting`, `placeholder`, or `excluded`. An important feature has an independently meaningful actor or entry point, permission or security boundary, data lifecycle, external provider, usage or cost effect, asynchronous or streaming behavior, or material failure semantics.

Assign every important feature to one primary proposed domain. Supporting surfaces may attach to that domain. Placeholder and excluded surfaces require an explicit exclusion reason backed by evidence. An unassigned important feature blocks completion of the proposal.

Keep this inventory in the active conversation, workflow artifact, or a temporary file outside `wiki/`. It is implementation evidence and proposal scaffolding, not approved intent.

## Domain Taxonomy

Domains are logical responsibilities and change boundaries such as authentication, users, search, documents, public access, or a processing pipeline. They do not need to match package, module, folder, or service boundaries.

One Reference domain may point to many code modules. Split domains when intent, actors, permissions, lifecycle, side effects, failure semantics, or Acceptance Criteria differ materially. Avoid broad technical domains such as backend, frontend, server, client, shared, or utilities when product responsibilities are visible.

Domain candidates may be discovered from code, but the shared taxonomy becomes normative when it is approved and written to `wiki/specs/index.md`. Renaming a canonical Spec domain therefore requires approval; its Reference counterpart follows the approved path.

## Project Memory Template

Keep `wiki/specs/project.md` short because every project session reads it.

```markdown
# Project Intent

## Purpose

## Product Priorities

## Global Intent

## Constraints

## Non-goals
```

## Domain Spec Template

```markdown
# Domain Name

## Intent

## Requirements

### Requirement: `<DOMAIN>-R001`

## Actor And Permission Requirements

## Calculation And Policy Contracts

## Domain Invariants

## Lifecycle And Side Effects

## Failure And Recovery Requirements

## Data, Retention And Audit Requirements

## Constraints

## Rationale

## Non-goals

## Acceptance Criteria

### Acceptance Criterion: `<DOMAIN>-AC001`

## Related Domains
```

Use stable requirement IDs and Acceptance Criterion IDs so agents can map implementation and verification evidence back to the approved contract without restating it in Reference. The risk-driven sections are required when applicable and may be omitted when the domain genuinely has no such behavior.

Calculation and policy contracts describe canonical dimensions, meanings, units, formulas, precedence, exclusivity, defaults, rounding, missing or invalid inputs, failure behavior, authoritative data, and hand-calculated acceptance vectors when those choices affect correctness. Internal identifiers belong in Reference unless the user explicitly approves them as a stable external contract.

Record only the current approved semantic state. Replace superseded requirements rather than accumulating a transcript. A domain Spec is sufficient only when a reviewer can determine correct behavior and verify the Acceptance Criteria without Reference or source inspection.

## Pre-approval Boundary

Inspect the current checkout before drafting any Wiki content. Record the inspected revision and the relevant working-tree state so the evidence can be checked again immediately before canonical creation.

Keep the complete Spec proposal and any internal Reference draft in the active conversation or workflow artifacts until approval. Do not create empty canonical Spec skeletons, candidate requirements under `wiki/specs/`, code-backed Reference pages, or a persistent draft tree inside the Wiki. A request to create project memory authorizes inspection and proposal; it does not approve requirements inferred from code or old prose.

**Do not write any files under `wiki/` before user approval.** Canonical placement asserts that the user approved the proposed Specs and taxonomy and authorized creation of the complete Wiki.

Exact Spec content already supplied by the user may be identified as already approved inside the proposal, but still present the complete user-facing Spec package once so the user can approve canonical creation without a second, separate Spec gate. Avoid status machinery that would force future agents to distinguish draft and approved files inside `wiki/specs/`.

## Spec Proposal And Approval

Present one complete user-facing Spec proposal with:

- the inspected revision, relevant working-tree state, and evidence scope
- the Feature Surface Inventory, its important-feature assignments, and evidence-backed exclusions
- the proposed domain taxonomy and exact complete content of the router, Spec registry, project memory, and every proposed Spec
- behaviorally complete actor, calculation, policy, invariant, lifecycle, failure, retention, audit, and Acceptance Criterion content for each applicable important feature
- candidate durable requirements inferred from code clearly separated from intent already supplied or approved by the user
- `Confirm needed` uncertainties and known Spec/code or Reference/code mismatches
- a concise statement of planned Reference coverage without requiring the user to inspect its paths, symbols, flows, or tests
- one explicit request to approve canonical creation plus the proposed Specs and taxonomy only

Approval authorizes writing the approved Specs and taxonomy and makes only that content normative. Reference is generated or refreshed separately from verified source and does not require user approval. If the user corrects an observed-state claim, verify that correction against the current code; if the correction instead states desired behavior, represent it as Spec intent and record any implementation mismatch.

Before writing, compare the current revision and relevant working-tree state with the recorded evidence snapshot. If a change affects a proposed requirement or Acceptance Criterion, re-inspect it and re-present the affected Spec content for approval. If it affects implementation evidence only, refresh Reference after approval without reopening unchanged Specs.

## Domain Reference Template

```markdown
# Domain Name

## Feature Coverage

## Entry Points

## Key Files And Symbols

## Internal Flow

## Spec Implementation Map

## Authorization Enforcement

## Invariant Enforcement

## Lifecycle Implementation

## Failure Implementation

## Usage, Cost And Audit Implementation

## Dependencies

## Contract Artifacts

## Tests Or Verification

## Pre-change Checklist

## Related Source
```

The enforcement and implementation sections are risk-driven. Include each section when a covered feature has that dimension. Otherwise omit it or write `N/A` with a concrete reason; never fill it with generic prose or desired-state policy.

Under `Feature Coverage`, name every important feature assigned by the inventory. Each feature starts with `Spec Basis` listing its stable approved requirement IDs, followed by an end-to-end feature trace covering the applicable sequence:

`user/operator surface → API method/path or event → authentication/permission/ownership/validation/limit → service branches → provider contract → persistence/lifecycle → usage/cost/audit → failure/interruption/retry/delete → exact tests`.

Every implementation claim must point to repository-root-relative paths and exact routes, symbols, models, jobs, configuration keys, or test files. `modules/jobs-image`, `normalize*Usage`, and `related tests` are examples of insufficient evidence.

`Spec Implementation Map` uses `requirement ID → current enforcement → source and test evidence → conformance or mismatch`. Authorization Enforcement and the other implementation sections explain how current code realizes the linked Spec; they never create a second permission, billing, retention, or invariant contract. Observed behavior without an approved requirement must be labeled `Observed only` or `Confirm needed` and raised as a candidate Proposed Spec Change when it should govern future work.

## Authority-Leakage Gate

Fail the authority-leakage gate when Reference is the sole location for an actor permission, calculation rule, price unit or precedence, invariant, lifecycle guarantee, failure policy, retention rule, audit meaning, or other durable behavior. Repair it by either:

- placing the exact desired behavior and testable outcome in the user-approved Spec, then linking Reference through `Spec Basis`; or
- keeping it explicitly descriptive as observed implementation when no durable requirement is approved.

Do not satisfy this gate by copying the same policy prose into both layers. Spec owns the rule; Reference owns current enforcement evidence.

## Coverage Gate

Do not present the complete proposal for approval until:

- every important inventory feature is assigned to one primary domain or explicitly excluded with evidence
- every applicable behavior-affecting decision is present in a behaviorally complete Spec with stable requirement IDs and testable Acceptance Criteria
- every assigned important feature has a complete applicable trace
- every Reference feature names its approved `Spec Basis` and maps risk-bearing behavior to current enforcement
- all cited source paths are repository-root-relative and exist in the inspected checkout
- exact routes, symbols, configuration keys, models, jobs, and test files replace wildcard or generic references
- success, failure, interruption, deletion, and retention behavior are distinguished when present
- Specs contain approved desired state only; inferred implementation facts remain in Reference or `Confirm needed`
- no durable permission, calculation, invariant, lifecycle, failure, retention, or audit rule exists only in Reference

This coverage gate measures important-feature coverage, trace completeness, and evidence specificity. Do not substitute page length, line count, token count, domain count, or file count.

## Creation Process

1. Inspect repository instructions, structure, source, configuration, manifests, routes, schemas, runtime composition, and focused tests before drafting.
2. Record the current revision, relevant working-tree state, and source evidence used for the proposal.
3. Build the Feature Surface Inventory and classify, assign, or explicitly exclude every discovered surface.
4. Identify logical domain candidates and plan paired Spec and Reference paths from important-feature responsibilities and change boundaries.
5. Gather candidate durable intent from the user and the current conversation. Treat code and older prose as prompts for confirmation, not requirement approval.
6. Draft the complete router, Spec registries, project memory, justified cross-cutting Specs, domain Specs, and taxonomy outside canonical `wiki/`.
7. Draft or plan agent-facing Reference traces internally, use them to surface candidate missing requirements, and run Spec sufficiency plus the authority-leakage gate.
8. Present only the complete Specs and taxonomy as the user-facing approval artifact and obtain one approval for canonical creation.
9. Recheck the recorded source state. Re-present only affected Spec content when desired behavior changed; refresh implementation-only evidence without reopening unchanged Specs.
10. Write the approved Specs and taxonomy, then generate paired Reference and cross-cutting maps from verified current source. Omit unapproved or empty architecture and security Specs rather than creating placeholders.
11. Link every Reference feature to requirement IDs through `Spec Basis`, then cross-link the router, registries, related domains, paired pages, and source paths.
12. Validate Spec sufficiency, authority leakage, exact domain pairing, concise always-read pages, current code paths, Reference coverage and freshness, and absence of raw history.

When regenerating a V1 or stale Wiki, preserve any demonstrably user-approved current intent. Re-propose uncertain requirement-like prose before canonicalizing it, and rebuild descriptive Reference from current source.

## Quality Bar

A useful V2 Wiki lets a user answer from Specs alone:

- Why does this project exist and where is it going?
- What must remain true for this task and why?
- What calculation, permission, invariant, lifecycle, failure, retention, and audit results define correctness?
- Which hand-computed examples and Acceptance Criteria prove conformance?

It lets an agent answer from paired Reference and source:

- Which related requirements also apply?
- Where should implementation inspection start?
- Which important feature surfaces belong to this domain, and are any unassigned?
- How does each important feature cross actors, APIs or events, permissions, providers, persistence, usage or audit, failures, and tests?
- Does current code conform to the approved contract?
- How will Acceptance Criteria be verified?

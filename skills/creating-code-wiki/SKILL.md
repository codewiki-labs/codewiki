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

Create the core structure below. Domains own product behavior. Optional policy Specs own approved rules that genuinely span domains, while optional Reference views summarize source-derived implementation across those domains.

```text
wiki/
├── index.md
├── specs/
│   ├── index.md
│   ├── project.md
│   ├── policies/               # only approved cross-domain policy
│   │   ├── architecture.md        # when approved
│   │   └── security.md            # when approved
│   └── domains/
│       └── <domain>.md
└── reference/
    ├── index.md
    ├── overview.md
    ├── coverage.json
    ├── views/                  # only applicable, useful cross-domain views
    │   ├── architecture.md
    │   └── security.md
    ├── data-flow.md
    ├── data-models.md
    ├── api-surface.md
    ├── configuration.md
    ├── dependencies.md
    ├── commands.md
    ├── testing.md
    ├── gotchas.md
    ├── glossary.md
    └── domains/
        └── <domain>.md
```

Every Spec has a corresponding Reference, but only domain pairs require identical relative paths. `wiki/specs/project.md` is paired with `wiki/reference/overview.md`; `wiki/specs/index.md` is paired with `wiki/reference/index.md`; `wiki/specs/policies/<concern>.md` is paired with `wiki/reference/views/<concern>.md`. A policy Spec therefore requires its same-named view. A source-derived view may exist without a policy Spec when it is useful and `coverage.json` identifies it; the view must label durable behavior as approved `Spec Basis`, `Observed only`, or `Confirm needed` rather than inventing policy. View-only `Spec Basis` IDs must resolve exactly in one of the concern's owning domain Specs. Other useful Reference-only operational pages do not require Specs.

**Every Spec domain has exactly one Reference domain with the same relative path.** For example, `wiki/specs/domains/search.md` pairs with `wiki/reference/domains/search.md`.

Reference-only domain files are invalid. The two domain trees must have identical relative file sets; the Reference-only allowance applies to cross-cutting operational pages outside `domains/`.

The generic pair is `wiki/specs/domains/<domain>.md` and `wiki/reference/domains/<domain>.md`.

Security is a concern, not a mandatory domain. Put authentication, authorization, ownership, public-access, secret-handling, sensitive-data, and trust-boundary requirements in the domain that owns the behavior. Create `wiki/specs/policies/security.md` only for approved rules shared by multiple domains. Create `wiki/reference/views/security.md` only when source shows an applicable project-specific security concern and a cross-domain navigation view is useful, or when the paired policy exists.

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

Assign every important feature to one primary proposed domain. Supporting features also name their owning domain but may attach to an important feature's domain trace instead of requiring an independent trace. Placeholder and excluded surfaces require an explicit exclusion reason backed by evidence. An unassigned important feature blocks completion of the proposal.

Before approval, keep this inventory in the active conversation, workflow artifact, or a temporary file outside `wiki/`. It is implementation evidence and proposal scaffolding, not approved intent. After approval, persist its source-derived coverage state in `wiki/reference/coverage.json`; that manifest is Reference evidence and does not require user approval.

## Coverage Manifest And Concern Applicability

`wiki/reference/coverage.json` makes feature closure and cross-domain concern applicability durable and machine-checkable. It must record the inspected source revision, every important feature's classification and primary domain, its exact source surfaces, and the Spec basis or evidence-backed observed/excluded reason. It must also contain explicit `security` and `architecture` concern entries.

Use `applicable` when active source contains a material project-specific boundary such as authentication, authorization, ownership, public/network exposure, untrusted input, secrets, sensitive data, privileged side effects, isolation, or a cross-domain architectural constraint. Use `not_applicable` only after inspecting those surfaces. It means no important project-specific concern was found in scope; it does not mean the project is risk-free.

Each concern records `applicability`, `owning_domains`, `policy_path`, `view_path`, `reason`, and exact `evidence`. For `not_applicable`, require a non-empty reason and evidence, leave ownership and paths empty, and omit the view and policy files. For `applicable`, name at least one owning domain. A policy path is valid only when the paired view path exists.

A complete example manifest with both concern shapes is bundled at [references/coverage-example.json](references/coverage-example.json); read it when drafting `wiki/reference/coverage.json`.

Each `surfaces` key is one of `ui`, `api`, `jobs`, `providers`, `schemas`, or `tests`, and its value is an array of repository-root-relative files. Evidence paths must exist. Important and supporting features require a primary domain plus exactly one of `spec_basis` or a concrete `observed_only_reason`; every supplied requirement ID must resolve exactly in the owning Spec. Important features require an independent paired-Reference feature trace. A supporting trace is optional, but when present its basis or observed-only label must agree with the manifest. Placeholders and exclusions require an explicit exclusion reason.

For a Git checkout, set `source_revision` to the immutable full commit ID inspected during generation. The validator permits later commits confined to `wiki/`, but marks the manifest stale when committed paths outside `wiki/` changed. It warns separately when uncommitted non-Wiki paths exist because a commit ID cannot certify those contents. For a non-Git source, use the repository's stable revision identifier and verify freshness through the available source mechanism.

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

## Security And Trust Boundaries

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

## Required Context

## See Also
```

Use stable requirement IDs and Acceptance Criterion IDs so agents can map implementation and verification evidence back to the approved contract without restating it in Reference. The risk-driven sections are required when applicable and may be omitted when the domain genuinely has no such behavior. `Required Context` lists only Specs that must also be read to determine correctness and is traversed recursively. `See Also` is nonrecursive navigation for adjacent but non-required context. Keep both selective.

## Policy Spec And Concern View Templates

Use a policy only for approved behavior that genuinely spans domains:

```markdown
# Concern Policy

## Intent

## Requirements

### Requirement: `<POLICY>-R001`

## Scope And Owning Domains

## Invariants

## Failure And Audit Requirements

## Acceptance Criteria

### Acceptance Criterion: `<POLICY>-AC001`

## Required Context

## See Also
```

Its paired source-derived view maps the policy and domain requirements to implementation without becoming another contract:

```markdown
# Concern View

## Applicability And Scope

## Owning Domains

## Spec Basis

## Entry Points And Trust Boundaries

## Enforcement Map

## Data And Secret Flow

## Failure, Audit And Verification

## Evidence
```

When no policy exists, the view may map domain requirement IDs and clearly marked observed behavior. It may not state a durable global rule as if source observation were approved intent.

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

Also report the source-derived feature inventory and concern applicability so the user can evaluate proposal completeness, but do not ask them to approve Reference prose or `coverage.json`.

Approval authorizes writing the approved Specs and taxonomy and makes only that content normative. Reference is generated or refreshed separately from verified source and does not require user approval. If the user corrects an observed-state claim, verify that correction against the current code; if the correction instead states desired behavior, represent it as Spec intent and record any implementation mismatch.

Before writing, compare the current revision and relevant working-tree state with the recorded evidence snapshot. If a change affects a proposed requirement or Acceptance Criterion, re-inspect it and re-present the affected Spec content for approval. If it affects implementation evidence only, refresh Reference after approval without reopening unchanged Specs.

## Domain Reference Template

```markdown
# Domain Name

## Feature Coverage

### Feature: `<feature_id>`

- Spec Basis: `<DOMAIN>-R001`

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

Under `Feature Coverage`, use the exact feature-heading shape shown above and match the manifest's `feature_id`. Each feature starts with `- Spec Basis:` listing its stable approved requirement IDs, or an explicit `Observed only`/`Confirm needed` label when the manifest has an observed-only reason, followed by an end-to-end feature trace covering the applicable sequence:

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
- `wiki/reference/coverage.json` accounts for every inventory feature and records evidence-backed security and architecture applicability
- every approved policy has a paired same-named view, every view is manifest-listed, and a `not_applicable` concern has neither file
- each security-relevant behavior is owned by a domain even when no global security policy exists
- recursive `Required Context` links resolve; `See Also` remains nonrecursive and selective
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
6. Draft the complete router, Spec registries, project memory, justified policy Specs, domain Specs, and taxonomy outside canonical `wiki/`.
7. Draft or plan agent-facing Reference traces internally, use them to surface candidate missing requirements, and run Spec sufficiency plus the authority-leakage gate.
8. Present only the complete Specs and taxonomy as the user-facing approval artifact and obtain one approval for canonical creation.
9. Recheck the recorded source state. Re-present only affected Spec content when desired behavior changed; refresh implementation-only evidence without reopening unchanged Specs.
10. Write the approved Specs and taxonomy, then generate paired Reference, `wiki/reference/coverage.json`, and applicable views from verified current source. Omit unapproved or empty policy Specs. Omit a concern view only when the manifest records evidence-backed `not_applicable` or when an applicable concern is completely owned and navigable through domain Reference without needing a cross-domain view.
11. Link every Reference feature to requirement IDs through `Spec Basis`, then cross-link the router, registries, `Required Context`, nonrecursive `See Also`, paired pages, and source paths.
12. Validate Spec sufficiency, authority leakage, exact domain pairing, policy and view pairing, concern applicability, typed links, current code paths, Reference coverage and freshness, and absence of raw history. Run the bundled generated-Wiki validator when available.

When migrating an older Wiki, move approved top-level `specs/security.md` or `specs/architecture.md` content into `specs/policies/` only if it is truly cross-domain policy. Move source-derived cross-domain material into `reference/views/`; domain-owned behavior stays in domain pairs. Treat Legacy `Related Domains` as one-hop input: classify each link as recursive `Required Context` or nonrecursive `See Also`, then remove the legacy section.

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

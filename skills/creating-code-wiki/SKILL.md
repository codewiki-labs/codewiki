---
name: creating-code-wiki
description: Use when initializing or substantially regenerating a repository-local Code-Wiki for persistent project memory.
---

# Creating Code-Wiki

Create a V2 Wiki from the current checkout, then obtain one user approval for the complete proposal before writing canonical project memory.

## Separate The Evidence

Use different evidence for different questions:

- Specs describe desired state and may contain only user-approved intent.
- Reference describes the current implementation and must be grounded in source code, configuration, manifests, schemas, routes, runtime composition, or runtime evidence observed during the task.
- Tests support verification paths and expected behavior candidates, but do not override active source or runtime evidence.
- Existing prose docs, comments, and an older Wiki are discovery hints. They are not automatically approved requirements or confirmed implementation facts.

Mark uncertain descriptive claims as `Confirm needed`. Do not use that label to place unapproved requirements in canonical Specs.

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

## Constraints

## Rationale

## Non-goals

## Acceptance Criteria

## Related Domains
```

Record only the current approved semantic state. Replace superseded requirements rather than accumulating a transcript.

## Pre-approval Boundary

Inspect the current checkout before drafting any Wiki content. Record the inspected revision and the relevant working-tree state so the evidence can be checked again immediately before canonical creation.

Keep the complete Wiki proposal in the active conversation or the workflow system's design artifact until approval. Do not create empty canonical Spec skeletons, candidate requirements under `wiki/specs/`, code-backed Reference pages, or a persistent draft tree inside the Wiki. A request to create project memory authorizes inspection and proposal; it does not approve requirements inferred from code or old prose.

**Do not write any files under `wiki/` before user approval.** Canonical placement asserts that the user approved the proposed Specs and taxonomy and authorized creation of the complete Wiki.

Exact Spec content already supplied by the user may be identified as already approved inside the proposal, but still present the complete creation package once so the user can approve canonical creation without a second, separate Spec gate. Avoid status machinery that would force future agents to distinguish draft and approved files inside `wiki/specs/`.

## Complete Proposal And Approval

Present one complete Wiki proposal with:

- the inspected revision, relevant working-tree state, and evidence scope
- the exact file tree and complete content of every proposed router, registry, Spec, and Reference page
- code-backed Reference facts with precise source paths, symbols, routes, jobs, models, configuration, and tests
- candidate durable requirements inferred from code clearly separated from intent already supplied or approved by the user
- `Confirm needed` uncertainties and known Spec/code or Reference/code mismatches
- one explicit request to approve canonical creation plus the proposed Specs and taxonomy

Approval authorizes writing the whole proposal and makes its exact Spec and taxonomy content normative. It does not make Reference authoritative over source. If the user corrects an observed-state claim, verify that correction against the current code; if the correction instead states desired behavior, represent it as Spec intent and record any implementation mismatch.

Before writing, compare the current revision and relevant working-tree state with the recorded evidence snapshot. If a change affects evidence used by the proposal, re-inspect it, update affected Reference facts and Spec candidates, and re-present the revised proposal for approval. Unrelated source changes do not invalidate approval.

## Domain Reference Template

```markdown
# Domain Name

## Entry Points

## Important Symbols

## Data Models

## Runtime Flow

## Tests

## Important Implementation Details

## Related Source
```

Prefer precise paths, symbols, routes, jobs, models, and test locations over encyclopedic prose. Reference should get an agent to source quickly, not replace inspection.

## Creation Process

1. Inspect repository instructions, structure, source, configuration, manifests, routes, schemas, runtime composition, and focused tests before drafting.
2. Record the current revision, relevant working-tree state, and source evidence used for the proposal.
3. Identify logical domain candidates and plan paired Spec and Reference paths.
4. Gather candidate durable intent from the user and the current conversation. Treat code and older prose as prompts for confirmation, not requirement approval.
5. Draft the exact complete Wiki outside canonical `wiki/`, including the router, registries, project memory, justified cross-cutting Specs, domain Specs, taxonomy, and every Reference page.
6. Present the complete proposal and obtain one user approval for canonical creation, proposed Specs, and taxonomy.
7. Recheck the recorded source state. When relevant evidence changed, refresh the draft and re-present the revised proposal; when it did not, continue with the approved proposal.
8. Write the approved proposal to canonical `wiki/`. Omit unapproved or empty architecture and security Specs rather than creating placeholders.
9. Cross-link the router, registries, related domains, paired Reference pages, and source paths.
10. Validate exact domain pairing, concise always-read pages, current code paths, and absence of raw history.

When regenerating a V1 or stale Wiki, preserve any demonstrably user-approved current intent. Re-propose uncertain requirement-like prose before canonicalizing it, and rebuild descriptive Reference from current source.

## Quality Bar

A useful V2 Wiki lets a future agent answer:

- Why does this project exist and where is it going?
- What must remain true for this task and why?
- Which related requirements also apply?
- Where should implementation inspection start?
- Does current code conform to the approved contract?
- How will Acceptance Criteria be verified?

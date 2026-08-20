# Code-Wiki V2 Skill Set Design

## Product Definition

Code-Wiki is repository-local persistent project memory for coding agents. It preserves user-approved current intent across sessions and connects each logical requirement domain to the current implementation.

Its layers answer different questions:

| Layer | Responsibility |
| --- | --- |
| `specs/project.md` | Why the project exists and where it is going |
| Specs | What must be true |
| Reference | Where and how the current implementation is organized |
| Code | What currently exists |

## Authority

- Approved Specs are normative over implementation.
- Source code and observed runtime state are authoritative over Reference.
- Reference is a navigation map, not a factual replacement for source inspection.
- Code changes may refresh Reference but cannot silently update Specs.
- Durable requirement changes require user approval before canonical Spec edits and implementation.

## Why The Skill Set Stays Split

Creation, memory retrieval, source tracing, canonical updates, auditing, and package maintenance occur at different times and have different failure modes. A small bootstrap skill routes among them without loading every detailed instruction for every request.

The V2 migration keeps seven skills. It changes their shared contract rather than introducing a parallel V2 router or a separate Spec-management skill.

```text
skills/
  using-code-wiki/
    SKILL.md
  creating-code-wiki/
    SKILL.md
  reading-code-wiki/
    SKILL.md
  exploring-code-with-wiki/
    SKILL.md
  updating-code-wiki/
    SKILL.md
  auditing-code-wiki/
    SKILL.md
  writing-code-wiki-skills/
    SKILL.md
```

## Skill Boundaries

| Skill | Owns | Does not own |
| --- | --- | --- |
| `using-code-wiki` | bootstrap, authority routing, durable-intent detection, sub-skill selection, closeout | detailed page writing or source tracing |
| `creating-code-wiki` | first creation, substantial regeneration, V2 structure, initial approval boundary | ordinary post-change maintenance |
| `reading-code-wiki` | always-read memory, domain registry selection, Related Domains closure | implementation truth |
| `exploring-code-with-wiki` | Reference-guided source inspection and two-direction mismatch handling | approving or inferring requirements |
| `updating-code-wiki` | approved Spec compaction and code-grounded Reference refresh | broad quality audits |
| `auditing-code-wiki` | authority, approval, taxonomy, pairing, freshness, and usefulness review | silent Spec repair |
| `writing-code-wiki-skills` | this package's boundaries, descriptions, docs, metadata, and tests | project-specific Wiki content |

## Retrieval Contract

The bootstrap and reading skills recover context in this order:

1. `wiki/index.md`
2. `wiki/specs/project.md`
3. `wiki/specs/index.md`
4. directly matched Specs
5. recursive `Related Domains` closure
6. paired Reference domains
7. relevant Reference-only pages
8. actual source and runtime evidence

Only the first two pages are always read. This protects global memory without loading the entire Wiki.

## Domain Contract

Specs and Reference share a logical domain taxonomy. Their domain trees have identical relative file sets; Reference-only domain files are invalid. A Reference domain may point to many code modules, packages, services, UI areas, models, and tests.

Every Spec has a counterpart: project pairs with overview, the registries pair with each other, architecture and security pair when their Specs exist, and domains pair by exact relative path. Operational pages such as commands, configuration, testing, dependencies, data flow, data models, API surface, gotchas, and glossary may be Reference-only.

## Feature Coverage And Deep Reference Contract

Before initial taxonomy approval, creation builds a noncanonical Feature Surface Inventory from active user and operator surfaces, routes and events, jobs and providers, schemas and persistence, configuration, security and ownership boundaries, usage and cost, failure paths, and focused tests. Each surface is classified as important, supporting, placeholder, or excluded. Every important feature has one primary proposed domain or an explicit evidence-backed exclusion; unassigned important features block the proposal.

The inventory remains in the active conversation, workflow artifact, or a temporary path outside canonical `wiki/` until approval. It is observed-state scaffolding, not approved intent.

Each important feature in a domain Reference receives an applicable end-to-end trace:

```text
user or operator surface
→ API method/path or event
→ authentication, permission, ownership, validation, and limit
→ service branches and provider contract
→ persistence, lifecycle, and side effects
→ usage, cost, and audit
→ failure, interruption, retry, deletion, and retention
→ exact tests
```

Deep Reference restores the useful operational depth of the earlier module format inside the V2 authority model: actor and permission contracts, domain invariants, lifecycle and side effects, failure semantics, dependencies, contract artifacts, verification, and pre-change guidance. Risk-driven sections are included only when supported by source; a non-applicable dimension requires a concrete reason rather than boilerplate.

The coverage gate checks important-feature assignment, trace completeness, high-risk contracts, repository-root-relative paths, and exact evidence. It does not use arbitrary page-length, line-count, token-count, domain-count, or file-count thresholds.

## Initial Creation Contract

Initial creation follows:

```text
Current checkout and relevant working-tree state
→ noncanonical Feature Surface Inventory and domain assignment
→ complete Wiki proposal outside canonical wiki/
→ coverage gate
→ one user approval for creation, Specs, and taxonomy
→ source-evidence recheck
→ canonical Wiki creation
```

The proposal contains the exact tree and complete Spec and Reference content. Nothing is written under `wiki/` before approval. If relevant evidence changes before creation, the affected proposal is refreshed and re-approved. Approval makes proposed Specs and taxonomy normative, while current source remains authoritative for Reference facts.

## Update Contract

Spec updates follow:

```text
User intent
→ exact proposed semantic change
→ user approval
→ canonical current Spec
→ implementation
→ Acceptance Criteria verification
```

Reference updates follow:

```text
Verified code or runtime change
→ affected navigation map
→ Reference refresh
```

Canonical Specs contain approved current intent only. They do not carry draft lifecycle metadata or chronological transcripts. Important rationale stays next to the relevant requirement; Git owns historical detail.

## Superpowers Boundary

Code-Wiki owns persistent WHAT, WHY, and WHERE. Superpowers owns HOW: brainstorming, planning, TDD, execution, review, and verification. The bootstrap skill composes with available workflow skills instead of duplicating them, and one-off plans do not become canonical requirements.

## Distribution Shape

The repository root is the Codex plugin package. `.codex-plugin/plugin.json` points to `./skills/`, while `.agents/plugins/marketplace.json` exposes the repository-backed plugin. The package remains skill-centered and does not declare hooks, apps, MCP servers, or visual assets that are not present.

The sync script publishes the manifest, skills, public docs, and examples while preserving destination-owned skill UI metadata.

## Validation Strategy

`scripts/validate_wiki_contract.py` checks:

- skill names, frontmatter trigger shape, and responsibility-specific V2 guidance
- public V2 concepts and removal of V1-only structure guidance
- plugin manifest fields and shared marketplace metadata
- sync regression-test presence and release version alignment

`scripts/validate_wiki_quality_fixtures.py` checks the deterministic semantic subset:

- every important fixture feature has a domain Reference trace
- every required trace dimension is present
- exact evidence cannot be replaced by vague folders, wildcard symbols, one-line flows, or generic test labels
- intentionally shallow candidates fail while complete candidates pass

`tests/skill-set-contract.md` records behavioral scenarios that are not fully captured by structural validation. Skill changes must update both deterministic checks and at least one relevant scenario.

The fixture does not prove discovery completeness or factual truth for an arbitrary repository. Creation and audit still inspect current source and apply judgment; the fixture protects the explicit coverage and output contract from regression.

Fixture-driven sync tests continue to verify payload boundaries, dry runs, dirty-tree protection, no-op convergence, and preservation of destination-owned metadata.

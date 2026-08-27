# Code-Wiki Skill Set Design

## Product Definition

Code-Wiki is repository-local persistent project memory for coding agents. It preserves user-approved current intent across sessions and connects each logical requirement domain to the current implementation.

Its layers answer different questions:

| Layer | Responsibility |
| --- | --- |
| `specs/project.md` | Why the project exists and where it is going |
| Specs | What must be true and how a user decides whether the result is correct |
| Reference | Where and how an agent finds the current implementation |
| Code | What currently exists |

## Authority

- Approved Specs are normative over implementation.
- Source code and observed runtime state are authoritative over Reference.
- Reference is a navigation map, not a factual replacement for source inspection.
- Code changes may refresh Reference but cannot silently update Specs.
- Durable requirement changes require user approval before canonical Spec edits and implementation.
- Users approve Specs and taxonomy only; source-grounded Reference is an agent-maintained map rather than part of the approval artifact.

## User And Agent Contract

Domain Specs are behaviorally complete user-facing contracts. A Spec must define every applicable actor permission, calculation and unit, policy precedence, invariant, lifecycle and failure outcome, retention and audit meaning, and observable Acceptance Criterion needed to reimplement and validate behavior without Reference. Each Spec item uses a level-three heading containing only its backticked stable ID: requirement IDs end in `-R` plus three digits, Acceptance Criterion IDs end in `-AC` plus three digits, and the parent section carries the item type. IDs remain unique within a Spec; generated-Wiki validation ignores heading-shaped fenced examples, rejects duplicate definitions, and rejects a legacy label that contradicts its ID type. These stable IDs support conformance reporting without repeating labels in every heading.

Reference is agent-facing. It maps each important feature's `Spec Basis` to current enforcement, paths, symbols, schemas, configuration, call flow, and exact tests. The replaceability rule sets the boundary: outcome-changing decisions belong in Spec; replaceable implementation details belong in Reference.

For example, canonical usage dimensions, non-overlap rules, per-million-token formulas, per-request prices, image-token versus per-image exclusivity, terminal-usage policy, ledger meaning, and hand-computed examples belong in Spec. `NormalizedLlmUsage`, provider SDK fields, normalizer function names, DB table names, and test paths belong in Reference unless explicitly approved as stable external contracts.

## Why The Skill Set Stays Split

Creation, memory retrieval, source tracing, canonical updates, auditing, and package maintenance occur at different times and have different failure modes. A small bootstrap skill routes among them without loading every detailed instruction for every request.

The current design keeps seven skills. It changes their shared contract rather than introducing a parallel router or a separate Spec-management skill.

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
| `creating-code-wiki` | first creation, substantial regeneration, current structure, initial approval boundary | ordinary post-change maintenance |
| `reading-code-wiki` | always-read memory, domain registry selection, typed context closure, concern applicability | implementation truth |
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
5. recursive `Required Context` closure and directly relevant nonrecursive `See Also`
6. `wiki/reference/coverage.json` when feature or concern evidence is needed
7. paired Reference domains and applicable policy/view pages
8. relevant Reference-only operational pages
9. actual source and runtime evidence

Only the first two pages are always read. This protects global memory without loading the entire Wiki.

## Domain Contract

Specs and Reference share a logical domain taxonomy. Their domain trees have identical relative file sets; Reference-only domain files are invalid. A Reference domain may point to many code modules, packages, services, UI areas, models, and tests.

Every Spec has a counterpart: project pairs with overview, the registries pair with each other, `specs/policies/<concern>.md` pairs with `reference/views/<concern>.md`, and domains pair by exact relative path. A source-derived view may exist without a policy only when the coverage manifest lists it and it does not create durable intent. Operational pages such as commands, configuration, testing, dependencies, data flow, data models, API surface, gotchas, and glossary may be Reference-only.

Security is a concern, not a mandatory domain. Authentication, authorization, ownership, exposure, secrets, sensitive data, and trust-boundary behavior belongs to the logical domain that owns it. A global security policy exists only for approved rules that genuinely span domains; a security view exists only when source evidence makes the concern applicable and a cross-domain map is useful, or when its paired policy requires it.

## Feature Coverage, Spec Sufficiency, And Deep Reference Contract

Before initial taxonomy approval, creation builds a noncanonical Feature Surface Inventory from active user and operator surfaces, routes and events, jobs and providers, schemas and persistence, configuration, security and ownership boundaries, usage and cost, failure paths, and focused tests. Each surface is classified as important, supporting, placeholder, or excluded. Every important feature has one primary proposed domain or an explicit evidence-backed exclusion; unassigned important features block the proposal.

The inventory remains in the active conversation, workflow artifact, or a temporary path outside canonical `wiki/` until approval. It is observed-state scaffolding, not approved intent. After approval, its verified closure persists in `wiki/reference/coverage.json` with source revision, classifications, domain assignments, exact `Spec Basis` IDs or observed-only reasons, exclusions, exact evidence, and explicit security and architecture applicability. Supporting features retain an owner and basis/reason but may attach to an important feature's domain trace rather than requiring an independent trace.

In Git repositories, `source_revision` is the immutable full commit ID inspected during generation. Freshness validation allows later Wiki-only commits and rejects committed changes elsewhere. Uncommitted non-Wiki paths produce an explicit warning because the revision cannot certify their content; source inspection remains responsible for that state.

Concern applicability is triaged from source rather than file-name convention. `applicable` records owning domains, a reason, exact evidence, and optional policy/view paths. Evidence-backed `not_applicable` records the inspected reason and evidence but has no owning domain, policy, view, or placeholder file. This is a scoped coverage statement, not an assertion that software has no risk.

Each important feature first receives behaviorally complete requirements and Acceptance Criteria in its domain Spec. Its domain Reference then receives `Spec Basis` plus an applicable end-to-end trace:

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

Deep Reference restores the useful operational depth of the earlier module format inside the authority model: authorization and invariant enforcement, lifecycle and failure implementation, usage/cost/audit implementation, dependencies, contract artifacts, verification, and pre-change guidance. Risk-driven sections are included only when supported by source; a non-applicable dimension requires a concrete reason rather than boilerplate.

The Spec sufficiency gate checks whether users can determine correct behavior without Reference. The authority-leakage gate rejects durable policy found only in Reference, including concern views. The Reference coverage gate checks important-feature assignment, `Spec Basis`, trace completeness, repository-root-relative paths, exact evidence, concern applicability, policy/view pairing, and typed links. None uses arbitrary page-length, line-count, token-count, domain-count, or file-count thresholds.

## Initial Creation Contract

Initial creation follows:

```text
Current checkout and relevant working-tree state
→ noncanonical Feature Surface Inventory and domain assignment
→ complete Spec proposal outside canonical wiki/
→ Spec sufficiency and authority-leakage gates
→ one user approval for creation, Specs, and taxonomy only
→ source-evidence recheck
→ canonical Specs plus coverage manifest and agent-facing Reference creation
```

The user-facing proposal contains the exact taxonomy and complete Spec content, not Reference prose. Nothing is written under `wiki/` before approval. If desired behavior changes before creation, affected Specs are refreshed and re-approved; implementation-only evidence refreshes Reference without reopening unchanged Specs. Approval makes proposed Specs and taxonomy normative, while current source remains authoritative for Reference facts.

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
→ affected feature or concern applicability
→ Reference, coverage manifest, and view refresh
```

Canonical Specs contain approved current intent only. They do not carry draft lifecycle metadata or chronological transcripts. Important rationale stays next to the relevant requirement; Git owns historical detail.

## Superpowers Boundary

Code-Wiki owns persistent WHAT, WHY, and WHERE. Superpowers owns HOW: brainstorming, planning, TDD, execution, review, and verification. The bootstrap skill composes with available workflow skills instead of duplicating them, and one-off plans do not become canonical requirements.

## Distribution Shape

The package has four layers, and only the outermost one is platform-specific:

| Layer | Contents | Agent coupling |
| --- | --- | --- |
| Packaging | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `scripts/install-to-kiro.sh` | Per-platform |
| Behavior | `skills/*/SKILL.md` | None |
| Core tooling | `codewiki/`, `pyproject.toml`, bundled `scripts/validate_generated_wiki.py` | None |
| Governance | Other `scripts/`, plus `tests/` and `.github/` | Repository-only |

This layering is the load-bearing invariant. Skill bodies name no agent, no CLI, no instruction file, and no tool — they reference only `wiki/**` relative paths. The Python Core is likewise adapter-neutral: the CLI and future MCP integrations consume its structured results directly. Because behavior and query logic stay platform-neutral, adding a platform does not require a fork of either layer.

The repository root is the plugin package for Codex and Claude Code and the installation source for Kiro CLI. `.codex-plugin/plugin.json` points `skills` at `./skills/` and carries Codex `interface` presentation metadata; `.agents/plugins/marketplace.json` exposes the repository-backed plugin to Codex. `.claude-plugin/plugin.json` stays minimal because Claude Code discovers `./skills/` on its own, and `.claude-plugin/marketplace.json` exposes the same repository as a one-plugin Claude Code marketplace. Shared identity fields are kept byte-identical across all four manifests; Codex-only `interface` and `policy` blocks never appear in the Claude manifests.

Kiro CLI consumes the same `SKILL.md` format without a Code-Wiki-specific manifest. `scripts/install-to-kiro.sh` copies all seven source skill directories to the documented user-level `${KIRO_HOME:-$HOME/.kiro}/skills` path or to a workspace's `.kiro/skills` path. The installer is intentionally a copy boundary rather than a second behavior tree: re-running it refreshes Code-Wiki files while unrelated skills remain untouched, and a new Kiro session loads the result.

The Codex sync script publishes the Codex manifest, skills, the shared `codewiki/` Core and CLI package metadata, the generated-Wiki validator, public docs, and examples while preserving destination-owned skill UI metadata and excluding development-only scripts and tests. The generated validator and CLI both use `codewiki.core.markdown`; adapters receive structured Core dataclasses and never invoke another adapter as a subprocess. The allowlist is opt-in, so Claude packaging files, the Kiro source-checkout installer, and repo-local governance files stay out of the Codex payload.

## Validation Strategy

`scripts/validate_wiki_contract.py` checks:

- skill names, frontmatter trigger shape, and responsibility-specific guidance
- public concepts and removal of legacy structure guidance
- plugin manifest fields and shared marketplace metadata, for both the Codex and Claude Code manifests
- that Codex-only presentation fields do not leak into the Claude Code manifests
- Kiro CLI installation paths, all-seven-skill copying, refresh behavior, and unrelated-skill preservation
- sync regression-test presence and release version alignment

`scripts/validate_wiki_quality_fixtures.py` checks the deterministic semantic subset:

- every important fixture feature has a domain Reference trace
- every important feature has paired approved Spec requirements with stable IDs and behavioral evidence
- every Reference feature maps those IDs through `Spec Basis`
- every required trace dimension is present
- exact evidence cannot be replaced by vague folders, wildcard symbols, one-line flows, or generic test labels
- intentionally shallow and authority-leakage candidates fail while complete candidates pass

`scripts/validate_generated_wiki.py` validates actual generated Wiki artifacts:

- core routers and registries plus exact Spec/Reference domain pairs
- coverage-manifest source revision, feature assignment, exclusions, exact evidence, and required concern entries
- policy/view pairing, manifest-listed view-only cases, and evidence-backed `not_applicable`
- recursive `Required Context`, nonrecursive `See Also`, and rejection of legacy ambiguous links

`tests/test_codewiki_core.py` and `tests/test_codewiki_cli.py` use a small repository fixture to check structured index/show results, bidirectional path and symbol traces, exact-ID/phrase/token/Korean search ranking, raw reads, assembled context, conservative Git freshness, file and symbol validation, parseable JSON, exit codes, root discovery, and compatibility with the generated-Wiki validator CLI.

`tests/skill-set-contract.md` records behavioral scenarios that are not fully captured by structural validation. Skill changes must update both deterministic checks and at least one relevant scenario.

The fixture does not prove discovery completeness or factual truth for an arbitrary repository. Creation and audit still inspect current source and apply judgment; the fixture protects the explicit coverage and output contract from regression.

Fixture-driven sync tests continue to verify payload boundaries, dry runs, dirty-tree protection, no-op convergence, and preservation of destination-owned metadata.

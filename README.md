# Code-Wiki V2

`code-wiki` is a Codex plugin that gives coding agents **repository-local persistent project memory**.

It preserves user-approved intent and requirements across sessions, maps those requirements to the current codebase, and keeps implementation aligned with the approved specification instead of letting code silently redefine it.

## Quickstart

Register the public marketplace and install the plugin:

```bash
codex plugin marketplace add mong3125/code-wiki
codex plugin add code-wiki@code-wiki
```

Restart Codex, open a repository, start a new thread, and ask:

```text
Create a Code-Wiki V2 for this repository.
```

The agent will inspect the current checkout, present complete proposed Specs and the domain taxonomy, and wait for one user approval before creating any files under `wiki/`. The user does not need to review Reference content.

## Problem

Agents commonly reconstruct a project's purpose, constraints, requirements, and code paths in every new session. Source inspection can recover what exists, but it cannot reliably recover why the user chose that behavior, which constraints must survive future changes, or where the project is heading.

Code-Wiki treats that missing context as project memory:

- Why the project exists
- Product priorities and global direction
- Durable requirements and non-goals
- Architecture and security invariants
- Important rationale
- Acceptance Criteria
- Navigation from each requirement domain to its implementation

It stores **current intent**, not a transcript of everything a user once said. Git retains detailed change history.

Initial creation also builds a noncanonical **Feature Surface Inventory** before the proposed taxonomy is finalized. Every important feature must be assigned to one primary domain or explicitly excluded with source-backed reasoning. A **coverage gate** blocks approval proposals that leave important features unassigned, shallow, or supported only by vague evidence.

Code-Wiki uses **spec-only approval**: users approve behaviorally complete Specs and taxonomy, while agents generate and maintain source-grounded Reference. A separate **authority-leakage gate** rejects durable permissions, calculations, pricing precedence, invariants, lifecycle guarantees, failure policy, retention, or audit meaning that appears only in Reference.

## Authority Model

Code-Wiki V2 has different authorities for different questions:

| Question | Authority | If it conflicts |
| --- | --- | --- |
| What SHOULD BE? | User-approved Specs | Change code to conform to the Spec. |
| What IS? | Source code and observed runtime state | Inspect the active implementation. |
| WHERE it is? | Reference | Refresh Reference from verified code. |

Specs are normative. Reference is descriptive.

This means:

```text
Spec != Code
→ fix Code

Reference != Code
→ fix Reference
```

Reference is a navigation layer, not a replacement for source inspection. Code changes may refresh Reference, but they never silently rewrite approved Specs.

## Wiki Structure

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

`wiki/index.md` is an authority and navigation router. `wiki/specs/index.md` is the domain registry. `wiki/specs/project.md` is short global memory that every project session reads.

### Specs

Specs preserve approved meaning and determine correctness without requiring Reference:

- Project purpose, priorities, global intent, constraints, and non-goals
- Stable requirement IDs plus domain Intent, actor permissions, calculations and policies, invariants, lifecycle and failure outcomes, retention and audit meaning, Constraints, and Rationale
- Architecture and security policies
- Non-goals and testable Acceptance Criteria, including hand-computed vectors for calculations when useful
- Minimal `Related Domains` links

Canonical Specs contain approved current requirements only. During initial creation, the complete Spec proposal stays in the active design or approval flow until accepted; no Spec, Reference, empty skeleton, or persistent draft is written under `wiki/` first. Architecture and security Specs are omitted when no corresponding global intent has been approved; empty canonical placeholders are not created.

### Reference

Agent-facing Reference maps approved domains to the current implementation:

- Important feature coverage and end-to-end traces
- Entry points and source paths
- Important symbols, routes, jobs, and data models
- `Spec Basis` links from stable requirement IDs to authorization and invariant enforcement
- Runtime flow plus lifecycle, failure, usage, cost, audit, provider, retention, cancellation, and deletion implementation when applicable
- Code-backed contract artifacts and pre-change checks
- Tests and verification locations
- Implementation details that make future inspection faster

Every Spec has a corresponding Reference: project pairs with overview, the registries pair with each other, architecture and security pair when their Specs exist, and the Spec and Reference domain trees have identical relative file sets. Reference-only domain files are invalid. A logical domain may point to many packages, services, frontend areas, and tests. Cross-cutting Reference-only pages such as commands, configuration, testing, dependencies, and glossary do not need Specs.

Deep Reference remains descriptive. It records code-backed implementation evidence without promoting observed behavior into approved intent. The creation and audit skills judge depth by important-feature coverage, complete applicable traces, `Spec Basis`, and exact evidence rather than by page length, domain count, or file count.

## Default Workflow

For project-related work, the plugin follows this retrieval and change protocol:

1. Recall `wiki/index.md` and concise `wiki/specs/project.md`.
2. Use the domain registry to find directly relevant Specs.
3. Read each selected Spec and its recursive `Related Domains` closure in full.
4. Read the paired Reference pages.
5. Follow Reference into source code and verify current behavior.
6. Decide whether the request changes durable intent.
7. If needed, draft the exact Spec change and obtain user approval.
8. Update canonical Specs, implement, and verify Acceptance Criteria.
9. Refresh Reference when verified implementation organization changed.

User-facing completion is a **Spec conformance matrix**: `requirement ID → verification result → pass or mismatch`. Agents may include source and Reference evidence when requested, but users do not need to inspect Reference to decide whether the implementation conforms.

Only the router and project memory are always read. Architecture, security, domains, and Reference pages are loaded when the task requires them.

An explicit request that supplies the exact requirement and asks for implementation counts as approval of that content. Ambiguous or conflicting durable requests require a proposed Spec change before implementation. One-off debugging commands, temporary test instructions, transient workarounds, and implementation plans are not project memory.

## With Superpowers

Code-Wiki and Superpowers have complementary responsibilities:

- **Code-Wiki:** persistent WHAT, WHY, and WHERE—project memory, approved Specs, and code navigation.
- **Superpowers:** HOW—brainstorming, planning, TDD, execution, review, and verification workflow.

Code-Wiki does not replace Superpowers or permanently store one-off implementation plans. When Superpowers is unavailable, the skills provide only a lightweight recall → inspect → approve → implement → verify → refresh sequence.

## Skills

| Skill | When to use |
| --- | --- |
| `using-code-wiki` | Bootstrap project work, recover memory, apply authority rules, and route the task. |
| `creating-code-wiki` | Create or substantially regenerate a V2 Wiki. |
| `reading-code-wiki` | Recover global intent and the smallest complete requirement-domain closure. |
| `exploring-code-with-wiki` | Follow Reference to inspect and compare current code with approved Specs. |
| `updating-code-wiki` | Apply approved Spec changes or refresh descriptive Reference. |
| `auditing-code-wiki` | Check authority, approval, domain pairing, freshness, and agent usefulness. |
| `writing-code-wiki-skills` | Maintain this package's skill boundaries, docs, metadata, and tests. |

Users do not need to explicitly say “use Code-Wiki” during ordinary repository work. The bootstrap skill checks for project memory when repository context matters.

## Examples

See [Basic workflow examples](examples/basic-workflow.md) for creation, retrieval, mismatch, approval, update, and audit scenarios.

## Manual Skills Installation

The Codex plugin is the recommended installation method. For another compatible agent or a standalone setup, copy all skill directories into that agent's skill directory:

```bash
git clone https://github.com/mong3125/code-wiki.git
cd code-wiki
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Install all skills so `using-code-wiki` can route to the supporting behaviors. The repository root is a plugin package, not a skill.

## Manage The Codex Plugin

### Update

```bash
codex plugin marketplace upgrade code-wiki
codex plugin add code-wiki@code-wiki
```

Restart Codex and start a new thread so the current skills are loaded.

### Remove

```bash
codex plugin remove code-wiki@code-wiki
codex plugin marketplace remove code-wiki
```

Removing the plugin does not delete project `wiki/` directories.

### Troubleshooting

```bash
codex plugin marketplace list
codex plugin list --available
```

If an installed plugin was updated while Codex was running, restart Codex and begin a new thread.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for skill boundaries, V2 contract expectations, and local validation.

## License

MIT. See [LICENSE](LICENSE).

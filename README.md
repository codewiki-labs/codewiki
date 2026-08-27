# Code-Wiki V2

`code-wiki` gives coding agents **repository-local persistent project memory**. It ships as both a Codex plugin and a Claude Code plugin, and the same seven agent-neutral skills install directly into Kiro CLI.

It preserves user-approved intent and requirements across sessions, maps those requirements to the current codebase, and keeps implementation aligned with the approved specification instead of letting code silently redefine it.

## Quickstart

Use the installation method for your coding agent.

**Codex plugin**

```bash
codex plugin marketplace add codewiki-labs/codewiki
codex plugin add code-wiki@code-wiki
```

**Claude Code plugin** — run these inside Claude Code:

```text
/plugin marketplace add codewiki-labs/codewiki
/plugin install code-wiki@code-wiki
```

**Kiro CLI skills** — clone this repository and install for the current user:

```bash
git clone https://github.com/codewiki-labs/codewiki.git
cd codewiki
./scripts/install-to-kiro.sh
```

The Kiro installer uses `${KIRO_HOME:-$HOME/.kiro}/skills`. For one workspace only, use `./scripts/install-to-kiro.sh --project /path/to/project`, which installs under `/path/to/project/.kiro/skills`. Re-run the installer from an updated checkout to refresh Code-Wiki without changing unrelated Kiro skills.

Then start a fresh session in a repository and ask:

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
- Domain-owned architecture, security, and trust-boundary invariants
- Important rationale
- Acceptance Criteria
- Navigation from each requirement domain to its implementation

It stores **current intent**, not a transcript of everything a user once said. Git retains detailed change history.

Initial creation also builds a noncanonical **Feature Surface Inventory** before the proposed taxonomy is finalized. Every important feature must be assigned to one primary domain or explicitly excluded with source-backed reasoning. After approval, this source-derived state is persisted in `reference/coverage.json`. A **coverage gate** blocks approval proposals that leave important features unassigned, shallow, or supported only by vague evidence.

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
│   ├── policies/               # approved cross-domain policy only
│   │   ├── architecture.md
│   │   └── security.md
│   └── domains/
│       └── <domain>.md
└── reference/
    ├── index.md
    ├── overview.md
    ├── coverage.json
    ├── views/                  # applicable source-derived views
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

`wiki/index.md` is an authority and navigation router. `wiki/specs/index.md` is the domain registry. `wiki/specs/project.md` is short global memory that every project session reads.

### Specs

Specs preserve approved meaning and determine correctness without requiring Reference:

- Project purpose, priorities, global intent, constraints, and non-goals
- Compact ID-only level-three headings for stable requirement (`-Rddd`) and Acceptance Criterion (`-ACddd`) IDs, plus domain Intent, actor permissions, calculations and policies, invariants, lifecycle and failure outcomes, retention and audit meaning, Constraints, and Rationale
- Approved cross-domain policy under `specs/policies/` only when the rule genuinely spans domains
- Non-goals and testable Acceptance Criteria, including hand-computed vectors for calculations when useful
- Recursive `Required Context` links and nonrecursive `See Also` links

Canonical Specs contain approved current requirements only. During initial creation, the complete Spec proposal stays in the active design or approval flow until accepted; no Spec, Reference, empty skeleton, or persistent draft is written under `wiki/` first. Security is a concern, not a mandatory domain: authentication, authorization, ownership, exposure, secrets, sensitive data, and trust boundaries live in their owning domain Specs. Empty global policy placeholders are not created.

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

Every Spec has a corresponding Reference: project pairs with overview, the registries pair with each other, policies pair with same-named views, and the Spec and Reference domain trees have identical relative file sets. Reference-only domain files are invalid. A logical domain may point to many packages, services, frontend areas, and tests. Cross-cutting Reference-only views and operational pages such as commands, configuration, testing, dependencies, and glossary do not otherwise need Specs.

Policy and view pairing is asymmetric by design: `specs/policies/<concern>.md` always requires `reference/views/<concern>.md`, while a source-derived view may exist without a policy when `coverage.json` lists it and the view does not invent durable intent. The manifest records every feature assignment plus explicit security and architecture applicability. Evidence-backed `not_applicable` means no important project-specific concern was found in the inspected scope, so no placeholder policy or view is required.

Deep Reference remains descriptive. It records code-backed implementation evidence without promoting observed behavior into approved intent. The creation and audit skills judge depth by important-feature coverage, complete applicable traces, `Spec Basis`, and exact evidence rather than by page length, domain count, or file count.

## Default Workflow

For project-related work, the plugin follows this retrieval and change protocol:

1. Recall `wiki/index.md` and concise `wiki/specs/project.md`.
2. Use the domain registry to find directly relevant Specs.
3. Read each selected Spec and its recursive `Required Context` closure in full; follow `See Also` only when directly relevant and never recursively.
4. Consult `reference/coverage.json` for feature or concern applicability, then read paired domains and manifest-listed views needed by the task.
5. Follow Reference into source code and verify current behavior.
6. Decide whether the request changes durable intent.
7. If needed, draft the exact Spec change and obtain user approval.
8. Update canonical Specs, implement, and verify Acceptance Criteria.
9. Refresh Reference, coverage evidence, and applicable views when verified implementation organization changed.

User-facing completion is a **Spec conformance matrix**: `requirement ID → verification result → pass or mismatch`. Agents may include source and Reference evidence when requested, but users do not need to inspect Reference to decide whether the implementation conforms.

Only the router and project memory are always read. Policies, domains, coverage, views, and operational Reference pages are loaded when the task requires them.

## CLI And Core

The repository also provides a read-only `codewiki` CLI backed by a reusable Python Core. Install it from a checkout with Python 3.10 or newer:

```bash
python3 -m pip install .
codewiki --version
```

Run commands from any directory inside a repository that contains `wiki/index.md`, or pass an explicit root before the command with `codewiki --repo-root /path/to/project ...`.

```bash
codewiki index
codewiki search "quiz validation"
codewiki show QUIZ-R001
codewiki trace QUIZ-R001
codewiki trace src/services/quiz.py
codewiki trace symbol:QuizService.createQuiz
codewiki read specs/domains/quiz.md
codewiki context QUIZ-R001
codewiki status
codewiki validate
codewiki validate QUIZ-R001
codewiki doctor
codewiki serve
```

`trace` explores recorded Spec-to-code relationships in either direction. `context` combines the matched Spec entities, related Acceptance Criteria or Requirements, Wiki documents, implementation references, and bounded source excerpts for an agent starting work. `read` emits the requested Markdown unchanged in human mode.

### Web Viewer

Start the read-only, Spec-first viewer from any directory inside a CodeWiki repository:

```bash
codewiki serve                         # http://127.0.0.1:8000
codewiki serve --open
codewiki serve --port 8080
codewiki serve --host 0.0.0.0
```

The viewer has three primary areas:

- **Overview** presents Specs, Requirement and Acceptance Criterion counts, trace coverage, unlinked entities, validation, and Wiki synchronization state.
- **Explorer** keeps the functional Spec index, structured Requirement/Acceptance Criterion content, implementation references, bounded source excerpts, related tests, and a selected-entity Local Trace Map in one three-pane view.
- **Changes** maps Git-reported changed files to recorded affected Spec entities and explicitly reports `unknown` rather than inferring impact.

The header search uses the same deterministic Core lexical search as `codewiki search`; selecting a Requirement, Acceptance Criterion, or Spec document opens it in Explorer. The bundled frontend has no Markdown parser, search index, graph database, or write API. It calls the reusable Core through read-only JSON endpoints under `/api/` (`index`, `spec`, `trace`, `context`, `search`, `status`, `validate`, `read`, and `doctor`).

The interface supports English and Korean. On the first visit it follows the browser's preferred language (`ko` selects Korean); the language selector in the header stores an explicit choice in local browser storage. Spec text, identifiers, paths, Core diagnostic evidence, and source excerpts remain in their recorded language instead of being machine-translated.

The default bind address is localhost. `--host 0.0.0.0` deliberately exposes the unauthenticated read-only viewer—and its traced source excerpts—to the surrounding network, so use it only on a trusted network.

Append `--json` to any subcommand for one parseable JSON value with no ANSI or human formatting:

```bash
codewiki show QUIZ-R001 --json
codewiki trace src/services/quiz.py --json
codewiki search "quiz validation" --json
codewiki context QUIZ-R001 --json
```

An empty search is a successful empty result. Human-readable errors go to stderr; JSON errors are a single object on stdout. Exit status `1` means validation or doctor findings, `2` means initialization or usage failure, `3` means a target or document was not found, and `4` means invalid Wiki data.

The CLI contains no parsing or trace logic. Python integrations, including a future MCP adapter, import the same structured Core directly instead of invoking a subprocess:

```python
from codewiki import CodeWiki

wiki = CodeWiki.open(repo_root="/path/to/project")
result = wiki.get_context("QUIZ-R001")
payload = result.to_dict()
```

The v1 lexical search is deterministic and in-memory: exact IDs rank before exact paths or symbols, then title or phrase matches, all query tokens, and partial token matches. `status` uses `reference/coverage.json` and Git when available; it reports `unknown` rather than guessing when freshness cannot be established. `validate` checks structural trace links, referenced files, and lexically verifiable symbols without calling an LLM or building a source index.

## Generated-Wiki Validator

The plugin ships a **generated-Wiki validator** for exact domain pairs, policy/view pairing, manifest evidence, concern applicability, and typed links. From a Code-Wiki checkout or installed plugin root, point it at the target repository:

```bash
python3 scripts/validate_generated_wiki.py \
  --repo-root /path/to/project \
  --wiki-root /path/to/project/wiki
```

For Git repositories, `source_revision` is an immutable full commit ID. Later Wiki-only commits remain valid, while committed non-Wiki changes make coverage stale; uncommitted source produces a warning because it is outside the commit snapshot. This structural and semantic gate does not replace source inspection or product tests.

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

A plugin install is the recommended method. For another compatible agent or a standalone setup, copy all skill directories into that agent's skill directory:

```bash
git clone https://github.com/codewiki-labs/codewiki.git
cd codewiki

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"

# Kiro CLI, for the current user
mkdir -p "${KIRO_HOME:-$HOME/.kiro}/skills"
cp -R skills/* "${KIRO_HOME:-$HOME/.kiro}/skills/"

# Kiro CLI, for one project only
mkdir -p /path/to/project/.kiro/skills
cp -R skills/* /path/to/project/.kiro/skills/

# Claude Code, for every project
mkdir -p "$HOME/.claude/skills"
cp -R skills/* "$HOME/.claude/skills/"

# Claude Code, for one project only
mkdir -p /path/to/project/.claude/skills
cp -R skills/* /path/to/project/.claude/skills/
```

Install all skills so `using-code-wiki` can route to the supporting behaviors. The repository root is a plugin package, not a skill.

Skills-only installation does not copy the bundled validator. Keep the cloned checkout when you want to run `scripts/validate_generated_wiki.py`, or install the full plugin payload.

## Manage The Plugin

### Update

Codex:

```bash
codex plugin marketplace upgrade code-wiki
codex plugin add code-wiki@code-wiki
```

Claude Code:

```text
/plugin marketplace update code-wiki
/plugin update code-wiki
```

Kiro CLI — update the source checkout, then refresh the copied skills:

```bash
git -C /path/to/codewiki pull --ff-only
/path/to/codewiki/scripts/install-to-kiro.sh
```

Start a new session so the current skills are loaded.

### Remove

Codex:

```bash
codex plugin remove code-wiki@code-wiki
codex plugin marketplace remove code-wiki
```

Claude Code:

```text
/plugin uninstall code-wiki
/plugin marketplace remove code-wiki
```

Kiro CLI — remove only the seven Code-Wiki skill directories:

```bash
kiro_skills="${KIRO_HOME:-$HOME/.kiro}/skills"
for skill in using-code-wiki creating-code-wiki reading-code-wiki exploring-code-with-wiki updating-code-wiki auditing-code-wiki writing-code-wiki-skills; do
  rm -rf "$kiro_skills/$skill"
done
```

Removing the plugin or skills does not delete project `wiki/` directories.

### Troubleshooting

Codex:

```bash
codex plugin marketplace list
codex plugin list --available
```

Claude Code:

```bash
claude plugin list
claude plugin details code-wiki
```

Kiro CLI: begin a new chat session after installing and use `/context show` to confirm that all seven files under the global or workspace `skills` path are loaded. Invoke `/using-code-wiki` to bootstrap directly.

`claude plugin details code-wiki` should list all seven skills. If an installed plugin or copied skill was updated while the agent was running, run `/reload-plugins` in Claude Code or restart Codex or Kiro CLI, then begin a new session.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for skill boundaries, V2 contract expectations, and local validation.

## License

MIT. See [LICENSE](LICENSE).

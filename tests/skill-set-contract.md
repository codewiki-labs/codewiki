# Code-Wiki V2 Skill Set Contract

This file records behavioral scenarios for the package. `scripts/validate_wiki_contract.py` enforces the deterministic structural subset.

## Scenario: Project Work Without An Explicit Code-Wiki Mention

User asks:

```text
Fix the failing authentication test in this repository.
```

Expected selection:

- `using-code-wiki`
- `reading-code-wiki` if a Code-Wiki exists
- `exploring-code-with-wiki` when source inspection is needed

Required behavior:

- Check for project memory before broad code search.
- Read `wiki/index.md` and concise `wiki/specs/project.md` first.
- Identify relevant domains from `wiki/specs/index.md`.
- Read matched Specs and their recursive `Required Context` closure in full; follow `See Also` only when directly relevant and never recursively.
- For a feature, architecture, permission, or security task, inspect `reference/coverage.json` for applicability, owning domains, policy paths, and view paths.
- Read paired Reference domains and only the manifest-listed cross-domain views needed by the task, then inspect source.
- Do not require a security policy, security view, or security domain when the concern is evidence-backed `not_applicable` or fully owned and traced by domains.
- For implementation or bug-fix work, include `reference/testing.md` unless selected domains already provide complete verification paths.
- Before completion, verify the implementation against approved Acceptance Criteria and refresh stale Reference.

## Scenario: First V2 Wiki

User asks:

```text
Create a Code-Wiki for this project.
```

Expected selection:

- `creating-code-wiki`

Required behavior:

- Inspect the current checkout before drafting any Wiki content, including repository instructions, source, configuration, manifests, routes, schemas, runtime composition, and focused tests.
- Record the inspected revision and relevant working-tree state so the proposal can be checked for source drift before it is written.
- Derive Reference from current source code, configuration, runtime evidence, and nearby tests.
- Build one complete Spec proposal outside canonical `wiki/`, including the exact taxonomy and complete router, Spec registry, project memory, and domain Spec content.
- Distinguish code-backed Reference facts from candidate durable requirements inferred from code; inferred behavior becomes normative only through approval as Spec content.
- Present the complete Spec proposal for one user approval covering canonical creation and the proposed Specs and taxonomy; do not require Reference review.
- Do not write any files under `wiki/` before user approval, including empty skeletons, Reference pages, or persistent drafts.
- If source drift changes proposed desired behavior, re-present the affected Spec content; if it changes implementation evidence only, refresh Reference without reopening unchanged Specs.
- After approval, write the approved Specs and taxonomy, then generate source-grounded Reference into the paired `specs/` and `reference/` structure.
- Pair every `specs/domains/<domain>.md` with exactly one `reference/domains/<domain>.md`.
- Pair `specs/project.md` with `reference/overview.md`, pair the two indexes, pair every `specs/policies/<concern>.md` with `reference/views/<concern>.md`, and allow a manifest-listed descriptive view without a policy.
- Keep `specs/project.md` short enough to read every session.
- Store important rationale beside its requirement.
- Do not create a chronological conversation/change history or a separate ADR store.
- Treat the proposed domain taxonomy as part of the Spec set the user approves; descriptive Reference scaffolding alone is not requirement approval.
- Treat security as a concern owned by domains, not a mandatory domain. Create a global policy only for approved cross-domain intent.
- Generate `reference/coverage.json` and any applicable cross-domain views from current source; omit placeholder policy and view files for evidence-backed `not_applicable` concerns.

## Scenario: Feature Surface Coverage During Creation

Given a repository with an active user tool, an administrator configuration surface, provider usage normalization, persistence, and permission guards, required behavior is:

- Build a noncanonical Feature Surface Inventory before finalizing the domain taxonomy.
- Inspect user and operator UI or catalogs, routes and events, services and providers, persistence and lifecycle, configuration and defaults, authentication and ownership, limits and usage or audit boundaries, failures and cancellation, and focused tests.
- Classify each discovered surface as important, supporting, placeholder, or excluded.
- Assign every important feature to one primary domain or provide an explicit evidence-backed exclusion reason.
- Treat any unassigned important feature as a creation blocker.
- Keep the inventory outside canonical `wiki/` until the complete proposal is approved.
- After approval, persist its source-derived feature assignments, exact evidence, exclusions, source revision, and security and architecture applicability in `reference/coverage.json`.
- Use an immutable full Git commit ID for `source_revision`; allow later Wiki-only commits, reject committed non-Wiki changes, and warn that uncommitted source requires separate inspection.

## Scenario: Spec-Only User Approval

The user wants to review and approve only durable product behavior, while Reference remains an agent-facing implementation map.

Required behavior:

- Present the complete proposed Specs and domain taxonomy as the user-facing approval artifact.
- Do not require the user to read or approve Reference content.
- Make each domain Spec behaviorally complete enough to reimplement and validate its actor permissions, calculation and policy rules, invariants, lifecycle, failures, audit or retention semantics, and observable Acceptance Criteria without reading Reference.
- Give normative requirements stable requirement IDs so implementation and verification evidence can map back without restating the policy in Reference.
- Generate or refresh Reference from verified source after Spec approval; Reference freshness remains an agent quality gate rather than a user approval gate.

## Scenario: Usage Calculation Is Normative

Given provider-specific cache tokens, image tokens, web-search counts, per-token prices, and per-request prices, required behavior is:

- Put canonical usage dimensions, non-overlap rules, calculation units, pricing formulas, precedence and exclusivity, terminal-failure handling, authoritative-ledger semantics, and hand-computed acceptance vectors in the approved Spec.
- Keep provider SDK field names, internal type and function names, source paths, table and column names, call flow, and exact test paths in Reference unless the user explicitly makes one a stable external contract.
- Ensure the Spec alone determines whether 300 cache-write tokens at 1 USD per million cost 0.0003 USD and whether image-token pricing excludes duplicate per-image charging.
- Treat a calculation or billing rule found only in Reference as authority leakage and a candidate Proposed Spec Change, not as approved behavior.

## Scenario: Agent-Facing Reference Mapping

Given an approved Spec and current implementation, required behavior is:

- Map each important Reference feature to its approved requirement IDs under `Spec Basis`.
- Describe current enforcement under implementation-shaped sections such as Authorization Enforcement, Invariant Enforcement, Lifecycle Implementation, Failure Implementation, and Usage, Cost And Audit Implementation.
- Use paths, symbols, routes, schemas, configuration, and exact tests as implementation evidence rather than repeating the desired rule as a second contract.
- Report conformance as `requirement ID → implementation evidence → verification result → mismatch` so the user can review Spec conformance without reading Reference.
- Allow observed implementation with no approved requirement only when labeled as observed state or `Confirm needed`; never let it silently become normative.

## Scenario: Deep Domain Reference

Given an important feature assigned to a domain, required behavior is:

- Trace its user or operator surface to its API method, route, or event contract.
- Record authentication, role, permission, ownership, validation, and limit enforcement when applicable.
- Trace service branches, provider contracts, persistence and lifecycle, usage, cost and audit, failure, interruption, retry and deletion semantics, and exact tests when applicable.
- Use repository-root-relative source paths, exact symbols, exact routes, and exact test files.
- Link each risk-bearing trace to stable approved requirement IDs under `Spec Basis`.
- Mark a trace dimension `N/A` only with a concrete reason.
- Reject wildcard symbols, vague folder references, generic test labels, and one-sentence flows as sufficient evidence for important features.
- Keep approved desired behavior in Specs and code-backed implementation detail in Reference.

## Scenario: Session Recall And Domain Closure

User asks:

```text
Change the public search permission behavior.
```

Expected selection:

- `using-code-wiki`
- `reading-code-wiki`

Required behavior:

- Always recover project purpose, priorities, global intent, constraints, and non-goals from `specs/project.md`.
- Use the domain registry to match `public` and `search`.
- Recursively follow each selected Spec's `Required Context`, such as `auth-and-current-user` or `roles-and-permissions`.
- Read `See Also` pages only when directly relevant and do not recurse through them.
- Deduplicate the closure and read every selected Spec in full before Reference or source.
- Read `reference/coverage.json`, the owning security-relevant domains, and `reference/views/security.md` only when the manifest lists it. Read `specs/policies/security.md` too when an approved global policy applies.
- Read each paired domain Reference and the relevant testing map before inspecting the scoped source paths.

## Scenario: Targeted Source Inspection

User asks:

```text
Use the Code-Wiki to inspect the smallest code path for document ingestion.
```

Expected selection:

- `exploring-code-with-wiki`

Required behavior:

- Start with the paired Reference domain's entry points, symbols, runtime flow, data models, tests, and implementation details.
- Follow concrete source paths instead of treating Reference prose as implementation truth.
- Expand only through named callers, dependencies, schemas, routes, jobs, or tests.
- If source tracing reveals an undocumented logical domain, load its approved Spec before making decisions in that domain and record the missing `Required Context`, `See Also`, coverage-manifest assignment, or Reference link.

## Scenario: Approved Spec Conflicts With Code

Given:

```text
The approved upload Spec says the limit is 200 MB, but code enforces 100 MB.
```

Required behavior:

- Treat the approved Spec as the authority for desired behavior.
- Report the mismatch.
- Change and verify the implementation against the Spec's Acceptance Criteria when implementation is in scope.
- Do not rewrite the Spec to 100 MB merely because that is what code currently does.

## Scenario: Reference Conflicts With Code

Given:

```text
Reference points to an old upload validator, but the active route calls a new validator.
```

Required behavior:

- Treat current source code as authority for implementation state.
- Inspect the active route and validator.
- Refresh Reference paths, symbols, and flow to match verified code.
- Do not infer a requirement change from this descriptive correction.

## Scenario: Deep Reference Refresh

When verified implementation changes an important feature surface, required behavior is:

- Refresh the affected feature coverage and end-to-end trace from current source.
- Update actor or permission, invariant, lifecycle, failure, usage or cost, contract-artifact, and verification details that changed.
- Preserve the approved Spec unless the user separately approved a durable requirement change.
- Re-run the coverage gate for the affected domain and its cross-domain trace before closeout.

## Scenario: New Durable Requirement

User asks:

```text
All future document exports must preserve the original filename.
```

Expected selection:

- `using-code-wiki`
- `updating-code-wiki` after approval

Required behavior:

- Recognize a durable requirement that changes canonical intent.
- Draft the exact affected Spec changes, including rationale and Acceptance Criteria where relevant.
- Obtain user approval.
- Update canonical Specs only after approval, then implement and verify.

## Scenario: Exact Spec Is Already Approved In The Request

User asks:

```text
Set the approved upload limit requirement to exactly 200 MB and implement it.
```

Required behavior:

- Treat the explicit exact content plus implementation instruction as approval of that content.
- Update the canonical Spec, implement it, and verify its Acceptance Criteria without asking the user to approve the same wording again.

## Scenario: Underspecified Durable Requirement

User asks:

```text
Increase the upload size.
```

Required behavior:

- Recognize a candidate durable requirement but not an exact approved semantic state.
- Inspect existing Specs and current implementation only to establish context, not to guess the target.
- Resolve the target, unit, scope, constraints, and acceptance meaning through one concise question or an exact proposal.
- Obtain user approval before editing canonical Specs or implementing a guessed limit.
- Do not treat instruction priority as approval of missing semantics.

## Scenario: Read-Only Mismatch Audit

User asks:

```text
Audit Spec/code and Reference/code mismatches. Do not edit anything.
```

Required behavior:

- Apply the authority rules to classify each mismatch.
- Report code changes needed for Spec conformance and Reference refreshes needed for stale navigation.
- Do not edit source, Specs, or Reference; mismatch direction does not expand the requested scope.

## Scenario: Ephemeral Request

User asks:

```text
Run the upload test once with extra debug logging.
```

Required behavior:

- Do not store the one-off debugging procedure as durable project intent.
- Do not edit Specs.
- Refresh Reference only if the task reveals a durable implementation fact or stale navigation.

## Scenario: Semantic Compaction

Given:

```text
An approved Spec once said 100 MB and now says 200 MB.
```

Required behavior:

- Canonical Specs retain the current 200 MB requirement.
- Preserve only useful current rationale, such as support for large scanned documents.
- Do not keep a chronological requirement transcript in the Wiki; Git owns detailed history.

## Scenario: Oversized Wiki Page

Given:

```text
wiki/specs/domains/billing.md has grown to 340 lines; wiki/reference/commands.md has grown to 260 lines.
```

Expected selection:

- `auditing-code-wiki` when discovered during an audit
- `updating-code-wiki` when discovered while completing project work

Required behavior:

- Treat each page larger than 200 lines as an oversize signal that triggers review; size is a review trigger, not an authority.
- Do not edit either page first: present an oversize report naming each page, its line count, what inflates it, the meaning units involved, and a recommended repair.
- Ask the user to choose per page: review the compaction together, split the domain, delegate to the agent, or accept the size.
- For the oversized Spec domain, the user's recorded choice is the approval; without it, do not edit the canonical file.
- Under delegation, inventory the page into discrete meaning units, classify each as keep, merge, or drop, and drop only source-restated, superseded, duplicated, or historical content.
- Size alone never deletes an approved requirement; a unit whose meaning would have to change becomes a Proposed Spec Change instead of being compacted.
- Report the kept, merged, and dropped dispositions in the closeout.
- A domain split maintains exact Spec/Reference pairing at the same relative paths and updates both registries.

## Scenario: Domain Pairing Audit

User asks:

```text
Audit this Code-Wiki for reliable future-agent use.
```

Expected selection:

- `auditing-code-wiki`

Required behavior:

- Check that every Spec domain has exactly one Reference domain at the same relative path.
- Reject orphan files in either domain tree; Reference-only domain files are invalid.
- Check project-to-overview, index-to-index, and policy-to-view counterparts so every Spec has a corresponding Reference.
- Allow a source-derived cross-domain view without a policy only when the coverage manifest lists it, every `Spec Basis` ID resolves exactly in an owning domain Spec, and observed-only content is explicitly labeled instead of creating durable intent; allow operational pages such as commands, testing, dependencies, and glossary.
- Check that domain taxonomy describes logical change boundaries rather than mirroring source modules.
- Check authority direction, approval integrity, current-intent compaction, concise always-read memory, and source-navigation quality.
- Inventory every Wiki file so noncanonical history, draft, or decision stores cannot escape the audit.
- Treat canonical placement as an approval assertion, while flagging visible draft markers or disputed provenance instead of inventing lifecycle metadata.
- Classify findings as desired-state, observed-state, or Wiki contract/representation defects.
- Report durable-intent approval and mutation authorization separately.

## Scenario: Coverage And Trace Audit

Given a structurally valid Wiki whose domain pairs and links are correct but whose active image, summary, poster, usage-accounting, or permission features are missing or shallow, required behavior is:

- Reconstruct a risk-weighted Feature Surface Inventory from current UI or catalogs, routes, jobs, providers, schemas, guards, configuration, persistence, and focused tests.
- Compare important source features with registry assignments and domain Reference coverage.
- Compare the reconstructed inventory with `reference/coverage.json`, including its recorded source revision, exact evidence, exclusions, and concern applicability.
- Report unassigned important features, incomplete traces, vague evidence, and missing high-risk contracts as Wiki contract or representation defects.
- Treat symbol presence without field mappings, formulas, precedence, lifecycle, failure, or tests as insufficient evidence.
- Do not repair Specs from source behavior and do not mutate any file during a read-only audit.

## Scenario: Security Is Not Applicable

Given a local-only utility with no authentication, authorization, ownership boundary, public or network exposure, secrets, sensitive data, untrusted input, or privileged side effect, required behavior is:

- Inspect the relevant entry points, configuration, data flow, and tests rather than assuming absence from file names.
- Record `security.applicability` as `not_applicable` in `reference/coverage.json` with a non-empty reason and exact repository-root-relative evidence.
- Leave `owning_domains`, `policy_path`, and `view_path` empty and omit `specs/policies/security.md` plus `reference/views/security.md`.
- Treat `not_applicable` as an evidence-backed scoped finding, not a claim that the project is risk-free.

## Scenario: Domain-Owned Security

Given authentication, authorization, ownership, or trust-boundary behavior that belongs to one or more product domains but has no approved global rule, required behavior is:

- Put the durable requirements and Acceptance Criteria in the owning domain Specs under Security And Trust Boundaries and related risk-driven sections.
- Map current enforcement in the paired domain Reference and list owning domains plus exact evidence in `reference/coverage.json`.
- Do not create a mandatory `security` domain or `specs/policies/security.md` placeholder.
- Create `reference/views/security.md` only when a cross-domain source map materially improves navigation; if created, list it in the manifest and keep unapproved observations descriptive.

## Scenario: Global Security Policy And View

Given an approved security rule that genuinely spans multiple domains, required behavior is:

- Store the normative rule, scope, stable IDs, invariants, failure or audit meaning, and Acceptance Criteria in `specs/policies/security.md`.
- Create the paired `reference/views/security.md` and map the policy plus owning-domain requirement IDs to exact current enforcement and verification evidence.
- Record both paths, owning domains, applicability reason, and exact evidence in `reference/coverage.json`.
- Reject a policy without its paired view and reject durable policy that exists only in the view as authority leakage.

## Scenario: Typed Domain Retrieval

Given Specs that cross-link multiple domains, required behavior is:

- Recursively traverse `Required Context`, deduplicate cycles, and read the complete resulting Spec closure.
- Treat `See Also` as nonrecursive navigation and load only directly relevant pages.
- Treat Legacy `Related Domains` as one-hop migration input, classify every link into one of the typed sections, and report the stale representation.
- Reject broken required links and excessive context expansion caused by recursive adjacency links.

## Scenario: Generated-Wiki Artifact Validation

Given a generated repository-local Wiki, required behavior is:

- Run the bundled `scripts/validate_generated_wiki.py` with `--repo-root <repository-root> --wiki-root <repository-root>/wiki`.
- Reject missing core files, unequal domain trees, invalid policy/view pairing, missing manifest evidence, unresolved feature traces or `Spec Basis`, inconsistent security or architecture applicability, broken typed links, and Legacy `Related Domains`.
- Accept an evidence-backed securityless Wiki, domain-owned security without a global policy, a manifest-listed view without a policy, and a paired approved global policy/view.
- Run the semantic authority-leakage fixture separately to reject durable policy that appears only in a view.
- Treat validator success as Wiki-contract evidence only; still inspect source and run product verification for implementation claims.

## Scenario: Source And Runtime Disagree

Given:

```text
Checked-out source says one thing, but a running deployment behaves differently.
```

Required behavior:

- Verify deployed revision, configuration, feature flags, migrations, and environment before drawing a conclusion.
- Treat repository source and observed runtime as two scoped observations rather than silently choosing one.
- Keep Reference for the checked-out repository grounded in source; record verified environment-specific divergence explicitly when useful.
- Do not infer a Spec change from either observed state.

## Scenario: Superpowers Is Available

Given:

```text
The environment provides Superpowers workflow skills.
```

Required behavior:

- Code-Wiki supplies persistent WHAT, WHY, and WHERE context.
- Superpowers owns HOW: brainstorming, planning, TDD, execution, review, and verification workflow.
- Code-Wiki does not persist one-off implementation plans as project requirements.
- Approved Spec changes remain the implementation contract used by the workflow.
- Invoke required Superpowers process skills first, recover Code-Wiki context during their project exploration before design decisions, and use one semantically identical approval artifact for both systems rather than duplicating approval gates.

## Scenario: Superpowers Is Not Available

Required behavior:

- Use the lightweight sequence: recall memory, find domains, read Specs, read Reference, inspect code, obtain approval for Spec changes, implement, verify, refresh Reference.
- Do not invent a competing full development-workflow system inside Code-Wiki.

## Scenario: Skill Maintenance

User asks:

```text
Change how Code-Wiki approves requirement updates.
```

Expected selection:

- `writing-code-wiki-skills`

Required behavior:

- Preserve the seven distinct skill boundaries unless split criteria justify a change.
- Update validator expectations and at least one behavioral scenario.
- Test both authority mismatch directions and the approval gate.
- Keep every skill useful when read alone.

## Scenario: Installable Codex Plugin

User asks:

```text
Package Code-Wiki V2 so Codex users can install it as a plugin.
```

Required result:

- `.codex-plugin/plugin.json` exists and points `skills` at `./skills/`.
- Plugin and marketplace metadata agree on version, description, keywords, prompts, and shared interface fields.
- Metadata describes persistent project memory, approved Specs, Reference navigation, and source inspection.
- The skill-centered plugin omits hooks, apps, MCP servers, icons, logos, and screenshots.

## Scenario: Installable Claude Code Plugin

User asks:

```text
Package Code-Wiki V2 so Claude Code users can install it as a plugin.
```

Required result:

- `.claude-plugin/plugin.json` exists and omits a `skills` field, because Claude Code discovers `./skills/` automatically.
- `.claude-plugin/marketplace.json` exposes exactly one plugin entry with a `source`, so `/plugin marketplace add codewiki-labs/codewiki` followed by `/plugin install code-wiki@code-wiki` installs all seven skills.
- Shared metadata — name, version, description, license, keywords, and author — matches `.codex-plugin/plugin.json`.
- Codex-only presentation and policy fields (`interface`, `policy`) stay out of the Claude manifests, and the plugin omits hooks, agents, and MCP servers.
- The same `skills/*/SKILL.md` files serve both platforms without agent-specific edits.
- Claude packaging files stay out of the Codex sync payload.

## Scenario: User Forbids Wiki Use

User asks:

```text
Do not read or update the Wiki. Just inspect this one file.
```

Required behavior:

- The explicit user instruction wins.
- `using-code-wiki` does not force Wiki reading or updates for that task.

## Scenario: No Wiki Exists

User asks:

```text
Explain the project structure.
```

Required behavior:

- Check for a Code-Wiki.
- If none exists, state that no Code-Wiki was found and do not invent project memory.
- Continue with normal source inspection when appropriate or offer `creating-code-wiki` when persistent memory would help.

## Scenario: Codex Plugin Sync

User asks:

```text
Sync this Code-Wiki checkout into a Codex plugin repository.
```

Required result:

- `scripts/sync-to-codex-plugin.sh` accepts `--repo owner/name`, `--dest plugins/code-wiki`, `--local PATH`, `--base`, and `--bootstrap`.
- Dry-run previews the payload without mutating the destination checkout.
- The payload includes the manifest, skills, generated-Wiki validator, README, license, changelog, code of conduct, contributing guide, public design doc, and examples.
- Internal implementation plans, development-only scripts, tests, Git data, ignored untracked files, and unrelated manifests stay excluded.
- Destination-owned `skills/**/agents/openai.yaml` metadata is preserved.
- Dirty destination plugin paths block apply mode, while a clean no-op apply exits without creating a sync branch.

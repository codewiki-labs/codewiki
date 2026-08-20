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
- Read matched Specs and their `Related Domains` closure in full.
- Read paired Reference domains, then inspect source.
- When architecture or security Specs are selected, read their paired cross-cutting Reference page before source inspection.
- For architecture work, always include `reference/architecture.md` whether or not an approved architecture Spec exists; include the Spec when present.
- For permission or security work, always include `reference/security.md` whether or not an approved security Spec exists; include the Spec when present.
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
- Build one complete Wiki proposal outside canonical `wiki/`, including the exact file tree and complete router, registry, Spec, and Reference content.
- Distinguish code-backed Reference facts from candidate durable requirements inferred from code; inferred behavior becomes normative only through approval as Spec content.
- Present the complete Wiki proposal for one user approval covering canonical creation and the proposed Specs and taxonomy.
- Do not write any files under `wiki/` before user approval, including empty skeletons, Reference pages, or persistent drafts.
- If relevant source evidence changes before canonical creation, update affected Reference facts and Spec candidates and re-present the revised proposal for approval.
- After approval, write the complete proposal into the `specs/` and `reference/` structure, not a mixed code-description tree.
- Pair every `specs/domains/<domain>.md` with exactly one `reference/domains/<domain>.md`.
- Pair `specs/project.md` with `reference/overview.md`, pair the two indexes, and pair architecture or security Specs when present.
- Keep `specs/project.md` short enough to read every session.
- Store important rationale beside its requirement.
- Do not create a chronological conversation/change history or a separate ADR store.
- Treat the proposed domain taxonomy as part of the Spec set the user approves; descriptive Reference scaffolding alone is not requirement approval.
- Omit architecture or security Specs when no corresponding global intent has been approved; create and pair them when approved.

## Scenario: Feature Surface Coverage During Creation

Given a repository with an active user tool, an administrator configuration surface, provider usage normalization, persistence, and permission guards, required behavior is:

- Build a noncanonical Feature Surface Inventory before finalizing the domain taxonomy.
- Inspect user and operator UI or catalogs, routes and events, services and providers, persistence and lifecycle, configuration and defaults, authentication and ownership, limits and usage or audit boundaries, failures and cancellation, and focused tests.
- Classify each discovered surface as important, supporting, placeholder, or excluded.
- Assign every important feature to one primary domain or provide an explicit evidence-backed exclusion reason.
- Treat any unassigned important feature as a creation blocker.
- Keep the inventory outside canonical `wiki/` until the complete proposal is approved.

## Scenario: Deep Domain Reference

Given an important feature assigned to a domain, required behavior is:

- Trace its user or operator surface to its API method, route, or event contract.
- Record authentication, role, permission, ownership, validation, and limit enforcement when applicable.
- Trace service branches, provider contracts, persistence and lifecycle, usage, cost and audit, failure, interruption, retry and deletion semantics, and exact tests when applicable.
- Use repository-root-relative source paths, exact symbols, exact routes, and exact test files.
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
- Follow each selected Spec's `Related Domains`, such as `auth-and-current-user` or `roles-and-permissions`.
- Deduplicate the closure and read every selected Spec in full before Reference or source.
- Always read `reference/security.md` for this permission task, whether or not an approved security Spec exists; read the Spec too when present.
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
- If source tracing reveals an undocumented logical domain, load its approved Spec before making decisions in that domain and record the missing Related Domains or Reference link.

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
- Check project-to-overview, index-to-index, architecture, and security Spec counterparts so every Spec has a corresponding Reference.
- Allow Reference-only cross-cutting pages such as commands, testing, dependencies, and glossary.
- Check that domain taxonomy describes logical change boundaries rather than mirroring source modules.
- Check authority direction, approval integrity, current-intent compaction, concise always-read memory, and source-navigation quality.
- Inventory every Wiki file so noncanonical history, draft, or decision stores cannot escape the audit.
- Treat canonical placement as an approval assertion, while flagging visible draft markers or disputed provenance instead of inventing lifecycle metadata.
- Classify findings as desired-state, observed-state, or Wiki contract/representation defects.
- Report durable-intent approval and mutation authorization separately.

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
- The payload includes the manifest, skills, README, license, changelog, code of conduct, contributing guide, docs, and examples.
- Repo-local scripts, tests, Git data, ignored untracked files, and unrelated manifests stay excluded.
- Destination-owned `skills/**/agents/openai.yaml` metadata is preserved.
- Dirty destination plugin paths block apply mode, while a clean no-op apply exits without creating a sync branch.

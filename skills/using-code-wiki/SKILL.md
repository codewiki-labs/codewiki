---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace, before any response or action that depends on project context, including quick factual questions about how the project behaves or is configured. Checks for a repository-local wiki/ and hands off to reading-code-wiki for approved intent and navigation, creating-code-wiki when no wiki exists, updating-code-wiki before finishing work that changed intent or navigation, or auditing-code-wiki when the wiki looks unreliable. Use when unsure which code-wiki skill applies.
---

# Using Code-Wiki

Use this bootstrap skill to recover repository-local persistent project memory before making project decisions. Load the smallest complete intent context for the task, and route detailed work to the supporting skills.

## Instruction Priority

1. The user's explicit instruction in the current conversation or repository instruction files has highest priority.
2. User-approved Code-Wiki Specs define durable project intent.
3. Code-Wiki skills define the default memory and navigation behavior.
4. Default agent behavior has lowest priority.

If the user explicitly says not to read or update the Wiki, honor that instruction. If the request is unrelated to the repository, Code-Wiki does not apply.

## Authority Model

- **Approved Specs are authoritative over implementation.** Specs answer what should be true.
- **Source code is authoritative over Reference.** Code and observed runtime state answer what is currently true.
- Reference answers where and how the current implementation is organized. It is a navigation layer, not an authority.

## User And Agent Boundary

- Specs are the user-facing contract. A user must be able to approve desired behavior and review Spec conformance without reading Reference.
- Reference is the agent-facing implementation map. Agents use it to find current enforcement, source, configuration, storage, and tests quickly, then verify those claims in source.
- User approval applies to Spec content and taxonomy. Reference creation and freshness checks are source-grounded agent work and do not ask the user to approve implementation prose.
- High-risk behavior such as actor permissions, calculations, pricing precedence, invariants, lifecycle outcomes, failure policy, retention, and audit meaning belongs in Specs. Reference maps stable requirement IDs to current implementation evidence.

Apply mismatches in the correct direction:

- Approved Spec differs from code: report the mismatch and change code to conform when implementation is in scope.
- Reference differs from code: verify the source and refresh Reference.
- Never derive or silently alter a requirement merely because code changed.

Mismatch direction does not grant edit authority. An audit, explanation, review, or diagnosis remains read-only unless the user also requested changes; report the required repair instead.

If checked-out source and observed runtime disagree, verify the deployed revision, configuration, feature flags, migrations, and environment. Treat them as scoped observations instead of collapsing them into one claim. Ground repository Reference in the checked-out source and record a verified environment-specific divergence explicitly when it matters.

## Preflight

Before a project-related answer, plan, edit, debug session, or source search:

1. Locate the repository root and check for `wiki/index.md`.
2. If no Code-Wiki exists, do not invent memory. Say it was not found when relevant, consider `creating-code-wiki`, and continue with source inspection only when appropriate.
3. If it exists, invoke `reading-code-wiki` and recover, in order:
   - the authority and navigation rules in `wiki/index.md`
   - the concise global memory in `wiki/specs/project.md`
   - relevant domains selected from `wiki/specs/index.md`
   - directly matched Specs plus their recursive `Required Context` closure
   - directly relevant, nonrecursive `See Also` pages
   - paired Reference pages and source-derived concern applicability from `wiki/reference/coverage.json` when relevant
4. Invoke `exploring-code-with-wiki` before relying on implementation claims or editing source.

Do not read the entire Wiki by default. The two always-read pages are `wiki/index.md` and `wiki/specs/project.md`; everything else is selected by task intent.

## Durable Intent Gate

Before implementation, decide whether the request changes what should remain true after this task.

Store durable user intent such as final behavior, project-wide direction, architectural constraints, actor permissions, calculation and policy rules, security invariants, lifecycle and failure outcomes, retention and audit meaning, important rationale, non-goals, and Acceptance Criteria. Do not store one-off debugging commands, temporary test instructions, implementation plans, transient workarounds, or raw conversation history.

Put product behavior in its owning domain Spec. Use `wiki/specs/policies/` only for approved rules that genuinely span domains. Security is a concern rather than a required domain or page: authentication, authorization, ownership, exposure, secrets, sensitive data, and trust boundaries stay with their owning domains unless an approved global policy is necessary.

When the request adds, removes, or conflicts with a durable requirement:

1. Identify the affected canonical Specs.
2. Write a **Proposed Spec Change** with exact current and proposed behavior, rationale when important, and testable Acceptance Criteria.
3. Obtain user approval.
4. Invoke `updating-code-wiki` to update canonical Specs.
5. Implement and verify against the approved Specs.

An explicit request that presents a complete requirement and instructs the agent to adopt or implement it counts as user approval of that presented content. Do not ask the user to approve identical wording twice. Approval is implied only when subject, scope, value, unit, constraints, and acceptance meaning are unambiguous in context. An underspecified instruction is not approval. User-instruction priority does not fill in missing semantics.

## Skill Routing

| Need | Skill |
| --- | --- |
| Initialize or substantially regenerate project memory | `creating-code-wiki` |
| Recover global and task-specific intent | `reading-code-wiki` |
| Follow Reference into implementation | `exploring-code-with-wiki` |
| Apply approved Spec changes or refresh Reference | `updating-code-wiki` |
| Review authority, pairing, freshness, or usefulness | `auditing-code-wiki` |
| Maintain this package's skill set | `writing-code-wiki-skills` |

## Working With Superpowers

**Superpowers owns the workflow. Code-Wiki owns the project contract and memory.**

- Code-Wiki supplies persistent WHAT, WHY, and WHERE.
- Superpowers supplies HOW: brainstorming, planning, TDD, execution, review, and verification.
- When Superpowers is available, use its required process while ensuring Wiki intent is recalled before design or implementation decisions.
- Invoke required Superpowers process skills first, then recover Code-Wiki context during their project exploration before design decisions. When the proposed design and Spec change are semantically identical, use a single approval artifact for both systems instead of asking twice.
- Do not copy one-off Superpowers plans into canonical Specs.
- When Superpowers is unavailable, use the lightweight sequence: recall memory, find domains, read Specs, read Reference, inspect code, approve Spec changes, implement, verify, refresh Reference.

## Closeout

Before completing project work:

1. Verify implementation against all affected approved Specs and Acceptance Criteria.
2. If code does not conform, do not redefine the Spec to make the task look complete.
3. Invoke `updating-code-wiki` when edits are authorized and verified code organization, runtime flow, commands, tests, configuration, dependencies, models, APIs, security behavior, or gotchas changed. Otherwise report the needed Reference refresh.
4. Refresh Reference only from verified current implementation.
5. Confirm that every affected Spec domain still has its paired Reference domain.
6. Refresh `wiki/reference/coverage.json` when feature assignments, source evidence, or security/architecture applicability changed. Confirm every policy has a same-named view, every view is manifest-listed, and evidence-backed `not_applicable` concerns do not have placeholder policy or view files.
7. Confirm recursive `Required Context` and nonrecursive `See Also` links remain selective and resolve.
8. Report whether Specs changed with approval, Reference changed from code, or no durable Wiki update was needed.

Lead user-facing closeout with a Spec conformance matrix: `requirement ID → verification result → mismatch or pass`. Keep Reference paths and freshness details available for agent traceability, but do not require the user to read Reference to decide whether the requested behavior was implemented.

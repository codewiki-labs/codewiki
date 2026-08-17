---
name: auditing-code-wiki
description: Use when the code-wiki appears stale, inconsistent, too vague, missing key domain context, or unreliable as persistent project memory.
---

# Auditing Code-Wiki

Audit whether a future agent can recover approved intent, navigate to current implementation, and apply mismatches in the correct direction.

## Checks

- **Authority direction:** Specs are treated as desired-state authority; source is treated as current-state authority over Reference. No document lets implementation drift redefine a requirement.
- **Approval integrity:** canonical Specs contain approved current intent, not drafts, inferred behavior, or unreviewed requirement candidates.
- **Domain pairing:** the complete relative file sets under `wiki/specs/domains/` and `wiki/reference/domains/` are identical, with no missing, duplicate, or orphan counterpart. Reference-only domain files are invalid.
- **Taxonomy:** Spec and Reference domains share logical responsibilities and change boundaries rather than mirroring source modules.
- **Current intent:** superseded requirements and raw conversation history are semantically compacted; important rationale stays beside the requirement it explains.
- **Always-read memory:** `wiki/index.md` and `wiki/specs/project.md` are present, concise, non-duplicative, and sufficient to recover authority plus global direction.
- **Navigation quality:** Reference pages point to concrete entry points, paths, symbols, models, flows, tests, commands, and dependencies without replacing source inspection.
- **Requirement quality:** domain Specs contain clear Intent, Requirements, Constraints, Rationale when important, Non-goals, testable Acceptance Criteria, and minimal Related Domains.
- **Registry closure:** `wiki/specs/index.md` lists domain responsibilities, and Related Domains resolve without broken links or unnecessary context expansion.
- **Cross-cutting pairs:** check project-to-overview, index-to-index, architecture, and security counterparts; Reference-only operational pages are allowed.
- **Freshness:** referenced paths and symbols still exist, documented commands remain plausible, and high-risk runtime claims are spot-checked.

The canonical location is the approval assertion; the audit does not reconstruct raw conversations or add lifecycle metadata. Flag visible draft markers, contradictions, or disputed provenance for user confirmation instead of silently demoting or deleting requirements.

Judge `project.md` by scope rather than an arbitrary token limit: it should contain only purpose, priorities, global intent, project-wide constraints, and non-goals that apply broadly. Domain behavior, source paths, APIs, and repeated details belong elsewhere.

## Audit Process

1. Inventory every file under `wiki/`, including noncanonical history, draft, decision, backup, or orphan files.
2. Read the two always-read pages and both registries.
3. Compare the complete Spec and Reference domain file lists by relative path.
4. Read all Specs to inspect authority, approval, current-intent compaction, rationale locality, Acceptance Criteria, and related-domain links.
5. Review Reference pages for navigation usefulness and stale claims.
6. Spot-check source, configuration, runtime composition, and focused tests where accuracy or risk matters.
7. Produce findings by severity with evidence and the correct repair direction.

## Safe Repair Boundary

- You may refresh a stale Reference claim after verifying source when edits are requested.
- Do not automatically change a Spec because code or Reference differs.
- For unclear, conflicting, or apparently unapproved requirements, propose exact Spec corrections and request user approval.
- Adding or renaming a domain requires maintaining exact pairing and both registries.

## Audit Output

For each finding, include:

- severity and issue
- classification: desired state, observed state, or Wiki contract/representation
- evidence
- affected Spec, Reference, and source paths
- whether desired state or observed state is wrong
- suggested repair
- whether durable-intent approval is required
- whether mutation authorization exists for this task
- whether the issue blocks reliable future-agent use

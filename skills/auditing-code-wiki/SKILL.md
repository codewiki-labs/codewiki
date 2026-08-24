---
name: auditing-code-wiki
description: Use when the code-wiki appears stale, inconsistent, too vague, missing key domain context, or unreliable as persistent project memory.
---

# Auditing Code-Wiki

Audit whether a user can validate desired behavior from Specs alone and whether a future agent can navigate current implementation through Reference without confusing the two authorities.

## Checks

- **Authority direction:** Specs are treated as desired-state authority; source is treated as current-state authority over Reference. No document lets implementation drift redefine a requirement.
- **Approval integrity:** canonical Specs contain approved current intent, not drafts, inferred behavior, or unreviewed requirement candidates.
- **Spec sufficiency:** each domain Spec is a behaviorally complete user-facing contract. It defines applicable actor permissions, calculations and units, policy precedence, invariants, lifecycle and failure outcomes, retention and audit meaning, and testable examples so the user can validate correctness without Reference.
- **Stable verification:** important requirements and Acceptance Criteria have stable IDs that support a Spec conformance matrix.
- **Domain pairing:** the complete relative file sets under `wiki/specs/domains/` and `wiki/reference/domains/` are identical, with no missing, duplicate, or orphan counterpart. Reference-only domain files are invalid.
- **Policy and view pairing:** every `wiki/specs/policies/<concern>.md` has `wiki/reference/views/<concern>.md`. A view without a policy is allowed only when `reference/coverage.json` lists it and the view keeps unapproved behavior descriptive.
- **Concern applicability:** `reference/coverage.json` records `security` and `architecture` as `applicable` or evidence-backed `not_applicable`, with owning domains, reasons, exact evidence, and policy/view paths consistent with actual files. Security is assessed as a concern owned by domains, not required as a fixed domain or placeholder page.
- **Taxonomy:** Spec and Reference domains share logical responsibilities and change boundaries rather than mirroring source modules.
- **Current intent:** superseded requirements and raw conversation history are semantically compacted; important rationale stays beside the requirement it explains.
- **Always-read memory:** `wiki/index.md` and `wiki/specs/project.md` are present, concise, non-duplicative, and sufficient to recover authority plus global direction.
- **Navigation quality:** Reference pages point to concrete entry points, paths, symbols, models, flows, tests, commands, and dependencies without replacing source inspection.
- **Spec implementation mapping:** each important Reference feature names its approved `Spec Basis` and maps requirement IDs to current enforcement, exact evidence, tests, and conformance or mismatch.
- **Authority leakage:** Reference is not the sole location for a durable permission, calculation, price precedence, invariant, lifecycle guarantee, failure policy, retention rule, or audit meaning. Unapproved observed behavior is explicitly descriptive rather than a shadow requirement.
- **Feature coverage:** every important current feature is assigned to a logical domain or has an explicit evidence-backed exclusion.
- **Trace completeness:** each important feature covers applicable surfaces, API or events, authorization and limits, service or provider behavior, persistence and lifecycle, usage or audit, failures, and exact tests.
- **Evidence specificity:** paths are repository-root-relative and current; routes, symbols, configuration keys, models, jobs, and test files are exact rather than wildcards or generic labels.
- **High-risk contracts:** security and permission, cost and usage, storage and retention, external provider, streaming and background work, and deletion paths receive focused checks when present.
- **Requirement quality:** domain Specs contain clear Intent, stable requirement IDs, applicable behavior contracts, Constraints, Rationale when important, Non-goals, testable Acceptance Criteria including hand-computed vectors when useful, and selective typed links.
- **Registry closure:** `wiki/specs/index.md` lists domain responsibilities; recursive `Required Context` resolves without broken links or unnecessary expansion, while `See Also` remains nonrecursive and directly relevant. Legacy `Related Domains` is a one-hop migration defect.
- **Cross-cutting pairs:** check project-to-overview, index-to-index, and policy-to-view counterparts. Reference-only concern views are allowed when manifest-listed as applicable; operational pages remain independently optional.
- **Freshness:** referenced paths and symbols still exist, documented commands remain plausible, and high-risk runtime claims are spot-checked.

The canonical location is the approval assertion; the audit does not reconstruct raw conversations or add lifecycle metadata. Flag visible draft markers, contradictions, or disputed provenance for user confirmation instead of silently demoting or deleting requirements.

Judge `project.md` by scope rather than an arbitrary token limit: it should contain only purpose, priorities, global intent, project-wide constraints, and non-goals that apply broadly. Domain behavior, source paths, APIs, and repeated details belong elsewhere.

A valid file tree, exact domain pairing, existing links, and named symbols do not establish semantic completeness. Treat a Spec that needs Reference to determine correct behavior as a Spec sufficiency defect. Treat symbol presence without implementation evidence as a Reference coverage defect.

## Audit Process

1. Inventory every file under `wiki/`, including noncanonical history, draft, decision, backup, or orphan files.
2. Read the two always-read pages and both registries.
3. Compare the complete Spec and Reference domain file lists by relative path, then compare policy and view paths.
4. Read all Specs to inspect authority, approval, current-intent compaction, stable IDs, behavior completeness, rationale locality, Acceptance Criteria, hand-computed vectors, and typed context links.
5. Reconstruct a risk-weighted Feature Surface Inventory from active UI or catalogs, routes, jobs, providers, schemas, guards, configuration, persistence, and focused tests.
6. Compare important source features with registry assignments, domain Reference coverage, and `reference/coverage.json`; independently check security and architecture applicability evidence.
7. Review Reference pages and concern views for `Spec Basis`, trace completeness, evidence specificity, navigation usefulness, stale claims, and authority leakage.
8. Spot-check source, configuration, runtime composition, and focused tests where accuracy or risk matters.
9. For a full plugin installation, run the bundled `../../scripts/validate_generated_wiki.py` (resolved relative to this skill) with `--repo-root <repository-root> --wiki-root <repository-root>/wiki`. For a skills-only installation, use the validator from the Code-Wiki source checkout or a repository-provided copy. Treat it as a contract gate, not proof of product correctness.
10. Produce findings by severity with evidence and the correct repair direction.

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
- affected important features and missing trace dimensions
- coverage-manifest omissions, stale evidence, or invalid concern applicability
- broken policy/view pairs, over-expanded `See Also`, or unresolved `Required Context`
- whether the user-facing Spec alone determines the correct result
- missing or stale `Spec Basis` mappings and authority-leakage findings
- whether desired state or observed state is wrong
- suggested repair
- whether durable-intent approval is required
- whether mutation authorization exists for this task
- whether the issue blocks reliable future-agent use

---
name: writing-code-wiki-skills
description: Use when modifying the Code-Wiki skill set, its boundaries, package documentation, plugin metadata, or validation scenarios.
---

# Writing Code-Wiki Skills

Keep skills small, task-specific, testable, and usable without private project context while preserving the authority and memory contract.

## Split Criteria

Create or keep a separate skill when at least one is true:

- use timing is different
- required inputs differ
- agent actions differ
- failure modes differ
- context would be costly to always load
- another skill can reuse it
- users would directly invoke it

Do not create a new skill when the behavior is a small checklist, always used with an existing skill, has no independent trigger, or would make routing ambiguous.

## Required Boundaries

- `using-code-wiki`: bootstrap, authority routing, durable-intent detection, and closeout.
- `creating-code-wiki`: first creation or substantial regeneration.
- `reading-code-wiki`: global-memory recovery, domain selection, and typed context closure.
- `exploring-code-with-wiki`: targeted source verification through Reference.
- `updating-code-wiki`: approval-gated Spec edits and code-grounded Reference refreshes.
- `auditing-code-wiki`: authority, pairing, quality, and stale-content review.
- `writing-code-wiki-skills`: maintenance of this package.

## Contract Invariants

- Approved Specs are normative over implementation.
- Specs are the behaviorally complete user-facing contract; users approve Specs and taxonomy without reviewing Reference content.
- Source code is authoritative for Reference.
- Reference is the agent-facing implementation map; it navigates to source and never replaces inspection.
- Stable requirement IDs connect Reference `Spec Basis`, implementation evidence, tests, and user-facing Spec conformance results.
- Calculations, permissions, policy precedence, invariants, lifecycle and failure outcomes, retention, and audit meaning cannot exist only in Reference as authority leakage.
- Specs and Reference share one logical domain taxonomy and exact domain pairing by relative path.
- Reference-only domain files are invalid. The two domain trees have identical relative file sets.
- Domain Specs own behavior, including security and trust-boundary behavior. `specs/policies` is reserved for approved cross-domain rules.
- Every policy has a paired same-named page under `reference/views`; a source-derived view may exist without a policy only when the coverage manifest lists it and it does not invent durable intent.
- `reference/coverage.json` persists source revision, feature assignments, exclusions, evidence, and explicit security and architecture applicability. Evidence-backed `not_applicable` concerns have no placeholder policy or view.
- `Required Context` is recursively retrieved; `See Also` is nonrecursive. Legacy `Related Domains` is one-hop migration input only.
- Code changes never silently change Specs.
- Durable requirement changes pass an approval gate before canonical Spec edits or implementation.
- Canonical Specs store semantically compacted current intent, not raw history.
- Important rationale stays near its requirement.
- Code-Wiki owns persistent WHAT, WHY, and WHERE; available workflow skills own HOW.

## Description Rules

- Start with `Use when` or `Use before`.
- The description describes when to use the skill, not its internal sequence.
- Include concrete triggers that users and agents will search for.
- Do not repeat routing tables or implementation detail in frontmatter.

## Skill File Rules

- Every skill lives at `skills/<skill-name>/SKILL.md`.
- Each skill must be useful when read alone.
- Repeated common rules may be summarized, but no skill may reverse the authority model.
- Do not claim behavior that is absent from the skill files.
- Keep the two always-read Wiki pages concise and task-specific retrieval selective.

## Test Scenarios

For every behavior change, update `scripts/validate_wiki_contract.py` and at least one scenario in `tests/skill-set-contract.md`; test scenarios are part of the contract, not optional notes.

When the change affects generated-Wiki structure, manifest semantics, domain pairing, policy/view pairing, typed links, or authority boundaries, update `scripts/validate_generated_wiki.py` and `tests/test_generated_wiki_validator.py`. Validate actual generated artifacts, not only this package's phrases.

When a change affects Spec sufficiency, feature discovery, Reference depth, evidence specificity, authority leakage, or audit completeness, update the semantic quality fixture manifest, paired Spec and Reference fixtures for shallow, complete, or authority-leakage candidates, and `scripts/validate_wiki_quality_fixtures.py` as applicable. Phrase presence alone is not sufficient evidence for these behaviors.

Scenarios must cover, when relevant:

- trigger clarity and boundary confusion
- approved Spec versus code
- Reference versus code
- durable versus ephemeral user requests
- exact-content approval versus a proposed change requiring approval
- exact domain pairing, policy/view pairing, and view-only applicability
- recursive `Required Context`, nonrecursive `See Also`, and legacy-link migration
- securityless, domain-owned security, and approved global security-policy cases
- `reference/coverage.json` feature closure, evidence, exclusions, and concern applicability
- semantic compaction of current intent
- Superpowers or other workflow integration
- verifiable outputs and Reference freshness
- Spec-only user approval and user-facing conformance review
- behaviorally complete calculations, permissions, invariants, lifecycle, failure, retention, and audit rules
- requirement-ID mapping from approved Specs to agent-facing Reference evidence

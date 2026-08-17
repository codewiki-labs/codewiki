---
name: writing-code-wiki-skills
description: Use when modifying the Code-Wiki skill set, its boundaries, package documentation, plugin metadata, or validation scenarios.
---

# Writing Code-Wiki Skills

Keep skills small, task-specific, testable, and usable without private project context while preserving the V2 authority and memory contract.

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
- `creating-code-wiki`: first creation or substantial V2 regeneration.
- `reading-code-wiki`: global-memory recovery, domain selection, and related-domain closure.
- `exploring-code-with-wiki`: targeted source verification through Reference.
- `updating-code-wiki`: approval-gated Spec edits and code-grounded Reference refreshes.
- `auditing-code-wiki`: authority, pairing, quality, and stale-content review.
- `writing-code-wiki-skills`: maintenance of this package.

## V2 Invariants

- Approved Specs are normative over implementation.
- Source code is authoritative for Reference.
- Reference navigates to source and never replaces inspection.
- Specs and Reference share one logical domain taxonomy and exact domain pairing by relative path.
- Reference-only domain files are invalid. The two domain trees have identical relative file sets.
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
- Repeated common rules may be summarized, but no skill may reverse the V2 authority model.
- Do not claim behavior that is absent from the skill files.
- Keep the two always-read Wiki pages concise and task-specific retrieval selective.

## Test Scenarios

For every behavior change, update `scripts/validate_wiki_contract.py` and at least one scenario in `tests/skill-set-contract.md`; test scenarios are part of the contract, not optional notes.

Scenarios must cover, when relevant:

- trigger clarity and boundary confusion
- approved Spec versus code
- Reference versus code
- durable versus ephemeral user requests
- exact-content approval versus a proposed change requiring approval
- domain pairing and Related Domains closure
- semantic compaction of current intent
- Superpowers or other workflow integration
- verifiable outputs and Reference freshness

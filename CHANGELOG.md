# Changelog

## Unreleased

- Replaced repeated `Requirement:` and `Acceptance Criterion:` level-three labels with compact backticked `-Rddd` and `-ACddd` IDs, while retaining section-aware compatibility for legacy requirement headings, ignoring fenced examples, rejecting duplicate Spec item IDs, and rejecting legacy labels that contradict their ID type.
- Changed the `reading-code-wiki` and `using-code-wiki` descriptions to enumerate concrete question triggers, so ordinary factual questions about project behavior load the wiki skills instead of bypassing them.
- Made security and architecture source-derived concerns owned by product domains instead of mandatory Wiki domains or pages.
- Added optional approved cross-domain policy Specs under `specs/policies/` and source-derived concern maps under `reference/views/`, with mandatory policy-to-view pairing and manifest-listed view-only support.
- Added persistent `reference/coverage.json` feature closure and evidence-backed concern applicability, including valid securityless projects through `not_applicable`.
- Replaced recursive `Related Domains` retrieval with recursive `Required Context` and nonrecursive `See Also`, retaining legacy links only as one-hop migration input.
- Added a generated-Wiki validator and fixtures for no-security, domain-owned security, global policy/view, typed-link, pairing, and authority-leakage cases.
- Included the generated-Wiki validator in the Codex plugin sync payload while continuing to exclude development-only scripts and tests.
- Kept internal implementation plans out of the runtime plugin payload.
- Made domain Specs behaviorally complete user-facing contracts for permissions, calculations, policy precedence, invariants, lifecycle, failures, retention, audit meaning, and Spec-only conformance review.
- Reframed Reference as an agent-facing implementation map using stable requirement IDs and `Spec Basis`, with no user approval requirement for source-grounded refreshes.
- Added authority-leakage fixtures that reject billing or other durable rules present only in Reference.
- Changed initial approval from a complete Spec-and-Reference review to user approval of Specs and taxonomy only.
- Restored deep code-backed domain Reference sections for permissions, invariants, lifecycle, failures, contract artifacts, and verification while preserving the V2 Spec/Reference authority split.
- Added a pre-canonical Feature Surface Inventory, important-feature assignment, end-to-end trace, and coverage completion gates.
- Added semantic quality fixtures that reject shallow symbol lists and one-line flows for important features.
- Added oversize handling for wiki pages: any page larger than 200 lines is an oversize signal that triggers a report-first review — the agent reports what inflates the page and asks the user to review the compaction together, split the domain, delegate, or accept the size; delegated compaction follows a meaning-unit inventory protocol that only drops source-restated, superseded, duplicated, or historical content and reports kept/merged/dropped dispositions, and size alone never deletes an approved requirement.
- Added Claude Code plugin packaging with `.claude-plugin/plugin.json` and a one-plugin `.claude-plugin/marketplace.json`, so the same skill set installs via `/plugin install code-wiki@code-wiki`.
- Changed plugin metadata to describe coding agents rather than Codex specifically, and added the `claude-code` keyword.
- Bumped plugin metadata to `0.3.0` across all four manifests.
- Extended contract validation to cover the Claude Code manifests and to reject Codex-only `interface` and `policy` fields there.
- Added a sync regression assertion that Claude packaging files stay out of the Codex payload.
- Documented the three-layer packaging model and the agent-neutral skill-body invariant that lets one skill set serve both platforms.
- Aligned the plugin and marketplace `category` values, which previously disagreed without being validated.
- Changed initial Wiki creation to inspect the current checkout and wait for user approval before writing any canonical Wiki files.
- Reframed Code-Wiki as repository-local persistent project memory.
- Added normative user-approved Specs and descriptive code-backed Reference with separate authority rules.
- Replaced the mixed Wiki layout with `specs/` and `reference/` trees plus exact domain pairing.
- Added concise always-read project memory, domain registries, typed context closure, and Reference-guided source retrieval.
- Added approval-gated durable requirement changes, current-intent semantic compaction, and Acceptance Criteria verification.
- Removed chronological Wiki history and standalone decision-store guidance in favor of Git history and requirement-local rationale.
- Defined the boundary where Code-Wiki owns WHAT/WHY/WHERE and Superpowers owns HOW.
- Bumped the Codex plugin metadata to `0.2.0` and aligned marketplace presentation metadata.

- Added Codex plugin packaging with `.codex-plugin/plugin.json`.
- Added a generalized `scripts/sync-to-codex-plugin.sh` for publishing the plugin payload into a destination Codex plugin repository.
- Added fixture-driven sync regression tests for Codex plugin packaging.
- Extended package validation to cover the plugin manifest and sync test.
- Changed `using-code-wiki` from an explicit-request router into the bootstrap skill for project-related conversations.
- Added preflight and closeout rules so agents check wiki context before work and wiki update needs before completion.
- Removed the root compatibility `SKILL.md`; install individual `skills/*` directories instead.
- Split the previous single wiki skill into a public code-wiki skill set.
- Added focused skills for routing, creating, reading, code exploration, updating, auditing, and skill-set maintenance.
- Added open-source package docs: README, contributing guide, code of conduct, license, examples, design notes, and validation contract.
- Enforced Anthropic's 500-line SKILL.md budget in contract validation and moved the coverage manifest example into `skills/creating-code-wiki/references/`, which is read on demand while drafting `wiki/reference/coverage.json`.

# Changelog

## Unreleased

- Made domain Specs behaviorally complete user-facing contracts for permissions, calculations, policy precedence, invariants, lifecycle, failures, retention, audit meaning, and Spec-only conformance review.
- Reframed Reference as an agent-facing implementation map using stable requirement IDs and `Spec Basis`, with no user approval requirement for source-grounded refreshes.
- Added authority-leakage fixtures that reject billing or other durable rules present only in Reference.
- Changed initial approval from a complete Spec-and-Reference review to user approval of Specs and taxonomy only.
- Restored deep code-backed domain Reference sections for permissions, invariants, lifecycle, failures, contract artifacts, and verification while preserving the V2 Spec/Reference authority split.
- Added a pre-canonical Feature Surface Inventory, important-feature assignment, end-to-end trace, and coverage completion gates.
- Added semantic quality fixtures that reject shallow symbol lists and one-line flows for important features.
- Changed initial Wiki creation to inspect the current checkout and wait for user approval before writing any canonical Wiki files.
- Reframed Code-Wiki as repository-local persistent project memory.
- Added normative user-approved Specs and descriptive code-backed Reference with separate authority rules.
- Replaced the mixed Wiki layout with `specs/` and `reference/` trees plus exact domain pairing.
- Added concise always-read project memory, domain registries, Related Domains closure, and Reference-guided source retrieval.
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

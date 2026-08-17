# Changelog

## Unreleased

- Changed initial Wiki creation to inspect the current checkout, present one complete Spec-and-Reference proposal, and wait for user approval before writing any canonical Wiki files.
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

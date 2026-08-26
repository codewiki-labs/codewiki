# Security Policy And Reference View Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace ambiguous top-level architecture/security pairs with optional approved policies, conditional source-derived views, a persistent coverage manifest, and selective typed domain links.

**Architecture:** Domain Spec/Reference files remain exact pairs. Approved cross-domain invariants live under `specs/policies/`, descriptive aggregation lives under `reference/views/`, and `reference/coverage.json` records feature ownership plus concern applicability. A new generated-Wiki validator checks these artifact invariants, while the existing semantic fixture validator continues to check Spec sufficiency, `Spec Basis`, trace depth, and authority leakage.

**Tech Stack:** Markdown skill contracts and documentation, Python 3 standard library validators and `unittest`, JSON fixtures, Bash packaging regression tests.

**Spec:** `docs/superpowers/specs/2026-08-24-security-policy-view-design.md`

## Global Constraints

- Approved Specs remain normative; source code remains authoritative for Reference.
- Every `specs/domains/<path>.md` has exactly one `reference/domains/<path>.md`.
- Every `specs/policies/<name>.md` has `reference/views/<name>.md`; a view may exist without a policy.
- Security requirements stay in their owning domains unless an approved invariant is genuinely cross-domain.
- `reference/coverage.json` is descriptive and never part of user approval.
- `Required Context` is recursive, `See Also` is nonrecursive, and legacy `Related Domains` is direct-only migration input.
- After implementation, review, and full verification, create one scoped commit and push the current branch as explicitly requested in the follow-up instruction. Do not create a PR unless separately requested.

---

### Task 1: Generated-Wiki Artifact Validator

**Files:**
- Create: `scripts/validate_generated_wiki.py`
- Create: `tests/test_generated_wiki_validator.py`
- Modify: `scripts/validate_wiki_contract.py`

**Interfaces:**
- Produces: `validate_generated_wiki(repo_root: Path, wiki_root: Path) -> list[str]`.
- Produces: CLI arguments `--repo-root PATH --wiki-root PATH` and exit code `0` only when no findings exist.
- Consumes: `reference/coverage.json` with `source_revision`, `features`, and `concerns`.

- [x] **Step 1: Write failing generated-artifact tests**

Create a temporary minimal Wiki helper that writes the router, project and Spec
indexes, overview, one exact domain pair, source/test evidence files, and a
coverage manifest. Add tests with these assertions:

```python
self.assertEqual(validate_generated_wiki(repo, wiki), [])
self.assertIn("security: not_applicable requires evidence", failures)
self.assertIn("security: not_applicable forbids view_path", failures)
self.assertIn("policy security.md missing paired view", failures)
self.assertEqual(domain_owned_security_failures, [])
self.assertEqual(global_security_policy_failures, [])
self.assertIn("legacy Related Domains section requires migration", failures)
```

- [x] **Step 2: Run tests and confirm RED**

Run: `python3 -m unittest tests/test_generated_wiki_validator.py`

Expected: import failure because `scripts/validate_generated_wiki.py` does not exist.

- [x] **Step 3: Implement the validator**

Implement focused helpers:

```python
def relative_markdown_files(root: Path) -> set[str]: ...
def load_coverage(wiki_root: Path) -> tuple[dict, list[str]]: ...
def validate_domain_pairs(wiki_root: Path) -> list[str]: ...
def validate_policy_views(wiki_root: Path, concerns: dict) -> list[str]: ...
def validate_features(repo_root: Path, wiki_root: Path, coverage: dict) -> list[str]: ...
def validate_concerns(repo_root: Path, wiki_root: Path, coverage: dict) -> list[str]: ...
def validate_domain_links(wiki_root: Path) -> list[str]: ...
def validate_generated_wiki(repo_root: Path, wiki_root: Path) -> list[str]: ...
```

The validator must require the five core Markdown files plus
`reference/coverage.json`, compare complete relative domain file sets, require
policy/view pairs, allow view-only source maps, validate applicable versus
not-applicable concern fields, resolve all named domains and paths, check exact
evidence paths under `repo_root`, validate important/excluded feature ownership,
and reject legacy `## Related Domains` in a newly validated artifact.

- [x] **Step 4: Run generated-artifact tests and confirm GREEN**

Run: `python3 -m unittest tests/test_generated_wiki_validator.py`

Expected: all tests pass.

- [x] **Step 5: Register package files and CLI contract**

Add the new script/test to `PACKAGE_FILES` and require generated-Wiki validator
phrases in `README.md`, `tests/skill-set-contract.md`, and the relevant skills.

---

### Task 2: Policy/View Semantic Authority Fixtures

**Files:**
- Modify: `tests/fixtures/wiki-quality/feature-surfaces.json`
- Create: `tests/fixtures/wiki-quality/complete/specs/policies/security.md`
- Create: `tests/fixtures/wiki-quality/complete/reference/views/security.md`
- Create: `tests/fixtures/wiki-quality/shallow/specs/policies/security.md`
- Create: `tests/fixtures/wiki-quality/shallow/reference/views/security.md`
- Create: `tests/fixtures/wiki-quality/authority-leakage/reference/views/security.md`
- Modify: `scripts/validate_wiki_quality_fixtures.py`
- Modify: `tests/test_wiki_quality_fixtures.py`
- Modify: `tests/wiki-quality-contract.md`

**Interfaces:**
- Consumes: optional manifest `policies` entries with `id`, `policy`,
  `spec_requirements`, `feature_id`, and exact `evidence`.
- Produces: deterministic failures for missing approved policy requirements even
  when the Reference view is otherwise deep.

- [x] **Step 1: Add the failing policy fixture test**

Extend the manifest with a global security requirement such as:

```json
{
  "id": "security-baseline",
  "policy": "security",
  "feature_id": "security-enforcement-view",
  "spec_requirements": [
    {
      "id": "SEC-R001",
      "evidence": [
        "Authentication secrets must never be written to application logs."
      ]
    }
  ],
  "evidence": ["src/auth/guards.ts", "redactSensitiveHeaders"]
}
```

Add a complete policy/view pair, a shallow policy/view pair with no machine-
readable feature trace, and a leakage view without the policy. Assert that
complete passes, shallow detects the missing trace, and leakage contains
`security-enforcement-view: missing approved policy Spec security.md`.

- [x] **Step 2: Run semantic tests and confirm RED**

Run: `python3 -m unittest tests/test_wiki_quality_fixtures.py tests/test_wiki_contract_semantic_integration.py`

Expected: policy leakage is not detected yet or complete reports unexpected fixture content.

- [x] **Step 3: Implement policy validation**

Add `validate_policy(candidate_root, policy) -> list[str]`. Reuse
`requirement_block` and `feature_block`; require policy requirement evidence,
paired view `Spec Basis`, all trace dimensions, and exact evidence. Extend
expected leakage findings without weakening the existing `MU-USAGE-003` gate.

- [x] **Step 4: Run semantic tests and confirm GREEN**

Run: `python3 -m unittest tests/test_wiki_quality_fixtures.py tests/test_wiki_contract_semantic_integration.py`

Expected: all semantic and integration tests pass.

---

### Task 3: Skill And Behavioral Contract Migration

**Files:**
- Modify: `skills/using-code-wiki/SKILL.md`
- Modify: `skills/creating-code-wiki/SKILL.md`
- Modify: `skills/reading-code-wiki/SKILL.md`
- Modify: `skills/exploring-code-with-wiki/SKILL.md`
- Modify: `skills/updating-code-wiki/SKILL.md`
- Modify: `skills/auditing-code-wiki/SKILL.md`
- Modify: `skills/writing-code-wiki-skills/SKILL.md`
- Modify: `tests/skill-set-contract.md`
- Modify: `scripts/validate_wiki_contract.py`

**Interfaces:**
- Produces: consistent `specs/policies`, `reference/views`, and
  `reference/coverage.json` instructions across all seven skills.
- Produces: retrieval rules for `Required Context`, `See Also`, and legacy
  `Related Domains`.

- [x] **Step 1: Strengthen package expectations before skill edits**

Replace old expected phrases such as fixed `wiki/reference/security.md` and
recursive `Related Domains` with exact new contract phrases:

```text
wiki/specs/policies/security.md
wiki/reference/views/security.md
wiki/reference/coverage.json
Security is a concern, not a mandatory domain.
Required Context
See Also
Legacy `Related Domains`
```

Add behavioral scenarios for no-security, domain-owned security, global policy,
conditional view retrieval, coverage-manifest refresh, and typed link closure.

- [x] **Step 2: Run the main validator and confirm RED**

Run: `python3 scripts/validate_wiki_contract.py`

Expected: missing new contract phrases and stale old structure guidance.

- [x] **Step 3: Update creation and retrieval skills**

Make `creating-code-wiki` persist the source-derived inventory as
`reference/coverage.json` after approval, add policy/view and domain security
templates, and define applicability states. Make `reading-code-wiki` consult the
manifest for concern views, recurse only through `Required Context`, and load
legacy `Related Domains` one hop while reporting migration.

- [x] **Step 4: Update maintenance, exploration, audit, and bootstrap skills**

Make update/audit refresh feature and concern evidence from source, validate
policy/view pairs and not-applicable exclusions, and prevent Reference views
from becoming shadow policy. Replace recursive `Related Domains` wording in
bootstrap/exploration with the typed retrieval contract.

- [x] **Step 5: Run the main validator and confirm GREEN**

Run: `python3 scripts/validate_wiki_contract.py`

Expected: package and embedded semantic validation pass.

---

### Task 4: Public Documentation And Workflow Examples

**Files:**
- Modify: `README.md`
- Modify: `docs/skill-set-design.md`
- Modify: `examples/basic-workflow.md`
- Modify: `CONTRIBUTING.md`
- Modify: `CHANGELOG.md`
- Modify: `scripts/sync-to-codex-plugin.sh`
- Modify: `tests/codex-plugin-sync/test-sync-to-codex-plugin.sh`

**Interfaces:**
- Produces: one public description of the new schema, authority model,
  applicability gate, typed link retrieval, migration, and validator commands.

- [x] **Step 1: Update the public tree and semantics**

Document policies versus views, conditionally absent security artifacts,
domain-owned security, coverage manifest fields, and exact pairing rules. Keep
operational Reference pages optional and descriptive.

- [x] **Step 2: Update workflow and contribution guidance**

Change examples from session-only inventory to persisted Reference coverage,
use `Required Context`/`See Also`, and add the generated-Wiki validator command
to local checks and audit examples.

- [x] **Step 3: Record the unreleased change**

Add concise Unreleased entries without changing the existing `0.2.0` package
version because this branch is already the unreleased development line.

- [x] **Step 4: Run package validation**

Run: `python3 scripts/validate_wiki_contract.py`

Expected: pass with no forbidden V1 or stale fixed-security guidance.

- [x] **Step 5: Keep the validator in the plugin runtime payload**

Sync only `scripts/validate_generated_wiki.py` alongside skills and public docs;
continue excluding development-only scripts and tests. Verify both inclusion and
no-op convergence with the sync regression test.

---

### Task 5: Full Verification And Review

**Files:**
- Verify all modified and created files.

**Interfaces:**
- Consumes: all task outputs.
- Produces: evidence-backed completion status, one scoped commit, and the pushed current branch.

- [x] **Step 1: Run focused Python verification**

```bash
python3 scripts/validate_generated_wiki.py --help
python3 scripts/validate_wiki_quality_fixtures.py
python3 -m unittest tests/test_generated_wiki_validator.py tests/test_wiki_quality_fixtures.py tests/test_wiki_contract_semantic_integration.py
```

- [x] **Step 2: Run the complete package contract**

```bash
python3 scripts/validate_wiki_contract.py
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
```

- [x] **Step 3: Scan for stale schema names and placeholders**

Run focused `rg` checks for `specs/security.md`, `reference/security.md`,
recursive `Related Domains`, placeholder markers, and unregistered new files.
Keep only explicit migration references to legacy paths/sections.

- [x] **Step 4: Review the complete diff and worktree state**

Run: `git diff --check`, `git diff --stat`, `git diff`, and
`git status --short --branch`. Confirm no unrelated or generated cache changes
were introduced. After review, commit the complete scoped change, push the
current branch safely, and verify the upstream state.

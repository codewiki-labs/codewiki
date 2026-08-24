# Contributing

Thank you for improving code-wiki skills.

## Principles

- Keep one skill focused on one use situation.
- Do not split a skill only for visual symmetry.
- Do not add broad claims that are not implemented in the skill files.
- Keep `description` focused on when to use the skill.
- Preserve the V2 authority split: approved Specs are normative, while source is authoritative for Reference.
- Keep Specs behaviorally complete for user-only review and Reference agent-facing with requirement-ID implementation mappings.
- Treat permissions, calculations, policy precedence, invariants, lifecycle and failure outcomes, retention, and audit meaning found only in Reference as authority leakage.
- Preserve exact Spec/Reference domain pairing, policy/view pairing, and source-derived feature and concern coverage in `reference/coverage.json`.
- Keep security and trust-boundary behavior in owning domains; use `specs/policies/` only for approved cross-domain rules and `reference/views/` only for manifest-listed source maps.
- Preserve selective retrieval: recurse through `Required Context`, never through `See Also`, and treat legacy `Related Domains` as one-hop migration input.
- Never let code-driven maintenance rewrite canonical Specs without user approval.
- Add tests or validation for any boundary or structure change.

## Local Checks

Run:

```bash
python3 scripts/validate_wiki_contract.py
python3 -m unittest tests/test_generated_wiki_validator.py tests/test_wiki_quality_fixtures.py tests/test_wiki_contract_semantic_integration.py
bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
```

Maintainers with the Codex system skill validators installed should also run `quick_validate.py` for every `skills/*` directory and `validate_plugin.py` for the repository root.

## Commit And PR Title Convention

PRs are squash-merged, so the PR title becomes the commit message on `main`. PR titles must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(optional scope): <subject>
```

Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`, `build`, `revert`.

Examples:

```
feat(skills): add closeout check to updating-code-wiki
fix: restore approval-gate phrase in creating-code-wiki
ci: run contract validation on pull requests
```

Individual commits inside a PR branch are not checked — only the PR title is, by the "PR title" workflow.

## Plugin Packaging

The repository root is a Codex plugin package, but each behavior unit still lives in `skills/<name>/SKILL.md`.

- Keep `.codex-plugin/plugin.json` focused on the existing skills payload.
- Keep plugin and marketplace version, description, keywords, prompts, and shared interface metadata aligned.
- Do not add `hooks`, `apps`, `mcpServers`, icons, logos, or screenshots unless the referenced files exist and pass validation.
- Keep `scripts/sync-to-codex-plugin.sh` destination-agnostic. It must accept `--repo owner/name`, `--dest plugins/code-wiki`, and `--local PATH`.
- Keep `scripts/validate_generated_wiki.py` in the synced runtime payload while excluding development-only scripts and tests.
- Sync `docs/skill-set-design.md` as public documentation without shipping internal implementation plans.
- Update `tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` when sync payload rules change.
- Preserve destination-owned `skills/**/agents/openai.yaml` metadata during sync.

## Adding A Skill

Before adding a skill, answer:

- Does it have a distinct use time?
- Does it need different inputs?
- Does it make the agent follow a different action path?
- Does it have different failure modes?
- Would users invoke it directly?
- Would keeping it inside another skill cause repeated unnecessary context?

If the answer is no, add a checklist or section to an existing skill instead.

## Pull Request Checklist

- Updated or added `skills/<name>/SKILL.md`.
- Added or updated a V2 authority, approval, retrieval, or pairing scenario.
- Updated `README.md` if the public skill list changed.
- Updated `docs/skill-set-design.md` if boundaries changed.
- Updated `tests/skill-set-contract.md`.
- Updated the semantic quality manifest and paired Spec/Reference shallow, complete, or authority-leakage fixtures when Spec sufficiency, feature discovery, Reference depth, evidence specificity, or audit completeness changed.
- Updated generated-Wiki validator cases when domain pairing, policy/view pairing, typed links, coverage evidence, or concern applicability changed.
- Ran `python3 scripts/validate_wiki_contract.py`.
- Ran the generated-Wiki and semantic-quality unit tests.
- Ran plugin validation if `.codex-plugin/plugin.json` or package structure changed.
- Ran `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` if sync behavior changed.

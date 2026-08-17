## Summary

<!-- What does this PR change, and why? One or two sentences. -->

## Type of change

<!-- Check all that apply. -->

- [ ] Skill behavior change (`skills/*/SKILL.md`)
- [ ] New skill
- [ ] Contract / validator change (`scripts/validate_wiki_contract.py`, `tests/skill-set-contract.md`)
- [ ] Plugin packaging (`.codex-plugin/`, `.agents/`, sync script)
- [ ] Docs only (README, examples, design notes)
- [ ] CI / repository tooling

## Affected skills

<!-- List the skills this PR touches, or "none". -->

## Contract impact

<!-- The V2 contract = authority split (Specs > code > Reference), approval gates,
     Spec/Reference domain pairing, and the wiki/ layout. Pick exactly one. -->

- [ ] Does **not** change the contract — wording, docs, or tooling only
- [ ] **Changes the contract** — `scripts/validate_wiki_contract.py` and `tests/skill-set-contract.md` are updated in this PR to match

<!-- If the contract changes, explain what rule changes and why the new rule is safer or more useful: -->

## New skill justification

<!-- Only for PRs adding a skill — answer the questions from CONTRIBUTING.md ("Adding A Skill").
     Delete this section otherwise. -->

- Distinct use time:
- Different inputs:
- Different action path:
- Different failure modes:
- Why it can't live inside an existing skill:

## Verification

<!-- Paste the result line of each command you ran. -->

- [ ] `python3 scripts/validate_wiki_contract.py` passes
- [ ] `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` passes (required if sync or packaging changed)
- [ ] Manually exercised the changed skill with an agent (describe the scenario below, or state why not applicable)

<!-- Manual scenario, if any: prompt given, skill invoked, observed behavior. -->

## Docs and metadata

- [ ] `README.md` updated (required if the public skill list or install flow changed)
- [ ] `docs/skill-set-design.md` updated (required if skill boundaries changed)
- [ ] `CHANGELOG.md` — entry added under `Unreleased`
- [ ] Version bumped in **both** `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` (only for release PRs)

## Notes for the reviewer

<!-- Anything to look at first, known limitations, follow-ups, or open questions. -->

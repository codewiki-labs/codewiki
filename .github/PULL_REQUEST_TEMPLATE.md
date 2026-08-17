## Summary

<!-- What does this PR change, and why? -->

## Checklist

From [CONTRIBUTING.md](../CONTRIBUTING.md):

- [ ] Updated or added `skills/<name>/SKILL.md`
- [ ] Updated `README.md` if the public skill list changed
- [ ] Updated `docs/skill-set-design.md` if skill boundaries changed
- [ ] Updated `tests/skill-set-contract.md`
- [ ] Ran `python3 scripts/validate_wiki_contract.py`
- [ ] Ran `bash tests/codex-plugin-sync/test-sync-to-codex-plugin.sh` (if sync behavior changed)

## Contract impact

- [ ] This PR does **not** change the V2 contract (authority split, approval gates, domain pairing)
- [ ] This PR **changes the contract**, and `scripts/validate_wiki_contract.py` was updated to match

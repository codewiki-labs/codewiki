# Code-Wiki Semantic Quality Fixture Contract

The fixture validates the deterministic subset of feature assignment and trace completeness. It proves that important feature IDs, required trace dimensions, and exact evidence cannot be replaced by folder names, wildcard symbols, one-line flows, or generic test labels.

It does not prove that an agent discovered every feature in an arbitrary repository or that prose claims are true. `creating-code-wiki` and `auditing-code-wiki` still require source inspection and judgment; the fixture prevents regressions in the explicit output contract.

## Shallow Candidate Must Fail

The shallow candidate has the expected domain files but replaces feature traces with vague folders, wildcard symbols, one-line flows, and generic tests. The validator must report a missing trace for every important feature in the manifest.

## Complete Candidate Must Pass

The complete candidate assigns all important fixture features, provides every required trace dimension, and includes every exact evidence string declared by the manifest.

## Authority Must Remain Separate

The complete Reference describes observed implementation only. Desired behavior belongs in approved Specs, and fixture completeness must never be used to infer approval.

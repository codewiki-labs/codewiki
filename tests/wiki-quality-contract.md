# Code-Wiki Semantic Quality Fixture Contract

The fixture validates the deterministic subset of Spec sufficiency, authority separation, feature assignment, and trace completeness. It proves that approved requirement IDs, behavioral evidence, `Spec Basis`, required trace dimensions, and exact implementation evidence cannot be replaced by Reference-only policy, folder names, wildcard symbols, one-line flows, or generic test labels.

It does not prove that an agent discovered every feature in an arbitrary repository or that prose claims are true. `creating-code-wiki` and `auditing-code-wiki` still require source inspection and judgment; the fixture prevents regressions in the explicit output contract.

## Shallow Candidate Must Fail

The shallow candidate has the expected domain files but replaces feature traces with vague folders, wildcard symbols, one-line flows, and generic tests. The validator must report a missing trace for every important feature in the manifest.

## Complete Candidate Must Pass

The complete candidate gives every important feature approved Spec requirements with behavioral evidence, maps them through Reference `Spec Basis`, provides every required trace dimension, and includes every exact implementation evidence string declared by the manifest.

## Authority Must Remain Separate

The complete Reference describes observed implementation only. Desired behavior belongs in approved Specs, and fixture completeness must never be used to infer approval.

## Authority-Leakage Candidate Must Fail

The authority-leakage candidate puts image-token versus per-image pricing exclusivity in Reference while omitting its approved Spec requirement. The validator must report `MU-USAGE-003` as missing even though the Reference trace is otherwise deep and exact.

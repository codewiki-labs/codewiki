# Basic Code-Wiki V2 Workflow Examples

## Project Work Without Explicit Invocation

Prompt:

```text
Fix the failing authentication test in this repository.
```

Expected behavior:

- `using-code-wiki` checks for project memory.
- The agent reads `wiki/index.md` and `wiki/specs/project.md` first.
- It selects authentication domains from `wiki/specs/index.md`, recursively follows `Required Context`, and reads directly relevant `See Also` pages without recursing.
- It consults `reference/coverage.json`, reads paired domain Reference plus any manifest-listed security view needed by the task, then inspects current source and tests.
- It verifies the fix against approved Acceptance Criteria and refreshes stale Reference if needed.

## Create A Wiki

Prompt:

```text
Use creating-code-wiki to initialize persistent project memory for this repository.
```

Expected behavior:

- Inspect the current checkout before drafting, including source, configuration, routes, schemas, runtime composition, and focused tests.
- Record the inspected revision and relevant working-tree state.
- Build a noncanonical Feature Surface Inventory across active surfaces, routes, providers, persistence, configuration, security, usage or audit, failure paths, and focused tests.
- Assign every important feature to one primary domain or provide an explicit evidence-backed exclusion.
- Determine security and architecture applicability from exact source evidence rather than requiring fixed domains or pages.
- Identify logical domains by user responsibility and change boundary rather than folder names.
- Build one complete user-facing proposal containing the taxonomy and all behaviorally complete Spec content outside canonical `wiki/`.
- Put actor permissions, calculations, policy precedence, invariants, lifecycle and failure outcomes, retention, audit meaning, and testable examples in Specs with stable requirement IDs.
- Give every important Reference feature a `Spec Basis` and complete applicable trace with repository-root-relative paths, exact symbols, routes, implementation evidence, and test files.
- Pass the Spec sufficiency, authority-leakage, and Reference coverage gates before creation.
- Separate code-backed Reference facts from candidate durable requirements inferred from code.
- Obtain one user approval for canonical creation, Specs, and taxonomy before writing any files under `wiki/`.
- If desired behavior changes before creation, refresh affected Specs and obtain approval again; refresh implementation-only Reference evidence without asking the user to approve it.
- Create identical Spec and Reference domain file sets at the same relative paths; do not create Reference-only domain files.
- Persist approved-proposal coverage as source-derived `reference/coverage.json`; pair every approved `specs/policies/<concern>.md` with `reference/views/<concern>.md`.
- Keep `specs/project.md` concise and keep important rationale next to its requirement.

## Read Before Editing

Prompt:

```text
I need to change public search permissions.
```

Expected behavior:

- Recover global purpose, priorities, intent, constraints, and non-goals.
- Match `public` and `search` in the domain registry.
- Recursively follow their `Required Context`, such as authentication or roles, and load `See Also` only when directly relevant.
- Read each selected Spec completely, then its paired Reference page.
- Use the coverage manifest to select applicable concern views; do not invent a security page when evidence says `not_applicable`.
- Inspect only the source paths, symbols, routes, and tests needed to establish current behavior.
- Report completion as a requirement-ID Spec conformance matrix; do not require the user to read Reference.

## Usage Calculation Contract

Prompt:

```text
Define and implement provider usage accounting so I only need to review the Spec.
```

Expected behavior:

- Put canonical usage dimensions, non-overlap rules, calculation units, price formulas, image-token versus per-image precedence, terminal usage, ledger meaning, and hand-computed vectors in the Spec.
- Keep provider raw fields, normalizer names, database identifiers, paths, and test locations in agent-facing Reference.
- Verify examples such as 300 cache-write tokens at 1 USD per million producing 0.0003 USD.
- Link current implementation and exact tests to the approved calculation requirement IDs through `Spec Basis`.

## Spec And Code Conflict

Prompt:

```text
The approved upload Spec says 200 MB, but the validator enforces 100 MB. Fix it.
```

Expected behavior:

- Treat the approved Spec as desired-state authority.
- Change code to conform to 200 MB.
- Verify the Spec's Acceptance Criteria.
- Keep the 200 MB requirement; do not rewrite it from implementation drift.
- Refresh Reference only if implementation paths or flow changed.

## Reference And Code Conflict

Prompt:

```text
The upload Reference points to a validator that no longer exists.
```

Expected behavior:

- Follow the active route and current source to find the real validator.
- Update Reference paths, symbols, and flow.
- Do not infer or change requirements from the descriptive correction.

## New Durable Requirement

Prompt:

```text
From now on, document exports must preserve the original filename.
```

Expected behavior:

- Identify this as durable intent.
- Draft the exact affected Spec changes, rationale when useful, and Acceptance Criteria.
- Obtain user approval before canonical Spec updates and implementation.
- After approval, update the Spec, implement it, verify it, and refresh Reference.

## One-Off Request

Prompt:

```text
Run the upload test once with extra debug logging.
```

Expected behavior:

- Do not turn a temporary command into a durable requirement.
- Do not edit Specs.
- Refresh Reference only if the investigation reveals a durable implementation fact or stale path.

## Semantic Compaction

Situation:

```text
The old approved upload limit was 100 MB. The current approved limit is 200 MB.
```

Expected behavior:

- Keep only the current 200 MB requirement in canonical Specs.
- Retain useful current rationale, such as support for large scanned documents.
- Leave detailed historical change tracking to Git.

## Audit Existing Memory

Prompt:

```text
Use auditing-code-wiki to check whether this Wiki is reliable for future agents.
```

Expected behavior:

- Check authority direction, approval integrity, current-intent compaction, and concise always-read memory.
- Compare Spec and Reference domain paths exactly.
- Verify recursive `Required Context`, nonrecursive `See Also`, registries, policy/view pairs, and `reference/coverage.json`.
- Reconstruct a risk-weighted Feature Surface Inventory and compare important source features with domain coverage.
- Reject Specs that need Reference to determine permissions, calculations, invariants, lifecycle, failures, usage, cost, audit, or retention outcomes.
- Reject Reference-only durable policy as authority leakage and reject wildcard symbols, vague folders, one-line flows, and generic tests as insufficient implementation evidence.
- Spot-check Reference paths, complete traces, and high-risk implementation claims against source.
- Propose user-approved Spec fixes separately from safe code-grounded Reference repairs.

## Security Without A Fixed Domain

Prompt:

```text
Create the Wiki and account for security even if this project has no global security policy.
```

Expected behavior:

- Inspect authentication, authorization, ownership, exposure, untrusted input, secrets, sensitive data, and privileged side effects.
- Put applicable durable behavior in its owning domain Spec and current enforcement in the paired domain Reference.
- Create `specs/policies/security.md` only for an approved rule shared across domains; pair it with `reference/views/security.md`.
- Allow a manifest-listed security view without a global policy when cross-domain source navigation is useful.
- For a genuinely securityless scope, record evidence-backed `not_applicable` in `reference/coverage.json` and omit both files.
- Run the plugin's bundled `scripts/validate_generated_wiki.py` with the target repository and Wiki paths after generation.

## With Superpowers

Prompt:

```text
Design and implement the approved search behavior using Superpowers and Code-Wiki.
```

Expected behavior:

- Code-Wiki provides project memory, approved requirements, rationale, Acceptance Criteria, and source navigation.
- Superpowers drives brainstorming, planning, TDD, execution, review, and verification.
- The one-off implementation plan stays outside canonical Specs.
- Completion is judged against the approved Spec, followed by a Reference refresh when code organization changed.

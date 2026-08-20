# Basic Code-Wiki V2 Workflow Examples

## Project Work Without Explicit Invocation

Prompt:

```text
Fix the failing authentication test in this repository.
```

Expected behavior:

- `using-code-wiki` checks for project memory.
- The agent reads `wiki/index.md` and `wiki/specs/project.md` first.
- It selects authentication domains from `wiki/specs/index.md`, follows `Related Domains`, and reads the selected Specs in full.
- It reads paired Reference pages before inspecting current source and tests.
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
- Identify logical domains by user responsibility and change boundary rather than folder names.
- Build one complete proposal containing the exact Wiki tree and all Spec and Reference content outside canonical `wiki/`.
- Give every important feature a complete applicable trace with repository-root-relative paths, exact symbols, routes, contracts, and test files.
- Pass the coverage gate before presenting the proposal for approval.
- Separate code-backed Reference facts from candidate durable requirements inferred from code.
- Obtain one user approval for canonical creation, Specs, and taxonomy before writing any files under `wiki/`.
- If relevant code changes before creation, refresh the affected proposal and obtain approval again.
- Create identical Spec and Reference domain file sets at the same relative paths; do not create Reference-only domain files.
- Keep `specs/project.md` concise and keep important rationale next to its requirement.

## Read Before Editing

Prompt:

```text
I need to change public search permissions.
```

Expected behavior:

- Recover global purpose, priorities, intent, constraints, and non-goals.
- Match `public` and `search` in the domain registry.
- Follow their Related Domains, such as authentication or roles.
- Read each selected Spec completely, then its paired Reference page.
- Inspect only the source paths, symbols, routes, and tests needed to establish current behavior.

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
- Verify Related Domains and registries.
- Reconstruct a risk-weighted Feature Surface Inventory and compare important source features with domain coverage.
- Reject wildcard symbols, vague folders, one-line flows, generic tests, and missing permission, invariant, lifecycle, failure, usage, cost, audit, or retention contracts when those dimensions apply.
- Spot-check Reference paths, complete traces, and high-risk implementation claims against source.
- Propose user-approved Spec fixes separately from safe code-grounded Reference repairs.

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

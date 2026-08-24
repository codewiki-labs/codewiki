# Security Policy And Reference View Design

## Context

Code-Wiki currently makes architecture and security Specs optional while listing
same-named Reference pages in the canonical tree and requiring agents to read
those Reference pages for related work. This preserves authority separation, but
the same Reference path ambiguously acts as an optional Spec counterpart and as
an independent cross-domain implementation summary. It also gives a project no
durable way to distinguish a justified non-applicable concern from an omitted
security review.

## Goals

- Keep approved desired behavior in Specs and source-derived implementation
  facts in Reference.
- Keep exact one-to-one pairing for logical domain files.
- Let security requirements live with the domain that owns the behavior.
- Represent approved cross-domain security or architecture invariants as
  optional policies.
- Represent source-derived cross-domain implementation summaries as optional
  views.
- Omit security artifacts for a project with no material security surface while
  retaining an evidence-backed applicability decision.
- Persist feature coverage and exclusions so they survive the creation session.
- Prevent recursive domain retrieval from expanding through navigational links.

## Canonical Structure

```text
wiki/
├── index.md
├── specs/
│   ├── index.md
│   ├── project.md
│   ├── policies/
│   │   ├── architecture.md     # only with approved global intent
│   │   └── security.md         # only with approved global intent
│   └── domains/
│       └── <domain>.md
└── reference/
    ├── index.md
    ├── overview.md
    ├── coverage.json
    ├── views/
    │   ├── architecture.md     # only when applicable and useful
    │   └── security.md         # only when applicable and useful
    ├── domains/
    │   └── <domain>.md
    └── <optional operational pages>
```

Every `specs/domains/<path>.md` remains paired with exactly one
`reference/domains/<path>.md`. Every `specs/policies/<name>.md` requires
`reference/views/<name>.md`. A Reference view may exist without a policy when it
aggregates source-backed enforcement owned by domain Specs. Its independent
`views/` namespace makes that asymmetry explicit.

## Security Ownership Rules

Security is a concern, not a mandatory catch-all domain.

1. Authentication, authorization, ownership, public boundaries, secret
   handling, sensitive-data outcomes, untrusted input, and privileged side
   effects belong in the Spec domain that owns the affected behavior.
2. A domain such as identity and access is created only when it is a real
   responsibility and change boundary; a generic security domain is not added
   solely to satisfy structure.
3. `specs/policies/security.md` is created only for approved invariants that
   govern multiple domains or the platform as a whole.
4. `reference/views/security.md` is created only when a material security
   surface exists and the cross-domain map improves navigation. Every normative
   claim links to a domain or policy requirement ID; unapproved implementation
   remains a structured `Observed only` or `Confirm needed` statement. In a
   view without a policy, every `Spec Basis` ID resolves exactly in an owning
   domain Spec.
5. When security is not applicable, neither security policy nor security view is
   created. `reference/coverage.json` records the inspected revision, reason,
   and exact evidence for that conclusion.

The same policy/view distinction applies to architecture.

## Persistent Coverage Manifest

`reference/coverage.json` is source-grounded Reference, not approved intent. It
is required after initial Wiki creation and contains:

- `source_revision`, using an immutable full commit ID for Git checkouts
- `features`, each with `feature_id`, classification, primary domain,
  `spec_basis` or an observed-only reason, exact surface evidence, and an
  exclusion reason when excluded
- `concerns`, including security and architecture applicability, owning domains,
  optional policy/view paths, a reason, and exact evidence

For a concern, `applicability` is `applicable` or `not_applicable`.
`not_applicable` requires a non-empty reason and evidence and forbids policy or
view paths. `applicable` requires at least one owning domain. A policy path
requires its paired view path.

## Retrieval Contract

Domain Specs replace the overloaded `Related Domains` closure with two link
types:

- `Required Context`: normative dependencies whose requirements jointly
  determine correctness; follow recursively.
- `See Also`: navigational relationships; load only when the task directly
  needs them and never recurse automatically.

Legacy `Related Domains` links are read one hop and reported for migration.
Creation and substantial regeneration emit only the new sections.

For security or permission work, agents first select the owning domains. They
read `reference/views/security.md` only when the coverage manifest lists it.
When no view exists, they use the manifest applicability decision and paired
domain References rather than treating the missing file as an error.

## Validation

A generated-Wiki validator accepts `--repo-root` and `--wiki-root` and checks:

- core files and persistent coverage manifest
- exact domain pairing
- policy-to-view pairing
- security and architecture applicability invariants
- concern paths and owning domains
- important feature assignment or evidence-backed exclusion
- `spec_basis` versus observed-only classification
- important feature traces and requirement IDs resolving in paired domain pages
- typed link sections and internal link targets in domain and policy Specs
- committed source freshness since `source_revision`, while warning separately about uncommitted non-Wiki paths

Deterministic fixtures cover:

- a project with no security surface
- domain-owned security without a global policy
- an approved global security policy with a paired view
- a Reference-only durable policy that fails authority separation
- invalid concern paths and missing exclusion evidence
- manifest entries whose feature traces or requirement IDs do not resolve

Package contract validation continues to verify that all public docs and skills
describe the same structure. Semantic feature-trace fixtures remain responsible
for deep Reference evidence and authority-leakage checks.

## Migration

- Move approved `specs/security.md` and `specs/architecture.md` to
  `specs/policies/`.
- Move source-derived cross-domain maps to `reference/views/` only when the
  manifest marks the concern applicable.
- Classify existing `Related Domains` links as `Required Context` or `See Also`.
- Build `reference/coverage.json` from the current checkout and record explicit
  exclusions.
- Do not infer policy content from an existing Reference page. Policy migration
  requires evidence of prior user approval or a new approval.

## Non-goals

- Making every project create a security document.
- Replacing domain-owned permission and trust-boundary contracts with one broad
  security Spec.
- Making Reference content part of user approval.
- Treating structural validation as proof that source claims are factually
  correct or that every feature was discovered.

## Acceptance Criteria

1. A no-security fixture passes without security policy or view only when the
   coverage manifest contains an evidence-backed `not_applicable` decision.
2. Domain-owned authentication and authorization pass without a global security
   policy when their domain Spec/Reference pair and applicable concern entry are
   present.
3. A global security policy fails without a paired security view.
4. A security view may exist without a global policy, but durable behavior found
   only in that view still fails the authority-leakage fixture.
5. Only `Required Context` is recursively expanded; `See Also` is not.
6. Package validation and all semantic/generated-Wiki tests pass.

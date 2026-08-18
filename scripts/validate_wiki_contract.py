#!/usr/bin/env python3
"""Validate the Code-Wiki V2 skill-set package contract."""

from pathlib import Path
import json
import re
import sys

from validate_wiki_quality_fixtures import validate_fixture_contract


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED_VERSION = "0.3.0"
PACKAGE_DESCRIPTION = "Persistent project memory and code navigation for coding agents."
PACKAGE_REPOSITORY = "https://github.com/codewiki-labs/codewiki"
AUTHOR_NAME = "code-wiki contributors"

EXPECTED_SKILLS = {
    "using-code-wiki": [
        "Use when starting any conversation in a code repository or project workspace",
        "repository-local persistent project memory",
        "Approved Specs are authoritative over implementation.",
        "Source code is authoritative over Reference.",
        "wiki/index.md",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "Required Context",
        "See Also",
        "wiki/reference/coverage.json",
        "Proposed Spec Change",
        "user approval",
        "Mismatch direction does not grant edit authority.",
        "An underspecified instruction is not approval.",
        "subject, scope, value, unit",
        "checked-out source and observed runtime disagree",
        "single approval artifact",
        "Superpowers owns the workflow",
        "user-facing contract",
        "agent-facing implementation map",
        "Spec conformance",
        "creating-code-wiki",
        "reading-code-wiki",
        "exploring-code-with-wiki",
        "updating-code-wiki",
        "auditing-code-wiki",
        "writing-code-wiki-skills",
    ],
    "creating-code-wiki": [
        "user-approved intent",
        "current implementation",
        "Inspect the current checkout before drafting any Wiki content.",
        "complete Spec proposal",
        "Do not write any files under `wiki/` before user approval.",
        "re-present the affected Spec content",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "wiki/specs/domains/<domain>.md",
        "wiki/specs/policies/security.md",
        "wiki/reference/index.md",
        "wiki/reference/domains/<domain>.md",
        "wiki/reference/views/security.md",
        "wiki/reference/coverage.json",
        "Every Spec has a corresponding Reference",
        "wiki/specs/project.md` is paired with `wiki/reference/overview.md",
        "wiki/specs/index.md` is paired with `wiki/reference/index.md",
        "Every Spec domain has exactly one Reference domain with the same relative path.",
        "Reference-only domain files are invalid.",
        "## Product Priorities",
        "## Global Intent",
        "## Acceptance Criteria",
        "## Required Context",
        "## See Also",
        "## Entry Points",
        "## Key Files And Symbols",
        "## Internal Flow",
        "user approval",
        "Do not create empty canonical Spec skeletons",
        "persistent draft tree",
        "Security is a concern, not a mandatory domain.",
        "Legacy `Related Domains`",
        "not_applicable",
        "taxonomy becomes normative",
        "chronological history",
        "standalone decision store",
        "Feature Surface Inventory",
        "explicit exclusion reason",
        "end-to-end feature trace",
        "behaviorally complete",
        "Users approve Specs and taxonomy, not Reference content.",
        "stable requirement IDs",
        "## Actor And Permission Requirements",
        "## Security And Trust Boundaries",
        "## Calculation And Policy Contracts",
        "## Domain Invariants",
        "## Spec Implementation Map",
        "## Authorization Enforcement",
        "## Invariant Enforcement",
        "## Lifecycle Implementation",
        "## Failure Implementation",
        "## Usage, Cost And Audit Implementation",
        "Spec Basis",
        "authority-leakage gate",
        "Contract Artifacts",
        "Pre-change Checklist",
        "coverage gate",
    ],
    "reading-code-wiki": [
        "Use when starting project-related work in a repository that has a code-wiki",
        "wiki/index.md",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "wiki/reference/coverage.json",
        "Read every selected Spec in full",
        "Required Context",
        "See Also",
        "Legacy `Related Domains`",
        "same relative path",
        "wiki/reference/views/architecture.md",
        "permission or security task",
        "wiki/reference/views/security.md",
        "when the coverage manifest lists it",
        "implementation or bug-fix task",
        "wiki/reference/testing.md",
        "Specs are normative",
        "Reference is descriptive",
        "user-facing contract",
        "agent-facing implementation map",
        "requirement IDs",
        "Spec conformance",
        "larger than 200 lines, always end your response with a one-line oversize note",
        "even when the user asked for a short answer",
        "Do not start compacting",
    ],
    "exploring-code-with-wiki": [
        "Use when source-code inspection is needed and a code-wiki exists",
        "navigation map",
        "Spec differs from code",
        "change the implementation",
        "Reference differs from code",
        "refresh Reference",
        "Never infer a Spec change from code",
        "does not expand the user's requested scope",
        "undocumented logical domain",
        "load its Spec",
        "Required Context",
        "See Also",
        "Acceptance Criteria",
        "Spec Implementation Map",
        "Authorization Enforcement",
        "Invariant Enforcement",
        "Lifecycle Implementation",
        "Failure Implementation",
        "Usage, Cost And Audit Implementation",
        "Spec conformance matrix",
        "requirement ID",
        "Do not require the user to read Reference",
    ],
    "updating-code-wiki": [
        "Use before completing project-related work",
        "durable user intent",
        "semantic compaction",
        "current approved intent",
        "user approval",
        "never silently rewrite Specs",
        "Reference from verified source code",
        "Acceptance Criteria",
        "same relative path",
        "Reference-only domain files are invalid.",
        "wiki/reference/coverage.json",
        "specs/policies",
        "reference/views",
        "applicability",
        "feature surface",
        "end-to-end trace",
        "coverage gate",
        "Reference refresh does not require user approval",
        "authority leakage",
        "Spec Basis",
        "behaviorally complete",
        "Oversize Compaction",
        "larger than 200 lines as an oversize signal",
        "Size is a review trigger, not an authority",
        "Size alone never deletes an approved requirement",
        "obtain user approval before editing the canonical file",
        "Report before changing",
        "do not edit the page first",
        "Delegated compaction protocol",
        "Delegation authorizes rewording and restructuring, never meaning change.",
        "Inventory the page into discrete meaning units",
        "becomes a Proposed Spec Change instead of being compacted",
        "units kept, merged, and dropped",
    ],
    "auditing-code-wiki": [
        "Use when the code-wiki appears stale",
        "Authority direction",
        "Approval integrity",
        "Domain pairing",
        "Policy and view pairing",
        "Reference-only domain files are invalid.",
        "project-to-overview",
        "Taxonomy",
        "Current intent",
        "Always-read memory",
        "Navigation quality",
        "Inventory every file under `wiki/`",
        "canonical location is the approval assertion",
        "Wiki contract/representation",
        "mutation authorization",
        "Feature coverage",
        "reference/coverage.json",
        "not_applicable",
        "Required Context",
        "See Also",
        "Trace completeness",
        "Evidence specificity",
        "risk-weighted Feature Surface Inventory",
        "symbol presence",
        "Spec sufficiency",
        "Authority leakage",
        "user can validate",
        "Spec Basis",
        "Page size",
        "larger than 200 lines is flagged as an oversize signal",
        "Size alone never deletes an approved requirement",
        "do not compact it directly from the audit",
        "follow the `updating-code-wiki` oversize flow",
    ],
    "writing-code-wiki-skills": [
        "Do not create a new skill",
        "description describes when to use",
        "Approved Specs are normative",
        "Source code is authoritative for Reference",
        "domain pairing",
        "Reference-only domain files are invalid.",
        "specs/policies",
        "reference/views",
        "reference/coverage.json",
        "Required Context",
        "See Also",
        "approval gate",
        "test scenarios",
        "semantic quality fixture",
        "user-facing contract",
        "agent-facing implementation map",
        "authority leakage",
        "paired Spec and Reference fixtures",
    ],
}

PACKAGE_FILES = [
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "docs/skill-set-design.md",
    "examples/basic-workflow.md",
    "tests/codex-plugin-sync/test-sync-to-codex-plugin.sh",
    "tests/skill-set-contract.md",
    "scripts/validate_generated_wiki.py",
    "scripts/validate_wiki_quality_fixtures.py",
    "tests/test_generated_wiki_validator.py",
    "tests/test_wiki_quality_fixtures.py",
    "tests/test_wiki_contract_semantic_integration.py",
    "tests/wiki-quality-contract.md",
    "tests/fixtures/wiki-quality/feature-surfaces.json",
    "tests/fixtures/wiki-quality/authority-leakage/specs/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/authority-leakage/specs/domains/model-usage.md",
    "tests/fixtures/wiki-quality/authority-leakage/specs/domains/identity-access.md",
    "tests/fixtures/wiki-quality/authority-leakage/reference/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/authority-leakage/reference/domains/model-usage.md",
    "tests/fixtures/wiki-quality/authority-leakage/reference/domains/identity-access.md",
    "tests/fixtures/wiki-quality/shallow/specs/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/shallow/specs/domains/model-usage.md",
    "tests/fixtures/wiki-quality/shallow/specs/domains/identity-access.md",
    "tests/fixtures/wiki-quality/complete/specs/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/complete/specs/domains/model-usage.md",
    "tests/fixtures/wiki-quality/complete/specs/domains/identity-access.md",
    "tests/fixtures/wiki-quality/shallow/reference/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/shallow/reference/domains/model-usage.md",
    "tests/fixtures/wiki-quality/shallow/reference/domains/identity-access.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/model-usage.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/identity-access.md",
    "tests/fixtures/wiki-quality/complete/specs/policies/security.md",
    "tests/fixtures/wiki-quality/complete/reference/views/security.md",
    "tests/fixtures/wiki-quality/shallow/specs/policies/security.md",
    "tests/fixtures/wiki-quality/shallow/reference/views/security.md",
    "tests/fixtures/wiki-quality/authority-leakage/reference/views/security.md",
]

FORBIDDEN_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
]

V2_CONTENT_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "docs/skill-set-design.md",
    "examples/basic-workflow.md",
]

FORBIDDEN_V1_GUIDANCE = [
    "wiki/modules/",
    "`modules/",
    "wiki/log.md",
    "wiki/decisions/",
    "`decisions/",
]

README_PHRASES = [
    "persistent project memory",
    "approved specs",
    "source code",
    "reference",
    "what should be",
    "what is",
    "where it is",
    "project.md",
    "required context",
    "see also",
    "reference-only domain files are invalid",
    "user approval",
    "current intent",
    "superpowers",
    "default workflow",
    "skills",
    "codex plugin",
    "claude code plugin",
    "contributing",
    "license",
    "feature surface inventory",
    "deep reference",
    "coverage gate",
    "spec-only approval",
    "behaviorally complete",
    "agent-facing reference",
    "authority-leakage gate",
    "spec conformance matrix",
    "specs/policies",
    "reference/views",
    "coverage.json",
    "security is a concern",
    "not_applicable",
    "generated-wiki validator",
]

CONTRACT_REQUIRED_PHRASES = [
    "# Code-Wiki V2 Skill Set Contract",
    "## Scenario: Project Work Without An Explicit Code-Wiki Mention",
    "## Scenario: First V2 Wiki",
    "## Scenario: Feature Surface Coverage During Creation",
    "## Scenario: Spec-Only User Approval",
    "## Scenario: Usage Calculation Is Normative",
    "## Scenario: Agent-Facing Reference Mapping",
    "## Scenario: Deep Domain Reference",
    "## Scenario: Session Recall And Domain Closure",
    "## Scenario: Targeted Source Inspection",
    "## Scenario: Approved Spec Conflicts With Code",
    "## Scenario: Reference Conflicts With Code",
    "## Scenario: Deep Reference Refresh",
    "## Scenario: New Durable Requirement",
    "## Scenario: Exact Spec Is Already Approved In The Request",
    "## Scenario: Underspecified Durable Requirement",
    "## Scenario: Read-Only Mismatch Audit",
    "## Scenario: Ephemeral Request",
    "## Scenario: Semantic Compaction",
    "## Scenario: Oversized Wiki Page",
    "## Scenario: Domain Pairing Audit",
    "## Scenario: Coverage And Trace Audit",
    "## Scenario: Security Is Not Applicable",
    "## Scenario: Domain-Owned Security",
    "## Scenario: Global Security Policy And View",
    "## Scenario: Typed Domain Retrieval",
    "## Scenario: Generated-Wiki Artifact Validation",
    "## Scenario: Source And Runtime Disagree",
    "## Scenario: Superpowers Is Available",
    "## Scenario: Superpowers Is Not Available",
    "## Scenario: Skill Maintenance",
    "## Scenario: Installable Codex Plugin",
    "## Scenario: Installable Claude Code Plugin",
    "## Scenario: User Forbids Wiki Use",
    "## Scenario: No Wiki Exists",
    "## Scenario: Codex Plugin Sync",
    "Reference-only domain files are invalid.",
]

PLUGIN_EXPECTED = {
    "name": "code-wiki",
    "version": EXPECTED_VERSION,
    "description": PACKAGE_DESCRIPTION,
    "skills": "./skills/",
    "license": "MIT",
}

PLUGIN_INTERFACE_EXPECTED = {
    "displayName": "code-wiki",
    "shortDescription": "Persistent project memory for coding agents",
    "developerName": AUTHOR_NAME,
    "category": "Coding",
    "brandColor": "#2563EB",
}

PLUGIN_KEYWORDS = [
    "code-wiki",
    "skills",
    "codex",
    "claude-code",
    "project-memory",
    "specifications",
]

PLUGIN_FORBIDDEN_KEYS = [
    "hooks",
    "apps",
    "mcpServers",
]

# Claude Code discovers ./skills/, ./commands/, ./agents/ automatically, so the
# Claude manifest must stay minimal. Codex presentation fields ('interface') and
# Codex marketplace policy ('policy') must not leak into it.
CLAUDE_PLUGIN_SHARED_KEYS = [
    "name",
    "version",
    "description",
    "license",
    "keywords",
]

CLAUDE_PLUGIN_FORBIDDEN_KEYS = PLUGIN_FORBIDDEN_KEYS + [
    "interface",
    "policy",
    "skills",
    "commands",
    "agents",
]

PLUGIN_FORBIDDEN_INTERFACE_KEYS = [
    "composerIcon",
    "logo",
    "screenshots",
]

SYNC_TEST_PHRASES = [
    "code-wiki",
    ".codex-plugin/plugin.json",
    "skills/using-code-wiki/SKILL.md",
    "Preview includes generated-Wiki validator",
    "preserves destination-owned OpenAI agent metadata",
    "Dirty local apply exits with failure",
    "Clean no-op local apply exits successfully",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def validate_skills(failures: list[str]) -> None:
    if not SKILLS.is_dir():
        failures.append("missing skills directory: skills")
        return

    expected_skill_dirs = set(EXPECTED_SKILLS)
    actual_skill_dirs = {path.name for path in SKILLS.iterdir() if path.is_dir()}
    for skill in sorted(actual_skill_dirs - expected_skill_dirs):
        failures.append(f"unexpected skill directory: skills/{skill}")

    for skill, required_phrases in EXPECTED_SKILLS.items():
        path = SKILLS / skill / "SKILL.md"
        if not path.exists():
            failures.append(f"missing skill: {path.relative_to(ROOT)}")
            continue

        text = read(path)
        fields = parse_frontmatter(text)
        if fields.get("name") != skill:
            failures.append(f"{path.relative_to(ROOT)} has wrong name")

        description = fields.get("description", "")
        if not (description.startswith("Use when ") or description.startswith("Use before ")):
            failures.append(
                f"{path.relative_to(ROOT)} description must start with 'Use when ' or 'Use before '"
            )
        if any(term in description.lower() for term in ["then ", "step", "workflow", "procedure"]):
            failures.append(f"{path.relative_to(ROOT)} description should not summarize procedure")

        for phrase in required_phrases:
            if phrase not in text:
                failures.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")


def validate_package_files(failures: list[str]) -> None:
    for rel in PACKAGE_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"missing package file: {rel}")

    for rel in FORBIDDEN_FILES:
        if (ROOT / rel).exists():
            failures.append(f"forbidden compatibility file still exists: {rel}")

    for rel in V2_CONTENT_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = read(path)
        for phrase in FORBIDDEN_V1_GUIDANCE:
            if phrase in text:
                failures.append(f"{rel} contains V1-only guidance: {phrase}")


def validate_readme(failures: list[str]) -> None:
    path = ROOT / "README.md"
    if not path.exists():
        return
    text = read(path).lower()
    for phrase in README_PHRASES:
        if phrase not in text:
            failures.append(f"README.md missing V2 topic: {phrase}")


def validate_behavioral_contract(failures: list[str]) -> None:
    path = ROOT / "tests" / "skill-set-contract.md"
    if not path.exists():
        return
    text = read(path)
    for phrase in CONTRACT_REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"{path.relative_to(ROOT)} missing contract scenario: {phrase}")


def validate_semantic_fixture_contract(failures: list[str]) -> None:
    for failure in validate_fixture_contract():
        failures.append(f"semantic quality fixture: {failure}")


def validate_plugin_contract(plugin: object, failures: list[str]) -> None:
    if not isinstance(plugin, dict):
        failures.append(".codex-plugin/plugin.json must contain an object")
        return

    for key, expected in PLUGIN_EXPECTED.items():
        if plugin.get(key) != expected:
            failures.append(f".codex-plugin/plugin.json field {key!r} must be {expected!r}")

    author = plugin.get("author")
    if not isinstance(author, dict) or author.get("name") != AUTHOR_NAME:
        failures.append(f".codex-plugin/plugin.json field 'author.name' must be {AUTHOR_NAME!r}")

    if plugin.get("keywords") != PLUGIN_KEYWORDS:
        failures.append(f".codex-plugin/plugin.json field 'keywords' must be {PLUGIN_KEYWORDS!r}")

    for key in PLUGIN_FORBIDDEN_KEYS:
        if key in plugin:
            failures.append(f".codex-plugin/plugin.json must omit {key!r} for a skill-centered plugin")

    interface = plugin.get("interface")
    if not isinstance(interface, dict):
        failures.append(".codex-plugin/plugin.json field 'interface' must be an object")
        return

    for key, expected in PLUGIN_INTERFACE_EXPECTED.items():
        if interface.get(key) != expected:
            failures.append(f".codex-plugin/plugin.json field 'interface.{key}' must be {expected!r}")

    if interface.get("capabilities") != ["Interactive", "Read", "Write"]:
        failures.append(
            ".codex-plugin/plugin.json field 'interface.capabilities' must be ['Interactive', 'Read', 'Write']"
        )

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or len(prompts) != 3 or not all(
        isinstance(prompt, str) and prompt for prompt in prompts
    ):
        failures.append(
            ".codex-plugin/plugin.json field 'interface.defaultPrompt' must contain three non-empty prompts"
        )

    long_description = interface.get("longDescription")
    required_terms = ["user-approved Specs", "Reference", "source code"]
    if not isinstance(long_description, str) or any(term not in long_description for term in required_terms):
        failures.append(
            ".codex-plugin/plugin.json field 'interface.longDescription' must explain approved Specs, Reference, and source code"
        )

    for key in PLUGIN_FORBIDDEN_INTERFACE_KEYS:
        if key in interface:
            failures.append(
                f".codex-plugin/plugin.json must omit interface.{key!r} for a skill-centered plugin"
            )


def validate_marketplace_contract(
    marketplace: object, plugin: object, failures: list[str]
) -> None:
    if not isinstance(marketplace, dict):
        failures.append(".agents/plugins/marketplace.json must contain an object")
        return
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        failures.append(".agents/plugins/marketplace.json must contain exactly one plugin object")
        return
    if not isinstance(plugin, dict):
        return

    entry = plugins[0]
    for key in ["name", "version", "description", "license", "keywords"]:
        if entry.get(key) != plugin.get(key):
            failures.append(f"marketplace plugin field {key!r} must match .codex-plugin/plugin.json")

    plugin_interface_category = plugin.get("interface", {})
    if isinstance(plugin_interface_category, dict):
        expected_category = plugin_interface_category.get("category")
        if entry.get("category") != expected_category:
            failures.append(
                "marketplace plugin field 'category' must match .codex-plugin/plugin.json interface.category"
            )

    author = entry.get("author")
    plugin_author = plugin.get("author")
    if not isinstance(author, dict) or not isinstance(plugin_author, dict) or author.get("name") != plugin_author.get("name"):
        failures.append("marketplace plugin author.name must match .codex-plugin/plugin.json")

    entry_interface = entry.get("interface")
    plugin_interface = plugin.get("interface")
    if not isinstance(entry_interface, dict) or not isinstance(plugin_interface, dict):
        failures.append("both plugin manifests must contain interface objects")
        return
    for key in [
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "brandColor",
        "defaultPrompt",
    ]:
        if entry_interface.get(key) != plugin_interface.get(key):
            failures.append(f"marketplace interface field {key!r} must match .codex-plugin/plugin.json")


def validate_claude_plugin_contract(
    claude_plugin: object, codex_plugin: object, failures: list[str]
) -> None:
    rel = ".claude-plugin/plugin.json"
    if not isinstance(claude_plugin, dict):
        failures.append(f"{rel} must contain an object")
        return

    if isinstance(codex_plugin, dict):
        for key in CLAUDE_PLUGIN_SHARED_KEYS:
            if claude_plugin.get(key) != codex_plugin.get(key):
                failures.append(f"{rel} field {key!r} must match .codex-plugin/plugin.json")

    author = claude_plugin.get("author")
    if not isinstance(author, dict) or author.get("name") != AUTHOR_NAME:
        failures.append(f"{rel} field 'author.name' must be {AUTHOR_NAME!r}")

    for key in ["homepage", "repository"]:
        if claude_plugin.get(key) != PACKAGE_REPOSITORY:
            failures.append(f"{rel} field {key!r} must be {PACKAGE_REPOSITORY!r}")

    for key in CLAUDE_PLUGIN_FORBIDDEN_KEYS:
        if key in claude_plugin:
            failures.append(
                f"{rel} must omit {key!r}; Claude Code discovers ./skills/ automatically "
                "and Codex-only presentation fields do not belong here"
            )


def validate_claude_marketplace_contract(
    marketplace: object, claude_plugin: object, failures: list[str]
) -> None:
    rel = ".claude-plugin/marketplace.json"
    if not isinstance(marketplace, dict):
        failures.append(f"{rel} must contain an object")
        return

    if marketplace.get("name") != "code-wiki":
        failures.append(f"{rel} field 'name' must be 'code-wiki'")

    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or owner.get("name") != AUTHOR_NAME:
        failures.append(f"{rel} field 'owner.name' must be {AUTHOR_NAME!r}")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
        failures.append(f"{rel} must contain exactly one plugin object")
        return
    if not isinstance(claude_plugin, dict):
        return

    entry = plugins[0]
    for key in CLAUDE_PLUGIN_SHARED_KEYS:
        if entry.get(key) != claude_plugin.get(key):
            failures.append(f"{rel} plugin field {key!r} must match .claude-plugin/plugin.json")

    author = entry.get("author")
    claude_author = claude_plugin.get("author")
    if not isinstance(author, dict) or not isinstance(claude_author, dict) or author.get("name") != claude_author.get("name"):
        failures.append(f"{rel} plugin author.name must match .claude-plugin/plugin.json")

    if not entry.get("source"):
        failures.append(f"{rel} plugin entry must declare a 'source'")

    for key in ["interface", "policy"]:
        if key in entry:
            failures.append(f"{rel} plugin entry must omit Codex-only field {key!r}")


def validate_sync_test(failures: list[str]) -> None:
    path = ROOT / "tests" / "codex-plugin-sync" / "test-sync-to-codex-plugin.sh"
    if not path.exists():
        return
    text = read(path)
    for phrase in SYNC_TEST_PHRASES:
        if phrase not in text:
            failures.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")
    if f'MANIFEST_VERSION="{EXPECTED_VERSION}"' not in text:
        failures.append(
            f"{path.relative_to(ROOT)} must exercise manifest version {EXPECTED_VERSION}"
        )
    if not path.stat().st_mode & 0o111:
        failures.append(f"{path.relative_to(ROOT)} must be executable")


def main() -> int:
    failures: list[str] = []

    validate_skills(failures)
    validate_package_files(failures)
    validate_readme(failures)
    validate_behavioral_contract(failures)
    validate_semantic_fixture_contract(failures)

    plugin: object = None
    plugin_path = ROOT / ".codex-plugin" / "plugin.json"
    if plugin_path.exists():
        try:
            plugin = json.loads(read(plugin_path))
        except json.JSONDecodeError as exc:
            failures.append(f".codex-plugin/plugin.json is invalid JSON: {exc}")
        else:
            validate_plugin_contract(plugin, failures)

    marketplace_path = ROOT / ".agents" / "plugins" / "marketplace.json"
    if marketplace_path.exists():
        try:
            marketplace = json.loads(read(marketplace_path))
        except json.JSONDecodeError as exc:
            failures.append(f".agents/plugins/marketplace.json is invalid JSON: {exc}")
        else:
            validate_marketplace_contract(marketplace, plugin, failures)

    claude_plugin: object = None
    claude_plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    if claude_plugin_path.exists():
        try:
            claude_plugin = json.loads(read(claude_plugin_path))
        except json.JSONDecodeError as exc:
            failures.append(f".claude-plugin/plugin.json is invalid JSON: {exc}")
        else:
            validate_claude_plugin_contract(claude_plugin, plugin, failures)

    claude_marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    if claude_marketplace_path.exists():
        try:
            claude_marketplace = json.loads(read(claude_marketplace_path))
        except json.JSONDecodeError as exc:
            failures.append(f".claude-plugin/marketplace.json is invalid JSON: {exc}")
        else:
            validate_claude_marketplace_contract(claude_marketplace, claude_plugin, failures)

    validate_sync_test(failures)

    if failures:
        print("Code-Wiki V2 skill-set contract failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Code-Wiki V2 skill-set contract passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

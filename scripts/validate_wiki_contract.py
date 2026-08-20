#!/usr/bin/env python3
"""Validate the Code-Wiki V2 skill-set package contract."""

from pathlib import Path
import json
import re
import sys

from validate_wiki_quality_fixtures import validate_fixture_contract


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED_SKILLS = {
    "using-code-wiki": [
        "Use when starting any conversation in a code repository or project workspace",
        "repository-local persistent project memory",
        "Approved Specs are authoritative over implementation.",
        "Source code is authoritative over Reference.",
        "wiki/index.md",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "Related Domains",
        "Proposed Spec Change",
        "user approval",
        "Mismatch direction does not grant edit authority.",
        "An underspecified instruction is not approval.",
        "subject, scope, value, unit",
        "checked-out source and observed runtime disagree",
        "single approval artifact",
        "Superpowers owns the workflow",
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
        "complete Wiki proposal",
        "Do not write any files under `wiki/` before user approval.",
        "re-present the revised proposal",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "wiki/specs/domains/<domain>.md",
        "wiki/reference/index.md",
        "wiki/reference/domains/<domain>.md",
        "Every Spec has a corresponding Reference",
        "wiki/specs/project.md` is paired with `wiki/reference/overview.md",
        "wiki/specs/index.md` is paired with `wiki/reference/index.md",
        "Every Spec domain has exactly one Reference domain with the same relative path.",
        "Reference-only domain files are invalid.",
        "## Product Priorities",
        "## Global Intent",
        "## Acceptance Criteria",
        "## Related Domains",
        "## Entry Points",
        "## Key Files And Symbols",
        "## Internal Flow",
        "user approval",
        "Do not create empty canonical Spec skeletons",
        "persistent draft tree",
        "Architecture and security Specs are optional",
        "taxonomy becomes normative",
        "chronological history",
        "standalone decision store",
        "Feature Surface Inventory",
        "explicit exclusion reason",
        "end-to-end feature trace",
        "Actor / Permission Contract",
        "Domain Invariants",
        "Lifecycle And Side Effects",
        "Failure Semantics",
        "Usage, Cost And Audit Contract",
        "Contract Artifacts",
        "Pre-change Checklist",
        "coverage gate",
    ],
    "reading-code-wiki": [
        "Use when starting project-related work in a repository that has a code-wiki",
        "wiki/index.md",
        "wiki/specs/project.md",
        "wiki/specs/index.md",
        "Read every selected Spec in full",
        "Related Domains",
        "same relative path",
        "wiki/reference/architecture.md",
        "whether or not the corresponding Spec exists",
        "permission or security task",
        "wiki/reference/security.md",
        "implementation or bug-fix task",
        "wiki/reference/testing.md",
        "Specs are normative",
        "Reference is descriptive",
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
        "Acceptance Criteria",
        "Actor / Permission Contract",
        "Domain Invariants",
        "Lifecycle And Side Effects",
        "Failure Semantics",
        "Usage, Cost And Audit Contract",
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
        "feature surface",
        "end-to-end trace",
        "coverage gate",
    ],
    "auditing-code-wiki": [
        "Use when the code-wiki appears stale",
        "Authority direction",
        "Approval integrity",
        "Domain pairing",
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
        "Trace completeness",
        "Evidence specificity",
        "risk-weighted Feature Surface Inventory",
        "symbol presence",
    ],
    "writing-code-wiki-skills": [
        "Do not create a new skill",
        "description describes when to use",
        "Approved Specs are normative",
        "Source code is authoritative for Reference",
        "domain pairing",
        "Reference-only domain files are invalid.",
        "approval gate",
        "test scenarios",
        "semantic quality fixture",
    ],
}

PACKAGE_FILES = [
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "docs/skill-set-design.md",
    "examples/basic-workflow.md",
    "tests/codex-plugin-sync/test-sync-to-codex-plugin.sh",
    "tests/skill-set-contract.md",
    "scripts/validate_wiki_quality_fixtures.py",
    "tests/test_wiki_quality_fixtures.py",
    "tests/test_wiki_contract_semantic_integration.py",
    "tests/wiki-quality-contract.md",
    "tests/fixtures/wiki-quality/feature-surfaces.json",
    "tests/fixtures/wiki-quality/shallow/reference/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/shallow/reference/domains/model-usage.md",
    "tests/fixtures/wiki-quality/shallow/reference/domains/identity-access.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/workplace-tools.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/model-usage.md",
    "tests/fixtures/wiki-quality/complete/reference/domains/identity-access.md",
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
    "related domains",
    "reference-only domain files are invalid",
    "user approval",
    "current intent",
    "superpowers",
    "default workflow",
    "skills",
    "codex plugin",
    "contributing",
    "license",
    "feature surface inventory",
    "deep reference",
    "coverage gate",
]

CONTRACT_REQUIRED_PHRASES = [
    "# Code-Wiki V2 Skill Set Contract",
    "## Scenario: Project Work Without An Explicit Code-Wiki Mention",
    "## Scenario: First V2 Wiki",
    "## Scenario: Feature Surface Coverage During Creation",
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
    "## Scenario: Domain Pairing Audit",
    "## Scenario: Coverage And Trace Audit",
    "## Scenario: Source And Runtime Disagree",
    "## Scenario: Superpowers Is Available",
    "## Scenario: Superpowers Is Not Available",
    "## Scenario: Skill Maintenance",
    "## Scenario: Installable Codex Plugin",
    "## Scenario: User Forbids Wiki Use",
    "## Scenario: No Wiki Exists",
    "## Scenario: Codex Plugin Sync",
    "Reference-only domain files are invalid.",
]

PLUGIN_EXPECTED = {
    "name": "code-wiki",
    "version": "0.2.0",
    "description": "Persistent project memory and code navigation for Codex agents.",
    "skills": "./skills/",
    "license": "MIT",
}

PLUGIN_INTERFACE_EXPECTED = {
    "displayName": "code-wiki",
    "shortDescription": "Persistent project memory for Codex agents",
    "developerName": "code-wiki contributors",
    "category": "Coding",
    "brandColor": "#2563EB",
}

PLUGIN_KEYWORDS = [
    "code-wiki",
    "skills",
    "codex",
    "project-memory",
    "specifications",
]

PLUGIN_FORBIDDEN_KEYS = [
    "hooks",
    "apps",
    "mcpServers",
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
    if not isinstance(author, dict) or author.get("name") != "code-wiki contributors":
        failures.append(".codex-plugin/plugin.json field 'author.name' must be 'code-wiki contributors'")

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
        "capabilities",
        "brandColor",
        "defaultPrompt",
    ]:
        if entry_interface.get(key) != plugin_interface.get(key):
            failures.append(f"marketplace interface field {key!r} must match .codex-plugin/plugin.json")


def validate_sync_test(failures: list[str]) -> None:
    path = ROOT / "tests" / "codex-plugin-sync" / "test-sync-to-codex-plugin.sh"
    if not path.exists():
        return
    text = read(path)
    for phrase in SYNC_TEST_PHRASES:
        if phrase not in text:
            failures.append(f"{path.relative_to(ROOT)} missing phrase: {phrase}")
    if 'MANIFEST_VERSION="0.2.0"' not in text:
        failures.append(f"{path.relative_to(ROOT)} must exercise manifest version 0.2.0")
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

#!/usr/bin/env python3
"""Validate a generated Code-Wiki artifact against its source checkout."""

from argparse import ArgumentParser
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Optional


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from codewiki.core.markdown import (  # noqa: E402
    _parent_level_two_section,
    feature_block,
    mask_markdown_fences as _mask_markdown_fences,
    requirement_block,
    requirement_exists,
)


CORE_FILES = (
    "index.md",
    "specs/index.md",
    "specs/project.md",
    "reference/index.md",
    "reference/overview.md",
    "reference/coverage.json",
)
CLASSIFICATIONS = {"important", "supporting", "placeholder", "excluded"}
SURFACE_KEYS = {"ui", "api", "jobs", "providers", "schemas", "tests"}
CONCERN_APPLICABILITY = {"applicable", "not_applicable"}
REQUIRED_CONCERNS = {"architecture", "security"}
REQUIREMENT_SECTIONS = {
    "Requirements",
    "Actor And Permission Requirements",
    "Security And Trust Boundaries",
    "Calculation And Policy Contracts",
    "Domain Invariants",
    "Lifecycle And Side Effects",
    "Failure And Recovery Requirements",
    "Data, Retention And Audit Requirements",
    "Invariants",
    "Failure And Audit Requirements",
}
REQUIREMENT_ID = re.compile(r".+-R\d{3}$")
ACCEPTANCE_CRITERION_ID = re.compile(r".+-AC\d{3}$")


def relative_markdown_files(root: Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*.md")
        if path.is_file()
    }


def load_coverage(wiki_root: Path) -> tuple[dict[str, Any], list[str]]:
    path = wiki_root / "reference" / "coverage.json"
    if not path.is_file():
        return {}, ["missing required file reference/coverage.json"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {}, [f"reference/coverage.json is invalid JSON: {error}"]
    if not isinstance(value, dict):
        return {}, ["reference/coverage.json must contain an object"]
    return value, []


def validate_core_files(wiki_root: Path) -> list[str]:
    return [
        f"missing required file {relative}"
        for relative in CORE_FILES
        if not (wiki_root / relative).is_file()
    ]


def validate_domain_pairs(wiki_root: Path) -> list[str]:
    specs_root = wiki_root / "specs" / "domains"
    reference_root = wiki_root / "reference" / "domains"
    specs = relative_markdown_files(specs_root)
    references = relative_markdown_files(reference_root)
    failures = [
        f"missing Reference domain reference/domains/{relative}"
        for relative in sorted(specs - references)
    ]
    failures.extend(
        f"missing Spec domain specs/domains/{relative}"
        for relative in sorted(references - specs)
    )
    return failures


def domain_ids(wiki_root: Path) -> set[str]:
    return {
        relative.removesuffix(".md")
        for relative in relative_markdown_files(wiki_root / "specs" / "domains")
    }


def _safe_evidence_path(repo_root: Path, value: object) -> Optional[Path]:
    if not isinstance(value, str) or not value.strip():
        return None
    relative = Path(value)
    if relative.is_absolute():
        return None
    candidate = (repo_root / relative).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return candidate


def validate_evidence(
    repo_root: Path,
    owner: str,
    evidence: object,
    required_message: str,
) -> list[str]:
    if not isinstance(evidence, list) or not evidence:
        return [required_message]
    failures: list[str] = []
    for value in evidence:
        path = _safe_evidence_path(repo_root, value)
        if path is None:
            failures.append(f"{owner}: invalid evidence path {value!r}")
        elif not path.is_file():
            failures.append(f"{owner}: evidence path does not exist: {value}")
    return failures


def validate_spec_item_headings(wiki_root: Path) -> list[str]:
    failures: list[str] = []
    specs_root = wiki_root / "specs"
    for typed_root in (specs_root / "domains", specs_root / "policies"):
        paths = sorted(typed_root.rglob("*.md")) if typed_root.is_dir() else []
        for path in paths:
            relative = path.relative_to(wiki_root).as_posix()
            text = path.read_text(encoding="utf-8")
            structure = _mask_markdown_fences(text)
            item_headings = list(
                re.finditer(
                    r"(?m)^### (?:(Requirement|Acceptance Criterion): )?"
                    r"`([^`\n]+)`[ \t]*\r?$",
                    structure,
                )
            )
            seen_item_ids: set[str] = set()
            for match in item_headings:
                legacy_label = match.group(1)
                item_id = match.group(2)
                if legacy_label is None and not (
                    REQUIREMENT_ID.fullmatch(item_id)
                    or ACCEPTANCE_CRITERION_ID.fullmatch(item_id)
                ):
                    continue
                if (
                    legacy_label == "Requirement"
                    and ACCEPTANCE_CRITERION_ID.fullmatch(item_id)
                ):
                    failures.append(
                        f"{relative}: acceptance criterion ID {item_id} cannot "
                        "use legacy Requirement label"
                    )
                elif (
                    legacy_label == "Acceptance Criterion"
                    and REQUIREMENT_ID.fullmatch(item_id)
                ):
                    failures.append(
                        f"{relative}: requirement ID {item_id} cannot use "
                        "legacy Acceptance Criterion label"
                    )
                if item_id in seen_item_ids:
                    failures.append(
                        f"{relative}: duplicate Spec item ID {item_id}"
                    )
                else:
                    seen_item_ids.add(item_id)

            for match in re.finditer(
                r"(?m)^### `([^`\n]+)`[ \t]*\r?$",
                structure,
            ):
                item_id = match.group(1)
                section = _parent_level_two_section(structure, match.start())
                if section == "Acceptance Criteria":
                    if REQUIREMENT_ID.fullmatch(item_id):
                        failures.append(
                            f"{relative}: requirement ID {item_id} cannot appear "
                            "under Acceptance Criteria"
                        )
                    elif not ACCEPTANCE_CRITERION_ID.fullmatch(item_id):
                        failures.append(
                            f"{relative}: compact Spec item ID {item_id} under "
                            "Acceptance Criteria must end with -AC followed by "
                            "three digits"
                        )
                elif section in REQUIREMENT_SECTIONS:
                    if ACCEPTANCE_CRITERION_ID.fullmatch(item_id):
                        failures.append(
                            f"{relative}: acceptance criterion ID {item_id} must "
                            "appear under Acceptance Criteria"
                        )
                    elif not REQUIREMENT_ID.fullmatch(item_id):
                        failures.append(
                            f"{relative}: compact Spec item ID {item_id} under "
                            f"{section} must end with -R followed by three digits"
                        )
                elif ACCEPTANCE_CRITERION_ID.fullmatch(item_id):
                    failures.append(
                        f"{relative}: acceptance criterion ID {item_id} must "
                        "appear under Acceptance Criteria"
                    )
                elif REQUIREMENT_ID.fullmatch(item_id):
                    failures.append(
                        f"{relative}: requirement ID {item_id} must appear under "
                        "a requirement-bearing section"
                    )
                else:
                    failures.append(
                        f"{relative}: compact Spec item ID {item_id} must end "
                        "with -R or -AC followed by three digits"
                    )
    return failures


def backticked_ids(text: str) -> set[str]:
    return set(re.findall(r"`([^`\n]+)`", text))


def _section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
    )
    return match.group(1) if match else ""


def has_observation_marker(text: str) -> bool:
    return bool(
        re.search(
            r"(?m)^(?:[-*]\s*)?(?:Observed only|Confirm needed):\s*\S",
            text,
        )
    )


def view_spec_basis_ids(text: str) -> set[str]:
    identifiers: set[str] = set()
    for match in re.finditer(r"(?m)^- Spec Basis:\s*(.+)$", text):
        identifiers.update(backticked_ids(match.group(1)))
    identifiers.update(backticked_ids(_section_body(text, "Spec Basis")))
    return identifiers


def _git_command(
    repo_root: Path,
    *args: str,
) -> Optional[subprocess.CompletedProcess[str]]:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None


def _paths_outside_wiki(
    git_root: Path,
    wiki_root: Path,
    paths: list[str],
) -> list[str]:
    try:
        wiki_relative = wiki_root.resolve().relative_to(git_root.resolve()).as_posix()
    except ValueError:
        wiki_relative = None
    if not wiki_relative or wiki_relative == ".":
        return sorted(set(paths))
    prefix = f"{wiki_relative}/"
    return sorted(
        {
            path
            for path in paths
            if path and path != wiki_relative and not path.startswith(prefix)
        }
    )


def validate_source_revision(
    repo_root: Path,
    wiki_root: Path,
    source_revision: str,
) -> list[str]:
    top_level = _git_command(repo_root, "rev-parse", "--show-toplevel")
    if top_level is None or top_level.returncode != 0:
        return []
    git_root = Path(top_level.stdout.strip()).resolve()
    if git_root != repo_root.resolve():
        return [
            f"repo_root must be the Git worktree root: expected {git_root}"
        ]

    head_result = _git_command(repo_root, "rev-parse", "--verify", "HEAD")
    revision_result = _git_command(
        repo_root,
        "rev-parse",
        "--verify",
        f"{source_revision}^{{commit}}",
    )
    if head_result is None or head_result.returncode != 0:
        return []
    if revision_result is None or revision_result.returncode != 0:
        return [
            f"coverage source_revision does not resolve to a commit: {source_revision}"
        ]

    head = head_result.stdout.strip()
    resolved_revision = revision_result.stdout.strip()
    if source_revision != resolved_revision:
        return [
            "coverage source_revision must be an immutable full commit ID: "
            f"{source_revision} resolves to {resolved_revision}"
        ]

    ancestry = _git_command(
        repo_root,
        "merge-base",
        "--is-ancestor",
        resolved_revision,
        head,
    )
    if ancestry is None or ancestry.returncode not in {0, 1}:
        return ["could not compare coverage source_revision with repository HEAD"]
    if ancestry.returncode == 1:
        return [
            f"coverage source_revision {resolved_revision} is not an ancestor "
            f"of repository HEAD {head}"
        ]

    changed_result = _git_command(
        repo_root,
        "diff",
        "--name-only",
        "--no-renames",
        f"{resolved_revision}..{head}",
        "--",
    )
    if changed_result is None or changed_result.returncode != 0:
        return ["could not compare source paths with coverage source_revision"]
    changed = _paths_outside_wiki(
        git_root,
        wiki_root,
        changed_result.stdout.splitlines(),
    )
    if changed:
        return [
            f"coverage source changed since source_revision {resolved_revision}: "
            + ", ".join(changed)
        ]
    return []


def uncommitted_paths_outside_wiki(repo_root: Path, wiki_root: Path) -> list[str]:
    top_level = _git_command(repo_root, "rev-parse", "--show-toplevel")
    if top_level is None or top_level.returncode != 0:
        return []
    git_root = Path(top_level.stdout.strip()).resolve()
    commands = (
        ("diff", "--name-only", "--no-renames", "--"),
        ("diff", "--cached", "--name-only", "--no-renames", "--"),
        ("ls-files", "--others", "--exclude-standard", "--"),
    )
    paths: list[str] = []
    for command in commands:
        result = _git_command(repo_root, *command)
        if result is not None and result.returncode == 0:
            paths.extend(result.stdout.splitlines())
    return _paths_outside_wiki(git_root, wiki_root, paths)


def validate_features(
    repo_root: Path,
    wiki_root: Path,
    coverage: dict[str, Any],
) -> list[str]:
    features = coverage.get("features")
    if not isinstance(features, list):
        return ["coverage features must be an array"]
    known_domains = domain_ids(wiki_root)
    seen: set[str] = set()
    failures: list[str] = []
    for index, feature in enumerate(features):
        owner = f"feature[{index}]"
        if not isinstance(feature, dict):
            failures.append(f"{owner}: must be an object")
            continue
        feature_id = feature.get("feature_id")
        if not isinstance(feature_id, str) or not feature_id.strip():
            failures.append(f"{owner}: feature_id is required")
            continue
        owner = feature_id
        if feature_id in seen:
            failures.append(f"{owner}: duplicate feature_id")
        seen.add(feature_id)

        classification = feature.get("classification")
        if (
            not isinstance(classification, str)
            or classification not in CLASSIFICATIONS
        ):
            failures.append(f"{owner}: invalid classification {classification!r}")
            continue

        primary_domain = feature.get("primary_domain")
        if classification in {"important", "supporting"}:
            if not isinstance(primary_domain, str) or not primary_domain:
                failures.append(
                    f"{owner}: {classification} feature requires primary_domain"
                )
            elif primary_domain not in known_domains:
                failures.append(f"{owner}: unknown primary_domain {primary_domain}")
        elif primary_domain is not None:
            if not isinstance(primary_domain, str):
                failures.append(f"{owner}: primary_domain must be a string or null")
            elif primary_domain not in known_domains:
                failures.append(f"{owner}: unknown primary_domain {primary_domain}")

        spec_basis = feature.get("spec_basis")
        normalized_spec_basis: list[str] = []
        if spec_basis is not None:
            if not isinstance(spec_basis, list):
                failures.append(f"{owner}: spec_basis must be an array")
            else:
                for requirement_id in spec_basis:
                    if (
                        not isinstance(requirement_id, str)
                        or not requirement_id.strip()
                    ):
                        failures.append(
                            f"{owner}: spec_basis entries must be non-empty strings"
                        )
                    elif requirement_id in normalized_spec_basis:
                        failures.append(
                            f"{owner}: duplicate Spec Basis {requirement_id}"
                        )
                    else:
                        normalized_spec_basis.append(requirement_id)
        observed_only_reason = feature.get("observed_only_reason")
        if classification in {"important", "supporting"}:
            has_spec_basis = bool(normalized_spec_basis)
            has_observed_reason = isinstance(
                observed_only_reason,
                str,
            ) and bool(observed_only_reason.strip())
            if not has_spec_basis and not has_observed_reason:
                failures.append(
                    f"{owner}: {classification} feature requires spec_basis "
                    "or observed_only_reason"
                )
            elif has_spec_basis and has_observed_reason:
                failures.append(
                    f"{owner}: {classification} feature cannot combine spec_basis "
                    "and observed_only_reason"
                )

            if isinstance(primary_domain, str) and primary_domain in known_domains:
                spec_relative = f"specs/domains/{primary_domain}.md"
                reference_relative = f"reference/domains/{primary_domain}.md"
                spec_path = wiki_root / spec_relative
                reference_path = wiki_root / reference_relative
                if has_spec_basis and spec_path.is_file():
                    spec_text = spec_path.read_text(encoding="utf-8")
                    for requirement_id in normalized_spec_basis:
                        if not requirement_exists(spec_text, requirement_id):
                            failures.append(
                                f"{owner}: unknown Spec Basis {requirement_id} "
                                f"in {spec_relative}"
                            )
                if reference_path.is_file():
                    reference_text = reference_path.read_text(encoding="utf-8")
                    block = feature_block(reference_text, feature_id)
                    if block is None and classification == "important":
                        failures.append(
                            f"{owner}: missing Reference feature trace "
                            f"in {reference_relative}"
                        )
                    elif block is not None and has_spec_basis:
                        basis_line = re.search(
                            r"(?m)^- Spec Basis:\s*(.+)$",
                            block,
                        )
                        basis_ids = (
                            backticked_ids(basis_line.group(1))
                            if basis_line
                            else set()
                        )
                        for requirement_id in normalized_spec_basis:
                            if requirement_id not in basis_ids:
                                failures.append(
                                    f"{owner}: Reference feature trace missing "
                                    f"Spec Basis {requirement_id}"
                                )
                    elif (
                        block is not None
                        and has_observed_reason
                        and not has_observation_marker(block)
                    ):
                        failures.append(
                            f"{owner}: observed-only Reference trace must be labeled "
                            "Observed only or Confirm needed"
                        )

        if classification in {"placeholder", "excluded"}:
            reason = feature.get("exclusion_reason")
            if not isinstance(reason, str) or not reason.strip():
                failures.append(
                    f"{owner}: {classification} feature requires exclusion_reason"
                )

        surfaces = feature.get("surfaces")
        if not isinstance(surfaces, dict):
            failures.append(f"{owner}: surfaces must be an object")
            continue
        evidence: list[object] = []
        for key, values in surfaces.items():
            if key not in SURFACE_KEYS:
                failures.append(f"{owner}: unknown surface dimension {key}")
                continue
            if not isinstance(values, list):
                failures.append(f"{owner}: surfaces.{key} must be an array")
                continue
            evidence.extend(values)
        failures.extend(
            validate_evidence(
                repo_root,
                owner,
                evidence,
                f"{owner}: surfaces require at least one exact evidence path",
            )
        )
    return failures


def validate_concerns(
    repo_root: Path,
    wiki_root: Path,
    coverage: dict[str, Any],
) -> list[str]:
    concerns = coverage.get("concerns")
    if not isinstance(concerns, dict):
        return ["coverage concerns must be an object"]
    failures = [
        f"missing required concern {concern}"
        for concern in sorted(REQUIRED_CONCERNS - set(concerns))
    ]
    known_domains = domain_ids(wiki_root)
    for concern_id, concern in concerns.items():
        if not isinstance(concern, dict):
            failures.append(f"{concern_id}: concern must be an object")
            continue
        applicability = concern.get("applicability")
        if (
            not isinstance(applicability, str)
            or applicability not in CONCERN_APPLICABILITY
        ):
            failures.append(f"{concern_id}: invalid applicability {applicability!r}")
            continue
        owning_domains = concern.get("owning_domains")
        if not isinstance(owning_domains, list):
            failures.append(f"{concern_id}: owning_domains must be an array")
            owning_domains = []
        for domain in owning_domains:
            if not isinstance(domain, str) or not domain.strip():
                failures.append(
                    f"{concern_id}: owning domain entries must be non-empty strings"
                )
            elif domain not in known_domains:
                failures.append(f"{concern_id}: unknown owning domain {domain}")

        reason = concern.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            failures.append(f"{concern_id}: {applicability} requires a reason")
        failures.extend(
            validate_evidence(
                repo_root,
                concern_id,
                concern.get("evidence"),
                f"{concern_id}: {applicability} requires evidence",
            )
        )

        policy_path = concern.get("policy_path")
        view_path = concern.get("view_path")
        if applicability == "not_applicable":
            if owning_domains:
                failures.append(
                    f"{concern_id}: not_applicable forbids owning_domains"
                )
            if policy_path is not None:
                failures.append(f"{concern_id}: not_applicable forbids policy_path")
            if view_path is not None:
                failures.append(f"{concern_id}: not_applicable forbids view_path")
            continue

        if not owning_domains:
            failures.append(f"{concern_id}: applicable requires owning_domains")
        if policy_path is not None and view_path is None:
            failures.append(f"{concern_id}: policy_path requires view_path")
        expected_policy = f"specs/policies/{concern_id}.md"
        expected_view = f"reference/views/{concern_id}.md"
        if policy_path is not None:
            if policy_path != expected_policy:
                failures.append(
                    f"{concern_id}: policy_path must be {expected_policy}"
                )
            elif not (wiki_root / policy_path).is_file():
                failures.append(
                    f"{concern_id}: policy_path does not exist: {policy_path}"
                )
        if view_path is not None:
            if view_path != expected_view:
                failures.append(f"{concern_id}: view_path must be {expected_view}")
            elif not (wiki_root / view_path).is_file():
                failures.append(
                    f"{concern_id}: view_path does not exist: {view_path}"
                )
    return failures


def validate_policy_views(
    wiki_root: Path,
    concerns: object,
) -> list[str]:
    policies = relative_markdown_files(wiki_root / "specs" / "policies")
    views = relative_markdown_files(wiki_root / "reference" / "views")
    failures = [
        f"policy {relative} missing paired view"
        for relative in sorted(policies - views)
    ]
    if not isinstance(concerns, dict):
        return failures
    policy_paths = {
        path
        for value in concerns.values()
        if isinstance(value, dict)
        for path in [value.get("policy_path")]
        if isinstance(path, str)
    }
    view_paths = {
        path
        for value in concerns.values()
        if isinstance(value, dict)
        for path in [value.get("view_path")]
        if isinstance(path, str)
    }
    view_concerns = {
        view_path: value
        for value in concerns.values()
        if isinstance(value, dict)
        for view_path in [value.get("view_path")]
        if isinstance(view_path, str)
    }
    for relative in sorted(policies):
        path = f"specs/policies/{relative}"
        if path not in policy_paths:
            failures.append(f"policy {relative} missing coverage concern")
    for relative in sorted(views):
        path = f"reference/views/{relative}"
        if path not in view_paths:
            failures.append(f"view {relative} missing coverage concern")
        elif view_concerns[path].get("policy_path") is None:
            text = (wiki_root / path).read_text(encoding="utf-8")
            basis_ids = view_spec_basis_ids(text)
            if not basis_ids and not has_observation_marker(text):
                failures.append(
                    f"view {relative} without policy requires Spec Basis, "
                    "Observed only, or Confirm needed"
                )
            owning_domains = view_concerns[path].get("owning_domains")
            valid_domains = (
                [
                    domain
                    for domain in owning_domains
                    if isinstance(domain, str) and domain in domain_ids(wiki_root)
                ]
                if isinstance(owning_domains, list)
                else []
            )
            for requirement_id in sorted(basis_ids):
                if any(
                    requirement_exists(
                        (
                            wiki_root / "specs" / "domains" / f"{domain}.md"
                        ).read_text(encoding="utf-8"),
                        requirement_id,
                    )
                    for domain in valid_domains
                ):
                    continue
                domains_label = ", ".join(valid_domains) or "<none>"
                failures.append(
                    f"view {relative} has unknown Spec Basis {requirement_id} "
                    f"for owning domains: {domains_label}"
                )
    return failures


def validate_domain_links(wiki_root: Path) -> list[str]:
    specs_root = wiki_root / "specs"
    failures: list[str] = []
    typed_roots = (specs_root / "domains", specs_root / "policies")
    for typed_root in typed_roots:
        paths = sorted(typed_root.rglob("*.md")) if typed_root.is_dir() else []
        for path in paths:
            relative = path.relative_to(wiki_root).as_posix()
            text = path.read_text(encoding="utf-8")
            if re.search(r"(?m)^## Related Domains\s*$", text):
                failures.append(
                    f"{relative}: legacy Related Domains section requires migration"
                )
            for heading in ("Required Context", "See Also"):
                if not re.search(rf"(?m)^## {re.escape(heading)}\s*$", text):
                    failures.append(f"{relative}: missing {heading} section")
                    continue
                body = _section_body(text, heading)
                for link in re.findall(
                    r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)", body
                ):
                    target = (path.parent / link).resolve()
                    try:
                        target.relative_to(specs_root.resolve())
                    except ValueError:
                        failures.append(
                            f"{relative}: {heading} link escapes specs: {link}"
                        )
                        continue
                    if not target.is_file():
                        failures.append(
                            f"{relative}: broken {heading} link: {link}"
                        )
    return failures


def validate_generated_wiki(repo_root: Path, wiki_root: Path) -> list[str]:
    repo_root = repo_root.resolve()
    wiki_root = wiki_root.resolve()
    failures = validate_core_files(wiki_root)
    coverage, coverage_failures = load_coverage(wiki_root)
    failures.extend(coverage_failures)
    failures.extend(validate_domain_pairs(wiki_root))
    failures.extend(validate_domain_links(wiki_root))
    failures.extend(validate_spec_item_headings(wiki_root))
    if not coverage_failures:
        source_revision = coverage.get("source_revision")
        if not isinstance(source_revision, str) or not source_revision.strip():
            failures.append("coverage source_revision is required")
        else:
            failures.extend(
                validate_source_revision(repo_root, wiki_root, source_revision)
            )
        failures.extend(validate_features(repo_root, wiki_root, coverage))
        failures.extend(validate_concerns(repo_root, wiki_root, coverage))
        failures.extend(validate_policy_views(wiki_root, coverage.get("concerns")))
    return list(dict.fromkeys(failures))


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Validate a generated Code-Wiki against its source checkout."
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--wiki-root", required=True, type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    failures = validate_generated_wiki(args.repo_root, args.wiki_root)
    dirty_paths = uncommitted_paths_outside_wiki(args.repo_root, args.wiki_root)
    if dirty_paths:
        print(
            "WARN source_revision covers committed history only; "
            "uncommitted paths require separate inspection: "
            + ", ".join(dirty_paths),
            file=sys.stderr,
        )
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print("Generated Code-Wiki contract passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_generated_wiki import validate_generated_wiki  # noqa: E402


class GeneratedWikiValidatorTest(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def make_candidate(self, base: Path) -> tuple[Path, Path, dict]:
        repo = base / "repo"
        wiki = repo / "wiki"
        self.write(repo / "src" / "core.py", "def run():\n    return 'ok'\n")
        self.write(
            repo / "tests" / "test_core.py",
            "def test_core():\n    assert True\n",
        )
        self.write(wiki / "index.md", "# Router\n")
        self.write(wiki / "specs" / "index.md", "# Spec Registry\n")
        self.write(wiki / "specs" / "project.md", "# Project Intent\n")
        self.write(wiki / "reference" / "index.md", "# Reference Registry\n")
        self.write(wiki / "reference" / "overview.md", "# Overview\n")
        self.write(
            wiki / "specs" / "domains" / "core.md",
            """# Core

## Requirements

### Requirement: `CORE-R001`

The core operation returns a successful result.

## Required Context

## See Also
""",
        )
        self.write(
            wiki / "reference" / "domains" / "core.md",
            """# Core

## Feature Coverage

### Feature: `core-operation`

- Spec Basis: `CORE-R001`
""",
        )
        coverage = {
            "source_revision": "abc123",
            "features": [
                {
                    "feature_id": "core-operation",
                    "classification": "important",
                    "primary_domain": "core",
                    "spec_basis": ["CORE-R001"],
                    "surfaces": {
                        "ui": [],
                        "api": ["src/core.py"],
                        "jobs": [],
                        "providers": [],
                        "schemas": [],
                        "tests": ["tests/test_core.py"],
                    },
                }
            ],
            "concerns": {
                "security": {
                    "applicability": "not_applicable",
                    "owning_domains": [],
                    "policy_path": None,
                    "view_path": None,
                    "reason": (
                        "The inspected local-only core has no identity, secret, "
                        "network, or privileged boundary."
                    ),
                    "evidence": ["src/core.py"],
                },
                "architecture": {
                    "applicability": "not_applicable",
                    "owning_domains": [],
                    "policy_path": None,
                    "view_path": None,
                    "reason": (
                        "No approved cross-domain architecture policy or useful "
                        "aggregate view exists."
                    ),
                    "evidence": ["src/core.py"],
                },
            },
        }
        self.write(
            wiki / "reference" / "coverage.json",
            json.dumps(coverage, indent=2) + "\n",
        )
        return repo, wiki, coverage

    def save_coverage(self, wiki: Path, coverage: dict) -> None:
        self.write(
            wiki / "reference" / "coverage.json",
            json.dumps(coverage, indent=2) + "\n",
        )

    def git(self, repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def test_no_security_candidate_passes_without_security_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))

            failures = validate_generated_wiki(repo, wiki)

        self.assertEqual(failures, [])

    def test_important_feature_must_exist_in_its_domain_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))
            reference = wiki / "reference" / "domains" / "core.md"
            reference.write_text(
                reference.read_text(encoding="utf-8").replace(
                    "### Feature: `core-operation`",
                    "### Feature: `different-operation`",
                ),
                encoding="utf-8",
            )

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "core-operation: missing Reference feature trace "
            "in reference/domains/core.md",
            failures,
        )

    def test_missing_reference_pair_reports_findings_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))
            (wiki / "reference" / "domains" / "core.md").unlink()

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "missing Reference domain reference/domains/core.md",
            failures,
        )

    def test_spec_basis_must_resolve_in_domain_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["features"][0]["spec_basis"] = ["MISSING-R999"]
            reference = wiki / "reference" / "domains" / "core.md"
            reference.write_text(
                reference.read_text(encoding="utf-8").replace(
                    "CORE-R001", "MISSING-R999"
                ),
                encoding="utf-8",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "core-operation: unknown Spec Basis MISSING-R999 in specs/domains/core.md",
            failures,
        )

    def test_reference_feature_trace_must_list_manifest_spec_basis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))
            reference = wiki / "reference" / "domains" / "core.md"
            reference.write_text(
                reference.read_text(encoding="utf-8").replace(
                    "`CORE-R001`", "`XCORE-R001Y`"
                ),
                encoding="utf-8",
            )

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "core-operation: Reference feature trace missing Spec Basis CORE-R001",
            failures,
        )

    def test_supporting_feature_spec_basis_must_resolve(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["features"].append(
                {
                    "feature_id": "core-helper",
                    "classification": "supporting",
                    "primary_domain": "core",
                    "spec_basis": ["MISSING-R999"],
                    "surfaces": {"api": ["src/core.py"]},
                }
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "core-helper: unknown Spec Basis MISSING-R999 in specs/domains/core.md",
            failures,
        )

    def test_not_applicable_security_requires_reason_and_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"]["reason"] = ""
            coverage["concerns"]["security"]["evidence"] = []
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn("security: not_applicable requires a reason", failures)
        self.assertIn("security: not_applicable requires evidence", failures)

    def test_empty_coverage_manifest_cannot_skip_required_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))
            self.save_coverage(wiki, {})

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn("coverage source_revision is required", failures)
        self.assertIn("coverage features must be an array", failures)
        self.assertIn("coverage concerns must be an object", failures)

    def test_malformed_manifest_values_do_not_crash(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["features"][0]["classification"] = []
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": [{"domain": "core"}],
                "policy_path": None,
                "view_path": None,
                "reason": "Malformed ownership should be reported.",
                "evidence": ["src/core.py"],
            }
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn("core-operation: invalid classification []", failures)
        self.assertIn(
            "security: owning domain entries must be non-empty strings",
            failures,
        )

    def test_excluded_feature_requires_an_evidence_backed_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            feature = coverage["features"][0]
            feature["classification"] = "excluded"
            feature["primary_domain"] = None
            feature.pop("spec_basis")
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "core-operation: excluded feature requires exclusion_reason",
            failures,
        )

    def test_not_applicable_security_forbids_policy_and_view(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"]["view_path"] = (
                "reference/views/security.md"
            )
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn("security: not_applicable forbids view_path", failures)

    def test_applicable_concern_paths_use_the_canonical_namespaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/security.md",
                "reason": "A source-derived security map is useful.",
                "evidence": ["src/core.py"],
            }
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "security: view_path must be reference/views/security.md",
            failures,
        )

    def test_committed_source_change_after_revision_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            self.git(repo, "init", "-q")
            self.git(repo, "config", "user.name", "Test Bot")
            self.git(repo, "config", "user.email", "test@example.com")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "source baseline")
            source_revision = self.git(repo, "rev-parse", "HEAD")

            coverage = deepcopy(coverage)
            coverage["source_revision"] = source_revision
            self.save_coverage(wiki, coverage)
            self.git(repo, "add", "wiki/reference/coverage.json")
            self.git(repo, "commit", "-q", "-m", "record Wiki coverage")
            self.assertEqual(validate_generated_wiki(repo, wiki), [])

            self.write(repo / "src" / "core.py", "def run():\n    return 'changed'\n")
            self.git(repo, "add", "src/core.py")
            self.git(repo, "commit", "-q", "-m", "change source")

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            f"coverage source changed since source_revision "
            f"{source_revision}: src/core.py",
            failures,
        )

    def test_cli_warns_that_uncommitted_source_is_outside_revision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            self.git(repo, "init", "-q")
            self.git(repo, "config", "user.name", "Test Bot")
            self.git(repo, "config", "user.email", "test@example.com")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "source baseline")
            source_revision = self.git(repo, "rev-parse", "HEAD")
            coverage = deepcopy(coverage)
            coverage["source_revision"] = source_revision
            self.save_coverage(wiki, coverage)
            self.git(repo, "add", "wiki/reference/coverage.json")
            self.git(repo, "commit", "-q", "-m", "record Wiki coverage")
            self.write(repo / "src" / "core.py", "def run():\n    return 'dirty'\n")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_generated_wiki.py"),
                    "--repo-root",
                    str(repo),
                    "--wiki-root",
                    str(wiki),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0)
        self.assertIn(
            "WARN source_revision covers committed history only; "
            "uncommitted paths require separate inspection: src/core.py",
            result.stderr,
        )

    def test_domain_owned_security_does_not_require_global_policy_or_view(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": None,
                "reason": "The core domain owns its authenticated operation.",
                "evidence": ["src/core.py"],
            }
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertEqual(failures, [])

    def test_source_derived_security_view_may_exist_without_global_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/views/security.md",
                "reason": "A cross-domain implementation map improves navigation.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n\nObserved only: current implementation map.\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertEqual(failures, [])

    def test_view_without_policy_may_use_owning_domain_spec_basis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/views/security.md",
                "reason": "A source-derived cross-domain view is useful.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n\n## Spec Basis\n\n- `CORE-R001`\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertEqual(failures, [])

    def test_view_without_policy_must_not_present_observation_as_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/views/security.md",
                "reason": "A source-derived cross-domain view is useful.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n\nAll requests must follow this global rule.\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "view security.md without policy requires Spec Basis, Observed only, "
            "or Confirm needed",
            failures,
        )

    def test_view_without_policy_rejects_unstructured_spec_basis_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/views/security.md",
                "reason": "A source-derived cross-domain view is useful.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n\nNo Spec Basis is available for this rule.\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "view security.md without policy requires Spec Basis, Observed only, "
            "or Confirm needed",
            failures,
        )

    def test_view_without_policy_rejects_unknown_spec_basis(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": None,
                "view_path": "reference/views/security.md",
                "reason": "A source-derived cross-domain view is useful.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n\n## Spec Basis\n\n- `MISSING-R999`\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "view security.md has unknown Spec Basis MISSING-R999 "
            "for owning domains: core",
            failures,
        )

    def test_global_security_policy_requires_paired_view(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": "specs/policies/security.md",
                "view_path": None,
                "reason": "An approved platform-wide security invariant exists.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "specs" / "policies" / "security.md",
                "# Security Policy\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn("policy security.md missing paired view", failures)
        self.assertIn("security: policy_path requires view_path", failures)

    def test_global_security_policy_and_paired_view_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": "specs/policies/security.md",
                "view_path": "reference/views/security.md",
                "reason": "An approved platform-wide security invariant exists.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "specs" / "policies" / "security.md",
                "# Security Policy\n\n## Required Context\n\n## See Also\n",
            )
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertEqual(failures, [])

    def test_policy_typed_links_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage = deepcopy(coverage)
            coverage["concerns"]["security"] = {
                "applicability": "applicable",
                "owning_domains": ["core"],
                "policy_path": "specs/policies/security.md",
                "view_path": "reference/views/security.md",
                "reason": "An approved cross-domain policy exists.",
                "evidence": ["src/core.py"],
            }
            self.write(
                wiki / "specs" / "policies" / "security.md",
                """# Security Policy

## Required Context

- [Missing](../domains/missing.md)

## See Also
""",
            )
            self.write(
                wiki / "reference" / "views" / "security.md",
                "# Security View\n",
            )
            self.save_coverage(wiki, coverage)

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "specs/policies/security.md: broken Required Context link: "
            "../domains/missing.md",
            failures,
        )

    def test_legacy_related_domains_requires_migration(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, _ = self.make_candidate(Path(temp_dir))
            spec = wiki / "specs" / "domains" / "core.md"
            spec.write_text(
                spec.read_text(encoding="utf-8") + "\n## Related Domains\n",
                encoding="utf-8",
            )

            failures = validate_generated_wiki(repo, wiki)

        self.assertIn(
            "specs/domains/core.md: legacy Related Domains section requires migration",
            failures,
        )

    def test_cli_reports_findings_and_returns_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo, wiki, coverage = self.make_candidate(Path(temp_dir))
            coverage["concerns"]["security"]["evidence"] = []
            self.save_coverage(wiki, coverage)

            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "validate_generated_wiki.py"),
                    "--repo-root",
                    str(repo),
                    "--wiki-root",
                    str(wiki),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "FAIL security: not_applicable requires evidence",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()

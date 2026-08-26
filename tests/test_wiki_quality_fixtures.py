#!/usr/bin/env python3

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_wiki_quality_fixtures.py"
FIXTURES = ROOT / "tests" / "fixtures" / "wiki-quality"
sys.path.insert(0, str(ROOT / "scripts"))

from validate_wiki_quality_fixtures import (  # noqa: E402
    load_manifest,
    validate_candidate,
)


class SemanticQualityFixtureTest(unittest.TestCase):
    def test_fixture_acceptance_criteria_use_compact_id_headings(self) -> None:
        for candidate_name in ("shallow", "complete", "authority-leakage"):
            specs_root = FIXTURES / candidate_name / "specs"
            for spec in sorted(specs_root.rglob("*.md")):
                text = spec.read_text(encoding="utf-8")
                match = re.search(
                    r"(?ms)^## Acceptance Criteria\s*$\n"
                    r"(.*?)(?=^## |\Z)",
                    text,
                )
                if not match:
                    continue
                section = match.group(1)
                self.assertNotRegex(
                    section,
                    r"(?m)^- ",
                    f"{spec} still uses bullet Acceptance Criteria",
                )
                self.assertRegex(
                    section,
                    r"(?m)^### `.+-AC\d{3}`\s*$",
                    f"{spec} lacks a compact Acceptance Criterion heading",
                )

    def test_shallow_fails_and_complete_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "Code-Wiki semantic quality fixtures passed.\n")
        self.assertEqual(result.stderr, "")

    def test_reference_only_durable_rules_are_rejected(self) -> None:
        manifest = load_manifest(FIXTURES / "feature-surfaces.json")

        failures = validate_candidate(FIXTURES / "authority-leakage", manifest)

        self.assertEqual(
            failures,
            [
                "provider-usage-accounting: missing approved Spec requirement "
                "MU-USAGE-R003",
                "security-enforcement-view: missing approved policy Spec security.md",
            ],
        )

    def test_spec_basis_ids_match_exactly(self) -> None:
        manifest = load_manifest(FIXTURES / "feature-surfaces.json")
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "complete"
            shutil.copytree(FIXTURES / "complete", candidate)
            reference = candidate / "reference" / "domains" / "model-usage.md"
            reference.write_text(
                reference.read_text(encoding="utf-8").replace(
                    "`MU-USAGE-R001`", "`XMU-USAGE-R001Y`"
                ),
                encoding="utf-8",
            )

            failures = validate_candidate(candidate, manifest)

        self.assertIn(
            "provider-usage-accounting: Reference missing Spec Basis MU-USAGE-R001",
            failures,
        )

    def test_fenced_trace_fields_are_not_semantic_evidence(self) -> None:
        manifest = load_manifest(FIXTURES / "feature-surfaces.json")
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "complete"
            shutil.copytree(FIXTURES / "complete", candidate)
            reference = candidate / "reference" / "domains" / "model-usage.md"
            text = reference.read_text(encoding="utf-8")
            reference.write_text(
                text.replace(
                    "- Spec Basis: `MU-USAGE-R001`",
                    "```markdown\n- Spec Basis: `MU-USAGE-R001`",
                    1,
                ).rstrip()
                + "\n```\n",
                encoding="utf-8",
            )

            failures = validate_candidate(candidate, manifest)

        self.assertIn(
            "provider-usage-accounting: missing Surface",
            failures,
        )

    def test_compact_requirement_heading_preserves_behavioral_evidence(self) -> None:
        manifest = load_manifest(FIXTURES / "feature-surfaces.json")
        with tempfile.TemporaryDirectory() as temp_dir:
            candidate = Path(temp_dir) / "complete"
            shutil.copytree(FIXTURES / "complete", candidate)
            spec = candidate / "specs" / "domains" / "model-usage.md"
            spec.write_text(
                spec.read_text(encoding="utf-8").replace(
                    "## Requirements",
                    "## Domain Invariants",
                    1,
                ),
                encoding="utf-8",
            )

            failures = validate_candidate(candidate, manifest)

        self.assertNotIn(
            "provider-usage-accounting: missing approved Spec requirement "
            "MU-USAGE-R001",
            failures,
        )


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3

from pathlib import Path
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
                "MU-USAGE-003",
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
                    "`MU-USAGE-001`", "`XMU-USAGE-001Y`"
                ),
                encoding="utf-8",
            )

            failures = validate_candidate(candidate, manifest)

        self.assertIn(
            "provider-usage-accounting: Reference missing Spec Basis MU-USAGE-001",
            failures,
        )


if __name__ == "__main__":
    unittest.main()

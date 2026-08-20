#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_wiki_quality_fixtures.py"
FIXTURES = ROOT / "tests" / "fixtures" / "wiki-quality"
sys.path.insert(0, str(ROOT / "scripts"))

from validate_wiki_quality_fixtures import load_manifest, validate_candidate  # noqa: E402


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

    def test_reference_only_calculation_rule_is_rejected(self) -> None:
        manifest = load_manifest(FIXTURES / "feature-surfaces.json")

        failures = validate_candidate(FIXTURES / "authority-leakage", manifest)

        self.assertEqual(
            failures,
            [
                "provider-usage-accounting: missing approved Spec requirement "
                "MU-USAGE-003"
            ],
        )


if __name__ == "__main__":
    unittest.main()

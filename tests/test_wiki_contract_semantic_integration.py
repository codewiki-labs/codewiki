#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WikiContractSemanticIntegrationTest(unittest.TestCase):
    def test_main_validator_rejects_broken_complete_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            checkout = Path(temp_dir) / "code-wiki"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            usage_reference = (
                checkout
                / "tests"
                / "fixtures"
                / "wiki-quality"
                / "complete"
                / "reference"
                / "domains"
                / "model-usage.md"
            )
            text = usage_reference.read_text(encoding="utf-8")
            usage_reference.write_text(
                text.replace("computeCostBreakdown", "cost calculator", 1),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, "scripts/validate_wiki_contract.py"],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "semantic quality fixture: complete fixture: provider-usage-accounting: "
            "missing evidence computeCostBreakdown",
            result.stdout + result.stderr,
        )


if __name__ == "__main__":
    unittest.main()

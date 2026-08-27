from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "codewiki-cli"


class CodeWikiCliTest(unittest.TestCase):
    def run_cli(
        self,
        *args: str,
        include_repo: bool = True,
        cwd: Path = ROOT,
    ) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, "-m", "codewiki"]
        if include_repo:
            command.extend(("--repo-root", str(FIXTURE)))
        command.extend(args)
        env = os.environ.copy()
        existing_pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = (
            f"{ROOT}{os.pathsep}{existing_pythonpath}"
            if existing_pythonpath
            else str(ROOT)
        )
        return subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_json_command(self, *args: str) -> dict:
        result = self.run_cli(*args, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)

    def test_every_command_emits_parseable_json(self) -> None:
        commands = (
            ("index",),
            ("show", "QUIZ-R001"),
            ("show", "QUIZ-AC001"),
            ("trace", "QUIZ-R001"),
            ("trace", "src/services/quiz.py"),
            ("trace", "symbol:QuizService.create_quiz"),
            ("read", "specs/domains/quiz.md"),
            ("search", "quiz validation"),
            ("context", "QUIZ-R001"),
            ("status",),
            ("validate", "QUIZ-R001"),
            ("doctor",),
        )
        for command in commands:
            with self.subTest(command=command):
                payload = self.assert_json_command(*command)
                self.assertIsInstance(payload, dict)
                self.assertNotIn("error", payload)

    def test_index_and_show_json_are_structured_core_results(self) -> None:
        index = self.assert_json_command("index")
        shown = self.assert_json_command("show", "QUIZ-R001")

        self.assertIn("specs/domains/quiz.md", {item["path"] for item in index["specs"]})
        self.assertEqual(shown["entity"]["id"], "QUIZ-R001")
        self.assertIn("QUIZ-AC001", {item["id"] for item in shown["related_entities"]})

    def test_reverse_trace_json_contains_specs(self) -> None:
        payload = self.assert_json_command("trace", "src/services/quiz.py")

        self.assertIn("QUIZ-R001", {entity["id"] for entity in payload["entities"]})
        self.assertEqual(payload["target"]["kind"], "path")

    def test_read_human_output_is_exact_raw_markdown(self) -> None:
        expected = (FIXTURE / "wiki/specs/domains/quiz.md").read_text(encoding="utf-8")

        result = self.run_cli("read", "specs/domains/quiz.md")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected)
        self.assertEqual(result.stderr, "")

    def test_search_exact_id_ranks_first_and_empty_results_succeed(self) -> None:
        exact = self.assert_json_command("search", "QUIZ-R001")
        no_match = self.assert_json_command("search", "no-such-lexeme-xyz")
        empty_query = self.assert_json_command("search", "")

        self.assertEqual(exact["results"][0]["id"], "QUIZ-R001")
        self.assertEqual(exact["results"][0]["match_type"], "id_exact")
        self.assertEqual(no_match["results"], [])
        self.assertEqual(empty_query["results"], [])

    def test_json_error_is_single_stdout_value_with_exit_code(self) -> None:
        result = self.run_cli("show", "QUIZ-R999", "--json")

        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["error"]["code"], "target_not_found")

    def test_human_error_uses_stderr(self) -> None:
        result = self.run_cli("show", "QUIZ-R999")

        self.assertEqual(result.returncode, 3)
        self.assertEqual(result.stdout, "")
        self.assertIn("ERROR [target_not_found]", result.stderr)

    def test_invalid_limit_has_actionable_usage_error(self) -> None:
        result = self.run_cli("search", "quiz", "--limit", "0")

        self.assertEqual(result.returncode, 2)
        self.assertIn("limit must be at least 1", result.stderr)
        self.assertNotIn("_positive_int", result.stderr)

    def test_repository_discovery_works_from_fixture_child(self) -> None:
        result = self.run_cli(
            "show",
            "QUIZ-R001",
            "--json",
            include_repo=False,
            cwd=FIXTURE / "src/services",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["entity"]["id"], "QUIZ-R001")

    def test_help_version_and_console_script_metadata(self) -> None:
        help_result = self.run_cli("--help", include_repo=False)
        version_result = self.run_cli("--version", include_repo=False)
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

        self.assertEqual(help_result.returncode, 0)
        for command in (
            "index",
            "show",
            "trace",
            "read",
            "search",
            "context",
            "status",
            "validate",
            "doctor",
            "serve",
        ):
            self.assertIn(command, help_result.stdout)
        self.assertEqual(version_result.stdout.strip(), "codewiki 0.3.0")
        self.assertIn(
            'codewiki = "codewiki.cli:main"',
            pyproject,
        )
        self.assertIn('"codewiki.web" = ["static/*.html"', pyproject)

    def test_serve_defaults_and_options_dispatch_to_web_server(self) -> None:
        from unittest.mock import patch

        from codewiki import cli

        defaults = cli.build_parser().parse_args(["serve"])
        self.assertEqual(defaults.host, "127.0.0.1")
        self.assertEqual(defaults.port, 8000)
        self.assertFalse(defaults.open_browser)

        with patch("codewiki.server.serve") as run_server:
            exit_code = cli.main(
                [
                    "--repo-root",
                    str(FIXTURE),
                    "serve",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8080",
                    "--open",
                ]
            )

        self.assertEqual(exit_code, 0)
        run_server.assert_called_once()
        self.assertEqual(run_server.call_args.kwargs["host"], "0.0.0.0")
        self.assertEqual(run_server.call_args.kwargs["port"], 8080)
        self.assertTrue(run_server.call_args.kwargs["open_browser"])

        invalid = self.run_cli("serve", "--port", "0")
        self.assertEqual(invalid.returncode, 2)
        self.assertIn("port must be between 1 and 65535", invalid.stderr)

    def test_existing_generated_validator_cli_still_works(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_generated_wiki.py"),
                "--help",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--repo-root", result.stdout)
        self.assertIn("--wiki-root", result.stdout)


if __name__ == "__main__":
    unittest.main()

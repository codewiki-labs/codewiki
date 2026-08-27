from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from codewiki import CodeWiki, InvalidPathError, TargetNotFoundError
from codewiki.core import markdown
from codewiki.core.search import LexicalSearch, SearchCandidate


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "codewiki-cli"


class CodeWikiCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.core = CodeWiki.open(repo_root=FIXTURE)

    def test_index_uses_spec_registry_descriptions(self) -> None:
        result = self.core.get_index()

        quiz = next(spec for spec in result.specs if spec.path == "specs/domains/quiz.md")
        self.assertEqual(quiz.title, "Quiz")
        self.assertEqual(
            quiz.description,
            "Quiz creation, validation, and submission behavior.",
        )

    def test_index_includes_entity_and_traceability_summary(self) -> None:
        result = self.core.get_index()
        quiz = next(spec for spec in result.specs if spec.path == "specs/domains/quiz.md")

        self.assertEqual(result.entity_count, 4)
        self.assertEqual(result.requirement_count, 2)
        self.assertEqual(result.acceptance_criterion_count, 2)
        self.assertEqual(result.traced_entity_count, 4)
        self.assertEqual(result.untraced_entity_ids, ())
        self.assertEqual(quiz.requirement_ids, ("QUIZ-R001", "QUIZ-R002"))
        self.assertEqual(
            quiz.acceptance_criterion_ids,
            ("QUIZ-AC001", "QUIZ-AC002"),
        )
        all_entity_ids = (*quiz.requirement_ids, *quiz.acceptance_criterion_ids)
        self.assertEqual(set(quiz.traced_entity_ids), set(all_entity_ids))
        self.assertEqual(len(all_entity_ids), 4)
        self.assertEqual(quiz.untraced_entity_ids, ())

    def test_show_requirement_and_acceptance_criterion(self) -> None:
        requirement = self.core.get_spec("QUIZ-R001")
        criterion = self.core.get_spec("QUIZ-AC001")

        self.assertEqual(requirement.entity.entity_type, "requirement")
        self.assertIn("Quiz validation", requirement.entity.body)
        self.assertIn("QUIZ-AC001", {item.id for item in requirement.related_entities})
        self.assertIn(
            "QuizService.create_quiz",
            {reference.value for reference in requirement.code_references},
        )
        self.assertEqual(criterion.entity.entity_type, "acceptance_criterion")
        self.assertIn("QUIZ-R001", {item.id for item in criterion.related_entities})
        self.assertEqual(
            criterion.feature_links[0].relation,
            "acceptance_of_spec_requirements",
        )

    def test_spec_to_code_trace(self) -> None:
        result = self.core.trace("QUIZ-R001")

        self.assertEqual(result.target.kind, "spec_id")
        self.assertEqual(result.entities[0].id, "QUIZ-R001")
        self.assertIn(
            "src/services/quiz.py",
            {reference.value for reference in result.code_references},
        )
        self.assertIn(
            "QuizService.create_quiz",
            {reference.value for reference in result.code_references},
        )

    def test_code_to_spec_trace(self) -> None:
        result = self.core.trace("src/services/quiz.py")

        self.assertEqual(result.target.kind, "path")
        identifiers = {entity.id for entity in result.entities}
        self.assertTrue({"QUIZ-R001", "QUIZ-R002"}.issubset(identifiers))
        self.assertIn("QUIZ-AC001", identifiers)

    def test_symbol_trace(self) -> None:
        result = self.core.trace("symbol:QuizService.create_quiz")

        self.assertEqual(result.target.kind, "symbol")
        self.assertEqual(result.feature_links[0].feature_id, "quiz-creation")
        self.assertIn("QUIZ-R001", {entity.id for entity in result.entities})

    def test_read_returns_raw_markdown_and_blocks_escape(self) -> None:
        expected = (FIXTURE / "wiki/specs/domains/quiz.md").read_text(encoding="utf-8")

        self.assertEqual(
            self.core.read_document("specs/domains/quiz.md").content,
            expected,
        )
        with self.assertRaises(InvalidPathError):
            self.core.read_document("../src/services/quiz.py")

    def test_search_exact_id_is_first(self) -> None:
        results = self.core.search("QUIZ-R001").results

        self.assertEqual(results[0].id, "QUIZ-R001")
        self.assertEqual(results[0].match_type, "id_exact")

    def test_search_phrase_and_all_token_ranking(self) -> None:
        phrase = self.core.search("quiz validation").results
        tokens = self.core.search("creation stored").results

        self.assertEqual(phrase[0].id, "QUIZ-R001")
        self.assertEqual(phrase[0].match_type, "phrase")
        self.assertEqual(tokens[0].id, "QUIZ-R001")
        self.assertEqual(tokens[0].match_type, "all_tokens")

    def test_search_korean_substring(self) -> None:
        results = self.core.search("제목과 질문").results

        self.assertEqual(results[0].id, "QUIZ-R002")
        self.assertIn("제목과 질문", results[0].snippet)

    def test_empty_search_is_a_successful_empty_result(self) -> None:
        result = self.core.search("")

        self.assertEqual(result.query, "")
        self.assertEqual(result.results, ())

    def test_search_snippet_handles_nfkc_length_changes(self) -> None:
        candidate = SearchCandidate(
            entity_type="document",
            id=None,
            path="example.md",
            title="Example",
            body="ﬁrst section explains ﬁnding normalized text",
        )

        result = LexicalSearch().search("finding", (candidate,))[0]

        self.assertIn("finding", result.snippet)

    def test_context_combines_specs_reference_and_source(self) -> None:
        result = self.core.get_context("QUIZ-R001")

        self.assertEqual(result.primary_entities[0].id, "QUIZ-R001")
        self.assertIn("QUIZ-AC001", {entity.id for entity in result.related_entities})
        self.assertIn(
            "reference/domains/quiz.md",
            {document.path for document in result.documents},
        )
        self.assertTrue(
            any(excerpt.symbol == "QuizService.create_quiz" for excerpt in result.source_excerpts)
        )

    def test_nonexistent_target_is_explicit(self) -> None:
        with self.assertRaises(TargetNotFoundError):
            self.core.get_spec("QUIZ-R999")
        with self.assertRaises(TargetNotFoundError):
            self.core.trace("src/services/missing.py")

    def test_validate_checks_files_and_symbols(self) -> None:
        result = self.core.validate("QUIZ-R001")

        self.assertTrue(result.valid)
        self.assertTrue(
            any(
                check.check == "code.file_exists" and check.status == "pass"
                for check in result.checks
            )
        )
        self.assertTrue(
            any(
                check.check == "code.symbol_exists" and check.status == "pass"
                for check in result.checks
            )
        )

    def test_validate_reports_stale_symbol(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            shutil.copytree(FIXTURE, repo)
            source = repo / "src/services/quiz.py"
            source.write_text(
                "class QuizService:\n"
                "    def delete_quiz(self) -> None:\n"
                "        pass\n\n"
                "def create_quiz() -> None:\n"
                "    pass\n",
                encoding="utf-8",
            )

            result = CodeWiki.open(repo_root=repo).validate("QUIZ-R001")

        self.assertFalse(result.valid)
        self.assertTrue(
            any(
                check.check == "code.symbol_exists" and check.status == "fail"
                for check in result.checks
            )
        )

    def test_nested_non_worktree_status_is_unknown(self) -> None:
        status = self.core.get_status()

        self.assertEqual(status.state, "unknown")
        self.assertEqual(status.changed_files, ())

    def test_status_distinguishes_wiki_only_dirty_and_committed_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            shutil.copytree(FIXTURE, repo)
            self.git(repo, "init", "-q", "-b", "main")
            self.git(repo, "config", "user.name", "Test Bot")
            self.git(repo, "config", "user.email", "test@example.com")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "fixture baseline")
            indexed = self.git(repo, "rev-parse", "HEAD")

            coverage_path = repo / "wiki/reference/coverage.json"
            coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
            coverage["source_revision"] = indexed
            coverage_path.write_text(json.dumps(coverage, indent=2) + "\n", encoding="utf-8")
            self.git(repo, "add", "wiki/reference/coverage.json")
            self.git(repo, "commit", "-q", "-m", "record indexed revision")

            synchronized = CodeWiki.open(repo_root=repo).get_status()
            self.assertEqual(synchronized.state, "synchronized")

            source = repo / "src/services/quiz.py"
            source.write_text(source.read_text(encoding="utf-8") + "\n# dirty\n", encoding="utf-8")
            dirty = CodeWiki.open(repo_root=repo).get_status()
            self.assertEqual(dirty.state, "working_tree_changed")
            self.assertIn("src/services/quiz.py", dirty.changed_files)
            self.assertIn("QUIZ-R001", dirty.potentially_affected_specs)

            self.git(repo, "add", "src/services/quiz.py")
            self.git(repo, "commit", "-q", "-m", "change source")
            stale = CodeWiki.open(repo_root=repo).get_status()
            self.assertEqual(stale.state, "stale")

    def test_validator_uses_shared_markdown_parser(self) -> None:
        import scripts.validate_generated_wiki as validator

        self.assertIs(validator.requirement_block, markdown.requirement_block)
        self.assertIs(validator.feature_block, markdown.feature_block)

    @staticmethod
    def git(repo: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()

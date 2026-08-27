from __future__ import annotations

import json
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from codewiki import CodeWiki
from codewiki.server import create_server


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "codewiki-cli"


class CodeWikiServerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.core = CodeWiki.open(repo_root=FIXTURE)
        self.server = create_server(self.core, host="127.0.0.1", port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
    ) -> tuple[int, object, bytes]:
        request = Request(
            self.base_url + path,
            data=b"" if method not in {"GET", "HEAD"} else None,
            method=method,
        )
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, response.headers, response.read()
        except HTTPError as error:
            with error:
                return error.code, error.headers, error.read()

    def json_request(self, path: str, *, method: str = "GET") -> tuple[int, object, dict]:
        status, headers, body = self.request(path, method=method)
        return status, headers, json.loads(body)

    def test_all_api_routes_return_structured_core_results(self) -> None:
        index_status, _, index = self.json_request("/api/index")
        self.assertEqual(index_status, 200)
        self.assertEqual(index, json.loads(json.dumps(self.core.get_index().to_dict())))
        self.assertEqual(index["entity_count"], 4)
        self.assertEqual(index["specs"][1]["requirement_ids"], ["QUIZ-R001", "QUIZ-R002"])

        endpoints = {
            "/api/spec?" + urlencode({"id": "QUIZ-R001"}): ("entity", "id", "QUIZ-R001"),
            "/api/trace?" + urlencode({"target": "src/services/quiz.py"}): ("target", "kind", "path"),
            "/api/context?" + urlencode({"target": "QUIZ-R001"}): ("target", "kind", "spec_id"),
            "/api/search?" + urlencode({"q": "quiz validation"}): ("results", 0, "QUIZ-R001"),
            "/api/status": (None, "state", "unknown"),
            "/api/validate?" + urlencode({"target": "QUIZ-R001"}): (None, "valid", True),
            "/api/read?" + urlencode({"path": "specs/domains/quiz.md"}): (None, "path", "specs/domains/quiz.md"),
            "/api/doctor": (None, "healthy", True),
        }
        for path, (container, key, expected) in endpoints.items():
            with self.subTest(path=path):
                status, headers, payload = self.json_request(path)
                self.assertEqual(status, 200)
                self.assertIn("application/json", headers["Content-Type"])
                value = payload if container is None else payload[container]
                if isinstance(key, int):
                    self.assertEqual(value[key]["id"], expected)
                else:
                    self.assertEqual(value[key], expected)

        _, _, context = self.json_request(
            "/api/context?" + urlencode({"target": "QUIZ-R001"})
        )
        self.assertEqual(context["source_excerpts"][0]["symbol"], "QuizService.create_quiz")
        self.assertGreaterEqual(context["source_excerpts"][0]["start_line"], 1)

    def test_core_errors_and_read_only_policy_map_to_http(self) -> None:
        status, _, payload = self.json_request(
            "/api/spec?" + urlencode({"id": "QUIZ-R999"})
        )
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "target_not_found")

        status, _, payload = self.json_request("/api/spec")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "invalid_query")

        status, _, payload = self.json_request("/api/search?q=quiz&limit=0")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "invalid_query")

        status, _, payload = self.json_request(
            "/api/read?" + urlencode({"path": "../README.md"})
        )
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "invalid_path")

        status, _, payload = self.json_request("/api/missing")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "route_not_found")

        status, headers, payload = self.json_request("/api/index", method="POST")
        self.assertEqual(status, 405)
        self.assertEqual(headers["Allow"], "GET, HEAD")
        self.assertEqual(payload["error"]["code"], "method_not_allowed")

    def test_bundled_viewer_assets_and_security_headers(self) -> None:
        expectations = {
            "/": ("text/html", b"Spec Traceability"),
            "/app.js": ("text/javascript", b"Local Trace Map"),
            "/styles.css": ("text/css", b".explorer-layout"),
            "/explorer": ("text/html", b"Spec Traceability"),
        }
        for path, (content_type, marker) in expectations.items():
            with self.subTest(path=path):
                status, headers, body = self.request(path)
                self.assertEqual(status, 200)
                self.assertIn(content_type, headers["Content-Type"])
                self.assertIn(marker, body)
                self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
                self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
                self.assertEqual(headers["X-Frame-Options"], "DENY")

        status, headers, body = self.request("/app.js", method="HEAD")
        self.assertEqual(status, 200)
        self.assertEqual(body, b"")
        self.assertGreater(int(headers["Content-Length"]), 100)

        status, _, payload = self.json_request("/missing.js")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"]["code"], "asset_not_found")

        status, _, payload = self.json_request("/%2e%2e/app.js")
        self.assertEqual(status, 400)
        self.assertEqual(payload["error"]["code"], "invalid_path")

    def test_ui_uses_core_apis_without_a_browser_markdown_parser(self) -> None:
        script = (ROOT / "codewiki/web/static/app.js").read_text(encoding="utf-8")
        html = (ROOT / "codewiki/web/static/index.html").read_text(encoding="utf-8")

        for endpoint in (
            "/api/index",
            "/api/spec",
            "/api/context",
            "/api/trace",
            "/api/search",
            "/api/status",
            "/api/validate",
        ):
            self.assertIn(endpoint, script)
        for forbidden in ("innerHTML", "outerHTML", "marked(", "markdown-it", "eval("):
            self.assertNotIn(forbidden, script)
        self.assertIn("Overview", html)
        self.assertIn("Explorer", html)
        self.assertIn("Changes", html)

    def test_viewer_design_uses_calm_blue_product_tokens_and_states(self) -> None:
        stylesheet = (ROOT / "codewiki/web/static/styles.css").read_text(
            encoding="utf-8"
        )
        html = (ROOT / "codewiki/web/static/index.html").read_text(encoding="utf-8")
        script = (ROOT / "codewiki/web/static/app.js").read_text(encoding="utf-8")

        for token in (
            "--primary: #3182f6",
            "--primary-hover: #2272eb",
            "--primary-weak: #e8f3ff",
            "--primary-weak-foreground: #1b64da",
            "--foreground: #191f28",
            "--body: #4e5968",
            "--muted: #8b95a1",
            "--secondary-text: #65717f",
            "--surface: #f2f4f6",
            "--border: #e5e8eb",
            "--danger-text: #c62828",
            'font-family: "Toss Product Sans", -apple-system',
        ):
            self.assertIn(token, stylesheet)
        for state in (
            ":focus-visible",
            ".button-primary:hover",
            ".button-primary:active",
            ".button:disabled",
            '.button[aria-busy="true"]',
            'input[aria-invalid="true"]',
        ):
            self.assertIn(state, stylesheet)
        for legacy in (
            "#176a5b",
            "#142d2d",
            "#f5f4ef",
            "Georgia",
            "Times New Roman",
            "--shadow-md",
        ):
            self.assertNotIn(legacy, stylesheet)
        self.assertNotIn("@font-face", stylesheet)
        self.assertIn("Search requirements, Specs, or code", html)
        self.assertIn("See what should happen—and where it happens.", script)


    def test_viewer_supports_english_and_korean_localization(self) -> None:
        import re

        script = (ROOT / "codewiki/web/static/app.js").read_text(encoding="utf-8")
        html = (ROOT / "codewiki/web/static/index.html").read_text(encoding="utf-8")
        stylesheet = (ROOT / "codewiki/web/static/styles.css").read_text(
            encoding="utf-8"
        )

        for marker in (
            'id="language-select"',
            'value="en"',
            'value="ko"',
            'data-i18n="Overview"',
            'data-i18n-placeholder="Search requirements, Specs, or code"',
        ):
            self.assertIn(marker, html)

        for behavior in (
            'const LOCALE_STORAGE_KEY = "codewiki.locale"',
            'navigator.languages?.[0] || navigator.language || "en"',
            "window.localStorage.getItem(LOCALE_STORAGE_KEY)",
            "window.localStorage.setItem(LOCALE_STORAGE_KEY, locale)",
            "document.documentElement.lang = state.locale",
            'languageSelect.addEventListener("change"',
            'document.title = t("{page} · CodeWiki"',
        ):
            self.assertIn(behavior, script)

        catalog_body, runtime_source = script.split(
            "const KO_MESSAGES = Object.freeze({", 1
        )[1].split("\n});", 1)
        raw_catalog_keys = re.findall(
            r'^  ("(?:[^"\\]|\\.)*"):', catalog_body, flags=re.MULTILINE
        )
        catalog_keys = [json.loads(value) for value in raw_catalog_keys]
        literal_call_keys = {
            json.loads(value)
            for value in re.findall(
                r'\bt\(("(?:[^"\\]|\\.)*")', runtime_source
            )
        }
        html_keys = set(
            re.findall(
                r'data-i18n(?:-aria-label|-placeholder|-content)?="([^"]+)"',
                html,
            )
        )
        self.assertGreaterEqual(len(catalog_keys), 200)
        self.assertEqual(len(catalog_keys), len(set(catalog_keys)))
        self.assertEqual((literal_call_keys | html_keys) - set(catalog_keys), set())
        self.assertNotIn("t(t(", script)

        for korean_copy in (
            "무엇이 일어나야 하고, 어디에서 구현되는지 확인하세요.",
            "스펙 탐색기",
            "로컬 추적 맵",
            "변경된 파일 → 영향받는 스펙",
            "Core 어휘 검색",
            "요청한 CodeWiki 화면을 불러오지 못했습니다.",
        ):
            self.assertIn(korean_copy, script)

        for source_content in (
            'node("h3", {}, spec.title)',
            'node("div", { class: "entity-body" }, entity.body ||',
            'node("code", {}, excerpt.text)',
        ):
            self.assertIn(source_content, script)

        for state in (
            ".language-picker:hover",
            ".language-picker:active",
            ".language-picker:focus-within",
            ".language-picker select:disabled",
            "grid-template-columns: auto auto minmax(280px, 1fr) auto auto",
            "grid-template-columns: 1fr auto auto",
        ):
            self.assertIn(state, stylesheet)


if __name__ == "__main__":
    unittest.main()

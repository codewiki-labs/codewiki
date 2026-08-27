"""Read-only HTTP adapter for the CodeWiki Core and bundled web viewer."""

from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
import ipaddress
import json
from pathlib import PurePosixPath
import sys
from typing import Any, TextIO
from urllib.parse import parse_qs, unquote, urlsplit
import webbrowser

from .core import CodeWiki
from .core.errors import (
    CodeWikiError,
    DocumentNotFoundError,
    InvalidDataError,
    InvalidPathError,
    InvalidQueryError,
    TargetNotFoundError,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
_STATIC_ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
}


class CodeWikiHTTPServer(ThreadingHTTPServer):
    """Threaded local server holding one preloaded, read-only Core instance."""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address: tuple[str, int], core: CodeWiki):
        self.core = core
        super().__init__(address, CodeWikiRequestHandler)


class CodeWikiRequestHandler(BaseHTTPRequestHandler):
    """Route HTTP reads to Core calls without implementing domain logic."""

    server: CodeWikiHTTPServer
    protocol_version = "HTTP/1.1"
    server_version = "CodeWikiHTTP/0.1"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._handle_request(send_body=True)

    def do_HEAD(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._handle_request(send_body=False)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._method_not_allowed()

    def do_PUT(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._method_not_allowed()

    def do_PATCH(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._method_not_allowed()

    def do_DELETE(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        self._method_not_allowed()

    def _handle_request(self, *, send_body: bool) -> None:
        parsed = urlsplit(self.path)
        path = unquote(parsed.path)
        if "\x00" in path or ".." in PurePosixPath(path).parts:
            self._send_error_payload(
                HTTPStatus.BAD_REQUEST,
                "invalid_path",
                "Request path must remain inside the CodeWiki viewer.",
                send_body=send_body,
            )
            return
        if path == "/api" or path.startswith("/api/"):
            self._handle_api(path, parse_qs(parsed.query, keep_blank_values=True), send_body)
            return
        self._handle_static(path, send_body)

    def _handle_api(
        self,
        path: str,
        query: dict[str, list[str]],
        send_body: bool,
    ) -> None:
        try:
            result: object
            if path == "/api/index":
                result = self.server.core.get_index()
            elif path == "/api/spec":
                result = self.server.core.get_spec(self._required(query, "id"))
            elif path == "/api/trace":
                result = self.server.core.trace(self._required(query, "target"))
            elif path == "/api/context":
                result = self.server.core.get_context(self._required(query, "target"))
            elif path == "/api/search":
                result = self.server.core.search(
                    self._first(query, "q", default=""),
                    limit=self._search_limit(query),
                )
            elif path == "/api/status":
                result = self.server.core.get_status()
            elif path == "/api/validate":
                target = self._first(query, "target", default="").strip() or None
                result = self.server.core.validate(target)
            elif path == "/api/read":
                result = self.server.core.read_document(self._required(query, "path"))
            elif path == "/api/doctor":
                result = self.server.core.doctor()
            else:
                self._send_error_payload(
                    HTTPStatus.NOT_FOUND,
                    "route_not_found",
                    f"HTTP API route not found: {path}",
                    send_body=send_body,
                )
                return

            to_dict = getattr(result, "to_dict", None)
            if not callable(to_dict):
                raise TypeError(f"Core result is not serializable: {type(result).__name__}")
            self._send_json(to_dict(), HTTPStatus.OK, send_body=send_body)
        except CodeWikiError as error:
            self._send_core_error(error, send_body=send_body)
        except Exception as error:  # Do not leak local paths or internals to the browser.
            self.log_error("Unhandled API error: %s", type(error).__name__)
            self._send_error_payload(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "internal_error",
                "The CodeWiki viewer could not complete this request.",
                send_body=send_body,
            )

    def _handle_static(self, path: str, send_body: bool) -> None:
        asset = _STATIC_ASSETS.get(path)
        if asset is None and not PurePosixPath(path).suffix:
            asset = _STATIC_ASSETS["/"]
        if asset is None:
            self._send_error_payload(
                HTTPStatus.NOT_FOUND,
                "asset_not_found",
                f"Viewer asset not found: {path}",
                send_body=send_body,
            )
            return
        name, content_type = asset
        try:
            content = (
                resources.files("codewiki.web")
                .joinpath("static", name)
                .read_bytes()
            )
        except (FileNotFoundError, ModuleNotFoundError, OSError):
            self._send_error_payload(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                "viewer_unavailable",
                "The bundled CodeWiki viewer assets are unavailable.",
                send_body=send_body,
            )
            return
        self._send_bytes(
            content,
            HTTPStatus.OK,
            content_type,
            cache_control="no-cache",
            send_body=send_body,
        )

    def _send_core_error(self, error: CodeWikiError, *, send_body: bool) -> None:
        if isinstance(error, (TargetNotFoundError, DocumentNotFoundError)):
            status = HTTPStatus.NOT_FOUND
        elif isinstance(error, (InvalidPathError, InvalidQueryError)):
            status = HTTPStatus.BAD_REQUEST
        elif isinstance(error, InvalidDataError):
            status = HTTPStatus.UNPROCESSABLE_ENTITY
        else:
            status = HTTPStatus.BAD_REQUEST
        self._send_json(
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "details": error.details,
                }
            },
            status,
            send_body=send_body,
        )

    def _method_not_allowed(self) -> None:
        self._send_error_payload(
            HTTPStatus.METHOD_NOT_ALLOWED,
            "method_not_allowed",
            "The CodeWiki viewer is read-only and accepts GET or HEAD requests only.",
            send_body=True,
            extra_headers={"Allow": "GET, HEAD"},
        )

    def _send_error_payload(
        self,
        status: HTTPStatus,
        code: str,
        message: str,
        *,
        send_body: bool,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self._send_json(
            {"error": {"code": code, "message": message, "details": {}}},
            status,
            send_body=send_body,
            extra_headers=extra_headers,
        )

    def _send_json(
        self,
        payload: dict[str, Any],
        status: HTTPStatus,
        *,
        send_body: bool,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        content = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self._send_bytes(
            content,
            status,
            "application/json; charset=utf-8",
            cache_control="no-store",
            send_body=send_body,
            extra_headers=extra_headers,
        )

    def _send_bytes(
        self,
        content: bytes,
        status: HTTPStatus,
        content_type: str,
        *,
        cache_control: str,
        send_body: bool,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", cache_control)
        self.send_header("Content-Security-Policy", "default-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'; object-src 'none'; img-src 'self' data:; script-src 'self'; style-src 'self'; connect-src 'self'")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        if send_body:
            self.wfile.write(content)

    @staticmethod
    def _first(
        query: dict[str, list[str]],
        name: str,
        *,
        default: str,
    ) -> str:
        values = query.get(name)
        return values[0] if values else default

    @classmethod
    def _required(cls, cls_query: dict[str, list[str]], name: str) -> str:
        value = cls._first(cls_query, name, default="").strip()
        if not value:
            raise InvalidQueryError(f"Query parameter '{name}' is required.")
        return value

    @classmethod
    def _search_limit(cls, query: dict[str, list[str]]) -> int:
        value = cls._first(query, "limit", default="20")
        try:
            limit = int(value)
        except ValueError as error:
            raise InvalidQueryError("Search limit must be an integer.") from error
        if not 1 <= limit <= 100:
            raise InvalidQueryError("Search limit must be between 1 and 100.")
        return limit


def create_server(
    core: CodeWiki,
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> CodeWikiHTTPServer:
    """Create a preloaded HTTP server; port 0 is accepted for tests/embedding."""
    if not host.strip():
        raise CodeWikiError("Server host must not be empty.")
    if not 0 <= port <= 65535:
        raise CodeWikiError("Server port must be between 0 and 65535.")
    core.get_index()
    try:
        return CodeWikiHTTPServer((host, port), core)
    except OSError as error:
        raise CodeWikiError(
            f"Could not start the CodeWiki server on {host}:{port}: {error}",
            details={"host": host, "port": port},
        ) from error


def serve(
    core: CodeWiki,
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    open_browser: bool = False,
    output: TextIO | None = None,
    error_output: TextIO | None = None,
) -> None:
    """Serve until interrupted, optionally opening the local browser."""
    stdout = sys.stdout if output is None else output
    stderr = sys.stderr if error_output is None else error_output
    with create_server(core, host=host, port=port) as server:
        actual_port = int(server.server_address[1])
        browser_host = _browser_host(host)
        url = f"http://{browser_host}:{actual_port}/"
        print(f"CodeWiki Web Viewer: {url}", file=stdout, flush=True)
        print("Press Ctrl-C to stop.", file=stdout, flush=True)
        if not _is_loopback(host):
            print(
                "WARNING: the viewer is available beyond localhost; it has no authentication.",
                file=stderr,
                flush=True,
            )
        if open_browser:
            try:
                webbrowser.open(url)
            except webbrowser.Error as error:
                print(f"WARNING: could not open a browser: {error}", file=stderr, flush=True)
        try:
            server.serve_forever(poll_interval=0.25)
        except KeyboardInterrupt:
            print("\nCodeWiki Web Viewer stopped.", file=stdout, flush=True)


def _browser_host(host: str) -> str:
    value = host.strip()
    if value in {"0.0.0.0", "::", "[::]"}:
        value = "127.0.0.1"
    if ":" in value and not value.startswith("["):
        return f"[{value}]"
    return value


def _is_loopback(host: str) -> bool:
    value = host.strip().strip("[]")
    if value.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(value).is_loopback
    except ValueError:
        return False


__all__ = [
    "CodeWikiHTTPServer",
    "CodeWikiRequestHandler",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "create_server",
    "serve",
]

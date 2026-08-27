"""Command-line adapter for CodeWiki Core."""

from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError, Namespace
import json
from pathlib import Path
import sys
from typing import Callable

from . import __version__
from .core import CodeWiki
from .core.errors import (
    CodeWikiError,
    DocumentNotFoundError,
    InvalidDataError,
    InvalidPathError,
    InvalidQueryError,
    NotInitializedError,
    TargetNotFoundError,
)
from .formatting import (
    render_context,
    render_doctor,
    render_index,
    render_search,
    render_spec,
    render_status,
    render_trace,
    render_validation,
)


HumanRenderer = Callable[[object], str]


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="codewiki",
        description="Query CodeWiki Specs and their implementation traces.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root (default: discover from the current directory).",
    )
    parser.add_argument(
        "--wiki-root",
        type=Path,
        help="Wiki root (default: <repo-root>/wiki).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"codewiki {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)

    index_parser = subparsers.add_parser("index", help="List managed Specs.")
    _add_json(index_parser)

    show_parser = subparsers.add_parser(
        "show", help="Show one Requirement or Acceptance Criterion."
    )
    show_parser.add_argument("id", help="Stable Spec entity ID, for example QUIZ-R001.")
    _add_json(show_parser)

    trace_parser = subparsers.add_parser(
        "trace", help="Trace a Spec ID, source path, symbol, or feature in both directions."
    )
    trace_parser.add_argument("target", help="Spec ID, repository path, or symbol:<name>.")
    _add_json(trace_parser)

    read_parser = subparsers.add_parser("read", help="Read a Wiki Markdown document.")
    read_parser.add_argument("path", help="Wiki-relative path, for example specs/domains/quiz.md.")
    _add_json(read_parser)

    search_parser = subparsers.add_parser(
        "search", help="Search CodeWiki entities with deterministic lexical ranking."
    )
    search_parser.add_argument("query", help="Text, ID, path, or symbol to search for.")
    search_parser.add_argument(
        "--limit", type=_positive_int, default=20, help="Maximum results (default: 20)."
    )
    _add_json(search_parser)

    context_parser = subparsers.add_parser(
        "context", help="Assemble task context for a Spec or source target."
    )
    context_parser.add_argument("target", help="Spec ID, repository path, or symbol:<name>.")
    _add_json(context_parser)

    status_parser = subparsers.add_parser(
        "status", help="Report source revision synchronization information."
    )
    _add_json(status_parser)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate recorded Spec-to-code traceability."
    )
    validate_parser.add_argument(
        "target", nargs="?", help="Optional Spec ID, repository path, symbol, or feature."
    )
    _add_json(validate_parser)

    doctor_parser = subparsers.add_parser(
        "doctor", help="Run initialization, parsing, trace, and repository diagnostics."
    )
    _add_json(doctor_parser)

    serve_parser = subparsers.add_parser(
        "serve", help="Explore Specs and implementation traces in a local web viewer."
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Interface to bind (default: 127.0.0.1).",
    )
    serve_parser.add_argument(
        "--port",
        type=_tcp_port,
        default=8000,
        help="TCP port to bind (default: 8000).",
    )
    serve_parser.add_argument(
        "--open",
        action="store_true",
        dest="open_browser",
        help="Open the viewer in the default browser after startup.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    json_mode = bool(getattr(args, "json", False))
    try:
        core = CodeWiki.open(repo_root=args.repo_root, wiki_root=args.wiki_root)
        result, renderer, exit_code = _dispatch(core, args)
        if args.command == "read" and not json_mode:
            sys.stdout.write(result.content)
        else:
            _emit(result, renderer, json_mode)
        return exit_code
    except BrokenPipeError:
        return 0
    except CodeWikiError as error:
        return _emit_error(error, json_mode)


def _dispatch(
    core: CodeWiki,
    args: Namespace,
) -> tuple[object, HumanRenderer, int]:
    if args.command == "index":
        return core.get_index(), render_index, 0
    if args.command == "show":
        return core.get_spec(args.id), render_spec, 0
    if args.command == "trace":
        return core.trace(args.target), render_trace, 0
    if args.command == "read":
        return core.read_document(args.path), lambda _: "", 0
    if args.command == "search":
        return core.search(args.query, limit=args.limit), render_search, 0
    if args.command == "context":
        return core.get_context(args.target), render_context, 0
    if args.command == "status":
        return core.get_status(), render_status, 0
    if args.command == "validate":
        result = core.validate(args.target)
        return result, render_validation, 0 if result.valid else 1
    if args.command == "doctor":
        result = core.doctor()
        return result, render_doctor, 0 if result.healthy else 1
    if args.command == "serve":
        from .server import serve

        serve(
            core,
            host=args.host,
            port=args.port,
            open_browser=args.open_browser,
        )
        return None, lambda _: "", 0
    raise AssertionError(f"Unhandled command: {args.command}")


def _emit(result: object, renderer: HumanRenderer, json_mode: bool) -> None:
    if json_mode:
        to_dict = getattr(result, "to_dict", None)
        payload = to_dict() if callable(to_dict) else result
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        sys.stdout.write(renderer(result))


def _emit_error(error: CodeWikiError, json_mode: bool) -> int:
    if json_mode:
        print(
            json.dumps(
                {
                    "error": {
                        "code": error.code,
                        "message": error.message,
                        "details": error.details,
                    }
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print(f"ERROR [{error.code}] {error.message}", file=sys.stderr)
    return _error_exit_code(error)


def _error_exit_code(error: CodeWikiError) -> int:
    if isinstance(error, (TargetNotFoundError, DocumentNotFoundError)):
        return 3
    if isinstance(error, InvalidDataError):
        return 4
    if isinstance(
        error,
        (NotInitializedError, InvalidPathError, InvalidQueryError),
    ):
        return 2
    return 1


def _add_json(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit one JSON value with no ANSI or human formatting.",
    )


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ArgumentTypeError("limit must be an integer") from error
    if parsed < 1:
        raise ArgumentTypeError("limit must be at least 1")
    return parsed


def _tcp_port(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise ArgumentTypeError("port must be an integer") from error
    if not 1 <= parsed <= 65535:
        raise ArgumentTypeError("port must be between 1 and 65535")
    return parsed


if __name__ == "__main__":
    raise SystemExit(main())

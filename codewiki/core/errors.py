"""Public exceptions raised by CodeWiki Core."""

from __future__ import annotations


class CodeWikiError(Exception):
    """Base class for expected, user-actionable Core failures."""

    code = "codewiki_error"

    def __init__(self, message: str, *, details: dict[str, object] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotInitializedError(CodeWikiError):
    code = "not_initialized"


class TargetNotFoundError(CodeWikiError):
    code = "target_not_found"


class DocumentNotFoundError(CodeWikiError):
    code = "document_not_found"


class InvalidPathError(CodeWikiError):
    code = "invalid_path"


class InvalidQueryError(CodeWikiError):
    code = "invalid_query"


class InvalidDataError(CodeWikiError):
    code = "invalid_data"

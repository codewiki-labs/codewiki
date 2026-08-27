"""CodeWiki: repository-local Spec and implementation navigation."""

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

__version__ = "0.3.0"

__all__ = [
    "CodeWiki",
    "CodeWikiError",
    "DocumentNotFoundError",
    "InvalidDataError",
    "InvalidPathError",
    "InvalidQueryError",
    "NotInitializedError",
    "TargetNotFoundError",
    "__version__",
]

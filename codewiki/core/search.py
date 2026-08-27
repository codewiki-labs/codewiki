"""Deterministic in-memory lexical search over CodeWiki entities."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata

from .models import SearchResult


TOKEN = re.compile(r"[\w.-]+", re.UNICODE)


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().strip()


def tokenize(value: str) -> tuple[str, ...]:
    return tuple(token for token in TOKEN.findall(normalize(value)) if token)


@dataclass(frozen=True, slots=True)
class SearchCandidate:
    entity_type: str
    id: str | None
    path: str
    title: str
    body: str
    exact_references: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class _Scored:
    score: int
    match_type: str
    matched_fields: tuple[str, ...]
    candidate: SearchCandidate


class LexicalSearch:
    """Small replaceable search component with stable tiered ranking."""

    def search(
        self,
        query: str,
        candidates: tuple[SearchCandidate, ...],
        *,
        limit: int = 20,
    ) -> tuple[SearchResult, ...]:
        normalized_query = normalize(query)
        query_tokens = tokenize(query)
        scored: list[_Scored] = []
        for candidate in candidates:
            result = self._score(normalized_query, query_tokens, candidate)
            if result is not None:
                scored.append(result)
        scored.sort(
            key=lambda value: (
                -value.score,
                normalize(value.candidate.id or value.candidate.path),
                normalize(value.candidate.path),
            )
        )
        output: list[SearchResult] = []
        for rank, value in enumerate(scored[: max(0, limit)], start=1):
            candidate = value.candidate
            output.append(
                SearchResult(
                    rank=rank,
                    score=value.score,
                    match_type=value.match_type,
                    entity_type=candidate.entity_type,
                    id=candidate.id,
                    path=candidate.path,
                    title=candidate.title,
                    snippet=self._snippet(candidate.body, normalized_query, query_tokens),
                    matched_fields=value.matched_fields,
                )
            )
        return tuple(output)

    def _score(
        self,
        query: str,
        query_tokens: tuple[str, ...],
        candidate: SearchCandidate,
    ) -> _Scored | None:
        entity_id = normalize(candidate.id or "")
        path = normalize(candidate.path)
        title = normalize(candidate.title)
        body = normalize(candidate.body)
        references = tuple(normalize(value) for value in candidate.exact_references)

        if entity_id and query == entity_id:
            return _Scored(100_000, "id_exact", ("id",), candidate)
        exact_fields: list[str] = []
        if query == path:
            exact_fields.append("path")
        if query in references:
            exact_fields.append("reference")
        if exact_fields:
            return _Scored(90_000, "path_or_symbol_exact", tuple(exact_fields), candidate)
        if query and query == title:
            return _Scored(80_000, "title_exact", ("title",), candidate)

        phrase_fields = tuple(
            name
            for name, value in (("title", title), ("body", body), ("path", path))
            if query and query in value
        )
        if phrase_fields:
            phrase_bonus = 2_000 if "title" in phrase_fields else 0
            return _Scored(70_000 + phrase_bonus, "phrase", phrase_fields, candidate)

        searchable = " ".join((entity_id, path, title, body, *references))
        matched = tuple(token for token in query_tokens if token in searchable)
        if query_tokens and len(matched) == len(query_tokens):
            return _Scored(
                50_000 + len(matched) * 100,
                "all_tokens",
                self._matched_fields(query_tokens, entity_id, path, title, body, references),
                candidate,
            )
        if matched:
            return _Scored(
                10_000 + len(matched) * 100,
                "some_tokens",
                self._matched_fields(matched, entity_id, path, title, body, references),
                candidate,
            )
        return None

    @staticmethod
    def _matched_fields(
        tokens: tuple[str, ...],
        entity_id: str,
        path: str,
        title: str,
        body: str,
        references: tuple[str, ...],
    ) -> tuple[str, ...]:
        fields: list[str] = []
        values = (
            ("id", entity_id),
            ("path", path),
            ("title", title),
            ("body", body),
            ("reference", " ".join(references)),
        )
        for name, value in values:
            if any(token in value for token in tokens):
                fields.append(name)
        return tuple(fields)

    @staticmethod
    def _snippet(body: str, query: str, tokens: tuple[str, ...]) -> str:
        compact = re.sub(r"\s+", " ", body).strip()
        if not compact:
            return ""
        normalized_body = normalize(compact)
        # Normalization can expand or compose characters (for example, ﬁ -> fi).
        # Use the normalized display only in that rare case so search offsets and
        # snippet slicing stay in the same coordinate system.
        display_body = compact if len(normalized_body) == len(compact) else normalized_body
        position = normalized_body.find(query) if query else -1
        if position < 0:
            positions = [normalized_body.find(token) for token in tokens]
            positions = [value for value in positions if value >= 0]
            position = min(positions) if positions else 0
        start = max(0, position - 60)
        end = min(len(display_body), position + max(len(query), 1) + 140)
        prefix = "…" if start else ""
        suffix = "…" if end < len(display_body) else ""
        return f"{prefix}{display_body[start:end].strip()}{suffix}"

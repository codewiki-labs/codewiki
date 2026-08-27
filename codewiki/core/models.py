"""Structured values returned by the CodeWiki Core API."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class StructuredValue:
    """Mixin for JSON-safe Core results."""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class Target(StructuredValue):
    raw: str
    kind: str
    value: str


@dataclass(frozen=True, slots=True)
class CodeReference(StructuredValue):
    kind: str
    value: str
    path: str | None = None
    feature_id: str | None = None
    source: str = "reference"
    exists: bool | None = None


@dataclass(frozen=True, slots=True)
class DocumentSummary(StructuredValue):
    path: str
    title: str
    description: str
    document_type: str
    requirement_ids: tuple[str, ...] = ()
    acceptance_criterion_ids: tuple[str, ...] = ()
    traced_entity_ids: tuple[str, ...] = ()
    untraced_entity_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SpecEntity(StructuredValue):
    id: str
    entity_type: str
    body: str
    spec_path: str
    spec_title: str
    section: str
    related_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class FeatureTrace(StructuredValue):
    id: str
    classification: str
    domain: str | None
    spec_basis: tuple[str, ...]
    reference_path: str | None
    body: str
    code_references: tuple[CodeReference, ...] = ()


@dataclass(frozen=True, slots=True)
class FeatureLink(StructuredValue):
    feature_id: str
    relation: str
    via_spec_ids: tuple[str, ...]
    reference_path: str | None
    code_references: tuple[CodeReference, ...] = ()


@dataclass(frozen=True, slots=True)
class IndexResult(StructuredValue):
    wiki_root: str
    specs: tuple[DocumentSummary, ...]
    entity_count: int = 0
    requirement_count: int = 0
    acceptance_criterion_count: int = 0
    traced_entity_count: int = 0
    untraced_entity_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SpecDetail(StructuredValue):
    entity: SpecEntity
    related_entities: tuple[SpecEntity, ...]
    feature_links: tuple[FeatureLink, ...]
    code_references: tuple[CodeReference, ...]


@dataclass(frozen=True, slots=True)
class ReadResult(StructuredValue):
    path: str
    content: str


@dataclass(frozen=True, slots=True)
class SearchResult(StructuredValue):
    rank: int
    score: int
    match_type: str
    entity_type: str
    id: str | None
    path: str
    title: str
    snippet: str
    matched_fields: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SearchResults(StructuredValue):
    query: str
    results: tuple[SearchResult, ...]


@dataclass(frozen=True, slots=True)
class TraceResult(StructuredValue):
    target: Target
    entities: tuple[SpecEntity, ...]
    feature_links: tuple[FeatureLink, ...]
    code_references: tuple[CodeReference, ...]


@dataclass(frozen=True, slots=True)
class ContextDocument(StructuredValue):
    path: str
    title: str
    relation: str
    content: str


@dataclass(frozen=True, slots=True)
class SourceExcerpt(StructuredValue):
    path: str
    symbol: str | None
    start_line: int
    end_line: int
    text: str


@dataclass(frozen=True, slots=True)
class ContextResult(StructuredValue):
    target: Target
    primary_entities: tuple[SpecEntity, ...]
    related_entities: tuple[SpecEntity, ...]
    documents: tuple[ContextDocument, ...]
    feature_links: tuple[FeatureLink, ...]
    code_references: tuple[CodeReference, ...]
    source_excerpts: tuple[SourceExcerpt, ...]


@dataclass(frozen=True, slots=True)
class RepositoryStatus(StructuredValue):
    state: str
    indexed_revision: str | None
    current_revision: str | None
    committed_changed_files: tuple[str, ...]
    uncommitted_changed_files: tuple[str, ...]
    changed_files: tuple[str, ...]
    potentially_affected_specs: tuple[str, ...]
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidationCheck(StructuredValue):
    check: str
    status: str
    message: str
    target: str | None = None
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ValidationResult(StructuredValue):
    valid: bool
    target: Target | None
    checks: tuple[ValidationCheck, ...]
    passed: int
    failed: int
    warnings: int


@dataclass(frozen=True, slots=True)
class DoctorCheck(StructuredValue):
    check: str
    status: str
    message: str


@dataclass(frozen=True, slots=True)
class DoctorResult(StructuredValue):
    healthy: bool
    repo_root: str
    wiki_root: str
    checks: tuple[DoctorCheck, ...]

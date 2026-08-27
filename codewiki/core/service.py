"""Repository-local CodeWiki Core service used by CLI and future adapters."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, replace
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable

from .errors import (
    DocumentNotFoundError,
    InvalidDataError,
    InvalidPathError,
    NotInitializedError,
    TargetNotFoundError,
)
from .markdown import (
    extract_code_tokens,
    first_paragraph,
    markdown_title,
    parse_features,
    parse_spec_entities,
    parse_typed_links,
    plain_text,
)
from .models import (
    CodeReference,
    ContextDocument,
    ContextResult,
    DoctorCheck,
    DoctorResult,
    DocumentSummary,
    FeatureLink,
    FeatureTrace,
    IndexResult,
    ReadResult,
    RepositoryStatus,
    SearchResults,
    SourceExcerpt,
    SpecDetail,
    SpecEntity,
    Target,
    TraceResult,
    ValidationCheck,
    ValidationResult,
)
from .repository import compare_revision
from .search import LexicalSearch, SearchCandidate, normalize


CORE_FILES = (
    "index.md",
    "specs/index.md",
    "specs/project.md",
    "reference/index.md",
    "reference/overview.md",
    "reference/coverage.json",
)
SPEC_ID_LIKE = re.compile(r".+-(?:R|AC)\d{3}$")


@dataclass(frozen=True, slots=True)
class _Document:
    path: str
    title: str
    content: str


class CodeWiki:
    """Read-only facade over a repository's Code-Wiki.

    The class owns parsing and structured result construction. Presentation and
    process exit behavior intentionally live outside this module.
    """

    def __init__(self, repo_root: Path, wiki_root: Path):
        self.repo_root = repo_root.resolve()
        self.wiki_root = wiki_root.resolve()
        if not (self.wiki_root / "index.md").is_file():
            raise NotInitializedError(
                f"Code-Wiki is not initialized at {self.wiki_root}; "
                "expected wiki/index.md.",
                details={"repo_root": str(self.repo_root), "wiki_root": str(self.wiki_root)},
            )
        self._loaded = False
        self._documents: dict[str, _Document] = {}
        self._entities: dict[str, SpecEntity] = {}
        self._features: tuple[FeatureTrace, ...] = ()
        self._coverage: dict[str, Any] = {}
        self._diagnostics: list[ValidationCheck] = []
        self._search = LexicalSearch()

    @classmethod
    def open(
        cls,
        *,
        start: str | Path | None = None,
        repo_root: str | Path | None = None,
        wiki_root: str | Path | None = None,
    ) -> CodeWiki:
        """Open an explicit Wiki or discover the nearest repository Wiki."""
        explicit_repo = Path(repo_root).expanduser().resolve() if repo_root else None
        if wiki_root:
            wiki = Path(wiki_root).expanduser()
            if not wiki.is_absolute() and explicit_repo is not None:
                wiki = explicit_repo / wiki
            wiki = wiki.resolve()
            repository = explicit_repo or wiki.parent
            return cls(repository, wiki)
        if explicit_repo is not None:
            return cls(explicit_repo, explicit_repo / "wiki")

        current = Path(start or Path.cwd()).expanduser().resolve()
        if current.is_file():
            current = current.parent
        for parent in (current, *current.parents):
            if parent.name == "wiki" and (parent / "index.md").is_file():
                return cls(parent.parent, parent)
            candidate = parent / "wiki"
            if (candidate / "index.md").is_file():
                return cls(parent, candidate)
        raise NotInitializedError(
            f"No Code-Wiki was found from {current}; expected wiki/index.md "
            "in this directory or an ancestor.",
            details={"start": str(current)},
        )

    def get_index(self) -> IndexResult:
        self._ensure_loaded()
        descriptions, order = self._index_descriptions()
        spec_paths = [
            path
            for path in self._documents
            if path.startswith("specs/")
            and path.endswith(".md")
            and path != "specs/index.md"
        ]
        ordered = [path for path in order if path in spec_paths]
        ordered.extend(sorted(set(spec_paths) - set(ordered)))

        entities_by_path: dict[str, list[SpecEntity]] = defaultdict(list)
        traced_ids: list[str] = []
        untraced_ids: list[str] = []
        for entity in self._entities.values():
            entities_by_path[entity.spec_path].append(entity)
            target = traced_ids if self._links_for_entity(entity) else untraced_ids
            target.append(entity.id)

        summaries: list[DocumentSummary] = []
        for path in ordered:
            document = self._documents[path]
            if path == "specs/project.md":
                document_type = "project_spec"
            elif path.startswith("specs/policies/"):
                document_type = "policy_spec"
            elif path.startswith("specs/domains/"):
                document_type = "domain_spec"
            else:
                document_type = "spec"
            description = descriptions.get(path) or first_paragraph(document.content)
            entities = entities_by_path[path]
            entity_ids = {entity.id for entity in entities}
            summaries.append(
                DocumentSummary(
                    path=path,
                    title=document.title,
                    description=description,
                    document_type=document_type,
                    requirement_ids=tuple(
                        entity.id
                        for entity in entities
                        if entity.entity_type == "requirement"
                    ),
                    acceptance_criterion_ids=tuple(
                        entity.id
                        for entity in entities
                        if entity.entity_type == "acceptance_criterion"
                    ),
                    traced_entity_ids=tuple(
                        entity_id for entity_id in traced_ids if entity_id in entity_ids
                    ),
                    untraced_entity_ids=tuple(
                        entity_id for entity_id in untraced_ids if entity_id in entity_ids
                    ),
                )
            )
        requirement_count = sum(len(spec.requirement_ids) for spec in summaries)
        acceptance_count = sum(
            len(spec.acceptance_criterion_ids) for spec in summaries
        )
        return IndexResult(
            wiki_root=str(self.wiki_root),
            specs=tuple(summaries),
            entity_count=requirement_count + acceptance_count,
            requirement_count=requirement_count,
            acceptance_criterion_count=acceptance_count,
            traced_entity_count=len(traced_ids),
            untraced_entity_ids=tuple(untraced_ids),
        )

    def get_spec(self, entity_id: str) -> SpecDetail:
        self._ensure_loaded()
        entity = self._entities.get(entity_id)
        if entity is None:
            raise TargetNotFoundError(
                f"Spec entity not found: {entity_id}",
                details={"target": entity_id, "expected": "Requirement or Acceptance Criterion ID"},
            )
        related = tuple(
            self._entities[value]
            for value in entity.related_ids
            if value in self._entities
        )
        links = self._links_for_entity(entity)
        return SpecDetail(
            entity=entity,
            related_entities=related,
            feature_links=links,
            code_references=self._references_from_links(links),
        )

    def read_document(self, path: str | Path) -> ReadResult:
        relative, candidate = self._resolve_wiki_document(path)
        if not candidate.is_file() or candidate.suffix.lower() != ".md":
            raise DocumentNotFoundError(
                f"Code-Wiki Markdown document not found: {relative}",
                details={"path": relative},
            )
        try:
            content = candidate.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise InvalidDataError(f"Could not read {relative}: {error}") from error
        return ReadResult(relative, content)

    def search(self, query: str, *, limit: int = 20) -> SearchResults:
        self._ensure_loaded()
        if not query or not query.strip():
            return SearchResults(query=query, results=())
        candidates: list[SearchCandidate] = []
        for entity in self._entities.values():
            links = self._links_for_entity(entity)
            references = self._references_from_links(links)
            candidates.append(
                SearchCandidate(
                    entity_type=entity.entity_type,
                    id=entity.id,
                    path=entity.spec_path,
                    title=entity.spec_title,
                    body=entity.body,
                    exact_references=tuple(
                        dict.fromkeys(
                            value
                            for reference in references
                            for value in (reference.value, reference.path)
                            if value
                        )
                    ),
                )
            )
        for document in self._documents.values():
            candidates.append(
                SearchCandidate(
                    entity_type="document",
                    id=None,
                    path=document.path,
                    title=document.title,
                    body=plain_text(document.content),
                )
            )
        results = self._search.search(query, tuple(candidates), limit=limit)
        return SearchResults(query=query, results=results)

    def trace(self, target: str | Target) -> TraceResult:
        self._ensure_loaded()
        parsed = target if isinstance(target, Target) else self.parse_target(target)
        if parsed.kind == "spec_id":
            entity = self._entities[parsed.value]
            entities = (entity,)
            links = self._links_for_entity(entity)
        else:
            features = self._features_for_target(parsed)
            links = tuple(self._feature_link(feature, "direct", feature.spec_basis) for feature in features)
            entity_ids: list[str] = []
            for feature in features:
                for entity_id in feature.spec_basis:
                    if entity_id in self._entities and entity_id not in entity_ids:
                        entity_ids.append(entity_id)
                    entity = self._entities.get(entity_id)
                    if entity is not None:
                        for related_id in entity.related_ids:
                            if related_id not in entity_ids:
                                entity_ids.append(related_id)
            entities = tuple(
                self._entities[entity_id]
                for entity_id in entity_ids
                if entity_id in self._entities
            )
        return TraceResult(
            target=parsed,
            entities=entities,
            feature_links=links,
            code_references=self._references_from_links(links),
        )

    def get_context(self, target: str | Target) -> ContextResult:
        self._ensure_loaded()
        trace = self.trace(target)
        if trace.target.kind == "spec_id":
            detail = self.get_spec(trace.target.value)
            primary = (detail.entity,)
            related = detail.related_entities
        else:
            basis_ids = {
                entity_id
                for link in trace.feature_links
                for entity_id in link.via_spec_ids
            }
            primary = tuple(entity for entity in trace.entities if entity.id in basis_ids)
            related = tuple(entity for entity in trace.entities if entity.id not in basis_ids)

        documents = self._context_documents(primary, related, trace.feature_links)
        excerpts = self._source_excerpts(trace.target, trace.feature_links)
        return ContextResult(
            target=trace.target,
            primary_entities=primary,
            related_entities=related,
            documents=documents,
            feature_links=trace.feature_links,
            code_references=trace.code_references,
            source_excerpts=excerpts,
        )

    def get_status(self) -> RepositoryStatus:
        self._ensure_loaded()
        source_revision = self._coverage.get("source_revision")
        indexed = source_revision if isinstance(source_revision, str) and source_revision.strip() else None
        comparison = compare_revision(self.repo_root, self.wiki_root, indexed)
        changed = tuple(
            sorted(set(comparison.committed_paths) | set(comparison.uncommitted_paths))
        )
        affected: list[str] = []
        changed_set = set(changed)
        for feature in self._features:
            feature_paths = {
                reference.value
                for reference in feature.code_references
                if reference.kind == "file"
            }
            if feature_paths & changed_set:
                for entity_id in feature.spec_basis:
                    if entity_id not in affected:
                        affected.append(entity_id)

        if not indexed or not comparison.available:
            state = "unknown"
        elif comparison.revision_valid is False or comparison.is_ancestor is not True:
            state = "unknown"
        elif comparison.committed_paths:
            state = "stale"
        elif comparison.uncommitted_paths:
            state = "working_tree_changed"
        else:
            state = "synchronized"
        return RepositoryStatus(
            state=state,
            indexed_revision=indexed,
            current_revision=comparison.current_revision,
            committed_changed_files=comparison.committed_paths,
            uncommitted_changed_files=comparison.uncommitted_paths,
            changed_files=changed,
            potentially_affected_specs=tuple(affected),
            warnings=comparison.warnings,
        )

    def validate(self, target: str | Target | None = None) -> ValidationResult:
        self._ensure_loaded()
        parsed = None if target is None else (target if isinstance(target, Target) else self.parse_target(target))
        checks: list[ValidationCheck] = []
        if parsed is None:
            checks.extend(self._diagnostics)
            checks.extend(self._core_structure_checks())
            features = self._features
        else:
            trace = self.trace(parsed)
            feature_ids = {link.feature_id for link in trace.feature_links}
            features = tuple(feature for feature in self._features if feature.id in feature_ids)
            if parsed.kind == "spec_id" and not features:
                checks.append(
                    ValidationCheck(
                        check="trace.present",
                        status="fail",
                        message=f"No implementation trace is linked to {parsed.value}.",
                        target=parsed.value,
                    )
                )
            elif parsed.kind != "spec_id" and not features:
                checks.append(
                    ValidationCheck(
                        check="trace.present",
                        status="warn",
                        message=f"No Spec trace is recorded for {parsed.value}.",
                        target=parsed.value,
                    )
                )

        checks.extend(self._feature_validation_checks(features))
        if parsed is None:
            status = self.get_status()
            if status.state == "stale":
                checks.append(
                    ValidationCheck(
                        check="source_revision.freshness",
                        status="fail",
                        message="Committed source files changed after the indexed revision.",
                        evidence=status.committed_changed_files,
                    )
                )
            elif status.state == "working_tree_changed":
                checks.append(
                    ValidationCheck(
                        check="source_revision.freshness",
                        status="warn",
                        message="Uncommitted source changes are outside the indexed revision.",
                        evidence=status.uncommitted_changed_files,
                    )
                )
            elif status.state == "synchronized":
                checks.append(
                    ValidationCheck(
                        check="source_revision.freshness",
                        status="pass",
                        message="Committed source matches the indexed revision scope.",
                    )
                )
            else:
                checks.append(
                    ValidationCheck(
                        check="source_revision.freshness",
                        status="warn",
                        message="Source freshness could not be determined.",
                        evidence=status.warnings,
                    )
                )

        checks = list(self._dedupe_checks(checks))
        failed = sum(check.status == "fail" for check in checks)
        warnings = sum(check.status == "warn" for check in checks)
        passed = sum(check.status == "pass" for check in checks)
        return ValidationResult(
            valid=failed == 0,
            target=parsed,
            checks=tuple(checks),
            passed=passed,
            failed=failed,
            warnings=warnings,
        )

    def doctor(self) -> DoctorResult:
        self._ensure_loaded()
        validation = self.validate()
        status = self.get_status()
        checks: list[DoctorCheck] = [
            DoctorCheck("wiki.initialized", "pass", f"Found {self.wiki_root / 'index.md'}"),
            DoctorCheck(
                "wiki.documents",
                "pass" if self._documents else "fail",
                f"Parsed {len(self._documents)} Markdown documents.",
            ),
            DoctorCheck(
                "wiki.spec_entities",
                "pass" if self._entities else "warn",
                f"Parsed {len(self._entities)} Requirement/Acceptance Criterion entities.",
            ),
            DoctorCheck(
                "wiki.validation",
                "pass" if validation.valid else "fail",
                f"Validation: {validation.passed} passed, {validation.failed} failed, "
                f"{validation.warnings} warnings.",
            ),
            DoctorCheck(
                "repository.status",
                "pass" if status.state == "synchronized" else "warn",
                f"Repository synchronization state: {status.state}.",
            ),
        ]
        return DoctorResult(
            healthy=not any(check.status == "fail" for check in checks),
            repo_root=str(self.repo_root),
            wiki_root=str(self.wiki_root),
            checks=tuple(checks),
        )

    def parse_target(self, raw_target: str) -> Target:
        self._ensure_loaded()
        raw = raw_target.strip()
        if not raw:
            raise TargetNotFoundError("Target must not be empty.")
        if raw in self._entities:
            return Target(raw_target, "spec_id", raw)
        if SPEC_ID_LIKE.fullmatch(raw):
            raise TargetNotFoundError(
                f"Spec entity not found: {raw}", details={"target": raw}
            )
        if raw.startswith("symbol:"):
            symbol = raw.removeprefix("symbol:").strip()
            if not symbol:
                raise TargetNotFoundError("symbol: target must include a symbol name.")
            target = Target(raw_target, "symbol", symbol)
            if not self._features_for_target(target):
                raise TargetNotFoundError(
                    f"No Code-Wiki trace references symbol: {symbol}",
                    details={"target": raw},
                )
            return target
        if any(feature.id == raw for feature in self._features):
            return Target(raw_target, "feature", raw)

        path_value = self._normalize_target_path(raw)
        target = Target(raw_target, "path", path_value)
        candidate = self.repo_root / Path(path_value)
        if not candidate.exists() and not self._features_for_target(target):
            raise TargetNotFoundError(
                f"Repository path not found and not referenced by Code-Wiki: {path_value}",
                details={"target": raw},
            )
        return target

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._load_documents()
        self._load_entities()
        self._load_coverage()
        self._load_features()
        self._loaded = True

    def _load_documents(self) -> None:
        for path in sorted(self.wiki_root.rglob("*.md")):
            if not path.is_file():
                continue
            try:
                resolved = path.resolve()
                relative = resolved.relative_to(self.wiki_root).as_posix()
            except ValueError:
                continue
            try:
                content = resolved.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as error:
                raise InvalidDataError(f"Could not read Wiki document {relative}: {error}") from error
            self._documents[relative] = _Document(
                relative,
                markdown_title(content, Path(relative).stem.replace("-", " ").title()),
                content,
            )

    def _load_entities(self) -> None:
        parsed_by_path: dict[str, list[SpecEntity]] = defaultdict(list)
        seen: dict[str, str] = {}
        for path, document in self._documents.items():
            if not path.startswith("specs/"):
                continue
            for parsed in parse_spec_entities(document.content):
                entity = SpecEntity(
                    id=parsed.id,
                    entity_type=parsed.entity_type,
                    body=parsed.body,
                    spec_path=path,
                    spec_title=document.title,
                    section=parsed.section,
                )
                if parsed.id in seen:
                    self._diagnostics.append(
                        ValidationCheck(
                            check="spec.id_unique",
                            status="fail",
                            message=f"Duplicate Spec entity ID {parsed.id}.",
                            target=parsed.id,
                            evidence=(seen[parsed.id], path),
                        )
                    )
                    continue
                seen[parsed.id] = path
                parsed_by_path[path].append(entity)
                self._entities[parsed.id] = entity

        for entities in parsed_by_path.values():
            requirements = tuple(
                entity.id for entity in entities if entity.entity_type == "requirement"
            )
            criteria = tuple(
                entity.id
                for entity in entities
                if entity.entity_type == "acceptance_criterion"
            )
            for entity in entities:
                related = criteria if entity.entity_type == "requirement" else requirements
                self._entities[entity.id] = replace(entity, related_ids=related)

    def _load_coverage(self) -> None:
        path = self.wiki_root / "reference" / "coverage.json"
        if not path.is_file():
            self._diagnostics.append(
                ValidationCheck(
                    check="coverage.exists",
                    status="fail",
                    message="Missing reference/coverage.json.",
                    target="reference/coverage.json",
                )
            )
            return
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            self._diagnostics.append(
                ValidationCheck(
                    check="coverage.parse",
                    status="fail",
                    message=f"reference/coverage.json is invalid: {error}",
                    target="reference/coverage.json",
                )
            )
            return
        if not isinstance(value, dict):
            self._diagnostics.append(
                ValidationCheck(
                    check="coverage.type",
                    status="fail",
                    message="reference/coverage.json must contain an object.",
                    target="reference/coverage.json",
                )
            )
            return
        self._coverage = value

    def _load_features(self) -> None:
        reference_features: dict[str, list[tuple[str, object]]] = defaultdict(list)
        for path, document in self._documents.items():
            if not path.startswith("reference/"):
                continue
            for parsed in parse_features(document.content):
                reference_features[parsed.id].append((path, parsed))

        output: list[FeatureTrace] = []
        covered_ids: set[str] = set()
        features = self._coverage.get("features")
        if features is not None and not isinstance(features, list):
            self._diagnostics.append(
                ValidationCheck(
                    check="coverage.features",
                    status="fail",
                    message="coverage features must be an array.",
                    target="reference/coverage.json",
                )
            )
            features = []
        for index, value in enumerate(features or []):
            if not isinstance(value, dict):
                self._diagnostics.append(
                    ValidationCheck(
                        check="coverage.feature",
                        status="fail",
                        message=f"coverage feature[{index}] must be an object.",
                    )
                )
                continue
            feature_id = value.get("feature_id")
            if not isinstance(feature_id, str) or not feature_id.strip():
                self._diagnostics.append(
                    ValidationCheck(
                        check="coverage.feature_id",
                        status="fail",
                        message=f"coverage feature[{index}] has no feature_id.",
                    )
                )
                continue
            if feature_id in covered_ids:
                self._diagnostics.append(
                    ValidationCheck(
                        check="coverage.feature_id_unique",
                        status="fail",
                        message=f"Duplicate coverage feature_id {feature_id}.",
                        target=feature_id,
                    )
                )
                continue
            covered_ids.add(feature_id)
            domain_value = value.get("primary_domain")
            domain = domain_value if isinstance(domain_value, str) and domain_value else None
            classification_value = value.get("classification")
            classification = (
                classification_value
                if isinstance(classification_value, str)
                else "unknown"
            )
            basis_value = value.get("spec_basis")
            basis = tuple(
                item
                for item in (basis_value if isinstance(basis_value, list) else [])
                if isinstance(item, str) and item
            )
            expected_reference = f"reference/domains/{domain}.md" if domain else None
            candidates = reference_features.get(feature_id, [])
            selected = next(
                (item for item in candidates if item[0] == expected_reference),
                candidates[0] if candidates else None,
            )
            reference_path = selected[0] if selected else expected_reference
            parsed_feature = selected[1] if selected else None
            body = getattr(parsed_feature, "body", "")
            reference_basis = tuple(getattr(parsed_feature, "spec_basis", ()))
            if basis and reference_basis and not set(basis).issubset(reference_basis):
                self._diagnostics.append(
                    ValidationCheck(
                        check="trace.spec_basis",
                        status="fail",
                        message=f"Reference trace {feature_id} does not include every coverage Spec Basis ID.",
                        target=feature_id,
                        evidence=tuple(sorted(set(basis) - set(reference_basis))),
                    )
                )
            references = self._coverage_references(feature_id, value.get("surfaces"))
            references.extend(self._reference_tokens(feature_id, body))
            output.append(
                FeatureTrace(
                    id=feature_id,
                    classification=classification,
                    domain=domain,
                    spec_basis=basis or reference_basis,
                    reference_path=reference_path if reference_path in self._documents else None,
                    body=body,
                    code_references=self._dedupe_references(references),
                )
            )

        for feature_id, candidates in reference_features.items():
            if feature_id in covered_ids:
                continue
            for reference_path, parsed_feature in candidates:
                domain = self._domain_from_reference_path(reference_path)
                output.append(
                    FeatureTrace(
                        id=feature_id,
                        classification="observed",
                        domain=domain,
                        spec_basis=tuple(getattr(parsed_feature, "spec_basis", ())),
                        reference_path=reference_path,
                        body=getattr(parsed_feature, "body", ""),
                        code_references=self._dedupe_references(
                            self._reference_tokens(
                                feature_id, getattr(parsed_feature, "body", "")
                            )
                        ),
                    )
                )
        self._features = tuple(output)

    def _coverage_references(
        self,
        feature_id: str,
        surfaces: object,
    ) -> list[CodeReference]:
        references: list[CodeReference] = []
        if not isinstance(surfaces, dict):
            return references
        for values in surfaces.values():
            if not isinstance(values, list):
                continue
            for value in values:
                if not isinstance(value, str) or not value.strip():
                    continue
                normalized, exists = self._normalize_reference_path(value)
                references.append(
                    CodeReference(
                        kind="file",
                        value=normalized,
                        path=normalized,
                        feature_id=feature_id,
                        source="coverage",
                        exists=exists,
                    )
                )
        return references

    def _reference_tokens(self, feature_id: str, body: str) -> list[CodeReference]:
        references: list[CodeReference] = []
        for token in extract_code_tokens(body):
            if token.kind == "file":
                value, exists = self._normalize_reference_path(token.value)
                path = value
            elif token.path:
                path, _ = self._normalize_reference_path(token.path)
                value, exists = token.value, self._symbol_exists(token.value, (path,))
            else:
                value, path, exists = token.value, None, None
            references.append(
                CodeReference(
                    kind=token.kind,
                    value=value,
                    path=path,
                    feature_id=feature_id,
                    source="reference",
                    exists=exists,
                )
            )
        return references

    def _links_for_entity(self, entity: SpecEntity) -> tuple[FeatureLink, ...]:
        links: list[FeatureLink] = []
        for feature in self._features:
            if entity.id in feature.spec_basis:
                links.append(self._feature_link(feature, "direct", (entity.id,)))
                continue
            if entity.entity_type == "acceptance_criterion":
                via = tuple(value for value in entity.related_ids if value in feature.spec_basis)
                if via:
                    links.append(
                        self._feature_link(
                            feature,
                            "acceptance_of_spec_requirements",
                            via,
                        )
                    )
        return tuple(links)

    @staticmethod
    def _feature_link(
        feature: FeatureTrace,
        relation: str,
        via_spec_ids: Iterable[str],
    ) -> FeatureLink:
        return FeatureLink(
            feature_id=feature.id,
            relation=relation,
            via_spec_ids=tuple(via_spec_ids),
            reference_path=feature.reference_path,
            code_references=feature.code_references,
        )

    def _features_for_target(self, target: Target) -> tuple[FeatureTrace, ...]:
        if target.kind == "feature":
            return tuple(feature for feature in self._features if feature.id == target.value)
        if target.kind == "path":
            return tuple(
                feature
                for feature in self._features
                if any(
                    reference.kind == "file"
                    and (reference.value == target.value or reference.path == target.value)
                    for reference in feature.code_references
                )
            )
        if target.kind == "symbol":
            expected = normalize(target.value)
            return tuple(
                feature
                for feature in self._features
                if any(
                    reference.kind == "symbol" and normalize(reference.value) == expected
                    for reference in feature.code_references
                )
            )
        return ()

    @staticmethod
    def _references_from_links(links: Iterable[FeatureLink]) -> tuple[CodeReference, ...]:
        return CodeWiki._dedupe_references(
            reference for link in links for reference in link.code_references
        )

    @staticmethod
    def _dedupe_references(references: Iterable[CodeReference]) -> tuple[CodeReference, ...]:
        output: list[CodeReference] = []
        seen: set[tuple[str, str, str | None, str | None]] = set()
        for reference in references:
            key = (
                reference.kind,
                reference.value,
                reference.path,
                reference.feature_id,
            )
            if key not in seen:
                seen.add(key)
                output.append(reference)
        return tuple(output)

    def _context_documents(
        self,
        primary: tuple[SpecEntity, ...],
        related: tuple[SpecEntity, ...],
        links: tuple[FeatureLink, ...],
    ) -> tuple[ContextDocument, ...]:
        documents: list[ContextDocument] = []
        seen: set[str] = set()

        def add(path: str, relation: str) -> None:
            document = self._documents.get(path)
            if document is None or path in seen:
                return
            seen.add(path)
            documents.append(
                ContextDocument(path, document.title, relation, document.content)
            )

        for entity in primary:
            add(entity.spec_path, "spec")
        for entity in related:
            add(entity.spec_path, "related_spec")

        queue = [entity.spec_path for entity in (*primary, *related)]
        visited_links: set[str] = set()
        see_also: list[str] = []
        while queue:
            source_path = queue.pop(0)
            if source_path in visited_links:
                continue
            visited_links.add(source_path)
            document = self._documents.get(source_path)
            if document is None:
                continue
            for link in parse_typed_links(document.content):
                resolved = self._resolve_document_link(source_path, link.path)
                if resolved is None:
                    continue
                if link.relation == "required_context":
                    add(resolved, "required_context")
                    queue.append(resolved)
                else:
                    see_also.append(resolved)
        for path in see_also:
            add(path, "see_also")
        for link in links:
            if link.reference_path:
                add(link.reference_path, "reference")
        return tuple(documents)

    def _source_excerpts(
        self,
        target: Target,
        links: tuple[FeatureLink, ...],
    ) -> tuple[SourceExcerpt, ...]:
        excerpts: list[SourceExcerpt] = []
        seen: set[tuple[str, str | None]] = set()
        for link in links:
            files = tuple(
                reference.value
                for reference in link.code_references
                if reference.kind == "file" and reference.exists
            )
            symbols = tuple(
                reference
                for reference in link.code_references
                if reference.kind == "symbol"
            )
            for symbol in symbols:
                candidates = (symbol.path,) if symbol.path else files
                for path in candidates:
                    if not path or (path, symbol.value) in seen:
                        continue
                    excerpt = self._excerpt_for_symbol(path, symbol.value)
                    if excerpt is not None:
                        seen.add((path, symbol.value))
                        excerpts.append(excerpt)
                        break
        if target.kind == "path" and not any(excerpt.path == target.value for excerpt in excerpts):
            excerpt = self._head_excerpt(target.value)
            if excerpt is not None:
                excerpts.insert(0, excerpt)
        if not excerpts:
            files = [
                reference.value
                for link in links
                for reference in link.code_references
                if reference.kind == "file" and reference.exists
            ]
            for path in dict.fromkeys(files):
                excerpt = self._head_excerpt(path)
                if excerpt is not None:
                    excerpts.append(excerpt)
                if len(excerpts) >= 3:
                    break
        return tuple(excerpts[:12])

    def _excerpt_for_symbol(self, path: str, symbol: str) -> SourceExcerpt | None:
        lines = self._source_lines(path)
        if lines is None:
            return None
        segments = [segment for segment in symbol.split(".") if segment]
        for index, line in enumerate(lines):
            if all(re.search(rf"\b{re.escape(segment)}\b", line) for segment in segments[-1:]):
                start = max(0, index - 3)
                end = min(len(lines), index + 4)
                return SourceExcerpt(
                    path=path,
                    symbol=symbol,
                    start_line=start + 1,
                    end_line=end,
                    text="".join(lines[start:end]),
                )
        return None

    def _head_excerpt(self, path: str) -> SourceExcerpt | None:
        lines = self._source_lines(path)
        if lines is None:
            return None
        end = min(len(lines), 30)
        return SourceExcerpt(path, None, 1, end, "".join(lines[:end]))

    def _source_lines(self, path: str) -> list[str] | None:
        candidate = (self.repo_root / Path(path)).resolve()
        try:
            candidate.relative_to(self.repo_root)
        except ValueError:
            return None
        if not candidate.is_file():
            return None
        try:
            return candidate.read_text(encoding="utf-8").splitlines(keepends=True)
        except (OSError, UnicodeError):
            return None

    def _feature_validation_checks(
        self,
        features: tuple[FeatureTrace, ...],
    ) -> list[ValidationCheck]:
        checks: list[ValidationCheck] = []
        for feature in features:
            for entity_id in feature.spec_basis:
                if entity_id in self._entities:
                    checks.append(
                        ValidationCheck(
                            check="trace.spec_basis",
                            status="pass",
                            message=f"Spec Basis {entity_id} resolves.",
                            target=feature.id,
                            evidence=(entity_id,),
                        )
                    )
                else:
                    checks.append(
                        ValidationCheck(
                            check="trace.spec_basis",
                            status="fail",
                            message=f"Spec Basis {entity_id} does not resolve.",
                            target=feature.id,
                            evidence=(entity_id,),
                        )
                    )
            if feature.classification == "important" and not feature.reference_path:
                checks.append(
                    ValidationCheck(
                        check="trace.reference",
                        status="fail",
                        message=f"Important feature {feature.id} has no Reference feature trace.",
                        target=feature.id,
                    )
                )
            elif feature.reference_path:
                checks.append(
                    ValidationCheck(
                        check="trace.reference",
                        status="pass",
                        message=f"Reference trace exists for {feature.id}.",
                        target=feature.id,
                        evidence=(feature.reference_path,),
                    )
                )

            files = tuple(
                reference
                for reference in feature.code_references
                if reference.kind == "file"
            )
            for reference in files:
                checks.append(
                    ValidationCheck(
                        check="code.file_exists",
                        status="pass" if reference.exists else "fail",
                        message=(
                            f"Referenced file exists: {reference.value}"
                            if reference.exists
                            else f"Referenced file does not exist: {reference.value}"
                        ),
                        target=feature.id,
                        evidence=(reference.value,),
                    )
                )

            file_paths = tuple(
                dict.fromkeys(reference.value for reference in files if reference.exists)
            )
            for reference in feature.code_references:
                if reference.kind != "symbol":
                    continue
                candidates = (reference.path,) if reference.path else file_paths
                candidates = tuple(path for path in candidates if path)
                if not candidates:
                    checks.append(
                        ValidationCheck(
                            check="code.symbol_exists",
                            status="warn",
                            message=f"Could not select a file for symbol {reference.value}.",
                            target=feature.id,
                            evidence=(reference.value,),
                        )
                    )
                    continue
                found = self._symbol_exists(reference.value, candidates)
                checks.append(
                    ValidationCheck(
                        check="code.symbol_exists",
                        status="pass" if found else "fail",
                        message=(
                            f"Referenced symbol exists lexically: {reference.value}"
                            if found
                            else f"Referenced symbol was not found lexically: {reference.value}"
                        ),
                        target=feature.id,
                        evidence=(reference.value, *candidates),
                    )
                )
        return checks

    def _core_structure_checks(self) -> list[ValidationCheck]:
        checks: list[ValidationCheck] = []
        for relative in CORE_FILES:
            exists = (self.wiki_root / relative).is_file()
            checks.append(
                ValidationCheck(
                    check="wiki.core_file",
                    status="pass" if exists else "fail",
                    message=(
                        f"Required Wiki file exists: {relative}"
                        if exists
                        else f"Missing required Wiki file: {relative}"
                    ),
                    target=relative,
                )
            )
        specs = self._relative_markdown_files(self.wiki_root / "specs" / "domains")
        references = self._relative_markdown_files(
            self.wiki_root / "reference" / "domains"
        )
        for relative in sorted(specs - references):
            checks.append(
                ValidationCheck(
                    check="wiki.domain_pair",
                    status="fail",
                    message=f"Missing Reference domain for specs/domains/{relative}.",
                    target=relative,
                )
            )
        for relative in sorted(references - specs):
            checks.append(
                ValidationCheck(
                    check="wiki.domain_pair",
                    status="fail",
                    message=f"Missing Spec domain for reference/domains/{relative}.",
                    target=relative,
                )
            )
        if specs == references:
            checks.append(
                ValidationCheck(
                    check="wiki.domain_pair",
                    status="pass",
                    message=f"All {len(specs)} domain Spec/Reference pairs match.",
                )
            )
        return checks

    def _symbol_exists(self, symbol: str, paths: Iterable[str]) -> bool:
        segments = tuple(segment for segment in symbol.split(".") if segment)
        if not segments:
            return False
        patterns = tuple(
            re.compile(rf"\b{re.escape(segment)}\b") for segment in segments
        )
        dotted = re.compile(
            r"\s*\.\s*".join(
                rf"\b{re.escape(segment)}\b" for segment in segments
            )
        )
        for path in paths:
            lines = self._source_lines(path)
            if lines is None:
                continue
            text = "".join(lines)
            if len(segments) == 1:
                if patterns[0].search(text):
                    return True
                continue
            if dotted.search(text) or any(
                all(pattern.search(line) for pattern in patterns) for line in lines
            ):
                return True

            # For declarations such as Class.method, require the remaining
            # identifiers inside the first identifier's indented lexical scope.
            # This stays language-neutral while rejecting an unrelated top-level
            # function elsewhere in the same file.
            for index, line in enumerate(lines):
                if not patterns[0].search(line):
                    continue
                parent_indent = len(line) - len(line.lstrip(" \t"))
                scope: list[str] = []
                for scoped_line in lines[index + 1 : index + 201]:
                    if not scoped_line.strip():
                        scope.append(scoped_line)
                        continue
                    indent = len(scoped_line) - len(scoped_line.lstrip(" \t"))
                    if indent <= parent_indent:
                        break
                    scope.append(scoped_line)
                scope_text = "".join(scope)
                if scope_text and all(
                    pattern.search(scope_text) for pattern in patterns[1:]
                ):
                    return True
        return False

    def _index_descriptions(self) -> tuple[dict[str, str], list[str]]:
        descriptions: dict[str, str] = {}
        order: list[str] = []
        for index_path in ("index.md", "specs/index.md"):
            document = self._documents.get(index_path)
            if document is None:
                continue
            for line in document.content.splitlines():
                for match in re.finditer(r"\[([^]]+)\]\(([^)#]+\.md)(?:#[^)]+)?\)", line):
                    resolved = self._resolve_document_link(index_path, match.group(2))
                    if resolved is None:
                        continue
                    if resolved not in order:
                        order.append(resolved)
                    tail = line[match.end() :].strip()
                    tail = tail.strip(" |:-—–\t")
                    if tail:
                        descriptions.setdefault(resolved, plain_text(tail))
        return descriptions, order

    def _resolve_document_link(self, source_path: str, target: str) -> str | None:
        combined = PurePosixPath(source_path).parent / PurePosixPath(target)
        parts: list[str] = []
        for part in combined.parts:
            if part in {"", "."}:
                continue
            if part == "..":
                if not parts:
                    return None
                parts.pop()
            else:
                parts.append(part)
        relative = PurePosixPath(*parts).as_posix()
        return relative if relative in self._documents else None

    def _resolve_wiki_document(self, path: str | Path) -> tuple[str, Path]:
        supplied = Path(path).expanduser()
        if supplied.is_absolute():
            candidate = supplied.resolve()
        else:
            parts = supplied.parts
            if parts and parts[0] == "wiki":
                supplied = Path(*parts[1:])
            candidate = (self.wiki_root / supplied).resolve()
        try:
            relative = candidate.relative_to(self.wiki_root).as_posix()
        except ValueError as error:
            raise InvalidPathError(
                f"Wiki path escapes {self.wiki_root}: {path}",
                details={"path": str(path)},
            ) from error
        return relative, candidate

    def _normalize_target_path(self, value: str) -> str:
        supplied = Path(value).expanduser()
        candidate = supplied.resolve() if supplied.is_absolute() else (self.repo_root / supplied).resolve()
        try:
            return candidate.relative_to(self.repo_root).as_posix()
        except ValueError as error:
            raise InvalidPathError(
                f"Repository path escapes {self.repo_root}: {value}",
                details={"path": value},
            ) from error

    def _normalize_reference_path(self, value: str) -> tuple[str, bool]:
        supplied = Path(value)
        if supplied.is_absolute():
            return value, False
        candidate = (self.repo_root / supplied).resolve()
        try:
            relative = candidate.relative_to(self.repo_root).as_posix()
        except ValueError:
            return value, False
        return relative, candidate.is_file()

    @staticmethod
    def _domain_from_reference_path(path: str) -> str | None:
        prefix = "reference/domains/"
        if not path.startswith(prefix) or not path.endswith(".md"):
            return None
        return path[len(prefix) : -3]

    @staticmethod
    def _relative_markdown_files(root: Path) -> set[str]:
        if not root.is_dir():
            return set()
        return {
            path.relative_to(root).as_posix()
            for path in root.rglob("*.md")
            if path.is_file()
        }

    @staticmethod
    def _dedupe_checks(checks: Iterable[ValidationCheck]) -> tuple[ValidationCheck, ...]:
        output: list[ValidationCheck] = []
        seen: set[tuple[object, ...]] = set()
        for check in checks:
            key = (
                check.check,
                check.status,
                check.message,
                check.target,
                check.evidence,
            )
            if key not in seen:
                seen.add(key)
                output.append(check)
        return tuple(output)

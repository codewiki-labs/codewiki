"""Plain-text renderers for CodeWiki CLI results."""

from __future__ import annotations

from .core.models import (
    ContextResult,
    DoctorResult,
    IndexResult,
    RepositoryStatus,
    SearchResults,
    SpecDetail,
    TraceResult,
    ValidationResult,
)


ENTITY_LABELS = {
    "requirement": "Requirement",
    "acceptance_criterion": "Acceptance Criterion",
    "document": "Document",
}


def render_index(result: IndexResult) -> str:
    lines = ["Specs", ""]
    if not result.specs:
        lines.append("No Specs found.")
    for spec in result.specs:
        lines.append(spec.path)
        lines.append(f"  {spec.description or spec.title}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_spec(result: SpecDetail) -> str:
    entity = result.entity
    label = ENTITY_LABELS.get(entity.entity_type, entity.entity_type)
    lines = [
        entity.id,
        f"Type: {label}",
        f"Spec: {entity.spec_path} ({entity.spec_title})",
        f"Section: {entity.section}",
        "",
        entity.body or "(empty body)",
    ]
    lines.extend(("", "Related"))
    if result.related_entities:
        lines.extend(
            f"- {item.id} · {ENTITY_LABELS.get(item.entity_type, item.entity_type)}"
            for item in result.related_entities
        )
    else:
        lines.append("- None")
    lines.extend(("", "Implementation"))
    if result.feature_links:
        for link in result.feature_links:
            via = ", ".join(link.via_spec_ids)
            lines.append(f"- {link.feature_id} [{link.relation}] via {via}")
    else:
        lines.append("- No trace recorded")
    lines.extend(_render_code_references(result.code_references))
    return "\n".join(lines).rstrip() + "\n"


def render_trace(result: TraceResult) -> str:
    lines = [
        "CodeWiki Trace",
        "",
        f"Target: {result.target.raw}",
        f"Kind: {result.target.kind}",
        "",
        "Spec Entities",
    ]
    if result.entities:
        for entity in result.entities:
            label = ENTITY_LABELS.get(entity.entity_type, entity.entity_type)
            lines.append(f"- {entity.id} · {label} · {entity.spec_path}")
    else:
        lines.append("- None")
    lines.extend(("", "Feature Links"))
    if result.feature_links:
        for link in result.feature_links:
            via = ", ".join(link.via_spec_ids) or "observed-only"
            reference = f" · {link.reference_path}" if link.reference_path else ""
            lines.append(f"- {link.feature_id} [{link.relation}] via {via}{reference}")
    else:
        lines.append("- None")
    lines.extend(("", "Code"))
    references = _render_code_references(result.code_references)
    lines.extend(references or ["- None"])
    return "\n".join(lines).rstrip() + "\n"


def render_search(result: SearchResults) -> str:
    if not result.results:
        return f'No results for "{result.query}".\n'
    lines: list[str] = []
    for item in result.results:
        label = ENTITY_LABELS.get(item.entity_type, item.entity_type.replace("_", " ").title())
        identifier = item.id or item.title
        lines.append(f"{item.rank}. {identifier}")
        lines.append(f"   {label} · {item.path}")
        if item.snippet:
            lines.append(f"   {item.snippet}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_context(result: ContextResult) -> str:
    lines = [
        "CodeWiki Context",
        "",
        f"Target: {result.target.raw}",
        f"Kind: {result.target.kind}",
        "",
        "Primary Spec Entities",
    ]
    if result.primary_entities:
        for entity in result.primary_entities:
            lines.extend(_render_entity_body(entity.id, entity.entity_type, entity.body))
    else:
        lines.append("- None")
    lines.extend(("", "Related Spec Entities"))
    if result.related_entities:
        for entity in result.related_entities:
            lines.extend(_render_entity_body(entity.id, entity.entity_type, entity.body))
    else:
        lines.append("- None")
    lines.extend(("", "Implementation"))
    references = _render_code_references(result.code_references)
    lines.extend(references or ["- None"])

    lines.extend(("", "Wiki Documents"))
    if result.documents:
        for document in result.documents:
            lines.extend(
                (
                    "",
                    f"--- {document.path} [{document.relation}] ---",
                    document.content.rstrip(),
                )
            )
    else:
        lines.append("- None")

    lines.extend(("", "Source Excerpts"))
    if result.source_excerpts:
        for excerpt in result.source_excerpts:
            symbol = f" · {excerpt.symbol}" if excerpt.symbol else ""
            lines.extend(
                (
                    "",
                    f"--- {excerpt.path}:{excerpt.start_line}-{excerpt.end_line}{symbol} ---",
                    excerpt.text.rstrip(),
                )
            )
    else:
        lines.append("- None")
    return "\n".join(lines).rstrip() + "\n"


def render_status(result: RepositoryStatus) -> str:
    lines = [
        "CodeWiki Status",
        "",
        f"State: {result.state}",
        f"Indexed commit: {_short_revision(result.indexed_revision)}",
        f"Current commit: {_short_revision(result.current_revision)}",
        "",
        f"Changed files: {len(result.changed_files)}",
        f"Potentially affected specs: {len(result.potentially_affected_specs)}",
    ]
    if result.changed_files:
        lines.extend(("", "Changed Files"))
        lines.extend(f"- {path}" for path in result.changed_files)
    if result.potentially_affected_specs:
        lines.extend(("", "Potentially Affected Specs"))
        lines.extend(f"- {entity_id}" for entity_id in result.potentially_affected_specs)
    if result.warnings:
        lines.extend(("", "Warnings"))
        lines.extend(f"- {warning}" for warning in result.warnings)
    return "\n".join(lines).rstrip() + "\n"


def render_validation(result: ValidationResult) -> str:
    target = result.target.raw if result.target else "all traces"
    lines = [
        "CodeWiki Validation",
        "",
        f"Target: {target}",
        f"Result: {'valid' if result.valid else 'invalid'}",
        f"Checks: {result.passed} passed, {result.failed} failed, {result.warnings} warnings",
        "",
    ]
    if not result.checks:
        lines.append("No verifiable trace checks were found.")
    for check in result.checks:
        lines.append(f"[{check.status.upper()}] {check.message}")
        if check.evidence:
            lines.append(f"  Evidence: {', '.join(check.evidence)}")
    return "\n".join(lines).rstrip() + "\n"


def render_doctor(result: DoctorResult) -> str:
    lines = [
        "CodeWiki Doctor",
        "",
        f"Repository: {result.repo_root}",
        f"Wiki: {result.wiki_root}",
        f"Result: {'healthy' if result.healthy else 'issues found'}",
        "",
    ]
    for check in result.checks:
        lines.append(f"[{check.status.upper()}] {check.check}: {check.message}")
    return "\n".join(lines).rstrip() + "\n"


def _render_entity_body(entity_id: str, entity_type: str, body: str) -> list[str]:
    label = ENTITY_LABELS.get(entity_type, entity_type)
    indented = "\n".join(f"  {line}" for line in body.splitlines())
    return [f"- {entity_id} · {label}", indented or "  (empty body)"]


def _render_code_references(references: tuple) -> list[str]:
    lines: list[str] = []
    for reference in references:
        location = f" ({reference.path})" if reference.path and reference.path != reference.value else ""
        existence = ""
        if reference.exists is True:
            existence = " [exists]"
        elif reference.exists is False:
            existence = " [missing]"
        lines.append(f"- {reference.kind}: {reference.value}{location}{existence}")
    return lines


def _short_revision(value: str | None) -> str:
    if not value:
        return "unknown"
    return value[:12]

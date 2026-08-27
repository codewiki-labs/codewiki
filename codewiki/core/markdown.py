"""Deterministic Markdown parsing shared by the validator and Core service."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import re
from typing import Optional


REQUIREMENT_SECTIONS = {
    "Requirements",
    "Actor And Permission Requirements",
    "Security And Trust Boundaries",
    "Calculation And Policy Contracts",
    "Domain Invariants",
    "Lifecycle And Side Effects",
    "Failure And Recovery Requirements",
    "Data, Retention And Audit Requirements",
    "Invariants",
    "Failure And Audit Requirements",
}
REQUIREMENT_ID = re.compile(r".+-R\d{3}$")
ACCEPTANCE_CRITERION_ID = re.compile(r".+-AC\d{3}$")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
SPEC_ITEM_HEADING = re.compile(
    r"(?m)^### (?:(Requirement|Acceptance Criterion): )?"
    r"`([^`\n]+)`[ \t]*\r?$"
)
FEATURE_HEADING = re.compile(r"(?m)^### Feature: `([^`\n]+)`[ \t]*\r?$")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
HTTP_ROUTE = re.compile(
    r"^(?:GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\s+/\S+$",
    re.IGNORECASE,
)
SYMBOL = re.compile(r"^[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*$")


@dataclass(frozen=True, slots=True)
class ParsedSpecEntity:
    id: str
    entity_type: str
    body: str
    section: str


@dataclass(frozen=True, slots=True)
class ParsedFeature:
    id: str
    body: str
    spec_basis: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ParsedLink:
    path: str
    relation: str


@dataclass(frozen=True, slots=True)
class ParsedCodeToken:
    kind: str
    value: str
    path: str | None = None


def _mask_markdown_fences(text: str) -> str:
    """Mask fenced code while preserving offsets and line boundaries."""
    masked: list[str] = []
    fence_character: Optional[str] = None
    fence_length = 0
    for line in text.splitlines(keepends=True):
        visible = line.rstrip("\r\n")
        if fence_character is None:
            opening = FENCE_OPEN.match(visible)
            if opening:
                marker = opening.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
                masked.append(re.sub(r"[^\r\n]", " ", line))
                continue
            masked.append(line)
            continue

        closing = re.fullmatch(
            rf" {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*",
            visible,
        )
        masked.append(re.sub(r"[^\r\n]", " ", line))
        if closing:
            fence_character = None
            fence_length = 0
    return "".join(masked)


def mask_markdown_fences(text: str) -> str:
    return _mask_markdown_fences(text)


def _parent_level_two_section(text: str, offset: int) -> Optional[str]:
    matches = list(re.finditer(r"(?m)^## (?!#)(.+?)\s*$", text[:offset]))
    return matches[-1].group(1).strip() if matches else None


def _heading_block(text: str, structure: str, match: re.Match[str]) -> str:
    body_start = match.end()
    newline = re.match(r"\r?\n", structure[body_start:])
    if newline:
        body_start += len(newline.group(0))
    boundary = re.search(r"(?m)^(?:### |## |# )", structure[body_start:])
    body_end = body_start + boundary.start() if boundary else len(text)
    return text[body_start:body_end]


def feature_block(text: str, feature_id: str) -> Optional[str]:
    """Return one feature body with fenced code masked for validator safety."""
    structure = _mask_markdown_fences(text)
    matches = [
        match
        for match in FEATURE_HEADING.finditer(structure)
        if match.group(1) == feature_id
    ]
    if len(matches) != 1:
        return None
    match = matches[0]
    body_start = match.end()
    newline = re.match(r"\r?\n", structure[body_start:])
    if newline:
        body_start += len(newline.group(0))
    boundary = re.search(r"(?m)^(?:### |## |# )", structure[body_start:])
    body_end = body_start + boundary.start() if boundary else len(structure)
    return structure[body_start:body_end]


def requirement_block(text: str, requirement_id: str) -> Optional[str]:
    """Return one unambiguous Requirement body using the legacy validator rules."""
    structure = _mask_markdown_fences(text)
    matches: list[re.Match[str]] = []
    if REQUIREMENT_ID.fullmatch(requirement_id):
        compact = re.compile(
            rf"(?m)^### `{re.escape(requirement_id)}`[ \t]*\r?$",
        )
        for match in compact.finditer(structure):
            if _parent_level_two_section(structure, match.start()) in REQUIREMENT_SECTIONS:
                matches.append(match)

    if not ACCEPTANCE_CRITERION_ID.fullmatch(requirement_id):
        legacy = re.compile(
            rf"(?m)^### Requirement: `{re.escape(requirement_id)}`[ \t]*\r?$",
        )
        for match in legacy.finditer(structure):
            if _parent_level_two_section(structure, match.start()) in REQUIREMENT_SECTIONS:
                matches.append(match)
    if len(matches) != 1:
        return None
    return _heading_block(text, structure, matches[0])


def requirement_exists(text: str, requirement_id: str) -> bool:
    return requirement_block(text, requirement_id) is not None


def parse_spec_entities(text: str) -> tuple[ParsedSpecEntity, ...]:
    """Parse valid Requirement and Acceptance Criterion headings outside fences."""
    structure = _mask_markdown_fences(text)
    parsed: list[ParsedSpecEntity] = []
    for match in SPEC_ITEM_HEADING.finditer(structure):
        legacy_label, item_id = match.groups()
        section = _parent_level_two_section(structure, match.start())
        entity_type: str | None = None

        if legacy_label == "Requirement":
            if not ACCEPTANCE_CRITERION_ID.fullmatch(item_id):
                entity_type = "requirement"
        elif legacy_label == "Acceptance Criterion":
            if not REQUIREMENT_ID.fullmatch(item_id):
                entity_type = "acceptance_criterion"
        elif REQUIREMENT_ID.fullmatch(item_id) and section in REQUIREMENT_SECTIONS:
            entity_type = "requirement"
        elif ACCEPTANCE_CRITERION_ID.fullmatch(item_id) and section == "Acceptance Criteria":
            entity_type = "acceptance_criterion"

        if entity_type is None:
            continue
        if entity_type == "requirement" and section not in REQUIREMENT_SECTIONS:
            continue
        if entity_type == "acceptance_criterion" and section != "Acceptance Criteria":
            continue
        parsed.append(
            ParsedSpecEntity(
                id=item_id,
                entity_type=entity_type,
                body=_heading_block(text, structure, match).strip(),
                section=section or "",
            )
        )
    return tuple(parsed)


def backticked_ids(text: str) -> set[str]:
    return set(INLINE_CODE.findall(text))


def _section_body(text: str, heading: str) -> str:
    structure = _mask_markdown_fences(text)
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*$\r?\n(.*?)(?=^## |\Z)",
        structure,
    )
    if not match:
        return ""
    return text[match.start(1) : match.end(1)]


def has_observation_marker(text: str) -> bool:
    structure = _mask_markdown_fences(text)
    return bool(
        re.search(
            r"(?m)^(?:[-*]\s*)?(?:Observed only|Confirm needed):\s*\S",
            structure,
        )
    )


def view_spec_basis_ids(text: str) -> set[str]:
    structure = _mask_markdown_fences(text)
    identifiers: set[str] = set()
    for match in re.finditer(r"(?m)^- Spec Basis:\s*(.+)$", structure):
        identifiers.update(backticked_ids(match.group(1)))
    identifiers.update(backticked_ids(_section_body(text, "Spec Basis")))
    return identifiers


def parse_features(text: str) -> tuple[ParsedFeature, ...]:
    structure = _mask_markdown_fences(text)
    features: list[ParsedFeature] = []
    for match in FEATURE_HEADING.finditer(structure):
        body = _heading_block(text, structure, match).strip()
        basis_match = re.search(
            r"(?m)^- Spec Basis:\s*(.+)$",
            _mask_markdown_fences(body),
        )
        basis = tuple(
            value
            for value in (backticked_ids(basis_match.group(1)) if basis_match else ())
            if REQUIREMENT_ID.fullmatch(value) or ACCEPTANCE_CRITERION_ID.fullmatch(value)
        )
        features.append(ParsedFeature(match.group(1), body, tuple(sorted(basis))))
    return tuple(features)


def markdown_title(text: str, fallback: str = "") -> str:
    structure = _mask_markdown_fences(text)
    match = re.search(r"(?m)^# (?!#)(.+?)\s*$", structure)
    return match.group(1).strip() if match else fallback


def plain_text(value: str) -> str:
    value = re.sub(r"!?(\[([^]]+)\])\([^)]+\)", r"\2", value)
    value = re.sub(r"[`*_>#]", "", value)
    value = re.sub(r"(?m)^\s*[-+]\s+", "", value)
    return re.sub(r"\s+", " ", value).strip()


def first_paragraph(text: str) -> str:
    structure = _mask_markdown_fences(text)
    for block in re.split(r"\r?\n\s*\r?\n", structure):
        candidate = block.strip()
        if not candidate or candidate.startswith("#"):
            continue
        cleaned = plain_text(candidate)
        if cleaned:
            return cleaned
    return ""


def parse_typed_links(text: str) -> tuple[ParsedLink, ...]:
    links: list[ParsedLink] = []
    for heading, relation in (
        ("Required Context", "required_context"),
        ("See Also", "see_also"),
    ):
        body = _section_body(text, heading)
        for target in re.findall(r"\[[^]]+\]\(([^)#]+\.md)(?:#[^)]+)?\)", body):
            links.append(ParsedLink(target, relation))
    return tuple(links)


def _looks_like_file_path(value: str) -> bool:
    if value.startswith(("http://", "https://", "/")):
        return False
    if "/" not in value:
        return False
    path = PurePosixPath(value)
    return bool(path.suffix) or value.startswith(
        ("src/", "app/", "lib/", "tests/", "test/", "packages/", "services/")
    )


def extract_code_tokens(text: str) -> tuple[ParsedCodeToken, ...]:
    """Extract only explicit inline-code paths, symbols, and routes from Reference."""
    structure = _mask_markdown_fences(text)
    tokens: list[ParsedCodeToken] = []
    seen: set[tuple[str, str, str | None]] = set()
    for line in structure.splitlines():
        values = INLINE_CODE.findall(line)
        paths = [value for value in values if _looks_like_file_path(value)]
        line_path = paths[0] if len(paths) == 1 else None
        for value in values:
            kind: str | None = None
            associated_path: str | None = None
            if REQUIREMENT_ID.fullmatch(value) or ACCEPTANCE_CRITERION_ID.fullmatch(value):
                continue
            if HTTP_ROUTE.fullmatch(value):
                kind = "route"
            elif _looks_like_file_path(value):
                kind = "file"
                associated_path = value
            elif SYMBOL.fullmatch(value):
                kind = "symbol"
                associated_path = line_path
            if kind is None:
                continue
            key = (kind, value, associated_path)
            if key not in seen:
                seen.add(key)
                tokens.append(ParsedCodeToken(kind, value, associated_path))
    return tuple(tokens)

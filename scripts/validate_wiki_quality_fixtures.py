#!/usr/bin/env python3
"""Validate semantic-quality fixtures for Spec contracts and Reference traces."""

from pathlib import Path
import json
import re
import sys
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "wiki-quality"


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def feature_block(text: str, feature_id: str) -> Optional[str]:
    pattern = rf"(?ms)^### Feature: `{re.escape(feature_id)}`\s*$\n(.*?)(?=^### Feature: `|\Z)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def requirement_block(text: str, requirement_id: str) -> Optional[str]:
    pattern = (
        rf"(?ms)^### Requirement: `{re.escape(requirement_id)}`\s*$\n"
        rf"(.*?)(?=^### Requirement: `|^## |\Z)"
    )
    match = re.search(pattern, text)
    return match.group(1) if match else None


def validate_candidate(candidate_root: Path, manifest: dict) -> list[str]:
    failures: list[str] = []
    dimensions = manifest["trace_dimensions"]
    for feature in manifest["features"]:
        if feature["importance"] != "important":
            continue

        spec_page = candidate_root / "specs" / "domains" / f"{feature['domain']}.md"
        spec_text = spec_page.read_text(encoding="utf-8") if spec_page.exists() else ""
        if not spec_page.exists():
            failures.append(f"{feature['id']}: missing paired domain Spec {spec_page}")
        for requirement in feature["spec_requirements"]:
            block = requirement_block(spec_text, requirement["id"])
            if block is None:
                failures.append(
                    f"{feature['id']}: missing approved Spec requirement {requirement['id']}"
                )
                continue
            for evidence in requirement["evidence"]:
                if evidence not in block:
                    failures.append(
                        f"{feature['id']}: Spec requirement {requirement['id']} "
                        f"missing behavioral evidence {evidence}"
                    )

        page = candidate_root / "reference" / "domains" / f"{feature['domain']}.md"
        if not page.exists():
            failures.append(f"{feature['id']}: missing domain Reference {page}")
            continue
        text = page.read_text(encoding="utf-8")
        block = feature_block(text, feature["id"])
        if block is None:
            failures.append(f"{feature['id']}: missing feature trace")
            continue
        for dimension in dimensions:
            match = re.search(rf"(?m)^- {re.escape(dimension)}:\s*(.+)$", block)
            if not match or not match.group(1).strip():
                failures.append(f"{feature['id']}: missing {dimension}")
        spec_basis = re.search(r"(?m)^- Spec Basis:\s*(.+)$", block)
        if spec_basis:
            for requirement in feature["spec_requirements"]:
                if requirement["id"] not in spec_basis.group(1):
                    failures.append(
                        f"{feature['id']}: Reference missing Spec Basis {requirement['id']}"
                    )
        for evidence in feature["evidence"]:
            if evidence not in block:
                failures.append(f"{feature['id']}: missing evidence {evidence}")
    return failures


def validate_fixture_contract() -> list[str]:
    manifest = load_manifest(FIXTURES / "feature-surfaces.json")
    shallow = validate_candidate(FIXTURES / "shallow", manifest)
    complete = validate_candidate(FIXTURES / "complete", manifest)
    authority_leakage = validate_candidate(FIXTURES / "authority-leakage", manifest)
    expected_shallow = {
        "poster-generation: missing feature trace",
        "provider-usage-accounting: missing feature trace",
        "admin-menu-authorization: missing feature trace",
    }
    missing_expected = sorted(item for item in expected_shallow if item not in shallow)
    unexpected_shallow = sorted(item for item in shallow if item not in expected_shallow)
    failures = [f"shallow fixture did not detect: {item}" for item in missing_expected]
    failures.extend(f"shallow fixture unexpected finding: {item}" for item in unexpected_shallow)
    expected_authority_leakage = {
        "provider-usage-accounting: missing approved Spec requirement MU-USAGE-003",
    }
    missing_authority_leakage = sorted(
        item for item in expected_authority_leakage if item not in authority_leakage
    )
    unexpected_authority_leakage = sorted(
        item for item in authority_leakage if item not in expected_authority_leakage
    )
    failures.extend(
        f"authority-leakage fixture did not detect: {item}"
        for item in missing_authority_leakage
    )
    failures.extend(
        f"authority-leakage fixture unexpected finding: {item}"
        for item in unexpected_authority_leakage
    )
    failures.extend(f"complete fixture: {item}" for item in complete)
    return failures


def main() -> int:
    failures = validate_fixture_contract()
    if failures:
        for item in failures:
            print(f"FAIL {item}", file=sys.stderr)
        return 1
    print("Code-Wiki semantic quality fixtures passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

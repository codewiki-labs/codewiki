"""Repository and Git helpers for CodeWiki status checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence


@dataclass(frozen=True, slots=True)
class GitComparison:
    available: bool
    current_revision: str | None
    indexed_revision: str | None
    revision_valid: bool | None
    is_ancestor: bool | None
    committed_paths: tuple[str, ...]
    uncommitted_paths: tuple[str, ...]
    warnings: tuple[str, ...]


def git_command(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None


def _successful_stdout(repo_root: Path, *args: str) -> str | None:
    result = git_command(repo_root, *args)
    if result is None or result.returncode != 0:
        return None
    return result.stdout.strip()


def git_root(repo_root: Path) -> Path | None:
    value = _successful_stdout(repo_root, "rev-parse", "--show-toplevel")
    return Path(value).resolve() if value else None


def _wiki_relative(git_root_path: Path, wiki_root: Path) -> str | None:
    try:
        value = wiki_root.resolve().relative_to(git_root_path.resolve()).as_posix()
    except ValueError:
        return None
    return value


def paths_outside_wiki(
    git_root_path: Path,
    wiki_root: Path,
    paths: Sequence[str],
) -> tuple[str, ...]:
    wiki_relative = _wiki_relative(git_root_path, wiki_root)
    if not wiki_relative or wiki_relative == ".":
        return tuple(sorted({path for path in paths if path}))
    prefix = f"{wiki_relative}/"
    return tuple(
        sorted(
            {
                path
                for path in paths
                if path and path != wiki_relative and not path.startswith(prefix)
            }
        )
    )


def uncommitted_paths(repo_root: Path, wiki_root: Path) -> tuple[str, ...]:
    root = git_root(repo_root)
    if root is None:
        return ()
    commands = (
        ("diff", "--name-only", "--no-renames", "--"),
        ("diff", "--cached", "--name-only", "--no-renames", "--"),
        ("ls-files", "--others", "--exclude-standard", "--"),
    )
    paths: list[str] = []
    for command in commands:
        result = git_command(repo_root, *command)
        if result is not None and result.returncode == 0:
            paths.extend(result.stdout.splitlines())
    return paths_outside_wiki(root, wiki_root, paths)


def compare_revision(
    repo_root: Path,
    wiki_root: Path,
    indexed_revision: str | None,
) -> GitComparison:
    root = git_root(repo_root)
    if root is None:
        return GitComparison(
            available=False,
            current_revision=None,
            indexed_revision=indexed_revision,
            revision_valid=None,
            is_ancestor=None,
            committed_paths=(),
            uncommitted_paths=(),
            warnings=("Git repository information is unavailable.",),
        )
    warnings: list[str] = []
    if root != repo_root.resolve():
        return GitComparison(
            available=False,
            current_revision=None,
            indexed_revision=indexed_revision,
            revision_valid=None,
            is_ancestor=None,
            committed_paths=(),
            uncommitted_paths=(),
            warnings=(f"Repository root differs from Git worktree root: {root}",),
        )

    current = _successful_stdout(repo_root, "rev-parse", "--verify", "HEAD")
    dirty = uncommitted_paths(repo_root, wiki_root)
    if not indexed_revision:
        return GitComparison(
            available=True,
            current_revision=current,
            indexed_revision=None,
            revision_valid=None,
            is_ancestor=None,
            committed_paths=(),
            uncommitted_paths=dirty,
            warnings=tuple(warnings + ["coverage.json has no source_revision."]),
        )

    resolved = _successful_stdout(
        repo_root,
        "rev-parse",
        "--verify",
        f"{indexed_revision}^{{commit}}",
    )
    if not resolved:
        return GitComparison(
            available=True,
            current_revision=current,
            indexed_revision=indexed_revision,
            revision_valid=False,
            is_ancestor=None,
            committed_paths=(),
            uncommitted_paths=dirty,
            warnings=tuple(
                warnings
                + [f"coverage source_revision does not resolve: {indexed_revision}"]
            ),
        )

    immutable = indexed_revision == resolved
    if not immutable:
        warnings.append(
            "coverage source_revision is not an immutable full commit ID: "
            f"{indexed_revision} resolves to {resolved}"
        )
    ancestry_result = git_command(repo_root, "merge-base", "--is-ancestor", resolved, "HEAD")
    is_ancestor = (
        ancestry_result.returncode == 0
        if ancestry_result is not None and ancestry_result.returncode in {0, 1}
        else None
    )
    if is_ancestor is False:
        warnings.append(f"coverage source_revision is not an ancestor of HEAD: {resolved}")
    elif is_ancestor is None:
        warnings.append("Could not compare coverage source_revision with HEAD.")

    committed: tuple[str, ...] = ()
    if is_ancestor:
        changed = git_command(
            repo_root,
            "diff",
            "--name-only",
            "--no-renames",
            f"{resolved}..HEAD",
            "--",
        )
        if changed is not None and changed.returncode == 0:
            committed = paths_outside_wiki(root, wiki_root, changed.stdout.splitlines())
        else:
            warnings.append("Could not list committed source changes.")

    return GitComparison(
        available=True,
        current_revision=current,
        indexed_revision=indexed_revision,
        revision_valid=immutable,
        is_ancestor=is_ancestor,
        committed_paths=committed,
        uncommitted_paths=dirty,
        warnings=tuple(warnings),
    )

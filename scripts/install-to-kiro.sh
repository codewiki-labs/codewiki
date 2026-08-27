#!/bin/sh
set -eu

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/.." && pwd)
skill_names='using-code-wiki creating-code-wiki reading-code-wiki exploring-code-with-wiki updating-code-wiki auditing-code-wiki writing-code-wiki-skills'
mode=global
project_root=
dry_run=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install-to-kiro.sh [--global | --project PATH] [--dry-run]

Install the seven Code-Wiki skills for the current user or one workspace.

Options:
  --global        Install under ${KIRO_HOME:-$HOME/.kiro}/skills (default).
  --project PATH  Install under PATH/.kiro/skills.
  --dry-run       Print the destination without copying files.
  -h, --help      Show this help.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --global)
      mode=global
      project_root=
      shift
      ;;
    --project)
      [ "$#" -ge 2 ] || { printf 'ERROR: --project requires a path\n' >&2; exit 2; }
      mode=project
      project_root=$2
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'ERROR: unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [ "$mode" = project ]; then
  destination=$project_root/.kiro/skills
else
  kiro_root=${KIRO_HOME:-${HOME:?HOME must be set}/.kiro}
  destination=$kiro_root/skills
fi

printf 'Installing Code-Wiki skills to %s\n' "$destination"
if [ "$dry_run" -eq 1 ]; then
  printf 'Dry run: no files copied.\n'
  exit 0
fi

mkdir -p "$destination"
for skill in $skill_names; do
  source_dir=$repo_root/skills/$skill
  [ -d "$source_dir" ] || {
    printf 'ERROR: missing source skill: %s\n' "$source_dir" >&2
    exit 1
  }
  target_dir=$destination/$skill
  mkdir -p "$target_dir"
  cp -R "$source_dir/." "$target_dir/"
done

printf 'Installed seven Code-Wiki skills. Start a new Kiro CLI chat session to load them.\n'

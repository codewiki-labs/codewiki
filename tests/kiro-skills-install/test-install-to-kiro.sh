#!/bin/sh
set -eu

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/../.." && pwd)
installer=$repo_root/scripts/install-to-kiro.sh
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/code-wiki-kiro-install.XXXXXX")
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

skill_names='using-code-wiki creating-code-wiki reading-code-wiki exploring-code-with-wiki updating-code-wiki auditing-code-wiki writing-code-wiki-skills'

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

assert_install_matches() {
  destination=$1
  count=0
  for skill in $skill_names; do
    [ -f "$destination/$skill/SKILL.md" ] || fail "missing installed skill: $skill"
    cmp "$repo_root/skills/$skill/SKILL.md" "$destination/$skill/SKILL.md" >/dev/null || \
      fail "installed skill differs from source: $skill"
    count=$((count + 1))
  done
  [ "$count" -eq 7 ] || fail "expected seven skills"
  resource=creating-code-wiki/references/coverage-example.json
  [ -f "$destination/$resource" ] || fail "missing installed skill resource: $resource"
  cmp "$repo_root/skills/$resource" "$destination/$resource" >/dev/null || \
    fail "installed skill resource differs from source: $resource"
}

# Empty KIRO_HOME follows Kiro CLI's documented fallback to $HOME/.kiro.
home_root=$tmp_dir/home
HOME=$home_root KIRO_HOME= "$installer" >/dev/null
assert_install_matches "$home_root/.kiro/skills"

# A non-empty KIRO_HOME relocates the user-level Kiro root.
custom_root=$tmp_dir/custom-kiro
HOME=$home_root KIRO_HOME=$custom_root "$installer" --global >/dev/null
assert_install_matches "$custom_root/skills"

# Reinstall refreshes Code-Wiki while preserving unrelated skills and extra files.
printf '%s\n' stale > "$custom_root/skills/using-code-wiki/SKILL.md"
mkdir -p "$custom_root/skills/unrelated-skill"
printf '%s\n' keep > "$custom_root/skills/unrelated-skill/SKILL.md"
printf '%s\n' keep > "$custom_root/skills/using-code-wiki/local-note.txt"
HOME=$home_root KIRO_HOME=$custom_root "$installer" >/dev/null
assert_install_matches "$custom_root/skills"
[ "$(cat "$custom_root/skills/unrelated-skill/SKILL.md")" = keep ] || fail "unrelated skill changed"
[ "$(cat "$custom_root/skills/using-code-wiki/local-note.txt")" = keep ] || fail "extra skill file changed"

# Project installation uses the workspace-local .kiro/skills path.
project_root=$tmp_dir/project
mkdir -p "$project_root"
HOME=$home_root KIRO_HOME=$custom_root "$installer" --project "$project_root" >/dev/null
assert_install_matches "$project_root/.kiro/skills"

# Dry-run reports but does not create its destination.
dry_root=$tmp_dir/dry-kiro
output=$(HOME=$home_root KIRO_HOME=$dry_root "$installer" --dry-run)
printf '%s\n' "$output" | grep 'Dry run: no files copied.' >/dev/null || fail "dry-run message missing"
[ ! -e "$dry_root" ] || fail "dry-run created files"

printf '%s\n' 'PASS: Kiro CLI installer copies and refreshes all seven skills safely'

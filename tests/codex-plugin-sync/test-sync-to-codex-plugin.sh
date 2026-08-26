#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYNC_SCRIPT_SOURCE="$REPO_ROOT/scripts/sync-to-codex-plugin.sh"
BASH_UNDER_TEST="/bin/bash"
MANIFEST_VERSION="0.3.0"
FAILURES=0
TEST_ROOT=""

pass() {
    echo "  [PASS] $1"
}

fail() {
    echo "  [FAIL] $1"
    FAILURES=$((FAILURES + 1))
}

assert_equals() {
    local actual="$1"
    local expected="$2"
    local description="$3"

    if [[ "$actual" == "$expected" ]]; then
        pass "$description"
    else
        fail "$description"
        echo "    expected: $expected"
        echo "    actual:   $actual"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local description="$3"

    if printf '%s' "$haystack" | grep -Fq -- "$needle"; then
        pass "$description"
    else
        fail "$description"
        echo "    expected to find: $needle"
    fi
}

assert_not_contains() {
    local haystack="$1"
    local needle="$2"
    local description="$3"

    if printf '%s' "$haystack" | grep -Fq -- "$needle"; then
        fail "$description"
        echo "    did not expect to find: $needle"
    else
        pass "$description"
    fi
}

assert_matches() {
    local haystack="$1"
    local pattern="$2"
    local description="$3"

    if printf '%s' "$haystack" | grep -Eq -- "$pattern"; then
        pass "$description"
    else
        fail "$description"
        echo "    expected to match: $pattern"
    fi
}

assert_not_matches() {
    local haystack="$1"
    local pattern="$2"
    local description="$3"

    if printf '%s' "$haystack" | grep -Eq -- "$pattern"; then
        fail "$description"
        echo "    did not expect to match: $pattern"
    else
        pass "$description"
    fi
}

assert_path_absent() {
    local path="$1"
    local description="$2"

    if [[ ! -e "$path" ]]; then
        pass "$description"
    else
        fail "$description"
        echo "    did not expect path to exist: $path"
    fi
}

assert_branch_absent() {
    local repo="$1"
    local pattern="$2"
    local description="$3"
    local branches

    branches="$(git -C "$repo" branch --list "$pattern")"

    if [[ -z "$branches" ]]; then
        pass "$description"
    else
        fail "$description"
        echo "    did not expect matching branches:"
        echo "$branches" | sed 's/^/      /'
    fi
}

assert_current_branch() {
    local repo="$1"
    local expected="$2"
    local description="$3"
    local actual

    actual="$(git -C "$repo" branch --show-current)"
    assert_equals "$actual" "$expected" "$description"
}

assert_file_equals() {
    local path="$1"
    local expected="$2"
    local description="$3"
    local actual

    actual="$(cat "$path")"
    assert_equals "$actual" "$expected" "$description"
}

cleanup() {
    if [[ -n "$TEST_ROOT" && -d "$TEST_ROOT" ]]; then
        rm -rf "$TEST_ROOT"
    fi
}

configure_git_identity() {
    local repo="$1"

    git -C "$repo" config user.name "Test Bot"
    git -C "$repo" config user.email "test@example.com"
}

init_repo() {
    local repo="$1"

    git init -q -b main "$repo"
    configure_git_identity "$repo"
}

commit_fixture() {
    local repo="$1"
    local message="$2"

    git -C "$repo" commit -q -m "$message"
}

checkout_fixture_branch() {
    local repo="$1"
    local branch="$2"

    git -C "$repo" checkout -q -b "$branch"
}

write_upstream_fixture() {
    local repo="$1"

    mkdir -p \
        "$repo/.codex-plugin" \
        "$repo/.claude-plugin" \
        "$repo/.private-notes" \
        "$repo/.kimi-plugin" \
        "$repo/docs" \
        "$repo/docs/superpowers/plans" \
        "$repo/examples" \
        "$repo/scripts" \
        "$repo/skills/using-code-wiki" \
        "$repo/tests/codex-plugin-sync"

    cp "$SYNC_SCRIPT_SOURCE" "$repo/scripts/sync-to-codex-plugin.sh"

    cat > "$repo/.gitignore" <<'EOF'
.private-notes/
ignored-cache/
EOF

    cat > "$repo/.codex-plugin/plugin.json" <<EOF
{
  "name": "code-wiki",
  "version": "$MANIFEST_VERSION"
}
EOF

    cat > "$repo/.claude-plugin/plugin.json" <<EOF
{
  "name": "code-wiki",
  "version": "$MANIFEST_VERSION"
}
EOF

    cat > "$repo/.claude-plugin/marketplace.json" <<'EOF'
{
  "name": "code-wiki",
  "plugins": []
}
EOF

    cat > "$repo/.kimi-plugin/plugin.json" <<'EOF'
{
  "name": "not-for-codex"
}
EOF

    cat > "$repo/README.md" <<'EOF'
# code-wiki
EOF

    cat > "$repo/LICENSE" <<'EOF'
MIT
EOF

    cat > "$repo/CHANGELOG.md" <<'EOF'
# Changelog
EOF

    cat > "$repo/CODE_OF_CONDUCT.md" <<'EOF'
# Code of Conduct
EOF

    cat > "$repo/CONTRIBUTING.md" <<'EOF'
# Contributing
EOF

    cat > "$repo/docs/skill-set-design.md" <<'EOF'
# Skill Set Design
EOF

    cat > "$repo/docs/README.ko.md" <<'EOF'
# Code-Wiki
EOF

    cat > "$repo/docs/superpowers/plans/internal-plan.md" <<'EOF'
# Internal Implementation Plan
EOF

    cat > "$repo/examples/basic-workflow.md" <<'EOF'
# Basic Workflow
EOF

    cat > "$repo/scripts/dev-helper.sh" <<'EOF'
#!/usr/bin/env sh
echo dev helper
EOF

    cat > "$repo/scripts/validate_generated_wiki.py" <<'EOF'
#!/usr/bin/env python3
print("generated Wiki validator")
EOF

    cat > "$repo/tests/codex-plugin-sync/test-sync-to-codex-plugin.sh" <<'EOF'
#!/usr/bin/env sh
echo sync test
EOF

    cat > "$repo/skills/using-code-wiki/SKILL.md" <<'EOF'
---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace.
---

# Using code-wiki
EOF

    printf 'tracked private note\n' > "$repo/.private-notes/keep.txt"
    printf 'ignored private note\n' > "$repo/.private-notes/leak.txt"
    mkdir -p "$repo/ignored-cache/tmp"
    printf 'ignored cache state\n' > "$repo/ignored-cache/tmp/state.json"

    git -C "$repo" add \
        .codex-plugin/plugin.json \
        .claude-plugin/plugin.json \
        .claude-plugin/marketplace.json \
        .gitignore \
        .kimi-plugin/plugin.json \
        CHANGELOG.md \
        CODE_OF_CONDUCT.md \
        CONTRIBUTING.md \
        LICENSE \
        README.md \
        docs/README.ko.md \
        docs/skill-set-design.md \
        docs/superpowers/plans/internal-plan.md \
        examples/basic-workflow.md \
        scripts/dev-helper.sh \
        scripts/validate_generated_wiki.py \
        scripts/sync-to-codex-plugin.sh \
        skills/using-code-wiki/SKILL.md \
        tests/codex-plugin-sync/test-sync-to-codex-plugin.sh
    git -C "$repo" add -f .private-notes/keep.txt

    commit_fixture "$repo" "Initial upstream fixture"
}

write_destination_fixture() {
    local repo="$1"

    mkdir -p "$repo/plugins/code-wiki/skills/using-code-wiki"
    printf 'fixture keep\n' > "$repo/plugins/code-wiki/.fixture-keep"
cat > "$repo/plugins/code-wiki/skills/using-code-wiki/SKILL.md" <<'EOF'
---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace.
---

# Stale code-wiki
EOF

    git -C "$repo" add \
        plugins/code-wiki/.fixture-keep \
        plugins/code-wiki/skills/using-code-wiki/SKILL.md

    commit_fixture "$repo" "Initial destination fixture"
}

add_openai_agent_metadata_fixture() {
    local repo="$1"

    mkdir -p "$repo/plugins/code-wiki/skills/using-code-wiki/agents"

    cat > "$repo/plugins/code-wiki/skills/using-code-wiki/agents/openai.yaml" <<'EOF'
interface:
  display_name: "Using code-wiki"
  short_description: "Destination-owned OpenAI metadata"
EOF

    git -C "$repo" add plugins/code-wiki/skills/using-code-wiki/agents/openai.yaml

    commit_fixture "$repo" "Add OpenAI agent metadata fixture"
}

dirty_tracked_destination_skill() {
    local repo="$1"

    cat > "$repo/plugins/code-wiki/skills/using-code-wiki/SKILL.md" <<'EOF'
---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace.
---

# Locally modified code-wiki skill
EOF
}

write_synced_destination_fixture() {
    local repo="$1"

    mkdir -p \
        "$repo/plugins/code-wiki/.codex-plugin" \
        "$repo/plugins/code-wiki/docs" \
        "$repo/plugins/code-wiki/examples" \
        "$repo/plugins/code-wiki/scripts" \
        "$repo/plugins/code-wiki/skills/using-code-wiki/agents"

    cat > "$repo/plugins/code-wiki/.codex-plugin/plugin.json" <<EOF
{
  "name": "code-wiki",
  "version": "$MANIFEST_VERSION"
}
EOF

    cat > "$repo/plugins/code-wiki/README.md" <<'EOF'
# code-wiki
EOF

    cat > "$repo/plugins/code-wiki/LICENSE" <<'EOF'
MIT
EOF

    cat > "$repo/plugins/code-wiki/CHANGELOG.md" <<'EOF'
# Changelog
EOF

    cat > "$repo/plugins/code-wiki/CODE_OF_CONDUCT.md" <<'EOF'
# Code of Conduct
EOF

    cat > "$repo/plugins/code-wiki/CONTRIBUTING.md" <<'EOF'
# Contributing
EOF

    cat > "$repo/plugins/code-wiki/docs/skill-set-design.md" <<'EOF'
# Skill Set Design
EOF

    cat > "$repo/plugins/code-wiki/docs/README.ko.md" <<'EOF'
# Code-Wiki
EOF

    cat > "$repo/plugins/code-wiki/examples/basic-workflow.md" <<'EOF'
# Basic Workflow
EOF

    cat > "$repo/plugins/code-wiki/scripts/validate_generated_wiki.py" <<'EOF'
#!/usr/bin/env python3
print("generated Wiki validator")
EOF

    cat > "$repo/plugins/code-wiki/skills/using-code-wiki/SKILL.md" <<'EOF'
---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace.
---

# Using code-wiki
EOF

    cat > "$repo/plugins/code-wiki/skills/using-code-wiki/agents/openai.yaml" <<'EOF'
interface:
  display_name: "Using code-wiki"
  short_description: "Destination-owned OpenAI metadata"
EOF

    git -C "$repo" add plugins/code-wiki

    commit_fixture "$repo" "Initial synced destination fixture"
}

write_stale_destination_fixture() {
    local repo="$1"

    mkdir -p \
        "$repo/plugins/code-wiki/.kimi-plugin" \
        "$repo/plugins/code-wiki/scripts" \
        "$repo/plugins/code-wiki/tests"
    printf 'fixture keep\n' > "$repo/plugins/code-wiki/.fixture-keep"
    printf '{"name":"stale-kimi"}\n' > "$repo/plugins/code-wiki/.kimi-plugin/plugin.json"
    printf 'stale helper\n' > "$repo/plugins/code-wiki/scripts/dev-helper.sh"
    printf 'stale tests\n' > "$repo/plugins/code-wiki/tests/test.sh"
    git -C "$repo" add plugins/code-wiki

    commit_fixture "$repo" "Initial stale destination fixture"
}

write_bootstrap_destination_fixture() {
    local repo="$1"

    printf 'bootstrap fixture\n' > "$repo/README.md"
    git -C "$repo" add README.md

    commit_fixture "$repo" "Initial bootstrap destination fixture"
}

write_fake_gh() {
    local bin_dir="$1"

    mkdir -p "$bin_dir"

    cat > "$bin_dir/gh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

case "${1:-} ${2:-}" in
    "auth status")
        exit 0
        ;;
    "repo clone")
        echo "unexpected remote clone in local fixture: $*" >&2
        exit 1
        ;;
    "pr create")
        echo "https://github.com/example/codex-plugins/pull/123"
        exit 0
        ;;
esac

echo "unexpected gh invocation: $*" >&2
exit 1
EOF

    chmod +x "$bin_dir/gh"
}

run_preview() {
    local upstream="$1"
    local dest="$2"
    local fake_bin="$3"

    PATH="$fake_bin:$PATH" "$BASH_UNDER_TEST" "$upstream/scripts/sync-to-codex-plugin.sh" \
        -n --repo example/codex-plugins --local "$dest" 2>&1
}

run_bootstrap_preview() {
    local upstream="$1"
    local dest="$2"
    local fake_bin="$3"

    PATH="$fake_bin:$PATH" "$BASH_UNDER_TEST" "$upstream/scripts/sync-to-codex-plugin.sh" \
        -n --bootstrap --repo example/codex-plugins --local "$dest" 2>&1
}

run_preview_without_manifest() {
    local upstream="$1"
    local dest="$2"
    local fake_bin="$3"

    rm -f "$upstream/.codex-plugin/plugin.json"
    PATH="$fake_bin:$PATH" "$BASH_UNDER_TEST" "$upstream/scripts/sync-to-codex-plugin.sh" \
        -n --repo example/codex-plugins --local "$dest" 2>&1
}

run_apply() {
    local upstream="$1"
    local dest="$2"
    local fake_bin="$3"

    PATH="$fake_bin:$PATH" "$BASH_UNDER_TEST" "$upstream/scripts/sync-to-codex-plugin.sh" \
        -y --repo example/codex-plugins --local "$dest" 2>&1
}

run_help() {
    local upstream="$1"
    local fake_bin="$2"

    PATH="$fake_bin:$PATH" "$BASH_UNDER_TEST" "$upstream/scripts/sync-to-codex-plugin.sh" --help 2>&1
}

main() {
    local upstream
    local dest
    local stale_dest
    local dirty_apply_dest
    local dirty_apply_branch
    local noop_apply_dest
    local noop_apply_branch
    local bootstrap_dest
    local bootstrap_branch
    local fake_bin
    local preview_output
    local preview_status
    local preview_section
    local stale_preview_output
    local stale_preview_status
    local stale_preview_section
    local bootstrap_output
    local bootstrap_status
    local dirty_apply_output
    local dirty_apply_status
    local noop_apply_output
    local noop_apply_status
    local missing_manifest_output
    local missing_manifest_status
    local help_output
    local dirty_skill_path
    local noop_openai_metadata_path

    echo "=== Test: code-wiki sync-to-codex-plugin regression ==="

    TEST_ROOT="$(mktemp -d)"
    trap cleanup EXIT

    upstream="$TEST_ROOT/upstream"
    dest="$TEST_ROOT/destination"
    stale_dest="$TEST_ROOT/stale-destination"
    dirty_apply_dest="$TEST_ROOT/dirty-apply-destination"
    noop_apply_dest="$TEST_ROOT/noop-apply-destination"
    bootstrap_dest="$TEST_ROOT/bootstrap-destination"
    fake_bin="$TEST_ROOT/bin"
    dirty_apply_branch="fixture/dirty-apply-target"
    noop_apply_branch="fixture/noop-apply-target"
    bootstrap_branch="fixture/bootstrap-preview-target"

    init_repo "$upstream"
    write_upstream_fixture "$upstream"

    init_repo "$dest"
    write_destination_fixture "$dest"
    add_openai_agent_metadata_fixture "$dest"
    checkout_fixture_branch "$dest" "fixture/preview-target"

    init_repo "$stale_dest"
    write_stale_destination_fixture "$stale_dest"

    init_repo "$dirty_apply_dest"
    write_synced_destination_fixture "$dirty_apply_dest"
    checkout_fixture_branch "$dirty_apply_dest" "$dirty_apply_branch"
    dirty_tracked_destination_skill "$dirty_apply_dest"

    init_repo "$noop_apply_dest"
    write_synced_destination_fixture "$noop_apply_dest"
    checkout_fixture_branch "$noop_apply_dest" "$noop_apply_branch"

    init_repo "$bootstrap_dest"
    write_bootstrap_destination_fixture "$bootstrap_dest"
    checkout_fixture_branch "$bootstrap_dest" "$bootstrap_branch"

    write_fake_gh "$fake_bin"

    set +e
    preview_output="$(run_preview "$upstream" "$dest" "$fake_bin")"
    preview_status=$?
    stale_preview_output="$(run_preview "$upstream" "$stale_dest" "$fake_bin")"
    stale_preview_status=$?
    bootstrap_output="$(run_bootstrap_preview "$upstream" "$bootstrap_dest" "$fake_bin")"
    bootstrap_status=$?
    dirty_apply_output="$(run_apply "$upstream" "$dirty_apply_dest" "$fake_bin")"
    dirty_apply_status=$?
    noop_apply_output="$(run_apply "$upstream" "$noop_apply_dest" "$fake_bin")"
    noop_apply_status=$?
    missing_manifest_output="$(run_preview_without_manifest "$upstream" "$dest" "$fake_bin")"
    missing_manifest_status=$?
    set -e

    help_output="$(run_help "$upstream" "$fake_bin")"
    preview_section="$(printf '%s\n' "$preview_output" | sed -n '/^=== Preview (rsync --dry-run) ===$/,/^=== End preview ===$/p')"
    stale_preview_section="$(printf '%s\n' "$stale_preview_output" | sed -n '/^=== Preview (rsync --dry-run) ===$/,/^=== End preview ===$/p')"
    dirty_skill_path="$dirty_apply_dest/plugins/code-wiki/skills/using-code-wiki/SKILL.md"
    noop_openai_metadata_path="$noop_apply_dest/plugins/code-wiki/skills/using-code-wiki/agents/openai.yaml"

    echo ""
    echo "Preview assertions..."
    assert_equals "$preview_status" "0" "Preview exits successfully"
    assert_contains "$preview_output" "Plugin:   code-wiki" "Preview names code-wiki plugin"
    assert_contains "$preview_output" "Version:  $MANIFEST_VERSION" "Preview uses manifest version"
    assert_contains "$preview_section" ".codex-plugin/plugin.json" "Preview includes manifest path"
    assert_contains "$preview_section" "skills/using-code-wiki/SKILL.md" "Preview includes bootstrap skill"
    assert_contains "$preview_section" "README.md" "Preview includes README"
    assert_contains "$preview_section" "docs/README.ko.md" "Preview includes Korean README"
    assert_contains "$preview_section" "LICENSE" "Preview includes license"
    assert_contains "$preview_section" "docs/skill-set-design.md" "Preview includes docs"
    assert_not_contains "$preview_section" "docs/superpowers/plans/internal-plan.md" "Preview excludes internal implementation plans"
    assert_contains "$preview_section" "examples/basic-workflow.md" "Preview includes examples"
    assert_contains "$preview_section" "scripts/validate_generated_wiki.py" "Preview includes generated-Wiki validator"
    assert_not_contains "$preview_section" "scripts/dev-helper.sh" "Preview excludes development scripts"
    assert_not_contains "$preview_section" "tests/codex-plugin-sync/test-sync-to-codex-plugin.sh" "Preview excludes tests"
    assert_not_contains "$preview_section" ".kimi-plugin/plugin.json" "Preview excludes unrelated manifests"
    assert_not_contains "$preview_section" ".claude-plugin/plugin.json" "Preview excludes Claude Code manifest"
    assert_not_contains "$preview_section" ".claude-plugin/marketplace.json" "Preview excludes Claude Code marketplace"
    assert_not_contains "$preview_section" ".private-notes/leak.txt" "Preview excludes ignored untracked files"
    assert_not_contains "$preview_section" "ignored-cache/" "Preview excludes pure ignored directories"
    assert_not_matches "$preview_section" "\\*deleting +skills/using-code-wiki/agents/openai\\.yaml" "Preview preserves destination-owned OpenAI agent metadata"
    assert_current_branch "$dest" "fixture/preview-target" "Preview leaves destination checkout on its original branch"
    assert_branch_absent "$dest" "sync/code-wiki-*" "Preview does not create sync branch in destination checkout"

    echo ""
    echo "Convergence assertions..."
    assert_equals "$stale_preview_status" "0" "Stale destination preview exits successfully"
    assert_matches "$stale_preview_section" "\\*deleting +\\.kimi-plugin/plugin\\.json" "Preview deletes stale unrelated manifest"
    assert_matches "$stale_preview_section" "\\*deleting +scripts/dev-helper\\.sh" "Preview deletes stale scripts"
    assert_matches "$stale_preview_section" "\\*deleting +tests/test\\.sh" "Preview deletes stale tests"

    echo ""
    echo "Bootstrap assertions..."
    assert_equals "$bootstrap_status" "0" "Bootstrap preview exits successfully"
    assert_contains "$bootstrap_output" "Mode:     BOOTSTRAP (creating plugins/code-wiki/ when absent)" "Bootstrap preview describes code-wiki directory creation"
    assert_contains "$bootstrap_output" "Dry run only. Nothing was changed or pushed." "Bootstrap preview remains dry-run only"
    assert_path_absent "$bootstrap_dest/plugins/code-wiki" "Bootstrap preview does not create destination plugin directory"
    assert_current_branch "$bootstrap_dest" "$bootstrap_branch" "Bootstrap preview leaves destination checkout on its original branch"
    assert_branch_absent "$bootstrap_dest" "bootstrap/code-wiki-*" "Bootstrap preview does not create bootstrap branch in destination checkout"

    echo ""
    echo "Apply assertions..."
    assert_equals "$dirty_apply_status" "1" "Dirty local apply exits with failure"
    assert_contains "$dirty_apply_output" "ERROR: local checkout has uncommitted changes under 'plugins/code-wiki'" "Dirty local apply reports protected destination path"
    assert_current_branch "$dirty_apply_dest" "$dirty_apply_branch" "Dirty local apply leaves destination checkout on its original branch"
    assert_branch_absent "$dirty_apply_dest" "sync/code-wiki-*" "Dirty local apply does not create sync branch in destination checkout"
    assert_file_equals "$dirty_skill_path" "---
name: using-code-wiki
description: Use when starting any conversation in a code repository or project workspace.
---

# Locally modified code-wiki skill" "Dirty local apply preserves tracked working-tree file content"
    assert_equals "$noop_apply_status" "0" "Clean no-op local apply exits successfully"
    assert_contains "$noop_apply_output" "No changes - embedded plugin was already in sync with upstream" "Clean no-op local apply reports no changes"
    assert_current_branch "$noop_apply_dest" "$noop_apply_branch" "Clean no-op local apply leaves destination checkout on its original branch"
    assert_branch_absent "$noop_apply_dest" "sync/code-wiki-*" "Clean no-op local apply does not create sync branch"
    assert_file_equals "$noop_openai_metadata_path" "interface:
  display_name: \"Using code-wiki\"
  short_description: \"Destination-owned OpenAI metadata\"" "Clean no-op local apply preserves destination-owned OpenAI agent metadata"

    echo ""
    echo "Missing manifest assertions..."
    assert_equals "$missing_manifest_status" "1" "Missing manifest exits with failure"
    assert_contains "$missing_manifest_output" "ERROR: committed Codex manifest missing at" "Missing manifest reports committed manifest path"

    echo ""
    echo "Help assertions..."
    assert_contains "$help_output" "--repo owner/name" "Help documents generalized repo option"
    assert_contains "$help_output" "--dest plugins/code-wiki" "Help documents code-wiki destination"
    assert_not_contains "$help_output" "superpowers" "Help does not mention superpowers"

    if [[ $FAILURES -ne 0 ]]; then
        echo ""
        echo "FAILED: $FAILURES assertion(s) failed."
        exit 1
    fi

    echo ""
    echo "PASS"
}

main "$@"

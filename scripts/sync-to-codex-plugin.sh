#!/usr/bin/env bash
#
# sync-to-codex-plugin.sh
#
# Sync this code-wiki checkout into a Codex plugin repository.
#
# Usage:
#   ./scripts/sync-to-codex-plugin.sh                              # full run
#   ./scripts/sync-to-codex-plugin.sh -n                           # dry run
#   ./scripts/sync-to-codex-plugin.sh -y                           # skip confirm
#   ./scripts/sync-to-codex-plugin.sh --repo owner/name             # destination GitHub repo
#   ./scripts/sync-to-codex-plugin.sh --dest plugins/code-wiki       # destination path
#   ./scripts/sync-to-codex-plugin.sh --local PATH                  # existing destination checkout
#   ./scripts/sync-to-codex-plugin.sh --base BRANCH                 # default: main
#   ./scripts/sync-to-codex-plugin.sh --bootstrap                   # create destination path if missing
#
# If --repo is omitted, CODE_WIKI_CODEX_PLUGIN_REPO is used.
#
# Requires: bash, rsync, git, gh (authenticated), python3.

set -euo pipefail

DEFAULT_BASE="main"
DEFAULT_DEST_REL="plugins/code-wiki"
REPO="${CODE_WIKI_CODEX_PLUGIN_REPO:-}"
DEST_REL="$DEFAULT_DEST_REL"
BASE="$DEFAULT_BASE"
DRY_RUN=0
YES=0
LOCAL_CHECKOUT=""
BOOTSTRAP=0

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UPSTREAM="$(cd "$SCRIPT_DIR/.." && pwd)"

ALLOWLIST=(
  ".codex-plugin"
  "skills"
  "README.md"
  "LICENSE"
  "CHANGELOG.md"
  "CODE_OF_CONDUCT.md"
  "CONTRIBUTING.md"
  "docs"
  "examples"
)

usage() {
  sed -n '/^# Usage:/,/^# Requires:/s/^# \{0,1\}//p' "$0"
  exit "${1:-0}"
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

confirm() {
  [[ $YES -eq 1 ]] && return 0
  read -rp "$1 [y/N] " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]]
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--dry-run) DRY_RUN=1; shift ;;
    -y|--yes) YES=1; shift ;;
    --repo) REPO="$2"; shift 2 ;;
    --dest) DEST_REL="$2"; shift 2 ;;
    --local) LOCAL_CHECKOUT="$2"; shift 2 ;;
    --base) BASE="$2"; shift 2 ;;
    --bootstrap) BOOTSTRAP=1; shift ;;
    -h|--help) usage 0 ;;
    *) echo "Unknown arg: $1" >&2; usage 2 ;;
  esac
done

[[ "$DEST_REL" != /* ]] || die "--dest must be a relative path"
[[ -n "$DEST_REL" ]] || die "--dest must not be empty"

command -v rsync >/dev/null || die "rsync not found in PATH"
command -v git >/dev/null || die "git not found in PATH"
command -v gh >/dev/null || die "gh not found - install GitHub CLI"
command -v python3 >/dev/null || die "python3 not found in PATH"

gh auth status >/dev/null 2>&1 || die "gh not authenticated - run 'gh auth login'"

[[ -d "$UPSTREAM/.git" ]] || die "upstream '$UPSTREAM' is not a git checkout"
[[ -f "$UPSTREAM/.codex-plugin/plugin.json" ]] || die "committed Codex manifest missing at $UPSTREAM/.codex-plugin/plugin.json"

if [[ -z "$REPO" && -z "$LOCAL_CHECKOUT" ]]; then
  die "--repo owner/name is required unless --local PATH is provided; alternatively set CODE_WIKI_CODEX_PLUGIN_REPO"
fi

PLUGIN_NAME="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["name"])' "$UPSTREAM/.codex-plugin/plugin.json")"
PLUGIN_VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$UPSTREAM/.codex-plugin/plugin.json")"
[[ -n "$PLUGIN_NAME" ]] || die "could not read 'name' from committed Codex manifest"
[[ -n "$PLUGIN_VERSION" ]] || die "could not read 'version' from committed Codex manifest"

UPSTREAM_BRANCH="$(git -C "$UPSTREAM" branch --show-current)"
UPSTREAM_SHA="$(git -C "$UPSTREAM" rev-parse HEAD)"
UPSTREAM_SHORT="$(git -C "$UPSTREAM" rev-parse --short HEAD)"

if [[ -n "$UPSTREAM_BRANCH" && "$UPSTREAM_BRANCH" != "main" ]]; then
  echo "WARNING: upstream is on '$UPSTREAM_BRANCH', not 'main'"
  confirm "Sync from '$UPSTREAM_BRANCH' anyway?" || exit 1
fi

UPSTREAM_STATUS="$(git -C "$UPSTREAM" status --porcelain)"
if [[ -n "$UPSTREAM_STATUS" ]]; then
  echo "WARNING: upstream has uncommitted changes:"
  echo "$UPSTREAM_STATUS" | sed 's/^/  /'
  echo "Sync will use working-tree state, not HEAD ($UPSTREAM_SHORT)."
  confirm "Continue anyway?" || exit 1
fi

CLEANUP_DIR=""
DEST_REPO=""
DEST=""
PREVIEW_REPO=""
PREVIEW_DEST=""
SYNC_SOURCE=""

cleanup() {
  if [[ -n "$CLEANUP_DIR" && -d "$CLEANUP_DIR" ]]; then
    rm -rf "$CLEANUP_DIR"
  fi
}
trap cleanup EXIT

if [[ -n "$LOCAL_CHECKOUT" ]]; then
  DEST_REPO="$(cd "$LOCAL_CHECKOUT" && pwd)"
  [[ -d "$DEST_REPO/.git" ]] || die "--local path '$DEST_REPO' is not a git checkout"
else
  echo "Cloning $REPO..."
  CLEANUP_DIR="$(mktemp -d)"
  DEST_REPO="$CLEANUP_DIR/codex-plugin-destination"
  gh repo clone "$REPO" "$DEST_REPO" >/dev/null
fi

DEST="$DEST_REPO/$DEST_REL"
PREVIEW_REPO="$DEST_REPO"
PREVIEW_DEST="$DEST"

prepare_preview_checkout() {
  if [[ -n "$LOCAL_CHECKOUT" ]]; then
    [[ -n "$CLEANUP_DIR" ]] || CLEANUP_DIR="$(mktemp -d)"
    PREVIEW_REPO="$CLEANUP_DIR/preview"
    git clone -q --no-local "$DEST_REPO" "$PREVIEW_REPO"
    PREVIEW_DEST="$PREVIEW_REPO/$DEST_REL"
  fi

  git -C "$PREVIEW_REPO" checkout -q "$BASE" 2>/dev/null || die "base branch '$BASE' does not exist"
  if [[ $BOOTSTRAP -ne 1 ]]; then
    [[ -d "$PREVIEW_DEST" ]] || die "base branch '$BASE' has no '$DEST_REL/' - use --bootstrap, or pass --base <branch>"
  fi
}

prepare_apply_checkout() {
  git -C "$DEST_REPO" checkout -q "$BASE" 2>/dev/null || die "base branch '$BASE' does not exist"
  if [[ $BOOTSTRAP -ne 1 ]]; then
    [[ -d "$DEST" ]] || die "base branch '$BASE' has no '$DEST_REL/' - use --bootstrap, or pass --base <branch>"
  fi
}

copy_tracked_payload() {
  local path
  while IFS= read -r -d '' path; do
    mkdir -p "$SYNC_SOURCE/$(dirname "$path")"
    cp -p "$UPSTREAM/$path" "$SYNC_SOURCE/$path"
  done < <(git -C "$UPSTREAM" ls-files -z -- "${ALLOWLIST[@]}")
}

copy_preserved_destination_metadata() {
  local destination="$1"
  local path
  local rel

  [[ -d "$destination/skills" ]] || return 0

  while IFS= read -r -d '' path; do
    rel="${path#"$destination"/}"
    mkdir -p "$SYNC_SOURCE/$(dirname "$rel")"
    cp -p "$path" "$SYNC_SOURCE/$rel"
  done < <(find "$destination/skills" -path '*/agents/openai.yaml' -type f -print0)
}

prepare_sync_source() {
  local destination="$1"

  [[ -n "$CLEANUP_DIR" ]] || CLEANUP_DIR="$(mktemp -d)"
  SYNC_SOURCE="$CLEANUP_DIR/source-overlay"
  rm -rf "$SYNC_SOURCE"
  mkdir -p "$SYNC_SOURCE"

  copy_tracked_payload
  copy_preserved_destination_metadata "$destination"
}

apply_to_preview_checkout() {
  if [[ $BOOTSTRAP -eq 1 ]]; then
    mkdir -p "$PREVIEW_DEST"
  fi

  rsync -a --checksum --delete "$SYNC_SOURCE/" "$PREVIEW_DEST/"
}

preview_checkout_has_changes() {
  [[ -n "$(git -C "$PREVIEW_REPO" status --porcelain "$DEST_REL")" ]]
}

local_checkout_has_uncommitted_destination_changes() {
  [[ -n "$(git -C "$DEST_REPO" status --porcelain=1 --untracked-files=all --ignored=matching -- "$DEST_REL")" ]]
}

prepare_preview_checkout
prepare_sync_source "$PREVIEW_DEST"

TIMESTAMP="$(date -u +%Y%m%d-%H%M%S)"
if [[ $BOOTSTRAP -eq 1 ]]; then
  SYNC_BRANCH="bootstrap/$PLUGIN_NAME-$UPSTREAM_SHORT-$TIMESTAMP"
else
  SYNC_BRANCH="sync/$PLUGIN_NAME-$UPSTREAM_SHORT-$TIMESTAMP"
fi

echo ""
echo "Upstream: $UPSTREAM (${UPSTREAM_BRANCH:-detached} @ $UPSTREAM_SHORT)"
echo "Plugin:   $PLUGIN_NAME"
echo "Version:  $PLUGIN_VERSION"
if [[ -n "$REPO" ]]; then
  echo "Repo:     $REPO"
else
  echo "Repo:     local checkout"
fi
echo "Base:     $BASE"
echo "Dest:     $DEST_REL"
echo "Branch:   $SYNC_BRANCH"
if [[ $BOOTSTRAP -eq 1 ]]; then
  echo "Mode:     BOOTSTRAP (creating $DEST_REL/ when absent)"
fi
echo ""
echo "=== Preview (rsync --dry-run) ==="
rsync -av --checksum --delete --dry-run --itemize-changes "$SYNC_SOURCE/" "$PREVIEW_DEST/"
echo "=== End preview ==="
echo ""

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Dry run only. Nothing was changed or pushed."
  exit 0
fi

echo ""
confirm "Apply changes, push branch, and open PR?" || { echo "Aborted."; exit 1; }

if [[ -n "$LOCAL_CHECKOUT" ]] && local_checkout_has_uncommitted_destination_changes; then
  die "local checkout has uncommitted changes under '$DEST_REL' - commit, stash, or discard them before syncing"
fi

if [[ -n "$LOCAL_CHECKOUT" ]]; then
  apply_to_preview_checkout
  if ! preview_checkout_has_changes; then
    echo "No changes - embedded plugin was already in sync with upstream $UPSTREAM_SHORT (v$PLUGIN_VERSION)."
    exit 0
  fi
fi

prepare_apply_checkout
cd "$DEST_REPO"
git checkout -q -b "$SYNC_BRANCH"

echo "Syncing upstream content..."
if [[ $BOOTSTRAP -eq 1 ]]; then
  mkdir -p "$DEST"
fi
rsync -a --checksum --delete "$SYNC_SOURCE/" "$DEST/"

if [[ -z "$(git status --porcelain "$DEST_REL")" ]]; then
  echo "No changes - embedded plugin was already in sync with upstream $UPSTREAM_SHORT (v$PLUGIN_VERSION)."
  exit 0
fi

git add "$DEST_REL"

if [[ $BOOTSTRAP -eq 1 ]]; then
  COMMIT_TITLE="bootstrap $PLUGIN_NAME v$PLUGIN_VERSION from upstream main @ $UPSTREAM_SHORT"
  PR_BODY="Initial bootstrap of the $PLUGIN_NAME plugin from upstream \`main\` @ \`$UPSTREAM_SHORT\` (v$PLUGIN_VERSION).

Creates \`$DEST_REL/\` by copying the tracked plugin payload from upstream, including \`.codex-plugin/plugin.json\`, \`skills/\`, public docs, examples, and license files.

Run via: \`scripts/sync-to-codex-plugin.sh --bootstrap\`
Upstream commit: $UPSTREAM_SHA"
else
  COMMIT_TITLE="sync $PLUGIN_NAME v$PLUGIN_VERSION from upstream main @ $UPSTREAM_SHORT"
  PR_BODY="Automated sync from $PLUGIN_NAME upstream \`main\` @ \`$UPSTREAM_SHORT\` (v$PLUGIN_VERSION).

Copies the tracked plugin payload from upstream, including \`.codex-plugin/plugin.json\`, \`skills/\`, public docs, examples, and license files.

Run via: \`scripts/sync-to-codex-plugin.sh\`
Upstream commit: $UPSTREAM_SHA"
fi

git commit --quiet -m "$COMMIT_TITLE

Automated sync via scripts/sync-to-codex-plugin.sh
Upstream: $UPSTREAM_SHA
Branch:   $SYNC_BRANCH"

echo "Pushing $SYNC_BRANCH to $REPO..."
git push -u origin "$SYNC_BRANCH" --quiet

echo "Opening PR..."
PR_URL="$(gh pr create \
  --repo "$REPO" \
  --base "$BASE" \
  --head "$SYNC_BRANCH" \
  --title "$COMMIT_TITLE" \
  --body "$PR_BODY")"

PR_NUM="${PR_URL##*/}"
DIFF_URL="https://github.com/$REPO/pull/$PR_NUM/files"

echo ""
echo "PR opened: $PR_URL"
echo "Diff view: $DIFF_URL"

#!/usr/bin/env bash
# heditor installer: links the skill into your AI agents and runs the setup.
#   curl -fsSL https://raw.githubusercontent.com/pycodebr/heditor/main/install.sh | bash
#   bash install.sh [--agent claude|codex|opencode|cursor|hermes|all] [--copy] [--no-setup] [--no-audio]
set -euo pipefail
REPO="https://github.com/pycodebr/heditor.git"
SRC="${HEDITOR_SRC:-$HOME/.heditor/src}"
AGENT="auto"; MODE="link"; RUN_SETUP=1; SETUP_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --copy) MODE="copy"; shift ;;
    --no-setup) RUN_SETUP=0; shift ;;
    --no-audio) SETUP_ARGS+=(--no-audio); shift ;;
    *) echo "unknown option: $1"; exit 2 ;;
  esac
done
say() { printf '\033[1;33m[heditor]\033[0m %s\n' "$*"; }

# get the source (this checkout, or clone/update ~/.heditor/src)
HERE=""
if [[ -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; fi
if [[ -n "$HERE" && -f "$HERE/skills/heditor/SKILL.md" ]]; then SRC="$HERE"
elif [[ -d "$SRC/.git" ]]; then git -C "$SRC" pull --ff-only -q
else command -v git >/dev/null || { say "git is required"; exit 1; }; git clone -q --depth 1 "$REPO" "$SRC"; fi
SKILL="$SRC/skills/heditor"
say "source: $SKILL"

# plain case functions instead of associative arrays: macOS ships bash 3.2
skill_dir_for() {
  case "$1" in
    claude) echo "$HOME/.claude/skills" ;;
    codex) echo "$HOME/.agents/skills" ;;
    opencode) echo "$HOME/.config/opencode/skills" ;;
    cursor) echo "$HOME/.cursor/skills" ;;
    hermes) echo "$HOME/.hermes/skills/creative" ;;
    *) echo "" ;;
  esac
}
marker_for() {
  case "$1" in
    claude) echo "$HOME/.claude" ;;
    codex) echo "$HOME/.codex" ;;
    opencode) echo "$HOME/.config/opencode" ;;
    cursor) echo "$HOME/.cursor" ;;
    hermes) echo "$HOME/.hermes" ;;
  esac
}
targets=()
case "$AGENT" in
  all) targets=(claude codex opencode cursor hermes) ;;
  auto) for a in claude codex opencode cursor hermes; do [[ -d "$(marker_for "$a")" ]] && targets+=("$a"); done
        [[ ${#targets[@]} -gt 0 ]] || targets=(codex) ;;
  *) targets=("$AGENT") ;;
esac
for a in "${targets[@]}"; do
  d="$(skill_dir_for "$a")"; [[ -n "$d" ]] || { say "unknown agent $a"; continue; }
  mkdir -p "$d"; rm -rf "$d/heditor"
  if [[ "$MODE" == "copy" ]]; then cp -R "$SKILL" "$d/heditor"; else ln -s "$SKILL" "$d/heditor"; fi
  say "installed for $a -> $d/heditor"
done
say "other agents: npx skills add pycodebr/heditor -g"
if [[ $RUN_SETUP -eq 1 ]]; then bash "$SKILL/scripts/setup.sh" ${SETUP_ARGS[@]+"${SETUP_ARGS[@]}"}; fi
say "done. Edit ~/.heditor/brand.json, restart your agent and ask: \"edit this video in creative mode\"."

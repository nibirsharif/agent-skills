#!/usr/bin/env bash
# Install (symlink) every skill in ./skills into agent skills directories.
#
# Default targets:
#   ~/.agents/skills   shared location for agents that read it
#   ~/.claude/skills   Claude Code does not scan ~/.agents/skills, so it needs its own links
#
# Usage:
#   ./setup.sh                      install into the default targets
#   ./setup.sh --target DIR         install into DIR (repeatable; replaces the defaults)
#   ./setup.sh --uninstall [...]    remove the symlinks this repo created
#
# Symlinks mean edits in this repo take effect immediately. Installing also removes links
# to skills that were renamed or deleted here. Existing entries that were not created by
# this repo are never overwritten or removed.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$REPO_DIR/skills"
DEFAULT_TARGETS=("$HOME/.agents/skills" "$HOME/.claude/skills")

targets=()
uninstall=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      [[ $# -ge 2 ]] || { echo "error: --target needs a directory" >&2; exit 2; }
      targets+=("$2"); shift 2 ;;
    --uninstall) uninstall=1; shift ;;
    -h|--help) awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "error: unknown argument: $1" >&2; exit 2 ;;
  esac
done

[[ ${#targets[@]} -gt 0 ]] || targets=("${DEFAULT_TARGETS[@]}")

for target in "${targets[@]}"; do
  target="${target/#\~/$HOME}"
  echo "==> $target"

  if [[ ! -d "$target" ]]; then
    if [[ $uninstall -eq 1 ]]; then
      echo "    not found, skipping"
      continue
    fi
    mkdir -p "$target"
  fi

  # Links into this repo: remove all of them on uninstall, otherwise only those whose
  # skill no longer exists.
  for link in "$target"/*; do
    [[ -L "$link" ]] || continue
    dest="$(readlink "$link")"
    [[ "$dest" == "$SKILLS_DIR/"* ]] || continue
    if [[ $uninstall -eq 1 ]]; then
      rm "$link"; echo "    removed  $(basename "$link")"
    elif [[ ! -f "$dest/SKILL.md" ]]; then
      rm "$link"; echo "    removed  $(basename "$link") (no longer in this repo)"
    fi
  done
  [[ $uninstall -eq 0 ]] || continue

  for skill in "$SKILLS_DIR"/*/; do
    [[ -f "$skill/SKILL.md" ]] || continue
    skill="${skill%/}"
    name="$(basename "$skill")"
    link="$target/$name"

    if [[ -L "$link" && "$(readlink "$link")" == "$skill" ]]; then
      echo "    ok       $name (already linked)"
    elif [[ -e "$link" || -L "$link" ]]; then
      echo "    skipped  $name (exists and was not created by this repo)" >&2
    else
      ln -s "$skill" "$link"; echo "    linked   $name"
    fi
  done
done

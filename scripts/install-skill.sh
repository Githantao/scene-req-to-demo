#!/usr/bin/env bash
# install-skill.sh — Install scene-req-to-demo to all compatible agent directories
# Usage: ./scripts/install-skill.sh [--source DIR] [--force]
#   --source DIR  Custom source directory (default: auto-detect)
#   --force       Overwrite existing installations

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

SKILL_NAME="scene-req-to-demo"
SOURCE=""
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source) SOURCE="$2"; shift 2 ;;
    --force)  FORCE=true; shift ;;
    *) echo "Unknown option: $1"; echo "Usage: $0 [--source DIR] [--force]"; exit 1 ;;
  esac
done

# Auto-detect source
if [[ -z "$SOURCE" ]]; then
  if [[ -f "$HOME/.agents/skills/$SKILL_NAME/SKILL.md" ]]; then
    SOURCE="$HOME/.agents/skills/$SKILL_NAME"
  elif [[ -f "$PROJECT_DIR/.agents/skills/$SKILL_NAME/SKILL.md" ]]; then
    SOURCE="$PROJECT_DIR/.agents/skills/$SKILL_NAME"
  elif [[ -d "$PROJECT_DIR/skills/$SKILL_NAME" ]]; then
    SOURCE="$PROJECT_DIR/skills/$SKILL_NAME"
  else
    echo "Error: Cannot auto-detect skill source."
    echo "  Tried: ~/.agents/skills/$SKILL_NAME"
    echo "  Tried: $PROJECT_DIR/.agents/skills/$SKILL_NAME"
    echo "  Tried: $PROJECT_DIR/skills/$SKILL_NAME"
    echo "  Use --source DIR to specify manually."
    exit 1
  fi
fi

if [[ ! -f "$SOURCE/SKILL.md" ]]; then
  echo "Error: Source does not contain SKILL.md: $SOURCE"
  exit 1
fi

echo "Source: $SOURCE"
echo ""

# Target directories (compatible agent skill locations)
TARGETS=(
  "$HOME/.agents/skills/$SKILL_NAME"
  "$HOME/.config/opencode/skills/$SKILL_NAME"
)

# Primary target is the first one — copy files there
PRIMARY="${TARGETS[0]}"

# Install primary (copy)
if [[ -e "$PRIMARY" && "$FORCE" == "false" && "$SOURCE" != "$PRIMARY" ]]; then
  echo "Primary already exists: $PRIMARY"
  echo "  Use --force to overwrite, or remove it first."
else
  if [[ "$SOURCE" != "$PRIMARY" ]]; then
    echo "Installing primary: $PRIMARY"
    rm -rf "$PRIMARY"
    mkdir -p "$(dirname "$PRIMARY")"
    cp -r "$SOURCE" "$PRIMARY"
    echo "  -> copied"
  else
    echo "Primary is source (already installed): $PRIMARY"
  fi
fi

# Install secondary targets (symlink to primary)
for target in "${TARGETS[@]:1}"; do
  if [[ -e "$target" || -L "$target" ]]; then
    if [[ "$FORCE" == "true" ]]; then
      rm -rf "$target"
    else
      echo "Exists (skip): $target  (use --force to overwrite)"
      continue
    fi
  fi
  mkdir -p "$(dirname "$target")"
  ln -s "$PRIMARY" "$target"
  echo "Symlink: $target -> $PRIMARY"
done

echo ""
echo "Verification:"

# Verify
ALL_OK=true
for target in "${TARGETS[@]}"; do
  if [[ -f "$target/SKILL.md" ]]; then
    count=$(ls -1 "$target/assets/" 2>/dev/null | wc -l | tr -d ' ')
    echo "  OK  $target  (assets: $count files)"
  else
    echo "  MISS  $target"
    ALL_OK=false
  fi
done

echo ""
if [[ "$ALL_OK" == "true" ]]; then
  echo "Install complete. All targets verified."
else
  echo "Install incomplete. Some targets are missing."
  exit 1
fi

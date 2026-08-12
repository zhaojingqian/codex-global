#!/usr/bin/env bash
set -euo pipefail

readonly expected_remote="https://github.com/zhaojingqian/codex-global.git"
source_root="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
target_input="${CODEX_HOME:-${HOME}/.codex}"

if [[ -z "$target_input" || "$target_input" == "/" || "$target_input" == "$HOME" ]]; then
  echo "Refusing unsafe CODEX_HOME target: $target_input" >&2
  exit 2
fi

if [[ ! -d "$source_root/.git" ]]; then
  echo "Run this script from a Git clone of $expected_remote." >&2
  exit 2
fi

actual_remote="$(git -C "$source_root" remote get-url origin)"
if [[ "$actual_remote" != "$expected_remote" ]]; then
  echo "Unexpected source remote: $actual_remote" >&2
  echo "Expected: $expected_remote" >&2
  exit 2
fi

mkdir -p -- "$target_input"
target_root="$(CDPATH= cd -- "$target_input" && pwd -P)"

if [[ "$source_root" == "$target_root" ]]; then
  echo "This clone is already CODEX_HOME; no bootstrap is needed."
  exit 0
fi

if [[ -e "$target_root/.git" || -L "$target_root/.git" ]]; then
  echo "Refusing to replace existing Git metadata at $target_root/.git" >&2
  exit 2
fi

conflict_count=0
tracked_count=0
while IFS= read -r -d '' relative_path; do
  tracked_count=$((tracked_count + 1))
  source_path="$source_root/$relative_path"
  target_path="$target_root/$relative_path"

  if [[ -e "$target_path" || -L "$target_path" ]]; then
    if [[ ! -f "$target_path" ]] || ! cmp -s -- "$source_path" "$target_path"; then
      echo "Conflict: $target_path" >&2
      conflict_count=$((conflict_count + 1))
    fi
  fi
done < <(git -C "$source_root" ls-files -z)

if (( conflict_count > 0 )); then
  echo "Stopped before installation: $conflict_count conflicting path(s)." >&2
  exit 3
fi

# The source is a clean clone of the exact repository. Copying its Git metadata
# makes the existing CODEX_HOME the worktree without touching ignored live state.
cp -R -- "$source_root/.git" "$target_root/.git"

copied_count=0
while IFS= read -r -d '' relative_path; do
  source_path="$source_root/$relative_path"
  target_path="$target_root/$relative_path"

  if [[ ! -e "$target_path" && ! -L "$target_path" ]]; then
    mkdir -p -- "$(dirname -- "$target_path")"
    cp -p -- "$source_path" "$target_path"
    copied_count=$((copied_count + 1))
  fi
done < <(git -C "$source_root" ls-files -z)

if [[ -n "$(git -C "$target_root" status --short)" ]]; then
  echo "Bootstrap completed but the portable worktree is not clean:" >&2
  git -C "$target_root" status --short >&2
  exit 4
fi

echo "Installed $tracked_count tracked paths into $target_root ($copied_count copied)."
echo "Restart Codex to load the global guidance and skills."

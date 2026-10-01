#!/usr/bin/env bash
file=$(jq -r '.tool_input.file_path // .tool_response.filePath // .file_path // empty') || exit 2
[[ "$file" == *.dart ]] || exit 0
[[ "$file" == /* ]] || file="$PWD/$file"
[[ -f "$file" ]] || exit 0

root=${file%/*}
while [[ -n "$root" && ! -f "$root/.fvmrc" ]]; do
  root=${root%/*}
done

dart=dart
if [[ -n "$root" ]]; then
  version=$(jq -r '.flutter // empty' "$root/.fvmrc")
  dart="${FVM_CACHE_PATH:-$HOME/fvm}/versions/$version/bin/dart"
  if [[ -z "$version" || ! -x "$dart" ]]; then
    echo "dart format skipped: $root/.fvmrc pins Flutter '$version'," \
      "no SDK at $dart; install it: fvm install $version" >&2
    exit 2
  fi
fi

"$dart" format "$file" >/dev/null || exit 2

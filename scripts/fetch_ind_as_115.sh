#!/usr/bin/env bash
# Downloads the Ind AS 115 source documents listed in knowledge/ind-as-115/sources.tsv
# into knowledge/ind-as-115/raw/ and extracts plain text into knowledge/ind-as-115/text/.
# The documents are ICAI copyright, so they are fetched on demand rather than committed.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
kb="$root/knowledge/ind-as-115"
mkdir -p "$kb/raw" "$kb/text"
ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"

grep -v '^#' "$kb/sources.tsv" | while IFS=$'\t' read -r id file url _desc; do
  [ -z "$id" ] && continue
  out="$kb/raw/$file"
  if [ ! -s "$out" ]; then
    echo "fetching $id"
    curl -fsSL -A "$ua" --retry 3 --max-time 300 -o "$out.part" "$url"
    if ! head -c 5 "$out.part" | grep -q '%PDF'; then
      echo "error: $url did not return a PDF" >&2
      rm -f "$out.part"
      exit 1
    fi
    mv "$out.part" "$out"
  fi
  if command -v pdftotext >/dev/null; then
    pdftotext -layout "$out" "$kb/text/${file%.pdf}.txt"
  fi
done

echo "done: $(ls "$kb/raw" | wc -l) documents in $kb/raw"

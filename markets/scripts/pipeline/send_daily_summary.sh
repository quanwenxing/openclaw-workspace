#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/username/.openclaw/workspace"
DATE_JST="${1:-$(TZ=Asia/Tokyo date +%F)}"
SUMMARY="$ROOT/markets/runs/${DATE_JST}-summary.txt"
CHANNEL_ID="1473508792929882142"

if [[ ! -f "$SUMMARY" ]]; then
  echo "summary_not_found: $SUMMARY" >&2
  exit 1
fi

BODY="$(cat "$SUMMARY")"

openclaw message send \
  --channel discord \
  --target "$CHANNEL_ID" \
  --message "$BODY"

echo "sent_summary: $SUMMARY"

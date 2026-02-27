#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: $0 <session-dir>"
  exit 1
fi

session_dir="$1"
if [ ! -d "$session_dir" ]; then
  echo "Not found: $session_dir"
  exit 1
fi

echo "Session: $session_dir"
echo "Move deliverables manually to: projects/ docs/ research/"
echo "Archive leftovers to: archive/"
echo "(Safety-first: this script performs no destructive action yet.)"

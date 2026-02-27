#!/usr/bin/env bash
set -euo pipefail

if [ "${1:-}" = "" ]; then
  echo "Usage: $0 <topic>"
  exit 1
fi

topic="$1"
date_str="$(date +%F)"
dir="tmp/sessions/${date_str}_${topic}"

mkdir -p "$dir"
echo "$dir"

#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/username/.openclaw/workspace"
DATE_JST="$(TZ=Asia/Tokyo date +%F)"

X_BEARER_TOKEN="$(security find-generic-password -a "$USER" -s X_BEARER_TOKEN -w)" \
python3 "$ROOT/markets/scripts/collector/collect_x_posts.py" --root "$ROOT"

python3 "$ROOT/markets/scripts/pipeline/process_daily_run.py" --root "$ROOT" --date "$DATE_JST"
python3 "$ROOT/markets/scripts/pipeline/promote_strategy_candidates.py" --root "$ROOT"
python3 "$ROOT/markets/scripts/pipeline/update_kpi_metrics.py" --root "$ROOT" --date "$DATE_JST"

if [[ "${SKIP_SEND:-0}" != "1" ]]; then
  "$ROOT/markets/scripts/pipeline/send_daily_summary.sh" "$DATE_JST"
fi

echo "DONE: daily pipeline complete (${DATE_JST})"

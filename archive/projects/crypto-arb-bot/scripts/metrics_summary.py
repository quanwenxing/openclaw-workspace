#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def main():
    decisions = read_jsonl(ROOT / "reports" / "logs" / "decisions.jsonl")
    orders = read_jsonl(ROOT / "reports" / "logs" / "orders.jsonl")

    decision_count = len(decisions)
    reject_count = sum(1 for d in decisions if not d.get("exec"))
    net_total = sum(float(d.get("net", 0.0)) for d in decisions)

    fills = [o for o in orders if o.get("status") in {"filled", "partial"}]
    filled_qty = sum(float(o.get("filled_size", 0.0)) for o in fills)
    req_qty = sum(float(o.get("requested_size", 0.0)) for o in orders) or 1.0
    fill_ratio = filled_qty / req_qty

    print("metrics_summary")
    print(f"decisions={decision_count}")
    print(f"rejects={reject_count}")
    print(f"reject_ratio={reject_count / decision_count if decision_count else 0:.4f}")
    print(f"fill_ratio={fill_ratio:.4f}")
    print(f"pnl_estimate={net_total:.6f}")
    print("latency_note=decision_ts-recv_ts logged per entry; aggregate latency TODO")


if __name__ == "__main__":
    main()

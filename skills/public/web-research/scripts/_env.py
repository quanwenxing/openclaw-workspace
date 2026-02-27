#!/usr/bin/env python3
"""Tiny .env loader (no external deps).

Why:
- In OpenClaw runs, scripts are often executed without `source .env`.
- We want scripts to be usable out-of-the-box from the workspace.

Behavior:
- If KEY already exists in os.environ, keep it.
- Otherwise, try to load from `${WORKSPACE}/.env` (best-effort).

This is intentionally minimal and only supports:
  KEY=value
  KEY="value"
  KEY='value'
Comments (# ...) and blank lines are ignored.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _parse_env_line(line: str) -> Optional[tuple[str, str]]:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "=" not in line:
        return None
    k, v = line.split("=", 1)
    k = k.strip()
    v = v.strip()
    if not k:
        return None
    # Strip surrounding quotes
    if (len(v) >= 2) and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        v = v[1:-1]
    return k, v


def load_workspace_dotenv(workspace: Optional[str] = None) -> None:
    """Load .env from the OpenClaw workspace if present."""
    if workspace is None:
        # Default workspace is 3 levels up from this file: skills/public/web-research/scripts
        # scripts -> web-research -> public -> skills -> workspace
        workspace = str(Path(__file__).resolve().parents[4])
    env_path = Path(workspace) / ".env"
    if not env_path.exists():
        return
    try:
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            parsed = _parse_env_line(raw)
            if not parsed:
                continue
            k, v = parsed
            os.environ.setdefault(k, v)
    except Exception:
        # best-effort only
        return


def require_env(key: str) -> str:
    """Ensure key exists in environment; attempt to load workspace .env first."""
    if not os.environ.get(key):
        load_workspace_dotenv()
    v = os.environ.get(key)
    if not v:
        raise SystemExit(
            f"Missing env var: {key}. Put it in workspace .env or export it before running."
        )
    return v

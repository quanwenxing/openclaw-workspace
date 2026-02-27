from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import yaml


def _resolve_env(value):
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {k: _resolve_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env(v) for v in value]
    return value


@dataclass
class BotConfig:
    raw: dict

    @property
    def paper_mode(self) -> bool:
        return bool(self.raw.get("runtime", {}).get("paper_mode", True))

    @property
    def live_enabled(self) -> bool:
        return bool(self.raw.get("runtime", {}).get("live_enabled", False))


def load_config(path: str | Path) -> BotConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return BotConfig(raw=_resolve_env(data))

from __future__ import annotations

import os
import ccxt


def _env_name(exchange: str, field: str) -> str:
    return f"{exchange.upper()}_{field}"


def make_exchange(name: str, api_key: str | None = None, secret: str | None = None, password: str | None = None):
    cls = getattr(ccxt, name)
    kwargs = {"enableRateLimit": True}

    api_key = api_key or os.getenv(_env_name(name, "API_KEY"))
    secret = secret or os.getenv(_env_name(name, "SECRET"))
    password = password or os.getenv(_env_name(name, "PASSWORD"))

    if api_key and secret:
        kwargs.update({"apiKey": api_key, "secret": secret})
    if password:
        kwargs.update({"password": password})
    return cls(kwargs)

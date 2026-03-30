"""Чтение/запись списка путей в cookie: Base64(JSON) без проблемных кавычек в заголовке."""

import base64
import json

_PREFIX = "v2:"


def parse_visited_pages(raw: str | None) -> list[str]:
    if not raw:
        return []
    raw = raw.strip()
    # Старый формат: JSON в открытом виде
    if raw.startswith("["):
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [str(x) for x in data if x is not None]
        except json.JSONDecodeError:
            pass
        return []
    # Новый формат: v2:<base64 url-safe UTF-8 JSON>
    if raw.startswith(_PREFIX):
        try:
            b64 = raw[len(_PREFIX) :]
            pad = (-len(b64)) % 4
            if pad:
                b64 += "=" * pad
            payload = base64.urlsafe_b64decode(b64.encode("ascii")).decode("utf-8")
            data = json.loads(payload)
            if isinstance(data, list):
                return [str(x) for x in data if x is not None]
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return []
        return []
    return []


def encode_visited_pages(pages: list[str]) -> str:
    payload = json.dumps(pages, ensure_ascii=False, separators=(",", ":"))
    b64 = base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii").rstrip("=")
    return f"{_PREFIX}{b64}"

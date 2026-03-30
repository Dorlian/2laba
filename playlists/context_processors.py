import re

from .cookie_visited import parse_visited_pages
from .data import UI


def _label_for_path(path: str, t: dict) -> str:
    path = str(path)
    p = (path or "/").rstrip("/") or "/"
    if p == "/":
        return t["nav_home"]
    if p.startswith("/catalog"):
        return t["nav_catalog"]
    if p.startswith("/create"):
        return t["nav_create"]
    if p.startswith("/mine"):
        return t["nav_mine"]
    m = re.match(r"^/playlist/([^/]+)", p)
    if m:
        return f'{t["visited_playlist"]} · {m.group(1)}'
    return path


def user_preferences(request):
    theme = request.COOKIES.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"
    lang = request.COOKIES.get("ui_lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"
    visited_raw = request.COOKIES.get("visited_pages", "")
    visited = parse_visited_pages(visited_raw)
    t = UI[lang]
    visited_items = [
        {"href": str(raw), "label": _label_for_path(raw, t)}
        for raw in visited[:8]
    ]
    return {
        "theme": theme,
        "ui_lang": lang,
        "t": t,
        "visited_pages": visited_items,
    }

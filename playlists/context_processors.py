import json

from .data import UI


def user_preferences(request):
    theme = request.COOKIES.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"
    lang = request.COOKIES.get("ui_lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"
    visited_raw = request.COOKIES.get("visited_pages", "[]")
    try:
        visited = json.loads(visited_raw)
        if not isinstance(visited, list):
            visited = []
    except json.JSONDecodeError:
        visited = []
    return {
        "theme": theme,
        "ui_lang": lang,
        "t": UI[lang],
        "visited_pages": visited[:8],
    }

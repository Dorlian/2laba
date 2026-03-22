import json

from django.utils.deprecation import MiddlewareMixin


class LastVisitedPagesMiddleware(MiddlewareMixin):
    """Сохраняет последние посещённые пути в cookie `visited_pages` (JSON-массив)."""

    MAX_PAGES = 8
    SKIP_PREFIXES = ("/static/", "/admin/", "/favicon", "/preferences")

    def process_response(self, request, response):
        if response.status_code >= 400:
            return response
        path = request.path
        if any(path.startswith(p) for p in self.SKIP_PREFIXES):
            return response
        if request.method != "GET":
            return response
        try:
            raw = request.COOKIES.get("visited_pages", "[]")
            pages = json.loads(raw)
            if not isinstance(pages, list):
                pages = []
        except json.JSONDecodeError:
            pages = []
        label = path if path else "/"
        if label in pages:
            pages.remove(label)
        pages.insert(0, label)
        pages = pages[: self.MAX_PAGES]
        encoded = json.dumps(pages, ensure_ascii=False)
        response.set_cookie(
            "visited_pages",
            encoded,
            max_age=60 * 60 * 24 * 90,
            samesite="Lax",
        )
        return response

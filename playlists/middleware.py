from django.utils.deprecation import MiddlewareMixin

from .cookie_visited import encode_visited_pages, parse_visited_pages


class LastVisitedPagesMiddleware(MiddlewareMixin):
    """Сохраняет последние посещённые пути в cookie `visited_pages`."""

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
        raw = request.COOKIES.get("visited_pages", "")
        pages = parse_visited_pages(raw)
        label = path if path else "/"
        if label in pages:
            pages.remove(label)
        pages.insert(0, label)
        pages = pages[: self.MAX_PAGES]
        encoded = encode_visited_pages(pages)
        response.set_cookie(
            "visited_pages",
            encoded,
            max_age=60 * 60 * 24 * 90,
            samesite="Lax",
            path="/",
        )
        return response

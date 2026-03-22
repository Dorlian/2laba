import uuid

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .data import GENRES, TRACKS, TRACK_BY_ID, UI
from .forms import PlaylistForm


def _session_playlists(request):
    return request.session.setdefault("user_playlists", [])


def index(request):
    return render(request, "playlists/index.html", {})


def catalog(request):
    return render(
        request,
        "playlists/catalog.html",
        {"tracks": TRACKS, "genres": GENRES},
    )


@require_http_methods(["GET", "POST"])
def create_playlist(request):
    lang = request.COOKIES.get("ui_lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"
    ui = UI[lang]
    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            pl_id = str(uuid.uuid4())[:8]
            track_ids = form.cleaned_data["track_ids"]
            entry = {
                "id": pl_id,
                "name": form.cleaned_data["name"].strip(),
                "description": (form.cleaned_data.get("description") or "").strip(),
                "track_ids": track_ids,
            }
            playlists = _session_playlists(request)
            playlists.append(entry)
            request.session.modified = True
            return HttpResponseRedirect(reverse("playlists:detail", args=[pl_id]))
    else:
        form = PlaylistForm()
    return render(
        request,
        "playlists/create.html",
        {
            "form": form,
            "name_placeholder": ui["create_name"],
            "desc_placeholder": ui["create_desc"],
        },
    )


def my_playlists(request):
    playlists = list(reversed(_session_playlists(request)))
    enriched = []
    for p in playlists:
        tracks = [TRACK_BY_ID[tid] for tid in p["track_ids"] if tid in TRACK_BY_ID]
        enriched.append({**p, "tracks": tracks})
    return render(
        request,
        "playlists/mine.html",
        {"playlists": enriched},
    )


def playlist_detail(request, playlist_id):
    for p in _session_playlists(request):
        if p["id"] == playlist_id:
            tracks = [TRACK_BY_ID[tid] for tid in p["track_ids"] if tid in TRACK_BY_ID]
            return render(
                request,
                "playlists/detail.html",
                {"playlist": p, "tracks": tracks},
            )
    raise Http404("Плейлист не найден")


@require_http_methods(["POST"])
def set_preferences(request):
    """Тема и язык интерфейса сохраняются в cookies."""
    next_url = request.POST.get("next") or reverse("playlists:index")
    if not next_url.startswith("/"):
        next_url = reverse("playlists:index")
    theme = request.POST.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"
    lang = request.POST.get("ui_lang", "ru")
    if lang not in ("ru", "en"):
        lang = "ru"
    response = HttpResponseRedirect(next_url)
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365, samesite="Lax")
    response.set_cookie("ui_lang", lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response

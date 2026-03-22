from django.urls import path

from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.index, name="index"),
    path("catalog/", views.catalog, name="catalog"),
    path("create/", views.create_playlist, name="create"),
    path("mine/", views.my_playlists, name="mine"),
    path("playlist/<str:playlist_id>/", views.playlist_detail, name="detail"),
    path("preferences/", views.set_preferences, name="preferences"),
]

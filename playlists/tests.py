import json

from django.test import Client, TestCase
from django.urls import reverse


class PagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_ok(self):
        r = self.client.get(reverse("playlists:index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Playlist Hub")

    def test_catalog_ok(self):
        r = self.client.get(reverse("playlists:catalog"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Midnight Drive")

    def test_create_get_ok(self):
        r = self.client.get(reverse("playlists:create"))
        self.assertEqual(r.status_code, 200)

    def test_create_post_redirects(self):
        url = reverse("playlists:create")
        r = self.client.post(
            url,
            {
                "name": "Test PL",
                "description": "demo",
                "track_ids": ["t1", "t2"],
            },
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r["Location"].startswith("/playlist/"))

    def test_preferences_sets_cookies(self):
        r = self.client.post(
            reverse("playlists:preferences"),
            {"theme": "dark", "ui_lang": "en", "next": "/"},
            follow=False,
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.cookies["theme"].value, "dark")
        self.assertEqual(r.cookies["ui_lang"].value, "en")

    def test_visited_cookie_middleware(self):
        self.client.get(reverse("playlists:index"))
        r = self.client.get(reverse("playlists:catalog"))
        self.assertEqual(r.status_code, 200)
        raw = r.cookies.get("visited_pages")
        self.assertIsNotNone(raw)
        pages = json.loads(raw.value)
        self.assertIsInstance(pages, list)
        self.assertIn("/catalog/", pages)

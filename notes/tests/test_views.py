from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from notes.models import Note, Source, Topic


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class NoteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("ana", password="pw-for-tests-123")
        cls.topic = Topic.objects.create(name="Birds", slug="birds")

    def test_list_shows_published_only(self):
        Note.objects.create(title="Visible", body="x", author=self.user, topic=self.topic, published=True)
        Note.objects.create(title="Draft", body="y", author=self.user, topic=self.topic)
        response = self.client.get(reverse("notes:list"))
        self.assertContains(response, "Visible")
        self.assertNotContains(response, "Draft")

    def test_detail_renders_markdown(self):
        note = Note.objects.create(
            title="Herons", body="Seen **three** today", author=self.user, topic=self.topic, published=True
        )
        response = self.client.get(note.get_absolute_url())
        self.assertContains(response, "<strong>three</strong>", html=True)

    def test_source_create_lowercases_domain(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("notes:source_create"), {"title": "Audubon", "domain": "Audubon.ORG"}
        )
        self.assertRedirects(response, reverse("notes:sources"))
        self.assertTrue(Source.objects.filter(domain="audubon.org").exists())

    def test_theme_cookie(self):
        response = self.client.post(reverse("notes:theme"), {"theme": "dark"})
        self.assertEqual(response.cookies["fieldnotes_theme"].value, "dark")


class CacheTableTests(TestCase):
    def test_createcachetable_runs(self):
        call_command("createcachetable", verbosity=0)

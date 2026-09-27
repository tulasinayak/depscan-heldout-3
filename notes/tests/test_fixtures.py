from pathlib import Path

import yaml
from django.contrib.auth import get_user_model
from django.test import TestCase

from notes.models import Note, Topic

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "demo.yaml"


def load_demo_data():
    with FIXTURE.open(encoding="utf-8") as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    user, _ = get_user_model().objects.get_or_create(username=data["author"])
    for entry in data["topics"]:
        topic = Topic.objects.create(name=entry["name"], slug=entry["slug"])
        for note in entry.get("notes", []):
            Note.objects.create(topic=topic, author=user, published=True, **note)


class DemoDataTests(TestCase):
    def test_demo_data_loads(self):
        load_demo_data()
        self.assertEqual(Topic.objects.count(), 2)
        self.assertEqual(Note.objects.count(), 3)
        self.assertTrue(all(n.slug for n in Note.objects.all()))

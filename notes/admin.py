from django.contrib import admin

from .models import Note, Source, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ["domain", "title", "added"]
    search_fields = ["domain", "title"]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title", "topic", "author", "published", "created"]
    list_filter = ["published", "topic"]
    search_fields = ["title", "body"]
    raw_id_fields = ["author"]

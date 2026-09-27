from django.urls import path

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="list"),
    path("new/", views.note_create, name="create"),
    path("preview/", views.note_preview, name="preview"),
    path("sources/", views.source_list, name="sources"),
    path("sources/new/", views.source_create, name="source_create"),
    path("theme/", views.set_theme, name="theme"),
    path("n/<slug:slug>/", views.note_detail, name="detail"),
]

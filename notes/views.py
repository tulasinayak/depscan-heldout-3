from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .context_processors import THEMES
from .forms import NoteForm, PreviewForm, SearchForm, SourceForm
from .models import Note, Source, Topic
from .rendering import excerpt, render_markdown


def note_list(request):
    form = SearchForm(request.GET or None)
    notes = Note.objects.filter(published=True).select_related("topic", "author")
    if form.is_valid():
        query = form.cleaned_data.get("q")
        if query:
            notes = notes.filter(Q(title__icontains=query) | Q(body__icontains=query))
        topic = form.cleaned_data.get("topic")
        if topic:
            notes = notes.filter(topic__slug=topic)
    page = Paginator(notes, settings.NOTES_PER_PAGE).get_page(request.GET.get("page"))
    items = [(note, excerpt(note.body)) for note in page]
    context = {"form": form, "page": page, "items": items, "topics": Topic.objects.all()}
    return render(request, "notes/note_list.html", context)


def note_detail(request, slug):
    note = get_object_or_404(
        Note.objects.select_related("topic", "author", "source"), slug=slug, published=True
    )
    return render(request, "notes/note_detail.html", {"note": note, "body_html": render_markdown(note.body)})


@login_required
def note_create(request):
    form = NoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.author = request.user
        note.save()
        messages.success(request, "Note saved.")
        return redirect(note if note.published else "notes:list")
    return render(request, "notes/note_form.html", {"form": form})


@login_required
@require_POST
def note_preview(request):
    form = PreviewForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)
    return JsonResponse({"html": render_markdown(form.cleaned_data["body"])})


@login_required
def source_create(request):
    form = SourceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        source = form.save()
        messages.success(request, f"Added {source.domain}.")
        return redirect("notes:sources")
    return render(request, "notes/source_form.html", {"form": form})


def source_list(request):
    sources = Source.objects.all()
    return render(request, "notes/source_list.html", {"sources": sources})


@require_POST
def set_theme(request):
    choice = request.POST.get("theme", "light")
    response = redirect(request.POST.get("next") or "notes:list")
    if choice in THEMES:
        response.set_cookie(settings.THEME_COOKIE, choice, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response

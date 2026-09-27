# Fieldnotes

A small Django site where a group of members post short natural-history notes written in Markdown.
Visitors can browse and search published notes by topic; signed-in members can write notes, preview
the rendered Markdown, and register the websites they cite as sources.

## Layout

- `fieldnotes/` - project settings, URLs and WSGI entry point
- `notes/` - the app: models, forms, views, Markdown rendering, templates, admin
- `notes/tests/` - test suite (`python manage.py test`)

## Running locally

```
python -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
python manage.py migrate
python manage.py createcachetable
python manage.py createsuperuser
python manage.py runserver
```

Pages are cached site-wide for five minutes through the database cache backend.
Production runs under gunicorn on Python 3.12: `gunicorn fieldnotes.wsgi`.

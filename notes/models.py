from django.conf import settings
from django.core.validators import DomainNameValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Topic(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Source(models.Model):
    title = models.CharField(max_length=120)
    domain = models.CharField(max_length=253, unique=True, validators=[DomainNameValidator()])
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["domain"]

    def __str__(self):
        return self.domain

    @property
    def homepage(self):
        return f"https://{self.domain}/"


class Note(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="notes")
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:170] or "note"
            candidate, n = base, 2
            while Note.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{n}"
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("notes:detail", args=[self.slug])

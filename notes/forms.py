from django import forms

from .models import Note, Source


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "topic", "source", "body", "published"]
        widgets = {"body": forms.Textarea(attrs={"rows": 16})}


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ["title", "domain"]

    def clean_domain(self):
        return self.cleaned_data["domain"].lower()


class SearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)
    topic = forms.SlugField(required=False)


class PreviewForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, max_length=50000)

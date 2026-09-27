from django.conf import settings

THEMES = ("light", "dark")


def theme(request):
    value = request.COOKIES.get(settings.THEME_COOKIE, "light")
    return {"theme": value if value in THEMES else "light"}

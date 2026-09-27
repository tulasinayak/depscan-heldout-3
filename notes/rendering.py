import bleach
import markdown
from bleach.callbacks import nofollow

MARKDOWN_EXTENSIONS = ["fenced_code", "tables", "sane_lists"]

ALLOWED_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "code", "em", "h2", "h3", "h4", "hr",
    "i", "li", "ol", "p", "pre", "strong", "table", "tbody", "td", "th", "thead", "tr", "ul",
}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "abbr": ["title"],
    "code": ["class"],
    "th": ["align"],
    "td": ["align"],
}
ALLOWED_PROTOCOLS = {"http", "https", "mailto"}


def render_markdown(text):
    html = markdown.markdown(text, extensions=MARKDOWN_EXTENSIONS, output_format="html")
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return bleach.linkify(cleaned, callbacks=[nofollow])


def excerpt(text, length=240):
    plain = bleach.clean(markdown.markdown(text), tags=set(), strip=True)
    plain = " ".join(plain.split())
    if len(plain) <= length:
        return plain
    return plain[: length - 1].rsplit(" ", 1)[0] + "…"

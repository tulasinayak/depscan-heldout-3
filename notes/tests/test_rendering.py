from django.test import SimpleTestCase

from notes.rendering import excerpt, render_markdown


class RenderMarkdownTests(SimpleTestCase):
    def test_headings_and_lists(self):
        html = render_markdown("## Title\n\n- one\n- two\n")
        self.assertIn("<h2>Title</h2>", html)
        self.assertIn("<li>one</li>", html)

    def test_script_tags_are_removed(self):
        html = render_markdown("hello <script>alert(1)</script>")
        self.assertNotIn("<script>", html)

    def test_links_get_nofollow(self):
        html = render_markdown("[docs](https://example.org/docs)")
        self.assertIn('rel="nofollow"', html)

    def test_excerpt_is_plain_text(self):
        text = "**bold** " + "word " * 100
        result = excerpt(text, length=40)
        self.assertNotIn("<", result)
        self.assertLessEqual(len(result), 40)

# depscan-heldout-3 answer key

Django 6.0 site (`fieldnotes`) with per-site caching, Markdown notes sanitised by bleach, and a
dev-only PyYAML used by the test suite. OSV returns 8 distinct advisories across all pins
(`requirements.txt` + `requirements-dev.txt`); all 8 are labelled in `expected.yaml`.
3 likely_affected, 5 likely_not_affected.

| advisory | package | expected | why |
|---|---|---|---|
| CVE-2026-48588 | django 6.0.6 | uncertain (was likely_affected) (reachable_via_framework) | Site-wide `UpdateCacheMiddleware` is enabled (`fieldnotes/settings.py:21`); every page renders `{% csrf_token %}` so responses set a cookie and vary on Cookie; visitors with the unrelated theme cookie defeat the old "request has no cookies" check, so such responses get stored in the shared DB cache. Uncertain because the cached response is keyed on the full Cookie header, so another client only receives it when sending an identical Cookie header, which limits real exposure. |
| CVE-2026-53878 | django 6.0.6 | uncertain (was likely_not_affected) (safe_arguments) | `DomainNameValidator` on `Source.domain` (`notes/models.py:21`) is only fed through `SourceForm`/admin ModelForms, whose `CharField` strips the trailing newline (the case Django says is unaffected), and the domain is only rendered into HTML, never a header. Uncertain because forms.CharField strips only leading/trailing whitespace rather than all newlines, so the not-affected call rests on the trigger being a trailing newline plus the value never reaching a header. |
| CVE-2026-53877 | django 6.0.6 | likely_not_affected (framework_dependency_unused_api) | GDALRaster lives in `django.contrib.gis`; GeoDjango is not installed/imported, DB is SQLite. |
| CVE-2026-15830 | django 6.0.6 | likely_not_affected (framework_dependency_unused_api) | GEOSGeometry / GeometryField recursion; no GeoDjango usage at all. |
| CVE-2025-69534 | markdown 3.7 | likely_affected (reachable_untrusted_input) | `render_markdown()` (`notes/rendering.py:22`) parses member note bodies and arbitrary text POSTed to `/preview/`; malformed `<![` raises an uncaught error on Python < 3.13 and the project runs on 3.12. |
| GHSA-8rfp-98v4-mmr6 | bleach 6.2.0 | uncertain (was likely_affected) (reachable_untrusted_input) | `bleach.clean` is called on user HTML with `a` allowed and `href` allowed (`notes/rendering.py:8-12,23`), exactly the advisory's precondition. Practical browser impact is limited, but the allowlist contract is broken. Uncertain because the advisory itself says browsers do not execute these Unicode-obfuscated URIs, so the precondition is met but practical impact is doubtful. |
| GHSA-gj48-438w-jh9v | bleach 6.2.0 | likely_not_affected (safe_arguments) | Only exploitable when `formaction` is an allowed attribute; the allowlist has neither `formaction` nor `button`/`input`. |
| CVE-2020-14343 | pyyaml 5.3.1 (dev) | likely_not_affected (test_only) | The only `yaml.load(..., Loader=yaml.FullLoader)` is in `notes/tests/test_fixtures.py:14`, reading the repo's own fixture; PyYAML is a dev-only requirement never imported by the app. |

Notes
- `expected_sites` lists every import/usage line of the labelled packages, including test files.
- Pins with no OSV advisories: asgiref 3.12.1, gunicorn 26.2.0, sqlparse 0.6.0, webencodings 0.5.1.
- PyYAML 5.3.1 has no Python 3.12 wheel; it builds from sdist (pure-Python fallback) with pip's setuptools shim.

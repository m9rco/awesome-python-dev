"""Validate the generated site's crawlable HTML, metadata, sitemap, and local links."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

DEFAULT_BASE_URL = "https://m9rco.github.io/awesome-python-dev"


class Page(HTMLParser):
    """Collect only semantic information needed to audit a static HTML page."""

    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.titles: list[str] = []
        self.meta: dict[str, list[str]] = {}
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.ids: list[str] = []
        self.links: list[str] = []
        self.json_ld: list[str] = []
        self.h1_count = 0
        self.text: list[str] = []
        self._title: list[str] | None = None
        self._json: list[str] | None = None
        self.feed(source)
        self.close()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang") or ""
        if tag == "title":
            self._title = []
        if tag == "h1":
            self.h1_count += 1
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(values.get("content") or "")
        if tag == "link":
            rel = (values.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(values.get("href") or "")
            if "alternate" in rel and values.get("hreflang"):
                self.alternates[values["hreflang"]] = values.get("href") or ""
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute])
        if tag == "script" and values.get("type") == "application/ld+json":
            self._json = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._title is not None:
            self.titles.append("".join(self._title).strip())
            self._title = None
        if tag == "script" and self._json is not None:
            self.json_ld.append("".join(self._json))
            self._json = None

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._title is not None:
            self._title.append(data)
        if self._json is not None:
            self._json.append(data)


def page_url(base_url: str, relative: Path) -> str:
    """Map generated index files to their public directory URL."""
    path = relative.as_posix()
    if path == "index.html":
        path = ""
    elif path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return base_url.rstrip("/") + "/" + path


def check_site(site: Path, base_url: str = DEFAULT_BASE_URL) -> list[str]:
    """Return actionable errors; a valid generated site returns an empty list."""
    site = site.resolve()
    base_url = base_url.rstrip("/")
    errors: list[str] = []
    parsed_base = urlsplit(base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        return ["base URL must be an absolute HTTP(S) URL"]
    if not site.is_dir():
        return [f"site directory does not exist: {site}"]

    pages: dict[Path, Page] = {}
    urls: dict[str, Page] = {}
    expected: set[str] = set()
    titles: dict[str, str] = {}
    descriptions: dict[str, str] = {}
    for path in sorted(site.rglob("*.html")):
        relative = path.relative_to(site)
        name = relative.as_posix()
        source = path.read_text(encoding="utf-8")
        page = Page(source)
        pages[path] = page
        url = page_url(base_url, relative)
        urls[url] = page
        if not page.lang:
            errors.append(f"{name}: missing HTML language")
        if page.h1_count != 1:
            errors.append(f"{name}: expected one h1, found {page.h1_count}")
        for duplicate, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{name}: duplicate element ID {duplicate!r}")
        if re.search(r"\{\{\s*[A-Za-z_]|\{%|\$\{(?:base_url|title|description)\}", source):
            errors.append(f"{name}: unresolved template placeholder")
        noindex = "noindex" in ",".join(page.meta.get("robots", [])).lower()
        if name == "404.html":
            if not noindex:
                errors.append("404.html: error page must declare noindex")
            continue
        if noindex:
            errors.append(f"{name}: content page unexpectedly declares noindex")
        expected.add(url)
        if page.canonicals != [url]:
            errors.append(f"{name}: canonical must be exactly {url}")
        if len(page.titles) != 1 or not page.titles[0]:
            errors.append(f"{name}: expected one nonempty title")
        else:
            title = page.titles[0]
            if title in titles:
                errors.append(f"{name}: title duplicates {titles[title]}")
            titles[title] = name
        description = page.meta.get("description", [])
        if len(description) != 1 or not description[0].strip():
            errors.append(f"{name}: expected one nonempty meta description")
        else:
            if description[0] in descriptions:
                errors.append(f"{name}: description duplicates {descriptions[description[0]]}")
            descriptions[description[0]] = name
        required_meta = (
            "og:title", "og:description", "og:type", "og:url", "og:image",
            "twitter:card", "twitter:title", "twitter:description", "twitter:image",
        )
        for key in required_meta:
            if len(page.meta.get(key, [])) != 1 or not page.meta[key][0].strip():
                errors.append(f"{name}: expected one nonempty {key}")
        if page.meta.get("og:url") != [url]:
            errors.append(f"{name}: Open Graph URL must match canonical")
        if page.meta.get("og:image:width") != ["1200"]:
            errors.append(f"{name}: Open Graph image width must be 1200")
        if page.meta.get("og:image:height") != ["630"]:
            errors.append(f"{name}: Open Graph image height must be 630")
        for key in ("og:image", "twitter:image"):
            for image in page.meta.get(key, []):
                parsed = urlsplit(image)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    errors.append(f"{name}: {key} must be absolute")
                page.links.append(image)
        if not page.json_ld:
            errors.append(f"{name}: missing JSON-LD structured data")
        for data in page.json_ld:
            try:
                structured = json.loads(data)
                if not isinstance(structured, dict) or not structured.get("@context"):
                    errors.append(f"{name}: JSON-LD must declare @context")
            except json.JSONDecodeError as exc:
                errors.append(f"{name}: malformed JSON-LD: {exc.msg}")

    if site / "index.html" not in pages:
        errors.append("missing homepage index.html")
    if site / "404.html" not in pages:
        errors.append("missing custom 404.html")

    for path, page in pages.items():
        name = path.relative_to(site).as_posix()
        current_url = page_url(base_url, path.relative_to(site))
        for href in page.links:
            target = urlsplit(urljoin(current_url, href))
            if target.scheme not in {"http", "https"} or target.netloc != parsed_base.netloc:
                continue
            prefix = parsed_base.path.rstrip("/") + "/"
            if not unquote(target.path).startswith(prefix):
                errors.append(f"{name}: local link escapes site base path: {href}")
                continue
            local = (site / unquote(target.path)[len(prefix):]).resolve()
            if not local.is_relative_to(site):
                errors.append(f"{name}: local link escapes site directory: {href}")
                continue
            if local.is_dir():
                local /= "index.html"
            if not local.is_file():
                errors.append(f"{name}: broken local link: {href}")
            elif target.fragment and local in pages:
                if unquote(target.fragment) not in pages[local].ids:
                    errors.append(f"{name}: missing fragment target: {href}")
        for language, href in page.alternates.items():
            target_page = urls.get(href)
            if target_page is None:
                errors.append(f"{name}: hreflang target is not an indexable page: {href}")
            elif target_page.alternates != page.alternates:
                errors.append(f"{name}: hreflang links must be reciprocal: {language}")

    sitemap = site / "sitemap.xml"
    try:
        tree = ElementTree.parse(sitemap)
        locations = [node.text or "" for node in tree.findall("{*}url/{*}loc")]
        if len(locations) != len(set(locations)):
            errors.append("sitemap.xml: duplicate URLs")
        for missing in sorted(expected - set(locations)):
            errors.append(f"sitemap.xml: missing canonical URL: {missing}")
        for unexpected in sorted(set(locations) - expected):
            errors.append(f"sitemap.xml: noncanonical or missing page: {unexpected}")
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f"sitemap.xml: cannot read valid sitemap: {exc}")
    robots = site / "robots.txt"
    if not robots.is_file() or f"Sitemap: {base_url}/sitemap.xml" not in robots.read_text():
        errors.append("robots.txt: missing absolute sitemap URL")
    if not (site / ".nojekyll").is_file():
        errors.append("missing .nojekyll marker")
    social = site / "assets/social-card.png"
    if not social.is_file():
        errors.append("missing social sharing image")
    else:
        data = social.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
            errors.append("social-card.png: not a valid PNG")
        elif (int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")) != (1200, 630):
            errors.append("social-card.png: expected 1200 × 630 pixels")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    arguments = parser.parse_args()
    errors = check_site(arguments.site, arguments.base_url)
    if errors:
        for error in errors[:60]:
            print(f"ERROR: {error}")
        if len(errors) > 60:
            print(f"... and {len(errors) - 60} more errors")
        return 1
    count = len(list(arguments.site.rglob("*.html")))
    print(f"Website validated: {count} HTML pages; metadata, sitemap, and local links passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

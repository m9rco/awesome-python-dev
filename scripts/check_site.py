"""Validate the generated site's crawlable HTML, metadata, sitemap, and local links."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

from awesome_python_dev.catalog import load_catalog

DEFAULT_BASE_URL = "https://m9rco.github.io/awesome-python-dev"
FILESYSTEM_PATH = re.compile(r"file://|(?<![\w:/])/(?:Users|home|private|tmp)/|[A-Za-z]:\\Users\\")


class Page(HTMLParser):
    """Collect only semantic information needed to audit a static HTML page."""

    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.titles: list[str] = []
        self.meta: dict[str, list[str]] = {}
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.markdown_alternates: list[str] = []
        self.describedby: list[str] = []
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
            if "alternate" in rel and values.get("type") == "text/markdown":
                self.markdown_alternates.append(values.get("href") or "")
            if "describedby" in rel:
                self.describedby.append(values.get("href") or "")
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


def check_discovery(site: Path, base_url: str) -> list[str]:
    """Audit the machine-readable routes using the same catalog as the CLI."""
    errors: list[str] = []
    parsed_base = urlsplit(base_url)
    prefix = parsed_base.path.rstrip("/") + "/"
    llms = site / "llms.txt"
    if not llms.is_file():
        errors.append("missing llms.txt discovery index")
    documents = sorted(site.rglob("*.md")) + ([llms] if llms.is_file() else [])
    for document in documents:
        name = document.relative_to(site).as_posix()
        text = document.read_text(encoding="utf-8")
        if not text.startswith("# "):
            errors.append(f"{name}: Markdown discovery document must begin with a project/page heading")
        if str(site) in text or FILESYSTEM_PATH.search(text):
            errors.append(f"{name}: discovery output contains an absolute filesystem path")
        links = re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", text)
        if document == llms and not links:
            errors.append("llms.txt: discovery index has no links")
        for href in links:
            target = urlsplit(href)
            if target.scheme not in {"http", "https"} or not target.netloc:
                errors.append(f"{name}: discovery link must be absolute HTTP(S): {href}")
                continue
            if target.netloc != parsed_base.netloc:
                continue
            decoded = unquote(target.path)
            if not decoded.startswith(prefix):
                errors.append(f"{name}: discovery link escapes site base path: {href}")
                continue
            local = (site / decoded[len(prefix):]).resolve()
            if not local.is_relative_to(site):
                errors.append(f"{name}: discovery link escapes site directory: {href}")
            elif not local.is_file() and not (local / "index.html").is_file():
                errors.append(f"{name}: broken discovery link: {href}")

    try:
        catalog_text = (site / "catalog.json").read_text(encoding="utf-8")
        if str(site) in catalog_text or FILESYSTEM_PATH.search(catalog_text):
            errors.append("catalog.json: discovery output contains an absolute filesystem path")
        exported = json.loads(catalog_text)
        canonical = load_catalog()
        tools = {tool["id"]: tool for tool in exported["tools"]}
        expected = {tool["id"]: tool for tool in canonical["tools"]}
        if len(tools) != len(exported["tools"]) or tools.keys() != expected.keys():
            errors.append("catalog.json: tool IDs must match the CLI catalog without duplicates")
        if exported["profiles"] != canonical["profiles"]:
            errors.append("catalog.json: profiles must match the CLI catalog")
        discovery = exported["discovery"]
        if discovery.get("catalog_scope") != "source-snapshot" or not discovery.get("release_note"):
            errors.append("catalog.json: source snapshot must be distinguished from published runtime releases")
        if discovery.get("llms_url") != base_url + "/llms.txt":
            errors.append("catalog.json: llms_url must use the site base URL")
        if discovery.get("guide_url") != base_url + "/agents/index.md":
            errors.append("catalog.json: guide_url must use the site base URL")
        for tool_id, tool in tools.items():
            original = expected.get(tool_id)
            if original is None:
                continue
            if tool.get("kind") != original["kind"] or tool.get("installable") is not bool(original.get("install")):
                errors.append(f"catalog.json: kind/installability differs from CLI for {tool_id}")
            if tool.get("url") != f"{base_url}/tools/{tool_id}/" or tool.get("markdown_url") != f"{base_url}/tools/{tool_id}/index.md":
                errors.append(f"catalog.json: tool URLs must use canonical site paths for {tool_id}")
            preview = tool.get("preview_command", "")
            if original.get("install"):
                if f"--tools {tool_id}" not in preview or "--dry-run" not in preview:
                    errors.append(f"catalog.json: missing preview command for {tool_id}")
            elif preview:
                errors.append(f"catalog.json: reference-only tool {tool_id} must not have an install command")
        original_export = {key: value for key, value in exported.items() if key != "discovery"}
        derived = {"installable", "url", "markdown_url", "preview_command"}
        original_export["tools"] = [
            {key: value for key, value in tool.items() if key not in derived}
            for tool in exported["tools"]
        ]
        if original_export != canonical:
            errors.append("catalog.json: exported source data must exactly match the CLI catalog")
        payload = json.dumps(original_export, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        if discovery.get("catalog_sha256") != hashlib.sha256(payload.encode("utf-8")).hexdigest():
            errors.append("catalog.json: source catalog checksum does not match exported data")
        for document in documents:
            text = document.read_text(encoding="utf-8")
            for ids in re.findall(r"--tools\s+([a-z0-9][a-z0-9,-]*)", text):
                for tool_id in ids.split(","):
                    if tool_id not in expected or not expected[tool_id].get("install"):
                        errors.append(f"{document.relative_to(site)}: invalid installable tool in command: {tool_id}")
            for profile in re.findall(r"--profile\s+([a-z0-9][a-z0-9-]*)", text):
                if profile not in canonical["profiles"]:
                    errors.append(f"{document.relative_to(site)}: unknown profile in command: {profile}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f"catalog.json: cannot validate discovery export: {exc}")
    return errors


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
        markdown_url = base_url + "/" + relative.with_suffix(".md").as_posix()
        if page.markdown_alternates != [markdown_url]:
            errors.append(f"{name}: Markdown alternate must be exactly {markdown_url}")
        if page.describedby != [base_url + "/llms.txt"]:
            errors.append(f"{name}: describedby must point to the site's llms.txt")
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
    errors.extend(check_discovery(site, base_url))
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

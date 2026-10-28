"""Publish bounded Markdown navigation and a catalog with explicit provenance."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from copy import deepcopy
from html import escape
from html.parser import HTMLParser

from .config import REPOSITORY, ROOT

CATALOG_PATH = 'src/awesome_python_dev/data/catalog.json'
AGENT_IDS = ['codex', 'claude', 'cursor', 'vscode', 'opencode']
SNAPSHOT_NOTE = (
    'This website describes the repository catalog snapshot, which may contain unreleased '
    'entries. It is not a promise that every entry exists in the currently published package. '
    'Check `uvx awesome-python-dev list --json` for the catalog available in your installed '
    'runtime. GitHub stars and review dates are recorded snapshots, not live rankings.'
)


def source_metadata(catalog: dict, version: str) -> dict:
    """Use a commit permalink only when the input exactly matches that Git blob."""
    revision = None
    build_revision = None
    try:
        build_revision = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL,
            timeout=5,
        ).strip()
        if not re.fullmatch(r'[0-9a-f]{40,64}', build_revision):
            build_revision = None
        if build_revision:
            committed = subprocess.check_output(
                ['git', 'show', f'{build_revision}:{CATALOG_PATH}'], cwd=ROOT,
                stderr=subprocess.DEVNULL, timeout=5,
            )
            if json.loads(committed) == catalog:
                revision = build_revision
    except (OSError, ValueError, subprocess.SubprocessError):
        pass
    canonical = json.dumps(catalog, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return {
        'schema_version': 1,
        'catalog_scope': 'source-snapshot',
        'repository': REPOSITORY,
        'source_revision': revision,
        'build_revision': build_revision,
        'working_tree': revision is None,
        'source_url': f'{REPOSITORY}/blob/{revision or "main"}/{CATALOG_PATH}',
        'catalog_sha256': hashlib.sha256(canonical.encode('utf-8')).hexdigest(),
        'digest_format': 'UTF-8 JSON; ensure_ascii=false, sort_keys=true, separators=(comma,colon)',
        'runtime_version': version,
        'release_note': SNAPSHOT_NOTE,
        'supported_agents': AGENT_IDS,
    }


class Markdown(HTMLParser):
    """Small converter for the site's controlled, semantic HTML templates."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []
        self.pre = False
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'button', 'script', 'style', 'select', 'label'}:
            self.skip += 1
        if self.skip:
            return
        if tag in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.parts.append('\n\n' + '#' * min(int(tag[1]) + 1, 6) + ' ')
        elif tag in {'p', 'section', 'article', 'div', 'dl', 'ul', 'ol'}:
            self.parts.append('\n\n')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'dt':
            self.parts.append('\n- ')
        elif tag == 'dd':
            self.parts.append(': ')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'pre':
            self.pre = True
            self.parts.append('\n\n```sh\n')
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag == 'a':
            self.links.append(attrs.get('href', ''))
            self.parts.append('[')
        elif tag in {'strong', 'b'}:
            self.parts.append('**')

    def handle_endtag(self, tag):
        if tag in {'button', 'script', 'style', 'select', 'label'} and self.skip:
            self.skip -= 1
            return
        if self.skip:
            return
        if tag == 'pre':
            self.parts.append('\n```\n\n')
            self.pre = False
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag == 'a' and self.links:
            self.parts.append(f']({self.links.pop()}) ')
        elif tag in {'strong', 'b'}:
            self.parts.append('**')
        elif tag in {'p', 'section', 'article', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
            self.parts.append('\n\n')

    def handle_data(self, data):
        if not self.skip:
            # HTML-escaped catalog descriptions must not turn into executable raw HTML.
            self.parts.append(escape(data, quote=False))

    def render(self, source: str) -> str:
        self.feed(source)
        return re.sub(r'\n{3,}', '\n\n', ''.join(self.parts)).strip()


def write_markdown(site, path: str, title: str, description: str, body: str) -> None:
    target = site.output / path / 'index.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    source = site.discovery
    content = (
        f'# {escape(title, quote=False)}\n\n> {escape(description, quote=False)}\n\n'
        f'[HTML page]({site.url(path)}) · [Agent guide]({site.url("agents/index.md")}) · '
        f'[Discovery index]({site.url("llms.txt")})\n\n'
        f'{SNAPSHOT_NOTE}\n\n'
        f'Catalog reviewed: {site.catalog["reviewed_at"]}. '
        f'[Catalog source]({source["source_url"]}).\n\n'
        + Markdown().render(body) + '\n'
    )
    target.write_text(content, encoding='utf-8')


def write_discovery(site) -> None:
    exported = deepcopy(site.catalog)
    exported['discovery'] = {
        **site.discovery,
        'llms_url': site.url('llms.txt'),
        'guide_url': site.url('agents/index.md'),
    }
    for tool in exported['tools']:
        tool['installable'] = bool(tool.get('install'))
        tool['url'] = site.url(f'tools/{tool["id"]}/')
        tool['markdown_url'] = site.url(f'tools/{tool["id"]}/index.md')
        if tool['installable']:
            tool['preview_command'] = site.command(f'--tools {tool["id"]} --dry-run')
    (site.output / 'catalog.json').write_text(
        json.dumps(exported, ensure_ascii=False, indent=2) + '\n', encoding='utf-8',
    )
    lines = [
        '# Awesome Python Dev',
        '',
        '> Curated AI development skills, rules, MCP servers and LSP tools, with a CLI '
        'installer for Codex, Claude Code, Cursor, VS Code Copilot and OpenCode.',
        '',
        'Use the JSON catalog to filter resources and the linked Markdown pages for '
        'installation requirements, upstream evidence and review dates. Only entries '
        'with an install recipe are installable; reference entries point to upstream guides.',
        '',
        SNAPSHOT_NOTE,
        '',
        '## Start here',
        f'- [Agent discovery guide]({site.url("agents/index.md")}): discovery commands, '
        'preview-first setup and source/version boundaries.',
        f'- [Install and configure]({site.url("getting-started/index.md")}): prerequisites, '
        'agent selection, npm and uvx commands.',
        f'- [Catalog overview]({site.url("index.md")}): searchable resource descriptions and profiles.',
        f'- [中文介绍]({site.url("zh/index.md")}): Chinese overview and setup entry point.',
        f'- [Structured catalog]({site.url("catalog.json")}): complete JSON source snapshot '
        'with installability, provenance and Markdown URLs.',
        '',
        '## Resource categories',
    ]
    from .config import KINDS
    for kind, (label, _, _) in KINDS.items():
        lines.append(f'- [{label}]({site.url(f"categories/{kind}/index.md")}): '
                     'resource descriptions and links to individual setup pages.')
    lines.extend(['', '## Profiles'])
    for name in site.catalog['profiles']:
        lines.append(f'- [{name}]({site.url(f"profiles/{name}/index.md")}): '
                     'included resources and resolved rule dependencies.')
    lines.extend([
        '', '## Project and trust',
        f'- [Repository]({REPOSITORY}): source code, releases and contribution instructions.',
        f'- [Security model]({REPOSITORY}/blob/main/SECURITY.md): upstream trust, '
        'integrity checks and project configuration boundaries.',
        f'- [Source evidence]({REPOSITORY}/blob/main/docs/RESEARCH.md): curated project research.',
        '',
    ])
    (site.output / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8')

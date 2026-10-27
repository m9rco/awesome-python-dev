#!/usr/bin/env python3
"""Build the catalog website from the same validated data used by the CLI."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import tomllib
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

from awesome_python_dev.catalog import load_catalog, select_tools

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://m9rco.github.io/awesome-python-dev"
REPOSITORY = "https://github.com/m9rco/awesome-python-dev"
AGENTS = ("Codex", "Claude Code", "Cursor", "VS Code Copilot", "OpenCode")
KINDS = {
    "skill": (
        "Skills",
        "Reusable workflows for your coding agent",
        "Debugging, testing, security reviews and framework workflows, packaged as "
        "project-local skills with reviewed upstream sources.",
    ),
    "rules": (
        "Rules",
        "Engineering standards that travel with your project",
        "Common and language-specific rules for security, coding style, testing and "
        "delivery, adapted to each coding agent’s native instruction format.",
    ),
    "mcp": (
        "MCP servers",
        "Connect your agent to tools and context",
        "Pinned MCP recipes for library documentation, browser automation and web content. "
        "Your agent starts these servers after configuration.",
    ),
    "lsp": (
        "LSP tools",
        "Give your agent a view of your code",
        "Serena connects agents to language-server code intelligence through MCP. "
        "Native language servers are also collected here as upstream references.",
    ),
    "reference": (
        "References",
        "Explore the wider developer ecosystem",
        "Established projects for specifications, security, Python tooling and "
        "agent development. These entries link to upstream installation guides.",
    ),
}
PROFILES = {
    "starter": (
        "Starter",
        "Start with debugging, test-driven development, verification, "
        "library documentation and common engineering rules.",
        "基础工具包",
        "从调试、测试驱动开发、交付验证和通用工程规范开始。",
    ),
    "python": (
        "Python",
        "Equip Python projects with testing, packaging, language patterns, "
        "documentation and Python engineering rules.",
        "Python 开发",
        "组合测试、打包、语言最佳实践、文档工具和 Python 规范。",
    ),
    "web": (
        "Web",
        "Combine frontend workflows, browser automation, TypeScript rules "
        "and a test-first development loop.",
        "Web 开发",
        "组合前端实践、浏览器自动化、TypeScript 规则和测试工作流。",
    ),
    "engineering": (
        "Engineering",
        "Shape APIs, plan database migrations and deployment, "
        "and verify changes with reusable engineering workflows.",
        "工程实践",
        "覆盖 API 设计、数据库迁移、部署、调试与交付验证。",
    ),
    "security": (
        "Security",
        "Add security review guidance and common rules for implementation, testing and delivery.",
        "安全审查",
        "为实现、测试与交付加入安全审查流程和通用规范。",
    ),
    "django": (
        "Django",
        "Use Django architecture and security patterns alongside Python "
        "testing, rules and library documentation.",
        "Django",
        "整合 Django 架构、安全实践、Python 测试与工程规范。",
    ),
    "fastapi": (
        "FastAPI",
        "Bring FastAPI rules, API design, security review and Python "
        "testing into one project toolkit.",
        "FastAPI",
        "整合 FastAPI 规则、API 设计、安全审查与 Python 测试。",
    ),
    "springboot": (
        "Spring Boot",
        "Combine Java rules, Spring Boot patterns, security, API design and database migrations.",
        "Spring Boot",
        "整合 Java 规范、Spring Boot 实践、安全、API 与数据迁移。",
    ),
    "typescript": (
        "TypeScript",
        "Equip frontend and backend projects with TypeScript "
        "rules, Next.js guidance and security reviews.",
        "TypeScript",
        "覆盖前后端规范、Next.js 实践与安全审查。",
    ),
    "golang": (
        "Go",
        "Apply Go rules and language patterns with API design, security "
        "reviews and library documentation.",
        "Go",
        "组合 Go 规则、语言实践、API 设计、安全与文档工具。",
    ),
    "lsp": (
        "Code intelligence",
        "Configure Serena’s MCP-to-LSP bridge for symbol-aware navigation and code intelligence.",
        "代码智能",
        "通过 Serena 的 MCP-to-LSP 桥接接入符号与代码智能工具。",
    ),
}


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def json_script(value: object) -> str:
    # A catalog description must never be able to close its JSON-LD script element.
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def normalize_base_url(value: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme not in {"http", "https"}
        or not parsed.netloc
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
        or any(part in {".", ".."} for part in parsed.path.split("/"))
        or re.search(r"[\s<>\"\\]", value)
    ):
        raise ValueError("base URL must be an absolute HTTP(S) URL without query or fragment")
    return value.rstrip("/")


class Website:
    def __init__(self, output: Path, base_url: str, catalog: dict, version: str):
        self.output = output
        self.base_url = normalize_base_url(base_url)
        self.catalog = catalog
        self.version = version
        self.pages: list[str] = []
        self.tools = catalog["tools"]
        self.by_id = {tool["id"]: tool for tool in self.tools}

    def url(self, path: str = "") -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def href(self, path: str = "") -> str:
        return escape(self.url(path))

    def command(self, selection: str) -> str:
        return (
            f"uvx --from 'git+{REPOSITORY}.git@v{self.version}' "
            f"apd init --agents codex,claude {selection}"
        )

    def code(self, command: str, identifier: str = "install-command", zh: bool = False) -> str:
        label, copied, error = (
            ("复制", "已复制", "请选择并复制命令")
            if zh
            else ("Copy", "Copied", "Select and copy the command")
        )
        return f'''<div class="code-block"><pre><code id="{escape(identifier)}">{escape(command)}</code></pre>
<button class="copy-button" hidden type="button" data-copy-target="{escape(identifier)}"
 data-label="{label}" data-copied="{copied}" data-error="{error}" aria-label="{label} command">{label}</button></div>'''

    def page(
        self,
        path: str,
        title: str,
        description: str,
        body: str,
        *,
        zh: bool = False,
        collection: list[dict] | None = None,
        breadcrumbs: list[tuple[str, str]] | None = None,
        noindex: bool = False,
    ) -> None:
        lang = "zh-CN" if zh else "en"
        url = self.url(path)
        full_title = f"{title} | Awesome Python Dev"
        alternate = ""
        if path in {"", "zh/"}:
            alternate = (
                f'<link rel="alternate" hreflang="en" href="{self.href()}">\n'
                f'<link rel="alternate" hreflang="zh-CN" href="{self.href("zh/")}">\n'
                f'<link rel="alternate" hreflang="x-default" href="{self.href()}">'
            )
        graph: list[dict] = [
            {
                "@type": "WebSite",
                "@id": self.url("#website"),
                "url": self.url(),
                "name": "Awesome Python Dev",
                "inLanguage": ["en", "zh-CN"],
            },
            {
                "@type": "CollectionPage" if collection is not None else "WebPage",
                "@id": url + "#webpage",
                "url": url,
                "name": full_title,
                "description": description,
                "inLanguage": lang,
                "isPartOf": {"@id": self.url("#website")},
            },
        ]
        if collection is not None:
            graph[1]["mainEntity"] = {
                "@type": "ItemList",
                "numberOfItems": len(collection),
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": n,
                        "name": t["name"],
                        "url": self.url(f"tools/{t['id']}/"),
                    }
                    for n, t in enumerate(collection, 1)
                ],
            }
        if breadcrumbs:
            graph.append(
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": n, "name": name, "item": self.url(link)}
                        for n, (name, link) in enumerate(breadcrumbs, 1)
                    ],
                }
            )
        nav_home = "zh/" if zh else ""
        nav_catalog, nav_profiles, nav_start = (
            ("工具目录", "场景套餐", "安装指南") if zh else ("Catalog", "Profiles", "Get started")
        )
        locale_link = (
            f'<a href="{self.href()}" lang="en">English</a>'
            if zh
            else (f'<a href="{self.href("zh/")}" lang="zh-CN">中文</a>')
        )
        robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
        crumb_html = ""
        if breadcrumbs:
            crumb_html = (
                '<nav class="breadcrumbs" aria-label="Breadcrumb">'
                + " / ".join(
                    f'<a href="{self.href(link)}">{escape(name)}</a>'
                    for name, link in breadcrumbs[:-1]
                )
                + f" / <span>{escape(breadcrumbs[-1][0])}</span></nav>"
            )
        document = f'''<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(full_title)}</title><meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}"><meta name="theme-color" content="#f7f8f4">
<link rel="canonical" href="{escape(url)}">{alternate}
<meta property="og:type" content="website"><meta property="og:site_name" content="Awesome Python Dev">
<meta property="og:title" content="{escape(full_title)}"><meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{escape(url)}"><meta property="og:locale" content="{"zh_CN" if zh else "en_US"}">
<meta property="og:image" content="{self.href("assets/social-card.png")}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Awesome Python Dev — Skills, Rules, MCP and LSP">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(full_title)}">
<meta name="twitter:description" content="{escape(description)}"><meta name="twitter:image" content="{self.href("assets/social-card.png")}">
<link rel="icon" href="{self.href("assets/favicon.svg")}" type="image/svg+xml">
<link rel="sitemap" type="application/xml" href="{self.href("sitemap.xml")}">
<link rel="stylesheet" href="{self.href("assets/styles.css")}">
<script type="application/ld+json">{json_script({"@context": "https://schema.org", "@graph": graph})}</script>
<script src="{self.href("assets/site.js")}" defer></script>
</head><body>
<a class="skip-link" href="#main">{"跳转到内容" if zh else "Skip to content"}</a>
<header class="site-header"><div class="container nav">
<a class="brand" href="{self.href(nav_home)}"><span class="brand-mark" aria-hidden="true">a<span>_</span></span><span>awesome<span class="brand-suffix"> / python dev</span></span></a>
<nav class="nav-links" aria-label="{"主导航" if zh else "Main navigation"}">
<a href="{self.href("#catalog")}">{nav_catalog}</a><a href="{self.href(nav_home + "#profiles")}">{nav_profiles}</a>
<a href="{self.href("getting-started/")}">{nav_start}</a>{locale_link}
<a href="{REPOSITORY}" class="github-link">GitHub <span aria-hidden="true">↗</span></a></nav></div></header>
<main id="main" class="container">{crumb_html}{body}</main>
<footer class="site-footer"><div class="container footer-grid"><div><a class="brand" href="{self.href(nav_home)}">awesome / python dev</a>
<p>{"为 coding agent 精选的开发工具。" if zh else "A curated toolkit for the way you build."}</p>
<p class="footer-note">MIT · v{escape(self.version)} · {"目录审核于" if zh else "Catalog reviewed"} {escape(self.catalog["reviewed_at"])}</p></div>
<nav aria-label="Footer"><a href="{REPOSITORY}">GitHub ↗</a><a href="{REPOSITORY}/blob/main/CONTRIBUTING.md">{"参与贡献" if zh else "Contribute"}</a>
<a href="{REPOSITORY}/blob/main/SECURITY.md">{"安全说明" if zh else "Security"}</a><a href="{self.href("sitemap.xml")}">Sitemap</a></nav></div></footer>
</body></html>'''
        target = self.output / (path + "index.html" if not path.endswith(".html") else path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(document, encoding="utf-8")
        if not noindex:
            self.pages.append(url)

    def tool_cards(self, tools: list[dict]) -> str:
        cards = []
        for tool in tools:
            installable = bool(tool.get("install"))
            status = "Installable" if installable else "Reference"
            search = " ".join(
                str(tool.get(key, ""))
                for key in ("name", "description", "repository", "category", "id")
            )
            cards.append(f'''<article class="tool-card" data-name="{escape(search)}" data-kind="{escape(tool["kind"])}" data-installable="{str(installable).lower()}">
<div class="tool-top"><span class="tool-kind">{escape(KINDS[tool["kind"]][0])}</span><span class="tool-status {"is-installable" if installable else ""}">{status}</span></div>
<h3 class="tool-name"><a href="{self.href(f"tools/{tool['id']}/")}">{escape(tool["name"])}</a></h3>
<p class="tool-description">{escape(tool["description"])}</p>
<div class="tool-meta"><span>{escape(tool["repository"])}</span><span>{escape(tool["license"])}</span></div>
<a class="tool-link" href="{self.href(f"tools/{tool['id']}/")}">{"View setup" if installable else "Explore project"} <span aria-hidden="true">↗</span></a></article>''')
        return '<div class="tool-grid">' + "".join(cards) + "</div>"

    def profile_cards(self, zh: bool = False) -> str:
        cards = []
        for name in self.catalog["profiles"]:
            label, desc, zh_label, zh_desc = PROFILES.get(
                name,
                (
                    name.title(),
                    f"A curated {name} development toolkit.",
                    name,
                    f"{name} 开发工具套餐。",
                ),
            )
            count = len(select_tools(self.catalog, name))
            cards.append(f'''<a class="profile-card" href="{self.href(f"profiles/{name}/")}">
<span class="section-kicker">{escape(name)} / {count} {"项工具" if zh else "resources"}</span>
<h3>{escape(zh_label if zh else label)} <span aria-hidden="true">↗</span></h3>
<p>{escape(zh_desc if zh else desc)}</p></a>''')
        return '<div class="profile-grid">' + "".join(cards) + "</div>"

    def home(self, zh: bool = False) -> None:
        installable = sum(bool(t.get("install")) for t in self.tools)
        stats = [
            (len(self.tools), "精选资源" if zh else "curated resources"),
            (installable, "可安装工具" if zh else "ready to install"),
            (len(self.catalog["profiles"]), "场景套餐" if zh else "focused profiles"),
            (len(AGENTS), "coding agents" if zh else "coding agents"),
        ]
        headline = (
            "让 AI 编程助手，<br><span>带上好工具。</span>"
            if zh
            else "Your agent.<br><span>Better equipped.</span>"
        )
        intro = (
            "精选成熟的 Skills、Rules、MCP 与 LSP 工具。把安全、工程规范和框架最佳实践，"
            "一次装进你常用的 coding agent。"
            if zh
            else "Skills, rules, MCP and LSP tools from established open-source projects. "
            "One command to bring a thoughtful development toolkit to your coding agents."
        )
        body = f'''<section class="hero"><div class="eyebrow"><span class="status-dot" aria-hidden="true"></span> {"开源精选 · 为开发者而建" if zh else "OPEN SOURCE. CAREFULLY CURATED."}</div>
<div class="hero-grid"><div class="hero-copy"><h1 class="hero-title">{headline}</h1><p class="hero-description">{intro}</p>
<div class="actions"><a class="button button-primary" href="{self.href("getting-started/")}">{"开始安装" if zh else "Build your toolkit"} <span aria-hidden="true">↗</span></a>
<a class="button button-secondary" href="{self.href("#catalog")}">{"浏览工具目录" if zh else "Explore the catalog"} <span aria-hidden="true">↓</span></a></div></div>
<div class="terminal"><div class="terminal-top"><span aria-hidden="true">● ● ●</span><span>~/your-next-project</span></div>
<p class="terminal-label">{"01 / 选择工具包，开始构建" if zh else "01 / A small command. A capable toolkit."}</p>
{self.code(self.command("--profile starter"), zh=zh)}
<div class="terminal-foot"><span>{"✓ 固定上游版本" if zh else "✓ Pinned upstream sources"}</span><span>{"✓ 项目内配置" if zh else "✓ Project-local setup"}</span><span>{"✓ 支持预览与卸载" if zh else "✓ Preview & remove"}</span></div></div></div>
<div class="stats">{"".join(f'<div class="stat"><span class="stat-number">{n:02}</span><span class="stat-label">{label}</span></div>' for n, label in stats)}</div></section>
<section class="agent-strip" aria-label="Supported coding agents"><span class="section-kicker">{"适配你的工作方式" if zh else "FITS YOUR WORKFLOW"}</span>{"".join(f'<span class="agent-tag">{a}</span>' for a in AGENTS)}</section>
<section class="section" id="categories"><div class="section-heading"><div><p class="section-kicker">01 / {"探索" if zh else "DISCOVER"}</p>
<h2>{"四类能力，一个工具集合。" if zh else "A place for every part of your workflow."}</h2></div>
<p class="section-description">{"选择适合项目的工作流、规则与工具连接。每一项都保留上游来源。" if zh else "Reusable workflows. Clear standards. Connected tools. Every entry traces back to its upstream project."}</p></div><div class="category-grid">'''
        zh_kinds = {
            "skill": ("Skills / 工作流", "复用调试、测试、安全审查与框架开发流程。"),
            "rules": ("Rules / 开发规范", "将工程、安全和语言规范适配为 agent 原生规则。"),
            "mcp": ("MCP / 工具连接", "连接文档、浏览器与网页内容，提供更多开发上下文。"),
            "lsp": ("LSP / 代码智能", "通过 Serena 桥接代码智能，也可探索原生语言服务器。"),
            "reference": ("参考项目", "探索规范驱动开发、安全扫描与工具生态。"),
        }
        for kind, (label, _, desc) in KINDS.items():
            count = sum(t["kind"] == kind for t in self.tools)
            if zh:
                label, desc = zh_kinds[kind]
            body += f'''<a class="category-card" href="{self.href(f"categories/{kind}/")}"><span class="category-count">{count:02} ↗</span><h3>{label}</h3><p>{desc}</p></a>'''
        body += f"""</div></section><section class="section" id="profiles"><div class="section-heading"><div>
<p class="section-kicker">02 / {"组装" if zh else "ASSEMBLE"}</p><h2>{"从你的技术栈开始。" if zh else "Start with what you’re building."}</h2></div>
<p class="section-description">{"从 Python、Web、安全到框架专属套餐，依赖规则自动补齐。套餐详情和完整工具目录使用英文。" if zh else "Focused profiles for real projects. Required rule packs are included automatically."}</p></div>{self.profile_cards(zh)}</section>"""
        if not zh:
            body += f'''<section class="section" id="catalog"><div class="section-heading"><div><p class="section-kicker">03 / THE COLLECTION</p>
<h2>Good tools. Clear provenance.</h2></div><p class="section-description">Installable entries have a reviewed recipe. References point to upstream setup. No account or API key needed to browse.</p></div>
<div class="catalog-controls" hidden><label for="tool-search">Search the collection<input type="search" id="tool-search" placeholder="Try FastAPI, security, Python…" autocomplete="off"></label>
<label for="kind-filter">Resource type<select id="kind-filter"><option value="">All types</option>{"".join(f'<option value="{kind}">{info[0]}</option>' for kind, info in KINDS.items())}</select></label>
<label class="checkbox-label"><input type="checkbox" id="installable-only"> Installable only</label></div>
<p id="result-count" data-total="{len(self.tools)}" role="status" aria-live="polite">{len(self.tools)} resources</p>
{self.tool_cards(self.tools)}<p id="no-results" hidden>No matching tools. Try a different keyword or clear the filters.</p></section>'''
        body += f'''<section class="section prose"><p class="section-kicker">{"透明与可维护" if zh else "BUILT TO BE UNDERSTOOD"}</p><h2>{"知道安装了什么，也知道来自哪里。" if zh else "Know what goes into your project."}</h2>
<p>{"Skills 和 Rules 保留上游许可证与来源，MCP 配方固定版本。安装前可用 --dry-run 预览，安装后可用 apd doctor 检查，并通过 apd remove 卸载管理的条目。" if zh else "Skills and rules retain upstream licenses and provenance. MCP recipes pin their versions. Preview with --dry-run, inspect your setup with apd doctor, and remove managed entries with apd remove."}</p>
<a class="button button-secondary" href="{REPOSITORY}/blob/main/docs/ECC-MIGRATION.md">{"了解 ECC 迁移范围" if zh else "Read the ECC migration notes"} ↗</a></section>'''
        self.page(
            "zh/" if zh else "",
            "AI 开发工具集：Skills、Rules、MCP 与 LSP"
            if zh
            else "AI developer tools, skills, rules, MCP & LSP",
            "精选 AI 开发工具、Skills、Rules、MCP 与 LSP，覆盖安全、工程规范和框架最佳实践，一键配置到 Codex、Claude Code、Cursor 等 coding agent。"
            if zh
            else "Discover curated AI development skills, rules, MCP servers and LSP tools. Install reviewed toolkits into Codex, Claude Code, Cursor, Copilot and OpenCode.",
            body,
            zh=zh,
            collection=None if zh else self.tools,
        )

    def category(self, kind: str) -> None:
        name, heading, desc = KINDS[kind]
        tools = [t for t in self.tools if t["kind"] == kind]
        body = f"""<section class="section"><p class="eyebrow">THE COLLECTION / {len(tools)} RESOURCES</p><h1>{escape(heading)}</h1><p class="hero-description">{escape(desc)}</p>{self.tool_cards(tools)}</section>"""
        self.page(
            f"categories/{kind}/",
            f"{name} for AI coding agents",
            desc,
            body,
            collection=tools,
            breadcrumbs=[("Home", ""), (name, f"categories/{kind}/")],
        )

    def tool(self, tool: dict) -> None:
        identifier = tool["id"]
        path = f"tools/{identifier}/"
        kind = tool["kind"]
        recipe = tool.get("install")
        status = "Installable" if recipe else "Reference only"
        body = f'''<section class="section"><p class="eyebrow">{escape(KINDS[kind][0])} / {status}</p>
<h1>{escape(tool["name"])}</h1><p class="hero-description">{escape(tool["description"])}</p>
<div class="actions"><a class="button button-primary" href="{escape(tool["homepage"])}">Upstream project ↗</a><a class="button button-secondary" href="https://github.com/{escape(tool["repository"])}">View repository ↗</a></div></section>
<div class="detail-grid"><section class="detail-panel prose"><h2>{"Install into your coding agents" if recipe else "Install with the upstream project"}</h2>'''
        if recipe:
            body += self.code(self.command(f"--tools {identifier}"))
            body += (
                f"<p>Run inside the project you want to equip. This command targets Codex "
                f"and Claude Code; use <code>--agents</code> to choose other supported agents. "
                f'<a href="{self.href("getting-started/")}">Read the prerequisites and setup guide</a>.</p>'
            )
            if recipe["type"] == "mcp":
                body += (
                    "<p>The installer writes MCP configuration. Your coding agent starts the "
                    "server after reload and approval; installation does not run server tools.</p>"
                )
            if kind == "lsp":
                body += (
                    "<p>Serena uses Python 3.13 via uvx. Language-specific runtimes may also be "
                    "needed. Its project path is absolute: run init again after moving a project.</p>"
                )
            if kind == "rules":
                body += (
                    "<p>Rule packs are adapted to native agent instructions. Required common "
                    "and language packs are included automatically. Existing user instructions "
                    "outside managed sections are preserved.</p>"
                )
            dependencies = tool.get("requires", [])
            if dependencies:
                body += (
                    "<h3>Required resources</h3><ul>"
                    + "".join(
                        f'<li><a href="{self.href(f"tools/{dep}/")}">{escape(self.by_id[dep]["name"])}</a></li>'
                        for dep in dependencies
                    )
                    + "</ul>"
                )
        else:
            body += (
                f"<p>This entry is a reference. It has no <code>apd init</code> recipe in "
                f'v{escape(self.version)}. Follow the <a href="{escape(tool["homepage"])}">'
                f"upstream documentation</a> for installation and configuration.</p>"
            )
            if kind == "lsp":
                body += (
                    f"<p>A native language server is not an MCP server. To add an installable "
                    f"LSP bridge to your coding agent, explore "
                    f'<a href="{self.href("tools/serena/")}">Serena</a>.</p>'
                )
        if tool.get("notes"):
            body += f"<h2>Integration notes</h2><p>{escape(tool['notes'])}</p>"
        body += (
            '</section><aside class="detail-panel"><h2>Source & review</h2><dl class="metadata">'
        )
        for label, value in [
            ("Repository", tool["repository"]),
            ("License", tool["license"]),
            ("Category", tool["category"].replace("-", " ")),
            ("Reviewed", tool["checked_at"]),
            ("GitHub stars at review", f"{tool['stars']:,}"),
            ("Installation", status),
        ]:
            body += f"<dt>{label}</dt><dd>{escape(value)}</dd>"
        if recipe:
            pin = recipe.get("ref") or recipe.get("package")
            if pin:
                body += f"<dt>Pinned source</dt><dd><code>{escape(pin)}</code></dd>"
        body += (
            '</dl><p class="footer-note">Star counts are review snapshots, not live rankings. '
            "Upstream licenses apply to each resource.</p></aside></div>"
        )
        related_profiles = [
            name
            for name in self.catalog["profiles"]
            if any(t["id"] == identifier for t in select_tools(self.catalog, name))
        ]
        if related_profiles:
            body += (
                '<section class="section prose"><h2>Included in these profiles</h2><ul>'
                + "".join(
                    f'<li><a href="{self.href(f"profiles/{name}/")}">{escape(PROFILES.get(name, (name,))[0])}</a></li>'
                    for name in related_profiles
                )
                + "</ul></section>"
            )
        body += (
            '<section class="section prose"><h2>Review the source evidence</h2><ul>'
            + "".join(
                f'<li><a href="{escape(link)}">Upstream evidence {n} ↗</a></li>'
                for n, link in enumerate(tool.get("evidence", [tool["homepage"]]), 1)
            )
            + "</ul></section>"
        )
        self.page(
            path,
            f"{tool['name']}: {'setup' if recipe else 'reference'} & source",
            f"{tool['description']} {status} in Awesome Python Dev; review its source, license and setup.",
            body,
            breadcrumbs=[
                ("Home", ""),
                (KINDS[kind][0], f"categories/{kind}/"),
                (tool["name"], path),
            ],
        )

    def profile(self, name: str) -> None:
        label, desc, *_ = PROFILES.get(name, (name.title(), f"A curated {name} toolkit."))
        tools = select_tools(self.catalog, name)
        body = f'''<section class="section"><p class="eyebrow">PROFILE / {len(tools)} RESOURCES</p><h1>{escape(label)} toolkit</h1><p class="hero-description">{escape(desc)}</p>
{self.code(self.command(f"--profile {name}"))}<p>Run in your project directory. <a href="{self.href("getting-started/")}">Check prerequisites and agent setup</a>.</p></section>
<section class="section"><h2>What’s included</h2><p>The list includes required rule-pack dependencies, resolved by the same catalog logic as the CLI.</p>{self.tool_cards(tools)}</section>'''
        self.page(
            f"profiles/{name}/",
            f"{label} AI development toolkit",
            desc,
            body,
            collection=tools,
            breadcrumbs=[("Home", ""), (f"{label} profile", f"profiles/{name}/")],
        )

    def getting_started(self) -> None:
        maintenance = (
            "apd profiles\napd list --installable\napd doctor\n"
            "apd remove --agents codex,claude --tools serena"
        )
        body = f'''<section class="section prose"><p class="eyebrow">FROM COLLECTION TO CONFIGURATION</p><h1>Equip your coding agent.</h1>
<p class="hero-description">Choose a profile, preview the changes, and install into your project. Keep the same toolkit across your agents.</p>
<h2>1. Check your prerequisites</h2><p>Install <a href="https://docs.astral.sh/uv/getting-started/installation/">uv</a> and Git. The CLI requires Python 3.11 or newer and access to GitHub. Install your coding agent separately.</p>
<p>MCP requirements depend on your selection. The starter profile uses Context7 and needs Node.js 20.18.1 or newer with npx. Serena uses uvx with Python 3.13 and may need additional language runtimes. Skills and rules do not require a running MCP server.</p>
<h2>2. Preview the starter profile</h2><p>Open a terminal in the project you want to equip. A dry run downloads nothing and writes nothing.</p>
{self.code(self.command("--profile starter --dry-run"), "preview-command")}
<h2>3. Install your toolkit</h2>{self.code(self.command("--profile starter"))}
<p>This installs skills and rules and registers the selected MCP servers. Reload your agent and review its MCP approval prompts. Codex only loads project configuration from trusted projects.</p>
<h2>Choose your agents</h2><p>Use a comma-separated list: <code>codex,claude,cursor,vscode,opencode</code>. The command above selects Codex and Claude Code. To target every supported agent, use <code>--agents all</code>.</p>
<p>Agent-specific setup paths and constraints are documented in the <a href="{REPOSITORY}/blob/main/docs/AGENTS.md">agent compatibility guide</a>. Existing JSONC configuration must be converted to JSON before adding MCP entries. Skills-only selections avoid changing MCP configuration.</p>
<h2>Choose a framework or a single tool</h2><p>Explore the <a href="{self.href("#profiles")}">profile collection</a> for Python, FastAPI, Django, TypeScript, Go, Spring Boot and security. Install a single resource with <code>--tools</code>.</p>
{self.code(self.command("--tools serena"), "serena-command")}
<h2>Inspect and maintain your setup</h2><p>For repeat use, install the CLI once:</p>
{self.code(f"uv tool install 'git+{REPOSITORY}.git@v{self.version}'", "cli-command")}
{self.code(maintenance, "maintenance-command")}
<p>Rules and skills retain their source provenance and licenses. Managed configuration is tracked locally, and user modifications are protected. See the <a href="{REPOSITORY}/blob/main/README.md">README</a> for command options and the <a href="{REPOSITORY}/blob/main/SECURITY.md">security model</a> for trust boundaries.</p>
</section>'''
        self.page(
            "getting-started/",
            "Install AI tools into your coding agents",
            "Install Awesome Python Dev with uv, preview a toolkit, and configure skills, rules, MCP and LSP for Codex, Claude Code, Cursor, Copilot or OpenCode.",
            body,
            breadcrumbs=[("Home", ""), ("Getting started", "getting-started/")],
        )

    def build(self) -> int:
        self.home()
        self.home(zh=True)
        for kind in KINDS:
            self.category(kind)
        for tool in self.tools:
            self.tool(tool)
        for profile in self.catalog["profiles"]:
            self.profile(profile)
        self.getting_started()
        self.page(
            "404.html",
            "Page not found",
            "This page could not be found. Explore the Awesome Python Dev catalog.",
            f'<section class="section prose"><p class="eyebrow">404 / NOT FOUND</p><h1>This tool took another path.</h1><p>Browse the catalog to find the resource you need.</p><a class="button button-primary" href="{self.href()}">Back to the collection ↗</a></section>',
            noindex=True,
        )
        namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
        ET.register_namespace("", namespace)
        sitemap = ET.Element(f"{{{namespace}}}urlset")
        for url in self.pages:
            ET.SubElement(
                ET.SubElement(sitemap, f"{{{namespace}}}url"), f"{{{namespace}}}loc"
            ).text = url
        ET.ElementTree(sitemap).write(
            self.output / "sitemap.xml", encoding="utf-8", xml_declaration=True
        )
        (self.output / "robots.txt").write_text(
            f"# Effective only when served at the origin root; see docs/WEBSITE.md.\nUser-agent: *\nAllow: /\nSitemap: {self.url('sitemap.xml')}\n",
            encoding="utf-8",
        )
        (self.output / ".nojekyll").touch()
        shutil.copytree(ROOT / "site/assets", self.output / "assets", dirs_exist_ok=True)
        return len(self.pages)


def build_site(output: Path, base_url: str = DEFAULT_BASE_URL) -> int:
    base_url = normalize_base_url(base_url)
    if Path(output).is_symlink():
        raise ValueError("output must be a dedicated build directory, not a symlink")
    output = Path(output).resolve()
    # Never turn a typo in --output into deletion of a source or user directory.
    if output == ROOT or output in ROOT.parents or output.is_symlink():
        raise ValueError("output must be a dedicated build directory")
    marker = output / ".apd-generated-site"
    if output.exists() and any(output.iterdir()) and not marker.is_file():
        raise ValueError("refusing to replace a nonempty directory without a site build marker")
    catalog = load_catalog()
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "version"
    ]
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    marker.write_text("Generated by scripts/build_site.py\n", encoding="utf-8")
    return Website(output, base_url, catalog, version).build()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    count = build_site(args.output, args.base_url)
    print(f"Built {count} indexable pages + 404 into {args.output}")


if __name__ == "__main__":
    main()

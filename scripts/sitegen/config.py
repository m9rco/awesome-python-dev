"""Shared site identity, descriptions and safe serialization helpers."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
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


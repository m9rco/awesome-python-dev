"""Native project rules and a byte-preserving shared AGENTS.md activation block.

Rendering is pure: the installer owns collision checks, hashes, and writes.
Original upstream files are always returned alongside adapted native rules.
"""

from __future__ import annotations

import json
import posixpath
import re
from pathlib import PurePosixPath
from urllib.parse import quote, urlsplit

from .adapters import AGENTS

START_MARKER = b"<!-- awesome-python-dev:rules:start -->"
END_MARKER = b"<!-- awesome-python-dev:rules:end -->"
MARKER_PREFIX = b"<!-- awesome-python-dev:rules:"
DEFAULT_MAX_AGENTS_BYTES = 32 * 1024
SHARED_RULES_ROOT = ".awesome-python-dev/rules"
NATIVE_RULES_ROOTS = {
    "claude": ".claude/rules",
    "cursor": ".cursor/rules",
    "vscode": ".github/instructions",
}
_EXTENSIONS = {"claude": ".md", "cursor": ".mdc", "vscode": ".instructions.md"}

# Exact, reviewed clauses from affaan-m/ECC's selected English rule files.
# Do not turn this into a broad "agent" or "hook" rewrite: React hooks and code
# examples are ordinary rule content and must remain intact.
_ECC_REPLACEMENTS = {
    "Use **planner** agent to create implementation plan": "Create an implementation plan",
    "Use **tdd-guide** agent": "Follow a test-first development workflow",
    "Use **code-reviewer** agent immediately after writing code":
        "Review the code immediately after writing it",
    "Use **security-reviewer** agent": "Review the change for security issues",
    "- **tdd-guide** - Use PROACTIVELY for new features, enforces write-tests-first":
        "- Follow test-first development for new features",
    "2. Use parallel agents to evaluate options:":
        "2. Evaluate options across these dimensions (parallel reviews are optional):",
    "- **e2e-runner** - Playwright E2E testing specialist":
        "- Run and inspect Playwright end-to-end tests for critical flows",
    "- Use **security-reviewer** skill for comprehensive security audits":
        "- Perform a security review using the project's available checks and tools",
    "- See hooks for automatic detection":
        "- Check for production `console.log` statements with the project's lint or review workflow",
    "## Agent Support": "## Additional Workflow Guidance",
    "   - **Exa only when the first two are insufficient:** Use Exa for broader web research or discovery after GitHub search and primary docs.":
        "   - **Broader research when needed:** Use an available web research tool after GitHub search and primary docs.",
    'Note: ECC-managed installs set `"includeCoAuthoredBy": false` in `~/.claude/settings.json`, so commits carry no `Co-Authored-By` trailer by default. To keep Claude attribution, set `"includeCoAuthoredBy": true` or configure `attribution`; ECC never overwrites an explicit choice.':
        "Note: Follow this project's existing commit-attribution policy. This rules pack does not change global agent settings.",
}
_ECC_SKILL_NAMES = (
    "python-patterns", "python-testing", "django-security", "fastapi-patterns",
    "golang-patterns", "golang-testing", "java-coding-standards", "jpa-patterns",
    "springboot-patterns", "quarkus-patterns", "springboot-security", "quarkus-security",
    "security-review", "springboot-tdd", "quarkus-tdd",
)


def _relative_path(value: str) -> PurePosixPath:
    if not isinstance(value, str) or any(ord(char) < 32 for char in value):
        raise ValueError("Rule source paths must be printable relative paths")
    path = PurePosixPath(value)
    if (path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value
            or str(path) == "." or str(path) != value):
        raise ValueError(f"Unsafe rule source path: {value!r}")
    return path


def _tool_id(tool: dict) -> str:
    tool_id = tool.get("id", "")
    if not isinstance(tool_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", tool_id):
        raise ValueError("Rule packs need a lowercase, hyphenated tool ID")
    return tool_id


def rule_roots(agent_id: str, tool_id: str) -> tuple[str, ...]:
    """Allowed directory roots for this pack's manifest-owned files.

    Shared paths intentionally overlap across agents; callers must deduplicate
    equal contents and retain a shared file until its last owner is removed.
    """
    if agent_id not in AGENTS:
        raise ValueError(f"Unsupported rules agent: {agent_id}")
    _tool_id({"id": tool_id})
    roots = (f"{SHARED_RULES_ROOT}/{tool_id}",)
    if agent_id in NATIVE_RULES_ROOTS:
        roots += (f"{NATIVE_RULES_ROOTS[agent_id]}/apd-{tool_id}",)
    return roots


def rule_path_prefixes(agent_id: str, tool_id: str) -> tuple[str, ...]:
    """Directory prefixes accepted for this agent/pack's ownership manifest."""
    return tuple(root + "/" for root in rule_roots(agent_id, tool_id))


def _globs(tool: dict) -> list[str]:
    raw = tool["install"].get("globs", [])
    if isinstance(raw, str):
        # Split a comma-separated string without breaking **/*.{ts,tsx}.
        values, current, depth = [], [], 0
        for char in raw:
            if char in "{[":
                depth += 1
            elif char in "}]":
                depth -= 1
            if char == "," and depth == 0:
                values.append("".join(current).strip())
                current = []
            else:
                current.append(char)
            if depth < 0:
                raise ValueError("Unbalanced rule glob")
        if depth:
            raise ValueError("Unbalanced rule glob")
        values.append("".join(current).strip())
    elif isinstance(raw, list):
        values = raw
    else:
        raise ValueError("Rule globs must be a string or list of strings")
    if not values:
        return ["**"]
    for value in values:
        if (not isinstance(value, str) or not value or any(ord(c) < 32 for c in value)
                or "\\" in value or ":" in value or value.startswith("/")
                or ".." in PurePosixPath(value).parts):
            raise ValueError(f"Invalid rule glob: {value!r}")
    return ["**"] if any(value in {"**", "**/*"} for value in values) else list(dict.fromkeys(values))


def _sources(tool: dict, files: dict[str, bytes]) -> list[str]:
    _tool_id(tool)
    install = tool.get("install", {})
    names = install.get("files")
    if not isinstance(names, list) or not names or not all(isinstance(name, str) for name in names):
        raise ValueError("Rule packs must explicitly select install.files")
    if len({name.casefold() for name in names}) != len(names):
        raise ValueError("Duplicate or case-colliding rule source names")
    repository, ref = tool.get("repository", ""), install.get("ref", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Rules need an owner/repository source")
    if not re.fullmatch(r"[a-f0-9]{40}", ref):
        raise ValueError("Rules need a full pinned upstream commit")
    _relative_path(install.get("subdir", ""))
    for name in names:
        if _relative_path(name).suffix not in {".md", ".mdc"} or name not in files:
            raise ValueError(f"Missing Markdown rule source: {name}")
    if not isinstance(files, dict) or not all(isinstance(value, bytes) for value in files.values()):
        raise ValueError("Rule bundle files must contain bytes")
    for name in files:
        _relative_path(name)
    if len({name.casefold() for name in files}) != len(files):
        raise ValueError("Case-colliding rule bundle paths")
    if "UPSTREAM-LICENSE" not in files or "UPSTREAM.md" not in files:
        raise ValueError("Rule bundles require upstream license and attribution")
    if any(name.casefold() == "apd-adaptation.txt" for name in files):
        raise ValueError("Upstream file collides with generated APD-ADAPTATION.txt")
    _globs(tool)
    return names


def _source_url(tool: dict, name: str) -> str:
    path = posixpath.join(tool["install"]["subdir"], name)
    return f"https://github.com/{tool['repository']}/blob/{tool['install']['ref']}/{quote(path, safe='/')}"


def _body(data: bytes) -> str:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("Rules must contain UTF-8 Markdown") from exc
    if "\x00" in text or MARKER_PREFIX.decode() in text:
        raise ValueError("Rule content contains reserved markers or NUL bytes")
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
        if end is None:
            raise ValueError("Unclosed upstream rule frontmatter")
        text = "".join(lines[end + 1:])
    if not text.strip():
        raise ValueError("Rules must have a nonempty Markdown body")
    return text.strip("\r\n")


def _rewrite_links(tool: dict, name: str, text: str) -> str:
    base = posixpath.dirname(posixpath.join(tool["install"]["subdir"], name))

    def rewrite(match: re.Match) -> str:
        label, target = match.groups()
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path or parts.path.startswith("/"):
            return match.group(0)
        path = posixpath.normpath(posixpath.join(base, parts.path))
        if path == ".." or path.startswith("../"):
            raise ValueError("Relative rule reference escapes upstream repository")
        url = f"https://github.com/{tool['repository']}/blob/{tool['install']['ref']}/{quote(path, safe='/')}"
        if parts.fragment:
            url += "#" + parts.fragment
        return f"[{label}]({url})"

    # Keep examples in fenced code blocks exactly as supplied upstream.
    output, fence = [], None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            char = stripped[0]
            length = len(stripped) - len(stripped.lstrip(char))
            if fence is None:
                fence = (char, length)
            elif char == fence[0] and length >= fence[1]:
                fence = None
            output.append(line)
        elif fence is not None:
            output.append(line)
        else:
            output.append(re.sub(r"\[([^\]\n]+)\]\(([^\s)]+)\)", rewrite, line))
    return "".join(output)


def _adapted_body(tool: dict, name: str, data: bytes) -> str:
    text = _body(data)
    if tool["repository"].lower() == "affaan-m/ecc":
        for old, new in _ECC_REPLACEMENTS.items():
            text = text.replace(old, new)
        for skill in _ECC_SKILL_NAMES:
            source = (f"https://github.com/{tool['repository']}/blob/"
                      f"{tool['install']['ref']}/skills/{skill}/SKILL.md")
            text = text.replace(f"skill: `{skill}`", f"optional upstream reference [{skill}]({source})")
    return _rewrite_links(tool, name, text)


def _preamble(tool: dict, name: str) -> str:
    note = (
        "ECC-specific agent, hook, and global-settings assumptions are adapted to portable guidance; "
        "upstream skills are optional references. "
        if tool["repository"].lower() == "affaan-m/ecc" else ""
    )
    return (
        f"> Imported by awesome-python-dev from [the pinned upstream source]({_source_url(tool, name)}). "
        f"{note}This rules pack does not install subagents, hooks, commands, or global settings.\n\n"
    )


def _native_rule(agent_id: str, tool: dict, name: str, data: bytes) -> bytes:
    globs = _globs(tool)
    description = f"{tool.get('name', tool['id'])}: {name}"
    if agent_id == "claude":
        metadata = "" if globs == ["**"] else (
            "---\npaths:\n" + "".join(f"  - {json.dumps(value)}\n" for value in globs) + "---\n\n"
        )
    elif agent_id == "cursor":
        metadata = (
            f"---\ndescription: {json.dumps(description)}\n"
            f"globs: {json.dumps(','.join(globs))}\n"
            f"alwaysApply: {'true' if globs == ['**'] else 'false'}\n---\n\n"
        )
    else:
        metadata = (
            f"---\ndescription: {json.dumps(description)}\n"
            f"applyTo: {json.dumps(','.join(globs))}\n---\n\n"
        )
    return (metadata + _preamble(tool, name) + _adapted_body(tool, name, data) + "\n").encode()


def render_rules(agent_id: str, tool: dict, files: dict[str, bytes]) -> dict[str, bytes]:
    """Return originals, provenance, and agent-native active files for one pack."""
    roots = rule_roots(agent_id, _tool_id(tool))
    sources = _sources(tool, files)
    output = {f"{roots[0]}/{name}": content for name, content in files.items()}
    # Validate and adapt even on shared-AGENTS targets, so invalid Markdown fails
    # before any installer writes; build_activation uses exactly this same body.
    for name in sources:
        _adapted_body(tool, name, files[name])
    note = (
        "Original files in this directory are unchanged upstream source bytes.\n"
        "Active copies replace upstream YAML frontmatter with the selected agent's scope metadata.\n"
        "Relative Markdown links point to the pinned GitHub source, preserving references after relocation.\n"
        "Codex/OpenCode use the same adapted bodies embedded in one root AGENTS.md block.\n"
    )
    if tool["repository"].lower() == "affaan-m/ecc":
        note += (
            "ECC adaptation: named planner/reviewer/test agents become ordinary workflow steps;\n"
            "automatic hook claims become explicit lint/review checks; commit attribution follows\n"
            "existing project policy; Exa becomes an available research tool; referenced upstream\n"
            "skills are optional links. No ECC agents, hooks, commands, or global settings are installed.\n"
        )
    output[f"{roots[0]}/APD-ADAPTATION.txt"] = note.encode()
    if len(roots) == 2:
        folded = set()
        for name in sources:
            native_name = str(PurePosixPath(name).with_suffix(_EXTENSIONS[agent_id]))
            if native_name.casefold() in folded:
                raise ValueError(f"Native rule filename collision: {native_name}")
            folded.add(native_name.casefold())
            output[f"{roots[1]}/{native_name}"] = _native_rule(agent_id, tool, name, files[name])
    return output


def build_activation(packs: list[tuple[dict, dict[str, bytes]]]) -> bytes | None:
    """Build one shared AGENTS.md block, embedding each selected pack once.

    Packs remain in caller order so dependency/baseline rules can precede their
    language-specific extensions. Conflicting duplicates fail instead of winning
    by order. The caller applies the total-file byte cap with render_activation.
    """
    sections: dict[str, str] = {}
    for tool, files in packs:
        sources = _sources(tool, files)
        scope = _globs(tool)
        body = f"### {tool.get('name', tool['id'])} ({tool['id']})\n\n"
        body += (
            "Scope: project-wide coding conventions.\n\n" if scope == ["**"] else
            "Scope: apply the following guidance only to files matching "
            + ", ".join(f"`{pattern}`" for pattern in scope) + ".\n\n"
        )
        for name in sources:
            body += f"#### Source: {name}\n\n" + _preamble(tool, name)
            body += _adapted_body(tool, name, files[name]) + "\n\n"
        tool_id = tool["id"]
        if tool_id in sections and sections[tool_id] != body:
            raise ValueError(f"Conflicting rule pack copies: {tool_id}")
        sections[tool_id] = body
    if not sections:
        return None
    content = (
        "## Imported development rules\n\n"
        "These conventions apply within their stated scopes. Follow the project's specific "
        "instructions outside this managed block when they conflict with these imported defaults. "
        "Original sources and licenses are retained in `.awesome-python-dev/rules/`.\n\n"
        + "".join(sections.values())
    ).encode()
    # The block owns its leading/trailing separators, making removal lossless
    # even when the pre-existing AGENTS.md had no final newline.
    return b"\n\n" + START_MARKER + b"\n" + content + END_MARKER + b"\n"


def extract_activation(existing: bytes | None) -> bytes | None:
    """Find exactly one canonical managed block; reject broken/duplicate markers."""
    if existing is None:
        return None
    if not isinstance(existing, bytes):
        raise ValueError("AGENTS.md content must be bytes")
    if MARKER_PREFIX not in existing:
        return None
    if (existing.count(START_MARKER) != 1 or existing.count(END_MARKER) != 1
            or existing.count(MARKER_PREFIX) != 2):
        raise ValueError("AGENTS.md has malformed or duplicate managed rules markers")
    start = existing.index(START_MARKER)
    end = existing.index(END_MARKER)
    end_after = end + len(END_MARKER)
    if (start < 2 or existing[start - 2:start] != b"\n\n" or end < start
            or existing[start + len(START_MARKER):start + len(START_MARKER) + 1] != b"\n"
            or existing[end - 1:end] != b"\n" or existing[end_after:end_after + 1] != b"\n"):
        raise ValueError("AGENTS.md managed rules markers or separators were modified")
    return existing[start - 2:end_after + 1]


def render_activation(
    existing: bytes | None,
    desired: bytes | None,
    expected_owned: bytes | None = None,
    *,
    max_bytes: int | None = DEFAULT_MAX_AGENTS_BYTES,
) -> bytes | None:
    """Replace/remove only the exact owned block, preserving all other bytes.

    With no prior ownership, an existing managed marker is a collision even when
    its text happens to match. Missing or edited owned blocks also fail safely.
    Removing a sole block returns empty bytes; file deletion remains a caller
    decision. Pass max_bytes=None for an OpenCode-only installation.
    """
    current = extract_activation(existing)
    if expected_owned is None and current is not None:
        raise ValueError("Unmanaged rules block already exists in AGENTS.md")
    if expected_owned is not None:
        if extract_activation(expected_owned) != expected_owned:
            raise ValueError("Invalid rules block ownership record")
        if current != expected_owned:
            raise ValueError("Locally modified or missing managed rules block in AGENTS.md")
    if desired is not None and extract_activation(desired) != desired:
        raise ValueError("Desired rules activation must be one complete managed block")
    if existing is None:
        result = desired
    elif current is None:
        result = existing + (desired or b"")
    else:
        offset = existing.index(current)
        result = existing[:offset] + (desired or b"") + existing[offset + len(current):]
    if desired is not None and max_bytes is not None and len(result or b"") > max_bytes:
        raise ValueError(
            f"AGENTS.md would exceed the {max_bytes}-byte instruction budget; "
            "choose fewer rule packs or shorten existing project instructions"
        )
    return result

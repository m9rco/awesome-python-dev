"""Project-local coding agent adapters; no filesystem or subprocess side effects.

All merges preserve unrelated values. TOML also retains comments and formatting.
JSONC is deliberately rejected rather than silently dropping user comments.
"""

from __future__ import annotations

import copy
import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import tomlkit
from tomlkit.exceptions import ParseError


@dataclass(frozen=True)
class Agent:
    id: str
    name: str
    skills_dir: str
    mcp_path: str
    format: str
    root_key: str
    docs_url: str
    note: str = ""


AGENTS: dict[str, Agent] = {
    "claude": Agent(
        "claude", "Claude Code", ".claude/skills", ".mcp.json", "json", "mcpServers",
        "https://code.claude.com/docs/en/mcp",
        "Approve project MCP servers in Claude Code when prompted.",
    ),
    "codex": Agent(
        "codex", "Codex", ".agents/skills", ".codex/config.toml", "toml", "mcp_servers",
        "https://developers.openai.com/codex/mcp/",
        "Codex loads project configuration only after you trust the project.",
    ),
    "cursor": Agent(
        "cursor", "Cursor", ".cursor/skills", ".cursor/mcp.json", "json", "mcpServers",
        "https://cursor.com/docs/mcp",
    ),
    "vscode": Agent(
        "vscode", "GitHub Copilot in VS Code", ".github/skills", ".vscode/mcp.json",
        "json", "servers", "https://code.visualstudio.com/docs/agent-customization/mcp-servers",
        "Use Copilot Agent mode; review/start servers through VS Code's MCP controls.",
    ),
    "opencode": Agent(
        "opencode", "OpenCode", ".opencode/skills", "opencode.json", "json", "mcp",
        "https://opencode.ai/docs/mcp-servers/",
        "Existing opencode.jsonc must be reconciled manually before using this JSON adapter.",
    ),
}


def _agent(agent_id: str) -> Agent:
    try:
        return AGENTS[agent_id]
    except KeyError as exc:
        raise ValueError(f"Unknown agent {agent_id!r}; choose: {', '.join(AGENTS)}") from exc


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key {key!r}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> Any:
    raise ValueError(f"Invalid JSON constant {value!r}")


def _load(agent: Agent, existing: bytes | None) -> Any:
    if existing is None:
        return tomlkit.document() if agent.format == "toml" else {}
    try:
        text = existing.decode("utf-8")
        document = (
            tomlkit.parse(text)
            if agent.format == "toml"
            else json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
        )
    except (UnicodeDecodeError, ValueError, ParseError) as exc:
        hint = " JSON comments and trailing commas (JSONC) are not supported." if agent.format == "json" else ""
        raise ValueError(f"Cannot parse {agent.mcp_path}; leave it unchanged and fix its syntax.{hint}") from exc
    if not isinstance(document, Mapping):
        raise ValueError(f"{agent.mcp_path} must contain a configuration object")
    entries = document.get(agent.root_key, {})
    if not isinstance(entries, Mapping):
        raise ValueError(f"{agent.mcp_path}: {agent.root_key} must be an object/table")
    if any(not isinstance(value, Mapping) for value in entries.values()):
        raise ValueError(f"{agent.mcp_path}: every MCP server must be an object/table")
    return document


def _plain(value: Any) -> Any:
    """Unwrap TOML values without losing types in unknown configuration fields."""
    if hasattr(value, "unwrap"):
        return value.unwrap()
    return copy.deepcopy(value)


def _normalize(agent: Agent, entry: Mapping[str, Any]) -> dict[str, Any]:
    """Keep extra native fields so ownership checks notice user changes."""
    result = _plain(entry)
    if agent.id == "opencode" and result.get("type") == "local":
        command = result.get("command")
        if isinstance(command, list) and command and all(isinstance(part, str) for part in command):
            # Do not overwrite invalid extra keys: their presence must be detectable.
            if "args" in result or ("env" in result and "environment" in result):
                return result
            result.pop("type")
            result["command"] = command[0]
            result["args"] = command[1:]
            if "environment" in result:
                result["env"] = result.pop("environment")
            if result.get("enabled") is True:
                result.pop("enabled")
    elif agent.id in {"claude", "cursor", "vscode"} and result.get("type") == "stdio":
        result.pop("type")
    # Missing args and empty env have the same execution semantics as their defaults.
    if isinstance(result.get("command"), str):
        result.setdefault("args", [])
        if result.get("env") == {}:
            result.pop("env")
    return result


def read_mcp(agent_id: str, existing: bytes | None) -> dict[str, dict[str, Any]]:
    """Return normalized server entries, including unknown user-added fields.

    Remote/unsupported entries are retained, allowing the caller to detect name
    collisions without needing to interpret those transports.
    """
    agent = _agent(agent_id)
    document = _load(agent, existing)
    return {name: _normalize(agent, entry) for name, entry in document.get(agent.root_key, {}).items()}


def _encode(agent: Agent, server: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(server, Mapping) or set(server) - {"command", "args", "env"}:
        raise ValueError("New MCP servers support only command, args, and env")
    command, args, env = server.get("command"), server.get("args", []), server.get("env", {})
    if not isinstance(command, str) or not command.strip():
        raise ValueError("MCP command must be a nonempty string")
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        raise ValueError("MCP args must be a list of strings")
    if not isinstance(env, Mapping) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
        raise ValueError("MCP env must map strings to strings")
    if agent.id == "opencode":
        entry: dict[str, Any] = {"type": "local", "command": [command, *args], "enabled": True}
        if env:
            entry["environment"] = dict(env)
        return entry
    entry = {"command": command, "args": list(args)}
    if agent.id in {"claude", "vscode"}:
        entry = {"type": "stdio", **entry}
    if env:
        entry["env"] = dict(env)
    return entry


def render_mcp(
    agent_id: str,
    existing: bytes | None,
    servers: dict[str, dict[str, Any]],
    *,
    remove: set[str] | None = None,
) -> bytes:
    """Merge MCP servers without changing colliding entries or unrelated config.

    Explicit ``remove`` happens before merge, enabling the installer to refresh
    a server only after it has checked ownership against its manifest. This pure
    adapter does not decide which entries belong to the installer.
    """
    agent = _agent(agent_id)
    document = _load(agent, existing)
    entries = document.get(agent.root_key)
    changed = False
    if entries is None:
        if not servers:
            return existing if existing is not None else (b"" if agent.format == "toml" else b"{}\n")
        document[agent.root_key] = tomlkit.table() if agent.format == "toml" else {}
        entries = document[agent.root_key]
    for name in remove or set():
        if name in entries:
            del entries[name]
            changed = True
    for name, server in servers.items():
        if not isinstance(name, str) or not name:
            raise ValueError("MCP server names must be nonempty strings")
        encoded = _encode(agent, server)
        if name in entries:
            if _normalize(agent, entries[name]) != _normalize(agent, encoded):
                raise ValueError(f"MCP server {name!r} already exists with different settings in {agent.mcp_path}")
        else:
            entries[name] = encoded
            changed = True
    if not changed and existing is not None:
        return existing
    rendered = tomlkit.dumps(document) if agent.format == "toml" else json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    return rendered.encode("utf-8")

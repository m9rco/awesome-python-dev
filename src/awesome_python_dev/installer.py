"""Plan project-local changes, check ownership, then commit with rollback."""

import copy
import json
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from .adapters import AGENTS, read_mcp, render_mcp
from .downloads import digest, download, skill_files
from .rules import (
    build_activation,
    extract_activation,
    render_activation,
    render_rules,
    rule_path_prefixes,
)

STATE = ".awesome-python-dev"
MANIFEST = f"{STATE}/manifest.json"


@dataclass
class Plan:
    root: Path
    changes: dict[str, bytes | None] = field(default_factory=dict)
    before: dict[str, bytes | None] = field(default_factory=dict)
    modes: dict[str, int] = field(default_factory=dict)
    summary: list[str] = field(default_factory=list)

    def put(self, relative: str, content: bytes | None, *, mode: int = 0o600) -> None:
        path = safe_path(self.root, relative)
        current = path.read_bytes() if path.is_file() else None
        if path.exists() and not path.is_file():
            raise ValueError(f"Expected file: {relative}")
        if current != content:
            self.before[relative] = current
            self.changes[relative] = content
            self.modes[relative] = mode


def safe_path(root: Path, relative: str) -> Path:
    part = PurePosixPath(relative)
    if (part.is_absolute() or ".." in part.parts or "\\" in relative
            or ":" in relative or str(part) == "."):
        raise ValueError(f"Unsafe project path: {relative}")
    path = root
    for component in part.parts:
        path = path / component
        if path.is_symlink():
            raise ValueError(f"Refusing symlink in managed path: {path}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Managed path escapes project through a filesystem link: {relative}")
    return path


def runtime_config(install: dict, *, windows: bool | None = None, root: Path | None = None) -> dict:
    """Windows must launch npm's batch shim via cmd; no shell is used on POSIX."""
    config = {"command": install["command"], "args": list(install["args"])}
    if "{project}" in config["args"]:
        if root is None:
            raise ValueError("This MCP recipe requires a target project")
        config["args"] = [str(root.resolve()) if arg == "{project}" else arg for arg in config["args"]]
    if (os.name == "nt" if windows is None else windows) and config["command"] == "npx":
        config = {"command": "cmd", "args": ["/c", "npx", *config["args"]]}
    if install.get("env"):
        config["env"] = install["env"]
    return config


def load_manifest(root: Path) -> dict:
    path = safe_path(root, MANIFEST)
    if not path.exists():
        return {"schema_version": 2, "agents": {}}
    try:
        data = json.loads(path.read_text())
        if data.get("schema_version") not in {1, 2} or not isinstance(data.get("agents"), dict):
            raise ValueError("Unsupported installation manifest")
        for agent_id, record in data["agents"].items():
            if agent_id not in AGENTS or not isinstance(record, dict):
                raise ValueError("Invalid agent in manifest")
            agent = AGENTS[agent_id]
            for section in ("skills", "rules", "mcp"):
                if not isinstance(record.get(section, {}), dict):
                    raise ValueError("Invalid manifest resource collection")
                if any(not re.fullmatch(r"[a-z][a-z0-9-]*", name) for name in record.get(section, {})):
                    raise ValueError("Invalid manifest resource ID")
            for tool_id, skill in record.get("skills", {}).items():
                prefix = str(PurePosixPath(agent.skills_dir) / tool_id) + "/"
                for name, checksum in skill["files"].items():
                    if not name.startswith(prefix) or not isinstance(checksum, str) or len(checksum) != 64:
                        raise ValueError("Invalid skill ownership in manifest")
                    safe_path(root, name)
            for tool_id, rules in record.get("rules", {}).items():
                prefixes = rule_path_prefixes(agent_id, tool_id)
                for name, checksum in rules["files"].items():
                    if not name.startswith(prefixes) or not re.fullmatch(r"[a-f0-9]{64}", checksum):
                        raise ValueError("Invalid rules ownership in manifest")
                    safe_path(root, name)
                if rules["tool"]["id"] != tool_id:
                    raise ValueError("Invalid rule source metadata")
                for key, path in rules["source_files"].items():
                    if path != f"{STATE}/rules/{tool_id}/{key}" or path not in rules["files"]:
                        raise ValueError("Invalid rule source path")
                    safe_path(root, path)
            for tool_id, entry in record.get("mcp", {}).items():
                if entry["server_name"] != f"apd-{tool_id}" or not isinstance(entry["config"], dict):
                    raise ValueError("Invalid MCP ownership in manifest")
        activation = data.get("rule_activation")
        if activation is not None:
            if not isinstance(activation["block"], str) or not isinstance(activation["created"], bool):
                raise ValueError("Invalid rule activation ownership")
            block = activation["block"].encode()
            if extract_activation(block) != block:
                raise ValueError("Invalid rule activation block")
        return data
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as exc:
        raise ValueError(f"Invalid manifest {path}; restore from backup before proceeding") from exc


def read_file(root: Path, relative: str) -> bytes | None:
    path = safe_path(root, relative)
    if path.exists() and not path.is_file():
        raise ValueError(f"Expected file: {relative}")
    return path.read_bytes() if path.exists() else None


def check_owned_files(root: Path, record: dict) -> None:
    for relative, checksum in record.get("files", {}).items():
        current = read_file(root, relative)
        if current is not None and digest(current) != checksum:
            raise ValueError(f"Locally modified managed file: {relative}; preserve or revert it before retrying")


def sync_rule_activation(root: Path, plan: Plan, manifest: dict, result: dict) -> None:
    """Embed the union of Codex/OpenCode rule packs once, preserving user AGENTS text."""
    packs = []
    codex_has_rules = bool(result["agents"].get("codex", {}).get("rules"))
    if codex_has_rules and (read_file(root, "AGENTS.override.md") or b"").strip():
        raise ValueError("AGENTS.override.md shadows AGENTS.md; reconcile it before installing Codex rules")
    for agent_id in ("codex", "opencode"):
        for record in result["agents"].get(agent_id, {}).get("rules", {}).values():
            files = {}
            for key, path in record["source_files"].items():
                content = plan.changes[path] if path in plan.changes else read_file(root, path)
                if content is None or digest(content) != record["files"][path]:
                    raise ValueError(f"Missing or modified rule source: {path}; include its pack when refreshing")
                files[key] = content
            packs.append((record["tool"], files))
    previous = manifest.get("rule_activation")
    if not packs and not previous:
        return
    expected = previous["block"].encode() if previous else None
    desired = build_activation(packs)
    existing = read_file(root, "AGENTS.md")
    rendered = render_activation(existing, desired, expected,
                                 max_bytes=32768 if codex_has_rules else None)
    created = previous["created"] if previous else existing is None
    plan.put("AGENTS.md", None if desired is None and created and not rendered else rendered)
    if desired:
        result["rule_activation"] = {"block": desired.decode(), "created": created}
    else:
        result.pop("rule_activation", None)


def installation_plan(root: Path, agents: list[str], tools: list[dict], profile: str, *,
                      dry_run: bool = False) -> Plan:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    manifest = load_manifest(root)
    result = copy.deepcopy(manifest)
    result["schema_version"] = 2
    plan = Plan(root)
    bundles = {}
    archives = {}
    owners = {}
    for owner, record in manifest["agents"].items():
        for tool_id, item in record.get("rules", {}).items():
            for path, checksum in item["files"].items():
                owners.setdefault(path, []).append((owner, tool_id, checksum))
    has_mcp = any(tool["install"]["type"] == "mcp" for tool in tools)
    for tool in tools:
        if tool["install"]["type"] in {"skill", "rules"} and not dry_run:
            checksum = tool["install"]["sha256"]
            if checksum not in archives:
                archives[checksum] = download(tool["install"])
            bundles[tool["id"]] = skill_files(tool, archives[checksum])
    for agent_id in agents:
        if agent_id not in AGENTS:
            raise ValueError(f"Unsupported agent: {agent_id}")
        agent = AGENTS[agent_id]
        if has_mcp and agent_id == "opencode" and safe_path(root, "opencode.jsonc").exists():
            raise ValueError("opencode.jsonc exists; consolidate it into valid opencode.json before installing")
        record = result["agents"].setdefault(agent_id, {"skills": {}, "mcp": {}})
        record.setdefault("rules", {})
        existing = read_file(root, agent.mcp_path) if has_mcp else None
        servers = read_mcp(agent_id, existing) if has_mcp else {}
        additions = {}
        removals = set()
        for tool in tools:
            tool_id, install = tool["id"], tool["install"]
            if install["type"] == "skill":
                destination = f"{agent.skills_dir}/{tool_id}"
                old = record["skills"].get(tool_id)
                if old:
                    check_owned_files(root, old)
                elif safe_path(root, destination).exists():
                    raise ValueError(f"Unmanaged skill directory exists: {destination}")
                plan.summary.append(f"{agent_id}: skill {tool_id} -> {destination}")
                if dry_run:
                    continue
                contents = {f"{destination}/{name}": data for name, data in bundles[tool_id].items()}
                for relative, content in contents.items():
                    if (old is None or relative not in old["files"]) and safe_path(root, relative).exists():
                        raise ValueError(f"Unmanaged file exists: {relative}")
                    name = str(PurePosixPath(relative).relative_to(destination))
                    plan.put(relative, content, mode=bundles[tool_id].modes.get(name, 0o600))
                for relative in (old or {}).get("files", {}):
                    if relative not in contents:
                        plan.put(relative, None)
                record["skills"][tool_id] = {
                    "repository": tool["repository"], "ref": install["ref"],
                    "archive_sha256": install["sha256"],
                    "files": {name: digest(content) for name, content in contents.items()},
                }
            elif install["type"] == "rules":
                old = record["rules"].get(tool_id)
                if old:
                    check_owned_files(root, old)
                plan.summary.append(f"{agent_id}: rules {tool_id} -> native project instructions")
                if dry_run:
                    if agent_id == "codex" and (read_file(root, "AGENTS.override.md") or b"").strip():
                        raise ValueError("AGENTS.override.md shadows AGENTS.md; reconcile it before installing Codex rules")
                    continue
                source = bundles[tool_id]
                contents = render_rules(agent_id, tool, source)
                for relative, content in contents.items():
                    previous = read_file(root, relative)
                    known = owners.get(relative, [])
                    if previous is not None and relative not in (old or {}).get("files", {}) and not known:
                        raise ValueError(f"Unmanaged rule file exists: {relative}")
                    for owner, owned_id, checksum in known:
                        if previous is not None and digest(previous) != checksum:
                            raise ValueError(f"Locally modified rule file: {relative}")
                        if digest(content) != checksum and (owner not in agents or owned_id != tool_id):
                            raise ValueError(f"Shared rule source changed: {relative}; refresh this pack for all installed agents together")
                    if relative in plan.changes and plan.changes[relative] != content:
                        raise ValueError(f"Conflicting shared rule content: {relative}")
                    plan.put(relative, content)
                for relative in (old or {}).get("files", {}):
                    if relative not in contents:
                        if any(owner not in agents for owner, _, _ in owners.get(relative, [])):
                            raise ValueError("Refresh shared rule sources for all installed agents together")
                        plan.put(relative, None)
                record["rules"][tool_id] = {
                    "tool": copy.deepcopy(tool),
                    "source_files": {key: f"{STATE}/rules/{tool_id}/{key}" for key in source},
                    "files": {name: digest(content) for name, content in contents.items()},
                }
            else:
                name = f"apd-{tool_id}"
                old = record["mcp"].get(tool_id)
                if name in servers:
                    if old is None:
                        raise ValueError(f"Unmanaged MCP server exists: {name} in {agent.mcp_path}")
                    if servers[name] != old["config"]:
                        raise ValueError(f"Locally modified MCP server: {name} in {agent.mcp_path}")
                config = runtime_config(install, root=root)
                if name in servers and servers[name] != config:
                    removals.add(name)
                additions[name] = config
                record["mcp"][tool_id] = {"server_name": name, "config": config}
                if "{project}" in install["args"]:
                    record["mcp"][tool_id]["project_path"] = str(root)
                plan.summary.append(f"{agent_id}: MCP {tool_id} -> {agent.mcp_path}")
        if additions:
            rendered = render_mcp(agent_id, existing, additions, remove=removals)
            # Record the adapter's canonical form, including any transport defaults.
            normalized = read_mcp(agent_id, rendered)
            for item in record["mcp"].values():
                if item["server_name"] in additions:
                    item["config"] = normalized[item["server_name"]]
            plan.put(agent.mcp_path, rendered)
    if not dry_run:
        if any(tool["install"]["type"] == "rules" for tool in tools):
            sync_rule_activation(root, plan, manifest, result)
        result["last_profile"] = profile
        plan.put(MANIFEST, (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode())
    return plan


def removal_plan(root: Path) -> Plan:
    root = root.resolve()
    manifest = load_manifest(root)
    plan = Plan(root)
    for agent_id, record in manifest["agents"].items():
        agent = AGENTS[agent_id]
        for tool_id, skill in record.get("skills", {}).items():
            check_owned_files(root, skill)
            for relative in skill["files"]:
                plan.put(relative, None)
            plan.summary.append(f"{agent_id}: remove skill {tool_id}")
        for tool_id, rules in record.get("rules", {}).items():
            check_owned_files(root, rules)
            for relative in rules["files"]:
                plan.put(relative, None)
            plan.summary.append(f"{agent_id}: remove rules {tool_id}")
        if record.get("mcp"):
            existing = read_file(root, agent.mcp_path)
            servers = read_mcp(agent_id, existing)
            remove = set()
            for item in record["mcp"].values():
                name = item["server_name"]
                if name in servers:
                    if servers[name] != item["config"]:
                        raise ValueError(f"Locally modified MCP server: {name}; preserve or revert it before removal")
                    remove.add(name)
                plan.summary.append(f"{agent_id}: remove MCP {name}")
            if remove:
                plan.put(agent.mcp_path, render_mcp(agent_id, existing, {}, remove=remove))
    if manifest.get("rule_activation"):
        activation = manifest["rule_activation"]
        rendered = render_activation(read_file(root, "AGENTS.md"), None, activation["block"].encode())
        plan.put("AGENTS.md", None if activation["created"] and not rendered else rendered)
    plan.put(MANIFEST, None)
    return plan


@contextmanager
def project_lock(root: Path):
    state = safe_path(root, STATE)
    state.mkdir(exist_ok=True)
    path = safe_path(root, f"{STATE}/install.lock")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ValueError(f"Another installation is running; if none is active, remove stale lock {path}") from exc
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(str(os.getpid()))
        yield
    finally:
        path.unlink(missing_ok=True)


def atomic_write(path: Path, content: bytes, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    try:
        os.chmod(temporary, mode if mode is not None else 0o600)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def apply_plan(plan: Plan) -> int:
    """Optimistic file checks + atomic per-file replace + rollback on write failure."""
    if not plan.changes:
        return 0
    for relative, before in plan.before.items():
        if read_file(plan.root, relative) != before:
            raise ValueError(f"File changed during planning: {relative}; retry")
    backup = safe_path(plan.root, f"{STATE}/backups")
    backup.mkdir(parents=True, exist_ok=True)
    ignore = safe_path(plan.root, f"{STATE}/backups/.gitignore")
    if not ignore.exists():
        atomic_write(ignore, b"*\n")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup = backup / stamp
    modes = {}
    for relative, before in plan.before.items():
        path = safe_path(plan.root, relative)
        modes[relative] = path.stat().st_mode & 0o777 if path.exists() else None
        if before is not None:
            atomic_write(backup / relative, before)
    changed = []
    try:
        for relative, content in plan.changes.items():
            path = safe_path(plan.root, relative)
            if content is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, content, modes[relative] if modes[relative] is not None else plan.modes[relative])
            changed.append(relative)
    except (OSError, ValueError, KeyboardInterrupt):
        for relative in reversed(changed):
            path = safe_path(plan.root, relative)
            before = plan.before[relative]
            if before is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, before, modes[relative])
        raise
    # Only prune directories made empty by removal, never recursively delete user files.
    for relative, content in plan.changes.items():
        if content is not None:
            continue
        parent = safe_path(plan.root, relative).parent
        while parent != plan.root and parent.name != STATE:
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent
    return len(changed)


def doctor(root: Path) -> tuple[list[str], bool]:
    root = root.resolve()
    manifest = load_manifest(root)
    messages = []
    ok = True
    if not manifest["agents"]:
        return ["No installation found; run apd init --agents <ids> first."], False
    requirements = set()
    if manifest.get("rule_activation"):
        expected = manifest["rule_activation"]["block"].encode()
        instructions = read_file(root, "AGENTS.md")
        if extract_activation(instructions) != expected:
            messages.append("FAIL AGENTS.md: managed rules block missing or modified")
            ok = False
        if manifest["agents"].get("codex", {}).get("rules") and (read_file(root, "AGENTS.override.md") or b"").strip():
            messages.append("FAIL AGENTS.override.md shadows installed Codex rules")
            ok = False
        if manifest["agents"].get("codex", {}).get("rules") and len(instructions or b"") > 32768:
            messages.append("FAIL AGENTS.md exceeds Codex's 32768-byte instruction budget")
            ok = False
    for agent_id, record in manifest["agents"].items():
        for section in ("skills", "rules"):
            for item in record.get(section, {}).values():
                for relative, checksum in item["files"].items():
                    current = read_file(root, relative)
                    if current is None or digest(current) != checksum:
                        messages.append(f"FAIL {relative}: missing or modified")
                        ok = False
        if record.get("mcp"):
            servers = read_mcp(agent_id, read_file(root, AGENTS[agent_id].mcp_path))
            for item in record["mcp"].values():
                name = item["server_name"]
                if servers.get(name) != item["config"]:
                    messages.append(f"FAIL {agent_id}/{name}: missing or modified")
                    ok = False
                if item.get("project_path") and Path(item["project_path"]).resolve() != root:
                    messages.append(f"FAIL {agent_id}/{name}: project path changed; rerun init with this tool to update the binding")
                    ok = False
                config = item["config"]
                requirements.add("npx" if config["command"] == "cmd" and config["args"][:2] == ["/c", "npx"] else config["command"])
                if any(arg.startswith("git+https://") for arg in config["args"]):
                    requirements.add("git")
        messages.append(f"Checked {agent_id}: {len(record.get('skills', {}))} skills, {len(record.get('rules', {}))} rule packs, {len(record.get('mcp', {}))} MCP servers")
    for command in sorted(requirements):
        found = shutil.which(command)
        messages.append(f"{'OK' if found else 'FAIL'} runtime {command}: {found or 'not on PATH'}")
        ok = ok and bool(found)
    messages.append("Checks cover installed files, config and runtime presence; MCP connections and agent discovery are not exercised.")
    return messages, ok

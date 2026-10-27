"""Plan project-local changes, check ownership, then commit with rollback."""

import copy
import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from .adapters import AGENTS, read_mcp, render_mcp
from .downloads import digest, download, skill_files

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


def runtime_config(install: dict, *, windows: bool | None = None) -> dict:
    """Windows must launch npm's batch shim via cmd; no shell is used on POSIX."""
    config = {"command": install["command"], "args": list(install["args"])}
    if (os.name == "nt" if windows is None else windows) and config["command"] == "npx":
        config = {"command": "cmd", "args": ["/c", "npx", *config["args"]]}
    if install.get("env"):
        config["env"] = install["env"]
    return config


def load_manifest(root: Path) -> dict:
    path = safe_path(root, MANIFEST)
    if not path.exists():
        return {"schema_version": 1, "agents": {}}
    try:
        data = json.loads(path.read_text())
        if data.get("schema_version") != 1 or not isinstance(data.get("agents"), dict):
            raise ValueError("Unsupported installation manifest")
        for agent_id, record in data["agents"].items():
            if agent_id not in AGENTS or not isinstance(record, dict):
                raise ValueError("Invalid agent in manifest")
            agent = AGENTS[agent_id]
            for tool_id, skill in record.get("skills", {}).items():
                prefix = str(PurePosixPath(agent.skills_dir) / tool_id) + "/"
                for name, checksum in skill["files"].items():
                    if not name.startswith(prefix) or not isinstance(checksum, str) or len(checksum) != 64:
                        raise ValueError("Invalid skill ownership in manifest")
                    safe_path(root, name)
            for tool_id, entry in record.get("mcp", {}).items():
                if entry["server_name"] != f"apd-{tool_id}" or not isinstance(entry["config"], dict):
                    raise ValueError("Invalid MCP ownership in manifest")
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
            raise ValueError(f"Locally modified skill file: {relative}; preserve or revert it before retrying")


def installation_plan(root: Path, agents: list[str], tools: list[dict], profile: str, *,
                      dry_run: bool = False) -> Plan:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    manifest = load_manifest(root)
    result = copy.deepcopy(manifest)
    plan = Plan(root)
    bundles = {}
    has_mcp = any(tool["install"]["type"] == "mcp" for tool in tools)
    for tool in tools:
        if tool["install"]["type"] == "skill" and not dry_run:
            bundles[tool["id"]] = skill_files(tool, download(tool["install"]))
    for agent_id in agents:
        if agent_id not in AGENTS:
            raise ValueError(f"Unsupported agent: {agent_id}")
        agent = AGENTS[agent_id]
        if has_mcp and agent_id == "opencode" and safe_path(root, "opencode.jsonc").exists():
            raise ValueError("opencode.jsonc exists; consolidate it into valid opencode.json before installing")
        record = result["agents"].setdefault(agent_id, {"skills": {}, "mcp": {}})
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
            else:
                name = f"apd-{tool_id}"
                old = record["mcp"].get(tool_id)
                if name in servers:
                    if old is None:
                        raise ValueError(f"Unmanaged MCP server exists: {name} in {agent.mcp_path}")
                    if servers[name] != old["config"]:
                        raise ValueError(f"Locally modified MCP server: {name} in {agent.mcp_path}")
                config = runtime_config(install)
                if name in servers and servers[name] != config:
                    removals.add(name)
                additions[name] = config
                record["mcp"][tool_id] = {"server_name": name, "config": config}
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
    for agent_id, record in manifest["agents"].items():
        for tool_id, skill in record.get("skills", {}).items():
            for relative, checksum in skill["files"].items():
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
                config = item["config"]
                requirements.add("npx" if config["command"] == "cmd" and config["args"][:2] == ["/c", "npx"] else config["command"])
        messages.append(f"Checked {agent_id}: {len(record.get('skills', {}))} skills, {len(record.get('mcp', {}))} MCP servers")
    for command in sorted(requirements):
        found = shutil.which(command)
        messages.append(f"{'OK' if found else 'FAIL'} runtime {command}: {found or 'not on PATH'}")
        ok = ok and bool(found)
    messages.append("Checks cover installed files, config and runtime presence; MCP connections and agent discovery are not exercised.")
    return messages, ok

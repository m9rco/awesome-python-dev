"""Load and validate the bundled, reviewed catalog (never a remote manifest)."""

import json
import re
from importlib.resources import files
from pathlib import PurePosixPath


def load_catalog() -> dict:
    catalog = json.loads(files("awesome_python_dev").joinpath("data/catalog.json").read_text())
    validate_catalog(catalog)
    return catalog


def validate_catalog(catalog: dict) -> None:
    if catalog.get("schema_version") != 1:
        raise ValueError("Unsupported catalog schema")
    ids = set()
    for tool in catalog["tools"]:
        tool_id = tool["id"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", tool_id) or tool_id in ids:
            raise ValueError(f"Invalid or duplicate tool ID: {tool_id}")
        ids.add(tool_id)
        install = tool.get("install")
        if not install:
            continue
        if install["type"] == "skill":
            ref = install["ref"]
            if not re.fullmatch(r"[a-f0-9]{40}", ref):
                raise ValueError(f"Unpinned skill: {tool_id}")
            expected_url = f"https://codeload.github.com/{tool['repository']}/tar.gz/{ref}"
            if install["url"] != expected_url:
                raise ValueError(f"Unexpected skill archive URL: {tool_id}")
            if not re.fullmatch(r"[a-f0-9]{64}", install["sha256"]):
                raise ValueError(f"Missing skill checksum: {tool_id}")
            for key in ("subdir", "license_path"):
                path = PurePosixPath(install[key])
                if path.is_absolute() or ".." in path.parts or "\\" in str(path):
                    raise ValueError(f"Unsafe {key}: {tool_id}")
        elif install["type"] == "mcp":
            command, args = install["command"], install["args"]
            if command not in {"npx", "uvx"} or not args or not all(isinstance(a, str) for a in args):
                raise ValueError(f"Unsupported MCP command: {tool_id}")
            pin_pattern = r"@\d+\.\d+\.\d+(?:[-+][\w.-]+)?$" if command == "npx" else r"==\d+\.\d+\.\d+(?:[\w.-]+)?$"
            if not any(re.search(pin_pattern, arg) for arg in args):
                raise ValueError(f"Unpinned MCP package: {tool_id}")
        else:
            raise ValueError(f"Unsupported install type: {tool_id}")
    for name, selected in catalog["profiles"].items():
        if not selected or any(item not in ids for item in selected):
            raise ValueError(f"Invalid profile: {name}")
        if any(not tool.get("install") for tool in catalog["tools"] if tool["id"] in selected):
            raise ValueError(f"Profile {name} includes reference-only tools")


def select_tools(catalog: dict, profile: str, selected: str | None = None) -> list[dict]:
    if profile not in catalog["profiles"]:
        raise ValueError(f"Unknown profile {profile}; choose {', '.join(catalog['profiles'])}")
    names = selected.split(",") if selected else catalog["profiles"][profile]
    by_id = {tool["id"]: tool for tool in catalog["tools"]}
    result = []
    for name in dict.fromkeys(item.strip() for item in names):
        if name not in by_id:
            raise ValueError(f"Unknown tool {name!r}; use 'apd list'")
        tool = by_id[name]
        if not tool.get("install"):
            raise ValueError(f"{name} is reference-only; follow {tool['homepage']}")
        result.append(tool)
    return result

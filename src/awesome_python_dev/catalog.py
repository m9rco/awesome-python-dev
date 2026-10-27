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
    if catalog.get("schema_version") not in {1, 2}:
        raise ValueError("Unsupported catalog schema")
    ids = set()
    for tool in catalog["tools"]:
        tool_id = tool["id"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", tool_id) or tool_id in ids:
            raise ValueError(f"Invalid or duplicate tool ID: {tool_id}")
        ids.add(tool_id)
        if tool.get("kind") not in {"skill", "mcp", "rules", "lsp", "reference"}:
            raise ValueError(f"Unsupported catalog kind: {tool_id}")
        install = tool.get("install")
        if not install:
            continue
        if install["type"] in {"skill", "rules"}:
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
                if path.is_absolute() or ".." in path.parts or "\\" in str(path) or ":" in str(path):
                    raise ValueError(f"Unsafe {key}: {tool_id}")
            if install["type"] == "rules":
                names = install.get("files")
                if not isinstance(names, list) or not names or len(names) != len(set(names)):
                    raise ValueError(f"Rules require explicit unique source files: {tool_id}")
                for name in names:
                    path = PurePosixPath(name)
                    if (path.is_absolute() or ".." in path.parts or "\\" in name
                            or ":" in name or path.suffix != ".md"):
                        raise ValueError(f"Unsafe rule source: {tool_id}/{name}")
        elif install["type"] == "mcp":
            command, args = install["command"], install["args"]
            if command not in {"npx", "uvx"} or not args or not all(isinstance(a, str) for a in args):
                raise ValueError(f"Unsupported MCP command: {tool_id}")
            if install.get("source") == "git":
                ref = install.get("ref", "")
                if command != "uvx" or not re.fullmatch(r"[a-f0-9]{40}", ref):
                    raise ValueError(f"Unpinned MCP Git source: {tool_id}")
                source = f"git+https://github.com/{tool['repository']}@{ref}"
                source_git = f"git+https://github.com/{tool['repository']}.git@{ref}"
                if not any(args[i] == "--from" and args[i + 1] in {source, source_git}
                           for i in range(len(args) - 1)):
                    raise ValueError(f"MCP Git source does not match reviewed repository: {tool_id}")
            else:
                pin_pattern = r"@\d+\.\d+\.\d+(?:[-+][\w.-]+)?$" if command == "npx" else r"==\d+\.\d+\.\d+(?:[\w.-]+)?$"
                if not any(re.search(pin_pattern, arg) for arg in args):
                    raise ValueError(f"Unpinned MCP package: {tool_id}")
            if any("{" in arg or "}" in arg for arg in args if arg != "{project}"):
                raise ValueError(f"Unsupported MCP argument placeholder: {tool_id}")
        else:
            raise ValueError(f"Unsupported install type: {tool_id}")
    by_id = {tool["id"]: tool for tool in catalog["tools"]}
    visiting, visited = set(), set()

    def visit(tool_id):
        if tool_id in visiting:
            raise ValueError(f"Circular tool dependency: {tool_id}")
        if tool_id in visited:
            return
        visiting.add(tool_id)
        dependencies = by_id[tool_id].get("requires", [])
        if not isinstance(dependencies, list):
            raise ValueError(f"Invalid dependencies: {tool_id}")
        for name in dependencies:
            if name not in by_id or not by_id[name].get("install"):
                raise ValueError(f"Missing installable dependency {name}: {tool_id}")
            visit(name)
        visiting.remove(tool_id)
        visited.add(tool_id)

    for tool_id in by_id:
        visit(tool_id)
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
    visiting, visited = set(), set()

    def include(name):
        if name not in by_id:
            raise ValueError(f"Unknown tool {name!r}; use 'apd list'")
        tool = by_id[name]
        if not tool.get("install"):
            raise ValueError(f"{name} is reference-only; follow {tool['homepage']}")
        if name in visiting:
            raise ValueError(f"Circular tool dependency: {name}")
        if name in visited:
            return
        visiting.add(name)
        for dependency in tool.get("requires", []):
            include(dependency)
        visiting.remove(name)
        visited.add(name)
        result.append(tool)

    for name in dict.fromkeys(item.strip() for item in names):
        include(name)
    return result

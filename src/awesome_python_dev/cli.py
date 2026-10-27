"""Small, explicit CLI with an OpenSpec-style project initialization workflow."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .adapters import AGENTS
from .catalog import load_catalog, select_tools
from .installer import apply_plan, doctor, installation_plan, project_lock, removal_plan


def agent_selection(value: str | None, root: Path) -> list[str]:
    if value == "all":
        return list(AGENTS)
    if not value:
        detected = [name for name, agent in AGENTS.items()
                    if (root / agent.skills_dir).parent.exists() or (root / agent.mcp_path).exists()]
        if sys.stdin.isatty():
            print("Agents: " + ", ".join(AGENTS))
            default = ",".join(detected) or "codex,claude"
            value = input(f"Choose agents [{default}]: ").strip() or default
        elif detected:
            return detected
        else:
            raise ValueError("No agents detected. Pass --agents " + ",".join(AGENTS) + " (or all)")
    selected = list(dict.fromkeys(item.strip() for item in value.split(",")))
    unknown = set(selected) - set(AGENTS)
    if unknown:
        raise ValueError(f"Unknown agents: {', '.join(sorted(unknown))}; choose {', '.join(AGENTS)}")
    return selected


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(prog="apd", description="Curated skills + MCP servers for coding agents")
    cli.add_argument("--version", action="version", version=f"awesome-python-dev {__version__}")
    commands = cli.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="Browse the curated catalog")
    listing.add_argument("--kind", choices=["skill", "mcp", "reference"])
    listing.add_argument("--json", action="store_true", help="Print machine-readable catalog")
    commands.add_parser("agents", help="List supported agent paths")
    init = commands.add_parser("init", help="Install a toolkit into a project")
    init.add_argument("--agents", help="Comma-separated IDs, or all; prompts/detects when omitted")
    init.add_argument("--profile", default="starter", help="starter, python, or web")
    init.add_argument("--tools", help="Explicit comma-separated tool IDs instead of the profile")
    init.add_argument("--path", type=Path, default=Path.cwd(), help="Existing project directory")
    init.add_argument("--dry-run", action="store_true", help="Preview without downloads or writes")
    check = commands.add_parser("doctor", help="Check installed files, config and runtime availability")
    check.add_argument("--path", type=Path, default=Path.cwd())
    remove = commands.add_parser("remove", help="Remove all unchanged resources managed by apd in this project")
    remove.add_argument("--path", type=Path, default=Path.cwd())
    remove.add_argument("--dry-run", action="store_true")
    return cli


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "agents":
            for agent_id, agent in AGENTS.items():
                print(f"{agent_id:10} skills: {agent.skills_dir}  MCP: {agent.mcp_path}")
            return 0
        if args.command == "list":
            catalog = load_catalog()
            if args.kind:
                catalog["tools"] = [item for item in catalog["tools"] if item["kind"] == args.kind]
            if args.json:
                print(json.dumps(catalog, indent=2, ensure_ascii=False))
            else:
                print(f"Catalog reviewed: {catalog['reviewed_at']}\n")
                for tool in catalog["tools"]:
                    state = "installable" if tool.get("install") else "reference"
                    print(f"{tool['id']:32} {tool['kind']:9} {state:12} {tool['description']}")
                print("\nProfiles: " + ", ".join(catalog["profiles"]))
            return 0
        root = args.path.expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"Project directory does not exist: {root}")
        if args.command == "doctor":
            messages, ok = doctor(root)
            print("\n".join(messages))
            return 0 if ok else 1
        if args.command == "init":
            agents = agent_selection(args.agents, root)
            tools = select_tools(load_catalog(), args.profile, args.tools)

            def build_plan():
                return installation_plan(root, agents, tools, args.profile, dry_run=args.dry_run)
        else:
            def build_plan():
                return removal_plan(root)
        if args.dry_run:
            plan = build_plan()
            print("Preview only (no downloads or writes):")
            print("\n".join(plan.summary) or "Nothing installed.")
            return 0
        with project_lock(root):
            plan = build_plan()
            changed = apply_plan(plan)
        print("\n".join(plan.summary) or "Nothing installed.")
        print(f"\n{changed} files changed in {root}.")
        if args.command == "init":
            print("MCP configurations are registered; servers start when your agent enables them.")
            print("Run apd doctor, then restart/reload your agent. Review its project trust and MCP prompts.")
            for agent_id in agents:
                note = getattr(AGENTS[agent_id], "note", "")
                if note:
                    print(f"{agent_id}: {note}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130

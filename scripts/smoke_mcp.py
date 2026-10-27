"""Optional network smoke test; launches pinned MCPs but never calls their tools.

Run: uv run --no-project --with mcp python scripts/smoke_mcp.py
Select one: add --tool context7 (or playwright / fetch).
This is not part of offline unit tests. Packages may be downloaded by npx/uvx.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check(entry: dict, timeout: float) -> dict:
    install = entry["install"]
    result = {"id": entry["id"], "package_version": install["version"]}
    network_env = {
        key: value for key, value in os.environ.items()
        if key.lower().endswith("_proxy") or key in {"SSL_CERT_FILE", "SSL_CERT_DIR", "NODE_EXTRA_CA_CERTS"}
    }
    try:
        async with asyncio.timeout(timeout):
            with TemporaryDirectory(prefix="apd-mcp-smoke-") as cache:
                params = StdioServerParameters(
                    command=install["command"], args=install["args"],
                    env={**network_env, "npm_config_cache": cache},
                )
                with open(os.devnull, "w") as errors:
                    async with stdio_client(params, errlog=errors) as (reader, writer):
                        async with ClientSession(reader, writer) as session:
                            initialized = await session.initialize()
                            listed = await session.list_tools()
                            server_info = getattr(initialized, "server_info", None)
                            if server_info is None:
                                server_info = initialized.serverInfo
                            protocol = getattr(initialized, "protocol_version", None)
                            if protocol is None:
                                protocol = initialized.protocolVersion
                            result.update(
                                status="passed",
                                protocol_version=protocol,
                                server_name=server_info.name,
                                server_version=server_info.version,
                                tools=[tool.name for tool in listed.tools],
                            )
    except (Exception, BaseExceptionGroup) as exc:
        while isinstance(exc, BaseExceptionGroup) and exc.exceptions:
            exc = exc.exceptions[0]
        result.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    return result


async def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=["context7", "playwright", "fetch"])
    parser.add_argument("--timeout", type=float, default=90)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "src/awesome_python_dev/data/catalog.json").read_text())
    selected = [
        entry for entry in catalog["tools"]
        if entry["kind"] == "mcp" and (args.tool is None or entry["id"] == args.tool)
    ]
    print(json.dumps({"platform": platform.platform(), "python": platform.python_version(), "mcp_sdk": version("mcp")}), flush=True)
    results = []
    for entry in selected:
        result = await check(entry, args.timeout)
        results.append(result)
        print(json.dumps(result), flush=True)
    return int(any(result["status"] != "passed" for result in results))


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))

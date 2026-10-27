"""Smoke-test a built wheel in a fresh environment outside the source checkout.

Run after ``uv build`` with ``uv run python scripts/check_dist.py``.
Only previews installations; no upstream skills or MCP packages are downloaded.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


def run(*args: str, cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True, timeout=120)
    return result.stdout


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    wheels = list((root / "dist").glob("*.whl"))
    if len(wheels) != 1:
        raise ValueError("Expected one wheel in dist/; clear old build outputs and run uv build")
    uv = shutil.which("uv")
    if uv is None:
        raise ValueError("uv is required for the isolated wheel smoke test")
    version = tomllib.loads((root / "pyproject.toml").read_text())["project"]["version"]
    with tempfile.TemporaryDirectory(prefix="apd-wheel-check-") as folder:
        temporary = Path(folder)
        environment = temporary / "environment"
        project = temporary / "project"
        project.mkdir()
        run(uv, "venv", str(environment), "--python", sys.executable, cwd=temporary)
        binary = environment / ("Scripts" if os.name == "nt" else "bin")
        suffix = ".exe" if os.name == "nt" else ""
        python = binary / f"python{suffix}"
        run(uv, "pip", "install", "--python", str(python), str(wheels[0]), cwd=temporary)
        expected = f"awesome-python-dev {version}"
        for name in ("apd", "awesome-python-dev"):
            actual = run(str(binary / f"{name}{suffix}"), "--version", cwd=project).strip()
            if actual != expected:
                raise ValueError(f"{name} returned unexpected version: {actual!r}")
        cli = str(binary / f"apd{suffix}")
        catalog = json.loads(run(cli, "list", "--json", cwd=project))
        if not catalog.get("tools") or not catalog.get("profiles"):
            raise ValueError("Built wheel is missing its catalog or profiles")
        for profile in catalog["profiles"]:
            run(cli, "init", "--agents", "all", "--profile", profile, "--dry-run", cwd=project)
            if list(project.iterdir()):
                raise ValueError(f"Preview for {profile} wrote files to the target project")
        print(f"Wheel OK: {wheels[0].name}; both entry points, catalog, and all profile previews")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stdout, file=sys.stderr)
        print(error.stderr, file=sys.stderr)
        raise SystemExit(error.returncode) from error

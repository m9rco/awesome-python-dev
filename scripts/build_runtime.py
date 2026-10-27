#!/usr/bin/env python3
"""Build a self-contained Python zipapp for the independently released runtime.

Run after ``uv sync --locked``. The output needs Python 3.11+, but no installed
Python packages, pip environment, Git checkout, or source build at launch time.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import io
import json
import os
import re
import tempfile
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_API = 1
REPOSITORY = "https://github.com/m9rco/awesome-python-dev"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
ENTRY_POINT = b"""import sys

if sys.version_info < (3, 11):
    raise SystemExit("Awesome Python Dev runtime requires Python 3.11 or newer.")

from awesome_python_dev.cli import main

raise SystemExit(main())
"""


def source_version() -> str:
    """Reject inconsistent package versions before creating release artifacts."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    version = project["version"]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("runtime releases require a stable major.minor.patch version")
    module = ast.parse((ROOT / "src/awesome_python_dev/__init__.py").read_text(encoding="utf-8"))
    declared = next(
        (
            ast.literal_eval(node.value)
            for node in module.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "__version__"
                for target in node.targets
            )
        ),
        None,
    )
    if declared != version:
        raise ValueError("pyproject.toml and awesome_python_dev.__version__ must match")
    return version


def package_files(directory: Path, prefix: str) -> dict[str, bytes]:
    """Collect package source and data, excluding machine-local Python caches."""
    files: dict[str, bytes] = {}
    for source in sorted(directory.rglob("*")):
        if "__pycache__" in source.parts or source.suffix in {".pyc", ".pyo"}:
            continue
        if source.is_symlink():
            raise ValueError(f"runtime packages cannot contain symlinks: {source}")
        if source.is_file():
            if source.suffix.lower() in {".so", ".pyd", ".dll", ".dylib"}:
                raise ValueError(f"zipapp runtime cannot include a native extension: {source}")
            files[f"{prefix}/{source.relative_to(directory).as_posix()}"] = source.read_bytes()
    return files


def runtime_files(version: str) -> dict[str, bytes]:
    """Bundle first-party sources and the exact pure-Python dependency from uv.lock."""
    lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
    locked = [item["version"] for item in lock["package"] if item["name"] == "tomlkit"]
    if len(locked) != 1:
        raise ValueError("uv.lock must contain exactly one tomlkit version")
    dependency = importlib.metadata.distribution("tomlkit")
    if dependency.version != locked[0]:
        raise ValueError("installed tomlkit differs from uv.lock; run uv sync --locked")
    source = Path(dependency.locate_file("tomlkit"))
    if not source.is_dir():
        raise ValueError("tomlkit must be installed as a source package before bundling")

    files = {"__main__.py": ENTRY_POINT}
    files.update(package_files(ROOT / "src/awesome_python_dev", "awesome_python_dev"))
    files.update(package_files(source, "tomlkit"))
    license_count = 0
    for item in dependency.files or ():
        parts = item.parts
        if len(parts) < 2 or not parts[0].endswith(".dist-info"):
            continue
        if item.name in {"METADATA", "WHEEL"} or "licenses" in parts or item.name == "LICENSE":
            files[item.as_posix()] = Path(dependency.locate_file(item)).read_bytes()
            if "licenses" in parts or item.name == "LICENSE":
                license_count += 1
    if not license_count:
        raise ValueError("tomlkit installation is missing its license metadata")

    distribution = f"awesome_python_dev-{version}.dist-info"
    files[f"{distribution}/METADATA"] = (
        "Metadata-Version: 2.4\nName: awesome-python-dev\n"
        f"Version: {version}\n"
        "Summary: Curated AI development skills, rules, MCP and LSP tools.\n"
        "Requires-Python: >=3.11\nLicense-Expression: MIT\n"
        "License-File: LICENSE\nLicense-File: LICENSES/ECC-MIT.txt\n"
        f"Requires-Dist: tomlkit=={dependency.version}\n\n"
    ).encode("utf-8")
    files[f"{distribution}/entry_points.txt"] = (
        "[console_scripts]\napd = awesome_python_dev.cli:main\n"
        "awesome-python-dev = awesome_python_dev.cli:main\n"
    ).encode("utf-8")
    for name in ("LICENSE", "LICENSES/ECC-MIT.txt", "THIRD_PARTY_NOTICES.md"):
        contents = (ROOT / name).read_bytes()
        files[name] = contents
        files[f"{distribution}/licenses/{name}"] = contents
    files["runtime-dependencies.json"] = json_bytes(
        {
            "runtime_api": RUNTIME_API,
            "python_requires": ">=3.11",
            "packages": [
                {"name": "awesome-python-dev", "version": version},
                {"name": "tomlkit", "version": dependency.version},
            ],
        }
    )
    return files


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def zip_bytes(files: dict[str, bytes]) -> bytes:
    """Use fixed metadata and stored entries for byte-identical cross-version output."""
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)
    return stream.getvalue()


def atomic_write(path: Path, content: bytes) -> None:
    """Replace only the named release file; never remove an output directory."""
    if path.is_symlink():
        raise ValueError(f"refusing to replace a symlink: {path}")
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def build_runtime(output: Path) -> dict:
    """Write the zipapp, checksum manifest and SHA256SUMS; return its manifest."""
    output = Path(output)
    if output.is_symlink():
        raise ValueError("runtime output must not be a symlink")
    version = source_version()
    filename = f"awesome-python-dev-runtime-{version}.pyz"
    data = zip_bytes(runtime_files(version))
    sha256 = hashlib.sha256(data).hexdigest()
    manifest = {
        "schema_version": 1,
        "runtime_api": RUNTIME_API,
        "version": version,
        "python_requires": ">=3.11",
        "asset": {
            "url": f"{REPOSITORY}/releases/download/v{version}/{filename}",
            "sha256": sha256,
            "size": len(data),
        },
    }
    manifest_bytes = json_bytes(manifest)
    output.mkdir(parents=True, exist_ok=True)
    atomic_write(output / filename, data)
    atomic_write(output / "runtime.json", manifest_bytes)
    atomic_write(
        output / "SHA256SUMS",
        (
            f"{sha256}  {filename}\n{hashlib.sha256(manifest_bytes).hexdigest()}  runtime.json\n"
        ).encode("ascii"),
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/runtime")
    args = parser.parse_args()
    manifest = build_runtime(args.output)
    print(
        f"Built runtime {manifest['version']} ({manifest['asset']['size']:,} bytes) "
        f"into {args.output}"
    )


if __name__ == "__main__":
    main()

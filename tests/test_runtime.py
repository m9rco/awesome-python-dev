"""Verify the release runtime works without a checkout or installed dependencies."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def builder():
    spec = importlib.util.spec_from_file_location(
        "build_runtime", ROOT / "scripts/build_runtime.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runtime(tmp_path_factory, builder):
    output = tmp_path_factory.mktemp("runtime")
    manifest = builder.build_runtime(output)
    archive = output / manifest["asset"]["url"].rsplit("/", 1)[-1]
    return output, archive, manifest


def run_runtime(archive: Path, directory: Path, *arguments: str) -> subprocess.CompletedProcess:
    # -S excludes site-packages as well as the project's editable install;
    # -I ignores environment imports and the current working directory.
    return subprocess.run(
        [sys.executable, "-I", "-S", str(archive), *arguments],
        cwd=directory,
        env={**os.environ, "PYTHONPATH": str(ROOT / "does-not-exist")},
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )


def test_runtime_runs_from_isolated_directory_without_installed_packages(runtime, tmp_path):
    _, archive, manifest = runtime
    version = run_runtime(archive, tmp_path, "--version")
    assert version.returncode == 0, version.stderr
    assert version.stdout.strip() == f"awesome-python-dev {manifest['version']}"
    listing = run_runtime(archive, tmp_path, "list", "--json")
    assert listing.returncode == 0, listing.stderr
    catalog = json.loads(listing.stdout)
    expected = json.loads(
        (ROOT / "src/awesome_python_dev/data/catalog.json").read_text(encoding="utf-8")
    )
    assert catalog == expected
    profiles = run_runtime(archive, tmp_path, "profiles", "--json")
    assert profiles.returncode == 0, profiles.stderr
    assert json.loads(profiles.stdout) == expected["profiles"]


def test_runtime_dry_run_and_exit_status(runtime, tmp_path):
    _, archive, _ = runtime
    preview = run_runtime(
        archive, tmp_path, "init", "--agents", "codex,claude", "--profile", "fastapi", "--dry-run"
    )
    assert preview.returncode == 0, preview.stderr
    assert "Preview only" in preview.stdout
    assert "ecc-fastapi-rules" in preview.stdout
    assert list(tmp_path.iterdir()) == []
    invalid = run_runtime(
        archive, tmp_path, "init", "--agents", "codex", "--profile", "not-a-profile", "--dry-run"
    )
    assert invalid.returncode == 1
    assert "Error:" in invalid.stderr


def test_runtime_manifest_checksums_licenses_and_reproducibility(runtime, tmp_path, builder):
    output, archive, manifest = runtime
    contents = archive.read_bytes()
    assert manifest["schema_version"] == 1
    assert manifest["runtime_api"] == 1
    assert manifest["python_requires"] == ">=3.11"
    assert manifest["asset"]["sha256"] == hashlib.sha256(contents).hexdigest()
    assert manifest["asset"]["size"] == len(contents)
    assert json.loads((output / "runtime.json").read_text(encoding="utf-8")) == manifest
    for line in (output / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        digest, filename = line.split("  ", 1)
        assert hashlib.sha256((output / filename).read_bytes()).hexdigest() == digest
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        assert names == sorted(names)
        assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)
        assert bundle.read("LICENSE") == (ROOT / "LICENSE").read_bytes()
        assert bundle.read("LICENSES/ECC-MIT.txt") == (ROOT / "LICENSES/ECC-MIT.txt").read_bytes()
        assert "THIRD_PARTY_NOTICES.md" in names
        assert any(
            name.startswith("tomlkit-") and name.endswith("licenses/LICENSE") for name in names
        )
        info = json.loads(bundle.read("runtime-dependencies.json"))
        assert {p["name"] for p in info["packages"]} == {"awesome-python-dev", "tomlkit"}
        assert all(item.date_time == builder.ZIP_TIMESTAMP for item in bundle.infolist())
    again = builder.build_runtime(tmp_path)
    assert again == manifest
    assert (tmp_path / archive.name).read_bytes() == contents


def test_runtime_builder_preserves_unrelated_output_files(builder, tmp_path):
    sentinel = tmp_path / "notes.txt"
    sentinel.write_text("keep this file", encoding="utf-8")
    builder.build_runtime(tmp_path)
    assert sentinel.read_text(encoding="utf-8") == "keep this file"


def test_runtime_builder_rejects_dependency_not_matching_lock(builder, monkeypatch, tmp_path):
    real_distribution = builder.importlib.metadata.distribution

    class WrongVersion:
        version = "0.0.0"

    monkeypatch.setattr(
        builder.importlib.metadata,
        "distribution",
        lambda name: WrongVersion() if name == "tomlkit" else real_distribution(name),
    )
    with pytest.raises(ValueError, match="differs from uv.lock"):
        builder.build_runtime(tmp_path)
    assert list(tmp_path.iterdir()) == []

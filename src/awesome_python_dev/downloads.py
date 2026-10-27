"""Checksum-verified downloads and bounded archive reads; no extraction or execution."""

import hashlib
import http.client
import io
import os
import ssl
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path, PurePosixPath

from . import __version__

MAX_ARCHIVE = 64 * 1024 * 1024
MAX_EXPANDED = 256 * 1024 * 1024
MAX_FILES = 20000


class SkillFiles(dict[str, bytes]):
    """Selected files with sanitized owner-only executable permissions."""

    def __init__(self):
        super().__init__()
        self.modes: dict[str, int] = {}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(install: dict, cache: Path | None = None) -> bytes:
    cache = cache or Path(os.environ.get("APD_CACHE_DIR", Path.home() / ".cache/awesome-python-dev"))
    target = cache / (install["sha256"] + ".tar.gz")
    if target.exists():
        if target.stat().st_size > MAX_ARCHIVE:
            raise ValueError(f"Oversized archive cache file: {target}")
        data = target.read_bytes()
        if digest(data) == install["sha256"]:
            return data
        raise ValueError(f"Archive cache checksum mismatch: {target}; remove this cache file and retry")
    request = urllib.request.Request(install["url"], headers={"User-Agent": f"awesome-python-dev/{__version__}"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                if not response.url.startswith("https://codeload.github.com/"):
                    raise ValueError("Unexpected download redirect")
                data = response.read(MAX_ARCHIVE + 1)
            break
        except (urllib.error.URLError, TimeoutError, ConnectionError, ssl.SSLError, http.client.IncompleteRead) as exc:
            permanent = isinstance(exc, urllib.error.HTTPError) and 400 <= exc.code < 500 and exc.code != 429
            if attempt == 2 or permanent:
                raise ValueError(f"Could not download {install['url']}: {exc}") from exc
            time.sleep(attempt + 1)
    if len(data) > MAX_ARCHIVE:
        raise ValueError("Archive exceeds 64 MiB limit")
    if digest(data) != install["sha256"]:
        raise ValueError(f"Archive checksum mismatch for {install['url']}; nothing installed")
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=cache, delete=False) as handle:
        handle.write(data)
        temp = Path(handle.name)
    try:
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
    return data


def skill_files(tool: dict, archive: bytes) -> SkillFiles:
    """Return only the selected subtree plus its original repository license."""
    install = tool["install"]
    if digest(archive) != install["sha256"]:
        raise ValueError("Archive checksum mismatch")
    selected = SkillFiles()
    license_data = None
    total_size = 0
    count = 0
    roots = set()
    prefix = PurePosixPath(install["subdir"])
    wanted_files = set(install["files"]) if install["type"] == "rules" else None
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
            for member in tar:
                count += 1
                path = PurePosixPath(member.name)
                if path.is_absolute() or ".." in path.parts or "\\" in member.name or ":" in member.name:
                    raise ValueError("Unsafe path in upstream archive")
                if not path.parts:
                    continue
                roots.add(path.parts[0])
                if len(roots) != 1:
                    raise ValueError("Archive must have one root directory")
                total_size += member.size
                if count > MAX_FILES or total_size > MAX_EXPANDED:
                    raise ValueError("Archive exceeds extraction limits")
                relative = PurePosixPath(*path.parts[1:])
                in_subtree = relative.is_relative_to(prefix)
                selected_file = in_subtree and (wanted_files is None or str(relative.relative_to(prefix)) in wanted_files)
                wanted = selected_file or str(relative) == install["license_path"]
                if not wanted or member.isdir():
                    continue
                if not member.isfile():
                    raise ValueError("Links and special files are not allowed in skill bundles")
                handle = tar.extractfile(member)
                if handle is None:
                    raise ValueError("Unreadable archive member")
                content = handle.read()
                if str(relative) == install["license_path"]:
                    license_data = content
                else:
                    key = str(relative.relative_to(prefix))
                    if key in selected:
                        raise ValueError(f"Duplicate archive member: {key}")
                    selected[key] = content
                    selected.modes[key] = 0o700 if member.mode & 0o111 else 0o600
    except tarfile.TarError as exc:
        raise ValueError(f"Invalid skill archive: {exc}") from exc
    required = wanted_files if wanted_files is not None else {"SKILL.md"}
    if not required.issubset(selected) or license_data is None:
        raise ValueError(f"{tool['id']}: required upstream files or license not found")
    selected["UPSTREAM-LICENSE"] = license_data
    selected["UPSTREAM.md"] = (
        f"# Upstream attribution\n\nSource: https://github.com/{tool['repository']}\n\n"
        f"Commit: {install['ref']}\n\nPath: {install['subdir']}\n\n"
        f"Archive SHA-256: {install['sha256']}\n\n"
        "Original license: UPSTREAM-LICENSE. Installed by awesome-python-dev.\n"
    ).encode()
    return selected

import io
import json
import os
import tarfile

import pytest

from awesome_python_dev import installer
from awesome_python_dev.adapters import AGENTS, read_mcp
from awesome_python_dev.catalog import load_catalog, select_tools, validate_catalog
from awesome_python_dev.cli import main
from awesome_python_dev.downloads import digest, skill_files


def make_archive(extra=None):
    output = io.BytesIO()
    entries = {"repo/skills/demo/SKILL.md": b"---\nname: demo\ndescription: Demo\n---\nTest",
               "repo/skills/demo/references/detail.md": b"Details", "repo/LICENSE": b"MIT",
               "repo/skills/demo/example.sh": b"#!/bin/sh\necho test\n"}
    entries.update(extra or {})
    with tarfile.open(fileobj=output, mode="w:gz") as tar:
        for name, content in entries.items():
            member = tarfile.TarInfo(name)
            member.mode = 0o755 if name.endswith(".sh") else 0o644
            if content is None:
                member.type = tarfile.SYMTYPE
                member.linkname = "/etc/passwd"
                tar.addfile(member)
            else:
                member.size = len(content)
                tar.addfile(member, io.BytesIO(content))
    return output.getvalue()


@pytest.fixture
def toolkit(monkeypatch):
    archive = make_archive()
    skill = {"id": "demo", "repository": "owner/repo", "install": {
        "type": "skill", "ref": "a" * 40, "sha256": digest(archive),
        "subdir": "skills/demo", "license_path": "LICENSE"}}
    mcp = {"id": "demo-mcp", "install": {"type": "mcp", "command": "npx",
            "args": ["-y", "demo-mcp@1.2.3"]}}
    monkeypatch.setattr(installer, "download", lambda _: archive)
    return [skill, mcp]


@pytest.mark.parametrize("agent_id", AGENTS)
def test_install_repeat_remove_preserves_unrelated(tmp_path, toolkit, agent_id):
    agent = AGENTS[agent_id]
    config = tmp_path / agent.mcp_path
    config.parent.mkdir(parents=True, exist_ok=True)
    baseline = b'# keep this comment\nmodel = "example"\n' if agent_id == "codex" else b'{"custom": {"keep": true}}\n'
    config.write_bytes(baseline)
    plan = installer.installation_plan(tmp_path, [agent_id], toolkit, "starter")
    assert installer.apply_plan(plan) > 0
    assert (tmp_path / agent.skills_dir / "demo/UPSTREAM-LICENSE").read_bytes() == b"MIT"
    if os.name != "nt":
        assert (tmp_path / agent.skills_dir / "demo/example.sh").stat().st_mode & 0o100
    assert read_mcp(agent_id, config.read_bytes())["apd-demo-mcp"]["command"] == ("cmd" if os.name == "nt" else "npx")
    second = installer.installation_plan(tmp_path, [agent_id], toolkit, "starter")
    assert installer.apply_plan(second) == 0
    extra = tmp_path / agent.skills_dir / "demo/user.md"
    extra.write_text("mine")
    installer.apply_plan(installer.removal_plan(tmp_path))
    assert extra.read_text() == "mine"
    assert not (tmp_path / agent.skills_dir / "demo/SKILL.md").exists()
    assert not read_mcp(agent_id, config.read_bytes())
    assert "keep" in config.read_text()
    if agent_id == "codex":
        assert "# keep this comment" in config.read_text()


def test_all_agents_and_additive_init(tmp_path, toolkit):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], toolkit, "starter"))
    installer.apply_plan(installer.installation_plan(tmp_path, ["claude"], toolkit, "starter"))
    assert set(installer.load_manifest(tmp_path)["agents"]) == {"codex", "claude"}
    installer.apply_plan(installer.installation_plan(tmp_path, list(AGENTS), toolkit, "starter"))
    assert len(installer.load_manifest(tmp_path)["agents"]) == 5


def test_dry_run_never_downloads_or_writes(tmp_path, toolkit, monkeypatch):
    def forbidden(_):
        pytest.fail("dry run called download")
    monkeypatch.setattr(installer, "download", forbidden)
    plan = installer.installation_plan(tmp_path, list(AGENTS), toolkit, "starter", dry_run=True)
    assert len(plan.summary) == 10
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("operation", ["init", "remove"])
def test_modified_skill_aborts_whole_plan(tmp_path, toolkit, operation):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], toolkit, "starter"))
    path = tmp_path / ".agents/skills/demo/SKILL.md"
    path.write_text("my edit")
    with pytest.raises(ValueError, match="Locally modified"):
        if operation == "init":
            installer.installation_plan(tmp_path, ["codex"], toolkit, "starter")
        else:
            installer.removal_plan(tmp_path)
    assert path.read_text() == "my edit"


@pytest.mark.parametrize("agent_id", AGENTS)
def test_mcp_customization_prevents_removal(tmp_path, toolkit, agent_id):
    installer.apply_plan(installer.installation_plan(tmp_path, [agent_id], toolkit, "starter"))
    path = tmp_path / AGENTS[agent_id].mcp_path
    original = path.read_text()
    path.write_text(original.replace("demo-mcp@1.2.3", "demo-mcp@9.9.9"))
    with pytest.raises(ValueError, match="Locally modified MCP"):
        installer.removal_plan(tmp_path)
    assert "9.9.9" in path.read_text()


def test_unmanaged_skill_and_mcp_not_adopted(tmp_path, toolkit):
    path = tmp_path / ".agents/skills/demo"
    path.mkdir(parents=True)
    (path / "mine").write_text("keep")
    with pytest.raises(ValueError, match="Unmanaged skill"):
        installer.installation_plan(tmp_path, ["codex"], toolkit, "starter")
    config = tmp_path / ".mcp.json"
    config.write_text('{"mcpServers":{"apd-demo-mcp":{"command":"npx","args":["-y","demo-mcp@1.2.3"]}}}')
    with pytest.raises(ValueError, match="Unmanaged MCP"):
        installer.installation_plan(tmp_path, ["claude"], toolkit, "starter")
    assert not (tmp_path / ".claude").exists()


def test_malformed_or_jsonc_config_not_overwritten(tmp_path, toolkit):
    (tmp_path / "opencode.jsonc").write_text("// my config")
    with pytest.raises(ValueError, match="opencode.jsonc"):
        installer.installation_plan(tmp_path, ["opencode"], toolkit, "starter")
    (tmp_path / ".mcp.json").write_text('{"mcpServers":')
    with pytest.raises(ValueError, match="Cannot parse"):
        installer.installation_plan(tmp_path, ["claude"], toolkit, "starter")


def test_skill_only_install_does_not_parse_mcp_config(tmp_path, toolkit):
    (tmp_path / "opencode.jsonc").write_text("// my config")
    (tmp_path / ".mcp.json").write_text("// my JSONC")
    installer.apply_plan(installer.installation_plan(tmp_path, ["claude", "opencode"], toolkit[:1], "starter"))
    assert (tmp_path / ".mcp.json").read_text() == "// my JSONC"
    assert not (tmp_path / "opencode.json").exists()


def test_symlink_escape_and_manifest_path_traversal(tmp_path, toolkit):
    target = tmp_path / "outside"
    target.mkdir()
    try:
        (tmp_path / ".agents").symlink_to(target, target_is_directory=True)
    except OSError:
        pytest.skip("Symlink creation unavailable on this platform")
    with pytest.raises(ValueError, match="symlink"):
        installer.installation_plan(tmp_path, ["codex"], toolkit, "starter")
    assert list(target.iterdir()) == []
    with pytest.raises(ValueError, match="Unsafe"):
        installer.safe_path(tmp_path, "../outside")


@pytest.mark.parametrize("failure", [OSError, KeyboardInterrupt])
def test_write_failure_rolls_back(tmp_path, monkeypatch, failure):
    (tmp_path / "one").write_bytes(b"original")
    plan = installer.Plan(tmp_path)
    plan.put("one", b"new")
    plan.put("two", b"new")
    original_write = installer.atomic_write
    def faulty(path, data, mode=None):
        if path == tmp_path / "two":
            raise failure("simulated disk error")
        original_write(path, data, mode)
    monkeypatch.setattr(installer, "atomic_write", faulty)
    with pytest.raises(failure, match="simulated"):
        installer.apply_plan(plan)
    assert (tmp_path / "one").read_bytes() == b"original"
    assert not (tmp_path / "two").exists()


def test_changed_after_plan_not_overwritten(tmp_path):
    plan = installer.Plan(tmp_path)
    plan.put("file", b"planned")
    (tmp_path / "file").write_bytes(b"concurrent edit")
    with pytest.raises(ValueError, match="changed during planning"):
        installer.apply_plan(plan)
    assert (tmp_path / "file").read_bytes() == b"concurrent edit"


def test_lock_rejects_concurrent_install(tmp_path):
    with installer.project_lock(tmp_path):
        with pytest.raises(ValueError, match="Another installation"):
            with installer.project_lock(tmp_path):
                pytest.fail("Lock unexpectedly acquired")
    assert not (tmp_path / ".awesome-python-dev/install.lock").exists()


@pytest.mark.parametrize("extra", [{"repo/../escape": b"bad"}, {"repo/skills/demo/link": None}])
def test_bad_archives_rejected(toolkit, extra):
    archive = make_archive(extra)
    tool = toolkit[0]
    tool["install"]["sha256"] = digest(archive)
    with pytest.raises(ValueError):
        skill_files(tool, archive)


def test_checksum_rejected_before_archive_read(toolkit):
    with pytest.raises(ValueError, match="checksum"):
        skill_files(toolkit[0], b"corrupt")


def test_catalog_has_valid_pins_and_profiles():
    catalog = load_catalog()
    for profile in catalog["profiles"]:
        assert select_tools(catalog, profile)
    first = catalog["tools"][0]
    first["install"]["ref"] = "main"
    with pytest.raises(ValueError, match="Unpinned"):
        validate_catalog(catalog)


def test_cli_catalog_and_preview(tmp_path, capsys):
    assert main(["list", "--json"]) == 0
    assert len(json.loads(capsys.readouterr().out)["tools"]) >= 15
    assert main(["init", "--agents", "all", "--dry-run", "--path", str(tmp_path)]) == 0
    assert "Preview only" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []
    assert main(["init", "--agents", "invalid", "--path", str(tmp_path)]) == 1
    assert "Unknown agents" in capsys.readouterr().err


def test_doctor_reports_missing_and_modified(tmp_path, toolkit, monkeypatch):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], toolkit, "starter"))
    monkeypatch.setattr(installer.shutil, "which", lambda _: None)
    messages, ok = installer.doctor(tmp_path)
    assert not ok
    assert any("runtime npx" in msg for msg in messages)
    (tmp_path / ".agents/skills/demo/SKILL.md").unlink()
    assert not installer.doctor(tmp_path)[1]


def test_repeat_init_preserves_comments_in_owned_table(tmp_path, toolkit):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], toolkit, "starter"))
    path = tmp_path / ".codex/config.toml"
    path.write_text(path.read_text().replace('command = "npx"', 'command = "npx" # user note'))
    before = path.read_bytes()
    plan = installer.installation_plan(tmp_path, ["codex"], toolkit, "starter")
    assert installer.apply_plan(plan) == 0
    assert path.read_bytes() == before


def test_windows_path_and_runtime(tmp_path):
    with pytest.raises(ValueError, match="Unsafe"):
        installer.safe_path(tmp_path, ".claude/skills/demo/C:/outside")
    install = {"command": "npx", "args": ["-y", "demo@1.2.3"]}
    assert installer.runtime_config(install, windows=True) == {
        "command": "cmd", "args": ["/c", "npx", "-y", "demo@1.2.3"]}
    assert installer.runtime_config(install, windows=False) == install


@pytest.mark.skipif(os.name != "nt", reason="Windows junction regression")
def test_windows_junction_cannot_escape_project(tmp_path):
    import subprocess

    project = tmp_path / "project"
    outside = tmp_path / "outside"
    project.mkdir()
    outside.mkdir()
    result = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(project / ".agents"), str(outside)],
        capture_output=True,
    )
    if result.returncode:
        pytest.skip("Junction creation unavailable")
    try:
        with pytest.raises(ValueError, match="filesystem link|symlink"):
            installer.safe_path(project, ".agents/skills/demo/SKILL.md")
    finally:
        (project / ".agents").rmdir()

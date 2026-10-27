import copy
import io
import json
import tarfile

import pytest

from awesome_python_dev import installer
from awesome_python_dev.adapters import AGENTS, read_mcp
from awesome_python_dev.catalog import load_catalog, select_tools, validate_catalog
from awesome_python_dev.downloads import digest
from awesome_python_dev.rules import START_MARKER, extract_activation


def pack(tool_id="demo-rules", body=b"# Guidance\nReview your changes.\n", globs=None):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in {"repo/rules/demo/conventions.md": body, "repo/LICENSE": b"MIT"}.items():
            member = tarfile.TarInfo(name)
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    data = stream.getvalue()
    tool = {
        "id": tool_id, "name": "Demo Rules", "kind": "rules", "category": "engineering",
        "repository": "example/rules", "homepage": "https://github.com/example/rules",
        "install": {
            "type": "rules", "subdir": "rules/demo", "license_path": "LICENSE",
            "files": ["conventions.md"], "globs": globs or [], "ref": "a" * 40,
            "url": "https://codeload.github.com/example/rules/tar.gz/" + "a" * 40,
            "sha256": digest(data),
        },
    }
    return tool, data


@pytest.fixture
def bundle(monkeypatch):
    tool, data = pack()
    monkeypatch.setattr(installer, "download", lambda _: data)
    return tool


@pytest.mark.parametrize("agent", AGENTS)
def test_rule_install_repeat_doctor_remove_preserves_instructions(tmp_path, bundle, agent):
    original = b"# Project rules\r\nKeep this exact text without a final newline"
    path = tmp_path / "AGENTS.md"
    path.write_bytes(original)
    installer.apply_plan(installer.installation_plan(tmp_path, [agent], [bundle], "demo"))
    manifest = installer.load_manifest(tmp_path)
    record = manifest["agents"][agent]["rules"]["demo-rules"]
    assert record["source_files"]["conventions.md"].endswith("/demo-rules/conventions.md")
    assert installer.doctor(tmp_path)[1]
    if agent in {"codex", "opencode"}:
        assert path.read_bytes().startswith(original)
        assert extract_activation(path.read_bytes())
    else:
        assert path.read_bytes() == original
        assert any(not file.startswith(".awesome-python-dev/") for file in record["files"])
    repeated = installer.installation_plan(tmp_path, [agent], [bundle], "demo")
    assert installer.apply_plan(repeated) == 0
    installer.apply_plan(installer.removal_plan(tmp_path))
    assert path.read_bytes() == original
    assert not (tmp_path / ".awesome-python-dev/rules/demo-rules/conventions.md").exists()


def test_shared_rules_are_deduplicated_and_surrounding_edits_survive(tmp_path, bundle):
    original = b"# Existing user instructions"
    path = tmp_path / "AGENTS.md"
    path.write_bytes(original)
    installer.apply_plan(installer.installation_plan(tmp_path, ["opencode"], [bundle], "demo"))
    path.write_bytes(path.read_bytes() + b"\nUser-added footer\n")
    installer.apply_plan(installer.installation_plan(tmp_path, list(AGENTS), [bundle], "demo"))
    assert path.read_bytes().count(START_MARKER) == 1
    assert installer.doctor(tmp_path)[1]
    assert installer.apply_plan(installer.installation_plan(tmp_path, list(AGENTS), [bundle], "demo")) == 0
    installer.apply_plan(installer.removal_plan(tmp_path))
    assert path.read_bytes() == original + b"\nUser-added footer\n"


def test_generated_agents_file_removed_but_original_empty_file_kept(tmp_path, bundle):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], [bundle], "demo"))
    installer.apply_plan(installer.removal_plan(tmp_path))
    assert not (tmp_path / "AGENTS.md").exists()
    (tmp_path / "AGENTS.md").write_bytes(b"")
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], [bundle], "demo"))
    installer.apply_plan(installer.removal_plan(tmp_path))
    assert (tmp_path / "AGENTS.md").read_bytes() == b""


@pytest.mark.parametrize("operation", ["init", "remove"])
def test_modified_activation_blocks_changes(tmp_path, bundle, operation):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], [bundle], "demo"))
    path = tmp_path / "AGENTS.md"
    path.write_bytes(path.read_bytes().replace(b"Review your changes.", b"My customized review."))
    with pytest.raises(ValueError, match="Locally modified"):
        if operation == "init":
            installer.installation_plan(tmp_path, ["codex"], [bundle], "demo")
        else:
            installer.removal_plan(tmp_path)
    assert b"My customized review." in path.read_bytes()
    assert not installer.doctor(tmp_path)[1]


def test_native_rule_edits_and_unmanaged_collisions_protected(tmp_path, bundle):
    path = tmp_path / ".claude/rules/apd-demo-rules/conventions.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"my own rule")
    with pytest.raises(ValueError, match="Unmanaged rule file"):
        installer.installation_plan(tmp_path, ["claude"], [bundle], "demo")
    assert path.read_bytes() == b"my own rule"
    path.unlink()
    installer.apply_plan(installer.installation_plan(tmp_path, ["claude"], [bundle], "demo"))
    path.write_bytes(b"edited")
    with pytest.raises(ValueError, match="Locally modified"):
        installer.removal_plan(tmp_path)


def test_shadowing_and_instruction_budget_abort_before_writes(tmp_path, monkeypatch, bundle):
    (tmp_path / "AGENTS.override.md").write_text("Override")
    with pytest.raises(ValueError, match="shadows"):
        installer.installation_plan(tmp_path, ["codex"], [bundle], "demo")
    assert not (tmp_path / ".awesome-python-dev").exists()
    (tmp_path / "AGENTS.override.md").unlink()
    huge, archive = pack(body=b"A" * 33000)
    monkeypatch.setattr(installer, "download", lambda _: archive)
    with pytest.raises(ValueError, match="instruction budget"):
        installer.installation_plan(tmp_path, ["claude", "codex"], [huge], "demo")
    assert not list(tmp_path.iterdir())


def test_shared_source_updates_require_all_owners(tmp_path, monkeypatch, bundle):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex", "claude"], [bundle], "demo"))
    changed, archive = pack(body=b"# New guidance\nReview twice.\n")
    monkeypatch.setattr(installer, "download", lambda _: archive)
    with pytest.raises(ValueError, match="all installed agents"):
        installer.installation_plan(tmp_path, ["codex"], [changed], "demo")
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex", "claude"], [changed], "demo"))
    assert b"Review twice." in (tmp_path / "AGENTS.md").read_bytes()
    assert installer.doctor(tmp_path)[1]


def test_dependency_expansion_and_cycles():
    common, _ = pack("common-rules")
    language, _ = pack("python-rules")
    language["requires"] = ["common-rules"]
    catalog = {"schema_version": 2, "tools": [common, language], "profiles": {"python": ["python-rules"]}}
    validate_catalog(catalog)
    assert [t["id"] for t in select_tools(catalog, "python")] == ["common-rules", "python-rules"]
    common["requires"] = ["python-rules"]
    with pytest.raises(ValueError, match="Circular"):
        validate_catalog(catalog)
    with pytest.raises(ValueError, match="Circular"):
        select_tools(catalog, "python")


def test_pinned_lsp_source_and_absolute_project_path(tmp_path):
    catalog = load_catalog()
    tool = next(t for t in catalog["tools"] if t["id"] == "serena")
    installer.apply_plan(installer.installation_plan(tmp_path, list(AGENTS), [tool], "lsp"))
    for agent_id, agent in AGENTS.items():
        config = read_mcp(agent_id, (tmp_path / agent.mcp_path).read_bytes())["apd-serena"]
        args = config["args"]
        assert args[args.index("--project") + 1] == str(tmp_path.resolve())
        assert "{project}" not in args
        assert any(tool["install"]["ref"] in arg for arg in args)
    installer.apply_plan(installer.removal_plan(tmp_path))
    invalid = copy.deepcopy(catalog)
    next(t for t in invalid["tools"] if t["id"] == "serena")["install"]["ref"] = "main"
    with pytest.raises(ValueError, match="Unpinned MCP Git"):
        validate_catalog(invalid)


def test_old_manifest_upgrade_without_rules(tmp_path):
    state = tmp_path / ".awesome-python-dev"
    state.mkdir()
    (state / "manifest.json").write_text(json.dumps({"schema_version": 1, "agents": {}}))
    tool = {"id": "example", "install": {"type": "mcp", "command": "npx", "args": ["example@1.0.0"]}}
    installer.apply_plan(installer.installation_plan(tmp_path, ["claude"], [tool], "demo"))
    assert installer.load_manifest(tmp_path)["schema_version"] == 2
    installer.apply_plan(installer.removal_plan(tmp_path))


def test_doctor_detects_oversized_user_instructions(tmp_path, bundle):
    installer.apply_plan(installer.installation_plan(tmp_path, ["codex"], [bundle], "demo"))
    path = tmp_path / "AGENTS.md"
    path.write_bytes(b"x" * 33000 + path.read_bytes())
    messages, ok = installer.doctor(tmp_path)
    assert not ok
    assert any("instruction budget" in line for line in messages)


def test_moved_project_lsp_binding_is_diagnosed_and_repaired(tmp_path):
    root = tmp_path / "original"
    root.mkdir()
    tool = next(t for t in load_catalog()["tools"] if t["id"] == "serena")
    installer.apply_plan(installer.installation_plan(root, ["codex"], [tool], "lsp"))
    moved = root.rename(tmp_path / "moved")
    messages, ok = installer.doctor(moved)
    assert not ok
    assert any("project path changed" in line for line in messages)
    installer.apply_plan(installer.installation_plan(moved, ["codex"], [tool], "lsp"))
    assert not any("project path changed" in line for line in installer.doctor(moved)[0])

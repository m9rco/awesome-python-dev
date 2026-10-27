import copy

import pytest

from awesome_python_dev.rules import (
    DEFAULT_MAX_AGENTS_BYTES,
    END_MARKER,
    START_MARKER,
    build_activation,
    extract_activation,
    render_activation,
    render_rules,
    rule_roots,
)


@pytest.fixture
def pack():
    tool = {
        "id": "ecc-python-rules", "name": "Python conventions", "repository": "affaan-m/ECC",
        "install": {"type": "rules", "ref": "a" * 40, "subdir": "rules/python",
                    "files": ["coding-style.md"], "globs": ["**/*.py", "**/*.pyi"]},
    }
    files = {
        "coding-style.md": b'---\npaths:\n  - "**/*.py"\n---\n# Python rules\n\nUse typed functions.\n\nSee [common](../common/coding-style.md).\nSee skill: `python-patterns`.\n',
        "UPSTREAM-LICENSE": b"MIT upstream license\n",
        "UPSTREAM.md": b"Pinned original source attribution\n",
    }
    return tool, files


@pytest.mark.parametrize("agent", ["claude", "codex", "cursor", "vscode", "opencode"])
def test_originals_preserved_for_every_agent(pack, agent):
    tool, files = pack
    result = render_rules(agent, tool, files)
    shared = rule_roots(agent, tool["id"])[0]
    for path, content in files.items():
        assert result[f"{shared}/{path}"] == content
    assert b"Original files" in result[f"{shared}/APD-ADAPTATION.txt"]
    if agent in {"codex", "opencode"}:
        assert len(result) == len(files) + 1


def test_native_metadata_and_relocated_links(pack):
    tool, files = pack
    claude = render_rules("claude", tool, files)[".claude/rules/apd-ecc-python-rules/coding-style.md"]
    cursor = render_rules("cursor", tool, files)[".cursor/rules/apd-ecc-python-rules/coding-style.mdc"]
    vscode = render_rules("vscode", tool, files)[".github/instructions/apd-ecc-python-rules/coding-style.instructions.md"]
    assert claude.startswith(b'---\npaths:\n  - "**/*.py"\n  - "**/*.pyi"\n---\n')
    assert b'globs: "**/*.py,**/*.pyi"\nalwaysApply: false' in cursor
    assert b'applyTo: "**/*.py,**/*.pyi"' in vscode
    for result in [claude, cursor, vscode]:
        assert result.count(b"paths:") <= 1
        assert b"../common/coding-style.md" not in result
        assert ("/blob/" + "a" * 40 + "/rules/common/coding-style.md").encode() in result
        assert b"optional upstream reference [python-patterns]" in result
        assert b"does not install subagents, hooks, commands, or global settings" in result


def test_global_rules_are_native_always_on(pack):
    tool, files = pack
    tool["install"]["globs"] = []
    claude = render_rules("claude", tool, files)[".claude/rules/apd-ecc-python-rules/coding-style.md"]
    cursor = render_rules("cursor", tool, files)[".cursor/rules/apd-ecc-python-rules/coding-style.mdc"]
    vscode = render_rules("vscode", tool, files)[".github/instructions/apd-ecc-python-rules/coding-style.instructions.md"]
    assert not claude.startswith(b"---")
    assert b"alwaysApply: true" in cursor
    assert b'applyTo: "**"' in vscode


def test_glob_strings_keep_brace_groups(pack):
    tool, files = pack
    tool["install"]["globs"] = "**/*.{ts,tsx},**/*.js"
    result = render_rules("claude", tool, files)[".claude/rules/apd-ecc-python-rules/coding-style.md"]
    assert b'  - "**/*.{ts,tsx}"\n  - "**/*.js"\n' in result


def test_ecc_specific_adaptations_do_not_change_other_repositories(pack):
    tool, files = pack
    files["coding-style.md"] = (
        b"# Workflow\nUse **planner** agent to create implementation plan\n"
        b"Use **tdd-guide** agent\nUse **security-reviewer** agent\n"
        b"Use **code-reviewer** agent immediately after writing code\n"
        b"- **e2e-runner** - Playwright E2E testing specialist\n"
        b"- See hooks for automatic detection\n## Custom Hooks Pattern\n"
        b"Use React hooks.\n"
    )
    result = build_activation([(tool, files)])
    assert b"**planner**" not in result
    assert b"**tdd-guide**" not in result
    assert b"**security-reviewer**" not in result
    assert b"**code-reviewer**" not in result
    assert b"**e2e-runner**" not in result
    assert b"See hooks for automatic detection" not in result
    assert b"## Custom Hooks Pattern\nUse React hooks." in result
    tool["repository"] = "another/project"
    result = build_activation([(tool, files)])
    assert b"Use **planner** agent" in result
    assert b"See hooks for automatic detection" in result


def test_code_examples_keep_literal_markdown_links(pack):
    tool, files = pack
    files["coding-style.md"] = b"# Demo\n```md\n[example](../example.md)\n```\nSee [source](./other.md).\n"
    result = build_activation([(tool, files)])
    assert b"[example](../example.md)" in result
    assert b"[source](https://github.com/affaan-m/ECC/blob/" in result


@pytest.mark.parametrize("outside", [b"", b"# User instructions", b"# User instructions\r\n\r\n", b"\xef\xbb\xbf# Notes\n"])
def test_activation_preserves_original_bytes_on_install_repeat_and_remove(pack, outside):
    desired = build_activation([pack])
    installed = render_activation(outside, desired)
    assert installed.startswith(outside)
    assert extract_activation(installed) == desired
    assert render_activation(installed, desired, desired) == installed
    assert render_activation(installed, None, desired) == outside
    assert render_activation(None, None) is None


def test_activation_update_preserves_surrounding_user_edits(pack):
    block = build_activation([pack])
    original = b"User prefix without final newline"
    installed = render_activation(original, block) + b"\r\nUser suffix\r\n"
    new_pack = copy.deepcopy(pack)
    new_pack[1]["coding-style.md"] += b"\nAdd focused tests.\n"
    replacement = build_activation([new_pack])
    updated = render_activation(installed, replacement, block)
    assert updated == original + replacement + b"\r\nUser suffix\r\n"
    assert render_activation(updated, None, replacement) == original + b"\r\nUser suffix\r\n"


def test_unknown_edited_missing_and_duplicate_blocks_refused(pack):
    block = build_activation([pack])
    with pytest.raises(ValueError, match="Unmanaged"):
        render_activation(block, block)
    modified = block.replace(b"Use typed functions.", b"My local changes.")
    with pytest.raises(ValueError, match="Locally modified"):
        render_activation(modified, block, block)
    with pytest.raises(ValueError, match="missing"):
        render_activation(b"User removed block", block, block)
    for malformed in [block + block, block.replace(END_MARKER, b""), block[1:], block[:-1], START_MARKER + END_MARKER]:
        with pytest.raises(ValueError):
            extract_activation(malformed)


def test_combined_size_guard_and_unlimited_opencode_removal(pack):
    block = build_activation([pack])
    prefix = b"x" * (DEFAULT_MAX_AGENTS_BYTES - len(block))
    assert len(render_activation(prefix, block)) == DEFAULT_MAX_AGENTS_BYTES
    with pytest.raises(ValueError, match="choose fewer"):
        render_activation(prefix + b"x", block)
    large = render_activation(prefix + b"x", block, max_bytes=None)
    assert render_activation(large, None, block) == prefix + b"x"


def test_shared_activation_deduplicates_both_agents_and_rejects_conflicts(pack):
    block = build_activation([pack])
    assert build_activation([pack, pack]) == block
    assert block.count(b"### Python conventions") == 1
    assert b"Scope: apply the following guidance only to files matching `**/*.py`, `**/*.pyi`." in block
    different = copy.deepcopy(pack)
    different[1]["coding-style.md"] += b"\nDifferent guidance.\n"
    with pytest.raises(ValueError, match="Conflicting"):
        build_activation([pack, different])
    assert build_activation([]) is None


def test_invalid_rule_sources_and_output_collisions_fail_before_writes(pack):
    tool, files = pack
    for source in [b"\xff", b"---\npaths: bad", b"# NUL\x00", START_MARKER, b"\n"]:
        broken = dict(files, **{"coding-style.md": source})
        with pytest.raises(ValueError):
            render_rules("codex", tool, broken)
    for name in ["../outside.md", "C:/outside.md", "nested/../bad.md", "/absolute.md"]:
        broken = dict(files, **{name: b"# Bad"})
        with pytest.raises(ValueError):
            render_rules("cursor", tool, broken)
    with pytest.raises(ValueError, match="license"):
        render_rules("codex", tool, {"coding-style.md": b"# Rules"})
    with pytest.raises(ValueError, match="Unsupported"):
        render_rules("unknown", tool, files)
    collision_tool = copy.deepcopy(tool)
    collision_tool["install"]["files"] = ["coding-style.md", "coding-style.mdc"]
    collision_files = dict(files, **{"coding-style.mdc": b"# Other"})
    with pytest.raises(ValueError, match="collision"):
        render_rules("cursor", collision_tool, collision_files)

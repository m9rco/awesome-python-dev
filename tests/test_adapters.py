"""Adapter compatibility and data preservation regressions."""

import json
import unittest

import tomlkit

from awesome_python_dev.adapters import AGENTS, read_mcp, render_mcp

SERVER = {"command": "npx", "args": ["-y", "example-mcp@1.2.3"], "env": {"TOKEN": "example"}}


class AdapterTests(unittest.TestCase):
    def test_all_agents_roundtrip_and_idempotence(self):
        for agent_id in AGENTS:
            with self.subTest(agent=agent_id):
                result = render_mcp(agent_id, None, {"apd-example": SERVER})
                self.assertEqual(read_mcp(agent_id, result), {"apd-example": SERVER})
                self.assertEqual(render_mcp(agent_id, result, {"apd-example": SERVER}), result)
                self.assertEqual(read_mcp(agent_id, render_mcp(agent_id, result, {}, remove={"apd-example"})), {})

    def test_native_formats(self):
        for agent_id in ("claude", "cursor", "vscode"):
            data = json.loads(render_mcp(agent_id, None, {"test": SERVER}))
            native = data[AGENTS[agent_id].root_key]["test"]
            self.assertEqual(native["command"], "npx")
            self.assertEqual(native["args"], SERVER["args"])
            if agent_id in {"claude", "vscode"}:
                self.assertEqual(native["type"], "stdio")
        native = json.loads(render_mcp("opencode", None, {"test": SERVER}))["mcp"]["test"]
        self.assertEqual(native, {"type": "local", "enabled": True, "command": ["npx", *SERVER["args"]], "environment": SERVER["env"]})

    def test_preserves_remote_and_unrelated_json_settings(self):
        original = {"model": "custom", "mcp": {"remote": {"type": "remote", "url": "https://example.com/mcp", "enabled": False}}}
        result = render_mcp("opencode", json.dumps(original).encode(), {"apd-example": SERVER})
        parsed = json.loads(result)
        self.assertEqual(parsed["model"], "custom")
        self.assertEqual(parsed["mcp"]["remote"], original["mcp"]["remote"])
        removed = render_mcp("opencode", result, {}, remove={"apd-example"})
        self.assertEqual(json.loads(removed), original)

    def test_toml_preserves_comments_and_other_tables(self):
        original = b'# my settings\nmodel = "custom" # keep this\n\n[mcp_servers.personal]\nurl = "https://example.com"\n\n[projects."/tmp/project"]\ntrust_level = "trusted"\n'
        result = render_mcp("codex", original, {"apd-example": SERVER})
        self.assertIn(b'# my settings\nmodel = "custom" # keep this', result)
        parsed = tomlkit.parse(result.decode())
        self.assertEqual(parsed["projects"]["/tmp/project"]["trust_level"], "trusted")
        self.assertEqual(parsed["mcp_servers"]["personal"]["url"], "https://example.com")
        removed = render_mcp("codex", result, {}, remove={"apd-example"})
        self.assertEqual(tomlkit.parse(removed.decode()).unwrap(), tomlkit.parse(original.decode()).unwrap())

    def test_conflict_and_explicit_owned_refresh(self):
        for agent_id in AGENTS:
            with self.subTest(agent=agent_id):
                original = render_mcp(agent_id, None, {"owned": SERVER})
                newer = {"command": "uvx", "args": ["example==2.0.0"]}
                with self.assertRaisesRegex(ValueError, "already exists"):
                    render_mcp(agent_id, original, {"owned": newer})
                result = render_mcp(agent_id, original, {"owned": newer}, remove={"owned"})
                self.assertEqual(read_mcp(agent_id, result), {"owned": newer})

    def test_user_edits_visible_in_ownership_comparison(self):
        for agent_id in AGENTS:
            with self.subTest(agent=agent_id):
                raw = render_mcp(agent_id, None, {"owned": SERVER})
                agent = AGENTS[agent_id]
                parsed = tomlkit.parse(raw.decode()) if agent.format == "toml" else json.loads(raw)
                parsed[agent.root_key]["owned"]["cwd"] = "/my/custom/path"
                modified = (tomlkit.dumps(parsed) if agent.format == "toml" else json.dumps(parsed)).encode()
                self.assertEqual(read_mcp(agent_id, modified)["owned"]["cwd"], "/my/custom/path")
                with self.assertRaisesRegex(ValueError, "already exists"):
                    render_mcp(agent_id, modified, {"owned": SERVER})
        original = json.loads(render_mcp("opencode", None, {"owned": SERVER}))
        original["mcp"]["owned"]["enabled"] = False
        self.assertIs(read_mcp("opencode", json.dumps(original).encode())["owned"]["enabled"], False)

    def test_rejects_invalid_configs_and_duplicate_keys(self):
        for raw in [b'{ // comment\n}', b'{"servers":{},}', b'{"servers":{},"servers":{}}', b'{"servers":null}', b'[]', b'{"servers":{"bad":3}}', b'{"x":NaN}', b'\xff', b'']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                render_mcp("vscode", raw, {"owned": SERVER})
        with self.assertRaises(ValueError):
            render_mcp("codex", b'[mcp_servers\n', {"owned": SERVER})
        with self.assertRaises(ValueError):
            render_mcp("codex", b'mcp_servers = "wrong"\n', {"owned": SERVER})

    def test_invalid_new_servers(self):
        for server in [{"command": ""}, {"command": "x", "args": "bad"}, {"command": "x", "env": {"a": 1}}, {"url": "https://example.com"}, {"command": "x", "cwd": ".."}]:
            with self.subTest(server=server), self.assertRaises(ValueError):
                render_mcp("claude", None, {"bad": server})

    def test_no_op_keeps_bytes(self):
        original = b'{"servers":{}, "custom": 1}\n'
        self.assertEqual(render_mcp("vscode", original, {}, remove={"missing"}), original)
        self.assertEqual(read_mcp("codex", None), {})
        with self.assertRaisesRegex(ValueError, "Unknown agent"):
            render_mcp("unknown", None, {})


if __name__ == "__main__":
    unittest.main()

# Agent compatibility

The installer writes **project-local** files. It does not modify home-directory
configuration or install coding agent applications. Paths and native formats
were checked against the primary documentation on 2026-10-27.

| CLI ID | Agent | Skills directory | MCP configuration | MCP format |
| --- | --- | --- | --- | --- |
| `claude` | Claude Code | `.claude/skills/` | `.mcp.json` | JSON `mcpServers`, stdio |
| `codex` | Codex | `.agents/skills/` | `.codex/config.toml` | TOML `mcp_servers` |
| `cursor` | Cursor | `.cursor/skills/` | `.cursor/mcp.json` | JSON `mcpServers` |
| `vscode` | GitHub Copilot in VS Code | `.github/skills/` | `.vscode/mcp.json` | JSON `servers`, `type: stdio` |
| `opencode` | OpenCode | `.opencode/skills/` | `opencode.json` | JSON `mcp`, `type: local`, command array |

Each skill is a directory containing its original `SKILL.md` and supporting
files. Some agents also discover other agents' directories; installing the same
skill for multiple agents can make duplicate skill names visible in those
clients. Select only the clients needed by the project.

## Loading the installed toolkit

- **Claude Code:** open the project, approve project MCP servers when prompted,
  and inspect `/mcp`. Its project configuration is distinct from the local and
  user settings stored in `~/.claude.json`.
- **Codex:** trust the project through Codex's own interface. Codex ignores
  project MCP configuration in untrusted projects. Skills live in `.agents`,
  while MCP settings live in `.codex`.
- **Cursor:** inspect MCP servers in Customize/settings and review available
  skills. The adapter uses Cursor's native project directories.
- **VS Code:** use Copilot Agent mode and VS Code's MCP controls to start and
  inspect servers. This target configures the editor; it does not configure
  Copilot CLI's MCP settings.
- **OpenCode:** reopen the project and inspect MCP availability. Local commands
  are arrays and environment variables use `environment` in OpenCode's native
  schema.

Agent discovery and client approval are separate from writing valid files.
The test suite verifies configuration generation and preservation; it does not
claim to exercise a live authenticated session in every supported client.

## Merge behavior

The adapters preserve unrelated configuration values and refuse conflicting
server names. TOML edits also preserve comments. JSON files are reformatted on
change. JSON comments, trailing commas, duplicate keys, and malformed input are
rejected before writing. Existing `opencode.jsonc` needs manual reconciliation
before using the `opencode.json` adapter; the installer does not silently create
a competing file.

Only stdio MCP recipes are installed in this release. Existing remote entries
remain untouched. No adapter bypasses client trust prompts, injects credentials,
or enables unrestricted tool permissions.

## Primary documentation

- Claude Code: [skills](https://code.claude.com/docs/en/skills),
  [MCP scopes and configuration](https://code.claude.com/docs/en/mcp).
- Codex: [skill discovery](https://developers.openai.com/codex/skills/),
  [MCP configuration](https://developers.openai.com/codex/mcp/),
  [project trust and configuration precedence](https://developers.openai.com/codex/config-basic/).
- Cursor: [skills](https://cursor.com/docs/skills),
  [MCP configuration](https://cursor.com/docs/mcp).
- VS Code: [agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
  [MCP servers](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- OpenCode: [skills](https://opencode.ai/docs/skills/),
  [MCP servers](https://opencode.ai/docs/mcp-servers/),
  [project configuration](https://opencode.ai/docs/config/).

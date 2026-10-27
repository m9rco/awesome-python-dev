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

## Native project rules

Rule packs provide coding conventions in the host's instruction format. They are
separate from skills and MCP servers. Each source file remains byte-for-byte
intact under `.awesome-python-dev/rules/<pack>/`, alongside its upstream license
and provenance. Active copies use these locations:

| Agent | Active rules | Scope handling |
| --- | --- | --- |
| Claude Code | `.claude/rules/apd-<pack>/**/*.md` | YAML `paths`; omitted for project-wide rules |
| Cursor | `.cursor/rules/apd-<pack>/**/*.mdc` | `globs` with `alwaysApply: false`; project-wide packs use `alwaysApply: true` |
| VS Code Copilot | `.github/instructions/apd-<pack>/**/*.instructions.md` | YAML `applyTo` patterns |
| Codex | One managed block in root `AGENTS.md` | Actual rule text embedded with explicit language/file scopes |
| OpenCode | The same managed block in root `AGENTS.md` | Actual rule text embedded with explicit language/file scopes |

Claude discovers rule Markdown recursively. Cursor requires the `.mdc`
extension. VS Code attaches scoped instructions to matching files in supported
Copilot sessions; it does not use them for inline completion. Codex and OpenCode
receive the complete embedded text, with language scope expressed as instructions
inside the block. Their rule activation does not depend on following a Markdown
link. These formats are described in the official [Claude rules documentation](https://code.claude.com/docs/en/memory#organize-rules-with-clauderules),
[Cursor rules documentation](https://cursor.com/docs/rules), and
[VS Code instructions documentation](https://code.visualstudio.com/docs/agent-customization/custom-instructions).

Codex and OpenCode share one block and one copy of each source pack. Repeated
initialization updates only the installer-owned block. Changes elsewhere in
`AGENTS.md`, including existing line endings, remain unchanged. Missing, edited,
or duplicate managed markers stop updates/removal instead of replacing user
content. A pre-existing unowned marker block is a conflict, even if its contents
match a catalog pack.

Codex's default combined project instruction budget is 32 KiB. The installer
checks the total resulting root `AGENTS.md` and fails before writing when adding
rules would exceed that limit; select fewer language packs or shorten existing
instructions. Common rules plus one language pack fit in an otherwise empty
file, while all language packs together exceed the cap. Global and nested
instructions can consume additional budget. A nonempty `AGENTS.override.md` in
the same directory shadows `AGENTS.md`; the installer does not replace it or
raise Codex's configuration limits. See [Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md/).
OpenCode supports root `AGENTS.md` natively; nearer project instruction files can
change which guidance applies. See [OpenCode rules](https://opencode.ai/docs/rules/).

### ECC portability

The selected ECC rule packs contain some references to the upstream project's
agents and automation. Active copies replace reviewed, exact ECC clauses with
portable planning, code review, testing, and lint steps. They preserve the
project's existing commit-attribution policy and treat upstream skill references
as optional links. Relative source links point to the pinned GitHub commit so
they remain usable after relocation. React hooks and ordinary code examples
are not interpreted as agent automation.

Every active file identifies its pinned source and explains the adaptation.
`APD-ADAPTATION.txt` records the policy beside the unchanged originals. Installing
these rules does not install ECC agents, hooks, slash commands, or global
settings. Restart the target client and inspect its active instructions to
verify discovery in your environment; renderer tests alone do not establish
that an authenticated client session loaded a rule.

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

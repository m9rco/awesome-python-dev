# Changelog

## 0.1.0 — 2026-10-27

Initial release of a curated AI development toolkit and project-local installer.

- 23 curated resources: 5 installable skills, 3 installable MCP servers, 15 reference projects.
- Native adapters for Claude Code, Codex, Cursor, GitHub Copilot in VS Code, and OpenCode.
- `starter`, `python`, and `web` profiles; explicit tool selection; interactive or detected agents.
- `init`, `list`, `agents`, `doctor`, and `remove` commands, with installation/removal previews.
- Commit-pinned skill archives with SHA-256 verification, complete support files, and upstream licenses.
- Exact direct MCP package versions; npm launch commands adapted for Windows.
- Ownership checks, additive installation, local backups, per-file atomic replacement, and rollback on ordinary write failures or interruption.
- English and Chinese documentation, contribution templates, and cross-platform CI.

MCP registration and local integrity checks are separate from live coding-agent validation. Protocol smoke tests cover initialization and tool discovery only; see [research evidence](docs/RESEARCH.md).

# Changelog

## 0.2.0 — 2026-10-27

Expand the collection into skills, native rules, MCP, and LSP tooling for security, engineering, and framework development.

- 54 catalog entries: 20 installable skills, 6 installable rule packs, 3 package-pinned MCP servers, 1 installable Serena LSP bridge, and 24 references.
- 15 selected MIT-licensed ECC skills for security review, coding standards, Python, Django, FastAPI, Spring Boot, frontend/backend development, Go, API design, migrations, and deployment.
- Six ECC rule packs with commit/archive pins, explicit file allowlists, language scopes, original-source preservation, and automatic common-rule dependencies.
- Native rules for Claude Code, Cursor, and VS Code Copilot; one shared managed `AGENTS.md` block for Codex/OpenCode. Preserve outside text, reject conflicts, and guard Codex output against the 32 KiB default instruction limit.
- Eleven profiles: `starter`, `python`, `web`, `engineering`, `security`, `django`, `fastapi`, `springboot`, `typescript`, `golang`, and `lsp`.
- `apd profiles`, `apd list --kind rules`, and `apd list --kind lsp`; updated starter/Python/web profiles include relevant rules.
- Serena v2.1.0 pinned to a full Git commit, with Python 3.13, the LSP backend, a single-project context, and explicit tool interface. The installer resolves the project path in the generated MCP command.
- Native LSP references for Pyright, Python LSP Server, Ruff, TypeScript Language Server, gopls, rust-analyzer, and clangd; security references for Semgrep, Bandit, pip-audit, and Gitleaks.
- Manifest schema 2, with schemas 1 and 2 readable by the new CLI and schema 1 upgraded during `init`.
- GitHub CI/release/stars/issues badges, independent linting, cross-platform wheel smoke checks, and downloadable CI artifacts.

**Upgrade note:** retain the installation manifest and backups. v0.1 cannot manage a schema 2 manifest; use v0.2 or newer after migration. Profiles remain additive, so select the actual project stack instead of accumulating all language rules.

Rule installation provides guidance, without installing ECC hooks/agents or running security scanners. Serena passed MCP initialization and discovery of 22 tools in a temporary Python project; no symbol operations or agent UI sessions were exercised. See [ECC scope and attribution](docs/ECC-MIGRATION.md) and [LSP verification](docs/LSP.md).

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

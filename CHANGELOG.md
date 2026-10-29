# Changelog

## Unreleased

- Agent discovery: generated `llms.txt`, per-page Markdown counterparts, a
  source-attributed JSON catalog and an Agent integration guide. Discovery links
  preserve custom domains and project subpaths; source snapshots are explicitly
  distinguished from the catalog bundled in published runtimes.
- Website build implementation is organized into `scripts/sitegen/` modules,
  retaining the existing build entry point. Added a documentation index,
  architecture map and repository instructions for contributing agents.
- Bilingual README FAQs and GitHub metadata describe actual installation support;
  existing badges are preserved. CI validates discovery links, catalog parity,
  installable/reference boundaries and generated command IDs.

Catalogue additions from the daily candidate review.

- Two pinned skills from `addyosmani/agent-skills` (`code-review-and-quality`,
  `observability-and-instrumentation`) with their archive SHA-256, and three
  reference-only entries: `ty` (Python type checker and language server),
  `agent-lsp` (agent-facing LSP bridge), and `HypothesisWorks/hypothesis`.
- The catalog now has 59 entries: 32 installable resources (22 skills, 6 rule
  packs, 3 MCP servers, and Serena's bridge) and 27 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-10-29 candidate review.

- Two installable MCP servers, both smoke-checked through
  `scripts/smoke_mcp.py`: `code-review-graph` (pinned
  `uvx --from code-review-graph==2.3.9`, 30 tools discovered) and `mcp-tools-py`
  (pinned `uvx --from mcp-tools-py==0.1.10 --with mcp<2`, 17 tools discovered;
  Python lint, test, type, and refactor operations behind one project scope).
- Two reference-only entries: `codebase-memory-mcp`, a native code knowledge
  graph whose npm/PyPI packages are installer wrappers, and `mcpls`, a Rust
  MCP-to-LSP bridge over `rust-analyzer`, `pyright`, and `gopls`.
- The catalog now has 63 entries: 34 installable resources (22 skills, 6 rule
  packs, 5 MCP servers, and Serena's bridge) and 29 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

## npm shell 0.1.1 — 2026-10-28

- Honor HTTP/HTTPS proxy environment variables for GitHub runtime downloads,
  with `NO_PROXY` bypass rules and an explicit opt-out. Requires Node.js 22.21+
  (22.x) or 24.5+ for native proxy support; no npm dependencies were added.
- Publish the inspected npm tarball through GitHub OIDC and verify the exact
  version becomes publicly available with matching integrity.
- The Python package and runtime remain at **0.3.0**.

## 0.3.0 — 2026-10-28

Separate the npm command launcher from the Python toolkit runtime so routine
catalog and installer updates can ship through GitHub Releases.

- A small, dependency-free npm shell with independent versioning, command
  forwarding, verified runtime caching, explicit version pins and offline use.
- A self-contained Python zipapp with the locked `tomlkit` dependency, catalog,
  source provenance and licenses. Requires Python 3.11+ or an existing `uv`.
- Versioned runtime manifests and SHA-256 checksums, with a protocol-1 stable
  channel and independent GitHub runtime/npm publication workflows.
- PyPI distribution and short `uvx awesome-python-dev` / `uv tool install
  awesome-python-dev` entry points; runtime tags publish Python packages while
  npm shell tags publish only the launcher.
- Static GitHub Pages catalog with English and Chinese landing pages, tool and
  profile detail pages, metadata, sitemap and automatic deployment checks.

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

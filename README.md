# Awesome Python Dev

**Curated AI development toolkits, ready for your coding agents.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Catalog](https://img.shields.io/badge/Catalog-Skills%20%2B%20MCP-6f42c1)](docs/CATALOG.md)

English · [简体中文](README.zh-CN.md)

Find useful, established GitHub projects for AI assisted development, then install a selected toolkit into your project with one command. **Skills** supply reusable development workflows; **MCP servers** give agents access to tools and external context.

The installer is written in Python, with a dedicated Python toolkit. The collection also serves web and general software development across **Claude Code, Codex, Cursor, VS Code Copilot, and OpenCode**.

The initial catalog includes **23 entries: 5 installable skills, 3 installable MCP servers, and 15 reference projects**, with adapters for **5 coding agents**.

## Contents

- [Quick start](#quick-start)
- [Explore the collection](#explore-the-collection)
- [Choose your toolkit](#choose-your-toolkit)
- [Supported agents](#supported-agents)
- [Everyday commands](#everyday-commands)
- [How installation works](#how-installation-works)
- [What makes a project a good fit](#what-makes-a-project-a-good-fit)
- [Contribute](#contribute)
- [Acknowledgments](#acknowledgments)

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run this **inside the project you want to equip**:

```sh
uvx --from 'git+https://github.com/m9rco/awesome-python-dev.git@v0.1.0' apd init --agents codex,claude --profile starter
```

This downloads the selected skills and writes project-local agent configuration. Restart or reload your agent, review its MCP approval prompts, and start working. Codex loads project configuration only for a trusted project; see the [agent guide](docs/AGENTS.md).

For repeated use, install the CLI once:

```sh
uv tool install 'git+https://github.com/m9rco/awesome-python-dev.git@v0.1.0'
apd list
apd init --agents codex,claude --profile starter --dry-run
apd init --agents codex,claude --profile starter
apd doctor
```

`awesome-python-dev` is an alias for `apd`. Python 3.11+ is required. Installation from Git requires Git and access to GitHub. The initial release is distributed from this repository; the commands above do not depend on a package with this name being available on PyPI.

MCP runtime prerequisites depend on your selection: npm-based servers need Node.js and `npx`; Python-based servers need `uvx`. Your coding agent starts these processes when it loads the configuration. `apd init` configures MCP servers; it does not launch them or install your coding agent.

The starter profile needs **Node.js 20.18.1 or newer** for Context7. On Windows, npm recipes use `cmd /c npx`. Existing JSONC configuration is left untouched: convert it to JSON before adding MCP entries, or install skills only with `--tools`.

Example preview from `apd init --agents codex --profile starter --dry-run`:

```text
Preview only (no downloads or writes):
codex: skill systematic-debugging -> .agents/skills/systematic-debugging
codex: skill test-driven-development -> .agents/skills/test-driven-development
codex: skill verification-before-completion -> .agents/skills/verification-before-completion
codex: MCP context7 -> .codex/config.toml
```

## Explore the collection

Browse the [curated catalog](docs/CATALOG.md) for project descriptions, upstream links, licenses, review dates, and installation support. The [research notes](docs/RESEARCH.md) record selection evidence and pinned versions.

| Installable highlights | What this toolkit includes |
| --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | 3 skills: systematic debugging, test-driven development, and verification before completion. |
| [wshobson/agents](https://github.com/wshobson/agents) | 2 Python skills: testing patterns and packaging. |
| [Context7](https://github.com/upstash/context7) | MCP access to library documentation and version-specific examples. |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Browser inspection and interactive web testing. |
| [Fetch MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | Retrieve web pages as text or Markdown for documentation and research. |

Also explore [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Spec Kit](https://github.com/github/spec-kit), [GitHub MCP](https://github.com/github/github-mcp-server), [Serena](https://github.com/oraios/serena), [uv](https://github.com/astral-sh/uv), and [Ruff](https://github.com/astral-sh/ruff) in the [full reference collection](docs/CATALOG.md).

Entries marked **installable** have a recipe in this release. **Reference** entries are curated recommendations, with installation managed by their upstream projects.

```sh
apd list --kind skill
apd list --kind mcp
apd list --kind reference
apd list --json
```

## Choose your toolkit

| Profile | Intended use |
| --- | --- |
| `starter` | Systematic debugging, test-driven development, completion verification, and Context7. |
| `python` | Starter + Python testing patterns, Python packaging, and Fetch MCP. |
| `web` | Starter + Playwright MCP for browser tooling. |

The catalog contains the exact membership of each profile. You can select specific installable IDs instead:

```sh
apd init --agents cursor --profile web
apd init --agents codex --tools systematic-debugging
apd init --agents all --profile starter --dry-run
```

Choose the agents you actually use. `all` targets every supported adapter, even if the corresponding application is not installed.

## Supported agents

| Agent | CLI ID | Skills | MCP configuration |
| --- | --- | --- | --- |
| Claude Code | `claude` | Project-local | Project-local |
| Codex | `codex` | Project-local | Project-local TOML |
| Cursor | `cursor` | Project-local | Project-local |
| GitHub Copilot in VS Code | `vscode` | Project-local | VS Code workspace configuration |
| OpenCode | `opencode` | Project-local | Project-local |

See [paths, official documentation, and compatibility notes](docs/AGENTS.md). Adapter tests cover configuration formats and merge behavior. They do not establish end-to-end validation inside every agent application or compatibility with every historical version. The `vscode` target refers to Copilot in VS Code, not the separate GitHub Copilot CLI.

## Everyday commands

```sh
# Equip another project without changing directories.
apd init --path ../my-project --agents codex --profile python

# Show supported agents and their project paths.
apd agents

# Check installed files, configuration, and runtime prerequisites.
apd doctor --path ../my-project

# Preview removal, then remove the installation managed by apd.
apd remove --path ../my-project --dry-run
apd remove --path ../my-project
```

Run `apd --help` or `apd init --help` for the complete command reference. Re-running `init` adds selections; choosing a different profile does not remove previously installed tools. `remove` removes all unchanged resources owned by `apd` in the project, preserving unrelated user content. Conflicting user changes are protected. Review `git diff` after installation, and commit the generated project configuration if your team should share it.

## How installation works

```text
Reviewed catalog → toolkit selection → agent adapters → project files
                                           ↓
                            tracked installation and doctor checks
```

- Skill sources are pinned to Git commits and verified against archive SHA-256 hashes. Their supporting files and upstream licenses travel with the installation.
- MCP recipes use explicit package versions and are translated into each agent's configuration format.
- Installation records ownership so removal can preserve unrelated settings. Modified managed files are protected from silent overwrites.
- Keep `.awesome-python-dev/manifest.json` for subsequent refreshes and removal. Configuration backups stay under `.awesome-python-dev/backups/`, with a Git ignore rule; keep them private.
- Preview with `--dry-run` before writing. No home-directory agent configuration is changed.
- The installer does not run downloaded skill scripts. Skills and MCP servers can guide or execute actions later through your agent, under that agent's permissions.

Version pins make changes reviewable. They do not freeze all transitive dependencies or replace reviewing upstream code. Runtime authentication, API limits, browser downloads, and client approval remain specific to the selected tool. See [security and reporting](SECURITY.md).

## What makes a project a good fit

We prefer tools with a concrete development use case, useful documentation, an identifiable upstream, a clear license, and evidence of continued maintenance. Stars are one discovery signal; they are not a quality guarantee or a ranking system.

An installable entry additionally needs a reproducible recipe, a reviewable source or package version, verified paths and runtime requirements, and a way to preserve upstream attribution. Projects that need credentials, manual setup, or a richer adapter can remain useful reference entries while an integration is evaluated.

## Contribute

Suggest a tool, improve an installation recipe, or add a tested agent adapter. Start with the [contribution guide](CONTRIBUTING.md) and [roadmap](docs/ROADMAP.md). Report installation problems using the issue template, with secrets removed from logs and configuration.

## Acknowledgments

The organization follows the focused categories and contribution discipline of [Awesome](https://github.com/sindresorhus/awesome), the use-case-oriented curation of [Awesome Python](https://github.com/vinta/awesome-python), and the MCP discovery work of [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers). The project-local initialization experience is inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec).

This is an independent project. Upstream authors own their tools and trademarks. Our installer and original documentation are [MIT licensed](LICENSE); included upstream material retains its own license.

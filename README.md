# Awesome Python Dev

**Curated AI development toolkits, ready for your coding agents.**

> **Awesome Python Dev** (`awesome-python-dev`, CLI: `apd`) is a curated collection and project-local installer for **AI coding agent skills, engineering rules, MCP servers, and LSP tooling**. It supports **Claude Code, Codex, Cursor, GitHub Copilot in VS Code, and OpenCode**. Run `uvx awesome-python-dev init` to select a toolkit for debugging, testing, security review, or framework development. Installable recipes use exact commits or package versions; skill and rule archives are SHA-256 verified. Reference-only entries link to their upstream projects.

[![CI](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml) [![GitHub Pages](https://github.com/m9rco/awesome-python-dev/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/m9rco/awesome-python-dev/actions/workflows/pages.yml) [![GitHub release](https://img.shields.io/github/v/release/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/releases/latest) [![PyPI](https://img.shields.io/pypi/v/awesome-python-dev?logo=pypi&color=3775A9)](https://pypi.org/project/awesome-python-dev/) [![npm shell](https://img.shields.io/npm/v/awesome-python-dev?logo=npm&label=npm%20shell)](https://www.npmjs.com/package/awesome-python-dev) [![GitHub stars](https://img.shields.io/github/stars/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/stargazers) [![GitHub issues](https://img.shields.io/github/issues/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/issues) [![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Catalog](https://img.shields.io/badge/Catalog-Skills%20%7C%20Rules%20%7C%20MCP%20%7C%20LSP-6f42c1)](docs/CATALOG.md)


English · [简体中文](README.zh-CN.md)

**[Browse the website](https://m9rco.github.io/awesome-python-dev/) · [Getting started](https://m9rco.github.io/awesome-python-dev/getting-started/) · [Documentation index](docs/index.md) · [Website maintenance](docs/WEBSITE.md)**

**For agents:** [Integration guide](https://m9rco.github.io/awesome-python-dev/agents/) · [Text index (`llms.txt`)](https://m9rco.github.io/awesome-python-dev/llms.txt) · [Catalog JSON](https://m9rco.github.io/awesome-python-dev/catalog.json)

Find useful, established GitHub projects for AI assisted development, then install a selected toolkit into your project with one command. **Skills** supply reusable workflows, **rules** activate engineering and security guidance, **MCP servers** connect tools and context, and an **LSP bridge** exposes code intelligence to your agent.

The installer is written in Python, with a dedicated Python toolkit. The collection also serves web and general software development across **Claude Code, Codex, Cursor, VS Code Copilot, and OpenCode**.

The repository catalog includes **59 entries**: **32 installable resources** (22 skills, 6 rule packs, 3 MCP servers, and Serena's LSP bridge) and **27 references** (agent-lsp, 8 native language servers, and 18 other tools). Choose from **11 profiles** across **5 coding agents**. Repository `main` may include unreleased additions; `apd list --json` reports the catalog in your installed runtime.

## Contents

- [Quick start](#quick-start)
- [npm shell and runtime updates](#npm-shell-and-runtime-updates)
- [Explore the collection](#explore-the-collection)
- [Choose your toolkit](#choose-your-toolkit)
- [Supported agents](#supported-agents)
- [Rules and framework guidance](#rules-and-framework-guidance)
- [LSP and security tools](#lsp-and-security-tools)
- [Everyday commands](#everyday-commands)
- [How installation works](#how-installation-works)
- [What makes a project a good fit](#what-makes-a-project-a-good-fit)
- [Project structure](#project-structure)
- [FAQ](#faq)
- [Contribute](#contribute)
- [Acknowledgments](#acknowledgments)

## Quick start

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run this **inside the project you want to equip**:

```sh
uvx awesome-python-dev init --agents codex,claude --profile starter
```

Or use npm:

```sh
npx awesome-python-dev init --agents codex,claude --profile starter
```

The Python package requires Python 3.11+. The npm launcher requires **Node.js 22.21+ (22.x) or 24.5+** and **Python 3.11+ or an existing uv installation**. When Python is unavailable, uv can provision Python 3.13. Both entry points run the same toolkit.

This downloads the selected skills and common rules, then writes project-local agent configuration. Restart or reload your agent, review its MCP approval prompts, and start working. Codex loads project configuration only for a trusted project; see the [agent guide](docs/AGENTS.md).

For repeated use, install the CLI once:

```sh
uv tool install awesome-python-dev
apd list
apd init --agents codex,claude --profile starter --dry-run
apd init --agents codex,claude --profile starter
apd doctor
```

For a global npm installation, use `npm install --global awesome-python-dev` instead. Both distributions provide `apd` and `awesome-python-dev`; choose one global installation method. Refresh the Python installation with `uv tool upgrade awesome-python-dev`, or request a particular release with `uvx awesome-python-dev@0.3.0`.

The registry commands do not require a Git checkout. A version-pinned source fallback is also available when Git is installed:

```sh
uvx --from 'git+https://github.com/m9rco/awesome-python-dev.git@v0.3.0' apd init --agents codex,claude --profile starter
```

MCP runtime prerequisites depend on your selection: npm-based servers need Node.js and `npx`; Python-based servers need `uvx`. Your coding agent starts these processes when it loads the configuration. `apd init` configures MCP servers; it does not launch them or install your coding agent.

The starter profile needs **Node.js 20.18.1 or newer** for Context7. On Windows, npm recipes use `cmd /c npx`. Existing JSONC configuration is left untouched: convert it to JSON before adding MCP entries, or install skills only with `--tools`.

Example preview from `apd init --agents codex --profile starter --dry-run`:

```text
Preview only (no downloads or writes):
codex: skill systematic-debugging -> .agents/skills/systematic-debugging
codex: skill test-driven-development -> .agents/skills/test-driven-development
codex: skill verification-before-completion -> .agents/skills/verification-before-completion
codex: MCP context7 -> .codex/config.toml
codex: rules ecc-common-rules -> native project instructions
```

## npm shell and runtime updates

The **npm shell** and **Python runtime** have independent versions. The shell is a small entry point; it downloads the bundled runtime from GitHub Releases on first use, checks its SHA-256 hash, and caches it. Normal commands check for a compatible runtime update at most once every 24 hours. Catalog and installer updates therefore ship without another npm upload.

```sh
apd --shell-version     # npm shell version
apd --version           # selected runtime version
apd runtime status      # inspect local selection; no network request
apd runtime update      # check the stable runtime channel now
```

These `runtime` commands belong to the npm launcher. For reproducible use, set `APD_RUNTIME_VERSION=0.3.0`; `APD_OFFLINE=1` uses an already cached runtime. Offline mode covers the launcher, so installing uncached upstream skills can still require network access. See [runtime selection and caching](docs/NPM-RUNTIME.md) and the [release workflow](docs/RELEASING.md).

## Explore the collection

Browse the [curated catalog](docs/CATALOG.md) for project descriptions, upstream links, licenses, review dates, and installation support. The [research notes](docs/RESEARCH.md) record selection evidence and pinned versions.

| Installable highlights | What this toolkit includes |
| --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | 3 skills: systematic debugging, test-driven development, and verification before completion. |
| [wshobson/agents](https://github.com/wshobson/agents) | 2 Python skills: testing patterns and packaging. |
| [ECC](https://github.com/affaan-m/ECC) | 15 skills and 6 rule packs covering security, engineering, Python, TypeScript, Go, Java, and framework workflows. |
| [Context7](https://github.com/upstash/context7) | MCP access to library documentation and version-specific examples. |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Browser inspection and interactive web testing. |
| [Fetch MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | Retrieve web pages as text or Markdown for documentation and research. |
| [Serena](https://github.com/oraios/serena) | A commit-pinned MCP-to-LSP bridge for symbols, references, and diagnostics. |

Also explore [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Spec Kit](https://github.com/github/spec-kit), [GitHub MCP](https://github.com/github/github-mcp-server), [uv](https://github.com/astral-sh/uv), [Ruff](https://github.com/astral-sh/ruff), and security scanners in the [full reference collection](docs/CATALOG.md).

Entries marked **installable** have a recipe in this release. Entries without an install recipe are references, with installation managed by their upstream projects. `lsp` includes both the installable Serena bridge and standalone language-server references.

```sh
apd list --kind skill
apd list --kind rules
apd list --kind mcp
apd list --kind lsp
apd list --kind reference
apd list --json
```

## Choose your toolkit

| Profile | Intended use |
| --- | --- |
| 🌱 `starter` | Debugging, test-driven development, verification, Context7, and common engineering rules. |
| 🐍 `python` | Python patterns, testing, packaging, Python rules, and Fetch MCP alongside the core workflow. |
| 🌐 `web` | Frontend patterns, TypeScript rules, Playwright MCP, and the core workflow. |
| `engineering` | Coding standards, API design, migrations, deployment, and common rules. |
| `security` | Security review guidance and common engineering/security rules. |
| `django` | Django patterns and security, Python testing, and Python rules. |
| `fastapi` | FastAPI/Python patterns, API design, security review, testing, and FastAPI rules. |
| `springboot` | Spring Boot patterns and security, Java rules, API design, and migrations. |
| `typescript` | Frontend/backend patterns, Next.js/Turbopack guidance, security review, and TypeScript rules. |
| `golang` | Go patterns and rules, API design, and security review. |
| `lsp` | Serena's LSP bridge, configured as an MCP server. |

`apd profiles` shows the exact membership of each profile. Rule dependencies are included automatically: language packs require common rules, and FastAPI rules also require Python rules. You can select specific installable IDs instead:

```sh
apd profiles
apd init --profile fastapi --agents codex,claude
apd init --agents codex --tools systematic-debugging
apd init --agents codex --tools serena
apd init --agents all --profile starter --dry-run
```

Choose the agents you actually use. `all` targets every supported adapter, even if the corresponding application is not installed.

Select the profile for your actual stack. Framework guidance must be checked against your project's versions; the selected Next.js/Turbopack skill targets Next.js 16+. Profiles are additive, so installing unrelated language packs accumulates instructions and may reach an agent's size limit.

## Supported agents

| Agent | CLI ID | Skills | MCP configuration |
| --- | --- | --- | --- |
| Claude Code | `claude` | Project-local | Project-local |
| Codex | `codex` | Project-local | Project-local TOML |
| Cursor | `cursor` | Project-local | Project-local |
| GitHub Copilot in VS Code | `vscode` | Project-local | VS Code workspace configuration |
| OpenCode | `opencode` | Project-local | Project-local |

See [paths, official documentation, and compatibility notes](docs/AGENTS.md). Adapter tests cover configuration formats and merge behavior. They do not establish end-to-end validation inside every agent application or compatibility with every historical version. The `vscode` target refers to Copilot in VS Code, not the separate GitHub Copilot CLI.

## Rules and framework guidance

The selected [ECC](https://github.com/affaan-m/ECC) skills and rules are MIT licensed, pinned to a reviewed commit, and archive-hash verified. The [ECC migration guide](docs/ECC-MIGRATION.md) records the source, exact pins, file allowlists, dependencies, and adaptations. Original rule files are preserved under `.awesome-python-dev/rules/<id>/` with attribution; adapted copies activate through each agent's instruction system.

| Agent | Activated rule files |
| --- | --- |
| Claude Code | `.claude/rules/apd-<id>/*.md` |
| Cursor | `.cursor/rules/apd-<id>/*.mdc` |
| GitHub Copilot in VS Code | `.github/instructions/apd-<id>/*.instructions.md` |
| Codex / OpenCode | A shared managed block in project `AGENTS.md`, containing adapted rule text and language scopes. |

Existing text outside the `AGENTS.md` block is preserved. The installer rejects conflicts and offers no force-overwrite mode. With Codex selected, it guards the generated `AGENTS.md` against the 32 KiB default instruction limit. It refuses oversized output rather than truncating rules.

These are selected guidance files, not the entire ECC plugin. Installation does not register ECC agents, hooks, model preferences, or background services. References to workflow roles are adapted for the host agent. Security checks, tests, migrations, and deployment still use the target project's real tools and permissions.

## LSP and security tools

`apd init --agents codex --tools serena` configures a pinned Serena MCP launch command. It selects Python 3.13 and the LSP backend; the agent starts it later. The recipe passed MCP initialization and discovery of 22 tools in a temporary Python project. That check did not execute symbol operations or validate every agent interface. See the [LSP guide](docs/LSP.md) for prerequisites, language-server references, OpenCode's separate native LSP support, and known limitations.

The `security` profile installs review guidance and rules. [Semgrep](https://github.com/semgrep/semgrep), [Bandit](https://github.com/PyCQA/bandit), [pip-audit](https://github.com/pypa/pip-audit), and [Gitleaks](https://github.com/gitleaks/gitleaks) are catalog references for project checks and CI. Installing guidance does not install these scanners or certify a project as secure.

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

**Upgrading from v0.1:** the v0.2 CLI reads manifest schemas 1 and 2, and upgrades schema 1 during `init`. Keep the manifest and backups. Once upgraded, use v0.2 or newer to manage that installation; v0.1 cannot manage schema 2 manifests.

## How installation works

```text
Reviewed catalog → toolkit selection → agent adapters → project files
                                           ↓
                            tracked installation and doctor checks
```

- Skill and rule sources are pinned to Git commits and verified against archive SHA-256 hashes. Their selected supporting files and upstream licenses travel with the installation.
- MCP recipes use explicit package versions; the Serena bridge pins a Git commit. Recipes are translated into each agent's configuration format.
- Installation records ownership so removal can preserve unrelated settings. Modified managed files are protected from silent overwrites.
- Keep `.awesome-python-dev/manifest.json` for subsequent refreshes and removal. Configuration backups stay under `.awesome-python-dev/backups/`, with a Git ignore rule; keep them private.
- Preview with `--dry-run` before writing. No home-directory agent configuration is changed.
- The installer does not run downloaded skill scripts. Skills and MCP servers can guide or execute actions later through your agent, under that agent's permissions.

Version pins make changes reviewable. They do not freeze all transitive dependencies or replace reviewing upstream code. Runtime authentication, API limits, browser downloads, and client approval remain specific to the selected tool. See [security and reporting](SECURITY.md).

## What makes a project a good fit

We prefer tools with a concrete development use case, useful documentation, an identifiable upstream, a clear license, and evidence of continued maintenance. Stars are one discovery signal; they are not a quality guarantee or a ranking system.

An installable entry additionally needs a reproducible recipe, a reviewable source or package version, verified paths and runtime requirements, and a way to preserve upstream attribution. Rule packs also need explicit file selection, dependencies, and tested native activation. Projects that need credentials, manual setup, or a richer adapter can remain useful reference entries while an integration is evaluated.

## Project structure

| Path | Responsibility |
| --- | --- |
| [`src/awesome_python_dev/`](src/awesome_python_dev/) | Python CLI, installation plans, downloads, agent adapters, and native rule activation. |
| [`src/awesome_python_dev/data/catalog.json`](src/awesome_python_dev/data/catalog.json) | Canonical tool descriptions, installation recipes, source pins, review metadata, and profiles. |
| [`npm/`](npm/) | Independently versioned Node launcher, verified runtime cache, and launcher tests. |
| [`scripts/`](scripts/) | Build and validation entry points for the website, distributions, and runtime. |
| [`scripts/sitegen/`](scripts/sitegen/) | Website configuration, page rendering, and generated Agent discovery documents. |
| [`site/assets/`](site/assets/) | Website styles, browser enhancements, and shared static assets. |
| [`tests/`](tests/) | Python behavior, packaging, and website tests using temporary projects. |
| [`docs/`](docs/index.md) | User guides, compatibility evidence, source attribution, and maintainer workflows. |
| [`.github/workflows/`](.github/workflows/) | Cross-platform CI, Pages deployment, and separate runtime/npm releases. |

`_site/` and `dist/` are generated output. Update the catalog and build sources,
then regenerate; do not maintain a second catalog in generated HTML. See the
[documentation index](docs/index.md) for the right source to change, the
[architecture guide](docs/ARCHITECTURE.md) for module boundaries, and
[repository agent instructions](AGENTS.md) when contributing with an agent.

## FAQ

### What is the difference between skills, rules, MCP, and LSP here?

Skills describe reusable development workflows. Rules supply engineering and
framework instructions through each agent's native rule format. MCP recipes
configure tool servers that the agent can start. The installable LSP integration
is Serena's MCP bridge; standalone language servers are references. Check
[the catalog](docs/CATALOG.md) for each entry's installation support.

### Which coding agents can I configure?

Claude Code (`claude`), Codex (`codex`), Cursor (`cursor`), GitHub Copilot in VS Code
(`vscode`), and OpenCode (`opencode`). Use `--agents codex,claude` to select targets
or `--agents all` for all five. The VS Code adapter does not target the separate
Copilot CLI. See [agent paths and compatibility limits](docs/AGENTS.md).

### What is the shortest installation command?

Run `uvx awesome-python-dev init` inside the target project. Use
`uvx awesome-python-dev init --agents codex --profile python --dry-run` for an
explicit preview without downloads or writes. For repeated use, install once
with `uv tool install awesome-python-dev`, then run `apd init`. The npm alternative
is `npx awesome-python-dev init`; see [runtime prerequisites](#quick-start).

### Why do npm and Python have different versions or catalog contents?

The npm package is a small launcher that selects a verified Python runtime from
GitHub Releases. PyPI distributes that Python toolkit directly. Catalog and
installer updates use runtime releases; launcher changes use npm releases.
Repository `main` and its website can include unreleased catalog additions.
Use `apd --version` and `apd list --json` to identify what your installed release
contains, and read [release and cache behavior](docs/NPM-RUNTIME.md).

### How are projects selected and versions pinned?

Selection considers the development use case, documentation, license,
maintenance evidence, and integration requirements. Stars help discover
candidates; they do not certify quality. Installable skills and rules use full
Git commits and verified archive hashes. MCP recipes use exact package versions
or full commits. Reference entries have no installer recipe. Review evidence
and dates are recorded in [the research notes](docs/RESEARCH.md) and
[canonical catalog](src/awesome_python_dev/data/catalog.json).

### Does installation execute tools or overwrite my agent settings?

`init` downloads selected skill/rule files and writes project-local configuration.
It preserves unrelated settings and rejects conflicting managed changes. It does
not execute downloaded skill scripts or start MCP servers; your agent may do so
later under its own permissions. The npm launcher executes its verified toolkit
runtime. Review a dry run and the [security model](SECURITY.md) before installing.

### Do I need an account or API key?

Browsing the catalog and using the installer require no Awesome Python Dev
account. Selected services can have their own authentication, rate limits,
runtime dependencies, or charges. Follow the linked upstream documentation;
never put credentials into catalog recipes or committed project configuration.

### How can I suggest a missing tool or agent adapter?

Open a [tool suggestion](https://github.com/m9rco/awesome-python-dev/issues/new?template=tool-suggestion.yml)
with its official repository, license, concrete use case, maintenance evidence,
and what you tested. An entry may first be reference-only while its integration
is evaluated. For adapter contributions, include official configuration
documentation and merge/removal tests; see [contributing](CONTRIBUTING.md).

## Contribute

Suggest a tool, improve an installation recipe, or add a tested agent adapter. Start with the [contribution guide](CONTRIBUTING.md) and [roadmap](docs/ROADMAP.md). Report installation problems using the issue template, with secrets removed from logs and configuration.

See the [CI workflow and latest runs](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml) for automated checks, and the [contribution guide](CONTRIBUTING.md) to run them locally.

## Acknowledgments

The organization follows the focused categories and contribution discipline of [Awesome](https://github.com/sindresorhus/awesome), the use-case-oriented curation of [Awesome Python](https://github.com/vinta/awesome-python), and the MCP discovery work of [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers). The project-local initialization experience is inspired by [OpenSpec](https://github.com/Fission-AI/OpenSpec).

This is an independent project. Upstream authors own their tools and trademarks. Our installer and original documentation are [MIT licensed](LICENSE); included upstream material retains its own license.

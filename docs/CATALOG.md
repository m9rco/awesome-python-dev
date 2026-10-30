# Curated catalog / 精选目录

Reviewed **2026-10-30**, catalog schema **2**. **67 entries**, with **35 installable/configurable integrations** and **32 reference-only tools**. The installable set contains 22 skills, 6 rule packs, 6 MCP servers, and 1 MCP-to-LSP bridge. The 11 LSP entries comprise Serena, the two reference-only bridges (agent-lsp, mcpls), and 8 standalone language-server references.

Stars are dated repository-level snapshots, not scores for individual skills or rules. Multiple entries from ECC, Superpowers, agent-skills, or another monorepo share the same repository evidence. The executable source of truth is [`catalog.json`](../src/awesome_python_dev/data/catalog.json); every entry records its source, license, review date, and installation status.

## Browse and select

```sh
apd profiles
apd list --installable
apd list --kind rules
apd list --kind lsp
apd list --category framework-best-practices --installable
apd init --agents codex --profile django --dry-run
```

`install: null` means the CLI lists the tool and its upstream setup guidance. An installable skill copies the pinned skill directory. A rule pack selects and activates reviewed Markdown rules for the chosen agent. A configurable MCP entry writes a pinned server launch configuration; the coding agent starts it later. Serena uses that MCP path to expose language-server capabilities.

## Presets

Profiles select relevant tools instead of loading every available rule and framework. `requires` adds shared rules transitively. For example, FastAPI rules add Python rules, which add common rules.

| Preset | Selected entries | Dependencies added |
| --- | --- | --- |
| `starter` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7`, `ecc-common-rules` | None |
| `python` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7`, `python-testing-patterns`, `python-packaging`, `fetch`, `ecc-python-rules`, `python-patterns` | `ecc-common-rules` |
| `web` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7`, `playwright`, `ecc-typescript-rules`, `frontend-patterns` | `ecc-common-rules` |
| `engineering` | `ecc-common-rules`, `coding-standards`, `api-design`, `database-migrations`, `deployment-patterns`, `systematic-debugging`, `test-driven-development`, `verification-before-completion` | None |
| `security` | `ecc-common-rules`, `security-review` | None |
| `django` | `ecc-python-rules`, `python-patterns`, `django-patterns`, `django-security`, `python-testing-patterns`, `context7` | `ecc-common-rules` |
| `fastapi` | `ecc-fastapi-rules`, `python-patterns`, `fastapi-patterns`, `api-design`, `security-review`, `python-testing-patterns`, `context7` | `ecc-common-rules`, `ecc-python-rules` |
| `springboot` | `ecc-java-rules`, `springboot-patterns`, `springboot-security`, `api-design`, `database-migrations`, `context7` | `ecc-common-rules` |
| `typescript` | `ecc-typescript-rules`, `coding-standards`, `frontend-patterns`, `backend-patterns`, `nextjs-turbopack`, `security-review`, `context7` | `ecc-common-rules` |
| `golang` | `ecc-golang-rules`, `golang-patterns`, `api-design`, `security-review`, `context7` | `ecc-common-rules` |
| `lsp` | `serena` | None |

## Engineering skills, standards, and delivery

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`systematic-debugging`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging) | Root-cause investigation, reproducible failures, and hypothesis-driven debugging. | Install skill | 306,063 | MIT |
| [`test-driven-development`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development) | A test-first workflow with guidance for meaningful regression tests. | Install skill | 306,063 | MIT |
| [`verification-before-completion`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion) | Require fresh verification evidence before claiming a change is complete. | Install skill | 306,063 | MIT |
| [`coding-standards`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/coding-standards) | Shared naming, readability, error-handling, immutability, and code-quality conventions. | Install skill | 290,505 | MIT |
| [`api-design`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/api-design) | REST resources, HTTP semantics, pagination, versioning, error contracts, and rate limits. | Install skill | 290,505 | MIT |
| [`database-migrations`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/database-migrations) | Expand-contract schema changes, safe indexes, batched backfills, and migration-tool workflows. | Install skill | 290,505 | MIT |
| [`deployment-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/deployment-patterns) | Deployment strategies, container builds, health checks, CI/CD, rollback, and production readiness. | Install skill | 290,505 | MIT |
| [`code-review-and-quality`](https://github.com/addyosmani/agent-skills/tree/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/code-review-and-quality) | Structured review of a diff or pull request across correctness, readability, architecture, security, and performance before merge. | Install skill | 111,131 | MIT |
| [`observability-and-instrumentation`](https://github.com/addyosmani/agent-skills/tree/aeac41d4d005999432bb7312f7ff06383a91d59d/skills/observability-and-instrumentation) | Logging, metrics, tracing, and alerting decisions that make production behavior diagnosable. | Install skill | 111,131 | MIT |

## Python, languages, and framework practices

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`python-testing-patterns`](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills/python-testing-patterns) | Practical pytest fixtures, parametrization, mocking, async testing, and coverage guidance. | Install skill | 41,868 | MIT |
| [`python-packaging`](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills/python-packaging) | Build Python libraries and CLIs with package metadata, wheels, and release workflows. | Install skill | 41,868 | MIT |
| [`python-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/python-patterns) | Python idioms, type hints, error handling, resource management, and maintainable code structure. | Install skill | 290,505 | MIT |
| [`fastapi-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/fastapi-patterns) | FastAPI application structure, Pydantic v2, async dependencies, service layers, and HTTP testing. | Install skill | 290,505 | MIT |
| [`django-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/django-patterns) | Django and DRF architecture, ORM access, caching, middleware, and service organization. | Install skill | 290,505 | MIT |
| [`frontend-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/frontend-patterns) | React and Next.js component composition, state, data fetching, forms, performance, and accessibility. | Install skill | 290,505 | MIT |
| [`nextjs-turbopack`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/nextjs-turbopack) | Next.js 16+ bundler selection, development performance, and middleware-to-proxy migration guidance. | Install skill | 290,505 | MIT |
| [`backend-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/backend-patterns) | Node.js, Express, and Next.js API architecture, data access, caching, and observability. | Install skill | 290,505 | MIT |
| [`springboot-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/springboot-patterns) | Spring Boot REST layers, transactional services, repositories, caching, and production defaults. | Install skill | 290,505 | MIT |
| [`golang-patterns`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/golang-patterns) | Idiomatic Go errors, interfaces, concurrency, package organization, and resource lifecycle patterns. | Install skill | 290,505 | MIT |

## Security review and scanning

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`security-review`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/security-review) | Review authentication, authorization, untrusted input, secrets, and sensitive application changes. | Install skill | 290,505 | MIT |
| [`django-security`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/django-security) | Django authentication, authorization, request protections, and production security settings. | Install skill | 290,505 | MIT |
| [`springboot-security`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills/springboot-security) | Spring Security authentication, authorization, validation, secrets, headers, and release checks. | Install skill | 290,505 | MIT |
| [`semgrep`](https://github.com/semgrep/semgrep) | Rule-based static analysis for security issues and code patterns across multiple languages. | Reference only | 17,306 | LGPL-2.1 (community engine); additional offerings/rules have separate terms |
| [`bandit`](https://github.com/PyCQA/bandit) | Find common Python security issues through AST-based static analysis. | Reference only | 8,352 | Apache-2.0 |
| [`pip-audit`](https://github.com/pypa/pip-audit) | Audit Python environments and dependency specifications against known vulnerability data. | Reference only | 1,386 | Apache-2.0 |
| [`gitleaks`](https://github.com/gitleaks/gitleaks) | Detect committed or working-tree secrets using configurable rules and allowlists. | Reference only | 30,384 | MIT |

## Portable agent rules

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`ecc-common-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/common) | Portable cross-language engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |
| [`ecc-python-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/python) | Portable python-specific engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |
| [`ecc-typescript-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/typescript) | Portable typescript-specific engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |
| [`ecc-golang-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/golang) | Portable golang-specific engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |
| [`ecc-java-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/java) | Portable java-specific engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |
| [`ecc-fastapi-rules`](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/rules/python) | Portable fastapi-specific engineering guidance selected from ECC rules. | Install rules | 290,505 | MIT |

## Documentation, browser, and MCP ecosystem

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`context7`](https://github.com/upstash/context7/tree/master/packages/mcp) | Retrieve library documentation and version-specific examples for coding tasks. | Configure MCP | 63,759 | MIT |
| [`playwright`](https://github.com/microsoft/playwright-mcp) | Browser inspection and interactive web testing through accessibility snapshots. | Configure MCP | 38,702 | Apache-2.0 |
| [`fetch`](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | Retrieve web pages as text/Markdown for documentation and research. | Configure MCP | 91,599 | Apache-2.0 / MIT; docs CC-BY-4.0 |
| [`code-review-graph`](https://github.com/tirth8205/code-review-graph) | Serve a Tree-sitter code graph over MCP for review context, change impact, and affected-test hints. | Configure MCP | 32,459 | MIT |
| [`mcp-tools-py`](https://github.com/MarcusJellinghaus/mcp-tools-py) | Run pylint, pytest, mypy, Ruff, Bandit, formatting, and symbol refactors on a Python project through one scoped MCP server. | Configure MCP | 20 | MIT |
| [`fallow`](https://github.com/fallow-rs/fallow) | Report TypeScript and JavaScript complexity, duplication, architecture, styling, and dead-code findings over MCP. | Configure MCP | 5,273 | MIT |
| [`github-mcp`](https://github.com/github/github-mcp-server) | Official GitHub tools for repositories, issues, and pull requests. | Reference only | 33,999 | MIT |
| [`chrome-devtools`](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Inspect browser performance, network activity, and runtime behavior. | Reference only | 54,261 | Apache-2.0 |
| [`sequential-thinking`](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | A reference server for structured problem-solving tool calls. | Reference only | 91,599 | Apache-2.0 / MIT; docs CC-BY-4.0 |
| [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) | Local knowledge graph over code, documentation, configuration, and infrastructure for navigation and change impact. | Reference only | 47,734 | MIT |
| [`chunkhound`](https://github.com/chunkhound/chunkhound) | Index a codebase locally and answer code questions over MCP with citations from current code, git history, and docs. | Reference only | 1,455 | MIT |

## Language intelligence and LSP

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`serena`](https://github.com/oraios/serena) | Expose semantic code navigation, references, diagnostics, and edits to coding agents through an MCP-to-LSP bridge. | Configure LSP bridge | 30,759 | GPL-3.0-or-later (application); MIT (SolidLSP) |
| [`agent-lsp`](https://github.com/blackwell-systems/agent-lsp) | Orchestrate native language servers into batch, refactor, and speculative-edit workflows for coding agents. | Reference only | 166 | MIT |
| [`mcpls`](https://bug-ops.github.io/mcpls/) | Bridge MCP to rust-analyzer, pyright, gopls, and other language servers and expose 31 code tools to agents. | Reference only | 80 | MIT OR Apache-2.0 |
| [`ruff`](https://docs.astral.sh/ruff/editors/) | Python linting, formatting, and the built-in Ruff language server for diagnostics and code actions. | Reference only | 50,317 | MIT |
| [`pyright`](https://github.com/microsoft/pyright) | Python type checking and language-server support for navigation and diagnostics. | Reference only | 15,707 | MIT |
| [`ty`](https://docs.astral.sh/ty/) | Rust-based Python type checker and language server with editor integrations; upstream labels it beta. | Reference only | 19,973 | MIT |
| [`python-lsp-server`](https://github.com/python-lsp/python-lsp-server) | Jedi-based Python completion and navigation with configurable linting and formatting plugins. | Reference only | 2,605 | MIT |
| [`typescript-language-server`](https://github.com/typescript-language-server/typescript-language-server) | Language Server Protocol wrapper around TypeScript language services for JavaScript and TypeScript. | Reference only | 2,587 | Apache-2.0; MIT portions |
| [`gopls`](https://go.dev/gopls/) | Official Go language server providing code navigation, diagnostics, and refactoring. | Reference only | 8,009 | BSD-3-Clause |
| [`rust-analyzer`](https://rust-analyzer.github.io/) | Rust language server with code navigation, completion, diagnostics, and assists. | Reference only | 16,949 | MIT OR Apache-2.0 |
| [`clangd`](https://clangd.llvm.org/) | C/C++ language server with completion, cross-references, diagnostics, and refactoring support. | Reference only | 2,315 | Apache-2.0 WITH LLVM-exception |

## Specification-driven development

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`openspec`](https://github.com/Fission-AI/OpenSpec) | Spec-driven change workflows with per-agent skills and initialization. | Reference only | 73,139 | MIT |
| [`spec-kit`](https://github.com/github/spec-kit) | Specification, planning, and implementation templates for coding agents. | Reference only | 143,181 | MIT |

## Skill ecosystems and discovery

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`anthropic-skills`](https://github.com/anthropics/skills) | Official examples of reusable agent skills and document workflows. | Reference only | 184,157 | Per-skill licenses; see upstream |
| [`vercel-agent-skills`](https://github.com/vercel-labs/agent-skills) | Frontend and deployment-oriented skills maintained by Vercel. | Reference only | 33,096 | See upstream and individual skills |
| [`skills-cli`](https://github.com/vercel-labs/skills) | Discover and install Agent Skills across supported coding agents. | Reference only | 36,801 | MIT |
| [`awesome-copilot`](https://github.com/github/awesome-copilot) | Community-contributed GitHub Copilot instructions, custom agents, skills, and prompts for Python and web projects. | Reference only | 40,570 | MIT |
| [`skillevaluator`](https://github.com/NVIDIA/SkillEvaluator) | Score agent skill quality, detect overlap between skills, and measure a skill's effect on live agent runs. | Reference only | 612 | Apache-2.0 |

## Python project toolchain

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`uv`](https://github.com/astral-sh/uv) | Python environments, dependency management, and isolated tool execution. | Reference only | 91,242 | Apache-2.0 OR MIT |
| [`pytest`](https://github.com/pytest-dev/pytest) | Python testing with fixtures and a broad plugin ecosystem. | Reference only | 14,649 | MIT |
| [`hypothesis`](https://github.com/HypothesisWorks/hypothesis) | Property-based testing for Python that generates inputs and shrinks failing examples. | Reference only | 9,113 | MPL-2.0 |
| [`pre-commit`](https://github.com/pre-commit/pre-commit) | Run configured repository checks before commits. | Reference only | 15,664 | MIT |

## Building MCP integrations

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`fastmcp`](https://github.com/jlowin/fastmcp) | Build Python MCP servers and clients with a high-level API. | Reference only | 28,217 | Apache-2.0 |
| [`mcp-python-sdk`](https://github.com/modelcontextprotocol/python-sdk) | Official Python SDK for implementing MCP servers and clients. | Reference only | 24,684 | MIT |

## Source pins and installation boundaries

Skill and rule archives are pinned to full commits and verified against a recorded SHA-256. Skills retain their complete selected directories and supporting documents. Rules use explicit file allowlists, keep upstream originals and attribution, and generate an adapted activation form for each supported agent. See [ECC migration](ECC-MIGRATION.md) for the exact selection and transformations.

| Source | Pinned revision | Archive SHA-256 |
| --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | `da34247c51339cdd6175b3590261f16e25b08d46669afd5b6fc3f842ab303e20` |
| [wshobson/agents](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06) | `0874a27b17a22e2b7c2e2bcd725768e0803cad06` | `468c5d32d4a24ea9629c7713d209bbb46cf462ac487d3bc442414aec4ed54c43` |
| [affaan-m/ECC](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b) | `25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b` | `7979cc21e2093aed6218fa1709373eff5eb8641b0c0a5128c68db91bbedd7bb1` |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/aeac41d4d005999432bb7312f7ff06383a91d59d) | `aeac41d4d005999432bb7312f7ff06383a91d59d` | `0211a580aab7d45c73886d6f96d2f0679416119b4f9add08b6ceea5c0c15fbf1` |

| Service | Pinned launcher | Runtime / setup |
| --- | --- | --- |
| `context7` | `npx -y @upstash/context7-mcp@4.4.4` | Node.js >=20.18.1 |
| `playwright` | `npx -y @playwright/mcp@0.0.83` | Node.js >=18 |
| `fetch` | `uvx mcp-server-fetch==2026.10.24` | Python >=3.10 |
| `serena` | See [exact Serena command](LSP.md#install-the-lsp-bridge); v2.1.0 at `5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc` | uv/uvx + Git; Python 3.13 selected by uvx; language-specific dependencies |
| `code-review-graph` | `uvx --from code-review-graph==2.3.9 code-review-graph serve --repo {project}` | uv/uvx; Python >=3.10 selected by uvx |
| `mcp-tools-py` | `uvx --from mcp-tools-py==0.1.10 --with mcp<2 mcp-tools-py --project-dir {project}` | uv/uvx; Python >=3.11 selected by uvx; pylint/pytest/mypy for the checks |
| `fallow` | `npx --yes --package fallow@3.37.0 fallow-mcp` | Node.js >=22; the server analyses the directory it starts in |

- **Context7:** API keys are optional in the pinned stdio package guidance for higher limits/private repositories. Service access and policy can change independently of the package version. Configure credentials through the chosen agent; do not commit secrets.
- **Playwright:** A supported browser is needed for browser operations. Configuring the server does not install browser binaries.
- **Fetch:** Requires uv/uvx and a compatible Python. No private-IP bypass is enabled by this recipe.
- **Serena:** The project path is resolved into the MCP configuration. First startup may download language-server dependencies and create Serena-owned state. The installer does not manage or uninstall those upstream caches. See [language intelligence and setup](LSP.md).
- **Native language servers:** Pyright, Python LSP Server, Ruff, TypeScript Language Server, gopls, rust-analyzer, and clangd remain reference-only. Their native LSP commands need an LSP client; they are not interchangeable with MCP servers.
- **agent-lsp:** One of two reference-only LSP bridges besides Serena. It ships as a Go binary from an upstream install script, release archive, or container image, and requires the underlying language servers separately; there is no registry package or dependency version for this catalog to pin, so `apd` writes only the Serena recipe.
- **mcpls:** The other reference-only bridge. It is distributed as a Rust binary through `cargo install mcpls`, an upstream install script, release archives, or a container image, and needs at least one language server (for example pyright) installed separately. Enabling it next to Serena would give the same project two bridges over the same servers.
- **code-review-graph:** The project path is resolved into the MCP configuration and the server indexes it with Tree-sitter; graph data stays in a `.code-review-graph` directory inside the project. Building or refreshing the graph is an explicit CLI or tool step, and upstream `install` also writes hooks, skills, and rules files that this recipe does not touch.
- **mcp-tools-py:** A Python-only companion to the reference-only pytest, Ruff, and Bandit entries. Its `--with mcp<2` pin is deliberate: published `0.1.10` imports `mcp.server.fastmcp` without capping `mcp`, so the default mcp 2.x resolution fails at startup. The checks run through the server's own interpreter unless `--python-executable`/`--venv-path` is configured, so pylint, pytest, and mypy must exist in that environment.
- **fallow:** TypeScript and JavaScript health analysis over MCP — complexity, duplication, architecture boundaries, styling drift, and dead code. The server analyses the directory it is launched in and takes no project argument. Upstream `fallow agent install` additionally writes an `AGENTS.md` task map, installs skills, registers itself, and adds git commit and push gates; this recipe writes only the launch configuration. The npm package pins a per-platform binary and needs Node.js 22 or newer.
- **awesome-copilot:** A large community collection of Copilot instructions, chat modes, custom agents, skills, and prompts, contributed file by file rather than shipped as one pinnable artifact, so it is recorded without a selection being copied. Pick and review the files a project needs; nothing here activates an instruction file.
- **skillevaluator:** Framework for scoring skill quality, detecting overlap, and measuring a skill's effect on live agent runs. It is reference-only because the PyPI name is a zero-version placeholder and the documented quickstart runs from a source checkout. Installing the catalog's skills does not evaluate them; the static path needs no key, while rubric scoring and security coverage need external services or scanners.
- **chunkhound:** Reference only because the pinned launch check did not pass: the server never answered `initialize` in a fresh project within a 300-second window, first failing before connecting (uvx picked Python 3.10, whose scipy build does not load on arm64 macOS) and then stalling on an outbound HTTPS request at startup even with Python 3.12 pinned, with and without `--no-daemon` and `--no-embeddings`. `--read-only` avoids that path but requires an index built beforehand. Indexing is an explicit step, the database is created inside the project at `.chunkhound/db`, and semantic search or deep research needs an embedding or LLM provider that is not configured here.
- **codebase-memory-mcp:** The documented MCP entry points at an installed native executable, and the npm, PyPI, and Go packages of the same name only verify and cache that runtime for the host, so there is no registry launch command to pin. Its installer also writes agent configuration, rules, skills, and hooks and its indexing persists to a shared cache directory with an optional daemon, which is a broader change than writing one launch configuration.
- **Two code-graph servers overlap:** `code-review-graph` and `codebase-memory-mcp` both index a repository into a local graph for review and impact questions, with different runtimes and scope. Enable one per project rather than both.
- **Conflict to resolve yourself:** `pyright` and `ty` are alternative Python type-checking servers, and `ruff server` covers lint/format diagnostics. Pick the servers your editor should run instead of enabling all of them.
- **Test dependencies:** `hypothesis` is a project dependency next to `pytest`, not an MCP server or agent skill. Recording it neither adds nor runs tests and does not configure CI.
- **agent-skills collection:** The two selected skills come from a larger, mostly single-file skill collection with its own plugin manifests and hooks. Only the pinned skill directories are copied; hooks, commands, and agent definitions stay upstream.
- **Security tooling:** Semgrep, Bandit, pip-audit, and Gitleaks remain reference-only. Installing security skills/rules does not install or run scanners, configure CI, or establish an audit result.
- **Rule scope:** Choose the language/framework in the project. FastAPI rules are separate from general Python rules. Embedded instruction blocks have a size guard; the full set of rule packs is larger than 32 KiB.
- **Upstream plugin boundaries:** Superpowers and ECC integrations install only the selected skills/rules. Plugin registration, agent definitions, hooks, commands, memory services, models, and account settings are outside this migration.

MCP package/source pins identify the top-level server revision. npm/uv and upstream language-server managers may resolve additional dependencies at launch; this is not a hermetic runtime lock.

## Selection, verification, and maintenance

Admission considers the coding task served, documented setup, maintenance activity, license, upstream identity, and whether a reproducible integration can be tested. The catalog separates source/configuration checks from runtime operation. Inclusion does not claim every upstream feature or every agent version was tested.

See [research and verification evidence](RESEARCH.md), [ECC migration details](ECC-MIGRATION.md), [LSP and security-tool setup](LSP.md), and [agent configuration paths](AGENTS.md).

**Updates are curated and pinned.** Refreshing installed instructions regenerates them from the catalog shipped with this CLI version. It does not watch upstream repositories, follow their default branches, or silently adopt new skills/rules. A catalog update requires reviewing upstream changes and licenses, selecting a new pin, recomputing archive hashes where applicable, updating these documents, and testing the installation lifecycle.

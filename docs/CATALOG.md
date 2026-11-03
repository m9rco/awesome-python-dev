# Curated catalog / 精选目录

Reviewed **2026-11-03**, catalog schema **2**. **79 entries**, with **40 installable/configurable integrations** and **39 reference-only tools**. The installable set contains 22 skills, 6 rule packs, 10 MCP servers, and 2 MCP-to-LSP bridges. The 13 LSP entries comprise the two installable bridges (Serena, lsp-mcp-server), the two reference-only bridges (agent-lsp, mcpls), and 9 standalone language-server references.

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
| [`open-code-review`](https://github.com/alibaba/open-code-review) | Run an AI review over a diff with deterministic analysis pipelines plus a tuned review model, with matching agent skills and plugins. | Reference only | 49,294 | Apache-2.0 |

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
| [`osv-scanner`](https://github.com/google/osv-scanner) | Scan lockfiles, manifests, SBOMs, and containers across ecosystems against the OSV vulnerability database. | Reference only | 11,342 | Apache-2.0 |
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
| [`repomix`](https://github.com/yamadashy/repomix) | Pack a repository into one AI-friendly file and serve packing, search, and reading of the output over MCP. | Configure MCP | 29,100 | MIT |
| [`roam-code`](https://github.com/Cranot/roam-code) | Serve a local codebase index over MCP for symbol search, dependency and coupling maps, dead code, taint, and change-impact questions. | Configure MCP | 516 | Apache-2.0 |
| [`headroom`](https://github.com/headroomlabs-ai/headroom) | Compress tool output, logs, files, and RAG chunks locally before they reach the model, and retrieve the originals over MCP. | Configure MCP | 78,668 | Apache-2.0 |
| [`mcp-toolbox`](https://github.com/googleapis/mcp-toolbox) | Connect an agent to PostgreSQL, MySQL, SQLite, SQL Server, BigQuery, and other databases through prebuilt or hand-defined SQL tools. | Reference only | 16,792 | Apache-2.0 |
| [`github-mcp`](https://github.com/github/github-mcp-server) | Official GitHub tools for repositories, issues, and pull requests. | Reference only | 33,999 | MIT |
| [`chrome-devtools`](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Inspect browser performance, network activity, and runtime behavior. | Reference only | 54,261 | Apache-2.0 |
| [`sequential-thinking`](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | A reference server for structured problem-solving tool calls. | Reference only | 91,599 | Apache-2.0 / MIT; docs CC-BY-4.0 |
| [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) | Local knowledge graph over code, documentation, configuration, and infrastructure for navigation and change impact. | Reference only | 47,734 | MIT |
| [`chunkhound`](https://github.com/chunkhound/chunkhound) | Index a codebase locally and answer code questions over MCP with citations from current code, git history, and docs. | Reference only | 1,455 | MIT |

## Language intelligence and LSP

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`serena`](https://github.com/oraios/serena) | Expose semantic code navigation, references, diagnostics, and edits to coding agents through an MCP-to-LSP bridge. | Configure LSP bridge | 30,759 | GPL-3.0-or-later (application); MIT (SolidLSP) |
| [`lsp-mcp-server`](https://github.com/ProfessioneIT/lsp-mcp-server) | Bridge MCP clients to whichever language server a project configures, exposing navigation, references, diagnostics, completion, and edits as 29 tools. | Configure LSP bridge | 24 | MIT |
| [`agent-lsp`](https://github.com/blackwell-systems/agent-lsp) | Orchestrate native language servers into batch, refactor, and speculative-edit workflows for coding agents. | Reference only | 166 | MIT |
| [`mcpls`](https://bug-ops.github.io/mcpls/) | Bridge MCP to rust-analyzer, pyright, gopls, and other language servers and expose 31 code tools to agents. | Reference only | 80 | MIT OR Apache-2.0 |
| [`ruff`](https://docs.astral.sh/ruff/editors/) | Python linting, formatting, and the built-in Ruff language server for diagnostics and code actions. | Reference only | 50,317 | MIT |
| [`pyright`](https://github.com/microsoft/pyright) | Python type checking and language-server support for navigation and diagnostics. | Reference only | 15,707 | MIT |
| [`ty`](https://docs.astral.sh/ty/) | Rust-based Python type checker and language server with editor integrations; upstream labels it beta. | Reference only | 19,973 | MIT |
| [`pyrefly`](https://github.com/meta/pyrefly) | Rust-based Python type checker and language server with navigation, completion, inlay hints, and semantic highlighting. | Reference only | 7,172 | MIT |
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
| [`ai-rulez`](https://github.com/Goldziher/ai-rulez) | Compile one rules, skills, and MCP source into native instruction files for dozens of coding agents, with lock files, signing, approvals, and policy checks. | Reference only | 166 | MIT |

## Python project toolchain

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`uv`](https://github.com/astral-sh/uv) | Python environments, dependency management, and isolated tool execution. | Reference only | 91,242 | Apache-2.0 OR MIT |
| [`pytest`](https://github.com/pytest-dev/pytest) | Python testing with fixtures and a broad plugin ecosystem. | Reference only | 14,649 | MIT |
| [`hypothesis`](https://github.com/HypothesisWorks/hypothesis) | Property-based testing for Python that generates inputs and shrinks failing examples. | Reference only | 9,113 | MPL-2.0 |
| [`pre-commit`](https://github.com/pre-commit/pre-commit) | Run configured repository checks before commits. | Reference only | 15,664 | MIT |
| [`deptry`](https://github.com/osprey-oss/deptry) | Detect missing, unused, and misplaced dependencies in a Python project. | Reference only | 1,498 | MIT |
| [`orm-lens`](https://github.com/FROWNINGdev/orm-lens) | Answer Django model questions over MCP from static parsing — relations, ER diagrams, migration risk, N+1 candidates, and schema drift — with SQLAlchemy preview support. | Configure MCP | 96 | MIT |

## Building MCP integrations

| ID / source | Use case | Delivery | Stars | License |
| --- | --- | --- | ---: | --- |
| [`fastmcp`](https://github.com/jlowin/fastmcp) | Build Python MCP servers and clients with a high-level API. | Reference only | 28,217 | Apache-2.0 |
| [`mcp-python-sdk`](https://github.com/modelcontextprotocol/python-sdk) | Official Python SDK for implementing MCP servers and clients. | Reference only | 24,684 | MIT |
| [`mcp-inspector`](https://github.com/modelcontextprotocol/inspector) | Launch, inspect, and call any MCP server from a web UI, TUI, or CLI while developing or debugging an integration. | Reference only | 11,216 | MIT and Apache-2.0 (relicensing in progress) |

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
| `repomix` | `npx -y repomix@1.18.1 --mcp` | Node.js >=22; without `--sandbox` the server can read any path the host user can and trusts the config of the directory it packs |
| `roam-code` | `uvx --python 3.12 --from 'roam-code[mcp]==14.1.0' roam mcp` | uv/uvx; Python 3.12 pinned; indexes the directory it starts in, state in `.roam/` |
| `orm-lens` | `uvx --python 3.12 --from 'orm-lens[mcp]==1.16.0' orm-lens-mcp` | uv/uvx; Python 3.12 pinned; static parsing only, no database or settings module |
| `headroom` | `uvx --python 3.13 --from 'headroom-ai[mcp]==0.42.0' headroom mcp serve` | uv/uvx; Python 3.13 pinned; MCP server mode only, no model download or proxy |
| `lsp-mcp-server` | `npx -y lsp-mcp-server@1.1.27` | Node.js >=18; the target language server must be installed and on PATH |

- **Context7:** API keys are optional in the pinned stdio package guidance for higher limits/private repositories. Service access and policy can change independently of the package version. Configure credentials through the chosen agent; do not commit secrets.
- **Playwright:** A supported browser is needed for browser operations. Configuring the server does not install browser binaries.
- **Fetch:** Requires uv/uvx and a compatible Python. No private-IP bypass is enabled by this recipe.
- **Serena:** The project path is resolved into the MCP configuration. First startup may download language-server dependencies and create Serena-owned state. The installer does not manage or uninstall those upstream caches. See [language intelligence and setup](LSP.md).
- **lsp-mcp-server:** The second installable bridge and the only TypeScript one here: it drives whichever language server a project configures, so Python coverage depends on pyright, Python LSP Server, or another LSP binary installed separately. It pins npm release `1.1.27` (upstream tag `v1.1.27`, commit `2b9005387fbf5ebd101ec84cfc34a8196bf9d347`), reads per-project server settings from `.lsp-mcp.json`, and upstream recommends a longer client tool timeout because the first call starts a language server and its initial analysis. The npm package also ships a `SKILL.md` that teaches tool selection and says it should be re-copied when the server version changes; only the MCP launch configuration is written here. The smoke check completed `initialize` and listed 29 tools, but no language server was started through it and no project file was read by a tool call, so the LSP round trip itself is unverified.
- **Native language servers:** Pyright, Pyrefly, Python LSP Server, Ruff, TypeScript Language Server, gopls, rust-analyzer, and clangd remain reference-only. Their native LSP commands need an LSP client; they are not interchangeable with MCP servers.
- **agent-lsp:** One of the two reference-only LSP bridges next to the installable Serena and lsp-mcp-server recipes. It ships as a Go binary from an upstream install script, release archive, or container image, and requires the underlying language servers separately; there is no registry package or dependency version for this catalog to pin, so `apd` writes only the Serena and lsp-mcp-server recipes.
- **mcpls:** The other reference-only bridge. It is distributed as a Rust binary through `cargo install mcpls`, an upstream install script, release archives, or a container image, and needs at least one language server (for example pyright) installed separately. Enabling it next to Serena or lsp-mcp-server would give the same project two bridges over the same servers.
- **code-review-graph:** The project path is resolved into the MCP configuration and the server indexes it with Tree-sitter; graph data stays in a `.code-review-graph` directory inside the project. Building or refreshing the graph is an explicit CLI or tool step, and upstream `install` also writes hooks, skills, and rules files that this recipe does not touch.
- **mcp-tools-py:** A Python-only companion to the reference-only pytest, Ruff, and Bandit entries. Its `--with mcp<2` pin is deliberate: published `0.1.10` imports `mcp.server.fastmcp` without capping `mcp`, so the default mcp 2.x resolution fails at startup. The checks run through the server's own interpreter unless `--python-executable`/`--venv-path` is configured, so pylint, pytest, and mypy must exist in that environment.
- **fallow:** TypeScript and JavaScript health analysis over MCP — complexity, duplication, architecture boundaries, styling drift, and dead code. The server analyses the directory it is launched in and takes no project argument. Upstream `fallow agent install` additionally writes an `AGENTS.md` task map, installs skills, registers itself, and adds git commit and push gates; this recipe writes only the launch configuration. The npm package pins a per-platform binary and needs Node.js 22 or newer.
- **repomix:** Packs a repository into a single AI-oriented file and exposes the pack plus read/grep tools over MCP. The npm package pins a per-platform payload and needs Node.js 22 or newer. Upstream documents `repomix --mcp` and the npx form used here; the smoke check completed `initialize` and listed six tools. Without `--sandbox` the server can read any path the host user can and trusts `repomix.config.*` in whatever directory it packs, which upstream describes as code execution; `--mcp --sandbox path/to/project` confines the file tools to one workspace and drops config loading, remote packing, and skill generation, at the cost of remote targets.
- **roam-code:** Local codebase intelligence over MCP — symbol search, dependency and coupling maps, dead code, taint paths, file metrics, and change-impact answers for the directory the server starts in. The launcher pins `--python 3.12` because the package requires Python >=3.10 while an unpinned `uvx` resolution on the smoke host picked Python 3.9 and exited before the handshake. The index and its lock/state sidecars live in `.roam/` (`ROAM_DB_DIR` relocates the store, `ROAM_NO_AUTO_INDEX=1` refuses implicit builds); upstream documents `roam init` and `roam index` as explicit steps. The CLI and MCP server are Apache-2.0 and need no account or API key for local analysis, and upstream states local analysis does not upload source, indexes, findings, or telemetry; separate review and cloud services exist and are not configured here. The smoke check completed `initialize` and listed 17 tools, and no tool was called, so analysis quality is unverified.
- **headroom:** A local context-compression layer: it shrinks tool output, logs, files, and RAG chunks before they reach the model, keeps the originals retrievable, and exposes `headroom_compress`, `headroom_retrieve`, and `headroom_stats` over MCP. The recipe pins the published PyPI release `0.42.0` with its `mcp` extra and `--python 3.13`, because the package requires Python 3.10 or newer and an unpinned `uvx` resolves the interpreter itself. The CLI ships only in that package — the npm `headroom-ai` package is the TypeScript SDK and provides no `headroom` command — and upstream notes that clients which do not inherit an interactive shell need the absolute path to the `headroom` executable. Only the MCP server mode is configured: `headroom proxy`, `headroom wrap` (which also registers Serena for the wrapped project), `headroom learn`, and the cross-agent memory store are separate upstream features. Upstream states compression runs locally, but the `[ml]` extra downloads the Kompress-v2-base model from Hugging Face and proxy mode still talks to a model provider; neither is part of this recipe, and no model is pinned here. The smoke check completed `initialize` (server `headroom`, reported version `1.30.0`, protocol `2025-11-25`) and listed the three tools; no tool was called, so compression ratios, retrieval fidelity, and token savings are unverified.
- **mcp-toolbox:** Google's MCP server and framework for databases: prebuilt toolsets for PostgreSQL, MySQL, SQLite, SQL Server, and BigQuery, plus SQL tools, prompts, and resources defined in a `tools.yaml`. It stays reference-only because every useful launch needs database connection settings supplied by the project, and the custom-tool path reads a configuration file that names those sources; npm publishes a per-platform binary behind `npx -y @toolbox-sdk/server --prebuilt=postgres`, so a recipe would register a server that cannot answer its first query until credentials — and, for custom tools, a `tools.yaml` — exist, the same reason GitHub's MCP server is reference-only. Keep that file and any credentials out of version control and out of an agent's context. Upstream also documents an OCI image, release archives, and the Google Antigravity MCP store as install paths.
- **open-code-review:** Alibaba's agent-driven code review: deterministic analysis pipelines feed a review model, and the repository also ships two agent skills (`skills/open-code-review`, `skills/open-code-review-delegate`) plus plugins for Claude Code, Codex, Cursor, Kimi, OpenCode, and QCA. It stays reference-only because the reviewer is a globally installed npm CLI (`npm install -g @alibaba-group/open-code-review`, command `ocr`) that needs an LLM provider and an API key saved through its own interactive configuration before it can review a diff, and because the catalog's skill recipes copy reviewed files without being able to install or configure that CLI — copying the skill alone would leave a project with instructions and no engine. Delegation mode runs the review through the calling agent's own model and needs no OCR key. Upstream also documents install scripts, a release binary, and a source build. Recording it neither installs the CLI nor runs a review, spends provider tokens, or uploads source.
- **mcp-inspector:** The reference client for MCP servers, maintained by the project that maintains the protocol: `npx @modelcontextprotocol/inspector` opens a web UI, `--cli` a scriptable client, and `--tui` a terminal UI over stdio, SSE, and streamable HTTP, and the package also ships an `mcpdo` CLI. It stays reference-only because it is a development client rather than a server a project registers, and because upstream publishes it on the npm `latest` tag rather than pinning a version in its own instructions. Its secret store keeps OAuth tokens and stdio `env:` values in the OS keychain, falling back to an unencrypted `~/.mcp-inspector/secrets.json` where no keychain exists. It is the tool to reach for when a recipe in this catalog does not answer the handshake; running it changes no project and installs no server.
- **orm-lens:** Answers Django model questions over MCP from static parsing — relations, ER diagrams, migration dependencies, cascade and blast radius, index suggestions, N+1 candidates, and schema drift — with SQLAlchemy models, Alembic revisions, and FastAPI/Flask documented as preview support. Upstream states it needs no database, no `runserver`, and no working virtualenv, so it still reports models from a cold clone or a broken environment; the base package accepts Python >=3.9 but the `mcp` extra needs >=3.10, hence the `--python 3.12` launcher pin. A paid cloud service exists upstream for PR review and table statistics and is not used here. The same repository also ships a VS Code/Open VSX extension, an `orm-lens` CLI, a pre-commit hook, and an agent skill directory; only the MCP launch configuration is written. The smoke check completed `initialize` and listed 13 tools against a one-model sample module, and no tool was called, so no real project was analysed.
- **awesome-copilot:** A large community collection of Copilot instructions, chat modes, custom agents, skills, and prompts, contributed file by file rather than shipped as one pinnable artifact, so it is recorded without a selection being copied. Pick and review the files a project needs; nothing here activates an instruction file.
- **skillevaluator:** Framework for scoring skill quality, detecting overlap, and measuring a skill's effect on live agent runs. It is reference-only because the PyPI name is a zero-version placeholder and the documented quickstart runs from a source checkout. Installing the catalog's skills does not evaluate them; the static path needs no key, while rubric scoring and security coverage need external services or scanners.
- **ai-rulez:** An authoring and governance layer: one `.ai-rulez/` source compiles into the native instruction files, skills, and MCP configuration of the harnesses a team uses, with `ai-rulez.lock` pins, Sigstore signing, SBOM output, reviewer approvals, an organisation policy layer, and a read-only MCP server for reports and skill serving. It is reference-only because the npm and PyPI packages of the same name are Go installer wrappers that download a native release binary — the wrapper's own fetch of the v5.10.0 darwin/arm64 archive timed out and retried on the smoke host before any MCP handshake — so there is no registry launch command to pin; release archives, Homebrew, and the Go module are the other distribution paths. The catalog's skill and rule-pack recipes copy reviewed files rather than generate output for dozens of targets, so nothing is installed or activated here. It overlaps `skills-cli` and `awesome-copilot` as discovery and authoring tooling.
- **chunkhound:** Reference only because the pinned launch check did not pass: the server never answered `initialize` in a fresh project within a 300-second window, first failing before connecting (uvx picked Python 3.10, whose scipy build does not load on arm64 macOS) and then stalling on an outbound HTTPS request at startup even with Python 3.12 pinned, with and without `--no-daemon` and `--no-embeddings`. `--read-only` avoids that path but requires an index built beforehand. Indexing is an explicit step, the database is created inside the project at `.chunkhound/db`, and semantic search or deep research needs an embedding or LLM provider that is not configured here.
- **codebase-memory-mcp:** The documented MCP entry points at an installed native executable, and the npm, PyPI, and Go packages of the same name only verify and cache that runtime for the host, so there is no registry launch command to pin. Its installer also writes agent configuration, rules, skills, and hooks and its indexing persists to a shared cache directory with an optional daemon, which is a broader change than writing one launch configuration.
- **Two code-graph servers overlap:** `code-review-graph` and `codebase-memory-mcp` both index a repository into a local graph for review and impact questions, with different runtimes and scope. Enable one per project rather than both.
- **pyrefly:** A third Rust-based Python type checker and language server next to `pyright` and `ty`. Only the `pyrefly lsp` subcommand is documented as LSP entry (as registered by nvim-lspconfig); there is no MCP or agent-config recipe to pin. Upstream ships monthly minor releases that may report new errors, so a project-wide first run should be expected to fail until errors are triaged with `pyrefly suppress`.
- **deptry:** Reference only. It is a CLI run inside a project environment, because it inspects the declared dependencies and compares them against the imports actually used; running it in the wrong interpreter reports misleading results. It is not part of the catalog's checks, and recording it neither installs nor runs it.
- **Conflict to resolve yourself:** `pyright`, `pyrefly`, and `ty` are alternative Python type-checking servers, and `ruff server` covers lint/format diagnostics. Pick the servers your editor should run instead of enabling all of them.
- **Test dependencies:** `hypothesis` is a project dependency next to `pytest`, not an MCP server or agent skill. Recording it neither adds nor runs tests and does not configure CI.
- **agent-skills collection:** The two selected skills come from a larger, mostly single-file skill collection with its own plugin manifests and hooks. Only the pinned skill directories are copied; hooks, commands, and agent definitions stay upstream.
- **Security tooling:** Semgrep, Bandit, pip-audit, OSV-Scanner, and Gitleaks remain reference-only. Installing security skills/rules does not install or run scanners, configure CI, or establish an audit result. OSV-Scanner overlaps pip-audit for Python dependencies while also covering other ecosystems and containers, so a project needs one of them, not both by default.
- **Rule scope:** Choose the language/framework in the project. FastAPI rules are separate from general Python rules. Embedded instruction blocks have a size guard; the full set of rule packs is larger than 32 KiB.
- **Upstream plugin boundaries:** Superpowers and ECC integrations install only the selected skills/rules. Plugin registration, agent definitions, hooks, commands, memory services, models, and account settings are outside this migration.

MCP package/source pins identify the top-level server revision. npm/uv and upstream language-server managers may resolve additional dependencies at launch; this is not a hermetic runtime lock.

## Selection, verification, and maintenance

Admission considers the coding task served, documented setup, maintenance activity, license, upstream identity, and whether a reproducible integration can be tested. The catalog separates source/configuration checks from runtime operation. Inclusion does not claim every upstream feature or every agent version was tested.

See [research and verification evidence](RESEARCH.md), [ECC migration details](ECC-MIGRATION.md), [LSP and security-tool setup](LSP.md), and [agent configuration paths](AGENTS.md).

**Updates are curated and pinned.** Refreshing installed instructions regenerates them from the catalog shipped with this CLI version. It does not watch upstream repositories, follow their default branches, or silently adopt new skills/rules. A catalog update requires reviewing upstream changes and licenses, selecting a new pin, recomputing archive hashes where applicable, updating these documents, and testing the installation lifecycle.

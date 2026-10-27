# Curated catalog / 精选目录

Reviewed **2026-10-27**. 23 curated entries: 5 installable skills, 3 configurable MCP servers, and 15 reference-only tools. Stars are a dated repository-level snapshot, not a score for an individual skill.

The executable catalog lives in [`catalog.json`](../src/awesome_python_dev/data/catalog.json). `install: null` means the CLI only lists the project; use its upstream installation instructions. “Installable MCP” means the CLI writes a pinned launch configuration; the coding agent starts the server on demand.

## Presets

| Preset | Included tools |
| --- | --- |
| `starter` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7` |
| `python` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7`, `python-testing-patterns`, `python-packaging`, `fetch` |
| `web` | `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `context7`, `playwright` |

## Installable skills

| ID / source | Use case | Repository stars | License |
| --- | --- | ---: | --- |
| [`systematic-debugging`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging) | Root-cause investigation, reproducible failures, and hypothesis-driven debugging. | 306,063 | MIT |
| [`test-driven-development`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development) | A test-first workflow with guidance for meaningful regression tests. | 306,063 | MIT |
| [`verification-before-completion`](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion) | Require fresh verification evidence before claiming a change is complete. | 306,063 | MIT |
| [`python-testing-patterns`](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills/python-testing-patterns) | Practical pytest fixtures, parametrization, mocking, async testing, and coverage guidance. | 41,868 | MIT |
| [`python-packaging`](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills/python-packaging) | Build Python libraries and CLIs with package metadata, wheels, and release workflows. | 41,868 | MIT |

## Configurable MCP servers

| ID / source | Use case | Repository stars | License |
| --- | --- | ---: | --- |
| [`context7`](https://github.com/upstash/context7/tree/master/packages/mcp) | Retrieve library documentation and version-specific examples for coding tasks. | 63,759 | MIT |
| [`playwright`](https://github.com/microsoft/playwright-mcp) | Browser inspection and interactive web testing through accessibility snapshots. | 38,702 | Apache-2.0 |
| [`fetch`](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | Retrieve web pages as text/Markdown for documentation and research. | 91,599 | Apache-2.0 / MIT; docs CC-BY-4.0 |

## Reference tools

| ID / source | Use case | Repository stars | License |
| --- | --- | ---: | --- |
| [`github-mcp`](https://github.com/github/github-mcp-server) | Official GitHub tools for repositories, issues, and pull requests. | 33,999 | MIT |
| [`serena`](https://github.com/oraios/serena) | Semantic code navigation and editing backed by language servers. | 30,759 | GPL-3.0-or-later (application); MIT (SolidLSP) |
| [`chrome-devtools`](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Inspect browser performance, network activity, and runtime behavior. | 54,261 | Apache-2.0 |
| [`sequential-thinking`](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) | A reference server for structured problem-solving tool calls. | 91,599 | Apache-2.0 / MIT; docs CC-BY-4.0 |
| [`openspec`](https://github.com/Fission-AI/OpenSpec) | Spec-driven change workflows with per-agent skills and initialization. | 73,139 | MIT |
| [`spec-kit`](https://github.com/github/spec-kit) | Specification, planning, and implementation templates for coding agents. | 143,181 | MIT |
| [`anthropic-skills`](https://github.com/anthropics/skills) | Official examples of reusable agent skills and document workflows. | 184,157 | Per-skill licenses; see upstream |
| [`vercel-agent-skills`](https://github.com/vercel-labs/agent-skills) | Frontend and deployment-oriented skills maintained by Vercel. | 33,096 | See upstream and individual skills |
| [`skills-cli`](https://github.com/vercel-labs/skills) | Discover and install Agent Skills across supported coding agents. | 36,801 | MIT |
| [`uv`](https://github.com/astral-sh/uv) | Python environments, dependency management, and isolated tool execution. | 91,242 | Apache-2.0 OR MIT |
| [`ruff`](https://github.com/astral-sh/ruff) | Python linting and formatting for fast agent feedback. | 50,318 | MIT |
| [`pytest`](https://github.com/pytest-dev/pytest) | Python testing with fixtures and a broad plugin ecosystem. | 14,649 | MIT |
| [`pre-commit`](https://github.com/pre-commit/pre-commit) | Run configured repository checks before commits. | 15,664 | MIT |
| [`fastmcp`](https://github.com/jlowin/fastmcp) | Build Python MCP servers and clients with a high-level API. | 28,217 | Apache-2.0 |
| [`mcp-python-sdk`](https://github.com/modelcontextprotocol/python-sdk) | Official Python SDK for implementing MCP servers and clients. | 24,684 | MIT |

## Installation details

Skill downloads are pinned to full upstream commits and checked against recorded SHA-256 values. The entire selected directory is retained, including reference documents, and the upstream root license accompanies the installation. This is a skills-only integration: Superpowers plugin hooks, agents, marketplace registration, and namespaced commands are not installed. Refer to installed skills by their native names.

| Source | Pinned revision | Archive SHA-256 |
| --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | `da34247c51339cdd6175b3590261f16e25b08d46669afd5b6fc3f842ab303e20` |
| [wshobson/agents](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06) | `0874a27b17a22e2b7c2e2bcd725768e0803cad06` | `468c5d32d4a24ea9629c7713d209bbb46cf462ac487d3bc442414aec4ed54c43` |

| MCP | Launch command | Runtime |
| --- | --- | --- |
| `context7` | `npx -y @upstash/context7-mcp@4.4.4` | Node.js >=20.18.1 |
| `playwright` | `npx -y @playwright/mcp@0.0.83` | Node.js >=18 |
| `fetch` | `uvx mcp-server-fetch==2026.10.24` | Python >=3.10 |

## Tool-specific setup notes

- **Systematic Debugging:** Upstream cross-references test-driven-development and verification-before-completion; all three are included in presets. Copies the skill directory, not the full Superpowers plugin.
- **Context7:** Node.js >=20.18.1. The upstream stdio README documents an optional API key for higher limits/private repositories; service policies and availability apply. Set credentials through your agent, never commit secrets.
- **Playwright MCP:** Node.js >=18 plus a supported browser. First browser use may require a browser installation. This entry configures the MCP server; it does not install browser binaries.
- **Fetch MCP:** uv/uvx and Python >=3.10. This is an upstream reference server; assess URL/network access for your environment. No private-IP bypass is enabled.
- **GitHub MCP Server:** Configure authentication and allowed toolsets with the official installer. No credentials or remote OAuth flow is provisioned by this CLI.
- **Serena:** Project activation and language-server dependencies need a dedicated integration.
- **Chrome DevTools MCP:** Browser lifecycle and environment requirements are configured upstream.
- **Sequential Thinking MCP:** Current npm release 2.0.0 requires Node.js >=24. Kept out of the starter runtime and installer until separately tested.
- **OpenSpec:** Use the upstream CLI for its coordinated workflow artifacts and update semantics.
- **Spec Kit:** Use the official Specify CLI to initialize its own project structure.
- **Anthropic Skills:** Licenses vary by skill, especially document skills. Review the selected directory before redistribution.
- **Vercel Agent Skills:** Select skills and inspect their individual licenses and runtime assumptions.
- **Skills CLI:** Useful when a skill is outside this curated catalog; upstream manages its own installation.
- **uv:** Installed separately; provides uvx for the Fetch MCP preset.
- **Ruff:** Add to the target project development dependencies and CI.
- **pytest:** Add to the target project development dependencies; the testing skill does not install pytest.
- **pre-commit:** Project hooks require an explicit project configuration.
- **FastMCP:** Development framework, not a ready-to-register MCP server.
- **MCP Python SDK:** Development dependency; follow the protocol version supported by your clients.

## Selection and maintenance

We favor a clear coding workflow, documented installation, visible maintenance, a usable license, and a stable upstream source. We distinguish runtime/configuration checks from actual day-to-day usage; inclusion does not assert that every upstream feature has been tested. A popular project with unsuitable setup requirements stays reference-only.

See [research and source evidence](RESEARCH.md) for the awesome-list references, collection date, and verification boundaries. To update a skill, review the upstream diff, download the new full-commit archive, recompute the hash, verify supporting files and license, and test installation before changing the manifest. To update an MCP entry, check its published package and runtime requirements, then test the client configuration.

# Research and provenance

Research date: **2026-10-27**. Repository metadata was fetched with `gh api repos/<owner>/<repo>`; package versions came from the npm and PyPI registries. The manifest records the snapshot date, repository stars, latest push timestamp, license, and source links. Stars belong to whole repositories, so the five skill entries represent two upstream repositories rather than five separate popularity measurements.

## Patterns adopted

| Reference | What this project adopts |
| --- | --- |
| [Awesome manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md) | A narrow scope, short explanations of why an item belongs, and selection criteria. Popularity alone does not qualify a tool. |
| [Awesome Python](https://github.com/vinta/awesome-python) | Organize by developer tasks so readers can find a suitable tool quickly. Keep Python tooling adjacent to the agent workflows it supports. |
| [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) | Group MCP capabilities and provide direct upstream links. This project adds explicit installable/reference-only states. |
| [OpenSpec supported tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) and [installation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md) | A project initialization command, explicit agent selection, repeatable updates, and native agent configuration paths. OpenSpec remains an upstream tool with its own workflow rather than copied templates. |
| [Agent Skills specification](https://agentskills.io/specification) | Keep each selected skill's `SKILL.md` and supporting directory together, retaining the native name and description. |

## Installable upstream evidence

| Item | Evidence checked | Result |
| --- | --- | --- |
| Superpowers skills | [Pinned source tree](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills), repository metadata, root `LICENSE`, complete archive | Three selected skill directories exist with their native frontmatter. The debugging skill links to TDD and verification, so presets include all three. |
| Python skills | [Pinned Python development skills](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills), [upstream skill installation guidance](https://github.com/wshobson/agents/blob/main/docs/harnesses.md), complete archive | Testing and packaging each include `references/details.md` and `references/advanced-patterns.md`. These files must be copied with `SKILL.md`. |
| Context7 | [MCP package README](https://github.com/upstash/context7/blob/master/packages/mcp/README.md), [client configuration](https://context7.com/docs/resources/all-clients), [npm version metadata](https://registry.npmjs.org/@upstash%2fcontext7-mcp/4.4.4) | Published stdio package `4.4.4`; Node.js `>=20.18.1`. The package README describes optional API keys for higher limits/private repositories. Hosted service behavior can change independently of the package pin. |
| Playwright MCP | [Official README](https://github.com/microsoft/playwright-mcp), [npm version metadata](https://registry.npmjs.org/@playwright%2fmcp/0.0.83) | Published stdio package `0.0.83`; Node.js `>=18`. Browser installation is a separate prerequisite. |
| Fetch MCP | [Official README](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch), [PyPI version metadata](https://pypi.org/pypi/mcp-server-fetch/2026.10.24/json), [licensing](https://github.com/modelcontextprotocol/servers/blob/main/LICENSE) | Published `2026.10.24`; Python `>=3.10`; supports `uvx`. The repository is transitioning from MIT to Apache-2.0, with separate documentation licensing. |

The two skill archives were downloaded from `codeload.github.com` at full 40-character commits. Their SHA-256 values in the manifest were computed from the downloaded bytes. Skill contents are upstream third-party material; catalog descriptions and selection notes are authored for this project. No archive or third-party code is vendored into this repository.

## Why some tools are reference-only

- [GitHub MCP Server](https://github.com/github/github-mcp-server) needs an authentication and tool-permission decision. Its official setup remains the entry point.
- [Serena](https://github.com/oraios/serena) adds project/language-server setup and component-specific licensing; it needs its own tested integration.
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) has browser environment assumptions beyond writing a configuration entry.
- [Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) currently publishes `2.0.0` with Node.js `>=24`, verified through [npm metadata](https://registry.npmjs.org/@modelcontextprotocol%2fserver-sequential-thinking/2.0.0). It is not part of the starter runtime.
- [Anthropic Skills](https://github.com/anthropics/skills) and [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) are collections whose individual skills have different capabilities and license considerations. They are discovery sources, not bulk-install defaults.
- [uv](https://github.com/astral-sh/uv), [Ruff](https://github.com/astral-sh/ruff), [pytest](https://github.com/pytest-dev/pytest), and [pre-commit](https://github.com/pre-commit/pre-commit) belong in a project's development toolchain. Registering them as MCP servers would misrepresent their role.
- [FastMCP](https://github.com/jlowin/fastmcp) and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) help build integrations; they are not preconfigured MCP services.

## Verification boundaries

This research verifies source identity, published package availability, manifest pins, skill directory completeness, declared setup requirements, and the protocol checks below. It does not establish a security audit, benchmark ranking, or compatibility with every version of every agent. Installer tests and release CI cover this repository's configuration behavior; users still need the selected agent, required runtimes, network access, and any upstream service credentials.

### MCP protocol smoke results

On 2026-10-27, the three exact manifest launch commands passed `initialize` and `tools/list` through the official Python MCP SDK **2.3.0**, running Python **3.12.13** on macOS arm64 with Node.js **22.23.1** and uv **0.8.17**. All negotiated protocol **2025-11-25**.

| Package pin | Reported server version | Tools discovered | Result |
| --- | --- | ---: | --- |
| `@upstash/context7-mcp@4.4.4` | `4.4.4` | 2 | Passed |
| `@playwright/mcp@0.0.83` | `1.64.0-alpha-1790635538000` | 25 | Passed |
| `mcp-server-fetch==2026.10.24` | `2026.10.24` | 1 | Passed |

The Playwright server reports its underlying implementation version, which differs from the published MCP wrapper version. No browser was opened, no MCP tool was invoked, and no Context7 query or Fetch request was made. These results establish process startup and tool discovery; they do not establish browser availability, API access, or end-to-end application behavior.

Reproduce with `uv run --no-project --python 3.12 --with mcp==2.3.0 python scripts/smoke_mcp.py`. The optional script uses a 90-second timeout per server and a temporary npm cache. It forwards only network proxy/CA settings in addition to the SDK's default subprocess environment. Initial attempts on this host exposed missing proxy forwarding and SDK 2.x field-name changes in the smoke helper; the recorded results are from clean reruns after fixing both.

MCP top-level package versions are pinned. Their transitive dependency graphs are resolved by npm/uv at launch and are not fully locked by this catalog. A registry version pin should therefore not be described as a hermetic runtime. Skill archives are checked against an exact recorded digest; an upstream archive byte change causes a verification failure until deliberately reviewed.

## Refresh procedure

1. Fetch repository metadata and check that the project remains active, documented, and suitable for its category.
2. Review upstream changes and license changes; do not automatically equate a larger star count with admission.
3. For a skill, choose a full commit, download its archive, compute SHA-256, and check the complete selected directory and root license.
4. For MCP, verify the exact registry version, binary entry point, supported runtime, and documented configuration. Test the server with a compatible client before expanding support claims.
5. Update `catalog.json`, `CATALOG.md`, and this research record in the same change, then exercise preview/install/repeat-install/remove in a temporary project.

# Research and provenance

Research date: **2026-10-28**. Repository metadata was fetched with `gh api repos/<owner>/<repo>`; package versions came from the npm and PyPI registries. The manifest records the snapshot date, repository stars, latest push timestamp, license, and source links. Stars belong to whole repositories: the 22 skill entries come from four upstream repositories, and the six ECC rule packs share the ECC repository snapshot. A high star count is not an independent quality score for every skill or rule.

## Patterns adopted

| Reference | What this project adopts |
| --- | --- |
| [Awesome manifesto](https://github.com/sindresorhus/awesome/blob/main/awesome.md) | A narrow scope, short explanations of why an item belongs, and selection criteria. Popularity alone does not qualify a tool. |
| [Awesome Python](https://github.com/vinta/awesome-python) | Organize by developer tasks so readers can find a suitable tool quickly. Keep Python tooling adjacent to the agent workflows it supports. |
| [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) | Group MCP capabilities and provide direct upstream links. This project adds explicit installable/reference-only states. |
| [OpenSpec supported tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) and [installation](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md) | A project initialization command, explicit agent selection, repeatable updates, and native agent configuration paths. OpenSpec remains an upstream tool with its own workflow rather than copied templates. |
| [Agent Skills specification](https://agentskills.io/specification) | Keep each selected skill's `SKILL.md` and supporting directory together, retaining the native name and description. |

## Version 0.2 catalog expansion

Catalog schema 2 contains **59 entries** and **11 profiles**. Thirty-two entries have an installation recipe: **22 skills, 6 rule packs, 3 MCP servers, and the Serena MCP-to-LSP bridge**. The remaining 27 are references, including a second LSP bridge, eight native language servers, and four security scanners.

The expansion adds a reviewed subset of ECC for engineering standards, security review, Python/FastAPI/Django, TypeScript/React/Next.js, Spring Boot, Go, API design, migrations, and deployment guidance. Rule packs use explicit source-file allowlists, native language scopes, and shared-rule dependencies. They preserve upstream originals while activating a disclosed portable adaptation. See [ECC source selection and migration boundaries](ECC-MIGRATION.md).

Serena changes from a discovery-only reference in the initial catalog to a pinned, project-aware MCP launch recipe. Native language servers remain separate reference entries; security scanners remain project/CI tooling references. [LSP and security-tool documentation](LSP.md) describes setup, prerequisites, protocol boundaries, and the recorded Serena smoke result.

`starter` now includes common rules. The Python and web profiles add the appropriate language rules and selected practices; dependencies include the common layer automatically. Framework profiles narrow the loaded guidance to the selected stack. `apd profiles`, `apd list --kind rules`, `apd list --kind lsp`, `--category`, and `--installable` expose these distinctions in the CLI.

## Candidate review on 2026-10-28

A search pass over GitHub for recently active coding-agent skills, MCP servers, LSP bridges, and Python development tooling added five entries after de-duplication against the previous 54: two pinned skills from `addyosmani/agent-skills` (`code-review-and-quality`, `observability-and-instrumentation`) and three references (`astral-sh/ty`, `blackwell-systems/agent-lsp`, `HypothesisWorks/hypothesis`). Rejected candidates were either duplicative (another Python type checker, further Python LSP bridges already covered by Serena's backends, skill collections without a stable pin or clear license) or outside the coding-toolkit scope.

Both new skills are single-directory skills whose `SKILL.md` is self-contained; the collection's plugin manifests, hooks, and commands are not installed, and the two entries share one archive digest. The three new references record repository metadata, upstream documentation, and license files only. No package install, language-server startup, client configuration, or MCP session was run for `ty`, `agent-lsp`, or `hypothesis` in this pass, so they stay reference-only until verified.

## Installable upstream evidence

| Item | Evidence checked | Result |
| --- | --- | --- |
| Superpowers skills | [Pinned source tree](https://github.com/obra/superpowers/tree/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills), repository metadata, root `LICENSE`, complete archive | Three selected skill directories exist with their native frontmatter. The debugging skill links to TDD and verification, so presets include all three. |
| Python skills | [Pinned Python development skills](https://github.com/wshobson/agents/tree/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/python-development/skills), [upstream skill installation guidance](https://github.com/wshobson/agents/blob/main/docs/harnesses.md), complete archive | Testing and packaging each include `references/details.md` and `references/advanced-patterns.md`. These files must be copied with `SKILL.md`. |
| ECC skills and rules | [Pinned source tree](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b), repository metadata, MIT license, downloaded archive | Fifteen native skill directories and six explicit rule selections were checked. Selected paths are regular files/directories; skill frontmatter names match their IDs. Archive SHA-256 and size limits were verified. See [migration evidence](ECC-MIGRATION.md). |
| agent-skills | [Pinned source tree](https://github.com/addyosmani/agent-skills/tree/aeac41d4d005999432bb7312f7ff06383a91d59d/skills), repository metadata, root `LICENSE` (MIT), complete downloaded archive | Both selected directories exist at the pin and contain a single `SKILL.md`; the skill directories hold no scripts or auxiliary files to copy. Archive SHA-256 `0211a580aab7…` recorded in the manifest. The collection's plugin manifests and hooks are out of scope for this installation. |
| Serena | [v2.1.0 release](https://github.com/oraios/serena/releases/tag/v2.1.0), [pinned package metadata](https://github.com/oraios/serena/blob/5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc/pyproject.toml), [component licensing](https://github.com/oraios/serena/blob/5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc/LICENSE), [server configuration](https://oraios.github.io/serena/02-usage/020_running.html) | v2.1.0 pinned to full commit; Python 3.13 selected explicitly. Generic project context, LSP backend, individual tool interface; dashboard/browser/GUI opening disabled. MCP startup and discovery of 22 tools verified; symbol calls were not exercised. |
| Context7 | [MCP package README](https://github.com/upstash/context7/blob/master/packages/mcp/README.md), [client configuration](https://context7.com/docs/resources/all-clients), [npm version metadata](https://registry.npmjs.org/@upstash%2fcontext7-mcp/4.4.4) | Published stdio package `4.4.4`; Node.js `>=20.18.1`. The package README describes optional API keys for higher limits/private repositories. Hosted service behavior can change independently of the package pin. |
| Playwright MCP | [Official README](https://github.com/microsoft/playwright-mcp), [npm version metadata](https://registry.npmjs.org/@playwright%2fmcp/0.0.83) | Published stdio package `0.0.83`; Node.js `>=18`. Browser installation is a separate prerequisite. |
| Fetch MCP | [Official README](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch), [PyPI version metadata](https://pypi.org/pypi/mcp-server-fetch/2026.10.24/json), [licensing](https://github.com/modelcontextprotocol/servers/blob/main/LICENSE) | Published `2026.10.24`; Python `>=3.10`; supports `uvx`. The repository is transitioning from MIT to Apache-2.0, with separate documentation licensing. |

The three skill/rule source archives were downloaded from `codeload.github.com` at full 40-character commits. Their SHA-256 values in the manifest were computed from the downloaded bytes. Serena instead uses an explicit Git source revision through uvx. Skill and original rule contents are upstream third-party material; catalog descriptions, selection notes, and disclosed rule adaptations are authored for this project. No upstream archive is vendored into this repository.

## Why some tools are reference-only

- [GitHub MCP Server](https://github.com/github/github-mcp-server) needs an authentication and tool-permission decision. Its official setup remains the entry point.
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) has browser environment assumptions beyond writing a configuration entry.
- [Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) currently publishes `2.0.0` with Node.js `>=24`, verified through [npm metadata](https://registry.npmjs.org/@modelcontextprotocol%2fserver-sequential-thinking/2.0.0). It is not part of the starter runtime.
- [Anthropic Skills](https://github.com/anthropics/skills) and [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) are collections whose individual skills have different capabilities and license considerations. They are discovery sources, not bulk-install defaults.
- [uv](https://github.com/astral-sh/uv), [pytest](https://github.com/pytest-dev/pytest), [hypothesis](https://github.com/HypothesisWorks/hypothesis), and [pre-commit](https://github.com/pre-commit/pre-commit) belong in a project's development toolchain. They are not ready-to-register MCP servers.
- The eight native LSP references — [Pyright](https://github.com/microsoft/pyright), [Python LSP Server](https://github.com/python-lsp/python-lsp-server), [Ruff](https://docs.astral.sh/ruff/editors/), [ty](https://docs.astral.sh/ty/), [TypeScript Language Server](https://github.com/typescript-language-server/typescript-language-server), [gopls](https://go.dev/gopls/), [rust-analyzer](https://rust-analyzer.github.io/), and [clangd](https://clangd.llvm.org/) — require compatible toolchains and an LSP client. Their raw launch commands do not speak MCP. Ruff also remains useful as a Python lint/format CLI, and `ty` overlaps Pyright on Python type checking.
- [agent-lsp](https://github.com/blackwell-systems/agent-lsp) does speak MCP, but it is distributed as a Go binary built by its own install script or release archive. There is no registry version or dependency revision to pin here, and it needs the individual language servers installed separately, so it stays a reference next to Serena rather than a configured bridge.
- [Semgrep](https://github.com/semgrep/semgrep), [Bandit](https://github.com/PyCQA/bandit), [pip-audit](https://github.com/pypa/pip-audit), and [Gitleaks](https://github.com/gitleaks/gitleaks) need project-specific inputs, scan scope, reviewed policies/rules, and CI decisions. Their official metadata, licensing, and setup links are recorded in the manifest. Installing security guidance does not execute a scanner or imply a clean result.
- [FastMCP](https://github.com/jlowin/fastmcp) and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) help build integrations; they are not preconfigured MCP services.

## Verification boundaries

This research verifies source identity, published package availability, manifest pins, selected skill/rule directory completeness, declared setup requirements, and the protocol checks below. Native rule generation is covered by this project's adapter tests; that does not imply every upstream guidance example was executed. It does not establish a security audit, benchmark ranking, or compatibility with every version of every agent. Installer tests and release CI cover this repository's configuration behavior; users still need the selected agent, required runtimes, network access, and any upstream service credentials.

### MCP protocol smoke results

On 2026-10-27, the three exact manifest launch commands passed `initialize` and `tools/list` through the official Python MCP SDK **2.3.0**, running Python **3.12.13** on macOS arm64 with Node.js **22.23.1** and uv **0.8.17**. All negotiated protocol **2025-11-25**.

| Package pin | Reported server version | Tools discovered | Result |
| --- | --- | ---: | --- |
| `@upstash/context7-mcp@4.4.4` | `4.4.4` | 2 | Passed |
| `@playwright/mcp@0.0.83` | `1.64.0-alpha-1790635538000` | 25 | Passed |
| `mcp-server-fetch==2026.10.24` | `2026.10.24` | 1 | Passed |

The Playwright server reports its underlying implementation version, which differs from the published MCP wrapper version. No browser was opened, no MCP tool was invoked, and no Context7 query or Fetch request was made. These results establish process startup and tool discovery; they do not establish browser availability, API access, or end-to-end application behavior.

Reproduce with `uv run --no-project --python 3.12 --with mcp==2.3.0 python scripts/smoke_mcp.py`. The optional script uses a 90-second timeout per server and a temporary npm cache. It forwards only network proxy/CA settings in addition to the SDK's default subprocess environment. Initial attempts on this host exposed missing proxy forwarding and SDK 2.x field-name changes in the smoke helper; the recorded results are from clean reruns after fixing both.

### Serena bridge smoke result

On 2026-10-27, the exact pinned Serena v2.1.0 launcher completed `initialize` and `tools/list` on macOS using Python 3.13, an isolated `SERENA_HOME`, and a temporary Python project. It exposed 22 tools, including symbol search, reference search, and file diagnostics. Startup and discovery took about 35 seconds. No `tools/call` request was made, and the check ended before language-server initialization completed. This verifies process launch and MCP discovery, not symbol correctness or operation inside every supported agent UI. See [the complete recipe and verification boundaries](LSP.md#verification-recorded-for-this-recipe).

MCP top-level package versions or Git source revisions are pinned. Their transitive dependency graphs are resolved by npm/uv at launch and are not fully locked by this catalog. Serena may download additional language-server dependencies when it activates a project. A registry version or Git revision pin should therefore not be described as a hermetic runtime. Skill/rule archives are checked against an exact recorded digest; an upstream archive byte change causes a verification failure until deliberately reviewed.

## Refresh procedure

Updates are curated and pinned. Regenerating installed instructions uses the catalog bundled with the installed CLI version; it does not watch upstream projects, follow new default-branch commits, or automatically import new rules, hooks, or skills. Changing an upstream pin is a reviewed catalog change.


1. Fetch repository metadata and check that the project remains active, documented, and suitable for its category.
2. Review upstream changes and license changes; do not automatically equate a larger star count with admission.
3. For a skill or rule pack, choose a full commit, download its archive, compute SHA-256, and check the selected directories/files and root license. For rules, review scopes, shared dependencies, relative links, portable transformations, and activated instruction size.
4. For MCP or an LSP bridge, verify the exact registry version or Git revision, binary entry point, supported runtime, and documented configuration. Test the server with a compatible client before expanding support claims. Keep native LSP servers and project scanners reference-only until a separate integration is deliberately implemented.
5. Update `catalog.json`, `CATALOG.md`, this research record, and relevant migration/setup documents in the same change, then exercise preview/install/repeat-install/update/remove in a temporary project.

# Language intelligence and security tools

The `lsp` profile configures **Serena**, an MCP bridge to language servers, for the coding agent you select. The catalog also lists a second installable bridge, [`lsp-mcp-server`](https://github.com/ProfessioneIT/lsp-mcp-server), standal...[truncated]

```text
Coding agent → MCP → Serena → language server → project symbols and diagnostics
Coding agent → MCP → lsp-mcp-server → configured language server → project symbols and diagnostics
Editor or native LSP client → language server → editor features and diagnostics
Project checks / CI → security scanner → findings to review and fix
```

`apd` writes an MCP launch configuration for Serena or `lsp-mcp-server`. It does not invent a shared native LSP configuration for all agents, install editor extensions, install the language servers a bridge drives, or automatically run security scans.

## Install the LSP bridge

From a project directory containing source code:

```sh
apd list --kind lsp
apd init --agents codex --profile lsp --dry-run
apd init --agents codex --profile lsp
apd doctor
```

The same profile can target `claude`, `cursor`, `vscode`, or `opencode`. Select the clients you use. `apd init --agents codex --tools serena` selects the bridge directly.

The recipe pins [Serena v2.1.0](https://github.com/oraios/serena/releases/tag/v2.1.0) to commit `5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc` and selects Python 3.13. The upstream package supports Python `>=3.11,<3.15`; selecting an interpreter avoids accidentally using Python 3.15. `uvx` can download a compatible Python when needed. Git, `uvx`, and network access must be available to the agent process. See the pinned [package metadata](https://github.com/oraios/serena/blob/5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc/pyproject.toml) and [installation guide](https://oraios.github.io/serena/02-usage/010_installation.html).

The generated command is equivalent to the following, with the project path resolved by `apd`:

```sh
uvx --python 3.13 \
  --from git+https://github.com/oraios/serena@5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc \
  serena start-mcp-server \
  --context ide --project /absolute/path/to/your-project \
  --language-backend LSP --agent-interface tools \
  --enable-web-dashboard false --open-web-dashboard false \
  --enable-gui-log-window false
```

The generic `ide` context assumes the coding agent already provides basic file and shell tools and binds Serena to one project. The explicit `tools` interface exposes individual operations instead of a Python REPL. Dashboard, browser opening, and GUI logging are disabled in this recipe. These choices use Serena's documented [server options](https://oraios.github.io/serena/02-usage/020_running.html) and [contexts/interfaces](https://oraios.github.io/serena/02-usage/050_configuration.html); they are configuration choices, not a sandbox.

Restart or reload your agent, approve the MCP server through its normal controls, and inspect the exposed tools. A useful first prompt is: “Read Serena's initial instructions, then find the relevant symbol and its references before changing it.” Client-specific setup and startup timeout guidance are in Serena's [MCP client guide](https://oraios.github.io/serena/02-usage/030_clients.html).

## What first startup may do

`apd init` only adds the MCP configuration. When the agent starts Serena, Serena may create its own user configuration and `.serena/` project state, detect languages, and download language-server dependencies. Those upstream files and caches are not owned or removed by `apd`. The default Python backend is Pyright; TypeScript support uses a TypeScript language server, while Go and Rust require appropriate toolchains. For C/C++, provide compilation information such as `compile_commands.json`. Check the [language requirements](https://oraios.github.io/serena/01-about/020_programming-languages.html) before first use.

The generated command contains an absolute project path. After moving the project or cloning it elsewhere, inspect the MCP entry and reconcile the path before starting the server. Existing conflicting configuration is protected rather than overwritten silently.

Source pins identify the Serena revision. They do not lock every package or language-server download that upstream may perform. Serena's application is GPL-3.0-or-later and SolidLSP is MIT; see its [component licensing](https://github.com/oraios/serena/blob/5e4f5cd173c7ff3eed37ee3f1de6c266b937c5dc/LICENSE).

## Standalone language servers

These catalog entries are references (`install: null`). An LSP client must start them and send protocol requests; registering their raw commands as MCP servers does not work.

| Server | Role | Native launch command | Official setup |
| --- | --- | --- | --- |
| [Pyright](https://github.com/microsoft/pyright) | Python types, navigation, diagnostics | `pyright-langserver --stdio` | [Installation](https://github.com/microsoft/pyright/blob/main/docs/installation.md) |
| [ty](https://docs.astral.sh/ty/) | Python type checks and diagnostics from a Rust-based server; beta | `ty server` | [Editor integration](https://docs.astral.sh/ty/editors/) |
| [Pyrefly](https://github.com/meta/pyrefly) | Python types, navigation, diagnostics from a Rust-based server | `pyrefly lsp` | [IDE and language-server setup](https://pyrefly.org/en/docs/IDE/) |
| [Python LSP Server](https://github.com/python-lsp/python-lsp-server) | Python navigation/completion with optional lint and formatting plugins | `pylsp` | [Install and configure](https://github.com/python-lsp/python-lsp-server#installation) |
| [Ruff](https://github.com/astral-sh/ruff) | Python lint diagnostics, fixes, formatting | `ruff server` | [Editor integration](https://docs.astral.sh/ruff/editors/) |
| [TypeScript Language Server](https://github.com/typescript-language-server/typescript-language-server) | JavaScript/TypeScript language services | `typescript-language-server --stdio` | [Installation and compatible TypeScript version](https://github.com/typescript-language-server/typescript-language-server#installing) |
| [gopls](https://github.com/golang/tools/tree/master/gopls) | Go navigation, diagnostics, refactoring | `gopls` | [Go setup guide](https://go.dev/gopls/) |
| [rust-analyzer](https://github.com/rust-lang/rust-analyzer) | Rust navigation, completion, diagnostics, assists | `rust-analyzer` | [Rust toolchain installation](https://rust-analyzer.github.io/book/rust_analyzer_binary.html) |
| [clangd](https://github.com/clangd/clangd) | C/C++ navigation, completion, diagnostics | `clangd` | [Install and describe the build](https://clangd.llvm.org/installation) |
| [Tombi](https://github.com/tombi-toml/tombi) | TOML formatting, linting, and schema-aware diagnostics for `pyproject.toml` and other project configuration | `tombi lsp` | [Installation](https://tombi-toml.github.io/tombi/docs/installation) |
| [agnix](https://github.com/agent-sh/agnix) | Linting, validation, and optional auto-fix for agent configuration — `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, hooks, plugin and MCP files — across Claude Code, Codex CLI, Cursor, Copilot, and OpenCode | `agnix-lsp` | [Documentation](https://agent-sh.github.io/agnix/) |
| [basedpyright](https://docs.basedpyright.com) | Python types, navigation, diagnostics, inlay hints, semantic highlighting, and import organization from a maintained Pyright fork with `recommended`/`all` checking modes and a baseline file | `basedpyright-langserver --stdio` | [Command line and language server](https://github.com/DetachHead/basedpyright/blob/main/docs/installation/command-line-and-language-server.md) |
| [pytest-language-server](https://github.com/bellini666/pytest-language-server) | pytest fixture navigation across `conftest.py` and plugin fixtures, `yield` and teardown jumps, fixture call hierarchy, completion, references, rename, and diagnostics for test code | `pytest-language-server` | [Installation](https://github.com/bellini666/pytest-language-server#installation) |

For example, upstream documents `python -m pip install python-lsp-server` inside the environment you want to use, followed by configuring `pylsp` in your editor. Rust's toolchain method is `rustup component add rust-analyzer`, followed by client configuration. Choose versions and environment scope appropriate to your project; these commands are not run by `apd`.

Ruff supplies lint and formatting capabilities. Pair it with a navigation/type server when that functionality is needed; it does not replace every Python language-server feature. Its built-in `ruff server` supersedes the older `ruff-lsp` wrapper. See the [Ruff language-server description](https://docs.astral.sh/ruff/editors/).

Pyrefly is a third Rust-based Python type checker with an editor-facing server, next to Pyright and ty. Upstream's own extensions cover VSCode and OpenVSX-based editors, and the `lsp` argument recorded above is the one their default `pyrefly.lspArguments` value passes to the binary; for other editors upstream points at community setups. Its release notes describe monthly minor releases that can report new errors, so a first run over an existing project should be expected to fail until errors are triaged. Choose one Python type checker per project rather than running Pyright, ty, and Pyrefly at once.
Tombi is the one server in this table that targets configuration rather than source code: Python projects describe themselves in TOML (`pyproject.toml`, uv, Ruff, and pytest settings), and Tombi formats, lints, and validates those files against schemas from the JSON Schema Store. It is a single Rust binary distributed through the curl installer, Homebrew, winget, `uvx`/`uv tool install`, npm, and the VS Code, Open VSX, Zed, JetBrains, Helix, Neovim, and Emacs integrations, so which command a client needs depends on that client; Neovim's own configuration registers `tombi lsp` for `toml` files and roots the workspace at `pyproject.toml`. Pair it with a navigation/type server rather than instead of one.
agnix is the second configuration-facing server recorded here and, like Tombi, it is a single binary rather than an MCP service; unlike Tombi it validates the agent's own files instead of the project's. Its 758 rules cover `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, `.claude/rules/*.md`, hooks, plugin manifests, and MCP configuration, with several hundred rules scoped per client (Claude Code 170, Codex CLI 89, Cursor 40), and the CLI's `--fix`, `--fix-safe`, and `--fix-unsafe` modes apply the findings. It ships the `agnix` CLI, an `agnix-lsp` language server, and an optional `agnix-mcp` server, and reaches clients through npm, Homebrew, PyPI, cargo, a GitHub Action, and the VS Code, JetBrains, Neovim, and Zed integrations, so which command a client needs depends on that client. Nothing here runs it: no lint pass, no fix, and no language-server session was performed for this entry.

basedpyright is a maintained fork of Pyright, so it is recorded as a third Python type checker next to Pyright, ty and Pyrefly rather than as a replacement for any of them. Upstream's reason for the fork is the feature set Pyright does not open-source: Pylance-style inlay hints, semantic highlighting and import organization, the `recommended` and `all` checking modes, and a baseline file that lets a project adopt stricter checking incrementally instead of fixing every existing error before it can be enabled. It is distributed as the PyPI package `basedpyright`, a Homebrew formula, and VS Code, Open VSX and Sublime Text integrations, and it pairs with a formatter/linter such as Ruff. The launch command above is the one the project's own Zed configuration uses. Its `LICENSE.txt` carries the MIT text inherited from Pyright while the GitHub API reports `NOASSERTION` for the modified header. Nothing here installs or starts it.

pytest-language-server is the one server in this table that targets tests instead of source: it resolves fixture definitions in the same file, in `conftest.py` and in plugin-provided fixtures while respecting pytest's shadowing rules, jumps to the `yield` that produces a generator fixture, exposes fixture call hierarchy in both directions, completes fixture names inside test and fixture functions, and reports diagnostics for scope and circular-dependency problems. It is a Rust binary launched as `pytest-language-server`, distributed through PyPI (`uv tool install`, `pip`, `pipx`), a Homebrew tap, crates.io, release binaries and a source build, with root markers `pytest.ini`, `pyproject.toml`, `setup.py`, `setup.cfg` and `.git`. It is young and single-maintainer (first release November 2025, 124 stars) and its README states it was built with AI coding agents and reviewed afterwards, so it belongs next to a navigation and type server rather than in place of one. Nothing here installs or starts it either.

## Another installable bridge: lsp-mcp-server

[`lsp-mcp-server`](https://github.com/ProfessioneIT/lsp-mcp-server) is the second bridge the catalog can write. `apd init --agents codex --tools lsp-mcp-server` configures the npm release `lsp-mcp-server@1.1.27` (tag `v1.1.27`, commit `2b9005387fbf5ebd101ec84cfc34a8196bf9d347`) with `npx`:

```sh
npx -y lsp-mcp-server@1.1.27
```

Node.js 18 or newer must be available to the agent process. Unlike Serena, it does not ship or choose a language server: it drives whichever server the project configures. Settings come from the nearest `.lsp-mcp.json` (then `lsp-mcp.json`, `~/.config/lsp-mcp/config.json`, or `~/.lsp-mcp.json`), and the server executables themselves — for Python, `pylsp` from `python-lsp-server` — must already be on the agent's `PATH`. With no configuration file it falls back to upstream's defaults for TypeScript/JavaScript, Python, and Rust and has nothing to query yet. Upstream's own client guides set a 20-second startup timeout and a 120-second tool timeout, because the first request also pays language-server startup.

It exposes 29 tools, including `lsp_goto_definition`, `lsp_find_references`, `lsp_hover`, `lsp_diagnostics`, `lsp_completions`, `lsp_rename`, and the `lsp_start_server` / `lsp_stop_server` / `lsp_server_status` controls, and it advertises file-size limits, workspace-boundary validation, and absolute-path enforcement. It is MIT-licensed; its servers start on demand and restart after a crash. The `lsp` profile still selects Serena only, so pick one bridge per project rather than running both over the same language servers.

## Another bridge: agent-lsp

[agent-lsp](https://github.com/blackwell-systems/agent-lsp) is catalogued as a reference-only bridge. It starts and manages external language servers such as `gopls`, `pyright`, and `rust-analyzer` in one session and exposes batch, refactor, and speculative-edit workflows over MCP.

It is a Go binary installed by the upstream script, a release archive, or a container image. The project publishes no registry package or dependency revision for this catalog to pin, and it needs the underlying language servers installed separately, so `apd` writes only the two pinned bridge recipes and leaves agent-lsp a reference. Review its tool surface and install path upstream if that workflow fits your project.

## Another bridge: mcpls

[mcpls](https://bug-ops.github.io/mcpls/) is catalogued as a second reference-only bridge next to agent-lsp. It runs language servers such as `rust-analyzer`, `pyright`, and `gopls` in one session and exposes their type information, references, diagnostics, and refactoring as 31 MCP tools over stdio or optional HTTP transport.

It is a Rust binary distributed through `cargo install mcpls`, an upstream install script, release archives, or a container image, so there is no registry package revision for this catalog to pin; it also needs at least one language server installed separately. Like agent-lsp it stays a reference while `apd` writes only the pinned Serena and lsp-mcp-server recipes. Use it when a project needs several of its supported language servers at once; otherwise an editor's native LSP setup already covers that work.

## OpenCode's native LSP support

OpenCode also has native LSP integration independently of Serena. Its current documentation says LSP is disabled by default and can be enabled in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": true
}
```

Merge this into your existing configuration manually if desired. OpenCode starts eligible servers when it opens matching files and the runtime requirements are met; some servers are downloaded automatically. `OPENCODE_DISABLE_LSP_DOWNLOAD=true` disables those automatic downloads. Custom entries can specify a command, extensions, environment, and initialization options. `apd` preserves existing top-level configuration but does not manage this native `lsp` setting. Check the [official OpenCode LSP documentation](https://opencode.ai/docs/lsp/) for current behavior.

## Security tooling references

Use these in project checks or CI according to their own setup guides. Agent rules can require the checks and explain how findings are reviewed; they do not install the scanners or guarantee a clean result.

| Tool | What it checks | Setup |
| --- | --- | --- |
| [Semgrep](https://github.com/semgrep/semgrep) | Source patterns and security rules across languages | [Getting started](https://semgrep.dev/docs/getting-started/) |
| [Bandit](https://github.com/PyCQA/bandit) | Common Python security issues in syntax trees | [Quick start](https://bandit.readthedocs.io/en/latest/start.html) |
| [pip-audit](https://github.com/pypa/pip-audit) | Known vulnerabilities in Python dependencies | [Usage and input formats](https://github.com/pypa/pip-audit#usage) |
| [OSV-Scanner](https://github.com/google/osv-scanner) | Known vulnerabilities across ecosystems, SBOMs, and container images | [Guided walkthrough](https://google.github.io/osv-scanner/usage/) |
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Secrets in Git history or directory contents | [Installation and usage](https://github.com/gitleaks/gitleaks#usage) |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | Prompt injection, exfiltration, credential access, obfuscation, and supply-chain risk in a skill, MCP server, Git URL, archive, or registry snapshot | [Scanning agent skills](https://docs.nvidia.com/skills/scanning-agent-skills) |

Select the intended scan scope and reviewed rule sets, pin dependencies in the project, keep sensitive findings private, and record the command and outcome. Confirm that dependency audits use the actual project environment or supported lock/requirements input. Configure any network, hosted service, or telemetry behavior according to the selected upstream tool.

## Verification recorded for this recipe

On 2026-11-10, no MCP or language-server entry was added or changed: the `planning-with-files` skill added that day had its pinned archive downloaded and SHA-256 verified but was not installed, and the `ui-ux-pro-max`, `agent-skills-spec` and `arcade-mcp` references added the same day were recorded from repository metadata, upstream documentation, package metadata and license files only, so no client files were generated, no skill was validated and no MCP server was started. On 2026-11-09, the `squirrelscan` MCP entry added that day was launched through its pinned command from a temporary project and completed MCP `initialize` and `tools/list` with 15 tools discovered ([research evidence](RESEARCH.md#mcp-protocol-smoke-results)); no `tools/call` request was issued, so no site was audited, no report was written, and no account was used. The `pipelock`, `elephant-goldfish`, and `lspyx` references added the same day were recorded from repository metadata, upstream documentation, package metadata, and license files only: no proxy was started and no policy was loaded, no traffic was intercepted, no plugin, agent, or skill was activated, and no language-server startup or MCP session was run for `lspyx`. On 2026-11-06, the `misata` MCP entry added that day was launched through its pinned command from a temporary project and completed MCP `initialize` and `tools/list` with 15 tools discovered ([research evidence](RESEARCH.md#mcp-protocol-smoke-results)); no `tools/call` request was issued, so no dataset was generated, no certificate was re-verified, and no database was seeded. The `agnix`, `skillspector`, and `brooks-lint` references added the same day were recorded from repository metadata, upstream documentation, package metadata, and license files only: no lint run or `--fix`, no scan, no installer, and no editor or MCP session was started. On 2026-11-02, the `roam-code`, `orm-lens`, and `lsp-mcp-server` entries added that day were launched through their pinned commands from a temporary project and completed MCP `initialize` and `tools/list` with 17, 13, and 29 tools discovered ([research evidence](RESEARCH.md#mcp-protocol-smoke-results)); no `tools/call` request was issued, so no codebase was indexed, no Django or SQLAlchemy project was analysed, and no language server was driven. The `ai-rulez` entry added the same day stays a reference: its npm and PyPI packages are installers for a native binary, and the wrapper's own download did not finish in the smoke window, so no MCP session was started. On 2026-11-01, the `repomix` MCP entry added that day passed the same launch check with six tools discovered, while `pyrefly`, `osv-scanner`, and `deptry` were added from repository metadata, upstream documentation, and license files only: no language-server startup, editor configuration, scan, or MCP session was run for those three references. On 2026-10-29, `mcpls` was added from repository metadata, the upstream documentation book, license files, and release v0.8.0 only: no language-server startup, editor configuration, or MCP session was run. The `code-review-graph` and `mcp-tools-py` MCP entries added the same day were launched through the pinned commands and completed `initialize` and `tools/list`; see [research evidence](RESEARCH.md#mcp-protocol-smoke-results). On 2026-10-30, the `fallow` MCP entry added that day passed the same launch check with 43 tools discovered, while `chunkhound` was recorded as a reference after its pinned command failed to complete `initialize` in a fresh project within the smoke window. On 2026-10-28, `ty` and `agent-lsp` were added from repository metadata, upstream documentation, and license files only: no language-server startup, editor configuration, or MCP session was run for either entry. On 2026-10-27, the exact pinned Serena command completed MCP `initialize` and `tools/list` on macOS with Python 3.13 in a temporary Python project, using an isolated `SERENA_HOME`. Startup and tool discovery took about 35 seconds. It exposed 22 tools, including `find_symbol`, `find_referencing_symbols`, and `get_diagnostics_for_file`.

The check made no `tools/call` requests and ended before language-server initialization completed. It verifies the package launch and MCP discovery path, not symbol correctness, every programming language, every operating system, or integration inside all five agent applications.

On **2026-11-10**, a second pass on the same date added the two language-server references in the table above, `basedpyright` and `pytest-language-server`, plus two reference-only entries in the catalog (`trailofbits/skills` in `security`, `oceanbase/powercontext` in `mcp-ecosystem`). Their rows come from repository metadata, upstream documentation, package metadata and license files; no binary was installed, no language-server session was started, no hook or plugin was activated, and no MCP server was launched. The recorded launch commands were not executed, so this pass adds no protocol evidence.

## 中文速览

`apd init --agents codex --profile lsp` 会配置 Serena，通过 MCP 将 LSP 的符号导航、引用和诊断能力提供给 agent。配置固定上游版本，使用 Python 3.13；首次启动可能下载解释器或语言服务依赖。安装器不替你配置编辑器原生 LSP，也不自动运行安全扫描。

`apd list --kind lsp` 可查看 Serena、lsp-mcp-server 与独立语言服务。后者需按各自官方指南安装，再由编辑器或其他原生 LSP 客户端加载。OpenCode 原生 `lsp` 设置与 MCP 桥接是两条独立路径；本工具保留你的设置，不自动开启原生 LSP。

已验证 Serena 的 MCP 握手和工具列表，尚未执行符号操作或逐一验证所有 agent 界面。项目移动后需核对生成配置中的绝对路径；Serena 自己创建的缓存和项目状态不由 `apd remove` 清理。lsp-mcp-server 不自带语言服务：需自行安装（Python 用 python-lsp-server 提供的 `pylsp`）并在项目内配置 `.lsp-mcp.json`，它只是把已有语言服务接到 agent。2026-11-02 新增的 roam-code、orm-lens、lsp-mcp-server 也通过了握手与工具列表检查（分别 17、13、29 个工具），但没有调用任何工具。2026-11-06 新增的 `misata`（Python 合成测试数据 MCP）通过握手与工具列表检查（15 个工具），未调用任何工具；同期的 `agnix`（agent 配置 lint / LSP）、`skillspector`（技能与 MCP 安全扫描）、`brooks-lint`（六种代码审查模式）仅按仓库元数据、上游文档与许可证收录，未运行安装器、扫描或语言服务。 2026-11-09 新增的 `squirrelscan`（网站审计 MCP）通过握手与工具列表检查（15 个工具），未调用任何工具、未审计任何站点；同期的 `pipelock`（出网与 MCP 策略网关）、`elephant-goldfish`（多 harness 设计评审插件）、`lspyx`（Python 专用 ty+Ruff 桥接）仅按仓库元数据、上游文档与许可证收录，未运行安装器、代理、插件或语言服务。 2026-11-10 新增的 `planning-with-files`（把计划、进度与发现写进 `.planning/` 文件的 skill）只下载并校验了固定归档的 SHA-256，未安装、未启动 agent 会话；同期的 `ui-ux-pro-max`（本地设计数据 skill，经生成器 CLI 交付）、`agent-skills-spec`（Agent Skills 规范与 `skills-ref` 校验器）、`arcade-mcp`（Python MCP 框架）仅按仓库元数据、上游文档与许可证收录，未生成客户端文件、未运行校验、未启动 MCP 会话。

2026-11-10 晚间追加的两个独立语言服务参考（`basedpyright`、`pytest-language-server`）仅按仓库元数据、上游文档、包元数据与许可证收录：未安装、未启动语言服务、未开启编辑器会话；同批的 `trailofbits-skills`（CC-BY-SA-4.0 插件市场）与 `powercontext`（需自建服务并信任 hooks 的记忆层）同样未安装或运行。

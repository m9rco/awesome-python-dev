# Language intelligence and security tools

The `lsp` profile configures **Serena**, an MCP bridge to language servers, for the coding agent you select. The catalog also lists standalone language servers and security scanners with their upstream setup guides. These categories solve different parts of a development workflow.

```text
Coding agent → MCP → Serena → language server → project symbols and diagnostics
Editor or native LSP client → language server → editor features and diagnostics
Project checks / CI → security scanner → findings to review and fix
```

`apd` writes an MCP launch configuration for Serena. It does not invent a shared native LSP configuration for all agents, install editor extensions, or automatically run security scans.

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
| [Python LSP Server](https://github.com/python-lsp/python-lsp-server) | Python navigation/completion with optional lint and formatting plugins | `pylsp` | [Install and configure](https://github.com/python-lsp/python-lsp-server#installation) |
| [Ruff](https://github.com/astral-sh/ruff) | Python lint diagnostics, fixes, formatting | `ruff server` | [Editor integration](https://docs.astral.sh/ruff/editors/) |
| [TypeScript Language Server](https://github.com/typescript-language-server/typescript-language-server) | JavaScript/TypeScript language services | `typescript-language-server --stdio` | [Installation and compatible TypeScript version](https://github.com/typescript-language-server/typescript-language-server#installing) |
| [gopls](https://github.com/golang/tools/tree/master/gopls) | Go navigation, diagnostics, refactoring | `gopls` | [Go setup guide](https://go.dev/gopls/) |
| [rust-analyzer](https://github.com/rust-lang/rust-analyzer) | Rust navigation, completion, diagnostics, assists | `rust-analyzer` | [Rust toolchain installation](https://rust-analyzer.github.io/book/rust_analyzer_binary.html) |
| [clangd](https://github.com/clangd/clangd) | C/C++ navigation, completion, diagnostics | `clangd` | [Install and describe the build](https://clangd.llvm.org/installation) |

For example, upstream documents `python -m pip install python-lsp-server` inside the environment you want to use, followed by configuring `pylsp` in your editor. Rust's toolchain method is `rustup component add rust-analyzer`, followed by client configuration. Choose versions and environment scope appropriate to your project; these commands are not run by `apd`.

Ruff supplies lint and formatting capabilities. Pair it with a navigation/type server when that functionality is needed; it does not replace every Python language-server feature. Its built-in `ruff server` supersedes the older `ruff-lsp` wrapper. See the [Ruff language-server description](https://docs.astral.sh/ruff/editors/).

## Another bridge: agent-lsp

[agent-lsp](https://github.com/blackwell-systems/agent-lsp) is catalogued as a reference-only bridge. It starts and manages external language servers such as `gopls`, `pyright`, and `rust-analyzer` in one session and exposes batch, refactor, and speculative-edit workflows over MCP.

It is a Go binary installed by the upstream script, a release archive, or a container image. The project publishes no registry package or dependency revision for this catalog to pin, and it needs the underlying language servers installed separately, so `apd` keeps writing only the Serena recipe. Configuring a second bridge would also duplicate Serena's role in the `lsp` profile. Review its tool surface and install path upstream if that workflow fits your project.

## Another bridge: mcpls

[mcpls](https://bug-ops.github.io/mcpls/) is catalogued as a second reference-only bridge next to agent-lsp. It runs language servers such as `rust-analyzer`, `pyright`, and `gopls` in one session and exposes their type information, references, diagnostics, and refactoring as 31 MCP tools over stdio or optional HTTP transport.

It is a Rust binary distributed through `cargo install mcpls`, an upstream install script, release archives, or a container image, so there is no registry package revision for this catalog to pin; it also needs at least one language server installed separately. Like agent-lsp it stays a reference while `apd` writes only the Serena recipe. Use it when a project needs several of its supported language servers at once; otherwise an editor's native LSP setup already covers that work.

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
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Secrets in Git history or directory contents | [Installation and usage](https://github.com/gitleaks/gitleaks#usage) |

Select the intended scan scope and reviewed rule sets, pin dependencies in the project, keep sensitive findings private, and record the command and outcome. Confirm that dependency audits use the actual project environment or supported lock/requirements input. Configure any network, hosted service, or telemetry behavior according to the selected upstream tool.

## Verification recorded for this recipe

On 2026-10-29, `mcpls` was added from repository metadata, the upstream documentation book, license files, and release v0.8.0 only: no language-server startup, editor configuration, or MCP session was run. The `code-review-graph` and `mcp-tools-py` MCP entries added the same day were launched through the pinned commands and completed `initialize` and `tools/list`; see [research evidence](RESEARCH.md#mcp-protocol-smoke-results). On 2026-10-28, `ty` and `agent-lsp` were added from repository metadata, upstream documentation, and license files only: no language-server startup, editor configuration, or MCP session was run for either entry. On 2026-10-27, the exact pinned Serena command completed MCP `initialize` and `tools/list` on macOS with Python 3.13 in a temporary Python project, using an isolated `SERENA_HOME`. Startup and tool discovery took about 35 seconds. It exposed 22 tools, including `find_symbol`, `find_referencing_symbols`, and `get_diagnostics_for_file`.

The check made no `tools/call` requests and ended before language-server initialization completed. It verifies the package launch and MCP discovery path, not symbol correctness, every programming language, every operating system, or integration inside all five agent applications.

## 中文速览

`apd init --agents codex --profile lsp` 会配置 Serena，通过 MCP 将 LSP 的符号导航、引用和诊断能力提供给 agent。配置固定上游版本，使用 Python 3.13；首次启动可能下载解释器或语言服务依赖。安装器不替你配置编辑器原生 LSP，也不自动运行安全扫描。

`apd list --kind lsp` 可查看 Serena 与独立语言服务。后者需按各自官方指南安装，再由编辑器或其他原生 LSP 客户端加载。OpenCode 原生 `lsp` 设置与 Serena MCP 是两条独立路径；本工具保留你的设置，不自动开启原生 LSP。

已验证 Serena 的 MCP 握手和工具列表，尚未执行符号操作或逐一验证所有 agent 界面。项目移动后需核对生成配置中的绝对路径；Serena 自己创建的缓存和项目状态不由 `apd remove` 清理。

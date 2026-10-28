# Awesome Python Dev

**精选 AI 开发工具包，一条命令装进你的 coding agent。**

> **Awesome Python Dev** 是面向 AI 编程助手的精选可安装工具集：**Coding Agent Skills（技能）、工程规则包（Rules）、MCP 服务器（MCP）与 LSP 桥接**，适配 **Claude Code、Codex、Cursor、GitHub Copilot 和 OpenCode**。提供 Python 安装器（`uvx awesome-python-dev init`）与 npm 启动器，为 Python 与 Web 项目一键配置本地工具链：调试流程、测试驱动开发、API 设计、数据库迁移、安全评审与框架最佳实践（FastAPI、Django、Spring Boot、Go、TypeScript、Next.js）。每个条目均锁定上游 commit，并记录许可证与 SHA-256 校验证据——浏览与安装均无需账号或 API key。

[![CI](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml)
[![GitHub Pages](https://github.com/m9rco/awesome-python-dev/actions/workflows/pages.yml/badge.svg?branch=main)](https://github.com/m9rco/awesome-python-dev/actions/workflows/pages.yml)

[![GitHub release](https://img.shields.io/github/v/release/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/awesome-python-dev?logo=pypi&color=3775A9)](https://pypi.org/project/awesome-python-dev/)
[![npm shell](https://img.shields.io/npm/v/awesome-python-dev?logo=npm&label=npm%20shell)](https://www.npmjs.com/package/awesome-python-dev)
[![GitHub stars](https://img.shields.io/github/stars/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/issues)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Catalog](https://img.shields.io/badge/Catalog-Skills%20%7C%20Rules%20%7C%20MCP%20%7C%20LSP-6f42c1)](docs/CATALOG.md)


[English](README.md) · 简体中文

**[浏览项目网站](https://m9rco.github.io/awesome-python-dev/zh/) · [安装指南](https://m9rco.github.io/awesome-python-dev/getting-started/) · [网站自动发布说明](docs/WEBSITE.md)**

收集 GitHub 上实用、成熟、有明确来源的 AI 开发工具，并将经过适配的工具组合成可安装的工具包。**Skill** 提供开发流程，**规则** 激活工程规范与安全指导，**MCP** 连接工具和上下文，**LSP 桥接** 提供符号导航和代码诊断。

安装器使用 Python 编写，并提供 Python 开发预设；整个集合也覆盖 Web 和通用软件开发。目前支持 **Claude Code、Codex、Cursor、VS Code Copilot 和 OpenCode**。

收录 **59 个条目**：**32 个可安装资源**（22 个 skills、6 套规则、3 个 MCP servers、1 个 Serena LSP 桥接），以及 **27 个参考条目**（agent-lsp、8 个原生语言服务、18 个其他工具）。提供 **11 种预设、5 种 coding agent** 适配。

## 目录

- [快速开始](#快速开始)
- [npm 外壳与 runtime 更新](#npm-外壳与-runtime-更新)
- [浏览工具集合](#浏览工具集合)
- [选择工具包](#选择工具包)
- [支持的 agent](#支持的-agent)
- [规则与框架实践](#规则与框架实践)
- [LSP 与安全工具](#lsp-与安全工具)
- [常用命令](#常用命令)
- [安装机制](#安装机制)
- [收录标准](#收录标准)
- [参与贡献](#参与贡献)

## 快速开始

先安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，然后在**需要配置的项目目录**中执行：

```sh
uvx awesome-python-dev init --agents codex,claude --profile starter
```

也可以使用 npm：

```sh
npx awesome-python-dev init --agents codex,claude --profile starter
```

Python 包需要 Python 3.11+。npm 外壳需要 **Node.js 22.21+（22.x）或 24.5+**，以及 **Python 3.11+ 或已安装的 uv**；缺少 Python 时，uv 可以准备 Python 3.13。两种入口使用相同的工具包。

命令会下载选中的 skills 和通用规则，生成项目内的 agent 配置。随后重启或重新加载 agent，处理客户端的 MCP 授权提示即可使用。Codex 需要信任该项目后才会读取项目配置，具体见 [agent 适配说明](docs/AGENTS.md)。

经常使用时，可以先安装 CLI：

```sh
uv tool install awesome-python-dev
apd list
apd init --agents codex,claude --profile starter --dry-run
apd init --agents codex,claude --profile starter
apd doctor
```

偏好 npm 时，改用 `npm install --global awesome-python-dev` 全局安装。两种发行方式都提供 `apd` 和 `awesome-python-dev`，选择一种全局安装方式即可。Python 版本通过 `uv tool upgrade awesome-python-dev` 升级，也可以用 `uvx awesome-python-dev@0.3.0` 指定版本。

从包仓库安装不需要 Git checkout。已安装 Git 时，也可使用固定版本的源码入口：

```sh
uvx --from 'git+https://github.com/m9rco/awesome-python-dev.git@v0.3.0' apd init --agents codex,claude --profile starter
```

不同 MCP 的运行条件不同：npm 类型需要 Node.js 和 `npx`，Python 类型需要 `uvx`。`apd init` 负责写入 MCP 配置，agent 加载配置后才会启动相关进程；coding agent 本身仍需自行安装。

Starter 预设中的 Context7 需要 **Node.js 20.18.1 或更新版本**。Windows 下的 npm 配方使用 `cmd /c npx`。已有 JSONC 配置会保留；添加 MCP 前需转换为 JSON，也可以通过 `--tools` 仅安装 skills。

运行 `apd init --agents codex --profile starter --dry-run` 的预览示例：

```text
Preview only (no downloads or writes):
codex: skill systematic-debugging -> .agents/skills/systematic-debugging
codex: skill test-driven-development -> .agents/skills/test-driven-development
codex: skill verification-before-completion -> .agents/skills/verification-before-completion
codex: MCP context7 -> .codex/config.toml
codex: rules ecc-common-rules -> native project instructions
```

## npm 外壳与 runtime 更新

**npm 外壳**与 **Python runtime** 独立编号。外壳只提供稳定入口：首次运行时从 GitHub Releases 下载已打包的 runtime，验证 SHA-256 并缓存；普通命令最多每 24 小时检查一次兼容版本。工具目录、安装器与框架适配更新只需发布 runtime，无需重复上传 npm 包。

```sh
apd --shell-version     # npm 外壳版本
apd --version           # 当前 runtime 版本
apd runtime status      # 读取本地选择与缓存，不联网
apd runtime update      # 立即检查稳定 runtime 通道
```

`runtime` 子命令由 npm 外壳提供。需要固定版本时设置 `APD_RUNTIME_VERSION=0.3.0`；设置 `APD_OFFLINE=1` 可使用已经缓存的 runtime。离线模式控制的是启动器，安装尚未缓存的上游 skills 仍可能需要联网。详见 [runtime 选择与缓存](docs/NPM-RUNTIME.md) 和 [发布流程](docs/RELEASING.md)。

## 浏览工具集合

[精选目录](docs/CATALOG.md) 包含工具用途、上游仓库、许可证、核验日期和安装支持情况；[调研记录](docs/RESEARCH.md) 提供筛选依据与版本来源。

| 可安装精选 | 本工具包包含的能力 |
| --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | 3 个 skills：系统调试、测试驱动开发、交付前验证。 |
| [wshobson/agents](https://github.com/wshobson/agents) | 2 个 Python skills：测试模式与打包发布。 |
| [ECC](https://github.com/affaan-m/ECC) | 15 个 skills、6 套规则，覆盖安全、工程规范、Python、TypeScript、Go、Java 和框架实践。 |
| [Context7](https://github.com/upstash/context7) | 通过 MCP 获取库文档和对应版本的代码示例。 |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 浏览器检查与交互式 Web 测试。 |
| [Fetch MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 将网页获取为文本或 Markdown，用于文档查阅和调研。 |
| [Serena](https://github.com/oraios/serena) | 固定 commit 的 MCP-to-LSP 桥接，提供符号导航、引用和诊断。 |

[完整参考集合](docs/CATALOG.md) 还收录了 [OpenSpec](https://github.com/Fission-AI/OpenSpec)、[Spec Kit](https://github.com/github/spec-kit)、[GitHub MCP](https://github.com/github/github-mcp-server)、[uv](https://github.com/astral-sh/uv)、[Ruff](https://github.com/astral-sh/ruff) 和安全扫描工具。

标记为 **installable** 的条目已提供安装配方；没有安装配方的条目作为参考，由上游项目负责安装。`lsp` 分类同时包含可安装的 Serena 桥接和独立语言服务参考。

```sh
apd list --kind skill
apd list --kind rules
apd list --kind mcp
apd list --kind lsp
apd list --kind reference
apd list --json
```

## 选择工具包

| 预设 | 适用场景 |
| --- | --- |
| 🌱 `starter` | 系统调试、测试驱动开发、交付验证、Context7 与通用工程规则。 |
| 🐍 `python` | 核心工作流，加 Python 模式、测试、打包、Python 规则与 Fetch MCP。 |
| 🌐 `web` | 核心工作流，加前端模式、TypeScript 规则与 Playwright MCP。 |
| `engineering` | 编码规范、API 设计、数据库迁移、部署与通用规则。 |
| `security` | 安全复核指导与通用工程、安全规则。 |
| `django` | Django 模式与安全、Python 测试和规则。 |
| `fastapi` | FastAPI/Python 模式、API 设计、安全复核、测试与 FastAPI 规则。 |
| `springboot` | Spring Boot 模式与安全、Java 规则、API 设计和数据库迁移。 |
| `typescript` | 前后端模式、Next.js/Turbopack 指导、安全复核与 TypeScript 规则。 |
| `golang` | Go 模式与规则、API 设计、安全复核。 |
| `lsp` | 将 Serena LSP 桥接配置为 MCP server。 |

`apd profiles` 列出每个预设的具体条目。规则依赖会自动加入：语言规则依赖通用规则，FastAPI 规则还依赖 Python 规则。也可以通过 ID 选择单项工具：

```sh
apd profiles
apd init --profile fastapi --agents codex,claude
apd init --agents codex --tools systematic-debugging
apd init --agents codex --tools serena
apd init --agents all --profile starter --dry-run
```

按实际使用的 agent 选择目标。`all` 会为所有已支持的适配器生成配置，无论对应应用是否已安装。

按项目真实技术栈选择预设，并结合实际框架版本使用指导；其中 Next.js/Turbopack skill 面向 Next.js 16+。预设安装是叠加的，连续安装无关语言规则会增加指令体积，可能触及 agent 的大小限制。

## 支持的 agent

| Agent | 参数 ID | 安装范围 |
| --- | --- | --- |
| Claude Code | `claude` | 项目内 skills 与 MCP 配置。 |
| Codex | `codex` | 项目内 skills 与 TOML MCP 配置。 |
| Cursor | `cursor` | 项目内 skills 与 MCP 配置。 |
| GitHub Copilot in VS Code | `vscode` | 项目内 skills 与 VS Code 工作区 MCP 配置。 |
| OpenCode | `opencode` | 项目内 skills 与 MCP 配置。 |

具体路径、官方文档和兼容性边界见 [适配说明](docs/AGENTS.md)。自动化测试覆盖配置格式与合并行为；各 agent 应用的端到端运行验证状态应单独判断。`vscode` 指 VS Code 内的 Copilot，不代表独立的 GitHub Copilot CLI。

## 规则与框架实践

精选的 [ECC](https://github.com/affaan-m/ECC) skills 和规则采用 MIT 许可证，固定到经过审阅的 commit，并校验归档 SHA-256。[ECC 迁移说明](docs/ECC-MIGRATION.md) 记录了来源、版本、文件白名单、依赖及宿主适配。原始规则保存在 `.awesome-python-dev/rules/<id>/`，附带归属信息；适配后的副本通过各 agent 原生指令机制激活。

| Agent | 规则激活位置 |
| --- | --- |
| Claude Code | `.claude/rules/apd-<id>/*.md` |
| Cursor | `.cursor/rules/apd-<id>/*.mdc` |
| GitHub Copilot in VS Code | `.github/instructions/apd-<id>/*.instructions.md` |
| Codex / OpenCode | 项目 `AGENTS.md` 中共享的受管理块，嵌入适配后的正文和语言范围。 |

`AGENTS.md` 受管理块以外的原文会保留。安装器拒绝冲突，没有强制覆盖模式。选择 Codex 时，会检查生成的 `AGENTS.md` 是否超过默认的 32 KiB 指令限制，超限即停止，不截断规则。

这里迁移的是精选指导文件，不会整套安装 ECC 的 agents、hooks、模型偏好或后台服务；工作流角色引用会按宿主 agent 进行适配。安全扫描、测试、迁移和部署仍使用项目自己的工具与权限。

## LSP 与安全工具

`apd init --agents codex --tools serena` 会写入固定版本的 Serena MCP 启动配置，选择 Python 3.13 和 LSP 后端，由 agent 后续启动。在临时 Python 项目中已验证 MCP 握手和 22 项工具发现，但没有执行符号操作或逐个验证 agent 界面。运行条件、独立语言服务、OpenCode 原生 LSP 和兼容边界见 [LSP 指南](docs/LSP.md)。

`security` 预设安装安全复核指导与规则。[Semgrep](https://github.com/semgrep/semgrep)、[Bandit](https://github.com/PyCQA/bandit)、[pip-audit](https://github.com/pypa/pip-audit) 和 [Gitleaks](https://github.com/gitleaks/gitleaks) 作为项目检查、CI 的参考工具收录。安装指导不会自动安装扫描器，也不代表项目已经通过安全审计。

## 常用命令

```sh
# 指定项目目录。
apd init --path ../my-project --agents codex --profile python

# 查看支持的 agent 及项目配置路径。
apd agents

# 检查已安装文件、配置和运行条件。
apd doctor --path ../my-project

# 预览卸载，再移除 apd 管理的安装内容。
apd remove --path ../my-project --dry-run
apd remove --path ../my-project
```

通过 `apd --help` 和 `apd init --help` 查看完整参数。重复运行 `init` 会添加所选工具，切换预设不会删除之前安装的内容。`remove` 移除本项目中由 `apd` 管理且未被修改的资源，保留无关的用户内容；发生修改冲突时保护用户变更。安装后查看 `git diff`，需要团队共享时将生成的项目配置提交到版本管理。

**从 v0.1 升级：**v0.2 CLI 可读取 schema 1、2 的安装记录，执行 `init` 时会将 schema 1 升至 2。请保留 manifest 和备份；升级后使用 v0.2 或更新版本管理该安装，v0.1 无法管理 schema 2。

## 安装机制

```text
精选目录 → 选择预设或工具 → agent 适配 → 写入项目
                              ↓
                       安装记录与 doctor 检查
```

- Skills 与规则固定到上游 Git commit，下载归档时校验 SHA-256，并保留选中的辅助文件和上游许可证。
- MCP 配方固定包版本，Serena 桥接固定 Git commit，再转换为不同 agent 的配置格式。
- 安装记录用于识别本工具管理的内容，避免卸载时影响其他配置；已修改的托管文件受到保护。
- 请保留 `.awesome-python-dev/manifest.json`，供后续刷新和卸载使用。配置备份位于 `.awesome-python-dev/backups/`，带有 Git 忽略规则，应保持私密。
- `--dry-run` 可先预览操作；安装范围为项目目录，不修改用户主目录中的 agent 配置。
- 安装器不会执行下载的 skill 脚本。后续 skill 指令和 MCP 工具如何运行，由 coding agent 的权限机制控制。

固定版本有助于审查更新，但不会锁定所有间接依赖。认证、服务限额、浏览器下载与客户端授权仍取决于具体工具。详见 [安全说明](SECURITY.md)。

## 收录标准

优先选择用途明确、文档可用、来源可信、许可证清晰，并具有持续维护证据的项目。Star 数用于发现候选项目，同时结合实际场景与集成成本判断。

进入可安装集合，还需要可复现的安装配方、可核验的源码或包版本、明确的目录和运行要求，以及完整的上游归属信息。规则包还需要文件白名单、依赖声明和原生激活测试。需要凭据、手动配置或额外适配的工具，可以先作为参考项目收录。

## 参与贡献

欢迎推荐项目、完善安装配方、补充经过测试的 agent 适配。请先阅读 [贡献指南](CONTRIBUTING.md) 和 [路线图](docs/ROADMAP.md)。提交问题时，请移除日志、配置中的密钥和其他敏感内容。

自动化检查与执行结果见 [CI 工作流](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml)，本地运行方法见 [贡献指南](CONTRIBUTING.md)。

组织方式参考 [Awesome](https://github.com/sindresorhus/awesome)、[Awesome Python](https://github.com/vinta/awesome-python) 和 [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)；项目初始化体验受到 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 启发。

本项目独立维护。安装器和原创文档采用 [MIT 许可证](LICENSE)，上游项目的代码、skills 与商标归原作者所有，并保留各自许可证。

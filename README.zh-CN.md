# Awesome Python Dev

**精选 AI 开发工具包，一条命令装进你的 coding agent。**

[![CI](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/m9rco/awesome-python-dev?logo=github)](https://github.com/m9rco/awesome-python-dev/issues)

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Catalog](https://img.shields.io/badge/Catalog-Skills%20%2B%20MCP-6f42c1)](docs/CATALOG.md)

[English](README.md) · 简体中文

收集 GitHub 上实用、成熟、有明确来源的 AI 开发工具，并将经过适配的工具组合成可安装的工具包。**Skill** 提供可复用的开发流程，**MCP** 让 coding agent 连接工具和外部上下文。

安装器使用 Python 编写，并提供 Python 开发预设；整个集合也覆盖 Web 和通用软件开发。目前支持 **Claude Code、Codex、Cursor、VS Code Copilot 和 OpenCode**。

首版收录 **23 个条目：5 个可安装 skill、3 个可安装 MCP server，以及 15 个参考项目**，提供 **5 种 coding agent** 适配。

## 目录

- [快速开始](#快速开始)
- [浏览工具集合](#浏览工具集合)
- [选择工具包](#选择工具包)
- [支持的 agent](#支持的-agent)
- [常用命令](#常用命令)
- [安装机制](#安装机制)
- [收录标准](#收录标准)
- [参与贡献](#参与贡献)

## 快速开始

先安装 [uv](https://docs.astral.sh/uv/getting-started/installation/)，然后在**需要配置的项目目录**中执行：

```sh
uvx --from 'git+https://github.com/m9rco/awesome-python-dev.git@v0.1.0' apd init --agents codex,claude --profile starter
```

命令会下载选中的 skills，生成项目内的 agent 配置。随后重启或重新加载 agent，处理客户端的 MCP 授权提示即可使用。Codex 需要信任该项目后才会读取项目配置，具体见 [agent 适配说明](docs/AGENTS.md)。

经常使用时，可以先安装 CLI：

```sh
uv tool install 'git+https://github.com/m9rco/awesome-python-dev.git@v0.1.0'
apd list
apd init --agents codex,claude --profile starter --dry-run
apd init --agents codex,claude --profile starter
apd doctor
```

`awesome-python-dev` 与 `apd` 是同一个命令的两个名称。需要 Python 3.11+，从 Git 安装还需要 Git 和 GitHub 网络访问。首版直接从本仓库安装，不依赖 PyPI 上的同名包。

不同 MCP 的运行条件不同：npm 类型需要 Node.js 和 `npx`，Python 类型需要 `uvx`。`apd init` 负责写入 MCP 配置，agent 加载配置后才会启动相关进程；coding agent 本身仍需自行安装。

Starter 预设中的 Context7 需要 **Node.js 20.18.1 或更新版本**。Windows 下的 npm 配方使用 `cmd /c npx`。已有 JSONC 配置会保留；添加 MCP 前需转换为 JSON，也可以通过 `--tools` 仅安装 skills。

运行 `apd init --agents codex --profile starter --dry-run` 的预览示例：

```text
Preview only (no downloads or writes):
codex: skill systematic-debugging -> .agents/skills/systematic-debugging
codex: skill test-driven-development -> .agents/skills/test-driven-development
codex: skill verification-before-completion -> .agents/skills/verification-before-completion
codex: MCP context7 -> .codex/config.toml
```

## 浏览工具集合

[精选目录](docs/CATALOG.md) 包含工具用途、上游仓库、许可证、核验日期和安装支持情况；[调研记录](docs/RESEARCH.md) 提供筛选依据与版本来源。

| 可安装精选 | 本工具包包含的能力 |
| --- | --- |
| [Superpowers](https://github.com/obra/superpowers) | 3 个 skills：系统调试、测试驱动开发、交付前验证。 |
| [wshobson/agents](https://github.com/wshobson/agents) | 2 个 Python skills：测试模式与打包发布。 |
| [Context7](https://github.com/upstash/context7) | 通过 MCP 获取库文档和对应版本的代码示例。 |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 浏览器检查与交互式 Web 测试。 |
| [Fetch MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) | 将网页获取为文本或 Markdown，用于文档查阅和调研。 |

[完整参考集合](docs/CATALOG.md) 还收录了 [OpenSpec](https://github.com/Fission-AI/OpenSpec)、[Spec Kit](https://github.com/github/spec-kit)、[GitHub MCP](https://github.com/github/github-mcp-server)、[Serena](https://github.com/oraios/serena)、[uv](https://github.com/astral-sh/uv) 和 [Ruff](https://github.com/astral-sh/ruff) 等项目。

标记为 **installable** 的条目已提供安装配方；**reference** 条目已收录，安装仍由上游项目负责。

```sh
apd list --kind skill
apd list --kind mcp
apd list --kind reference
apd list --json
```

## 选择工具包

| 预设 | 适用场景 |
| --- | --- |
| 🌱 `starter` | 系统调试、测试驱动开发、交付验证，以及 Context7。 |
| 🐍 `python` | Starter + Python 测试模式、Python 打包，以及 Fetch MCP。 |
| 🌐 `web` | Starter + Playwright MCP 浏览器工具。 |

每个预设包含的具体条目见目录。也可以通过 ID 选择单项工具：

```sh
apd init --agents cursor --profile web
apd init --agents codex --tools systematic-debugging
apd init --agents all --profile starter --dry-run
```

按实际使用的 agent 选择目标。`all` 会为所有已支持的适配器生成配置，无论对应应用是否已安装。

## 支持的 agent

| Agent | 参数 ID | 安装范围 |
| --- | --- | --- |
| Claude Code | `claude` | 项目内 skills 与 MCP 配置。 |
| Codex | `codex` | 项目内 skills 与 TOML MCP 配置。 |
| Cursor | `cursor` | 项目内 skills 与 MCP 配置。 |
| GitHub Copilot in VS Code | `vscode` | 项目内 skills 与 VS Code 工作区 MCP 配置。 |
| OpenCode | `opencode` | 项目内 skills 与 MCP 配置。 |

具体路径、官方文档和兼容性边界见 [适配说明](docs/AGENTS.md)。自动化测试覆盖配置格式与合并行为；各 agent 应用的端到端运行验证状态应单独判断。`vscode` 指 VS Code 内的 Copilot，不代表独立的 GitHub Copilot CLI。

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

## 安装机制

```text
精选目录 → 选择预设或工具 → agent 适配 → 写入项目
                              ↓
                       安装记录与 doctor 检查
```

- Skills 固定到上游 Git commit，下载归档时校验 SHA-256，并保留辅助文件和上游许可证。
- MCP 配方固定包版本，再转换为不同 agent 的配置格式。
- 安装记录用于识别本工具管理的内容，避免卸载时影响其他配置；已修改的托管文件受到保护。
- 请保留 `.awesome-python-dev/manifest.json`，供后续刷新和卸载使用。配置备份位于 `.awesome-python-dev/backups/`，带有 Git 忽略规则，应保持私密。
- `--dry-run` 可先预览操作；安装范围为项目目录，不修改用户主目录中的 agent 配置。
- 安装器不会执行下载的 skill 脚本。后续 skill 指令和 MCP 工具如何运行，由 coding agent 的权限机制控制。

固定版本有助于审查更新，但不会锁定所有间接依赖。认证、服务限额、浏览器下载与客户端授权仍取决于具体工具。详见 [安全说明](SECURITY.md)。

## 收录标准

优先选择用途明确、文档可用、来源可信、许可证清晰，并具有持续维护证据的项目。Star 数用于发现候选项目，同时结合实际场景与集成成本判断。

进入可安装集合，还需要可复现的安装配方、可核验的源码或包版本、明确的目录和运行要求，以及完整的上游归属信息。需要凭据、手动配置或额外适配的工具，可以先作为参考项目收录。

## 参与贡献

欢迎推荐项目、完善安装配方、补充经过测试的 agent 适配。请先阅读 [贡献指南](CONTRIBUTING.md) 和 [路线图](docs/ROADMAP.md)。提交问题时，请移除日志、配置中的密钥和其他敏感内容。

自动化检查与执行结果见 [CI 工作流](https://github.com/m9rco/awesome-python-dev/actions/workflows/ci.yml)，本地运行方法见 [贡献指南](CONTRIBUTING.md)。

组织方式参考 [Awesome](https://github.com/sindresorhus/awesome)、[Awesome Python](https://github.com/vinta/awesome-python) 和 [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)；项目初始化体验受到 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 启发。

本项目独立维护。安装器和原创文档采用 [MIT 许可证](LICENSE)，上游项目的代码、skills 与商标归原作者所有，并保留各自许可证。

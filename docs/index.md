# Documentation / 文档索引

Awesome Python Dev is a curated catalog and project-local installer for coding
agent skills, rules, MCP servers, and LSP integrations. The package name is
`awesome-python-dev`; the CLI aliases are `apd` and `awesome-python-dev`.

这是项目文档入口：按使用场景查找安装、兼容性、收录证据和维护流程。
首次使用可从 [English README](../README.md) 或 [中文 README](../README.zh-CN.md)
开始；无需克隆仓库即可运行 `uvx awesome-python-dev init`。

## Use the toolkit / 使用工具包

| Need / 需求 | Documentation / 文档 |
| --- | --- |
| Install and preview a toolkit / 安装与预览 | [Quick start](../README.md#quick-start) · [中文快速开始](../README.zh-CN.md#快速开始) |
| Find a tool and check installation support / 查找工具及安装支持 | [Curated catalog](CATALOG.md) · [Browsable website](https://m9rco.github.io/awesome-python-dev/) |
| Check agent paths and configuration / 查看 agent 路径及配置 | [Agent compatibility](AGENTS.md) |
| Use code intelligence / 使用代码智能 | [LSP bridge and native language servers](LSP.md) |
| Understand imported rules / 了解上游规则适配 | [ECC source, scope, and adaptations](ECC-MIGRATION.md) |
| Choose npm or Python and update / 选择发行方式与更新 | [npm shell, runtime selection, cache, and proxies](NPM-RUNTIME.md) |
| Review trust and report vulnerabilities / 安全边界及漏洞反馈 | [Security policy](../SECURITY.md) |

## Verify and contribute / 核验与贡献

| Need / 需求 | Documentation / 文档 |
| --- | --- |
| Find selection evidence and review dates / 收录依据与核验日期 | [Research notes](RESEARCH.md) |
| Suggest tools, add recipes, or develop adapters / 推荐工具及开发适配 | [Contribution guide](../CONTRIBUTING.md) |
| Inspect upstream attribution / 查看上游归属 | [Third-party notices](../THIRD_PARTY_NOTICES.md) |
| Distinguish shipped features from plans / 区分已交付功能与计划 | [Changelog](../CHANGELOG.md) · [Roadmap](ROADMAP.md) |
| Build and publish the website / 构建与发布网站 | [Website maintenance](WEBSITE.md) |
| Publish a runtime or launcher / 发布 runtime 或外壳 | [Independent release workflows](RELEASING.md) |
| Understand module responsibilities / 理解模块职责 | [Architecture guide](ARCHITECTURE.md) |
| Work on this repository with an agent / 使用 agent 修改本仓库 | [Repository instructions](../AGENTS.md) |

`../AGENTS.md` guides contributors working on this repository.
[`docs/AGENTS.md`](AGENTS.md) documents the coding agents that the toolkit can
configure in a user's project; they serve different purposes.

## Agent discovery / Agent 检索入口

The website serves HTML and plain-text representations of the reviewed catalog,
so agents can read project facts and installation requirements without running
browser JavaScript. Prefer these public entry points when referring another
agent to the project:

| Endpoint | Contents |
| --- | --- |
| [Integration guide](https://m9rco.github.io/awesome-python-dev/agents/) | How to inspect the catalog, select a supported target, and preview installation. |
| [Text integration guide](https://m9rco.github.io/awesome-python-dev/agents/index.md) | The guide as Markdown. |
| [llms.txt](https://m9rco.github.io/awesome-python-dev/llms.txt) | A compact index linking project documentation and tool pages. |
| [catalog.json](https://m9rco.github.io/awesome-python-dev/catalog.json) | Machine-readable catalog data generated from the repository's canonical source. |
| [English overview](https://m9rco.github.io/awesome-python-dev/index.md) · [中文概览](https://m9rco.github.io/awesome-python-dev/zh/index.md) | Project summaries as Markdown. |

Tool and profile pages also have `index.md` companions. These files help readers
retrieve project information; they do not guarantee that a search engine or
agent will discover, rank, recommend, or cite it.

## Source of truth / 数据与源码归属

The [catalog JSON](../src/awesome_python_dev/data/catalog.json) is the canonical
source for tool IDs, kinds, descriptions, upstream URLs, review metadata,
installation recipes, and profile membership. A missing installation recipe
means reference-only. [`CATALOG.md`](CATALOG.md) explains the collection, while
[`RESEARCH.md`](RESEARCH.md) records the evidence supporting integration choices.
Keep those documents consistent when changing the catalog.

The Python implementation lives in [`src/awesome_python_dev/`](../src/awesome_python_dev/).
The independently versioned npm launcher lives in [`npm/`](../npm/).
[`pyproject.toml`](../pyproject.toml) defines Python package metadata;
[`npm/package.json`](../npm/package.json) defines launcher metadata.

Website build and validation entry points live in [`scripts/`](../scripts/).
The [`scripts/sitegen/`](../scripts/sitegen/) package owns configuration, page
rendering, and discovery-file generation; [`site/assets/`](../site/assets/)
contains browser styles and enhancements. The build reads canonical catalog
and release metadata. `_site/` contains generated HTML and discovery files;
`dist/` contains generated distribution assets. Neither is an independent source
to edit. CI regenerates and validates outputs before publishing them.

仓库 `main` 与网站可能包含尚未发布的新增条目。查询已安装版本时使用
`apd --version`、`apd list --json` 和 `apd profiles --json`，引用能力时注明对应版本。
适配器测试、MCP 协议握手与真实 agent 会话是不同层次的验证，应按文档记录说明。

# ECC migration / ECC 精选迁移

本项目从 [affaan-m/ECC](https://github.com/affaan-m/ECC) 迁移一组可独立使用的 Skills 和规则。旧地址 [`affaan-m/everything-claude-code`](https://github.com/affaan-m/everything-claude-code) 目前重定向到该仓库。

用户提到的“黑客松获奖者项目”与这个来源相符：上游作者在 [README 的 Background](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/README.md#background) 中称，自己和合作者在 2025 年 9 月 Anthropic × Forum Ventures 黑客松获胜，并以 agent 工作流构建了 zenith.chat。这是作者的背景陈述；本项目没有独立核验比赛结果，也不把 ECC 本身称作获奖作品。

## 来源与校验

| 字段 | 已核验值 |
| --- | --- |
| Canonical repository | `affaan-m/ECC` |
| 核验日期 | 2026-10-27 |
| GitHub stars | 290,505，整个仓库的当日快照 |
| 最近 push | 2026-10-26T04:56:56Z |
| 许可证 | MIT；根 `LICENSE` 为 Copyright (c) 2026 Affaan Mustafa |
| 固定 commit | `25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b` |
| Archive SHA-256 | `7979cc21e2093aed6218fa1709373eff5eb8641b0c0a5128c68db91bbedd7bb1` |
| 压缩包大小 | 35,750,329 bytes，约 34.1 MiB |
| 展开文件内容合计 | 62,082,979 bytes，约 59.2 MiB |
| Archive members | 6,384 |

数据来自 [GitHub repository API](https://api.github.com/repos/affaan-m/ECC)、[固定源码树](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b)、[根许可证](https://github.com/affaan-m/ECC/blob/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/LICENSE) 和实际下载的 [固定 commit 归档](https://codeload.github.com/affaan-m/ECC/tar.gz/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b)。所有条目共享同一个归档和缓存，不需要为每个 Skill 重复下载。归档在 64 MiB 下载限制、256 MiB 展开限制内。

## 精选 Skills

每个条目保留上游原生名称、`SKILL.md` frontmatter、完整子目录及 MIT 许可证。固定快照中已核验以下 15 个目录；它们的原生名称没有与现有目录冲突。

| 工作领域 | Skills |
| --- | --- |
| 安全与工程规范 | `security-review`、`coding-standards` |
| Python / FastAPI | `python-patterns`、`fastapi-patterns` |
| Django | `django-patterns`、`django-security` |
| React / Next.js / Node.js | `frontend-patterns`、`nextjs-turbopack`、`backend-patterns` |
| Spring Boot | `springboot-patterns`、`springboot-security` |
| Go | `golang-patterns` |
| API、数据库与发布 | `api-design`、`database-migrations`、`deployment-patterns` |

`security-review` 的 `cloud-infrastructure-security.md` 随同安装。`frontend-patterns` 是本次 React/Next.js 入口；它在这个快照中是完整的独立目录，不依赖其他 ECC Skill 或 reviewer agent。更专门的 `react-patterns` 包含多个未选中的同级 Skill 和规则链接，因此没有整套引入。`nextjs-turbopack` 明确面向 Next.js 16+，应结合项目实际版本和官方文档使用。

这里的成熟度依据是可追溯上游、维护活动、明确许可证、完整目录和实际集成校验。仓库 star 数不能证明每个 Skill 的示例都适用于任意框架版本；本项目没有执行所有示例，也没有声称这些文字指导等同于安全审计。

## 规则包与依赖

规则采用 `install.type: "rules"`，`install.files` 是相对 `install.subdir` 的明确白名单，`install.globs` 是目标语言范围。语言包通过 `requires` 依赖 `ecc-common-rules`；FastAPI 包依赖 Python 包，并传递获得通用包。

| ID | 上游目录与文件 | 原始 UTF-8 bytes |
| --- | --- | ---: |
| `ecc-common-rules` | `rules/common/`: `coding-style.md`, `security.md`, `testing.md`, `git-workflow.md`, `patterns.md`, `development-workflow.md` | 9,399 |
| `ecc-python-rules` | `rules/python/`: `coding-style.md`, `security.md`, `testing.md`, `patterns.md` | 2,639 |
| `ecc-typescript-rules` | `rules/typescript/`: 同上四个文件 | 6,230 |
| `ecc-golang-rules` | `rules/golang/`: 同上四个文件 | 2,484 |
| `ecc-java-rules` | `rules/java/`: 同上四个文件 | 14,794 |
| `ecc-fastapi-rules` | `rules/python/`: 仅 `fastapi.md` | 1,736 |

通用包无语言范围；Python 使用 `**/*.py` / `**/*.pyi`，TypeScript 包含 TS/TSX/JS/JSX，Go 包含 Go 文件及 `go.mod` / `go.sum`，Java 使用 `**/*.java`。FastAPI 保留上游的 `**/app/**/*.py`、`**/fastapi/**/*.py`、`**/*_api.py`，只应在实际 FastAPI 项目中选择；`app/` 名称本身不能识别框架，所以它不并入通用 Python 包。

上游语言文件具有简单 `paths:` YAML frontmatter，并通过 `../common/<name>.md` 引用对应通用规则。通用 `git-workflow.md` 与 `development-workflow.md` 相互引用。原始文件需要保留；目标 agent 的激活副本负责转换 frontmatter 和链接，不能通过简单平铺文件破坏这些关系。

通用包加最大的 Java 包原始合计 24,193 bytes，适合有大小保护的单语言指令块。六套原始规则合计 37,282 bytes，已经超过 32 KiB；应选用实际技术栈，不能宣称把全部规则嵌入一个 32 KiB 指令块仍然无损。

实际激活内容还包含来源链接、范围和适配说明。当前渲染器测得通用包为 12,463 bytes，通用加 Python 为 17,563 bytes，通用加 TypeScript 为 20,662 bytes，通用加 Go 为 17,218 bytes，通用加 Java 为 30,943 bytes。六套合并为 51,357 bytes，超过嵌入上限；尺寸判断应使用最终渲染结果，而非仅使用上表原始文件大小。

## 可移植激活的边界

没有选择 `common/agents.md`、`common/hooks.md`、`common/performance.md` 或任何语言的 `hooks.md`。这避免直接导入 ECC 的 agent 调度、自动 hooks 和模型选择策略。但其余文件仍含少量 ECC 环境假设，目标适配器必须明确处理这些内容，而不能声称复制文本就安装了对应功能。

| 上游位置 | 可移植解释 / 适配要求 |
| --- | --- |
| `common/security.md` | `security-reviewer` 是安全复核角色；使用当前 agent 或已有可用复核者，不假定 ECC agent 已注册。 |
| `common/testing.md` | `tdd-guide` 是测试工作流角色；不能自动调用未安装的 agent。 |
| `common/development-workflow.md` | `planner` / `tdd-guide` / `code-reviewer` 按规划、测试、复核职责理解；不隐式安装 Exa，也不强制当前 agent 具有这些工具。 |
| `common/patterns.md` | 并行评估是可选执行方式；保留安全、扩展性、适配性等评估事项，不要求开启多 agent。 |
| `common/git-workflow.md` | 关于 ECC 修改 `~/.claude/settings.json` 署名设置的段落不适用于本安装器；不修改 attribution 或用户配置。 |
| `typescript/coding-style.md` | `See hooks for automatic detection` 不能成为已安装自动检查的承诺。 |
| `typescript/security.md` / `testing.md` | `security-reviewer` / `e2e-runner` 是可选复核角色；安装规则不会注册这些 agent 或运行 Playwright。 |

激活规则时应注明它们来自 ECC、经过哪些宿主适配，并服从目标项目已有约定。原始归档内容、来源和许可证保持可追溯；不能把激活副本的改写冒充上游原文。语言规则中提到的 Bandit、gosec、pytest、formatter、Java 工具链等仍是项目依赖，规则安装不会自动安装或运行它们。

适配器把原始文件保存在 `.awesome-python-dev/rules/<id>/`，附带来源、许可证和 `APD-ADAPTATION.txt`。激活副本包含来源说明，转换已知 ECC 专用语句，并将相对上游链接转换为固定 commit 的 GitHub 链接。

| 目标 | 激活位置 |
| --- | --- |
| Claude Code | `.claude/rules/apd-<id>/*.md` |
| Cursor | `.cursor/rules/apd-<id>/*.mdc` |
| GitHub Copilot | `.github/instructions/apd-<id>/*.instructions.md` |
| Codex / OpenCode | 项目 `AGENTS.md` 中带标记的受管理块；嵌入适配后的规则正文和语言范围说明 |

Codex 与 OpenCode 共享同一个项目指令块；原始文件保存位置与激活副本分开，便于校验来源和追踪宿主适配。安装器不把整个 ECC 根指令文件复制到目标项目。

部分规则把其他 ECC Skill 列为延伸阅读，例如 `python-testing`、`golang-testing`、`java-coding-standards`、`jpa-patterns`、`springboot-tdd` 和 Quarkus 系列。它们不属于本次精选集，也不作为悬空 `requires`。需要阅读时应使用 [固定上游 skills 目录](https://github.com/affaan-m/ECC/tree/25278e7d7b6cf6e6a4e7a6c8e10f14ff22f0eb5b/skills)；现有 `python-testing-patterns` 仍承担本项目的 pytest 指导。

## 没有迁移的 ECC 组件

本集成不安装 ECC marketplace/plugin、slash commands、agents、hooks、memory/instinct 服务、后台任务、模型配置、provider、凭据或其根 `AGENTS.md` / `CLAUDE.md`。它也不运行上游安装脚本，不把 ECC 仓库的身份或研发要求写成宿主项目身份。需要完整 ECC 工作流时应查看其 [官方安装说明](https://github.com/affaan-m/ECC#install-ecc)，并检查与已有相同名称 Skills 的冲突。

安装完成代表选定的指导文件及目标 agent 激活配置已经生成；它不代表安全扫描、类型检查、测试、迁移或部署已经执行。这些工作仍应由实际项目工具、权限和用户任务决定。

## 后续更新

更新固定 commit 时同时审阅 Skills、规则白名单、路径范围、许可和跨文件链接，重新下载归档计算 SHA-256，并检查尺寸限制。对新增 hook、agent、全局设置或模型条款单独评估；不因上游新增文件就自动扩大迁移范围。随后验证各目标 agent 的预览、安装、重复安装、更新和卸载行为。

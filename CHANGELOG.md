# Changelog

## Unreleased

- Agent discovery: generated `llms.txt`, per-page Markdown counterparts, a
  source-attributed JSON catalog and an Agent integration guide. Discovery links
  preserve custom domains and project subpaths; source snapshots are explicitly
  distinguished from the catalog bundled in published runtimes.
- Website build implementation is organized into `scripts/sitegen/` modules,
  retaining the existing build entry point. Added a documentation index,
  architecture map and repository instructions for contributing agents.
- Bilingual README FAQs and GitHub metadata describe actual installation support;
  existing badges are preserved. CI validates discovery links, catalog parity,
  installable/reference boundaries and generated command IDs.

Catalogue additions from the daily candidate review.

- Two pinned skills from `addyosmani/agent-skills` (`code-review-and-quality`,
  `observability-and-instrumentation`) with their archive SHA-256, and three
  reference-only entries: `ty` (Python type checker and language server),
  `agent-lsp` (agent-facing LSP bridge), and `HypothesisWorks/hypothesis`.
- The catalog now has 59 entries: 32 installable resources (22 skills, 6 rule
  packs, 3 MCP servers, and Serena's bridge) and 27 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-10-29 candidate review.

- Two installable MCP servers, both smoke-checked through
  `scripts/smoke_mcp.py`: `code-review-graph` (pinned
  `uvx --from code-review-graph==2.3.9`, 30 tools discovered) and `mcp-tools-py`
  (pinned `uvx --from mcp-tools-py==0.1.10 --with mcp<2`, 17 tools discovered;
  Python lint, test, type, and refactor operations behind one project scope).
- Two reference-only entries: `codebase-memory-mcp`, a native code knowledge
  graph whose npm/PyPI packages are installer wrappers, and `mcpls`, a Rust
  MCP-to-LSP bridge over `rust-analyzer`, `pyright`, and `gopls`.
- The catalog now has 63 entries: 34 installable resources (22 skills, 6 rule
  packs, 5 MCP servers, and Serena's bridge) and 29 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-10-30 candidate review.

- One installable MCP server, smoke-checked through `scripts/smoke_mcp.py`:
  `fallow` (pinned `npx --yes --package fallow@3.37.0 fallow-mcp`, 43 tools
  discovered; TypeScript and JavaScript complexity, duplication, architecture,
  styling, and dead-code findings).
- Two reference-only entries: `github/awesome-copilot`, a large community
  Copilot instruction/agent/skill collection contributed file by file, and
  `NVIDIA/SkillEvaluator`, a skill-quality and live-impact evaluator whose PyPI
  name is a zero-version placeholder.
- `chunkhound` was reviewed and recorded as a reference: its pinned stdio
  command never completed `initialize` in a fresh project inside the smoke
  window on this host, so no recipe was admitted.
- The catalog now has 67 entries: 35 installable resources (22 skills, 6 rule
  packs, 6 MCP servers, and Serena's bridge) and 32 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-01 candidate review.

- One installable MCP server, smoke-checked through `scripts/smoke_mcp.py`:
  `repomix` (pinned `npx -y repomix@1.18.1 --mcp`, 6 tools discovered;
  repository packing and pack read/grep for agent context, with the documented
  non-sandbox boundary recorded in the notes).
- Three reference-only entries: `meta/pyrefly` (Rust-based Python type checker
  and language server next to Pyright and ty), `google/osv-scanner`
  (dependency, SBOM, and container vulnerability scanning against the OSV
  database), and `osprey-oss/deptry` (declared-versus-used dependency checks,
  previously published under `fpgmaas/deptry`).
- The catalog now has 71 entries: 36 installable resources (22 skills, 6 rule
  packs, 7 MCP servers, and Serena's bridge) and 35 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-02 candidate review.

- Three installable integrations, all smoke-checked through
  `scripts/smoke_mcp.py`: `Cranot/roam-code` (pinned
  `uvx --python 3.12 --from 'roam-code[mcp]==14.1.0' roam mcp`, 17 tools
  discovered), `FROWNINGdev/orm-lens` (pinned
  `uvx --python 3.12 --from 'orm-lens[mcp]==1.16.0' orm-lens-mcp`, 13 tools
  discovered), and `ProfessioneIT/lsp-mcp-server` (pinned
  `npx -y lsp-mcp-server@1.1.27`, 29 tools discovered) as the second
  MCP-to-LSP bridge next to Serena. The two `uvx` recipes pin the interpreter
  because their MCP extras require Python 3.10 or newer.
- One reference-only entry: `Goldziher/ai-rulez`, an authoring and governance
  layer that compiles rules, skills, and MCP settings into native files for
  dozens of agents. Its npm and PyPI packages install a native release binary
  instead of providing a pinnable launcher, so it is recorded as a reference.
- The catalog now has 75 entries: 39 installable resources (22 skills, 6 rule
  packs, 9 MCP servers, and 2 LSP bridges) and 36 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change; the generated site's LSP tool pages now describe
  each bridge's own prerequisites instead of Serena's.

Catalogue additions from the 2026-11-03 candidate review.

- One installable integration, smoke-checked through `scripts/smoke_mcp.py`:
  `headroomlabs-ai/headroom` (pinned
  `uvx --python 3.13 --from 'headroom-ai[mcp]==0.42.0' headroom mcp serve`,
  3 tools discovered), a local context-compression layer that shrinks tool
  output, logs, files, and RAG chunks before they reach the model and exposes
  `headroom_compress`, `headroom_retrieve`, and `headroom_stats` over MCP.
- Three reference-only entries: `alibaba/open-code-review`, an agent-driven
  review CLI whose reviewer is a global npm CLI needing a configured provider;
  `modelcontextprotocol/inspector`, the reference MCP debugging client; and
  `googleapis/mcp-toolbox`, Google's database MCP server whose useful launches
  need database credentials and a `tools.yaml`.
- The catalog now has 79 entries: 40 installable resources (22 skills, 6 rule
  packs, 10 MCP servers, and 2 LSP bridges) and 39 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-04 candidate review.

- Two installable MCP servers, both smoke-checked through `scripts/smoke_mcp.py`:
  `kitfunso/hippo-memory` (pinned `npx -y hippo-memory@3.2.2 mcp`, 13 tools
  discovered), a local-first long-term memory store for coding agents, and
  `reticlehq/reticle` (pinned `npx -y @reticlehq/server@3.9.0 mcp`, 10 tools
  discovered), which drives a project's running web app in a real browser and
  returns pass/fail/cannot-tell verdicts with the `file:line` behind them.
- Two reference-only entries: `redhat-et/ripwire`, a ranked call-graph CLI whose
  one-line install ships a release binary and seventeen agent skills and whose
  MCP server is a flag on the same binary, and `tombi-toml/tombi`, a
  schema-driven TOML formatter, linter, and language server for files such as
  `pyproject.toml`.
- The catalog now has 83 entries: 42 installable resources (22 skills, 6 rule
  packs, 12 MCP servers, and 2 LSP bridges) and 41 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-05 candidate review.

- Four reference-only entries: `Graphify-Labs/graphify`, a coding-agent skill
  that turns a repository, its docs, SQL schemas and configuration into a
  queryable knowledge graph from local deterministic parsing with no vector
  store; `CodeBoarding/CodeBoarding`, hybrid static analysis plus LLM agents
  that render a codebase as interactive architecture maps and Markdown, HTML,
  MDX or reStructuredText documentation; `IBM/mcp-context-forge`, IBM's
  gateway, registry and proxy in front of MCP, A2A and REST/gRPC servers; and
  `intellectronica/ruler`, which applies one `.ruler/` instruction and MCP
  source to the native rule, skill, subagent and MCP files of more than thirty
  coding agents.
- None of the four was admitted as installable: `graphify` and `CodeBoarding`
  are CLI steps that need an installed engine, a registered skill, or a
  configured model provider before they produce anything, `mcp-context-forge`
  is a long-running gateway that will not start without generated secrets, and
  `ruler` rewrites many native files across a project rather than writing one
  launch configuration.
- The catalog now has 87 entries: 42 installable resources (22 skills, 6 rule
  packs, 12 MCP servers, and 2 LSP bridges) and 45 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-06 candidate review.

- One installable MCP server, smoke-checked through `scripts/smoke_mcp.py`:
  `misata` (pinned `uvx --python 3.12 --from 'misata[mcp]==0.9.8.1'
  misata-mcp`, 15 tools discovered; multi-table synthetic test data compiled
  from declared facts, with a DuckDB-checkable certificate, next to a CLI and
  a pytest plugin).
- Three reference-only entries: `agent-sh/agnix`, 758 rules that lint and
  auto-fix agent configuration (`CLAUDE.md`, `AGENTS.md`, `SKILL.md`, hooks,
  plugin and MCP files) shipped as a CLI, an `agnix-lsp` language server and an
  optional `agnix-mcp` server; `NVIDIA/SkillSpector`, which scans a skill
  directory, MCP server, Git URL, archive or registry snapshot for prompt
  injection, exfiltration, credential access and supply-chain risk before
  installation; and `hyhmrright/brooks-lint`, six review modes for architecture
  decay, technical debt and test weakness whose installer copies a
  shared-`_shared/` skill set this catalog cannot pin as one directory.
- The catalog now has 91 entries: 43 installable resources (22 skills, 6 rule
  packs, 13 MCP servers, and 2 LSP bridges) and 48 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-07 candidate review.

- Two installable MCP servers, both smoke-checked through `scripts/smoke_mcp.py`:
  `SeleniumBase/SeleniumBase` (pinned `uvx --python 3.13 --from
  'seleniumbase[mcp]==4.57.1' seleniumbase-mcp`, 24 tools discovered) drives
  Chrome through SeleniumBase's pure CDP Mode with no WebDriver or chromedriver
  and ships that server inside the test framework's own PyPI distribution;
  `bytebase/dbhub` (pinned `npx -y @bytebase/dbhub@1.5.1 --transport stdio
  --demo`, `execute_sql` and `search_objects` discovered) executes SQL and
  searches schemas on PostgreSQL, MySQL, MariaDB, SQL Server, Oracle and SQLite
  and starts on a bundled sample SQLite database, so its stored command needs no
  credentials before the user swaps in a `--dsn`.
- Two reference-only entries: `spec-kitty/spec-kitty`, which keeps specs, work
  packages, review and merge state in the repository and runs each work package
  in an isolated git worktree (reference-only because `spec-kitty init` installs
  into every harness it detects and its 4.x line is still a release candidate
  over the stable `3.2.7` on PyPI), and `mcpware/cross-code-organizer`, a local
  dashboard that inventories what each harness loads, edits memory and skill
  files in place, repairs duplicates and scans MCP tool descriptions for
  poisoning (reference-only because it is an interactive local application
  rather than one of the four install types).
- The catalog now has 95 entries: 45 installable resources (22 skills, 6 rule
  packs, 15 MCP servers, and 2 LSP bridges) and 50 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-08 candidate review.

- One installable MCP server, smoke-checked through `scripts/smoke_mcp.py`:
  `mustel-py/mustel` (pinned
  `uvx --python 3.12 --with mcp<2 --from mustel==0.3.4 mustel serve`, 5 tools
  discovered; Ruff, Bandit, Oxlint and pip-audit in one stdio server with a
  compressed AST code map and an audit mode that also runs dependency
  vulnerability checks).
- Three reference-only entries: `stbenjam/skillsaw`, a PyPI linter for the
  skills, plugin manifests, hooks, instruction files and MCP metadata a coding
  agent loads, recorded next to `agnix` for its different delivery shape;
  `wdm0006/python-skills`, a Claude Code plugin marketplace whose Python bundles
  cover the library lifecycle but whose members share `skills/common/*` files and
  whose repository is scheduled to be renamed; and `google/agents-cli`, Google's
  seven-skill ADK lifecycle bundle plus the `google-agents-cli` CLI, which stays
  a reference because the bundle is not one pinnable subtree and its deploy,
  publish and hosted-eval paths need the user's own Google Cloud project.
- The catalog now has 99 entries: 46 installable resources (22 skills, 6 rule
  packs, 16 MCP servers, and 2 LSP bridges) and 53 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-09 candidate review.

- One installable MCP server, smoke-checked through `scripts/smoke_mcp.py`:
  `squirrelscan/squirrelscan` (pinned `npx -y squirrelscan@0.0.173 mcp`, protocol
  2025-11-25, 15 tools discovered; a website audit that returns SEO,
  accessibility, performance, content and link findings written for an agent to
  fix).
- Three reference-only entries: `google/elephant-goldfish-model`, a
  Google-published multi-harness plugin whose ten reviewer agents draft a design
  and then attack it, recorded in `spec-driven-development`; `pipelab-org/pipelock`,
  an AI agent firewall that mediates egress and MCP traffic against a policy file
  and emits signed action receipts, recorded in `security-tooling`; and
  `iyazerski/lspyx`, a Python-only MCP bridge over `ty` and Ruff, recorded in
  `lsp-bridge` next to `mcpls` and `agent-lsp`.
- The catalog now has 103 entries: 47 installable resources (22 skills, 6 rule
  packs, 17 MCP servers, and 2 LSP bridges) and 56 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-10 candidate review.

- One installable skill: `OthmanAdi/planning-with-files` — plans, progress and
  findings kept in `.planning/`, per-turn plan re-injection against context rot,
  recovery after `/clear` or compaction, and a deterministic completion gate.
  The pinned `skills/planning-with-files` archive was downloaded and SHA-256
  verified; nothing was installed.
- Three reference-only entries: `nextlevelbuilder/ui-ux-pro-max-skill`, the
  design-intelligence skill whose local style, palette, typography and UX data
  is queried by Python scripts and delivered through a per-client generator CLI,
  recorded in `framework-best-practices`; `agentskills/agentskills`, the Agent
  Skills specification plus the `skills-ref` reference validator, recorded in
  `skill-ecosystem`; and `ArcadeAI/arcade-mcp`, the Python MCP server framework
  (`pip install arcade-mcp`), recorded in `build-mcp` next to `fastmcp` and the
  official `mcp-python-sdk`.
- The catalog now holds 107 entries: 48 installable resources (23 skills, 6 rule
  packs, 17 MCP servers, and 2 LSP bridges) and 59 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-10 evening candidate review.

- Four reference-only entries after de-duplication against the previous 107:
  `trailofbits/skills`, the Trail of Bits Agent Skills marketplace (47
  plugins) recorded in `security`; `oceanbase/powercontext`, the server-side
  memory, handoff and experience layer recorded in `mcp-ecosystem`; and two
  standalone language servers, `DetachHead/basedpyright` and
  `bellini666/pytest-language-server`, recorded next to `pyright`, `ty` and
  `pyrefly`.
- The catalog now holds 111 entries: 48 installable resources (23 skills, 6 rule
  packs, 17 MCP servers, and 2 LSP bridges) and 63 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-11 candidate review.

- One installable skill, `retentioneering/retentioneering-tools`
  (`retentioneering-product-analytics`), pinned to commit
  `68f699f67674375c59ea26c6a719e91e83905f51` with archive SHA-256
  `c0fe070c7ad6…`, recorded in `data-workflows`.
- Four reference-only entries: `ast-grep/ast-grep` (structural search and
  rewrite for the Python toolchain), `anthropics/claude-plugins-official`
  (the 317-plugin Claude Code marketplace), `google/mantis` (agentic security
  review: 19 skills plus an ADK harness) and `aoci-spec/aoci-code`
  (local-first code-map MCP server, FSL-1.1-MIT).
- The catalog now holds 116 entries: 49 installable resources (24 skills, 6 rule
  packs, 17 MCP servers, and 2 LSP bridges) and 67 references.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, `docs/LSP.md`, and both READMEs were
  updated in the same change.

Catalogue additions from the 2026-11-12 candidate review.

- Two installable MCP servers, both smoke-checked through
  `scripts/smoke_mcp.py`: `MinishLab/semble` (pinned
  `uvx --python 3.12 --from 'semble[mcp]==0.7.3' semble`, 2 tools discovered;
  CPU-only code search, recorded in `mcp-ecosystem`) and `hslee16/Archy`
  (pinned `uvx --python 3.12 --from archy==0.55.1 archy mcp`, 14 tools
  discovered; Python import-graph architecture assertions, recorded in
  `python-toolchain`).
- One reference-only entry: `scverse/acumen`, harness and scoring method for
  building an agentic skill for a Python package, recorded in
  `skill-ecosystem`.
- The catalog now holds 119 entries: 51 installable resources (24 skills, 6 rule
  packs, 19 MCP servers, and 2 LSP bridges) and 68 references. Profiles and rule
  dependencies are unchanged; no launcher or installer behaviour was touched.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.

Catalogue additions from the 2026-11-13 candidate review.

- Four reference-only entries, recorded from repository, package and registry
  metadata only: `schemathesis/schemathesis` (tests derived from an OpenAPI,
  GraphQL or gRPC schema, run through a CLI that exits non-zero or through
  pytest; PyPI `4.33.4`) and `inducer/pudb` (full-screen console debugger, the
  first debugger in the catalog; PyPI `2026.1`) in `python-toolchain`,
  `miqdadbadjuber/anti-slop` (six Agent Skills that filter generic AI output,
  installed flat by `npx antislop-ai` or a per-agent plugin route, so no single
  subtree is pinnable) in `engineering-skills`, and `modem-dev/hunk` (terminal
  review surface for an agent's diff, delivered as a standalone binary or
  `hunkdiff` npm `0.25.0`) in `delivery-workflows`.
- The catalog now holds 123 entries: 51 installable resources (24 skills, 6 rule
  packs, 19 MCP servers, and 2 LSP bridges) and 72 references. Profiles and rule
  dependencies are unchanged; no launcher or installer behaviour was touched.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change.
- `docs/LSP.md` records both the 2026-11-13 verification and the 2026-11-12 one
  the previous pass omitted (two MCP entries launched through their pinned
  commands, 2 and 14 tools listed, no `tools/call`), and `docs/RESEARCH.md`
  moves its research date to 2026-11-13.

Catalogue additions from the 2026-11-14 candidate review.

- One installable MCP server, launched through `scripts/smoke_mcp.py` at the
  pinned version: `Ataraxy-Labs/sem` (pinned `npx -y @ataraxy-labs/sem@0.30.1
  mcp`; `initialize` negotiated protocol `2025-11-25` against server `rmcp`
  1.6.0 and 8 tools were listed, with no `tools/call`; entity-level diff,
  impact, history, context and review verdicts over a change, recorded in
  `delivery-workflows`).
- Two reference-only entries, recorded from repository, package and registry
  metadata only: `syrupy-project/syrupy` (pytest snapshot testing, the entry
  the previous pass held back until the `--snapshot-update` workflow had been
  reviewed; PyPI `7.0.0`) in `python-toolchain`, and `level09/enferno` (Flask
  and Vue 3 framework that ships its own agent contract - `AGENTS.md`, an
  `.agents/skills/enferno-dev` skill, an opt-in read-only `flask mcp` server
  and `/llms.txt`) in `framework-best-practices`.
- The catalog now holds 126 entries: 52 installable resources (24 skills, 6 rule
  packs, 20 MCP servers, and 2 LSP bridges) and 74 references. Profiles and rule
  dependencies are unchanged; no launcher or installer behaviour was touched.
- `docs/CATALOG.md`, `docs/RESEARCH.md`, and both READMEs were updated in the
  same change; `docs/RESEARCH.md` moves its research date to 2026-11-14 and
  `docs/LSP.md` is untouched because this pass added no LSP entry.

Catalogue additions from the 2026-11-15 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `mcp-assert`
  (`build-mcp`, wire-level YAML assertions and schema linting for MCP servers,
  26 stars), `code-review-gate` (`engineering-skills`, four-probe
  evidence-backed review with a JSON-derived merge gate, 504 stars),
  `easement` (`engineering-rules`, cross-language architecture gate with a
  bundled agent skill and AGENTS.md setup prompt, 56 stars), `gawain`
  (`python-toolchain`, explicit-annotation gate before ty or pyrefly, 40
  stars) and `snitch` (`delivery-workflows`, deterministic detection of
  agent test tampering, 4 stars).
- All five are reference-only: their install paths are CLI/package/plugin
  routes that this catalog cannot pin, and no install, MCP handshake, hook or
  check was executed. Stars and `last_pushed_at` are the dated `gh api`
  observation; no launcher, profile or installer behaviour was changed.
- The catalog now holds 131 entries: 52 installable resources (24 skills, 6
  rule packs, 20 MCP servers, and 2 LSP bridges) and 79 references.
  `docs/CATALOG.md`, `docs/RESEARCH.md` and both READMEs were updated in the
  same change; `docs/LSP.md` is untouched because this pass added no LSP entry.

Catalogue additions from the 2026-11-16 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `pyscn`
  (`python-toolchain`, CFG-based dead code, clone, complexity and coupling
  analysis of AI-written Python with Agent Skills and an MCP server, 1,109
  stars), `wheelgap` (`python-toolchain`, prebuilt-wheel availability for a
  target platform from a lockfile, 3 stars), `agentic-radar`
  (`security-tooling`, agentic-workflow graph with OWASP LLM and Agentic AI
  threat mapping, 1,070 stars), `flisk` (`delivery-workflows`, one-command
  local multi-service runtime with 24 MCP tools and bundled skills, 50 stars)
  and `nreki` (`mcp-ecosystem`, RAM-side LSP edit validation and auto-heal
  before a file is written, 11 stars).
- All five are reference-only: their install paths are CLI, package or plugin
  routes this catalog cannot pin, and no install, MCP handshake, hook, scan or
  runtime check was executed. All 35 recorded GitHub blob evidence links were
  re-checked against the `/contents` endpoint; stars and `last_pushed_at` are
  the dated `gh api` observation. No launcher, profile or installer behaviour
  was changed.
- The catalog now holds 136 entries: 52 installable resources (24 skills, 6
  rule packs, 20 MCP servers, and 2 LSP bridges) and 84 references.
  `docs/CATALOG.md`, `docs/RESEARCH.md` and both READMEs were updated in the
  same change; `docs/LSP.md` is untouched because this pass added no
  `kind: lsp` entry.

Catalogue additions from the 2026-11-17 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `invaris-agentsec`
  (`security-tooling`, adversarial testing of a running agent over HTTP or MCP,
  26 stars), `tego` (`security-tooling`, kernel-enforced file, program and host
  contract on an agent process with a hash-chained run ledger, 25 stars),
  `kith` (`delivery-workflows`, scoped claims, isolated worktrees and mutexes
  for parallel coding agents, 4 stars), `qikly` (`python-toolchain`, mutation
  scoring of an existing Python test suite, 19 stars) and `techne`
  (`mcp-ecosystem`, checked IDE-grade navigation with evidence behind every
  answer, 3 stars).
- All five are reference-only: their install paths are CLI, package, Homebrew
  or plugin routes this catalog cannot pin, and no install, MCP handshake,
  hook, scan, mutation run or kernel behaviour check was executed. All 45
  recorded GitHub blob evidence links were validated against each repository's
  recursive git tree and re-checked against the `/contents` endpoint on
  `main`; stars and `last_pushed_at` are the dated `gh api` observation. No
  launcher, profile or installer behaviour was changed.
- The catalog now holds 141 entries: 52 installable resources (24 skills, 6
  rule packs, 20 MCP servers, and 2 LSP bridges) and 89 references.
  `docs/CATALOG.md`, `docs/RESEARCH.md` and both READMEs were updated in the
  same change; `docs/LSP.md` is untouched because this pass added no
  `kind: lsp` entry.


Catalogue additions from the 2026-11-18 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `kikimimi`
  (`delivery-workflows`, live agent token cost, stuck-agent thrash and MCP/skill
  context tax in local Parquet, 4 stars), `cap-evolve` (`skill-ecosystem`,
  eval-driven optimization of prompts, tools and skill packages behind a
  held-out significance gate, 70 stars), `acr` (`engineering-rules`, a package
  manager for agent instructions with byte-identical preservation of user-owned
  files, 9 stars), `backendskills` (`framework-best-practices`, backend
  correctness skills with a reproducible 150-run hidden-check benchmark, 60
  stars) and `skillware` (`skill-ecosystem`, versioned Python skill modules with
  typed contracts and offline assurance suites, 193 stars).
- All five are reference-only: their install paths are unpinned CLI, PyPI, npm,
  Homebrew, Go or plugin routes this catalog cannot pin, and no install, MCP
  handshake, hook, benchmark, optimization loop or kernel behaviour check was
  executed. All 56 recorded GitHub blob evidence links were validated against
  each repository's recursive git tree and re-checked against the `/contents`
  endpoint on `main`; stars and `last_pushed_at` are the dated `gh api`
  observation refreshed immediately before the write. No launcher, profile or
  installer behaviour was changed.
- The catalog now holds 146 entries: 52 installable resources (24 skills, 6
  rule packs, 20 MCP servers, and 2 LSP bridges) and 94 references.
  `docs/CATALOG.md`, `docs/RESEARCH.md` and both READMEs were updated in the
  same change; `docs/LSP.md` is untouched because this pass added no
  `kind: lsp` entry.


## npm shell 0.1.1 — 2026-10-28

- Honor HTTP/HTTPS proxy environment variables for GitHub runtime downloads,
  with `NO_PROXY` bypass rules and an explicit opt-out. Requires Node.js 22.21+
  (22.x) or 24.5+ for native proxy support; no npm dependencies were added.
- Publish the inspected npm tarball through GitHub OIDC and verify the exact
  version becomes publicly available with matching integrity.
- The Python package and runtime remain at **0.3.0**.

## 0.3.0 — 2026-10-28

Separate the npm command launcher from the Python toolkit runtime so routine
catalog and installer updates can ship through GitHub Releases.

- A small, dependency-free npm shell with independent versioning, command
  forwarding, verified runtime caching, explicit version pins and offline use.
- A self-contained Python zipapp with the locked `tomlkit` dependency, catalog,
  source provenance and licenses. Requires Python 3.11+ or an existing `uv`.
- Versioned runtime manifests and SHA-256 checksums, with a protocol-1 stable
  channel and independent GitHub runtime/npm publication workflows.
- PyPI distribution and short `uvx awesome-python-dev` / `uv tool install
  awesome-python-dev` entry points; runtime tags publish Python packages while
  npm shell tags publish only the launcher.
- Static GitHub Pages catalog with English and Chinese landing pages, tool and
  profile detail pages, metadata, sitemap and automatic deployment checks.

## 0.2.0 — 2026-10-27

Expand the collection into skills, native rules, MCP, and LSP tooling for security, engineering, and framework development.

- 54 catalog entries: 20 installable skills, 6 installable rule packs, 3 package-pinned MCP servers, 1 installable Serena LSP bridge, and 24 references.
- 15 selected MIT-licensed ECC skills for security review, coding standards, Python, Django, FastAPI, Spring Boot, frontend/backend development, Go, API design, migrations, and deployment.
- Six ECC rule packs with commit/archive pins, explicit file allowlists, language scopes, original-source preservation, and automatic common-rule dependencies.
- Native rules for Claude Code, Cursor, and VS Code Copilot; one shared managed `AGENTS.md` block for Codex/OpenCode. Preserve outside text, reject conflicts, and guard Codex output against the 32 KiB default instruction limit.
- Eleven profiles: `starter`, `python`, `web`, `engineering`, `security`, `django`, `fastapi`, `springboot`, `typescript`, `golang`, and `lsp`.
- `apd profiles`, `apd list --kind rules`, and `apd list --kind lsp`; updated starter/Python/web profiles include relevant rules.
- Serena v2.1.0 pinned to a full Git commit, with Python 3.13, the LSP backend, a single-project context, and explicit tool interface. The installer resolves the project path in the generated MCP command.
- Native LSP references for Pyright, Python LSP Server, Ruff, TypeScript Language Server, gopls, rust-analyzer, and clangd; security references for Semgrep, Bandit, pip-audit, and Gitleaks.
- Manifest schema 2, with schemas 1 and 2 readable by the new CLI and schema 1 upgraded during `init`.
- GitHub CI/release/stars/issues badges, independent linting, cross-platform wheel smoke checks, and downloadable CI artifacts.

**Upgrade note:** retain the installation manifest and backups. v0.1 cannot manage a schema 2 manifest; use v0.2 or newer after migration. Profiles remain additive, so select the actual project stack instead of accumulating all language rules.

Rule installation provides guidance, without installing ECC hooks/agents or running security scanners. Serena passed MCP initialization and discovery of 22 tools in a temporary Python project; no symbol operations or agent UI sessions were exercised. See [ECC scope and attribution](docs/ECC-MIGRATION.md) and [LSP verification](docs/LSP.md).

## 0.1.0 — 2026-10-27

Initial release of a curated AI development toolkit and project-local installer.

- 23 curated resources: 5 installable skills, 3 installable MCP servers, 15 reference projects.
- Native adapters for Claude Code, Codex, Cursor, GitHub Copilot in VS Code, and OpenCode.
- `starter`, `python`, and `web` profiles; explicit tool selection; interactive or detected agents.
- `init`, `list`, `agents`, `doctor`, and `remove` commands, with installation/removal previews.
- Commit-pinned skill archives with SHA-256 verification, complete support files, and upstream licenses.
- Exact direct MCP package versions; npm launch commands adapted for Windows.
- Ownership checks, additive installation, local backups, per-file atomic replacement, and rollback on ordinary write failures or interruption.
- English and Chinese documentation, contribution templates, and cross-platform CI.

MCP registration and local integrity checks are separate from live coding-agent validation. Protocol smoke tests cover initialization and tool discovery only; see [research evidence](docs/RESEARCH.md).


Catalogue additions from the 2026-11-19 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `eval-view`
  (`python-toolchain`, golden-baseline regression testing of an agent's
  tool-call trajectory plus MCP contract drift checks, 142 stars),
  `trajectory-ir` (`delivery-workflows`, portable hash-verifiable agent
  execution trajectory IR with sealed plans and signed `.tir` packages,
  32 stars), `signet` (`skill-ecosystem`, signed and transparency-logged
  skill/agent publication registry with a read-only MCP verification plane,
  132 stars), `agent-airlock` (`security-tooling`, Pydantic-strict in-process
  contract for agent tool calls with MCP CVE guards, 17 stars) and
  `phantom-secrets` (`security-tooling`, `.env` placeholder and local-proxy
  credential isolation for coding agents with an MCP server, 20 stars).
- Catalog grows from 146 to 151 entries: 52 installable/configurable
  integrations and 99 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  59 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint. No upstream
  package, binary, hook, proxy or MCP server was installed, configured or run,
  so no MCP smoke result is recorded for this date, `docs/LSP.md` is untouched
  and the count of `kind: lsp` entries remains 18.


Catalogue additions from the 2026-11-20 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `skillcrew`
  (`skill-ecosystem`, a governed team Git registry that keeps Agent Skills
  pinned and updated across agents, 39 stars), `prod-code` (`mcp-ecosystem`,
  remote LAN code-intelligence gateway exposing MCP tools to agents and an LSP
  server to editors, 8 stars), `rulebook` (`engineering-rules`, a macOS app
  that finds, compares, merges and audits CLAUDE.md and AGENTS.md across
  projects, 24 stars), `stalemap` (`framework-best-practices`, dependency API
  changes after a model's training cutoff written into agent instruction files,
  106 stars) and `ctxray` (`delivery-workflows`, static harness-loadout
  inspection with per-agent CI tests, 0 stars).
- Catalog grows from 151 to 156 entries: 52 installable/configurable
  integrations and 104 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  64 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint. No upstream
  package, binary, hook, application, gateway or MCP server was installed,
  configured or run, so no MCP smoke result is recorded for this date,
  `docs/LSP.md` is untouched and the count of `kind: lsp` entries remains 18.


Catalogue additions from the 2026-11-21 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `playwright-e2e`
  (`python-toolchain`, an MCP server and Agent Skill that runs, diagnoses,
  fixes and re-verifies failing Playwright and pytest tests, 6 stars),
  `testdesk` (`delivery-workflows`, a desktop test runner and stdio MCP
  server with a per-project queue and history, 0 stars), `sessionflow`
  (`delivery-workflows`, one local SQLite index over nine coding agents'
  session formats with provenance-linked handoff bundles, 7 stars),
  `symbolhop` (`mcp-ecosystem`, five read-only LSP navigation tools for
  terminal agents with no dependencies or network, 2 stars) and
  `mothersauce` (`python-skills`, 26 typed, tested Python 3.15 recipes
  served over MCP, a plugin and a skill, 0 stars).
- Catalog grows from 156 to 161 entries: 52 installable/configurable
  integrations and 109 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  60 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint. No upstream
  package, binary, application, server or language server was installed,
  configured or run, so no MCP smoke result is recorded for this date,
  `docs/LSP.md` is untouched and the count of `kind: lsp` entries remains 18.

Catalogue additions from the 2026-11-22 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `heki`
  (`python-toolchain`, a Python side-effect and mutation checker with
  certified exact rules, an LSP server and an Agent Skill, 1 star),
  `codecov-rust-mcp` (`python-toolchain`, Codecov patch coverage and missed
  changed lines over MCP, 3 stars), `python-upgrade-runner`
  (`python-toolchain`, a staged Python version upgrade skill with 161
  standard-library removal rules, 0 stars), `mcp-doctor` (`build-mcp`,
  validation, lint, conversion and handshake tests for nine MCP client
  config dialects, 0 stars) and `mcp-spy` (`mcp-ecosystem`, record, replay,
  mock and policy-gate the MCP traffic a real agent sends, 0 stars).
- Catalog grows from 161 to 166 entries: 52 installable/configurable
  integrations and 114 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  69 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint; one
  repository defaults to `dev` rather than `main`, and its evidence uses that
  ref. No upstream package, binary, application, server or language server
  was installed, configured or run, so no MCP smoke result is recorded for
  this date, `docs/LSP.md` is untouched and the count of `kind: lsp` entries
  remains 18.

Catalogue additions from the 2026-11-23 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `pydantic-ai-skills`
  (`python-skills`, Agent Skills for Pydantic AI with progressive disclosure,
  remote registries, bundled-file execution and a sandbox, 382 stars),
  `mipcode` (`python-toolchain`, a source-only Python delta check naming the
  other files a change left inconsistent, 2 stars),
  `python-package-template` (`python-toolchain`, a greenfield PEP 621
  template with nine checks, CI, releases and a bootstrap agent skill, 2
  stars), `devlogs` (`python-toolchain`, runtime application logs searchable
  by an agent over MCP, 0 stars) and `prefix-cache-audit`
  (`delivery-workflows`, first-divergence attribution of lost prompt-prefix
  cache hits with a counterfactual replay, 0 stars).
- Catalog grows from 166 to 171 entries: 52 installable/configurable
  integrations and 119 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  69 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint on `main`;
  the `/contents` check uses a `?ref=main` query string because passing
  `-f ref=main` to `gh api` on a GET returns a spurious 404. Candidates with
  no SPDX licence or `NOASSERTION` were excluded under the 2026-11-20 rule,
  including a Python-debugger MCP server that would otherwise have filled
  the last toolchain gap. No upstream package, binary, application, server,
  language server or MCP server was installed, configured or run, so no MCP
  smoke result is recorded for this date, `docs/LSP.md` is untouched and the
  count of `kind: lsp` entries remains 18.

Catalogue additions from the 2026-11-24 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `library-skills`
  (`skill-ecosystem`, version-matched Agent Skills shipped inside installed
  Python/JavaScript library packages as managed symlinks, 850 stars),
  `modern-web-guidance` (`framework-best-practices`, browser-vendor skills
  with compatibility data and a legacy-pattern scan, 25,796 stars), `woolly`
  (`engineering-rules`, flag instruction-file lines that name code a commit
  removed and rewrite them, 14 stars), `crapkit` (`python-toolchain`, CRAP
  scores from complexity and coverage.py with a ratchet commit gate over CLI,
  MCP and a GitHub Action, 1 star) and `trace2rules` (`engineering-rules`,
  audit AGENTS.md rules against real agent sessions and mine evidence-backed
  proposals, 6 stars).
- Catalog grows from 171 to 176 entries: 52 installable/configurable
  integrations and 124 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  75 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint, with
  `?ref=<branch>` in the URL query string; `trace2rules` uses `master` as its
  default branch. Candidates with no SPDX licence or `NOASSERTION` were
  excluded under the 2026-11-20 rule. No upstream package, binary,
  application, server, language server or MCP server was installed,
  configured or run, so no MCP smoke result is recorded for this date,
  `docs/LSP.md` is untouched and the count of `kind: lsp` entries remains 18.


Catalogue additions from the 2026-11-25 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `mcp-ade`
  (`mcp-ecosystem`, a headless MCP server orchestrating 52 LSP servers, nine
  DAP debug adapters and BSP build targets with a Python Pyright/debugpy
  extension, 0 stars, EPL-2.0, an Eclipse Foundation project proposal),
  `pkgtruth` (`python-toolchain`, npm and PyPI package-name ground truth for
  hallucinated and slopsquatted dependencies, 4 stars), `agentcheck`
  (`security-tooling`, hidden prompt injection in CLAUDE.md, AGENTS.md and
  MCP configs, 5 stars), `verdict-qa` (`delivery-workflows`, hash-chained QA
  finding memory with regression ranking and a read-only contract, 33 stars)
  and `context-inspector` (`delivery-workflows`, a live six-component context
  window token budget for OpenChamber and OpenCode, 5 stars).
- Catalog grows from 176 to 181 entries: 52 installable/configurable
  integrations and 129 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  78 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint, with
  `?ref=main` in the URL query string; every candidate in this batch uses
  `main` as its default branch. Candidates with no SPDX licence or
  `NOASSERTION` were excluded under the 2026-11-20 rule. No upstream package,
  binary, application, server, language server, debug adapter or MCP server
  was installed, configured or run, so no MCP smoke result is recorded for
  this date and `docs/LSP.md` is untouched; the count of `kind: lsp` entries
  remains 18.

Catalogue additions from the 2026-11-26 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `complaint-replay`
  (`delivery-workflows`, reproduce a user bug report in a real browser under
  the user's own conditions and open a PR with a fix and a guard test, 2 stars),
  `stitch-skills` (`framework-best-practices`, sixteen Agent Skills that turn
  Google Stitch designs into React, Vite, shadcn/ui or React Native components,
  13,193 stars, a first-party `google-labs-code` project), `secpriv-skill`
  (`security-tooling`, one detector-validator code-review skill across 20 CWE
  security and 10 GDPR privacy categories with a 128-case benchmark, 12 stars,
  a first-party `facebookresearch` artifact), `codex-config-doctor`
  (`engineering-rules`, report the merged config Codex CLI will actually apply,
  with 44 lint findings and a `why` command verified against the real binary,
  0 stars) and `ajiro-api` (`python-toolchain`, scan backend routes into one
  YAML contract per endpoint and run them as regression tests and mocks, 0 stars).
- Catalog grows from 181 to 186 entries: 52 installable/configurable
  integrations and 134 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write. All
  84 GitHub blob links in the five evidence lists were checked against each
  repository's recursive git tree and the `/contents` endpoint, with
  `?ref=main` in the URL query string; all five default branches are `main`.
  Candidates with no SPDX licence or `NOASSERTION` were excluded under the
  2026-11-20 rule. No upstream package, binary, application, server, language
  server or MCP server was installed, configured or run, so no MCP smoke result
  is recorded for this date, `docs/LSP.md` is untouched; the count of
  `kind: lsp` entries remains 18. The review ran across midnight CST: the
  branch is `feat/catalog-daily-20261127` while `checked_at`, `reviewed_at`
  and every document date are 2026-11-26, the date the review began.

Catalogue additions from the 2026-11-27 candidate review.

- Five reference-only entries, recorded from repository metadata, upstream
  documentation, file trees and licence files only: `mcpspan`
  (`mcp-ecosystem`, self-hosted analytics for MCP server calls, latency,
  failures, sessions and releases with eight SDKs including Python FastMCP,
  24 stars), `mcp-attest` (`security-tooling`, prove a live MCP server denies
  what a written policy denies with 24 rules, twelve OAuth checks and
  hash-chained signed evidence, 10 stars), `depquiet` (`python-toolchain`,
  turn unfixable Dependabot alerts into a change plan verified with the
  project's own uv, Poetry or npm resolver over CLI, MCP and a weekly Action,
  3 stars), `honest-tests` (`python-toolchain`, detect AI-written tests that
  can never fail and prove weak tests with mutation testing across JS/TS and
  Python pytest/unittest, 3 stars) and `research-to-fix`
  (`delivery-workflows`, research prior fixes across GitHub, arXiv and papers
  then repair and validate against a frozen, hash-pinned evidence ledger,
  3 stars).
- Catalog grows from 186 to 191 entries: 52 installable/configurable
  integrations and 139 reference-only tools. The installable counts and the
  18 LSP entries are unchanged; no recipe, adapter, profile, website template
  or release asset was modified.
- Stars, push timestamps, licences and archive flags are dated
  `gh api repos/<owner>/<repo>` observations refreshed before the write and
  again before the commit. All 70 GitHub blob links in the five evidence
  lists were checked against each repository's recursive git tree and the
  `/contents` endpoint, with `?ref=main` in the URL query string; all five
  default branches are `main`, and one transient `/contents` failure was
  confirmed present on retry. Candidates with no SPDX licence or
  `NOASSERTION` were excluded under the 2026-11-20 rule. No upstream package,
  binary, application, server, language server or MCP server was installed,
  configured or run, so no MCP smoke result is recorded for this date and
  `docs/LSP.md` is untouched; the count of `kind: lsp` entries remains 18.
  The review ran across midnight CST: the branch is
  `feat/catalog-daily-20261128` while `checked_at`, `reviewed_at` and every
  document date are 2026-11-27, the date the review began.

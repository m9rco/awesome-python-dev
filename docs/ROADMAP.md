# Roadmap

The goal is a curated AI development toolkit that can be installed into the coding agents a team uses. The collection should stay useful as upstream tools and agent formats change.

## v0.2 scope

- A reviewed catalog of 54 entries: 30 installable resources and 24 references, with explicit installation support.
- 20 skills, 6 native rule packs, 3 package-pinned MCP recipes, and a commit-pinned Serena MCP-to-LSP bridge.
- 11 profiles: starter, Python, web, engineering, security, Django, FastAPI, Spring Boot, TypeScript, Go, and LSP.
- Project-local adapters for Claude Code, Codex, Cursor, VS Code Copilot, and OpenCode.
- Native rule files and a shared managed `AGENTS.md` block, automatic common-rule dependencies, source preservation, and Codex instruction-size protection.
- Versioned sources, skill/rule archive integrity checks, upstream license preservation, dry-run previews, installation records, diagnostics, and removal.
- Manifest schema 1 compatibility with schema 2 upgrades during initialization.
- English and Chinese onboarding and a documented contribution process.

See the [changelog](../CHANGELOG.md) and test results for delivered behavior. Agent adapter tests validate files and merge semantics; client-level runtime verification is recorded separately. Serena passed protocol initialization and tool discovery; its symbol operations and every agent interface still need broader validation. See [LSP evidence](LSP.md) and the [ECC migration notes](ECC-MIGRATION.md).

## Next priorities

1. **Verify real client workflows.** Record a versioned compatibility matrix from installation through skill discovery, native rule activation, and an MCP tool call in each supported application. Exercise LSP symbol operations on representative projects and languages.
2. **Maintain the catalog.** Add automated checks for archived repositories, removed releases, source changes, package availability, and broken links. Review proposed pin updates before merging.
3. **Improve lifecycle management.** Add an explicit update plan with version diffs, selective removal, and recovery paths for interrupted writes. Preserve user modifications throughout.
4. **Validate framework guidance.** Test representative Django, FastAPI, Spring Boot, TypeScript, and Go workflows against documented framework versions. Evaluate data engineering and other profiles when there is a concrete use case.
5. **Support more agents.** Add adapters when project-local configuration and its merge behavior are documented and testable.
6. **Broaden delivery.** Evaluate package registry releases and signed release artifacts once release automation and provenance checks are in place.

## Requires a design proposal

- Remote HTTP MCP with client-specific authentication and secret references.
- Global or team-managed installation scope.
- Richer support for upstream plugin marketplaces and skills with cross-package dependencies.
- Native LSP configuration beyond the current MCP bridge, with explicit handling of client capabilities and language toolchains.
- Executable security/engineering checks, with reviewed commands and configuration rather than treating written rules as enforcement.
- Organization policies, private catalogs, and stricter dependency locking.

These items are plans, not current capabilities. Open an issue with the intended workflow and official upstream references to help prioritize them.

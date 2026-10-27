# Roadmap

The goal is a curated AI development toolkit that can be installed into the coding agents a team uses. The collection should stay useful as upstream tools and agent formats change.

## Initial scope

- A reviewed catalog with explicit installable and reference-only entries.
- Skills and stdio MCP recipes grouped into starter, Python, and web profiles.
- Project-local adapters for Claude Code, Codex, Cursor, VS Code Copilot, and OpenCode.
- Versioned sources, skill archive integrity checks, upstream license preservation, dry-run previews, installation records, diagnostics, and removal.
- English and Chinese onboarding and a documented contribution process.

See the release notes and test results for delivered behavior. Agent adapter tests validate files and merge semantics; client-level runtime verification is recorded separately.

## Next priorities

1. **Verify real client workflows.** Record a versioned compatibility matrix from installation through skill discovery and an MCP tool call in each supported application.
2. **Maintain the catalog.** Add automated checks for archived repositories, removed releases, source changes, package availability, and broken links. Review proposed pin updates before merging.
3. **Improve lifecycle management.** Add an explicit update plan with version diffs, selective removal, and recovery paths for interrupted writes. Preserve user modifications throughout.
4. **Expand useful profiles.** Evaluate API/backend, data engineering, testing, and release workflows based on concrete use cases.
5. **Support more agents.** Add adapters when project-local configuration and its merge behavior are documented and testable.
6. **Broaden delivery.** Evaluate package registry releases and signed release artifacts once release automation and provenance checks are in place.

## Requires a design proposal

- Remote HTTP MCP with client-specific authentication and secret references.
- Global or team-managed installation scope.
- Richer support for upstream plugin marketplaces and skills with cross-package dependencies.
- Organization policies, private catalogs, and stricter dependency locking.

These items are plans, not current capabilities. Open an issue with the intended workflow and official upstream references to help prioritize them.

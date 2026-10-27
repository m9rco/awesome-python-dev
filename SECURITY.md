# Security

## Installation boundary

`apd` installs selected skill files and configures MCP launch commands within a project. It does not execute downloaded skill scripts during installation, install coding agent applications, or silently add credentials. Your agent may subsequently follow those skills or start the configured MCP servers using its own permissions.

Skill archives are pinned to commits and checked against recorded SHA-256 hashes. MCP recipes pin direct package versions. These controls make upstream changes reviewable; they do not audit all upstream code or lock every transitive dependency resolved by package managers.

Review the catalog and upstream sources before using a toolkit in a sensitive repository. Keep secrets out of committed agent configuration. Handle authentication through the relevant client or the upstream tool's documented mechanism.

## Configuration and removal

Installation is project-local. The installer tracks managed content, preserves unrelated configuration, and stops on conflicts rather than silently replacing user changes. `--dry-run` provides a preview. Review generated changes before committing them.

Changed files are backed up under `.awesome-python-dev/backups/`, which includes its own Git ignore rule. Backups may contain existing configuration secrets; keep them private. Skill content hashes and source pins are recorded in `.awesome-python-dev/manifest.json`; retain that manifest to refresh or remove the installation. File replacements are atomic individually, with rollback for ordinary write failures and keyboard interrupts. This does not promise recovery from power loss or forced process termination.

Client trust settings, MCP approval prompts, and workspace permissions still apply. See [`docs/AGENTS.md`](docs/AGENTS.md) for client-specific notes. Local file checks and successful configuration generation do not establish that an upstream server is safe or available.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/m9rco/awesome-python-dev/security/advisories/new) when it is enabled. Include the affected version, a minimal reproduction, the impact, and any suggested fix. Do not include real credentials or private repository content.

If private reporting is unavailable, open an issue asking for a private reporting channel without disclosing exploit details. Ordinary installation failures can use the public bug template after sensitive information is removed.

Report vulnerabilities in an upstream skill or server to its maintainers as well. We can update or disable an affected recipe, while the upstream project owns its implementation.

## Supported versions

Security fixes are applied to the latest release. Earlier versions may require upgrading. Check the repository's releases and catalog history before refreshing a toolkit.

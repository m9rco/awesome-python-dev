# Security

## npm shell and runtime trust

The npm package is a launcher with a version independent of the Python toolkit.
It downloads executable runtime code from this project's GitHub Releases on
first use and refreshes the compatible stable selection at most once every
24 hours. `APD_RUNTIME_VERSION` pins an exact runtime; `APD_OFFLINE=1` requires
cached runtime files and disables launcher network access. Neither setting
changes the network requirements of third-party tool installation commands.

The launcher restricts manifests to its supported protocol, stable versions and
the project's versioned release asset paths. HTTPS redirects and download sizes
are bounded. Runtime size and SHA-256 are verified before caching and before
every launch. A network failure can fall back to an already verified cached
stable runtime; a malformed manifest or hash mismatch stops execution. Explicit
version pins never fall back to a different version.

Checksums detect altered or incomplete downloads; they are not a signature from
an independent authority. The npm package publisher, this GitHub repository and
its release maintainers remain trust sources. Anyone able to alter both the
runtime and its accepted manifest can replace executable code. Protect release
access and CI publishing configuration accordingly.

The bundled runtime includes its Python dependencies and licenses. It runs with
an existing Python 3.11+ in isolated mode, or through an existing uv installation
that can provision Python 3.13. There are no npm installation hooks and no
downloaded shell installer. `APD_PYTHON` accepts an exact executable path, not a
shell command. Runtime caches should remain writable only by the local user.
See [runtime distribution](docs/NPM-RUNTIME.md) and [publishing](docs/RELEASING.md).

## Installation boundary

`apd` installs selected skills and rules, activates project instructions, and configures MCP launch commands within a project. It does not execute downloaded skill scripts during installation, install coding agent applications, or silently add credentials. Your agent may subsequently follow those instructions or start the configured MCP servers using its own permissions.

Skill and rule archives are pinned to commits and checked against recorded SHA-256 hashes. Rules use an explicit file allowlist. MCP recipes pin direct package versions or, for Serena, a full Git commit. These controls make upstream changes reviewable; they do not audit all upstream code or lock every transitive dependency or language-server download.

Review the catalog and upstream sources before using a toolkit in a sensitive repository. Keep secrets out of committed agent configuration. Handle authentication through the relevant client or the upstream tool's documented mechanism.

## Guidance, rules, and LSP

Native rules are instructions interpreted by the coding agent, not a security enforcement mechanism. Original ECC files and licenses remain in `.awesome-python-dev/rules/<id>/`; adapted activation files identify their source. The integration does not install ECC agents, hooks, model settings, providers, or background services. Read the [migration scope](docs/ECC-MIGRATION.md) when reviewing the resulting instructions.

The `security` profile supplies review guidance and common rules. It does not run Semgrep, Bandit, pip-audit, Gitleaks, or a security audit. Framework examples must be checked against actual dependencies and versions, and checks must run with the project's intended scope and permissions.

Serena is configured as an MCP-to-LSP bridge. When the agent starts it, Serena may download dependencies, initialize language servers, and create its own user/project state. Its code-editing tools operate under that process's permissions. The selected context and tool interface are not a sandbox. `apd remove` does not remove upstream-created `.serena` state or caches. See [LSP runtime details and verification limits](docs/LSP.md).

## Configuration and removal

Installation is project-local. The installer tracks managed content, preserves unrelated configuration, and stops on conflicts rather than silently replacing user changes. `--dry-run` provides a preview. Review generated changes before committing them.

Codex and OpenCode share an embedded managed block in project `AGENTS.md`; existing text outside that block is preserved. Managed content changes are checked for conflicts, with no force-overwrite option. The installer enforces a 32 KiB output guard when Codex is selected, rather than truncating instructions. Repeated profile installation is additive and can reach that limit.

Changed files are backed up under `.awesome-python-dev/backups/`, which includes its own Git ignore rule. Backups may contain existing configuration secrets; keep them private. Content hashes, ownership, and source pins are recorded in `.awesome-python-dev/manifest.json`; retain that manifest to refresh or remove the installation. File replacements are atomic individually, with rollback for ordinary write failures and keyboard interrupts. This does not promise recovery from power loss or forced process termination.

v0.2 reads manifest schemas 1 and 2 and upgrades schema 1 during `init`. Keep the manifest and backups across the upgrade; use v0.2 or newer afterward because v0.1 cannot manage schema 2. Do not discard ownership records to bypass a conflict.

Client trust settings, MCP approval prompts, and workspace permissions still apply. See [`docs/AGENTS.md`](docs/AGENTS.md) for client-specific notes. Local file checks and successful configuration generation do not establish that an upstream server is safe or available.

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/m9rco/awesome-python-dev/security/advisories/new) when it is enabled. Include the affected version, a minimal reproduction, the impact, and any suggested fix. Do not include real credentials or private repository content.

If private reporting is unavailable, open an issue asking for a private reporting channel without disclosing exploit details. Ordinary installation failures can use the public bug template after sensitive information is removed.

Report vulnerabilities in an upstream skill or server to its maintainers as well. We can update or disable an affected recipe, while the upstream project owns its implementation.

## Supported versions

Security fixes are applied to the latest release. Earlier versions may require upgrading. Check the repository's releases and catalog history before refreshing a toolkit.

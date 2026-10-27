# Contributing

Help make a small, useful collection easy to trust and easy to install. Contributions may add a tool, improve an existing recipe, document a limitation, or support another coding agent.

## Suggest a tool

Open a tool suggestion issue or submit a focused pull request. Include:

1. The canonical upstream repository and official documentation.
2. A concrete AI development task it helps with, and why an existing entry does not cover that task.
3. Its license, maintenance status, recent release or commit, and any required accounts or services.
4. Whether you have used it, in which environment, and what you verified.
5. A proposed category and whether it should initially be reference-only or installable.

Prefer maintained projects with clear documentation and a useful workflow. A high star count helps discovery but is not sufficient for admission. Disclose if you maintain or are commercially affiliated with the project. Avoid duplicate entries, paid placement, unexplained superlatives, and large batches of unrelated links.

## Add an installable recipe

The machine-readable source is [`src/awesome_python_dev/data/catalog.json`](src/awesome_python_dev/data/catalog.json). Keep its documentation in [`docs/CATALOG.md`](docs/CATALOG.md) and evidence in [`docs/RESEARCH.md`](docs/RESEARCH.md) consistent.

- Use a stable, descriptive ID and a concise description of what the tool does.
- Skills require a full upstream commit, an HTTPS archive URL, its verified SHA-256, the skill directory, and the license location. Inspect the complete directory, including scripts and references.
- MCP recipes require an exact package version, the official launch command, and explicit runtime requirements. Do not use `latest`, shell pipelines, or embedded credentials.
- Link official source material for paths, configuration, and package identity. Record when you verified it; do not present a star snapshot as live data.
- Document network access, authentication, costs, or manual steps where they affect whether the user can run the tool.
- Confirm installation, a repeated installation, and removal in a temporary project. Test modified and unrelated configuration so it survives correctly.

Reference entries should use `install: null`. Never mark a tool installable solely because its upstream README has an install command.

## Add an agent adapter

Use current official documentation for project-local skill discovery and MCP configuration. Add the paths and limitations to [`docs/AGENTS.md`](docs/AGENTS.md). Include tests for empty configuration, existing unrelated values, name conflicts, malformed input, and removal. If the client supports a format the installer cannot safely edit, return a clear error rather than replacing it.

State what you tested: serialization and merge tests, MCP protocol startup, or a real session in the target client. These are different levels of evidence.

## Develop locally

```sh
git clone https://github.com/m9rco/awesome-python-dev.git
cd awesome-python-dev
uv sync --group dev
uv run pytest
uv run apd list
uv run apd init --agents codex --profile starter --dry-run
```

Keep changes focused. Add behavioral tests for new installation or configuration logic, and update both README languages when the user workflow changes. Use temporary paths for tests; never require a contributor's real agent configuration or credentials.

## Pull requests

Describe the user-visible change, upstream evidence, and verification performed. Identify breaking behavior and known limitations. Small fixes can go directly to a pull request; discuss major format, ownership, or distribution changes in an issue first.

By contributing, you agree that your original contribution is licensed under this project's MIT license. Third-party material must retain its original attribution and compatible license. Be respectful, assume good intent, and focus feedback on the work.

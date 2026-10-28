# Architecture and source ownership

The project has three independently maintained areas: the Python toolkit, the
npm launcher, and the generated documentation website. They share catalog facts
without making website generation part of an installed runtime.

| Area | Source | Responsibility |
| --- | --- | --- |
| Catalog | `src/awesome_python_dev/data/catalog.json` | Tool identity, kind, source evidence, install recipe and profile membership |
| CLI | `src/awesome_python_dev/cli.py` | Parse commands and present plans/results |
| Catalog validation | `src/awesome_python_dev/catalog.py` | Load and validate canonical data |
| Agent adapters | `src/awesome_python_dev/adapters.py` | Read and merge each client's MCP configuration |
| Rules | `src/awesome_python_dev/rules.py` | Preserve sources and generate native rule activation |
| Downloads | `src/awesome_python_dev/downloads.py` | Fetch and verify pinned upstream archives |
| Installer | `src/awesome_python_dev/installer.py` | Plan changes, track ownership, apply/roll back, inspect and remove |
| npm shell | `npm/bin/`, `npm/lib/` | Select, verify and cache the Python runtime; forward commands |
| Website configuration | `scripts/sitegen/config.py` | Shared site identity, presentation data and URL helpers |
| HTML rendering | `scripts/sitegen/renderer.py` | Static pages, navigation and structured metadata |
| Agent discovery | `scripts/sitegen/discovery.py` | Markdown counterparts, `llms.txt` and JSON catalog exports |
| Website assets | `site/assets/` | Optional browser search, copying and styling |

## Data flow

The CLI reads the validated canonical catalog. Website generation reads that
same catalog and derives tool/profile pages, counts and Agent discovery exports.
The generated `_site/` directory is disposable output and is not committed.
`docs/CATALOG.md` is the maintained human-readable catalog overview; it is not an
independent recipe database. Evidence and licensing belong in `docs/RESEARCH.md`,
`THIRD_PARTY_NOTICES.md` and the source records.

The website is deployed from `main`, so it can show catalog additions before a
runtime release includes them. Agents should use the site's source/snapshot
metadata to cite it, then use `apd list --json` and `apd profiles --json` to check
the catalog actually installed before choosing IDs. `init --dry-run` previews
the resulting configuration changes.

## Distribution boundaries

- **Python package / runtime:** `src/awesome_python_dev/` is packaged into a wheel
  and a self-contained zipapp. Runtime tags publish GitHub assets and PyPI.
- **npm shell:** the small `npm/` package obtains an integrity-checked runtime
  from GitHub Releases. Shell tags publish only npm; ordinary catalog updates do
  not need a new shell.
- **Website:** `scripts/build_site.py` is the stable build entry point;
  `scripts/sitegen/` contains its implementation. These build tools are outside
  the installed Python package and npm allowlist.

Existing `scripts/build_site.py` imports remain compatible for tests and local
automation. Keeping this entry point avoids breaking CI and contributors while
the implementation is organized by responsibility.

## Where to make common changes

| Change | Update | Verification |
| --- | --- | --- |
| Add a tool/profile | Canonical catalog, evidence, catalog docs | Catalog and installation preview tests; generated-site validation |
| Support another client | Adapters/rules/installer and `docs/AGENTS.md` | Configuration preservation, repeated installation and removal tests |
| Change Agent discovery | `scripts/sitegen/discovery.py` and renderer link metadata | Markdown/JSON parity, base-path links and reference-only behavior |
| Change website presentation | Renderer and `site/assets/` | Static-site tests, metadata and internal-link validation |
| Change runtime loading | `npm/lib/`, launcher docs | Node tests and installed-tarball smoke test |
| Publish | Version metadata and release workflows | [Release guide](RELEASING.md); never overwrite an immutable release |

See [the documentation index](index.md), [website operations](WEBSITE.md), and
[repository agent instructions](../AGENTS.md) for navigation and commands.

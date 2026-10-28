# npm shell and independent runtime

`awesome-python-dev` has two independently versioned layers. The npm shell
provides the command entry point and runtime loader. The Python runtime contains
the installer, agent adapters, catalog, rules support and locked dependencies.
The current shell is **0.1.1** and the runtime is **0.3.0**. Runtime updates do not
require a new npm version.

| Layer | Distribution | Update trigger |
| --- | --- | --- |
| npm shell | `awesome-python-dev` on npm; roughly 8 KB packed | Launcher behavior, platform support or runtime protocol changes |
| Python runtime | GitHub Release `.pyz`; roughly 362 KB for 0.3.0 | Installer, catalog, skills/rules integration and agent adapter changes |
| Python package | PyPI wheel and source distribution | Same version as the runtime, published by the runtime release workflow |

Package sizes are approximate and change with content. The zipapp includes
`tomlkit`, catalog data, dependency metadata and licenses; it does not include
the Python interpreter or download upstream skills in advance.

## Install

The npm entry point requires **Node.js 22.21+ (22.x) or 24.5+** and **Python 3.11+ or uv**:

```sh
npx awesome-python-dev init --agents codex,claude --profile starter
```

For repeated use:

```sh
npm install --global awesome-python-dev
apd init --agents codex,claude --profile fastapi --dry-run
apd init --agents codex,claude --profile fastapi
```

Use these commands inside the project you want to equip. When Python is not
available but uv is installed, uv can provision Python 3.13. The shell does not
install uv itself. Selected MCP servers may have additional prerequisites.

The Python distribution offers a separate, shorter Python-native route:

```sh
uvx awesome-python-dev init --agents codex,claude --profile starter
uv tool install awesome-python-dev
```

Choose one global installation method: both provide `apd` and
`awesome-python-dev`. A PyPI installation follows uv's package version and
upgrade behavior; it does not use the npm shell's runtime channel, cache or
`runtime` subcommands. Upgrade it with `uv tool upgrade awesome-python-dev`, or
use `uvx awesome-python-dev@latest` for a fresh latest-version invocation.

## Selection and updates

```sh
apd --shell-version
apd --version
apd runtime status
apd runtime update
```

`--shell-version` prints the npm package version without network access.
`--version` launches the selected runtime and prints its version. `runtime
status` reads local selection and cache information without downloading files.
`runtime update` checks the stable channel immediately unless a version is
selected through `APD_RUNTIME_VERSION`.

On normal invocations, the shell checks the compatible stable channel at most
once every 24 hours. The channel is the `runtime.json` asset on the
[`runtime-v1` GitHub Release](https://github.com/m9rco/awesome-python-dev/releases/tag/runtime-v1).
It points to an immutable versioned asset such as
`v0.3.0/awesome-python-dev-runtime-0.3.0.pyz`. The channel release is marked as a
prerelease to keep it separate from the project's normal latest release.

The loader validates the manifest, downloads the runtime if needed, checks its
size and SHA-256, and writes cache files atomically. It verifies the cached
runtime again before every launch. A failed network refresh can use a previously
verified stable runtime. An invalid manifest or checksum fails closed. The npm
package's embedded bootstrap manifest supplies a known version if the channel
is unreachable; first use still needs access to that runtime asset.

Runtime code downloads happen on first **use**, not during `npm install`. The
package has no `postinstall` hook or npm runtime dependencies. Arguments and
working directory pass through to the Python CLI.

## Proxies

The launcher honors `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY`, including their
lowercase forms, using Node's built-in proxy support. This applies to both
manifest and runtime asset downloads. Set `NODE_USE_ENV_PROXY=0` to explicitly
disable this behavior. The launcher does not change system or shell settings.

For a local HTTP proxy, export its actual address before invoking the CLI:

```sh
export HTTPS_PROXY=http://127.0.0.1:7897
npx awesome-python-dev --version
```

Use the HTTP endpoint provided by your proxy. A macOS system proxy setting or
`ALL_PROXY` alone does not configure Node's built-in HTTP proxy support.

## Pin a runtime

```sh
apd runtime update 0.3.0
APD_RUNTIME_VERSION=0.3.0 apd list
APD_RUNTIME_VERSION=0.3.0 apd init --agents codex --profile python --dry-run
```

`runtime update VERSION` downloads and verifies that exact version. It does not
permanently switch the default stable selection. Set `APD_RUNTIME_VERSION` to
select the version on subsequent commands. Exact pins never fall back to a
different runtime. Unset the variable to resume the stable channel.

For PowerShell:

```powershell
$env:APD_RUNTIME_VERSION = '0.3.0'
apd list
Remove-Item Env:APD_RUNTIME_VERSION
```

## Cache and offline use

| Variable | Meaning |
| --- | --- |
| `APD_RUNTIME_VERSION` | Exact stable version, such as `0.3.0` |
| `APD_OFFLINE=1` | Disable launcher network access; require a cached runtime |
| `APD_CACHE_DIR` | Override the runtime cache directory |
| `APD_PYTHON` | Exact path to a Python 3.11+ executable; no command arguments |

Default runtime cache locations are:

- macOS: `~/Library/Caches/awesome-python-dev`
- Linux: `$XDG_CACHE_HOME/awesome-python-dev`, or `~/.cache/awesome-python-dev`
- Windows: `%LOCALAPPDATA%\awesome-python-dev`

After caching a version, it can launch offline:

```sh
APD_RUNTIME_VERSION=0.3.0 APD_OFFLINE=1 apd list
```

Offline mode also disables uv network access and Python downloads when uv is
used. It does **not** make installation of uncached upstream skills, rules or
MCP dependencies work offline. The runtime cache is separate from the npm
installation and the project's `.awesome-python-dev` ownership records.
Deleting the user runtime cache reclaims space; the next online invocation
downloads the selected runtime again.

## Trust and compatibility

The loader accepts protocol-1 manifests and restricts download URLs to this
project's GitHub Releases, with bounded HTTPS redirects, timeouts and sizes.
SHA-256 verifies integrity against the manifest. It is not an independent
signature: the repository's release maintainers and npm publisher remain trust
sources. See the [security model](../SECURITY.md).

New runtime releases keep protocol 1 while compatible with existing shells. A
future incompatible protocol requires a new shell release and its own channel;
older shells must not silently execute an unsupported manifest. Follow the
[release guide](RELEASING.md) to publish runtime and shell changes separately.

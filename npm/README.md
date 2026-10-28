# Awesome Python Dev — npm launcher

A small command-line entry point for [Awesome Python Dev](https://m9rco.github.io/awesome-python-dev/): curated development skills, rules, MCP and LSP tools for Codex, Claude Code, Cursor, VS Code Copilot and OpenCode.

The npm package contains the **launcher only**. The Python **runtime** and tool catalog are distributed separately through GitHub Releases. Routine runtime releases do not require publishing another npm version.

## Install and use

Requires **Node.js 22.21+ (22.x) or 24.5+**, plus **Python 3.11+ or uv**. If Python is unavailable but uv is installed, uv can provision Python 3.13. The launcher does not install uv or run a downloaded shell installer.

```sh
npm install --global awesome-python-dev
apd init --agents codex,claude --profile starter --dry-run
apd init --agents codex,claude --profile starter
```

For a one-off invocation:

```sh
npx awesome-python-dev init --agents codex,claude --profile fastapi
```

Run commands inside the project you want to equip. The selected MCP servers may require their own runtimes, such as Node.js/npx. See the [installation guide](https://m9rco.github.io/awesome-python-dev/getting-started/).

## Two independent versions

```sh
apd --shell-version   # npm launcher version
apd --version         # Python runtime version
apd runtime status    # local selection and cache information; no network request
apd runtime update    # fetch the latest compatible stable runtime now
```

On normal commands the launcher checks the protocol-1 channel at most once every 24 hours. A verified runtime is cached in your user cache directory and SHA-256 checked again before every launch. A failed network refresh can use the previously verified cached stable runtime; invalid manifests and checksums fail closed. First use requires GitHub access.

The bootstrap manifest in the npm package supplies a known runtime when the channel cannot be reached. Runtime files are downloaded on first **use**, never during `npm install`; there is no `postinstall` hook and no npm runtime dependency.

If `HTTP_PROXY` or `HTTPS_PROXY` (including lowercase variants) is set, the launcher enables Node's built-in environment proxy support in a one-time child process. Node also honors `NO_PROXY`/`no_proxy`. An explicit `NODE_USE_ENV_PROXY=0` or Node proxy flag is preserved. This does not modify your system proxy or shell settings.

## Pinning and offline use

```sh
apd runtime update 0.3.0
APD_RUNTIME_VERSION=0.3.0 apd list
APD_RUNTIME_VERSION=0.3.0 APD_OFFLINE=1 apd list
```

`runtime update VERSION` downloads that version but does not change the default stable selection. Set `APD_RUNTIME_VERSION` to keep using a specific version. Explicit pins never fall back to another runtime. On PowerShell, set variables with `$env:APD_RUNTIME_VERSION = '0.3.0'`.

`APD_OFFLINE=1` disables **launcher** network access and requires an already cached runtime. It does not make runtime commands such as installing uncached third-party skills work offline. If uv is used, offline mode also disables its network access and Python downloads.

| Variable | Purpose |
| --- | --- |
| `APD_RUNTIME_VERSION` | Exact stable runtime version, for example `0.3.0`. |
| `APD_OFFLINE=1` | Use cached runtime metadata and files without network access. |
| `APD_CACHE_DIR` | Override the runtime cache directory. |
| `APD_PYTHON` | Exact path to a Python 3.11+ executable; shell arguments are not accepted. |

The default cache is `~/Library/Caches/awesome-python-dev` on macOS, `$XDG_CACHE_HOME/awesome-python-dev` (or `~/.cache/awesome-python-dev`) on Linux, and `%LOCALAPPDATA%\awesome-python-dev` on Windows. Runtime packages are isolated from the npm installation directory. You can remove this cache to reclaim space; the next online invocation downloads the selected runtime again.

## Integrity and publishing

The launcher accepts only protocol-1 manifests, exact stable versions and runtime asset URLs in this project's GitHub Releases. Downloads have size limits, restricted HTTPS redirects and SHA-256 verification. Cache writes are atomic, and Python runs in isolated mode with bundled dependencies. SHA-256 protects file integrity; the GitHub repository and its release maintainers remain the trust source.

The npm launcher version changes only when launcher behavior or protocol support changes. Runtime versions, catalog contents and framework integrations are released through GitHub. Publishing instructions live in the [repository](https://github.com/m9rco/awesome-python-dev).

MIT license. Individual upstream resources retain their own licenses.

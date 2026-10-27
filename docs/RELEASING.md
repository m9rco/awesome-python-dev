# Release Python runtimes and npm shells independently

Routine catalog, installer and agent-adapter work changes the Python runtime.
Publish those changes to GitHub Releases and PyPI. Publish npm only when the
launcher itself needs a new version.

| Release | Version source | Git tag | Workflow | Destinations |
| --- | --- | --- | --- | --- |
| Python runtime | `pyproject.toml`, `src/awesome_python_dev/__init__.py`, `uv.lock` | `vX.Y.Z` | [`runtime-release.yml`](../.github/workflows/runtime-release.yml) | GitHub assets, `runtime-v1` channel and PyPI |
| npm shell | `npm/package.json`, `npm/package-lock.json` | `npm-vX.Y.Z` | [`npm-publish.yml`](../.github/workflows/npm-publish.yml) | npm |

The initial runtime is `0.3.0`; the initial npm shell is `0.1.0`. Their versions
are intentionally independent. Tags must match their package metadata and point
to a commit reachable from `main`.

## One-time registry setup

Trusted publishing uses GitHub OIDC instead of a long-lived registry token.
Configure each registry with the exact workflow and environment names below.
Publishing still requires the package owner to establish that trust; committing
a workflow does not register a publisher by itself.

| Registry | Project/package | GitHub owner | Repository | Workflow filename | Environment |
| --- | --- | --- | --- | --- | --- |
| PyPI | `awesome-python-dev` | `m9rco` | `awesome-python-dev` | `runtime-release.yml` | `pypi` |
| npm | `awesome-python-dev` | `m9rco` | `awesome-python-dev` | `npm-publish.yml` | `npm` |

For a new PyPI project, create a pending trusted publisher in the owner's PyPI
account before the first runtime tag. The first successful OIDC upload creates
the project and activates the publisher. For an existing project, add the
publisher in project publishing settings. See [PyPI's pending publisher
instructions](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

For npm, first publish the initial package from an authenticated maintainer
session, completing any registry-required browser or 2FA step. Then configure
the GitHub trusted publisher in the package's npm settings with the values above
and permission to publish directly. Future shell tags publish from the
`npm` GitHub environment with OIDC. The workflow uses Node.js 24 and checks for
npm 11.5.1 or newer, which is required for trusted publishing. See [npm's trusted
publishing instructions](https://docs.npmjs.com/trusted-publishers/).

The initial npm command, after the tagged runtime and bootstrap asset are
publicly available, is:

```sh
cd npm
npm ci --ignore-scripts
npm test
npm pack --dry-run --ignore-scripts
npm publish --access public --ignore-scripts
```

Do not push an `npm-v0.1.0` tag to republish a version already published manually.
Use the tag workflow for the next new shell version. Registry versions are
immutable; an existing version must not be overwritten.

## Publish a runtime

1. Update the Python version, changelog and catalog as needed. Keep the Python
   package's two version declarations aligned and regenerate `uv.lock`.
2. Run the checks below. Commit the release changes to `main` and wait for CI.
3. Tag the reviewed commit with `vX.Y.Z` and push that tag.
4. Verify both the GitHub release and PyPI publication before announcing the
   version. Check the stable channel points to the intended runtime.

```sh
uv sync --locked
uv run ruff check .
uv run pytest -q
npm --prefix npm ci --ignore-scripts
npm --prefix npm test
uv run python scripts/build_runtime.py --output dist/runtime
uv build
```

For example, after the matching `0.3.0` version change is committed:

```sh
git tag v0.3.0
git push origin v0.3.0
```

The runtime workflow builds the Python wheel and source distribution, the
standalone `.pyz`, `runtime.json`, a packed npm launcher for convenient GitHub
distribution, and `SHA256SUMS`. It verifies the zipapp in isolated Python mode,
then uploads the release assets. Existing assets are compared byte for byte;
different content under an already published filename is rejected.

After the versioned GitHub assets are available, the workflow promotes
`runtime.json` to the `runtime-v1` channel. Promotion is serialized and will not
move the channel backward to an older version or replace an existing version's
manifest with different contents. The channel release is marked prerelease and
never replaces the normal latest release.

The PyPI job publishes only the wheel and source distribution built for that
tag. The runtime release workflow does **not** publish to npm. Packing a `.tgz`
for the GitHub release is not an npm registry upload.

Validate the two user-facing routes:

```sh
uvx awesome-python-dev@0.3.0 --version
apd runtime update 0.3.0
APD_RUNTIME_VERSION=0.3.0 apd --version
```

`apd runtime` is an npm-shell command; use an npm-installed shell for those last
two checks. Package publication and channel promotion can complete at different
times, so check each result separately if a workflow needs retrying.

## Publish a shell change

1. Change `npm/` only as needed for launcher behavior or supported runtime APIs.
2. Bump `npm/package.json` and the matching lockfile. Do not bump this version
   for ordinary catalog or Python changes.
3. Retain a valid published bootstrap runtime. If changing it, copy the exact
   reviewed release `runtime.json` to `npm/runtime-bootstrap.json`; do not edit
   the checksum by hand.
4. Run the shell tests and package inspection, commit to `main`, then push the
   matching `npm-vX.Y.Z` tag.
5. Verify the npm version and test a clean installation.

```sh
npm --prefix npm ci --ignore-scripts
npm --prefix npm test
npm --prefix npm run test:package
```

The npm workflow validates the tag, tests the shell, inspects its file list and
publishes using the configured trusted publisher. It does not create a new
runtime release. A shell can therefore remain at `0.1.0` while compatible
runtime versions continue to advance.

## Protocol and reproducibility

Runtime protocol 1 carries schema version, runtime API, exact runtime version,
Python requirement, asset URL, byte count and SHA-256. The default shell
bootstrap is a fallback, while the channel points to the newest compatible
stable release. The zipapp builder uses the dependency version in `uv.lock`,
fixed archive metadata and sorted entries for reproducible output.

Do not reuse a published runtime version for new bytes. Correct a faulty
release by publishing a new version. Users who need an older runtime can set
`APD_RUNTIME_VERSION` explicitly; pinning does not require republishing npm.

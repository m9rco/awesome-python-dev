"use strict";

const fs = require("node:fs/promises");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");

const RELEASES = "https://github.com/m9rco/awesome-python-dev/releases/download/";
const CHANNEL_URL = `${RELEASES}runtime-v1/runtime.json`;
const MANIFEST_LIMIT = 64 * 1024;
const RUNTIME_LIMIT = 10 * 1024 * 1024;
const CHECK_INTERVAL = 24 * 60 * 60 * 1000;
const VERSION = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

class RuntimeError extends Error {}
class NetworkError extends RuntimeError {}
class IntegrityError extends RuntimeError {}

function version(value) {
  if (typeof value !== "string" || !VERSION.test(value)) {
    throw new IntegrityError("Runtime version must have the form 0.3.0 (stable releases only).");
  }
  return value;
}

function validateManifest(value, expectedVersion) {
  if (!value || typeof value !== "object" || Array.isArray(value)
      || value.schema_version !== 1 || value.runtime_api !== 1
      || value.python_requires !== ">=3.11") {
    throw new IntegrityError("Unsupported runtime manifest. Update the npm shell if the runtime protocol changed.");
  }
  version(value.version);
  if (expectedVersion && value.version !== expectedVersion) {
    throw new IntegrityError(`Runtime manifest does not match requested version ${expectedVersion}.`);
  }
  const asset = value.asset;
  const expectedUrl = `${RELEASES}v${value.version}/awesome-python-dev-runtime-${value.version}.pyz`;
  if (!asset || asset.url !== expectedUrl || !/^[a-f0-9]{64}$/.test(asset.sha256)
      || !Number.isSafeInteger(asset.size) || asset.size < 1 || asset.size > RUNTIME_LIMIT) {
    throw new IntegrityError("Invalid runtime asset URL, checksum or size.");
  }
  return {
    schema_version: 1, runtime_api: 1, version: value.version, python_requires: ">=3.11",
    asset: {url: asset.url, sha256: asset.sha256, size: asset.size},
  };
}

function decodeManifest(bytes, expectedVersion) {
  if (bytes.length > MANIFEST_LIMIT) throw new IntegrityError("Runtime manifest is too large.");
  let data;
  try { data = JSON.parse(bytes.toString("utf8")); }
  catch { throw new IntegrityError("Runtime manifest is not valid JSON."); }
  return validateManifest(data, expectedVersion);
}

function cacheDirectory(env = process.env, platform = process.platform, home = os.homedir()) {
  if (env.APD_CACHE_DIR) return path.resolve(env.APD_CACHE_DIR);
  const root = platform === "win32" ? (env.LOCALAPPDATA || path.join(home, "AppData", "Local"))
    : platform === "darwin" ? path.join(home, "Library", "Caches")
    : (env.XDG_CACHE_HOME || path.join(home, ".cache"));
  return path.join(root, "awesome-python-dev");
}

function paths(cache, selectedVersion) {
  const directory = path.join(cache, "runtimes", version(selectedVersion));
  return {directory, manifest: path.join(directory, "runtime.json"), binary: path.join(directory, "runtime.pyz")};
}

function verifyBytes(bytes, manifest) {
  if (bytes.length !== manifest.asset.size
      || crypto.createHash("sha256").update(bytes).digest("hex") !== manifest.asset.sha256) {
    throw new IntegrityError(`Runtime ${manifest.version} failed SHA-256/size verification. Refusing to execute it.`);
  }
}

function redirectAllowed(url) {
  const parsed = new URL(url);
  return parsed.protocol === "https:" && !parsed.username && !parsed.password
    && (!parsed.port || parsed.port === "443")
    && ["github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com"].includes(parsed.hostname);
}

async function download(url, limit, fetchImpl = globalThis.fetch) {
  // Callers supply fixed release URLs. Redirects are restricted to GitHub release hosts.
  if (!url.startsWith(RELEASES) || !redirectAllowed(url)) {
    throw new IntegrityError("Download must originate from this project's GitHub releases.");
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);
  let current = url;
  try {
    for (let redirects = 0; redirects <= 5; redirects += 1) {
      if (!redirectAllowed(current)) throw new IntegrityError("Unexpected runtime download redirect.");
      let response;
      try {
        response = await fetchImpl(current, {
          redirect: "manual", signal: controller.signal,
          headers: {"User-Agent": "awesome-python-dev-npm-shell/1", Accept: "application/octet-stream"},
        });
      } catch (error) {
        throw new NetworkError(`Cannot reach GitHub: ${error.message}`);
      }
      if ([301, 302, 303, 307, 308].includes(response.status)) {
        await response.body?.cancel();
        const location = response.headers.get("location");
        if (!location) throw new IntegrityError("GitHub redirect has no destination.");
        try { current = new URL(location, current).href; }
        catch { throw new IntegrityError("Invalid GitHub redirect destination."); }
        continue;
      }
      if (!response.ok) {
        await response.body?.cancel();
        throw new NetworkError(`GitHub returned HTTP ${response.status} for ${url}.`);
      }
      const length = Number(response.headers.get("content-length"));
      if (length > limit) {
        await response.body?.cancel();
        throw new IntegrityError("Runtime download exceeds the allowed size.");
      }
      const chunks = [];
      let size = 0;
      try {
        for await (const chunk of response.body || []) {
          size += chunk.length;
          if (size > limit) {
            controller.abort();
            throw new IntegrityError("Runtime download exceeds the allowed size.");
          }
          chunks.push(chunk);
        }
      } catch (error) {
        if (error instanceof IntegrityError) throw error;
        throw new NetworkError(`Runtime download interrupted: ${error.message}`);
      }
      return Buffer.concat(chunks);
    }
    throw new IntegrityError("Too many runtime download redirects.");
  } finally { clearTimeout(timeout); }
}

async function readOptional(file) {
  try { return await fs.readFile(file); }
  catch (error) { if (error.code === "ENOENT") return null; throw error; }
}

async function atomicWrite(file, bytes) {
  await fs.mkdir(path.dirname(file), {recursive: true, mode: 0o700});
  const temporary = `${file}.${process.pid}.${crypto.randomBytes(8).toString("hex")}.tmp`;
  try {
    await fs.writeFile(temporary, bytes, {flag: "wx", mode: 0o600});
    await fs.rename(temporary, file);
  } finally { await fs.rm(temporary, {force: true}); }
}

async function readManifest(cache, selectedVersion) {
  const bytes = await readOptional(paths(cache, selectedVersion).manifest);
  return bytes ? decodeManifest(bytes, selectedVersion) : null;
}

async function readState(cache) {
  const bytes = await readOptional(path.join(cache, "stable.json"));
  if (!bytes) return null;
  let state;
  try { state = JSON.parse(bytes.toString("utf8")); }
  catch { throw new IntegrityError("Cached runtime channel metadata is invalid JSON."); }
  if (!state || !Number.isFinite(state.checked_at) || state.checked_at < 0
      || state.checked_at > 8640000000000000) {
    throw new IntegrityError("Cached runtime channel timestamp is invalid.");
  }
  return {checked_at: state.checked_at, manifest: validateManifest(state.manifest)};
}

async function cachedBinary(cache, manifest) {
  const file = paths(cache, manifest.version).binary;
  const bytes = await readOptional(file);
  if (!bytes) return null;
  verifyBytes(bytes, manifest);
  return file;
}

async function ensureRuntime(cache, manifest, offline, fetchBytes) {
  const savedManifest = await readManifest(cache, manifest.version);
  if (savedManifest && JSON.stringify(savedManifest) !== JSON.stringify(manifest)) {
    throw new IntegrityError(`Runtime ${manifest.version} changed after it was cached. Release versions must be immutable.`);
  }
  let file = await cachedBinary(cache, manifest);
  if (!file) {
    if (offline) throw new RuntimeError(`Runtime ${manifest.version} is not cached. Run once online before using APD_OFFLINE=1.`);
    const bytes = await fetchBytes(manifest.asset.url, RUNTIME_LIMIT);
    verifyBytes(bytes, manifest);
    file = paths(cache, manifest.version).binary;
    await atomicWrite(file, bytes);
  }
  await atomicWrite(paths(cache, manifest.version).manifest, JSON.stringify(manifest, null, 2) + "\n");
  return file;
}

function context(options = {}) {
  const env = options.env || process.env;
  return {
    env, cache: options.cache || cacheDirectory(env),
    offline: options.offline ?? env.APD_OFFLINE === "1",
    pinned: options.version || env.APD_RUNTIME_VERSION || null,
    force: Boolean(options.force), now: options.now ?? Date.now(),
    fetchBytes: options.fetchBytes || download,
    bootstrap: validateManifest(options.bootstrap || require("../runtime-bootstrap.json")),
    warn: options.warn || ((message) => process.stderr.write(`apd: ${message}\n`)),
  };
}

async function resolveRuntime(options = {}) {
  const ctx = context(options);
  if (ctx.force && ctx.offline) throw new RuntimeError("runtime update requires network access; unset APD_OFFLINE first.");
  if (ctx.pinned) version(ctx.pinned);
  const state = ctx.pinned ? null : await readState(ctx.cache);
  let manifest = ctx.pinned ? await readManifest(ctx.cache, ctx.pinned) : state?.manifest;
  if (!manifest && (!ctx.pinned || ctx.bootstrap.version === ctx.pinned)) manifest = ctx.bootstrap;
  const check = ctx.force || (ctx.pinned ? !await readManifest(ctx.cache, ctx.pinned)
    : !state || ctx.now - state.checked_at >= CHECK_INTERVAL || state.checked_at > ctx.now);
  let refreshed = false;
  if (check && !ctx.offline) {
    try {
      const url = ctx.pinned ? `${RELEASES}v${ctx.pinned}/runtime.json` : CHANNEL_URL;
      manifest = decodeManifest(await ctx.fetchBytes(url, MANIFEST_LIMIT), ctx.pinned);
      refreshed = true;
    } catch (error) {
      if (!(error instanceof NetworkError) || ctx.force || !manifest) throw error;
      ctx.warn(`Runtime update check unavailable; using ${manifest.version}. ${error.message}`);
    }
  }
  if (!manifest) throw new RuntimeError(`Runtime ${ctx.pinned} is not cached. Run once online to resolve this pinned version.`);
  let file;
  try { file = await ensureRuntime(ctx.cache, manifest, ctx.offline, ctx.fetchBytes); }
  catch (error) {
    if (!(error instanceof NetworkError) || ctx.force || ctx.pinned || !state
        || state.manifest.version === manifest.version) throw error;
    file = await cachedBinary(ctx.cache, state.manifest);
    if (!file) throw error;
    manifest = state.manifest;
    ctx.warn(`New runtime download unavailable; using verified cached ${manifest.version}. ${error.message}`);
  }
  if (!ctx.pinned && !ctx.offline && check) {
    await atomicWrite(path.join(ctx.cache, "stable.json"), JSON.stringify({checked_at: ctx.now, manifest}, null, 2) + "\n");
  }
  return {file, manifest, cache: ctx.cache, selection: ctx.pinned ? "pinned" : "stable", refreshed};
}

async function runtimeStatus(options = {}) {
  const ctx = context(options);
  if (ctx.pinned) version(ctx.pinned);
  const state = ctx.pinned ? null : await readState(ctx.cache);
  const manifest = (ctx.pinned ? await readManifest(ctx.cache, ctx.pinned) : state?.manifest)
    || ((!ctx.pinned || ctx.bootstrap.version === ctx.pinned) ? ctx.bootstrap : null);
  const file = manifest ? await cachedBinary(ctx.cache, manifest) : null;
  return {
    shell_version: require("../package.json").version,
    runtime_version: manifest?.version || ctx.pinned,
    runtime_api: 1, selection: ctx.pinned ? "pinned" : "stable",
    cache_dir: ctx.cache, cached: Boolean(file), offline: ctx.offline,
    last_checked: state ? new Date(state.checked_at).toISOString() : null,
  };
}

module.exports = {CHANNEL_URL, RELEASES, CHECK_INTERVAL, MANIFEST_LIMIT, RUNTIME_LIMIT,
  RuntimeError, NetworkError, IntegrityError, version, validateManifest, decodeManifest,
  cacheDirectory, paths, verifyBytes, download, atomicWrite, resolveRuntime, runtimeStatus};

"use strict";

const {test} = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs/promises");
const os = require("node:os");
const path = require("node:path");
const crypto = require("node:crypto");
const {EventEmitter} = require("node:events");
const runtime = require("../lib/runtime.cjs");
const {findPython, runRuntime} = require("../lib/launch.cjs");

function fixture(selectedVersion = "0.3.0") {
  const bytes = Buffer.from(`fake-runtime-${selectedVersion}`);
  const manifest = {
    schema_version: 1, runtime_api: 1, version: selectedVersion, python_requires: ">=3.11",
    asset: {url: `${runtime.RELEASES}v${selectedVersion}/awesome-python-dev-runtime-${selectedVersion}.pyz`,
      size: bytes.length, sha256: crypto.createHash("sha256").update(bytes).digest("hex")},
  };
  return {bytes, manifest};
}

async function environment(t) {
  const cache = await fs.mkdtemp(path.join(os.tmpdir(), "apd-shell-test-"));
  t.after(() => fs.rm(cache, {recursive: true, force: true}));
  const bundle = fixture();
  const requests = [];
  return {
    ...bundle, cache, requests,
    options: {cache, bootstrap: bundle.manifest, env: {}, now: 100000, warn: () => {},
      fetchBytes: async (url) => {
        requests.push(url);
        return url.endsWith("runtime.json") ? Buffer.from(JSON.stringify(bundle.manifest)) : bundle.bytes;
      }},
  };
}

test("download once, reuse verified cache, and upgrade runtime without changing shell version", async (t) => {
  const env = await environment(t);
  const shellVersion = require("../package.json").version;
  const initial = await runtime.resolveRuntime(env.options);
  assert.equal(initial.manifest.version, "0.3.0");
  assert.equal(env.requests.length, 2);
  await runtime.resolveRuntime({...env.options, now: 100001});
  assert.equal(env.requests.length, 2);
  const next = fixture("0.4.0");
  const upgraded = await runtime.resolveRuntime({...env.options, now: 100000 + runtime.CHECK_INTERVAL,
    fetchBytes: async (url) => url.endsWith("runtime.json") ? Buffer.from(JSON.stringify(next.manifest)) : next.bytes});
  assert.equal(upgraded.manifest.version, "0.4.0");
  assert.equal(require("../package.json").version, shellVersion);
  assert.equal((await runtime.runtimeStatus(env.options)).runtime_version, "0.4.0");
});

test("pinned version does not follow channel or change stable selection", async (t) => {
  const env = await environment(t);
  await runtime.resolveRuntime(env.options);
  const pinned = fixture("0.3.1");
  const seen = [];
  const result = await runtime.resolveRuntime({...env.options, version: "0.3.1", fetchBytes: async (url) => {
    seen.push(url);
    return url.endsWith("runtime.json") ? Buffer.from(JSON.stringify(pinned.manifest)) : pinned.bytes;
  }});
  assert.equal(result.selection, "pinned");
  assert.equal(seen[0], `${runtime.RELEASES}v0.3.1/runtime.json`);
  assert.equal((await runtime.runtimeStatus(env.options)).runtime_version, "0.3.0");
  const offline = await runtime.resolveRuntime({...env.options, env: {APD_RUNTIME_VERSION: "0.3.1", APD_OFFLINE: "1"},
    fetchBytes: async () => { throw new Error("unexpected network"); }});
  assert.equal(offline.manifest.version, "0.3.1");
});

test("offline selection requires the exact cached runtime and does not make network calls", async (t) => {
  const env = await environment(t);
  await assert.rejects(runtime.resolveRuntime({...env.options, offline: true}), /not cached/);
  await runtime.resolveRuntime(env.options);
  const offline = {...env.options, offline: true, fetchBytes: async () => { throw new Error("network"); }};
  assert.equal((await runtime.resolveRuntime(offline)).manifest.version, "0.3.0");
  await assert.rejects(runtime.resolveRuntime({...offline, version: "0.9.0"}), /not cached/);
});

test("corrupt cached bytes fail closed without downloading or executing a replacement", async (t) => {
  const env = await environment(t);
  const result = await runtime.resolveRuntime(env.options);
  await fs.writeFile(result.file, "tampered");
  const count = env.requests.length;
  await assert.rejects(runtime.resolveRuntime(env.options), /SHA-256/);
  assert.equal(env.requests.length, count);
});

test("bad downloaded checksums leave no usable cache binary", async (t) => {
  const env = await environment(t);
  await assert.rejects(runtime.resolveRuntime({...env.options,
    fetchBytes: async (url) => url.endsWith("runtime.json") ? Buffer.from(JSON.stringify(env.manifest)) : Buffer.from("tampered")}), /SHA-256/);
  await assert.rejects(fs.access(runtime.paths(env.cache, "0.3.0").binary), {code: "ENOENT"});
});

test("manifest validation rejects unsupported protocols, URLs, paths and mismatched pins", () => {
  const {manifest} = fixture();
  for (const patch of [
    {schema_version: 2}, {runtime_api: 2}, {python_requires: ">=3.15"},
    {version: "../escape"}, {version: "1.0.0-beta.1"},
    {asset: {...manifest.asset, url: "https://evil.example/runtime.pyz"}},
    {asset: {...manifest.asset, url: manifest.asset.url + "?download=1"}},
    {asset: {...manifest.asset, size: runtime.RUNTIME_LIMIT + 1}},
    {asset: {...manifest.asset, sha256: "oops"}},
  ]) assert.throws(() => runtime.validateManifest({...manifest, ...patch}), runtime.IntegrityError);
  assert.throws(() => runtime.validateManifest(manifest, "0.4.0"), /requested version/);
  assert.throws(() => runtime.decodeManifest(Buffer.from("not json")), /valid JSON/);
});

test("invalid channel manifests never fall back to an otherwise valid cached runtime", async (t) => {
  const env = await environment(t);
  await runtime.resolveRuntime(env.options);
  await assert.rejects(runtime.resolveRuntime({...env.options, now: env.options.now + runtime.CHECK_INTERVAL,
    fetchBytes: async () => Buffer.from(JSON.stringify({...env.manifest, runtime_api: 2}))}), runtime.IntegrityError);
});

test("network failure falls back to bootstrap and does not retry channel before 24 hours", async (t) => {
  const env = await environment(t);
  let checks = 0;
  const options = {...env.options, fetchBytes: async (url) => {
    if (url === runtime.CHANNEL_URL) { checks += 1; throw new runtime.NetworkError("offline"); }
    return env.bytes;
  }};
  await runtime.resolveRuntime(options);
  await runtime.resolveRuntime({...options, now: options.now + 1});
  assert.equal(checks, 1);
});

test("failed newer runtime download retains verified old runtime; forced updates surface failure", async (t) => {
  const env = await environment(t);
  await runtime.resolveRuntime(env.options);
  const next = fixture("0.5.0");
  const options = {...env.options, now: env.options.now + runtime.CHECK_INTERVAL,
    fetchBytes: async (url) => {
      if (url.endsWith("runtime.json")) return Buffer.from(JSON.stringify(next.manifest));
      throw new runtime.NetworkError("download unavailable");
    }};
  assert.equal((await runtime.resolveRuntime(options)).manifest.version, "0.3.0");
  await assert.rejects(runtime.resolveRuntime({...options, force: true}), /download unavailable/);
});

test("an explicit pin never falls back to another installed version", async (t) => {
  const env = await environment(t);
  await runtime.resolveRuntime(env.options);
  await assert.rejects(runtime.resolveRuntime({...env.options, version: "0.9.0",
    fetchBytes: async () => { throw new runtime.NetworkError("missing version"); }}), /missing version/);
});

test("published versions are immutable even if a new manifest carries a valid checksum", async (t) => {
  const env = await environment(t);
  await runtime.resolveRuntime(env.options);
  const replacement = Buffer.from("replacement runtime");
  const changed = {...env.manifest, asset: {...env.manifest.asset, size: replacement.length,
    sha256: crypto.createHash("sha256").update(replacement).digest("hex")}};
  await assert.rejects(runtime.resolveRuntime({...env.options, force: true,
    fetchBytes: async (url) => url.endsWith("runtime.json") ? Buffer.from(JSON.stringify(changed)) : replacement}), /immutable/);
});

test("runtime status reads only local metadata, and cache defaults stay outside npm installation", async (t) => {
  const env = await environment(t);
  assert.equal((await runtime.runtimeStatus(env.options)).cached, false);
  assert.equal(env.requests.length, 0);
  assert.ok(runtime.cacheDirectory({}, "linux", "/example").endsWith(path.join(".cache", "awesome-python-dev")));
  assert.ok(runtime.cacheDirectory({}, "darwin", "/example").endsWith(path.join("Library", "Caches", "awesome-python-dev")));
  assert.equal(runtime.cacheDirectory({APD_CACHE_DIR: env.cache}), env.cache);
});

test("download restricts redirects and enforces streamed size limits", async () => {
  await assert.rejects(runtime.download(runtime.CHANNEL_URL, 100, async () => new Response(null,
    {status: 302, headers: {location: "https://evil.example/payload"}})), /redirect/);
  await assert.rejects(runtime.download(runtime.CHANNEL_URL, 3, async () => new Response("long body")), /size/);
  const bytes = await runtime.download(runtime.CHANNEL_URL, 100, async () => new Response("ok"));
  assert.equal(bytes.toString(), "ok");
  await assert.rejects(runtime.download(runtime.CHANNEL_URL, 100, async () => new Response(null, {status: 404})), runtime.NetworkError);
});

test("concurrent launches produce complete verified cache files", async (t) => {
  const env = await environment(t);
  const results = await Promise.all(Array.from({length: 6}, () => runtime.resolveRuntime(env.options)));
  assert.equal(new Set(results.map((result) => result.file)).size, 1);
  assert.deepEqual(await fs.readFile(results[0].file), env.bytes);
  assert.equal((await fs.readdir(path.dirname(results[0].file))).filter((name) => name.endsWith(".tmp")).length, 0);
});

test("Python discovery honors executable override and uses uv only when needed", () => {
  const seen = [];
  const direct = findPython({APD_PYTHON: "/custom/python"}, "linux", (command, args, options) => {
    seen.push({command, args, options});
    return {status: 0, stdout: "3.13\n"};
  });
  assert.equal(direct.command, "/custom/python");
  assert.deepEqual(direct.prefix, ["-I", "-S", "-X", "utf8"]);
  assert.equal(seen[0].options.shell, false);
  assert.throws(() => findPython({APD_PYTHON: "bad"}, "linux", () => ({status: 1})), /APD_PYTHON/);
  const uv = findPython({APD_OFFLINE: "1"}, "linux", (command) => command === "uv" ? {status: 0} : {status: 1});
  assert.equal(uv.command, "uv");
  assert.ok(uv.prefix.includes("--no-project"));
  assert.ok(uv.prefix.includes("--no-python-downloads"));
  assert.ok(uv.prefix.includes("--offline"));
});

test("runtime execution forwards literal argv, working directory, stdio, exit and signals", async () => {
  const child = new EventEmitter();
  const signals = new EventEmitter();
  let invocation;
  child.kill = (signal) => { child.killed = true; child.signal = signal; };
  const args = ["init", "--path", "space and $(touch injected)", "--tools", "a;b"];
  const promise = runRuntime("/cache/runtime.pyz", args, {
    python: {command: "python3", prefix: ["-I"]}, cwd: "/work", env: {EXAMPLE: "yes"}, signals,
    spawn: (command, actual, options) => { invocation = {command, actual, options}; return child; },
  });
  signals.emit("SIGTERM");
  assert.equal(child.signal, "SIGTERM");
  child.emit("exit", 7, null);
  assert.deepEqual(await promise, {code: 7, signal: null});
  assert.deepEqual(invocation.actual, ["-I", "/cache/runtime.pyz", ...args]);
  assert.equal(invocation.options.shell, false);
  assert.equal(invocation.options.stdio, "inherit");
  assert.equal(invocation.options.cwd, "/work");
  assert.equal(signals.listenerCount("SIGTERM"), 0);
});

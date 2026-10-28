"use strict";

const {test} = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs/promises");
const path = require("node:path");
const os = require("node:os");
const http = require("node:http");
const https = require("node:https");
const net = require("node:net");
const crypto = require("node:crypto");
const {spawn} = require("node:child_process");
const {proxyRestartEnvironment} = require("../lib/proxy.cjs");

test("proxy startup honors environment settings, explicit opt-out, and restarts at most once", () => {
  const flags = new Set(["--use-env-proxy"]);
  const env = {https_proxy: "http://proxy.example:3128", no_proxy: "localhost", KEEP: "value"};
  const childEnv = proxyRestartEnvironment(env, [], flags);
  assert.deepEqual(childEnv, {...env, NODE_USE_ENV_PROXY: "1"});
  assert.equal(env.NODE_USE_ENV_PROXY, undefined);
  assert.equal(proxyRestartEnvironment(childEnv, [], flags), null);
  assert.equal(proxyRestartEnvironment({...env, NODE_USE_ENV_PROXY: "0"}, [], flags), null);
  assert.equal(proxyRestartEnvironment(env, ["--no-use-env-proxy"], flags), null);
  assert.equal(proxyRestartEnvironment({...env, NODE_OPTIONS: "--no-use-env-proxy"}, [], flags), null);
  assert.equal(proxyRestartEnvironment({...env, APD_OFFLINE: "1"}, [], flags), null);
  assert.equal(proxyRestartEnvironment({}, [], flags), null);
  assert.throws(() => proxyRestartEnvironment(env, [], new Set()), /22.21/);
});

test("real CLI downloads through a local CONNECT proxy with TLS verification enabled", {timeout: 30000}, async (t) => {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), "apd-proxy-test-"));
  const fixtures = path.join(__dirname, "fixtures");
  const certPath = path.join(fixtures, "proxy-test-cert.fixture");
  const bytes = Buffer.from("test payload is cached but never executed");
  const manifest = {
    schema_version: 1, runtime_api: 1, version: "0.3.0", python_requires: ">=3.11",
    asset: {
      url: "https://github.com/m9rco/awesome-python-dev/releases/download/v0.3.0/awesome-python-dev-runtime-0.3.0.pyz",
      sha256: crypto.createHash("sha256").update(bytes).digest("hex"), size: bytes.length,
    },
  };
  const requestedPaths = [];
  const sockets = new Set();
  function track(socket) { sockets.add(socket); socket.once("close", () => sockets.delete(socket)); }
  const origin = https.createServer({
    key: await fs.readFile(path.join(fixtures, "proxy-test-key.fixture")),
    cert: await fs.readFile(certPath),
  }, (req, res) => {
    requestedPaths.push(req.url);
    if (req.url.endsWith("/runtime.json")) {
      res.writeHead(200, {"content-type": "application/json"});
      res.end(JSON.stringify(manifest));
    } else if (req.url.endsWith("/awesome-python-dev-runtime-0.3.0.pyz")) {
      res.writeHead(200, {"content-type": "application/octet-stream"});
      res.end(bytes);
    } else { res.writeHead(404); res.end(); }
  });
  const proxy = http.createServer((_req, res) => { res.writeHead(405); res.end(); });
  origin.on("connection", track);
  proxy.on("connection", track);
  t.after(async () => {
    for (const socket of sockets) socket.destroy();
    await Promise.all([origin, proxy].map((server) => new Promise((resolve) => server.close(resolve))));
    await fs.rm(directory, {recursive: true, force: true});
  });
  await new Promise((resolve) => origin.listen(0, "127.0.0.1", resolve));
  const destinations = [];
  proxy.on("connect", (request, client, head) => {
    destinations.push(request.url);
    if (request.url !== "github.com:443") { client.destroy(); return; }
    const upstream = net.connect(origin.address().port, "127.0.0.1", () => {
      client.write("HTTP/1.1 200 Connection Established\r\n\r\n");
      if (head.length) upstream.write(head);
      client.pipe(upstream).pipe(client);
    });
    track(upstream);
    upstream.on("error", () => client.destroy());
    client.on("error", () => upstream.destroy());
    client.on("close", () => upstream.destroy());
  });
  await new Promise((resolve) => proxy.listen(0, "127.0.0.1", resolve));
  const proxyUrl = `http://127.0.0.1:${proxy.address().port}`;
  const env = {...process.env, APD_CACHE_DIR: path.join(directory, "runtime cache"),
    HTTP_PROXY: proxyUrl, HTTPS_PROXY: proxyUrl, http_proxy: proxyUrl, https_proxy: proxyUrl,
    NO_PROXY: "", no_proxy: "", NODE_EXTRA_CA_CERTS: certPath};
  for (const key of ["APD_OFFLINE", "APD_RUNTIME_VERSION", "NODE_USE_ENV_PROXY", "NODE_OPTIONS", "NODE_TLS_REJECT_UNAUTHORIZED"])
    delete env[key];
  const child = spawn(process.execPath, [path.resolve(__dirname, "../bin/apd.cjs"), "runtime", "update"],
    {cwd: directory, env, stdio: ["ignore", "pipe", "pipe"], shell: false});
  t.after(() => { if (child.exitCode === null) child.kill(); });
  let stdout = "";
  let stderr = "";
  child.stdout.on("data", (data) => { stdout += data; });
  child.stderr.on("data", (data) => { stderr += data; });
  const code = await new Promise((resolve, reject) => {
    child.once("error", reject);
    child.once("exit", resolve);
  });
  assert.equal(code, 0, stderr);
  assert.match(stdout, /Runtime 0\.3\.0 is verified and cached/);
  assert.ok(destinations.length >= 1);
  assert.deepEqual(new Set(destinations), new Set(["github.com:443"]));
  assert.deepEqual(requestedPaths, [
    "/m9rco/awesome-python-dev/releases/download/runtime-v1/runtime.json",
    "/m9rco/awesome-python-dev/releases/download/v0.3.0/awesome-python-dev-runtime-0.3.0.pyz",
  ]);
  assert.deepEqual(await fs.readFile(path.join(env.APD_CACHE_DIR, "runtimes/0.3.0/runtime.pyz")), bytes);
});

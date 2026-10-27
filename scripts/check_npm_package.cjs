#!/usr/bin/env node
"use strict";

// Exercise the actual npm tarball from an unrelated directory, without network.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const {spawnSync} = require("node:child_process");

const root = path.resolve(__dirname, "..");
const npmCli = process.env.npm_execpath;
if (!npmCli) throw new Error("Run with npm --prefix npm run test:package");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "dist/runtime/runtime.json"), "utf8"));
const directory = fs.mkdtempSync(path.join(os.tmpdir(), "apd packed runtime "));
const cache = path.join(directory, "cache");
const runtimeDir = path.join(cache, "runtimes", manifest.version);
const prefix = path.join(directory, "install");
const cwd = path.join(directory, "project with spaces");
const env = {...process.env, APD_CACHE_DIR: cache, APD_RUNTIME_VERSION: manifest.version, APD_OFFLINE: "1"};

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {cwd, env, encoding: "utf8", timeout: 60000, ...options});
  assert.ifError(result.error);
  assert.equal(result.status, 0, `${command} ${args.join(" ")}\n${result.stderr}`);
  return result.stdout.trim();
}

try {
  fs.mkdirSync(cwd, {recursive: true});
  fs.mkdirSync(runtimeDir, {recursive: true});
  fs.copyFileSync(path.join(root, "dist/runtime", path.basename(manifest.asset.url)), path.join(runtimeDir, "runtime.pyz"));
  fs.writeFileSync(path.join(runtimeDir, "runtime.json"), JSON.stringify(manifest));
  const packed = JSON.parse(run(process.execPath, [npmCli, "pack", "--json", "--ignore-scripts", "--pack-destination", directory], {cwd: path.join(root, "npm")}))[0];
  assert(!packed.files.some(file => /^(test|node_modules)\//.test(file.path)));
  assert(packed.files.some(file => file.path === "runtime-bootstrap.json"));
  run(process.execPath, [npmCli, "install", "--prefix", prefix, "--offline", "--ignore-scripts", "--no-audit", "--no-fund", path.join(directory, packed.filename)]);
  const bin = path.join(prefix, "node_modules", "awesome-python-dev", "bin", "apd.cjs");
  const shellVersion = JSON.parse(fs.readFileSync(path.join(root, "npm/package.json"), "utf8")).version;
  assert.equal(run(process.execPath, [bin, "--shell-version"]), shellVersion);
  assert.equal(run(process.execPath, [bin, "--version"]), `awesome-python-dev ${manifest.version}`);
  const status = JSON.parse(run(process.execPath, [bin, "runtime", "status"]));
  assert.equal(status.runtime_version, manifest.version);
  assert.equal(status.cached, true);
  const preview = run(process.execPath, [bin, "init", "--agents", "codex,claude", "--tools", "serena", "--dry-run", "--path", cwd]);
  assert.match(preview, /Preview only/);
  assert.match(preview, /serena/);
  assert.deepEqual(fs.readdirSync(cwd), []);
  // Argument errors must retain the Python CLI's non-zero exit status.
  const failure = spawnSync(process.execPath, [bin, "does-not-exist"], {cwd, env, encoding: "utf8"});
  assert.equal(failure.status, 2);
  console.log(`Packed npm shell ${shellVersion} launched runtime ${manifest.version}: offline cache, version, dry-run and exit status passed.`);
} finally {
  fs.rmSync(directory, {recursive: true, force: true});
}

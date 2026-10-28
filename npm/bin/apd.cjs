#!/usr/bin/env node
"use strict";

const {resolveRuntime, runtimeStatus, RuntimeError} = require("../lib/runtime.cjs");
const {runRuntime, runCommand} = require("../lib/launch.cjs");
const {proxyRestartEnvironment} = require("../lib/proxy.cjs");

function exitWith(result) {
  if (result.signal && process.platform !== "win32") process.kill(process.pid, result.signal);
  else process.exitCode = result.code;
}

async function main(args = process.argv.slice(2)) {
  if (args.length === 1 && args[0] === "--shell-version") {
    console.log(require("../package.json").version);
    return;
  }
  if (!(args[0] === "runtime" && args[1] === "status" && args.length === 2)) {
    const proxyEnv = proxyRestartEnvironment();
    if (proxyEnv) {
      exitWith(await runCommand(process.execPath, [...process.execArgv, __filename, ...args], {env: proxyEnv}));
      return;
    }
  }
  if (args[0] === "runtime") {
    if (args[1] === "status" && args.length === 2) {
      console.log(JSON.stringify(await runtimeStatus(), null, 2));
      return;
    }
    if (args[1] === "update" && args.length <= 3) {
      if (process.env.APD_OFFLINE === "1") throw new RuntimeError("runtime update requires network access; unset APD_OFFLINE first.");
      const runtime = await resolveRuntime({version: args[2], force: true});
      console.log(`Runtime ${runtime.manifest.version} is verified and cached (${runtime.selection}).`);
      if (args[2]) console.log(`Use APD_RUNTIME_VERSION=${args[2]} to select this version on subsequent commands.`);
      return;
    }
    throw new RuntimeError("Usage: apd runtime status | apd runtime update [VERSION]");
  }
  const runtime = await resolveRuntime();
  const result = await runRuntime(runtime.file, args);
  exitWith(result);
}

if (require.main === module) {
  main().catch((error) => {
    process.stderr.write(`apd: ${error.message}\n`);
    process.exitCode = 1;
  });
}

module.exports = {main};

"use strict";

const {RuntimeError} = require("./runtime.cjs");

function proxyRestartEnvironment(env = process.env, execArgv = process.execArgv,
  flags = process.allowedNodeEnvironmentFlags) {
  // Node reads this setting only at startup. A child with the explicit setting
  // never re-enters this branch, so proxy discovery adds at most one process.
  if (env.NODE_USE_ENV_PROXY !== undefined || env.APD_OFFLINE === "1"
      || execArgv.some((arg) => /^--(?:no-)?use-env-proxy(?:=|$)/.test(arg))
      || /(?:^|\s)--(?:no-)?use-env-proxy(?:[=\s]|$)/.test(env.NODE_OPTIONS || "")) return null;
  if (!["HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"].some((key) => env[key])) return null;
  if (!flags.has("--use-env-proxy")) {
    throw new RuntimeError("Proxy support requires Node.js 22.21+ (22.x) or Node.js 24.5+. Upgrade Node to honor HTTP(S)_PROXY and NO_PROXY.");
  }
  return {...env, NODE_USE_ENV_PROXY: "1"};
}

module.exports = {proxyRestartEnvironment};

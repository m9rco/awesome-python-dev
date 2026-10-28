"use strict";

const {spawnSync, spawn} = require("node:child_process");
const {RuntimeError} = require("./runtime.cjs");

const PROBE = "import sys; print('%d.%d' % sys.version_info[:2]); raise SystemExit(0 if sys.version_info >= (3,11) else 1)";

function findPython(env = process.env, platform = process.platform, probe = spawnSync) {
  const candidates = env.APD_PYTHON ? [[env.APD_PYTHON, []]]
    : platform === "win32" ? [["py", ["-3"]], ["python", []], ["python3", []]]
      : [["python3", []], ["python", []]];
  for (const [command, prefix] of candidates) {
    const result = probe(command, [...prefix, "-I", "-S", "-c", PROBE], {
      encoding: "utf8", timeout: 5000, windowsHide: true, env, shell: false,
    });
    if (!result.error && result.status === 0 && /^3\.(1[1-9]|[2-9]\d)\s*$/.test(result.stdout || "")) {
      return {command, prefix: [...prefix, "-I", "-S", "-X", "utf8"]};
    }
  }
  if (env.APD_PYTHON) throw new RuntimeError("APD_PYTHON must point to a working Python 3.11+ interpreter (an executable path, not shell arguments).");
  const uv = probe("uv", ["--version"], {encoding: "utf8", timeout: 5000, windowsHide: true, env, shell: false});
  if (!uv.error && uv.status === 0) {
    const prefix = ["run", "--no-project", "--no-config", "--no-env-file", "--isolated", "--python", "3.13"];
    if (env.APD_OFFLINE === "1") prefix.push("--offline", "--no-python-downloads");
    prefix.push("--", "python", "-I", "-S", "-X", "utf8");
    return {command: "uv", prefix};
  }
  throw new RuntimeError("Python 3.11+ or uv is required by the runtime. Install Python (https://www.python.org/downloads/) or uv (https://docs.astral.sh/uv/), then run apd again. The npm shell does not run an installer automatically.");
}

function runRuntime(file, args, options = {}) {
  const env = options.env || process.env;
  const python = options.python || findPython(env);
  return runCommand(python.command, [...python.prefix, file, ...args], {...options, env});
}

function runCommand(command, args, options = {}) {
  const env = options.env || process.env;
  const spawnImpl = options.spawn || spawn;
  const signals = options.signals || process;
  return new Promise((resolve, reject) => {
    const child = spawnImpl(command, args, {
      cwd: options.cwd || process.cwd(), env, stdio: "inherit", shell: false,
    });
    const forward = (signal) => { if (!child.killed) child.kill(signal); };
    const listeners = new Map(["SIGINT", "SIGTERM", "SIGHUP"].map((signal) => {
      const handler = () => forward(signal);
      signals.on(signal, handler);
      return [signal, handler];
    }));
    const cleanup = () => { for (const [signal, handler] of listeners) signals.removeListener(signal, handler); };
    child.once("error", (error) => { cleanup(); reject(new RuntimeError(`Cannot start ${command}: ${error.message}`)); });
    child.once("exit", (code, signal) => { cleanup(); resolve({code: code ?? 1, signal}); });
  });
}

module.exports = {findPython, runRuntime, runCommand};

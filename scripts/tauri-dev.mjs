import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2).filter((arg) => arg !== "--");
const env = { ...process.env };

function fail(message) {
  console.error(message);
  process.exit(1);
}

function ensurePathExists(targetPath, label) {
  if (!fs.existsSync(targetPath)) {
    fail(`${label} 不存在: ${targetPath}\n请先执行 pnpm pytauri:install:mac`);
  }
}

function appendRustFlag(existingFlags, nextFlag) {
  if (existingFlags.includes(nextFlag)) {
    return existingFlags;
  }
  return existingFlags ? `${existingFlags} ${nextFlag}` : nextFlag;
}

function isFile(targetPath) {
  try {
    return fs.statSync(targetPath).isFile();
  } catch {
    return false;
  }
}

function getPathEntries() {
  return (env.Path || env.PATH || "").split(path.delimiter).filter(Boolean);
}

function isNodeEntrypoint(targetPath) {
  const extension = path.extname(targetPath).toLowerCase();

  return [".cjs", ".js", ".mjs"].includes(extension) && isFile(targetPath);
}

function resolveEntrypointFromPnpmCmd(cmdPath) {
  if (!isFile(cmdPath)) {
    return null;
  }

  const shimDir = path.dirname(cmdPath);
  const content = fs.readFileSync(cmdPath, "utf8");
  const matches = content.matchAll(/"([^"]*pnpm\.cjs)"/gi);

  for (const match of matches) {
    const rawPath = match[1];
    const expandedPath = rawPath.replace(/^%~dp0[\\/]?/i, `${shimDir}${path.sep}`);
    const entrypoint = path.normalize(expandedPath);

    if (isFile(entrypoint)) {
      return entrypoint;
    }
  }

  return null;
}

function findPnpmCmd() {
  const candidates = [
    env.npm_execpath,
    env.PNPM_HOME ? path.join(env.PNPM_HOME, "pnpm.CMD") : null,
    ...getPathEntries().map((entry) => path.join(entry, "pnpm.CMD")),
  ].filter(Boolean);

  for (const candidate of candidates) {
    if (path.extname(candidate).toLowerCase() === ".cmd" && isFile(candidate)) {
      return candidate;
    }
  }

  return null;
}

function resolveWindowsPnpmEntrypoint() {
  if (env.npm_execpath && isNodeEntrypoint(env.npm_execpath)) {
    return env.npm_execpath;
  }

  const cmdPath = findPnpmCmd();
  const entrypoint = cmdPath ? resolveEntrypointFromPnpmCmd(cmdPath) : null;

  if (!entrypoint) {
    fail("无法定位 pnpm JS 入口，请确认 pnpm.CMD 在 PATH 中，或通过 pnpm tauri:dev 启动。");
  }

  return entrypoint;
}

if (process.platform === "darwin") {
  const pyembedPython = path.resolve("src-tauri", "pyembed", "python", "bin", "python3");
  const pyembedLib = path.resolve("src-tauri", "pyembed", "python", "lib");

  ensurePathExists(pyembedPython, "pyembed Python");
  ensurePathExists(pyembedLib, "pyembed Python lib 目录");

  env.PYO3_PYTHON = env.PYO3_PYTHON || pyembedPython;

  let rustFlags = env.RUSTFLAGS?.trim() || "";
  rustFlags = appendRustFlag(rustFlags, `-C link-arg=-Wl,-rpath,${pyembedLib}`);
  rustFlags = appendRustFlag(rustFlags, `-L ${pyembedLib}`);
  env.RUSTFLAGS = rustFlags;
}

const command = env.npm_execpath || "pnpm";
const commandArgs = ["exec", "tauri", "dev", ...args];
const spawnCommand = process.platform === "win32" ? process.execPath : command;
const spawnArgs =
  process.platform === "win32" ? [resolveWindowsPnpmEntrypoint(), ...commandArgs] : commandArgs;

const child = spawn(spawnCommand, spawnArgs, {
  stdio: "inherit",
  env,
  shell: false,
});

child.on("error", (error) => {
  fail(`启动 tauri dev 失败: ${error.message}`);
});

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});

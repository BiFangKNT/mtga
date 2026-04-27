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

const child = spawn(command, commandArgs, {
  stdio: "inherit",
  env,
  shell: process.platform === "win32",
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

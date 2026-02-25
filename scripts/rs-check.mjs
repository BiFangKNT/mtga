import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2).filter((arg) => arg !== "--");
const mode = args[0] ?? "dev";

if (mode !== "dev" && mode !== "gate") {
  console.error(`Unsupported rs-check mode: ${mode}`);
  console.error("Usage: node ./scripts/rs-check.mjs [dev|gate]");
  process.exit(1);
}

const env = { ...process.env };
const fmtArgs = mode === "gate" ? ["fmt", "--check"] : ["fmt"];

if (mode === "gate") {
  delete env.PYO3_PYTHON;

  const pyembedResourceDir = path.resolve("src-tauri", "pyembed", "python");
  if (!fs.existsSync(pyembedResourceDir)) {
    fs.mkdirSync(pyembedResourceDir, { recursive: true });
  }
} else {
  const pyembedPython =
    process.platform === "win32"
      ? path.resolve("src-tauri", "pyembed", "python", "python.exe")
      : path.resolve("src-tauri", "pyembed", "python", "bin", "python3");

  if (!fs.existsSync(pyembedPython)) {
    console.error(`pyembed Python 不存在: ${pyembedPython}`);
    process.exit(1);
  }

  env.PYO3_PYTHON = pyembedPython;
}

execFileSync("cargo", fmtArgs, {
  cwd: "src-tauri",
  stdio: "inherit",
  env,
});

execFileSync("cargo", ["check", "-p", "mtga-tauri"], {
  cwd: "src-tauri",
  stdio: "inherit",
  env,
});

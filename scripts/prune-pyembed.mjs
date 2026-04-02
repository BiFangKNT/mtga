import fs from "node:fs";
import path from "node:path";

const args = new Set(process.argv.slice(2));
const dryRun = args.has("--dry-run");

const pyembedRoot = path.resolve("src-tauri", "pyembed", "python");

const formatSize = (bytes) => {
  if (bytes < 1024) {
    return `${bytes} B`;
  }
  const units = ["KB", "MB", "GB"];
  let value = bytes / 1024;
  let unitIndex = 0;
  while (value >= 1024 && unitIndex < units.length - 1) {
    value /= 1024;
    unitIndex += 1;
  }
  return `${value.toFixed(value >= 100 ? 0 : value >= 10 ? 1 : 2)} ${units[unitIndex]}`;
};

const lstatSafe = (target) => {
  try {
    return fs.lstatSync(target);
  } catch {
    return null;
  }
};

const exists = (target) => lstatSafe(target) !== null;

const ensureWithinRoot = (target) => {
  const resolved = path.resolve(target);
  const relative = path.relative(pyembedRoot, resolved);
  if (relative === "") {
    return resolved;
  }
  if (relative.startsWith("..") || path.isAbsolute(relative)) {
    throw new Error(`Refuse to operate outside pyembed root: ${resolved}`);
  }
  return resolved;
};

const resolveWithinRoot = (...segments) => ensureWithinRoot(path.join(pyembedRoot, ...segments));

const walk = (target, visit) => {
  const stat = lstatSafe(target);
  if (!stat) {
    return;
  }
  visit(target, stat);
  if (!stat.isDirectory() || stat.isSymbolicLink()) {
    return;
  }
  for (const entry of fs.readdirSync(target, { withFileTypes: true })) {
    walk(path.join(target, entry.name), visit);
  }
};

const measureSize = (target) => {
  let total = 0;
  walk(target, (_entry, stat) => {
    if (stat.isFile()) {
      total += stat.size;
    }
  });
  return total;
};

const scheduled = new Map();

const hasScheduledAncestor = (target) => {
  for (const existing of scheduled.keys()) {
    if (target === existing || target.startsWith(`${existing}${path.sep}`)) {
      return true;
    }
  }
  return false;
};

const scheduleRemoval = (target, reason) => {
  const resolved = ensureWithinRoot(target);
  if (!exists(resolved) || hasScheduledAncestor(resolved)) {
    return;
  }
  for (const existing of [...scheduled.keys()]) {
    if (existing.startsWith(`${resolved}${path.sep}`)) {
      scheduled.delete(existing);
    }
  }
  scheduled.set(resolved, reason);
};

const scheduleRelativeRemoval = (relativePath, reason) => {
  scheduleRemoval(resolveWithinRoot(relativePath), reason);
};

const windowsPython = resolveWithinRoot("python.exe");
const unixBinDir = resolveWithinRoot("bin");
const hasWindowsLayout = exists(windowsPython);
const hasUnixLayout = exists(unixBinDir);

if (!hasWindowsLayout && !hasUnixLayout) {
  throw new Error(`Invalid pyembed layout: ${pyembedRoot}`);
}

const resolveUnixStdlibDir = () => {
  const libRoot = resolveWithinRoot("lib");
  if (!exists(libRoot)) {
    throw new Error(`Missing lib directory in pyembed: ${libRoot}`);
  }
  const candidates = fs
    .readdirSync(libRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && /^python\d+(?:\.\d+)?$/.test(entry.name))
    .map((entry) => entry.name)
    .sort();
  if (candidates.length === 0) {
    throw new Error(`Cannot locate stdlib directory under: ${libRoot}`);
  }
  return resolveWithinRoot("lib", candidates[0]);
};

const stdlibDir = hasWindowsLayout ? resolveWithinRoot("Lib") : resolveUnixStdlibDir();
const sitePackagesDir = path.join(stdlibDir, "site-packages");

if (!exists(sitePackagesDir)) {
  throw new Error(`Missing site-packages directory: ${sitePackagesDir}`);
}

const stdlibRelative = path.relative(pyembedRoot, stdlibDir);
const sitePackagesRelative = path.relative(pyembedRoot, sitePackagesDir);

scheduleRelativeRemoval(path.join(sitePackagesRelative, "pip"), "pip package");
scheduleRelativeRemoval(
  path.join(sitePackagesRelative, "modules", "resources", "openssl"),
  "legacy OpenSSL runtime files",
);
scheduleRelativeRemoval(path.join(stdlibRelative, "ensurepip"), "ensurepip");
scheduleRelativeRemoval(path.join(stdlibRelative, "idlelib"), "idlelib");
scheduleRelativeRemoval(path.join(stdlibRelative, "tkinter"), "tkinter");
scheduleRelativeRemoval(path.join(stdlibRelative, "turtledemo"), "turtledemo");
scheduleRelativeRemoval(path.join(stdlibRelative, "test"), "stdlib test suite");

if (hasWindowsLayout) {
  scheduleRelativeRemoval("Scripts", "CLI entry points");
  scheduleRelativeRemoval("tcl", "Tk runtime");
  scheduleRelativeRemoval(path.join("DLLs", "_tkinter.pyd"), "Tk native module");
}

const sitePackagesEntries = fs.readdirSync(sitePackagesDir, { withFileTypes: true });
for (const entry of sitePackagesEntries) {
  if (/^pip-[^/\\]+\.dist-info$/i.test(entry.name)) {
    scheduleRemoval(path.join(sitePackagesDir, entry.name), "pip dist-info");
  }
}

if (hasUnixLayout) {
  const unixBinKeepPattern = /^python(?:\d+(?:\.\d+)*)?$/;
  for (const entry of fs.readdirSync(unixBinDir, { withFileTypes: true })) {
    if (unixBinKeepPattern.test(entry.name)) {
      continue;
    }
    scheduleRemoval(path.join(unixBinDir, entry.name), "non-runtime CLI entry point");
  }
}

walk(pyembedRoot, (entry, stat) => {
  const name = path.basename(entry);
  if (stat.isDirectory() && name === "__pycache__") {
    scheduleRemoval(entry, "Python bytecode cache");
    return;
  }
  if (stat.isFile() && (name.endsWith(".pyc") || name.endsWith(".pyo"))) {
    scheduleRemoval(entry, "Python bytecode file");
  }
});

const planned = [...scheduled.entries()]
  .map(([target, reason]) => ({
    target,
    reason,
    size: measureSize(target),
    relative: path.relative(pyembedRoot, target) || ".",
  }))
  .sort((left, right) => left.relative.localeCompare(right.relative));

if (planned.length === 0) {
  console.log(`No prune targets found under ${pyembedRoot}`);
  process.exit(0);
}

let removedBytes = 0;
for (const item of planned) {
  const prefix = dryRun ? "[dry-run] " : "";
  console.log(`${prefix}remove ${item.relative} (${formatSize(item.size)}) - ${item.reason}`);
  removedBytes += item.size;
  if (!dryRun) {
    fs.rmSync(item.target, { recursive: true, force: true });
  }
}

console.log(
  `${dryRun ? "Dry run complete" : "Prune complete"}: ${planned.length} target(s), ${formatSize(removedBytes)} total`,
);

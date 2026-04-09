import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import isInstalledGlobally from 'is-installed-globally';

const packageDir = resolve(fileURLToPath(import.meta.url), "../..");
const distDir = resolve(fileURLToPath(import.meta.url), "..");
const BACKSLASH_RE = /\\/g;
const runtimeDir = resolve(distDir, "runtime");
const clientDir = resolve(distDir, "client");
const globalInstallMatch = [
  "/yarn/global/",
  "/pnpm/global/",
  "/npm/global/",
  "/.nvm/",
  "/.volta/",
  "/.fnm/",
  // On Windows
  "/nvm/versions/",
  "/n/versions/"
  // TODO: More info for other package managers
];
function isGlobalInstall() {
  if (isInstalledGlobally === true || isInstalledGlobally.default === true)
    return true;
  const dir = packageDir.replace(BACKSLASH_RE, "/");
  return globalInstallMatch.some((i) => dir.includes(i));
}

export { clientDir, distDir, isGlobalInstall, packageDir, runtimeDir };

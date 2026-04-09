import { colors } from 'consola/utils';
import { consola } from 'consola';
import { isMinimal } from 'std-env';
import { updateUser } from 'rc9';
import { statSync, readFileSync } from 'node:fs';

const version = "2.7.0";

const consentVersion = 1;

function updateUserNuxtRc(key, val) {
  updateUser({ [key]: val }, ".nuxtrc");
}

let isDockerCached;
function hasDockerEnv() {
  try {
    statSync("/.dockerenv");
    return true;
  } catch {
    return false;
  }
}
function hasDockerCGroup() {
  try {
    return readFileSync("/proc/self/cgroup", "utf8").includes("docker");
  } catch {
    return false;
  }
}
function hasDockerMountInfo() {
  try {
    return readFileSync("/proc/self/mountinfo", "utf8").includes("/docker/containers/");
  } catch {
    return false;
  }
}
function isDocker() {
  isDockerCached ??= hasDockerEnv() || hasDockerCGroup() || hasDockerMountInfo();
  return isDockerCached;
}

async function ensureUserconsent(options) {
  if (options.consent && options.consent >= consentVersion) {
    return true;
  }
  if (isMinimal || process.env.CODESANDBOX_SSE || process.env.NEXT_TELEMETRY_DISABLED || isDocker()) {
    return false;
  }
  consola.restoreAll();
  process.stdout.write("\n");
  consola.info(`${colors.green("Nuxt")} collects completely anonymous data about usage.
  This will help us improve Nuxt developer experience over time.
  Read more on ${colors.underline(colors.cyan("https://github.com/nuxt/telemetry"))}
`);
  const accepted = await consola.prompt("Are you interested in participating?", {
    type: "confirm"
  });
  process.stdout.write("\n");
  consola.wrapAll();
  if (accepted) {
    updateUserNuxtRc("telemetry.consent", consentVersion);
    updateUserNuxtRc("telemetry.enabled", true);
    return true;
  }
  updateUserNuxtRc("telemetry.enabled", false);
  return false;
}

export { consentVersion as c, ensureUserconsent as e, isDocker as i, updateUserNuxtRc as u, version as v };

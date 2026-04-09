'use strict';

const utils = require('consola/utils');
const consola = require('consola');
const stdEnv = require('std-env');
const rc = require('rc9');
const fs = require('node:fs');

const version = "2.7.0";

const consentVersion = 1;

function updateUserNuxtRc(key, val) {
  rc.updateUser({ [key]: val }, ".nuxtrc");
}

let isDockerCached;
function hasDockerEnv() {
  try {
    fs.statSync("/.dockerenv");
    return true;
  } catch {
    return false;
  }
}
function hasDockerCGroup() {
  try {
    return fs.readFileSync("/proc/self/cgroup", "utf8").includes("docker");
  } catch {
    return false;
  }
}
function hasDockerMountInfo() {
  try {
    return fs.readFileSync("/proc/self/mountinfo", "utf8").includes("/docker/containers/");
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
  if (stdEnv.isMinimal || process.env.CODESANDBOX_SSE || process.env.NEXT_TELEMETRY_DISABLED || isDocker()) {
    return false;
  }
  consola.consola.restoreAll();
  process.stdout.write("\n");
  consola.consola.info(`${utils.colors.green("Nuxt")} collects completely anonymous data about usage.
  This will help us improve Nuxt developer experience over time.
  Read more on ${utils.colors.underline(utils.colors.cyan("https://github.com/nuxt/telemetry"))}
`);
  const accepted = await consola.consola.prompt("Are you interested in participating?", {
    type: "confirm"
  });
  process.stdout.write("\n");
  consola.consola.wrapAll();
  if (accepted) {
    updateUserNuxtRc("telemetry.consent", consentVersion);
    updateUserNuxtRc("telemetry.enabled", true);
    return true;
  }
  updateUserNuxtRc("telemetry.enabled", false);
  return false;
}

exports.consentVersion = consentVersion;
exports.ensureUserconsent = ensureUserconsent;
exports.isDocker = isDocker;
exports.updateUserNuxtRc = updateUserNuxtRc;
exports.version = version;

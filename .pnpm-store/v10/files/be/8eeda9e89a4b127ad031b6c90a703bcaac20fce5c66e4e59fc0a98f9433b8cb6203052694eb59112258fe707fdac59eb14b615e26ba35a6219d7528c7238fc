import { existsSync, readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { resolve } from 'node:path';
import * as rc from 'rc9';
import { colors } from 'consola/utils';
import { consola } from 'consola';
import { loadNuxtConfig } from '@nuxt/kit';
import { isTest } from 'std-env';
import { createMain, defineCommand } from 'citty';
import { v as version, e as ensureUserconsent, c as consentVersion } from './shared/telemetry.Dgzu-axG.mjs';

function isTruthy(val) {
  return val === true || val === "true" || val === "1" || val === 1;
}
function parseDotenv(src) {
  const result = {};
  for (const line of src.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIndex = trimmed.indexOf("=");
    if (eqIndex === -1) continue;
    const key = trimmed.slice(0, eqIndex).trim();
    let value = trimmed.slice(eqIndex + 1).trim();
    if (value.startsWith('"') && value.endsWith('"') || value.startsWith("'") && value.endsWith("'")) {
      value = value.slice(1, -1);
    }
    result[key] = value;
  }
  return result;
}
const RC_FILENAME = ".nuxtrc";
const sharedArgs = {
  global: {
    type: "boolean",
    alias: "g",
    default: false,
    description: "Apply globally"
  },
  dir: {
    type: "positional",
    default: "."
  }
};
const main = createMain({
  meta: {
    name: "nuxt-telemetry",
    description: "Manage consent for Nuxt collecting anonymous telemetry data about general usage.",
    version
  },
  subCommands: {
    status: defineCommand({
      meta: {
        name: "status",
        description: "Show telemetry status"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = resolve(args.dir);
        await showStatus(dir, args.global);
      }
    }),
    enable: defineCommand({
      meta: {
        name: "enable",
        description: "Enable telemetry"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = resolve(args.dir);
        setRC(dir, "telemetry.enabled", true, args.global);
        setRC(dir, "telemetry.consent", consentVersion, args.global);
        await showStatus(dir, args.global);
        consola.info("You can disable telemetry with `npx nuxt-telemetry disable" + (args.global ? " --global" : args.dir ? " " + args.dir : "") + "`");
      }
    }),
    disable: defineCommand({
      meta: {
        name: "disable",
        description: "Disable telemetry"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = resolve(args.dir);
        setRC(dir, "telemetry.enabled", false, args.global);
        setRC(dir, "telemetry.consent", 0, args.global);
        await showStatus(dir, args.global);
        consola.info("You can enable telemetry with `npx nuxt-telemetry enable" + (args.global ? " --global" : args.dir ? " " + args.dir : "") + "`");
      }
    }),
    consent: defineCommand({
      meta: {
        name: "consent",
        description: "Prompt for user consent"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = resolve(args.dir);
        const accepted = await ensureUserconsent({});
        if (accepted && !args.global) {
          setRC(dir, "telemetry.enabled", true, args.global);
          setRC(dir, "telemetry.consent", consentVersion, args.global);
        }
        await showStatus(dir, args.global);
      }
    })
  }
});
async function _checkDisabled(dir) {
  if (isTest) {
    return "because you are running in a test environment";
  }
  if (isTruthy(process.env.NUXT_TELEMETRY_DISABLED)) {
    return "by the `NUXT_TELEMETRY_DISABLED` environment variable";
  }
  const dotenvFile = resolve(dir, ".env");
  if (existsSync(dotenvFile)) {
    const _env = parseDotenv(readFileSync(dotenvFile, "utf8"));
    if (isTruthy(_env.NUXT_TELEMETRY_DISABLED)) {
      return "by the `NUXT_TELEMETRY_DISABLED` environment variable set in " + dotenvFile;
    }
  }
  const disabledByConf = (conf) => conf.telemetry === false || conf.telemetry && conf.telemetry.enabled === false;
  try {
    const config = await loadNuxtConfig({ cwd: dir });
    for (const layer of config._layers) {
      if (disabledByConf(layer.config)) {
        return "by " + config._layers[0].configFile;
      }
    }
  } catch {
  }
  if (disabledByConf(rc.read({ name: RC_FILENAME, dir }))) {
    return "by " + resolve(dir, RC_FILENAME);
  }
  if (disabledByConf(rc.readUser({ name: RC_FILENAME }))) {
    return "by " + resolve(homedir(), RC_FILENAME);
  }
}
async function showStatus(dir, global) {
  const disabled = await _checkDisabled(dir);
  if (disabled) {
    consola.info(`Nuxt telemetry is ${colors.yellow("disabled")} ${disabled}.`);
  } else {
    consola.info(`Nuxt telemetry is ${colors.green("enabled")}`, global ? "on your machine." : "in the current project.");
  }
}
function setRC(dir, key, val, global) {
  const update = { [key]: val };
  if (global) {
    rc.updateUser(update, RC_FILENAME);
  } else {
    rc.update(update, { name: RC_FILENAME, dir });
  }
}
async function ensureNuxtProject(args) {
  if (args.global) {
    return;
  }
  const dir = resolve(args.dir);
  const nuxtConfig = await loadNuxtConfig({ cwd: dir });
  if (!nuxtConfig || !nuxtConfig._layers[0]?.configFile) {
    consola.error("You are not in a Nuxt project.");
    consola.info("You can try specifying a directory or by using the `--global` flag to configure telemetry for your machine.");
    process.exit();
  }
}

export { main };

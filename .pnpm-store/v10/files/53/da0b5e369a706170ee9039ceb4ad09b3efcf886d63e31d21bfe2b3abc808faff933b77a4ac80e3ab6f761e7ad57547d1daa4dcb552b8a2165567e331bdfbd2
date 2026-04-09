'use strict';

const fs = require('node:fs');
const os = require('node:os');
const node_path = require('node:path');
const rc = require('rc9');
const utils = require('consola/utils');
const consola = require('consola');
const kit = require('@nuxt/kit');
const stdEnv = require('std-env');
const citty = require('citty');
const consent = require('./shared/telemetry.BikY0E3b.cjs');

function _interopNamespaceCompat(e) {
  if (e && typeof e === 'object' && 'default' in e) return e;
  const n = Object.create(null);
  if (e) {
    for (const k in e) {
      n[k] = e[k];
    }
  }
  n.default = e;
  return n;
}

const rc__namespace = /*#__PURE__*/_interopNamespaceCompat(rc);

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
const main = citty.createMain({
  meta: {
    name: "nuxt-telemetry",
    description: "Manage consent for Nuxt collecting anonymous telemetry data about general usage.",
    version: consent.version
  },
  subCommands: {
    status: citty.defineCommand({
      meta: {
        name: "status",
        description: "Show telemetry status"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = node_path.resolve(args.dir);
        await showStatus(dir, args.global);
      }
    }),
    enable: citty.defineCommand({
      meta: {
        name: "enable",
        description: "Enable telemetry"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = node_path.resolve(args.dir);
        setRC(dir, "telemetry.enabled", true, args.global);
        setRC(dir, "telemetry.consent", consent.consentVersion, args.global);
        await showStatus(dir, args.global);
        consola.consola.info("You can disable telemetry with `npx nuxt-telemetry disable" + (args.global ? " --global" : args.dir ? " " + args.dir : "") + "`");
      }
    }),
    disable: citty.defineCommand({
      meta: {
        name: "disable",
        description: "Disable telemetry"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = node_path.resolve(args.dir);
        setRC(dir, "telemetry.enabled", false, args.global);
        setRC(dir, "telemetry.consent", 0, args.global);
        await showStatus(dir, args.global);
        consola.consola.info("You can enable telemetry with `npx nuxt-telemetry enable" + (args.global ? " --global" : args.dir ? " " + args.dir : "") + "`");
      }
    }),
    consent: citty.defineCommand({
      meta: {
        name: "consent",
        description: "Prompt for user consent"
      },
      args: sharedArgs,
      async run({ args }) {
        ensureNuxtProject(args);
        const dir = node_path.resolve(args.dir);
        const accepted = await consent.ensureUserconsent({});
        if (accepted && !args.global) {
          setRC(dir, "telemetry.enabled", true, args.global);
          setRC(dir, "telemetry.consent", consent.consentVersion, args.global);
        }
        await showStatus(dir, args.global);
      }
    })
  }
});
async function _checkDisabled(dir) {
  if (stdEnv.isTest) {
    return "because you are running in a test environment";
  }
  if (isTruthy(process.env.NUXT_TELEMETRY_DISABLED)) {
    return "by the `NUXT_TELEMETRY_DISABLED` environment variable";
  }
  const dotenvFile = node_path.resolve(dir, ".env");
  if (fs.existsSync(dotenvFile)) {
    const _env = parseDotenv(fs.readFileSync(dotenvFile, "utf8"));
    if (isTruthy(_env.NUXT_TELEMETRY_DISABLED)) {
      return "by the `NUXT_TELEMETRY_DISABLED` environment variable set in " + dotenvFile;
    }
  }
  const disabledByConf = (conf) => conf.telemetry === false || conf.telemetry && conf.telemetry.enabled === false;
  try {
    const config = await kit.loadNuxtConfig({ cwd: dir });
    for (const layer of config._layers) {
      if (disabledByConf(layer.config)) {
        return "by " + config._layers[0].configFile;
      }
    }
  } catch {
  }
  if (disabledByConf(rc__namespace.read({ name: RC_FILENAME, dir }))) {
    return "by " + node_path.resolve(dir, RC_FILENAME);
  }
  if (disabledByConf(rc__namespace.readUser({ name: RC_FILENAME }))) {
    return "by " + node_path.resolve(os.homedir(), RC_FILENAME);
  }
}
async function showStatus(dir, global) {
  const disabled = await _checkDisabled(dir);
  if (disabled) {
    consola.consola.info(`Nuxt telemetry is ${utils.colors.yellow("disabled")} ${disabled}.`);
  } else {
    consola.consola.info(`Nuxt telemetry is ${utils.colors.green("enabled")}`, global ? "on your machine." : "in the current project.");
  }
}
function setRC(dir, key, val, global) {
  const update = { [key]: val };
  if (global) {
    rc__namespace.updateUser(update, RC_FILENAME);
  } else {
    rc__namespace.update(update, { name: RC_FILENAME, dir });
  }
}
async function ensureNuxtProject(args) {
  if (args.global) {
    return;
  }
  const dir = node_path.resolve(args.dir);
  const nuxtConfig = await kit.loadNuxtConfig({ cwd: dir });
  if (!nuxtConfig || !nuxtConfig._layers[0]?.configFile) {
    consola.consola.error("You are not in a Nuxt project.");
    consola.consola.info("You can try specifying a directory or by using the `--global` flag to configure telemetry for your machine.");
    process.exit();
  }
}

exports.main = main;

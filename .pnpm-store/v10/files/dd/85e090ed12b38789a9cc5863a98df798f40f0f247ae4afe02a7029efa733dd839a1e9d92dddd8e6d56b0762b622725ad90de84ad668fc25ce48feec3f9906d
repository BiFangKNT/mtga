'use strict';

const kit = require('@nuxt/kit');
const consent = require('./shared/telemetry.BikY0E3b.cjs');
const ofetch = require('ofetch');
const os = require('node:os');
const fs = require('node:fs');
const node_child_process = require('node:child_process');
const stdEnv = require('std-env');
const node_crypto = require('node:crypto');
const node_path = require('node:path');
require('consola/utils');
require('consola');
require('rc9');

function _interopDefaultCompat (e) { return e && typeof e === 'object' && 'default' in e ? e.default : e; }

const os__default = /*#__PURE__*/_interopDefaultCompat(os);
const fs__default = /*#__PURE__*/_interopDefaultCompat(fs);

async function postEvent(endpoint, body) {
  const res = await ofetch.fetch(endpoint, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "content-type": "application/json",
      "user-agent": "Nuxt Telemetry " + consent.version
    }
  });
  if (!res.ok) {
    throw new Error(res.statusText);
  }
}

function hash(str) {
  return node_crypto.createHash("sha256").update(str).digest("hex").substr(0, 16);
}
function randomSeed() {
  return hash(node_crypto.randomUUID());
}

function getNuxtMajorVersion(nuxt) {
  for (let i = 2; i < 10; i++) {
    if (kit.isNuxtMajorVersion(i, nuxt)) {
      return i;
    }
  }
  return 2;
}
async function createContext(nuxt, options) {
  const rootDir = nuxt.options.workspaceDir || nuxt.options.rootDir || process.cwd();
  const git = await getGit(rootDir);
  const packageManager = detectPackageManager(rootDir);
  const { seed } = options;
  const projectHash = getProjectHash(rootDir, git, seed);
  const projectSession = getProjectSession(projectHash, seed);
  const nuxtVersion = kit.getNuxtVersion(nuxt);
  const nuxtMajorVersion = getNuxtMajorVersion(nuxt);
  const nodeVersion = process.version.replace("v", "");
  const isEdge = nuxtVersion.includes("edge");
  return {
    nuxt,
    seed,
    git,
    projectHash,
    projectSession,
    nuxtVersion,
    nuxtMajorVersion,
    isEdge,
    cli: getCLI(),
    nodeVersion,
    os: os__default.type().toLocaleLowerCase(),
    environment: getEnv(),
    packageManager: packageManager || "unknown",
    concent: options.consent
  };
}
function getEnv() {
  if (stdEnv.provider) {
    return stdEnv.provider;
  }
  if (consent.isDocker()) {
    return "Docker";
  }
  return "unknown";
}
function getCLI() {
  const entry = process.argv[1] ?? "";
  const knownCLIs = {
    "nuxt-ts.js": "nuxt-ts",
    "nuxt-start.js": "nuxt-start",
    "nuxt.js": "nuxt",
    "nuxi": "nuxi"
  };
  for (const _key in knownCLIs) {
    const key = _key;
    if (entry.includes(key)) {
      const edge = entry.includes("-edge") ? "-edge" : entry.includes("-nightly") ? "-nightly" : "";
      return knownCLIs[key] + edge;
    }
  }
  return "programmatic";
}
function getProjectSession(projectHash, sessionId) {
  return hash(`${projectHash}#${sessionId}`);
}
function getProjectHash(rootDir, git, seed) {
  let id;
  if (git && git.url) {
    id = `${git.source}#${git.owner}#${git.name}`;
  } else {
    id = `${rootDir}#${seed}`;
  }
  return hash(id);
}
async function getGitRemote(cwd) {
  let gitRemoteUrl = null;
  try {
    gitRemoteUrl = node_child_process.execSync("git config --get remote.origin.url  ", { encoding: "utf8", cwd }).trim() || null;
  } catch {
  }
  return gitRemoteUrl;
}
function detectPackageManager(rootDir) {
  const lockFiles = {
    "bun.lockb": "bun",
    "bun.lock": "bun",
    "deno.lock": "deno",
    "pnpm-lock.yaml": "pnpm",
    "pnpm-workspace.yaml": "pnpm",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
    "npm-shrinkwrap.json": "npm"
  };
  for (const [file, manager] of Object.entries(lockFiles)) {
    if (fs.existsSync(`${rootDir}/${file}`)) {
      return manager;
    }
  }
  try {
    const pkgJson = JSON.parse(fs.readFileSync(`${rootDir}/package.json`, "utf8"));
    if (typeof pkgJson.packageManager === "string") {
      const name = pkgJson.packageManager.split("@")[0];
      if (name) return name;
    }
  } catch {
  }
  return "unknown";
}
function parseGitUrl(gitUrl) {
  const normalized = gitUrl.trim();
  const sshMatch = normalized.match(/^[\w-]+@([^:]+):(.+?)(?:\.git)?$/);
  if (sshMatch) {
    const source = sshMatch[1];
    const path = sshMatch[2];
    const parts = path.split("/");
    if (parts.length >= 2) {
      return { source, owner: parts.slice(0, -1).join("/"), name: parts.at(-1) };
    }
  }
  try {
    const url = new URL(normalized);
    const pathname = url.pathname.replace(/\.git$/, "").replace(/^\//, "");
    const parts = pathname.split("/");
    if (parts.length >= 2) {
      return { source: url.hostname, owner: parts.slice(0, -1).join("/"), name: parts.at(-1) };
    }
  } catch {
  }
  return null;
}
async function getGit(rootDir) {
  const gitRemote = await getGitRemote(rootDir);
  if (!gitRemote) {
    return;
  }
  const meta = parseGitUrl(gitRemote);
  if (!meta) {
    return;
  }
  return {
    url: `https://${meta.source}/${meta.owner}/${meta.name}`,
    gitRemote,
    source: meta.source,
    owner: meta.owner,
    name: meta.name
  };
}

const logger = kit.useLogger("@nuxt/telemetry");

const build = function({ nuxt }, payload) {
  const duration = { build: payload.duration.build };
  let isSuccess = true;
  for (const [name, stat] of Object.entries(payload.stats)) {
    duration[name] = stat.duration;
    if (!stat.success) {
      isSuccess = false;
    }
  }
  return {
    name: "build",
    isSuccess,
    isDev: nuxt.options.dev || false,
    duration
    // size
  };
};

const command = function({ nuxt }) {
  let command2 = process.argv[2] || "unknown";
  const flagMap = {
    dev: "dev",
    _generate: "generate",
    _export: "export",
    _build: "build",
    _serve: "serve",
    _start: "start"
  };
  for (const _flag in flagMap) {
    const flag = _flag;
    if (nuxt.options[flag]) {
      command2 = flagMap[flag];
      break;
    }
  }
  return {
    name: "command",
    command: command2
  };
};

const generate = function generate2({ nuxt }, payload) {
  return {
    name: "generate",
    // @ts-expect-error Legacy type from Nuxt 2
    isExport: !!nuxt.options._export,
    routesCount: payload.routesCount,
    duration: {
      generate: payload.duration.generate
    }
  };
};

const module$2 = function({ nuxt: { options } }) {
  const events = [];
  const modules = (options._installedModules || []).filter((m) => m.meta?.version).map((m) => ({
    name: m.meta.name,
    version: m.meta.version,
    timing: m.timings?.setup || 0
  }));
  for (const m of modules) {
    events.push({
      name: "module",
      moduleName: m.name,
      version: m.version,
      timing: m.timing
    });
  }
  return events;
};

const project = function(context) {
  const { options } = context.nuxt;
  return {
    name: "project",
    type: context.git && context.git.url ? "git" : "local",
    isSSR: options.ssr !== false,
    target: options.server ? "server" : "static",
    packageManager: context.packageManager
  };
};

const session = function({ seed }) {
  return {
    name: "session",
    id: seed
  };
};

const files = async function(context) {
  const { options } = context.nuxt;
  const nuxtIgnore = fs__default.existsSync(node_path.resolve(options.rootDir, ".nuxtignore"));
  const nuxtRc = fs__default.existsSync(node_path.resolve(options.rootDir, ".nuxtrc"));
  const appConfig = fs__default.existsSync(await kit.resolvePath("~/app.config"));
  return {
    name: "files",
    nuxtIgnore,
    nuxtRc,
    appConfig
  };
};

class Telemetry {
  nuxt;
  options;
  storage;
  // TODO
  _contextPromise;
  events = [];
  eventFactories = {
    build,
    command,
    generate,
    module: module$2,
    project,
    session,
    files
  };
  constructor(nuxt, options) {
    this.nuxt = nuxt;
    this.options = options;
  }
  getContext() {
    if (!this._contextPromise) {
      this._contextPromise = createContext(this.nuxt, this.options);
    }
    return this._contextPromise;
  }
  createEvent(name, payload) {
    const eventFactory = this.eventFactories[name];
    if (typeof eventFactory !== "function") {
      logger.warn("Unknown event:", name);
      return;
    }
    const eventPromise = this._invokeEvent(name, eventFactory, payload);
    this.events.push(eventPromise);
  }
  async _invokeEvent(name, eventFactory, payload) {
    try {
      const context = await this.getContext();
      const event = await eventFactory(context, payload);
      event.name = name;
      return event;
    } catch (err) {
      logger.error("Error while running event:", err);
    }
  }
  async getPublicContext() {
    const context = await this.getContext();
    const eventContext = {};
    for (const key of [
      "nuxtVersion",
      "nuxtMajorVersion",
      "isEdge",
      "nodeVersion",
      "cli",
      "os",
      "environment",
      "projectHash",
      "projectSession"
    ]) {
      eventContext[key] = context[key];
    }
    return eventContext;
  }
  async sendEvents(debug) {
    const events = [].concat(...(await Promise.all(this.events)).filter(Boolean));
    this.events = [];
    const context = await this.getPublicContext();
    const body = {
      timestamp: Date.now(),
      context,
      events
    };
    if (this.options.endpoint) {
      const start = Date.now();
      try {
        if (debug) {
          logger.info("Sending events:", JSON.stringify(body, null, 2));
        }
        await postEvent(this.options.endpoint, body);
        if (debug) {
          logger.success(`Events sent to \`${this.options.endpoint}\` (${Date.now() - start} ms)`);
        }
      } catch (err) {
        if (debug) {
          logger.error(`Error sending sent to \`${this.options.endpoint}\` (${Date.now() - start} ms)
`, err);
        }
      }
    }
  }
}

const module$1 = kit.defineNuxtModule({
  meta: {
    name: "@nuxt/telemetry",
    configKey: "telemetry"
  },
  defaults: {
    endpoint: process.env.NUXT_TELEMETRY_ENDPOINT || "https://telemetry.nuxt.com",
    debug: process.env.NUXT_TELEMETRY_DEBUG === "1" || process.env.NUXT_TELEMETRY_DEBUG === "true",
    enabled: void 0,
    seed: void 0
  },
  async setup(toptions, nuxt) {
    if (!toptions.debug) {
      logger.level = 0;
    }
    const _topLevelTelemetry = nuxt.options.telemetry;
    if (_topLevelTelemetry !== true) {
      if (toptions.enabled === false || _topLevelTelemetry === false || !await consent.ensureUserconsent(toptions)) {
        logger.info("Telemetry disabled");
        return;
      }
    }
    logger.info("Telemetry enabled");
    if (!toptions.seed || typeof toptions.seed !== "string") {
      toptions.seed = randomSeed();
      consent.updateUserNuxtRc("telemetry.seed", toptions.seed);
      logger.info("Seed generated:", toptions.seed);
    }
    const t = new Telemetry(nuxt, toptions);
    nuxt.hook("modules:done", async () => {
      t.createEvent("project");
      if (nuxt.options.dev) {
        t.createEvent("session");
        t.createEvent("files");
      }
      t.createEvent("command");
      t.createEvent("module");
      await nuxt.callHook("telemetry:setup", t);
      t.sendEvents(toptions.debug);
    });
  }
});

module.exports = module$1;

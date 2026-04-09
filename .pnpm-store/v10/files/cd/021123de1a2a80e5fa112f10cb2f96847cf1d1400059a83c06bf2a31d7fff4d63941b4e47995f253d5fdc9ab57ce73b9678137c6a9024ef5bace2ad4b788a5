import process from 'node:process';
import c from 'ansis';
import { debounce } from 'perfect-debounce';
import sirv from 'sirv';
import { createRPCServer } from 'vite-dev-rpc';
import { DIR_CLIENT } from '../dirs.mjs';
import fs from 'node:fs/promises';
import { isAbsolute, resolve, join } from 'node:path';
import { hash } from 'ohash';
import { Buffer } from 'node:buffer';
import { createFilter } from 'unplugin-utils';
import Debug from 'debug';
import { parse } from 'error-stack-parser-es';
import { createServer } from 'node:http';

function createEnvOrderHooks(environmentNames, { onFirst, onEach, onLast }) {
  const remainingEnvs = new Set(environmentNames);
  let ranFirst = false;
  let ranLast = false;
  return async (envName, ...args) => {
    if (!ranFirst) {
      ranFirst = true;
      await onFirst?.(...args);
    }
    remainingEnvs.delete(envName);
    await onEach?.(...args);
    if (!ranLast && remainingEnvs.size === 0) {
      ranLast = true;
      await onLast?.(...args);
    }
  };
}
function createBuildGenerator(ctx) {
  const {
    outputDir = ".vite-inspect"
  } = ctx.options;
  const targetDir = isAbsolute(outputDir) ? outputDir : resolve(process.cwd(), outputDir);
  const reportsDir = join(targetDir, "reports");
  return {
    getOutputDir() {
      return targetDir;
    },
    async setupOutputDir() {
      await fs.rm(targetDir, { recursive: true, force: true });
      await fs.mkdir(reportsDir, { recursive: true });
      await fs.cp(DIR_CLIENT, targetDir, { recursive: true });
      await Promise.all([
        fs.writeFile(
          join(targetDir, "index.html"),
          (await fs.readFile(join(targetDir, "index.html"), "utf-8")).replace(
            'data-vite-inspect-mode="DEV"',
            'data-vite-inspect-mode="BUILD"'
          )
        )
      ]);
    },
    async generateForEnv(pluginCtx) {
      const env = pluginCtx.environment;
      await Promise.all(
        [...ctx._idToInstances.values()].filter((v) => v.environments.has(env.name)).map((v) => {
          const e = v.environments.get(env.name);
          const key = `${v.id}-${env.name}`;
          return [key, e];
        }).map(async ([key, env2]) => {
          await fs.mkdir(join(reportsDir, key, "transforms"), { recursive: true });
          return await Promise.all([
            writeJSON(
              join(reportsDir, key, "modules.json"),
              env2.getModulesList(pluginCtx)
            ),
            writeJSON(
              join(reportsDir, key, "metric-plugins.json"),
              env2.getPluginMetrics()
            ),
            ...Object.entries(env2.data.transform).map(([id, info]) => writeJSON(
              join(reportsDir, key, "transforms", `${hash(id)}.json`),
              {
                resolvedId: id,
                transforms: info
              }
            ))
          ]);
        })
      );
    },
    async generateMetadata() {
      await writeJSON(
        join(reportsDir, "metadata.json"),
        ctx.getMetadata()
      );
    }
  };
}
function writeJSON(filename, data) {
  return fs.writeFile(filename, `${JSON.stringify(data, null, 2)}
`);
}

const DUMMY_LOAD_PLUGIN_NAME = "__load__";

async function openBrowser(address) {
  await import('open').then((r) => r.default(address, { newInstance: true })).catch(() => {
  });
}
function serializePlugin(plugin) {
  return JSON.parse(JSON.stringify(plugin, (key, value) => {
    if (typeof value === "function") {
      let name = value.name;
      if (name === "anonymous")
        name = "";
      if (name === key)
        name = "";
      if (name)
        return `[Function ${name}]`;
      return "[Function]";
    }
    if (key === "api" && value)
      return "[Object API]";
    return value;
  }));
}
function removeVersionQuery(url) {
  if (url.includes("v=")) {
    return url.replace(/&v=\w+/, "").replace(/\?v=\w+/, "?").replace(/\?$/, "");
  }
  return url;
}

let viteCount = 0;
class InspectContext {
  constructor(options) {
    this.options = options;
    this.filter = createFilter(options.include, options.exclude);
  }
  _configToInstances = /* @__PURE__ */ new Map();
  _idToInstances = /* @__PURE__ */ new Map();
  filter;
  getMetadata() {
    return {
      instances: [...this._idToInstances.values()].map((vite) => ({
        root: vite.config.root,
        vite: vite.id,
        plugins: vite.config.plugins.map((i) => serializePlugin(i)),
        environments: [...vite.environments.keys()],
        environmentPlugins: Object.fromEntries(
          [...vite.environments.entries()].map(([name, env]) => {
            return [name, env.env.getTopLevelConfig().plugins.map((i) => vite.config.plugins.indexOf(i))];
          })
        )
      })),
      embedded: this.options.embedded
    };
  }
  getViteContext(configOrId) {
    if (typeof configOrId === "string") {
      if (!this._idToInstances.has(configOrId))
        throw new Error(`Can not found vite context for ${configOrId}`);
      return this._idToInstances.get(configOrId);
    }
    if (this._configToInstances.has(configOrId))
      return this._configToInstances.get(configOrId);
    const id = `vite${++viteCount}`;
    const vite = new InspectContextVite(id, this, configOrId);
    this._idToInstances.set(id, vite);
    this._configToInstances.set(configOrId, vite);
    return vite;
  }
  getEnvContext(env) {
    if (!env)
      return void 0;
    const vite = this.getViteContext(env.getTopLevelConfig());
    return vite.getEnvContext(env);
  }
  queryEnv(query) {
    const vite = this.getViteContext(query.vite);
    const env = vite.getEnvContext(query.env);
    return env;
  }
}
class InspectContextVite {
  constructor(id, context, config) {
    this.id = id;
    this.context = context;
    this.config = config;
  }
  environments = /* @__PURE__ */ new Map();
  data = {
    serverMetrics: {
      middleware: {}
    }
  };
  getEnvContext(env) {
    if (typeof env === "string") {
      if (!this.environments.has(env))
        throw new Error(`Can not found environment context for ${env}`);
      return this.environments.get(env);
    }
    if (env.getTopLevelConfig() !== this.config)
      throw new Error("Environment config does not match Vite config");
    if (!this.environments.has(env.name))
      this.environments.set(env.name, new InspectContextViteEnv(this.context, this, env));
    return this.environments.get(env.name);
  }
}
class InspectContextViteEnv {
  constructor(contextMain, contextVite, env) {
    this.contextMain = contextMain;
    this.contextVite = contextVite;
    this.env = env;
  }
  data = {
    transform: {},
    resolveId: {},
    transformCounter: {}
  };
  recordTransform(id, info, preTransformCode) {
    id = this.normalizeId(id);
    if (!this.data.transform[id] || !this.data.transform[id].some((tr) => tr.result)) {
      this.data.transform[id] = [{
        name: DUMMY_LOAD_PLUGIN_NAME,
        result: preTransformCode,
        start: info.start,
        end: info.start,
        sourcemaps: info.sourcemaps
      }];
      this.data.transformCounter[id] = (this.data.transformCounter[id] || 0) + 1;
    }
    this.data.transform[id].push(info);
  }
  recordLoad(id, info) {
    id = this.normalizeId(id);
    this.data.transform[id] = [info];
    this.data.transformCounter[id] = (this.data.transformCounter[id] || 0) + 1;
  }
  recordResolveId(id, info) {
    id = this.normalizeId(id);
    if (!this.data.resolveId[id])
      this.data.resolveId[id] = [];
    this.data.resolveId[id].push(info);
  }
  invalidate(id) {
    id = this.normalizeId(id);
    delete this.data.transform[id];
  }
  normalizeId(id) {
    if (this.contextMain.options.removeVersionQuery !== false)
      return removeVersionQuery(id);
    return id;
  }
  getModulesList(pluginCtx) {
    const moduleGraph = this.env.mode === "dev" ? this.env.moduleGraph : void 0;
    const getDeps = moduleGraph ? (id) => Array.from(moduleGraph.getModuleById(id)?.importedModules || []).map((i) => i.id || "").filter(Boolean) : pluginCtx ? (id) => pluginCtx.getModuleInfo(id)?.importedIds || [] : () => [];
    const getImporters = moduleGraph ? (id) => Array.from(moduleGraph?.getModuleById(id)?.importers || []).map((i) => i.id || "").filter(Boolean) : pluginCtx ? (id) => pluginCtx.getModuleInfo(id)?.importers || [] : () => [];
    function isVirtual(pluginName, transformName) {
      return pluginName !== DUMMY_LOAD_PLUGIN_NAME && transformName !== "vite:load-fallback" && transformName !== "vite:build-load-fallback";
    }
    const transformedIdMap = Object.values(this.data.resolveId).reduce((map, ids2) => {
      ids2.forEach((id) => {
        map[id.result] ??= [];
        map[id.result].push(id);
      });
      return map;
    }, {});
    const ids = new Set(Object.keys(this.data.transform).concat(Object.keys(transformedIdMap)));
    return Array.from(ids).sort().map((id) => {
      let totalTime = 0;
      const plugins = (this.data.transform[id] || []).filter((tr) => tr.result).map((transItem) => {
        const delta = transItem.end - transItem.start;
        totalTime += delta;
        return { name: transItem.name, transform: delta };
      }).concat(
        // @ts-expect-error transform is optional
        (transformedIdMap[id] || []).map((idItem) => {
          return { name: idItem.name, resolveId: idItem.end - idItem.start };
        })
      );
      function getSize(str) {
        if (!str)
          return 0;
        return Buffer.byteLength(str, "utf8");
      }
      return {
        id,
        deps: getDeps(id),
        importers: getImporters(id),
        plugins,
        virtual: isVirtual(plugins[0]?.name || "", this.data.transform[id]?.[0].name || ""),
        totalTime,
        invokeCount: this.data.transformCounter?.[id] || 0,
        sourceSize: getSize(this.data.transform[id]?.[0]?.result),
        distSize: getSize(this.data.transform[id]?.[this.data.transform[id].length - 1]?.result)
      };
    });
  }
  resolveId(id = "", ssr = false) {
    if (id.startsWith("./"))
      id = resolve(this.env.getTopLevelConfig().root, id).replace(/\\/g, "/");
    return this.resolveIdRecursive(id, ssr);
  }
  resolveIdRecursive(id, ssr = false) {
    const resolved = this.data.resolveId[id]?.[0]?.result;
    return resolved ? this.resolveIdRecursive(resolved, ssr) : id;
  }
  getPluginMetrics() {
    const map = {};
    const defaultMetricInfo = () => ({
      transform: { invokeCount: 0, totalTime: 0 },
      resolveId: { invokeCount: 0, totalTime: 0 }
    });
    this.env.getTopLevelConfig().plugins.forEach((i) => {
      map[i.name] = {
        ...defaultMetricInfo(),
        name: i.name,
        enforce: i.enforce
      };
    });
    Object.values(this.data.transform).forEach((transformInfos) => {
      transformInfos.forEach(({ name, start, end }) => {
        if (name === DUMMY_LOAD_PLUGIN_NAME)
          return;
        if (!map[name])
          map[name] = { ...defaultMetricInfo(), name };
        map[name].transform.totalTime += end - start;
        map[name].transform.invokeCount += 1;
      });
    });
    Object.values(this.data.resolveId).forEach((resolveIdInfos) => {
      resolveIdInfos.forEach(({ name, start, end }) => {
        if (!map[name])
          map[name] = { ...defaultMetricInfo(), name };
        map[name].resolveId.totalTime += end - start;
        map[name].resolveId.invokeCount += 1;
      });
    });
    const metrics = Object.values(map).filter(Boolean).sort((a, b) => a.name.localeCompare(b.name));
    return metrics;
  }
  async getModuleTransformInfo(id, clear = false) {
    if (clear) {
      this.clearId(id);
      try {
        if (this.env.mode === "dev")
          await this.env.transformRequest(id);
      } catch {
      }
    }
    const resolvedId = this.resolveId(id);
    return {
      resolvedId,
      transforms: this.data.transform[resolvedId] || []
    };
  }
  clearId(_id) {
    const id = this.resolveId(_id);
    if (id) {
      const moduleGraph = this.env.mode === "dev" ? this.env.moduleGraph : void 0;
      const mod = moduleGraph?.getModuleById(id);
      if (mod)
        moduleGraph?.invalidateModule(mod);
      this.invalidate(id);
    }
  }
}

const debug = Debug("vite-plugin-inspect");
function hijackHook(plugin, name, wrapper) {
  if (!plugin[name])
    return;
  debug(`hijack plugin "${name}"`, plugin.name);
  let order = plugin.order || plugin.enforce || "normal";
  const hook = plugin[name];
  if ("handler" in hook) {
    const oldFn = hook.handler;
    order += `-${hook.order || hook.enforce || "normal"}`;
    hook.handler = function(...args) {
      return wrapper(oldFn, this, args, order);
    };
  } else if ("transform" in hook) {
    const oldFn = hook.transform;
    order += `-${hook.order || hook.enforce || "normal"}`;
    hook.transform = function(...args) {
      return wrapper(oldFn, this, args, order);
    };
  } else {
    const oldFn = hook;
    plugin[name] = function(...args) {
      return wrapper(oldFn, this, args, order);
    };
  }
}
const hijackedPlugins = /* @__PURE__ */ new WeakSet();
function hijackPlugin(plugin, ctx) {
  if (hijackedPlugins.has(plugin))
    return;
  hijackedPlugins.add(plugin);
  hijackHook(plugin, "transform", async (fn, context, args, order) => {
    const code = args[0];
    const id = args[1];
    let _result;
    let error;
    const start = Date.now();
    try {
      _result = await fn.apply(context, args);
    } catch (_err) {
      error = _err;
    }
    const end = Date.now();
    const result = error ? "[Error]" : typeof _result === "string" ? _result : _result?.code;
    if (ctx.filter(id)) {
      const sourcemaps = typeof _result === "string" ? null : _result?.map;
      ctx.getEnvContext(context?.environment)?.recordTransform(id, {
        name: plugin.name,
        result,
        start,
        end,
        order,
        sourcemaps,
        error: error ? parseError(error) : void 0
      }, code);
    }
    if (error)
      throw error;
    return _result;
  });
  hijackHook(plugin, "load", async (fn, context, args) => {
    const id = args[0];
    let _result;
    let error;
    const start = Date.now();
    try {
      _result = await fn.apply(context, args);
    } catch (err) {
      error = err;
    }
    const end = Date.now();
    const result = error ? "[Error]" : typeof _result === "string" ? _result : _result?.code;
    const sourcemaps = typeof _result === "string" ? null : _result?.map;
    if (result) {
      ctx.getEnvContext(context?.environment)?.recordLoad(id, {
        name: plugin.name,
        result,
        start,
        end,
        sourcemaps,
        error: error ? parseError(error) : void 0
      });
    }
    if (error)
      throw error;
    return _result;
  });
  hijackHook(plugin, "resolveId", async (fn, context, args) => {
    const id = args[0];
    let _result;
    let error;
    const start = Date.now();
    try {
      _result = await fn.apply(context, args);
    } catch (err) {
      error = err;
    }
    const end = Date.now();
    if (!ctx.filter(id)) {
      if (error)
        throw error;
      return _result;
    }
    const result = error ? stringifyError(error) : typeof _result === "object" ? _result?.id : _result;
    if (result && result !== id) {
      ctx.getEnvContext(context?.environment)?.recordResolveId(id, {
        name: plugin.name,
        result,
        start,
        end,
        error
      });
    }
    if (error)
      throw error;
    return _result;
  });
}
function parseError(error) {
  const stack = parse(error, { allowEmpty: true });
  const message = error.message || String(error);
  return {
    message,
    stack,
    raw: error
  };
}
function stringifyError(err) {
  return String(err.stack ? err.stack : err);
}

function createPreviewServer(staticPath) {
  const server = createServer();
  const statics = sirv(staticPath);
  server.on("request", (req, res) => {
    statics(req, res, () => {
      res.statusCode = 404;
      res.end("File not found");
    });
  });
  server.listen(0, () => {
    const { port } = server.address();
    const url = `http://localhost:${port}`;
    console.log(`  ${c.green("\u279C")}  ${c.bold("Inspect Preview Started")}: ${url}`);
    openBrowser(url);
  });
}

function createServerRpc(ctx) {
  const rpc = {
    async getMetadata() {
      return ctx.getMetadata();
    },
    async getModulesList(query) {
      return ctx.queryEnv(query).getModulesList();
    },
    async getPluginMetrics(query) {
      return ctx.queryEnv(query).getPluginMetrics();
    },
    async getModuleTransformInfo(query, id, clear) {
      return ctx.queryEnv(query).getModuleTransformInfo(id, clear);
    },
    async resolveId(query, id) {
      return ctx.queryEnv(query).resolveId(id);
    },
    async getServerMetrics(query) {
      return ctx.getViteContext(query.vite).data.serverMetrics || {};
    },
    async onModuleUpdated() {
    }
  };
  return rpc;
}

const NAME = "vite-plugin-inspect";
const isCI = !!process.env.CI;
function PluginInspect(options = {}) {
  const {
    dev = true,
    build = false,
    silent = false,
    open: _open = false
  } = options;
  if (!dev && !build) {
    return {
      name: NAME
    };
  }
  const ctx = new InspectContext(options);
  let onBuildEnd;
  const timestampRE = /\bt=\d{13}&?\b/;
  const trailingSeparatorRE = /[?&]$/;
  function setupMiddlewarePerf(ctx2, middlewares) {
    let firstMiddlewareIndex = -1;
    middlewares.forEach((middleware, index) => {
      const { handle: originalHandle } = middleware;
      if (typeof originalHandle !== "function" || !originalHandle.name)
        return middleware;
      middleware.handle = function(...middlewareArgs) {
        let req;
        if (middlewareArgs.length === 4)
          [, req] = middlewareArgs;
        else
          [req] = middlewareArgs;
        const start = Date.now();
        const url = req.url?.replace(timestampRE, "").replace(trailingSeparatorRE, "");
        ctx2.data.serverMetrics.middleware[url] ??= [];
        if (firstMiddlewareIndex < 0)
          firstMiddlewareIndex = index;
        if (index === firstMiddlewareIndex)
          ctx2.data.serverMetrics.middleware[url] = [];
        const result = originalHandle.apply(this, middlewareArgs);
        Promise.resolve(result).then(() => {
          const total = Date.now() - start;
          const metrics = ctx2.data.serverMetrics.middleware[url];
          ctx2.data.serverMetrics.middleware[url].push({
            self: metrics.length ? Math.max(total - metrics[metrics.length - 1].total, 0) : total,
            total,
            name: originalHandle.name
          });
        });
        return result;
      };
      Object.defineProperty(middleware.handle, "name", {
        value: originalHandle.name,
        configurable: true,
        enumerable: true
      });
      return middleware;
    });
  }
  function configureServer(server) {
    const config = server.config;
    Object.values(server.environments).forEach((env) => {
      const envCtx = ctx.getEnvContext(env);
      const _invalidateModule = env.moduleGraph.invalidateModule;
      env.moduleGraph.invalidateModule = function(...args) {
        const mod = args[0];
        if (mod?.id)
          envCtx.invalidate(mod.id);
        return _invalidateModule.apply(this, args);
      };
    });
    const base = (options.base ?? server.config.base) || "/";
    server.middlewares.use(`${base}__inspect`, sirv(DIR_CLIENT, {
      single: true,
      dev: true
    }));
    const rpc = createServerRpc(ctx);
    const rpcServer = createRPCServer(
      "vite-plugin-inspect",
      server.ws,
      rpc
    );
    const debouncedModuleUpdated = debounce(() => {
      rpcServer.onModuleUpdated.asEvent();
    }, 100);
    server.middlewares.use((req, res, next) => {
      debouncedModuleUpdated();
      next();
    });
    const _print = server.printUrls;
    server.printUrls = () => {
      let host = `${config.server.https ? "https" : "http"}://localhost:${config.server.port || "80"}`;
      const url = server.resolvedUrls?.local[0];
      if (url) {
        try {
          const u = new URL(url);
          host = `${u.protocol}//${u.host}`;
        } catch (error) {
          config.logger.warn(`Parse resolved url failed: ${error}`);
        }
      }
      _print();
      if (!silent) {
        const colorUrl = (url2) => c.green(url2.replace(/:(\d+)\//, (_, port) => `:${c.bold(port)}/`));
        config.logger.info(`  ${c.green("\u279C")}  ${c.bold("Inspect")}: ${colorUrl(`${host}${base}__inspect/`)}`);
      }
      if (_open && !isCI) {
        setTimeout(() => {
          openBrowser(`${host}${base}__inspect/`);
        }, 500);
      }
    };
    return rpc;
  }
  const plugin = {
    name: NAME,
    enforce: "pre",
    apply(_, { command }) {
      if (command === "serve" && dev)
        return true;
      if (command === "build" && build)
        return true;
      return false;
    },
    configResolved(config) {
      config.plugins.forEach((plugin2) => hijackPlugin(plugin2, ctx));
      const _createResolver = config.createResolver;
      config.createResolver = function(...args) {
        const _resolver = _createResolver.apply(this, args);
        return async function(...args2) {
          const id = args2[0];
          const aliasOnly = args2[2];
          const ssr = args2[3];
          const start = Date.now();
          const result = await _resolver.apply(this, args2);
          const end = Date.now();
          if (result && result !== id) {
            const pluginName = aliasOnly ? "alias" : "vite:resolve (+alias)";
            const vite = ctx.getViteContext(config);
            const env = vite.getEnvContext(ssr ? "ssr" : "client");
            env.recordResolveId(id, { name: pluginName, result, start, end });
          }
          return result;
        };
      };
      if (build) {
        const buildGenerator = createBuildGenerator(ctx);
        onBuildEnd = createEnvOrderHooks(Object.keys(config.environments), {
          async onFirst() {
            await buildGenerator.setupOutputDir();
          },
          async onEach(pluginCtx) {
            await buildGenerator.generateForEnv(pluginCtx);
          },
          async onLast(pluginCtx) {
            await buildGenerator.generateMetadata();
            const dir = buildGenerator.getOutputDir();
            pluginCtx.environment.logger.info(`${c.green("Inspect report generated at")}  ${c.dim(dir)}`);
            if (_open && !isCI)
              createPreviewServer(dir);
          }
        });
      }
    },
    configureServer(server) {
      const rpc = configureServer(server);
      plugin.api = {
        rpc
      };
      return () => {
        setupMiddlewarePerf(
          ctx.getViteContext(server.config),
          server.middlewares.stack
        );
      };
    },
    load: {
      order: "pre",
      handler(id) {
        ctx.getEnvContext(this.environment)?.invalidate(id);
        return null;
      }
    },
    hotUpdate({ modules }) {
      const ids = modules.map((module) => module.id);
      this.environment.hot.send({
        type: "custom",
        event: "vite-plugin-inspect:update",
        data: { ids }
      });
    },
    async buildEnd() {
      onBuildEnd?.(this.environment.name, this);
    },
    sharedDuringBuild: true
  };
  return plugin;
}

export { PluginInspect as P };

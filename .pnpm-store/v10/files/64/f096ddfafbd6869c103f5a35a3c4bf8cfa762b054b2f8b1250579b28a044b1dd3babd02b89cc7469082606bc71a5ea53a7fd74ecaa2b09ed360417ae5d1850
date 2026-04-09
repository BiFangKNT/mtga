import { spawn } from "node:child_process";
import { npmRunPathEnv } from "npm-run-path";
import colors from "picocolors";
import { Checker } from "./Checker.js";
import {
  composePreambleCode,
  RUNTIME_CLIENT_ENTRY_PATH,
  RUNTIME_CLIENT_RUNTIME_PATH,
  runtimeCode,
  WS_CHECKER_RECONNECT_EVENT,
  wrapVirtualPrefix
} from "./client/index.js";
import {
  ACTION_TYPES
} from "./types.js";
const buildInCheckerKeys = [
  "typescript",
  "vueTsc",
  "vls",
  "eslint",
  "stylelint",
  "biome",
  "oxlint"
];
async function createCheckers(userConfig, env) {
  const serveAndBuildCheckers = [];
  const { enableBuild, overlay } = userConfig;
  const sharedConfig = { enableBuild, overlay };
  for (const name of buildInCheckerKeys) {
    if (!userConfig[name]) continue;
    const { createServeAndBuild } = await import(`./checkers/${name}/main.js`);
    serveAndBuildCheckers.push(
      createServeAndBuild({ [name]: userConfig[name], ...sharedConfig }, env)
    );
  }
  return serveAndBuildCheckers;
}
function checker(userConfig) {
  const enableBuild = (userConfig == null ? void 0 : userConfig.enableBuild) ?? true;
  const enableOverlay = (userConfig == null ? void 0 : userConfig.overlay) !== false;
  const enableTerminal = (userConfig == null ? void 0 : userConfig.terminal) !== false;
  const overlayConfig = typeof (userConfig == null ? void 0 : userConfig.overlay) === "object" ? userConfig == null ? void 0 : userConfig.overlay : {};
  let initialized = false;
  let initializeCounter = 0;
  let checkers = [];
  let isProduction = false;
  let baseWithOrigin;
  let viteMode;
  let buildWatch = false;
  let logger = null;
  let checkerPromise = null;
  return {
    name: "vite-plugin-checker",
    enforce: "pre",
    // @ts-ignore
    __internal__checker: Checker,
    config: async (_config, env) => {
      viteMode = env.command;
      if (initializeCounter === 0) {
        initializeCounter++;
      } else {
        initialized = true;
        return;
      }
      checkers = await createCheckers(userConfig || {}, env);
      if (viteMode !== "serve") return;
      for (const checker2 of checkers) {
        const workerConfig = checker2.serve.config;
        workerConfig({
          enableOverlay,
          enableTerminal,
          env
        });
      }
    },
    configResolved(config) {
      logger = config.logger;
      baseWithOrigin = config.server.origin ? config.server.origin + config.base : config.base;
      isProduction || (isProduction = config.isProduction || config.command === "build");
      buildWatch = !!config.build.watch;
    },
    async buildEnd() {
      if (viteMode !== "serve") {
        await checkerPromise;
      }
      if (initialized) return;
      if (viteMode === "serve") {
        for (const checker2 of checkers) {
          const { worker } = checker2.serve;
          worker.terminate();
        }
      }
    },
    resolveId(id) {
      if (id === RUNTIME_CLIENT_RUNTIME_PATH || id === RUNTIME_CLIENT_ENTRY_PATH) {
        return wrapVirtualPrefix(id);
      }
      return;
    },
    load(id) {
      if (id === wrapVirtualPrefix(RUNTIME_CLIENT_RUNTIME_PATH)) {
        return runtimeCode;
      }
      if (id === wrapVirtualPrefix(RUNTIME_CLIENT_ENTRY_PATH)) {
        return composePreambleCode({ baseWithOrigin, overlayConfig });
      }
      return;
    },
    transformIndexHtml() {
      if (initialized) return;
      if (isProduction) return;
      return [
        {
          tag: "script",
          attrs: { type: "module" },
          children: composePreambleCode({ baseWithOrigin, overlayConfig })
        }
      ];
    },
    buildStart: () => {
      if (initialized) return;
      if (!isProduction || !enableBuild) return;
      const localEnv = npmRunPathEnv({
        env: process.env,
        cwd: process.cwd(),
        execPath: process.execPath
      });
      const spawnedCheckers = checkers.map(
        (checker2) => spawnChecker(checker2, userConfig, localEnv)
      );
      checkerPromise = Promise.all(spawnedCheckers).then((exitCodes) => {
        const exitCode = exitCodes.find((code) => code !== 0) ?? 0;
        if (exitCode !== 0 && !buildWatch) {
          process.exit(exitCode);
        }
      });
    },
    configureServer(server) {
      if (initialized) return;
      const latestOverlayErrors = new Array(
        checkers.length
      );
      checkers.forEach((checker2, index) => {
        const { worker, configureServer: workerConfigureServer } = checker2.serve;
        workerConfigureServer({ root: userConfig.root || server.config.root });
        worker.on("message", (action) => {
          if (action.type === ACTION_TYPES.overlayError) {
            latestOverlayErrors[index] = action.payload;
            if (action.payload) {
              server.ws.send("vite-plugin-checker", action.payload);
            }
          } else if (action.type === ACTION_TYPES.console) {
            if (Checker.logger.length) {
              Checker.log(action);
            } else {
              logger[action.level](action.payload);
            }
          }
        });
      });
      if (server.ws.on) {
        server.watcher.on("change", () => {
          logger.clearScreen("error");
        });
        server.ws.on("vite-plugin-checker", (data) => {
          if (data.event === "runtime-loaded") {
            server.ws.send("vite-plugin-checker", {
              event: WS_CHECKER_RECONNECT_EVENT,
              data: latestOverlayErrors.filter(Boolean)
            });
          }
        });
      } else {
        setTimeout(() => {
          logger.warn(
            colors.yellow(
              "[vite-plugin-checker]: `server.ws.on` is introduced to Vite in 2.6.8, see [PR](https://github.com/vitejs/vite/pull/5273) and [changelog](https://github.com/vitejs/vite/blob/main/packages/vite/CHANGELOG.md#268-2021-10-18). \nvite-plugin-checker relies on `server.ws.on` to send overlay message to client. Support for Vite < 2.6.8 will be removed in the next major version release."
            )
          );
        }, 5e3);
      }
    }
  };
}
function spawnChecker(checker2, userConfig, localEnv) {
  return new Promise((resolve) => {
    const buildBin = checker2.build.buildBin;
    const finalBin = typeof buildBin === "function" ? buildBin(userConfig) : buildBin;
    const [command, args] = finalBin;
    const commandWithArgs = [command, ...args].join(" ");
    const proc = spawn(commandWithArgs, {
      cwd: process.cwd(),
      stdio: "inherit",
      env: localEnv,
      // shell is necessary on windows to get the process to even start.
      // Command line args constructed by checkers therefore need to escape double quotes
      // to have them not striped out by cmd.exe. Using shell on all platforms lets us avoid
      // having to perform platform-specific logic around escaping quotes since all platform
      // shells will strip out unescaped double quotes. E.g. shell=false on linux only would
      // result in escaped quotes not being unescaped.
      shell: true
    });
    proc.on("exit", (code) => {
      if (code !== null && code !== 0) {
        resolve(code);
      } else {
        resolve(0);
      }
    });
  });
}
var main_default = checker;
export {
  checker,
  main_default as default
};
//# sourceMappingURL=main.js.map
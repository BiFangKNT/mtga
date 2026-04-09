import path from "node:path";
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import chokidar from "chokidar";
import { Checker } from "../../Checker.js";
import { FileDiagnosticManager } from "../../FileDiagnosticManager.js";
import {
  composeCheckerSummary,
  consoleLog,
  diagnosticToConsoleLevel,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  filterLogLevel,
  toClientPayload
} from "../../logger.js";
import {
  ACTION_TYPES,
  DiagnosticLevel
} from "../../types.js";
import { getBiomeCommand, runBiome, severityMap } from "./cli.js";
const __filename = fileURLToPath(import.meta.url);
const manager = new FileDiagnosticManager();
let createServeAndBuild;
const createDiagnostic = (pluginConfig) => {
  var _a, _b;
  const biomeConfig = pluginConfig.biome;
  let overlay = true;
  let terminal = true;
  let command = "lint";
  let flags = "";
  if (typeof biomeConfig === "object") {
    command = ((_a = biomeConfig == null ? void 0 : biomeConfig.dev) == null ? void 0 : _a.command) || (biomeConfig == null ? void 0 : biomeConfig.command) || "lint";
    flags = ((_b = biomeConfig == null ? void 0 : biomeConfig.dev) == null ? void 0 : _b.flags) || (biomeConfig == null ? void 0 : biomeConfig.flags) || "";
  }
  return {
    config: async ({ enableOverlay, enableTerminal }) => {
      overlay = enableOverlay;
      terminal = enableTerminal;
    },
    async configureServer({ root }) {
      if (!biomeConfig) return;
      const logLevel = (() => {
        var _a2;
        if (typeof biomeConfig !== "object") return void 0;
        const userLogLevel = (_a2 = biomeConfig.dev) == null ? void 0 : _a2.logLevel;
        if (!userLogLevel) return void 0;
        return userLogLevel.map((l) => severityMap[l]);
      })();
      const dispatchDiagnostics = () => {
        var _a2;
        const diagnostics2 = filterLogLevel(manager.getDiagnostics(), logLevel);
        if (terminal) {
          for (const d of diagnostics2) {
            consoleLog(
              diagnosticToTerminalLog(d, "Biome"),
              diagnosticToConsoleLevel(d)
            );
          }
          const errorCount = diagnostics2.filter(
            (d) => d.level === DiagnosticLevel.Error
          ).length;
          const warningCount = diagnostics2.filter(
            (d) => d.level === DiagnosticLevel.Warning
          ).length;
          consoleLog(
            composeCheckerSummary("Biome", errorCount, warningCount),
            errorCount ? "error" : warningCount ? "warn" : "info"
          );
        }
        if (overlay) {
          (_a2 = parentPort) == null ? void 0 : _a2.postMessage({
            type: ACTION_TYPES.overlayError,
            payload: toClientPayload(
              "biome",
              diagnostics2.map((d) => diagnosticToRuntimeError(d))
            )
          });
        }
      };
      const handleFileChange = async (filePath, type) => {
        const absPath = path.resolve(root, filePath);
        if (type === "unlink") {
          manager.updateByFileId(absPath, []);
        } else if (type === "change") {
          const isConfigFile = path.basename(absPath) === "biome.json";
          if (isConfigFile) {
            const runCommand2 = getBiomeCommand(command, flags, root);
            const diagnostics2 = await runBiome(runCommand2, root);
            manager.initWith(diagnostics2);
          } else {
            const runCommand2 = getBiomeCommand(command, flags, absPath);
            const diagnosticsOfChangedFile = await runBiome(runCommand2, root);
            manager.updateByFileId(absPath, diagnosticsOfChangedFile);
          }
        }
        dispatchDiagnostics();
      };
      const runCommand = getBiomeCommand(command, flags, root);
      const diagnostics = await runBiome(runCommand, root);
      manager.initWith(diagnostics);
      dispatchDiagnostics();
      let watchTarget = root;
      if (typeof biomeConfig === "object" && biomeConfig.watchPath) {
        if (Array.isArray(biomeConfig.watchPath)) {
          watchTarget = biomeConfig.watchPath.map((p) => path.resolve(root, p));
        } else {
          watchTarget = path.resolve(root, biomeConfig.watchPath);
        }
      }
      const watcher = chokidar.watch(watchTarget, {
        cwd: root,
        ignored: (path2) => path2.includes("node_modules")
      });
      watcher.on("change", async (filePath) => {
        handleFileChange(filePath, "change");
      });
      watcher.on("unlink", async (filePath) => {
        handleFileChange(filePath, "unlink");
      });
    }
  };
};
class BiomeChecker extends Checker {
  constructor() {
    super({
      name: "biome",
      absFilePath: __filename,
      build: {
        buildBin: (pluginConfig) => {
          if (typeof pluginConfig.biome === "object") {
            const { command, flags } = pluginConfig.biome;
            return ["biome", [command || "check", flags || ""]];
          }
          return ["biome", ["check"]];
        }
      },
      createDiagnostic
    });
  }
  init() {
    const _createServeAndBuild = super.initMainThread();
    createServeAndBuild = _createServeAndBuild;
    super.initWorkerThread();
  }
}
const biomeChecker = new BiomeChecker();
biomeChecker.prepare();
biomeChecker.init();
export {
  BiomeChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
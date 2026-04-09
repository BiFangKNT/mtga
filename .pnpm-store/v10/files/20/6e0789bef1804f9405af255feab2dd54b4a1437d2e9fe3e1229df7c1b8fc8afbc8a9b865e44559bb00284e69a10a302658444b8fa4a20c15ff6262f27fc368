import path from "node:path";
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import chokidar from "chokidar";
import stylelint from "stylelint";
import { Checker } from "../../Checker.js";
import { FileDiagnosticManager } from "../../FileDiagnosticManager.js";
import { createIgnore } from "../../glob.js";
import {
  composeCheckerSummary,
  consoleLog,
  diagnosticToConsoleLevel,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  filterLogLevel,
  normalizeStylelintDiagnostic,
  toClientPayload
} from "../../logger.js";
import { ACTION_TYPES, DiagnosticLevel } from "../../types.js";
import { translateOptions } from "./options.js";
const manager = new FileDiagnosticManager();
let createServeAndBuild;
const __filename = fileURLToPath(import.meta.url);
const createDiagnostic = (pluginConfig) => {
  let overlay = true;
  let terminal = true;
  return {
    config: async ({ enableOverlay, enableTerminal }) => {
      overlay = enableOverlay;
      terminal = enableTerminal;
    },
    async configureServer({ root }) {
      var _a;
      if (!pluginConfig.stylelint) return;
      const translatedOptions = await translateOptions(
        pluginConfig.stylelint.lintCommand
      );
      const baseConfig = {
        cwd: root,
        ...translatedOptions
      };
      const logLevel = (() => {
        var _a2;
        if (typeof pluginConfig.stylelint !== "object") return void 0;
        const userLogLevel = (_a2 = pluginConfig.stylelint.dev) == null ? void 0 : _a2.logLevel;
        if (!userLogLevel) return void 0;
        const map = {
          error: DiagnosticLevel.Error,
          warning: DiagnosticLevel.Warning
        };
        return userLogLevel.map((l) => map[l]);
      })();
      const dispatchDiagnostics = () => {
        var _a2;
        const diagnostics2 = filterLogLevel(manager.getDiagnostics(), logLevel);
        if (terminal) {
          for (const d of diagnostics2) {
            consoleLog(
              diagnosticToTerminalLog(d, "Stylelint"),
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
            composeCheckerSummary("Stylelint", errorCount, warningCount),
            errorCount ? "error" : warningCount ? "warn" : "info"
          );
        }
        if (overlay) {
          (_a2 = parentPort) == null ? void 0 : _a2.postMessage({
            type: ACTION_TYPES.overlayError,
            payload: toClientPayload(
              "stylelint",
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
          const { results: diagnosticsOfChangedFile } = await stylelint.lint({
            ...baseConfig,
            files: filePath
          });
          const newDiagnostics = diagnosticsOfChangedFile.flatMap(
            (d) => normalizeStylelintDiagnostic(d)
          );
          manager.updateByFileId(absPath, newDiagnostics);
        }
        dispatchDiagnostics();
      };
      const { results: diagnostics } = await stylelint.lint({
        ...baseConfig,
        ...(_a = pluginConfig.stylelint.dev) == null ? void 0 : _a.overrideConfig
      });
      manager.initWith(
        diagnostics.flatMap((p) => normalizeStylelintDiagnostic(p))
      );
      dispatchDiagnostics();
      let watchTarget = root;
      if (pluginConfig.stylelint.watchPath) {
        if (Array.isArray(pluginConfig.stylelint.watchPath)) {
          watchTarget = pluginConfig.stylelint.watchPath.map(
            (p) => path.resolve(root, p)
          );
        } else {
          watchTarget = path.resolve(root, pluginConfig.stylelint.watchPath);
        }
      }
      const watcher = chokidar.watch(watchTarget, {
        cwd: root,
        ignored: createIgnore(root, translatedOptions.files)
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
class StylelintChecker extends Checker {
  constructor() {
    super({
      name: "stylelint",
      absFilePath: __filename,
      build: {
        buildBin: (pluginConfig) => {
          if (pluginConfig.stylelint) {
            const { lintCommand } = pluginConfig.stylelint;
            return ["stylelint", lintCommand.split(" ").slice(1)];
          }
          return ["stylelint", [""]];
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
const stylelintChecker = new StylelintChecker();
stylelintChecker.prepare();
stylelintChecker.init();
export {
  StylelintChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import { Checker } from "../../Checker.js";
import {
  composeCheckerSummary,
  consoleLog,
  diagnosticToConsoleLevel,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  toClientPayload
} from "../../logger.js";
import { ACTION_TYPES } from "../../types.js";
import { diagnostics } from "./diagnostics.js";
const __filename = fileURLToPath(import.meta.url);
let createServeAndBuild;
const createDiagnostic = (pluginConfig) => {
  let overlay = true;
  let terminal = true;
  let command;
  return {
    config: ({ enableOverlay, enableTerminal, env }) => {
      overlay = enableOverlay;
      terminal = enableTerminal;
      command = env.command;
    },
    async configureServer({ root }) {
      const workDir = root;
      const onDispatchDiagnosticsSummary = (errorCount, warningCount) => {
        if (!terminal) return;
        consoleLog(
          composeCheckerSummary("VLS", errorCount, warningCount),
          errorCount ? "error" : warningCount ? "warn" : "info"
        );
      };
      const onDispatchDiagnostics = (normalized) => {
        var _a;
        if (overlay && command === "serve") {
          (_a = parentPort) == null ? void 0 : _a.postMessage({
            type: ACTION_TYPES.overlayError,
            payload: toClientPayload(
              "vls",
              diagnosticToRuntimeError(normalized)
            )
          });
        }
        if (terminal) {
          for (const d of normalized) {
            consoleLog(
              diagnosticToTerminalLog(d, "VLS"),
              diagnosticToConsoleLevel(d)
            );
          }
        }
      };
      const vlsConfig = pluginConfig == null ? void 0 : pluginConfig.vls;
      await diagnostics(workDir, "WARN", {
        onDispatchDiagnostics,
        onDispatchDiagnosticsSummary,
        watch: true,
        verbose: false,
        config: typeof vlsConfig === "object" ? vlsConfig : null
      });
    }
  };
};
class VlsChecker extends Checker {
  constructor() {
    super({
      name: "vls",
      absFilePath: __filename,
      build: {
        buildBin: (config) => {
          if (typeof config.vls === "object") {
            return [
              "vti",
              [
                "diagnostics",
                // Escape quotes so that the system shell doesn't strip them out:
                `"${JSON.stringify(config.vls).replace(/[\\"]/g, "\\$&")}"`
              ]
            ];
          }
          return ["vti", ["diagnostics"]];
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
const vlsChecker = new VlsChecker();
vlsChecker.prepare();
vlsChecker.init();
export {
  VlsChecker,
  createDiagnostic,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
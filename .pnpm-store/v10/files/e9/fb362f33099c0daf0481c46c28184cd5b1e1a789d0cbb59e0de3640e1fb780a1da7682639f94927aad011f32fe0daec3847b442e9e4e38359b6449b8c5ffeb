import { createRequire } from "node:module";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import invariant from "tiny-invariant";
import { Checker } from "../../Checker.js";
import {
  consoleLog,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  ensureCall,
  normalizeVueTscDiagnostic,
  toClientPayload,
  wrapCheckerSummary
} from "../../logger.js";
import {
  ACTION_TYPES
} from "../../types.js";
import { prepareVueTsc } from "./prepareVueTsc.js";
const _require = createRequire(import.meta.url);
const __filename = fileURLToPath(import.meta.url);
let createServeAndBuild;
const createDiagnostic = (pluginConfig) => {
  let overlay = true;
  let terminal = true;
  let currDiagnostics = [];
  return {
    config: ({ enableOverlay, enableTerminal }) => {
      overlay = enableOverlay;
      terminal = enableTerminal;
    },
    async configureServer({ root }) {
      invariant(pluginConfig.vueTsc, "config.vueTsc should be `false`");
      const { targetTsDir } = await prepareVueTsc();
      const vueTs = _require(path.resolve(targetTsDir, "lib/typescript.js"));
      const finalConfig = pluginConfig.vueTsc === true ? { root, tsconfigPath: "tsconfig.json" } : {
        root: pluginConfig.vueTsc.root ?? root,
        tsconfigPath: pluginConfig.vueTsc.tsconfigPath ?? "tsconfig.json"
      };
      const configFile = vueTs.findConfigFile(
        finalConfig.root,
        vueTs.sys.fileExists,
        finalConfig.tsconfigPath
      );
      if (configFile === void 0) {
        throw Error(
          `Failed to find a valid tsconfig.json: ${finalConfig.tsconfigPath} at ${finalConfig.root} is not a valid tsconfig`
        );
      }
      let logChunk = "";
      let prevLogChunk = "";
      const reportDiagnostic = (diagnostic) => {
        const normalizedDiagnostic = normalizeVueTscDiagnostic(diagnostic);
        if (normalizedDiagnostic === null) {
          return;
        }
        currDiagnostics.push(diagnosticToRuntimeError(normalizedDiagnostic));
        logChunk += os.EOL + diagnosticToTerminalLog(normalizedDiagnostic, "vue-tsc");
      };
      const reportWatchStatusChanged = (diagnostic, _newLine, _options, errorCount) => {
        var _a;
        if (diagnostic.code === 6031) return;
        switch (diagnostic.code) {
          case 6031:
          case 6032:
            logChunk = "";
            currDiagnostics = [];
            return;
          case 6193:
          // 1 Error
          case 6194:
            if (overlay) {
              (_a = parentPort) == null ? void 0 : _a.postMessage({
                type: ACTION_TYPES.overlayError,
                payload: toClientPayload("vue-tsc", currDiagnostics)
              });
            }
        }
        ensureCall(() => {
          if (errorCount === 0) {
            logChunk = "";
          }
          if (terminal) {
            logChunk = logChunk + os.EOL + wrapCheckerSummary("vue-tsc", diagnostic.messageText.toString());
            if (logChunk === prevLogChunk) {
              return;
            }
            prevLogChunk = logChunk;
            consoleLog(logChunk, errorCount ? "error" : "info");
          }
        });
      };
      const createProgram = vueTs.createEmitAndSemanticDiagnosticsBuilderProgram;
      if (typeof pluginConfig.vueTsc === "object" && pluginConfig.vueTsc.buildMode) {
        const host = vueTs.createSolutionBuilderWithWatchHost(
          vueTs.sys,
          createProgram,
          reportDiagnostic,
          void 0,
          reportWatchStatusChanged
        );
        vueTs.createSolutionBuilderWithWatch(host, [configFile], {}).build();
      } else {
        const host = vueTs.createWatchCompilerHost(
          configFile,
          { noEmit: true },
          vueTs.sys,
          createProgram,
          reportDiagnostic,
          reportWatchStatusChanged
        );
        vueTs.createWatchProgram(host);
      }
    }
  };
};
class VueTscChecker extends Checker {
  constructor() {
    super({
      name: "vueTsc",
      absFilePath: __filename,
      build: {
        buildBin: (config) => {
          if (typeof config.vueTsc === "object") {
            const { root = "", tsconfigPath = "", buildMode } = config.vueTsc;
            const args = [buildMode ? "-b" : "--noEmit"];
            let projectPath = "";
            if (root || tsconfigPath) {
              projectPath = root ? path.join(root, tsconfigPath) : tsconfigPath;
            }
            if (projectPath) {
              if (buildMode) {
                args.push(projectPath);
              } else {
                args.push("-p", projectPath);
              }
            }
            return ["vue-tsc", args];
          }
          return ["vue-tsc", ["--noEmit"]];
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
const tscChecker = new VueTscChecker();
tscChecker.prepare();
tscChecker.init();
export {
  VueTscChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
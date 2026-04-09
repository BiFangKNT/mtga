import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import colors from "picocolors";
import invariant from "tiny-invariant";
import { Checker } from "../../Checker.js";
import {
  consoleLog,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  ensureCall,
  normalizeTsDiagnostic,
  toClientPayload,
  wrapCheckerSummary
} from "../../logger.js";
import {
  ACTION_TYPES
} from "../../types.js";
const __filename = fileURLToPath(import.meta.url);
let createServeAndBuild;
const createDiagnostic = (pluginConfig) => {
  let overlay = true;
  let terminal = true;
  let currDiagnostics = [];
  return {
    config: async ({ enableOverlay, enableTerminal }) => {
      overlay = enableOverlay;
      terminal = enableTerminal;
    },
    async configureServer({ root }) {
      invariant(pluginConfig.typescript, "config.typescript should be `false`");
      const finalConfig = pluginConfig.typescript === true ? {
        root,
        tsconfigPath: "tsconfig.json",
        typescriptPath: "typescript"
      } : {
        root: pluginConfig.typescript.root ?? root,
        tsconfigPath: pluginConfig.typescript.tsconfigPath ?? "tsconfig.json",
        typescriptPath: pluginConfig.typescript.typescriptPath ?? "typescript"
      };
      let configFile;
      const ts = await import(finalConfig.typescriptPath).then((r) => r.default || r);
      configFile = ts.findConfigFile(
        finalConfig.root,
        ts.sys.fileExists,
        finalConfig.tsconfigPath
      );
      if (configFile === void 0) {
        throw Error(
          `Failed to find a valid tsconfig.json: ${finalConfig.tsconfigPath} at ${finalConfig.root} is not a valid tsconfig`
        );
      }
      let logChunk = "";
      const reportDiagnostic = (diagnostic) => {
        const normalizedDiagnostic = normalizeTsDiagnostic(diagnostic);
        if (normalizedDiagnostic === null) {
          return;
        }
        currDiagnostics.push(diagnosticToRuntimeError(normalizedDiagnostic));
        logChunk += os.EOL + diagnosticToTerminalLog(normalizedDiagnostic, "TypeScript");
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
                payload: toClientPayload("typescript", currDiagnostics)
              });
            }
        }
        ensureCall(() => {
          if (errorCount === 0) {
            logChunk = "";
          }
          if (terminal) {
            const color = errorCount && errorCount > 0 ? "red" : "green";
            consoleLog(
              colors[color](
                logChunk + os.EOL + wrapCheckerSummary(
                  "TypeScript",
                  diagnostic.messageText.toString()
                )
              ),
              errorCount ? "error" : "info"
            );
          }
        });
      };
      const createProgram = ts.createEmitAndSemanticDiagnosticsBuilderProgram;
      if (typeof pluginConfig.typescript === "object" && pluginConfig.typescript.buildMode) {
        const host = ts.createSolutionBuilderWithWatchHost(
          ts.sys,
          createProgram,
          reportDiagnostic,
          void 0,
          reportWatchStatusChanged
        );
        ts.createSolutionBuilderWithWatch(host, [configFile], {}).build();
      } else {
        const host = ts.createWatchCompilerHost(
          configFile,
          { noEmit: true },
          ts.sys,
          createProgram,
          reportDiagnostic,
          reportWatchStatusChanged
        );
        ts.createWatchProgram(host);
      }
    }
  };
};
class TscChecker extends Checker {
  constructor() {
    super({
      name: "typescript",
      absFilePath: __filename,
      build: {
        buildBin: (config) => {
          if (typeof config.typescript === "object") {
            const {
              root = "",
              tsconfigPath = "",
              buildMode
            } = config.typescript;
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
            return ["tsc", args];
          }
          return ["tsc", ["--noEmit"]];
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
const tscChecker = new TscChecker();
tscChecker.prepare();
tscChecker.init();
export {
  TscChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
import Module from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { parentPort } from "node:worker_threads";
import chokidar from "chokidar";
import { ESLint } from "eslint";
import invariant from "tiny-invariant";
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
  normalizeEslintDiagnostic,
  toClientPayload
} from "../../logger.js";
import { ACTION_TYPES, DiagnosticLevel } from "../../types.js";
import { translateOptions } from "./cli.js";
import { options as optionator } from "./options.js";
const __filename = fileURLToPath(import.meta.url);
const require2 = Module.createRequire(import.meta.url);
const manager = new FileDiagnosticManager();
let createServeAndBuild;
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
      if (!pluginConfig.eslint) return;
      const options = optionator.parse(pluginConfig.eslint.lintCommand);
      invariant(
        !options.fix,
        "Using `--fix` in `config.eslint.lintCommand` is not allowed in vite-plugin-checker, you could using `--fix` with editor."
      );
      const translatedOptions = translateOptions(options);
      const logLevel = (() => {
        var _a2;
        if (typeof pluginConfig.eslint !== "object") return void 0;
        const userLogLevel = (_a2 = pluginConfig.eslint.dev) == null ? void 0 : _a2.logLevel;
        if (!userLogLevel) return void 0;
        const map = {
          error: DiagnosticLevel.Error,
          warning: DiagnosticLevel.Warning
        };
        return userLogLevel.map((l) => map[l]);
      })();
      const eslintOptions = {
        cwd: root,
        ...translatedOptions,
        ...(_a = pluginConfig.eslint.dev) == null ? void 0 : _a.overrideConfig
      };
      let eslint;
      if (pluginConfig.eslint.useFlatConfig) {
        const {
          FlatESLint,
          shouldUseFlatConfig
        } = require2("eslint/use-at-your-own-risk");
        if (shouldUseFlatConfig == null ? void 0 : shouldUseFlatConfig()) {
          eslint = new FlatESLint({
            cwd: root
          });
        } else {
          throw Error(
            "Please upgrade your eslint to latest version to use `useFlatConfig` option."
          );
        }
      } else {
        eslint = new ESLint(eslintOptions);
      }
      const dispatchDiagnostics = () => {
        var _a2;
        const diagnostics2 = filterLogLevel(manager.getDiagnostics(), logLevel);
        if (terminal) {
          for (const d of diagnostics2) {
            consoleLog(
              diagnosticToTerminalLog(d, "ESLint"),
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
            composeCheckerSummary("ESLint", errorCount, warningCount),
            errorCount ? "error" : warningCount ? "warn" : "info"
          );
        }
        if (overlay) {
          (_a2 = parentPort) == null ? void 0 : _a2.postMessage({
            type: ACTION_TYPES.overlayError,
            payload: toClientPayload(
              "eslint",
              diagnostics2.map((d) => diagnosticToRuntimeError(d))
            )
          });
        }
      };
      const handleFileChange = async (filePath, type) => {
        const extension = path.extname(filePath);
        const { extensions } = eslintOptions;
        const hasExtensionsConfig = Array.isArray(extensions);
        if (hasExtensionsConfig && !extensions.includes(extension)) return;
        const isChangedFileIgnored = await eslint.isPathIgnored(filePath);
        if (isChangedFileIgnored) return;
        const absPath = path.resolve(root, filePath);
        if (type === "unlink") {
          manager.updateByFileId(absPath, []);
        } else if (type === "change") {
          const diagnosticsOfChangedFile = await eslint.lintFiles(filePath);
          const newDiagnostics = diagnosticsOfChangedFile.flatMap(
            (d) => normalizeEslintDiagnostic(d)
          );
          manager.updateByFileId(absPath, newDiagnostics);
        }
        dispatchDiagnostics();
      };
      const files = options._.slice(1);
      const diagnostics = await eslint.lintFiles(files);
      manager.initWith(diagnostics.flatMap((p) => normalizeEslintDiagnostic(p)));
      dispatchDiagnostics();
      let watchTarget = root;
      if (pluginConfig.eslint.watchPath) {
        if (Array.isArray(pluginConfig.eslint.watchPath)) {
          watchTarget = pluginConfig.eslint.watchPath.map(
            (p) => path.resolve(root, p)
          );
        } else {
          watchTarget = path.resolve(root, pluginConfig.eslint.watchPath);
        }
      }
      const watcher = chokidar.watch(watchTarget, {
        cwd: root,
        ignored: createIgnore(root, files)
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
class EslintChecker extends Checker {
  constructor() {
    super({
      name: "eslint",
      absFilePath: __filename,
      build: {
        buildBin: (pluginConfig) => {
          if (pluginConfig.eslint) {
            const { lintCommand } = pluginConfig.eslint;
            return ["eslint", lintCommand.split(" ").slice(1)];
          }
          return ["eslint", [""]];
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
const eslintChecker = new EslintChecker();
eslintChecker.prepare();
eslintChecker.init();
export {
  EslintChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
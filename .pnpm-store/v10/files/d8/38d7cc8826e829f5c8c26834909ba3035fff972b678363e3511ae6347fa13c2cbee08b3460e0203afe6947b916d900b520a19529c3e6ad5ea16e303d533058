import { parentPort } from "node:worker_threads";
import { FileDiagnosticManager } from "../../FileDiagnosticManager.js";
import {
  composeCheckerSummary,
  consoleLog,
  diagnosticToConsoleLevel,
  diagnosticToRuntimeError,
  diagnosticToTerminalLog,
  toClientPayload
} from "../../logger.js";
import {
  ACTION_TYPES,
  DiagnosticLevel
} from "../../types.js";
import { resolveOptions } from "./options.js";
import { setupDevServer } from "./server.js";
const createDiagnostic = (pluginConfig) => {
  const manager = new FileDiagnosticManager();
  const oxlintConfig = pluginConfig.oxlint;
  const displayTargets = /* @__PURE__ */ new Set();
  return {
    config: async ({ enableOverlay, enableTerminal }) => {
      displayTargets.clear();
      if (enableOverlay) displayTargets.add("overlay");
      if (enableTerminal) displayTargets.add("terminal");
    },
    async configureServer({ root }) {
      if (!oxlintConfig) return;
      const options = resolveOptions(root, oxlintConfig);
      await setupDevServer(root, options, manager, displayTargets);
    }
  };
};
function dispatchDiagnostics(diagnostics, targets) {
  if (targets.size === 0) return;
  if (targets.has("terminal")) {
    dispatchTerminalDiagnostics(diagnostics);
  }
  if (targets.has("overlay")) {
    dispatchOverlayDiagnostics(diagnostics);
  }
}
function dispatchTerminalDiagnostics(diagnostics) {
  for (const d of diagnostics) {
    consoleLog(
      diagnosticToTerminalLog(d, "oxlint"),
      diagnosticToConsoleLevel(d)
    );
  }
  const errorCount = diagnostics.filter(
    (d) => d.level === DiagnosticLevel.Error
  ).length;
  const warningCount = diagnostics.filter(
    (d) => d.level === DiagnosticLevel.Warning
  ).length;
  consoleLog(
    composeCheckerSummary("oxlint", errorCount, warningCount),
    errorCount ? "error" : warningCount ? "warn" : "info"
  );
}
function dispatchOverlayDiagnostics(diagnostics) {
  var _a;
  (_a = parentPort) == null ? void 0 : _a.postMessage({
    type: ACTION_TYPES.overlayError,
    payload: toClientPayload(
      "oxlint",
      diagnostics.map((d) => diagnosticToRuntimeError(d))
    )
  });
}
export {
  createDiagnostic,
  dispatchDiagnostics
};
//# sourceMappingURL=diagnostics.js.map
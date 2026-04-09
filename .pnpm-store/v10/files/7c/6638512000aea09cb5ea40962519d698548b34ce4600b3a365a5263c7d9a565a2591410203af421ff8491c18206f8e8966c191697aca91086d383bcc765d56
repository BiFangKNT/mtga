import path from "node:path";
import { DiagnosticLevel } from "../../types.js";
import { getOxlintCommand, mapSeverity } from "./cli.js";
function resolveOptions(root, config) {
  var _a, _b;
  const options = config === true ? { lintCommand: "oxlint" } : config;
  return {
    watchTarget: resolveWatchTarget(root, options.watchPath),
    logLevel: ((_b = (_a = options.dev) == null ? void 0 : _a.logLevel) == null ? void 0 : _b.map((l) => mapSeverity(l))) ?? [
      DiagnosticLevel.Warning,
      DiagnosticLevel.Error
    ],
    command: getOxlintCommand(options.lintCommand ?? "oxlint").join(" ")
  };
}
function resolveWatchTarget(root, watchPath) {
  return Array.isArray(watchPath) ? watchPath.map((p) => path.resolve(root, p)) : typeof watchPath === "string" ? path.resolve(root, watchPath) : root;
}
export {
  resolveOptions
};
//# sourceMappingURL=options.js.map
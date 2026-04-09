import { fileURLToPath } from "node:url";
import { Checker } from "../../Checker.js";
import parseArgsStringToArgv from "../stylelint/argv.js";
import { createDiagnostic } from "./diagnostics.js";
const __filename = fileURLToPath(import.meta.url);
class OxlintChecker extends Checker {
  constructor() {
    super({
      name: "oxlint",
      absFilePath: __filename,
      build: {
        buildBin: ({ oxlint: oxlint2 }) => {
          const commandStr = typeof oxlint2 === "boolean" ? "oxlint" : (oxlint2 == null ? void 0 : oxlint2.lintCommand) ?? "oxlint";
          const command = parseArgsStringToArgv(commandStr);
          return [command[0], command.slice(1)];
        }
      },
      createDiagnostic
    });
  }
}
const oxlint = new OxlintChecker();
oxlint.prepare();
oxlint.initWorkerThread();
const createServeAndBuild = oxlint.initMainThread();
export {
  OxlintChecker,
  createServeAndBuild
};
//# sourceMappingURL=main.js.map
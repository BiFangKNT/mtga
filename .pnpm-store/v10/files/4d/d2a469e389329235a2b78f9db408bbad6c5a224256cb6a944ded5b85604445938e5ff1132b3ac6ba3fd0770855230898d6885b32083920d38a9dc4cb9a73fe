import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { Duplex } from "node:stream";
import chokidar from "chokidar";
import colors from "picocolors";
import { globSync } from "tinyglobby";
import { VLS } from "vls";
import {
  createConnection,
  createProtocolConnection,
  DiagnosticSeverity,
  DidChangeTextDocumentNotification,
  DidChangeWatchedFilesNotification,
  DidOpenTextDocumentNotification,
  InitializeRequest,
  StreamMessageReader,
  StreamMessageWriter
} from "vscode-languageserver/node.js";
import { URI } from "vscode-uri";
import { FileDiagnosticManager } from "../../FileDiagnosticManager.js";
import {
  diagnosticToTerminalLog,
  normalizeLspDiagnostic,
  normalizePublishDiagnosticParams
} from "../../logger.js";
import { getInitParams } from "./initParams.js";
var DOC_VERSION = /* @__PURE__ */ ((DOC_VERSION2) => {
  DOC_VERSION2[DOC_VERSION2["init"] = -1] = "init";
  return DOC_VERSION2;
})(DOC_VERSION || {});
const logLevels = ["ERROR", "WARN", "INFO", "HINT"];
let disposeSuppressConsole;
let initialVueFilesCount = 0;
let initialVueFilesTick = 0;
const fileDiagnosticManager = new FileDiagnosticManager();
const logLevel2Severity = {
  ERROR: DiagnosticSeverity.Error,
  WARN: DiagnosticSeverity.Warning,
  INFO: DiagnosticSeverity.Information,
  HINT: DiagnosticSeverity.Hint
};
async function diagnostics(workspace, logLevel, options = { watch: false, verbose: false, config: null }) {
  var _a;
  if (options.verbose) {
    console.log("====================================");
    console.log("Getting Vetur diagnostics");
  }
  let workspaceUri;
  if (workspace) {
    const absPath = path.resolve(process.cwd(), workspace);
    console.log(`Loading Vetur in workspace path: ${colors.green(absPath)}`);
    workspaceUri = URI.file(absPath);
  } else {
    console.log(
      `Loading Vetur in current directory: ${colors.green(process.cwd())}`
    );
    workspaceUri = URI.file(process.cwd());
  }
  const result = await getDiagnostics(
    workspaceUri,
    logLevel2Severity[logLevel],
    options
  );
  if (options.verbose) {
    console.log("====================================");
  }
  if (!options.watch && typeof result === "object" && result !== null) {
    const { initialErrorCount, initialWarningCount } = result;
    (_a = options == null ? void 0 : options.onDispatchDiagnosticsSummary) == null ? void 0 : _a.call(
      options,
      initialErrorCount,
      initialWarningCount
    );
    process.exit(initialErrorCount > 0 ? 1 : 0);
  }
}
class NullLogger {
  error(_message) {
  }
  warn(_message) {
  }
  info(_message) {
  }
  log(_message) {
  }
}
class TestStream extends Duplex {
  _write(chunk, _encoding, done) {
    this.emit("data", chunk);
    done();
  }
  _read(_size) {
  }
}
function suppressConsole() {
  let disposed = false;
  const rawConsoleLog = console.log;
  console.log = () => {
  };
  return () => {
    if (disposed) return;
    disposed = true;
    console.log = rawConsoleLog;
  };
}
async function prepareClientConnection(workspaceUri, severity, options) {
  const up = new TestStream();
  const down = new TestStream();
  const logger = new NullLogger();
  const clientConnection = createProtocolConnection(
    new StreamMessageReader(down),
    new StreamMessageWriter(up),
    logger
  );
  const serverConnection = createConnection(
    new StreamMessageReader(up),
    new StreamMessageWriter(down)
  );
  serverConnection.sendDiagnostics = async (publishDiagnostics) => {
    var _a, _b;
    disposeSuppressConsole == null ? void 0 : disposeSuppressConsole();
    if (publishDiagnostics.version === -1 /* init */) {
      return;
    }
    const absFilePath = URI.parse(publishDiagnostics.uri).fsPath;
    publishDiagnostics.diagnostics = filterDiagnostics(
      publishDiagnostics.diagnostics,
      severity
    );
    const nextDiagnosticInFile = await normalizePublishDiagnosticParams(publishDiagnostics);
    fileDiagnosticManager.updateByFileId(absFilePath, nextDiagnosticInFile);
    const normalized = fileDiagnosticManager.getDiagnostics();
    const errorCount = normalized.filter(
      (d) => d.level === DiagnosticSeverity.Error
    ).length;
    const warningCount = normalized.filter(
      (d) => d.level === DiagnosticSeverity.Warning
    ).length;
    initialVueFilesTick++;
    if (initialVueFilesTick >= initialVueFilesCount) {
      (_a = options.onDispatchDiagnostics) == null ? void 0 : _a.call(options, normalized);
      (_b = options.onDispatchDiagnosticsSummary) == null ? void 0 : _b.call(options, errorCount, warningCount);
    }
  };
  const vls = new VLS(serverConnection);
  vls.validateTextDocument = async (textDocument, cancellationToken) => {
    const diagnostics2 = await vls.doValidate(textDocument, cancellationToken);
    if (diagnostics2) {
      vls.lspConnection.sendDiagnostics({
        uri: textDocument.uri,
        version: textDocument.version,
        diagnostics: diagnostics2
      });
    }
  };
  serverConnection.onInitialize(
    async (params) => {
      await vls.init(params);
      if (options.verbose) {
        console.log("Vetur initialized");
        console.log("====================================");
      }
      return {
        capabilities: vls.capabilities
      };
    }
  );
  vls.listen();
  clientConnection.listen();
  const initParams = getInitParams(workspaceUri);
  if (options.config) {
    mergeDeep(initParams.initializationOptions.config, options.config);
  }
  await clientConnection.sendRequest(InitializeRequest.type, initParams);
  return { clientConnection, serverConnection, vls, up, down, logger };
}
function extToGlobs(exts) {
  return exts.map((e) => `**/*${e}`);
}
const watchedDidChangeContent = [".vue"];
const watchedDidChangeWatchedFiles = [".js", ".ts", ".json"];
const watchedDidChangeContentGlob = extToGlobs(watchedDidChangeContent);
async function getDiagnostics(workspaceUri, severity, options) {
  const { clientConnection } = await prepareClientConnection(
    workspaceUri,
    severity,
    options
  );
  const files = globSync([...watchedDidChangeContentGlob], {
    cwd: workspaceUri.fsPath,
    ignore: ["node_modules/**"]
  });
  if (files.length === 0) {
    console.log("[VLS checker] No input files");
    return { initialWarningCount: 0, initialErrorCount: 0 };
  }
  if (options.verbose) {
    console.log("");
    console.log("Getting diagnostics from: ", files, "\n");
  }
  const absFilePaths = files.map((f) => path.resolve(workspaceUri.fsPath, f));
  disposeSuppressConsole = suppressConsole();
  initialVueFilesCount = absFilePaths.length;
  let initialErrorCount = 0;
  let initialWarningCount = 0;
  await Promise.all(
    absFilePaths.map(async (absFilePath) => {
      const fileText = await fs.promises.readFile(absFilePath, "utf-8");
      clientConnection.sendNotification(DidOpenTextDocumentNotification.type, {
        textDocument: {
          languageId: "vue",
          uri: URI.file(absFilePath).toString(),
          version: -1 /* init */,
          text: fileText
        }
      });
      if (options.watch) return;
      try {
        let diagnostics2 = await clientConnection.sendRequest(
          "$/getDiagnostics",
          {
            uri: URI.file(absFilePath).toString(),
            version: -1 /* init */
          }
        );
        diagnostics2 = filterDiagnostics(diagnostics2, severity);
        let logChunk = "";
        if (diagnostics2.length > 0) {
          logChunk += os.EOL + diagnostics2.map(
            (d) => diagnosticToTerminalLog(
              normalizeLspDiagnostic({
                diagnostic: d,
                absFilePath,
                fileText
              }),
              "VLS"
            )
          ).join(os.EOL);
          for (const d of diagnostics2) {
            if (d.severity === DiagnosticSeverity.Error) {
              initialErrorCount++;
            }
            if (d.severity === DiagnosticSeverity.Warning) {
              initialWarningCount++;
            }
          }
        }
        console.log(logChunk);
        return { initialErrorCount, initialWarningCount };
      } catch (err) {
        console.error(err.stack);
        return { initialErrorCount, initialWarningCount };
      }
    })
  );
  if (!options.watch) {
    return { initialErrorCount, initialWarningCount };
  }
  await Promise.all(
    absFilePaths.map(async (absFilePath) => {
      const fileText = await fs.promises.readFile(absFilePath, "utf-8");
      clientConnection.sendNotification(DidOpenTextDocumentNotification.type, {
        textDocument: {
          languageId: "vue",
          uri: URI.file(absFilePath).toString(),
          version: -1 /* init */,
          text: fileText
        }
      });
    })
  );
  const watcher = chokidar.watch([], {
    ignored: (path2) => path2.includes("node_modules")
  });
  watcher.add(workspaceUri.fsPath);
  watcher.on("all", async (event, filePath) => {
    const extname = path.extname(filePath);
    if (!filePath.endsWith(".vue")) return;
    const fileContent = await fs.promises.readFile(filePath, "utf-8");
    clientConnection.sendNotification(DidChangeTextDocumentNotification.type, {
      textDocument: {
        uri: URI.file(filePath).toString(),
        version: Date.now()
      },
      contentChanges: [{ text: fileContent }]
    });
    if (watchedDidChangeWatchedFiles.includes(extname)) {
      clientConnection.sendNotification(
        DidChangeWatchedFilesNotification.type,
        {
          changes: [
            {
              uri: URI.file(filePath).toString(),
              type: event === "add" ? 1 : event === "unlink" ? 3 : 2
            }
          ]
        }
      );
    }
  });
  return null;
}
function isObject(item) {
  return item && typeof item === "object" && !Array.isArray(item);
}
function mergeDeep(target, source) {
  if (isObject(target) && isObject(source)) {
    for (const key in source) {
      if (isObject(source[key])) {
        if (!target[key]) Object.assign(target, { [key]: {} });
        mergeDeep(target[key], source[key]);
      } else {
        Object.assign(target, { [key]: source[key] });
      }
    }
  }
  return target;
}
function filterDiagnostics(diagnostics2, severity) {
  return diagnostics2.filter((r) => r.source !== "eslint-plugin-vue").filter((r) => r.severity && r.severity <= severity);
}
export {
  TestStream,
  diagnostics,
  logLevel2Severity,
  logLevels,
  prepareClientConnection
};
//# sourceMappingURL=diagnostics.js.map
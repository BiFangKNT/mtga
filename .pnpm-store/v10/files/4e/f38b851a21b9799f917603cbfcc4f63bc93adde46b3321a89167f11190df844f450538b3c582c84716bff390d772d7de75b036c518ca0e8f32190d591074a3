import { exec } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";
import { stripVTControlCharacters as strip } from "node:util";
import colors from "picocolors";
import { createFrame, offsetRangeToBabelLocation } from "../../codeFrame.js";
import { consoleLog } from "../../logger.js";
import { DiagnosticLevel } from "../../types.js";
import { parseArgsStringToArgv } from "../stylelint/argv.js";
const severityMap = {
  error: DiagnosticLevel.Error,
  warning: DiagnosticLevel.Warning,
  info: DiagnosticLevel.Suggestion
};
function mapSeverity(s) {
  return severityMap[s] ?? DiagnosticLevel.Error;
}
function getOxlintCommand(command) {
  const parsed = parseArgsStringToArgv(command);
  const index = parsed.findIndex((p) => p === "--format" || p === "-f");
  if (index === -1) {
    parsed.push("--format", "json");
  } else {
    consoleLog(
      colors.yellow(
        `vite-plugin-checker will force append "--format json" to the flags in dev mode, please don't use "--format" or "-f" flag in "config.oxlint.lintCommand".`
      ),
      "warn"
    );
    parsed.splice(index, 2, "--format", "json");
  }
  return parsed;
}
function runOxlint(command, cwd) {
  return new Promise((resolve, _reject) => {
    exec(
      command,
      {
        cwd,
        maxBuffer: Number.POSITIVE_INFINITY
      },
      (_error, stdout, _stderr) => {
        parseOxlintOutput(stdout, cwd).then(resolve).catch(() => resolve([]));
      }
    );
  });
}
async function parseOxlintOutput(output, cwd) {
  const parsed = safeParseOxlint(output);
  if (!parsed) return [];
  const entries = getEntries(parsed, cwd);
  if (entries.length === 0) return [];
  const files = getUniqueFiles(entries);
  const sourceCache = await readSources(files);
  return buildDiagnostics(entries, sourceCache);
}
function safeParseOxlint(output) {
  try {
    return JSON.parse(output);
  } catch {
    return null;
  }
}
function getEntries(parsed, cwd) {
  return parsed.diagnostics.flatMap(
    ({ filename, labels, code, message, severity }) => {
      const file = normalizePath(filename, cwd);
      const [label] = labels;
      if (!label) return [];
      return [
        {
          file,
          span: label.span,
          code,
          message,
          severity
        }
      ];
    }
  );
}
function getUniqueFiles(entries) {
  return [...new Set(entries.map((e) => e.file))];
}
async function readSources(files) {
  const cache = /* @__PURE__ */ new Map();
  await Promise.all(
    files.map(async (file) => {
      try {
        const source = await fs.readFile(file, "utf8");
        cache.set(file, source);
      } catch {
      }
    })
  );
  return cache;
}
function buildDiagnostics(entries, sources) {
  return entries.flatMap((entry) => {
    const source = sources.get(entry.file);
    if (!source) return [];
    const loc = offsetRangeToBabelLocation(
      source,
      entry.span.offset,
      entry.span.length
    );
    const codeFrame = createFrame(source, loc);
    return [
      {
        message: `${entry.code}: ${entry.message}`,
        conclusion: "",
        level: mapSeverity(entry.severity),
        checker: "oxlint",
        id: entry.file,
        codeFrame,
        stripedCodeFrame: codeFrame && strip(codeFrame),
        loc
      }
    ];
  });
}
function normalizePath(p, cwd) {
  let filename = p;
  if (filename) {
    filename = path.isAbsolute(filename) ? filename : path.resolve(cwd, filename);
    filename = path.normalize(filename);
  }
  return filename;
}
export {
  getOxlintCommand,
  mapSeverity,
  runOxlint
};
//# sourceMappingURL=cli.js.map
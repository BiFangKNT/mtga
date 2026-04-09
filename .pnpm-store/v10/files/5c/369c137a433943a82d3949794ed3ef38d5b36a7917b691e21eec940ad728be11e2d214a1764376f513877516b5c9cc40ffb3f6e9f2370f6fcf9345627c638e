import { TraceMap, originalPositionFor, sourceContentFor } from "@jridgewell/trace-mapping";
import { init, parse } from "es-module-lexer";
import { isAbsolute, join, relative } from "pathe";
import { createUnplugin } from "unplugin";
import { createFilter } from "unplugin-utils";

//#region src/index.ts
const PROXY_ID = "\0impound:proxy";
const PROXY_CODE = `
function createMock(name, overrides = {}) {
  const proxyFn = function () {};
  proxyFn.prototype.name = name;
  const props = {};
  const proxy = new Proxy(proxyFn, {
    get(_target, prop) {
      if (prop === "caller") return null;
      if (prop === "__createMock__") return createMock;
      if (prop === "__mock__") return true;
      if (prop in overrides) return overrides[prop];
      if (prop === "then") return (fn) => Promise.resolve(fn());
      if (prop === "catch") return (_fn) => Promise.resolve();
      if (prop === "finally") return (fn) => Promise.resolve(fn());
      return (props[prop] = props[prop] || createMock(\`\${name}.\${prop.toString()}\`));
    },
    apply(_target, _this, _args) { return createMock(\`\${name}()\`); },
    construct(_target, _args, _newT) { return createMock(\`[\${name}]\`); },
    enumerate() { return []; },
  });
  return proxy;
}
export default createMock("mock");
`.trim();
const RELATIVE_IMPORT_RE = /^\.\.?\//;
/** Convert a byte offset in source code to a 1-indexed line and 0-indexed column. */
function offsetToLineColumn(code, offset) {
	let line = 1;
	let lastNewline = -1;
	for (let i = 0; i < offset && i < code.length; i++) if (code[i] === "\n") {
		line++;
		lastNewline = i;
	}
	return {
		line,
		column: offset - lastNewline - 1
	};
}
/** Generate a code snippet with context lines, a `>` marker, and a `^` caret. */
function generateSnippet(code, line, column, context = 2) {
	const lines = code.split("\n");
	const start = Math.max(0, line - 1 - context);
	const end = Math.min(lines.length, line + context);
	const gutterWidth = String(end).length;
	const result = [];
	for (let i = start; i < end; i++) {
		const lineNum = i + 1;
		const gutter = String(lineNum).padStart(gutterWidth);
		const marker = lineNum === line ? ">" : " ";
		result.push(`${marker} ${gutter} | ${lines[i]}`);
		if (lineNum === line) result.push(`  ${" ".repeat(gutterWidth)} | ${" ".repeat(column)}^`);
	}
	return result.join("\n");
}
/** Build an import trace from entry to the importer via BFS backwards through the graph. */
function buildTrace(importer, moduleGraph, resolvedImports, entries, maxDepth, cwd) {
	const normalize = (p) => isAbsolute(p) && cwd ? relative(cwd, p) : p;
	const visited = /* @__PURE__ */ new Set();
	const queue = [[importer, [importer]]];
	visited.add(importer);
	const isEntry = (id) => entries.has(id) || entries.has(normalize(id));
	let bestPath = [importer];
	while (queue.length > 0) {
		const [current, path] = queue.shift();
		if (path.length > maxDepth) continue;
		if (isEntry(current)) {
			bestPath = path;
			break;
		}
		const normalizedCurrent = normalize(current);
		for (const [moduleId] of moduleGraph) {
			if (visited.has(moduleId)) continue;
			const resolvedForModule = resolvedImports.get(moduleId);
			if (resolvedForModule) {
				for (const [, resolvedId] of resolvedForModule) if (resolvedId === current || resolvedId === normalizedCurrent) {
					visited.add(moduleId);
					const newPath = [...path, moduleId];
					if (isEntry(moduleId)) {
						bestPath = newPath;
						queue.length = 0;
						break;
					}
					queue.push([moduleId, newPath]);
					break;
				}
			}
		}
	}
	bestPath.reverse();
	const trace = [];
	for (let i = 0; i < bestPath.length; i++) {
		const file = bestPath[i];
		const step = { file };
		if (i === 0 && entries.has(file)) {}
		if (i < bestPath.length - 1) {
			const nextFile = bestPath[i + 1];
			/* v8 ignore start -- BFS only builds paths through nodes with resolvedImports, so this is always defined */
			const resolvedForFile = resolvedImports.get(file);
			if (!resolvedForFile) continue;
			/* v8 ignore stop */
			for (const [specifier, resolvedId] of resolvedForFile) if (resolvedId === nextFile) {
				step.import = specifier;
				const loc = moduleGraph.get(file)?.imports.get(specifier);
				if (loc) {
					step.line = loc.line;
					step.column = loc.column;
				}
				break;
			}
		}
		trace.push(step);
	}
	return trace;
}
function formatTrace(trace, cwd) {
	return trace.map((step, i) => {
		const file = cwd && isAbsolute(step.file) ? relative(cwd, step.file) : step.file;
		const loc = step.line != null ? `:${step.line}:${step.column}` : "";
		const entry = i === 0 ? " (entry)" : "";
		const imp = step.import ? ` (import "${step.import}")` : "";
		return `  ${i + 1}. ${file}${loc}${entry}${imp}`;
	}).join("\n");
}
function enrichAndReport(violation, moduleGraph, resolvedImports, entries, maxTraceDepth, cwd, warnedMessages) {
	const { id, rawId, importer, relativeImporter, options, suggestions, errorFn } = violation;
	const trace = buildTrace(importer, moduleGraph, resolvedImports, entries, maxTraceDepth, cwd);
	let snippet;
	/* v8 ignore start -- always defined: enrichAndReport is only called when the importer is in the module graph */
	const importerEntry = moduleGraph.get(importer);
	if (importerEntry) {
		/* v8 ignore stop */
		let loc = importerEntry.imports.get(rawId);
		if (!loc) {
			const importerBase = importer.split("?")[0];
			for (const [specifier, specLoc] of importerEntry.imports) {
				const resolved = RELATIVE_IMPORT_RE.test(specifier) ? join(importerBase, "..", specifier) : specifier;
				let normalizedResolved = resolved;
				if (cwd && isAbsolute(resolved)) normalizedResolved = relative(cwd, resolved);
				if (normalizedResolved === id || resolved === rawId || specifier.endsWith(id)) {
					loc = specLoc;
					break;
				}
			}
		}
		if (loc) {
			let snippetCode = importerEntry.code;
			let snippetLine = loc.line;
			let snippetColumn = loc.column;
			if (importerEntry.sourceMap) try {
				const tracer = new TraceMap(importerEntry.sourceMap);
				const original = originalPositionFor(tracer, {
					line: loc.line,
					column: loc.column
				});
				if (original.line != null) {
					snippetLine = original.line;
					/* v8 ignore start -- originalPositionFor always returns column and source when line is non-null */
					snippetColumn = original.column ?? 0;
					const originalSource = original.source != null ? sourceContentFor(tracer, original.source) : null;
					/* v8 ignore stop */
					if (originalSource != null) snippetCode = originalSource;
					else if (importerEntry.originalCode) snippetCode = importerEntry.originalCode;
				}
			} catch {}
			snippet = {
				text: generateSnippet(snippetCode, snippetLine, snippetColumn),
				line: snippetLine,
				column: snippetColumn
			};
		}
	}
	let message = violation.message;
	if (trace.length > 1) message += `\n\nTrace:\n${formatTrace(trace, cwd)}`;
	if (snippet) message += `\n\nCode:\n${snippet.text}`;
	if (suggestions?.length) message += `\n\nSuggestions:\n${suggestions.map((s) => `  - ${s}`).join("\n")}`;
	const violationInfo = {
		id,
		importer: relativeImporter,
		message,
		trace: trace.length > 1 ? trace : void 0,
		snippet
	};
	if (options.onViolation?.(violationInfo) === false) return;
	if (!warnedMessages || !warnedMessages.has(message)) {
		warnedMessages?.add(message);
		errorFn(message);
	}
}
const ImpoundPlugin = createUnplugin((globalOptions) => {
	const matchers = "matchers" in globalOptions ? globalOptions.matchers : [globalOptions];
	const traceEnabled = globalOptions.trace === true;
	const maxTraceDepth = globalOptions.maxTraceDepth ?? 20;
	const moduleGraph = /* @__PURE__ */ new Map();
	const resolvedImports = /* @__PURE__ */ new Map();
	const entries = /* @__PURE__ */ new Set();
	const pendingViolations = /* @__PURE__ */ new Map();
	const plugins = matchers.map((options) => {
		const filter = createFilter(options.include, options.exclude, { resolve: globalOptions.cwd });
		const excludeFilter = options.excludeFiles?.length ? createFilter(options.excludeFiles, void 0, { resolve: globalOptions.cwd }) : void 0;
		const warnedMessages = options.warn !== "always" ? /* @__PURE__ */ new Set() : void 0;
		return {
			name: "impound",
			enforce: "pre",
			load(id) {
				if (id === PROXY_ID) return PROXY_CODE;
			},
			resolveId(id, importer, resolveOptions) {
				if (id === PROXY_ID) return id;
				if (!importer) {
					if (traceEnabled && resolveOptions?.isEntry) entries.add(id);
					return;
				}
				if (!filter(importer)) return;
				const rawId = id;
				if (RELATIVE_IMPORT_RE.test(id)) id = join(importer, "..", id);
				if (excludeFilter?.(id)) return;
				if (isAbsolute(id) && globalOptions.cwd) id = relative(globalOptions.cwd, id);
				if (traceEnabled) {
					let importerResolved = resolvedImports.get(importer);
					if (!importerResolved) {
						importerResolved = /* @__PURE__ */ new Map();
						resolvedImports.set(importer, importerResolved);
					}
					importerResolved.set(rawId, id);
				}
				let matched = false;
				const relativeImporter = isAbsolute(importer) && globalOptions.cwd ? relative(globalOptions.cwd, importer) : importer;
				for (const [pattern, warning, suggestions] of options.patterns) {
					const usesImport = pattern instanceof RegExp ? pattern.test(id) : typeof pattern === "string" ? pattern === id : pattern(id, relativeImporter);
					if (usesImport) {
						const formattedImporter = relativeImporter.split("?")[0];
						const baseMessage = `${typeof usesImport === "string" ? usesImport : warning || "Invalid import"} [importing \`${id}\` from \`${formattedImporter}\`]`;
						if (traceEnabled) {
							const errorFn = options.error === false ? console.error : this.error.bind(this);
							const violation = {
								id,
								rawId,
								importer,
								relativeImporter,
								message: baseMessage,
								suggestions,
								options,
								errorFn,
								warnedMessages
							};
							if (moduleGraph.has(importer)) enrichAndReport(violation, moduleGraph, resolvedImports, entries, maxTraceDepth, globalOptions.cwd, warnedMessages);
							else {
								let pending = pendingViolations.get(importer);
								if (!pending) {
									pending = [];
									pendingViolations.set(importer, pending);
								}
								pending.push(violation);
							}
						} else {
							let message = baseMessage;
							if (suggestions?.length) message += `\n\nSuggestions:\n${suggestions.map((s) => `  - ${s}`).join("\n")}`;
							if (options.onViolation?.({
								id,
								importer: relativeImporter,
								message
							}) === false) continue;
							if (!warnedMessages || !warnedMessages.has(message)) {
								warnedMessages?.add(message);
								(options.error === false ? console.error : this.error.bind(this))(message);
							}
						}
						matched = true;
					}
				}
				return matched ? PROXY_ID : null;
			}
		};
	});
	if (traceEnabled) {
		async function traceTransform(code, id, getCombinedSourcemap) {
			await init;
			let importMap = /* @__PURE__ */ new Map();
			let originalCode;
			let sourceMap;
			try {
				const [imports] = parse(code, id);
				for (const imp of imports) if (imp.n) {
					const { line, column } = offsetToLineColumn(code, imp.s);
					importMap.set(imp.n, {
						line,
						column,
						statementStart: imp.ss,
						statementEnd: imp.se
					});
				}
				if (getCombinedSourcemap) try {
					const map = getCombinedSourcemap();
					if (map?.mappings) {
						sourceMap = map;
						const sourcesContent = map.sourcesContent;
						if (sourcesContent?.length && sourcesContent[0]) originalCode = sourcesContent[0];
					}
				} catch {}
			} catch {
				importMap = /* @__PURE__ */ new Map();
			}
			const graphEntry = {
				code,
				originalCode,
				sourceMap,
				imports: importMap
			};
			moduleGraph.set(id, graphEntry);
			/* v8 ignore start -- defensive normalization for framework-specific virtual module IDs */
			const bareId = id.split("?")[0];
			if (bareId !== id) moduleGraph.set(bareId, graphEntry);
			if (isAbsolute(id) && globalOptions.cwd) {
				const relId = relative(globalOptions.cwd, id);
				moduleGraph.set(relId, graphEntry);
				const relBareId = relId.split("?")[0];
				if (relBareId !== relId) moduleGraph.set(relBareId, graphEntry);
			}
			/* v8 ignore stop */
			const relativeId = isAbsolute(id) && globalOptions.cwd ? relative(globalOptions.cwd, id) : id;
			const candidateKeys = new Set([
				id,
				relativeId,
				id.split("?")[0],
				relativeId.split("?")[0]
			]);
			for (const key of candidateKeys) {
				const pending = pendingViolations.get(key);
				if (pending) {
					pendingViolations.delete(key);
					for (const violation of pending) enrichAndReport(violation, moduleGraph, resolvedImports, entries, maxTraceDepth, globalOptions.cwd, violation.warnedMessages);
				}
			}
		}
		const transformWithSourceMap = { transform(code, id) {
			return traceTransform(code, id, this.getCombinedSourcemap?.bind(this));
		} };
		const tracePlugin = {
			name: "impound:trace",
			resolveId(_id, importer, resolveOptions) {
				if (!importer && resolveOptions?.isEntry) entries.add(_id);
				return null;
			},
			transform: traceTransform,
			rollup: transformWithSourceMap,
			vite: transformWithSourceMap,
			rolldown: transformWithSourceMap
		};
		plugins.push(tracePlugin);
	}
	return plugins;
});

//#endregion
export { ImpoundPlugin };
import { c as isNodeBuiltin, d as normalizeModuleId, f as normalizeRequestId, g as toFilePath, l as isPrimitive, m as slash, n as cleanUrl, o as isBareImport, r as createImportMetaEnvProxy, s as isInternalRequest } from "./utils-ExLpYVUV.mjs";
import { a as originalPositionFor, i as TraceMap, t as extractSourceMap } from "./source-map-CysB5F9m.mjs";
import { createRequire } from "node:module";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createDebug } from "obug";
import { dirname, resolve } from "node:path";
import vm from "node:vm";

//#region src/client.ts
const { setTimeout, clearTimeout } = globalThis;
const debugExecute = createDebug("vite-node:client:execute");
const debugNative = createDebug("vite-node:client:native");
const clientStub = {
	injectQuery: (id) => id,
	createHotContext: () => {
		return {
			accept: () => {},
			prune: () => {},
			dispose: () => {},
			decline: () => {},
			invalidate: () => {},
			on: () => {},
			send: () => {}
		};
	},
	updateStyle: () => {},
	removeStyle: () => {}
};
const env = createImportMetaEnvProxy();
const DEFAULT_REQUEST_STUBS = {
	"/@vite/client": clientStub,
	"@vite/client": clientStub
};
var ModuleCacheMap = class extends Map {
	normalizePath(fsPath) {
		return normalizeModuleId(fsPath);
	}
	/**
	* Assign partial data to the map
	*/
	update(fsPath, mod) {
		fsPath = this.normalizePath(fsPath);
		if (!super.has(fsPath)) this.setByModuleId(fsPath, mod);
		else Object.assign(super.get(fsPath), mod);
		return this;
	}
	setByModuleId(modulePath, mod) {
		return super.set(modulePath, mod);
	}
	set(fsPath, mod) {
		return this.setByModuleId(this.normalizePath(fsPath), mod);
	}
	getByModuleId(modulePath) {
		if (!super.has(modulePath)) this.setByModuleId(modulePath, {});
		const mod = super.get(modulePath);
		if (!mod.imports) Object.assign(mod, {
			imports: /* @__PURE__ */ new Set(),
			importers: /* @__PURE__ */ new Set()
		});
		return mod;
	}
	get(fsPath) {
		return this.getByModuleId(this.normalizePath(fsPath));
	}
	deleteByModuleId(modulePath) {
		return super.delete(modulePath);
	}
	delete(fsPath) {
		return this.deleteByModuleId(this.normalizePath(fsPath));
	}
	invalidateModule(mod) {
		delete mod.evaluated;
		delete mod.resolving;
		delete mod.promise;
		delete mod.exports;
		mod.importers?.clear();
		mod.imports?.clear();
		return true;
	}
	/**
	* Invalidate modules that dependent on the given modules, up to the main entry
	*/
	invalidateDepTree(ids, invalidated = /* @__PURE__ */ new Set()) {
		for (const _id of ids) {
			const id = this.normalizePath(_id);
			if (invalidated.has(id)) continue;
			invalidated.add(id);
			const mod = super.get(id);
			if (mod?.importers) this.invalidateDepTree(mod.importers, invalidated);
			super.delete(id);
		}
		return invalidated;
	}
	/**
	* Invalidate dependency modules of the given modules, down to the bottom-level dependencies
	*/
	invalidateSubDepTree(ids, invalidated = /* @__PURE__ */ new Set()) {
		for (const _id of ids) {
			const id = this.normalizePath(_id);
			if (invalidated.has(id)) continue;
			invalidated.add(id);
			const subIds = Array.from(super.entries()).filter(([, mod]) => mod.importers?.has(id)).map(([key]) => key);
			if (subIds.length) this.invalidateSubDepTree(subIds, invalidated);
			super.delete(id);
		}
		return invalidated;
	}
	/**
	* Return parsed source map based on inlined source map of the module
	*/
	getSourceMap(id) {
		const cache = this.get(id);
		if (cache.map) return cache.map;
		const map = cache.code && extractSourceMap(cache.code);
		if (map) {
			cache.map = map;
			return map;
		}
		return null;
	}
};
var ViteNodeRunner = class {
	root;
	debug;
	/**
	* Holds the cache of modules
	* Keys of the map are filepaths, or plain package names
	*/
	moduleCache;
	/**
	* Tracks the stack of modules being executed for the purpose of calculating import self-time.
	*
	* Note that while in most cases, imports are a linear stack of modules,
	* this is occasionally not the case, for example when you have parallel top-level dynamic imports like so:
	*
	* ```ts
	* await Promise.all([
	*  import('./module1'),
	*  import('./module2'),
	* ]);
	* ```
	*
	* In this case, the self time will be reported incorrectly for one of the modules (could go negative).
	* As top-level awaits with dynamic imports like this are uncommon, we don't handle this case specifically.
	*/
	executionStack = [];
	performanceNow = performance.now.bind(performance);
	constructor(options) {
		this.options = options;
		this.root = options.root ?? process.cwd();
		this.moduleCache = options.moduleCache ?? new ModuleCacheMap();
		this.debug = options.debug ?? (typeof process !== "undefined" ? !!process.env.VITE_NODE_DEBUG_RUNNER : false);
	}
	async executeFile(file) {
		const url = `/@fs/${slash(resolve(file))}`;
		return await this.cachedRequest(url, url, []);
	}
	async executeId(rawId) {
		const [id, url] = await this.resolveUrl(rawId);
		return await this.cachedRequest(id, url, []);
	}
	/** @internal */
	async cachedRequest(id, fsPath, callstack) {
		const importee = callstack[callstack.length - 1];
		const mod = this.moduleCache.get(fsPath);
		const { imports, importers } = mod;
		if (importee) importers.add(importee);
		const getStack = () => `stack:\n${[...callstack, fsPath].reverse().map((p) => `  - ${p}`).join("\n")}`;
		if (callstack.includes(fsPath) || Array.from(imports.values()).some((i) => importers.has(i))) {
			if (mod.exports) return mod.exports;
		}
		let debugTimer;
		if (this.debug) debugTimer = setTimeout(() => console.warn(`[vite-node] module ${fsPath} takes over 2s to load.\n${getStack()}`), 2e3);
		try {
			if (mod.promise) return await mod.promise;
			const promise = this.directRequest(id, fsPath, callstack);
			Object.assign(mod, {
				promise,
				evaluated: false
			});
			return await promise;
		} finally {
			mod.evaluated = true;
			if (debugTimer) clearTimeout(debugTimer);
		}
	}
	shouldResolveId(id, _importee) {
		return !isInternalRequest(id) && !isNodeBuiltin(id) && !id.startsWith("data:");
	}
	async _resolveUrl(id, importer) {
		const dep = normalizeRequestId(id, this.options.base);
		if (!this.shouldResolveId(dep)) return [dep, dep];
		const { path: path$1, exists } = toFilePath(dep, this.root);
		if (!this.options.resolveId || exists) return [dep, path$1];
		const resolved = await this.options.resolveId(dep, importer);
		if (resolved?.meta?.["vite:alias"]?.noResolved) {
			const error = /* @__PURE__ */ new Error(`Cannot find module '${id}'${importer ? ` imported from '${importer}'` : ""}.

- If you rely on tsconfig.json's "paths" to resolve modules, please install "vite-tsconfig-paths" plugin to handle module resolution.
- Make sure you don't have relative aliases in your Vitest config. Use absolute paths instead. Read more: https://vitest.dev/guide/common-errors`);
			Object.defineProperty(error, "code", {
				value: "ERR_MODULE_NOT_FOUND",
				enumerable: true
			});
			Object.defineProperty(error, Symbol.for("vitest.error.not_found.data"), {
				value: {
					id: dep,
					importer
				},
				enumerable: false
			});
			throw error;
		}
		const resolvedId = resolved ? normalizeRequestId(resolved.id, this.options.base) : dep;
		return [resolvedId, resolvedId];
	}
	async resolveUrl(id, importee) {
		const resolveKey = `resolve:${id}`;
		this.moduleCache.setByModuleId(resolveKey, { resolving: true });
		try {
			return await this._resolveUrl(id, importee);
		} finally {
			this.moduleCache.deleteByModuleId(resolveKey);
		}
	}
	/** @internal */
	async dependencyRequest(id, fsPath, callstack) {
		return await this.cachedRequest(id, fsPath, callstack);
	}
	async _fetchModule(id, importer) {
		try {
			return await this.options.fetchModule(id);
		} catch (cause) {
			if (typeof cause === "object" && cause.code === "ERR_LOAD_URL" || typeof cause?.message === "string" && cause.message.includes("Failed to load url")) {
				const error = new Error(`Cannot find ${isBareImport(id) ? "package" : "module"} '${id}'${importer ? ` imported from '${importer}'` : ""}`, { cause });
				error.code = "ERR_MODULE_NOT_FOUND";
				throw error;
			}
			throw cause;
		}
	}
	/** @internal */
	async directRequest(id, fsPath, _callstack) {
		const moduleId = normalizeModuleId(fsPath);
		const callstack = [..._callstack, moduleId];
		const mod = this.moduleCache.getByModuleId(moduleId);
		const request = async (dep) => {
			const [id$1, depFsPath] = await this.resolveUrl(String(dep), fsPath);
			this.moduleCache.getByModuleId(depFsPath).importers.add(moduleId);
			mod.imports.add(depFsPath);
			return this.dependencyRequest(id$1, depFsPath, callstack);
		};
		const requestStubs = this.options.requestStubs || DEFAULT_REQUEST_STUBS;
		if (id in requestStubs) return requestStubs[id];
		let { code: transformed, externalize } = await this._fetchModule(id, callstack[callstack.length - 2]);
		if (externalize) {
			debugNative(externalize);
			const exports$1 = await this.interopedImport(externalize);
			mod.exports = exports$1;
			return exports$1;
		}
		if (transformed == null) throw new Error(`[vite-node] Failed to load "${id}" imported from ${callstack[callstack.length - 2]}`);
		const { Object: Object$1, Reflect: Reflect$1, Symbol: Symbol$1 } = this.getContextPrimitives();
		const modulePath = cleanUrl(moduleId);
		const href = pathToFileURL(modulePath).href;
		const __filename = fileURLToPath(href);
		const __dirname = dirname(__filename);
		const meta = {
			url: href,
			env,
			filename: __filename,
			dirname: __dirname
		};
		const exports = Object$1.create(null);
		Object$1.defineProperty(exports, Symbol$1.toStringTag, {
			value: "Module",
			enumerable: false,
			configurable: false
		});
		const SYMBOL_NOT_DEFINED = Symbol$1("not defined");
		let moduleExports = SYMBOL_NOT_DEFINED;
		const cjsExports = new Proxy(exports, {
			get: (target, p, receiver) => {
				if (Reflect$1.has(target, p)) return Reflect$1.get(target, p, receiver);
				return Reflect$1.get(Object$1.prototype, p, receiver);
			},
			getPrototypeOf: () => Object$1.prototype,
			set: (_, p, value) => {
				if (p === "default" && this.shouldInterop(modulePath, { default: value }) && cjsExports !== value) {
					exportAll(cjsExports, value);
					exports.default = value;
					return true;
				}
				if (!Reflect$1.has(exports, "default")) exports.default = {};
				if (moduleExports !== SYMBOL_NOT_DEFINED && isPrimitive(moduleExports)) {
					defineExport(exports, p, () => void 0);
					return true;
				}
				if (!isPrimitive(exports.default)) exports.default[p] = value;
				if (p !== "default") defineExport(exports, p, () => value);
				return true;
			}
		});
		Object$1.assign(mod, {
			code: transformed,
			exports
		});
		const moduleProxy = {
			set exports(value) {
				exportAll(cjsExports, value);
				exports.default = value;
				moduleExports = value;
			},
			get exports() {
				return cjsExports;
			}
		};
		let hotContext;
		if (this.options.createHotContext) Object$1.defineProperty(meta, "hot", {
			enumerable: true,
			get: () => {
				hotContext ||= this.options.createHotContext?.(this, moduleId);
				return hotContext;
			},
			set: (value) => {
				hotContext = value;
			}
		});
		const context = this.prepareContext({
			__vite_ssr_import__: request,
			__vite_ssr_dynamic_import__: request,
			__vite_ssr_exports__: exports,
			__vite_ssr_exportAll__: (obj) => exportAll(exports, obj),
			__vite_ssr_exportName__: (name, getter) => Object$1.defineProperty(exports, name, {
				enumerable: true,
				configurable: true,
				get: getter
			}),
			__vite_ssr_import_meta__: meta,
			require: createRequire(href),
			exports: cjsExports,
			module: moduleProxy,
			__filename,
			__dirname
		});
		debugExecute(__filename);
		if (transformed[0] === "#") transformed = transformed.replace(/^#!.*/, (s) => " ".repeat(s.length));
		await this.runModule(context, transformed);
		return exports;
	}
	getContextPrimitives() {
		return {
			Object,
			Reflect,
			Symbol
		};
	}
	async runModule(context, transformed) {
		const codeDefinition = `'use strict';async (${Object.keys(context).join(",")})=>{{`;
		const code = `${codeDefinition}${transformed}\n}}`;
		const options = {
			filename: context.__filename,
			lineOffset: 0,
			columnOffset: -codeDefinition.length
		};
		const finishModuleExecutionInfo = this.startCalculateModuleExecutionInfo(options.filename, codeDefinition.length);
		try {
			await vm.runInThisContext(code, options)(...Object.values(context));
		} finally {
			this.options.moduleExecutionInfo?.set(options.filename, finishModuleExecutionInfo());
		}
	}
	/**
	* mutate the given error to have fixed stacktraces based on source maps
	* Does the same thing as Vite's ssrFixStacktrace
	*/
	async ssrFixStacktrace(error) {
		const stack = (error.stack || "").split("\n");
		const rewrittenStack = [];
		for (const line of stack) {
			const match = line.match(/\((.*):(\d+):(\d+)\)$/);
			if (match) {
				const [, file, lineStr, columnStr] = match;
				const lineNum = Number(lineStr);
				const columnNum = Number(columnStr);
				const sourceMap = this.moduleCache.getSourceMap(file);
				if (sourceMap) {
					const originalPos = originalPositionFor(new TraceMap(sourceMap), {
						line: lineNum,
						column: columnNum
					});
					if (originalPos.source) {
						const rewrittenLine = line.replace(/\(.*:\d+:\d+\)$/, `(${file}:${originalPos.line || lineNum}:${originalPos.column || columnNum})`);
						rewrittenStack.push(rewrittenLine);
						continue;
					}
				}
			}
			rewrittenStack.push(line);
		}
		error.stack = rewrittenStack.join("\n") || error.stack;
		return error;
	}
	/**
	* Starts calculating the module execution info such as the total duration and self time spent on executing the module.
	* Returns a function to call once the module has finished executing.
	*/
	startCalculateModuleExecutionInfo(filename, startOffset) {
		const startTime = this.performanceNow();
		this.executionStack.push({
			filename,
			startTime,
			subImportTime: 0
		});
		return () => {
			const duration = this.performanceNow() - startTime;
			const currentExecution = this.executionStack.pop();
			if (currentExecution == null) throw new Error("Execution stack is empty, this should never happen");
			const selfTime = duration - currentExecution.subImportTime;
			if (this.executionStack.length > 0) this.executionStack.at(-1).subImportTime += duration;
			return {
				startOffset,
				duration,
				selfTime
			};
		};
	}
	prepareContext(context) {
		return context;
	}
	/**
	* Define if a module should be interop-ed
	* This function mostly for the ability to override by subclass
	*/
	shouldInterop(path$1, mod) {
		if (this.options.interopDefault === false) return false;
		return !path$1.endsWith(".mjs") && "default" in mod;
	}
	importExternalModule(path$1) {
		return import(
			/* @vite-ignore */
			path$1
);
	}
	/**
	* Import a module and interop it
	*/
	async interopedImport(path$1) {
		const importedModule = await this.importExternalModule(path$1);
		if (!this.shouldInterop(path$1, importedModule)) return importedModule;
		const { mod, defaultExport } = interopModule(importedModule);
		return new Proxy(mod, {
			get(mod$1, prop) {
				if (prop === "default") return defaultExport;
				return mod$1[prop] ?? defaultExport?.[prop];
			},
			has(mod$1, prop) {
				if (prop === "default") return defaultExport !== void 0;
				return prop in mod$1 || defaultExport && prop in defaultExport;
			},
			getOwnPropertyDescriptor(mod$1, prop) {
				const descriptor = Reflect.getOwnPropertyDescriptor(mod$1, prop);
				if (descriptor) return descriptor;
				if (prop === "default" && defaultExport !== void 0) return {
					value: defaultExport,
					enumerable: true,
					configurable: true
				};
			}
		});
	}
};
function interopModule(mod) {
	if (isPrimitive(mod)) return {
		mod: { default: mod },
		defaultExport: mod
	};
	let defaultExport = "default" in mod ? mod.default : mod;
	if (!isPrimitive(defaultExport) && "__esModule" in defaultExport) {
		mod = defaultExport;
		if ("default" in defaultExport) defaultExport = defaultExport.default;
	}
	return {
		mod,
		defaultExport
	};
}
function defineExport(exports, key, value) {
	Object.defineProperty(exports, key, {
		enumerable: true,
		configurable: true,
		get: value
	});
}
function exportAll(exports, sourceModule) {
	if (exports === sourceModule) return;
	if (isPrimitive(sourceModule) || Array.isArray(sourceModule) || sourceModule instanceof Promise) return;
	for (const key in sourceModule) if (key !== "default" && !(key in exports)) try {
		defineExport(exports, key, () => sourceModule[key]);
	} catch {}
}

//#endregion
export { ModuleCacheMap as n, ViteNodeRunner as r, DEFAULT_REQUEST_STUBS as t };
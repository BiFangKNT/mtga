import { performance } from "node:perf_hooks";
import { createDefu, defu } from "defu";
import { applyDefaults } from "untyped";
import { consola } from "consola";
import { AsyncLocalStorage } from "node:async_hooks";
import { getContext } from "unctx";
import satisfies from "semver/functions/satisfies.js";
import { readPackageJSON, resolvePackageJSON } from "pkg-types";
import { existsSync, lstatSync, promises, readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { basename, dirname, isAbsolute, join, normalize, parse, relative, resolve } from "pathe";
import { createJiti } from "jiti";
import { interopDefault, lookupNodeModuleSubpath, parseNodeModulePath, resolveModuleExportNames } from "mlly";
import { resolveModulePath, resolveModuleURL } from "exsolve";
import { isRelative, withTrailingSlash, withoutTrailingSlash } from "ufo";
import { read, update } from "rc9";
import semver, { gte } from "semver";
import { captureStackTrace } from "errx";
import process from "node:process";
import { glob } from "tinyglobby";
import { resolveAlias as resolveAlias$1, reverseResolveAlias } from "pathe/utils";
import ignore from "ignore";
import { loadConfig } from "c12";
import destr from "destr";
import { kebabCase, pascalCase, snakeCase } from "scule";
import { klona } from "klona";
import { hash } from "ohash";
import { isAbsolute as isAbsolute$1 } from "node:path";
//#region src/logger.ts
const logger = consola;
function useLogger(tag, options = {}) {
	return tag ? logger.create(options).withTag(tag) : logger;
}
//#endregion
//#region src/context.ts
/**
* Direct access to the Nuxt global context - see https://github.com/unjs/unctx.
* @deprecated Use `getNuxtCtx` instead
*/
const nuxtCtx = getContext("nuxt");
/** async local storage for the name of the current nuxt instance */
const asyncNuxtStorage = getContext("asyncNuxtStorage", {
	asyncContext: true,
	AsyncLocalStorage
});
/** Direct access to the Nuxt context with asyncLocalStorage - see https://github.com/unjs/unctx. */
const getNuxtCtx = () => asyncNuxtStorage.tryUse();
/**
* Get access to Nuxt instance.
*
* Throws an error if Nuxt instance is unavailable.
* @example
* ```js
* const nuxt = useNuxt()
* ```
*/
function useNuxt() {
	const instance = asyncNuxtStorage.tryUse() || nuxtCtx.tryUse();
	if (!instance) throw new Error("Nuxt instance is unavailable!");
	return instance;
}
/**
* Get access to Nuxt instance.
*
* Returns null if Nuxt instance is unavailable.
* @example
* ```js
* const nuxt = tryUseNuxt()
* if (nuxt) {
*  // Do something
* }
* ```
*/
function tryUseNuxt() {
	return asyncNuxtStorage.tryUse() || nuxtCtx.tryUse();
}
function runWithNuxtContext(nuxt, fn) {
	return asyncNuxtStorage.call(nuxt, fn);
}
//#endregion
//#region src/compatibility.ts
const SEMANTIC_VERSION_RE = /-\d+\.[0-9a-f]+/;
function normalizeSemanticVersion(version) {
	return version.replace(SEMANTIC_VERSION_RE, "");
}
const builderMap = {
	"@nuxt/rspack-builder": "rspack",
	"@nuxt/vite-builder": "vite",
	"@nuxt/webpack-builder": "webpack"
};
function checkNuxtVersion(version, nuxt = useNuxt()) {
	return satisfies(normalizeSemanticVersion(getNuxtVersion(nuxt)), version, { includePrerelease: true });
}
/**
* Check version constraints and return incompatibility issues as an array
*/
async function checkNuxtCompatibility(constraints, nuxt = useNuxt()) {
	const issues = [];
	if (constraints.nuxt) {
		const nuxtVersion = getNuxtVersion(nuxt);
		if (!checkNuxtVersion(constraints.nuxt, nuxt)) issues.push({
			name: "nuxt",
			message: `Nuxt version \`${constraints.nuxt}\` is required but currently using \`${nuxtVersion}\``
		});
	}
	if (constraints.builder && typeof nuxt.options.builder === "string") {
		const currentBuilder = builderMap[nuxt.options.builder] || nuxt.options.builder;
		if (currentBuilder in constraints.builder) {
			const constraint = constraints.builder[currentBuilder];
			if (constraint === false) issues.push({
				name: "builder",
				message: `Not compatible with \`${nuxt.options.builder}\`.`
			});
			else for (const parent of [
				nuxt.options.rootDir,
				nuxt.options.workspaceDir,
				import.meta.url
			]) {
				const builderVersion = await readPackageJSON(nuxt.options.builder, { parent }).then((r) => r.version).catch(() => void 0);
				if (builderVersion) {
					if (!satisfies(normalizeSemanticVersion(builderVersion), constraint, { includePrerelease: true })) issues.push({
						name: "builder",
						message: `Not compatible with \`${builderVersion}\` of \`${currentBuilder}\`. This module requires \`${constraint}\`.`
					});
					break;
				}
			}
		}
	}
	await nuxt.callHook("kit:compatibility", constraints, issues);
	issues.toString = () => issues.map((issue) => ` - [${issue.name}] ${issue.message}`).join("\n");
	return issues;
}
/**
* Check version constraints and throw a detailed error if has any, otherwise returns true
*/
async function assertNuxtCompatibility(constraints, nuxt = useNuxt()) {
	const issues = await checkNuxtCompatibility(constraints, nuxt);
	if (issues.length) throw new Error("Nuxt compatibility issues found:\n" + issues.toString());
	return true;
}
/**
* Check version constraints and return true if passed, otherwise returns false
*/
async function hasNuxtCompatibility(constraints, nuxt = useNuxt()) {
	return !(await checkNuxtCompatibility(constraints, nuxt)).length;
}
/**
* Check if current Nuxt instance is of specified major version
*/
function isNuxtMajorVersion(majorVersion, nuxt = useNuxt()) {
	const version = getNuxtVersion(nuxt);
	return version[0] === majorVersion.toString() && version[1] === ".";
}
/**
* @deprecated Use `isNuxtMajorVersion(2, nuxt)` instead. This may be removed in \@nuxt/kit v5 or a future major version.
*/
function isNuxt2(nuxt = useNuxt()) {
	return isNuxtMajorVersion(2, nuxt);
}
/**
* @deprecated Use `isNuxtMajorVersion(3, nuxt)` instead. This may be removed in \@nuxt/kit v5 or a future major version.
*/
function isNuxt3(nuxt = useNuxt()) {
	return isNuxtMajorVersion(3, nuxt);
}
const NUXT_VERSION_RE = /^v/g;
/**
* Get nuxt version
*/
function getNuxtVersion(nuxt = useNuxt()) {
	const rawVersion = nuxt?._version || nuxt?.version || nuxt?.constructor?.version;
	if (typeof rawVersion !== "string") throw new TypeError("Cannot determine nuxt version! Is current instance passed?");
	return rawVersion.replace(NUXT_VERSION_RE, "");
}
//#endregion
//#region src/module/define.ts
function defineNuxtModule(definition) {
	if (definition) return _defineNuxtModule(definition);
	return { with: (definition) => _defineNuxtModule(definition) };
}
function _defineNuxtModule(definition) {
	if (typeof definition === "function") return _defineNuxtModule({ setup: definition });
	const module = defu(definition, { meta: {} });
	module.meta.configKey ||= module.meta.name;
	async function getOptions(inlineOptions, nuxt = useNuxt()) {
		const nuxtConfigOptionsKey = module.meta.configKey || module.meta.name;
		let options = defu(inlineOptions, nuxtConfigOptionsKey && nuxtConfigOptionsKey in nuxt.options ? nuxt.options[nuxtConfigOptionsKey] : {}, module.defaults instanceof Function ? await module.defaults(nuxt) : module.defaults ?? {});
		if (module.schema) options = await applyDefaults(module.schema, options);
		return Promise.resolve(options);
	}
	function getModuleDependencies(nuxt = useNuxt()) {
		if (typeof module.moduleDependencies === "function") return module.moduleDependencies(nuxt);
		return module.moduleDependencies;
	}
	async function normalizedModule(inlineOptions, nuxt = tryUseNuxt()) {
		if (!nuxt) throw new TypeError(`Cannot use ${module.meta.name || "module"} outside of Nuxt context`);
		const uniqueKey = module.meta.name || module.meta.configKey;
		if (uniqueKey) {
			nuxt.options._requiredModules ||= {};
			if (nuxt.options._requiredModules[uniqueKey]) return false;
			nuxt.options._requiredModules[uniqueKey] = true;
		}
		if (module.meta.compatibility) {
			const issues = await checkNuxtCompatibility(module.meta.compatibility, nuxt);
			if (issues.length) {
				const errorMessage = `Module \`${module.meta.name}\` is disabled due to incompatibility issues:\n${issues.toString()}`;
				if (nuxt.options.experimental.enforceModuleCompatibility) {
					const error = new Error(errorMessage);
					error.name = "ModuleCompatibilityError";
					throw error;
				}
				logger.warn(errorMessage);
				return;
			}
		}
		const _options = await getOptions(inlineOptions, nuxt);
		if (module.hooks) nuxt.hooks.addHooks(module.hooks);
		const moduleName = uniqueKey || module.meta.name || "<no name>";
		nuxt._perf?.startPhase(`module:${moduleName}`);
		const start = performance.now();
		let res = {};
		try {
			res = await module.setup?.call(null, _options, nuxt) ?? {};
		} finally {
			nuxt._perf?.endPhase(`module:${moduleName}`);
		}
		const perf = performance.now() - start;
		const setupTime = Math.round(perf * 100) / 100;
		if (setupTime > 5e3 && uniqueKey !== "@nuxt/telemetry") logger.warn(`Slow module \`${moduleName}\` took \`${setupTime}ms\` to setup.`);
		else if (nuxt.options.debug && nuxt.options.debug.modules) logger.info(`Module \`${moduleName}\` took \`${setupTime}ms\` to setup.`);
		if (res === false) return false;
		return defu(res, { timings: { setup: setupTime } });
	}
	normalizedModule.getMeta = () => Promise.resolve(module.meta);
	normalizedModule.getOptions = getOptions;
	normalizedModule.getModuleDependencies = getModuleDependencies;
	normalizedModule.onInstall = module.onInstall;
	normalizedModule.onUpgrade = module.onUpgrade;
	return normalizedModule;
}
//#endregion
//#region src/internal/trace.ts
const distURL = import.meta.url.replace(/\/dist\/.*$/, "/");
function getUserCaller() {
	if (!import.meta.dev) return null;
	const { source, line, column } = captureStackTrace().find((entry) => !entry.source.startsWith(distURL)) ?? {};
	if (!source) return null;
	return {
		source: source.replace(/^file:\/\//, ""),
		line,
		column
	};
}
const warnings = /* @__PURE__ */ new Set();
function warn(warning) {
	if (!warnings.has(warning)) {
		console.warn(warning);
		warnings.add(warning);
	}
}
//#endregion
//#region src/layers.ts
const layerMap = /* @__PURE__ */ new WeakMap();
/**
* Get the resolved directory paths for all layers in a Nuxt application.
*
* Returns an array of LayerDirectories objects, ordered by layer priority:
* - The first layer is the user/project layer (highest priority)
* - Earlier layers override later layers in the array
* - Base layers appear last in the array (lowest priority)
*
* @param nuxt - The Nuxt instance to get layers from. Defaults to the current Nuxt context.
* @returns Array of LayerDirectories objects, ordered by priority (user layer first)
*/
function getLayerDirectories(nuxt = useNuxt()) {
	return nuxt.options._layers.map((layer) => {
		if (layerMap.has(layer)) return layerMap.get(layer);
		const config = withTrailingSlash$2(layer.config.rootDir) === withTrailingSlash$2(nuxt.options.rootDir) ? nuxt.options : layer.config;
		const src = withTrailingSlash$2(config.srcDir || layer.cwd);
		const root = withTrailingSlash$2(config.rootDir || layer.cwd);
		const directories = {
			root,
			shared: withTrailingSlash$2(resolve(root, resolveAlias(config.dir?.shared || "shared", nuxt.options.alias))),
			server: withTrailingSlash$2(resolve(src, resolveAlias(config.serverDir || "server", nuxt.options.alias))),
			modules: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.modules || "modules", nuxt.options.alias))),
			public: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.public || "public", nuxt.options.alias))),
			app: src,
			appLayouts: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.layouts || "layouts", nuxt.options.alias))),
			appMiddleware: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.middleware || "middleware", nuxt.options.alias))),
			appPages: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.pages || "pages", nuxt.options.alias))),
			appPlugins: withTrailingSlash$2(resolve(src, resolveAlias(config.dir?.plugins || "plugins", nuxt.options.alias)))
		};
		layerMap.set(layer, directories);
		return directories;
	});
}
function withTrailingSlash$2(dir) {
	return dir.replace(/[^/]$/, "$&/");
}
//#endregion
//#region src/ignore.ts
function createIsIgnored(nuxt = tryUseNuxt()) {
	return (pathname, stats) => isIgnored(pathname, stats, nuxt);
}
/**
* Return a filter function to filter an array of paths
*/
function isIgnored(pathname, _stats, nuxt = tryUseNuxt()) {
	if (!nuxt) return false;
	if (!nuxt._ignore) {
		nuxt._ignore = ignore(nuxt.options.ignoreOptions);
		nuxt._ignore.add(resolveIgnorePatterns());
	}
	const relativePath = relative(getLayerDirectories(nuxt).map((dirs) => dirs.root).sort((a, b) => b.length - a.length).find((cwd) => pathname.startsWith(cwd)) ?? nuxt.options.rootDir, pathname);
	if (relativePath[0] === "." && relativePath[1] === ".") return false;
	return !!(relativePath && nuxt._ignore.ignores(relativePath));
}
const NEGATION_RE = /^(!?)(.*)$/;
function resolveIgnorePatterns(relativePath) {
	const nuxt = tryUseNuxt();
	if (!nuxt) return [];
	const ignorePatterns = nuxt.options.ignore.flatMap((s) => resolveGroupSyntax(s));
	const nuxtignoreFile = join(nuxt.options.rootDir, ".nuxtignore");
	if (existsSync(nuxtignoreFile)) {
		const contents = readFileSync(nuxtignoreFile, "utf-8");
		ignorePatterns.push(...contents.trim().split(/\r?\n/));
	}
	if (relativePath) return ignorePatterns.map((p) => {
		const [_, negation = "", pattern] = p.match(NEGATION_RE) || [];
		if (pattern && pattern[0] === "*") return p;
		return negation + relative(relativePath, resolve(nuxt.options.rootDir, pattern || p));
	});
	return ignorePatterns;
}
/**
* This function turns string containing groups '**\/*.{spec,test}.{js,ts}' into an array of strings.
* For example will '**\/*.{spec,test}.{js,ts}' be resolved to:
* ['**\/*.spec.js', '**\/*.spec.ts', '**\/*.test.js', '**\/*.test.ts']
* @param group string containing the group syntax
* @returns {string[]} array of strings without the group syntax
*/
function resolveGroupSyntax(group) {
	let groups = [group];
	while (groups.some((group) => group.includes("{"))) groups = groups.flatMap((group) => {
		const [head, ...tail] = group.split("{");
		if (tail.length) {
			const [body = "", ...rest] = tail.join("{").split("}");
			return body.split(",").map((part) => `${head}${part}${rest.join("")}`);
		}
		return group;
	});
	return groups;
}
//#endregion
//#region src/utils.ts
/** @since 3.9.0 */
function toArray(value) {
	return Array.isArray(value) ? value : [value];
}
/**
* Filter out items from an array in place. This function mutates the array.
* `predicate` get through the array from the end to the start for performance.
*
* This function should be faster than `Array.prototype.filter` on large arrays.
*/
function filterInPlace(array, predicate) {
	for (let i = array.length; i--;) if (!predicate(array[i], i, array)) array.splice(i, 1);
	return array;
}
const MODE_RE = /\.(server|client)(\.\w+)*$/;
const distDirURL = new URL(".", import.meta.url);
//#endregion
//#region src/resolve.ts
/**
* Resolve the full path to a file or a directory (based on the provided type), respecting Nuxt alias and extensions options.
*
* If a path cannot be resolved, normalized input will be returned unless the `fallbackToOriginal` option is set to `true`,
* in which case the original input path will be returned.
*/
async function resolvePath(path, opts = {}) {
	const { type = "file" } = opts;
	const res = await _resolvePathGranularly(path, {
		...opts,
		type
	});
	if (res.type === type) return res.path;
	return opts.fallbackToOriginal ? path : res.path;
}
/**
* Try to resolve first existing file in paths
*/
async function findPath(paths, opts, pathType = "file") {
	for (const path of toArray(paths)) {
		const res = await _resolvePathGranularly(path, {
			...opts,
			type: opts?.type || pathType
		});
		if (!res.type || pathType && res.type !== pathType) continue;
		if (res.virtual || await existsSensitive(res.path)) return res.path;
	}
	return null;
}
/**
* Resolve path aliases respecting Nuxt alias options
*/
function resolveAlias(path, alias) {
	alias ||= tryUseNuxt()?.options.alias || {};
	return resolveAlias$1(path, alias);
}
/**
* Create a relative resolver
*/
function createResolver(base) {
	if (!base) throw new Error("`base` argument is missing for createResolver(base)!");
	base = base.toString();
	if (base.startsWith("file://")) base = dirname(fileURLToPath(base));
	return {
		resolve: (...path) => resolve(base, ...path),
		resolvePath: (path, opts) => resolvePath(path, {
			cwd: base,
			...opts
		})
	};
}
async function resolveNuxtModule(base, paths) {
	const resolved = [];
	const resolver = createResolver(base);
	for (const path of paths) {
		if (path.startsWith(base)) {
			resolved.push(path.split("/index.ts")[0]);
			continue;
		}
		const resolvedPath = await resolver.resolvePath(path);
		const dir = parseNodeModulePath(resolvedPath).dir;
		if (dir) {
			resolved.push(dir);
			continue;
		}
		const index = resolvedPath.lastIndexOf(path);
		resolved.push(index === -1 ? dirname(resolvedPath) : resolvedPath.slice(0, index + path.length));
	}
	return resolved;
}
async function _resolvePathType(path, opts = {}, skipFs = false) {
	if (opts?.virtual && existsInVFS(path)) return {
		path,
		type: "file",
		virtual: true
	};
	if (skipFs) return;
	const fd = await promises.open(path, "r").catch(() => null);
	try {
		const stats = await fd?.stat();
		if (stats) return {
			path,
			type: stats.isFile() ? "file" : "dir",
			virtual: false
		};
	} finally {
		fd?.close();
	}
}
function normalizeExtension(ext) {
	return ext.startsWith(".") ? ext : `.${ext}`;
}
async function _resolvePathGranularly(path, opts = { type: "file" }) {
	const _path = path;
	path = normalize(path);
	if (isAbsolute(path)) {
		const res = await _resolvePathType(path, opts);
		if (res && res.type === opts.type) return res;
	}
	const nuxt = tryUseNuxt();
	const cwd = opts.cwd || (nuxt ? nuxt.options.rootDir : process.cwd());
	const extensions = opts.extensions || (nuxt ? nuxt.options.extensions : [
		".ts",
		".mjs",
		".cjs",
		".json"
	]);
	const modulesDir = nuxt ? nuxt.options.modulesDir : [];
	path = resolveAlias$1(path, opts.alias ?? nuxt?.options.alias ?? {});
	if (!isAbsolute(path)) path = resolve(cwd, path);
	const res = await _resolvePathType(path, opts);
	if (res && res.type === opts.type) return res;
	if (opts.type === "file") {
		for (const ext of extensions) {
			const normalizedExt = normalizeExtension(ext);
			const extPath = await _resolvePathType(path + normalizedExt, opts);
			if (extPath && extPath.type === "file") return extPath;
			const indexPath = await _resolvePathType(join(path, "index" + normalizedExt), opts, res?.type !== "dir");
			if (indexPath && indexPath.type === "file") return indexPath;
		}
		const resolvedModulePath = resolveModulePath(_path, {
			try: true,
			suffixes: ["", "index"],
			from: [cwd, ...modulesDir].map((d) => directoryToURL(d))
		});
		if (resolvedModulePath) return {
			path: resolvedModulePath,
			type: "file",
			virtual: false
		};
	}
	return { path };
}
async function existsSensitive(path) {
	return new Set(await promises.readdir(dirname(path)).catch(() => [])).has(basename(path));
}
function existsInVFS(path, nuxt = tryUseNuxt()) {
	if (!nuxt) return false;
	if (path in nuxt.vfs) return true;
	return (nuxt.apps.default?.templates ?? nuxt.options.build.templates).some((template) => template.dst === path);
}
/**
* Resolve absolute file paths in the provided directory with respect to `.nuxtignore` and return them sorted.
* @param path path to the directory to resolve files in
* @param pattern glob pattern or an array of glob patterns to match files
* @param opts options for globbing
* @param opts.followSymbolicLinks whether to follow symbolic links, default is `true`
* @param opts.ignore additional glob patterns to ignore
* @returns sorted array of absolute file paths
*/
async function resolveFiles(path, pattern, opts = {}) {
	const files = [];
	for (const p of await glob(pattern, {
		cwd: path,
		followSymbolicLinks: opts.followSymbolicLinks ?? true,
		absolute: true,
		ignore: opts.ignore
	})) if (!isIgnored(p)) files.push(p);
	return files.sort();
}
//#endregion
//#region src/internal/esm.ts
function directoryToURL(dir) {
	return pathToFileURL(dir + "/");
}
function tryResolveModule(id, url = import.meta.url) {
	return Promise.resolve(resolveModulePath(id, {
		from: url,
		suffixes: ["", "index"],
		try: true
	}));
}
function resolveModule(id, options) {
	return resolveModulePath(id, {
		from: options?.url ?? options?.paths ?? [import.meta.url],
		extensions: options?.extensions ?? [
			".js",
			".mjs",
			".cjs",
			".ts",
			".mts",
			".cts"
		]
	});
}
async function importModule(id, opts) {
	return await import(pathToFileURL(resolveModule(id, opts)).href).then((r) => opts?.interopDefault !== false ? interopDefault(r) : r);
}
function tryImportModule(id, opts) {
	try {
		return importModule(id, opts).catch(() => void 0);
	} catch {}
}
/**
* @deprecated Please use `importModule` instead.
*/
function requireModule(id, opts) {
	const caller = getUserCaller();
	warn(`[@nuxt/kit] \`requireModule\` is deprecated${caller ? ` (used at \`${resolveAlias(caller.source)}:${caller.line}:${caller.column}\`)` : ""}. Please use \`importModule\` instead.`);
	const resolvedPath = resolveModule(id, opts);
	return createJiti(import.meta.url, { interopDefault: opts?.interopDefault !== false })(pathToFileURL(resolvedPath).href);
}
/**
* @deprecated Please use `tryImportModule` instead.
*/
function tryRequireModule(id, opts) {
	try {
		return requireModule(id, opts);
	} catch {}
}
//#endregion
//#region src/module/install.ts
const NODE_MODULES_RE = /[/\\]node_modules[/\\]/;
const ignoredConfigKeys = new Set([
	"components",
	"imports",
	"pages",
	"devtools",
	"telemetry"
]);
/**
* Installs a set of modules on a Nuxt instance.
* @internal
*/
async function installModules(modulesToInstall, resolvedModulePaths, nuxt = useNuxt()) {
	const localLayerModuleDirs = [];
	for (const l of nuxt.options._layers) {
		const srcDir = l.config.srcDir || l.cwd;
		if (!NODE_MODULES_RE.test(srcDir)) localLayerModuleDirs.push(resolve(srcDir, l.config?.dir?.modules || "modules").replace(/\/?$/, "/"));
	}
	nuxt._moduleOptionsFunctions ||= /* @__PURE__ */ new Map();
	const resolvedModules = [];
	const modulesByMetaName = /* @__PURE__ */ new Map();
	const inlineConfigKeys = new Set(await Promise.all([...modulesToInstall].map(async ([mod]) => {
		if (typeof mod === "string") return;
		const meta = await Promise.resolve(mod.getMeta?.());
		if (meta?.name) modulesByMetaName.set(meta.name, mod);
		if (meta?.configKey) {
			if (meta.configKey !== meta.name) modulesByMetaName.set(meta.configKey, mod);
			return meta.configKey;
		}
	})));
	let error;
	const dependencyMap = /* @__PURE__ */ new Map();
	for (const [key, options] of modulesToInstall) {
		const res = await loadNuxtModuleInstance(key, nuxt).catch((err) => {
			if (dependencyMap.has(key) && typeof key === "string") err.cause = `Could not resolve \`${key}\` (specified as a dependency of ${dependencyMap.get(key)}).`;
			throw err;
		});
		const dependencyMeta = await res.nuxtModule.getModuleDependencies?.(nuxt) || {};
		for (const [name, value] of Object.entries(dependencyMeta)) {
			if (!value.overrides && !value.defaults && !value.version && value.optional) continue;
			const resolvedModule = modulesByMetaName.has(name) ? resolveModuleWithOptions(modulesByMetaName.get(name), nuxt) : resolveModuleWithOptions(name, nuxt);
			const moduleToAttribute = typeof key === "string" ? `\`${key}\`` : "a module in `nuxt.options`";
			if (!resolvedModule?.module) {
				const message = `Could not resolve \`${name}\` (specified as a dependency of ${moduleToAttribute}).`;
				error = new TypeError(message);
				continue;
			}
			if (value.version) {
				const pkg = await readPackageJSON(name, { from: [res.resolvedModulePath, ...nuxt.options.modulesDir].filter(Boolean) }).catch(() => null);
				if (pkg?.version && !semver.satisfies(pkg.version, value.version, { includePrerelease: true })) {
					const message = `Module \`${name}\` version (\`${pkg.version}\`) does not satisfy \`${value.version}\` (requested by ${moduleToAttribute}).`;
					error = new TypeError(message);
				}
			}
			if (value.overrides || value.defaults) {
				const currentFns = nuxt._moduleOptionsFunctions.get(resolvedModule.module) || [];
				nuxt._moduleOptionsFunctions.set(resolvedModule.module, [...currentFns, () => ({
					defaults: value.defaults,
					overrides: value.overrides
				})]);
			}
			if (value.optional === true) continue;
			nuxt.options.typescript.hoist.push(name);
			if (resolvedModule && !modulesToInstall.has(resolvedModule.module) && (!resolvedModule.resolvedPath || !resolvedModulePaths.has(resolvedModule.resolvedPath))) {
				if (typeof resolvedModule.module === "string" && inlineConfigKeys.has(resolvedModule.module)) continue;
				modulesToInstall.set(resolvedModule.module, resolvedModule.options);
				dependencyMap.set(resolvedModule.module, moduleToAttribute);
				const path = resolvedModule.resolvedPath || resolvedModule.module;
				if (typeof path === "string") resolvedModulePaths.add(path);
			}
		}
		resolvedModules.push({
			moduleToInstall: key,
			meta: await res.nuxtModule.getMeta?.(),
			nuxtModule: res.nuxtModule,
			buildTimeModuleMeta: res.buildTimeModuleMeta,
			resolvedModulePath: res.resolvedModulePath,
			inlineOptions: options
		});
	}
	if (error) throw error;
	for (const { nuxtModule, meta = {}, moduleToInstall, buildTimeModuleMeta, resolvedModulePath, inlineOptions } of resolvedModules) {
		const configKey = meta.configKey;
		const optionsFns = new Set([
			...nuxt._moduleOptionsFunctions.get(moduleToInstall) || [],
			...meta?.name ? nuxt._moduleOptionsFunctions.get(meta.name) || [] : [],
			...configKey ? nuxt._moduleOptionsFunctions.get(configKey) || [] : []
		]);
		if (optionsFns.size > 0) {
			const overrides = [];
			const defaults = [];
			for (const fn of optionsFns) {
				const options = fn();
				overrides.push(options.overrides);
				defaults.push(options.defaults);
			}
			if (configKey) nuxt.options[configKey] = defu(...overrides, nuxt.options[configKey], ...defaults);
		}
		const isDisabled = configKey && !ignoredConfigKeys.has(configKey) && nuxt.options[configKey] === false;
		if (!isDisabled) await callLifecycleHooks(nuxtModule, meta, inlineOptions, nuxt);
		const path = typeof moduleToInstall === "string" ? moduleToInstall : void 0;
		await callModule(nuxt, nuxtModule, inlineOptions, {
			meta: defu({ disabled: isDisabled }, meta, buildTimeModuleMeta),
			nameOrPath: path,
			modulePath: resolvedModulePath || path,
			localLayerModuleDirs
		});
	}
	delete nuxt._moduleOptionsFunctions;
}
/**
* Installs a module on a Nuxt instance.
* @deprecated Use module dependencies.
*/
async function installModule(moduleToInstall, inlineOptions, nuxt = useNuxt()) {
	const { nuxtModule, buildTimeModuleMeta, resolvedModulePath } = await loadNuxtModuleInstance(moduleToInstall, nuxt);
	const localLayerModuleDirs = [];
	for (const dirs of getLayerDirectories(nuxt)) if (!NODE_MODULES_RE.test(dirs.app)) localLayerModuleDirs.push(dirs.modules);
	const meta = await nuxtModule.getMeta?.();
	let mergedOptions = inlineOptions;
	const configKey = meta?.configKey;
	if (configKey && nuxt._moduleOptionsFunctions) {
		const optionsFns = [...nuxt._moduleOptionsFunctions.get(moduleToInstall) || [], ...nuxt._moduleOptionsFunctions.get(configKey) || []];
		if (optionsFns.length > 0) {
			const overrides = [];
			const defaults = [];
			for (const fn of optionsFns) {
				const options = fn();
				overrides.push(options.overrides);
				defaults.push(options.defaults);
			}
			mergedOptions = defu(inlineOptions, ...overrides, nuxt.options[configKey], ...defaults);
			nuxt.options[configKey] = mergedOptions;
		}
	}
	const isDisabled = configKey && !ignoredConfigKeys.has(configKey) && nuxt.options[configKey] === false;
	if (!isDisabled) await callLifecycleHooks(nuxtModule, meta, mergedOptions, nuxt);
	const path = typeof moduleToInstall === "string" ? moduleToInstall : void 0;
	await callModule(nuxt, nuxtModule, mergedOptions, {
		meta: defu({ disabled: isDisabled }, meta, buildTimeModuleMeta),
		nameOrPath: path,
		modulePath: resolvedModulePath || path,
		localLayerModuleDirs
	});
}
function resolveModuleWithOptions(definition, nuxt) {
	const [module, options = {}] = Array.isArray(definition) ? definition : [definition, {}];
	if (!module) return;
	if (typeof module !== "string") return {
		module,
		options
	};
	const modAlias = resolveAlias(module, nuxt.options.alias);
	return {
		module,
		resolvedPath: resolveModulePath(modAlias, {
			try: true,
			from: nuxt.options.modulesDir.map((m) => directoryToURL(m.replace(/\/node_modules\/?$/, "/"))),
			suffixes: [
				"nuxt",
				"nuxt/index",
				"module",
				"module/index",
				"",
				"index"
			],
			extensions: [
				".js",
				".mjs",
				".cjs",
				".ts",
				".mts",
				".cts"
			]
		}) || modAlias,
		options
	};
}
async function loadNuxtModuleInstance(nuxtModule, nuxt = useNuxt()) {
	let buildTimeModuleMeta = {};
	if (typeof nuxtModule === "function") return {
		nuxtModule,
		buildTimeModuleMeta
	};
	if (typeof nuxtModule !== "string") throw new TypeError(`Nuxt module should be a function or a string to import. Received: ${nuxtModule}.`);
	const jiti = createJiti(nuxt.options.rootDir, { alias: nuxt.options.alias });
	nuxtModule = resolveAlias(nuxtModule, nuxt.options.alias);
	if (isRelative(nuxtModule)) nuxtModule = resolve(nuxt.options.rootDir, nuxtModule);
	try {
		const src = resolveModuleURL(nuxtModule, {
			from: nuxt.options.modulesDir.map((m) => directoryToURL(m.replace(/\/node_modules\/?$/, "/"))),
			suffixes: [
				"nuxt",
				"nuxt/index",
				"module",
				"module/index",
				"",
				"index"
			],
			extensions: [
				".js",
				".mjs",
				".cjs",
				".ts",
				".mts",
				".cts"
			]
		});
		const resolvedModulePath = fileURLToPath(src);
		const resolvedNuxtModule = await jiti.import(src, { default: true });
		if (typeof resolvedNuxtModule !== "function") throw new TypeError(`Nuxt module should be a function: ${nuxtModule}.`);
		const moduleMetadataPath = new URL("module.json", src);
		if (existsSync(moduleMetadataPath)) buildTimeModuleMeta = JSON.parse(await promises.readFile(moduleMetadataPath, "utf-8"));
		return {
			nuxtModule: resolvedNuxtModule,
			buildTimeModuleMeta,
			resolvedModulePath
		};
	} catch (error) {
		const code = error.code;
		if (code === "ERR_PACKAGE_PATH_NOT_EXPORTED" || code === "ERR_UNSUPPORTED_DIR_IMPORT" || code === "ENOTDIR") throw new TypeError(`Could not load \`${nuxtModule}\`. Is it installed?`);
		if (code === "MODULE_NOT_FOUND" || code === "ERR_MODULE_NOT_FOUND") {
			const module = MissingModuleMatcher.exec(error.message)?.[1];
			if (module && !module.includes(nuxtModule)) throw new TypeError(`Error while importing module \`${nuxtModule}\`: ${error}`);
		}
	}
	throw new TypeError(`Could not load \`${nuxtModule}\`. Is it installed?`);
}
function getDirectory(p) {
	try {
		return isAbsolute(p) && lstatSync(p).isFile() ? dirname(p) : p;
	} catch {}
	return p;
}
const normalizeModuleTranspilePath = (p) => {
	return getDirectory(p).split("node_modules/").pop();
};
const MissingModuleMatcher = /Cannot find module\s+['"]?([^'")\s]+)['"]?/i;
async function callLifecycleHooks(nuxtModule, meta = {}, inlineOptions, nuxt = useNuxt()) {
	if (!meta.name || !meta.version) return;
	if (!nuxtModule.onInstall && !nuxtModule.onUpgrade) return;
	const previousVersion = read({
		dir: nuxt.options.rootDir,
		name: ".nuxtrc"
	})?.setups?.[meta.name];
	try {
		if (!previousVersion) await nuxtModule.onInstall?.(nuxt);
		else if (semver.gt(meta.version, previousVersion)) await nuxtModule.onUpgrade?.(nuxt, inlineOptions, previousVersion);
		if (previousVersion !== meta.version) update({ setups: { [meta.name]: meta?.version } }, {
			dir: nuxt.options.rootDir,
			name: ".nuxtrc"
		});
	} catch (e) {
		logger.error(`Error while executing ${!previousVersion ? "install" : "upgrade"} hook for module \`${meta.name}\`: ${e}`);
	}
}
async function callModule(nuxt, nuxtModule, moduleOptions = {}, options) {
	const modulePath = options.modulePath;
	const nameOrPath = options.nameOrPath;
	const localLayerModuleDirs = options.localLayerModuleDirs;
	const fn = () => nuxt.options.experimental?.debugModuleMutation && nuxt._asyncLocalStorageModule ? nuxt._asyncLocalStorageModule.run(nuxtModule, () => nuxtModule(moduleOptions, nuxt)) : nuxtModule(moduleOptions, nuxt);
	const res = options.meta.disabled ? false : await fn();
	let entryPath;
	if (typeof modulePath === "string") {
		const parsed = parseNodeModulePath(modulePath);
		if (parsed.name) {
			const subpath = await lookupNodeModuleSubpath(modulePath) || ".";
			entryPath = join(parsed.name, subpath === "./" ? "." : subpath);
		}
		if (res !== false) {
			const moduleRoot = parsed.dir ? parsed.dir + parsed.name : await resolvePackageJSON(modulePath, { try: true }).then((r) => r ? dirname(r) : modulePath);
			nuxt.options.build.transpile.push(normalizeModuleTranspilePath(moduleRoot));
			const directory = moduleRoot.replace(/\/?$/, "/");
			if (moduleRoot !== nameOrPath && !localLayerModuleDirs.some((dir) => directory.startsWith(dir))) nuxt.options.modulesDir.push(join(moduleRoot, "node_modules"));
		}
	}
	if (nameOrPath) {
		entryPath ||= resolveAlias(nameOrPath, nuxt.options.alias);
		if (entryPath !== nameOrPath) options.meta.rawPath = nameOrPath;
	}
	nuxt.options._installedModules ||= [];
	nuxt.options._installedModules.push({
		meta: options.meta,
		module: nuxtModule,
		timings: (res || {}).timings,
		entryPath
	});
}
//#endregion
//#region src/module/compatibility.ts
function resolveNuxtModuleEntryName(m) {
	if (typeof m === "object" && !Array.isArray(m)) return m.name;
	if (Array.isArray(m)) return resolveNuxtModuleEntryName(m[0]);
	return m || false;
}
/**
* Check if a Nuxt module is installed by name.
*
* This will check both the installed modules and the modules to be installed. Note
* that it cannot detect if a module is _going to be_ installed programmatically by another module.
*/
function hasNuxtModule(moduleName, nuxt = useNuxt()) {
	return nuxt.options._installedModules.some(({ meta }) => meta.name === moduleName) || nuxt.options.modules.some((m) => moduleName === resolveNuxtModuleEntryName(m));
}
/**
* Checks if a Nuxt module is compatible with a given semver version.
*/
async function hasNuxtModuleCompatibility(module, semverVersion, nuxt = useNuxt()) {
	const version = await getNuxtModuleVersion(module, nuxt);
	if (!version) return false;
	return satisfies(normalizeSemanticVersion(version), semverVersion, { includePrerelease: true });
}
/**
* Get the version of a Nuxt module.
*
* Scans installed modules for the version, if it's not found it will attempt to load the module instance and get the version from there.
*/
async function getNuxtModuleVersion(module, nuxt = useNuxt()) {
	const moduleMeta = (typeof module === "string" ? { name: module } : await module.getMeta?.()) || {};
	if (moduleMeta.version) return moduleMeta.version;
	if (!moduleMeta.name) return false;
	for (const m of nuxt.options._installedModules) if (m.meta.name === moduleMeta.name && m.meta.version) return m.meta.version;
	if (hasNuxtModule(moduleMeta.name)) {
		const { nuxtModule, buildTimeModuleMeta } = await loadNuxtModuleInstance(moduleMeta.name, nuxt);
		return buildTimeModuleMeta.version || await nuxtModule.getMeta?.().then((r) => r.version) || false;
	}
	return false;
}
//#endregion
//#region src/loader/config.ts
const merger = createDefu((obj, key, value) => {
	if (Array.isArray(obj[key]) && Array.isArray(value)) {
		obj[key] = obj[key].concat(value);
		return true;
	}
});
async function loadNuxtConfig(opts) {
	const localLayers = (await glob("layers/*", {
		onlyDirectories: true,
		cwd: opts.cwd || process.cwd()
	})).map((d) => withTrailingSlash(d)).sort((a, b) => b.localeCompare(a));
	opts.overrides = defu(opts.overrides, { _extends: localLayers });
	const { configFile, layers = [], cwd, config: nuxtConfig, meta } = await withDefineNuxtConfig(() => loadConfig({
		name: "nuxt",
		configFile: "nuxt.config",
		rcFile: ".nuxtrc",
		extend: { extendKey: [
			"theme",
			"_extends",
			"extends"
		] },
		dotenv: true,
		globalRc: true,
		merger,
		...opts
	}));
	nuxtConfig.rootDir ||= cwd;
	nuxtConfig._nuxtConfigFile = configFile;
	nuxtConfig._nuxtConfigFiles = [configFile];
	nuxtConfig._loadOptions = opts;
	nuxtConfig.alias ||= {};
	if (meta?.name) {
		const alias = `#layers/${meta.name}`;
		nuxtConfig.alias[alias] ||= withTrailingSlash(nuxtConfig.rootDir);
	}
	const defaultBuildDir = join(nuxtConfig.rootDir, ".nuxt");
	if (!opts.overrides?._prepare && !nuxtConfig.dev && !nuxtConfig.buildDir && existsSync(defaultBuildDir)) nuxtConfig.buildDir = join(nuxtConfig.rootDir, "node_modules/.cache/nuxt/.nuxt");
	const NuxtConfigSchema = await loadNuxtSchema(nuxtConfig.rootDir || cwd || process.cwd());
	const layerSchemaKeys = [
		"future",
		"srcDir",
		"rootDir",
		"serverDir",
		"dir"
	];
	const layerSchema = Object.create(null);
	for (const key of layerSchemaKeys) if (key in NuxtConfigSchema) layerSchema[key] = NuxtConfigSchema[key];
	const _layers = [];
	const processedLayers = /* @__PURE__ */ new Set();
	const localRelativePaths = new Set(localLayers.map((layer) => withoutTrailingSlash(layer)));
	for (const layer of layers) {
		const resolvedRootDir = layer.config?.rootDir ?? layer.cwd;
		layer.config = {
			...layer.config || {},
			rootDir: resolvedRootDir
		};
		if (processedLayers.has(resolvedRootDir)) continue;
		processedLayers.add(resolvedRootDir);
		layer.config = await applyDefaults(layerSchema, layer.config);
		if (!layer.configFile || layer.configFile.endsWith(".nuxtrc")) continue;
		if (layer.cwd && cwd && localRelativePaths.has(relative(cwd, layer.cwd))) {
			layer.meta ||= {};
			layer.meta.name ||= basename(layer.cwd);
		}
		if (layer.meta?.name) {
			const alias = `#layers/${layer.meta.name}`;
			nuxtConfig.alias[alias] ||= withTrailingSlash(layer.config.rootDir || layer.cwd);
		}
		_layers.push(layer);
	}
	nuxtConfig._layers = _layers;
	if (!_layers.length) _layers.push({
		cwd,
		config: {
			rootDir: cwd,
			srcDir: cwd
		}
	});
	return await applyDefaults(NuxtConfigSchema, nuxtConfig);
}
function loadNuxtSchema(cwd) {
	const url = directoryToURL(cwd);
	const urls = [url];
	const nuxtPath = resolveModuleURL("nuxt", {
		try: true,
		from: url
	}) ?? resolveModuleURL("nuxt-nightly", {
		try: true,
		from: url
	});
	if (nuxtPath) urls.unshift(nuxtPath);
	return import(resolveModuleURL("@nuxt/schema", {
		try: true,
		from: urls
	}) ?? "@nuxt/schema").then((r) => r.NuxtConfigSchema);
}
async function withDefineNuxtConfig(fn) {
	const key = "defineNuxtConfig";
	const globalSelf = globalThis;
	if (!globalSelf[key]) {
		globalSelf[key] = (c) => c;
		globalSelf[key].count = 0;
	}
	globalSelf[key].count++;
	try {
		return await fn();
	} finally {
		globalSelf[key].count--;
		if (!globalSelf[key].count) delete globalSelf[key];
	}
}
//#endregion
//#region src/loader/schema.ts
function extendNuxtSchema(def) {
	useNuxt().hook("schema:extend", (schemas) => {
		schemas.push(typeof def === "function" ? def() : def);
	});
}
//#endregion
//#region src/loader/nuxt.ts
async function loadNuxt(opts) {
	opts.cwd = resolve(opts.cwd || opts.rootDir || ".");
	opts.overrides ||= opts.config || {};
	opts.overrides.dev = !!opts.dev;
	const resolvedPath = ["nuxt-nightly", "nuxt"].reduce((resolvedPath, pkg) => {
		const path = resolveModulePath(pkg, {
			try: true,
			from: [directoryToURL(opts.cwd)]
		});
		return path && path.length > resolvedPath.length ? path : resolvedPath;
	}, "");
	if (!resolvedPath) throw new Error(`Cannot find any nuxt version from ${opts.cwd}`);
	const { loadNuxt } = await import(pathToFileURL(resolvedPath).href).then((r) => interopDefault(r));
	return await loadNuxt(opts);
}
async function buildNuxt(nuxt) {
	const rootURL = directoryToURL(nuxt.options.rootDir);
	const { build } = await tryImportModule("nuxt-nightly", { url: rootURL }) || await importModule("nuxt", { url: rootURL });
	return runWithNuxtContext(nuxt, () => build(nuxt));
}
//#endregion
//#region src/head.ts
function setGlobalHead(head) {
	const nuxt = useNuxt();
	nuxt.options.app.head = defu(head, nuxt.options.app.head);
}
//#endregion
//#region src/imports.ts
function addImports(imports) {
	useNuxt().hook("imports:extend", (_imports) => {
		_imports.push(...toArray(imports));
	});
}
function addImportsDir(dirs, opts = {}) {
	useNuxt().hook("imports:dirs", (_dirs) => {
		for (const dir of toArray(dirs)) _dirs[opts.prepend ? "unshift" : "push"](dir);
	});
}
function addImportsSources(presets) {
	useNuxt().hook("imports:sources", (_presets) => {
		for (const preset of toArray(presets)) _presets.push(preset);
	});
}
//#endregion
//#region src/nitro.ts
const HANDLER_METHOD_RE = /\.(get|head|patch|post|put|delete|connect|options|trace)(\.\w+)*$/;
/**
* normalize handler object
*
*/
function normalizeHandlerMethod(handler) {
	const [, method = void 0] = handler.handler.match(HANDLER_METHOD_RE) || [];
	return {
		method: method?.toUpperCase(),
		...handler,
		handler: normalize(handler.handler)
	};
}
/**
* Adds a nitro server handler
*
*/
function addServerHandler(handler) {
	useNuxt().options.serverHandlers.push(normalizeHandlerMethod(handler));
}
/**
* Adds a nitro server handler for development-only
*
*/
function addDevServerHandler(handler) {
	useNuxt().options.devServerHandlers.push(handler);
}
/**
* Adds a Nitro plugin
*/
function addServerPlugin(plugin) {
	const nuxt = useNuxt();
	nuxt.options.nitro.plugins ||= [];
	nuxt.options.nitro.plugins.push(normalize(plugin));
}
/**
* Adds routes to be prerendered
*/
function addPrerenderRoutes(routes) {
	const nuxt = useNuxt();
	routes = toArray(routes).filter(Boolean);
	if (!routes.length) return;
	nuxt.hook("prerender:routes", (ctx) => {
		for (const route of routes) ctx.routes.add(route);
	});
}
/**
* Access to the Nitro instance
*
* **Note:** You can call `useNitro()` only after `ready` hook.
*
* **Note:** Changes to the Nitro instance configuration are not applied.
* @example
*
* ```ts
* nuxt.hook('ready', () => {
*   console.log(useNitro())
* })
* ```
*/
function useNitro() {
	const nuxt = useNuxt();
	if (!nuxt._nitro) throw new Error("Nitro is not initialized yet. You can call `useNitro()` only after `ready` hook.");
	return nuxt._nitro;
}
/**
* Add server imports to be auto-imported by Nitro
*/
function addServerImports(imports) {
	const nuxt = useNuxt();
	const _imports = toArray(imports);
	nuxt.hook("nitro:config", (config) => {
		config.imports ||= {};
		config.imports.imports ||= [];
		config.imports.imports.push(..._imports);
	});
}
/**
* Add directories to be scanned for auto-imports by Nitro
*/
function addServerImportsDir(dirs, opts = {}) {
	const nuxt = useNuxt();
	const _dirs = toArray(dirs);
	nuxt.hook("nitro:config", (config) => {
		config.imports ||= {};
		config.imports.dirs ||= [];
		config.imports.dirs[opts.prepend ? "unshift" : "push"](..._dirs);
	});
}
/**
* Add directories to be scanned by Nitro. It will check for subdirectories,
* which will be registered just like the `~~/server` folder is.
*/
function addServerScanDir(dirs, opts = {}) {
	useNuxt().hook("nitro:config", (config) => {
		config.scanDirs ||= [];
		for (const dir of toArray(dirs)) config.scanDirs[opts.prepend ? "unshift" : "push"](dir);
	});
}
//#endregion
//#region src/runtime-config.ts
/**
* Access 'resolved' Nuxt runtime configuration, with values updated from environment.
*
* This mirrors the runtime behavior of Nitro.
*/
function useRuntimeConfig() {
	const nuxt = useNuxt();
	return applyEnv(klona(nuxt.options.nitro.runtimeConfig), {
		prefix: "NITRO_",
		altPrefix: "NUXT_",
		envExpansion: nuxt.options.nitro.experimental?.envExpansion ?? !!process.env.NITRO_ENV_EXPANSION
	});
}
/**
* Update Nuxt runtime configuration.
*/
function updateRuntimeConfig(runtimeConfig) {
	const nuxt = useNuxt();
	Object.assign(nuxt.options.nitro.runtimeConfig, defu(runtimeConfig, nuxt.options.nitro.runtimeConfig));
	try {
		return useNitro().updateConfig({ runtimeConfig });
	} catch {}
}
function getEnv(key, opts, env = process.env) {
	const envKey = snakeCase(key).toUpperCase();
	return destr(env[opts.prefix + envKey] ?? env[opts.altPrefix + envKey]);
}
function _isObject(input) {
	return typeof input === "object" && !Array.isArray(input);
}
function applyEnv(obj, opts, parentKey = "") {
	for (const key in obj) {
		const subKey = parentKey ? `${parentKey}_${key}` : key;
		const envValue = getEnv(subKey, opts);
		if (_isObject(obj[key])) if (_isObject(envValue)) {
			obj[key] = {
				...obj[key],
				...envValue
			};
			applyEnv(obj[key], opts, subKey);
		} else if (envValue === void 0) applyEnv(obj[key], opts, subKey);
		else obj[key] = envValue ?? obj[key];
		else obj[key] = envValue ?? obj[key];
		if (opts.envExpansion && typeof obj[key] === "string") obj[key] = _expandFromEnv(obj[key]);
	}
	return obj;
}
const envExpandRx = /\{\{([^{}]*)\}\}/g;
function _expandFromEnv(value, env = process.env) {
	return value.replace(envExpandRx, (match, key) => {
		return env[key] || match;
	});
}
//#endregion
//#region src/build.ts
const extendWebpackCompatibleConfig = (builder) => (fn, options = {}) => {
	const nuxt = useNuxt();
	if (options.dev === false && nuxt.options.dev) return;
	if (options.build === false && nuxt.options.build) return;
	nuxt.hook(`${builder}:config`, async (configs) => {
		if (options.server !== false) {
			const config = configs.find((i) => i.name === "server");
			if (config) await fn(config);
		}
		if (options.client !== false) {
			const config = configs.find((i) => i.name === "client");
			if (config) await fn(config);
		}
	});
};
/**
* Extend webpack config
*
* The fallback function might be called multiple times
* when applying to both client and server builds.
*/
const extendWebpackConfig = extendWebpackCompatibleConfig("webpack");
/**
* Extend rspack config
*
* The fallback function might be called multiple times
* when applying to both client and server builds.
*/
const extendRspackConfig = extendWebpackCompatibleConfig("rspack");
/**
* Extend Vite config
*/
function extendViteConfig(fn, options = {}) {
	const nuxt = useNuxt();
	if (options.dev === false && nuxt.options.dev) return;
	if (options.build === false && nuxt.options.build) return;
	if (options.server === false || options.client === false) {
		const caller = getUserCaller();
		warn(`[@nuxt/kit] calling \`extendViteConfig\` with only server/client environment is deprecated${caller ? ` (used at \`${resolveAlias(caller.source)}:${caller.line}:${caller.column}\`)` : ""}. Nuxt 5+ will use the Vite Environment API which shares a configuration between environments. You can likely use a Vite plugin to achieve the same result.`);
	}
	return nuxt.hook("vite:extend", ({ config }) => fn(config));
}
/**
* Append webpack plugin to the config.
*/
function addWebpackPlugin(pluginOrGetter, options) {
	extendWebpackConfig(async (config) => {
		const method = options?.prepend ? "unshift" : "push";
		const plugin = typeof pluginOrGetter === "function" ? await pluginOrGetter() : pluginOrGetter;
		config.plugins ||= [];
		config.plugins[method](...toArray(plugin));
	}, options);
}
/**
* Append rspack plugin to the config.
*/
function addRspackPlugin(pluginOrGetter, options) {
	extendRspackConfig(async (config) => {
		const method = options?.prepend ? "unshift" : "push";
		const plugin = typeof pluginOrGetter === "function" ? await pluginOrGetter() : pluginOrGetter;
		config.plugins ||= [];
		config.plugins[method](...toArray(plugin));
	}, options);
}
/**
* Append Vite plugin to the config.
*/
function addVitePlugin(pluginOrGetter, options = {}) {
	const nuxt = useNuxt();
	if (options.dev === false && nuxt.options.dev) return;
	if (options.build === false && nuxt.options.build) return;
	let needsEnvInjection = false;
	nuxt.hook("vite:extend", async ({ config }) => {
		config.plugins ||= [];
		const plugin = toArray(typeof pluginOrGetter === "function" ? await pluginOrGetter() : pluginOrGetter);
		if (options.server !== false && options.client !== false) {
			const method = options?.prepend ? "unshift" : "push";
			config.plugins[method](...plugin);
			return;
		}
		if (!config.environments?.ssr || !config.environments.client) {
			needsEnvInjection = true;
			return;
		}
		const environmentName = options.server === false ? "client" : "ssr";
		const pluginName = plugin.map((p) => p.name).join("|");
		config.plugins.push({
			name: `${pluginName}:wrapper`,
			enforce: options?.prepend ? "pre" : "post",
			applyToEnvironment(environment) {
				if (environment.name === environmentName) return plugin;
			}
		});
	});
	nuxt.hook("vite:extendConfig", async (config, env) => {
		if (!needsEnvInjection) return;
		const plugin = toArray(typeof pluginOrGetter === "function" ? await pluginOrGetter() : pluginOrGetter);
		const method = options?.prepend ? "unshift" : "push";
		if (env.isClient && options.server === false) config.plugins[method](...plugin);
		if (env.isServer && options.client === false) config.plugins[method](...plugin);
	});
}
function addBuildPlugin(pluginFactory, options) {
	if (pluginFactory.vite) addVitePlugin(pluginFactory.vite, options);
	if (pluginFactory.webpack) addWebpackPlugin(pluginFactory.webpack, options);
	if (pluginFactory.rspack) addRspackPlugin(pluginFactory.rspack, options);
}
//#endregion
//#region src/components.ts
/**
* Register a directory to be scanned for components and imported only when used.
*/
function addComponentsDir(dir, opts = {}) {
	const nuxt = useNuxt();
	nuxt.options.components ||= [];
	dir.priority ||= 0;
	nuxt.hook("components:dirs", (dirs) => {
		dirs[opts.prepend ? "unshift" : "push"](dir);
	});
}
/**
* This utility takes a file path or npm package that is scanned for named exports, which are get added automatically
*/
function addComponentExports(opts) {
	const nuxt = useNuxt();
	const components = [];
	nuxt.hook("components:dirs", async () => {
		const names = await resolveModuleExportNames(await resolvePath(opts.filePath), { extensions: nuxt.options.extensions });
		components.length = 0;
		for (const name of names) components.push(normalizeComponent({
			name: pascalCase([opts.prefix || "", name === "default" ? "" : name]),
			export: name,
			...opts
		}));
	});
	addComponents(components);
}
/**
* Register a component by its name and filePath.
*/
function addComponent(opts) {
	addComponents([normalizeComponent(opts)]);
}
function addComponents(addedComponents) {
	const nuxt = useNuxt();
	nuxt.options.components ||= [];
	nuxt.hook("components:extend", (components) => {
		for (const component of addedComponents) {
			const existingComponentIndex = components.findIndex((c) => (c.pascalName === component.pascalName || c.kebabName === component.kebabName) && c.mode === component.mode);
			if (existingComponentIndex !== -1) {
				const existingComponent = components[existingComponentIndex];
				const existingPriority = existingComponent.priority ?? 0;
				const newPriority = component.priority ?? 0;
				if (newPriority < existingPriority) continue;
				if (newPriority === existingPriority) {
					const name = existingComponent.pascalName || existingComponent.kebabName;
					logger.warn(`Overriding ${name} component. You can specify a \`priority\` option when calling \`addComponent\` to avoid this warning.`);
				}
				components.splice(existingComponentIndex, 1, component);
			} else components.push(component);
		}
	});
}
function normalizeComponent(opts) {
	if (!opts.mode) {
		const [, mode = "all"] = opts.filePath.match(MODE_RE) || [];
		opts.mode = mode;
	}
	return {
		export: opts.export || "default",
		chunkName: "components/" + kebabCase(opts.name),
		global: opts.global ?? false,
		kebabName: kebabCase(opts.name || ""),
		pascalName: pascalCase(opts.name || ""),
		prefetch: false,
		preload: false,
		mode: "all",
		shortPath: opts.filePath,
		priority: 0,
		meta: {},
		...opts
	};
}
//#endregion
//#region src/template.ts
/**
* Renders given template during build into the virtual file system (and optionally to disk in the project `buildDir`)
*/
function addTemplate(_template) {
	const nuxt = useNuxt();
	const template = normalizeTemplate(_template);
	filterInPlace(nuxt.options.build.templates, (p) => (p.dst || normalizeTemplate(p).dst) !== template.dst);
	try {
		const distDir = distDirURL.toString();
		const { source } = captureStackTrace().find((e) => e.source && !e.source.startsWith(distDir)) ?? {};
		if (source) {
			const path = normalize(fileURLToPath(source));
			if (existsSync(path)) template._path = path;
		}
	} catch {}
	nuxt.options.build.templates.push(template);
	return template;
}
/**
* Adds a virtual file that can be used within the Nuxt Nitro server build.
*/
function addServerTemplate(template) {
	const nuxt = useNuxt();
	nuxt.options.nitro.virtual ||= {};
	nuxt.options.nitro.virtual[template.filename] = template.getContents;
	return template;
}
/**
* Renders given types during build to disk in the project `buildDir`
* and register them as types.
*
* You can pass a second context object to specify in which context the type should be added.
*
* If no context object is passed, then it will only be added to the nuxt context.
*/
function addTypeTemplate(_template, context) {
	const nuxt = useNuxt();
	const template = addTemplate(_template);
	if (!template.filename.endsWith(".d.ts")) throw new Error(`Invalid type template. Filename must end with .d.ts : "${template.filename}"`);
	if (!context || context.nuxt) nuxt.hook("prepare:types", (payload) => {
		payload.references ||= [];
		payload.references.push({ path: template.dst });
	});
	if (context?.node) nuxt.hook("prepare:types", (payload) => {
		payload.nodeReferences ||= [];
		payload.nodeReferences.push({ path: template.dst });
	});
	if (context?.shared) nuxt.hook("prepare:types", (payload) => {
		payload.sharedReferences ||= [];
		payload.sharedReferences.push({ path: template.dst });
	});
	if (!context || context.nuxt || context.shared) nuxt.options.vite.vue = defu(nuxt.options.vite.vue, { script: { globalTypeFiles: [template.dst] } });
	if (context?.nitro) nuxt.hook("nitro:prepare:types", (payload) => {
		payload.references ||= [];
		payload.references.push({ path: template.dst });
	});
	return template;
}
/**
* Normalize a nuxt template object
*/
function normalizeTemplate(template, buildDir) {
	if (!template) throw new Error("Invalid template: " + JSON.stringify(template));
	if (typeof template === "string") template = { src: template };
	else template = { ...template };
	if (template.src) {
		if (!existsSync(template.src)) throw new Error("Template not found: " + template.src);
		if (!template.filename) {
			const srcPath = parse(template.src);
			template.filename = template.fileName || `${basename(srcPath.dir)}.${srcPath.name}.${hash(template.src).replace(/-/g, "_")}${srcPath.ext}`;
		}
	}
	if (!template.src && !template.getContents) throw new Error("Invalid template. Either `getContents` or `src` should be provided: " + JSON.stringify(template));
	if (!template.filename) throw new Error("Invalid template. `filename` must be provided: " + JSON.stringify(template));
	if (template.filename.endsWith(".d.ts")) template.write = true;
	template.dst ||= resolve(buildDir ?? useNuxt().options.buildDir, template.filename);
	return template;
}
/**
* Trigger rebuilding Nuxt templates
*
* You can pass a filter within the options to selectively regenerate a subset of templates.
*/
async function updateTemplates(options) {
	await tryUseNuxt()?.hooks.callHook("builder:generateApp", options);
}
function resolveLayerPaths(dirs, projectBuildDir) {
	const relativeRootDir = relativeWithDot(projectBuildDir, dirs.root);
	const relativeSrcDir = relativeWithDot(projectBuildDir, dirs.app);
	const relativeModulesDir = relativeWithDot(projectBuildDir, dirs.modules);
	const relativeSharedDir = relativeWithDot(projectBuildDir, dirs.shared);
	return {
		nuxt: [
			join(relativeSrcDir, "**/*"),
			join(relativeModulesDir, `*/runtime/**/*`),
			join(relativeRootDir, `test/nuxt/**/*`),
			join(relativeRootDir, `tests/nuxt/**/*`),
			join(relativeRootDir, `layers/*/app/**/*`),
			join(relativeRootDir, `layers/*/modules/*/runtime/**/*`)
		],
		nitro: [
			join(relativeModulesDir, `*/runtime/server/**/*`),
			join(relativeRootDir, `layers/*/server/**/*`),
			join(relativeRootDir, `layers/*/modules/*/runtime/server/**/*`)
		],
		node: [
			join(relativeModulesDir, `*.*`),
			join(relativeRootDir, `nuxt.config.*`),
			join(relativeRootDir, `.config/nuxt.*`),
			join(relativeRootDir, `layers/*/nuxt.config.*`),
			join(relativeRootDir, `layers/*/.config/nuxt.*`),
			join(relativeRootDir, `layers/*/modules/**/*`)
		],
		shared: [
			join(relativeSharedDir, `**/*`),
			join(relativeModulesDir, `*/shared/**/*`),
			join(relativeRootDir, `layers/*/shared/**/*`)
		],
		sharedDeclarations: [
			join(relativeSharedDir, `**/*.d.ts`),
			join(relativeModulesDir, `*/shared/**/*.d.ts`),
			join(relativeRootDir, `layers/*/shared/**/*.d.ts`)
		],
		globalDeclarations: [join(relativeRootDir, `*.d.ts`), join(relativeRootDir, `layers/*/*.d.ts`)]
	};
}
const EXTENSION_RE = /\b(?:\.d\.[cm]?ts|\.\w+)$/g;
const excludedAlias = [/^@vue\/.*$/, /^#internal\/nuxt/];
async function _generateTypes(nuxt) {
	const include = new Set(["./nuxt.d.ts"]);
	const nodeInclude = new Set(["./nuxt.node.d.ts"]);
	const sharedInclude = new Set(["./nuxt.shared.d.ts"]);
	const legacyInclude = new Set([...include, ...nodeInclude]);
	const exclude = /* @__PURE__ */ new Set();
	const nodeExclude = /* @__PURE__ */ new Set();
	const sharedExclude = /* @__PURE__ */ new Set();
	const legacyExclude = /* @__PURE__ */ new Set();
	if (nuxt.options.typescript.includeWorkspace && nuxt.options.workspaceDir !== nuxt.options.srcDir) {
		include.add(join(relative(nuxt.options.buildDir, nuxt.options.workspaceDir), "**/*"));
		legacyInclude.add(join(relative(nuxt.options.buildDir, nuxt.options.workspaceDir), "**/*"));
	}
	const layerDirs = getLayerDirectories(nuxt);
	const sourceDirs = layerDirs.map((layer) => layer.app);
	for (const dir of nuxt.options.modulesDir) {
		if (!sourceDirs.some((srcDir) => dir.startsWith(srcDir))) exclude.add(relativeWithDot(nuxt.options.buildDir, dir));
		nodeExclude.add(relativeWithDot(nuxt.options.buildDir, dir));
		legacyExclude.add(relativeWithDot(nuxt.options.buildDir, dir));
	}
	for (const dir of ["dist", ".data"]) {
		exclude.add(relativeWithDot(nuxt.options.buildDir, resolve(nuxt.options.rootDir, dir)));
		nodeExclude.add(relativeWithDot(nuxt.options.buildDir, resolve(nuxt.options.rootDir, dir)));
		legacyExclude.add(relativeWithDot(nuxt.options.buildDir, resolve(nuxt.options.rootDir, dir)));
	}
	const rootDirWithSlash = withTrailingSlash$1(nuxt.options.rootDir);
	for (const dirs of layerDirs) if (!dirs.app.startsWith(rootDirWithSlash) || dirs.root === rootDirWithSlash || dirs.app.includes("node_modules")) {
		const rootGlob = join(relativeWithDot(nuxt.options.buildDir, dirs.root), "**/*");
		const paths = resolveLayerPaths(dirs, nuxt.options.buildDir);
		for (const path of paths.nuxt) {
			include.add(path);
			legacyInclude.add(path);
			if (path !== rootGlob) nodeExclude.add(path);
		}
		for (const path of paths.nitro) {
			exclude.add(path);
			nodeExclude.add(path);
			legacyExclude.add(path);
		}
		for (const path of paths.node) {
			nodeInclude.add(path);
			legacyInclude.add(path);
			exclude.add(path);
		}
		for (const path of paths.shared) {
			legacyInclude.add(path);
			sharedInclude.add(path);
		}
		for (const path of paths.sharedDeclarations) include.add(path);
		for (const path of paths.globalDeclarations) {
			include.add(path);
			legacyInclude.add(path);
			sharedInclude.add(path);
		}
	}
	const moduleEntryPaths = [];
	for (const m of nuxt.options._installedModules) {
		const path = m.meta?.rawPath || m.entryPath;
		if (path) moduleEntryPaths.push(getDirectory(path));
	}
	const modulePaths = await resolveNuxtModule(rootDirWithSlash, moduleEntryPaths);
	for (const path of modulePaths) {
		const relative = relativeWithDot(nuxt.options.buildDir, path);
		if (!path.includes("node_modules") && path.startsWith(rootDirWithSlash)) {
			include.add(join(relative, "runtime"));
			include.add(join(relative, "dist/runtime"));
			nodeInclude.add(join(relative, "*.*"));
		}
		legacyInclude.add(join(relative, "runtime"));
		legacyInclude.add(join(relative, "dist/runtime"));
		nodeExclude.add(join(relative, "runtime"));
		nodeExclude.add(join(relative, "dist/runtime"));
		exclude.add(join(relative, "runtime/server"));
		exclude.add(join(relative, "dist/runtime/server"));
		exclude.add(join(relative, "*.*"));
		exclude.add(join(relative, "dist/*.*"));
		legacyExclude.add(join(relative, "runtime/server"));
		legacyExclude.add(join(relative, "dist/runtime/server"));
	}
	const nestedModulesDirs = [];
	for (const dir of [...nuxt.options.modulesDir].sort()) {
		const withSlash = withTrailingSlash$1(dir);
		if (nestedModulesDirs.every((d) => !d.startsWith(withSlash))) nestedModulesDirs.push(withSlash);
	}
	let hasTypescriptVersionWithModulePreserve;
	for (const parent of nestedModulesDirs) hasTypescriptVersionWithModulePreserve ??= await readPackageJSON("typescript", { parent }).then((r) => r?.version && gte(r.version, "5.4.0")).catch(() => void 0);
	hasTypescriptVersionWithModulePreserve ??= true;
	const useDecorators = Boolean(nuxt.options.experimental?.decorators);
	const tsConfig = defu(nuxt.options.typescript?.tsConfig, {
		compilerOptions: {
			esModuleInterop: true,
			skipLibCheck: true,
			target: "ESNext",
			allowJs: true,
			resolveJsonModule: true,
			moduleDetection: "force",
			isolatedModules: true,
			verbatimModuleSyntax: true,
			allowArbitraryExtensions: true,
			strict: nuxt.options.typescript?.strict ?? true,
			noUncheckedIndexedAccess: true,
			forceConsistentCasingInFileNames: true,
			noImplicitOverride: true,
			...useDecorators ? { experimentalDecorators: false } : {},
			module: hasTypescriptVersionWithModulePreserve ? "preserve" : "ESNext",
			noEmit: true,
			lib: [
				"ESNext",
				...useDecorators ? ["esnext.decorators"] : [],
				"dom",
				"dom.iterable",
				"webworker"
			],
			jsx: "preserve",
			jsxImportSource: "vue",
			types: [],
			paths: {},
			moduleResolution: nuxt.options.future?.typescriptBundlerResolution || nuxt.options.experimental?.typescriptBundlerResolution ? "Bundler" : "Node",
			useDefineForClassFields: true,
			noImplicitThis: true,
			allowSyntheticDefaultImports: true
		},
		include: [...include],
		exclude: [...exclude]
	});
	const nodeTsConfig = defu(nuxt.options.typescript?.nodeTsConfig, {
		compilerOptions: {
			esModuleInterop: tsConfig.compilerOptions?.esModuleInterop,
			skipLibCheck: tsConfig.compilerOptions?.skipLibCheck,
			target: tsConfig.compilerOptions?.target,
			allowJs: tsConfig.compilerOptions?.allowJs,
			resolveJsonModule: tsConfig.compilerOptions?.resolveJsonModule,
			moduleDetection: tsConfig.compilerOptions?.moduleDetection,
			isolatedModules: tsConfig.compilerOptions?.isolatedModules,
			verbatimModuleSyntax: tsConfig.compilerOptions?.verbatimModuleSyntax,
			allowArbitraryExtensions: tsConfig.compilerOptions?.allowArbitraryExtensions,
			strict: tsConfig.compilerOptions?.strict,
			noUncheckedIndexedAccess: tsConfig.compilerOptions?.noUncheckedIndexedAccess,
			forceConsistentCasingInFileNames: tsConfig.compilerOptions?.forceConsistentCasingInFileNames,
			noImplicitOverride: tsConfig.compilerOptions?.noImplicitOverride,
			module: tsConfig.compilerOptions?.module,
			noEmit: true,
			types: [],
			paths: {},
			moduleResolution: tsConfig.compilerOptions?.moduleResolution,
			useDefineForClassFields: tsConfig.compilerOptions?.useDefineForClassFields,
			noImplicitThis: tsConfig.compilerOptions?.noImplicitThis,
			allowSyntheticDefaultImports: tsConfig.compilerOptions?.allowSyntheticDefaultImports
		},
		include: [...nodeInclude],
		exclude: [...nodeExclude]
	});
	const sharedTsConfig = defu(nuxt.options.typescript?.sharedTsConfig, {
		compilerOptions: {
			esModuleInterop: tsConfig.compilerOptions?.esModuleInterop,
			skipLibCheck: tsConfig.compilerOptions?.skipLibCheck,
			target: tsConfig.compilerOptions?.target,
			allowJs: tsConfig.compilerOptions?.allowJs,
			resolveJsonModule: tsConfig.compilerOptions?.resolveJsonModule,
			moduleDetection: tsConfig.compilerOptions?.moduleDetection,
			isolatedModules: tsConfig.compilerOptions?.isolatedModules,
			verbatimModuleSyntax: tsConfig.compilerOptions?.verbatimModuleSyntax,
			allowArbitraryExtensions: tsConfig.compilerOptions?.allowArbitraryExtensions,
			strict: tsConfig.compilerOptions?.strict,
			noUncheckedIndexedAccess: tsConfig.compilerOptions?.noUncheckedIndexedAccess,
			forceConsistentCasingInFileNames: tsConfig.compilerOptions?.forceConsistentCasingInFileNames,
			noImplicitOverride: tsConfig.compilerOptions?.noImplicitOverride,
			module: tsConfig.compilerOptions?.module,
			noEmit: true,
			types: [],
			paths: {},
			moduleResolution: tsConfig.compilerOptions?.moduleResolution,
			useDefineForClassFields: tsConfig.compilerOptions?.useDefineForClassFields,
			noImplicitThis: tsConfig.compilerOptions?.noImplicitThis,
			allowSyntheticDefaultImports: tsConfig.compilerOptions?.allowSyntheticDefaultImports
		},
		include: [...sharedInclude],
		exclude: [...sharedExclude]
	});
	const aliases = nuxt.options.alias;
	const basePath = tsConfig.compilerOptions.baseUrl ? resolve(nuxt.options.buildDir, tsConfig.compilerOptions.baseUrl) : nuxt.options.buildDir;
	tsConfig.compilerOptions ||= {};
	tsConfig.compilerOptions.paths ||= {};
	tsConfig.include ||= [];
	const importPaths = nuxt.options.modulesDir.map((d) => directoryToURL(d));
	for (const alias in aliases) {
		if (excludedAlias.some((re) => re.test(alias))) continue;
		let absolutePath = resolve(basePath, aliases[alias]);
		let stats = await promises.stat(absolutePath).catch(() => null);
		if (!stats) {
			const resolvedModule = resolveModulePath(aliases[alias], {
				try: true,
				from: importPaths,
				extensions: [
					...nuxt.options.extensions,
					".d.ts",
					".d.mts",
					".d.cts"
				]
			});
			if (resolvedModule) {
				absolutePath = resolvedModule;
				stats = await promises.stat(resolvedModule).catch(() => null);
			}
		}
		const relativePath = relativeWithDot(nuxt.options.buildDir, absolutePath);
		if (stats?.isDirectory() || aliases[alias].endsWith("/")) {
			tsConfig.compilerOptions.paths[alias] = [relativePath];
			tsConfig.compilerOptions.paths[`${alias}/*`] = [`${relativePath}/*`];
		} else {
			const path = stats?.isFile() ? relativePath.replace(EXTENSION_RE, "") : aliases[alias];
			tsConfig.compilerOptions.paths[alias] = [path];
		}
	}
	const references = [];
	const nodeReferences = [];
	const sharedReferences = [];
	await Promise.all([...nuxt.options.modules, ...nuxt.options._modules].map(async (id) => {
		if (typeof id !== "string") return;
		for (const parent of nestedModulesDirs) {
			const pkg = await readPackageJSON(id, { parent }).catch(() => null);
			if (pkg) {
				nodeReferences.push({ types: pkg.name ?? id });
				references.push({ types: pkg.name ?? id });
				return;
			}
		}
		nodeReferences.push({ types: id });
		references.push({ types: id });
	}));
	const declarations = [];
	await nuxt.callHook("prepare:types", {
		references,
		declarations,
		tsConfig,
		nodeTsConfig,
		nodeReferences,
		sharedTsConfig,
		sharedReferences
	});
	const legacyTsConfig = defu({}, {
		...tsConfig,
		include: [...tsConfig.include, ...legacyInclude],
		exclude: [...legacyExclude]
	});
	async function resolveConfig(tsConfig) {
		for (const alias in tsConfig.compilerOptions.paths) {
			const paths = tsConfig.compilerOptions.paths[alias];
			tsConfig.compilerOptions.paths[alias] = [...new Set(await Promise.all(paths.map(async (path) => {
				if (!isAbsolute(path)) return path;
				const stats = await promises.stat(path).catch(() => null);
				return relativeWithDot(nuxt.options.buildDir, stats?.isFile() ? path.replace(EXTENSION_RE, "") : path);
			})))];
		}
		sortTsPaths(tsConfig.compilerOptions.paths);
		tsConfig.include = [...new Set(tsConfig.include.map((p) => isAbsolute(p) ? relativeWithDot(nuxt.options.buildDir, p) : p))];
		tsConfig.exclude = [...new Set(tsConfig.exclude.map((p) => isAbsolute(p) ? relativeWithDot(nuxt.options.buildDir, p) : p))];
	}
	await Promise.all([
		resolveConfig(tsConfig),
		resolveConfig(nodeTsConfig),
		resolveConfig(sharedTsConfig),
		resolveConfig(legacyTsConfig)
	]);
	const declaration = [
		...references.map((ref) => renderReference(ref, nuxt.options.buildDir)),
		...declarations,
		"",
		"export {}",
		""
	].join("\n");
	const nodeDeclaration = [
		...nodeReferences.map((ref) => renderReference(ref, nuxt.options.buildDir)),
		"",
		"export {}",
		""
	].join("\n");
	return {
		declaration,
		sharedTsConfig,
		sharedDeclaration: [
			...sharedReferences.map((ref) => renderReference(ref, nuxt.options.buildDir)),
			"",
			"export {}",
			""
		].join("\n"),
		nodeTsConfig,
		nodeDeclaration,
		tsConfig,
		legacyTsConfig
	};
}
async function writeTypes(nuxt) {
	const { tsConfig, nodeTsConfig, nodeDeclaration, declaration, legacyTsConfig, sharedDeclaration, sharedTsConfig } = await _generateTypes(nuxt);
	const appTsConfigPath = resolve(nuxt.options.buildDir, "tsconfig.app.json");
	const legacyTsConfigPath = resolve(nuxt.options.buildDir, "tsconfig.json");
	const nodeTsConfigPath = resolve(nuxt.options.buildDir, "tsconfig.node.json");
	const sharedTsConfigPath = resolve(nuxt.options.buildDir, "tsconfig.shared.json");
	const declarationPath = resolve(nuxt.options.buildDir, "nuxt.d.ts");
	const nodeDeclarationPath = resolve(nuxt.options.buildDir, "nuxt.node.d.ts");
	const sharedDeclarationPath = resolve(nuxt.options.buildDir, "nuxt.shared.d.ts");
	await promises.mkdir(nuxt.options.buildDir, { recursive: true });
	await Promise.all([
		promises.writeFile(appTsConfigPath, JSON.stringify(tsConfig, null, 2)),
		promises.writeFile(legacyTsConfigPath, JSON.stringify(legacyTsConfig, null, 2)),
		promises.writeFile(nodeTsConfigPath, JSON.stringify(nodeTsConfig, null, 2)),
		promises.writeFile(sharedTsConfigPath, JSON.stringify(sharedTsConfig, null, 2)),
		promises.writeFile(declarationPath, declaration),
		promises.writeFile(nodeDeclarationPath, nodeDeclaration),
		promises.writeFile(sharedDeclarationPath, sharedDeclaration)
	]);
}
function sortTsPaths(paths) {
	for (const pathKey in paths) if (pathKey.startsWith("#build")) {
		const pathValue = paths[pathKey];
		delete paths[pathKey];
		paths[pathKey] = pathValue;
	}
}
function renderReference(ref, baseDir) {
	return `/// <reference ${"path" in ref ? `path="${isAbsolute(ref.path) ? relative(baseDir, ref.path) : ref.path}"` : `types="${ref.types}"`} />`;
}
const RELATIVE_WITH_DOT_RE = /^([^.])/;
function relativeWithDot(from, to) {
	return relative(from, to).replace(RELATIVE_WITH_DOT_RE, "./$1") || ".";
}
function withTrailingSlash$1(dir) {
	return dir.replace(/[^/]$/, "$&/");
}
//#endregion
//#region src/layout.ts
const LAYOUT_RE = /["']/g;
function addLayout(template, name) {
	const nuxt = useNuxt();
	const { filename, src } = addTemplate(template);
	const layoutName = kebabCase(name || parse(filename).name).replace(LAYOUT_RE, "");
	nuxt.hook("app:templates", (app) => {
		if (layoutName in app.layouts) {
			const relativePath = reverseResolveAlias(app.layouts[layoutName].file, {
				...nuxt?.options.alias || {},
				...strippedAtAliases
			}).pop() || app.layouts[layoutName].file;
			return logger.warn(`Not overriding \`${layoutName}\` (provided by \`${relativePath}\`) with \`${src || filename}\`.`);
		}
		app.layouts[layoutName] = {
			file: join("#build", filename),
			name: layoutName
		};
	});
}
const strippedAtAliases = {
	"@": "",
	"@@": ""
};
//#endregion
//#region src/pages.ts
function extendPages(cb) {
	useNuxt().hook("pages:extend", cb);
}
function extendRouteRules(route, rule, options = {}) {
	const nuxt = useNuxt();
	for (const opts of [nuxt.options, nuxt.options.nitro]) {
		opts.routeRules ||= {};
		opts.routeRules[route] = options.override ? defu(rule, opts.routeRules[route]) : defu(opts.routeRules[route], rule);
	}
}
function addRouteMiddleware(input, options = {}) {
	const nuxt = useNuxt();
	const middlewares = toArray(input);
	nuxt.hook("app:resolve", (app) => {
		for (const middleware of middlewares) {
			const find = app.middleware.findIndex((item) => item.name === middleware.name);
			if (find >= 0) {
				const foundPath = app.middleware[find].path;
				if (foundPath === middleware.path) continue;
				if (options.override === true) app.middleware[find] = { ...middleware };
				else logger.warn(`'${middleware.name}' middleware already exists at '${foundPath}'. You can set \`override: true\` to replace it.`);
			} else if (options.prepend === true) app.middleware.unshift({ ...middleware });
			else app.middleware.push({ ...middleware });
		}
	});
}
//#endregion
//#region src/plugin.ts
/**
* Normalize a nuxt plugin object
*/
const pluginSymbol = Symbol.for("nuxt plugin");
function normalizePlugin(plugin) {
	if (typeof plugin === "string") plugin = { src: plugin };
	else plugin = { ...plugin };
	if (pluginSymbol in plugin) return plugin;
	if (!plugin.src) throw new Error("Invalid plugin. src option is required: " + JSON.stringify(plugin));
	plugin.src = normalize(resolveAlias(plugin.src));
	if (!existsSync(plugin.src) && isAbsolute$1(plugin.src)) try {
		plugin.src = resolveModulePath(plugin.src, { extensions: tryUseNuxt()?.options.extensions ?? [
			".js",
			".mjs",
			".cjs",
			".ts",
			".tsx",
			".mts",
			".cts"
		] });
	} catch {}
	if (plugin.ssr) plugin.mode = "server";
	if (!plugin.mode) {
		const [, mode = "all"] = plugin.src.match(MODE_RE) || [];
		plugin.mode = mode;
	}
	plugin[pluginSymbol] = true;
	return plugin;
}
function addPlugin(_plugin, opts = {}) {
	const nuxt = useNuxt();
	const plugin = normalizePlugin(_plugin);
	filterInPlace(nuxt.options.plugins, (p) => normalizePlugin(p).src !== plugin.src);
	nuxt.options.plugins[opts.append ? "push" : "unshift"](plugin);
	return plugin;
}
/**
* Adds a template and registers as a nuxt plugin.
*/
function addPluginTemplate(plugin, opts = {}) {
	return addPlugin(typeof plugin === "string" ? { src: plugin } : {
		...plugin,
		src: addTemplate(plugin).dst
	}, opts);
}
//#endregion
export { addBuildPlugin, addComponent, addComponentExports, addComponentsDir, addDevServerHandler, addImports, addImportsDir, addImportsSources, addLayout, addPlugin, addPluginTemplate, addPrerenderRoutes, addRouteMiddleware, addRspackPlugin, addServerHandler, addServerImports, addServerImportsDir, addServerPlugin, addServerScanDir, addServerTemplate, addTemplate, addTypeTemplate, addVitePlugin, addWebpackPlugin, assertNuxtCompatibility, buildNuxt, checkNuxtCompatibility, createIsIgnored, createResolver, defineNuxtModule, directoryToURL, extendNuxtSchema, extendPages, extendRouteRules, extendRspackConfig, extendViteConfig, extendWebpackConfig, findPath, getDirectory, getLayerDirectories, getNuxtCtx, getNuxtModuleVersion, getNuxtVersion, hasNuxtCompatibility, hasNuxtModule, hasNuxtModuleCompatibility, importModule, installModule, installModules, isIgnored, isNuxt2, isNuxt3, isNuxtMajorVersion, loadNuxt, loadNuxtConfig, loadNuxtModuleInstance, logger, normalizeModuleTranspilePath, normalizePlugin, normalizeSemanticVersion, normalizeTemplate, nuxtCtx, requireModule, resolveAlias, resolveFiles, resolveIgnorePatterns, resolveModule, resolveModuleWithOptions, resolveNuxtModule, resolvePath, runWithNuxtContext, setGlobalHead, tryImportModule, tryRequireModule, tryResolveModule, tryUseNuxt, updateRuntimeConfig, updateTemplates, useLogger, useNitro, useNuxt, useRuntimeConfig, writeTypes };

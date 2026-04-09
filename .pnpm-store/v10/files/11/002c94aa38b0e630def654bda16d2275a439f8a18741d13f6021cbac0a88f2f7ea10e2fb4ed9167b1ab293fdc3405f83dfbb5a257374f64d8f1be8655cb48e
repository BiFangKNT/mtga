import { existsSync, promises, statSync } from "node:fs";
import { basename, dirname, extname, join, normalize, resolve } from "pathe";
import * as dotenv from "dotenv";
import { readFile, rm } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import { homedir } from "node:os";
import { resolveModulePath } from "exsolve";
import { createJiti } from "jiti";
import * as rc9 from "rc9";
import { defu } from "defu";
import { findWorkspaceDir, readPackageJSON } from "pkg-types";
import { debounce } from "perfect-debounce";

//#region src/dotenv.ts
/**
* Load and interpolate environment variables into `process.env`.
* If you need more control (or access to the values), consider using `loadDotenv` instead
*
*/
async function setupDotenv(options) {
	const targetEnvironment = options.env ?? process.env;
	const environment = await loadDotenv({
		cwd: options.cwd,
		fileName: options.fileName ?? ".env",
		env: targetEnvironment,
		interpolate: options.interpolate ?? true
	});
	const dotenvVars = getDotEnvVars(targetEnvironment);
	for (const key in environment) {
		if (key.startsWith("_")) continue;
		if (targetEnvironment[key] === void 0 || dotenvVars.has(key)) targetEnvironment[key] = environment[key];
	}
	return environment;
}
/** Load environment variables into an object. */
async function loadDotenv(options) {
	const environment = Object.create(null);
	const cwd = resolve(options.cwd || ".");
	const _fileName = options.fileName || ".env";
	const dotenvFiles = typeof _fileName === "string" ? [_fileName] : _fileName;
	const dotenvVars = getDotEnvVars(options.env || {});
	Object.assign(environment, options.env);
	for (const file of dotenvFiles) {
		const dotenvFile = resolve(cwd, file);
		if (!statSync(dotenvFile, { throwIfNoEntry: false })?.isFile()) continue;
		const parsed = dotenv.parse(await promises.readFile(dotenvFile, "utf8"));
		for (const key in parsed) {
			if (key in environment && !dotenvVars.has(key)) continue;
			environment[key] = parsed[key];
			dotenvVars.add(key);
		}
	}
	if (options.interpolate) interpolate(environment);
	return environment;
}
function interpolate(target, source = {}, parse = (v) => v) {
	function getValue(key) {
		return source[key] === void 0 ? target[key] : source[key];
	}
	function interpolate$1(value, parents = []) {
		if (typeof value !== "string") return value;
		return parse((value.match(/(.?\${?(?:[\w:]+)?}?)/g) || []).reduce((newValue, match) => {
			const parts = /(.?)\${?([\w:]+)?}?/g.exec(match) || [];
			const prefix = parts[1];
			let value$1, replacePart;
			if (prefix === "\\") {
				replacePart = parts[0] || "";
				value$1 = replacePart.replace(String.raw`\$`, "$");
			} else {
				const key = parts[2];
				replacePart = (parts[0] || "").slice(prefix.length);
				if (parents.includes(key)) {
					console.warn(`Please avoid recursive environment variables ( loop: ${parents.join(" > ")} > ${key} )`);
					return "";
				}
				value$1 = getValue(key);
				value$1 = interpolate$1(value$1, [...parents, key]);
			}
			return value$1 === void 0 ? newValue : newValue.replace(replacePart, value$1);
		}, value));
	}
	for (const key in target) target[key] = interpolate$1(getValue(key));
}
function getDotEnvVars(targetEnvironment) {
	const globalRegistry = globalThis.__c12_dotenv_vars__ ||= /* @__PURE__ */ new Map();
	if (!globalRegistry.has(targetEnvironment)) globalRegistry.set(targetEnvironment, /* @__PURE__ */ new Set());
	return globalRegistry.get(targetEnvironment);
}

//#endregion
//#region src/loader.ts
const _normalize = (p) => p?.replace(/\\/g, "/");
const ASYNC_LOADERS = {
	".yaml": () => import("confbox/yaml").then((r) => r.parseYAML),
	".yml": () => import("confbox/yaml").then((r) => r.parseYAML),
	".jsonc": () => import("confbox/jsonc").then((r) => r.parseJSONC),
	".json5": () => import("confbox/json5").then((r) => r.parseJSON5),
	".toml": () => import("confbox/toml").then((r) => r.parseTOML)
};
const SUPPORTED_EXTENSIONS = Object.freeze([
	".js",
	".ts",
	".mjs",
	".cjs",
	".mts",
	".cts",
	".json",
	".jsonc",
	".json5",
	".yaml",
	".yml",
	".toml"
]);
async function loadConfig(options) {
	options.cwd = resolve(process.cwd(), options.cwd || ".");
	options.name = options.name || "config";
	options.envName = options.envName ?? process.env.NODE_ENV;
	options.configFile = options.configFile ?? (options.name === "config" ? "config" : `${options.name}.config`);
	options.rcFile = options.rcFile ?? `.${options.name}rc`;
	if (options.extend !== false) options.extend = {
		extendKey: "extends",
		...options.extend
	};
	const _merger = options.merger || defu;
	options.jiti = options.jiti || createJiti(join(options.cwd, options.configFile), {
		interopDefault: true,
		moduleCache: false,
		extensions: [...SUPPORTED_EXTENSIONS],
		...options.jitiOptions
	});
	const r = {
		config: {},
		cwd: options.cwd,
		configFile: resolve(options.cwd, options.configFile),
		layers: [],
		_configFile: void 0
	};
	const rawConfigs = {
		overrides: options.overrides,
		main: void 0,
		rc: void 0,
		packageJson: void 0,
		defaultConfig: options.defaultConfig
	};
	if (options.dotenv) await setupDotenv({
		cwd: options.cwd,
		...options.dotenv === true ? {} : options.dotenv
	});
	const _mainConfig = await resolveConfig(".", options);
	if (_mainConfig.configFile) {
		rawConfigs.main = _mainConfig.config;
		r.configFile = _mainConfig.configFile;
		r._configFile = _mainConfig._configFile;
	}
	if (_mainConfig.meta) r.meta = _mainConfig.meta;
	if (options.rcFile) {
		const rcSources = [];
		rcSources.push(rc9.read({
			name: options.rcFile,
			dir: options.cwd
		}));
		if (options.globalRc) {
			const workspaceDir = await findWorkspaceDir(options.cwd).catch(() => {});
			if (workspaceDir) rcSources.push(rc9.read({
				name: options.rcFile,
				dir: workspaceDir
			}));
			rcSources.push(rc9.readUser({
				name: options.rcFile,
				dir: options.cwd
			}));
		}
		rawConfigs.rc = _merger({}, ...rcSources);
	}
	if (options.packageJson) {
		const keys = (Array.isArray(options.packageJson) ? options.packageJson : [typeof options.packageJson === "string" ? options.packageJson : options.name]).filter((t) => t && typeof t === "string");
		const pkgJsonFile = await readPackageJSON(options.cwd).catch(() => {});
		rawConfigs.packageJson = _merger({}, ...keys.map((key) => pkgJsonFile?.[key]));
	}
	const configs = {};
	for (const key in rawConfigs) {
		const value = rawConfigs[key];
		configs[key] = await (typeof value === "function" ? value({
			configs,
			rawConfigs
		}) : value);
	}
	if (Array.isArray(configs.main)) r.config = configs.main;
	else {
		r.config = _merger(configs.overrides, configs.main, configs.rc, configs.packageJson, configs.defaultConfig);
		if (options.extend) {
			await extendConfig(r.config, options);
			r.layers = r.config._layers;
			delete r.config._layers;
			r.config = _merger(r.config, ...r.layers.map((e) => e.config));
		}
	}
	r.layers = [...[
		configs.overrides && {
			config: configs.overrides,
			configFile: void 0,
			cwd: void 0
		},
		{
			config: configs.main,
			configFile: options.configFile,
			cwd: options.cwd
		},
		configs.rc && {
			config: configs.rc,
			configFile: options.rcFile
		},
		configs.packageJson && {
			config: configs.packageJson,
			configFile: "package.json"
		}
	].filter((l) => l && l.config), ...r.layers];
	if (options.defaults) r.config = _merger(r.config, options.defaults);
	if (options.omit$Keys) {
		for (const key in r.config) if (key.startsWith("$")) delete r.config[key];
	}
	if (options.configFileRequired && !r._configFile) throw new Error(`Required config (${r.configFile}) cannot be resolved.`);
	return r;
}
async function extendConfig(config, options) {
	config._layers = config._layers || [];
	if (!options.extend) return;
	let keys = options.extend.extendKey;
	if (typeof keys === "string") keys = [keys];
	const extendSources = [];
	for (const key of keys) {
		extendSources.push(...(Array.isArray(config[key]) ? config[key] : [config[key]]).filter(Boolean));
		delete config[key];
	}
	for (let extendSource of extendSources) {
		const originalExtendSource = extendSource;
		let sourceOptions = {};
		if (extendSource.source) {
			sourceOptions = extendSource.options || {};
			extendSource = extendSource.source;
		}
		if (Array.isArray(extendSource)) {
			sourceOptions = extendSource[1] || {};
			extendSource = extendSource[0];
		}
		if (typeof extendSource !== "string") {
			console.warn(`Cannot extend config from \`${JSON.stringify(originalExtendSource)}\` in ${options.cwd}`);
			continue;
		}
		const _config = await resolveConfig(extendSource, options, sourceOptions);
		if (!_config.config) {
			console.warn(`Cannot extend config from \`${extendSource}\` in ${options.cwd}`);
			continue;
		}
		await extendConfig(_config.config, {
			...options,
			cwd: _config.cwd
		});
		config._layers.push(_config);
		if (_config.config._layers) {
			config._layers.push(..._config.config._layers);
			delete _config.config._layers;
		}
	}
}
const GIGET_PREFIXES = [
	"gh:",
	"github:",
	"gitlab:",
	"bitbucket:",
	"https://",
	"http://"
];
const NPM_PACKAGE_RE = /^(@[\da-z~-][\d._a-z~-]*\/)?[\da-z~-][\d._a-z~-]*($|\/.*)/;
async function resolveConfig(source, options, sourceOptions = {}) {
	if (options.resolve) {
		const res$1 = await options.resolve(source, options);
		if (res$1) return res$1;
	}
	const _merger = options.merger || defu;
	const customProviderKeys = Object.keys(sourceOptions.giget?.providers || {}).map((key) => `${key}:`);
	const gigetPrefixes = customProviderKeys.length > 0 ? [...new Set([...customProviderKeys, ...GIGET_PREFIXES])] : GIGET_PREFIXES;
	if (options.giget !== false && gigetPrefixes.some((prefix) => source.startsWith(prefix))) {
		const { downloadTemplate } = await import("giget");
		const { digest } = await import("ohash");
		const cloneName = source.replace(/\W+/g, "_").split("_").splice(0, 3).join("_") + "_" + digest(source).slice(0, 10).replace(/[-_]/g, "");
		let cloneDir;
		const localNodeModules = resolve(options.cwd, "node_modules");
		const parentDir = dirname(options.cwd);
		if (basename(parentDir) === ".c12") cloneDir = join(parentDir, cloneName);
		else if (existsSync(localNodeModules)) cloneDir = join(localNodeModules, ".c12", cloneName);
		else cloneDir = process.env.XDG_CACHE_HOME ? resolve(process.env.XDG_CACHE_HOME, "c12", cloneName) : resolve(homedir(), ".cache/c12", cloneName);
		if (existsSync(cloneDir) && !sourceOptions.install) await rm(cloneDir, { recursive: true });
		source = (await downloadTemplate(source, {
			dir: cloneDir,
			install: sourceOptions.install,
			force: sourceOptions.install,
			auth: sourceOptions.auth,
			...options.giget,
			...sourceOptions.giget
		})).dir;
	}
	if (NPM_PACKAGE_RE.test(source)) source = tryResolve(source, options) || source;
	const ext = extname(source);
	const isDir = !ext || ext === basename(source);
	const cwd = resolve(options.cwd, isDir ? source : dirname(source));
	if (isDir) source = options.configFile;
	const res = {
		config: void 0,
		configFile: void 0,
		cwd,
		source,
		sourceOptions
	};
	res.configFile = tryResolve(resolve(cwd, source), options) || tryResolve(resolve(cwd, ".config", source.replace(/\.config$/, "")), options) || tryResolve(resolve(cwd, ".config", source), options) || source;
	if (!existsSync(res.configFile)) return res;
	res._configFile = res.configFile;
	const configFileExt = extname(res.configFile) || "";
	if (configFileExt in ASYNC_LOADERS) res.config = (await ASYNC_LOADERS[configFileExt]())(await readFile(res.configFile, "utf8"));
	else res.config = await options.jiti.import(res.configFile, { default: true });
	if (typeof res.config === "function") res.config = await res.config(options.context);
	if (options.envName) {
		const envConfig = {
			...res.config["$" + options.envName],
			...res.config.$env?.[options.envName]
		};
		if (Object.keys(envConfig).length > 0) res.config = _merger(envConfig, res.config);
	}
	res.meta = defu(res.sourceOptions.meta, res.config.$meta);
	delete res.config.$meta;
	if (res.sourceOptions.overrides) res.config = _merger(res.sourceOptions.overrides, res.config);
	res.configFile = _normalize(res.configFile);
	res.source = _normalize(res.source);
	return res;
}
function tryResolve(id, options) {
	const res = resolveModulePath(id, {
		try: true,
		from: pathToFileURL(join(options.cwd || ".", options.configFile || "/")),
		suffixes: ["", "/index"],
		extensions: SUPPORTED_EXTENSIONS,
		cache: false
	});
	return res ? normalize(res) : void 0;
}

//#endregion
//#region src/types.ts
function createDefineConfig() {
	return (input) => input;
}

//#endregion
//#region src/watch.ts
const eventMap = {
	add: "created",
	change: "updated",
	unlink: "removed"
};
async function watchConfig(options) {
	let config = await loadConfig(options);
	const configName = options.name || "config";
	const configFileName = options.configFile ?? (options.name === "config" ? "config" : `${options.name}.config`);
	const watchingFiles = [...new Set((config.layers || []).filter((l) => l.cwd).flatMap((l) => [
		...SUPPORTED_EXTENSIONS.flatMap((ext) => [
			resolve(l.cwd, configFileName + ext),
			resolve(l.cwd, ".config", configFileName + ext),
			resolve(l.cwd, ".config", configFileName.replace(/\.config$/, "") + ext)
		]),
		l.source && resolve(l.cwd, l.source),
		options.rcFile && resolve(l.cwd, typeof options.rcFile === "string" ? options.rcFile : `.${configName}rc`),
		options.packageJson && resolve(l.cwd, "package.json")
	]).filter(Boolean))];
	const watch = await import("chokidar").then((r) => r.watch || r.default || r);
	const { diff } = await import("ohash/utils");
	const _fswatcher = watch(watchingFiles, {
		ignoreInitial: true,
		...options.chokidarOptions
	});
	const onChange = async (event, path) => {
		const type = eventMap[event];
		if (!type) return;
		if (options.onWatch) await options.onWatch({
			type,
			path
		});
		const oldConfig = config;
		try {
			config = await loadConfig(options);
		} catch (error) {
			console.warn(`Failed to load config ${path}\n${error}`);
			return;
		}
		const changeCtx = {
			newConfig: config,
			oldConfig,
			getDiff: () => diff(oldConfig.config, config.config)
		};
		if (options.acceptHMR) {
			if (await options.acceptHMR(changeCtx)) return;
		}
		if (options.onUpdate) await options.onUpdate(changeCtx);
	};
	if (options.debounce === false) _fswatcher.on("all", onChange);
	else _fswatcher.on("all", debounce(onChange, options.debounce ?? 100));
	const utils = {
		watchingFiles,
		unwatch: async () => {
			await _fswatcher.close();
		}
	};
	return new Proxy(utils, { get(_, prop) {
		if (prop in utils) return utils[prop];
		return config[prop];
	} });
}

//#endregion
export { SUPPORTED_EXTENSIONS, createDefineConfig, loadConfig, loadDotenv, setupDotenv, watchConfig };
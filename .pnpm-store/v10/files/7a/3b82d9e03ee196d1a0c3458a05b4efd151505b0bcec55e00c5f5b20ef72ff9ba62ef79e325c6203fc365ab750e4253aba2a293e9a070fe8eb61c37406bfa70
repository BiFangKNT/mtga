import { builtinModules, createRequire } from "node:module";
import fs, { existsSync, promises, realpathSync, statSync } from "node:fs";
import fs$1, { constants, readFile, stat } from "node:fs/promises";
import process$1 from "node:process";
import c from "ansis";
import cac from "cac";
import { createServer } from "node:net";
import os, { networkInterfaces } from "node:os";
import path from "node:path";
import { URL as URL$1, fileURLToPath, pathToFileURL } from "node:url";
import childProcess, { execFile } from "node:child_process";
import { format, inspect, promisify } from "node:util";
import { Buffer as Buffer$1 } from "node:buffer";
import { glob } from "tinyglobby";
import { bundleRequire } from "bundle-require";
import assert from "node:assert";
import v8 from "node:v8";
import tty from "node:tty";
import { createServer as createServer$1 } from "node:http";
import { createApp, eventHandler, serveStatic, toNodeListener } from "h3";
import chokidar from "chokidar";
import { WebSocketServer } from "ws";

//#region \0rolldown/runtime.js
var __create = Object.create;
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __getProtoOf = Object.getPrototypeOf;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __esmMin = (fn, res) => () => (fn && (res = fn(fn = 0)), res);
var __commonJSMin = (cb, mod) => () => (mod || cb((mod = { exports: {} }).exports, mod), mod.exports);
var __exportAll = (all, no_symbols) => {
	let target = {};
	for (var name in all) {
		__defProp(target, name, {
			get: all[name],
			enumerable: true
		});
	}
	if (!no_symbols) {
		__defProp(target, Symbol.toStringTag, { value: "Module" });
	}
	return target;
};
var __copyProps = (to, from, except, desc) => {
	if (from && typeof from === "object" || typeof from === "function") {
		for (var keys = __getOwnPropNames(from), i = 0, n = keys.length, key; i < n; i++) {
			key = keys[i];
			if (!__hasOwnProp.call(to, key) && key !== except) {
				__defProp(to, key, {
					get: ((k) => from[k]).bind(null, key),
					enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable
				});
			}
		}
	}
	return to;
};
var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", {
	value: mod,
	enumerable: true
}) : target, mod));
var __toCommonJS = (mod) => __hasOwnProp.call(mod, "module.exports") ? mod["module.exports"] : __copyProps(__defProp({}, "__esModule", { value: true }), mod);
var __require = /* @__PURE__ */ createRequire(import.meta.url);

//#endregion
//#region node_modules/.pnpm/get-port-please@3.2.0/node_modules/get-port-please/dist/index.mjs
const unsafePorts = /* @__PURE__ */ new Set([
	1,
	7,
	9,
	11,
	13,
	15,
	17,
	19,
	20,
	21,
	22,
	23,
	25,
	37,
	42,
	43,
	53,
	69,
	77,
	79,
	87,
	95,
	101,
	102,
	103,
	104,
	109,
	110,
	111,
	113,
	115,
	117,
	119,
	123,
	135,
	137,
	139,
	143,
	161,
	179,
	389,
	427,
	465,
	512,
	513,
	514,
	515,
	526,
	530,
	531,
	532,
	540,
	548,
	554,
	556,
	563,
	587,
	601,
	636,
	989,
	990,
	993,
	995,
	1719,
	1720,
	1723,
	2049,
	3659,
	4045,
	5060,
	5061,
	6e3,
	6566,
	6665,
	6666,
	6667,
	6668,
	6669,
	6697,
	10080
]);
function isUnsafePort(port) {
	return unsafePorts.has(port);
}
function isSafePort(port) {
	return !isUnsafePort(port);
}
var GetPortError = class extends Error {
	constructor(message, opts) {
		super(message, opts);
		this.message = message;
	}
	name = "GetPortError";
};
function _log(verbose, message) {
	if (verbose) console.log(`[get-port] ${message}`);
}
function _generateRange(from, to) {
	if (to < from) return [];
	const r = [];
	for (let index = from; index <= to; index++) r.push(index);
	return r;
}
function _tryPort(port, host) {
	return new Promise((resolve) => {
		const server = createServer();
		server.unref();
		server.on("error", () => {
			resolve(false);
		});
		server.listen({
			port,
			host
		}, () => {
			const { port: port2 } = server.address();
			server.close(() => {
				resolve(isSafePort(port2) && port2);
			});
		});
	});
}
function _getLocalHosts(additional) {
	const hosts = new Set(additional);
	for (const _interface of Object.values(networkInterfaces())) for (const config of _interface || []) if (config.address && !config.internal && !config.address.startsWith("fe80::") && !config.address.startsWith("169.254")) hosts.add(config.address);
	return [...hosts];
}
async function _findPort(ports, host) {
	for (const port of ports) {
		const r = await _tryPort(port, host);
		if (r) return r;
	}
}
function _fmtOnHost(hostname) {
	return hostname ? `on host ${JSON.stringify(hostname)}` : "on any host";
}
const HOSTNAME_RE = /^(?!-)[\d.:A-Za-z-]{1,63}(?<!-)$/;
function _validateHostname(hostname, _public, verbose) {
	if (hostname && !HOSTNAME_RE.test(hostname)) {
		const fallbackHost = _public ? "0.0.0.0" : "127.0.0.1";
		_log(verbose, `Invalid hostname: ${JSON.stringify(hostname)}. Using ${JSON.stringify(fallbackHost)} as fallback.`);
		return fallbackHost;
	}
	return hostname;
}
async function getPort(_userOptions = {}) {
	if (typeof _userOptions === "number" || typeof _userOptions === "string") _userOptions = { port: Number.parseInt(_userOptions + "") || 0 };
	const _port = Number(_userOptions.port ?? process.env.PORT);
	const _userSpecifiedAnyPort = Boolean(_userOptions.port || _userOptions.ports?.length || _userOptions.portRange?.length);
	const options = {
		random: _port === 0,
		ports: [],
		portRange: [],
		alternativePortRange: _userSpecifiedAnyPort ? [] : [3e3, 3100],
		verbose: false,
		..._userOptions,
		port: _port,
		host: _validateHostname(_userOptions.host ?? process.env.HOST, _userOptions.public, _userOptions.verbose)
	};
	if (options.random && !_userSpecifiedAnyPort) return getRandomPort(options.host);
	const portsToCheck = [
		options.port,
		...options.ports,
		..._generateRange(...options.portRange)
	].filter((port) => {
		if (!port) return false;
		if (!isSafePort(port)) {
			_log(options.verbose, `Ignoring unsafe port: ${port}`);
			return false;
		}
		return true;
	});
	if (portsToCheck.length === 0) portsToCheck.push(3e3);
	let availablePort = await _findPort(portsToCheck, options.host);
	if (!availablePort && options.alternativePortRange.length > 0) {
		availablePort = await _findPort(_generateRange(...options.alternativePortRange), options.host);
		if (portsToCheck.length > 0) {
			let message = `Unable to find an available port (tried ${portsToCheck.join("-")} ${_fmtOnHost(options.host)}).`;
			if (availablePort) message += ` Using alternative port ${availablePort}.`;
			_log(options.verbose, message);
		}
	}
	if (!availablePort && _userOptions.random !== false) {
		availablePort = await getRandomPort(options.host);
		if (availablePort) _log(options.verbose, `Using random port ${availablePort}`);
	}
	if (!availablePort) {
		const triedRanges = [
			options.port,
			options.portRange.join("-"),
			options.alternativePortRange.join("-")
		].filter(Boolean).join(", ");
		throw new GetPortError(`Unable to find an available port ${_fmtOnHost(options.host)} (tried ${triedRanges})`);
	}
	return availablePort;
}
async function getRandomPort(host) {
	const port = await checkPort(0, host);
	if (port === false) throw new GetPortError(`Unable to find a random port ${_fmtOnHost(host)}`);
	return port;
}
async function checkPort(port, host = process.env.HOST, verbose) {
	if (!host) host = _getLocalHosts([void 0, "0.0.0.0"]);
	if (!Array.isArray(host)) return _tryPort(port, host);
	for (const _host of host) {
		const _port = await _tryPort(port, _host);
		if (_port === false) {
			if (port < 1024 && verbose) _log(verbose, `Unable to listen to the privileged port ${port} ${_fmtOnHost(_host)}`);
			return false;
		}
		if (port === 0 && _port !== 0) port = _port;
	}
	return port;
}

//#endregion
//#region node_modules/.pnpm/is-docker@3.0.0/node_modules/is-docker/index.js
let isDockerCached;
function hasDockerEnv() {
	try {
		fs.statSync("/.dockerenv");
		return true;
	} catch {
		return false;
	}
}
function hasDockerCGroup() {
	try {
		return fs.readFileSync("/proc/self/cgroup", "utf8").includes("docker");
	} catch {
		return false;
	}
}
function isDocker() {
	if (isDockerCached === void 0) isDockerCached = hasDockerEnv() || hasDockerCGroup();
	return isDockerCached;
}

//#endregion
//#region node_modules/.pnpm/is-inside-container@1.0.0/node_modules/is-inside-container/index.js
let cachedResult;
const hasContainerEnv = () => {
	try {
		fs.statSync("/run/.containerenv");
		return true;
	} catch {
		return false;
	}
};
function isInsideContainer() {
	if (cachedResult === void 0) cachedResult = hasContainerEnv() || isDocker();
	return cachedResult;
}

//#endregion
//#region node_modules/.pnpm/is-wsl@3.1.0/node_modules/is-wsl/index.js
const isWsl = () => {
	if (process$1.platform !== "linux") return false;
	if (os.release().toLowerCase().includes("microsoft")) {
		if (isInsideContainer()) return false;
		return true;
	}
	try {
		return fs.readFileSync("/proc/version", "utf8").toLowerCase().includes("microsoft") ? !isInsideContainer() : false;
	} catch {
		return false;
	}
};
var is_wsl_default = process$1.env.__IS_WSL_TEST__ ? isWsl : isWsl();

//#endregion
//#region node_modules/.pnpm/powershell-utils@0.1.0/node_modules/powershell-utils/index.js
const execFile$2 = promisify(childProcess.execFile);
const powerShellPath$1 = () => `${process$1.env.SYSTEMROOT || process$1.env.windir || String.raw`C:\Windows`}\\System32\\WindowsPowerShell\\v1.0\\powershell.exe`;
const executePowerShell = async (command, options = {}) => {
	const { powerShellPath: psPath, ...execFileOptions } = options;
	const encodedCommand = executePowerShell.encodeCommand(command);
	return execFile$2(psPath ?? powerShellPath$1(), [...executePowerShell.argumentsPrefix, encodedCommand], {
		encoding: "utf8",
		...execFileOptions
	});
};
executePowerShell.argumentsPrefix = [
	"-NoProfile",
	"-NonInteractive",
	"-ExecutionPolicy",
	"Bypass",
	"-EncodedCommand"
];
executePowerShell.encodeCommand = (command) => Buffer$1.from(command, "utf16le").toString("base64");
executePowerShell.escapeArgument = (value) => `'${String(value).replaceAll("'", "''")}'`;

//#endregion
//#region node_modules/.pnpm/wsl-utils@0.3.0/node_modules/wsl-utils/index.js
const execFile$1 = promisify(childProcess.execFile);
const wslDrivesMountPoint = (() => {
	const defaultMountPoint = "/mnt/";
	let mountPoint;
	return async function() {
		if (mountPoint) return mountPoint;
		const configFilePath = "/etc/wsl.conf";
		let isConfigFileExists = false;
		try {
			await fs$1.access(configFilePath, constants.F_OK);
			isConfigFileExists = true;
		} catch {}
		if (!isConfigFileExists) return defaultMountPoint;
		const configContent = await fs$1.readFile(configFilePath, { encoding: "utf8" });
		const configMountPoint = /(?<!#.*)root\s*=\s*(?<mountPoint>.*)/g.exec(configContent);
		if (!configMountPoint) return defaultMountPoint;
		mountPoint = configMountPoint.groups.mountPoint.trim();
		mountPoint = mountPoint.endsWith("/") ? mountPoint : `${mountPoint}/`;
		return mountPoint;
	};
})();
const powerShellPathFromWsl = async () => {
	return `${await wslDrivesMountPoint()}c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`;
};
const powerShellPath = is_wsl_default ? powerShellPathFromWsl : powerShellPath$1;
let canAccessPowerShellPromise;
const canAccessPowerShell = async () => {
	canAccessPowerShellPromise ??= (async () => {
		try {
			const psPath = await powerShellPath();
			await fs$1.access(psPath, constants.X_OK);
			return true;
		} catch {
			return false;
		}
	})();
	return canAccessPowerShellPromise;
};
const wslDefaultBrowser = async () => {
	const psPath = await powerShellPath();
	const { stdout } = await executePowerShell(String.raw`(Get-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice").ProgId`, { powerShellPath: psPath });
	return stdout.trim();
};
const convertWslPathToWindows = async (path) => {
	if (/^[a-z]+:\/\//i.test(path)) return path;
	try {
		const { stdout } = await execFile$1("wslpath", ["-aw", path], { encoding: "utf8" });
		return stdout.trim();
	} catch {
		return path;
	}
};

//#endregion
//#region node_modules/.pnpm/define-lazy-prop@3.0.0/node_modules/define-lazy-prop/index.js
function defineLazyProperty(object, propertyName, valueGetter) {
	const define = (value) => Object.defineProperty(object, propertyName, {
		value,
		enumerable: true,
		writable: true
	});
	Object.defineProperty(object, propertyName, {
		configurable: true,
		enumerable: true,
		get() {
			const result = valueGetter();
			define(result);
			return result;
		},
		set(value) {
			define(value);
		}
	});
	return object;
}

//#endregion
//#region node_modules/.pnpm/default-browser-id@5.0.0/node_modules/default-browser-id/index.js
const execFileAsync$3 = promisify(execFile);
async function defaultBrowserId() {
	if (process$1.platform !== "darwin") throw new Error("macOS only");
	const { stdout } = await execFileAsync$3("defaults", [
		"read",
		"com.apple.LaunchServices/com.apple.launchservices.secure",
		"LSHandlers"
	]);
	return /LSHandlerRoleAll = "(?!-)(?<id>[^"]+?)";\s+?LSHandlerURLScheme = (?:http|https);/.exec(stdout)?.groups.id ?? "com.apple.Safari";
}

//#endregion
//#region node_modules/.pnpm/run-applescript@7.0.0/node_modules/run-applescript/index.js
const execFileAsync$2 = promisify(execFile);
async function runAppleScript(script, { humanReadableOutput = true } = {}) {
	if (process$1.platform !== "darwin") throw new Error("macOS only");
	const { stdout } = await execFileAsync$2("osascript", [
		"-e",
		script,
		humanReadableOutput ? [] : ["-ss"]
	]);
	return stdout.trim();
}

//#endregion
//#region node_modules/.pnpm/bundle-name@4.1.0/node_modules/bundle-name/index.js
async function bundleName(bundleId) {
	return runAppleScript(`tell application "Finder" to set app_path to application file id "${bundleId}" as string\ntell application "System Events" to get value of property list item "CFBundleName" of property list file (app_path & ":Contents:Info.plist")`);
}

//#endregion
//#region node_modules/.pnpm/default-browser@5.4.0/node_modules/default-browser/windows.js
const execFileAsync$1 = promisify(execFile);
const windowsBrowserProgIds = {
	MSEdgeHTM: {
		name: "Edge",
		id: "com.microsoft.edge"
	},
	MSEdgeBHTML: {
		name: "Edge Beta",
		id: "com.microsoft.edge.beta"
	},
	MSEdgeDHTML: {
		name: "Edge Dev",
		id: "com.microsoft.edge.dev"
	},
	AppXq0fevzme2pys62n3e0fbqa7peapykr8v: {
		name: "Edge",
		id: "com.microsoft.edge.old"
	},
	ChromeHTML: {
		name: "Chrome",
		id: "com.google.chrome"
	},
	ChromeBHTML: {
		name: "Chrome Beta",
		id: "com.google.chrome.beta"
	},
	ChromeDHTML: {
		name: "Chrome Dev",
		id: "com.google.chrome.dev"
	},
	ChromiumHTM: {
		name: "Chromium",
		id: "org.chromium.Chromium"
	},
	BraveHTML: {
		name: "Brave",
		id: "com.brave.Browser"
	},
	BraveBHTML: {
		name: "Brave Beta",
		id: "com.brave.Browser.beta"
	},
	BraveDHTML: {
		name: "Brave Dev",
		id: "com.brave.Browser.dev"
	},
	BraveSSHTM: {
		name: "Brave Nightly",
		id: "com.brave.Browser.nightly"
	},
	FirefoxURL: {
		name: "Firefox",
		id: "org.mozilla.firefox"
	},
	OperaStable: {
		name: "Opera",
		id: "com.operasoftware.Opera"
	},
	VivaldiHTM: {
		name: "Vivaldi",
		id: "com.vivaldi.Vivaldi"
	},
	"IE.HTTP": {
		name: "Internet Explorer",
		id: "com.microsoft.ie"
	}
};
const _windowsBrowserProgIdMap = new Map(Object.entries(windowsBrowserProgIds));
var UnknownBrowserError = class extends Error {};
async function defaultBrowser$1(_execFileAsync = execFileAsync$1) {
	const { stdout } = await _execFileAsync("reg", [
		"QUERY",
		" HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice",
		"/v",
		"ProgId"
	]);
	const match = /ProgId\s*REG_SZ\s*(?<id>\S+)/.exec(stdout);
	if (!match) throw new UnknownBrowserError(`Cannot find Windows browser in stdout: ${JSON.stringify(stdout)}`);
	const { id } = match.groups;
	const browser = windowsBrowserProgIds[id];
	if (!browser) throw new UnknownBrowserError(`Unknown browser ID: ${id}`);
	return browser;
}

//#endregion
//#region node_modules/.pnpm/default-browser@5.4.0/node_modules/default-browser/index.js
const execFileAsync = promisify(execFile);
const titleize = (string) => string.toLowerCase().replaceAll(/(?:^|\s|-)\S/g, (x) => x.toUpperCase());
async function defaultBrowser() {
	if (process$1.platform === "darwin") {
		const id = await defaultBrowserId();
		return {
			name: await bundleName(id),
			id
		};
	}
	if (process$1.platform === "linux") {
		const { stdout } = await execFileAsync("xdg-mime", [
			"query",
			"default",
			"x-scheme-handler/http"
		]);
		const id = stdout.trim();
		return {
			name: titleize(id.replace(/.desktop$/, "").replace("-", " ")),
			id
		};
	}
	if (process$1.platform === "win32") return defaultBrowser$1();
	throw new Error("Only macOS, Linux, and Windows are supported");
}

//#endregion
//#region node_modules/.pnpm/is-in-ssh@1.0.0/node_modules/is-in-ssh/index.js
const isInSsh = Boolean(process$1.env.SSH_CONNECTION || process$1.env.SSH_CLIENT || process$1.env.SSH_TTY);

//#endregion
//#region node_modules/.pnpm/open@11.0.0/node_modules/open/index.js
const fallbackAttemptSymbol = Symbol("fallbackAttempt");
const __dirname = import.meta.url ? path.dirname(fileURLToPath(import.meta.url)) : "";
const localXdgOpenPath = path.join(__dirname, "xdg-open");
const { platform, arch } = process$1;
const tryEachApp = async (apps, opener) => {
	if (apps.length === 0) return;
	const errors = [];
	for (const app of apps) try {
		return await opener(app);
	} catch (error) {
		errors.push(error);
	}
	throw new AggregateError(errors, "Failed to open in all supported apps");
};
const baseOpen = async (options) => {
	options = {
		wait: false,
		background: false,
		newInstance: false,
		allowNonzeroExitCode: false,
		...options
	};
	const isFallbackAttempt = options[fallbackAttemptSymbol] === true;
	delete options[fallbackAttemptSymbol];
	if (Array.isArray(options.app)) return tryEachApp(options.app, (singleApp) => baseOpen({
		...options,
		app: singleApp,
		[fallbackAttemptSymbol]: true
	}));
	let { name: app, arguments: appArguments = [] } = options.app ?? {};
	appArguments = [...appArguments];
	if (Array.isArray(app)) return tryEachApp(app, (appName) => baseOpen({
		...options,
		app: {
			name: appName,
			arguments: appArguments
		},
		[fallbackAttemptSymbol]: true
	}));
	if (app === "browser" || app === "browserPrivate") {
		const ids = {
			"com.google.chrome": "chrome",
			"google-chrome.desktop": "chrome",
			"com.brave.browser": "brave",
			"org.mozilla.firefox": "firefox",
			"firefox.desktop": "firefox",
			"com.microsoft.msedge": "edge",
			"com.microsoft.edge": "edge",
			"com.microsoft.edgemac": "edge",
			"microsoft-edge.desktop": "edge",
			"com.apple.safari": "safari"
		};
		const flags = {
			chrome: "--incognito",
			brave: "--incognito",
			firefox: "--private-window",
			edge: "--inPrivate"
		};
		let browser;
		if (is_wsl_default) {
			const progId = await wslDefaultBrowser();
			browser = _windowsBrowserProgIdMap.get(progId) ?? {};
		} else browser = await defaultBrowser();
		if (browser.id in ids) {
			const browserName = ids[browser.id.toLowerCase()];
			if (app === "browserPrivate") {
				if (browserName === "safari") throw new Error("Safari doesn't support opening in private mode via command line");
				appArguments.push(flags[browserName]);
			}
			return baseOpen({
				...options,
				app: {
					name: apps[browserName],
					arguments: appArguments
				}
			});
		}
		throw new Error(`${browser.name} is not supported as a default browser`);
	}
	let command;
	const cliArguments = [];
	const childProcessOptions = {};
	let shouldUseWindowsInWsl = false;
	if (is_wsl_default && !isInsideContainer() && !isInSsh && !app) shouldUseWindowsInWsl = await canAccessPowerShell();
	if (platform === "darwin") {
		command = "open";
		if (options.wait) cliArguments.push("--wait-apps");
		if (options.background) cliArguments.push("--background");
		if (options.newInstance) cliArguments.push("--new");
		if (app) cliArguments.push("-a", app);
	} else if (platform === "win32" || shouldUseWindowsInWsl) {
		command = await powerShellPath();
		cliArguments.push(...executePowerShell.argumentsPrefix);
		if (!is_wsl_default) childProcessOptions.windowsVerbatimArguments = true;
		if (is_wsl_default && options.target) options.target = await convertWslPathToWindows(options.target);
		const encodedArguments = ["$ProgressPreference = 'SilentlyContinue';", "Start"];
		if (options.wait) encodedArguments.push("-Wait");
		if (app) {
			encodedArguments.push(executePowerShell.escapeArgument(app));
			if (options.target) appArguments.push(options.target);
		} else if (options.target) encodedArguments.push(executePowerShell.escapeArgument(options.target));
		if (appArguments.length > 0) {
			appArguments = appArguments.map((argument) => executePowerShell.escapeArgument(argument));
			encodedArguments.push("-ArgumentList", appArguments.join(","));
		}
		options.target = executePowerShell.encodeCommand(encodedArguments.join(" "));
		if (!options.wait) childProcessOptions.stdio = "ignore";
	} else {
		if (app) command = app;
		else {
			const isBundled = !__dirname || __dirname === "/";
			let exeLocalXdgOpen = false;
			try {
				await fs$1.access(localXdgOpenPath, constants.X_OK);
				exeLocalXdgOpen = true;
			} catch {}
			command = process$1.versions.electron ?? (platform === "android" || isBundled || !exeLocalXdgOpen) ? "xdg-open" : localXdgOpenPath;
		}
		if (appArguments.length > 0) cliArguments.push(...appArguments);
		if (!options.wait) {
			childProcessOptions.stdio = "ignore";
			childProcessOptions.detached = true;
		}
	}
	if (platform === "darwin" && appArguments.length > 0) cliArguments.push("--args", ...appArguments);
	if (options.target) cliArguments.push(options.target);
	const subprocess = childProcess.spawn(command, cliArguments, childProcessOptions);
	if (options.wait) return new Promise((resolve, reject) => {
		subprocess.once("error", reject);
		subprocess.once("close", (exitCode) => {
			if (!options.allowNonzeroExitCode && exitCode !== 0) {
				reject(/* @__PURE__ */ new Error(`Exited with code ${exitCode}`));
				return;
			}
			resolve(subprocess);
		});
	});
	if (isFallbackAttempt) return new Promise((resolve, reject) => {
		subprocess.once("error", reject);
		subprocess.once("spawn", () => {
			subprocess.once("close", (exitCode) => {
				subprocess.off("error", reject);
				if (exitCode !== 0) {
					reject(/* @__PURE__ */ new Error(`Exited with code ${exitCode}`));
					return;
				}
				subprocess.unref();
				resolve(subprocess);
			});
		});
	});
	subprocess.unref();
	return new Promise((resolve, reject) => {
		subprocess.once("error", reject);
		subprocess.once("spawn", () => {
			subprocess.off("error", reject);
			resolve(subprocess);
		});
	});
};
const open = (target, options) => {
	if (typeof target !== "string") throw new TypeError("Expected a `target`");
	return baseOpen({
		...options,
		target
	});
};
function detectArchBinary(binary) {
	if (typeof binary === "string" || Array.isArray(binary)) return binary;
	const { [arch]: archBinary } = binary;
	if (!archBinary) throw new Error(`${arch} is not supported`);
	return archBinary;
}
function detectPlatformBinary({ [platform]: platformBinary }, { wsl } = {}) {
	if (wsl && is_wsl_default) return detectArchBinary(wsl);
	if (!platformBinary) throw new Error(`${platform} is not supported`);
	return detectArchBinary(platformBinary);
}
const apps = {
	browser: "browser",
	browserPrivate: "browserPrivate"
};
defineLazyProperty(apps, "chrome", () => detectPlatformBinary({
	darwin: "google chrome",
	win32: "chrome",
	linux: [
		"google-chrome",
		"google-chrome-stable",
		"chromium",
		"chromium-browser"
	]
}, { wsl: {
	ia32: "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
	x64: ["/mnt/c/Program Files/Google/Chrome/Application/chrome.exe", "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"]
} }));
defineLazyProperty(apps, "brave", () => detectPlatformBinary({
	darwin: "brave browser",
	win32: "brave",
	linux: ["brave-browser", "brave"]
}, { wsl: {
	ia32: "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe",
	x64: ["/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe", "/mnt/c/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"]
} }));
defineLazyProperty(apps, "firefox", () => detectPlatformBinary({
	darwin: "firefox",
	win32: String.raw`C:\Program Files\Mozilla Firefox\firefox.exe`,
	linux: "firefox"
}, { wsl: "/mnt/c/Program Files/Mozilla Firefox/firefox.exe" }));
defineLazyProperty(apps, "edge", () => detectPlatformBinary({
	darwin: "microsoft edge",
	win32: "msedge",
	linux: ["microsoft-edge", "microsoft-edge-dev"]
}, { wsl: "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" }));
defineLazyProperty(apps, "safari", () => detectPlatformBinary({ darwin: "Safari" }));

//#endregion
//#region node_modules/.pnpm/pathe@2.0.3/node_modules/pathe/dist/shared/pathe.M-eThtNZ.mjs
const _DRIVE_LETTER_START_RE = /^[A-Za-z]:\//;
function normalizeWindowsPath(input = "") {
	if (!input) return input;
	return input.replace(/\\/g, "/").replace(_DRIVE_LETTER_START_RE, (r) => r.toUpperCase());
}
const _UNC_REGEX = /^[/\\]{2}/;
const _IS_ABSOLUTE_RE = /^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[A-Za-z]:[/\\]/;
const _DRIVE_LETTER_RE = /^[A-Za-z]:$/;
const _ROOT_FOLDER_RE = /^\/([A-Za-z]:)?$/;
const normalize$3 = function(path) {
	if (path.length === 0) return ".";
	path = normalizeWindowsPath(path);
	const isUNCPath = path.match(_UNC_REGEX);
	const isPathAbsolute = isAbsolute$2(path);
	const trailingSeparator = path[path.length - 1] === "/";
	path = normalizeString$2(path, !isPathAbsolute);
	if (path.length === 0) {
		if (isPathAbsolute) return "/";
		return trailingSeparator ? "./" : ".";
	}
	if (trailingSeparator) path += "/";
	if (_DRIVE_LETTER_RE.test(path)) path += "/";
	if (isUNCPath) {
		if (!isPathAbsolute) return `//./${path}`;
		return `//${path}`;
	}
	return isPathAbsolute && !isAbsolute$2(path) ? `/${path}` : path;
};
const join$2 = function(...segments) {
	let path = "";
	for (const seg of segments) {
		if (!seg) continue;
		if (path.length > 0) {
			const pathTrailing = path[path.length - 1] === "/";
			const segLeading = seg[0] === "/";
			if (pathTrailing && segLeading) path += seg.slice(1);
			else path += pathTrailing || segLeading ? seg : `/${seg}`;
		} else path += seg;
	}
	return normalize$3(path);
};
function cwd() {
	if (typeof process !== "undefined" && typeof process.cwd === "function") return process.cwd().replace(/\\/g, "/");
	return "/";
}
const resolve$3 = function(...arguments_) {
	arguments_ = arguments_.map((argument) => normalizeWindowsPath(argument));
	let resolvedPath = "";
	let resolvedAbsolute = false;
	for (let index = arguments_.length - 1; index >= -1 && !resolvedAbsolute; index--) {
		const path = index >= 0 ? arguments_[index] : cwd();
		if (!path || path.length === 0) continue;
		resolvedPath = `${path}/${resolvedPath}`;
		resolvedAbsolute = isAbsolute$2(path);
	}
	resolvedPath = normalizeString$2(resolvedPath, !resolvedAbsolute);
	if (resolvedAbsolute && !isAbsolute$2(resolvedPath)) return `/${resolvedPath}`;
	return resolvedPath.length > 0 ? resolvedPath : ".";
};
function normalizeString$2(path, allowAboveRoot) {
	let res = "";
	let lastSegmentLength = 0;
	let lastSlash = -1;
	let dots = 0;
	let char = null;
	for (let index = 0; index <= path.length; ++index) {
		if (index < path.length) char = path[index];
		else if (char === "/") break;
		else char = "/";
		if (char === "/") {
			if (lastSlash === index - 1 || dots === 1);
			else if (dots === 2) {
				if (res.length < 2 || lastSegmentLength !== 2 || res[res.length - 1] !== "." || res[res.length - 2] !== ".") {
					if (res.length > 2) {
						const lastSlashIndex = res.lastIndexOf("/");
						if (lastSlashIndex === -1) {
							res = "";
							lastSegmentLength = 0;
						} else {
							res = res.slice(0, lastSlashIndex);
							lastSegmentLength = res.length - 1 - res.lastIndexOf("/");
						}
						lastSlash = index;
						dots = 0;
						continue;
					} else if (res.length > 0) {
						res = "";
						lastSegmentLength = 0;
						lastSlash = index;
						dots = 0;
						continue;
					}
				}
				if (allowAboveRoot) {
					res += res.length > 0 ? "/.." : "..";
					lastSegmentLength = 2;
				}
			} else {
				if (res.length > 0) res += `/${path.slice(lastSlash + 1, index)}`;
				else res = path.slice(lastSlash + 1, index);
				lastSegmentLength = index - lastSlash - 1;
			}
			lastSlash = index;
			dots = 0;
		} else if (char === "." && dots !== -1) ++dots;
		else dots = -1;
	}
	return res;
}
const isAbsolute$2 = function(p) {
	return _IS_ABSOLUTE_RE.test(p);
};
const relative$2 = function(from, to) {
	const _from = resolve$3(from).replace(_ROOT_FOLDER_RE, "$1").split("/");
	const _to = resolve$3(to).replace(_ROOT_FOLDER_RE, "$1").split("/");
	if (_to[0][1] === ":" && _from[0][1] === ":" && _from[0] !== _to[0]) return _to.join("/");
	const _fromCopy = [..._from];
	for (const segment of _fromCopy) {
		if (_to[0] !== segment) break;
		_from.shift();
		_to.shift();
	}
	return [..._from.map(() => ".."), ..._to].join("/");
};
const dirname$2 = function(p) {
	const segments = normalizeWindowsPath(p).replace(/\/$/, "").split("/").slice(0, -1);
	if (segments.length === 1 && _DRIVE_LETTER_RE.test(segments[0])) segments[0] += "/";
	return segments.join("/") || (isAbsolute$2(p) ? "/" : ".");
};
const basename$2 = function(p, extension) {
	const segments = normalizeWindowsPath(p).split("/");
	let lastSegment = "";
	for (let i = segments.length - 1; i >= 0; i--) {
		const val = segments[i];
		if (val) {
			lastSegment = val;
			break;
		}
	}
	return extension && lastSegment.endsWith(extension) ? lastSegment.slice(0, -extension.length) : lastSegment;
};

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/providers/async.js
var require_async$3 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.AsyncProvider = void 0;
	var AsyncProvider = class {
		#reader;
		constructor(reader) {
			this.#reader = reader;
		}
		read(root, callback) {
			const entries = [];
			this.#reader.onError((error) => {
				callFailureCallback(callback, error);
			});
			this.#reader.onEntry((entry) => {
				entries.push(entry);
			});
			this.#reader.onEnd(() => {
				callSuccessCallback(callback, entries);
			});
			this.#reader.read(root);
		}
	};
	exports.AsyncProvider = AsyncProvider;
	function callFailureCallback(callback, error) {
		callback(error);
	}
	function callSuccessCallback(callback, entries) {
		callback(null, entries);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/providers/stream.js
var require_stream = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.StreamProvider = void 0;
	const node_stream_1 = __require("node:stream");
	var StreamProvider = class {
		#reader;
		#stream;
		constructor(reader) {
			this.#reader = reader;
			this.#stream = this.#createOutputStream();
		}
		read(root) {
			this.#reader.onError((error) => {
				this.#stream.emit("error", error);
			});
			this.#reader.onEntry((entry) => {
				this.#stream.push(entry);
			});
			this.#reader.onEnd(() => {
				this.#stream.push(null);
			});
			this.#reader.read(root);
			return this.#stream;
		}
		#createOutputStream() {
			return new node_stream_1.Readable({
				objectMode: true,
				read: () => {},
				destroy: (error, callback) => {
					if (!this.#reader.isDestroyed) this.#reader.destroy();
					callback(error);
				}
			});
		}
	};
	exports.StreamProvider = StreamProvider;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/providers/sync.js
var require_sync$3 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.SyncProvider = void 0;
	var SyncProvider = class {
		#reader;
		constructor(reader) {
			this.#reader = reader;
		}
		read(root) {
			return this.#reader.read(root);
		}
	};
	exports.SyncProvider = SyncProvider;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/providers/index.js
var require_providers = /* @__PURE__ */ __commonJSMin(((exports) => {
	var __createBinding = exports && exports.__createBinding || (Object.create ? (function(o, m, k, k2) {
		if (k2 === void 0) k2 = k;
		var desc = Object.getOwnPropertyDescriptor(m, k);
		if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) desc = {
			enumerable: true,
			get: function() {
				return m[k];
			}
		};
		Object.defineProperty(o, k2, desc);
	}) : (function(o, m, k, k2) {
		if (k2 === void 0) k2 = k;
		o[k2] = m[k];
	}));
	var __exportStar = exports && exports.__exportStar || function(m, exports$2) {
		for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports$2, p)) __createBinding(exports$2, m, p);
	};
	Object.defineProperty(exports, "__esModule", { value: true });
	__exportStar(require_async$3(), exports);
	__exportStar(require_stream(), exports);
	__exportStar(require_sync$3(), exports);
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/providers/async.js
var require_async$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.read = read;
	function read(path, settings, callback) {
		settings.fs.lstat(path, (lstatError, lstat) => {
			if (lstatError !== null) {
				callFailureCallback(callback, lstatError);
				return;
			}
			if (!lstat.isSymbolicLink() || !settings.followSymbolicLink) {
				callSuccessCallback(callback, lstat);
				return;
			}
			settings.fs.stat(path, (statError, stat) => {
				if (statError !== null) {
					if (settings.throwErrorOnBrokenSymbolicLink) {
						callFailureCallback(callback, statError);
						return;
					}
					callSuccessCallback(callback, lstat);
					return;
				}
				if (settings.markSymbolicLink) stat.isSymbolicLink = () => true;
				callSuccessCallback(callback, stat);
			});
		});
	}
	function callFailureCallback(callback, error) {
		callback(error);
	}
	function callSuccessCallback(callback, result) {
		callback(null, result);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/providers/sync.js
var require_sync$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.read = read;
	function read(path, settings) {
		const lstat = settings.fs.lstatSync(path);
		if (!lstat.isSymbolicLink() || !settings.followSymbolicLink) return lstat;
		try {
			const stat = settings.fs.statSync(path);
			if (settings.markSymbolicLink) stat.isSymbolicLink = () => true;
			return stat;
		} catch (error) {
			if (!settings.throwErrorOnBrokenSymbolicLink) return lstat;
			throw error;
		}
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/adapters/fs.js
var require_fs$3 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.FILE_SYSTEM_ADAPTER = void 0;
	exports.createFileSystemAdapter = createFileSystemAdapter;
	const fs$4 = __require("node:fs");
	exports.FILE_SYSTEM_ADAPTER = {
		lstat: fs$4.lstat,
		stat: fs$4.stat,
		lstatSync: fs$4.lstatSync,
		statSync: fs$4.statSync
	};
	function createFileSystemAdapter(fsMethods) {
		if (fsMethods === void 0) return exports.FILE_SYSTEM_ADAPTER;
		return {
			...exports.FILE_SYSTEM_ADAPTER,
			...fsMethods
		};
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/settings.js
var require_settings$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = void 0;
	const fs = require_fs$3();
	var Settings = class {
		followSymbolicLink;
		fs;
		markSymbolicLink;
		throwErrorOnBrokenSymbolicLink;
		constructor(options = {}) {
			this.followSymbolicLink = options.followSymbolicLink ?? true;
			this.fs = fs.createFileSystemAdapter(options.fs);
			this.markSymbolicLink = options.markSymbolicLink ?? false;
			this.throwErrorOnBrokenSymbolicLink = options.throwErrorOnBrokenSymbolicLink ?? true;
		}
	};
	exports.Settings = Settings;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/stat.js
var require_stat = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.stat = stat;
	exports.statSync = statSync;
	const async = require_async$2();
	const sync = require_sync$2();
	const settings_1 = require_settings$2();
	function stat(path, optionsOrSettingsOrCallback, callback) {
		if (typeof optionsOrSettingsOrCallback === "function") {
			async.read(path, getSettings(), optionsOrSettingsOrCallback);
			return;
		}
		async.read(path, getSettings(optionsOrSettingsOrCallback), callback);
	}
	function statSync(path, optionsOrSettings) {
		const settings = getSettings(optionsOrSettings);
		return sync.read(path, settings);
	}
	function getSettings(settingsOrOptions = {}) {
		if (settingsOrOptions instanceof settings_1.Settings) return settingsOrOptions;
		return new settings_1.Settings(settingsOrOptions);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.stat@4.0.0/node_modules/@nodelib/fs.stat/out/index.js
var require_out$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = exports.statSync = exports.stat = void 0;
	var stat_1 = require_stat();
	Object.defineProperty(exports, "stat", {
		enumerable: true,
		get: function() {
			return stat_1.stat;
		}
	});
	Object.defineProperty(exports, "statSync", {
		enumerable: true,
		get: function() {
			return stat_1.statSync;
		}
	});
	var settings_1 = require_settings$2();
	Object.defineProperty(exports, "Settings", {
		enumerable: true,
		get: function() {
			return settings_1.Settings;
		}
	});
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/adapters/fs.js
var require_fs$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.FILE_SYSTEM_ADAPTER = void 0;
	exports.createFileSystemAdapter = createFileSystemAdapter;
	const fs$3 = __require("node:fs");
	exports.FILE_SYSTEM_ADAPTER = {
		lstat: fs$3.lstat,
		stat: fs$3.stat,
		lstatSync: fs$3.lstatSync,
		statSync: fs$3.statSync,
		readdir: fs$3.readdir,
		readdirSync: fs$3.readdirSync
	};
	function createFileSystemAdapter(fsMethods) {
		if (fsMethods === void 0) return exports.FILE_SYSTEM_ADAPTER;
		return {
			...exports.FILE_SYSTEM_ADAPTER,
			...fsMethods
		};
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/settings.js
var require_settings$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = void 0;
	const path$3 = __require("node:path");
	const fsStat = require_out$2();
	const fs = require_fs$2();
	var Settings = class {
		followSymbolicLinks;
		fs;
		pathSegmentSeparator;
		stats;
		throwErrorOnBrokenSymbolicLink;
		fsStatSettings;
		constructor(options = {}) {
			this.followSymbolicLinks = options.followSymbolicLinks ?? false;
			this.fs = fs.createFileSystemAdapter(options.fs);
			this.pathSegmentSeparator = options.pathSegmentSeparator ?? path$3.sep;
			this.stats = options.stats ?? false;
			this.throwErrorOnBrokenSymbolicLink = options.throwErrorOnBrokenSymbolicLink ?? true;
			this.fsStatSettings = new fsStat.Settings({
				followSymbolicLink: this.followSymbolicLinks,
				fs: this.fs,
				throwErrorOnBrokenSymbolicLink: this.throwErrorOnBrokenSymbolicLink
			});
		}
	};
	exports.Settings = Settings;
}));

//#endregion
//#region node_modules/.pnpm/queue-microtask@1.2.3/node_modules/queue-microtask/index.js
var require_queue_microtask = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/*! queue-microtask. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */
	let promise;
	module.exports = typeof queueMicrotask === "function" ? queueMicrotask.bind(typeof window !== "undefined" ? window : global) : (cb) => (promise || (promise = Promise.resolve())).then(cb).catch((err) => setTimeout(() => {
		throw err;
	}, 0));
}));

//#endregion
//#region node_modules/.pnpm/run-parallel@1.2.0/node_modules/run-parallel/index.js
var require_run_parallel = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/*! run-parallel. MIT License. Feross Aboukhadijeh <https://feross.org/opensource> */
	module.exports = runParallel;
	const queueMicrotask = require_queue_microtask();
	function runParallel(tasks, cb) {
		let results, pending, keys;
		let isSync = true;
		if (Array.isArray(tasks)) {
			results = [];
			pending = tasks.length;
		} else {
			keys = Object.keys(tasks);
			results = {};
			pending = keys.length;
		}
		function done(err) {
			function end() {
				if (cb) cb(err, results);
				cb = null;
			}
			if (isSync) queueMicrotask(end);
			else end();
		}
		function each(i, err, result) {
			results[i] = result;
			if (--pending === 0 || err) done(err);
		}
		if (!pending) done(null);
		else if (keys) keys.forEach(function(key) {
			tasks[key](function(err, result) {
				each(key, err, result);
			});
		});
		else tasks.forEach(function(task, i) {
			task(function(err, result) {
				each(i, err, result);
			});
		});
		isSync = false;
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/utils/fs.js
var require_fs$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.DirentFromStats = void 0;
	exports.createDirentFromStats = createDirentFromStats;
	const fs$2 = __require("node:fs");
	const kStats = Symbol("stats");
	function createDirentFromStats(name, stats, parentPath) {
		return new DirentFromStats(name, stats, parentPath);
	}
	var DirentFromStats = class extends fs$2.Dirent {
		[kStats];
		constructor(name, stats, parentPath) {
			super(name, null, parentPath);
			this[kStats] = stats;
		}
	};
	exports.DirentFromStats = DirentFromStats;
	for (const key of Reflect.ownKeys(fs$2.Dirent.prototype)) {
		const name = key;
		const descriptor = Object.getOwnPropertyDescriptor(fs$2.Dirent.prototype, name);
		if (descriptor?.writable === false || descriptor?.set === void 0) continue;
		DirentFromStats.prototype[name] = function() {
			return this[kStats][name]();
		};
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/utils/index.js
var require_utils = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.fs = void 0;
	exports.fs = require_fs$1();
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/providers/common.js
var require_common$2 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.joinPathSegments = joinPathSegments;
	function joinPathSegments(a, b, separator) {
		/**
		* The correct handling of cases when the first segment is a root (`/`, `C:/`) or UNC path (`//?/C:/`).
		*/
		if (a.endsWith(separator)) return a + b;
		return a + separator + b;
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/providers/async.js
var require_async$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.read = read;
	const fsStat = require_out$2();
	const rpl = require_run_parallel();
	const utils = require_utils();
	const common = require_common$2();
	function read(directory, settings, callback) {
		settings.fs.readdir(directory, { withFileTypes: true }, (readdirError, dirents) => {
			if (readdirError !== null) {
				callFailureCallback(callback, readdirError);
				return;
			}
			const entries = dirents.map((dirent) => ({
				dirent,
				name: dirent.name,
				path: common.joinPathSegments(directory, dirent.name, settings.pathSegmentSeparator)
			}));
			if (!settings.stats && !settings.followSymbolicLinks) {
				callSuccessCallback(callback, entries);
				return;
			}
			rpl(makeRplTasks(directory, entries, settings), (rplError) => {
				if (rplError !== null) {
					callFailureCallback(callback, rplError);
					return;
				}
				callSuccessCallback(callback, entries);
			});
		});
	}
	function makeRplTasks(directory, entries, settings) {
		const tasks = [];
		for (const entry of entries) {
			const task = makeRplTask(directory, entry, settings);
			if (task !== void 0) tasks.push(task);
		}
		return tasks;
	}
	/**
	* The task mutates the incoming entry object depending on the settings.
	* Returns the task, or undefined if the task is empty.
	*/
	function makeRplTask(directory, entry, settings) {
		const action = getStatsAction(entry, settings);
		if (action === void 0) return;
		return (done) => {
			action((error, stats) => {
				if (error !== null) {
					done(settings.throwErrorOnBrokenSymbolicLink ? error : null);
					return;
				}
				if (settings.stats) entry.stats = stats;
				if (settings.followSymbolicLinks) entry.dirent = utils.fs.createDirentFromStats(entry.name, stats, directory);
				done(null, entry);
			});
		};
	}
	function getStatsAction(entry, settings) {
		if (settings.stats) return (callback) => {
			fsStat.stat(entry.path, settings.fsStatSettings, callback);
		};
		if (settings.followSymbolicLinks && entry.dirent.isSymbolicLink()) return (callback) => {
			settings.fs.stat(entry.path, callback);
		};
	}
	function callFailureCallback(callback, error) {
		callback(error);
	}
	function callSuccessCallback(callback, result) {
		callback(null, result);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/providers/sync.js
var require_sync$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.read = read;
	const fsStat = require_out$2();
	const utils = require_utils();
	const common = require_common$2();
	function read(directory, settings) {
		return settings.fs.readdirSync(directory, { withFileTypes: true }).map((dirent) => {
			const entry = {
				dirent,
				name: dirent.name,
				path: common.joinPathSegments(directory, dirent.name, settings.pathSegmentSeparator)
			};
			if (settings.stats) entry.stats = fsStat.statSync(entry.path, settings.fsStatSettings);
			if (settings.followSymbolicLinks && entry.dirent.isSymbolicLink()) try {
				const stats = entry.stats ?? settings.fs.statSync(entry.path);
				entry.dirent = utils.fs.createDirentFromStats(entry.name, stats, directory);
			} catch (error) {
				if (settings.throwErrorOnBrokenSymbolicLink) throw error;
			}
			return entry;
		});
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/scandir.js
var require_scandir = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.scandir = scandir;
	exports.scandirSync = scandirSync;
	const settings_1 = require_settings$1();
	const async = require_async$1();
	const sync = require_sync$1();
	function scandir(path, optionsOrSettingsOrCallback, callback) {
		if (typeof optionsOrSettingsOrCallback === "function") {
			async.read(path, getSettings(), optionsOrSettingsOrCallback);
			return;
		}
		async.read(path, getSettings(optionsOrSettingsOrCallback), callback);
	}
	function scandirSync(path, optionsOrSettings) {
		const settings = getSettings(optionsOrSettings);
		return sync.read(path, settings);
	}
	function getSettings(settingsOrOptions = {}) {
		if (settingsOrOptions instanceof settings_1.Settings) return settingsOrOptions;
		return new settings_1.Settings(settingsOrOptions);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.scandir@4.0.1/node_modules/@nodelib/fs.scandir/out/index.js
var require_out$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = exports.scandirSync = exports.scandir = void 0;
	var scandir_1 = require_scandir();
	Object.defineProperty(exports, "scandir", {
		enumerable: true,
		get: function() {
			return scandir_1.scandir;
		}
	});
	Object.defineProperty(exports, "scandirSync", {
		enumerable: true,
		get: function() {
			return scandir_1.scandirSync;
		}
	});
	var settings_1 = require_settings$1();
	Object.defineProperty(exports, "Settings", {
		enumerable: true,
		get: function() {
			return settings_1.Settings;
		}
	});
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/settings.js
var require_settings = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = void 0;
	const path$2 = __require("node:path");
	const fsScandir = require_out$1();
	var Settings = class {
		basePath;
		concurrency;
		deepFilter;
		entryFilter;
		errorFilter;
		pathSegmentSeparator;
		fsScandirSettings;
		signal;
		constructor(options = {}) {
			this.basePath = options.basePath ?? void 0;
			this.concurrency = options.concurrency ?? Number.POSITIVE_INFINITY;
			this.deepFilter = options.deepFilter ?? null;
			this.entryFilter = options.entryFilter ?? null;
			this.errorFilter = options.errorFilter ?? null;
			this.pathSegmentSeparator = options.pathSegmentSeparator ?? path$2.sep;
			this.signal = options.signal;
			this.fsScandirSettings = new fsScandir.Settings({
				followSymbolicLinks: options.followSymbolicLinks,
				fs: options.fs,
				pathSegmentSeparator: this.pathSegmentSeparator,
				stats: options.stats,
				throwErrorOnBrokenSymbolicLink: options.throwErrorOnBrokenSymbolicLink
			});
		}
	};
	exports.Settings = Settings;
}));

//#endregion
//#region node_modules/.pnpm/reusify@1.1.0/node_modules/reusify/reusify.js
var require_reusify = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	function reusify(Constructor) {
		var head = new Constructor();
		var tail = head;
		function get() {
			var current = head;
			if (current.next) head = current.next;
			else {
				head = new Constructor();
				tail = head;
			}
			current.next = null;
			return current;
		}
		function release(obj) {
			tail.next = obj;
			tail = obj;
		}
		return {
			get,
			release
		};
	}
	module.exports = reusify;
}));

//#endregion
//#region node_modules/.pnpm/fastq@1.19.1/node_modules/fastq/queue.js
var require_queue = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	var reusify = require_reusify();
	function fastqueue(context, worker, _concurrency) {
		if (typeof context === "function") {
			_concurrency = worker;
			worker = context;
			context = null;
		}
		if (!(_concurrency >= 1)) throw new Error("fastqueue concurrency must be equal to or greater than 1");
		var cache = reusify(Task);
		var queueHead = null;
		var queueTail = null;
		var _running = 0;
		var errorHandler = null;
		var self = {
			push,
			drain: noop,
			saturated: noop,
			pause,
			paused: false,
			get concurrency() {
				return _concurrency;
			},
			set concurrency(value) {
				if (!(value >= 1)) throw new Error("fastqueue concurrency must be equal to or greater than 1");
				_concurrency = value;
				if (self.paused) return;
				for (; queueHead && _running < _concurrency;) {
					_running++;
					release();
				}
			},
			running,
			resume,
			idle,
			length,
			getQueue,
			unshift,
			empty: noop,
			kill,
			killAndDrain,
			error
		};
		return self;
		function running() {
			return _running;
		}
		function pause() {
			self.paused = true;
		}
		function length() {
			var current = queueHead;
			var counter = 0;
			while (current) {
				current = current.next;
				counter++;
			}
			return counter;
		}
		function getQueue() {
			var current = queueHead;
			var tasks = [];
			while (current) {
				tasks.push(current.value);
				current = current.next;
			}
			return tasks;
		}
		function resume() {
			if (!self.paused) return;
			self.paused = false;
			if (queueHead === null) {
				_running++;
				release();
				return;
			}
			for (; queueHead && _running < _concurrency;) {
				_running++;
				release();
			}
		}
		function idle() {
			return _running === 0 && self.length() === 0;
		}
		function push(value, done) {
			var current = cache.get();
			current.context = context;
			current.release = release;
			current.value = value;
			current.callback = done || noop;
			current.errorHandler = errorHandler;
			if (_running >= _concurrency || self.paused) if (queueTail) {
				queueTail.next = current;
				queueTail = current;
			} else {
				queueHead = current;
				queueTail = current;
				self.saturated();
			}
			else {
				_running++;
				worker.call(context, current.value, current.worked);
			}
		}
		function unshift(value, done) {
			var current = cache.get();
			current.context = context;
			current.release = release;
			current.value = value;
			current.callback = done || noop;
			current.errorHandler = errorHandler;
			if (_running >= _concurrency || self.paused) if (queueHead) {
				current.next = queueHead;
				queueHead = current;
			} else {
				queueHead = current;
				queueTail = current;
				self.saturated();
			}
			else {
				_running++;
				worker.call(context, current.value, current.worked);
			}
		}
		function release(holder) {
			if (holder) cache.release(holder);
			var next = queueHead;
			if (next && _running <= _concurrency) if (!self.paused) {
				if (queueTail === queueHead) queueTail = null;
				queueHead = next.next;
				next.next = null;
				worker.call(context, next.value, next.worked);
				if (queueTail === null) self.empty();
			} else _running--;
			else if (--_running === 0) self.drain();
		}
		function kill() {
			queueHead = null;
			queueTail = null;
			self.drain = noop;
		}
		function killAndDrain() {
			queueHead = null;
			queueTail = null;
			self.drain();
			self.drain = noop;
		}
		function error(handler) {
			errorHandler = handler;
		}
	}
	function noop() {}
	function Task() {
		this.value = null;
		this.callback = noop;
		this.next = null;
		this.release = noop;
		this.context = null;
		this.errorHandler = null;
		var self = this;
		this.worked = function worked(err, result) {
			var callback = self.callback;
			var errorHandler = self.errorHandler;
			var val = self.value;
			self.value = null;
			self.callback = noop;
			if (self.errorHandler) errorHandler(err, val);
			callback.call(self.context, err, result);
			self.release(self);
		};
	}
	function queueAsPromised(context, worker, _concurrency) {
		if (typeof context === "function") {
			_concurrency = worker;
			worker = context;
			context = null;
		}
		function asyncWrapper(arg, cb) {
			worker.call(this, arg).then(function(res) {
				cb(null, res);
			}, cb);
		}
		var queue = fastqueue(context, asyncWrapper, _concurrency);
		var pushCb = queue.push;
		var unshiftCb = queue.unshift;
		queue.push = push;
		queue.unshift = unshift;
		queue.drained = drained;
		return queue;
		function push(value) {
			var p = new Promise(function(resolve, reject) {
				pushCb(value, function(err, result) {
					if (err) {
						reject(err);
						return;
					}
					resolve(result);
				});
			});
			p.catch(noop);
			return p;
		}
		function unshift(value) {
			var p = new Promise(function(resolve, reject) {
				unshiftCb(value, function(err, result) {
					if (err) {
						reject(err);
						return;
					}
					resolve(result);
				});
			});
			p.catch(noop);
			return p;
		}
		function drained() {
			return new Promise(function(resolve) {
				process.nextTick(function() {
					if (queue.idle()) resolve();
					else {
						var previousDrain = queue.drain;
						queue.drain = function() {
							if (typeof previousDrain === "function") previousDrain();
							resolve();
							queue.drain = previousDrain;
						};
					}
				});
			});
		}
	}
	module.exports = fastqueue;
	module.exports.promise = queueAsPromised;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/readers/common.js
var require_common$1 = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.isFatalError = isFatalError;
	exports.isAppliedFilter = isAppliedFilter;
	exports.replacePathSegmentSeparator = replacePathSegmentSeparator;
	exports.joinPathSegments = joinPathSegments;
	function isFatalError(settings, error) {
		if (settings.errorFilter === null) return true;
		return !settings.errorFilter(error);
	}
	function isAppliedFilter(filter, value) {
		return filter === null || filter(value);
	}
	function replacePathSegmentSeparator(filepath, separator) {
		return filepath.split(/[/\\]/).join(separator);
	}
	function joinPathSegments(a, b, separator) {
		if (a === "") return b;
		/**
		* The correct handling of cases when the first segment is a root (`/`, `C:/`) or UNC path (`//?/C:/`).
		*/
		if (a.endsWith(separator)) return a + b;
		return a + separator + b;
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/readers/async.js
var require_async = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.AsyncReader = void 0;
	const node_events_1 = __require("node:events");
	const fastq = require_queue();
	const common = require_common$1();
	var AsyncReaderEmitter = class {
		#emitter = new node_events_1.EventEmitter();
		onEntry(callback) {
			this.#emitter.on("entry", callback);
		}
		onError(callback) {
			this.#emitter.once("error", callback);
		}
		onEnd(callback) {
			this.#emitter.once("end", callback);
		}
		_emitEntry(entry) {
			this.#emitter.emit("entry", entry);
		}
		_emitEnd() {
			this.#emitter.emit("end");
		}
		_emitError(error) {
			this.#emitter.emit("error", error);
		}
	};
	var AsyncReader = class extends AsyncReaderEmitter {
		#isFatalError = false;
		#isDestroyed = false;
		#fs;
		#settings;
		#queue;
		constructor(fs, settings) {
			super();
			const queue = fastq(this.#worker.bind(this), settings.concurrency);
			queue.drain = () => {
				if (!this.#isFatalError) this._emitEnd();
			};
			this.#fs = fs;
			this.#settings = settings;
			this.#queue = queue;
		}
		read(root) {
			this.#isFatalError = false;
			this.#isDestroyed = false;
			this.#attachAbortSignal();
			const directory = common.replacePathSegmentSeparator(root, this.#settings.pathSegmentSeparator);
			this.#pushToQueue(directory, this.#settings.basePath);
		}
		get isDestroyed() {
			return this.#isDestroyed;
		}
		destroy() {
			if (this.#isDestroyed) return;
			this.#isDestroyed = true;
			this.#queue.killAndDrain();
		}
		#attachAbortSignal() {
			const signal = this.#settings.signal;
			if (signal?.aborted === true) this.#handleError(signal.reason);
			signal?.addEventListener("abort", () => {
				this.#handleError(signal.reason);
			}, { once: true });
		}
		#pushToQueue(directory, base) {
			this.#queue.push({
				directory,
				base
			}, (error) => {
				if (error !== null) this.#handleError(error);
			});
		}
		#worker(item, done) {
			this.#fs.scandir(item.directory, this.#settings.fsScandirSettings, (error, entries) => {
				if (error !== null) {
					done(error, void 0);
					return;
				}
				/**
				* The user can define their own custom filtering and error handling functions.
				* If the user throws an error, we need to catch it and emit it to the user error handler.
				*
				* Without this, the error will be thrown immediately bypassing the error handler.
				*/
				try {
					for (const entry of entries) this.#handleEntry(entry, item.base);
				} catch (error) {
					done(error, void 0);
					return;
				}
				done(null, void 0);
			});
		}
		#handleError(error) {
			if (this.#isDestroyed || !common.isFatalError(this.#settings, error)) return;
			this.#isFatalError = true;
			this.#isDestroyed = true;
			this._emitError(error);
		}
		#handleEntry(entry, base) {
			if (this.#isDestroyed || this.#isFatalError) return;
			const fullpath = entry.path;
			if (base !== void 0) entry.path = common.joinPathSegments(base, entry.name, this.#settings.pathSegmentSeparator);
			if (common.isAppliedFilter(this.#settings.entryFilter, entry)) this._emitEntry(entry);
			if (entry.dirent.isDirectory() && common.isAppliedFilter(this.#settings.deepFilter, entry)) this.#pushToQueue(fullpath, base === void 0 ? void 0 : entry.path);
		}
	};
	exports.AsyncReader = AsyncReader;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/readers/sync.js
var require_sync = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.SyncReader = void 0;
	const common = require_common$1();
	var SyncReader = class {
		#fs;
		#settings;
		#queue = /* @__PURE__ */ new Set();
		#storage = [];
		constructor(fs, settings) {
			this.#fs = fs;
			this.#settings = settings;
		}
		read(root) {
			const directory = common.replacePathSegmentSeparator(root, this.#settings.pathSegmentSeparator);
			this.#pushToQueue(directory, this.#settings.basePath);
			this.#handleQueue();
			return this.#storage;
		}
		#pushToQueue(directory, base) {
			this.#queue.add({
				directory,
				base
			});
		}
		#handleQueue() {
			for (const item of this.#queue.values()) this.#handleDirectory(item.directory, item.base);
		}
		#handleDirectory(directory, base) {
			try {
				const entries = this.#fs.scandirSync(directory, this.#settings.fsScandirSettings);
				for (const entry of entries) this.#handleEntry(entry, base);
			} catch (error) {
				this.#handleError(error);
			}
		}
		#handleError(error) {
			if (common.isFatalError(this.#settings, error)) throw error;
		}
		#handleEntry(entry, base) {
			const fullpath = entry.path;
			if (base !== void 0) entry.path = common.joinPathSegments(base, entry.name, this.#settings.pathSegmentSeparator);
			if (common.isAppliedFilter(this.#settings.entryFilter, entry)) this.#pushToStorage(entry);
			if (entry.dirent.isDirectory() && common.isAppliedFilter(this.#settings.deepFilter, entry)) this.#pushToQueue(fullpath, base === void 0 ? void 0 : entry.path);
		}
		#pushToStorage(entry) {
			this.#storage.push(entry);
		}
	};
	exports.SyncReader = SyncReader;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/readers/index.js
var require_readers = /* @__PURE__ */ __commonJSMin(((exports) => {
	var __createBinding = exports && exports.__createBinding || (Object.create ? (function(o, m, k, k2) {
		if (k2 === void 0) k2 = k;
		var desc = Object.getOwnPropertyDescriptor(m, k);
		if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) desc = {
			enumerable: true,
			get: function() {
				return m[k];
			}
		};
		Object.defineProperty(o, k2, desc);
	}) : (function(o, m, k, k2) {
		if (k2 === void 0) k2 = k;
		o[k2] = m[k];
	}));
	var __exportStar = exports && exports.__exportStar || function(m, exports$1) {
		for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports$1, p)) __createBinding(exports$1, m, p);
	};
	Object.defineProperty(exports, "__esModule", { value: true });
	__exportStar(require_async(), exports);
	__exportStar(require_sync(), exports);
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/adapters/fs.js
var require_fs = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.FileSystemAdapter = void 0;
	const fsScandir = require_out$1();
	var FileSystemAdapter = class {
		scandir = fsScandir.scandir;
		scandirSync = fsScandir.scandirSync;
	};
	exports.FileSystemAdapter = FileSystemAdapter;
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/walk.js
var require_walk = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.walk = walk;
	exports.walkSync = walkSync;
	exports.walkStream = walkStream;
	const providers_1 = require_providers();
	const settings_1 = require_settings();
	const readers_1 = require_readers();
	const fs = new (require_fs()).FileSystemAdapter();
	function walk(directory, options, callback) {
		const optionsIsCallback = typeof options === "function";
		const callback_ = optionsIsCallback ? options : callback;
		const settings = optionsIsCallback ? getSettings() : getSettings(options);
		const reader = new readers_1.AsyncReader(fs, settings);
		new providers_1.AsyncProvider(reader).read(directory, callback_);
	}
	function walkSync(directory, optionsOrSettings) {
		const settings = getSettings(optionsOrSettings);
		const reader = new readers_1.SyncReader(fs, settings);
		return new providers_1.SyncProvider(reader).read(directory);
	}
	function walkStream(directory, optionsOrSettings) {
		const settings = getSettings(optionsOrSettings);
		const reader = new readers_1.AsyncReader(fs, settings);
		return new providers_1.StreamProvider(reader).read(directory);
	}
	function getSettings(settingsOrOptions = {}) {
		if (settingsOrOptions instanceof settings_1.Settings) return settingsOrOptions;
		return new settings_1.Settings(settingsOrOptions);
	}
}));

//#endregion
//#region node_modules/.pnpm/@nodelib+fs.walk@3.0.1/node_modules/@nodelib/fs.walk/out/index.js
var require_out = /* @__PURE__ */ __commonJSMin(((exports) => {
	Object.defineProperty(exports, "__esModule", { value: true });
	exports.Settings = exports.walkSync = exports.walkStream = exports.walk = void 0;
	var walk_1 = require_walk();
	Object.defineProperty(exports, "walk", {
		enumerable: true,
		get: function() {
			return walk_1.walk;
		}
	});
	Object.defineProperty(exports, "walkStream", {
		enumerable: true,
		get: function() {
			return walk_1.walkStream;
		}
	});
	Object.defineProperty(exports, "walkSync", {
		enumerable: true,
		get: function() {
			return walk_1.walkSync;
		}
	});
	var settings_1 = require_settings();
	Object.defineProperty(exports, "Settings", {
		enumerable: true,
		get: function() {
			return settings_1.Settings;
		}
	});
}));

//#endregion
//#region node_modules/.pnpm/@voxpelli+config-array-find-files@1.2.2_@eslint+config-array@0.23.2_patch_hash=9c568392_f034bacff9fe697827b3ce75a45874bf/node_modules/@voxpelli/config-array-find-files/index.js
var import_out = /* @__PURE__ */ __toESM(require_out(), 1);
/**
* Searches a directory looking for matching files. This uses the config
* array's logic to determine if a directory or file should be ignored.
*
* Derived from {@link https://github.com/eslint/eslint/blob/d2d06f7a70d9b96b125ecf2de8951bea549db4da/lib/eslint/eslint-helpers.js#L217-L382|ESLint globSearch()}
*
* @param {Object} options The options for this function.
* @param {string} options.basePath The directory to search.
* @param {import('@eslint/config-array').ConfigArray} options.configs The config array to use for determining what to ignore.
* @param {import('@nodelib/fs.walk').DeepFilterFunction} [options.deepFilter] Optional function that indicates whether the directory will be read deep or not.
* @param {import('@nodelib/fs.walk').EntryFilterFunction} [options.entryFilter] Optional function that indicates whether the entry will be included to results or not.
* @returns {Promise<Array<string>>} An array of matching file paths or an empty array if there are no matches.
*/
async function configArrayFindFiles(options) {
	const { basePath, configs, deepFilter, entryFilter } = options;
	return (await new Promise((resolve, reject) => {
		let promiseRejected = false;
		/**
		* Wraps a boolean-returning filter function. The wrapped function will reject the promise if an error occurs.
		*
		* @param {import('@nodelib/fs.walk').DeepFilterFunction | import('@nodelib/fs.walk').EntryFilterFunction} filter A filter function to wrap.
		* @returns {import('@nodelib/fs.walk').DeepFilterFunction | import('@nodelib/fs.walk').EntryFilterFunction} A function similar to the wrapped filter that rejects the promise if an error occurs.
		*/
		function wrapFilter(filter) {
			/** @type {import('@nodelib/fs.walk').DeepFilterFunction | import('@nodelib/fs.walk').EntryFilterFunction} */
			const result = (...args) => {
				if (!promiseRejected) try {
					return filter(...args);
				} catch (err) {
					promiseRejected = true;
					reject(err);
				}
				return false;
			};
			return result;
		}
		import_out.walk(basePath, {
			deepFilter: wrapFilter((entry) => {
				if (deepFilter && !deepFilter(entry)) return false;
				return !configs.isDirectoryIgnored(entry.path);
			}),
			entryFilter: wrapFilter((entry) => {
				if (entry.dirent.isDirectory()) return false;
				if (entryFilter && !entryFilter(entry)) return false;
				return configs.getConfig(entry.path) !== void 0;
			})
		}, (error, entries) => {
			if (error) reject(error);
			else resolve(entries);
		});
	})).map((entry) => entry.path);
}

//#endregion
//#region node_modules/.pnpm/yocto-queue@1.2.1/node_modules/yocto-queue/index.js
var Node$1 = class {
	value;
	next;
	constructor(value) {
		this.value = value;
	}
};
var Queue = class {
	#head;
	#tail;
	#size;
	constructor() {
		this.clear();
	}
	enqueue(value) {
		const node = new Node$1(value);
		if (this.#head) {
			this.#tail.next = node;
			this.#tail = node;
		} else {
			this.#head = node;
			this.#tail = node;
		}
		this.#size++;
	}
	dequeue() {
		const current = this.#head;
		if (!current) return;
		this.#head = this.#head.next;
		this.#size--;
		return current.value;
	}
	peek() {
		if (!this.#head) return;
		return this.#head.value;
	}
	clear() {
		this.#head = void 0;
		this.#tail = void 0;
		this.#size = 0;
	}
	get size() {
		return this.#size;
	}
	*[Symbol.iterator]() {
		let current = this.#head;
		while (current) {
			yield current.value;
			current = current.next;
		}
	}
	*drain() {
		while (this.#head) yield this.dequeue();
	}
};

//#endregion
//#region node_modules/.pnpm/p-limit@4.0.0/node_modules/p-limit/index.js
function pLimit(concurrency) {
	if (!((Number.isInteger(concurrency) || concurrency === Number.POSITIVE_INFINITY) && concurrency > 0)) throw new TypeError("Expected `concurrency` to be a number from 1 and up");
	const queue = new Queue();
	let activeCount = 0;
	const next = () => {
		activeCount--;
		if (queue.size > 0) queue.dequeue()();
	};
	const run = async (fn, resolve, args) => {
		activeCount++;
		const result = (async () => fn(...args))();
		resolve(result);
		try {
			await result;
		} catch {}
		next();
	};
	const enqueue = (fn, resolve, args) => {
		queue.enqueue(run.bind(void 0, fn, resolve, args));
		(async () => {
			await Promise.resolve();
			if (activeCount < concurrency && queue.size > 0) queue.dequeue()();
		})();
	};
	const generator = (fn, ...args) => new Promise((resolve) => {
		enqueue(fn, resolve, args);
	});
	Object.defineProperties(generator, {
		activeCount: { get: () => activeCount },
		pendingCount: { get: () => queue.size },
		clearQueue: { value: () => {
			queue.clear();
		} }
	});
	return generator;
}

//#endregion
//#region node_modules/.pnpm/p-locate@6.0.0/node_modules/p-locate/index.js
var EndError = class extends Error {
	constructor(value) {
		super();
		this.value = value;
	}
};
const testElement = async (element, tester) => tester(await element);
const finder = async (element) => {
	const values = await Promise.all(element);
	if (values[1] === true) throw new EndError(values[0]);
	return false;
};
async function pLocate(iterable, tester, { concurrency = Number.POSITIVE_INFINITY, preserveOrder = true } = {}) {
	const limit = pLimit(concurrency);
	const items = [...iterable].map((element) => [element, limit(testElement, element, tester)]);
	const checkLimit = pLimit(preserveOrder ? 1 : Number.POSITIVE_INFINITY);
	try {
		await Promise.all(items.map((element) => checkLimit(finder, element)));
	} catch (error) {
		if (error instanceof EndError) return error.value;
		throw error;
	}
}

//#endregion
//#region node_modules/.pnpm/locate-path@8.0.0/node_modules/locate-path/index.js
const typeMappings = {
	directory: "isDirectory",
	file: "isFile"
};
function checkType(type) {
	if (type === "both" || Object.hasOwn(typeMappings, type)) return;
	throw new Error(`Invalid type specified: ${type}`);
}
const matchType = (type, stat) => type === "both" ? stat.isFile() || stat.isDirectory() : stat[typeMappings[type]]();
const toPath$1 = (urlOrPath) => urlOrPath instanceof URL ? fileURLToPath(urlOrPath) : urlOrPath;
async function locatePath(paths, { cwd = process$1.cwd(), type = "file", allowSymlinks = true, concurrency, preserveOrder } = {}) {
	checkType(type);
	cwd = toPath$1(cwd);
	const statFunction = allowSymlinks ? promises.stat : promises.lstat;
	return pLocate(paths, async (path_) => {
		try {
			return matchType(type, await statFunction(path.resolve(cwd, path_)));
		} catch {
			return false;
		}
	}, {
		concurrency,
		preserveOrder
	});
}

//#endregion
//#region node_modules/.pnpm/unicorn-magic@0.3.0/node_modules/unicorn-magic/node.js
const execFileOriginal = promisify(execFile);
function toPath(urlOrPath) {
	return urlOrPath instanceof URL ? fileURLToPath(urlOrPath) : urlOrPath;
}
const TEN_MEGABYTES_IN_BYTES = 10 * 1024 * 1024;

//#endregion
//#region node_modules/.pnpm/find-up@8.0.0/node_modules/find-up/index.js
const findUpStop = Symbol("findUpStop");
async function findUpMultiple(name, options = {}) {
	let directory = path.resolve(toPath(options.cwd) ?? "");
	const { root } = path.parse(directory);
	const stopAt = path.resolve(directory, toPath(options.stopAt) ?? root);
	const limit = options.limit ?? Number.POSITIVE_INFINITY;
	const paths = [name].flat();
	const runMatcher = async (locateOptions) => {
		if (typeof name !== "function") return locatePath(paths, locateOptions);
		const foundPath = await name(locateOptions.cwd);
		if (typeof foundPath === "string") return locatePath([foundPath], locateOptions);
		return foundPath;
	};
	const matches = [];
	while (true) {
		const foundPath = await runMatcher({
			...options,
			cwd: directory
		});
		if (foundPath === findUpStop) break;
		if (foundPath) matches.push(path.resolve(directory, foundPath));
		if (directory === stopAt || matches.length >= limit) break;
		directory = path.dirname(directory);
	}
	return matches;
}
async function findUp(name, options = {}) {
	return (await findUpMultiple(name, {
		...options,
		limit: 1
	}))[0];
}

//#endregion
//#region node_modules/.pnpm/acorn@8.16.0/node_modules/acorn/dist/acorn.mjs
var astralIdentifierCodes = [
	509,
	0,
	227,
	0,
	150,
	4,
	294,
	9,
	1368,
	2,
	2,
	1,
	6,
	3,
	41,
	2,
	5,
	0,
	166,
	1,
	574,
	3,
	9,
	9,
	7,
	9,
	32,
	4,
	318,
	1,
	78,
	5,
	71,
	10,
	50,
	3,
	123,
	2,
	54,
	14,
	32,
	10,
	3,
	1,
	11,
	3,
	46,
	10,
	8,
	0,
	46,
	9,
	7,
	2,
	37,
	13,
	2,
	9,
	6,
	1,
	45,
	0,
	13,
	2,
	49,
	13,
	9,
	3,
	2,
	11,
	83,
	11,
	7,
	0,
	3,
	0,
	158,
	11,
	6,
	9,
	7,
	3,
	56,
	1,
	2,
	6,
	3,
	1,
	3,
	2,
	10,
	0,
	11,
	1,
	3,
	6,
	4,
	4,
	68,
	8,
	2,
	0,
	3,
	0,
	2,
	3,
	2,
	4,
	2,
	0,
	15,
	1,
	83,
	17,
	10,
	9,
	5,
	0,
	82,
	19,
	13,
	9,
	214,
	6,
	3,
	8,
	28,
	1,
	83,
	16,
	16,
	9,
	82,
	12,
	9,
	9,
	7,
	19,
	58,
	14,
	5,
	9,
	243,
	14,
	166,
	9,
	71,
	5,
	2,
	1,
	3,
	3,
	2,
	0,
	2,
	1,
	13,
	9,
	120,
	6,
	3,
	6,
	4,
	0,
	29,
	9,
	41,
	6,
	2,
	3,
	9,
	0,
	10,
	10,
	47,
	15,
	199,
	7,
	137,
	9,
	54,
	7,
	2,
	7,
	17,
	9,
	57,
	21,
	2,
	13,
	123,
	5,
	4,
	0,
	2,
	1,
	2,
	6,
	2,
	0,
	9,
	9,
	49,
	4,
	2,
	1,
	2,
	4,
	9,
	9,
	55,
	9,
	266,
	3,
	10,
	1,
	2,
	0,
	49,
	6,
	4,
	4,
	14,
	10,
	5350,
	0,
	7,
	14,
	11465,
	27,
	2343,
	9,
	87,
	9,
	39,
	4,
	60,
	6,
	26,
	9,
	535,
	9,
	470,
	0,
	2,
	54,
	8,
	3,
	82,
	0,
	12,
	1,
	19628,
	1,
	4178,
	9,
	519,
	45,
	3,
	22,
	543,
	4,
	4,
	5,
	9,
	7,
	3,
	6,
	31,
	3,
	149,
	2,
	1418,
	49,
	513,
	54,
	5,
	49,
	9,
	0,
	15,
	0,
	23,
	4,
	2,
	14,
	1361,
	6,
	2,
	16,
	3,
	6,
	2,
	1,
	2,
	4,
	101,
	0,
	161,
	6,
	10,
	9,
	357,
	0,
	62,
	13,
	499,
	13,
	245,
	1,
	2,
	9,
	233,
	0,
	3,
	0,
	8,
	1,
	6,
	0,
	475,
	6,
	110,
	6,
	6,
	9,
	4759,
	9,
	787719,
	239
];
var astralIdentifierStartCodes = [
	0,
	11,
	2,
	25,
	2,
	18,
	2,
	1,
	2,
	14,
	3,
	13,
	35,
	122,
	70,
	52,
	268,
	28,
	4,
	48,
	48,
	31,
	14,
	29,
	6,
	37,
	11,
	29,
	3,
	35,
	5,
	7,
	2,
	4,
	43,
	157,
	19,
	35,
	5,
	35,
	5,
	39,
	9,
	51,
	13,
	10,
	2,
	14,
	2,
	6,
	2,
	1,
	2,
	10,
	2,
	14,
	2,
	6,
	2,
	1,
	4,
	51,
	13,
	310,
	10,
	21,
	11,
	7,
	25,
	5,
	2,
	41,
	2,
	8,
	70,
	5,
	3,
	0,
	2,
	43,
	2,
	1,
	4,
	0,
	3,
	22,
	11,
	22,
	10,
	30,
	66,
	18,
	2,
	1,
	11,
	21,
	11,
	25,
	7,
	25,
	39,
	55,
	7,
	1,
	65,
	0,
	16,
	3,
	2,
	2,
	2,
	28,
	43,
	28,
	4,
	28,
	36,
	7,
	2,
	27,
	28,
	53,
	11,
	21,
	11,
	18,
	14,
	17,
	111,
	72,
	56,
	50,
	14,
	50,
	14,
	35,
	39,
	27,
	10,
	22,
	251,
	41,
	7,
	1,
	17,
	5,
	57,
	28,
	11,
	0,
	9,
	21,
	43,
	17,
	47,
	20,
	28,
	22,
	13,
	52,
	58,
	1,
	3,
	0,
	14,
	44,
	33,
	24,
	27,
	35,
	30,
	0,
	3,
	0,
	9,
	34,
	4,
	0,
	13,
	47,
	15,
	3,
	22,
	0,
	2,
	0,
	36,
	17,
	2,
	24,
	20,
	1,
	64,
	6,
	2,
	0,
	2,
	3,
	2,
	14,
	2,
	9,
	8,
	46,
	39,
	7,
	3,
	1,
	3,
	21,
	2,
	6,
	2,
	1,
	2,
	4,
	4,
	0,
	19,
	0,
	13,
	4,
	31,
	9,
	2,
	0,
	3,
	0,
	2,
	37,
	2,
	0,
	26,
	0,
	2,
	0,
	45,
	52,
	19,
	3,
	21,
	2,
	31,
	47,
	21,
	1,
	2,
	0,
	185,
	46,
	42,
	3,
	37,
	47,
	21,
	0,
	60,
	42,
	14,
	0,
	72,
	26,
	38,
	6,
	186,
	43,
	117,
	63,
	32,
	7,
	3,
	0,
	3,
	7,
	2,
	1,
	2,
	23,
	16,
	0,
	2,
	0,
	95,
	7,
	3,
	38,
	17,
	0,
	2,
	0,
	29,
	0,
	11,
	39,
	8,
	0,
	22,
	0,
	12,
	45,
	20,
	0,
	19,
	72,
	200,
	32,
	32,
	8,
	2,
	36,
	18,
	0,
	50,
	29,
	113,
	6,
	2,
	1,
	2,
	37,
	22,
	0,
	26,
	5,
	2,
	1,
	2,
	31,
	15,
	0,
	24,
	43,
	261,
	18,
	16,
	0,
	2,
	12,
	2,
	33,
	125,
	0,
	80,
	921,
	103,
	110,
	18,
	195,
	2637,
	96,
	16,
	1071,
	18,
	5,
	26,
	3994,
	6,
	582,
	6842,
	29,
	1763,
	568,
	8,
	30,
	18,
	78,
	18,
	29,
	19,
	47,
	17,
	3,
	32,
	20,
	6,
	18,
	433,
	44,
	212,
	63,
	33,
	24,
	3,
	24,
	45,
	74,
	6,
	0,
	67,
	12,
	65,
	1,
	2,
	0,
	15,
	4,
	10,
	7381,
	42,
	31,
	98,
	114,
	8702,
	3,
	2,
	6,
	2,
	1,
	2,
	290,
	16,
	0,
	30,
	2,
	3,
	0,
	15,
	3,
	9,
	395,
	2309,
	106,
	6,
	12,
	4,
	8,
	8,
	9,
	5991,
	84,
	2,
	70,
	2,
	1,
	3,
	0,
	3,
	1,
	3,
	3,
	2,
	11,
	2,
	0,
	2,
	6,
	2,
	64,
	2,
	3,
	3,
	7,
	2,
	6,
	2,
	27,
	2,
	3,
	2,
	4,
	2,
	0,
	4,
	6,
	2,
	339,
	3,
	24,
	2,
	24,
	2,
	30,
	2,
	24,
	2,
	30,
	2,
	24,
	2,
	30,
	2,
	24,
	2,
	30,
	2,
	24,
	2,
	7,
	1845,
	30,
	7,
	5,
	262,
	61,
	147,
	44,
	11,
	6,
	17,
	0,
	322,
	29,
	19,
	43,
	485,
	27,
	229,
	29,
	3,
	0,
	208,
	30,
	2,
	2,
	2,
	1,
	2,
	6,
	3,
	4,
	10,
	1,
	225,
	6,
	2,
	3,
	2,
	1,
	2,
	14,
	2,
	196,
	60,
	67,
	8,
	0,
	1205,
	3,
	2,
	26,
	2,
	1,
	2,
	0,
	3,
	0,
	2,
	9,
	2,
	3,
	2,
	0,
	2,
	0,
	7,
	0,
	5,
	0,
	2,
	0,
	2,
	0,
	2,
	2,
	2,
	1,
	2,
	0,
	3,
	0,
	2,
	0,
	2,
	0,
	2,
	0,
	2,
	0,
	2,
	1,
	2,
	0,
	3,
	3,
	2,
	6,
	2,
	3,
	2,
	3,
	2,
	0,
	2,
	9,
	2,
	16,
	6,
	2,
	2,
	4,
	2,
	16,
	4421,
	42719,
	33,
	4381,
	3,
	5773,
	3,
	7472,
	16,
	621,
	2467,
	541,
	1507,
	4938,
	6,
	8489
];
var nonASCIIidentifierChars = "‌‍·̀-ͯ·҃-֑҇-ׇֽֿׁׂׅׄؐ-ًؚ-٩ٰۖ-ۜ۟-۪ۤۧۨ-ۭ۰-۹ܑܰ-݊ަ-ް߀-߉߫-߽߳ࠖ-࠙ࠛ-ࠣࠥ-ࠧࠩ-࡙࠭-࡛ࢗ-࢟࣊-ࣣ࣡-ःऺ-़ा-ॏ॑-ॗॢॣ०-९ঁ-ঃ়া-ৄেৈো-্ৗৢৣ০-৯৾ਁ-ਃ਼ਾ-ੂੇੈੋ-੍ੑ੦-ੱੵઁ-ઃ઼ા-ૅે-ૉો-્ૢૣ૦-૯ૺ-૿ଁ-ଃ଼ା-ୄେୈୋ-୍୕-ୗୢୣ୦-୯ஂா-ூெ-ைொ-்ௗ௦-௯ఀ-ఄ఼ా-ౄె-ైొ-్ౕౖౢౣ౦-౯ಁ-ಃ಼ಾ-ೄೆ-ೈೊ-್ೕೖೢೣ೦-೯ೳഀ-ഃ഻഼ാ-ൄെ-ൈൊ-്ൗൢൣ൦-൯ඁ-ඃ්ා-ුූෘ-ෟ෦-෯ෲෳัิ-ฺ็-๎๐-๙ັິ-ຼ່-໎໐-໙༘༙༠-༩༹༵༷༾༿ཱ-྄྆྇ྍ-ྗྙ-ྼ࿆ါ-ှ၀-၉ၖ-ၙၞ-ၠၢ-ၤၧ-ၭၱ-ၴႂ-ႍႏ-ႝ፝-፟፩-፱ᜒ-᜕ᜲ-᜴ᝒᝓᝲᝳ឴-៓៝០-៩᠋-᠍᠏-᠙ᢩᤠ-ᤫᤰ-᤻᥆-᥏᧐-᧚ᨗ-ᨛᩕ-ᩞ᩠-᩿᩼-᪉᪐-᪙᪰-᪽ᪿ-᫝᫠-᫫ᬀ-ᬄ᬴-᭄᭐-᭙᭫-᭳ᮀ-ᮂᮡ-ᮭ᮰-᮹᯦-᯳ᰤ-᰷᱀-᱉᱐-᱙᳐-᳔᳒-᳨᳭᳴᳷-᳹᷀-᷿‌‍‿⁀⁔⃐-⃥⃜⃡-⃰⳯-⵿⳱ⷠ-〪ⷿ-゙゚〯・꘠-꘩꙯ꙴ-꙽ꚞꚟ꛰꛱ꠂ꠆ꠋꠣ-ꠧ꠬ꢀꢁꢴ-ꣅ꣐-꣙꣠-꣱ꣿ-꤉ꤦ-꤭ꥇ-꥓ꦀ-ꦃ꦳-꧀꧐-꧙ꧥ꧰-꧹ꨩ-ꨶꩃꩌꩍ꩐-꩙ꩻ-ꩽꪰꪲ-ꪴꪷꪸꪾ꪿꫁ꫫ-ꫯꫵ꫶ꯣ-ꯪ꯬꯭꯰-꯹ﬞ︀-️︠-︯︳︴﹍-﹏０-９＿･";
var nonASCIIidentifierStartChars = "ªµºÀ-ÖØ-öø-ˁˆ-ˑˠ-ˤˬˮͰ-ʹͶͷͺ-ͽͿΆΈ-ΊΌΎ-ΡΣ-ϵϷ-ҁҊ-ԯԱ-Ֆՙՠ-ֈא-תׯ-ײؠ-يٮٯٱ-ۓەۥۦۮۯۺ-ۼۿܐܒ-ܯݍ-ޥޱߊ-ߪߴߵߺࠀ-ࠕࠚࠤࠨࡀ-ࡘࡠ-ࡪࡰ-ࢇࢉ-࢏ࢠ-ࣉऄ-हऽॐक़-ॡॱ-ঀঅ-ঌএঐও-নপ-রলশ-হঽৎড়ঢ়য়-ৡৰৱৼਅ-ਊਏਐਓ-ਨਪ-ਰਲਲ਼ਵਸ਼ਸਹਖ਼-ੜਫ਼ੲ-ੴઅ-ઍએ-ઑઓ-નપ-રલળવ-હઽૐૠૡૹଅ-ଌଏଐଓ-ନପ-ରଲଳଵ-ହଽଡ଼ଢ଼ୟ-ୡୱஃஅ-ஊஎ-ஐஒ-கஙசஜஞடணதந-பம-ஹௐఅ-ఌఎ-ఐఒ-నప-హఽౘ-ౚ౜ౝౠౡಀಅ-ಌಎ-ಐಒ-ನಪ-ಳವ-ಹಽ೜-ೞೠೡೱೲഄ-ഌഎ-ഐഒ-ഺഽൎൔ-ൖൟ-ൡൺ-ൿඅ-ඖක-නඳ-රලව-ෆก-ะาำเ-ๆກຂຄຆ-ຊຌ-ຣລວ-ະາຳຽເ-ໄໆໜ-ໟༀཀ-ཇཉ-ཬྈ-ྌက-ဪဿၐ-ၕၚ-ၝၡၥၦၮ-ၰၵ-ႁႎႠ-ჅჇჍა-ჺჼ-ቈቊ-ቍቐ-ቖቘቚ-ቝበ-ኈኊ-ኍነ-ኰኲ-ኵኸ-ኾዀዂ-ዅወ-ዖዘ-ጐጒ-ጕጘ-ፚᎀ-ᎏᎠ-Ᏽᏸ-ᏽᐁ-ᙬᙯ-ᙿᚁ-ᚚᚠ-ᛪᛮ-ᛸᜀ-ᜑᜟ-ᜱᝀ-ᝑᝠ-ᝬᝮ-ᝰក-ឳៗៜᠠ-ᡸᢀ-ᢨᢪᢰ-ᣵᤀ-ᤞᥐ-ᥭᥰ-ᥴᦀ-ᦫᦰ-ᧉᨀ-ᨖᨠ-ᩔᪧᬅ-ᬳᭅ-ᭌᮃ-ᮠᮮᮯᮺ-ᯥᰀ-ᰣᱍ-ᱏᱚ-ᱽᲀ-ᲊᲐ-ᲺᲽ-Ჿᳩ-ᳬᳮ-ᳳᳵᳶᳺᴀ-ᶿḀ-ἕἘ-Ἕἠ-ὅὈ-Ὅὐ-ὗὙὛὝὟ-ώᾀ-ᾴᾶ-ᾼιῂ-ῄῆ-ῌῐ-ΐῖ-Ίῠ-Ῥῲ-ῴῶ-ῼⁱⁿₐ-ₜℂℇℊ-ℓℕ℘-ℝℤΩℨK-ℹℼ-ℿⅅ-ⅉⅎⅠ-ↈⰀ-ⳤⳫ-ⳮⳲⳳⴀ-ⴥⴧⴭⴰ-ⵧⵯⶀ-ⶖⶠ-ⶦⶨ-ⶮⶰ-ⶶⶸ-ⶾⷀ-ⷆⷈ-ⷎⷐ-ⷖⷘ-ⷞ々-〇〡-〩〱-〵〸-〼ぁ-ゖ゛-ゟァ-ヺー-ヿㄅ-ㄯㄱ-ㆎㆠ-ㆿㇰ-ㇿ㐀-䶿一-ꒌꓐ-ꓽꔀ-ꘌꘐ-ꘟꘪꘫꙀ-ꙮꙿ-ꚝꚠ-ꛯꜗ-ꜟꜢ-ꞈꞋ-Ƛ꟱-ꠁꠃ-ꠅꠇ-ꠊꠌ-ꠢꡀ-ꡳꢂ-ꢳꣲ-ꣷꣻꣽꣾꤊ-ꤥꤰ-ꥆꥠ-ꥼꦄ-ꦲꧏꧠ-ꧤꧦ-ꧯꧺ-ꧾꨀ-ꨨꩀ-ꩂꩄ-ꩋꩠ-ꩶꩺꩾ-ꪯꪱꪵꪶꪹ-ꪽꫀꫂꫛ-ꫝꫠ-ꫪꫲ-ꫴꬁ-ꬆꬉ-ꬎꬑ-ꬖꬠ-ꬦꬨ-ꬮꬰ-ꭚꭜ-ꭩꭰ-ꯢ가-힣ힰ-ퟆퟋ-ퟻ豈-舘並-龎ﬀ-ﬆﬓ-ﬗיִײַ-ﬨשׁ-זּטּ-לּמּנּסּףּפּצּ-ﮱﯓ-ﴽﵐ-ﶏﶒ-ﷇﷰ-ﷻﹰ-ﹴﹶ-ﻼＡ-Ｚａ-ｚｦ-ﾾￂ-ￇￊ-ￏￒ-ￗￚ-ￜ";
var reservedWords = {
	3: "abstract boolean byte char class double enum export extends final float goto implements import int interface long native package private protected public short static super synchronized throws transient volatile",
	5: "class enum extends super const export import",
	6: "enum",
	strict: "implements interface let package private protected public static yield",
	strictBind: "eval arguments"
};
var ecma5AndLessKeywords = "break case catch continue debugger default do else finally for function if return switch throw try var while with null true false instanceof typeof void delete new in this";
var keywords$1 = {
	5: ecma5AndLessKeywords,
	"5module": ecma5AndLessKeywords + " export import",
	6: ecma5AndLessKeywords + " const class extends export import super"
};
var keywordRelationalOperator = /^in(stanceof)?$/;
var nonASCIIidentifierStart = new RegExp("[" + nonASCIIidentifierStartChars + "]");
var nonASCIIidentifier = new RegExp("[" + nonASCIIidentifierStartChars + nonASCIIidentifierChars + "]");
function isInAstralSet(code, set) {
	var pos = 65536;
	for (var i = 0; i < set.length; i += 2) {
		pos += set[i];
		if (pos > code) return false;
		pos += set[i + 1];
		if (pos >= code) return true;
	}
	return false;
}
function isIdentifierStart(code, astral) {
	if (code < 65) return code === 36;
	if (code < 91) return true;
	if (code < 97) return code === 95;
	if (code < 123) return true;
	if (code <= 65535) return code >= 170 && nonASCIIidentifierStart.test(String.fromCharCode(code));
	if (astral === false) return false;
	return isInAstralSet(code, astralIdentifierStartCodes);
}
function isIdentifierChar(code, astral) {
	if (code < 48) return code === 36;
	if (code < 58) return true;
	if (code < 65) return false;
	if (code < 91) return true;
	if (code < 97) return code === 95;
	if (code < 123) return true;
	if (code <= 65535) return code >= 170 && nonASCIIidentifier.test(String.fromCharCode(code));
	if (astral === false) return false;
	return isInAstralSet(code, astralIdentifierStartCodes) || isInAstralSet(code, astralIdentifierCodes);
}
var TokenType = function TokenType(label, conf) {
	if (conf === void 0) conf = {};
	this.label = label;
	this.keyword = conf.keyword;
	this.beforeExpr = !!conf.beforeExpr;
	this.startsExpr = !!conf.startsExpr;
	this.isLoop = !!conf.isLoop;
	this.isAssign = !!conf.isAssign;
	this.prefix = !!conf.prefix;
	this.postfix = !!conf.postfix;
	this.binop = conf.binop || null;
	this.updateContext = null;
};
function binop(name, prec) {
	return new TokenType(name, {
		beforeExpr: true,
		binop: prec
	});
}
var beforeExpr = { beforeExpr: true }, startsExpr = { startsExpr: true };
var keywords = {};
function kw(name, options) {
	if (options === void 0) options = {};
	options.keyword = name;
	return keywords[name] = new TokenType(name, options);
}
var types$1 = {
	num: new TokenType("num", startsExpr),
	regexp: new TokenType("regexp", startsExpr),
	string: new TokenType("string", startsExpr),
	name: new TokenType("name", startsExpr),
	privateId: new TokenType("privateId", startsExpr),
	eof: new TokenType("eof"),
	bracketL: new TokenType("[", {
		beforeExpr: true,
		startsExpr: true
	}),
	bracketR: new TokenType("]"),
	braceL: new TokenType("{", {
		beforeExpr: true,
		startsExpr: true
	}),
	braceR: new TokenType("}"),
	parenL: new TokenType("(", {
		beforeExpr: true,
		startsExpr: true
	}),
	parenR: new TokenType(")"),
	comma: new TokenType(",", beforeExpr),
	semi: new TokenType(";", beforeExpr),
	colon: new TokenType(":", beforeExpr),
	dot: new TokenType("."),
	question: new TokenType("?", beforeExpr),
	questionDot: new TokenType("?."),
	arrow: new TokenType("=>", beforeExpr),
	template: new TokenType("template"),
	invalidTemplate: new TokenType("invalidTemplate"),
	ellipsis: new TokenType("...", beforeExpr),
	backQuote: new TokenType("`", startsExpr),
	dollarBraceL: new TokenType("${", {
		beforeExpr: true,
		startsExpr: true
	}),
	eq: new TokenType("=", {
		beforeExpr: true,
		isAssign: true
	}),
	assign: new TokenType("_=", {
		beforeExpr: true,
		isAssign: true
	}),
	incDec: new TokenType("++/--", {
		prefix: true,
		postfix: true,
		startsExpr: true
	}),
	prefix: new TokenType("!/~", {
		beforeExpr: true,
		prefix: true,
		startsExpr: true
	}),
	logicalOR: binop("||", 1),
	logicalAND: binop("&&", 2),
	bitwiseOR: binop("|", 3),
	bitwiseXOR: binop("^", 4),
	bitwiseAND: binop("&", 5),
	equality: binop("==/!=/===/!==", 6),
	relational: binop("</>/<=/>=", 7),
	bitShift: binop("<</>>/>>>", 8),
	plusMin: new TokenType("+/-", {
		beforeExpr: true,
		binop: 9,
		prefix: true,
		startsExpr: true
	}),
	modulo: binop("%", 10),
	star: binop("*", 10),
	slash: binop("/", 10),
	starstar: new TokenType("**", { beforeExpr: true }),
	coalesce: binop("??", 1),
	_break: kw("break"),
	_case: kw("case", beforeExpr),
	_catch: kw("catch"),
	_continue: kw("continue"),
	_debugger: kw("debugger"),
	_default: kw("default", beforeExpr),
	_do: kw("do", {
		isLoop: true,
		beforeExpr: true
	}),
	_else: kw("else", beforeExpr),
	_finally: kw("finally"),
	_for: kw("for", { isLoop: true }),
	_function: kw("function", startsExpr),
	_if: kw("if"),
	_return: kw("return", beforeExpr),
	_switch: kw("switch"),
	_throw: kw("throw", beforeExpr),
	_try: kw("try"),
	_var: kw("var"),
	_const: kw("const"),
	_while: kw("while", { isLoop: true }),
	_with: kw("with"),
	_new: kw("new", {
		beforeExpr: true,
		startsExpr: true
	}),
	_this: kw("this", startsExpr),
	_super: kw("super", startsExpr),
	_class: kw("class", startsExpr),
	_extends: kw("extends", beforeExpr),
	_export: kw("export"),
	_import: kw("import", startsExpr),
	_null: kw("null", startsExpr),
	_true: kw("true", startsExpr),
	_false: kw("false", startsExpr),
	_in: kw("in", {
		beforeExpr: true,
		binop: 7
	}),
	_instanceof: kw("instanceof", {
		beforeExpr: true,
		binop: 7
	}),
	_typeof: kw("typeof", {
		beforeExpr: true,
		prefix: true,
		startsExpr: true
	}),
	_void: kw("void", {
		beforeExpr: true,
		prefix: true,
		startsExpr: true
	}),
	_delete: kw("delete", {
		beforeExpr: true,
		prefix: true,
		startsExpr: true
	})
};
var lineBreak = /\r\n?|\n|\u2028|\u2029/;
var lineBreakG = new RegExp(lineBreak.source, "g");
function isNewLine(code) {
	return code === 10 || code === 13 || code === 8232 || code === 8233;
}
function nextLineBreak(code, from, end) {
	if (end === void 0) end = code.length;
	for (var i = from; i < end; i++) {
		var next = code.charCodeAt(i);
		if (isNewLine(next)) return i < end - 1 && next === 13 && code.charCodeAt(i + 1) === 10 ? i + 2 : i + 1;
	}
	return -1;
}
var nonASCIIwhitespace = /[\u1680\u2000-\u200a\u202f\u205f\u3000\ufeff]/;
var skipWhiteSpace = /(?:\s|\/\/.*|\/\*[^]*?\*\/)*/g;
var ref = Object.prototype;
var hasOwnProperty$2 = ref.hasOwnProperty;
var toString = ref.toString;
var hasOwn = Object.hasOwn || (function(obj, propName) {
	return hasOwnProperty$2.call(obj, propName);
});
var isArray = Array.isArray || (function(obj) {
	return toString.call(obj) === "[object Array]";
});
var regexpCache = Object.create(null);
function wordsRegexp(words) {
	return regexpCache[words] || (regexpCache[words] = new RegExp("^(?:" + words.replace(/ /g, "|") + ")$"));
}
function codePointToString(code) {
	if (code <= 65535) return String.fromCharCode(code);
	code -= 65536;
	return String.fromCharCode((code >> 10) + 55296, (code & 1023) + 56320);
}
var loneSurrogate = /(?:[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?:[^\uD800-\uDBFF]|^)[\uDC00-\uDFFF])/;
var Position = function Position(line, col) {
	this.line = line;
	this.column = col;
};
Position.prototype.offset = function offset(n) {
	return new Position(this.line, this.column + n);
};
var SourceLocation = function SourceLocation(p, start, end) {
	this.start = start;
	this.end = end;
	if (p.sourceFile !== null) this.source = p.sourceFile;
};
function getLineInfo(input, offset) {
	for (var line = 1, cur = 0;;) {
		var nextBreak = nextLineBreak(input, cur, offset);
		if (nextBreak < 0) return new Position(line, offset - cur);
		++line;
		cur = nextBreak;
	}
}
var defaultOptions = {
	ecmaVersion: null,
	sourceType: "script",
	onInsertedSemicolon: null,
	onTrailingComma: null,
	allowReserved: null,
	allowReturnOutsideFunction: false,
	allowImportExportEverywhere: false,
	allowAwaitOutsideFunction: null,
	allowSuperOutsideMethod: null,
	allowHashBang: false,
	checkPrivateFields: true,
	locations: false,
	onToken: null,
	onComment: null,
	ranges: false,
	program: null,
	sourceFile: null,
	directSourceFile: null,
	preserveParens: false
};
var warnedAboutEcmaVersion = false;
function getOptions(opts) {
	var options = {};
	for (var opt in defaultOptions) options[opt] = opts && hasOwn(opts, opt) ? opts[opt] : defaultOptions[opt];
	if (options.ecmaVersion === "latest") options.ecmaVersion = 1e8;
	else if (options.ecmaVersion == null) {
		if (!warnedAboutEcmaVersion && typeof console === "object" && console.warn) {
			warnedAboutEcmaVersion = true;
			console.warn("Since Acorn 8.0.0, options.ecmaVersion is required.\nDefaulting to 2020, but this will stop working in the future.");
		}
		options.ecmaVersion = 11;
	} else if (options.ecmaVersion >= 2015) options.ecmaVersion -= 2009;
	if (options.allowReserved == null) options.allowReserved = options.ecmaVersion < 5;
	if (!opts || opts.allowHashBang == null) options.allowHashBang = options.ecmaVersion >= 14;
	if (isArray(options.onToken)) {
		var tokens = options.onToken;
		options.onToken = function(token) {
			return tokens.push(token);
		};
	}
	if (isArray(options.onComment)) options.onComment = pushComment(options, options.onComment);
	if (options.sourceType === "commonjs" && options.allowAwaitOutsideFunction) throw new Error("Cannot use allowAwaitOutsideFunction with sourceType: commonjs");
	return options;
}
function pushComment(options, array) {
	return function(block, text, start, end, startLoc, endLoc) {
		var comment = {
			type: block ? "Block" : "Line",
			value: text,
			start,
			end
		};
		if (options.locations) comment.loc = new SourceLocation(this, startLoc, endLoc);
		if (options.ranges) comment.range = [start, end];
		array.push(comment);
	};
}
var SCOPE_TOP = 1, SCOPE_FUNCTION = 2, SCOPE_ASYNC = 4, SCOPE_GENERATOR = 8, SCOPE_ARROW = 16, SCOPE_SIMPLE_CATCH = 32, SCOPE_SUPER = 64, SCOPE_DIRECT_SUPER = 128, SCOPE_CLASS_STATIC_BLOCK = 256, SCOPE_CLASS_FIELD_INIT = 512, SCOPE_SWITCH = 1024, SCOPE_VAR = SCOPE_TOP | SCOPE_FUNCTION | SCOPE_CLASS_STATIC_BLOCK;
function functionFlags(async, generator) {
	return SCOPE_FUNCTION | (async ? SCOPE_ASYNC : 0) | (generator ? SCOPE_GENERATOR : 0);
}
var BIND_NONE = 0, BIND_VAR = 1, BIND_LEXICAL = 2, BIND_FUNCTION = 3, BIND_SIMPLE_CATCH = 4, BIND_OUTSIDE = 5;
var Parser = function Parser(options, input, startPos) {
	this.options = options = getOptions(options);
	this.sourceFile = options.sourceFile;
	this.keywords = wordsRegexp(keywords$1[options.ecmaVersion >= 6 ? 6 : options.sourceType === "module" ? "5module" : 5]);
	var reserved = "";
	if (options.allowReserved !== true) {
		reserved = reservedWords[options.ecmaVersion >= 6 ? 6 : options.ecmaVersion === 5 ? 5 : 3];
		if (options.sourceType === "module") reserved += " await";
	}
	this.reservedWords = wordsRegexp(reserved);
	var reservedStrict = (reserved ? reserved + " " : "") + reservedWords.strict;
	this.reservedWordsStrict = wordsRegexp(reservedStrict);
	this.reservedWordsStrictBind = wordsRegexp(reservedStrict + " " + reservedWords.strictBind);
	this.input = String(input);
	this.containsEsc = false;
	if (startPos) {
		this.pos = startPos;
		this.lineStart = this.input.lastIndexOf("\n", startPos - 1) + 1;
		this.curLine = this.input.slice(0, this.lineStart).split(lineBreak).length;
	} else {
		this.pos = this.lineStart = 0;
		this.curLine = 1;
	}
	this.type = types$1.eof;
	this.value = null;
	this.start = this.end = this.pos;
	this.startLoc = this.endLoc = this.curPosition();
	this.lastTokEndLoc = this.lastTokStartLoc = null;
	this.lastTokStart = this.lastTokEnd = this.pos;
	this.context = this.initialContext();
	this.exprAllowed = true;
	this.inModule = options.sourceType === "module";
	this.strict = this.inModule || this.strictDirective(this.pos);
	this.potentialArrowAt = -1;
	this.potentialArrowInForAwait = false;
	this.yieldPos = this.awaitPos = this.awaitIdentPos = 0;
	this.labels = [];
	this.undefinedExports = Object.create(null);
	if (this.pos === 0 && options.allowHashBang && this.input.slice(0, 2) === "#!") this.skipLineComment(2);
	this.scopeStack = [];
	this.enterScope(this.options.sourceType === "commonjs" ? SCOPE_FUNCTION : SCOPE_TOP);
	this.regexpState = null;
	this.privateNameStack = [];
};
var prototypeAccessors = {
	inFunction: { configurable: true },
	inGenerator: { configurable: true },
	inAsync: { configurable: true },
	canAwait: { configurable: true },
	allowReturn: { configurable: true },
	allowSuper: { configurable: true },
	allowDirectSuper: { configurable: true },
	treatFunctionsAsVar: { configurable: true },
	allowNewDotTarget: { configurable: true },
	allowUsing: { configurable: true },
	inClassStaticBlock: { configurable: true }
};
Parser.prototype.parse = function parse() {
	var node = this.options.program || this.startNode();
	this.nextToken();
	return this.parseTopLevel(node);
};
prototypeAccessors.inFunction.get = function() {
	return (this.currentVarScope().flags & SCOPE_FUNCTION) > 0;
};
prototypeAccessors.inGenerator.get = function() {
	return (this.currentVarScope().flags & SCOPE_GENERATOR) > 0;
};
prototypeAccessors.inAsync.get = function() {
	return (this.currentVarScope().flags & SCOPE_ASYNC) > 0;
};
prototypeAccessors.canAwait.get = function() {
	for (var i = this.scopeStack.length - 1; i >= 0; i--) {
		var flags = this.scopeStack[i].flags;
		if (flags & (SCOPE_CLASS_STATIC_BLOCK | SCOPE_CLASS_FIELD_INIT)) return false;
		if (flags & SCOPE_FUNCTION) return (flags & SCOPE_ASYNC) > 0;
	}
	return this.inModule && this.options.ecmaVersion >= 13 || this.options.allowAwaitOutsideFunction;
};
prototypeAccessors.allowReturn.get = function() {
	if (this.inFunction) return true;
	if (this.options.allowReturnOutsideFunction && this.currentVarScope().flags & SCOPE_TOP) return true;
	return false;
};
prototypeAccessors.allowSuper.get = function() {
	return (this.currentThisScope().flags & SCOPE_SUPER) > 0 || this.options.allowSuperOutsideMethod;
};
prototypeAccessors.allowDirectSuper.get = function() {
	return (this.currentThisScope().flags & SCOPE_DIRECT_SUPER) > 0;
};
prototypeAccessors.treatFunctionsAsVar.get = function() {
	return this.treatFunctionsAsVarInScope(this.currentScope());
};
prototypeAccessors.allowNewDotTarget.get = function() {
	for (var i = this.scopeStack.length - 1; i >= 0; i--) {
		var flags = this.scopeStack[i].flags;
		if (flags & (SCOPE_CLASS_STATIC_BLOCK | SCOPE_CLASS_FIELD_INIT) || flags & SCOPE_FUNCTION && !(flags & SCOPE_ARROW)) return true;
	}
	return false;
};
prototypeAccessors.allowUsing.get = function() {
	var flags = this.currentScope().flags;
	if (flags & SCOPE_SWITCH) return false;
	if (!this.inModule && flags & SCOPE_TOP) return false;
	return true;
};
prototypeAccessors.inClassStaticBlock.get = function() {
	return (this.currentVarScope().flags & SCOPE_CLASS_STATIC_BLOCK) > 0;
};
Parser.extend = function extend() {
	var plugins = [], len = arguments.length;
	while (len--) plugins[len] = arguments[len];
	var cls = this;
	for (var i = 0; i < plugins.length; i++) cls = plugins[i](cls);
	return cls;
};
Parser.parse = function parse(input, options) {
	return new this(options, input).parse();
};
Parser.parseExpressionAt = function parseExpressionAt(input, pos, options) {
	var parser = new this(options, input, pos);
	parser.nextToken();
	return parser.parseExpression();
};
Parser.tokenizer = function tokenizer(input, options) {
	return new this(options, input);
};
Object.defineProperties(Parser.prototype, prototypeAccessors);
var pp$9 = Parser.prototype;
var literal = /^(?:'((?:\\[^]|[^'\\])*?)'|"((?:\\[^]|[^"\\])*?)")/;
pp$9.strictDirective = function(start) {
	if (this.options.ecmaVersion < 5) return false;
	for (;;) {
		skipWhiteSpace.lastIndex = start;
		start += skipWhiteSpace.exec(this.input)[0].length;
		var match = literal.exec(this.input.slice(start));
		if (!match) return false;
		if ((match[1] || match[2]) === "use strict") {
			skipWhiteSpace.lastIndex = start + match[0].length;
			var spaceAfter = skipWhiteSpace.exec(this.input), end = spaceAfter.index + spaceAfter[0].length;
			var next = this.input.charAt(end);
			return next === ";" || next === "}" || lineBreak.test(spaceAfter[0]) && !(/[(`.[+\-/*%<>=,?^&]/.test(next) || next === "!" && this.input.charAt(end + 1) === "=");
		}
		start += match[0].length;
		skipWhiteSpace.lastIndex = start;
		start += skipWhiteSpace.exec(this.input)[0].length;
		if (this.input[start] === ";") start++;
	}
};
pp$9.eat = function(type) {
	if (this.type === type) {
		this.next();
		return true;
	} else return false;
};
pp$9.isContextual = function(name) {
	return this.type === types$1.name && this.value === name && !this.containsEsc;
};
pp$9.eatContextual = function(name) {
	if (!this.isContextual(name)) return false;
	this.next();
	return true;
};
pp$9.expectContextual = function(name) {
	if (!this.eatContextual(name)) this.unexpected();
};
pp$9.canInsertSemicolon = function() {
	return this.type === types$1.eof || this.type === types$1.braceR || lineBreak.test(this.input.slice(this.lastTokEnd, this.start));
};
pp$9.insertSemicolon = function() {
	if (this.canInsertSemicolon()) {
		if (this.options.onInsertedSemicolon) this.options.onInsertedSemicolon(this.lastTokEnd, this.lastTokEndLoc);
		return true;
	}
};
pp$9.semicolon = function() {
	if (!this.eat(types$1.semi) && !this.insertSemicolon()) this.unexpected();
};
pp$9.afterTrailingComma = function(tokType, notNext) {
	if (this.type === tokType) {
		if (this.options.onTrailingComma) this.options.onTrailingComma(this.lastTokStart, this.lastTokStartLoc);
		if (!notNext) this.next();
		return true;
	}
};
pp$9.expect = function(type) {
	this.eat(type) || this.unexpected();
};
pp$9.unexpected = function(pos) {
	this.raise(pos != null ? pos : this.start, "Unexpected token");
};
var DestructuringErrors = function DestructuringErrors() {
	this.shorthandAssign = this.trailingComma = this.parenthesizedAssign = this.parenthesizedBind = this.doubleProto = -1;
};
pp$9.checkPatternErrors = function(refDestructuringErrors, isAssign) {
	if (!refDestructuringErrors) return;
	if (refDestructuringErrors.trailingComma > -1) this.raiseRecoverable(refDestructuringErrors.trailingComma, "Comma is not permitted after the rest element");
	var parens = isAssign ? refDestructuringErrors.parenthesizedAssign : refDestructuringErrors.parenthesizedBind;
	if (parens > -1) this.raiseRecoverable(parens, isAssign ? "Assigning to rvalue" : "Parenthesized pattern");
};
pp$9.checkExpressionErrors = function(refDestructuringErrors, andThrow) {
	if (!refDestructuringErrors) return false;
	var shorthandAssign = refDestructuringErrors.shorthandAssign;
	var doubleProto = refDestructuringErrors.doubleProto;
	if (!andThrow) return shorthandAssign >= 0 || doubleProto >= 0;
	if (shorthandAssign >= 0) this.raise(shorthandAssign, "Shorthand property assignments are valid only in destructuring patterns");
	if (doubleProto >= 0) this.raiseRecoverable(doubleProto, "Redefinition of __proto__ property");
};
pp$9.checkYieldAwaitInDefaultParams = function() {
	if (this.yieldPos && (!this.awaitPos || this.yieldPos < this.awaitPos)) this.raise(this.yieldPos, "Yield expression cannot be a default value");
	if (this.awaitPos) this.raise(this.awaitPos, "Await expression cannot be a default value");
};
pp$9.isSimpleAssignTarget = function(expr) {
	if (expr.type === "ParenthesizedExpression") return this.isSimpleAssignTarget(expr.expression);
	return expr.type === "Identifier" || expr.type === "MemberExpression";
};
var pp$8 = Parser.prototype;
pp$8.parseTopLevel = function(node) {
	var exports = Object.create(null);
	if (!node.body) node.body = [];
	while (this.type !== types$1.eof) {
		var stmt = this.parseStatement(null, true, exports);
		node.body.push(stmt);
	}
	if (this.inModule) for (var i = 0, list = Object.keys(this.undefinedExports); i < list.length; i += 1) {
		var name = list[i];
		this.raiseRecoverable(this.undefinedExports[name].start, "Export '" + name + "' is not defined");
	}
	this.adaptDirectivePrologue(node.body);
	this.next();
	node.sourceType = this.options.sourceType === "commonjs" ? "script" : this.options.sourceType;
	return this.finishNode(node, "Program");
};
var loopLabel = { kind: "loop" }, switchLabel = { kind: "switch" };
pp$8.isLet = function(context) {
	if (this.options.ecmaVersion < 6 || !this.isContextual("let")) return false;
	skipWhiteSpace.lastIndex = this.pos;
	var skip = skipWhiteSpace.exec(this.input);
	var next = this.pos + skip[0].length, nextCh = this.fullCharCodeAt(next);
	if (nextCh === 91 || nextCh === 92) return true;
	if (context) return false;
	if (nextCh === 123) return true;
	if (isIdentifierStart(nextCh)) {
		var start = next;
		do
			next += nextCh <= 65535 ? 1 : 2;
		while (isIdentifierChar(nextCh = this.fullCharCodeAt(next)));
		if (nextCh === 92) return true;
		var ident = this.input.slice(start, next);
		if (!keywordRelationalOperator.test(ident)) return true;
	}
	return false;
};
pp$8.isAsyncFunction = function() {
	if (this.options.ecmaVersion < 8 || !this.isContextual("async")) return false;
	skipWhiteSpace.lastIndex = this.pos;
	var skip = skipWhiteSpace.exec(this.input);
	var next = this.pos + skip[0].length, after;
	return !lineBreak.test(this.input.slice(this.pos, next)) && this.input.slice(next, next + 8) === "function" && (next + 8 === this.input.length || !(isIdentifierChar(after = this.fullCharCodeAt(next + 8)) || after === 92));
};
pp$8.isUsingKeyword = function(isAwaitUsing, isFor) {
	if (this.options.ecmaVersion < 17 || !this.isContextual(isAwaitUsing ? "await" : "using")) return false;
	skipWhiteSpace.lastIndex = this.pos;
	var skip = skipWhiteSpace.exec(this.input);
	var next = this.pos + skip[0].length;
	if (lineBreak.test(this.input.slice(this.pos, next))) return false;
	if (isAwaitUsing) {
		var usingEndPos = next + 5, after;
		if (this.input.slice(next, usingEndPos) !== "using" || usingEndPos === this.input.length || isIdentifierChar(after = this.fullCharCodeAt(usingEndPos)) || after === 92) return false;
		skipWhiteSpace.lastIndex = usingEndPos;
		var skipAfterUsing = skipWhiteSpace.exec(this.input);
		next = usingEndPos + skipAfterUsing[0].length;
		if (skipAfterUsing && lineBreak.test(this.input.slice(usingEndPos, next))) return false;
	}
	var ch = this.fullCharCodeAt(next);
	if (!isIdentifierStart(ch) && ch !== 92) return false;
	var idStart = next;
	do
		next += ch <= 65535 ? 1 : 2;
	while (isIdentifierChar(ch = this.fullCharCodeAt(next)));
	if (ch === 92) return true;
	var id = this.input.slice(idStart, next);
	if (keywordRelationalOperator.test(id) || isFor && id === "of") return false;
	return true;
};
pp$8.isAwaitUsing = function(isFor) {
	return this.isUsingKeyword(true, isFor);
};
pp$8.isUsing = function(isFor) {
	return this.isUsingKeyword(false, isFor);
};
pp$8.parseStatement = function(context, topLevel, exports) {
	var starttype = this.type, node = this.startNode(), kind;
	if (this.isLet(context)) {
		starttype = types$1._var;
		kind = "let";
	}
	switch (starttype) {
		case types$1._break:
		case types$1._continue: return this.parseBreakContinueStatement(node, starttype.keyword);
		case types$1._debugger: return this.parseDebuggerStatement(node);
		case types$1._do: return this.parseDoStatement(node);
		case types$1._for: return this.parseForStatement(node);
		case types$1._function:
			if (context && (this.strict || context !== "if" && context !== "label") && this.options.ecmaVersion >= 6) this.unexpected();
			return this.parseFunctionStatement(node, false, !context);
		case types$1._class:
			if (context) this.unexpected();
			return this.parseClass(node, true);
		case types$1._if: return this.parseIfStatement(node);
		case types$1._return: return this.parseReturnStatement(node);
		case types$1._switch: return this.parseSwitchStatement(node);
		case types$1._throw: return this.parseThrowStatement(node);
		case types$1._try: return this.parseTryStatement(node);
		case types$1._const:
		case types$1._var:
			kind = kind || this.value;
			if (context && kind !== "var") this.unexpected();
			return this.parseVarStatement(node, kind);
		case types$1._while: return this.parseWhileStatement(node);
		case types$1._with: return this.parseWithStatement(node);
		case types$1.braceL: return this.parseBlock(true, node);
		case types$1.semi: return this.parseEmptyStatement(node);
		case types$1._export:
		case types$1._import:
			if (this.options.ecmaVersion > 10 && starttype === types$1._import) {
				skipWhiteSpace.lastIndex = this.pos;
				var skip = skipWhiteSpace.exec(this.input);
				var next = this.pos + skip[0].length, nextCh = this.input.charCodeAt(next);
				if (nextCh === 40 || nextCh === 46) return this.parseExpressionStatement(node, this.parseExpression());
			}
			if (!this.options.allowImportExportEverywhere) {
				if (!topLevel) this.raise(this.start, "'import' and 'export' may only appear at the top level");
				if (!this.inModule) this.raise(this.start, "'import' and 'export' may appear only with 'sourceType: module'");
			}
			return starttype === types$1._import ? this.parseImport(node) : this.parseExport(node, exports);
		default:
			if (this.isAsyncFunction()) {
				if (context) this.unexpected();
				this.next();
				return this.parseFunctionStatement(node, true, !context);
			}
			var usingKind = this.isAwaitUsing(false) ? "await using" : this.isUsing(false) ? "using" : null;
			if (usingKind) {
				if (!this.allowUsing) this.raise(this.start, "Using declaration cannot appear in the top level when source type is `script` or in the bare case statement");
				if (usingKind === "await using") {
					if (!this.canAwait) this.raise(this.start, "Await using cannot appear outside of async function");
					this.next();
				}
				this.next();
				this.parseVar(node, false, usingKind);
				this.semicolon();
				return this.finishNode(node, "VariableDeclaration");
			}
			var maybeName = this.value, expr = this.parseExpression();
			if (starttype === types$1.name && expr.type === "Identifier" && this.eat(types$1.colon)) return this.parseLabeledStatement(node, maybeName, expr, context);
			else return this.parseExpressionStatement(node, expr);
	}
};
pp$8.parseBreakContinueStatement = function(node, keyword) {
	var isBreak = keyword === "break";
	this.next();
	if (this.eat(types$1.semi) || this.insertSemicolon()) node.label = null;
	else if (this.type !== types$1.name) this.unexpected();
	else {
		node.label = this.parseIdent();
		this.semicolon();
	}
	var i = 0;
	for (; i < this.labels.length; ++i) {
		var lab = this.labels[i];
		if (node.label == null || lab.name === node.label.name) {
			if (lab.kind != null && (isBreak || lab.kind === "loop")) break;
			if (node.label && isBreak) break;
		}
	}
	if (i === this.labels.length) this.raise(node.start, "Unsyntactic " + keyword);
	return this.finishNode(node, isBreak ? "BreakStatement" : "ContinueStatement");
};
pp$8.parseDebuggerStatement = function(node) {
	this.next();
	this.semicolon();
	return this.finishNode(node, "DebuggerStatement");
};
pp$8.parseDoStatement = function(node) {
	this.next();
	this.labels.push(loopLabel);
	node.body = this.parseStatement("do");
	this.labels.pop();
	this.expect(types$1._while);
	node.test = this.parseParenExpression();
	if (this.options.ecmaVersion >= 6) this.eat(types$1.semi);
	else this.semicolon();
	return this.finishNode(node, "DoWhileStatement");
};
pp$8.parseForStatement = function(node) {
	this.next();
	var awaitAt = this.options.ecmaVersion >= 9 && this.canAwait && this.eatContextual("await") ? this.lastTokStart : -1;
	this.labels.push(loopLabel);
	this.enterScope(0);
	this.expect(types$1.parenL);
	if (this.type === types$1.semi) {
		if (awaitAt > -1) this.unexpected(awaitAt);
		return this.parseFor(node, null);
	}
	var isLet = this.isLet();
	if (this.type === types$1._var || this.type === types$1._const || isLet) {
		var init$1 = this.startNode(), kind = isLet ? "let" : this.value;
		this.next();
		this.parseVar(init$1, true, kind);
		this.finishNode(init$1, "VariableDeclaration");
		return this.parseForAfterInit(node, init$1, awaitAt);
	}
	var startsWithLet = this.isContextual("let"), isForOf = false;
	var usingKind = this.isUsing(true) ? "using" : this.isAwaitUsing(true) ? "await using" : null;
	if (usingKind) {
		var init$2 = this.startNode();
		this.next();
		if (usingKind === "await using") {
			if (!this.canAwait) this.raise(this.start, "Await using cannot appear outside of async function");
			this.next();
		}
		this.parseVar(init$2, true, usingKind);
		this.finishNode(init$2, "VariableDeclaration");
		return this.parseForAfterInit(node, init$2, awaitAt);
	}
	var containsEsc = this.containsEsc;
	var refDestructuringErrors = new DestructuringErrors();
	var initPos = this.start;
	var init = awaitAt > -1 ? this.parseExprSubscripts(refDestructuringErrors, "await") : this.parseExpression(true, refDestructuringErrors);
	if (this.type === types$1._in || (isForOf = this.options.ecmaVersion >= 6 && this.isContextual("of"))) {
		if (awaitAt > -1) {
			if (this.type === types$1._in) this.unexpected(awaitAt);
			node.await = true;
		} else if (isForOf && this.options.ecmaVersion >= 8) {
			if (init.start === initPos && !containsEsc && init.type === "Identifier" && init.name === "async") this.unexpected();
			else if (this.options.ecmaVersion >= 9) node.await = false;
		}
		if (startsWithLet && isForOf) this.raise(init.start, "The left-hand side of a for-of loop may not start with 'let'.");
		this.toAssignable(init, false, refDestructuringErrors);
		this.checkLValPattern(init);
		return this.parseForIn(node, init);
	} else this.checkExpressionErrors(refDestructuringErrors, true);
	if (awaitAt > -1) this.unexpected(awaitAt);
	return this.parseFor(node, init);
};
pp$8.parseForAfterInit = function(node, init, awaitAt) {
	if ((this.type === types$1._in || this.options.ecmaVersion >= 6 && this.isContextual("of")) && init.declarations.length === 1) {
		if (this.options.ecmaVersion >= 9) if (this.type === types$1._in) {
			if (awaitAt > -1) this.unexpected(awaitAt);
		} else node.await = awaitAt > -1;
		return this.parseForIn(node, init);
	}
	if (awaitAt > -1) this.unexpected(awaitAt);
	return this.parseFor(node, init);
};
pp$8.parseFunctionStatement = function(node, isAsync, declarationPosition) {
	this.next();
	return this.parseFunction(node, FUNC_STATEMENT | (declarationPosition ? 0 : FUNC_HANGING_STATEMENT), false, isAsync);
};
pp$8.parseIfStatement = function(node) {
	this.next();
	node.test = this.parseParenExpression();
	node.consequent = this.parseStatement("if");
	node.alternate = this.eat(types$1._else) ? this.parseStatement("if") : null;
	return this.finishNode(node, "IfStatement");
};
pp$8.parseReturnStatement = function(node) {
	if (!this.allowReturn) this.raise(this.start, "'return' outside of function");
	this.next();
	if (this.eat(types$1.semi) || this.insertSemicolon()) node.argument = null;
	else {
		node.argument = this.parseExpression();
		this.semicolon();
	}
	return this.finishNode(node, "ReturnStatement");
};
pp$8.parseSwitchStatement = function(node) {
	this.next();
	node.discriminant = this.parseParenExpression();
	node.cases = [];
	this.expect(types$1.braceL);
	this.labels.push(switchLabel);
	this.enterScope(SCOPE_SWITCH);
	var cur;
	for (var sawDefault = false; this.type !== types$1.braceR;) if (this.type === types$1._case || this.type === types$1._default) {
		var isCase = this.type === types$1._case;
		if (cur) this.finishNode(cur, "SwitchCase");
		node.cases.push(cur = this.startNode());
		cur.consequent = [];
		this.next();
		if (isCase) cur.test = this.parseExpression();
		else {
			if (sawDefault) this.raiseRecoverable(this.lastTokStart, "Multiple default clauses");
			sawDefault = true;
			cur.test = null;
		}
		this.expect(types$1.colon);
	} else {
		if (!cur) this.unexpected();
		cur.consequent.push(this.parseStatement(null));
	}
	this.exitScope();
	if (cur) this.finishNode(cur, "SwitchCase");
	this.next();
	this.labels.pop();
	return this.finishNode(node, "SwitchStatement");
};
pp$8.parseThrowStatement = function(node) {
	this.next();
	if (lineBreak.test(this.input.slice(this.lastTokEnd, this.start))) this.raise(this.lastTokEnd, "Illegal newline after throw");
	node.argument = this.parseExpression();
	this.semicolon();
	return this.finishNode(node, "ThrowStatement");
};
var empty$1 = [];
pp$8.parseCatchClauseParam = function() {
	var param = this.parseBindingAtom();
	var simple = param.type === "Identifier";
	this.enterScope(simple ? SCOPE_SIMPLE_CATCH : 0);
	this.checkLValPattern(param, simple ? BIND_SIMPLE_CATCH : BIND_LEXICAL);
	this.expect(types$1.parenR);
	return param;
};
pp$8.parseTryStatement = function(node) {
	this.next();
	node.block = this.parseBlock();
	node.handler = null;
	if (this.type === types$1._catch) {
		var clause = this.startNode();
		this.next();
		if (this.eat(types$1.parenL)) clause.param = this.parseCatchClauseParam();
		else {
			if (this.options.ecmaVersion < 10) this.unexpected();
			clause.param = null;
			this.enterScope(0);
		}
		clause.body = this.parseBlock(false);
		this.exitScope();
		node.handler = this.finishNode(clause, "CatchClause");
	}
	node.finalizer = this.eat(types$1._finally) ? this.parseBlock() : null;
	if (!node.handler && !node.finalizer) this.raise(node.start, "Missing catch or finally clause");
	return this.finishNode(node, "TryStatement");
};
pp$8.parseVarStatement = function(node, kind, allowMissingInitializer) {
	this.next();
	this.parseVar(node, false, kind, allowMissingInitializer);
	this.semicolon();
	return this.finishNode(node, "VariableDeclaration");
};
pp$8.parseWhileStatement = function(node) {
	this.next();
	node.test = this.parseParenExpression();
	this.labels.push(loopLabel);
	node.body = this.parseStatement("while");
	this.labels.pop();
	return this.finishNode(node, "WhileStatement");
};
pp$8.parseWithStatement = function(node) {
	if (this.strict) this.raise(this.start, "'with' in strict mode");
	this.next();
	node.object = this.parseParenExpression();
	node.body = this.parseStatement("with");
	return this.finishNode(node, "WithStatement");
};
pp$8.parseEmptyStatement = function(node) {
	this.next();
	return this.finishNode(node, "EmptyStatement");
};
pp$8.parseLabeledStatement = function(node, maybeName, expr, context) {
	for (var i$1 = 0, list = this.labels; i$1 < list.length; i$1 += 1) if (list[i$1].name === maybeName) this.raise(expr.start, "Label '" + maybeName + "' is already declared");
	var kind = this.type.isLoop ? "loop" : this.type === types$1._switch ? "switch" : null;
	for (var i = this.labels.length - 1; i >= 0; i--) {
		var label$1 = this.labels[i];
		if (label$1.statementStart === node.start) {
			label$1.statementStart = this.start;
			label$1.kind = kind;
		} else break;
	}
	this.labels.push({
		name: maybeName,
		kind,
		statementStart: this.start
	});
	node.body = this.parseStatement(context ? context.indexOf("label") === -1 ? context + "label" : context : "label");
	this.labels.pop();
	node.label = expr;
	return this.finishNode(node, "LabeledStatement");
};
pp$8.parseExpressionStatement = function(node, expr) {
	node.expression = expr;
	this.semicolon();
	return this.finishNode(node, "ExpressionStatement");
};
pp$8.parseBlock = function(createNewLexicalScope, node, exitStrict) {
	if (createNewLexicalScope === void 0) createNewLexicalScope = true;
	if (node === void 0) node = this.startNode();
	node.body = [];
	this.expect(types$1.braceL);
	if (createNewLexicalScope) this.enterScope(0);
	while (this.type !== types$1.braceR) {
		var stmt = this.parseStatement(null);
		node.body.push(stmt);
	}
	if (exitStrict) this.strict = false;
	this.next();
	if (createNewLexicalScope) this.exitScope();
	return this.finishNode(node, "BlockStatement");
};
pp$8.parseFor = function(node, init) {
	node.init = init;
	this.expect(types$1.semi);
	node.test = this.type === types$1.semi ? null : this.parseExpression();
	this.expect(types$1.semi);
	node.update = this.type === types$1.parenR ? null : this.parseExpression();
	this.expect(types$1.parenR);
	node.body = this.parseStatement("for");
	this.exitScope();
	this.labels.pop();
	return this.finishNode(node, "ForStatement");
};
pp$8.parseForIn = function(node, init) {
	var isForIn = this.type === types$1._in;
	this.next();
	if (init.type === "VariableDeclaration" && init.declarations[0].init != null && (!isForIn || this.options.ecmaVersion < 8 || this.strict || init.kind !== "var" || init.declarations[0].id.type !== "Identifier")) this.raise(init.start, (isForIn ? "for-in" : "for-of") + " loop variable declaration may not have an initializer");
	node.left = init;
	node.right = isForIn ? this.parseExpression() : this.parseMaybeAssign();
	this.expect(types$1.parenR);
	node.body = this.parseStatement("for");
	this.exitScope();
	this.labels.pop();
	return this.finishNode(node, isForIn ? "ForInStatement" : "ForOfStatement");
};
pp$8.parseVar = function(node, isFor, kind, allowMissingInitializer) {
	node.declarations = [];
	node.kind = kind;
	for (;;) {
		var decl = this.startNode();
		this.parseVarId(decl, kind);
		if (this.eat(types$1.eq)) decl.init = this.parseMaybeAssign(isFor);
		else if (!allowMissingInitializer && kind === "const" && !(this.type === types$1._in || this.options.ecmaVersion >= 6 && this.isContextual("of"))) this.unexpected();
		else if (!allowMissingInitializer && (kind === "using" || kind === "await using") && this.options.ecmaVersion >= 17 && this.type !== types$1._in && !this.isContextual("of")) this.raise(this.lastTokEnd, "Missing initializer in " + kind + " declaration");
		else if (!allowMissingInitializer && decl.id.type !== "Identifier" && !(isFor && (this.type === types$1._in || this.isContextual("of")))) this.raise(this.lastTokEnd, "Complex binding patterns require an initialization value");
		else decl.init = null;
		node.declarations.push(this.finishNode(decl, "VariableDeclarator"));
		if (!this.eat(types$1.comma)) break;
	}
	return node;
};
pp$8.parseVarId = function(decl, kind) {
	decl.id = kind === "using" || kind === "await using" ? this.parseIdent() : this.parseBindingAtom();
	this.checkLValPattern(decl.id, kind === "var" ? BIND_VAR : BIND_LEXICAL, false);
};
var FUNC_STATEMENT = 1, FUNC_HANGING_STATEMENT = 2, FUNC_NULLABLE_ID = 4;
pp$8.parseFunction = function(node, statement, allowExpressionBody, isAsync, forInit) {
	this.initFunction(node);
	if (this.options.ecmaVersion >= 9 || this.options.ecmaVersion >= 6 && !isAsync) {
		if (this.type === types$1.star && statement & FUNC_HANGING_STATEMENT) this.unexpected();
		node.generator = this.eat(types$1.star);
	}
	if (this.options.ecmaVersion >= 8) node.async = !!isAsync;
	if (statement & FUNC_STATEMENT) {
		node.id = statement & FUNC_NULLABLE_ID && this.type !== types$1.name ? null : this.parseIdent();
		if (node.id && !(statement & FUNC_HANGING_STATEMENT)) this.checkLValSimple(node.id, this.strict || node.generator || node.async ? this.treatFunctionsAsVar ? BIND_VAR : BIND_LEXICAL : BIND_FUNCTION);
	}
	var oldYieldPos = this.yieldPos, oldAwaitPos = this.awaitPos, oldAwaitIdentPos = this.awaitIdentPos;
	this.yieldPos = 0;
	this.awaitPos = 0;
	this.awaitIdentPos = 0;
	this.enterScope(functionFlags(node.async, node.generator));
	if (!(statement & FUNC_STATEMENT)) node.id = this.type === types$1.name ? this.parseIdent() : null;
	this.parseFunctionParams(node);
	this.parseFunctionBody(node, allowExpressionBody, false, forInit);
	this.yieldPos = oldYieldPos;
	this.awaitPos = oldAwaitPos;
	this.awaitIdentPos = oldAwaitIdentPos;
	return this.finishNode(node, statement & FUNC_STATEMENT ? "FunctionDeclaration" : "FunctionExpression");
};
pp$8.parseFunctionParams = function(node) {
	this.expect(types$1.parenL);
	node.params = this.parseBindingList(types$1.parenR, false, this.options.ecmaVersion >= 8);
	this.checkYieldAwaitInDefaultParams();
};
pp$8.parseClass = function(node, isStatement) {
	this.next();
	var oldStrict = this.strict;
	this.strict = true;
	this.parseClassId(node, isStatement);
	this.parseClassSuper(node);
	var privateNameMap = this.enterClassBody();
	var classBody = this.startNode();
	var hadConstructor = false;
	classBody.body = [];
	this.expect(types$1.braceL);
	while (this.type !== types$1.braceR) {
		var element = this.parseClassElement(node.superClass !== null);
		if (element) {
			classBody.body.push(element);
			if (element.type === "MethodDefinition" && element.kind === "constructor") {
				if (hadConstructor) this.raiseRecoverable(element.start, "Duplicate constructor in the same class");
				hadConstructor = true;
			} else if (element.key && element.key.type === "PrivateIdentifier" && isPrivateNameConflicted(privateNameMap, element)) this.raiseRecoverable(element.key.start, "Identifier '#" + element.key.name + "' has already been declared");
		}
	}
	this.strict = oldStrict;
	this.next();
	node.body = this.finishNode(classBody, "ClassBody");
	this.exitClassBody();
	return this.finishNode(node, isStatement ? "ClassDeclaration" : "ClassExpression");
};
pp$8.parseClassElement = function(constructorAllowsSuper) {
	if (this.eat(types$1.semi)) return null;
	var ecmaVersion = this.options.ecmaVersion;
	var node = this.startNode();
	var keyName = "";
	var isGenerator = false;
	var isAsync = false;
	var kind = "method";
	var isStatic = false;
	if (this.eatContextual("static")) {
		if (ecmaVersion >= 13 && this.eat(types$1.braceL)) {
			this.parseClassStaticBlock(node);
			return node;
		}
		if (this.isClassElementNameStart() || this.type === types$1.star) isStatic = true;
		else keyName = "static";
	}
	node.static = isStatic;
	if (!keyName && ecmaVersion >= 8 && this.eatContextual("async")) if ((this.isClassElementNameStart() || this.type === types$1.star) && !this.canInsertSemicolon()) isAsync = true;
	else keyName = "async";
	if (!keyName && (ecmaVersion >= 9 || !isAsync) && this.eat(types$1.star)) isGenerator = true;
	if (!keyName && !isAsync && !isGenerator) {
		var lastValue = this.value;
		if (this.eatContextual("get") || this.eatContextual("set")) if (this.isClassElementNameStart()) kind = lastValue;
		else keyName = lastValue;
	}
	if (keyName) {
		node.computed = false;
		node.key = this.startNodeAt(this.lastTokStart, this.lastTokStartLoc);
		node.key.name = keyName;
		this.finishNode(node.key, "Identifier");
	} else this.parseClassElementName(node);
	if (ecmaVersion < 13 || this.type === types$1.parenL || kind !== "method" || isGenerator || isAsync) {
		var isConstructor = !node.static && checkKeyName(node, "constructor");
		var allowsDirectSuper = isConstructor && constructorAllowsSuper;
		if (isConstructor && kind !== "method") this.raise(node.key.start, "Constructor can't have get/set modifier");
		node.kind = isConstructor ? "constructor" : kind;
		this.parseClassMethod(node, isGenerator, isAsync, allowsDirectSuper);
	} else this.parseClassField(node);
	return node;
};
pp$8.isClassElementNameStart = function() {
	return this.type === types$1.name || this.type === types$1.privateId || this.type === types$1.num || this.type === types$1.string || this.type === types$1.bracketL || this.type.keyword;
};
pp$8.parseClassElementName = function(element) {
	if (this.type === types$1.privateId) {
		if (this.value === "constructor") this.raise(this.start, "Classes can't have an element named '#constructor'");
		element.computed = false;
		element.key = this.parsePrivateIdent();
	} else this.parsePropertyName(element);
};
pp$8.parseClassMethod = function(method, isGenerator, isAsync, allowsDirectSuper) {
	var key = method.key;
	if (method.kind === "constructor") {
		if (isGenerator) this.raise(key.start, "Constructor can't be a generator");
		if (isAsync) this.raise(key.start, "Constructor can't be an async method");
	} else if (method.static && checkKeyName(method, "prototype")) this.raise(key.start, "Classes may not have a static property named prototype");
	var value = method.value = this.parseMethod(isGenerator, isAsync, allowsDirectSuper);
	if (method.kind === "get" && value.params.length !== 0) this.raiseRecoverable(value.start, "getter should have no params");
	if (method.kind === "set" && value.params.length !== 1) this.raiseRecoverable(value.start, "setter should have exactly one param");
	if (method.kind === "set" && value.params[0].type === "RestElement") this.raiseRecoverable(value.params[0].start, "Setter cannot use rest params");
	return this.finishNode(method, "MethodDefinition");
};
pp$8.parseClassField = function(field) {
	if (checkKeyName(field, "constructor")) this.raise(field.key.start, "Classes can't have a field named 'constructor'");
	else if (field.static && checkKeyName(field, "prototype")) this.raise(field.key.start, "Classes can't have a static field named 'prototype'");
	if (this.eat(types$1.eq)) {
		this.enterScope(SCOPE_CLASS_FIELD_INIT | SCOPE_SUPER);
		field.value = this.parseMaybeAssign();
		this.exitScope();
	} else field.value = null;
	this.semicolon();
	return this.finishNode(field, "PropertyDefinition");
};
pp$8.parseClassStaticBlock = function(node) {
	node.body = [];
	var oldLabels = this.labels;
	this.labels = [];
	this.enterScope(SCOPE_CLASS_STATIC_BLOCK | SCOPE_SUPER);
	while (this.type !== types$1.braceR) {
		var stmt = this.parseStatement(null);
		node.body.push(stmt);
	}
	this.next();
	this.exitScope();
	this.labels = oldLabels;
	return this.finishNode(node, "StaticBlock");
};
pp$8.parseClassId = function(node, isStatement) {
	if (this.type === types$1.name) {
		node.id = this.parseIdent();
		if (isStatement) this.checkLValSimple(node.id, BIND_LEXICAL, false);
	} else {
		if (isStatement === true) this.unexpected();
		node.id = null;
	}
};
pp$8.parseClassSuper = function(node) {
	node.superClass = this.eat(types$1._extends) ? this.parseExprSubscripts(null, false) : null;
};
pp$8.enterClassBody = function() {
	var element = {
		declared: Object.create(null),
		used: []
	};
	this.privateNameStack.push(element);
	return element.declared;
};
pp$8.exitClassBody = function() {
	var ref = this.privateNameStack.pop();
	var declared = ref.declared;
	var used = ref.used;
	if (!this.options.checkPrivateFields) return;
	var len = this.privateNameStack.length;
	var parent = len === 0 ? null : this.privateNameStack[len - 1];
	for (var i = 0; i < used.length; ++i) {
		var id = used[i];
		if (!hasOwn(declared, id.name)) if (parent) parent.used.push(id);
		else this.raiseRecoverable(id.start, "Private field '#" + id.name + "' must be declared in an enclosing class");
	}
};
function isPrivateNameConflicted(privateNameMap, element) {
	var name = element.key.name;
	var curr = privateNameMap[name];
	var next = "true";
	if (element.type === "MethodDefinition" && (element.kind === "get" || element.kind === "set")) next = (element.static ? "s" : "i") + element.kind;
	if (curr === "iget" && next === "iset" || curr === "iset" && next === "iget" || curr === "sget" && next === "sset" || curr === "sset" && next === "sget") {
		privateNameMap[name] = "true";
		return false;
	} else if (!curr) {
		privateNameMap[name] = next;
		return false;
	} else return true;
}
function checkKeyName(node, name) {
	var computed = node.computed;
	var key = node.key;
	return !computed && (key.type === "Identifier" && key.name === name || key.type === "Literal" && key.value === name);
}
pp$8.parseExportAllDeclaration = function(node, exports) {
	if (this.options.ecmaVersion >= 11) if (this.eatContextual("as")) {
		node.exported = this.parseModuleExportName();
		this.checkExport(exports, node.exported, this.lastTokStart);
	} else node.exported = null;
	this.expectContextual("from");
	if (this.type !== types$1.string) this.unexpected();
	node.source = this.parseExprAtom();
	if (this.options.ecmaVersion >= 16) node.attributes = this.parseWithClause();
	this.semicolon();
	return this.finishNode(node, "ExportAllDeclaration");
};
pp$8.parseExport = function(node, exports) {
	this.next();
	if (this.eat(types$1.star)) return this.parseExportAllDeclaration(node, exports);
	if (this.eat(types$1._default)) {
		this.checkExport(exports, "default", this.lastTokStart);
		node.declaration = this.parseExportDefaultDeclaration();
		return this.finishNode(node, "ExportDefaultDeclaration");
	}
	if (this.shouldParseExportStatement()) {
		node.declaration = this.parseExportDeclaration(node);
		if (node.declaration.type === "VariableDeclaration") this.checkVariableExport(exports, node.declaration.declarations);
		else this.checkExport(exports, node.declaration.id, node.declaration.id.start);
		node.specifiers = [];
		node.source = null;
		if (this.options.ecmaVersion >= 16) node.attributes = [];
	} else {
		node.declaration = null;
		node.specifiers = this.parseExportSpecifiers(exports);
		if (this.eatContextual("from")) {
			if (this.type !== types$1.string) this.unexpected();
			node.source = this.parseExprAtom();
			if (this.options.ecmaVersion >= 16) node.attributes = this.parseWithClause();
		} else {
			for (var i = 0, list = node.specifiers; i < list.length; i += 1) {
				var spec = list[i];
				this.checkUnreserved(spec.local);
				this.checkLocalExport(spec.local);
				if (spec.local.type === "Literal") this.raise(spec.local.start, "A string literal cannot be used as an exported binding without `from`.");
			}
			node.source = null;
			if (this.options.ecmaVersion >= 16) node.attributes = [];
		}
		this.semicolon();
	}
	return this.finishNode(node, "ExportNamedDeclaration");
};
pp$8.parseExportDeclaration = function(node) {
	return this.parseStatement(null);
};
pp$8.parseExportDefaultDeclaration = function() {
	var isAsync;
	if (this.type === types$1._function || (isAsync = this.isAsyncFunction())) {
		var fNode = this.startNode();
		this.next();
		if (isAsync) this.next();
		return this.parseFunction(fNode, FUNC_STATEMENT | FUNC_NULLABLE_ID, false, isAsync);
	} else if (this.type === types$1._class) {
		var cNode = this.startNode();
		return this.parseClass(cNode, "nullableID");
	} else {
		var declaration = this.parseMaybeAssign();
		this.semicolon();
		return declaration;
	}
};
pp$8.checkExport = function(exports, name, pos) {
	if (!exports) return;
	if (typeof name !== "string") name = name.type === "Identifier" ? name.name : name.value;
	if (hasOwn(exports, name)) this.raiseRecoverable(pos, "Duplicate export '" + name + "'");
	exports[name] = true;
};
pp$8.checkPatternExport = function(exports, pat) {
	var type = pat.type;
	if (type === "Identifier") this.checkExport(exports, pat, pat.start);
	else if (type === "ObjectPattern") for (var i = 0, list = pat.properties; i < list.length; i += 1) {
		var prop = list[i];
		this.checkPatternExport(exports, prop);
	}
	else if (type === "ArrayPattern") for (var i$1 = 0, list$1 = pat.elements; i$1 < list$1.length; i$1 += 1) {
		var elt = list$1[i$1];
		if (elt) this.checkPatternExport(exports, elt);
	}
	else if (type === "Property") this.checkPatternExport(exports, pat.value);
	else if (type === "AssignmentPattern") this.checkPatternExport(exports, pat.left);
	else if (type === "RestElement") this.checkPatternExport(exports, pat.argument);
};
pp$8.checkVariableExport = function(exports, decls) {
	if (!exports) return;
	for (var i = 0, list = decls; i < list.length; i += 1) {
		var decl = list[i];
		this.checkPatternExport(exports, decl.id);
	}
};
pp$8.shouldParseExportStatement = function() {
	return this.type.keyword === "var" || this.type.keyword === "const" || this.type.keyword === "class" || this.type.keyword === "function" || this.isLet() || this.isAsyncFunction();
};
pp$8.parseExportSpecifier = function(exports) {
	var node = this.startNode();
	node.local = this.parseModuleExportName();
	node.exported = this.eatContextual("as") ? this.parseModuleExportName() : node.local;
	this.checkExport(exports, node.exported, node.exported.start);
	return this.finishNode(node, "ExportSpecifier");
};
pp$8.parseExportSpecifiers = function(exports) {
	var nodes = [], first = true;
	this.expect(types$1.braceL);
	while (!this.eat(types$1.braceR)) {
		if (!first) {
			this.expect(types$1.comma);
			if (this.afterTrailingComma(types$1.braceR)) break;
		} else first = false;
		nodes.push(this.parseExportSpecifier(exports));
	}
	return nodes;
};
pp$8.parseImport = function(node) {
	this.next();
	if (this.type === types$1.string) {
		node.specifiers = empty$1;
		node.source = this.parseExprAtom();
	} else {
		node.specifiers = this.parseImportSpecifiers();
		this.expectContextual("from");
		node.source = this.type === types$1.string ? this.parseExprAtom() : this.unexpected();
	}
	if (this.options.ecmaVersion >= 16) node.attributes = this.parseWithClause();
	this.semicolon();
	return this.finishNode(node, "ImportDeclaration");
};
pp$8.parseImportSpecifier = function() {
	var node = this.startNode();
	node.imported = this.parseModuleExportName();
	if (this.eatContextual("as")) node.local = this.parseIdent();
	else {
		this.checkUnreserved(node.imported);
		node.local = node.imported;
	}
	this.checkLValSimple(node.local, BIND_LEXICAL);
	return this.finishNode(node, "ImportSpecifier");
};
pp$8.parseImportDefaultSpecifier = function() {
	var node = this.startNode();
	node.local = this.parseIdent();
	this.checkLValSimple(node.local, BIND_LEXICAL);
	return this.finishNode(node, "ImportDefaultSpecifier");
};
pp$8.parseImportNamespaceSpecifier = function() {
	var node = this.startNode();
	this.next();
	this.expectContextual("as");
	node.local = this.parseIdent();
	this.checkLValSimple(node.local, BIND_LEXICAL);
	return this.finishNode(node, "ImportNamespaceSpecifier");
};
pp$8.parseImportSpecifiers = function() {
	var nodes = [], first = true;
	if (this.type === types$1.name) {
		nodes.push(this.parseImportDefaultSpecifier());
		if (!this.eat(types$1.comma)) return nodes;
	}
	if (this.type === types$1.star) {
		nodes.push(this.parseImportNamespaceSpecifier());
		return nodes;
	}
	this.expect(types$1.braceL);
	while (!this.eat(types$1.braceR)) {
		if (!first) {
			this.expect(types$1.comma);
			if (this.afterTrailingComma(types$1.braceR)) break;
		} else first = false;
		nodes.push(this.parseImportSpecifier());
	}
	return nodes;
};
pp$8.parseWithClause = function() {
	var nodes = [];
	if (!this.eat(types$1._with)) return nodes;
	this.expect(types$1.braceL);
	var attributeKeys = {};
	var first = true;
	while (!this.eat(types$1.braceR)) {
		if (!first) {
			this.expect(types$1.comma);
			if (this.afterTrailingComma(types$1.braceR)) break;
		} else first = false;
		var attr = this.parseImportAttribute();
		var keyName = attr.key.type === "Identifier" ? attr.key.name : attr.key.value;
		if (hasOwn(attributeKeys, keyName)) this.raiseRecoverable(attr.key.start, "Duplicate attribute key '" + keyName + "'");
		attributeKeys[keyName] = true;
		nodes.push(attr);
	}
	return nodes;
};
pp$8.parseImportAttribute = function() {
	var node = this.startNode();
	node.key = this.type === types$1.string ? this.parseExprAtom() : this.parseIdent(this.options.allowReserved !== "never");
	this.expect(types$1.colon);
	if (this.type !== types$1.string) this.unexpected();
	node.value = this.parseExprAtom();
	return this.finishNode(node, "ImportAttribute");
};
pp$8.parseModuleExportName = function() {
	if (this.options.ecmaVersion >= 13 && this.type === types$1.string) {
		var stringLiteral = this.parseLiteral(this.value);
		if (loneSurrogate.test(stringLiteral.value)) this.raise(stringLiteral.start, "An export name cannot include a lone surrogate.");
		return stringLiteral;
	}
	return this.parseIdent(true);
};
pp$8.adaptDirectivePrologue = function(statements) {
	for (var i = 0; i < statements.length && this.isDirectiveCandidate(statements[i]); ++i) statements[i].directive = statements[i].expression.raw.slice(1, -1);
};
pp$8.isDirectiveCandidate = function(statement) {
	return this.options.ecmaVersion >= 5 && statement.type === "ExpressionStatement" && statement.expression.type === "Literal" && typeof statement.expression.value === "string" && (this.input[statement.start] === "\"" || this.input[statement.start] === "'");
};
var pp$7 = Parser.prototype;
pp$7.toAssignable = function(node, isBinding, refDestructuringErrors) {
	if (this.options.ecmaVersion >= 6 && node) switch (node.type) {
		case "Identifier":
			if (this.inAsync && node.name === "await") this.raise(node.start, "Cannot use 'await' as identifier inside an async function");
			break;
		case "ObjectPattern":
		case "ArrayPattern":
		case "AssignmentPattern":
		case "RestElement": break;
		case "ObjectExpression":
			node.type = "ObjectPattern";
			if (refDestructuringErrors) this.checkPatternErrors(refDestructuringErrors, true);
			for (var i = 0, list = node.properties; i < list.length; i += 1) {
				var prop = list[i];
				this.toAssignable(prop, isBinding);
				if (prop.type === "RestElement" && (prop.argument.type === "ArrayPattern" || prop.argument.type === "ObjectPattern")) this.raise(prop.argument.start, "Unexpected token");
			}
			break;
		case "Property":
			if (node.kind !== "init") this.raise(node.key.start, "Object pattern can't contain getter or setter");
			this.toAssignable(node.value, isBinding);
			break;
		case "ArrayExpression":
			node.type = "ArrayPattern";
			if (refDestructuringErrors) this.checkPatternErrors(refDestructuringErrors, true);
			this.toAssignableList(node.elements, isBinding);
			break;
		case "SpreadElement":
			node.type = "RestElement";
			this.toAssignable(node.argument, isBinding);
			if (node.argument.type === "AssignmentPattern") this.raise(node.argument.start, "Rest elements cannot have a default value");
			break;
		case "AssignmentExpression":
			if (node.operator !== "=") this.raise(node.left.end, "Only '=' operator can be used for specifying default value.");
			node.type = "AssignmentPattern";
			delete node.operator;
			this.toAssignable(node.left, isBinding);
			break;
		case "ParenthesizedExpression":
			this.toAssignable(node.expression, isBinding, refDestructuringErrors);
			break;
		case "ChainExpression":
			this.raiseRecoverable(node.start, "Optional chaining cannot appear in left-hand side");
			break;
		case "MemberExpression": if (!isBinding) break;
		default: this.raise(node.start, "Assigning to rvalue");
	}
	else if (refDestructuringErrors) this.checkPatternErrors(refDestructuringErrors, true);
	return node;
};
pp$7.toAssignableList = function(exprList, isBinding) {
	var end = exprList.length;
	for (var i = 0; i < end; i++) {
		var elt = exprList[i];
		if (elt) this.toAssignable(elt, isBinding);
	}
	if (end) {
		var last = exprList[end - 1];
		if (this.options.ecmaVersion === 6 && isBinding && last && last.type === "RestElement" && last.argument.type !== "Identifier") this.unexpected(last.argument.start);
	}
	return exprList;
};
pp$7.parseSpread = function(refDestructuringErrors) {
	var node = this.startNode();
	this.next();
	node.argument = this.parseMaybeAssign(false, refDestructuringErrors);
	return this.finishNode(node, "SpreadElement");
};
pp$7.parseRestBinding = function() {
	var node = this.startNode();
	this.next();
	if (this.options.ecmaVersion === 6 && this.type !== types$1.name) this.unexpected();
	node.argument = this.parseBindingAtom();
	return this.finishNode(node, "RestElement");
};
pp$7.parseBindingAtom = function() {
	if (this.options.ecmaVersion >= 6) switch (this.type) {
		case types$1.bracketL:
			var node = this.startNode();
			this.next();
			node.elements = this.parseBindingList(types$1.bracketR, true, true);
			return this.finishNode(node, "ArrayPattern");
		case types$1.braceL: return this.parseObj(true);
	}
	return this.parseIdent();
};
pp$7.parseBindingList = function(close, allowEmpty, allowTrailingComma, allowModifiers) {
	var elts = [], first = true;
	while (!this.eat(close)) {
		if (first) first = false;
		else this.expect(types$1.comma);
		if (allowEmpty && this.type === types$1.comma) elts.push(null);
		else if (allowTrailingComma && this.afterTrailingComma(close)) break;
		else if (this.type === types$1.ellipsis) {
			var rest = this.parseRestBinding();
			this.parseBindingListItem(rest);
			elts.push(rest);
			if (this.type === types$1.comma) this.raiseRecoverable(this.start, "Comma is not permitted after the rest element");
			this.expect(close);
			break;
		} else elts.push(this.parseAssignableListItem(allowModifiers));
	}
	return elts;
};
pp$7.parseAssignableListItem = function(allowModifiers) {
	var elem = this.parseMaybeDefault(this.start, this.startLoc);
	this.parseBindingListItem(elem);
	return elem;
};
pp$7.parseBindingListItem = function(param) {
	return param;
};
pp$7.parseMaybeDefault = function(startPos, startLoc, left) {
	left = left || this.parseBindingAtom();
	if (this.options.ecmaVersion < 6 || !this.eat(types$1.eq)) return left;
	var node = this.startNodeAt(startPos, startLoc);
	node.left = left;
	node.right = this.parseMaybeAssign();
	return this.finishNode(node, "AssignmentPattern");
};
pp$7.checkLValSimple = function(expr, bindingType, checkClashes) {
	if (bindingType === void 0) bindingType = BIND_NONE;
	var isBind = bindingType !== BIND_NONE;
	switch (expr.type) {
		case "Identifier":
			if (this.strict && this.reservedWordsStrictBind.test(expr.name)) this.raiseRecoverable(expr.start, (isBind ? "Binding " : "Assigning to ") + expr.name + " in strict mode");
			if (isBind) {
				if (bindingType === BIND_LEXICAL && expr.name === "let") this.raiseRecoverable(expr.start, "let is disallowed as a lexically bound name");
				if (checkClashes) {
					if (hasOwn(checkClashes, expr.name)) this.raiseRecoverable(expr.start, "Argument name clash");
					checkClashes[expr.name] = true;
				}
				if (bindingType !== BIND_OUTSIDE) this.declareName(expr.name, bindingType, expr.start);
			}
			break;
		case "ChainExpression":
			this.raiseRecoverable(expr.start, "Optional chaining cannot appear in left-hand side");
			break;
		case "MemberExpression":
			if (isBind) this.raiseRecoverable(expr.start, "Binding member expression");
			break;
		case "ParenthesizedExpression":
			if (isBind) this.raiseRecoverable(expr.start, "Binding parenthesized expression");
			return this.checkLValSimple(expr.expression, bindingType, checkClashes);
		default: this.raise(expr.start, (isBind ? "Binding" : "Assigning to") + " rvalue");
	}
};
pp$7.checkLValPattern = function(expr, bindingType, checkClashes) {
	if (bindingType === void 0) bindingType = BIND_NONE;
	switch (expr.type) {
		case "ObjectPattern":
			for (var i = 0, list = expr.properties; i < list.length; i += 1) {
				var prop = list[i];
				this.checkLValInnerPattern(prop, bindingType, checkClashes);
			}
			break;
		case "ArrayPattern":
			for (var i$1 = 0, list$1 = expr.elements; i$1 < list$1.length; i$1 += 1) {
				var elem = list$1[i$1];
				if (elem) this.checkLValInnerPattern(elem, bindingType, checkClashes);
			}
			break;
		default: this.checkLValSimple(expr, bindingType, checkClashes);
	}
};
pp$7.checkLValInnerPattern = function(expr, bindingType, checkClashes) {
	if (bindingType === void 0) bindingType = BIND_NONE;
	switch (expr.type) {
		case "Property":
			this.checkLValInnerPattern(expr.value, bindingType, checkClashes);
			break;
		case "AssignmentPattern":
			this.checkLValPattern(expr.left, bindingType, checkClashes);
			break;
		case "RestElement":
			this.checkLValPattern(expr.argument, bindingType, checkClashes);
			break;
		default: this.checkLValPattern(expr, bindingType, checkClashes);
	}
};
var TokContext = function TokContext(token, isExpr, preserveSpace, override, generator) {
	this.token = token;
	this.isExpr = !!isExpr;
	this.preserveSpace = !!preserveSpace;
	this.override = override;
	this.generator = !!generator;
};
var types$2 = {
	b_stat: new TokContext("{", false),
	b_expr: new TokContext("{", true),
	b_tmpl: new TokContext("${", false),
	p_stat: new TokContext("(", false),
	p_expr: new TokContext("(", true),
	q_tmpl: new TokContext("`", true, true, function(p) {
		return p.tryReadTemplateToken();
	}),
	f_stat: new TokContext("function", false),
	f_expr: new TokContext("function", true),
	f_expr_gen: new TokContext("function", true, false, null, true),
	f_gen: new TokContext("function", false, false, null, true)
};
var pp$6 = Parser.prototype;
pp$6.initialContext = function() {
	return [types$2.b_stat];
};
pp$6.curContext = function() {
	return this.context[this.context.length - 1];
};
pp$6.braceIsBlock = function(prevType) {
	var parent = this.curContext();
	if (parent === types$2.f_expr || parent === types$2.f_stat) return true;
	if (prevType === types$1.colon && (parent === types$2.b_stat || parent === types$2.b_expr)) return !parent.isExpr;
	if (prevType === types$1._return || prevType === types$1.name && this.exprAllowed) return lineBreak.test(this.input.slice(this.lastTokEnd, this.start));
	if (prevType === types$1._else || prevType === types$1.semi || prevType === types$1.eof || prevType === types$1.parenR || prevType === types$1.arrow) return true;
	if (prevType === types$1.braceL) return parent === types$2.b_stat;
	if (prevType === types$1._var || prevType === types$1._const || prevType === types$1.name) return false;
	return !this.exprAllowed;
};
pp$6.inGeneratorContext = function() {
	for (var i = this.context.length - 1; i >= 1; i--) {
		var context = this.context[i];
		if (context.token === "function") return context.generator;
	}
	return false;
};
pp$6.updateContext = function(prevType) {
	var update, type = this.type;
	if (type.keyword && prevType === types$1.dot) this.exprAllowed = false;
	else if (update = type.updateContext) update.call(this, prevType);
	else this.exprAllowed = type.beforeExpr;
};
pp$6.overrideContext = function(tokenCtx) {
	if (this.curContext() !== tokenCtx) this.context[this.context.length - 1] = tokenCtx;
};
types$1.parenR.updateContext = types$1.braceR.updateContext = function() {
	if (this.context.length === 1) {
		this.exprAllowed = true;
		return;
	}
	var out = this.context.pop();
	if (out === types$2.b_stat && this.curContext().token === "function") out = this.context.pop();
	this.exprAllowed = !out.isExpr;
};
types$1.braceL.updateContext = function(prevType) {
	this.context.push(this.braceIsBlock(prevType) ? types$2.b_stat : types$2.b_expr);
	this.exprAllowed = true;
};
types$1.dollarBraceL.updateContext = function() {
	this.context.push(types$2.b_tmpl);
	this.exprAllowed = true;
};
types$1.parenL.updateContext = function(prevType) {
	var statementParens = prevType === types$1._if || prevType === types$1._for || prevType === types$1._with || prevType === types$1._while;
	this.context.push(statementParens ? types$2.p_stat : types$2.p_expr);
	this.exprAllowed = true;
};
types$1.incDec.updateContext = function() {};
types$1._function.updateContext = types$1._class.updateContext = function(prevType) {
	if (prevType.beforeExpr && prevType !== types$1._else && !(prevType === types$1.semi && this.curContext() !== types$2.p_stat) && !(prevType === types$1._return && lineBreak.test(this.input.slice(this.lastTokEnd, this.start))) && !((prevType === types$1.colon || prevType === types$1.braceL) && this.curContext() === types$2.b_stat)) this.context.push(types$2.f_expr);
	else this.context.push(types$2.f_stat);
	this.exprAllowed = false;
};
types$1.colon.updateContext = function() {
	if (this.curContext().token === "function") this.context.pop();
	this.exprAllowed = true;
};
types$1.backQuote.updateContext = function() {
	if (this.curContext() === types$2.q_tmpl) this.context.pop();
	else this.context.push(types$2.q_tmpl);
	this.exprAllowed = false;
};
types$1.star.updateContext = function(prevType) {
	if (prevType === types$1._function) {
		var index = this.context.length - 1;
		if (this.context[index] === types$2.f_expr) this.context[index] = types$2.f_expr_gen;
		else this.context[index] = types$2.f_gen;
	}
	this.exprAllowed = true;
};
types$1.name.updateContext = function(prevType) {
	var allowed = false;
	if (this.options.ecmaVersion >= 6 && prevType !== types$1.dot) {
		if (this.value === "of" && !this.exprAllowed || this.value === "yield" && this.inGeneratorContext()) allowed = true;
	}
	this.exprAllowed = allowed;
};
var pp$5 = Parser.prototype;
pp$5.checkPropClash = function(prop, propHash, refDestructuringErrors) {
	if (this.options.ecmaVersion >= 9 && prop.type === "SpreadElement") return;
	if (this.options.ecmaVersion >= 6 && (prop.computed || prop.method || prop.shorthand)) return;
	var key = prop.key;
	var name;
	switch (key.type) {
		case "Identifier":
			name = key.name;
			break;
		case "Literal":
			name = String(key.value);
			break;
		default: return;
	}
	var kind = prop.kind;
	if (this.options.ecmaVersion >= 6) {
		if (name === "__proto__" && kind === "init") {
			if (propHash.proto) if (refDestructuringErrors) {
				if (refDestructuringErrors.doubleProto < 0) refDestructuringErrors.doubleProto = key.start;
			} else this.raiseRecoverable(key.start, "Redefinition of __proto__ property");
			propHash.proto = true;
		}
		return;
	}
	name = "$" + name;
	var other = propHash[name];
	if (other) {
		var redefinition;
		if (kind === "init") redefinition = this.strict && other.init || other.get || other.set;
		else redefinition = other.init || other[kind];
		if (redefinition) this.raiseRecoverable(key.start, "Redefinition of property");
	} else other = propHash[name] = {
		init: false,
		get: false,
		set: false
	};
	other[kind] = true;
};
pp$5.parseExpression = function(forInit, refDestructuringErrors) {
	var startPos = this.start, startLoc = this.startLoc;
	var expr = this.parseMaybeAssign(forInit, refDestructuringErrors);
	if (this.type === types$1.comma) {
		var node = this.startNodeAt(startPos, startLoc);
		node.expressions = [expr];
		while (this.eat(types$1.comma)) node.expressions.push(this.parseMaybeAssign(forInit, refDestructuringErrors));
		return this.finishNode(node, "SequenceExpression");
	}
	return expr;
};
pp$5.parseMaybeAssign = function(forInit, refDestructuringErrors, afterLeftParse) {
	if (this.isContextual("yield")) if (this.inGenerator) return this.parseYield(forInit);
	else this.exprAllowed = false;
	var ownDestructuringErrors = false, oldParenAssign = -1, oldTrailingComma = -1, oldDoubleProto = -1;
	if (refDestructuringErrors) {
		oldParenAssign = refDestructuringErrors.parenthesizedAssign;
		oldTrailingComma = refDestructuringErrors.trailingComma;
		oldDoubleProto = refDestructuringErrors.doubleProto;
		refDestructuringErrors.parenthesizedAssign = refDestructuringErrors.trailingComma = -1;
	} else {
		refDestructuringErrors = new DestructuringErrors();
		ownDestructuringErrors = true;
	}
	var startPos = this.start, startLoc = this.startLoc;
	if (this.type === types$1.parenL || this.type === types$1.name) {
		this.potentialArrowAt = this.start;
		this.potentialArrowInForAwait = forInit === "await";
	}
	var left = this.parseMaybeConditional(forInit, refDestructuringErrors);
	if (afterLeftParse) left = afterLeftParse.call(this, left, startPos, startLoc);
	if (this.type.isAssign) {
		var node = this.startNodeAt(startPos, startLoc);
		node.operator = this.value;
		if (this.type === types$1.eq) left = this.toAssignable(left, false, refDestructuringErrors);
		if (!ownDestructuringErrors) refDestructuringErrors.parenthesizedAssign = refDestructuringErrors.trailingComma = refDestructuringErrors.doubleProto = -1;
		if (refDestructuringErrors.shorthandAssign >= left.start) refDestructuringErrors.shorthandAssign = -1;
		if (this.type === types$1.eq) this.checkLValPattern(left);
		else this.checkLValSimple(left);
		node.left = left;
		this.next();
		node.right = this.parseMaybeAssign(forInit);
		if (oldDoubleProto > -1) refDestructuringErrors.doubleProto = oldDoubleProto;
		return this.finishNode(node, "AssignmentExpression");
	} else if (ownDestructuringErrors) this.checkExpressionErrors(refDestructuringErrors, true);
	if (oldParenAssign > -1) refDestructuringErrors.parenthesizedAssign = oldParenAssign;
	if (oldTrailingComma > -1) refDestructuringErrors.trailingComma = oldTrailingComma;
	return left;
};
pp$5.parseMaybeConditional = function(forInit, refDestructuringErrors) {
	var startPos = this.start, startLoc = this.startLoc;
	var expr = this.parseExprOps(forInit, refDestructuringErrors);
	if (this.checkExpressionErrors(refDestructuringErrors)) return expr;
	if (this.eat(types$1.question)) {
		var node = this.startNodeAt(startPos, startLoc);
		node.test = expr;
		node.consequent = this.parseMaybeAssign();
		this.expect(types$1.colon);
		node.alternate = this.parseMaybeAssign(forInit);
		return this.finishNode(node, "ConditionalExpression");
	}
	return expr;
};
pp$5.parseExprOps = function(forInit, refDestructuringErrors) {
	var startPos = this.start, startLoc = this.startLoc;
	var expr = this.parseMaybeUnary(refDestructuringErrors, false, false, forInit);
	if (this.checkExpressionErrors(refDestructuringErrors)) return expr;
	return expr.start === startPos && expr.type === "ArrowFunctionExpression" ? expr : this.parseExprOp(expr, startPos, startLoc, -1, forInit);
};
pp$5.parseExprOp = function(left, leftStartPos, leftStartLoc, minPrec, forInit) {
	var prec = this.type.binop;
	if (prec != null && (!forInit || this.type !== types$1._in)) {
		if (prec > minPrec) {
			var logical = this.type === types$1.logicalOR || this.type === types$1.logicalAND;
			var coalesce = this.type === types$1.coalesce;
			if (coalesce) prec = types$1.logicalAND.binop;
			var op = this.value;
			this.next();
			var startPos = this.start, startLoc = this.startLoc;
			var right = this.parseExprOp(this.parseMaybeUnary(null, false, false, forInit), startPos, startLoc, prec, forInit);
			var node = this.buildBinary(leftStartPos, leftStartLoc, left, right, op, logical || coalesce);
			if (logical && this.type === types$1.coalesce || coalesce && (this.type === types$1.logicalOR || this.type === types$1.logicalAND)) this.raiseRecoverable(this.start, "Logical expressions and coalesce expressions cannot be mixed. Wrap either by parentheses");
			return this.parseExprOp(node, leftStartPos, leftStartLoc, minPrec, forInit);
		}
	}
	return left;
};
pp$5.buildBinary = function(startPos, startLoc, left, right, op, logical) {
	if (right.type === "PrivateIdentifier") this.raise(right.start, "Private identifier can only be left side of binary expression");
	var node = this.startNodeAt(startPos, startLoc);
	node.left = left;
	node.operator = op;
	node.right = right;
	return this.finishNode(node, logical ? "LogicalExpression" : "BinaryExpression");
};
pp$5.parseMaybeUnary = function(refDestructuringErrors, sawUnary, incDec, forInit) {
	var startPos = this.start, startLoc = this.startLoc, expr;
	if (this.isContextual("await") && this.canAwait) {
		expr = this.parseAwait(forInit);
		sawUnary = true;
	} else if (this.type.prefix) {
		var node = this.startNode(), update = this.type === types$1.incDec;
		node.operator = this.value;
		node.prefix = true;
		this.next();
		node.argument = this.parseMaybeUnary(null, true, update, forInit);
		this.checkExpressionErrors(refDestructuringErrors, true);
		if (update) this.checkLValSimple(node.argument);
		else if (this.strict && node.operator === "delete" && isLocalVariableAccess(node.argument)) this.raiseRecoverable(node.start, "Deleting local variable in strict mode");
		else if (node.operator === "delete" && isPrivateFieldAccess(node.argument)) this.raiseRecoverable(node.start, "Private fields can not be deleted");
		else sawUnary = true;
		expr = this.finishNode(node, update ? "UpdateExpression" : "UnaryExpression");
	} else if (!sawUnary && this.type === types$1.privateId) {
		if ((forInit || this.privateNameStack.length === 0) && this.options.checkPrivateFields) this.unexpected();
		expr = this.parsePrivateIdent();
		if (this.type !== types$1._in) this.unexpected();
	} else {
		expr = this.parseExprSubscripts(refDestructuringErrors, forInit);
		if (this.checkExpressionErrors(refDestructuringErrors)) return expr;
		while (this.type.postfix && !this.canInsertSemicolon()) {
			var node$1 = this.startNodeAt(startPos, startLoc);
			node$1.operator = this.value;
			node$1.prefix = false;
			node$1.argument = expr;
			this.checkLValSimple(expr);
			this.next();
			expr = this.finishNode(node$1, "UpdateExpression");
		}
	}
	if (!incDec && this.eat(types$1.starstar)) if (sawUnary) this.unexpected(this.lastTokStart);
	else return this.buildBinary(startPos, startLoc, expr, this.parseMaybeUnary(null, false, false, forInit), "**", false);
	else return expr;
};
function isLocalVariableAccess(node) {
	return node.type === "Identifier" || node.type === "ParenthesizedExpression" && isLocalVariableAccess(node.expression);
}
function isPrivateFieldAccess(node) {
	return node.type === "MemberExpression" && node.property.type === "PrivateIdentifier" || node.type === "ChainExpression" && isPrivateFieldAccess(node.expression) || node.type === "ParenthesizedExpression" && isPrivateFieldAccess(node.expression);
}
pp$5.parseExprSubscripts = function(refDestructuringErrors, forInit) {
	var startPos = this.start, startLoc = this.startLoc;
	var expr = this.parseExprAtom(refDestructuringErrors, forInit);
	if (expr.type === "ArrowFunctionExpression" && this.input.slice(this.lastTokStart, this.lastTokEnd) !== ")") return expr;
	var result = this.parseSubscripts(expr, startPos, startLoc, false, forInit);
	if (refDestructuringErrors && result.type === "MemberExpression") {
		if (refDestructuringErrors.parenthesizedAssign >= result.start) refDestructuringErrors.parenthesizedAssign = -1;
		if (refDestructuringErrors.parenthesizedBind >= result.start) refDestructuringErrors.parenthesizedBind = -1;
		if (refDestructuringErrors.trailingComma >= result.start) refDestructuringErrors.trailingComma = -1;
	}
	return result;
};
pp$5.parseSubscripts = function(base, startPos, startLoc, noCalls, forInit) {
	var maybeAsyncArrow = this.options.ecmaVersion >= 8 && base.type === "Identifier" && base.name === "async" && this.lastTokEnd === base.end && !this.canInsertSemicolon() && base.end - base.start === 5 && this.potentialArrowAt === base.start;
	var optionalChained = false;
	while (true) {
		var element = this.parseSubscript(base, startPos, startLoc, noCalls, maybeAsyncArrow, optionalChained, forInit);
		if (element.optional) optionalChained = true;
		if (element === base || element.type === "ArrowFunctionExpression") {
			if (optionalChained) {
				var chainNode = this.startNodeAt(startPos, startLoc);
				chainNode.expression = element;
				element = this.finishNode(chainNode, "ChainExpression");
			}
			return element;
		}
		base = element;
	}
};
pp$5.shouldParseAsyncArrow = function() {
	return !this.canInsertSemicolon() && this.eat(types$1.arrow);
};
pp$5.parseSubscriptAsyncArrow = function(startPos, startLoc, exprList, forInit) {
	return this.parseArrowExpression(this.startNodeAt(startPos, startLoc), exprList, true, forInit);
};
pp$5.parseSubscript = function(base, startPos, startLoc, noCalls, maybeAsyncArrow, optionalChained, forInit) {
	var optionalSupported = this.options.ecmaVersion >= 11;
	var optional = optionalSupported && this.eat(types$1.questionDot);
	if (noCalls && optional) this.raise(this.lastTokStart, "Optional chaining cannot appear in the callee of new expressions");
	var computed = this.eat(types$1.bracketL);
	if (computed || optional && this.type !== types$1.parenL && this.type !== types$1.backQuote || this.eat(types$1.dot)) {
		var node = this.startNodeAt(startPos, startLoc);
		node.object = base;
		if (computed) {
			node.property = this.parseExpression();
			this.expect(types$1.bracketR);
		} else if (this.type === types$1.privateId && base.type !== "Super") node.property = this.parsePrivateIdent();
		else node.property = this.parseIdent(this.options.allowReserved !== "never");
		node.computed = !!computed;
		if (optionalSupported) node.optional = optional;
		base = this.finishNode(node, "MemberExpression");
	} else if (!noCalls && this.eat(types$1.parenL)) {
		var refDestructuringErrors = new DestructuringErrors(), oldYieldPos = this.yieldPos, oldAwaitPos = this.awaitPos, oldAwaitIdentPos = this.awaitIdentPos;
		this.yieldPos = 0;
		this.awaitPos = 0;
		this.awaitIdentPos = 0;
		var exprList = this.parseExprList(types$1.parenR, this.options.ecmaVersion >= 8, false, refDestructuringErrors);
		if (maybeAsyncArrow && !optional && this.shouldParseAsyncArrow()) {
			this.checkPatternErrors(refDestructuringErrors, false);
			this.checkYieldAwaitInDefaultParams();
			if (this.awaitIdentPos > 0) this.raise(this.awaitIdentPos, "Cannot use 'await' as identifier inside an async function");
			this.yieldPos = oldYieldPos;
			this.awaitPos = oldAwaitPos;
			this.awaitIdentPos = oldAwaitIdentPos;
			return this.parseSubscriptAsyncArrow(startPos, startLoc, exprList, forInit);
		}
		this.checkExpressionErrors(refDestructuringErrors, true);
		this.yieldPos = oldYieldPos || this.yieldPos;
		this.awaitPos = oldAwaitPos || this.awaitPos;
		this.awaitIdentPos = oldAwaitIdentPos || this.awaitIdentPos;
		var node$1 = this.startNodeAt(startPos, startLoc);
		node$1.callee = base;
		node$1.arguments = exprList;
		if (optionalSupported) node$1.optional = optional;
		base = this.finishNode(node$1, "CallExpression");
	} else if (this.type === types$1.backQuote) {
		if (optional || optionalChained) this.raise(this.start, "Optional chaining cannot appear in the tag of tagged template expressions");
		var node$2 = this.startNodeAt(startPos, startLoc);
		node$2.tag = base;
		node$2.quasi = this.parseTemplate({ isTagged: true });
		base = this.finishNode(node$2, "TaggedTemplateExpression");
	}
	return base;
};
pp$5.parseExprAtom = function(refDestructuringErrors, forInit, forNew) {
	if (this.type === types$1.slash) this.readRegexp();
	var node, canBeArrow = this.potentialArrowAt === this.start;
	switch (this.type) {
		case types$1._super:
			if (!this.allowSuper) this.raise(this.start, "'super' keyword outside a method");
			node = this.startNode();
			this.next();
			if (this.type === types$1.parenL && !this.allowDirectSuper) this.raise(node.start, "super() call outside constructor of a subclass");
			if (this.type !== types$1.dot && this.type !== types$1.bracketL && this.type !== types$1.parenL) this.unexpected();
			return this.finishNode(node, "Super");
		case types$1._this:
			node = this.startNode();
			this.next();
			return this.finishNode(node, "ThisExpression");
		case types$1.name:
			var startPos = this.start, startLoc = this.startLoc, containsEsc = this.containsEsc;
			var id = this.parseIdent(false);
			if (this.options.ecmaVersion >= 8 && !containsEsc && id.name === "async" && !this.canInsertSemicolon() && this.eat(types$1._function)) {
				this.overrideContext(types$2.f_expr);
				return this.parseFunction(this.startNodeAt(startPos, startLoc), 0, false, true, forInit);
			}
			if (canBeArrow && !this.canInsertSemicolon()) {
				if (this.eat(types$1.arrow)) return this.parseArrowExpression(this.startNodeAt(startPos, startLoc), [id], false, forInit);
				if (this.options.ecmaVersion >= 8 && id.name === "async" && this.type === types$1.name && !containsEsc && (!this.potentialArrowInForAwait || this.value !== "of" || this.containsEsc)) {
					id = this.parseIdent(false);
					if (this.canInsertSemicolon() || !this.eat(types$1.arrow)) this.unexpected();
					return this.parseArrowExpression(this.startNodeAt(startPos, startLoc), [id], true, forInit);
				}
			}
			return id;
		case types$1.regexp:
			var value = this.value;
			node = this.parseLiteral(value.value);
			node.regex = {
				pattern: value.pattern,
				flags: value.flags
			};
			return node;
		case types$1.num:
		case types$1.string: return this.parseLiteral(this.value);
		case types$1._null:
		case types$1._true:
		case types$1._false:
			node = this.startNode();
			node.value = this.type === types$1._null ? null : this.type === types$1._true;
			node.raw = this.type.keyword;
			this.next();
			return this.finishNode(node, "Literal");
		case types$1.parenL:
			var start = this.start, expr = this.parseParenAndDistinguishExpression(canBeArrow, forInit);
			if (refDestructuringErrors) {
				if (refDestructuringErrors.parenthesizedAssign < 0 && !this.isSimpleAssignTarget(expr)) refDestructuringErrors.parenthesizedAssign = start;
				if (refDestructuringErrors.parenthesizedBind < 0) refDestructuringErrors.parenthesizedBind = start;
			}
			return expr;
		case types$1.bracketL:
			node = this.startNode();
			this.next();
			node.elements = this.parseExprList(types$1.bracketR, true, true, refDestructuringErrors);
			return this.finishNode(node, "ArrayExpression");
		case types$1.braceL:
			this.overrideContext(types$2.b_expr);
			return this.parseObj(false, refDestructuringErrors);
		case types$1._function:
			node = this.startNode();
			this.next();
			return this.parseFunction(node, 0);
		case types$1._class: return this.parseClass(this.startNode(), false);
		case types$1._new: return this.parseNew();
		case types$1.backQuote: return this.parseTemplate();
		case types$1._import: if (this.options.ecmaVersion >= 11) return this.parseExprImport(forNew);
		else return this.unexpected();
		default: return this.parseExprAtomDefault();
	}
};
pp$5.parseExprAtomDefault = function() {
	this.unexpected();
};
pp$5.parseExprImport = function(forNew) {
	var node = this.startNode();
	if (this.containsEsc) this.raiseRecoverable(this.start, "Escape sequence in keyword import");
	this.next();
	if (this.type === types$1.parenL && !forNew) return this.parseDynamicImport(node);
	else if (this.type === types$1.dot) {
		var meta = this.startNodeAt(node.start, node.loc && node.loc.start);
		meta.name = "import";
		node.meta = this.finishNode(meta, "Identifier");
		return this.parseImportMeta(node);
	} else this.unexpected();
};
pp$5.parseDynamicImport = function(node) {
	this.next();
	node.source = this.parseMaybeAssign();
	if (this.options.ecmaVersion >= 16) if (!this.eat(types$1.parenR)) {
		this.expect(types$1.comma);
		if (!this.afterTrailingComma(types$1.parenR)) {
			node.options = this.parseMaybeAssign();
			if (!this.eat(types$1.parenR)) {
				this.expect(types$1.comma);
				if (!this.afterTrailingComma(types$1.parenR)) this.unexpected();
			}
		} else node.options = null;
	} else node.options = null;
	else if (!this.eat(types$1.parenR)) {
		var errorPos = this.start;
		if (this.eat(types$1.comma) && this.eat(types$1.parenR)) this.raiseRecoverable(errorPos, "Trailing comma is not allowed in import()");
		else this.unexpected(errorPos);
	}
	return this.finishNode(node, "ImportExpression");
};
pp$5.parseImportMeta = function(node) {
	this.next();
	var containsEsc = this.containsEsc;
	node.property = this.parseIdent(true);
	if (node.property.name !== "meta") this.raiseRecoverable(node.property.start, "The only valid meta property for import is 'import.meta'");
	if (containsEsc) this.raiseRecoverable(node.start, "'import.meta' must not contain escaped characters");
	if (this.options.sourceType !== "module" && !this.options.allowImportExportEverywhere) this.raiseRecoverable(node.start, "Cannot use 'import.meta' outside a module");
	return this.finishNode(node, "MetaProperty");
};
pp$5.parseLiteral = function(value) {
	var node = this.startNode();
	node.value = value;
	node.raw = this.input.slice(this.start, this.end);
	if (node.raw.charCodeAt(node.raw.length - 1) === 110) node.bigint = node.value != null ? node.value.toString() : node.raw.slice(0, -1).replace(/_/g, "");
	this.next();
	return this.finishNode(node, "Literal");
};
pp$5.parseParenExpression = function() {
	this.expect(types$1.parenL);
	var val = this.parseExpression();
	this.expect(types$1.parenR);
	return val;
};
pp$5.shouldParseArrow = function(exprList) {
	return !this.canInsertSemicolon();
};
pp$5.parseParenAndDistinguishExpression = function(canBeArrow, forInit) {
	var startPos = this.start, startLoc = this.startLoc, val, allowTrailingComma = this.options.ecmaVersion >= 8;
	if (this.options.ecmaVersion >= 6) {
		this.next();
		var innerStartPos = this.start, innerStartLoc = this.startLoc;
		var exprList = [], first = true, lastIsComma = false;
		var refDestructuringErrors = new DestructuringErrors(), oldYieldPos = this.yieldPos, oldAwaitPos = this.awaitPos, spreadStart;
		this.yieldPos = 0;
		this.awaitPos = 0;
		while (this.type !== types$1.parenR) {
			first ? first = false : this.expect(types$1.comma);
			if (allowTrailingComma && this.afterTrailingComma(types$1.parenR, true)) {
				lastIsComma = true;
				break;
			} else if (this.type === types$1.ellipsis) {
				spreadStart = this.start;
				exprList.push(this.parseParenItem(this.parseRestBinding()));
				if (this.type === types$1.comma) this.raiseRecoverable(this.start, "Comma is not permitted after the rest element");
				break;
			} else exprList.push(this.parseMaybeAssign(false, refDestructuringErrors, this.parseParenItem));
		}
		var innerEndPos = this.lastTokEnd, innerEndLoc = this.lastTokEndLoc;
		this.expect(types$1.parenR);
		if (canBeArrow && this.shouldParseArrow(exprList) && this.eat(types$1.arrow)) {
			this.checkPatternErrors(refDestructuringErrors, false);
			this.checkYieldAwaitInDefaultParams();
			this.yieldPos = oldYieldPos;
			this.awaitPos = oldAwaitPos;
			return this.parseParenArrowList(startPos, startLoc, exprList, forInit);
		}
		if (!exprList.length || lastIsComma) this.unexpected(this.lastTokStart);
		if (spreadStart) this.unexpected(spreadStart);
		this.checkExpressionErrors(refDestructuringErrors, true);
		this.yieldPos = oldYieldPos || this.yieldPos;
		this.awaitPos = oldAwaitPos || this.awaitPos;
		if (exprList.length > 1) {
			val = this.startNodeAt(innerStartPos, innerStartLoc);
			val.expressions = exprList;
			this.finishNodeAt(val, "SequenceExpression", innerEndPos, innerEndLoc);
		} else val = exprList[0];
	} else val = this.parseParenExpression();
	if (this.options.preserveParens) {
		var par = this.startNodeAt(startPos, startLoc);
		par.expression = val;
		return this.finishNode(par, "ParenthesizedExpression");
	} else return val;
};
pp$5.parseParenItem = function(item) {
	return item;
};
pp$5.parseParenArrowList = function(startPos, startLoc, exprList, forInit) {
	return this.parseArrowExpression(this.startNodeAt(startPos, startLoc), exprList, false, forInit);
};
var empty = [];
pp$5.parseNew = function() {
	if (this.containsEsc) this.raiseRecoverable(this.start, "Escape sequence in keyword new");
	var node = this.startNode();
	this.next();
	if (this.options.ecmaVersion >= 6 && this.type === types$1.dot) {
		var meta = this.startNodeAt(node.start, node.loc && node.loc.start);
		meta.name = "new";
		node.meta = this.finishNode(meta, "Identifier");
		this.next();
		var containsEsc = this.containsEsc;
		node.property = this.parseIdent(true);
		if (node.property.name !== "target") this.raiseRecoverable(node.property.start, "The only valid meta property for new is 'new.target'");
		if (containsEsc) this.raiseRecoverable(node.start, "'new.target' must not contain escaped characters");
		if (!this.allowNewDotTarget) this.raiseRecoverable(node.start, "'new.target' can only be used in functions and class static block");
		return this.finishNode(node, "MetaProperty");
	}
	var startPos = this.start, startLoc = this.startLoc;
	node.callee = this.parseSubscripts(this.parseExprAtom(null, false, true), startPos, startLoc, true, false);
	if (this.eat(types$1.parenL)) node.arguments = this.parseExprList(types$1.parenR, this.options.ecmaVersion >= 8, false);
	else node.arguments = empty;
	return this.finishNode(node, "NewExpression");
};
pp$5.parseTemplateElement = function(ref) {
	var isTagged = ref.isTagged;
	var elem = this.startNode();
	if (this.type === types$1.invalidTemplate) {
		if (!isTagged) this.raiseRecoverable(this.start, "Bad escape sequence in untagged template literal");
		elem.value = {
			raw: this.value.replace(/\r\n?/g, "\n"),
			cooked: null
		};
	} else elem.value = {
		raw: this.input.slice(this.start, this.end).replace(/\r\n?/g, "\n"),
		cooked: this.value
	};
	this.next();
	elem.tail = this.type === types$1.backQuote;
	return this.finishNode(elem, "TemplateElement");
};
pp$5.parseTemplate = function(ref) {
	if (ref === void 0) ref = {};
	var isTagged = ref.isTagged;
	if (isTagged === void 0) isTagged = false;
	var node = this.startNode();
	this.next();
	node.expressions = [];
	var curElt = this.parseTemplateElement({ isTagged });
	node.quasis = [curElt];
	while (!curElt.tail) {
		if (this.type === types$1.eof) this.raise(this.pos, "Unterminated template literal");
		this.expect(types$1.dollarBraceL);
		node.expressions.push(this.parseExpression());
		this.expect(types$1.braceR);
		node.quasis.push(curElt = this.parseTemplateElement({ isTagged }));
	}
	this.next();
	return this.finishNode(node, "TemplateLiteral");
};
pp$5.isAsyncProp = function(prop) {
	return !prop.computed && prop.key.type === "Identifier" && prop.key.name === "async" && (this.type === types$1.name || this.type === types$1.num || this.type === types$1.string || this.type === types$1.bracketL || this.type.keyword || this.options.ecmaVersion >= 9 && this.type === types$1.star) && !lineBreak.test(this.input.slice(this.lastTokEnd, this.start));
};
pp$5.parseObj = function(isPattern, refDestructuringErrors) {
	var node = this.startNode(), first = true, propHash = {};
	node.properties = [];
	this.next();
	while (!this.eat(types$1.braceR)) {
		if (!first) {
			this.expect(types$1.comma);
			if (this.options.ecmaVersion >= 5 && this.afterTrailingComma(types$1.braceR)) break;
		} else first = false;
		var prop = this.parseProperty(isPattern, refDestructuringErrors);
		if (!isPattern) this.checkPropClash(prop, propHash, refDestructuringErrors);
		node.properties.push(prop);
	}
	return this.finishNode(node, isPattern ? "ObjectPattern" : "ObjectExpression");
};
pp$5.parseProperty = function(isPattern, refDestructuringErrors) {
	var prop = this.startNode(), isGenerator, isAsync, startPos, startLoc;
	if (this.options.ecmaVersion >= 9 && this.eat(types$1.ellipsis)) {
		if (isPattern) {
			prop.argument = this.parseIdent(false);
			if (this.type === types$1.comma) this.raiseRecoverable(this.start, "Comma is not permitted after the rest element");
			return this.finishNode(prop, "RestElement");
		}
		prop.argument = this.parseMaybeAssign(false, refDestructuringErrors);
		if (this.type === types$1.comma && refDestructuringErrors && refDestructuringErrors.trailingComma < 0) refDestructuringErrors.trailingComma = this.start;
		return this.finishNode(prop, "SpreadElement");
	}
	if (this.options.ecmaVersion >= 6) {
		prop.method = false;
		prop.shorthand = false;
		if (isPattern || refDestructuringErrors) {
			startPos = this.start;
			startLoc = this.startLoc;
		}
		if (!isPattern) isGenerator = this.eat(types$1.star);
	}
	var containsEsc = this.containsEsc;
	this.parsePropertyName(prop);
	if (!isPattern && !containsEsc && this.options.ecmaVersion >= 8 && !isGenerator && this.isAsyncProp(prop)) {
		isAsync = true;
		isGenerator = this.options.ecmaVersion >= 9 && this.eat(types$1.star);
		this.parsePropertyName(prop);
	} else isAsync = false;
	this.parsePropertyValue(prop, isPattern, isGenerator, isAsync, startPos, startLoc, refDestructuringErrors, containsEsc);
	return this.finishNode(prop, "Property");
};
pp$5.parseGetterSetter = function(prop) {
	var kind = prop.key.name;
	this.parsePropertyName(prop);
	prop.value = this.parseMethod(false);
	prop.kind = kind;
	var paramCount = prop.kind === "get" ? 0 : 1;
	if (prop.value.params.length !== paramCount) {
		var start = prop.value.start;
		if (prop.kind === "get") this.raiseRecoverable(start, "getter should have no params");
		else this.raiseRecoverable(start, "setter should have exactly one param");
	} else if (prop.kind === "set" && prop.value.params[0].type === "RestElement") this.raiseRecoverable(prop.value.params[0].start, "Setter cannot use rest params");
};
pp$5.parsePropertyValue = function(prop, isPattern, isGenerator, isAsync, startPos, startLoc, refDestructuringErrors, containsEsc) {
	if ((isGenerator || isAsync) && this.type === types$1.colon) this.unexpected();
	if (this.eat(types$1.colon)) {
		prop.value = isPattern ? this.parseMaybeDefault(this.start, this.startLoc) : this.parseMaybeAssign(false, refDestructuringErrors);
		prop.kind = "init";
	} else if (this.options.ecmaVersion >= 6 && this.type === types$1.parenL) {
		if (isPattern) this.unexpected();
		prop.method = true;
		prop.value = this.parseMethod(isGenerator, isAsync);
		prop.kind = "init";
	} else if (!isPattern && !containsEsc && this.options.ecmaVersion >= 5 && !prop.computed && prop.key.type === "Identifier" && (prop.key.name === "get" || prop.key.name === "set") && this.type !== types$1.comma && this.type !== types$1.braceR && this.type !== types$1.eq) {
		if (isGenerator || isAsync) this.unexpected();
		this.parseGetterSetter(prop);
	} else if (this.options.ecmaVersion >= 6 && !prop.computed && prop.key.type === "Identifier") {
		if (isGenerator || isAsync) this.unexpected();
		this.checkUnreserved(prop.key);
		if (prop.key.name === "await" && !this.awaitIdentPos) this.awaitIdentPos = startPos;
		if (isPattern) prop.value = this.parseMaybeDefault(startPos, startLoc, this.copyNode(prop.key));
		else if (this.type === types$1.eq && refDestructuringErrors) {
			if (refDestructuringErrors.shorthandAssign < 0) refDestructuringErrors.shorthandAssign = this.start;
			prop.value = this.parseMaybeDefault(startPos, startLoc, this.copyNode(prop.key));
		} else prop.value = this.copyNode(prop.key);
		prop.kind = "init";
		prop.shorthand = true;
	} else this.unexpected();
};
pp$5.parsePropertyName = function(prop) {
	if (this.options.ecmaVersion >= 6) if (this.eat(types$1.bracketL)) {
		prop.computed = true;
		prop.key = this.parseMaybeAssign();
		this.expect(types$1.bracketR);
		return prop.key;
	} else prop.computed = false;
	return prop.key = this.type === types$1.num || this.type === types$1.string ? this.parseExprAtom() : this.parseIdent(this.options.allowReserved !== "never");
};
pp$5.initFunction = function(node) {
	node.id = null;
	if (this.options.ecmaVersion >= 6) node.generator = node.expression = false;
	if (this.options.ecmaVersion >= 8) node.async = false;
};
pp$5.parseMethod = function(isGenerator, isAsync, allowDirectSuper) {
	var node = this.startNode(), oldYieldPos = this.yieldPos, oldAwaitPos = this.awaitPos, oldAwaitIdentPos = this.awaitIdentPos;
	this.initFunction(node);
	if (this.options.ecmaVersion >= 6) node.generator = isGenerator;
	if (this.options.ecmaVersion >= 8) node.async = !!isAsync;
	this.yieldPos = 0;
	this.awaitPos = 0;
	this.awaitIdentPos = 0;
	this.enterScope(functionFlags(isAsync, node.generator) | SCOPE_SUPER | (allowDirectSuper ? SCOPE_DIRECT_SUPER : 0));
	this.expect(types$1.parenL);
	node.params = this.parseBindingList(types$1.parenR, false, this.options.ecmaVersion >= 8);
	this.checkYieldAwaitInDefaultParams();
	this.parseFunctionBody(node, false, true, false);
	this.yieldPos = oldYieldPos;
	this.awaitPos = oldAwaitPos;
	this.awaitIdentPos = oldAwaitIdentPos;
	return this.finishNode(node, "FunctionExpression");
};
pp$5.parseArrowExpression = function(node, params, isAsync, forInit) {
	var oldYieldPos = this.yieldPos, oldAwaitPos = this.awaitPos, oldAwaitIdentPos = this.awaitIdentPos;
	this.enterScope(functionFlags(isAsync, false) | SCOPE_ARROW);
	this.initFunction(node);
	if (this.options.ecmaVersion >= 8) node.async = !!isAsync;
	this.yieldPos = 0;
	this.awaitPos = 0;
	this.awaitIdentPos = 0;
	node.params = this.toAssignableList(params, true);
	this.parseFunctionBody(node, true, false, forInit);
	this.yieldPos = oldYieldPos;
	this.awaitPos = oldAwaitPos;
	this.awaitIdentPos = oldAwaitIdentPos;
	return this.finishNode(node, "ArrowFunctionExpression");
};
pp$5.parseFunctionBody = function(node, isArrowFunction, isMethod, forInit) {
	var isExpression = isArrowFunction && this.type !== types$1.braceL;
	var oldStrict = this.strict, useStrict = false;
	if (isExpression) {
		node.body = this.parseMaybeAssign(forInit);
		node.expression = true;
		this.checkParams(node, false);
	} else {
		var nonSimple = this.options.ecmaVersion >= 7 && !this.isSimpleParamList(node.params);
		if (!oldStrict || nonSimple) {
			useStrict = this.strictDirective(this.end);
			if (useStrict && nonSimple) this.raiseRecoverable(node.start, "Illegal 'use strict' directive in function with non-simple parameter list");
		}
		var oldLabels = this.labels;
		this.labels = [];
		if (useStrict) this.strict = true;
		this.checkParams(node, !oldStrict && !useStrict && !isArrowFunction && !isMethod && this.isSimpleParamList(node.params));
		if (this.strict && node.id) this.checkLValSimple(node.id, BIND_OUTSIDE);
		node.body = this.parseBlock(false, void 0, useStrict && !oldStrict);
		node.expression = false;
		this.adaptDirectivePrologue(node.body.body);
		this.labels = oldLabels;
	}
	this.exitScope();
};
pp$5.isSimpleParamList = function(params) {
	for (var i = 0, list = params; i < list.length; i += 1) if (list[i].type !== "Identifier") return false;
	return true;
};
pp$5.checkParams = function(node, allowDuplicates) {
	var nameHash = Object.create(null);
	for (var i = 0, list = node.params; i < list.length; i += 1) {
		var param = list[i];
		this.checkLValInnerPattern(param, BIND_VAR, allowDuplicates ? null : nameHash);
	}
};
pp$5.parseExprList = function(close, allowTrailingComma, allowEmpty, refDestructuringErrors) {
	var elts = [], first = true;
	while (!this.eat(close)) {
		if (!first) {
			this.expect(types$1.comma);
			if (allowTrailingComma && this.afterTrailingComma(close)) break;
		} else first = false;
		var elt = void 0;
		if (allowEmpty && this.type === types$1.comma) elt = null;
		else if (this.type === types$1.ellipsis) {
			elt = this.parseSpread(refDestructuringErrors);
			if (refDestructuringErrors && this.type === types$1.comma && refDestructuringErrors.trailingComma < 0) refDestructuringErrors.trailingComma = this.start;
		} else elt = this.parseMaybeAssign(false, refDestructuringErrors);
		elts.push(elt);
	}
	return elts;
};
pp$5.checkUnreserved = function(ref) {
	var start = ref.start;
	var end = ref.end;
	var name = ref.name;
	if (this.inGenerator && name === "yield") this.raiseRecoverable(start, "Cannot use 'yield' as identifier inside a generator");
	if (this.inAsync && name === "await") this.raiseRecoverable(start, "Cannot use 'await' as identifier inside an async function");
	if (!(this.currentThisScope().flags & SCOPE_VAR) && name === "arguments") this.raiseRecoverable(start, "Cannot use 'arguments' in class field initializer");
	if (this.inClassStaticBlock && (name === "arguments" || name === "await")) this.raise(start, "Cannot use " + name + " in class static initialization block");
	if (this.keywords.test(name)) this.raise(start, "Unexpected keyword '" + name + "'");
	if (this.options.ecmaVersion < 6 && this.input.slice(start, end).indexOf("\\") !== -1) return;
	if ((this.strict ? this.reservedWordsStrict : this.reservedWords).test(name)) {
		if (!this.inAsync && name === "await") this.raiseRecoverable(start, "Cannot use keyword 'await' outside an async function");
		this.raiseRecoverable(start, "The keyword '" + name + "' is reserved");
	}
};
pp$5.parseIdent = function(liberal) {
	var node = this.parseIdentNode();
	this.next(!!liberal);
	this.finishNode(node, "Identifier");
	if (!liberal) {
		this.checkUnreserved(node);
		if (node.name === "await" && !this.awaitIdentPos) this.awaitIdentPos = node.start;
	}
	return node;
};
pp$5.parseIdentNode = function() {
	var node = this.startNode();
	if (this.type === types$1.name) node.name = this.value;
	else if (this.type.keyword) {
		node.name = this.type.keyword;
		if ((node.name === "class" || node.name === "function") && (this.lastTokEnd !== this.lastTokStart + 1 || this.input.charCodeAt(this.lastTokStart) !== 46)) this.context.pop();
		this.type = types$1.name;
	} else this.unexpected();
	return node;
};
pp$5.parsePrivateIdent = function() {
	var node = this.startNode();
	if (this.type === types$1.privateId) node.name = this.value;
	else this.unexpected();
	this.next();
	this.finishNode(node, "PrivateIdentifier");
	if (this.options.checkPrivateFields) if (this.privateNameStack.length === 0) this.raise(node.start, "Private field '#" + node.name + "' must be declared in an enclosing class");
	else this.privateNameStack[this.privateNameStack.length - 1].used.push(node);
	return node;
};
pp$5.parseYield = function(forInit) {
	if (!this.yieldPos) this.yieldPos = this.start;
	var node = this.startNode();
	this.next();
	if (this.type === types$1.semi || this.canInsertSemicolon() || this.type !== types$1.star && !this.type.startsExpr) {
		node.delegate = false;
		node.argument = null;
	} else {
		node.delegate = this.eat(types$1.star);
		node.argument = this.parseMaybeAssign(forInit);
	}
	return this.finishNode(node, "YieldExpression");
};
pp$5.parseAwait = function(forInit) {
	if (!this.awaitPos) this.awaitPos = this.start;
	var node = this.startNode();
	this.next();
	node.argument = this.parseMaybeUnary(null, true, false, forInit);
	return this.finishNode(node, "AwaitExpression");
};
var pp$4 = Parser.prototype;
pp$4.raise = function(pos, message) {
	var loc = getLineInfo(this.input, pos);
	message += " (" + loc.line + ":" + loc.column + ")";
	if (this.sourceFile) message += " in " + this.sourceFile;
	var err = new SyntaxError(message);
	err.pos = pos;
	err.loc = loc;
	err.raisedAt = this.pos;
	throw err;
};
pp$4.raiseRecoverable = pp$4.raise;
pp$4.curPosition = function() {
	if (this.options.locations) return new Position(this.curLine, this.pos - this.lineStart);
};
var pp$3 = Parser.prototype;
var Scope = function Scope(flags) {
	this.flags = flags;
	this.var = [];
	this.lexical = [];
	this.functions = [];
};
pp$3.enterScope = function(flags) {
	this.scopeStack.push(new Scope(flags));
};
pp$3.exitScope = function() {
	this.scopeStack.pop();
};
pp$3.treatFunctionsAsVarInScope = function(scope) {
	return scope.flags & SCOPE_FUNCTION || !this.inModule && scope.flags & SCOPE_TOP;
};
pp$3.declareName = function(name, bindingType, pos) {
	var redeclared = false;
	if (bindingType === BIND_LEXICAL) {
		var scope = this.currentScope();
		redeclared = scope.lexical.indexOf(name) > -1 || scope.functions.indexOf(name) > -1 || scope.var.indexOf(name) > -1;
		scope.lexical.push(name);
		if (this.inModule && scope.flags & SCOPE_TOP) delete this.undefinedExports[name];
	} else if (bindingType === BIND_SIMPLE_CATCH) this.currentScope().lexical.push(name);
	else if (bindingType === BIND_FUNCTION) {
		var scope$2 = this.currentScope();
		if (this.treatFunctionsAsVar) redeclared = scope$2.lexical.indexOf(name) > -1;
		else redeclared = scope$2.lexical.indexOf(name) > -1 || scope$2.var.indexOf(name) > -1;
		scope$2.functions.push(name);
	} else for (var i = this.scopeStack.length - 1; i >= 0; --i) {
		var scope$3 = this.scopeStack[i];
		if (scope$3.lexical.indexOf(name) > -1 && !(scope$3.flags & SCOPE_SIMPLE_CATCH && scope$3.lexical[0] === name) || !this.treatFunctionsAsVarInScope(scope$3) && scope$3.functions.indexOf(name) > -1) {
			redeclared = true;
			break;
		}
		scope$3.var.push(name);
		if (this.inModule && scope$3.flags & SCOPE_TOP) delete this.undefinedExports[name];
		if (scope$3.flags & SCOPE_VAR) break;
	}
	if (redeclared) this.raiseRecoverable(pos, "Identifier '" + name + "' has already been declared");
};
pp$3.checkLocalExport = function(id) {
	if (this.scopeStack[0].lexical.indexOf(id.name) === -1 && this.scopeStack[0].var.indexOf(id.name) === -1) this.undefinedExports[id.name] = id;
};
pp$3.currentScope = function() {
	return this.scopeStack[this.scopeStack.length - 1];
};
pp$3.currentVarScope = function() {
	for (var i = this.scopeStack.length - 1;; i--) {
		var scope = this.scopeStack[i];
		if (scope.flags & (SCOPE_VAR | SCOPE_CLASS_FIELD_INIT | SCOPE_CLASS_STATIC_BLOCK)) return scope;
	}
};
pp$3.currentThisScope = function() {
	for (var i = this.scopeStack.length - 1;; i--) {
		var scope = this.scopeStack[i];
		if (scope.flags & (SCOPE_VAR | SCOPE_CLASS_FIELD_INIT | SCOPE_CLASS_STATIC_BLOCK) && !(scope.flags & SCOPE_ARROW)) return scope;
	}
};
var Node = function Node(parser, pos, loc) {
	this.type = "";
	this.start = pos;
	this.end = 0;
	if (parser.options.locations) this.loc = new SourceLocation(parser, loc);
	if (parser.options.directSourceFile) this.sourceFile = parser.options.directSourceFile;
	if (parser.options.ranges) this.range = [pos, 0];
};
var pp$2 = Parser.prototype;
pp$2.startNode = function() {
	return new Node(this, this.start, this.startLoc);
};
pp$2.startNodeAt = function(pos, loc) {
	return new Node(this, pos, loc);
};
function finishNodeAt(node, type, pos, loc) {
	node.type = type;
	node.end = pos;
	if (this.options.locations) node.loc.end = loc;
	if (this.options.ranges) node.range[1] = pos;
	return node;
}
pp$2.finishNode = function(node, type) {
	return finishNodeAt.call(this, node, type, this.lastTokEnd, this.lastTokEndLoc);
};
pp$2.finishNodeAt = function(node, type, pos, loc) {
	return finishNodeAt.call(this, node, type, pos, loc);
};
pp$2.copyNode = function(node) {
	var newNode = new Node(this, node.start, this.startLoc);
	for (var prop in node) newNode[prop] = node[prop];
	return newNode;
};
var scriptValuesAddedInUnicode = "Berf Beria_Erfe Gara Garay Gukh Gurung_Khema Hrkt Katakana_Or_Hiragana Kawi Kirat_Rai Krai Nag_Mundari Nagm Ol_Onal Onao Sidetic Sidt Sunu Sunuwar Tai_Yo Tayo Todhri Todr Tolong_Siki Tols Tulu_Tigalari Tutg Unknown Zzzz";
var ecma9BinaryProperties = "ASCII ASCII_Hex_Digit AHex Alphabetic Alpha Any Assigned Bidi_Control Bidi_C Bidi_Mirrored Bidi_M Case_Ignorable CI Cased Changes_When_Casefolded CWCF Changes_When_Casemapped CWCM Changes_When_Lowercased CWL Changes_When_NFKC_Casefolded CWKCF Changes_When_Titlecased CWT Changes_When_Uppercased CWU Dash Default_Ignorable_Code_Point DI Deprecated Dep Diacritic Dia Emoji Emoji_Component Emoji_Modifier Emoji_Modifier_Base Emoji_Presentation Extender Ext Grapheme_Base Gr_Base Grapheme_Extend Gr_Ext Hex_Digit Hex IDS_Binary_Operator IDSB IDS_Trinary_Operator IDST ID_Continue IDC ID_Start IDS Ideographic Ideo Join_Control Join_C Logical_Order_Exception LOE Lowercase Lower Math Noncharacter_Code_Point NChar Pattern_Syntax Pat_Syn Pattern_White_Space Pat_WS Quotation_Mark QMark Radical Regional_Indicator RI Sentence_Terminal STerm Soft_Dotted SD Terminal_Punctuation Term Unified_Ideograph UIdeo Uppercase Upper Variation_Selector VS White_Space space XID_Continue XIDC XID_Start XIDS";
var ecma10BinaryProperties = ecma9BinaryProperties + " Extended_Pictographic";
var ecma11BinaryProperties = ecma10BinaryProperties;
var ecma12BinaryProperties = ecma11BinaryProperties + " EBase EComp EMod EPres ExtPict";
var ecma13BinaryProperties = ecma12BinaryProperties;
var ecma14BinaryProperties = ecma13BinaryProperties;
var unicodeBinaryProperties = {
	9: ecma9BinaryProperties,
	10: ecma10BinaryProperties,
	11: ecma11BinaryProperties,
	12: ecma12BinaryProperties,
	13: ecma13BinaryProperties,
	14: ecma14BinaryProperties
};
var ecma14BinaryPropertiesOfStrings = "Basic_Emoji Emoji_Keycap_Sequence RGI_Emoji_Modifier_Sequence RGI_Emoji_Flag_Sequence RGI_Emoji_Tag_Sequence RGI_Emoji_ZWJ_Sequence RGI_Emoji";
var unicodeBinaryPropertiesOfStrings = {
	9: "",
	10: "",
	11: "",
	12: "",
	13: "",
	14: ecma14BinaryPropertiesOfStrings
};
var unicodeGeneralCategoryValues = "Cased_Letter LC Close_Punctuation Pe Connector_Punctuation Pc Control Cc cntrl Currency_Symbol Sc Dash_Punctuation Pd Decimal_Number Nd digit Enclosing_Mark Me Final_Punctuation Pf Format Cf Initial_Punctuation Pi Letter L Letter_Number Nl Line_Separator Zl Lowercase_Letter Ll Mark M Combining_Mark Math_Symbol Sm Modifier_Letter Lm Modifier_Symbol Sk Nonspacing_Mark Mn Number N Open_Punctuation Ps Other C Other_Letter Lo Other_Number No Other_Punctuation Po Other_Symbol So Paragraph_Separator Zp Private_Use Co Punctuation P punct Separator Z Space_Separator Zs Spacing_Mark Mc Surrogate Cs Symbol S Titlecase_Letter Lt Unassigned Cn Uppercase_Letter Lu";
var ecma9ScriptValues = "Adlam Adlm Ahom Anatolian_Hieroglyphs Hluw Arabic Arab Armenian Armn Avestan Avst Balinese Bali Bamum Bamu Bassa_Vah Bass Batak Batk Bengali Beng Bhaiksuki Bhks Bopomofo Bopo Brahmi Brah Braille Brai Buginese Bugi Buhid Buhd Canadian_Aboriginal Cans Carian Cari Caucasian_Albanian Aghb Chakma Cakm Cham Cham Cherokee Cher Common Zyyy Coptic Copt Qaac Cuneiform Xsux Cypriot Cprt Cyrillic Cyrl Deseret Dsrt Devanagari Deva Duployan Dupl Egyptian_Hieroglyphs Egyp Elbasan Elba Ethiopic Ethi Georgian Geor Glagolitic Glag Gothic Goth Grantha Gran Greek Grek Gujarati Gujr Gurmukhi Guru Han Hani Hangul Hang Hanunoo Hano Hatran Hatr Hebrew Hebr Hiragana Hira Imperial_Aramaic Armi Inherited Zinh Qaai Inscriptional_Pahlavi Phli Inscriptional_Parthian Prti Javanese Java Kaithi Kthi Kannada Knda Katakana Kana Kayah_Li Kali Kharoshthi Khar Khmer Khmr Khojki Khoj Khudawadi Sind Lao Laoo Latin Latn Lepcha Lepc Limbu Limb Linear_A Lina Linear_B Linb Lisu Lisu Lycian Lyci Lydian Lydi Mahajani Mahj Malayalam Mlym Mandaic Mand Manichaean Mani Marchen Marc Masaram_Gondi Gonm Meetei_Mayek Mtei Mende_Kikakui Mend Meroitic_Cursive Merc Meroitic_Hieroglyphs Mero Miao Plrd Modi Mongolian Mong Mro Mroo Multani Mult Myanmar Mymr Nabataean Nbat New_Tai_Lue Talu Newa Newa Nko Nkoo Nushu Nshu Ogham Ogam Ol_Chiki Olck Old_Hungarian Hung Old_Italic Ital Old_North_Arabian Narb Old_Permic Perm Old_Persian Xpeo Old_South_Arabian Sarb Old_Turkic Orkh Oriya Orya Osage Osge Osmanya Osma Pahawh_Hmong Hmng Palmyrene Palm Pau_Cin_Hau Pauc Phags_Pa Phag Phoenician Phnx Psalter_Pahlavi Phlp Rejang Rjng Runic Runr Samaritan Samr Saurashtra Saur Sharada Shrd Shavian Shaw Siddham Sidd SignWriting Sgnw Sinhala Sinh Sora_Sompeng Sora Soyombo Soyo Sundanese Sund Syloti_Nagri Sylo Syriac Syrc Tagalog Tglg Tagbanwa Tagb Tai_Le Tale Tai_Tham Lana Tai_Viet Tavt Takri Takr Tamil Taml Tangut Tang Telugu Telu Thaana Thaa Thai Thai Tibetan Tibt Tifinagh Tfng Tirhuta Tirh Ugaritic Ugar Vai Vaii Warang_Citi Wara Yi Yiii Zanabazar_Square Zanb";
var ecma10ScriptValues = ecma9ScriptValues + " Dogra Dogr Gunjala_Gondi Gong Hanifi_Rohingya Rohg Makasar Maka Medefaidrin Medf Old_Sogdian Sogo Sogdian Sogd";
var ecma11ScriptValues = ecma10ScriptValues + " Elymaic Elym Nandinagari Nand Nyiakeng_Puachue_Hmong Hmnp Wancho Wcho";
var ecma12ScriptValues = ecma11ScriptValues + " Chorasmian Chrs Diak Dives_Akuru Khitan_Small_Script Kits Yezi Yezidi";
var ecma13ScriptValues = ecma12ScriptValues + " Cypro_Minoan Cpmn Old_Uyghur Ougr Tangsa Tnsa Toto Vithkuqi Vith";
var ecma14ScriptValues = ecma13ScriptValues + " " + scriptValuesAddedInUnicode;
var unicodeScriptValues = {
	9: ecma9ScriptValues,
	10: ecma10ScriptValues,
	11: ecma11ScriptValues,
	12: ecma12ScriptValues,
	13: ecma13ScriptValues,
	14: ecma14ScriptValues
};
var data = {};
function buildUnicodeData(ecmaVersion) {
	var d = data[ecmaVersion] = {
		binary: wordsRegexp(unicodeBinaryProperties[ecmaVersion] + " " + unicodeGeneralCategoryValues),
		binaryOfStrings: wordsRegexp(unicodeBinaryPropertiesOfStrings[ecmaVersion]),
		nonBinary: {
			General_Category: wordsRegexp(unicodeGeneralCategoryValues),
			Script: wordsRegexp(unicodeScriptValues[ecmaVersion])
		}
	};
	d.nonBinary.Script_Extensions = d.nonBinary.Script;
	d.nonBinary.gc = d.nonBinary.General_Category;
	d.nonBinary.sc = d.nonBinary.Script;
	d.nonBinary.scx = d.nonBinary.Script_Extensions;
}
for (var i = 0, list = [
	9,
	10,
	11,
	12,
	13,
	14
]; i < list.length; i += 1) {
	var ecmaVersion = list[i];
	buildUnicodeData(ecmaVersion);
}
var pp$1 = Parser.prototype;
var BranchID = function BranchID(parent, base) {
	this.parent = parent;
	this.base = base || this;
};
BranchID.prototype.separatedFrom = function separatedFrom(alt) {
	for (var self = this; self; self = self.parent) for (var other = alt; other; other = other.parent) if (self.base === other.base && self !== other) return true;
	return false;
};
BranchID.prototype.sibling = function sibling() {
	return new BranchID(this.parent, this.base);
};
var RegExpValidationState = function RegExpValidationState(parser) {
	this.parser = parser;
	this.validFlags = "gim" + (parser.options.ecmaVersion >= 6 ? "uy" : "") + (parser.options.ecmaVersion >= 9 ? "s" : "") + (parser.options.ecmaVersion >= 13 ? "d" : "") + (parser.options.ecmaVersion >= 15 ? "v" : "");
	this.unicodeProperties = data[parser.options.ecmaVersion >= 14 ? 14 : parser.options.ecmaVersion];
	this.source = "";
	this.flags = "";
	this.start = 0;
	this.switchU = false;
	this.switchV = false;
	this.switchN = false;
	this.pos = 0;
	this.lastIntValue = 0;
	this.lastStringValue = "";
	this.lastAssertionIsQuantifiable = false;
	this.numCapturingParens = 0;
	this.maxBackReference = 0;
	this.groupNames = Object.create(null);
	this.backReferenceNames = [];
	this.branchID = null;
};
RegExpValidationState.prototype.reset = function reset(start, pattern, flags) {
	var unicodeSets = flags.indexOf("v") !== -1;
	var unicode = flags.indexOf("u") !== -1;
	this.start = start | 0;
	this.source = pattern + "";
	this.flags = flags;
	if (unicodeSets && this.parser.options.ecmaVersion >= 15) {
		this.switchU = true;
		this.switchV = true;
		this.switchN = true;
	} else {
		this.switchU = unicode && this.parser.options.ecmaVersion >= 6;
		this.switchV = false;
		this.switchN = unicode && this.parser.options.ecmaVersion >= 9;
	}
};
RegExpValidationState.prototype.raise = function raise(message) {
	this.parser.raiseRecoverable(this.start, "Invalid regular expression: /" + this.source + "/: " + message);
};
RegExpValidationState.prototype.at = function at(i, forceU) {
	if (forceU === void 0) forceU = false;
	var s = this.source;
	var l = s.length;
	if (i >= l) return -1;
	var c = s.charCodeAt(i);
	if (!(forceU || this.switchU) || c <= 55295 || c >= 57344 || i + 1 >= l) return c;
	var next = s.charCodeAt(i + 1);
	return next >= 56320 && next <= 57343 ? (c << 10) + next - 56613888 : c;
};
RegExpValidationState.prototype.nextIndex = function nextIndex(i, forceU) {
	if (forceU === void 0) forceU = false;
	var s = this.source;
	var l = s.length;
	if (i >= l) return l;
	var c = s.charCodeAt(i), next;
	if (!(forceU || this.switchU) || c <= 55295 || c >= 57344 || i + 1 >= l || (next = s.charCodeAt(i + 1)) < 56320 || next > 57343) return i + 1;
	return i + 2;
};
RegExpValidationState.prototype.current = function current(forceU) {
	if (forceU === void 0) forceU = false;
	return this.at(this.pos, forceU);
};
RegExpValidationState.prototype.lookahead = function lookahead(forceU) {
	if (forceU === void 0) forceU = false;
	return this.at(this.nextIndex(this.pos, forceU), forceU);
};
RegExpValidationState.prototype.advance = function advance(forceU) {
	if (forceU === void 0) forceU = false;
	this.pos = this.nextIndex(this.pos, forceU);
};
RegExpValidationState.prototype.eat = function eat(ch, forceU) {
	if (forceU === void 0) forceU = false;
	if (this.current(forceU) === ch) {
		this.advance(forceU);
		return true;
	}
	return false;
};
RegExpValidationState.prototype.eatChars = function eatChars(chs, forceU) {
	if (forceU === void 0) forceU = false;
	var pos = this.pos;
	for (var i = 0, list = chs; i < list.length; i += 1) {
		var ch = list[i];
		var current = this.at(pos, forceU);
		if (current === -1 || current !== ch) return false;
		pos = this.nextIndex(pos, forceU);
	}
	this.pos = pos;
	return true;
};
/**
* Validate the flags part of a given RegExpLiteral.
*
* @param {RegExpValidationState} state The state to validate RegExp.
* @returns {void}
*/
pp$1.validateRegExpFlags = function(state) {
	var validFlags = state.validFlags;
	var flags = state.flags;
	var u = false;
	var v = false;
	for (var i = 0; i < flags.length; i++) {
		var flag = flags.charAt(i);
		if (validFlags.indexOf(flag) === -1) this.raise(state.start, "Invalid regular expression flag");
		if (flags.indexOf(flag, i + 1) > -1) this.raise(state.start, "Duplicate regular expression flag");
		if (flag === "u") u = true;
		if (flag === "v") v = true;
	}
	if (this.options.ecmaVersion >= 15 && u && v) this.raise(state.start, "Invalid regular expression flag");
};
function hasProp(obj) {
	for (var _ in obj) return true;
	return false;
}
/**
* Validate the pattern part of a given RegExpLiteral.
*
* @param {RegExpValidationState} state The state to validate RegExp.
* @returns {void}
*/
pp$1.validateRegExpPattern = function(state) {
	this.regexp_pattern(state);
	if (!state.switchN && this.options.ecmaVersion >= 9 && hasProp(state.groupNames)) {
		state.switchN = true;
		this.regexp_pattern(state);
	}
};
pp$1.regexp_pattern = function(state) {
	state.pos = 0;
	state.lastIntValue = 0;
	state.lastStringValue = "";
	state.lastAssertionIsQuantifiable = false;
	state.numCapturingParens = 0;
	state.maxBackReference = 0;
	state.groupNames = Object.create(null);
	state.backReferenceNames.length = 0;
	state.branchID = null;
	this.regexp_disjunction(state);
	if (state.pos !== state.source.length) {
		if (state.eat(41)) state.raise("Unmatched ')'");
		if (state.eat(93) || state.eat(125)) state.raise("Lone quantifier brackets");
	}
	if (state.maxBackReference > state.numCapturingParens) state.raise("Invalid escape");
	for (var i = 0, list = state.backReferenceNames; i < list.length; i += 1) {
		var name = list[i];
		if (!state.groupNames[name]) state.raise("Invalid named capture referenced");
	}
};
pp$1.regexp_disjunction = function(state) {
	var trackDisjunction = this.options.ecmaVersion >= 16;
	if (trackDisjunction) state.branchID = new BranchID(state.branchID, null);
	this.regexp_alternative(state);
	while (state.eat(124)) {
		if (trackDisjunction) state.branchID = state.branchID.sibling();
		this.regexp_alternative(state);
	}
	if (trackDisjunction) state.branchID = state.branchID.parent;
	if (this.regexp_eatQuantifier(state, true)) state.raise("Nothing to repeat");
	if (state.eat(123)) state.raise("Lone quantifier brackets");
};
pp$1.regexp_alternative = function(state) {
	while (state.pos < state.source.length && this.regexp_eatTerm(state));
};
pp$1.regexp_eatTerm = function(state) {
	if (this.regexp_eatAssertion(state)) {
		if (state.lastAssertionIsQuantifiable && this.regexp_eatQuantifier(state)) {
			if (state.switchU) state.raise("Invalid quantifier");
		}
		return true;
	}
	if (state.switchU ? this.regexp_eatAtom(state) : this.regexp_eatExtendedAtom(state)) {
		this.regexp_eatQuantifier(state);
		return true;
	}
	return false;
};
pp$1.regexp_eatAssertion = function(state) {
	var start = state.pos;
	state.lastAssertionIsQuantifiable = false;
	if (state.eat(94) || state.eat(36)) return true;
	if (state.eat(92)) {
		if (state.eat(66) || state.eat(98)) return true;
		state.pos = start;
	}
	if (state.eat(40) && state.eat(63)) {
		var lookbehind = false;
		if (this.options.ecmaVersion >= 9) lookbehind = state.eat(60);
		if (state.eat(61) || state.eat(33)) {
			this.regexp_disjunction(state);
			if (!state.eat(41)) state.raise("Unterminated group");
			state.lastAssertionIsQuantifiable = !lookbehind;
			return true;
		}
	}
	state.pos = start;
	return false;
};
pp$1.regexp_eatQuantifier = function(state, noError) {
	if (noError === void 0) noError = false;
	if (this.regexp_eatQuantifierPrefix(state, noError)) {
		state.eat(63);
		return true;
	}
	return false;
};
pp$1.regexp_eatQuantifierPrefix = function(state, noError) {
	return state.eat(42) || state.eat(43) || state.eat(63) || this.regexp_eatBracedQuantifier(state, noError);
};
pp$1.regexp_eatBracedQuantifier = function(state, noError) {
	var start = state.pos;
	if (state.eat(123)) {
		var min = 0, max = -1;
		if (this.regexp_eatDecimalDigits(state)) {
			min = state.lastIntValue;
			if (state.eat(44) && this.regexp_eatDecimalDigits(state)) max = state.lastIntValue;
			if (state.eat(125)) {
				if (max !== -1 && max < min && !noError) state.raise("numbers out of order in {} quantifier");
				return true;
			}
		}
		if (state.switchU && !noError) state.raise("Incomplete quantifier");
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatAtom = function(state) {
	return this.regexp_eatPatternCharacters(state) || state.eat(46) || this.regexp_eatReverseSolidusAtomEscape(state) || this.regexp_eatCharacterClass(state) || this.regexp_eatUncapturingGroup(state) || this.regexp_eatCapturingGroup(state);
};
pp$1.regexp_eatReverseSolidusAtomEscape = function(state) {
	var start = state.pos;
	if (state.eat(92)) {
		if (this.regexp_eatAtomEscape(state)) return true;
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatUncapturingGroup = function(state) {
	var start = state.pos;
	if (state.eat(40)) {
		if (state.eat(63)) {
			if (this.options.ecmaVersion >= 16) {
				var addModifiers = this.regexp_eatModifiers(state);
				var hasHyphen = state.eat(45);
				if (addModifiers || hasHyphen) {
					for (var i = 0; i < addModifiers.length; i++) {
						var modifier = addModifiers.charAt(i);
						if (addModifiers.indexOf(modifier, i + 1) > -1) state.raise("Duplicate regular expression modifiers");
					}
					if (hasHyphen) {
						var removeModifiers = this.regexp_eatModifiers(state);
						if (!addModifiers && !removeModifiers && state.current() === 58) state.raise("Invalid regular expression modifiers");
						for (var i$1 = 0; i$1 < removeModifiers.length; i$1++) {
							var modifier$1 = removeModifiers.charAt(i$1);
							if (removeModifiers.indexOf(modifier$1, i$1 + 1) > -1 || addModifiers.indexOf(modifier$1) > -1) state.raise("Duplicate regular expression modifiers");
						}
					}
				}
			}
			if (state.eat(58)) {
				this.regexp_disjunction(state);
				if (state.eat(41)) return true;
				state.raise("Unterminated group");
			}
		}
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatCapturingGroup = function(state) {
	if (state.eat(40)) {
		if (this.options.ecmaVersion >= 9) this.regexp_groupSpecifier(state);
		else if (state.current() === 63) state.raise("Invalid group");
		this.regexp_disjunction(state);
		if (state.eat(41)) {
			state.numCapturingParens += 1;
			return true;
		}
		state.raise("Unterminated group");
	}
	return false;
};
pp$1.regexp_eatModifiers = function(state) {
	var modifiers = "";
	var ch = 0;
	while ((ch = state.current()) !== -1 && isRegularExpressionModifier(ch)) {
		modifiers += codePointToString(ch);
		state.advance();
	}
	return modifiers;
};
function isRegularExpressionModifier(ch) {
	return ch === 105 || ch === 109 || ch === 115;
}
pp$1.regexp_eatExtendedAtom = function(state) {
	return state.eat(46) || this.regexp_eatReverseSolidusAtomEscape(state) || this.regexp_eatCharacterClass(state) || this.regexp_eatUncapturingGroup(state) || this.regexp_eatCapturingGroup(state) || this.regexp_eatInvalidBracedQuantifier(state) || this.regexp_eatExtendedPatternCharacter(state);
};
pp$1.regexp_eatInvalidBracedQuantifier = function(state) {
	if (this.regexp_eatBracedQuantifier(state, true)) state.raise("Nothing to repeat");
	return false;
};
pp$1.regexp_eatSyntaxCharacter = function(state) {
	var ch = state.current();
	if (isSyntaxCharacter(ch)) {
		state.lastIntValue = ch;
		state.advance();
		return true;
	}
	return false;
};
function isSyntaxCharacter(ch) {
	return ch === 36 || ch >= 40 && ch <= 43 || ch === 46 || ch === 63 || ch >= 91 && ch <= 94 || ch >= 123 && ch <= 125;
}
pp$1.regexp_eatPatternCharacters = function(state) {
	var start = state.pos;
	var ch = 0;
	while ((ch = state.current()) !== -1 && !isSyntaxCharacter(ch)) state.advance();
	return state.pos !== start;
};
pp$1.regexp_eatExtendedPatternCharacter = function(state) {
	var ch = state.current();
	if (ch !== -1 && ch !== 36 && !(ch >= 40 && ch <= 43) && ch !== 46 && ch !== 63 && ch !== 91 && ch !== 94 && ch !== 124) {
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_groupSpecifier = function(state) {
	if (state.eat(63)) {
		if (!this.regexp_eatGroupName(state)) state.raise("Invalid group");
		var trackDisjunction = this.options.ecmaVersion >= 16;
		var known = state.groupNames[state.lastStringValue];
		if (known) if (trackDisjunction) {
			for (var i = 0, list = known; i < list.length; i += 1) if (!list[i].separatedFrom(state.branchID)) state.raise("Duplicate capture group name");
		} else state.raise("Duplicate capture group name");
		if (trackDisjunction) (known || (state.groupNames[state.lastStringValue] = [])).push(state.branchID);
		else state.groupNames[state.lastStringValue] = true;
	}
};
pp$1.regexp_eatGroupName = function(state) {
	state.lastStringValue = "";
	if (state.eat(60)) {
		if (this.regexp_eatRegExpIdentifierName(state) && state.eat(62)) return true;
		state.raise("Invalid capture group name");
	}
	return false;
};
pp$1.regexp_eatRegExpIdentifierName = function(state) {
	state.lastStringValue = "";
	if (this.regexp_eatRegExpIdentifierStart(state)) {
		state.lastStringValue += codePointToString(state.lastIntValue);
		while (this.regexp_eatRegExpIdentifierPart(state)) state.lastStringValue += codePointToString(state.lastIntValue);
		return true;
	}
	return false;
};
pp$1.regexp_eatRegExpIdentifierStart = function(state) {
	var start = state.pos;
	var forceU = this.options.ecmaVersion >= 11;
	var ch = state.current(forceU);
	state.advance(forceU);
	if (ch === 92 && this.regexp_eatRegExpUnicodeEscapeSequence(state, forceU)) ch = state.lastIntValue;
	if (isRegExpIdentifierStart(ch)) {
		state.lastIntValue = ch;
		return true;
	}
	state.pos = start;
	return false;
};
function isRegExpIdentifierStart(ch) {
	return isIdentifierStart(ch, true) || ch === 36 || ch === 95;
}
pp$1.regexp_eatRegExpIdentifierPart = function(state) {
	var start = state.pos;
	var forceU = this.options.ecmaVersion >= 11;
	var ch = state.current(forceU);
	state.advance(forceU);
	if (ch === 92 && this.regexp_eatRegExpUnicodeEscapeSequence(state, forceU)) ch = state.lastIntValue;
	if (isRegExpIdentifierPart(ch)) {
		state.lastIntValue = ch;
		return true;
	}
	state.pos = start;
	return false;
};
function isRegExpIdentifierPart(ch) {
	return isIdentifierChar(ch, true) || ch === 36 || ch === 95 || ch === 8204 || ch === 8205;
}
pp$1.regexp_eatAtomEscape = function(state) {
	if (this.regexp_eatBackReference(state) || this.regexp_eatCharacterClassEscape(state) || this.regexp_eatCharacterEscape(state) || state.switchN && this.regexp_eatKGroupName(state)) return true;
	if (state.switchU) {
		if (state.current() === 99) state.raise("Invalid unicode escape");
		state.raise("Invalid escape");
	}
	return false;
};
pp$1.regexp_eatBackReference = function(state) {
	var start = state.pos;
	if (this.regexp_eatDecimalEscape(state)) {
		var n = state.lastIntValue;
		if (state.switchU) {
			if (n > state.maxBackReference) state.maxBackReference = n;
			return true;
		}
		if (n <= state.numCapturingParens) return true;
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatKGroupName = function(state) {
	if (state.eat(107)) {
		if (this.regexp_eatGroupName(state)) {
			state.backReferenceNames.push(state.lastStringValue);
			return true;
		}
		state.raise("Invalid named reference");
	}
	return false;
};
pp$1.regexp_eatCharacterEscape = function(state) {
	return this.regexp_eatControlEscape(state) || this.regexp_eatCControlLetter(state) || this.regexp_eatZero(state) || this.regexp_eatHexEscapeSequence(state) || this.regexp_eatRegExpUnicodeEscapeSequence(state, false) || !state.switchU && this.regexp_eatLegacyOctalEscapeSequence(state) || this.regexp_eatIdentityEscape(state);
};
pp$1.regexp_eatCControlLetter = function(state) {
	var start = state.pos;
	if (state.eat(99)) {
		if (this.regexp_eatControlLetter(state)) return true;
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatZero = function(state) {
	if (state.current() === 48 && !isDecimalDigit(state.lookahead())) {
		state.lastIntValue = 0;
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_eatControlEscape = function(state) {
	var ch = state.current();
	if (ch === 116) {
		state.lastIntValue = 9;
		state.advance();
		return true;
	}
	if (ch === 110) {
		state.lastIntValue = 10;
		state.advance();
		return true;
	}
	if (ch === 118) {
		state.lastIntValue = 11;
		state.advance();
		return true;
	}
	if (ch === 102) {
		state.lastIntValue = 12;
		state.advance();
		return true;
	}
	if (ch === 114) {
		state.lastIntValue = 13;
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_eatControlLetter = function(state) {
	var ch = state.current();
	if (isControlLetter(ch)) {
		state.lastIntValue = ch % 32;
		state.advance();
		return true;
	}
	return false;
};
function isControlLetter(ch) {
	return ch >= 65 && ch <= 90 || ch >= 97 && ch <= 122;
}
pp$1.regexp_eatRegExpUnicodeEscapeSequence = function(state, forceU) {
	if (forceU === void 0) forceU = false;
	var start = state.pos;
	var switchU = forceU || state.switchU;
	if (state.eat(117)) {
		if (this.regexp_eatFixedHexDigits(state, 4)) {
			var lead = state.lastIntValue;
			if (switchU && lead >= 55296 && lead <= 56319) {
				var leadSurrogateEnd = state.pos;
				if (state.eat(92) && state.eat(117) && this.regexp_eatFixedHexDigits(state, 4)) {
					var trail = state.lastIntValue;
					if (trail >= 56320 && trail <= 57343) {
						state.lastIntValue = (lead - 55296) * 1024 + (trail - 56320) + 65536;
						return true;
					}
				}
				state.pos = leadSurrogateEnd;
				state.lastIntValue = lead;
			}
			return true;
		}
		if (switchU && state.eat(123) && this.regexp_eatHexDigits(state) && state.eat(125) && isValidUnicode(state.lastIntValue)) return true;
		if (switchU) state.raise("Invalid unicode escape");
		state.pos = start;
	}
	return false;
};
function isValidUnicode(ch) {
	return ch >= 0 && ch <= 1114111;
}
pp$1.regexp_eatIdentityEscape = function(state) {
	if (state.switchU) {
		if (this.regexp_eatSyntaxCharacter(state)) return true;
		if (state.eat(47)) {
			state.lastIntValue = 47;
			return true;
		}
		return false;
	}
	var ch = state.current();
	if (ch !== 99 && (!state.switchN || ch !== 107)) {
		state.lastIntValue = ch;
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_eatDecimalEscape = function(state) {
	state.lastIntValue = 0;
	var ch = state.current();
	if (ch >= 49 && ch <= 57) {
		do {
			state.lastIntValue = 10 * state.lastIntValue + (ch - 48);
			state.advance();
		} while ((ch = state.current()) >= 48 && ch <= 57);
		return true;
	}
	return false;
};
var CharSetNone = 0;
var CharSetOk = 1;
var CharSetString = 2;
pp$1.regexp_eatCharacterClassEscape = function(state) {
	var ch = state.current();
	if (isCharacterClassEscape(ch)) {
		state.lastIntValue = -1;
		state.advance();
		return CharSetOk;
	}
	var negate = false;
	if (state.switchU && this.options.ecmaVersion >= 9 && ((negate = ch === 80) || ch === 112)) {
		state.lastIntValue = -1;
		state.advance();
		var result;
		if (state.eat(123) && (result = this.regexp_eatUnicodePropertyValueExpression(state)) && state.eat(125)) {
			if (negate && result === CharSetString) state.raise("Invalid property name");
			return result;
		}
		state.raise("Invalid property name");
	}
	return CharSetNone;
};
function isCharacterClassEscape(ch) {
	return ch === 100 || ch === 68 || ch === 115 || ch === 83 || ch === 119 || ch === 87;
}
pp$1.regexp_eatUnicodePropertyValueExpression = function(state) {
	var start = state.pos;
	if (this.regexp_eatUnicodePropertyName(state) && state.eat(61)) {
		var name = state.lastStringValue;
		if (this.regexp_eatUnicodePropertyValue(state)) {
			var value = state.lastStringValue;
			this.regexp_validateUnicodePropertyNameAndValue(state, name, value);
			return CharSetOk;
		}
	}
	state.pos = start;
	if (this.regexp_eatLoneUnicodePropertyNameOrValue(state)) {
		var nameOrValue = state.lastStringValue;
		return this.regexp_validateUnicodePropertyNameOrValue(state, nameOrValue);
	}
	return CharSetNone;
};
pp$1.regexp_validateUnicodePropertyNameAndValue = function(state, name, value) {
	if (!hasOwn(state.unicodeProperties.nonBinary, name)) state.raise("Invalid property name");
	if (!state.unicodeProperties.nonBinary[name].test(value)) state.raise("Invalid property value");
};
pp$1.regexp_validateUnicodePropertyNameOrValue = function(state, nameOrValue) {
	if (state.unicodeProperties.binary.test(nameOrValue)) return CharSetOk;
	if (state.switchV && state.unicodeProperties.binaryOfStrings.test(nameOrValue)) return CharSetString;
	state.raise("Invalid property name");
};
pp$1.regexp_eatUnicodePropertyName = function(state) {
	var ch = 0;
	state.lastStringValue = "";
	while (isUnicodePropertyNameCharacter(ch = state.current())) {
		state.lastStringValue += codePointToString(ch);
		state.advance();
	}
	return state.lastStringValue !== "";
};
function isUnicodePropertyNameCharacter(ch) {
	return isControlLetter(ch) || ch === 95;
}
pp$1.regexp_eatUnicodePropertyValue = function(state) {
	var ch = 0;
	state.lastStringValue = "";
	while (isUnicodePropertyValueCharacter(ch = state.current())) {
		state.lastStringValue += codePointToString(ch);
		state.advance();
	}
	return state.lastStringValue !== "";
};
function isUnicodePropertyValueCharacter(ch) {
	return isUnicodePropertyNameCharacter(ch) || isDecimalDigit(ch);
}
pp$1.regexp_eatLoneUnicodePropertyNameOrValue = function(state) {
	return this.regexp_eatUnicodePropertyValue(state);
};
pp$1.regexp_eatCharacterClass = function(state) {
	if (state.eat(91)) {
		var negate = state.eat(94);
		var result = this.regexp_classContents(state);
		if (!state.eat(93)) state.raise("Unterminated character class");
		if (negate && result === CharSetString) state.raise("Negated character class may contain strings");
		return true;
	}
	return false;
};
pp$1.regexp_classContents = function(state) {
	if (state.current() === 93) return CharSetOk;
	if (state.switchV) return this.regexp_classSetExpression(state);
	this.regexp_nonEmptyClassRanges(state);
	return CharSetOk;
};
pp$1.regexp_nonEmptyClassRanges = function(state) {
	while (this.regexp_eatClassAtom(state)) {
		var left = state.lastIntValue;
		if (state.eat(45) && this.regexp_eatClassAtom(state)) {
			var right = state.lastIntValue;
			if (state.switchU && (left === -1 || right === -1)) state.raise("Invalid character class");
			if (left !== -1 && right !== -1 && left > right) state.raise("Range out of order in character class");
		}
	}
};
pp$1.regexp_eatClassAtom = function(state) {
	var start = state.pos;
	if (state.eat(92)) {
		if (this.regexp_eatClassEscape(state)) return true;
		if (state.switchU) {
			var ch$1 = state.current();
			if (ch$1 === 99 || isOctalDigit(ch$1)) state.raise("Invalid class escape");
			state.raise("Invalid escape");
		}
		state.pos = start;
	}
	var ch = state.current();
	if (ch !== 93) {
		state.lastIntValue = ch;
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_eatClassEscape = function(state) {
	var start = state.pos;
	if (state.eat(98)) {
		state.lastIntValue = 8;
		return true;
	}
	if (state.switchU && state.eat(45)) {
		state.lastIntValue = 45;
		return true;
	}
	if (!state.switchU && state.eat(99)) {
		if (this.regexp_eatClassControlLetter(state)) return true;
		state.pos = start;
	}
	return this.regexp_eatCharacterClassEscape(state) || this.regexp_eatCharacterEscape(state);
};
pp$1.regexp_classSetExpression = function(state) {
	var result = CharSetOk, subResult;
	if (this.regexp_eatClassSetRange(state));
	else if (subResult = this.regexp_eatClassSetOperand(state)) {
		if (subResult === CharSetString) result = CharSetString;
		var start = state.pos;
		while (state.eatChars([38, 38])) {
			if (state.current() !== 38 && (subResult = this.regexp_eatClassSetOperand(state))) {
				if (subResult !== CharSetString) result = CharSetOk;
				continue;
			}
			state.raise("Invalid character in character class");
		}
		if (start !== state.pos) return result;
		while (state.eatChars([45, 45])) {
			if (this.regexp_eatClassSetOperand(state)) continue;
			state.raise("Invalid character in character class");
		}
		if (start !== state.pos) return result;
	} else state.raise("Invalid character in character class");
	for (;;) {
		if (this.regexp_eatClassSetRange(state)) continue;
		subResult = this.regexp_eatClassSetOperand(state);
		if (!subResult) return result;
		if (subResult === CharSetString) result = CharSetString;
	}
};
pp$1.regexp_eatClassSetRange = function(state) {
	var start = state.pos;
	if (this.regexp_eatClassSetCharacter(state)) {
		var left = state.lastIntValue;
		if (state.eat(45) && this.regexp_eatClassSetCharacter(state)) {
			var right = state.lastIntValue;
			if (left !== -1 && right !== -1 && left > right) state.raise("Range out of order in character class");
			return true;
		}
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatClassSetOperand = function(state) {
	if (this.regexp_eatClassSetCharacter(state)) return CharSetOk;
	return this.regexp_eatClassStringDisjunction(state) || this.regexp_eatNestedClass(state);
};
pp$1.regexp_eatNestedClass = function(state) {
	var start = state.pos;
	if (state.eat(91)) {
		var negate = state.eat(94);
		var result = this.regexp_classContents(state);
		if (state.eat(93)) {
			if (negate && result === CharSetString) state.raise("Negated character class may contain strings");
			return result;
		}
		state.pos = start;
	}
	if (state.eat(92)) {
		var result$1 = this.regexp_eatCharacterClassEscape(state);
		if (result$1) return result$1;
		state.pos = start;
	}
	return null;
};
pp$1.regexp_eatClassStringDisjunction = function(state) {
	var start = state.pos;
	if (state.eatChars([92, 113])) {
		if (state.eat(123)) {
			var result = this.regexp_classStringDisjunctionContents(state);
			if (state.eat(125)) return result;
		} else state.raise("Invalid escape");
		state.pos = start;
	}
	return null;
};
pp$1.regexp_classStringDisjunctionContents = function(state) {
	var result = this.regexp_classString(state);
	while (state.eat(124)) if (this.regexp_classString(state) === CharSetString) result = CharSetString;
	return result;
};
pp$1.regexp_classString = function(state) {
	var count = 0;
	while (this.regexp_eatClassSetCharacter(state)) count++;
	return count === 1 ? CharSetOk : CharSetString;
};
pp$1.regexp_eatClassSetCharacter = function(state) {
	var start = state.pos;
	if (state.eat(92)) {
		if (this.regexp_eatCharacterEscape(state) || this.regexp_eatClassSetReservedPunctuator(state)) return true;
		if (state.eat(98)) {
			state.lastIntValue = 8;
			return true;
		}
		state.pos = start;
		return false;
	}
	var ch = state.current();
	if (ch < 0 || ch === state.lookahead() && isClassSetReservedDoublePunctuatorCharacter(ch)) return false;
	if (isClassSetSyntaxCharacter(ch)) return false;
	state.advance();
	state.lastIntValue = ch;
	return true;
};
function isClassSetReservedDoublePunctuatorCharacter(ch) {
	return ch === 33 || ch >= 35 && ch <= 38 || ch >= 42 && ch <= 44 || ch === 46 || ch >= 58 && ch <= 64 || ch === 94 || ch === 96 || ch === 126;
}
function isClassSetSyntaxCharacter(ch) {
	return ch === 40 || ch === 41 || ch === 45 || ch === 47 || ch >= 91 && ch <= 93 || ch >= 123 && ch <= 125;
}
pp$1.regexp_eatClassSetReservedPunctuator = function(state) {
	var ch = state.current();
	if (isClassSetReservedPunctuator(ch)) {
		state.lastIntValue = ch;
		state.advance();
		return true;
	}
	return false;
};
function isClassSetReservedPunctuator(ch) {
	return ch === 33 || ch === 35 || ch === 37 || ch === 38 || ch === 44 || ch === 45 || ch >= 58 && ch <= 62 || ch === 64 || ch === 96 || ch === 126;
}
pp$1.regexp_eatClassControlLetter = function(state) {
	var ch = state.current();
	if (isDecimalDigit(ch) || ch === 95) {
		state.lastIntValue = ch % 32;
		state.advance();
		return true;
	}
	return false;
};
pp$1.regexp_eatHexEscapeSequence = function(state) {
	var start = state.pos;
	if (state.eat(120)) {
		if (this.regexp_eatFixedHexDigits(state, 2)) return true;
		if (state.switchU) state.raise("Invalid escape");
		state.pos = start;
	}
	return false;
};
pp$1.regexp_eatDecimalDigits = function(state) {
	var start = state.pos;
	var ch = 0;
	state.lastIntValue = 0;
	while (isDecimalDigit(ch = state.current())) {
		state.lastIntValue = 10 * state.lastIntValue + (ch - 48);
		state.advance();
	}
	return state.pos !== start;
};
function isDecimalDigit(ch) {
	return ch >= 48 && ch <= 57;
}
pp$1.regexp_eatHexDigits = function(state) {
	var start = state.pos;
	var ch = 0;
	state.lastIntValue = 0;
	while (isHexDigit(ch = state.current())) {
		state.lastIntValue = 16 * state.lastIntValue + hexToInt(ch);
		state.advance();
	}
	return state.pos !== start;
};
function isHexDigit(ch) {
	return ch >= 48 && ch <= 57 || ch >= 65 && ch <= 70 || ch >= 97 && ch <= 102;
}
function hexToInt(ch) {
	if (ch >= 65 && ch <= 70) return 10 + (ch - 65);
	if (ch >= 97 && ch <= 102) return 10 + (ch - 97);
	return ch - 48;
}
pp$1.regexp_eatLegacyOctalEscapeSequence = function(state) {
	if (this.regexp_eatOctalDigit(state)) {
		var n1 = state.lastIntValue;
		if (this.regexp_eatOctalDigit(state)) {
			var n2 = state.lastIntValue;
			if (n1 <= 3 && this.regexp_eatOctalDigit(state)) state.lastIntValue = n1 * 64 + n2 * 8 + state.lastIntValue;
			else state.lastIntValue = n1 * 8 + n2;
		} else state.lastIntValue = n1;
		return true;
	}
	return false;
};
pp$1.regexp_eatOctalDigit = function(state) {
	var ch = state.current();
	if (isOctalDigit(ch)) {
		state.lastIntValue = ch - 48;
		state.advance();
		return true;
	}
	state.lastIntValue = 0;
	return false;
};
function isOctalDigit(ch) {
	return ch >= 48 && ch <= 55;
}
pp$1.regexp_eatFixedHexDigits = function(state, length) {
	var start = state.pos;
	state.lastIntValue = 0;
	for (var i = 0; i < length; ++i) {
		var ch = state.current();
		if (!isHexDigit(ch)) {
			state.pos = start;
			return false;
		}
		state.lastIntValue = 16 * state.lastIntValue + hexToInt(ch);
		state.advance();
	}
	return true;
};
var Token = function Token(p) {
	this.type = p.type;
	this.value = p.value;
	this.start = p.start;
	this.end = p.end;
	if (p.options.locations) this.loc = new SourceLocation(p, p.startLoc, p.endLoc);
	if (p.options.ranges) this.range = [p.start, p.end];
};
var pp = Parser.prototype;
pp.next = function(ignoreEscapeSequenceInKeyword) {
	if (!ignoreEscapeSequenceInKeyword && this.type.keyword && this.containsEsc) this.raiseRecoverable(this.start, "Escape sequence in keyword " + this.type.keyword);
	if (this.options.onToken) this.options.onToken(new Token(this));
	this.lastTokEnd = this.end;
	this.lastTokStart = this.start;
	this.lastTokEndLoc = this.endLoc;
	this.lastTokStartLoc = this.startLoc;
	this.nextToken();
};
pp.getToken = function() {
	this.next();
	return new Token(this);
};
if (typeof Symbol !== "undefined") pp[Symbol.iterator] = function() {
	var this$1$1 = this;
	return { next: function() {
		var token = this$1$1.getToken();
		return {
			done: token.type === types$1.eof,
			value: token
		};
	} };
};
pp.nextToken = function() {
	var curContext = this.curContext();
	if (!curContext || !curContext.preserveSpace) this.skipSpace();
	this.start = this.pos;
	if (this.options.locations) this.startLoc = this.curPosition();
	if (this.pos >= this.input.length) return this.finishToken(types$1.eof);
	if (curContext.override) return curContext.override(this);
	else this.readToken(this.fullCharCodeAtPos());
};
pp.readToken = function(code) {
	if (isIdentifierStart(code, this.options.ecmaVersion >= 6) || code === 92) return this.readWord();
	return this.getTokenFromCode(code);
};
pp.fullCharCodeAt = function(pos) {
	var code = this.input.charCodeAt(pos);
	if (code <= 55295 || code >= 56320) return code;
	var next = this.input.charCodeAt(pos + 1);
	return next <= 56319 || next >= 57344 ? code : (code << 10) + next - 56613888;
};
pp.fullCharCodeAtPos = function() {
	return this.fullCharCodeAt(this.pos);
};
pp.skipBlockComment = function() {
	var startLoc = this.options.onComment && this.curPosition();
	var start = this.pos, end = this.input.indexOf("*/", this.pos += 2);
	if (end === -1) this.raise(this.pos - 2, "Unterminated comment");
	this.pos = end + 2;
	if (this.options.locations) for (var nextBreak = void 0, pos = start; (nextBreak = nextLineBreak(this.input, pos, this.pos)) > -1;) {
		++this.curLine;
		pos = this.lineStart = nextBreak;
	}
	if (this.options.onComment) this.options.onComment(true, this.input.slice(start + 2, end), start, this.pos, startLoc, this.curPosition());
};
pp.skipLineComment = function(startSkip) {
	var start = this.pos;
	var startLoc = this.options.onComment && this.curPosition();
	var ch = this.input.charCodeAt(this.pos += startSkip);
	while (this.pos < this.input.length && !isNewLine(ch)) ch = this.input.charCodeAt(++this.pos);
	if (this.options.onComment) this.options.onComment(false, this.input.slice(start + startSkip, this.pos), start, this.pos, startLoc, this.curPosition());
};
pp.skipSpace = function() {
	loop: while (this.pos < this.input.length) {
		var ch = this.input.charCodeAt(this.pos);
		switch (ch) {
			case 32:
			case 160:
				++this.pos;
				break;
			case 13: if (this.input.charCodeAt(this.pos + 1) === 10) ++this.pos;
			case 10:
			case 8232:
			case 8233:
				++this.pos;
				if (this.options.locations) {
					++this.curLine;
					this.lineStart = this.pos;
				}
				break;
			case 47:
				switch (this.input.charCodeAt(this.pos + 1)) {
					case 42:
						this.skipBlockComment();
						break;
					case 47:
						this.skipLineComment(2);
						break;
					default: break loop;
				}
				break;
			default: if (ch > 8 && ch < 14 || ch >= 5760 && nonASCIIwhitespace.test(String.fromCharCode(ch))) ++this.pos;
			else break loop;
		}
	}
};
pp.finishToken = function(type, val) {
	this.end = this.pos;
	if (this.options.locations) this.endLoc = this.curPosition();
	var prevType = this.type;
	this.type = type;
	this.value = val;
	this.updateContext(prevType);
};
pp.readToken_dot = function() {
	var next = this.input.charCodeAt(this.pos + 1);
	if (next >= 48 && next <= 57) return this.readNumber(true);
	var next2 = this.input.charCodeAt(this.pos + 2);
	if (this.options.ecmaVersion >= 6 && next === 46 && next2 === 46) {
		this.pos += 3;
		return this.finishToken(types$1.ellipsis);
	} else {
		++this.pos;
		return this.finishToken(types$1.dot);
	}
};
pp.readToken_slash = function() {
	var next = this.input.charCodeAt(this.pos + 1);
	if (this.exprAllowed) {
		++this.pos;
		return this.readRegexp();
	}
	if (next === 61) return this.finishOp(types$1.assign, 2);
	return this.finishOp(types$1.slash, 1);
};
pp.readToken_mult_modulo_exp = function(code) {
	var next = this.input.charCodeAt(this.pos + 1);
	var size = 1;
	var tokentype = code === 42 ? types$1.star : types$1.modulo;
	if (this.options.ecmaVersion >= 7 && code === 42 && next === 42) {
		++size;
		tokentype = types$1.starstar;
		next = this.input.charCodeAt(this.pos + 2);
	}
	if (next === 61) return this.finishOp(types$1.assign, size + 1);
	return this.finishOp(tokentype, size);
};
pp.readToken_pipe_amp = function(code) {
	var next = this.input.charCodeAt(this.pos + 1);
	if (next === code) {
		if (this.options.ecmaVersion >= 12) {
			if (this.input.charCodeAt(this.pos + 2) === 61) return this.finishOp(types$1.assign, 3);
		}
		return this.finishOp(code === 124 ? types$1.logicalOR : types$1.logicalAND, 2);
	}
	if (next === 61) return this.finishOp(types$1.assign, 2);
	return this.finishOp(code === 124 ? types$1.bitwiseOR : types$1.bitwiseAND, 1);
};
pp.readToken_caret = function() {
	if (this.input.charCodeAt(this.pos + 1) === 61) return this.finishOp(types$1.assign, 2);
	return this.finishOp(types$1.bitwiseXOR, 1);
};
pp.readToken_plus_min = function(code) {
	var next = this.input.charCodeAt(this.pos + 1);
	if (next === code) {
		if (next === 45 && !this.inModule && this.input.charCodeAt(this.pos + 2) === 62 && (this.lastTokEnd === 0 || lineBreak.test(this.input.slice(this.lastTokEnd, this.pos)))) {
			this.skipLineComment(3);
			this.skipSpace();
			return this.nextToken();
		}
		return this.finishOp(types$1.incDec, 2);
	}
	if (next === 61) return this.finishOp(types$1.assign, 2);
	return this.finishOp(types$1.plusMin, 1);
};
pp.readToken_lt_gt = function(code) {
	var next = this.input.charCodeAt(this.pos + 1);
	var size = 1;
	if (next === code) {
		size = code === 62 && this.input.charCodeAt(this.pos + 2) === 62 ? 3 : 2;
		if (this.input.charCodeAt(this.pos + size) === 61) return this.finishOp(types$1.assign, size + 1);
		return this.finishOp(types$1.bitShift, size);
	}
	if (next === 33 && code === 60 && !this.inModule && this.input.charCodeAt(this.pos + 2) === 45 && this.input.charCodeAt(this.pos + 3) === 45) {
		this.skipLineComment(4);
		this.skipSpace();
		return this.nextToken();
	}
	if (next === 61) size = 2;
	return this.finishOp(types$1.relational, size);
};
pp.readToken_eq_excl = function(code) {
	var next = this.input.charCodeAt(this.pos + 1);
	if (next === 61) return this.finishOp(types$1.equality, this.input.charCodeAt(this.pos + 2) === 61 ? 3 : 2);
	if (code === 61 && next === 62 && this.options.ecmaVersion >= 6) {
		this.pos += 2;
		return this.finishToken(types$1.arrow);
	}
	return this.finishOp(code === 61 ? types$1.eq : types$1.prefix, 1);
};
pp.readToken_question = function() {
	var ecmaVersion = this.options.ecmaVersion;
	if (ecmaVersion >= 11) {
		var next = this.input.charCodeAt(this.pos + 1);
		if (next === 46) {
			var next2 = this.input.charCodeAt(this.pos + 2);
			if (next2 < 48 || next2 > 57) return this.finishOp(types$1.questionDot, 2);
		}
		if (next === 63) {
			if (ecmaVersion >= 12) {
				if (this.input.charCodeAt(this.pos + 2) === 61) return this.finishOp(types$1.assign, 3);
			}
			return this.finishOp(types$1.coalesce, 2);
		}
	}
	return this.finishOp(types$1.question, 1);
};
pp.readToken_numberSign = function() {
	var ecmaVersion = this.options.ecmaVersion;
	var code = 35;
	if (ecmaVersion >= 13) {
		++this.pos;
		code = this.fullCharCodeAtPos();
		if (isIdentifierStart(code, true) || code === 92) return this.finishToken(types$1.privateId, this.readWord1());
	}
	this.raise(this.pos, "Unexpected character '" + codePointToString(code) + "'");
};
pp.getTokenFromCode = function(code) {
	switch (code) {
		case 46: return this.readToken_dot();
		case 40:
			++this.pos;
			return this.finishToken(types$1.parenL);
		case 41:
			++this.pos;
			return this.finishToken(types$1.parenR);
		case 59:
			++this.pos;
			return this.finishToken(types$1.semi);
		case 44:
			++this.pos;
			return this.finishToken(types$1.comma);
		case 91:
			++this.pos;
			return this.finishToken(types$1.bracketL);
		case 93:
			++this.pos;
			return this.finishToken(types$1.bracketR);
		case 123:
			++this.pos;
			return this.finishToken(types$1.braceL);
		case 125:
			++this.pos;
			return this.finishToken(types$1.braceR);
		case 58:
			++this.pos;
			return this.finishToken(types$1.colon);
		case 96:
			if (this.options.ecmaVersion < 6) break;
			++this.pos;
			return this.finishToken(types$1.backQuote);
		case 48:
			var next = this.input.charCodeAt(this.pos + 1);
			if (next === 120 || next === 88) return this.readRadixNumber(16);
			if (this.options.ecmaVersion >= 6) {
				if (next === 111 || next === 79) return this.readRadixNumber(8);
				if (next === 98 || next === 66) return this.readRadixNumber(2);
			}
		case 49:
		case 50:
		case 51:
		case 52:
		case 53:
		case 54:
		case 55:
		case 56:
		case 57: return this.readNumber(false);
		case 34:
		case 39: return this.readString(code);
		case 47: return this.readToken_slash();
		case 37:
		case 42: return this.readToken_mult_modulo_exp(code);
		case 124:
		case 38: return this.readToken_pipe_amp(code);
		case 94: return this.readToken_caret();
		case 43:
		case 45: return this.readToken_plus_min(code);
		case 60:
		case 62: return this.readToken_lt_gt(code);
		case 61:
		case 33: return this.readToken_eq_excl(code);
		case 63: return this.readToken_question();
		case 126: return this.finishOp(types$1.prefix, 1);
		case 35: return this.readToken_numberSign();
	}
	this.raise(this.pos, "Unexpected character '" + codePointToString(code) + "'");
};
pp.finishOp = function(type, size) {
	var str = this.input.slice(this.pos, this.pos + size);
	this.pos += size;
	return this.finishToken(type, str);
};
pp.readRegexp = function() {
	var escaped, inClass, start = this.pos;
	for (;;) {
		if (this.pos >= this.input.length) this.raise(start, "Unterminated regular expression");
		var ch = this.input.charAt(this.pos);
		if (lineBreak.test(ch)) this.raise(start, "Unterminated regular expression");
		if (!escaped) {
			if (ch === "[") inClass = true;
			else if (ch === "]" && inClass) inClass = false;
			else if (ch === "/" && !inClass) break;
			escaped = ch === "\\";
		} else escaped = false;
		++this.pos;
	}
	var pattern = this.input.slice(start, this.pos);
	++this.pos;
	var flagsStart = this.pos;
	var flags = this.readWord1();
	if (this.containsEsc) this.unexpected(flagsStart);
	var state = this.regexpState || (this.regexpState = new RegExpValidationState(this));
	state.reset(start, pattern, flags);
	this.validateRegExpFlags(state);
	this.validateRegExpPattern(state);
	var value = null;
	try {
		value = new RegExp(pattern, flags);
	} catch (e) {}
	return this.finishToken(types$1.regexp, {
		pattern,
		flags,
		value
	});
};
pp.readInt = function(radix, len, maybeLegacyOctalNumericLiteral) {
	var allowSeparators = this.options.ecmaVersion >= 12 && len === void 0;
	var isLegacyOctalNumericLiteral = maybeLegacyOctalNumericLiteral && this.input.charCodeAt(this.pos) === 48;
	var start = this.pos, total = 0, lastCode = 0;
	for (var i = 0, e = len == null ? Infinity : len; i < e; ++i, ++this.pos) {
		var code = this.input.charCodeAt(this.pos), val = void 0;
		if (allowSeparators && code === 95) {
			if (isLegacyOctalNumericLiteral) this.raiseRecoverable(this.pos, "Numeric separator is not allowed in legacy octal numeric literals");
			if (lastCode === 95) this.raiseRecoverable(this.pos, "Numeric separator must be exactly one underscore");
			if (i === 0) this.raiseRecoverable(this.pos, "Numeric separator is not allowed at the first of digits");
			lastCode = code;
			continue;
		}
		if (code >= 97) val = code - 97 + 10;
		else if (code >= 65) val = code - 65 + 10;
		else if (code >= 48 && code <= 57) val = code - 48;
		else val = Infinity;
		if (val >= radix) break;
		lastCode = code;
		total = total * radix + val;
	}
	if (allowSeparators && lastCode === 95) this.raiseRecoverable(this.pos - 1, "Numeric separator is not allowed at the last of digits");
	if (this.pos === start || len != null && this.pos - start !== len) return null;
	return total;
};
function stringToNumber(str, isLegacyOctalNumericLiteral) {
	if (isLegacyOctalNumericLiteral) return parseInt(str, 8);
	return parseFloat(str.replace(/_/g, ""));
}
function stringToBigInt(str) {
	if (typeof BigInt !== "function") return null;
	return BigInt(str.replace(/_/g, ""));
}
pp.readRadixNumber = function(radix) {
	var start = this.pos;
	this.pos += 2;
	var val = this.readInt(radix);
	if (val == null) this.raise(this.start + 2, "Expected number in radix " + radix);
	if (this.options.ecmaVersion >= 11 && this.input.charCodeAt(this.pos) === 110) {
		val = stringToBigInt(this.input.slice(start, this.pos));
		++this.pos;
	} else if (isIdentifierStart(this.fullCharCodeAtPos())) this.raise(this.pos, "Identifier directly after number");
	return this.finishToken(types$1.num, val);
};
pp.readNumber = function(startsWithDot) {
	var start = this.pos;
	if (!startsWithDot && this.readInt(10, void 0, true) === null) this.raise(start, "Invalid number");
	var octal = this.pos - start >= 2 && this.input.charCodeAt(start) === 48;
	if (octal && this.strict) this.raise(start, "Invalid number");
	var next = this.input.charCodeAt(this.pos);
	if (!octal && !startsWithDot && this.options.ecmaVersion >= 11 && next === 110) {
		var val$1 = stringToBigInt(this.input.slice(start, this.pos));
		++this.pos;
		if (isIdentifierStart(this.fullCharCodeAtPos())) this.raise(this.pos, "Identifier directly after number");
		return this.finishToken(types$1.num, val$1);
	}
	if (octal && /[89]/.test(this.input.slice(start, this.pos))) octal = false;
	if (next === 46 && !octal) {
		++this.pos;
		this.readInt(10);
		next = this.input.charCodeAt(this.pos);
	}
	if ((next === 69 || next === 101) && !octal) {
		next = this.input.charCodeAt(++this.pos);
		if (next === 43 || next === 45) ++this.pos;
		if (this.readInt(10) === null) this.raise(start, "Invalid number");
	}
	if (isIdentifierStart(this.fullCharCodeAtPos())) this.raise(this.pos, "Identifier directly after number");
	var val = stringToNumber(this.input.slice(start, this.pos), octal);
	return this.finishToken(types$1.num, val);
};
pp.readCodePoint = function() {
	var ch = this.input.charCodeAt(this.pos), code;
	if (ch === 123) {
		if (this.options.ecmaVersion < 6) this.unexpected();
		var codePos = ++this.pos;
		code = this.readHexChar(this.input.indexOf("}", this.pos) - this.pos);
		++this.pos;
		if (code > 1114111) this.invalidStringToken(codePos, "Code point out of bounds");
	} else code = this.readHexChar(4);
	return code;
};
pp.readString = function(quote) {
	var out = "", chunkStart = ++this.pos;
	for (;;) {
		if (this.pos >= this.input.length) this.raise(this.start, "Unterminated string constant");
		var ch = this.input.charCodeAt(this.pos);
		if (ch === quote) break;
		if (ch === 92) {
			out += this.input.slice(chunkStart, this.pos);
			out += this.readEscapedChar(false);
			chunkStart = this.pos;
		} else if (ch === 8232 || ch === 8233) {
			if (this.options.ecmaVersion < 10) this.raise(this.start, "Unterminated string constant");
			++this.pos;
			if (this.options.locations) {
				this.curLine++;
				this.lineStart = this.pos;
			}
		} else {
			if (isNewLine(ch)) this.raise(this.start, "Unterminated string constant");
			++this.pos;
		}
	}
	out += this.input.slice(chunkStart, this.pos++);
	return this.finishToken(types$1.string, out);
};
var INVALID_TEMPLATE_ESCAPE_ERROR = {};
pp.tryReadTemplateToken = function() {
	this.inTemplateElement = true;
	try {
		this.readTmplToken();
	} catch (err) {
		if (err === INVALID_TEMPLATE_ESCAPE_ERROR) this.readInvalidTemplateToken();
		else throw err;
	}
	this.inTemplateElement = false;
};
pp.invalidStringToken = function(position, message) {
	if (this.inTemplateElement && this.options.ecmaVersion >= 9) throw INVALID_TEMPLATE_ESCAPE_ERROR;
	else this.raise(position, message);
};
pp.readTmplToken = function() {
	var out = "", chunkStart = this.pos;
	for (;;) {
		if (this.pos >= this.input.length) this.raise(this.start, "Unterminated template");
		var ch = this.input.charCodeAt(this.pos);
		if (ch === 96 || ch === 36 && this.input.charCodeAt(this.pos + 1) === 123) {
			if (this.pos === this.start && (this.type === types$1.template || this.type === types$1.invalidTemplate)) if (ch === 36) {
				this.pos += 2;
				return this.finishToken(types$1.dollarBraceL);
			} else {
				++this.pos;
				return this.finishToken(types$1.backQuote);
			}
			out += this.input.slice(chunkStart, this.pos);
			return this.finishToken(types$1.template, out);
		}
		if (ch === 92) {
			out += this.input.slice(chunkStart, this.pos);
			out += this.readEscapedChar(true);
			chunkStart = this.pos;
		} else if (isNewLine(ch)) {
			out += this.input.slice(chunkStart, this.pos);
			++this.pos;
			switch (ch) {
				case 13: if (this.input.charCodeAt(this.pos) === 10) ++this.pos;
				case 10:
					out += "\n";
					break;
				default:
					out += String.fromCharCode(ch);
					break;
			}
			if (this.options.locations) {
				++this.curLine;
				this.lineStart = this.pos;
			}
			chunkStart = this.pos;
		} else ++this.pos;
	}
};
pp.readInvalidTemplateToken = function() {
	for (; this.pos < this.input.length; this.pos++) switch (this.input[this.pos]) {
		case "\\":
			++this.pos;
			break;
		case "$": if (this.input[this.pos + 1] !== "{") break;
		case "`": return this.finishToken(types$1.invalidTemplate, this.input.slice(this.start, this.pos));
		case "\r": if (this.input[this.pos + 1] === "\n") ++this.pos;
		case "\n":
		case "\u2028":
		case "\u2029":
			++this.curLine;
			this.lineStart = this.pos + 1;
			break;
	}
	this.raise(this.start, "Unterminated template");
};
pp.readEscapedChar = function(inTemplate) {
	var ch = this.input.charCodeAt(++this.pos);
	++this.pos;
	switch (ch) {
		case 110: return "\n";
		case 114: return "\r";
		case 120: return String.fromCharCode(this.readHexChar(2));
		case 117: return codePointToString(this.readCodePoint());
		case 116: return "	";
		case 98: return "\b";
		case 118: return "\v";
		case 102: return "\f";
		case 13: if (this.input.charCodeAt(this.pos) === 10) ++this.pos;
		case 10:
			if (this.options.locations) {
				this.lineStart = this.pos;
				++this.curLine;
			}
			return "";
		case 56:
		case 57:
			if (this.strict) this.invalidStringToken(this.pos - 1, "Invalid escape sequence");
			if (inTemplate) {
				var codePos = this.pos - 1;
				this.invalidStringToken(codePos, "Invalid escape sequence in template string");
			}
		default:
			if (ch >= 48 && ch <= 55) {
				var octalStr = this.input.substr(this.pos - 1, 3).match(/^[0-7]+/)[0];
				var octal = parseInt(octalStr, 8);
				if (octal > 255) {
					octalStr = octalStr.slice(0, -1);
					octal = parseInt(octalStr, 8);
				}
				this.pos += octalStr.length - 1;
				ch = this.input.charCodeAt(this.pos);
				if ((octalStr !== "0" || ch === 56 || ch === 57) && (this.strict || inTemplate)) this.invalidStringToken(this.pos - 1 - octalStr.length, inTemplate ? "Octal literal in template string" : "Octal literal in strict mode");
				return String.fromCharCode(octal);
			}
			if (isNewLine(ch)) {
				if (this.options.locations) {
					this.lineStart = this.pos;
					++this.curLine;
				}
				return "";
			}
			return String.fromCharCode(ch);
	}
};
pp.readHexChar = function(len) {
	var codePos = this.pos;
	var n = this.readInt(16, len);
	if (n === null) this.invalidStringToken(codePos, "Bad character escape sequence");
	return n;
};
pp.readWord1 = function() {
	this.containsEsc = false;
	var word = "", first = true, chunkStart = this.pos;
	var astral = this.options.ecmaVersion >= 6;
	while (this.pos < this.input.length) {
		var ch = this.fullCharCodeAtPos();
		if (isIdentifierChar(ch, astral)) this.pos += ch <= 65535 ? 1 : 2;
		else if (ch === 92) {
			this.containsEsc = true;
			word += this.input.slice(chunkStart, this.pos);
			var escStart = this.pos;
			if (this.input.charCodeAt(++this.pos) !== 117) this.invalidStringToken(this.pos, "Expecting Unicode escape sequence \\uXXXX");
			++this.pos;
			var esc = this.readCodePoint();
			if (!(first ? isIdentifierStart : isIdentifierChar)(esc, astral)) this.invalidStringToken(escStart, "Invalid Unicode escape");
			word += codePointToString(esc);
			chunkStart = this.pos;
		} else break;
		first = false;
	}
	return word + this.input.slice(chunkStart, this.pos);
};
pp.readWord = function() {
	var word = this.readWord1();
	var type = types$1.name;
	if (this.keywords.test(word)) type = keywords[word];
	return this.finishToken(type, word);
};
var version = "8.16.0";
Parser.acorn = {
	Parser,
	version,
	defaultOptions,
	Position,
	SourceLocation,
	getLineInfo,
	Node,
	TokenType,
	tokTypes: types$1,
	keywordTypes: keywords,
	TokContext,
	tokContexts: types$2,
	isIdentifierChar,
	isIdentifierStart,
	Token,
	isNewLine,
	lineBreak,
	lineBreakG,
	nonASCIIwhitespace
};

//#endregion
//#region node_modules/.pnpm/ufo@1.6.3/node_modules/ufo/dist/index.mjs
const r = String.fromCharCode;
const TRAILING_SLASH_RE = /\/$|\/\?|\/#/;
const JOIN_LEADING_SLASH_RE = /^\.?\//;
function hasTrailingSlash(input = "", respectQueryAndFragment) {
	if (!respectQueryAndFragment) return input.endsWith("/");
	return TRAILING_SLASH_RE.test(input);
}
function withTrailingSlash(input = "", respectQueryAndFragment) {
	if (!respectQueryAndFragment) return input.endsWith("/") ? input : input + "/";
	if (hasTrailingSlash(input, true)) return input || "/";
	let path = input;
	let fragment = "";
	const fragmentIndex = input.indexOf("#");
	if (fragmentIndex !== -1) {
		path = input.slice(0, fragmentIndex);
		fragment = input.slice(fragmentIndex);
		if (!path) return fragment;
	}
	const [s0, ...s] = path.split("?");
	return s0 + "/" + (s.length > 0 ? `?${s.join("?")}` : "") + fragment;
}
function isNonEmptyURL(url) {
	return url && url !== "/";
}
function joinURL(base, ...input) {
	let url = base || "";
	for (const segment of input.filter((url2) => isNonEmptyURL(url2))) if (url) {
		const _segment = segment.replace(JOIN_LEADING_SLASH_RE, "");
		url = withTrailingSlash(url) + _segment;
	} else url = segment;
	return url;
}
const protocolRelative = Symbol.for("ufo:protocolRelative");

//#endregion
//#region node_modules/.pnpm/mlly@1.8.0/node_modules/mlly/dist/index.mjs
const BUILTIN_MODULES = new Set(builtinModules);
function normalizeSlash(path) {
	return path.replace(/\\/g, "/");
}
/**
* @typedef ErrnoExceptionFields
* @property {number | undefined} [errnode]
* @property {string | undefined} [code]
* @property {string | undefined} [path]
* @property {string | undefined} [syscall]
* @property {string | undefined} [url]
*
* @typedef {Error & ErrnoExceptionFields} ErrnoException
*/
const own$1 = {}.hasOwnProperty;
const classRegExp = /^([A-Z][a-z\d]*)+$/;
const kTypes = new Set([
	"string",
	"function",
	"number",
	"object",
	"Function",
	"Object",
	"boolean",
	"bigint",
	"symbol"
]);
const codes = {};
/**
* Create a list string in the form like 'A and B' or 'A, B, ..., and Z'.
* We cannot use Intl.ListFormat because it's not available in
* --without-intl builds.
*
* @param {Array<string>} array
*   An array of strings.
* @param {string} [type]
*   The list type to be inserted before the last element.
* @returns {string}
*/
function formatList(array, type = "and") {
	return array.length < 3 ? array.join(` ${type} `) : `${array.slice(0, -1).join(", ")}, ${type} ${array[array.length - 1]}`;
}
/** @type {Map<string, MessageFunction | string>} */
const messages = /* @__PURE__ */ new Map();
const nodeInternalPrefix = "__node_internal_";
/** @type {number} */
let userStackTraceLimit;
codes.ERR_INVALID_ARG_TYPE = createError(
	"ERR_INVALID_ARG_TYPE",
	/**
	* @param {string} name
	* @param {Array<string> | string} expected
	* @param {unknown} actual
	*/
	(name, expected, actual) => {
		assert(typeof name === "string", "'name' must be a string");
		if (!Array.isArray(expected)) expected = [expected];
		let message = "The ";
		if (name.endsWith(" argument")) message += `${name} `;
		else {
			const type = name.includes(".") ? "property" : "argument";
			message += `"${name}" ${type} `;
		}
		message += "must be ";
		/** @type {Array<string>} */
		const types = [];
		/** @type {Array<string>} */
		const instances = [];
		/** @type {Array<string>} */
		const other = [];
		for (const value of expected) {
			assert(typeof value === "string", "All expected entries have to be of type string");
			if (kTypes.has(value)) types.push(value.toLowerCase());
			else if (classRegExp.exec(value) === null) {
				assert(value !== "object", "The value \"object\" should be written as \"Object\"");
				other.push(value);
			} else instances.push(value);
		}
		if (instances.length > 0) {
			const pos = types.indexOf("object");
			if (pos !== -1) {
				types.slice(pos, 1);
				instances.push("Object");
			}
		}
		if (types.length > 0) {
			message += `${types.length > 1 ? "one of type" : "of type"} ${formatList(types, "or")}`;
			if (instances.length > 0 || other.length > 0) message += " or ";
		}
		if (instances.length > 0) {
			message += `an instance of ${formatList(instances, "or")}`;
			if (other.length > 0) message += " or ";
		}
		if (other.length > 0) if (other.length > 1) message += `one of ${formatList(other, "or")}`;
		else {
			if (other[0].toLowerCase() !== other[0]) message += "an ";
			message += `${other[0]}`;
		}
		message += `. Received ${determineSpecificType(actual)}`;
		return message;
	},
	TypeError
);
codes.ERR_INVALID_MODULE_SPECIFIER = createError(
	"ERR_INVALID_MODULE_SPECIFIER",
	/**
	* @param {string} request
	* @param {string} reason
	* @param {string} [base]
	*/
	(request, reason, base = void 0) => {
		return `Invalid module "${request}" ${reason}${base ? ` imported from ${base}` : ""}`;
	},
	TypeError
);
codes.ERR_INVALID_PACKAGE_CONFIG = createError(
	"ERR_INVALID_PACKAGE_CONFIG",
	/**
	* @param {string} path
	* @param {string} [base]
	* @param {string} [message]
	*/
	(path, base, message) => {
		return `Invalid package config ${path}${base ? ` while importing ${base}` : ""}${message ? `. ${message}` : ""}`;
	},
	Error
);
codes.ERR_INVALID_PACKAGE_TARGET = createError(
	"ERR_INVALID_PACKAGE_TARGET",
	/**
	* @param {string} packagePath
	* @param {string} key
	* @param {unknown} target
	* @param {boolean} [isImport=false]
	* @param {string} [base]
	*/
	(packagePath, key, target, isImport = false, base = void 0) => {
		const relatedError = typeof target === "string" && !isImport && target.length > 0 && !target.startsWith("./");
		if (key === ".") {
			assert(isImport === false);
			return `Invalid "exports" main target ${JSON.stringify(target)} defined in the package config ${packagePath}package.json${base ? ` imported from ${base}` : ""}${relatedError ? "; targets must start with \"./\"" : ""}`;
		}
		return `Invalid "${isImport ? "imports" : "exports"}" target ${JSON.stringify(target)} defined for '${key}' in the package config ${packagePath}package.json${base ? ` imported from ${base}` : ""}${relatedError ? "; targets must start with \"./\"" : ""}`;
	},
	Error
);
codes.ERR_MODULE_NOT_FOUND = createError(
	"ERR_MODULE_NOT_FOUND",
	/**
	* @param {string} path
	* @param {string} base
	* @param {boolean} [exactUrl]
	*/
	(path, base, exactUrl = false) => {
		return `Cannot find ${exactUrl ? "module" : "package"} '${path}' imported from ${base}`;
	},
	Error
);
codes.ERR_NETWORK_IMPORT_DISALLOWED = createError("ERR_NETWORK_IMPORT_DISALLOWED", "import of '%s' by %s is not supported: %s", Error);
codes.ERR_PACKAGE_IMPORT_NOT_DEFINED = createError(
	"ERR_PACKAGE_IMPORT_NOT_DEFINED",
	/**
	* @param {string} specifier
	* @param {string} packagePath
	* @param {string} base
	*/
	(specifier, packagePath, base) => {
		return `Package import specifier "${specifier}" is not defined${packagePath ? ` in package ${packagePath}package.json` : ""} imported from ${base}`;
	},
	TypeError
);
codes.ERR_PACKAGE_PATH_NOT_EXPORTED = createError(
	"ERR_PACKAGE_PATH_NOT_EXPORTED",
	/**
	* @param {string} packagePath
	* @param {string} subpath
	* @param {string} [base]
	*/
	(packagePath, subpath, base = void 0) => {
		if (subpath === ".") return `No "exports" main defined in ${packagePath}package.json${base ? ` imported from ${base}` : ""}`;
		return `Package subpath '${subpath}' is not defined by "exports" in ${packagePath}package.json${base ? ` imported from ${base}` : ""}`;
	},
	Error
);
codes.ERR_UNSUPPORTED_DIR_IMPORT = createError("ERR_UNSUPPORTED_DIR_IMPORT", "Directory import '%s' is not supported resolving ES modules imported from %s", Error);
codes.ERR_UNSUPPORTED_RESOLVE_REQUEST = createError("ERR_UNSUPPORTED_RESOLVE_REQUEST", "Failed to resolve module specifier \"%s\" from \"%s\": Invalid relative URL or base scheme is not hierarchical.", TypeError);
codes.ERR_UNKNOWN_FILE_EXTENSION = createError(
	"ERR_UNKNOWN_FILE_EXTENSION",
	/**
	* @param {string} extension
	* @param {string} path
	*/
	(extension, path) => {
		return `Unknown file extension "${extension}" for ${path}`;
	},
	TypeError
);
codes.ERR_INVALID_ARG_VALUE = createError(
	"ERR_INVALID_ARG_VALUE",
	/**
	* @param {string} name
	* @param {unknown} value
	* @param {string} [reason='is invalid']
	*/
	(name, value, reason = "is invalid") => {
		let inspected = inspect(value);
		if (inspected.length > 128) inspected = `${inspected.slice(0, 128)}...`;
		return `The ${name.includes(".") ? "property" : "argument"} '${name}' ${reason}. Received ${inspected}`;
	},
	TypeError
);
/**
* Utility function for registering the error codes. Only used here. Exported
* *only* to allow for testing.
* @param {string} sym
* @param {MessageFunction | string} value
* @param {ErrorConstructor} constructor
* @returns {new (...parameters: Array<any>) => Error}
*/
function createError(sym, value, constructor) {
	messages.set(sym, value);
	return makeNodeErrorWithCode(constructor, sym);
}
/**
* @param {ErrorConstructor} Base
* @param {string} key
* @returns {ErrorConstructor}
*/
function makeNodeErrorWithCode(Base, key) {
	return NodeError;
	/**
	* @param {Array<unknown>} parameters
	*/
	function NodeError(...parameters) {
		const limit = Error.stackTraceLimit;
		if (isErrorStackTraceLimitWritable()) Error.stackTraceLimit = 0;
		const error = new Base();
		if (isErrorStackTraceLimitWritable()) Error.stackTraceLimit = limit;
		const message = getMessage(key, parameters, error);
		Object.defineProperties(error, {
			message: {
				value: message,
				enumerable: false,
				writable: true,
				configurable: true
			},
			toString: {
				value() {
					return `${this.name} [${key}]: ${this.message}`;
				},
				enumerable: false,
				writable: true,
				configurable: true
			}
		});
		captureLargerStackTrace(error);
		error.code = key;
		return error;
	}
}
/**
* @returns {boolean}
*/
function isErrorStackTraceLimitWritable() {
	try {
		if (v8.startupSnapshot.isBuildingSnapshot()) return false;
	} catch {}
	const desc = Object.getOwnPropertyDescriptor(Error, "stackTraceLimit");
	if (desc === void 0) return Object.isExtensible(Error);
	return own$1.call(desc, "writable") && desc.writable !== void 0 ? desc.writable : desc.set !== void 0;
}
/**
* This function removes unnecessary frames from Node.js core errors.
* @template {(...parameters: unknown[]) => unknown} T
* @param {T} wrappedFunction
* @returns {T}
*/
function hideStackFrames(wrappedFunction) {
	const hidden = nodeInternalPrefix + wrappedFunction.name;
	Object.defineProperty(wrappedFunction, "name", { value: hidden });
	return wrappedFunction;
}
const captureLargerStackTrace = hideStackFrames(
	/**
	* @param {Error} error
	* @returns {Error}
	*/
	function(error) {
		const stackTraceLimitIsWritable = isErrorStackTraceLimitWritable();
		if (stackTraceLimitIsWritable) {
			userStackTraceLimit = Error.stackTraceLimit;
			Error.stackTraceLimit = Number.POSITIVE_INFINITY;
		}
		Error.captureStackTrace(error);
		if (stackTraceLimitIsWritable) Error.stackTraceLimit = userStackTraceLimit;
		return error;
	}
);
/**
* @param {string} key
* @param {Array<unknown>} parameters
* @param {Error} self
* @returns {string}
*/
function getMessage(key, parameters, self) {
	const message = messages.get(key);
	assert(message !== void 0, "expected `message` to be found");
	if (typeof message === "function") {
		assert(message.length <= parameters.length, `Code: ${key}; The provided arguments length (${parameters.length}) does not match the required ones (${message.length}).`);
		return Reflect.apply(message, self, parameters);
	}
	const regex = /%[dfijoOs]/g;
	let expectedLength = 0;
	while (regex.exec(message) !== null) expectedLength++;
	assert(expectedLength === parameters.length, `Code: ${key}; The provided arguments length (${parameters.length}) does not match the required ones (${expectedLength}).`);
	if (parameters.length === 0) return message;
	parameters.unshift(message);
	return Reflect.apply(format, null, parameters);
}
/**
* Determine the specific type of a value for type-mismatch errors.
* @param {unknown} value
* @returns {string}
*/
function determineSpecificType(value) {
	if (value === null || value === void 0) return String(value);
	if (typeof value === "function" && value.name) return `function ${value.name}`;
	if (typeof value === "object") {
		if (value.constructor && value.constructor.name) return `an instance of ${value.constructor.name}`;
		return `${inspect(value, { depth: -1 })}`;
	}
	let inspected = inspect(value, { colors: false });
	if (inspected.length > 28) inspected = `${inspected.slice(0, 25)}...`;
	return `type ${typeof value} (${inspected})`;
}
const hasOwnProperty$1 = {}.hasOwnProperty;
const { ERR_INVALID_PACKAGE_CONFIG: ERR_INVALID_PACKAGE_CONFIG$1 } = codes;
/** @type {Map<string, PackageConfig>} */
const cache = /* @__PURE__ */ new Map();
/**
* @param {string} jsonPath
* @param {{specifier: URL | string, base?: URL}} options
* @returns {PackageConfig}
*/
function read(jsonPath, { base, specifier }) {
	const existing = cache.get(jsonPath);
	if (existing) return existing;
	/** @type {string | undefined} */
	let string;
	try {
		string = fs.readFileSync(path.toNamespacedPath(jsonPath), "utf8");
	} catch (error) {
		const exception = error;
		if (exception.code !== "ENOENT") throw exception;
	}
	/** @type {PackageConfig} */
	const result = {
		exists: false,
		pjsonPath: jsonPath,
		main: void 0,
		name: void 0,
		type: "none",
		exports: void 0,
		imports: void 0
	};
	if (string !== void 0) {
		/** @type {Record<string, unknown>} */
		let parsed;
		try {
			parsed = JSON.parse(string);
		} catch (error_) {
			const cause = error_;
			const error = new ERR_INVALID_PACKAGE_CONFIG$1(jsonPath, (base ? `"${specifier}" from ` : "") + fileURLToPath(base || specifier), cause.message);
			error.cause = cause;
			throw error;
		}
		result.exists = true;
		if (hasOwnProperty$1.call(parsed, "name") && typeof parsed.name === "string") result.name = parsed.name;
		if (hasOwnProperty$1.call(parsed, "main") && typeof parsed.main === "string") result.main = parsed.main;
		if (hasOwnProperty$1.call(parsed, "exports")) result.exports = parsed.exports;
		if (hasOwnProperty$1.call(parsed, "imports")) result.imports = parsed.imports;
		if (hasOwnProperty$1.call(parsed, "type") && (parsed.type === "commonjs" || parsed.type === "module")) result.type = parsed.type;
	}
	cache.set(jsonPath, result);
	return result;
}
/**
* @param {URL | string} resolved
* @returns {PackageConfig}
*/
function getPackageScopeConfig(resolved) {
	let packageJSONUrl = new URL("package.json", resolved);
	while (true) {
		if (packageJSONUrl.pathname.endsWith("node_modules/package.json")) break;
		const packageConfig = read(fileURLToPath(packageJSONUrl), { specifier: resolved });
		if (packageConfig.exists) return packageConfig;
		const lastPackageJSONUrl = packageJSONUrl;
		packageJSONUrl = new URL("../package.json", packageJSONUrl);
		if (packageJSONUrl.pathname === lastPackageJSONUrl.pathname) break;
	}
	return {
		pjsonPath: fileURLToPath(packageJSONUrl),
		exists: false,
		type: "none"
	};
}
/**
* Returns the package type for a given URL.
* @param {URL} url - The URL to get the package type for.
* @returns {PackageType}
*/
function getPackageType(url) {
	return getPackageScopeConfig(url).type;
}
const { ERR_UNKNOWN_FILE_EXTENSION } = codes;
const hasOwnProperty = {}.hasOwnProperty;
/** @type {Record<string, string>} */
const extensionFormatMap = {
	__proto__: null,
	".cjs": "commonjs",
	".js": "module",
	".json": "json",
	".mjs": "module"
};
/**
* @param {string | null} mime
* @returns {string | null}
*/
function mimeToFormat(mime) {
	if (mime && /\s*(text|application)\/javascript\s*(;\s*charset=utf-?8\s*)?/i.test(mime)) return "module";
	if (mime === "application/json") return "json";
	return null;
}
/**
* @callback ProtocolHandler
* @param {URL} parsed
* @param {{parentURL: string, source?: Buffer}} context
* @param {boolean} ignoreErrors
* @returns {string | null | void}
*/
/**
* @type {Record<string, ProtocolHandler>}
*/
const protocolHandlers = {
	__proto__: null,
	"data:": getDataProtocolModuleFormat,
	"file:": getFileProtocolModuleFormat,
	"http:": getHttpProtocolModuleFormat,
	"https:": getHttpProtocolModuleFormat,
	"node:"() {
		return "builtin";
	}
};
/**
* @param {URL} parsed
*/
function getDataProtocolModuleFormat(parsed) {
	const { 1: mime } = /^([^/]+\/[^;,]+)[^,]*?(;base64)?,/.exec(parsed.pathname) || [
		null,
		null,
		null
	];
	return mimeToFormat(mime);
}
/**
* Returns the file extension from a URL.
*
* Should give similar result to
* `require('node:path').extname(require('node:url').fileURLToPath(url))`
* when used with a `file:` URL.
*
* @param {URL} url
* @returns {string}
*/
function extname$2(url) {
	const pathname = url.pathname;
	let index = pathname.length;
	while (index--) {
		const code = pathname.codePointAt(index);
		if (code === 47) return "";
		if (code === 46) return pathname.codePointAt(index - 1) === 47 ? "" : pathname.slice(index);
	}
	return "";
}
/**
* @type {ProtocolHandler}
*/
function getFileProtocolModuleFormat(url, _context, ignoreErrors) {
	const value = extname$2(url);
	if (value === ".js") {
		const packageType = getPackageType(url);
		if (packageType !== "none") return packageType;
		return "commonjs";
	}
	if (value === "") {
		const packageType = getPackageType(url);
		if (packageType === "none" || packageType === "commonjs") return "commonjs";
		return "module";
	}
	const format = extensionFormatMap[value];
	if (format) return format;
	if (ignoreErrors) return;
	throw new ERR_UNKNOWN_FILE_EXTENSION(value, fileURLToPath(url));
}
function getHttpProtocolModuleFormat() {}
/**
* @param {URL} url
* @param {{parentURL: string}} context
* @returns {string | null}
*/
function defaultGetFormatWithoutErrors(url, context) {
	const protocol = url.protocol;
	if (!hasOwnProperty.call(protocolHandlers, protocol)) return null;
	return protocolHandlers[protocol](url, context, true) || null;
}
const RegExpPrototypeSymbolReplace = RegExp.prototype[Symbol.replace];
const { ERR_INVALID_MODULE_SPECIFIER, ERR_INVALID_PACKAGE_CONFIG, ERR_INVALID_PACKAGE_TARGET, ERR_MODULE_NOT_FOUND, ERR_PACKAGE_IMPORT_NOT_DEFINED, ERR_PACKAGE_PATH_NOT_EXPORTED, ERR_UNSUPPORTED_DIR_IMPORT, ERR_UNSUPPORTED_RESOLVE_REQUEST } = codes;
const own = {}.hasOwnProperty;
const invalidSegmentRegEx = /(^|\\|\/)((\.|%2e)(\.|%2e)?|(n|%6e|%4e)(o|%6f|%4f)(d|%64|%44)(e|%65|%45)(_|%5f)(m|%6d|%4d)(o|%6f|%4f)(d|%64|%44)(u|%75|%55)(l|%6c|%4c)(e|%65|%45)(s|%73|%53))?(\\|\/|$)/i;
const deprecatedInvalidSegmentRegEx = /(^|\\|\/)((\.|%2e)(\.|%2e)?|(n|%6e|%4e)(o|%6f|%4f)(d|%64|%44)(e|%65|%45)(_|%5f)(m|%6d|%4d)(o|%6f|%4f)(d|%64|%44)(u|%75|%55)(l|%6c|%4c)(e|%65|%45)(s|%73|%53))(\\|\/|$)/i;
const invalidPackageNameRegEx = /^\.|%|\\/;
const patternRegEx = /\*/g;
const encodedSeparatorRegEx = /%2f|%5c/i;
/** @type {Set<string>} */
const emittedPackageWarnings = /* @__PURE__ */ new Set();
const doubleSlashRegEx = /[/\\]{2}/;
/**
*
* @param {string} target
* @param {string} request
* @param {string} match
* @param {URL} packageJsonUrl
* @param {boolean} internal
* @param {URL} base
* @param {boolean} isTarget
*/
function emitInvalidSegmentDeprecation(target, request, match, packageJsonUrl, internal, base, isTarget) {
	if (process$1.noDeprecation) return;
	const pjsonPath = fileURLToPath(packageJsonUrl);
	const double = doubleSlashRegEx.exec(isTarget ? target : request) !== null;
	process$1.emitWarning(`Use of deprecated ${double ? "double slash" : "leading or trailing slash matching"} resolving "${target}" for module request "${request}" ${request === match ? "" : `matched to "${match}" `}in the "${internal ? "imports" : "exports"}" field module resolution of the package at ${pjsonPath}${base ? ` imported from ${fileURLToPath(base)}` : ""}.`, "DeprecationWarning", "DEP0166");
}
/**
* @param {URL} url
* @param {URL} packageJsonUrl
* @param {URL} base
* @param {string} [main]
* @returns {void}
*/
function emitLegacyIndexDeprecation(url, packageJsonUrl, base, main) {
	if (process$1.noDeprecation) return;
	if (defaultGetFormatWithoutErrors(url, { parentURL: base.href }) !== "module") return;
	const urlPath = fileURLToPath(url.href);
	const packagePath = fileURLToPath(new URL$1(".", packageJsonUrl));
	const basePath = fileURLToPath(base);
	if (!main) process$1.emitWarning(`No "main" or "exports" field defined in the package.json for ${packagePath} resolving the main entry point "${urlPath.slice(packagePath.length)}", imported from ${basePath}.\nDefault "index" lookups for the main are deprecated for ES modules.`, "DeprecationWarning", "DEP0151");
	else if (path.resolve(packagePath, main) !== urlPath) process$1.emitWarning(`Package ${packagePath} has a "main" field set to "${main}", excluding the full filename and extension to the resolved file at "${urlPath.slice(packagePath.length)}", imported from ${basePath}.\n Automatic extension resolution of the "main" field is deprecated for ES modules.`, "DeprecationWarning", "DEP0151");
}
/**
* @param {string} path
* @returns {Stats | undefined}
*/
function tryStatSync(path) {
	try {
		return statSync(path);
	} catch {}
}
/**
* Legacy CommonJS main resolution:
* 1. let M = pkg_url + (json main field)
* 2. TRY(M, M.js, M.json, M.node)
* 3. TRY(M/index.js, M/index.json, M/index.node)
* 4. TRY(pkg_url/index.js, pkg_url/index.json, pkg_url/index.node)
* 5. NOT_FOUND
*
* @param {URL} url
* @returns {boolean}
*/
function fileExists(url) {
	const stats = statSync(url, { throwIfNoEntry: false });
	const isFile = stats ? stats.isFile() : void 0;
	return isFile === null || isFile === void 0 ? false : isFile;
}
/**
* @param {URL} packageJsonUrl
* @param {PackageConfig} packageConfig
* @param {URL} base
* @returns {URL}
*/
function legacyMainResolve(packageJsonUrl, packageConfig, base) {
	/** @type {URL | undefined} */
	let guess;
	if (packageConfig.main !== void 0) {
		guess = new URL$1(packageConfig.main, packageJsonUrl);
		if (fileExists(guess)) return guess;
		const tries = [
			`./${packageConfig.main}.js`,
			`./${packageConfig.main}.json`,
			`./${packageConfig.main}.node`,
			`./${packageConfig.main}/index.js`,
			`./${packageConfig.main}/index.json`,
			`./${packageConfig.main}/index.node`
		];
		let i = -1;
		while (++i < tries.length) {
			guess = new URL$1(tries[i], packageJsonUrl);
			if (fileExists(guess)) break;
			guess = void 0;
		}
		if (guess) {
			emitLegacyIndexDeprecation(guess, packageJsonUrl, base, packageConfig.main);
			return guess;
		}
	}
	const tries = [
		"./index.js",
		"./index.json",
		"./index.node"
	];
	let i = -1;
	while (++i < tries.length) {
		guess = new URL$1(tries[i], packageJsonUrl);
		if (fileExists(guess)) break;
		guess = void 0;
	}
	if (guess) {
		emitLegacyIndexDeprecation(guess, packageJsonUrl, base, packageConfig.main);
		return guess;
	}
	throw new ERR_MODULE_NOT_FOUND(fileURLToPath(new URL$1(".", packageJsonUrl)), fileURLToPath(base));
}
/**
* @param {URL} resolved
* @param {URL} base
* @param {boolean} [preserveSymlinks]
* @returns {URL}
*/
function finalizeResolution(resolved, base, preserveSymlinks) {
	if (encodedSeparatorRegEx.exec(resolved.pathname) !== null) throw new ERR_INVALID_MODULE_SPECIFIER(resolved.pathname, "must not include encoded \"/\" or \"\\\" characters", fileURLToPath(base));
	/** @type {string} */
	let filePath;
	try {
		filePath = fileURLToPath(resolved);
	} catch (error) {
		const cause = error;
		Object.defineProperty(cause, "input", { value: String(resolved) });
		Object.defineProperty(cause, "module", { value: String(base) });
		throw cause;
	}
	const stats = tryStatSync(filePath.endsWith("/") ? filePath.slice(-1) : filePath);
	if (stats && stats.isDirectory()) {
		const error = new ERR_UNSUPPORTED_DIR_IMPORT(filePath, fileURLToPath(base));
		error.url = String(resolved);
		throw error;
	}
	if (!stats || !stats.isFile()) {
		const error = new ERR_MODULE_NOT_FOUND(filePath || resolved.pathname, base && fileURLToPath(base), true);
		error.url = String(resolved);
		throw error;
	}
	{
		const real = realpathSync(filePath);
		const { search, hash } = resolved;
		resolved = pathToFileURL(real + (filePath.endsWith(path.sep) ? "/" : ""));
		resolved.search = search;
		resolved.hash = hash;
	}
	return resolved;
}
/**
* @param {string} specifier
* @param {URL | undefined} packageJsonUrl
* @param {URL} base
* @returns {Error}
*/
function importNotDefined(specifier, packageJsonUrl, base) {
	return new ERR_PACKAGE_IMPORT_NOT_DEFINED(specifier, packageJsonUrl && fileURLToPath(new URL$1(".", packageJsonUrl)), fileURLToPath(base));
}
/**
* @param {string} subpath
* @param {URL} packageJsonUrl
* @param {URL} base
* @returns {Error}
*/
function exportsNotFound(subpath, packageJsonUrl, base) {
	return new ERR_PACKAGE_PATH_NOT_EXPORTED(fileURLToPath(new URL$1(".", packageJsonUrl)), subpath, base && fileURLToPath(base));
}
/**
* @param {string} request
* @param {string} match
* @param {URL} packageJsonUrl
* @param {boolean} internal
* @param {URL} [base]
* @returns {never}
*/
function throwInvalidSubpath(request, match, packageJsonUrl, internal, base) {
	throw new ERR_INVALID_MODULE_SPECIFIER(request, `request is not a valid match in pattern "${match}" for the "${internal ? "imports" : "exports"}" resolution of ${fileURLToPath(packageJsonUrl)}`, base && fileURLToPath(base));
}
/**
* @param {string} subpath
* @param {unknown} target
* @param {URL} packageJsonUrl
* @param {boolean} internal
* @param {URL} [base]
* @returns {Error}
*/
function invalidPackageTarget(subpath, target, packageJsonUrl, internal, base) {
	target = typeof target === "object" && target !== null ? JSON.stringify(target, null, "") : `${target}`;
	return new ERR_INVALID_PACKAGE_TARGET(fileURLToPath(new URL$1(".", packageJsonUrl)), subpath, target, internal, base && fileURLToPath(base));
}
/**
* @param {string} target
* @param {string} subpath
* @param {string} match
* @param {URL} packageJsonUrl
* @param {URL} base
* @param {boolean} pattern
* @param {boolean} internal
* @param {boolean} isPathMap
* @param {Set<string> | undefined} conditions
* @returns {URL}
*/
function resolvePackageTargetString(target, subpath, match, packageJsonUrl, base, pattern, internal, isPathMap, conditions) {
	if (subpath !== "" && !pattern && target[target.length - 1] !== "/") throw invalidPackageTarget(match, target, packageJsonUrl, internal, base);
	if (!target.startsWith("./")) {
		if (internal && !target.startsWith("../") && !target.startsWith("/")) {
			let isURL = false;
			try {
				new URL$1(target);
				isURL = true;
			} catch {}
			if (!isURL) return packageResolve(pattern ? RegExpPrototypeSymbolReplace.call(patternRegEx, target, () => subpath) : target + subpath, packageJsonUrl, conditions);
		}
		throw invalidPackageTarget(match, target, packageJsonUrl, internal, base);
	}
	if (invalidSegmentRegEx.exec(target.slice(2)) !== null) if (deprecatedInvalidSegmentRegEx.exec(target.slice(2)) === null) {
		if (!isPathMap) {
			const request = pattern ? match.replace("*", () => subpath) : match + subpath;
			emitInvalidSegmentDeprecation(pattern ? RegExpPrototypeSymbolReplace.call(patternRegEx, target, () => subpath) : target, request, match, packageJsonUrl, internal, base, true);
		}
	} else throw invalidPackageTarget(match, target, packageJsonUrl, internal, base);
	const resolved = new URL$1(target, packageJsonUrl);
	const resolvedPath = resolved.pathname;
	const packagePath = new URL$1(".", packageJsonUrl).pathname;
	if (!resolvedPath.startsWith(packagePath)) throw invalidPackageTarget(match, target, packageJsonUrl, internal, base);
	if (subpath === "") return resolved;
	if (invalidSegmentRegEx.exec(subpath) !== null) {
		const request = pattern ? match.replace("*", () => subpath) : match + subpath;
		if (deprecatedInvalidSegmentRegEx.exec(subpath) === null) {
			if (!isPathMap) emitInvalidSegmentDeprecation(pattern ? RegExpPrototypeSymbolReplace.call(patternRegEx, target, () => subpath) : target, request, match, packageJsonUrl, internal, base, false);
		} else throwInvalidSubpath(request, match, packageJsonUrl, internal, base);
	}
	if (pattern) return new URL$1(RegExpPrototypeSymbolReplace.call(patternRegEx, resolved.href, () => subpath));
	return new URL$1(subpath, resolved);
}
/**
* @param {string} key
* @returns {boolean}
*/
function isArrayIndex(key) {
	const keyNumber = Number(key);
	if (`${keyNumber}` !== key) return false;
	return keyNumber >= 0 && keyNumber < 4294967295;
}
/**
* @param {URL} packageJsonUrl
* @param {unknown} target
* @param {string} subpath
* @param {string} packageSubpath
* @param {URL} base
* @param {boolean} pattern
* @param {boolean} internal
* @param {boolean} isPathMap
* @param {Set<string> | undefined} conditions
* @returns {URL | null}
*/
function resolvePackageTarget(packageJsonUrl, target, subpath, packageSubpath, base, pattern, internal, isPathMap, conditions) {
	if (typeof target === "string") return resolvePackageTargetString(target, subpath, packageSubpath, packageJsonUrl, base, pattern, internal, isPathMap, conditions);
	if (Array.isArray(target)) {
		/** @type {Array<unknown>} */
		const targetList = target;
		if (targetList.length === 0) return null;
		/** @type {ErrnoException | null | undefined} */
		let lastException;
		let i = -1;
		while (++i < targetList.length) {
			const targetItem = targetList[i];
			/** @type {URL | null} */
			let resolveResult;
			try {
				resolveResult = resolvePackageTarget(packageJsonUrl, targetItem, subpath, packageSubpath, base, pattern, internal, isPathMap, conditions);
			} catch (error) {
				const exception = error;
				lastException = exception;
				if (exception.code === "ERR_INVALID_PACKAGE_TARGET") continue;
				throw error;
			}
			if (resolveResult === void 0) continue;
			if (resolveResult === null) {
				lastException = null;
				continue;
			}
			return resolveResult;
		}
		if (lastException === void 0 || lastException === null) return null;
		throw lastException;
	}
	if (typeof target === "object" && target !== null) {
		const keys = Object.getOwnPropertyNames(target);
		let i = -1;
		while (++i < keys.length) {
			const key = keys[i];
			if (isArrayIndex(key)) throw new ERR_INVALID_PACKAGE_CONFIG(fileURLToPath(packageJsonUrl), base, "\"exports\" cannot contain numeric property keys.");
		}
		i = -1;
		while (++i < keys.length) {
			const key = keys[i];
			if (key === "default" || conditions && conditions.has(key)) {
				const conditionalTarget = target[key];
				const resolveResult = resolvePackageTarget(packageJsonUrl, conditionalTarget, subpath, packageSubpath, base, pattern, internal, isPathMap, conditions);
				if (resolveResult === void 0) continue;
				return resolveResult;
			}
		}
		return null;
	}
	if (target === null) return null;
	throw invalidPackageTarget(packageSubpath, target, packageJsonUrl, internal, base);
}
/**
* @param {unknown} exports
* @param {URL} packageJsonUrl
* @param {URL} base
* @returns {boolean}
*/
function isConditionalExportsMainSugar(exports, packageJsonUrl, base) {
	if (typeof exports === "string" || Array.isArray(exports)) return true;
	if (typeof exports !== "object" || exports === null) return false;
	const keys = Object.getOwnPropertyNames(exports);
	let isConditionalSugar = false;
	let i = 0;
	let keyIndex = -1;
	while (++keyIndex < keys.length) {
		const key = keys[keyIndex];
		const currentIsConditionalSugar = key === "" || key[0] !== ".";
		if (i++ === 0) isConditionalSugar = currentIsConditionalSugar;
		else if (isConditionalSugar !== currentIsConditionalSugar) throw new ERR_INVALID_PACKAGE_CONFIG(fileURLToPath(packageJsonUrl), base, "\"exports\" cannot contain some keys starting with '.' and some not. The exports object must either be an object of package subpath keys or an object of main entry condition name keys only.");
	}
	return isConditionalSugar;
}
/**
* @param {string} match
* @param {URL} pjsonUrl
* @param {URL} base
*/
function emitTrailingSlashPatternDeprecation(match, pjsonUrl, base) {
	if (process$1.noDeprecation) return;
	const pjsonPath = fileURLToPath(pjsonUrl);
	if (emittedPackageWarnings.has(pjsonPath + "|" + match)) return;
	emittedPackageWarnings.add(pjsonPath + "|" + match);
	process$1.emitWarning(`Use of deprecated trailing slash pattern mapping "${match}" in the "exports" field module resolution of the package at ${pjsonPath}${base ? ` imported from ${fileURLToPath(base)}` : ""}. Mapping specifiers ending in "/" is no longer supported.`, "DeprecationWarning", "DEP0155");
}
/**
* @param {URL} packageJsonUrl
* @param {string} packageSubpath
* @param {Record<string, unknown>} packageConfig
* @param {URL} base
* @param {Set<string> | undefined} conditions
* @returns {URL}
*/
function packageExportsResolve(packageJsonUrl, packageSubpath, packageConfig, base, conditions) {
	let exports = packageConfig.exports;
	if (isConditionalExportsMainSugar(exports, packageJsonUrl, base)) exports = { ".": exports };
	if (own.call(exports, packageSubpath) && !packageSubpath.includes("*") && !packageSubpath.endsWith("/")) {
		const target = exports[packageSubpath];
		const resolveResult = resolvePackageTarget(packageJsonUrl, target, "", packageSubpath, base, false, false, false, conditions);
		if (resolveResult === null || resolveResult === void 0) throw exportsNotFound(packageSubpath, packageJsonUrl, base);
		return resolveResult;
	}
	let bestMatch = "";
	let bestMatchSubpath = "";
	const keys = Object.getOwnPropertyNames(exports);
	let i = -1;
	while (++i < keys.length) {
		const key = keys[i];
		const patternIndex = key.indexOf("*");
		if (patternIndex !== -1 && packageSubpath.startsWith(key.slice(0, patternIndex))) {
			if (packageSubpath.endsWith("/")) emitTrailingSlashPatternDeprecation(packageSubpath, packageJsonUrl, base);
			const patternTrailer = key.slice(patternIndex + 1);
			if (packageSubpath.length >= key.length && packageSubpath.endsWith(patternTrailer) && patternKeyCompare(bestMatch, key) === 1 && key.lastIndexOf("*") === patternIndex) {
				bestMatch = key;
				bestMatchSubpath = packageSubpath.slice(patternIndex, packageSubpath.length - patternTrailer.length);
			}
		}
	}
	if (bestMatch) {
		const target = exports[bestMatch];
		const resolveResult = resolvePackageTarget(packageJsonUrl, target, bestMatchSubpath, bestMatch, base, true, false, packageSubpath.endsWith("/"), conditions);
		if (resolveResult === null || resolveResult === void 0) throw exportsNotFound(packageSubpath, packageJsonUrl, base);
		return resolveResult;
	}
	throw exportsNotFound(packageSubpath, packageJsonUrl, base);
}
/**
* @param {string} a
* @param {string} b
*/
function patternKeyCompare(a, b) {
	const aPatternIndex = a.indexOf("*");
	const bPatternIndex = b.indexOf("*");
	const baseLengthA = aPatternIndex === -1 ? a.length : aPatternIndex + 1;
	const baseLengthB = bPatternIndex === -1 ? b.length : bPatternIndex + 1;
	if (baseLengthA > baseLengthB) return -1;
	if (baseLengthB > baseLengthA) return 1;
	if (aPatternIndex === -1) return 1;
	if (bPatternIndex === -1) return -1;
	if (a.length > b.length) return -1;
	if (b.length > a.length) return 1;
	return 0;
}
/**
* @param {string} name
* @param {URL} base
* @param {Set<string>} [conditions]
* @returns {URL}
*/
function packageImportsResolve(name, base, conditions) {
	if (name === "#" || name.startsWith("#/") || name.endsWith("/")) throw new ERR_INVALID_MODULE_SPECIFIER(name, "is not a valid internal imports specifier name", fileURLToPath(base));
	/** @type {URL | undefined} */
	let packageJsonUrl;
	const packageConfig = getPackageScopeConfig(base);
	if (packageConfig.exists) {
		packageJsonUrl = pathToFileURL(packageConfig.pjsonPath);
		const imports = packageConfig.imports;
		if (imports) if (own.call(imports, name) && !name.includes("*")) {
			const resolveResult = resolvePackageTarget(packageJsonUrl, imports[name], "", name, base, false, true, false, conditions);
			if (resolveResult !== null && resolveResult !== void 0) return resolveResult;
		} else {
			let bestMatch = "";
			let bestMatchSubpath = "";
			const keys = Object.getOwnPropertyNames(imports);
			let i = -1;
			while (++i < keys.length) {
				const key = keys[i];
				const patternIndex = key.indexOf("*");
				if (patternIndex !== -1 && name.startsWith(key.slice(0, -1))) {
					const patternTrailer = key.slice(patternIndex + 1);
					if (name.length >= key.length && name.endsWith(patternTrailer) && patternKeyCompare(bestMatch, key) === 1 && key.lastIndexOf("*") === patternIndex) {
						bestMatch = key;
						bestMatchSubpath = name.slice(patternIndex, name.length - patternTrailer.length);
					}
				}
			}
			if (bestMatch) {
				const target = imports[bestMatch];
				const resolveResult = resolvePackageTarget(packageJsonUrl, target, bestMatchSubpath, bestMatch, base, true, true, false, conditions);
				if (resolveResult !== null && resolveResult !== void 0) return resolveResult;
			}
		}
	}
	throw importNotDefined(name, packageJsonUrl, base);
}
/**
* @param {string} specifier
* @param {URL} base
*/
function parsePackageName(specifier, base) {
	let separatorIndex = specifier.indexOf("/");
	let validPackageName = true;
	let isScoped = false;
	if (specifier[0] === "@") {
		isScoped = true;
		if (separatorIndex === -1 || specifier.length === 0) validPackageName = false;
		else separatorIndex = specifier.indexOf("/", separatorIndex + 1);
	}
	const packageName = separatorIndex === -1 ? specifier : specifier.slice(0, separatorIndex);
	if (invalidPackageNameRegEx.exec(packageName) !== null) validPackageName = false;
	if (!validPackageName) throw new ERR_INVALID_MODULE_SPECIFIER(specifier, "is not a valid package name", fileURLToPath(base));
	return {
		packageName,
		packageSubpath: "." + (separatorIndex === -1 ? "" : specifier.slice(separatorIndex)),
		isScoped
	};
}
/**
* @param {string} specifier
* @param {URL} base
* @param {Set<string> | undefined} conditions
* @returns {URL}
*/
function packageResolve(specifier, base, conditions) {
	if (builtinModules.includes(specifier)) return new URL$1("node:" + specifier);
	const { packageName, packageSubpath, isScoped } = parsePackageName(specifier, base);
	const packageConfig = getPackageScopeConfig(base);
	/* c8 ignore next 16 */
	if (packageConfig.exists) {
		const packageJsonUrl = pathToFileURL(packageConfig.pjsonPath);
		if (packageConfig.name === packageName && packageConfig.exports !== void 0 && packageConfig.exports !== null) return packageExportsResolve(packageJsonUrl, packageSubpath, packageConfig, base, conditions);
	}
	let packageJsonUrl = new URL$1("./node_modules/" + packageName + "/package.json", base);
	let packageJsonPath = fileURLToPath(packageJsonUrl);
	/** @type {string} */
	let lastPath;
	do {
		const stat = tryStatSync(packageJsonPath.slice(0, -13));
		if (!stat || !stat.isDirectory()) {
			lastPath = packageJsonPath;
			packageJsonUrl = new URL$1((isScoped ? "../../../../node_modules/" : "../../../node_modules/") + packageName + "/package.json", packageJsonUrl);
			packageJsonPath = fileURLToPath(packageJsonUrl);
			continue;
		}
		const packageConfig = read(packageJsonPath, {
			base,
			specifier
		});
		if (packageConfig.exports !== void 0 && packageConfig.exports !== null) return packageExportsResolve(packageJsonUrl, packageSubpath, packageConfig, base, conditions);
		if (packageSubpath === ".") return legacyMainResolve(packageJsonUrl, packageConfig, base);
		return new URL$1(packageSubpath, packageJsonUrl);
	} while (packageJsonPath.length !== lastPath.length);
	throw new ERR_MODULE_NOT_FOUND(packageName, fileURLToPath(base), false);
}
/**
* @param {string} specifier
* @returns {boolean}
*/
function isRelativeSpecifier(specifier) {
	if (specifier[0] === ".") {
		if (specifier.length === 1 || specifier[1] === "/") return true;
		if (specifier[1] === "." && (specifier.length === 2 || specifier[2] === "/")) return true;
	}
	return false;
}
/**
* @param {string} specifier
* @returns {boolean}
*/
function shouldBeTreatedAsRelativeOrAbsolutePath(specifier) {
	if (specifier === "") return false;
	if (specifier[0] === "/") return true;
	return isRelativeSpecifier(specifier);
}
/**
* The “Resolver Algorithm Specification” as detailed in the Node docs (which is
* sync and slightly lower-level than `resolve`).
*
* @param {string} specifier
*   `/example.js`, `./example.js`, `../example.js`, `some-package`, `fs`, etc.
* @param {URL} base
*   Full URL (to a file) that `specifier` is resolved relative from.
* @param {Set<string>} [conditions]
*   Conditions.
* @param {boolean} [preserveSymlinks]
*   Keep symlinks instead of resolving them.
* @returns {URL}
*   A URL object to the found thing.
*/
function moduleResolve(specifier, base, conditions, preserveSymlinks) {
	const protocol = base.protocol;
	const isRemote = protocol === "data:" || protocol === "http:" || protocol === "https:";
	/** @type {URL | undefined} */
	let resolved;
	if (shouldBeTreatedAsRelativeOrAbsolutePath(specifier)) try {
		resolved = new URL$1(specifier, base);
	} catch (error_) {
		const error = new ERR_UNSUPPORTED_RESOLVE_REQUEST(specifier, base);
		error.cause = error_;
		throw error;
	}
	else if (protocol === "file:" && specifier[0] === "#") resolved = packageImportsResolve(specifier, base, conditions);
	else try {
		resolved = new URL$1(specifier);
	} catch (error_) {
		if (isRemote && !builtinModules.includes(specifier)) {
			const error = new ERR_UNSUPPORTED_RESOLVE_REQUEST(specifier, base);
			error.cause = error_;
			throw error;
		}
		resolved = packageResolve(specifier, base, conditions);
	}
	assert(resolved !== void 0, "expected to be defined");
	if (resolved.protocol !== "file:") return resolved;
	return finalizeResolution(resolved, base);
}
function fileURLToPath$1(id) {
	if (typeof id === "string" && !id.startsWith("file://")) return normalizeSlash(id);
	return normalizeSlash(fileURLToPath(id));
}
function pathToFileURL$1(id) {
	return pathToFileURL(fileURLToPath$1(id)).toString();
}
function normalizeid(id) {
	if (typeof id !== "string") id = id.toString();
	if (/(?:node|data|http|https|file):/.test(id)) return id;
	if (BUILTIN_MODULES.has(id)) return "node:" + id;
	return "file://" + encodeURI(normalizeSlash(id));
}
const DEFAULT_CONDITIONS_SET = /* @__PURE__ */ new Set(["node", "import"]);
const DEFAULT_EXTENSIONS = [
	".mjs",
	".cjs",
	".js",
	".json"
];
const NOT_FOUND_ERRORS = /* @__PURE__ */ new Set([
	"ERR_MODULE_NOT_FOUND",
	"ERR_UNSUPPORTED_DIR_IMPORT",
	"MODULE_NOT_FOUND",
	"ERR_PACKAGE_PATH_NOT_EXPORTED"
]);
function _tryModuleResolve(id, url, conditions) {
	try {
		return moduleResolve(id, url, conditions);
	} catch (error) {
		if (!NOT_FOUND_ERRORS.has(error?.code)) throw error;
	}
}
function _resolve(id, options = {}) {
	if (typeof id !== "string") if (id instanceof URL) id = fileURLToPath$1(id);
	else throw new TypeError("input must be a `string` or `URL`");
	if (/(?:node|data|http|https):/.test(id)) return id;
	if (BUILTIN_MODULES.has(id)) return "node:" + id;
	if (id.startsWith("file://")) id = fileURLToPath$1(id);
	if (isAbsolute$2(id)) try {
		if (statSync(id).isFile()) return pathToFileURL$1(id);
	} catch (error) {
		if (error?.code !== "ENOENT") throw error;
	}
	const conditionsSet = options.conditions ? new Set(options.conditions) : DEFAULT_CONDITIONS_SET;
	const _urls = (Array.isArray(options.url) ? options.url : [options.url]).filter(Boolean).map((url) => new URL(normalizeid(url.toString())));
	if (_urls.length === 0) _urls.push(new URL(pathToFileURL$1(process.cwd())));
	const urls = [..._urls];
	for (const url of _urls) if (url.protocol === "file:") urls.push(new URL("./", url), new URL(joinURL(url.pathname, "_index.js"), url), new URL("node_modules", url));
	let resolved;
	for (const url of urls) {
		resolved = _tryModuleResolve(id, url, conditionsSet);
		if (resolved) break;
		for (const prefix of ["", "/index"]) {
			for (const extension of options.extensions || DEFAULT_EXTENSIONS) {
				resolved = _tryModuleResolve(joinURL(id, prefix) + extension, url, conditionsSet);
				if (resolved) break;
			}
			if (resolved) break;
		}
		if (resolved) break;
	}
	if (!resolved) {
		const error = /* @__PURE__ */ new Error(`Cannot find module ${id} imported from ${urls.join(", ")}`);
		error.code = "ERR_MODULE_NOT_FOUND";
		throw error;
	}
	return pathToFileURL$1(resolved);
}
function resolveSync(id, options) {
	return _resolve(id, options);
}
function resolve$2(id, options) {
	try {
		return Promise.resolve(resolveSync(id, options));
	} catch (error) {
		return Promise.reject(error);
	}
}

//#endregion
//#region node_modules/.pnpm/@eslint+config-array@0.23.2_patch_hash=9c56839266cb75a04e2a96a342456c69afd7549bf6c13a9ade49cc6d42de892a/node_modules/@eslint/config-array/dist/esm/std__path/posix.js
var posix_exports = /* @__PURE__ */ __exportAll({
	DELIMITER: () => DELIMITER$1,
	SEPARATOR: () => SEPARATOR$1,
	SEPARATOR_PATTERN: () => SEPARATOR_PATTERN$1,
	basename: () => basename$1,
	common: () => common$2,
	dirname: () => dirname$1,
	extname: () => extname$1,
	format: () => format$2,
	fromFileUrl: () => fromFileUrl$1,
	globToRegExp: () => globToRegExp$1,
	isAbsolute: () => isAbsolute$1,
	isGlob: () => isGlob$1,
	join: () => join$1,
	joinGlobs: () => joinGlobs$1,
	normalize: () => normalize$2,
	normalizeGlob: () => normalizeGlob$1,
	parse: () => parse$1,
	relative: () => relative$1,
	resolve: () => resolve$1,
	toFileUrl: () => toFileUrl$1,
	toNamespacedPath: () => toNamespacedPath$1
});
function assertPath$1(path) {
	if (typeof path !== "string") throw new TypeError(`Path must be a string, received "${JSON.stringify(path)}"`);
}
function stripSuffix$1(name, suffix) {
	if (suffix.length >= name.length) return name;
	const lenDiff = name.length - suffix.length;
	for (let i = suffix.length - 1; i >= 0; --i) if (name.charCodeAt(lenDiff + i) !== suffix.charCodeAt(i)) return name;
	return name.slice(0, -suffix.length);
}
function lastPathSegment$1(path, isSep, start = 0) {
	let matchedNonSeparator = false;
	let end = path.length;
	for (let i = path.length - 1; i >= start; --i) if (isSep(path.charCodeAt(i))) {
		if (matchedNonSeparator) {
			start = i + 1;
			break;
		}
	} else if (!matchedNonSeparator) {
		matchedNonSeparator = true;
		end = i + 1;
	}
	return path.slice(start, end);
}
function assertArgs$1$1(path, suffix) {
	assertPath$1(path);
	if (path.length === 0) return path;
	if (typeof suffix !== "string") throw new TypeError(`Suffix must be a string, received "${JSON.stringify(suffix)}"`);
}
function assertArg$3$1(url) {
	url = url instanceof URL ? url : new URL(url);
	if (url.protocol !== "file:") throw new TypeError(`URL must be a file URL: received "${url.protocol}"`);
	return url;
}
/**
* Converts a file URL to a path string.
*
* @example Usage
* ```ts
* import { fromFileUrl } from "@std/path/posix/from-file-url";
* import { assertEquals } from "@std/assert";
*
* assertEquals(fromFileUrl(new URL("file:///home/foo")), "/home/foo");
* ```
*
* @param url The file URL to convert.
* @returns The path string.
*/ function fromFileUrl$1(url) {
	url = assertArg$3$1(url);
	return decodeURIComponent(url.pathname.replace(/%(?![0-9A-Fa-f]{2})/g, "%25"));
}
function stripTrailingSeparators$1(segment, isSep) {
	if (segment.length <= 1) return segment;
	let end = segment.length;
	for (let i = segment.length - 1; i > 0; i--) if (isSep(segment.charCodeAt(i))) end = i;
	else break;
	return segment.slice(0, end);
}
const CHAR_DOT$1 = 46;
const CHAR_FORWARD_SLASH$1 = 47;
function isPosixPathSeparator$1(code) {
	return code === CHAR_FORWARD_SLASH$1;
}
/**
* Return the last portion of a `path`.
* Trailing directory separators are ignored, and optional suffix is removed.
*
* @example Usage
* ```ts
* import { basename } from "@std/path/posix/basename";
* import { assertEquals } from "@std/assert";
*
* assertEquals(basename("/home/user/Documents/"), "Documents");
* assertEquals(basename("/home/user/Documents/image.png"), "image.png");
* assertEquals(basename("/home/user/Documents/image.png", ".png"), "image");
* assertEquals(basename(new URL("file:///home/user/Documents/image.png")), "image.png");
* assertEquals(basename(new URL("file:///home/user/Documents/image.png"), ".png"), "image");
* ```
*
* @example Working with URLs
*
* Note: This function doesn't automatically strip hash and query parts from
* URLs. If your URL contains a hash or query, remove them before passing the
* URL to the function. This can be done by passing the URL to `new URL(url)`,
* and setting the `hash` and `search` properties to empty strings.
*
* ```ts
* import { basename } from "@std/path/posix/basename";
* import { assertEquals } from "@std/assert";
*
* assertEquals(basename("https://deno.land/std/path/mod.ts"), "mod.ts");
* assertEquals(basename("https://deno.land/std/path/mod.ts", ".ts"), "mod");
* assertEquals(basename("https://deno.land/std/path/mod.ts?a=b"), "mod.ts?a=b");
* assertEquals(basename("https://deno.land/std/path/mod.ts#header"), "mod.ts#header");
* ```
*
* @param path The path to extract the name from.
* @param suffix The suffix to remove from extracted name.
* @returns The extracted name.
*/ function basename$1(path, suffix = "") {
	if (path instanceof URL) path = fromFileUrl$1(path);
	assertArgs$1$1(path, suffix);
	const strippedSegment = stripTrailingSeparators$1(lastPathSegment$1(path, isPosixPathSeparator$1), isPosixPathSeparator$1);
	return suffix ? stripSuffix$1(strippedSegment, suffix) : strippedSegment;
}
/**
* The character used to separate entries in the PATH environment variable.
*/ const DELIMITER$1 = ":";
/**
* The character used to separate components of a file path.
*/ const SEPARATOR$1 = "/";
/**
* A regular expression that matches one or more path separators.
*/ const SEPARATOR_PATTERN$1 = /\/+/;
function assertArg$2$1(path) {
	assertPath$1(path);
	if (path.length === 0) return ".";
}
/**
* Return the directory path of a `path`.
*
* @example Usage
* ```ts
* import { dirname } from "@std/path/posix/dirname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(dirname("/home/user/Documents/"), "/home/user");
* assertEquals(dirname("/home/user/Documents/image.png"), "/home/user/Documents");
* assertEquals(dirname("https://deno.land/std/path/mod.ts"), "https://deno.land/std/path");
* assertEquals(dirname(new URL("file:///home/user/Documents/image.png")), "/home/user/Documents");
* ```
*
* @example Working with URLs
*
* ```ts
* import { dirname } from "@std/path/posix/dirname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(dirname("https://deno.land/std/path/mod.ts"), "https://deno.land/std/path");
* assertEquals(dirname("https://deno.land/std/path/mod.ts?a=b"), "https://deno.land/std/path");
* assertEquals(dirname("https://deno.land/std/path/mod.ts#header"), "https://deno.land/std/path");
* ```
*
* @param path The path to get the directory from.
* @returns The directory path.
*/ function dirname$1(path) {
	if (path instanceof URL) path = fromFileUrl$1(path);
	assertArg$2$1(path);
	let end = -1;
	let matchedNonSeparator = false;
	for (let i = path.length - 1; i >= 1; --i) if (isPosixPathSeparator$1(path.charCodeAt(i))) {
		if (matchedNonSeparator) {
			end = i;
			break;
		}
	} else matchedNonSeparator = true;
	if (end === -1) return isPosixPathSeparator$1(path.charCodeAt(0)) ? "/" : ".";
	return stripTrailingSeparators$1(path.slice(0, end), isPosixPathSeparator$1);
}
/**
* Return the extension of the `path` with leading period.
*
* @example Usage
* ```ts
* import { extname } from "@std/path/posix/extname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(extname("/home/user/Documents/file.ts"), ".ts");
* assertEquals(extname("/home/user/Documents/"), "");
* assertEquals(extname("/home/user/Documents/image.png"), ".png");
* assertEquals(extname(new URL("file:///home/user/Documents/file.ts")), ".ts");
* assertEquals(extname(new URL("file:///home/user/Documents/file.ts?a=b")), ".ts");
* assertEquals(extname(new URL("file:///home/user/Documents/file.ts#header")), ".ts");
* ```
*
* @example Working with URLs
*
* Note: This function doesn't automatically strip hash and query parts from
* URLs. If your URL contains a hash or query, remove them before passing the
* URL to the function. This can be done by passing the URL to `new URL(url)`,
* and setting the `hash` and `search` properties to empty strings.
*
* ```ts
* import { extname } from "@std/path/posix/extname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(extname("https://deno.land/std/path/mod.ts"), ".ts");
* assertEquals(extname("https://deno.land/std/path/mod.ts?a=b"), ".ts?a=b");
* assertEquals(extname("https://deno.land/std/path/mod.ts#header"), ".ts#header");
* ```
*
* @param path The path to get the extension from.
* @returns The extension (ex. for `file.ts` returns `.ts`).
*/ function extname$1(path) {
	if (path instanceof URL) path = fromFileUrl$1(path);
	assertPath$1(path);
	let startDot = -1;
	let startPart = 0;
	let end = -1;
	let matchedSlash = true;
	let preDotState = 0;
	for (let i = path.length - 1; i >= 0; --i) {
		const code = path.charCodeAt(i);
		if (isPosixPathSeparator$1(code)) {
			if (!matchedSlash) {
				startPart = i + 1;
				break;
			}
			continue;
		}
		if (end === -1) {
			matchedSlash = false;
			end = i + 1;
		}
		if (code === CHAR_DOT$1) {
			if (startDot === -1) startDot = i;
			else if (preDotState !== 1) preDotState = 1;
		} else if (startDot !== -1) preDotState = -1;
	}
	if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1) return "";
	return path.slice(startDot, end);
}
function _format$1(sep, pathObject) {
	const dir = pathObject.dir || pathObject.root;
	const base = pathObject.base || (pathObject.name ?? "") + (pathObject.ext ?? "");
	if (!dir) return base;
	if (base === sep) return dir;
	if (dir === pathObject.root) return dir + base;
	return dir + sep + base;
}
function assertArg$1$1(pathObject) {
	if (pathObject === null || typeof pathObject !== "object") throw new TypeError(`The "pathObject" argument must be of type Object, received type "${typeof pathObject}"`);
}
/**
* Generate a path from `ParsedPath` object.
*
* @example Usage
* ```ts
* import { format } from "@std/path/posix/format";
* import { assertEquals } from "@std/assert";
*
* const path = format({
*   root: "/",
*   dir: "/path/dir",
*   base: "file.txt",
*   ext: ".txt",
*   name: "file"
* });
* assertEquals(path, "/path/dir/file.txt");
* ```
*
* @param pathObject The path object to format.
* @returns The formatted path.
*/ function format$2(pathObject) {
	assertArg$1$1(pathObject);
	return _format$1("/", pathObject);
}
/**
* Verifies whether provided path is absolute.
*
* @example Usage
* ```ts
* import { isAbsolute } from "@std/path/posix/is-absolute";
* import { assert, assertFalse } from "@std/assert";
*
* assert(isAbsolute("/home/user/Documents/"));
* assertFalse(isAbsolute("home/user/Documents/"));
* ```
*
* @param path The path to verify.
* @returns Whether the path is absolute.
*/ function isAbsolute$1(path) {
	assertPath$1(path);
	return path.length > 0 && isPosixPathSeparator$1(path.charCodeAt(0));
}
function assertArg$4(path) {
	assertPath$1(path);
	if (path.length === 0) return ".";
}
function normalizeString$1(path, allowAboveRoot, separator, isPathSeparator) {
	let res = "";
	let lastSegmentLength = 0;
	let lastSlash = -1;
	let dots = 0;
	let code;
	for (let i = 0; i <= path.length; ++i) {
		if (i < path.length) code = path.charCodeAt(i);
		else if (isPathSeparator(code)) break;
		else code = CHAR_FORWARD_SLASH$1;
		if (isPathSeparator(code)) {
			if (lastSlash === i - 1 || dots === 1);
			else if (lastSlash !== i - 1 && dots === 2) {
				if (res.length < 2 || lastSegmentLength !== 2 || res.charCodeAt(res.length - 1) !== CHAR_DOT$1 || res.charCodeAt(res.length - 2) !== CHAR_DOT$1) {
					if (res.length > 2) {
						const lastSlashIndex = res.lastIndexOf(separator);
						if (lastSlashIndex === -1) {
							res = "";
							lastSegmentLength = 0;
						} else {
							res = res.slice(0, lastSlashIndex);
							lastSegmentLength = res.length - 1 - res.lastIndexOf(separator);
						}
						lastSlash = i;
						dots = 0;
						continue;
					} else if (res.length === 2 || res.length === 1) {
						res = "";
						lastSegmentLength = 0;
						lastSlash = i;
						dots = 0;
						continue;
					}
				}
				if (allowAboveRoot) {
					if (res.length > 0) res += `${separator}..`;
					else res = "..";
					lastSegmentLength = 2;
				}
			} else {
				if (res.length > 0) res += separator + path.slice(lastSlash + 1, i);
				else res = path.slice(lastSlash + 1, i);
				lastSegmentLength = i - lastSlash - 1;
			}
			lastSlash = i;
			dots = 0;
		} else if (code === CHAR_DOT$1 && dots !== -1) ++dots;
		else dots = -1;
	}
	return res;
}
/**
* Normalize the `path`, resolving `'..'` and `'.'` segments.
* Note that resolving these segments does not necessarily mean that all will be eliminated.
* A `'..'` at the top-level will be preserved, and an empty path is canonically `'.'`.
*
* @example Usage
* ```ts
* import { normalize } from "@std/path/posix/normalize";
* import { assertEquals } from "@std/assert";
*
* assertEquals(normalize("/foo/bar//baz/asdf/quux/.."), "/foo/bar/baz/asdf");
* assertEquals(normalize(new URL("file:///foo/bar//baz/asdf/quux/..")), "/foo/bar/baz/asdf/");
* ```
*
* @example Working with URLs
*
* Note: This function will remove the double slashes from a URL's scheme.
* Hence, do not pass a full URL to this function. Instead, pass the pathname of
* the URL.
*
* ```ts
* import { normalize } from "@std/path/posix/normalize";
* import { assertEquals } from "@std/assert";
*
* const url = new URL("https://deno.land");
* url.pathname = normalize("//std//assert//.//mod.ts");
* assertEquals(url.href, "https://deno.land/std/assert/mod.ts");
*
* url.pathname = normalize("std/assert/../async/retry.ts");
* assertEquals(url.href, "https://deno.land/std/async/retry.ts");
* ```
*
* @param path The path to normalize.
* @returns The normalized path.
*/ function normalize$2(path) {
	if (path instanceof URL) path = fromFileUrl$1(path);
	assertArg$4(path);
	const isAbsolute = isPosixPathSeparator$1(path.charCodeAt(0));
	const trailingSeparator = isPosixPathSeparator$1(path.charCodeAt(path.length - 1));
	path = normalizeString$1(path, !isAbsolute, "/", isPosixPathSeparator$1);
	if (path.length === 0 && !isAbsolute) path = ".";
	if (path.length > 0 && trailingSeparator) path += "/";
	if (isAbsolute) return `/${path}`;
	return path;
}
/**
* Join all given a sequence of `paths`,then normalizes the resulting path.
*
* @example Usage
* ```ts
* import { join } from "@std/path/posix/join";
* import { assertEquals } from "@std/assert";
*
* assertEquals(join("/foo", "bar", "baz/asdf", "quux", ".."), "/foo/bar/baz/asdf");
* assertEquals(join(new URL("file:///foo"), "bar", "baz/asdf", "quux", ".."), "/foo/bar/baz/asdf");
* ```
*
* @example Working with URLs
* ```ts
* import { join } from "@std/path/posix/join";
* import { assertEquals } from "@std/assert";
*
* const url = new URL("https://deno.land");
* url.pathname = join("std", "path", "mod.ts");
* assertEquals(url.href, "https://deno.land/std/path/mod.ts");
*
* url.pathname = join("//std", "path/", "/mod.ts");
* assertEquals(url.href, "https://deno.land/std/path/mod.ts");
* ```
*
* @param path The path to join. This can be string or file URL.
* @param paths The paths to join.
* @returns The joined path.
*/ function join$1(path, ...paths) {
	if (path === void 0) return ".";
	if (path instanceof URL) path = fromFileUrl$1(path);
	paths = path ? [path, ...paths] : paths;
	paths.forEach((path) => assertPath$1(path));
	const joined = paths.filter((path) => path.length > 0).join("/");
	return joined === "" ? "." : normalize$2(joined);
}
/**
* Return a `ParsedPath` object of the `path`.
*
* @example Usage
* ```ts
* import { parse } from "@std/path/posix/parse";
* import { assertEquals } from "@std/assert";
*
* const path = parse("/home/user/file.txt");
* assertEquals(path, {
*   root: "/",
*   dir: "/home/user",
*   base: "file.txt",
*   ext: ".txt",
*   name: "file"
* });
* ```
*
* @param path The path to parse.
* @returns The parsed path object.
*/ function parse$1(path) {
	assertPath$1(path);
	const ret = {
		root: "",
		dir: "",
		base: "",
		ext: "",
		name: ""
	};
	if (path.length === 0) return ret;
	const isAbsolute = isPosixPathSeparator$1(path.charCodeAt(0));
	let start;
	if (isAbsolute) {
		ret.root = "/";
		start = 1;
	} else start = 0;
	let startDot = -1;
	let startPart = 0;
	let end = -1;
	let matchedSlash = true;
	let i = path.length - 1;
	let preDotState = 0;
	for (; i >= start; --i) {
		const code = path.charCodeAt(i);
		if (isPosixPathSeparator$1(code)) {
			if (!matchedSlash) {
				startPart = i + 1;
				break;
			}
			continue;
		}
		if (end === -1) {
			matchedSlash = false;
			end = i + 1;
		}
		if (code === CHAR_DOT$1) {
			if (startDot === -1) startDot = i;
			else if (preDotState !== 1) preDotState = 1;
		} else if (startDot !== -1) preDotState = -1;
	}
	if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1) {
		if (end !== -1) if (startPart === 0 && isAbsolute) ret.base = ret.name = path.slice(1, end);
		else ret.base = ret.name = path.slice(startPart, end);
		ret.base = ret.base || "/";
	} else {
		if (startPart === 0 && isAbsolute) {
			ret.name = path.slice(1, startDot);
			ret.base = path.slice(1, end);
		} else {
			ret.name = path.slice(startPart, startDot);
			ret.base = path.slice(startPart, end);
		}
		ret.ext = path.slice(startDot, end);
	}
	if (startPart > 0) ret.dir = stripTrailingSeparators$1(path.slice(0, startPart - 1), isPosixPathSeparator$1);
	else if (isAbsolute) ret.dir = "/";
	return ret;
}
/**
* Resolves path segments into a `path`.
*
* @example Usage
* ```ts
* import { resolve } from "@std/path/posix/resolve";
* import { assertEquals } from "@std/assert";
*
* const path = resolve("/foo", "bar", "baz/asdf", "quux", "..");
* assertEquals(path, "/foo/bar/baz/asdf");
* ```
*
* @param pathSegments The path segments to resolve.
* @returns The resolved path.
*/ function resolve$1(...pathSegments) {
	let resolvedPath = "";
	let resolvedAbsolute = false;
	for (let i = pathSegments.length - 1; i >= -1 && !resolvedAbsolute; i--) {
		let path;
		if (i >= 0) path = pathSegments[i];
		else {
			const { Deno } = globalThis;
			if (typeof Deno?.cwd !== "function") throw new TypeError("Resolved a relative path without a current working directory (CWD)");
			path = Deno.cwd();
		}
		assertPath$1(path);
		if (path.length === 0) continue;
		resolvedPath = `${path}/${resolvedPath}`;
		resolvedAbsolute = isPosixPathSeparator$1(path.charCodeAt(0));
	}
	resolvedPath = normalizeString$1(resolvedPath, !resolvedAbsolute, "/", isPosixPathSeparator$1);
	if (resolvedAbsolute) if (resolvedPath.length > 0) return `/${resolvedPath}`;
	else return "/";
	else if (resolvedPath.length > 0) return resolvedPath;
	else return ".";
}
function assertArgs$2(from, to) {
	assertPath$1(from);
	assertPath$1(to);
	if (from === to) return "";
}
/**
* Return the relative path from `from` to `to` based on current working directory.
*
* If `from` and `to` are the same, return an empty string.
*
* @example Usage
* ```ts
* import { relative } from "@std/path/posix/relative";
* import { assertEquals } from "@std/assert";
*
* const path = relative("/data/orandea/test/aaa", "/data/orandea/impl/bbb");
* assertEquals(path, "../../impl/bbb");
* ```
*
* @param from The path to start from.
* @param to The path to reach.
* @returns The relative path.
*/ function relative$1(from, to) {
	assertArgs$2(from, to);
	from = resolve$1(from);
	to = resolve$1(to);
	if (from === to) return "";
	let fromStart = 1;
	const fromEnd = from.length;
	for (; fromStart < fromEnd; ++fromStart) if (!isPosixPathSeparator$1(from.charCodeAt(fromStart))) break;
	const fromLen = fromEnd - fromStart;
	let toStart = 1;
	const toEnd = to.length;
	for (; toStart < toEnd; ++toStart) if (!isPosixPathSeparator$1(to.charCodeAt(toStart))) break;
	const toLen = toEnd - toStart;
	const length = fromLen < toLen ? fromLen : toLen;
	let lastCommonSep = -1;
	let i = 0;
	for (; i <= length; ++i) {
		if (i === length) {
			if (toLen > length) {
				if (isPosixPathSeparator$1(to.charCodeAt(toStart + i))) return to.slice(toStart + i + 1);
				else if (i === 0) return to.slice(toStart + i);
			} else if (fromLen > length) {
				if (isPosixPathSeparator$1(from.charCodeAt(fromStart + i))) lastCommonSep = i;
				else if (i === 0) lastCommonSep = 0;
			}
			break;
		}
		const fromCode = from.charCodeAt(fromStart + i);
		if (fromCode !== to.charCodeAt(toStart + i)) break;
		else if (isPosixPathSeparator$1(fromCode)) lastCommonSep = i;
	}
	let out = "";
	for (i = fromStart + lastCommonSep + 1; i <= fromEnd; ++i) if (i === fromEnd || isPosixPathSeparator$1(from.charCodeAt(i))) if (out.length === 0) out += "..";
	else out += "/..";
	if (out.length > 0) return out + to.slice(toStart + lastCommonSep);
	else {
		toStart += lastCommonSep;
		if (isPosixPathSeparator$1(to.charCodeAt(toStart))) ++toStart;
		return to.slice(toStart);
	}
}
const WHITESPACE_ENCODINGS$1 = {
	"	": "%09",
	"\n": "%0A",
	"\v": "%0B",
	"\f": "%0C",
	"\r": "%0D",
	" ": "%20"
};
function encodeWhitespace$1(string) {
	return string.replaceAll(/[\s]/g, (c) => {
		return WHITESPACE_ENCODINGS$1[c] ?? c;
	});
}
/**
* Converts a path string to a file URL.
*
* @example Usage
* ```ts
* import { toFileUrl } from "@std/path/posix/to-file-url";
* import { assertEquals } from "@std/assert";
*
* assertEquals(toFileUrl("/home/foo"), new URL("file:///home/foo"));
* assertEquals(toFileUrl("/home/foo bar"), new URL("file:///home/foo%20bar"));
* ```
*
* @param path The path to convert.
* @returns The file URL.
*/ function toFileUrl$1(path) {
	if (!isAbsolute$1(path)) throw new TypeError(`Path must be absolute: received "${path}"`);
	const url = new URL("file:///");
	url.pathname = encodeWhitespace$1(path.replace(/%/g, "%25").replace(/\\/g, "%5C"));
	return url;
}
/**
* Converts a path to a namespaced path. This function returns the path as is on posix.
*
* @example Usage
* ```ts
* import { toNamespacedPath } from "@std/path/posix/to-namespaced-path";
* import { assertEquals } from "@std/assert";
*
* assertEquals(toNamespacedPath("/home/foo"), "/home/foo");
* ```
*
* @param path The path.
* @returns The namespaced path.
*/ function toNamespacedPath$1(path) {
	return path;
}
function common$1$1(paths, sep) {
	const [first = "", ...remaining] = paths;
	const parts = first.split(sep);
	let endOfPrefix = parts.length;
	let append = "";
	for (const path of remaining) {
		const compare = path.split(sep);
		if (compare.length <= endOfPrefix) {
			endOfPrefix = compare.length;
			append = "";
		}
		for (let i = 0; i < endOfPrefix; i++) if (compare[i] !== parts[i]) {
			endOfPrefix = i;
			append = i === 0 ? "" : sep;
			break;
		}
	}
	return parts.slice(0, endOfPrefix).join(sep) + append;
}
/** Determines the common path from a set of paths for POSIX systems.
*
* @example Usage
* ```ts
* import { common } from "@std/path/posix/common";
* import { assertEquals } from "@std/assert";
*
* const path = common([
*   "./deno/std/path/mod.ts",
*   "./deno/std/fs/mod.ts",
* ]);
* assertEquals(path, "./deno/std/");
* ```
*
* @param paths The paths to compare.
* @returns The common path.
*/ function common$2(paths) {
	return common$1$1(paths, SEPARATOR$1);
}
/**
* Options for {@linkcode globToRegExp}, {@linkcode joinGlobs},
* {@linkcode normalizeGlob} and {@linkcode expandGlob}.
*/ const REG_EXP_ESCAPE_CHARS$1 = [
	"!",
	"$",
	"(",
	")",
	"*",
	"+",
	".",
	"=",
	"?",
	"[",
	"\\",
	"^",
	"{",
	"|"
];
const RANGE_ESCAPE_CHARS$1 = [
	"-",
	"\\",
	"]"
];
function _globToRegExp$1(c, glob, { extended = true, globstar: globstarOption = true, caseInsensitive = false } = {}) {
	if (glob === "") return /(?!)/;
	let newLength = glob.length;
	for (; newLength > 1 && c.seps.includes(glob[newLength - 1]); newLength--);
	glob = glob.slice(0, newLength);
	let regExpString = "";
	for (let j = 0; j < glob.length;) {
		let segment = "";
		const groupStack = [];
		let inRange = false;
		let inEscape = false;
		let endsWithSep = false;
		let i = j;
		for (; i < glob.length && !(c.seps.includes(glob[i]) && groupStack.length === 0); i++) {
			if (inEscape) {
				inEscape = false;
				segment += (inRange ? RANGE_ESCAPE_CHARS$1 : REG_EXP_ESCAPE_CHARS$1).includes(glob[i]) ? `\\${glob[i]}` : glob[i];
				continue;
			}
			if (glob[i] === c.escapePrefix) {
				inEscape = true;
				continue;
			}
			if (glob[i] === "[") {
				if (!inRange) {
					inRange = true;
					segment += "[";
					if (glob[i + 1] === "!") {
						i++;
						segment += "^";
					} else if (glob[i + 1] === "^") {
						i++;
						segment += "\\^";
					}
					continue;
				} else if (glob[i + 1] === ":") {
					let k = i + 1;
					let value = "";
					while (glob[k + 1] !== void 0 && glob[k + 1] !== ":") {
						value += glob[k + 1];
						k++;
					}
					if (glob[k + 1] === ":" && glob[k + 2] === "]") {
						i = k + 2;
						if (value === "alnum") segment += "\\dA-Za-z";
						else if (value === "alpha") segment += "A-Za-z";
						else if (value === "ascii") segment += "\0-";
						else if (value === "blank") segment += "	 ";
						else if (value === "cntrl") segment += "\0-";
						else if (value === "digit") segment += "\\d";
						else if (value === "graph") segment += "!-~";
						else if (value === "lower") segment += "a-z";
						else if (value === "print") segment += " -~";
						else if (value === "punct") segment += "!\"#$%&'()*+,\\-./:;<=>?@[\\\\\\]^_‘{|}~";
						else if (value === "space") segment += "\\s\v";
						else if (value === "upper") segment += "A-Z";
						else if (value === "word") segment += "\\w";
						else if (value === "xdigit") segment += "\\dA-Fa-f";
						continue;
					}
				}
			}
			if (glob[i] === "]" && inRange) {
				inRange = false;
				segment += "]";
				continue;
			}
			if (inRange) {
				segment += glob[i];
				continue;
			}
			if (glob[i] === ")" && groupStack.length > 0 && groupStack[groupStack.length - 1] !== "BRACE") {
				segment += ")";
				const type = groupStack.pop();
				if (type === "!") segment += c.wildcard;
				else if (type !== "@") segment += type;
				continue;
			}
			if (glob[i] === "|" && groupStack.length > 0 && groupStack[groupStack.length - 1] !== "BRACE") {
				segment += "|";
				continue;
			}
			if (glob[i] === "+" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("+");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "@" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("@");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "?") {
				if (extended && glob[i + 1] === "(") {
					i++;
					groupStack.push("?");
					segment += "(?:";
				} else segment += ".";
				continue;
			}
			if (glob[i] === "!" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("!");
				segment += "(?!";
				continue;
			}
			if (glob[i] === "{") {
				groupStack.push("BRACE");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "}" && groupStack[groupStack.length - 1] === "BRACE") {
				groupStack.pop();
				segment += ")";
				continue;
			}
			if (glob[i] === "," && groupStack[groupStack.length - 1] === "BRACE") {
				segment += "|";
				continue;
			}
			if (glob[i] === "*") {
				if (extended && glob[i + 1] === "(") {
					i++;
					groupStack.push("*");
					segment += "(?:";
				} else {
					const prevChar = glob[i - 1];
					let numStars = 1;
					while (glob[i + 1] === "*") {
						i++;
						numStars++;
					}
					const nextChar = glob[i + 1];
					if (globstarOption && numStars === 2 && [...c.seps, void 0].includes(prevChar) && [...c.seps, void 0].includes(nextChar)) {
						segment += c.globstar;
						endsWithSep = true;
					} else segment += c.wildcard;
				}
				continue;
			}
			segment += REG_EXP_ESCAPE_CHARS$1.includes(glob[i]) ? `\\${glob[i]}` : glob[i];
		}
		if (groupStack.length > 0 || inRange || inEscape) {
			segment = "";
			for (const c of glob.slice(j, i)) {
				segment += REG_EXP_ESCAPE_CHARS$1.includes(c) ? `\\${c}` : c;
				endsWithSep = false;
			}
		}
		regExpString += segment;
		if (!endsWithSep) {
			regExpString += i < glob.length ? c.sep : c.sepMaybe;
			endsWithSep = true;
		}
		while (c.seps.includes(glob[i])) i++;
		j = i;
	}
	regExpString = `^${regExpString}$`;
	return new RegExp(regExpString, caseInsensitive ? "i" : "");
}
const constants$2 = {
	sep: "/+",
	sepMaybe: "/*",
	seps: ["/"],
	globstar: "(?:[^/]*(?:/|$)+)*",
	wildcard: "[^/]*",
	escapePrefix: "\\"
};
/** Convert a glob string to a regular expression.
*
* Tries to match bash glob expansion as closely as possible.
*
* Basic glob syntax:
* - `*` - Matches everything without leaving the path segment.
* - `?` - Matches any single character.
* - `{foo,bar}` - Matches `foo` or `bar`.
* - `[abcd]` - Matches `a`, `b`, `c` or `d`.
* - `[a-d]` - Matches `a`, `b`, `c` or `d`.
* - `[!abcd]` - Matches any single character besides `a`, `b`, `c` or `d`.
* - `[[:<class>:]]` - Matches any character belonging to `<class>`.
*     - `[[:alnum:]]` - Matches any digit or letter.
*     - `[[:digit:]abc]` - Matches any digit, `a`, `b` or `c`.
*     - See https://facelessuser.github.io/wcmatch/glob/#posix-character-classes
*       for a complete list of supported character classes.
* - `\` - Escapes the next character for an `os` other than `"windows"`.
* - \` - Escapes the next character for `os` set to `"windows"`.
* - `/` - Path separator.
* - `\` - Additional path separator only for `os` set to `"windows"`.
*
* Extended syntax:
* - Requires `{ extended: true }`.
* - `?(foo|bar)` - Matches 0 or 1 instance of `{foo,bar}`.
* - `@(foo|bar)` - Matches 1 instance of `{foo,bar}`. They behave the same.
* - `*(foo|bar)` - Matches _n_ instances of `{foo,bar}`.
* - `+(foo|bar)` - Matches _n > 0_ instances of `{foo,bar}`.
* - `!(foo|bar)` - Matches anything other than `{foo,bar}`.
* - See https://www.linuxjournal.com/content/bash-extended-globbing.
*
* Globstar syntax:
* - Requires `{ globstar: true }`.
* - `**` - Matches any number of any path segments.
*     - Must comprise its entire path segment in the provided glob.
* - See https://www.linuxjournal.com/content/globstar-new-bash-globbing-option.
*
* Note the following properties:
* - The generated `RegExp` is anchored at both start and end.
* - Repeating and trailing separators are tolerated. Trailing separators in the
*   provided glob have no meaning and are discarded.
* - Absolute globs will only match absolute paths, etc.
* - Empty globs will match nothing.
* - Any special glob syntax must be contained to one path segment. For example,
*   `?(foo|bar/baz)` is invalid. The separator will take precedence and the
*   first segment ends with an unclosed group.
* - If a path segment ends with unclosed groups or a dangling escape prefix, a
*   parse error has occurred. Every character for that segment is taken
*   literally in this event.
*
* Limitations:
* - A negative group like `!(foo|bar)` will wrongly be converted to a negative
*   look-ahead followed by a wildcard. This means that `!(foo).js` will wrongly
*   fail to match `foobar.js`, even though `foobar` is not `foo`. Effectively,
*   `!(foo|bar)` is treated like `!(@(foo|bar)*)`. This will work correctly if
*   the group occurs not nested at the end of the segment.
*
* @example Usage
* ```ts
* import { globToRegExp } from "@std/path/posix/glob-to-regexp";
* import { assertEquals } from "@std/assert";
*
* assertEquals(globToRegExp("*.js"), /^[^/]*\.js\/*$/);
* ```
*
* @param glob Glob string to convert.
* @param options Conversion options.
* @returns The regular expression equivalent to the glob.
*/ function globToRegExp$1(glob, options = {}) {
	return _globToRegExp$1(constants$2, glob, options);
}
/**
* Test whether the given string is a glob.
*
* @example Usage
* ```ts
* import { isGlob } from "@std/path/is-glob";
* import { assert } from "@std/assert";
*
* assert(!isGlob("foo/bar/../baz"));
* assert(isGlob("foo/*ar/../baz"));
* ```
*
* @param str String to test.
* @returns `true` if the given string is a glob, otherwise `false`
*/ function isGlob$1(str) {
	const chars = {
		"{": "}",
		"(": ")",
		"[": "]"
	};
	const regex = /\\(.)|(^!|\*|\?|[\].+)]\?|\[[^[\\\]]+\]|\{[^{\\}]+\}|\(\?[:!=][^\\)]+\)|\([^(|]+\|[^\\)]+\)|@\([^)]+\))/;
	if (str === "") return false;
	let match;
	while (match = regex.exec(str)) {
		if (match[2]) return true;
		let idx = match.index + match[0].length;
		const open = match[1];
		const close = open ? chars[open] : null;
		if (open && close) {
			const n = str.indexOf(close, idx);
			if (n !== -1) idx = n + 1;
		}
		str = str.slice(idx);
	}
	return false;
}
/**
* Like normalize(), but doesn't collapse "**\/.." when `globstar` is true.
*
* @example Usage
* ```ts
* import { normalizeGlob } from "@std/path/posix/normalize-glob";
* import { assertEquals } from "@std/assert";
*
* const path = normalizeGlob("foo/bar/../*", { globstar: true });
* assertEquals(path, "foo/*");
* ```
*
* @param glob The glob to normalize.
* @param options The options to use.
* @returns The normalized path.
*/ function normalizeGlob$1(glob, options = {}) {
	const { globstar = false } = options;
	if (glob.match(/\0/g)) throw new Error(`Glob contains invalid characters: "${glob}"`);
	if (!globstar) return normalize$2(glob);
	const s = SEPARATOR_PATTERN$1.source;
	const badParentPattern = new RegExp(`(?<=(${s}|^)\\*\\*${s})\\.\\.(?=${s}|$)`, "g");
	return normalize$2(glob.replace(badParentPattern, "\0")).replace(/\0/g, "..");
}
/**
* Like join(), but doesn't collapse "**\/.." when `globstar` is true.
*
* @example Usage
* ```ts
* import { joinGlobs } from "@std/path/posix/join-globs";
* import { assertEquals } from "@std/assert";
*
* const path = joinGlobs(["foo", "bar", "**"], { globstar: true });
* assertEquals(path, "foo/bar/**");
* ```
*
* @param globs The globs to join.
* @param options The options to use.
* @returns The joined path.
*/ function joinGlobs$1(globs, options = {}) {
	const { globstar = false } = options;
	if (!globstar || globs.length === 0) return join$1(...globs);
	let joined;
	for (const glob of globs) {
		const path = glob;
		if (path.length > 0) if (!joined) joined = path;
		else joined += `${SEPARATOR$1}${path}`;
	}
	if (!joined) return ".";
	return normalizeGlob$1(joined, { globstar });
}

//#endregion
//#region node_modules/.pnpm/@eslint+config-array@0.23.2_patch_hash=9c56839266cb75a04e2a96a342456c69afd7549bf6c13a9ade49cc6d42de892a/node_modules/@eslint/config-array/dist/esm/std__path/windows.js
var windows_exports = /* @__PURE__ */ __exportAll({
	DELIMITER: () => DELIMITER,
	SEPARATOR: () => SEPARATOR,
	SEPARATOR_PATTERN: () => SEPARATOR_PATTERN,
	basename: () => basename,
	common: () => common,
	dirname: () => dirname,
	extname: () => extname,
	format: () => format$1,
	fromFileUrl: () => fromFileUrl,
	globToRegExp: () => globToRegExp,
	isAbsolute: () => isAbsolute,
	isGlob: () => isGlob,
	join: () => join,
	joinGlobs: () => joinGlobs,
	normalize: () => normalize$1,
	normalizeGlob: () => normalizeGlob,
	parse: () => parse,
	relative: () => relative,
	resolve: () => resolve,
	toFileUrl: () => toFileUrl,
	toNamespacedPath: () => toNamespacedPath
});
function assertPath(path) {
	if (typeof path !== "string") throw new TypeError(`Path must be a string, received "${JSON.stringify(path)}"`);
}
function stripSuffix(name, suffix) {
	if (suffix.length >= name.length) return name;
	const lenDiff = name.length - suffix.length;
	for (let i = suffix.length - 1; i >= 0; --i) if (name.charCodeAt(lenDiff + i) !== suffix.charCodeAt(i)) return name;
	return name.slice(0, -suffix.length);
}
function lastPathSegment(path, isSep, start = 0) {
	let matchedNonSeparator = false;
	let end = path.length;
	for (let i = path.length - 1; i >= start; --i) if (isSep(path.charCodeAt(i))) {
		if (matchedNonSeparator) {
			start = i + 1;
			break;
		}
	} else if (!matchedNonSeparator) {
		matchedNonSeparator = true;
		end = i + 1;
	}
	return path.slice(start, end);
}
function assertArgs$1(path, suffix) {
	assertPath(path);
	if (path.length === 0) return path;
	if (typeof suffix !== "string") throw new TypeError(`Suffix must be a string, received "${JSON.stringify(suffix)}"`);
}
const CHAR_UPPERCASE_A = 65;
const CHAR_LOWERCASE_A = 97;
const CHAR_UPPERCASE_Z = 90;
const CHAR_LOWERCASE_Z = 122;
const CHAR_DOT = 46;
const CHAR_FORWARD_SLASH = 47;
const CHAR_BACKWARD_SLASH = 92;
const CHAR_COLON = 58;
const CHAR_QUESTION_MARK = 63;
function stripTrailingSeparators(segment, isSep) {
	if (segment.length <= 1) return segment;
	let end = segment.length;
	for (let i = segment.length - 1; i > 0; i--) if (isSep(segment.charCodeAt(i))) end = i;
	else break;
	return segment.slice(0, end);
}
function isPosixPathSeparator(code) {
	return code === CHAR_FORWARD_SLASH;
}
function isPathSeparator(code) {
	return code === CHAR_FORWARD_SLASH || code === CHAR_BACKWARD_SLASH;
}
function isWindowsDeviceRoot(code) {
	return code >= CHAR_LOWERCASE_A && code <= CHAR_LOWERCASE_Z || code >= CHAR_UPPERCASE_A && code <= CHAR_UPPERCASE_Z;
}
function assertArg$3(url) {
	url = url instanceof URL ? url : new URL(url);
	if (url.protocol !== "file:") throw new TypeError(`URL must be a file URL: received "${url.protocol}"`);
	return url;
}
/**
* Converts a file URL to a path string.
*
* @example Usage
* ```ts
* import { fromFileUrl } from "@std/path/windows/from-file-url";
* import { assertEquals } from "@std/assert";
*
* assertEquals(fromFileUrl("file:///home/foo"), "\\home\\foo");
* assertEquals(fromFileUrl("file:///C:/Users/foo"), "C:\\Users\\foo");
* assertEquals(fromFileUrl("file://localhost/home/foo"), "\\home\\foo");
* ```
*
* @param url The file URL to convert.
* @returns The path string.
*/ function fromFileUrl(url) {
	url = assertArg$3(url);
	let path = decodeURIComponent(url.pathname.replace(/\//g, "\\").replace(/%(?![0-9A-Fa-f]{2})/g, "%25")).replace(/^\\*([A-Za-z]:)(\\|$)/, "$1\\");
	if (url.hostname !== "") path = `\\\\${url.hostname}${path}`;
	return path;
}
/**
* Return the last portion of a `path`.
* Trailing directory separators are ignored, and optional suffix is removed.
*
* @example Usage
* ```ts
* import { basename } from "@std/path/windows/basename";
* import { assertEquals } from "@std/assert";
*
* assertEquals(basename("C:\\user\\Documents\\"), "Documents");
* assertEquals(basename("C:\\user\\Documents\\image.png"), "image.png");
* assertEquals(basename("C:\\user\\Documents\\image.png", ".png"), "image");
* assertEquals(basename(new URL("file:///C:/user/Documents/image.png")), "image.png");
* assertEquals(basename(new URL("file:///C:/user/Documents/image.png"), ".png"), "image");
* ```
*
* @param path The path to extract the name from.
* @param suffix The suffix to remove from extracted name.
* @returns The extracted name.
*/ function basename(path, suffix = "") {
	if (path instanceof URL) path = fromFileUrl(path);
	assertArgs$1(path, suffix);
	let start = 0;
	if (path.length >= 2) {
		if (isWindowsDeviceRoot(path.charCodeAt(0))) {
			if (path.charCodeAt(1) === CHAR_COLON) start = 2;
		}
	}
	const strippedSegment = stripTrailingSeparators(lastPathSegment(path, isPathSeparator, start), isPathSeparator);
	return suffix ? stripSuffix(strippedSegment, suffix) : strippedSegment;
}
/**
* The character used to separate entries in the PATH environment variable.
*/ const DELIMITER = ";";
/**
* The character used to separate components of a file path.
*/ const SEPARATOR = "\\";
/**
* A regular expression that matches one or more path separators.
*/ const SEPARATOR_PATTERN = /[\\/]+/;
function assertArg$2(path) {
	assertPath(path);
	if (path.length === 0) return ".";
}
/**
* Return the directory path of a `path`.
*
* @example Usage
* ```ts
* import { dirname } from "@std/path/windows/dirname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(dirname("C:\\foo\\bar\\baz.ext"), "C:\\foo\\bar");
* assertEquals(dirname(new URL("file:///C:/foo/bar/baz.ext")), "C:\\foo\\bar");
* ```
*
* @param path The path to get the directory from.
* @returns The directory path.
*/ function dirname(path) {
	if (path instanceof URL) path = fromFileUrl(path);
	assertArg$2(path);
	const len = path.length;
	let rootEnd = -1;
	let end = -1;
	let matchedSlash = true;
	let offset = 0;
	const code = path.charCodeAt(0);
	if (len > 1) {
		if (isPathSeparator(code)) {
			rootEnd = offset = 1;
			if (isPathSeparator(path.charCodeAt(1))) {
				let j = 2;
				let last = j;
				for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
				if (j < len && j !== last) {
					last = j;
					for (; j < len; ++j) if (!isPathSeparator(path.charCodeAt(j))) break;
					if (j < len && j !== last) {
						last = j;
						for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
						if (j === len) return path;
						if (j !== last) rootEnd = offset = j + 1;
					}
				}
			}
		} else if (isWindowsDeviceRoot(code)) {
			if (path.charCodeAt(1) === CHAR_COLON) {
				rootEnd = offset = 2;
				if (len > 2) {
					if (isPathSeparator(path.charCodeAt(2))) rootEnd = offset = 3;
				}
			}
		}
	} else if (isPathSeparator(code)) return path;
	for (let i = len - 1; i >= offset; --i) if (isPathSeparator(path.charCodeAt(i))) {
		if (!matchedSlash) {
			end = i;
			break;
		}
	} else matchedSlash = false;
	if (end === -1) if (rootEnd === -1) return ".";
	else end = rootEnd;
	return stripTrailingSeparators(path.slice(0, end), isPosixPathSeparator);
}
/**
* Return the extension of the `path` with leading period.
*
* @example Usage
* ```ts
* import { extname } from "@std/path/windows/extname";
* import { assertEquals } from "@std/assert";
*
* assertEquals(extname("file.ts"), ".ts");
* assertEquals(extname(new URL("file:///C:/foo/bar/baz.ext")), ".ext");
* ```
*
* @param path The path to get the extension from.
* @returns The extension of the `path`.
*/ function extname(path) {
	if (path instanceof URL) path = fromFileUrl(path);
	assertPath(path);
	let start = 0;
	let startDot = -1;
	let startPart = 0;
	let end = -1;
	let matchedSlash = true;
	let preDotState = 0;
	if (path.length >= 2 && path.charCodeAt(1) === CHAR_COLON && isWindowsDeviceRoot(path.charCodeAt(0))) start = startPart = 2;
	for (let i = path.length - 1; i >= start; --i) {
		const code = path.charCodeAt(i);
		if (isPathSeparator(code)) {
			if (!matchedSlash) {
				startPart = i + 1;
				break;
			}
			continue;
		}
		if (end === -1) {
			matchedSlash = false;
			end = i + 1;
		}
		if (code === CHAR_DOT) {
			if (startDot === -1) startDot = i;
			else if (preDotState !== 1) preDotState = 1;
		} else if (startDot !== -1) preDotState = -1;
	}
	if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1) return "";
	return path.slice(startDot, end);
}
function _format(sep, pathObject) {
	const dir = pathObject.dir || pathObject.root;
	const base = pathObject.base || (pathObject.name ?? "") + (pathObject.ext ?? "");
	if (!dir) return base;
	if (base === sep) return dir;
	if (dir === pathObject.root) return dir + base;
	return dir + sep + base;
}
function assertArg$1(pathObject) {
	if (pathObject === null || typeof pathObject !== "object") throw new TypeError(`The "pathObject" argument must be of type Object, received type "${typeof pathObject}"`);
}
/**
* Generate a path from `ParsedPath` object.
*
* @example Usage
* ```ts
* import { format } from "@std/path/windows/format";
* import { assertEquals } from "@std/assert";
*
* const path = format({
*   root: "C:\\",
*   dir: "C:\\path\\dir",
*   base: "file.txt",
*   ext: ".txt",
*   name: "file"
* });
* assertEquals(path, "C:\\path\\dir\\file.txt");
* ```
*
* @param pathObject The path object to format.
* @returns The formatted path.
*/ function format$1(pathObject) {
	assertArg$1(pathObject);
	return _format("\\", pathObject);
}
/**
* Verifies whether provided path is absolute.
*
* @example Usage
* ```ts
* import { isAbsolute } from "@std/path/windows/is-absolute";
* import { assert, assertFalse } from "@std/assert";
*
* assert(isAbsolute("C:\\foo\\bar"));
* assertFalse(isAbsolute("..\\baz"));
* ```
*
* @param path The path to verify.
* @returns `true` if the path is absolute, `false` otherwise.
*/ function isAbsolute(path) {
	assertPath(path);
	const len = path.length;
	if (len === 0) return false;
	const code = path.charCodeAt(0);
	if (isPathSeparator(code)) return true;
	else if (isWindowsDeviceRoot(code)) {
		if (len > 2 && path.charCodeAt(1) === CHAR_COLON) {
			if (isPathSeparator(path.charCodeAt(2))) return true;
		}
	}
	return false;
}
function assertArg(path) {
	assertPath(path);
	if (path.length === 0) return ".";
}
function normalizeString(path, allowAboveRoot, separator, isPathSeparator) {
	let res = "";
	let lastSegmentLength = 0;
	let lastSlash = -1;
	let dots = 0;
	let code;
	for (let i = 0; i <= path.length; ++i) {
		if (i < path.length) code = path.charCodeAt(i);
		else if (isPathSeparator(code)) break;
		else code = CHAR_FORWARD_SLASH;
		if (isPathSeparator(code)) {
			if (lastSlash === i - 1 || dots === 1);
			else if (lastSlash !== i - 1 && dots === 2) {
				if (res.length < 2 || lastSegmentLength !== 2 || res.charCodeAt(res.length - 1) !== CHAR_DOT || res.charCodeAt(res.length - 2) !== CHAR_DOT) {
					if (res.length > 2) {
						const lastSlashIndex = res.lastIndexOf(separator);
						if (lastSlashIndex === -1) {
							res = "";
							lastSegmentLength = 0;
						} else {
							res = res.slice(0, lastSlashIndex);
							lastSegmentLength = res.length - 1 - res.lastIndexOf(separator);
						}
						lastSlash = i;
						dots = 0;
						continue;
					} else if (res.length === 2 || res.length === 1) {
						res = "";
						lastSegmentLength = 0;
						lastSlash = i;
						dots = 0;
						continue;
					}
				}
				if (allowAboveRoot) {
					if (res.length > 0) res += `${separator}..`;
					else res = "..";
					lastSegmentLength = 2;
				}
			} else {
				if (res.length > 0) res += separator + path.slice(lastSlash + 1, i);
				else res = path.slice(lastSlash + 1, i);
				lastSegmentLength = i - lastSlash - 1;
			}
			lastSlash = i;
			dots = 0;
		} else if (code === CHAR_DOT && dots !== -1) ++dots;
		else dots = -1;
	}
	return res;
}
/**
* Normalize the `path`, resolving `'..'` and `'.'` segments.
* Note that resolving these segments does not necessarily mean that all will be eliminated.
* A `'..'` at the top-level will be preserved, and an empty path is canonically `'.'`.
*
* @example Usage
* ```ts
* import { normalize } from "@std/path/windows/normalize";
* import { assertEquals } from "@std/assert";
*
* assertEquals(normalize("C:\\foo\\..\\bar"), "C:\\bar");
* assertEquals(normalize(new URL("file:///C:/foo/../bar")), "C:\\bar");
* ```
*
* @param path The path to normalize
* @returns The normalized path
*/ function normalize$1(path) {
	if (path instanceof URL) path = fromFileUrl(path);
	assertArg(path);
	const len = path.length;
	let rootEnd = 0;
	let device;
	let isAbsolute = false;
	const code = path.charCodeAt(0);
	if (len > 1) {
		if (isPathSeparator(code)) {
			isAbsolute = true;
			if (isPathSeparator(path.charCodeAt(1))) {
				let j = 2;
				let last = j;
				for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
				if (j < len && j !== last) {
					const firstPart = path.slice(last, j);
					last = j;
					for (; j < len; ++j) if (!isPathSeparator(path.charCodeAt(j))) break;
					if (j < len && j !== last) {
						last = j;
						for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
						if (j === len) return `\\\\${firstPart}\\${path.slice(last)}\\`;
						else if (j !== last) {
							device = `\\\\${firstPart}\\${path.slice(last, j)}`;
							rootEnd = j;
						}
					}
				}
			} else rootEnd = 1;
		} else if (isWindowsDeviceRoot(code)) {
			if (path.charCodeAt(1) === CHAR_COLON) {
				device = path.slice(0, 2);
				rootEnd = 2;
				if (len > 2) {
					if (isPathSeparator(path.charCodeAt(2))) {
						isAbsolute = true;
						rootEnd = 3;
					}
				}
			}
		}
	} else if (isPathSeparator(code)) return "\\";
	let tail;
	if (rootEnd < len) tail = normalizeString(path.slice(rootEnd), !isAbsolute, "\\", isPathSeparator);
	else tail = "";
	if (tail.length === 0 && !isAbsolute) tail = ".";
	if (tail.length > 0 && isPathSeparator(path.charCodeAt(len - 1))) tail += "\\";
	if (device === void 0) {
		if (isAbsolute) if (tail.length > 0) return `\\${tail}`;
		else return "\\";
		return tail;
	} else if (isAbsolute) if (tail.length > 0) return `${device}\\${tail}`;
	else return `${device}\\`;
	return device + tail;
}
/**
* Join all given a sequence of `paths`,then normalizes the resulting path.
*
* @example Usage
* ```ts
* import { join } from "@std/path/windows/join";
* import { assertEquals } from "@std/assert";
*
* assertEquals(join("C:\\foo", "bar", "baz\\.."), "C:\\foo\\bar");
* assertEquals(join(new URL("file:///C:/foo"), "bar", "baz\\.."), "C:\\foo\\bar");
* ```
*
* @param path The path to join. This can be string or file URL.
* @param paths The paths to join.
* @returns The joined path.
*/ function join(path, ...paths) {
	if (path instanceof URL) path = fromFileUrl(path);
	paths = path ? [path, ...paths] : paths;
	paths.forEach((path) => assertPath(path));
	paths = paths.filter((path) => path.length > 0);
	if (paths.length === 0) return ".";
	let needsReplace = true;
	let slashCount = 0;
	const firstPart = paths[0];
	if (isPathSeparator(firstPart.charCodeAt(0))) {
		++slashCount;
		const firstLen = firstPart.length;
		if (firstLen > 1) {
			if (isPathSeparator(firstPart.charCodeAt(1))) {
				++slashCount;
				if (firstLen > 2) if (isPathSeparator(firstPart.charCodeAt(2))) ++slashCount;
				else needsReplace = false;
			}
		}
	}
	let joined = paths.join("\\");
	if (needsReplace) {
		for (; slashCount < joined.length; ++slashCount) if (!isPathSeparator(joined.charCodeAt(slashCount))) break;
		if (slashCount >= 2) joined = `\\${joined.slice(slashCount)}`;
	}
	return normalize$1(joined);
}
/**
* Return a `ParsedPath` object of the `path`.
*
* @example Usage
* ```ts
* import { parse } from "@std/path/windows/parse";
* import { assertEquals } from "@std/assert";
*
* const parsed = parse("C:\\foo\\bar\\baz.ext");
* assertEquals(parsed, {
*   root: "C:\\",
*   dir: "C:\\foo\\bar",
*   base: "baz.ext",
*   ext: ".ext",
*   name: "baz",
* });
* ```
*
* @param path The path to parse.
* @returns The `ParsedPath` object.
*/ function parse(path) {
	assertPath(path);
	const ret = {
		root: "",
		dir: "",
		base: "",
		ext: "",
		name: ""
	};
	const len = path.length;
	if (len === 0) return ret;
	let rootEnd = 0;
	let code = path.charCodeAt(0);
	if (len > 1) {
		if (isPathSeparator(code)) {
			rootEnd = 1;
			if (isPathSeparator(path.charCodeAt(1))) {
				let j = 2;
				let last = j;
				for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
				if (j < len && j !== last) {
					last = j;
					for (; j < len; ++j) if (!isPathSeparator(path.charCodeAt(j))) break;
					if (j < len && j !== last) {
						last = j;
						for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
						if (j === len) rootEnd = j;
						else if (j !== last) rootEnd = j + 1;
					}
				}
			}
		} else if (isWindowsDeviceRoot(code)) {
			if (path.charCodeAt(1) === CHAR_COLON) {
				rootEnd = 2;
				if (len > 2) {
					if (isPathSeparator(path.charCodeAt(2))) {
						if (len === 3) {
							ret.root = ret.dir = path;
							ret.base = "\\";
							return ret;
						}
						rootEnd = 3;
					}
				} else {
					ret.root = ret.dir = path;
					return ret;
				}
			}
		}
	} else if (isPathSeparator(code)) {
		ret.root = ret.dir = path;
		ret.base = "\\";
		return ret;
	}
	if (rootEnd > 0) ret.root = path.slice(0, rootEnd);
	let startDot = -1;
	let startPart = rootEnd;
	let end = -1;
	let matchedSlash = true;
	let i = path.length - 1;
	let preDotState = 0;
	for (; i >= rootEnd; --i) {
		code = path.charCodeAt(i);
		if (isPathSeparator(code)) {
			if (!matchedSlash) {
				startPart = i + 1;
				break;
			}
			continue;
		}
		if (end === -1) {
			matchedSlash = false;
			end = i + 1;
		}
		if (code === CHAR_DOT) {
			if (startDot === -1) startDot = i;
			else if (preDotState !== 1) preDotState = 1;
		} else if (startDot !== -1) preDotState = -1;
	}
	if (startDot === -1 || end === -1 || preDotState === 0 || preDotState === 1 && startDot === end - 1 && startDot === startPart + 1) {
		if (end !== -1) ret.base = ret.name = path.slice(startPart, end);
	} else {
		ret.name = path.slice(startPart, startDot);
		ret.base = path.slice(startPart, end);
		ret.ext = path.slice(startDot, end);
	}
	ret.base = ret.base || "\\";
	if (startPart > 0 && startPart !== rootEnd) ret.dir = path.slice(0, startPart - 1);
	else ret.dir = ret.root;
	return ret;
}
/**
* Resolves path segments into a `path`.
*
* @example Usage
* ```ts
* import { resolve } from "@std/path/windows/resolve";
* import { assertEquals } from "@std/assert";
*
* const resolved = resolve("C:\\foo\\bar", "..\\baz");
* assertEquals(resolved, "C:\\foo\\baz");
* ```
*
* @param pathSegments The path segments to process to path
* @returns The resolved path
*/ function resolve(...pathSegments) {
	let resolvedDevice = "";
	let resolvedTail = "";
	let resolvedAbsolute = false;
	for (let i = pathSegments.length - 1; i >= -1; i--) {
		let path;
		const { Deno } = globalThis;
		if (i >= 0) path = pathSegments[i];
		else if (!resolvedDevice) {
			if (typeof Deno?.cwd !== "function") throw new TypeError("Resolved a drive-letter-less path without a current working directory (CWD)");
			path = Deno.cwd();
		} else {
			if (typeof Deno?.env?.get !== "function" || typeof Deno?.cwd !== "function") throw new TypeError("Resolved a relative path without a current working directory (CWD)");
			path = Deno.cwd();
			if (path === void 0 || path.slice(0, 3).toLowerCase() !== `${resolvedDevice.toLowerCase()}\\`) path = `${resolvedDevice}\\`;
		}
		assertPath(path);
		const len = path.length;
		if (len === 0) continue;
		let rootEnd = 0;
		let device = "";
		let isAbsolute = false;
		const code = path.charCodeAt(0);
		if (len > 1) {
			if (isPathSeparator(code)) {
				isAbsolute = true;
				if (isPathSeparator(path.charCodeAt(1))) {
					let j = 2;
					let last = j;
					for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
					if (j < len && j !== last) {
						const firstPart = path.slice(last, j);
						last = j;
						for (; j < len; ++j) if (!isPathSeparator(path.charCodeAt(j))) break;
						if (j < len && j !== last) {
							last = j;
							for (; j < len; ++j) if (isPathSeparator(path.charCodeAt(j))) break;
							if (j === len) {
								device = `\\\\${firstPart}\\${path.slice(last)}`;
								rootEnd = j;
							} else if (j !== last) {
								device = `\\\\${firstPart}\\${path.slice(last, j)}`;
								rootEnd = j;
							}
						}
					}
				} else rootEnd = 1;
			} else if (isWindowsDeviceRoot(code)) {
				if (path.charCodeAt(1) === CHAR_COLON) {
					device = path.slice(0, 2);
					rootEnd = 2;
					if (len > 2) {
						if (isPathSeparator(path.charCodeAt(2))) {
							isAbsolute = true;
							rootEnd = 3;
						}
					}
				}
			}
		} else if (isPathSeparator(code)) {
			rootEnd = 1;
			isAbsolute = true;
		}
		if (device.length > 0 && resolvedDevice.length > 0 && device.toLowerCase() !== resolvedDevice.toLowerCase()) continue;
		if (resolvedDevice.length === 0 && device.length > 0) resolvedDevice = device;
		if (!resolvedAbsolute) {
			resolvedTail = `${path.slice(rootEnd)}\\${resolvedTail}`;
			resolvedAbsolute = isAbsolute;
		}
		if (resolvedAbsolute && resolvedDevice.length > 0) break;
	}
	resolvedTail = normalizeString(resolvedTail, !resolvedAbsolute, "\\", isPathSeparator);
	return resolvedDevice + (resolvedAbsolute ? "\\" : "") + resolvedTail || ".";
}
function assertArgs(from, to) {
	assertPath(from);
	assertPath(to);
	if (from === to) return "";
}
/**
* Return the relative path from `from` to `to` based on current working directory.
*
* An example in windows, for instance:
*  from = 'C:\\orandea\\test\\aaa'
*  to = 'C:\\orandea\\impl\\bbb'
* The output of the function should be: '..\\..\\impl\\bbb'
*
* @example Usage
* ```ts
* import { relative } from "@std/path/windows/relative";
* import { assertEquals } from "@std/assert";
*
* const relativePath = relative("C:\\foobar\\test\\aaa", "C:\\foobar\\impl\\bbb");
* assertEquals(relativePath, "..\\..\\impl\\bbb");
* ```
*
* @param from The path from which to calculate the relative path
* @param to The path to which to calculate the relative path
* @returns The relative path from `from` to `to`
*/ function relative(from, to) {
	assertArgs(from, to);
	const fromOrig = resolve(from);
	const toOrig = resolve(to);
	if (fromOrig === toOrig) return "";
	from = fromOrig.toLowerCase();
	to = toOrig.toLowerCase();
	if (from === to) return "";
	let fromStart = 0;
	let fromEnd = from.length;
	for (; fromStart < fromEnd; ++fromStart) if (from.charCodeAt(fromStart) !== CHAR_BACKWARD_SLASH) break;
	for (; fromEnd - 1 > fromStart; --fromEnd) if (from.charCodeAt(fromEnd - 1) !== CHAR_BACKWARD_SLASH) break;
	const fromLen = fromEnd - fromStart;
	let toStart = 0;
	let toEnd = to.length;
	for (; toStart < toEnd; ++toStart) if (to.charCodeAt(toStart) !== CHAR_BACKWARD_SLASH) break;
	for (; toEnd - 1 > toStart; --toEnd) if (to.charCodeAt(toEnd - 1) !== CHAR_BACKWARD_SLASH) break;
	const toLen = toEnd - toStart;
	const length = fromLen < toLen ? fromLen : toLen;
	let lastCommonSep = -1;
	let i = 0;
	for (; i <= length; ++i) {
		if (i === length) {
			if (toLen > length) {
				if (to.charCodeAt(toStart + i) === CHAR_BACKWARD_SLASH) return toOrig.slice(toStart + i + 1);
				else if (i === 2) return toOrig.slice(toStart + i);
			}
			if (fromLen > length) {
				if (from.charCodeAt(fromStart + i) === CHAR_BACKWARD_SLASH) lastCommonSep = i;
				else if (i === 2) lastCommonSep = 3;
			}
			break;
		}
		const fromCode = from.charCodeAt(fromStart + i);
		if (fromCode !== to.charCodeAt(toStart + i)) break;
		else if (fromCode === CHAR_BACKWARD_SLASH) lastCommonSep = i;
	}
	if (i !== length && lastCommonSep === -1) return toOrig;
	let out = "";
	if (lastCommonSep === -1) lastCommonSep = 0;
	for (i = fromStart + lastCommonSep + 1; i <= fromEnd; ++i) if (i === fromEnd || from.charCodeAt(i) === CHAR_BACKWARD_SLASH) if (out.length === 0) out += "..";
	else out += "\\..";
	if (out.length > 0) return out + toOrig.slice(toStart + lastCommonSep, toEnd);
	else {
		toStart += lastCommonSep;
		if (toOrig.charCodeAt(toStart) === CHAR_BACKWARD_SLASH) ++toStart;
		return toOrig.slice(toStart, toEnd);
	}
}
const WHITESPACE_ENCODINGS = {
	"	": "%09",
	"\n": "%0A",
	"\v": "%0B",
	"\f": "%0C",
	"\r": "%0D",
	" ": "%20"
};
function encodeWhitespace(string) {
	return string.replaceAll(/[\s]/g, (c) => {
		return WHITESPACE_ENCODINGS[c] ?? c;
	});
}
/**
* Converts a path string to a file URL.
*
* @example Usage
* ```ts
* import { toFileUrl } from "@std/path/windows/to-file-url";
* import { assertEquals } from "@std/assert";
*
* assertEquals(toFileUrl("\\home\\foo"), new URL("file:///home/foo"));
* assertEquals(toFileUrl("C:\\Users\\foo"), new URL("file:///C:/Users/foo"));
* assertEquals(toFileUrl("\\\\127.0.0.1\\home\\foo"), new URL("file://127.0.0.1/home/foo"));
* ```
* @param path The path to convert.
* @returns The file URL.
*/ function toFileUrl(path) {
	if (!isAbsolute(path)) throw new TypeError(`Path must be absolute: received "${path}"`);
	const [, hostname, pathname] = path.match(/^(?:[/\\]{2}([^/\\]+)(?=[/\\](?:[^/\\]|$)))?(.*)/);
	const url = new URL("file:///");
	url.pathname = encodeWhitespace(pathname.replace(/%/g, "%25"));
	if (hostname !== void 0 && hostname !== "localhost") {
		url.hostname = hostname;
		if (!url.hostname) throw new TypeError(`Invalid hostname: "${url.hostname}"`);
	}
	return url;
}
/**
* Resolves path to a namespace path
*
* @example Usage
* ```ts
* import { toNamespacedPath } from "@std/path/windows/to-namespaced-path";
* import { assertEquals } from "@std/assert";
*
* const namespaced = toNamespacedPath("C:\\foo\\bar");
* assertEquals(namespaced, "\\\\?\\C:\\foo\\bar");
* ```
*
* @param path The path to resolve to namespaced path
* @returns The resolved namespaced path
*/ function toNamespacedPath(path) {
	if (typeof path !== "string") return path;
	if (path.length === 0) return "";
	const resolvedPath = resolve(path);
	if (resolvedPath.length >= 3) {
		if (resolvedPath.charCodeAt(0) === CHAR_BACKWARD_SLASH) {
			if (resolvedPath.charCodeAt(1) === CHAR_BACKWARD_SLASH) {
				const code = resolvedPath.charCodeAt(2);
				if (code !== CHAR_QUESTION_MARK && code !== CHAR_DOT) return `\\\\?\\UNC\\${resolvedPath.slice(2)}`;
			}
		} else if (isWindowsDeviceRoot(resolvedPath.charCodeAt(0))) {
			if (resolvedPath.charCodeAt(1) === CHAR_COLON && resolvedPath.charCodeAt(2) === CHAR_BACKWARD_SLASH) return `\\\\?\\${resolvedPath}`;
		}
	}
	return path;
}
function common$1(paths, sep) {
	const [first = "", ...remaining] = paths;
	const parts = first.split(sep);
	let endOfPrefix = parts.length;
	let append = "";
	for (const path of remaining) {
		const compare = path.split(sep);
		if (compare.length <= endOfPrefix) {
			endOfPrefix = compare.length;
			append = "";
		}
		for (let i = 0; i < endOfPrefix; i++) if (compare[i] !== parts[i]) {
			endOfPrefix = i;
			append = i === 0 ? "" : sep;
			break;
		}
	}
	return parts.slice(0, endOfPrefix).join(sep) + append;
}
/**
* Determines the common path from a set of paths for Windows systems.
*
* @example Usage
* ```ts
* import { common } from "@std/path/windows/common";
* import { assertEquals } from "@std/assert";
*
* const path = common([
*   "C:\\foo\\bar",
*   "C:\\foo\\baz",
* ]);
* assertEquals(path, "C:\\foo\\");
* ```
*
* @param paths The paths to compare.
* @returns The common path.
*/ function common(paths) {
	return common$1(paths, SEPARATOR);
}
/**
* Options for {@linkcode globToRegExp}, {@linkcode joinGlobs},
* {@linkcode normalizeGlob} and {@linkcode expandGlob}.
*/ const REG_EXP_ESCAPE_CHARS = [
	"!",
	"$",
	"(",
	")",
	"*",
	"+",
	".",
	"=",
	"?",
	"[",
	"\\",
	"^",
	"{",
	"|"
];
const RANGE_ESCAPE_CHARS = [
	"-",
	"\\",
	"]"
];
function _globToRegExp(c, glob, { extended = true, globstar: globstarOption = true, caseInsensitive = false } = {}) {
	if (glob === "") return /(?!)/;
	let newLength = glob.length;
	for (; newLength > 1 && c.seps.includes(glob[newLength - 1]); newLength--);
	glob = glob.slice(0, newLength);
	let regExpString = "";
	for (let j = 0; j < glob.length;) {
		let segment = "";
		const groupStack = [];
		let inRange = false;
		let inEscape = false;
		let endsWithSep = false;
		let i = j;
		for (; i < glob.length && !(c.seps.includes(glob[i]) && groupStack.length === 0); i++) {
			if (inEscape) {
				inEscape = false;
				segment += (inRange ? RANGE_ESCAPE_CHARS : REG_EXP_ESCAPE_CHARS).includes(glob[i]) ? `\\${glob[i]}` : glob[i];
				continue;
			}
			if (glob[i] === c.escapePrefix) {
				inEscape = true;
				continue;
			}
			if (glob[i] === "[") {
				if (!inRange) {
					inRange = true;
					segment += "[";
					if (glob[i + 1] === "!") {
						i++;
						segment += "^";
					} else if (glob[i + 1] === "^") {
						i++;
						segment += "\\^";
					}
					continue;
				} else if (glob[i + 1] === ":") {
					let k = i + 1;
					let value = "";
					while (glob[k + 1] !== void 0 && glob[k + 1] !== ":") {
						value += glob[k + 1];
						k++;
					}
					if (glob[k + 1] === ":" && glob[k + 2] === "]") {
						i = k + 2;
						if (value === "alnum") segment += "\\dA-Za-z";
						else if (value === "alpha") segment += "A-Za-z";
						else if (value === "ascii") segment += "\0-";
						else if (value === "blank") segment += "	 ";
						else if (value === "cntrl") segment += "\0-";
						else if (value === "digit") segment += "\\d";
						else if (value === "graph") segment += "!-~";
						else if (value === "lower") segment += "a-z";
						else if (value === "print") segment += " -~";
						else if (value === "punct") segment += "!\"#$%&'()*+,\\-./:;<=>?@[\\\\\\]^_‘{|}~";
						else if (value === "space") segment += "\\s\v";
						else if (value === "upper") segment += "A-Z";
						else if (value === "word") segment += "\\w";
						else if (value === "xdigit") segment += "\\dA-Fa-f";
						continue;
					}
				}
			}
			if (glob[i] === "]" && inRange) {
				inRange = false;
				segment += "]";
				continue;
			}
			if (inRange) {
				segment += glob[i];
				continue;
			}
			if (glob[i] === ")" && groupStack.length > 0 && groupStack[groupStack.length - 1] !== "BRACE") {
				segment += ")";
				const type = groupStack.pop();
				if (type === "!") segment += c.wildcard;
				else if (type !== "@") segment += type;
				continue;
			}
			if (glob[i] === "|" && groupStack.length > 0 && groupStack[groupStack.length - 1] !== "BRACE") {
				segment += "|";
				continue;
			}
			if (glob[i] === "+" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("+");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "@" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("@");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "?") {
				if (extended && glob[i + 1] === "(") {
					i++;
					groupStack.push("?");
					segment += "(?:";
				} else segment += ".";
				continue;
			}
			if (glob[i] === "!" && extended && glob[i + 1] === "(") {
				i++;
				groupStack.push("!");
				segment += "(?!";
				continue;
			}
			if (glob[i] === "{") {
				groupStack.push("BRACE");
				segment += "(?:";
				continue;
			}
			if (glob[i] === "}" && groupStack[groupStack.length - 1] === "BRACE") {
				groupStack.pop();
				segment += ")";
				continue;
			}
			if (glob[i] === "," && groupStack[groupStack.length - 1] === "BRACE") {
				segment += "|";
				continue;
			}
			if (glob[i] === "*") {
				if (extended && glob[i + 1] === "(") {
					i++;
					groupStack.push("*");
					segment += "(?:";
				} else {
					const prevChar = glob[i - 1];
					let numStars = 1;
					while (glob[i + 1] === "*") {
						i++;
						numStars++;
					}
					const nextChar = glob[i + 1];
					if (globstarOption && numStars === 2 && [...c.seps, void 0].includes(prevChar) && [...c.seps, void 0].includes(nextChar)) {
						segment += c.globstar;
						endsWithSep = true;
					} else segment += c.wildcard;
				}
				continue;
			}
			segment += REG_EXP_ESCAPE_CHARS.includes(glob[i]) ? `\\${glob[i]}` : glob[i];
		}
		if (groupStack.length > 0 || inRange || inEscape) {
			segment = "";
			for (const c of glob.slice(j, i)) {
				segment += REG_EXP_ESCAPE_CHARS.includes(c) ? `\\${c}` : c;
				endsWithSep = false;
			}
		}
		regExpString += segment;
		if (!endsWithSep) {
			regExpString += i < glob.length ? c.sep : c.sepMaybe;
			endsWithSep = true;
		}
		while (c.seps.includes(glob[i])) i++;
		j = i;
	}
	regExpString = `^${regExpString}$`;
	return new RegExp(regExpString, caseInsensitive ? "i" : "");
}
const constants$1 = {
	sep: "(?:\\\\|/)+",
	sepMaybe: "(?:\\\\|/)*",
	seps: ["\\", "/"],
	globstar: "(?:[^\\\\/]*(?:\\\\|/|$)+)*",
	wildcard: "[^\\\\/]*",
	escapePrefix: "`"
};
/** Convert a glob string to a regular expression.
*
* Tries to match bash glob expansion as closely as possible.
*
* Basic glob syntax:
* - `*` - Matches everything without leaving the path segment.
* - `?` - Matches any single character.
* - `{foo,bar}` - Matches `foo` or `bar`.
* - `[abcd]` - Matches `a`, `b`, `c` or `d`.
* - `[a-d]` - Matches `a`, `b`, `c` or `d`.
* - `[!abcd]` - Matches any single character besides `a`, `b`, `c` or `d`.
* - `[[:<class>:]]` - Matches any character belonging to `<class>`.
*     - `[[:alnum:]]` - Matches any digit or letter.
*     - `[[:digit:]abc]` - Matches any digit, `a`, `b` or `c`.
*     - See https://facelessuser.github.io/wcmatch/glob/#posix-character-classes
*       for a complete list of supported character classes.
* - `\` - Escapes the next character for an `os` other than `"windows"`.
* - \` - Escapes the next character for `os` set to `"windows"`.
* - `/` - Path separator.
* - `\` - Additional path separator only for `os` set to `"windows"`.
*
* Extended syntax:
* - Requires `{ extended: true }`.
* - `?(foo|bar)` - Matches 0 or 1 instance of `{foo,bar}`.
* - `@(foo|bar)` - Matches 1 instance of `{foo,bar}`. They behave the same.
* - `*(foo|bar)` - Matches _n_ instances of `{foo,bar}`.
* - `+(foo|bar)` - Matches _n > 0_ instances of `{foo,bar}`.
* - `!(foo|bar)` - Matches anything other than `{foo,bar}`.
* - See https://www.linuxjournal.com/content/bash-extended-globbing.
*
* Globstar syntax:
* - Requires `{ globstar: true }`.
* - `**` - Matches any number of any path segments.
*     - Must comprise its entire path segment in the provided glob.
* - See https://www.linuxjournal.com/content/globstar-new-bash-globbing-option.
*
* Note the following properties:
* - The generated `RegExp` is anchored at both start and end.
* - Repeating and trailing separators are tolerated. Trailing separators in the
*   provided glob have no meaning and are discarded.
* - Absolute globs will only match absolute paths, etc.
* - Empty globs will match nothing.
* - Any special glob syntax must be contained to one path segment. For example,
*   `?(foo|bar/baz)` is invalid. The separator will take precedence and the
*   first segment ends with an unclosed group.
* - If a path segment ends with unclosed groups or a dangling escape prefix, a
*   parse error has occurred. Every character for that segment is taken
*   literally in this event.
*
* Limitations:
* - A negative group like `!(foo|bar)` will wrongly be converted to a negative
*   look-ahead followed by a wildcard. This means that `!(foo).js` will wrongly
*   fail to match `foobar.js`, even though `foobar` is not `foo`. Effectively,
*   `!(foo|bar)` is treated like `!(@(foo|bar)*)`. This will work correctly if
*   the group occurs not nested at the end of the segment.
*
* @example Usage
* ```ts
* import { globToRegExp } from "@std/path/windows/glob-to-regexp";
* import { assertEquals } from "@std/assert";
*
* assertEquals(globToRegExp("*.js"), /^[^\\/]*\.js(?:\\|\/)*$/);
* ```
*
* @param glob Glob string to convert.
* @param options Conversion options.
* @returns The regular expression equivalent to the glob.
*/ function globToRegExp(glob, options = {}) {
	return _globToRegExp(constants$1, glob, options);
}
/**
* Test whether the given string is a glob.
*
* @example Usage
* ```ts
* import { isGlob } from "@std/path/is-glob";
* import { assert } from "@std/assert";
*
* assert(!isGlob("foo/bar/../baz"));
* assert(isGlob("foo/*ar/../baz"));
* ```
*
* @param str String to test.
* @returns `true` if the given string is a glob, otherwise `false`
*/ function isGlob(str) {
	const chars = {
		"{": "}",
		"(": ")",
		"[": "]"
	};
	const regex = /\\(.)|(^!|\*|\?|[\].+)]\?|\[[^[\\\]]+\]|\{[^{\\}]+\}|\(\?[:!=][^\\)]+\)|\([^(|]+\|[^\\)]+\)|@\([^)]+\))/;
	if (str === "") return false;
	let match;
	while (match = regex.exec(str)) {
		if (match[2]) return true;
		let idx = match.index + match[0].length;
		const open = match[1];
		const close = open ? chars[open] : null;
		if (open && close) {
			const n = str.indexOf(close, idx);
			if (n !== -1) idx = n + 1;
		}
		str = str.slice(idx);
	}
	return false;
}
/**
* Like normalize(), but doesn't collapse "**\/.." when `globstar` is true.
*
* @example Usage
* ```ts
* import { normalizeGlob } from "@std/path/windows/normalize-glob";
* import { assertEquals } from "@std/assert";
*
* const normalized = normalizeGlob("**\\foo\\..\\bar", { globstar: true });
* assertEquals(normalized, "**\\bar");
* ```
*
* @param glob The glob pattern to normalize.
* @param options The options for glob pattern.
* @returns The normalized glob pattern.
*/ function normalizeGlob(glob, options = {}) {
	const { globstar = false } = options;
	if (glob.match(/\0/g)) throw new Error(`Glob contains invalid characters: "${glob}"`);
	if (!globstar) return normalize$1(glob);
	const s = SEPARATOR_PATTERN.source;
	const badParentPattern = new RegExp(`(?<=(${s}|^)\\*\\*${s})\\.\\.(?=${s}|$)`, "g");
	return normalize$1(glob.replace(badParentPattern, "\0")).replace(/\0/g, "..");
}
/**
* Like join(), but doesn't collapse "**\/.." when `globstar` is true.
*
* @example Usage
*
* ```ts
* import { joinGlobs } from "@std/path/windows/join-globs";
* import { assertEquals } from "@std/assert";
*
* const joined = joinGlobs(["foo", "**", "bar"], { globstar: true });
* assertEquals(joined, "foo\\**\\bar");
* ```
*
* @param globs The globs to join.
* @param options The options for glob pattern.
* @returns The joined glob pattern.
*/ function joinGlobs(globs, options = {}) {
	const { globstar = false } = options;
	if (!globstar || globs.length === 0) return join(...globs);
	let joined;
	for (const glob of globs) {
		const path = glob;
		if (path.length > 0) if (!joined) joined = path;
		else joined += `${SEPARATOR}${path}`;
	}
	if (!joined) return ".";
	return normalizeGlob(joined, { globstar });
}

//#endregion
//#region node_modules/.pnpm/balanced-match@4.0.4/node_modules/balanced-match/dist/esm/index.js
const balanced = (a, b, str) => {
	const ma = a instanceof RegExp ? maybeMatch(a, str) : a;
	const mb = b instanceof RegExp ? maybeMatch(b, str) : b;
	const r = ma !== null && mb != null && range(ma, mb, str);
	return r && {
		start: r[0],
		end: r[1],
		pre: str.slice(0, r[0]),
		body: str.slice(r[0] + ma.length, r[1]),
		post: str.slice(r[1] + mb.length)
	};
};
const maybeMatch = (reg, str) => {
	const m = str.match(reg);
	return m ? m[0] : null;
};
const range = (a, b, str) => {
	let begs, beg, left, right = void 0, result;
	let ai = str.indexOf(a);
	let bi = str.indexOf(b, ai + 1);
	let i = ai;
	if (ai >= 0 && bi > 0) {
		if (a === b) return [ai, bi];
		begs = [];
		left = str.length;
		while (i >= 0 && !result) {
			if (i === ai) {
				begs.push(i);
				ai = str.indexOf(a, i + 1);
			} else if (begs.length === 1) {
				const r = begs.pop();
				if (r !== void 0) result = [r, bi];
			} else {
				beg = begs.pop();
				if (beg !== void 0 && beg < left) {
					left = beg;
					right = bi;
				}
				bi = str.indexOf(b, i + 1);
			}
			i = ai < bi && ai >= 0 ? ai : bi;
		}
		if (begs.length && right !== void 0) result = [left, right];
	}
	return result;
};

//#endregion
//#region node_modules/.pnpm/brace-expansion@5.0.4/node_modules/brace-expansion/dist/esm/index.js
const escSlash = "\0SLASH" + Math.random() + "\0";
const escOpen = "\0OPEN" + Math.random() + "\0";
const escClose = "\0CLOSE" + Math.random() + "\0";
const escComma = "\0COMMA" + Math.random() + "\0";
const escPeriod = "\0PERIOD" + Math.random() + "\0";
const escSlashPattern = new RegExp(escSlash, "g");
const escOpenPattern = new RegExp(escOpen, "g");
const escClosePattern = new RegExp(escClose, "g");
const escCommaPattern = new RegExp(escComma, "g");
const escPeriodPattern = new RegExp(escPeriod, "g");
const slashPattern = /\\\\/g;
const openPattern = /\\{/g;
const closePattern = /\\}/g;
const commaPattern = /\\,/g;
const periodPattern = /\\\./g;
const EXPANSION_MAX = 1e5;
function numeric(str) {
	return !isNaN(str) ? parseInt(str, 10) : str.charCodeAt(0);
}
function escapeBraces(str) {
	return str.replace(slashPattern, escSlash).replace(openPattern, escOpen).replace(closePattern, escClose).replace(commaPattern, escComma).replace(periodPattern, escPeriod);
}
function unescapeBraces(str) {
	return str.replace(escSlashPattern, "\\").replace(escOpenPattern, "{").replace(escClosePattern, "}").replace(escCommaPattern, ",").replace(escPeriodPattern, ".");
}
/**
* Basically just str.split(","), but handling cases
* where we have nested braced sections, which should be
* treated as individual members, like {a,{b,c},d}
*/
function parseCommaParts(str) {
	if (!str) return [""];
	const parts = [];
	const m = balanced("{", "}", str);
	if (!m) return str.split(",");
	const { pre, body, post } = m;
	const p = pre.split(",");
	p[p.length - 1] += "{" + body + "}";
	const postParts = parseCommaParts(post);
	if (post.length) {
		p[p.length - 1] += postParts.shift();
		p.push.apply(p, postParts);
	}
	parts.push.apply(parts, p);
	return parts;
}
function expand(str, options = {}) {
	if (!str) return [];
	const { max = EXPANSION_MAX } = options;
	if (str.slice(0, 2) === "{}") str = "\\{\\}" + str.slice(2);
	return expand_(escapeBraces(str), max, true).map(unescapeBraces);
}
function embrace(str) {
	return "{" + str + "}";
}
function isPadded(el) {
	return /^-?0\d/.test(el);
}
function lte(i, y) {
	return i <= y;
}
function gte(i, y) {
	return i >= y;
}
function expand_(str, max, isTop) {
	/** @type {string[]} */
	const expansions = [];
	const m = balanced("{", "}", str);
	if (!m) return [str];
	const pre = m.pre;
	const post = m.post.length ? expand_(m.post, max, false) : [""];
	if (/\$$/.test(m.pre)) for (let k = 0; k < post.length && k < max; k++) {
		const expansion = pre + "{" + m.body + "}" + post[k];
		expansions.push(expansion);
	}
	else {
		const isNumericSequence = /^-?\d+\.\.-?\d+(?:\.\.-?\d+)?$/.test(m.body);
		const isAlphaSequence = /^[a-zA-Z]\.\.[a-zA-Z](?:\.\.-?\d+)?$/.test(m.body);
		const isSequence = isNumericSequence || isAlphaSequence;
		const isOptions = m.body.indexOf(",") >= 0;
		if (!isSequence && !isOptions) {
			if (m.post.match(/,(?!,).*\}/)) {
				str = m.pre + "{" + m.body + escClose + m.post;
				return expand_(str, max, true);
			}
			return [str];
		}
		let n;
		if (isSequence) n = m.body.split(/\.\./);
		else {
			n = parseCommaParts(m.body);
			if (n.length === 1 && n[0] !== void 0) {
				n = expand_(n[0], max, false).map(embrace);
				/* c8 ignore start */
				if (n.length === 1) return post.map((p) => m.pre + n[0] + p);
			}
		}
		let N;
		if (isSequence && n[0] !== void 0 && n[1] !== void 0) {
			const x = numeric(n[0]);
			const y = numeric(n[1]);
			const width = Math.max(n[0].length, n[1].length);
			let incr = n.length === 3 && n[2] !== void 0 ? Math.abs(numeric(n[2])) : 1;
			let test = lte;
			if (y < x) {
				incr *= -1;
				test = gte;
			}
			const pad = n.some(isPadded);
			N = [];
			for (let i = x; test(i, y); i += incr) {
				let c;
				if (isAlphaSequence) {
					c = String.fromCharCode(i);
					if (c === "\\") c = "";
				} else {
					c = String(i);
					if (pad) {
						const need = width - c.length;
						if (need > 0) {
							const z = new Array(need + 1).join("0");
							if (i < 0) c = "-" + z + c.slice(1);
							else c = z + c;
						}
					}
				}
				N.push(c);
			}
		} else {
			N = [];
			for (let j = 0; j < n.length; j++) N.push.apply(N, expand_(n[j], max, false));
		}
		for (let j = 0; j < N.length; j++) for (let k = 0; k < post.length && expansions.length < max; k++) {
			const expansion = pre + N[j] + post[k];
			if (!isTop || isSequence || expansion) expansions.push(expansion);
		}
	}
	return expansions;
}

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/assert-valid-pattern.js
const MAX_PATTERN_LENGTH = 1024 * 64;
const assertValidPattern = (pattern) => {
	if (typeof pattern !== "string") throw new TypeError("invalid pattern");
	if (pattern.length > MAX_PATTERN_LENGTH) throw new TypeError("pattern is too long");
};

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/brace-expressions.js
const posixClasses = {
	"[:alnum:]": ["\\p{L}\\p{Nl}\\p{Nd}", true],
	"[:alpha:]": ["\\p{L}\\p{Nl}", true],
	"[:ascii:]": ["\\x00-\\x7f", false],
	"[:blank:]": ["\\p{Zs}\\t", true],
	"[:cntrl:]": ["\\p{Cc}", true],
	"[:digit:]": ["\\p{Nd}", true],
	"[:graph:]": [
		"\\p{Z}\\p{C}",
		true,
		true
	],
	"[:lower:]": ["\\p{Ll}", true],
	"[:print:]": ["\\p{C}", true],
	"[:punct:]": ["\\p{P}", true],
	"[:space:]": ["\\p{Z}\\t\\r\\n\\v\\f", true],
	"[:upper:]": ["\\p{Lu}", true],
	"[:word:]": ["\\p{L}\\p{Nl}\\p{Nd}\\p{Pc}", true],
	"[:xdigit:]": ["A-Fa-f0-9", false]
};
const braceEscape = (s) => s.replace(/[[\]\\-]/g, "\\$&");
const regexpEscape = (s) => s.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
const rangesToString = (ranges) => ranges.join("");
const parseClass = (glob, position) => {
	const pos = position;
	/* c8 ignore start */
	if (glob.charAt(pos) !== "[") throw new Error("not in a brace expression");
	/* c8 ignore stop */
	const ranges = [];
	const negs = [];
	let i = pos + 1;
	let sawStart = false;
	let uflag = false;
	let escaping = false;
	let negate = false;
	let endPos = pos;
	let rangeStart = "";
	WHILE: while (i < glob.length) {
		const c = glob.charAt(i);
		if ((c === "!" || c === "^") && i === pos + 1) {
			negate = true;
			i++;
			continue;
		}
		if (c === "]" && sawStart && !escaping) {
			endPos = i + 1;
			break;
		}
		sawStart = true;
		if (c === "\\") {
			if (!escaping) {
				escaping = true;
				i++;
				continue;
			}
		}
		if (c === "[" && !escaping) {
			for (const [cls, [unip, u, neg]] of Object.entries(posixClasses)) if (glob.startsWith(cls, i)) {
				if (rangeStart) return [
					"$.",
					false,
					glob.length - pos,
					true
				];
				i += cls.length;
				if (neg) negs.push(unip);
				else ranges.push(unip);
				uflag = uflag || u;
				continue WHILE;
			}
		}
		escaping = false;
		if (rangeStart) {
			if (c > rangeStart) ranges.push(braceEscape(rangeStart) + "-" + braceEscape(c));
			else if (c === rangeStart) ranges.push(braceEscape(c));
			rangeStart = "";
			i++;
			continue;
		}
		if (glob.startsWith("-]", i + 1)) {
			ranges.push(braceEscape(c + "-"));
			i += 2;
			continue;
		}
		if (glob.startsWith("-", i + 1)) {
			rangeStart = c;
			i += 2;
			continue;
		}
		ranges.push(braceEscape(c));
		i++;
	}
	if (endPos < i) return [
		"",
		false,
		0,
		false
	];
	if (!ranges.length && !negs.length) return [
		"$.",
		false,
		glob.length - pos,
		true
	];
	if (negs.length === 0 && ranges.length === 1 && /^\\?.$/.test(ranges[0]) && !negate) return [
		regexpEscape(ranges[0].length === 2 ? ranges[0].slice(-1) : ranges[0]),
		false,
		endPos - pos,
		false
	];
	const sranges = "[" + (negate ? "^" : "") + rangesToString(ranges) + "]";
	const snegs = "[" + (negate ? "" : "^") + rangesToString(negs) + "]";
	return [
		ranges.length && negs.length ? "(" + sranges + "|" + snegs + ")" : ranges.length ? sranges : snegs,
		uflag,
		endPos - pos,
		true
	];
};

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/unescape.js
/**
* Un-escape a string that has been escaped with {@link escape}.
*
* If the {@link MinimatchOptions.windowsPathsNoEscape} option is used, then
* square-bracket escapes are removed, but not backslash escapes.
*
* For example, it will turn the string `'[*]'` into `*`, but it will not
* turn `'\\*'` into `'*'`, because `\` is a path separator in
* `windowsPathsNoEscape` mode.
*
* When `windowsPathsNoEscape` is not set, then both square-bracket escapes and
* backslash escapes are removed.
*
* Slashes (and backslashes in `windowsPathsNoEscape` mode) cannot be escaped
* or unescaped.
*
* When `magicalBraces` is not set, escapes of braces (`{` and `}`) will not be
* unescaped.
*/
const unescape = (s, { windowsPathsNoEscape = false, magicalBraces = true } = {}) => {
	if (magicalBraces) return windowsPathsNoEscape ? s.replace(/\[([^\/\\])\]/g, "$1") : s.replace(/((?!\\).|^)\[([^\/\\])\]/g, "$1$2").replace(/\\([^\/])/g, "$1");
	return windowsPathsNoEscape ? s.replace(/\[([^\/\\{}])\]/g, "$1") : s.replace(/((?!\\).|^)\[([^\/\\{}])\]/g, "$1$2").replace(/\\([^\/{}])/g, "$1");
};

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/ast.js
var _a;
const types = new Set([
	"!",
	"?",
	"+",
	"*",
	"@"
]);
const isExtglobType = (c) => types.has(c);
const isExtglobAST = (c) => isExtglobType(c.type);
const adoptionMap = new Map([
	["!", ["@"]],
	["?", ["?", "@"]],
	["@", ["@"]],
	["*", [
		"*",
		"+",
		"?",
		"@"
	]],
	["+", ["+", "@"]]
]);
const adoptionWithSpaceMap = new Map([
	["!", ["?"]],
	["@", ["?"]],
	["+", ["?", "*"]]
]);
const adoptionAnyMap = new Map([
	["!", ["?", "@"]],
	["?", ["?", "@"]],
	["@", ["?", "@"]],
	["*", [
		"*",
		"+",
		"?",
		"@"
	]],
	["+", [
		"+",
		"@",
		"?",
		"*"
	]]
]);
const usurpMap = new Map([
	["!", new Map([["!", "@"]])],
	["?", new Map([["*", "*"], ["+", "*"]])],
	["@", new Map([
		["!", "!"],
		["?", "?"],
		["@", "@"],
		["*", "*"],
		["+", "+"]
	])],
	["+", new Map([["?", "*"], ["*", "*"]])]
]);
const startNoTraversal = "(?!(?:^|/)\\.\\.?(?:$|/))";
const startNoDot = "(?!\\.)";
const addPatternStart = new Set(["[", "."]);
const justDots = new Set(["..", "."]);
const reSpecials = /* @__PURE__ */ new Set("().*{}+?[]^$\\!");
const regExpEscape$1 = (s) => s.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
const qmark = "[^/]";
const star$1 = qmark + "*?";
const starNoEmpty = qmark + "+?";
let ID = 0;
var AST = class {
	type;
	#root;
	#hasMagic;
	#uflag = false;
	#parts = [];
	#parent;
	#parentIndex;
	#negs;
	#filledNegs = false;
	#options;
	#toString;
	#emptyExt = false;
	id = ++ID;
	get depth() {
		return (this.#parent?.depth ?? -1) + 1;
	}
	[Symbol.for("nodejs.util.inspect.custom")]() {
		return {
			"@@type": "AST",
			id: this.id,
			type: this.type,
			root: this.#root.id,
			parent: this.#parent?.id,
			depth: this.depth,
			partsLength: this.#parts.length,
			parts: this.#parts
		};
	}
	constructor(type, parent, options = {}) {
		this.type = type;
		if (type) this.#hasMagic = true;
		this.#parent = parent;
		this.#root = this.#parent ? this.#parent.#root : this;
		this.#options = this.#root === this ? options : this.#root.#options;
		this.#negs = this.#root === this ? [] : this.#root.#negs;
		if (type === "!" && !this.#root.#filledNegs) this.#negs.push(this);
		this.#parentIndex = this.#parent ? this.#parent.#parts.length : 0;
	}
	get hasMagic() {
		/* c8 ignore start */
		if (this.#hasMagic !== void 0) return this.#hasMagic;
		/* c8 ignore stop */
		for (const p of this.#parts) {
			if (typeof p === "string") continue;
			if (p.type || p.hasMagic) return this.#hasMagic = true;
		}
		return this.#hasMagic;
	}
	toString() {
		if (this.#toString !== void 0) return this.#toString;
		if (!this.type) return this.#toString = this.#parts.map((p) => String(p)).join("");
		else return this.#toString = this.type + "(" + this.#parts.map((p) => String(p)).join("|") + ")";
	}
	#fillNegs() {
		/* c8 ignore start */
		if (this !== this.#root) throw new Error("should only call on root");
		if (this.#filledNegs) return this;
		/* c8 ignore stop */
		this.toString();
		this.#filledNegs = true;
		let n;
		while (n = this.#negs.pop()) {
			if (n.type !== "!") continue;
			let p = n;
			let pp = p.#parent;
			while (pp) {
				for (let i = p.#parentIndex + 1; !pp.type && i < pp.#parts.length; i++) for (const part of n.#parts) {
					/* c8 ignore start */
					if (typeof part === "string") throw new Error("string part in extglob AST??");
					/* c8 ignore stop */
					part.copyIn(pp.#parts[i]);
				}
				p = pp;
				pp = p.#parent;
			}
		}
		return this;
	}
	push(...parts) {
		for (const p of parts) {
			if (p === "") continue;
			/* c8 ignore start */
			if (typeof p !== "string" && !(p instanceof _a && p.#parent === this)) throw new Error("invalid part: " + p);
			/* c8 ignore stop */
			this.#parts.push(p);
		}
	}
	toJSON() {
		const ret = this.type === null ? this.#parts.slice().map((p) => typeof p === "string" ? p : p.toJSON()) : [this.type, ...this.#parts.map((p) => p.toJSON())];
		if (this.isStart() && !this.type) ret.unshift([]);
		if (this.isEnd() && (this === this.#root || this.#root.#filledNegs && this.#parent?.type === "!")) ret.push({});
		return ret;
	}
	isStart() {
		if (this.#root === this) return true;
		if (!this.#parent?.isStart()) return false;
		if (this.#parentIndex === 0) return true;
		const p = this.#parent;
		for (let i = 0; i < this.#parentIndex; i++) {
			const pp = p.#parts[i];
			if (!(pp instanceof _a && pp.type === "!")) return false;
		}
		return true;
	}
	isEnd() {
		if (this.#root === this) return true;
		if (this.#parent?.type === "!") return true;
		if (!this.#parent?.isEnd()) return false;
		if (!this.type) return this.#parent?.isEnd();
		/* c8 ignore start */
		const pl = this.#parent ? this.#parent.#parts.length : 0;
		/* c8 ignore stop */
		return this.#parentIndex === pl - 1;
	}
	copyIn(part) {
		if (typeof part === "string") this.push(part);
		else this.push(part.clone(this));
	}
	clone(parent) {
		const c = new _a(this.type, parent);
		for (const p of this.#parts) c.copyIn(p);
		return c;
	}
	static #parseAST(str, ast, pos, opt, extDepth) {
		const maxDepth = opt.maxExtglobRecursion ?? 2;
		let escaping = false;
		let inBrace = false;
		let braceStart = -1;
		let braceNeg = false;
		if (ast.type === null) {
			let i = pos;
			let acc = "";
			while (i < str.length) {
				const c = str.charAt(i++);
				if (escaping || c === "\\") {
					escaping = !escaping;
					acc += c;
					continue;
				}
				if (inBrace) {
					if (i === braceStart + 1) {
						if (c === "^" || c === "!") braceNeg = true;
					} else if (c === "]" && !(i === braceStart + 2 && braceNeg)) inBrace = false;
					acc += c;
					continue;
				} else if (c === "[") {
					inBrace = true;
					braceStart = i;
					braceNeg = false;
					acc += c;
					continue;
				}
				if (!opt.noext && isExtglobType(c) && str.charAt(i) === "(" && extDepth <= maxDepth) {
					ast.push(acc);
					acc = "";
					const ext = new _a(c, ast);
					i = _a.#parseAST(str, ext, i, opt, extDepth + 1);
					ast.push(ext);
					continue;
				}
				acc += c;
			}
			ast.push(acc);
			return i;
		}
		let i = pos + 1;
		let part = new _a(null, ast);
		const parts = [];
		let acc = "";
		while (i < str.length) {
			const c = str.charAt(i++);
			if (escaping || c === "\\") {
				escaping = !escaping;
				acc += c;
				continue;
			}
			if (inBrace) {
				if (i === braceStart + 1) {
					if (c === "^" || c === "!") braceNeg = true;
				} else if (c === "]" && !(i === braceStart + 2 && braceNeg)) inBrace = false;
				acc += c;
				continue;
			} else if (c === "[") {
				inBrace = true;
				braceStart = i;
				braceNeg = false;
				acc += c;
				continue;
			}
			/* c8 ignore stop */
			if (!opt.noext && isExtglobType(c) && str.charAt(i) === "(" && (extDepth <= maxDepth || ast && ast.#canAdoptType(c))) {
				const depthAdd = ast && ast.#canAdoptType(c) ? 0 : 1;
				part.push(acc);
				acc = "";
				const ext = new _a(c, part);
				part.push(ext);
				i = _a.#parseAST(str, ext, i, opt, extDepth + depthAdd);
				continue;
			}
			if (c === "|") {
				part.push(acc);
				acc = "";
				parts.push(part);
				part = new _a(null, ast);
				continue;
			}
			if (c === ")") {
				if (acc === "" && ast.#parts.length === 0) ast.#emptyExt = true;
				part.push(acc);
				acc = "";
				ast.push(...parts, part);
				return i;
			}
			acc += c;
		}
		ast.type = null;
		ast.#hasMagic = void 0;
		ast.#parts = [str.substring(pos - 1)];
		return i;
	}
	#canAdoptWithSpace(child) {
		return this.#canAdopt(child, adoptionWithSpaceMap);
	}
	#canAdopt(child, map = adoptionMap) {
		if (!child || typeof child !== "object" || child.type !== null || child.#parts.length !== 1 || this.type === null) return false;
		const gc = child.#parts[0];
		if (!gc || typeof gc !== "object" || gc.type === null) return false;
		return this.#canAdoptType(gc.type, map);
	}
	#canAdoptType(c, map = adoptionAnyMap) {
		return !!map.get(this.type)?.includes(c);
	}
	#adoptWithSpace(child, index) {
		const gc = child.#parts[0];
		const blank = new _a(null, gc, this.options);
		blank.#parts.push("");
		gc.push(blank);
		this.#adopt(child, index);
	}
	#adopt(child, index) {
		const gc = child.#parts[0];
		this.#parts.splice(index, 1, ...gc.#parts);
		for (const p of gc.#parts) if (typeof p === "object") p.#parent = this;
		this.#toString = void 0;
	}
	#canUsurpType(c) {
		return !!usurpMap.get(this.type)?.has(c);
	}
	#canUsurp(child) {
		if (!child || typeof child !== "object" || child.type !== null || child.#parts.length !== 1 || this.type === null || this.#parts.length !== 1) return false;
		const gc = child.#parts[0];
		if (!gc || typeof gc !== "object" || gc.type === null) return false;
		return this.#canUsurpType(gc.type);
	}
	#usurp(child) {
		const m = usurpMap.get(this.type);
		const gc = child.#parts[0];
		const nt = m?.get(gc.type);
		/* c8 ignore start - impossible */
		if (!nt) return false;
		/* c8 ignore stop */
		this.#parts = gc.#parts;
		for (const p of this.#parts) if (typeof p === "object") p.#parent = this;
		this.type = nt;
		this.#toString = void 0;
		this.#emptyExt = false;
	}
	static fromGlob(pattern, options = {}) {
		const ast = new _a(null, void 0, options);
		_a.#parseAST(pattern, ast, 0, options, 0);
		return ast;
	}
	toMMPattern() {
		/* c8 ignore start */
		if (this !== this.#root) return this.#root.toMMPattern();
		/* c8 ignore stop */
		const glob = this.toString();
		const [re, body, hasMagic, uflag] = this.toRegExpSource();
		if (!(hasMagic || this.#hasMagic || this.#options.nocase && !this.#options.nocaseMagicOnly && glob.toUpperCase() !== glob.toLowerCase())) return body;
		const flags = (this.#options.nocase ? "i" : "") + (uflag ? "u" : "");
		return Object.assign(new RegExp(`^${re}$`, flags), {
			_src: re,
			_glob: glob
		});
	}
	get options() {
		return this.#options;
	}
	toRegExpSource(allowDot) {
		const dot = allowDot ?? !!this.#options.dot;
		if (this.#root === this) {
			this.#flatten();
			this.#fillNegs();
		}
		if (!isExtglobAST(this)) {
			const noEmpty = this.isStart() && this.isEnd() && !this.#parts.some((s) => typeof s !== "string");
			const src = this.#parts.map((p) => {
				const [re, _, hasMagic, uflag] = typeof p === "string" ? _a.#parseGlob(p, this.#hasMagic, noEmpty) : p.toRegExpSource(allowDot);
				this.#hasMagic = this.#hasMagic || hasMagic;
				this.#uflag = this.#uflag || uflag;
				return re;
			}).join("");
			let start = "";
			if (this.isStart()) {
				if (typeof this.#parts[0] === "string") {
					if (!(this.#parts.length === 1 && justDots.has(this.#parts[0]))) {
						const aps = addPatternStart;
						const needNoTrav = dot && aps.has(src.charAt(0)) || src.startsWith("\\.") && aps.has(src.charAt(2)) || src.startsWith("\\.\\.") && aps.has(src.charAt(4));
						const needNoDot = !dot && !allowDot && aps.has(src.charAt(0));
						start = needNoTrav ? startNoTraversal : needNoDot ? startNoDot : "";
					}
				}
			}
			let end = "";
			if (this.isEnd() && this.#root.#filledNegs && this.#parent?.type === "!") end = "(?:$|\\/)";
			return [
				start + src + end,
				unescape(src),
				this.#hasMagic = !!this.#hasMagic,
				this.#uflag
			];
		}
		const repeated = this.type === "*" || this.type === "+";
		const start = this.type === "!" ? "(?:(?!(?:" : "(?:";
		let body = this.#partsToRegExp(dot);
		if (this.isStart() && this.isEnd() && !body && this.type !== "!") {
			const s = this.toString();
			const me = this;
			me.#parts = [s];
			me.type = null;
			me.#hasMagic = void 0;
			return [
				s,
				unescape(this.toString()),
				false,
				false
			];
		}
		let bodyDotAllowed = !repeated || allowDot || dot || false ? "" : this.#partsToRegExp(true);
		if (bodyDotAllowed === body) bodyDotAllowed = "";
		if (bodyDotAllowed) body = `(?:${body})(?:${bodyDotAllowed})*?`;
		let final = "";
		if (this.type === "!" && this.#emptyExt) final = (this.isStart() && !dot ? startNoDot : "") + starNoEmpty;
		else {
			const close = this.type === "!" ? "))" + (this.isStart() && !dot && !allowDot ? startNoDot : "") + star$1 + ")" : this.type === "@" ? ")" : this.type === "?" ? ")?" : this.type === "+" && bodyDotAllowed ? ")" : this.type === "*" && bodyDotAllowed ? `)?` : `)${this.type}`;
			final = start + body + close;
		}
		return [
			final,
			unescape(body),
			this.#hasMagic = !!this.#hasMagic,
			this.#uflag
		];
	}
	#flatten() {
		if (!isExtglobAST(this)) {
			for (const p of this.#parts) if (typeof p === "object") p.#flatten();
		} else {
			let iterations = 0;
			let done = false;
			do {
				done = true;
				for (let i = 0; i < this.#parts.length; i++) {
					const c = this.#parts[i];
					if (typeof c === "object") {
						c.#flatten();
						if (this.#canAdopt(c)) {
							done = false;
							this.#adopt(c, i);
						} else if (this.#canAdoptWithSpace(c)) {
							done = false;
							this.#adoptWithSpace(c, i);
						} else if (this.#canUsurp(c)) {
							done = false;
							this.#usurp(c);
						}
					}
				}
			} while (!done && ++iterations < 10);
		}
		this.#toString = void 0;
	}
	#partsToRegExp(dot) {
		return this.#parts.map((p) => {
			/* c8 ignore start */
			if (typeof p === "string") throw new Error("string type in extglob ast??");
			/* c8 ignore stop */
			const [re, _, _hasMagic, uflag] = p.toRegExpSource(dot);
			this.#uflag = this.#uflag || uflag;
			return re;
		}).filter((p) => !(this.isStart() && this.isEnd()) || !!p).join("|");
	}
	static #parseGlob(glob, hasMagic, noEmpty = false) {
		let escaping = false;
		let re = "";
		let uflag = false;
		let inStar = false;
		for (let i = 0; i < glob.length; i++) {
			const c = glob.charAt(i);
			if (escaping) {
				escaping = false;
				re += (reSpecials.has(c) ? "\\" : "") + c;
				continue;
			}
			if (c === "*") {
				if (inStar) continue;
				inStar = true;
				re += noEmpty && /^[*]+$/.test(glob) ? starNoEmpty : star$1;
				hasMagic = true;
				continue;
			} else inStar = false;
			if (c === "\\") {
				if (i === glob.length - 1) re += "\\\\";
				else escaping = true;
				continue;
			}
			if (c === "[") {
				const [src, needUflag, consumed, magic] = parseClass(glob, i);
				if (consumed) {
					re += src;
					uflag = uflag || needUflag;
					i += consumed - 1;
					hasMagic = hasMagic || magic;
					continue;
				}
			}
			if (c === "?") {
				re += qmark;
				hasMagic = true;
				continue;
			}
			re += regExpEscape$1(c);
		}
		return [
			re,
			unescape(glob),
			!!hasMagic,
			uflag
		];
	}
};
_a = AST;

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/escape.js
/**
* Escape all magic characters in a glob pattern.
*
* If the {@link MinimatchOptions.windowsPathsNoEscape}
* option is used, then characters are escaped by wrapping in `[]`, because
* a magic character wrapped in a character class can only be satisfied by
* that exact character.  In this mode, `\` is _not_ escaped, because it is
* not interpreted as a magic character, but instead as a path separator.
*
* If the {@link MinimatchOptions.magicalBraces} option is used,
* then braces (`{` and `}`) will be escaped.
*/
const escape = (s, { windowsPathsNoEscape = false, magicalBraces = false } = {}) => {
	if (magicalBraces) return windowsPathsNoEscape ? s.replace(/[?*()[\]{}]/g, "[$&]") : s.replace(/[?*()[\]\\{}]/g, "\\$&");
	return windowsPathsNoEscape ? s.replace(/[?*()[\]]/g, "[$&]") : s.replace(/[?*()[\]\\]/g, "\\$&");
};

//#endregion
//#region node_modules/.pnpm/minimatch@10.2.4/node_modules/minimatch/dist/esm/index.js
const minimatch$1 = (p, pattern, options = {}) => {
	assertValidPattern(pattern);
	if (!options.nocomment && pattern.charAt(0) === "#") return false;
	return new Minimatch(pattern, options).match(p);
};
const starDotExtRE = /^\*+([^+@!?\*\[\(]*)$/;
const starDotExtTest = (ext) => (f) => !f.startsWith(".") && f.endsWith(ext);
const starDotExtTestDot = (ext) => (f) => f.endsWith(ext);
const starDotExtTestNocase = (ext) => {
	ext = ext.toLowerCase();
	return (f) => !f.startsWith(".") && f.toLowerCase().endsWith(ext);
};
const starDotExtTestNocaseDot = (ext) => {
	ext = ext.toLowerCase();
	return (f) => f.toLowerCase().endsWith(ext);
};
const starDotStarRE = /^\*+\.\*+$/;
const starDotStarTest = (f) => !f.startsWith(".") && f.includes(".");
const starDotStarTestDot = (f) => f !== "." && f !== ".." && f.includes(".");
const dotStarRE = /^\.\*+$/;
const dotStarTest = (f) => f !== "." && f !== ".." && f.startsWith(".");
const starRE = /^\*+$/;
const starTest = (f) => f.length !== 0 && !f.startsWith(".");
const starTestDot = (f) => f.length !== 0 && f !== "." && f !== "..";
const qmarksRE = /^\?+([^+@!?\*\[\(]*)?$/;
const qmarksTestNocase = ([$0, ext = ""]) => {
	const noext = qmarksTestNoExt([$0]);
	if (!ext) return noext;
	ext = ext.toLowerCase();
	return (f) => noext(f) && f.toLowerCase().endsWith(ext);
};
const qmarksTestNocaseDot = ([$0, ext = ""]) => {
	const noext = qmarksTestNoExtDot([$0]);
	if (!ext) return noext;
	ext = ext.toLowerCase();
	return (f) => noext(f) && f.toLowerCase().endsWith(ext);
};
const qmarksTestDot = ([$0, ext = ""]) => {
	const noext = qmarksTestNoExtDot([$0]);
	return !ext ? noext : (f) => noext(f) && f.endsWith(ext);
};
const qmarksTest = ([$0, ext = ""]) => {
	const noext = qmarksTestNoExt([$0]);
	return !ext ? noext : (f) => noext(f) && f.endsWith(ext);
};
const qmarksTestNoExt = ([$0]) => {
	const len = $0.length;
	return (f) => f.length === len && !f.startsWith(".");
};
const qmarksTestNoExtDot = ([$0]) => {
	const len = $0.length;
	return (f) => f.length === len && f !== "." && f !== "..";
};
/* c8 ignore start */
const defaultPlatform = typeof process === "object" && process ? typeof process.env === "object" && process.env && process.env.__MINIMATCH_TESTING_PLATFORM__ || process.platform : "posix";
const path$1 = {
	win32: { sep: "\\" },
	posix: { sep: "/" }
};
/* c8 ignore stop */
const sep = defaultPlatform === "win32" ? path$1.win32.sep : path$1.posix.sep;
minimatch$1.sep = sep;
const GLOBSTAR = Symbol("globstar **");
minimatch$1.GLOBSTAR = GLOBSTAR;
const star = "[^/]*?";
const twoStarDot = "(?:(?!(?:\\/|^)(?:\\.{1,2})($|\\/)).)*?";
const twoStarNoDot = "(?:(?!(?:\\/|^)\\.).)*?";
const filter = (pattern, options = {}) => (p) => minimatch$1(p, pattern, options);
minimatch$1.filter = filter;
const ext = (a, b = {}) => Object.assign({}, a, b);
const defaults = (def) => {
	if (!def || typeof def !== "object" || !Object.keys(def).length) return minimatch$1;
	const orig = minimatch$1;
	const m = (p, pattern, options = {}) => orig(p, pattern, ext(def, options));
	return Object.assign(m, {
		Minimatch: class Minimatch extends orig.Minimatch {
			constructor(pattern, options = {}) {
				super(pattern, ext(def, options));
			}
			static defaults(options) {
				return orig.defaults(ext(def, options)).Minimatch;
			}
		},
		AST: class AST extends orig.AST {
			/* c8 ignore start */
			constructor(type, parent, options = {}) {
				super(type, parent, ext(def, options));
			}
			/* c8 ignore stop */
			static fromGlob(pattern, options = {}) {
				return orig.AST.fromGlob(pattern, ext(def, options));
			}
		},
		unescape: (s, options = {}) => orig.unescape(s, ext(def, options)),
		escape: (s, options = {}) => orig.escape(s, ext(def, options)),
		filter: (pattern, options = {}) => orig.filter(pattern, ext(def, options)),
		defaults: (options) => orig.defaults(ext(def, options)),
		makeRe: (pattern, options = {}) => orig.makeRe(pattern, ext(def, options)),
		braceExpand: (pattern, options = {}) => orig.braceExpand(pattern, ext(def, options)),
		match: (list, pattern, options = {}) => orig.match(list, pattern, ext(def, options)),
		sep: orig.sep,
		GLOBSTAR
	});
};
minimatch$1.defaults = defaults;
const braceExpand = (pattern, options = {}) => {
	assertValidPattern(pattern);
	if (options.nobrace || !/\{(?:(?!\{).)*\}/.test(pattern)) return [pattern];
	return expand(pattern, { max: options.braceExpandMax });
};
minimatch$1.braceExpand = braceExpand;
const makeRe = (pattern, options = {}) => new Minimatch(pattern, options).makeRe();
minimatch$1.makeRe = makeRe;
const match = (list, pattern, options = {}) => {
	const mm = new Minimatch(pattern, options);
	list = list.filter((f) => mm.match(f));
	if (mm.options.nonull && !list.length) list.push(pattern);
	return list;
};
minimatch$1.match = match;
const globMagic = /[?*]|[+@!]\(.*?\)|\[|\]/;
const regExpEscape = (s) => s.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
var Minimatch = class {
	options;
	set;
	pattern;
	windowsPathsNoEscape;
	nonegate;
	negate;
	comment;
	empty;
	preserveMultipleSlashes;
	partial;
	globSet;
	globParts;
	nocase;
	isWindows;
	platform;
	windowsNoMagicRoot;
	maxGlobstarRecursion;
	regexp;
	constructor(pattern, options = {}) {
		assertValidPattern(pattern);
		options = options || {};
		this.options = options;
		this.maxGlobstarRecursion = options.maxGlobstarRecursion ?? 200;
		this.pattern = pattern;
		this.platform = options.platform || defaultPlatform;
		this.isWindows = this.platform === "win32";
		this.windowsPathsNoEscape = !!options.windowsPathsNoEscape || options["allowWindowsEscape"] === false;
		if (this.windowsPathsNoEscape) this.pattern = this.pattern.replace(/\\/g, "/");
		this.preserveMultipleSlashes = !!options.preserveMultipleSlashes;
		this.regexp = null;
		this.negate = false;
		this.nonegate = !!options.nonegate;
		this.comment = false;
		this.empty = false;
		this.partial = !!options.partial;
		this.nocase = !!this.options.nocase;
		this.windowsNoMagicRoot = options.windowsNoMagicRoot !== void 0 ? options.windowsNoMagicRoot : !!(this.isWindows && this.nocase);
		this.globSet = [];
		this.globParts = [];
		this.set = [];
		this.make();
	}
	hasMagic() {
		if (this.options.magicalBraces && this.set.length > 1) return true;
		for (const pattern of this.set) for (const part of pattern) if (typeof part !== "string") return true;
		return false;
	}
	debug(..._) {}
	make() {
		const pattern = this.pattern;
		const options = this.options;
		if (!options.nocomment && pattern.charAt(0) === "#") {
			this.comment = true;
			return;
		}
		if (!pattern) {
			this.empty = true;
			return;
		}
		this.parseNegate();
		this.globSet = [...new Set(this.braceExpand())];
		if (options.debug) this.debug = (...args) => console.error(...args);
		this.debug(this.pattern, this.globSet);
		const rawGlobParts = this.globSet.map((s) => this.slashSplit(s));
		this.globParts = this.preprocess(rawGlobParts);
		this.debug(this.pattern, this.globParts);
		let set = this.globParts.map((s, _, __) => {
			if (this.isWindows && this.windowsNoMagicRoot) {
				const isUNC = s[0] === "" && s[1] === "" && (s[2] === "?" || !globMagic.test(s[2])) && !globMagic.test(s[3]);
				const isDrive = /^[a-z]:/i.test(s[0]);
				if (isUNC) return [...s.slice(0, 4), ...s.slice(4).map((ss) => this.parse(ss))];
				else if (isDrive) return [s[0], ...s.slice(1).map((ss) => this.parse(ss))];
			}
			return s.map((ss) => this.parse(ss));
		});
		this.debug(this.pattern, set);
		this.set = set.filter((s) => s.indexOf(false) === -1);
		if (this.isWindows) for (let i = 0; i < this.set.length; i++) {
			const p = this.set[i];
			if (p[0] === "" && p[1] === "" && this.globParts[i][2] === "?" && typeof p[3] === "string" && /^[a-z]:$/i.test(p[3])) p[2] = "?";
		}
		this.debug(this.pattern, this.set);
	}
	preprocess(globParts) {
		if (this.options.noglobstar) {
			for (let i = 0; i < globParts.length; i++) for (let j = 0; j < globParts[i].length; j++) if (globParts[i][j] === "**") globParts[i][j] = "*";
		}
		const { optimizationLevel = 1 } = this.options;
		if (optimizationLevel >= 2) {
			globParts = this.firstPhasePreProcess(globParts);
			globParts = this.secondPhasePreProcess(globParts);
		} else if (optimizationLevel >= 1) globParts = this.levelOneOptimize(globParts);
		else globParts = this.adjascentGlobstarOptimize(globParts);
		return globParts;
	}
	adjascentGlobstarOptimize(globParts) {
		return globParts.map((parts) => {
			let gs = -1;
			while (-1 !== (gs = parts.indexOf("**", gs + 1))) {
				let i = gs;
				while (parts[i + 1] === "**") i++;
				if (i !== gs) parts.splice(gs, i - gs);
			}
			return parts;
		});
	}
	levelOneOptimize(globParts) {
		return globParts.map((parts) => {
			parts = parts.reduce((set, part) => {
				const prev = set[set.length - 1];
				if (part === "**" && prev === "**") return set;
				if (part === "..") {
					if (prev && prev !== ".." && prev !== "." && prev !== "**") {
						set.pop();
						return set;
					}
				}
				set.push(part);
				return set;
			}, []);
			return parts.length === 0 ? [""] : parts;
		});
	}
	levelTwoFileOptimize(parts) {
		if (!Array.isArray(parts)) parts = this.slashSplit(parts);
		let didSomething = false;
		do {
			didSomething = false;
			if (!this.preserveMultipleSlashes) {
				for (let i = 1; i < parts.length - 1; i++) {
					const p = parts[i];
					if (i === 1 && p === "" && parts[0] === "") continue;
					if (p === "." || p === "") {
						didSomething = true;
						parts.splice(i, 1);
						i--;
					}
				}
				if (parts[0] === "." && parts.length === 2 && (parts[1] === "." || parts[1] === "")) {
					didSomething = true;
					parts.pop();
				}
			}
			let dd = 0;
			while (-1 !== (dd = parts.indexOf("..", dd + 1))) {
				const p = parts[dd - 1];
				if (p && p !== "." && p !== ".." && p !== "**") {
					didSomething = true;
					parts.splice(dd - 1, 2);
					dd -= 2;
				}
			}
		} while (didSomething);
		return parts.length === 0 ? [""] : parts;
	}
	firstPhasePreProcess(globParts) {
		let didSomething = false;
		do {
			didSomething = false;
			for (let parts of globParts) {
				let gs = -1;
				while (-1 !== (gs = parts.indexOf("**", gs + 1))) {
					let gss = gs;
					while (parts[gss + 1] === "**") gss++;
					if (gss > gs) parts.splice(gs + 1, gss - gs);
					let next = parts[gs + 1];
					const p = parts[gs + 2];
					const p2 = parts[gs + 3];
					if (next !== "..") continue;
					if (!p || p === "." || p === ".." || !p2 || p2 === "." || p2 === "..") continue;
					didSomething = true;
					parts.splice(gs, 1);
					const other = parts.slice(0);
					other[gs] = "**";
					globParts.push(other);
					gs--;
				}
				if (!this.preserveMultipleSlashes) {
					for (let i = 1; i < parts.length - 1; i++) {
						const p = parts[i];
						if (i === 1 && p === "" && parts[0] === "") continue;
						if (p === "." || p === "") {
							didSomething = true;
							parts.splice(i, 1);
							i--;
						}
					}
					if (parts[0] === "." && parts.length === 2 && (parts[1] === "." || parts[1] === "")) {
						didSomething = true;
						parts.pop();
					}
				}
				let dd = 0;
				while (-1 !== (dd = parts.indexOf("..", dd + 1))) {
					const p = parts[dd - 1];
					if (p && p !== "." && p !== ".." && p !== "**") {
						didSomething = true;
						const splin = dd === 1 && parts[dd + 1] === "**" ? ["."] : [];
						parts.splice(dd - 1, 2, ...splin);
						if (parts.length === 0) parts.push("");
						dd -= 2;
					}
				}
			}
		} while (didSomething);
		return globParts;
	}
	secondPhasePreProcess(globParts) {
		for (let i = 0; i < globParts.length - 1; i++) for (let j = i + 1; j < globParts.length; j++) {
			const matched = this.partsMatch(globParts[i], globParts[j], !this.preserveMultipleSlashes);
			if (matched) {
				globParts[i] = [];
				globParts[j] = matched;
				break;
			}
		}
		return globParts.filter((gs) => gs.length);
	}
	partsMatch(a, b, emptyGSMatch = false) {
		let ai = 0;
		let bi = 0;
		let result = [];
		let which = "";
		while (ai < a.length && bi < b.length) if (a[ai] === b[bi]) {
			result.push(which === "b" ? b[bi] : a[ai]);
			ai++;
			bi++;
		} else if (emptyGSMatch && a[ai] === "**" && b[bi] === a[ai + 1]) {
			result.push(a[ai]);
			ai++;
		} else if (emptyGSMatch && b[bi] === "**" && a[ai] === b[bi + 1]) {
			result.push(b[bi]);
			bi++;
		} else if (a[ai] === "*" && b[bi] && (this.options.dot || !b[bi].startsWith(".")) && b[bi] !== "**") {
			if (which === "b") return false;
			which = "a";
			result.push(a[ai]);
			ai++;
			bi++;
		} else if (b[bi] === "*" && a[ai] && (this.options.dot || !a[ai].startsWith(".")) && a[ai] !== "**") {
			if (which === "a") return false;
			which = "b";
			result.push(b[bi]);
			ai++;
			bi++;
		} else return false;
		return a.length === b.length && result;
	}
	parseNegate() {
		if (this.nonegate) return;
		const pattern = this.pattern;
		let negate = false;
		let negateOffset = 0;
		for (let i = 0; i < pattern.length && pattern.charAt(i) === "!"; i++) {
			negate = !negate;
			negateOffset++;
		}
		if (negateOffset) this.pattern = pattern.slice(negateOffset);
		this.negate = negate;
	}
	matchOne(file, pattern, partial = false) {
		let fileStartIndex = 0;
		let patternStartIndex = 0;
		if (this.isWindows) {
			const fileDrive = typeof file[0] === "string" && /^[a-z]:$/i.test(file[0]);
			const fileUNC = !fileDrive && file[0] === "" && file[1] === "" && file[2] === "?" && /^[a-z]:$/i.test(file[3]);
			const patternDrive = typeof pattern[0] === "string" && /^[a-z]:$/i.test(pattern[0]);
			const patternUNC = !patternDrive && pattern[0] === "" && pattern[1] === "" && pattern[2] === "?" && typeof pattern[3] === "string" && /^[a-z]:$/i.test(pattern[3]);
			const fdi = fileUNC ? 3 : fileDrive ? 0 : void 0;
			const pdi = patternUNC ? 3 : patternDrive ? 0 : void 0;
			if (typeof fdi === "number" && typeof pdi === "number") {
				const [fd, pd] = [file[fdi], pattern[pdi]];
				if (fd.toLowerCase() === pd.toLowerCase()) {
					pattern[pdi] = fd;
					patternStartIndex = pdi;
					fileStartIndex = fdi;
				}
			}
		}
		const { optimizationLevel = 1 } = this.options;
		if (optimizationLevel >= 2) file = this.levelTwoFileOptimize(file);
		if (pattern.includes(GLOBSTAR)) return this.#matchGlobstar(file, pattern, partial, fileStartIndex, patternStartIndex);
		return this.#matchOne(file, pattern, partial, fileStartIndex, patternStartIndex);
	}
	#matchGlobstar(file, pattern, partial, fileIndex, patternIndex) {
		const firstgs = pattern.indexOf(GLOBSTAR, patternIndex);
		const lastgs = pattern.lastIndexOf(GLOBSTAR);
		const [head, body, tail] = partial ? [
			pattern.slice(patternIndex, firstgs),
			pattern.slice(firstgs + 1),
			[]
		] : [
			pattern.slice(patternIndex, firstgs),
			pattern.slice(firstgs + 1, lastgs),
			pattern.slice(lastgs + 1)
		];
		if (head.length) {
			const fileHead = file.slice(fileIndex, fileIndex + head.length);
			if (!this.#matchOne(fileHead, head, partial, 0, 0)) return false;
			fileIndex += head.length;
			patternIndex += head.length;
		}
		let fileTailMatch = 0;
		if (tail.length) {
			if (tail.length + fileIndex > file.length) return false;
			let tailStart = file.length - tail.length;
			if (this.#matchOne(file, tail, partial, tailStart, 0)) fileTailMatch = tail.length;
			else {
				if (file[file.length - 1] !== "" || fileIndex + tail.length === file.length) return false;
				tailStart--;
				if (!this.#matchOne(file, tail, partial, tailStart, 0)) return false;
				fileTailMatch = tail.length + 1;
			}
		}
		if (!body.length) {
			let sawSome = !!fileTailMatch;
			for (let i = fileIndex; i < file.length - fileTailMatch; i++) {
				const f = String(file[i]);
				sawSome = true;
				if (f === "." || f === ".." || !this.options.dot && f.startsWith(".")) return false;
			}
			return partial || sawSome;
		}
		const bodySegments = [[[], 0]];
		let currentBody = bodySegments[0];
		let nonGsParts = 0;
		const nonGsPartsSums = [0];
		for (const b of body) if (b === GLOBSTAR) {
			nonGsPartsSums.push(nonGsParts);
			currentBody = [[], 0];
			bodySegments.push(currentBody);
		} else {
			currentBody[0].push(b);
			nonGsParts++;
		}
		let i = bodySegments.length - 1;
		const fileLength = file.length - fileTailMatch;
		for (const b of bodySegments) b[1] = fileLength - (nonGsPartsSums[i--] + b[0].length);
		return !!this.#matchGlobStarBodySections(file, bodySegments, fileIndex, 0, partial, 0, !!fileTailMatch);
	}
	#matchGlobStarBodySections(file, bodySegments, fileIndex, bodyIndex, partial, globStarDepth, sawTail) {
		const bs = bodySegments[bodyIndex];
		if (!bs) {
			for (let i = fileIndex; i < file.length; i++) {
				sawTail = true;
				const f = file[i];
				if (f === "." || f === ".." || !this.options.dot && f.startsWith(".")) return false;
			}
			return sawTail;
		}
		const [body, after] = bs;
		while (fileIndex <= after) {
			if (this.#matchOne(file.slice(0, fileIndex + body.length), body, partial, fileIndex, 0) && globStarDepth < this.maxGlobstarRecursion) {
				const sub = this.#matchGlobStarBodySections(file, bodySegments, fileIndex + body.length, bodyIndex + 1, partial, globStarDepth + 1, sawTail);
				if (sub !== false) return sub;
			}
			const f = file[fileIndex];
			if (f === "." || f === ".." || !this.options.dot && f.startsWith(".")) return false;
			fileIndex++;
		}
		return partial || null;
	}
	#matchOne(file, pattern, partial, fileIndex, patternIndex) {
		let fi;
		let pi;
		let pl;
		let fl;
		for (fi = fileIndex, pi = patternIndex, fl = file.length, pl = pattern.length; fi < fl && pi < pl; fi++, pi++) {
			this.debug("matchOne loop");
			let p = pattern[pi];
			let f = file[fi];
			this.debug(pattern, p, f);
			/* c8 ignore start */
			if (p === false || p === GLOBSTAR) return false;
			/* c8 ignore stop */
			let hit;
			if (typeof p === "string") {
				hit = f === p;
				this.debug("string match", p, f, hit);
			} else {
				hit = p.test(f);
				this.debug("pattern match", p, f, hit);
			}
			if (!hit) return false;
		}
		if (fi === fl && pi === pl) return true;
		else if (fi === fl) return partial;
		else if (pi === pl) return fi === fl - 1 && file[fi] === "";
		else throw new Error("wtf?");
		/* c8 ignore stop */
	}
	braceExpand() {
		return braceExpand(this.pattern, this.options);
	}
	parse(pattern) {
		assertValidPattern(pattern);
		const options = this.options;
		if (pattern === "**") return GLOBSTAR;
		if (pattern === "") return "";
		let m;
		let fastTest = null;
		if (m = pattern.match(starRE)) fastTest = options.dot ? starTestDot : starTest;
		else if (m = pattern.match(starDotExtRE)) fastTest = (options.nocase ? options.dot ? starDotExtTestNocaseDot : starDotExtTestNocase : options.dot ? starDotExtTestDot : starDotExtTest)(m[1]);
		else if (m = pattern.match(qmarksRE)) fastTest = (options.nocase ? options.dot ? qmarksTestNocaseDot : qmarksTestNocase : options.dot ? qmarksTestDot : qmarksTest)(m);
		else if (m = pattern.match(starDotStarRE)) fastTest = options.dot ? starDotStarTestDot : starDotStarTest;
		else if (m = pattern.match(dotStarRE)) fastTest = dotStarTest;
		const re = AST.fromGlob(pattern, this.options).toMMPattern();
		if (fastTest && typeof re === "object") Reflect.defineProperty(re, "test", { value: fastTest });
		return re;
	}
	makeRe() {
		if (this.regexp || this.regexp === false) return this.regexp;
		const set = this.set;
		if (!set.length) {
			this.regexp = false;
			return this.regexp;
		}
		const options = this.options;
		const twoStar = options.noglobstar ? star : options.dot ? twoStarDot : twoStarNoDot;
		const flags = new Set(options.nocase ? ["i"] : []);
		let re = set.map((pattern) => {
			const pp = pattern.map((p) => {
				if (p instanceof RegExp) for (const f of p.flags.split("")) flags.add(f);
				return typeof p === "string" ? regExpEscape(p) : p === GLOBSTAR ? GLOBSTAR : p._src;
			});
			pp.forEach((p, i) => {
				const next = pp[i + 1];
				const prev = pp[i - 1];
				if (p !== GLOBSTAR || prev === GLOBSTAR) return;
				if (prev === void 0) if (next !== void 0 && next !== GLOBSTAR) pp[i + 1] = "(?:\\/|" + twoStar + "\\/)?" + next;
				else pp[i] = twoStar;
				else if (next === void 0) pp[i - 1] = prev + "(?:\\/|\\/" + twoStar + ")?";
				else if (next !== GLOBSTAR) {
					pp[i - 1] = prev + "(?:\\/|\\/" + twoStar + "\\/)" + next;
					pp[i + 1] = GLOBSTAR;
				}
			});
			const filtered = pp.filter((p) => p !== GLOBSTAR);
			if (this.partial && filtered.length >= 1) {
				const prefixes = [];
				for (let i = 1; i <= filtered.length; i++) prefixes.push(filtered.slice(0, i).join("/"));
				return "(?:" + prefixes.join("|") + ")";
			}
			return filtered.join("/");
		}).join("|");
		const [open, close] = set.length > 1 ? ["(?:", ")"] : ["", ""];
		re = "^" + open + re + close + "$";
		if (this.partial) re = "^(?:\\/|" + open + re.slice(1, -1) + close + ")$";
		if (this.negate) re = "^(?!" + re + ").+$";
		try {
			this.regexp = new RegExp(re, [...flags].join(""));
		} catch (ex) {
			this.regexp = false;
		}
		/* c8 ignore stop */
		return this.regexp;
	}
	slashSplit(p) {
		if (this.preserveMultipleSlashes) return p.split("/");
		else if (this.isWindows && /^\/\/[^\/]+/.test(p)) return ["", ...p.split(/\/+/)];
		else return p.split(/\/+/);
	}
	match(f, partial = this.partial) {
		this.debug("match", f, this.pattern);
		if (this.comment) return false;
		if (this.empty) return f === "";
		if (f === "/" && partial) return true;
		const options = this.options;
		if (this.isWindows) f = f.split("\\").join("/");
		const ff = this.slashSplit(f);
		this.debug(this.pattern, "split", ff);
		const set = this.set;
		this.debug(this.pattern, "set", set);
		let filename = ff[ff.length - 1];
		if (!filename) for (let i = ff.length - 2; !filename && i >= 0; i--) filename = ff[i];
		for (let i = 0; i < set.length; i++) {
			const pattern = set[i];
			let file = ff;
			if (options.matchBase && pattern.length === 1) file = [filename];
			if (this.matchOne(file, pattern, partial)) {
				if (options.flipNegate) return true;
				return !this.negate;
			}
		}
		if (options.flipNegate) return false;
		return this.negate;
	}
	static defaults(def) {
		return minimatch$1.defaults(def).Minimatch;
	}
};
/* c8 ignore stop */
minimatch$1.AST = AST;
minimatch$1.Minimatch = Minimatch;
minimatch$1.escape = escape;
minimatch$1.unescape = unescape;

//#endregion
//#region node_modules/.pnpm/ms@2.1.3/node_modules/ms/index.js
var require_ms = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/**
	* Helpers.
	*/
	var s = 1e3;
	var m = s * 60;
	var h = m * 60;
	var d = h * 24;
	var w = d * 7;
	var y = d * 365.25;
	/**
	* Parse or format the given `val`.
	*
	* Options:
	*
	*  - `long` verbose formatting [false]
	*
	* @param {String|Number} val
	* @param {Object} [options]
	* @throws {Error} throw an error if val is not a non-empty string or a number
	* @return {String|Number}
	* @api public
	*/
	module.exports = function(val, options) {
		options = options || {};
		var type = typeof val;
		if (type === "string" && val.length > 0) return parse(val);
		else if (type === "number" && isFinite(val)) return options.long ? fmtLong(val) : fmtShort(val);
		throw new Error("val is not a non-empty string or a valid number. val=" + JSON.stringify(val));
	};
	/**
	* Parse the given `str` and return milliseconds.
	*
	* @param {String} str
	* @return {Number}
	* @api private
	*/
	function parse(str) {
		str = String(str);
		if (str.length > 100) return;
		var match = /^(-?(?:\d+)?\.?\d+) *(milliseconds?|msecs?|ms|seconds?|secs?|s|minutes?|mins?|m|hours?|hrs?|h|days?|d|weeks?|w|years?|yrs?|y)?$/i.exec(str);
		if (!match) return;
		var n = parseFloat(match[1]);
		switch ((match[2] || "ms").toLowerCase()) {
			case "years":
			case "year":
			case "yrs":
			case "yr":
			case "y": return n * y;
			case "weeks":
			case "week":
			case "w": return n * w;
			case "days":
			case "day":
			case "d": return n * d;
			case "hours":
			case "hour":
			case "hrs":
			case "hr":
			case "h": return n * h;
			case "minutes":
			case "minute":
			case "mins":
			case "min":
			case "m": return n * m;
			case "seconds":
			case "second":
			case "secs":
			case "sec":
			case "s": return n * s;
			case "milliseconds":
			case "millisecond":
			case "msecs":
			case "msec":
			case "ms": return n;
			default: return;
		}
	}
	/**
	* Short format for `ms`.
	*
	* @param {Number} ms
	* @return {String}
	* @api private
	*/
	function fmtShort(ms) {
		var msAbs = Math.abs(ms);
		if (msAbs >= d) return Math.round(ms / d) + "d";
		if (msAbs >= h) return Math.round(ms / h) + "h";
		if (msAbs >= m) return Math.round(ms / m) + "m";
		if (msAbs >= s) return Math.round(ms / s) + "s";
		return ms + "ms";
	}
	/**
	* Long format for `ms`.
	*
	* @param {Number} ms
	* @return {String}
	* @api private
	*/
	function fmtLong(ms) {
		var msAbs = Math.abs(ms);
		if (msAbs >= d) return plural(ms, msAbs, d, "day");
		if (msAbs >= h) return plural(ms, msAbs, h, "hour");
		if (msAbs >= m) return plural(ms, msAbs, m, "minute");
		if (msAbs >= s) return plural(ms, msAbs, s, "second");
		return ms + " ms";
	}
	/**
	* Pluralization helper.
	*/
	function plural(ms, msAbs, n, name) {
		var isPlural = msAbs >= n * 1.5;
		return Math.round(ms / n) + " " + name + (isPlural ? "s" : "");
	}
}));

//#endregion
//#region node_modules/.pnpm/debug@4.4.3/node_modules/debug/src/common.js
var require_common = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/**
	* This is the common logic for both the Node.js and web browser
	* implementations of `debug()`.
	*/
	function setup(env) {
		createDebug.debug = createDebug;
		createDebug.default = createDebug;
		createDebug.coerce = coerce;
		createDebug.disable = disable;
		createDebug.enable = enable;
		createDebug.enabled = enabled;
		createDebug.humanize = require_ms();
		createDebug.destroy = destroy;
		Object.keys(env).forEach((key) => {
			createDebug[key] = env[key];
		});
		/**
		* The currently active debug mode names, and names to skip.
		*/
		createDebug.names = [];
		createDebug.skips = [];
		/**
		* Map of special "%n" handling functions, for the debug "format" argument.
		*
		* Valid key names are a single, lower or upper-case letter, i.e. "n" and "N".
		*/
		createDebug.formatters = {};
		/**
		* Selects a color for a debug namespace
		* @param {String} namespace The namespace string for the debug instance to be colored
		* @return {Number|String} An ANSI color code for the given namespace
		* @api private
		*/
		function selectColor(namespace) {
			let hash = 0;
			for (let i = 0; i < namespace.length; i++) {
				hash = (hash << 5) - hash + namespace.charCodeAt(i);
				hash |= 0;
			}
			return createDebug.colors[Math.abs(hash) % createDebug.colors.length];
		}
		createDebug.selectColor = selectColor;
		/**
		* Create a debugger with the given `namespace`.
		*
		* @param {String} namespace
		* @return {Function}
		* @api public
		*/
		function createDebug(namespace) {
			let prevTime;
			let enableOverride = null;
			let namespacesCache;
			let enabledCache;
			function debug(...args) {
				if (!debug.enabled) return;
				const self = debug;
				const curr = Number(/* @__PURE__ */ new Date());
				self.diff = curr - (prevTime || curr);
				self.prev = prevTime;
				self.curr = curr;
				prevTime = curr;
				args[0] = createDebug.coerce(args[0]);
				if (typeof args[0] !== "string") args.unshift("%O");
				let index = 0;
				args[0] = args[0].replace(/%([a-zA-Z%])/g, (match, format) => {
					if (match === "%%") return "%";
					index++;
					const formatter = createDebug.formatters[format];
					if (typeof formatter === "function") {
						const val = args[index];
						match = formatter.call(self, val);
						args.splice(index, 1);
						index--;
					}
					return match;
				});
				createDebug.formatArgs.call(self, args);
				(self.log || createDebug.log).apply(self, args);
			}
			debug.namespace = namespace;
			debug.useColors = createDebug.useColors();
			debug.color = createDebug.selectColor(namespace);
			debug.extend = extend;
			debug.destroy = createDebug.destroy;
			Object.defineProperty(debug, "enabled", {
				enumerable: true,
				configurable: false,
				get: () => {
					if (enableOverride !== null) return enableOverride;
					if (namespacesCache !== createDebug.namespaces) {
						namespacesCache = createDebug.namespaces;
						enabledCache = createDebug.enabled(namespace);
					}
					return enabledCache;
				},
				set: (v) => {
					enableOverride = v;
				}
			});
			if (typeof createDebug.init === "function") createDebug.init(debug);
			return debug;
		}
		function extend(namespace, delimiter) {
			const newDebug = createDebug(this.namespace + (typeof delimiter === "undefined" ? ":" : delimiter) + namespace);
			newDebug.log = this.log;
			return newDebug;
		}
		/**
		* Enables a debug mode by namespaces. This can include modes
		* separated by a colon and wildcards.
		*
		* @param {String} namespaces
		* @api public
		*/
		function enable(namespaces) {
			createDebug.save(namespaces);
			createDebug.namespaces = namespaces;
			createDebug.names = [];
			createDebug.skips = [];
			const split = (typeof namespaces === "string" ? namespaces : "").trim().replace(/\s+/g, ",").split(",").filter(Boolean);
			for (const ns of split) if (ns[0] === "-") createDebug.skips.push(ns.slice(1));
			else createDebug.names.push(ns);
		}
		/**
		* Checks if the given string matches a namespace template, honoring
		* asterisks as wildcards.
		*
		* @param {String} search
		* @param {String} template
		* @return {Boolean}
		*/
		function matchesTemplate(search, template) {
			let searchIndex = 0;
			let templateIndex = 0;
			let starIndex = -1;
			let matchIndex = 0;
			while (searchIndex < search.length) if (templateIndex < template.length && (template[templateIndex] === search[searchIndex] || template[templateIndex] === "*")) if (template[templateIndex] === "*") {
				starIndex = templateIndex;
				matchIndex = searchIndex;
				templateIndex++;
			} else {
				searchIndex++;
				templateIndex++;
			}
			else if (starIndex !== -1) {
				templateIndex = starIndex + 1;
				matchIndex++;
				searchIndex = matchIndex;
			} else return false;
			while (templateIndex < template.length && template[templateIndex] === "*") templateIndex++;
			return templateIndex === template.length;
		}
		/**
		* Disable debug output.
		*
		* @return {String} namespaces
		* @api public
		*/
		function disable() {
			const namespaces = [...createDebug.names, ...createDebug.skips.map((namespace) => "-" + namespace)].join(",");
			createDebug.enable("");
			return namespaces;
		}
		/**
		* Returns true if the given mode name is enabled, false otherwise.
		*
		* @param {String} name
		* @return {Boolean}
		* @api public
		*/
		function enabled(name) {
			for (const skip of createDebug.skips) if (matchesTemplate(name, skip)) return false;
			for (const ns of createDebug.names) if (matchesTemplate(name, ns)) return true;
			return false;
		}
		/**
		* Coerce `val`.
		*
		* @param {Mixed} val
		* @return {Mixed}
		* @api private
		*/
		function coerce(val) {
			if (val instanceof Error) return val.stack || val.message;
			return val;
		}
		/**
		* XXX DO NOT USE. This is a temporary stub function.
		* XXX It WILL be removed in the next major release.
		*/
		function destroy() {
			console.warn("Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.");
		}
		createDebug.enable(createDebug.load());
		return createDebug;
	}
	module.exports = setup;
}));

//#endregion
//#region node_modules/.pnpm/debug@4.4.3/node_modules/debug/src/browser.js
var require_browser = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/**
	* This is the web browser implementation of `debug()`.
	*/
	exports.formatArgs = formatArgs;
	exports.save = save;
	exports.load = load;
	exports.useColors = useColors;
	exports.storage = localstorage();
	exports.destroy = (() => {
		let warned = false;
		return () => {
			if (!warned) {
				warned = true;
				console.warn("Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.");
			}
		};
	})();
	/**
	* Colors.
	*/
	exports.colors = [
		"#0000CC",
		"#0000FF",
		"#0033CC",
		"#0033FF",
		"#0066CC",
		"#0066FF",
		"#0099CC",
		"#0099FF",
		"#00CC00",
		"#00CC33",
		"#00CC66",
		"#00CC99",
		"#00CCCC",
		"#00CCFF",
		"#3300CC",
		"#3300FF",
		"#3333CC",
		"#3333FF",
		"#3366CC",
		"#3366FF",
		"#3399CC",
		"#3399FF",
		"#33CC00",
		"#33CC33",
		"#33CC66",
		"#33CC99",
		"#33CCCC",
		"#33CCFF",
		"#6600CC",
		"#6600FF",
		"#6633CC",
		"#6633FF",
		"#66CC00",
		"#66CC33",
		"#9900CC",
		"#9900FF",
		"#9933CC",
		"#9933FF",
		"#99CC00",
		"#99CC33",
		"#CC0000",
		"#CC0033",
		"#CC0066",
		"#CC0099",
		"#CC00CC",
		"#CC00FF",
		"#CC3300",
		"#CC3333",
		"#CC3366",
		"#CC3399",
		"#CC33CC",
		"#CC33FF",
		"#CC6600",
		"#CC6633",
		"#CC9900",
		"#CC9933",
		"#CCCC00",
		"#CCCC33",
		"#FF0000",
		"#FF0033",
		"#FF0066",
		"#FF0099",
		"#FF00CC",
		"#FF00FF",
		"#FF3300",
		"#FF3333",
		"#FF3366",
		"#FF3399",
		"#FF33CC",
		"#FF33FF",
		"#FF6600",
		"#FF6633",
		"#FF9900",
		"#FF9933",
		"#FFCC00",
		"#FFCC33"
	];
	/**
	* Currently only WebKit-based Web Inspectors, Firefox >= v31,
	* and the Firebug extension (any Firefox version) are known
	* to support "%c" CSS customizations.
	*
	* TODO: add a `localStorage` variable to explicitly enable/disable colors
	*/
	function useColors() {
		if (typeof window !== "undefined" && window.process && (window.process.type === "renderer" || window.process.__nwjs)) return true;
		if (typeof navigator !== "undefined" && navigator.userAgent && navigator.userAgent.toLowerCase().match(/(edge|trident)\/(\d+)/)) return false;
		let m;
		return typeof document !== "undefined" && document.documentElement && document.documentElement.style && document.documentElement.style.WebkitAppearance || typeof window !== "undefined" && window.console && (window.console.firebug || window.console.exception && window.console.table) || typeof navigator !== "undefined" && navigator.userAgent && (m = navigator.userAgent.toLowerCase().match(/firefox\/(\d+)/)) && parseInt(m[1], 10) >= 31 || typeof navigator !== "undefined" && navigator.userAgent && navigator.userAgent.toLowerCase().match(/applewebkit\/(\d+)/);
	}
	/**
	* Colorize log arguments if enabled.
	*
	* @api public
	*/
	function formatArgs(args) {
		args[0] = (this.useColors ? "%c" : "") + this.namespace + (this.useColors ? " %c" : " ") + args[0] + (this.useColors ? "%c " : " ") + "+" + module.exports.humanize(this.diff);
		if (!this.useColors) return;
		const c = "color: " + this.color;
		args.splice(1, 0, c, "color: inherit");
		let index = 0;
		let lastC = 0;
		args[0].replace(/%[a-zA-Z%]/g, (match) => {
			if (match === "%%") return;
			index++;
			if (match === "%c") lastC = index;
		});
		args.splice(lastC, 0, c);
	}
	/**
	* Invokes `console.debug()` when available.
	* No-op when `console.debug` is not a "function".
	* If `console.debug` is not available, falls back
	* to `console.log`.
	*
	* @api public
	*/
	exports.log = console.debug || console.log || (() => {});
	/**
	* Save `namespaces`.
	*
	* @param {String} namespaces
	* @api private
	*/
	function save(namespaces) {
		try {
			if (namespaces) exports.storage.setItem("debug", namespaces);
			else exports.storage.removeItem("debug");
		} catch (error) {}
	}
	/**
	* Load `namespaces`.
	*
	* @return {String} returns the previously persisted debug modes
	* @api private
	*/
	function load() {
		let r;
		try {
			r = exports.storage.getItem("debug") || exports.storage.getItem("DEBUG");
		} catch (error) {}
		if (!r && typeof process !== "undefined" && "env" in process) r = process.env.DEBUG;
		return r;
	}
	/**
	* Localstorage attempts to return the localstorage.
	*
	* This is necessary because safari throws
	* when a user disables cookies/localstorage
	* and you attempt to access it.
	*
	* @return {LocalStorage}
	* @api private
	*/
	function localstorage() {
		try {
			return localStorage;
		} catch (error) {}
	}
	module.exports = require_common()(exports);
	const { formatters } = module.exports;
	/**
	* Map %j to `JSON.stringify()`, since no Web Inspectors do that by default.
	*/
	formatters.j = function(v) {
		try {
			return JSON.stringify(v);
		} catch (error) {
			return "[UnexpectedJSONParseError]: " + error.message;
		}
	};
}));

//#endregion
//#region node_modules/.pnpm/supports-color@10.1.0/node_modules/supports-color/index.js
var supports_color_exports = /* @__PURE__ */ __exportAll({
	createSupportsColor: () => createSupportsColor,
	default: () => supportsColor
});
function hasFlag(flag, argv = globalThis.Deno ? globalThis.Deno.args : process$1.argv) {
	const prefix = flag.startsWith("-") ? "" : flag.length === 1 ? "-" : "--";
	const position = argv.indexOf(prefix + flag);
	const terminatorPosition = argv.indexOf("--");
	return position !== -1 && (terminatorPosition === -1 || position < terminatorPosition);
}
function envForceColor() {
	if (!("FORCE_COLOR" in env)) return;
	if (env.FORCE_COLOR === "true") return 1;
	if (env.FORCE_COLOR === "false") return 0;
	if (env.FORCE_COLOR.length === 0) return 1;
	const level = Math.min(Number.parseInt(env.FORCE_COLOR, 10), 3);
	if (![
		0,
		1,
		2,
		3
	].includes(level)) return;
	return level;
}
function translateLevel(level) {
	if (level === 0) return false;
	return {
		level,
		hasBasic: true,
		has256: level >= 2,
		has16m: level >= 3
	};
}
function _supportsColor(haveStream, { streamIsTTY, sniffFlags = true } = {}) {
	const noFlagForceColor = envForceColor();
	if (noFlagForceColor !== void 0) flagForceColor = noFlagForceColor;
	const forceColor = sniffFlags ? flagForceColor : noFlagForceColor;
	if (forceColor === 0) return 0;
	if (sniffFlags) {
		if (hasFlag("color=16m") || hasFlag("color=full") || hasFlag("color=truecolor")) return 3;
		if (hasFlag("color=256")) return 2;
	}
	if ("TF_BUILD" in env && "AGENT_NAME" in env) return 1;
	if (haveStream && !streamIsTTY && forceColor === void 0) return 0;
	const min = forceColor || 0;
	if (env.TERM === "dumb") return min;
	if (process$1.platform === "win32") {
		const osRelease = os.release().split(".");
		if (Number(osRelease[0]) >= 10 && Number(osRelease[2]) >= 10586) return Number(osRelease[2]) >= 14931 ? 3 : 2;
		return 1;
	}
	if ("CI" in env) {
		if ([
			"GITHUB_ACTIONS",
			"GITEA_ACTIONS",
			"CIRCLECI"
		].some((key) => key in env)) return 3;
		if ([
			"TRAVIS",
			"APPVEYOR",
			"GITLAB_CI",
			"BUILDKITE",
			"DRONE"
		].some((sign) => sign in env) || env.CI_NAME === "codeship") return 1;
		return min;
	}
	if ("TEAMCITY_VERSION" in env) return /^(9\.(0*[1-9]\d*)\.|\d{2,}\.)/.test(env.TEAMCITY_VERSION) ? 1 : 0;
	if (env.COLORTERM === "truecolor") return 3;
	if (env.TERM === "xterm-kitty") return 3;
	if (env.TERM === "xterm-ghostty") return 3;
	if ("TERM_PROGRAM" in env) {
		const version = Number.parseInt((env.TERM_PROGRAM_VERSION || "").split(".")[0], 10);
		switch (env.TERM_PROGRAM) {
			case "iTerm.app": return version >= 3 ? 3 : 2;
			case "Apple_Terminal": return 2;
		}
	}
	if (/-256(color)?$/i.test(env.TERM)) return 2;
	if (/^screen|^xterm|^vt100|^vt220|^rxvt|color|ansi|cygwin|linux/i.test(env.TERM)) return 1;
	if ("COLORTERM" in env) return 1;
	return min;
}
function createSupportsColor(stream, options = {}) {
	return translateLevel(_supportsColor(stream, {
		streamIsTTY: stream && stream.isTTY,
		...options
	}));
}
var env, flagForceColor, supportsColor;
var init_supports_color = __esmMin((() => {
	({env} = process$1);
	;
	if (hasFlag("no-color") || hasFlag("no-colors") || hasFlag("color=false") || hasFlag("color=never")) flagForceColor = 0;
	else if (hasFlag("color") || hasFlag("colors") || hasFlag("color=true") || hasFlag("color=always")) flagForceColor = 1;
	supportsColor = {
		stdout: createSupportsColor({ isTTY: tty.isatty(1) }),
		stderr: createSupportsColor({ isTTY: tty.isatty(2) })
	};
}));

//#endregion
//#region node_modules/.pnpm/debug@4.4.3/node_modules/debug/src/node.js
var require_node = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/**
	* Module dependencies.
	*/
	const tty$1 = __require("tty");
	const util = __require("util");
	/**
	* This is the Node.js implementation of `debug()`.
	*/
	exports.init = init;
	exports.log = log;
	exports.formatArgs = formatArgs;
	exports.save = save;
	exports.load = load;
	exports.useColors = useColors;
	exports.destroy = util.deprecate(() => {}, "Instance method `debug.destroy()` is deprecated and no longer does anything. It will be removed in the next major version of `debug`.");
	/**
	* Colors.
	*/
	exports.colors = [
		6,
		2,
		3,
		4,
		5,
		1
	];
	try {
		const supportsColor = (init_supports_color(), __toCommonJS(supports_color_exports));
		if (supportsColor && (supportsColor.stderr || supportsColor).level >= 2) exports.colors = [
			20,
			21,
			26,
			27,
			32,
			33,
			38,
			39,
			40,
			41,
			42,
			43,
			44,
			45,
			56,
			57,
			62,
			63,
			68,
			69,
			74,
			75,
			76,
			77,
			78,
			79,
			80,
			81,
			92,
			93,
			98,
			99,
			112,
			113,
			128,
			129,
			134,
			135,
			148,
			149,
			160,
			161,
			162,
			163,
			164,
			165,
			166,
			167,
			168,
			169,
			170,
			171,
			172,
			173,
			178,
			179,
			184,
			185,
			196,
			197,
			198,
			199,
			200,
			201,
			202,
			203,
			204,
			205,
			206,
			207,
			208,
			209,
			214,
			215,
			220,
			221
		];
	} catch (error) {}
	/**
	* Build up the default `inspectOpts` object from the environment variables.
	*
	*   $ DEBUG_COLORS=no DEBUG_DEPTH=10 DEBUG_SHOW_HIDDEN=enabled node script.js
	*/
	exports.inspectOpts = Object.keys(process.env).filter((key) => {
		return /^debug_/i.test(key);
	}).reduce((obj, key) => {
		const prop = key.substring(6).toLowerCase().replace(/_([a-z])/g, (_, k) => {
			return k.toUpperCase();
		});
		let val = process.env[key];
		if (/^(yes|on|true|enabled)$/i.test(val)) val = true;
		else if (/^(no|off|false|disabled)$/i.test(val)) val = false;
		else if (val === "null") val = null;
		else val = Number(val);
		obj[prop] = val;
		return obj;
	}, {});
	/**
	* Is stdout a TTY? Colored output is enabled when `true`.
	*/
	function useColors() {
		return "colors" in exports.inspectOpts ? Boolean(exports.inspectOpts.colors) : tty$1.isatty(process.stderr.fd);
	}
	/**
	* Adds ANSI color escape codes if enabled.
	*
	* @api public
	*/
	function formatArgs(args) {
		const { namespace: name, useColors } = this;
		if (useColors) {
			const c = this.color;
			const colorCode = "\x1B[3" + (c < 8 ? c : "8;5;" + c);
			const prefix = `  ${colorCode};1m${name} \u001B[0m`;
			args[0] = prefix + args[0].split("\n").join("\n" + prefix);
			args.push(colorCode + "m+" + module.exports.humanize(this.diff) + "\x1B[0m");
		} else args[0] = getDate() + name + " " + args[0];
	}
	function getDate() {
		if (exports.inspectOpts.hideDate) return "";
		return (/* @__PURE__ */ new Date()).toISOString() + " ";
	}
	/**
	* Invokes `util.formatWithOptions()` with the specified arguments and writes to stderr.
	*/
	function log(...args) {
		return process.stderr.write(util.formatWithOptions(exports.inspectOpts, ...args) + "\n");
	}
	/**
	* Save `namespaces`.
	*
	* @param {String} namespaces
	* @api private
	*/
	function save(namespaces) {
		if (namespaces) process.env.DEBUG = namespaces;
		else delete process.env.DEBUG;
	}
	/**
	* Load `namespaces`.
	*
	* @return {String} returns the previously persisted debug modes
	* @api private
	*/
	function load() {
		return process.env.DEBUG;
	}
	/**
	* Init logic for `debug` instances.
	*
	* Create a new `inspectOpts` object in case `useColors` is set
	* differently for a particular `debug` instance.
	*/
	function init(debug) {
		debug.inspectOpts = {};
		const keys = Object.keys(exports.inspectOpts);
		for (let i = 0; i < keys.length; i++) debug.inspectOpts[keys[i]] = exports.inspectOpts[keys[i]];
	}
	module.exports = require_common()(exports);
	const { formatters } = module.exports;
	/**
	* Map %o to `util.inspect()`, all on a single line.
	*/
	formatters.o = function(v) {
		this.inspectOpts.colors = this.useColors;
		return util.inspect(v, this.inspectOpts).split("\n").map((str) => str.trim()).join(" ");
	};
	/**
	* Map %O to `util.inspect()`, allowing multiple lines if needed.
	*/
	formatters.O = function(v) {
		this.inspectOpts.colors = this.useColors;
		return util.inspect(v, this.inspectOpts);
	};
}));

//#endregion
//#region node_modules/.pnpm/debug@4.4.3/node_modules/debug/src/index.js
var require_src = /* @__PURE__ */ __commonJSMin(((exports, module) => {
	/**
	* Detect Electron renderer / nwjs process, which is node, but we should
	* treat as a browser.
	*/
	if (typeof process === "undefined" || process.type === "renderer" || process.browser === true || process.__nwjs) module.exports = require_browser();
	else module.exports = require_node();
}));

//#endregion
//#region node_modules/.pnpm/@eslint+object-schema@3.0.2/node_modules/@eslint/object-schema/dist/esm/index.js
var import_src = /* @__PURE__ */ __toESM(require_src(), 1);
/**
* @fileoverview Merge Strategy
*/
/**
* Container class for several different merge strategies.
*/
var MergeStrategy = class {
	/**
	* Merges two keys by overwriting the first with the second.
	* @template TValue1 The type of the value from the first object key.
	* @template TValue2 The type of the value from the second object key.
	* @param {TValue1} value1 The value from the first object key.
	* @param {TValue2} value2 The value from the second object key.
	* @returns {TValue2} The second value.
	*/
	static overwrite(value1, value2) {
		return value2;
	}
	/**
	* Merges two keys by replacing the first with the second only if the
	* second is defined.
	* @template TValue1 The type of the value from the first object key.
	* @template TValue2 The type of the value from the second object key.
	* @param {TValue1} value1 The value from the first object key.
	* @param {TValue2} value2 The value from the second object key.
	* @returns {TValue1 | TValue2} The second value if it is defined.
	*/
	static replace(value1, value2) {
		if (typeof value2 !== "undefined") return value2;
		return value1;
	}
	/**
	* Merges two properties by assigning properties from the second to the first.
	* @template {Record<string | number | symbol, unknown> | undefined} TValue1 The type of the value from the first object key.
	* @template {Record<string | number | symbol, unknown>} TValue2 The type of the value from the second object key.
	* @param {TValue1} value1 The value from the first object key.
	* @param {TValue2} value2 The value from the second object key.
	* @returns {Omit<TValue1, keyof TValue2> & TValue2} A new object containing properties from both value1 and
	*      value2.
	*/
	static assign(value1, value2) {
		return Object.assign({}, value1, value2);
	}
};
/**
* @fileoverview Validation Strategy
*/
/**
* Container class for several different validation strategies.
*/
var ValidationStrategy = class {
	/**
	* Validates that a value is an array.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static array(value) {
		if (!Array.isArray(value)) throw new TypeError("Expected an array.");
	}
	/**
	* Validates that a value is a boolean.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static boolean(value) {
		if (typeof value !== "boolean") throw new TypeError("Expected a Boolean.");
	}
	/**
	* Validates that a value is a number.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static number(value) {
		if (typeof value !== "number") throw new TypeError("Expected a number.");
	}
	/**
	* Validates that a value is a object.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static object(value) {
		if (!value || typeof value !== "object") throw new TypeError("Expected an object.");
	}
	/**
	* Validates that a value is a object or null.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static "object?"(value) {
		if (typeof value !== "object") throw new TypeError("Expected an object or null.");
	}
	/**
	* Validates that a value is a string.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static string(value) {
		if (typeof value !== "string") throw new TypeError("Expected a string.");
	}
	/**
	* Validates that a value is a non-empty string.
	* @param {*} value The value to validate.
	* @returns {void}
	* @throws {TypeError} If the value is invalid.
	*/
	static "string!"(value) {
		if (typeof value !== "string" || value.length === 0) throw new TypeError("Expected a non-empty string.");
	}
};
/**
* @fileoverview Object Schema
*/
/** @import * as $typests from "./types.ts"; */
/** @typedef {$typests.BuiltInMergeStrategy} BuiltInMergeStrategy */
/** @typedef {$typests.BuiltInValidationStrategy} BuiltInValidationStrategy */
/** @typedef {$typests.ObjectDefinition} ObjectDefinition */
/** @typedef {$typests.PropertyDefinition} PropertyDefinition */
/**
* Validates a schema strategy.
* @param {string} name The name of the key this strategy is for.
* @param {PropertyDefinition} definition The strategy for the object key.
* @returns {void}
* @throws {TypeError} When the strategy is missing a name.
* @throws {TypeError} When the strategy is missing a merge() method.
* @throws {TypeError} When the strategy is missing a validate() method.
*/
function validateDefinition(name, definition) {
	let hasSchema = false;
	if (definition.schema) if (typeof definition.schema === "object") hasSchema = true;
	else throw new TypeError("Schema must be an object.");
	if (typeof definition.merge === "string") {
		if (!(definition.merge in MergeStrategy)) throw new TypeError(`Definition for key "${name}" missing valid merge strategy.`);
	} else if (!hasSchema && typeof definition.merge !== "function") throw new TypeError(`Definition for key "${name}" must have a merge property.`);
	if (typeof definition.validate === "string") {
		if (!(definition.validate in ValidationStrategy)) throw new TypeError(`Definition for key "${name}" missing valid validation strategy.`);
	} else if (!hasSchema && typeof definition.validate !== "function") throw new TypeError(`Definition for key "${name}" must have a validate() method.`);
}
/**
* Error when an unexpected key is found.
*/
var UnexpectedKeyError = class extends Error {
	/**
	* Creates a new instance.
	* @param {string} key The key that was unexpected.
	*/
	constructor(key) {
		super(`Unexpected key "${key}" found.`);
	}
};
/**
* Error when a required key is missing.
*/
var MissingKeyError = class extends Error {
	/**
	* Creates a new instance.
	* @param {string} key The key that was missing.
	*/
	constructor(key) {
		super(`Missing required key "${key}".`);
	}
};
/**
* Error when a key requires other keys that are missing.
*/
var MissingDependentKeysError = class extends Error {
	/**
	* Creates a new instance.
	* @param {string} key The key that was unexpected.
	* @param {Array<string>} requiredKeys The keys that are required.
	*/
	constructor(key, requiredKeys) {
		super(`Key "${key}" requires keys "${requiredKeys.join("\", \"")}".`);
	}
};
/**
* Wrapper error for errors occuring during a merge or validate operation.
*/
var WrapperError = class extends Error {
	/**
	* Creates a new instance.
	* @param {string} key The object key causing the error.
	* @param {Error} source The source error.
	*/
	constructor(key, source) {
		super(`Key "${key}": ${source.message}`, { cause: source });
		for (const sourceKey of Object.keys(source)) if (!(sourceKey in this)) this[sourceKey] = source[sourceKey];
	}
};
/**
* Represents an object validation/merging schema.
*/
var ObjectSchema = class ObjectSchema {
	/**
	* Track all definitions in the schema by key.
	* @type {Map<string, PropertyDefinition>}
	*/
	#definitions = /* @__PURE__ */ new Map();
	/**
	* Separately track any keys that are required for faster validation.
	* @type {Map<string, PropertyDefinition>}
	*/
	#requiredKeys = /* @__PURE__ */ new Map();
	/**
	* Creates a new instance.
	* @param {ObjectDefinition} definitions The schema definitions.
	* @throws {Error} When the definitions are missing or invalid.
	*/
	constructor(definitions) {
		if (!definitions) throw new Error("Schema definitions missing.");
		for (const key of Object.keys(definitions)) {
			validateDefinition(key, definitions[key]);
			if (typeof definitions[key].schema === "object") {
				const schema = new ObjectSchema(definitions[key].schema);
				definitions[key] = {
					...definitions[key],
					merge(first = {}, second = {}) {
						return schema.merge(first, second);
					},
					validate(value) {
						ValidationStrategy.object(value);
						schema.validate(value);
					}
				};
			}
			if (typeof definitions[key].merge === "string") definitions[key] = {
				...definitions[key],
				merge: MergeStrategy[definitions[key].merge]
			};
			if (typeof definitions[key].validate === "string") definitions[key] = {
				...definitions[key],
				validate: ValidationStrategy[definitions[key].validate]
			};
			this.#definitions.set(key, definitions[key]);
			if (definitions[key].required) this.#requiredKeys.set(key, definitions[key]);
		}
	}
	/**
	* Determines if a strategy has been registered for the given object key.
	* @param {string} key The object key to find a strategy for.
	* @returns {boolean} True if the key has a strategy registered, false if not.
	*/
	hasKey(key) {
		return this.#definitions.has(key);
	}
	/**
	* Merges objects together to create a new object comprised of the keys
	* of the all objects. Keys are merged based on the each key's merge
	* strategy.
	* @param {...Object} objects The objects to merge.
	* @returns {Object} A new object with a mix of all objects' keys.
	* @throws {TypeError} If any object is invalid.
	*/
	merge(...objects) {
		if (objects.length < 2) throw new TypeError("merge() requires at least two arguments.");
		if (objects.some((object) => object === null || typeof object !== "object")) throw new TypeError("All arguments must be objects.");
		return objects.reduce((result, object) => {
			this.validate(object);
			for (const [key, strategy] of this.#definitions) try {
				if (key in result || key in object) {
					const value = strategy.merge.call(this, result[key], object[key]);
					if (value !== void 0) result[key] = value;
				}
			} catch (ex) {
				throw new WrapperError(key, ex);
			}
			return result;
		}, {});
	}
	/**
	* Validates an object's keys based on the validate strategy for each key.
	* @param {Object} object The object to validate.
	* @returns {void}
	* @throws {Error} When the object is invalid.
	*/
	validate(object) {
		for (const key of Object.keys(object)) {
			if (!this.hasKey(key)) throw new UnexpectedKeyError(key);
			const definition = this.#definitions.get(key);
			if (Array.isArray(definition.requires)) {
				if (!definition.requires.every((otherKey) => otherKey in object)) throw new MissingDependentKeysError(key, definition.requires);
			}
			try {
				definition.validate.call(definition, object[key]);
			} catch (ex) {
				throw new WrapperError(key, ex);
			}
		}
		for (const [key] of this.#requiredKeys) if (!(key in object)) throw new MissingKeyError(key);
	}
};

//#endregion
//#region node_modules/.pnpm/@eslint+config-array@0.23.2_patch_hash=9c56839266cb75a04e2a96a342456c69afd7549bf6c13a9ade49cc6d42de892a/node_modules/@eslint/config-array/dist/esm/index.js
/**
* @fileoverview ConfigSchema
* @author Nicholas C. Zakas
*/
/** @import * as $eslintobjectschema from "@eslint/object-schema"; */
/** @typedef {$eslintobjectschema.PropertyDefinition} PropertyDefinition */
/** @typedef {$eslintobjectschema.ObjectDefinition} ObjectDefinition */
/**
* A strategy that does nothing.
* @type {PropertyDefinition}
*/
const NOOP_STRATEGY = {
	required: false,
	merge() {},
	validate() {}
};
/**
* The base schema that every ConfigArray uses.
* @type {ObjectDefinition}
*/
const baseSchema = Object.freeze({
	name: {
		required: false,
		merge() {},
		validate(value) {
			if (typeof value !== "string") throw new TypeError("Property must be a string.");
		}
	},
	basePath: NOOP_STRATEGY,
	files: NOOP_STRATEGY,
	ignores: NOOP_STRATEGY
});
/**
* @fileoverview ConfigSchema
* @author Nicholas C. Zakas
*/
/**
* Asserts that a given value is an array.
* @param {*} value The value to check.
* @returns {void}
* @throws {TypeError} When the value is not an array.
*/
function assertIsArray(value) {
	if (!Array.isArray(value)) throw new TypeError("Expected value to be an array.");
}
/**
* Asserts that a given value is an array containing only strings and functions.
* @param {*} value The value to check.
* @returns {void}
* @throws {TypeError} When the value is not an array of strings and functions.
*/
function assertIsArrayOfStringsAndFunctions(value) {
	assertIsArray(value);
	if (value.some((item) => typeof item !== "string" && typeof item !== "function")) throw new TypeError("Expected array to only contain strings and functions.");
}
/**
* Asserts that a given value is a non-empty array.
* @param {*} value The value to check.
* @returns {void}
* @throws {TypeError} When the value is not an array or an empty array.
*/
function assertIsNonEmptyArray(value) {
	if (!Array.isArray(value) || value.length === 0) throw new TypeError("Expected value to be a non-empty array.");
}
/**
* The schema for `files` and `ignores` that every ConfigArray uses.
* @type {ObjectDefinition}
*/
const filesAndIgnoresSchema = Object.freeze({
	basePath: {
		required: false,
		merge() {},
		validate(value) {
			if (typeof value !== "string") throw new TypeError("Expected value to be a string.");
		}
	},
	files: {
		required: false,
		merge() {},
		validate(value) {
			assertIsNonEmptyArray(value);
			value.forEach((item) => {
				if (Array.isArray(item)) assertIsArrayOfStringsAndFunctions(item);
				else if (typeof item !== "string" && typeof item !== "function") throw new TypeError("Items must be a string, a function, or an array of strings and functions.");
			});
		}
	},
	ignores: {
		required: false,
		merge() {},
		validate: assertIsArrayOfStringsAndFunctions
	}
});
/**
* @fileoverview ConfigArray
* @author Nicholas C. Zakas
*/
/** @import * as $typests from "./types.ts"; */
/** @typedef {$typests.ConfigObject} ConfigObject */
/** @import * as $minimatch from "minimatch"; */
/** @typedef {$minimatch.MinimatchOptions} MinimatchOptions */
/** @import * as PathImpl from "@jsr/std__path" */
/** @typedef {ObjectSchema} ObjectSchemaInstance */
const debug = (0, import_src.default)("@eslint/config-array");
/**
* A cache for minimatch instances.
* @type {Map<string, Minimatch>}
*/
const minimatchCache = /* @__PURE__ */ new Map();
/**
* A cache for negated minimatch instances.
* @type {Map<string, Minimatch>}
*/
const negatedMinimatchCache = /* @__PURE__ */ new Map();
/**
* Options to use with minimatch.
* @type {MinimatchOptions}
*/
const MINIMATCH_OPTIONS = { dot: true };
/**
* The types of config objects that are supported.
* @type {Set<string>}
*/
const CONFIG_TYPES = new Set(["array", "function"]);
/**
* Fields that are considered metadata and not part of the config object.
* @type {Set<string>}
*/
const META_FIELDS = new Set([
	"name",
	"basePath",
	"index"
]);
/**
* A schema containing just files and ignores for early validation.
* @type {ObjectSchemaInstance}
*/
const FILES_AND_IGNORES_SCHEMA = new ObjectSchema(filesAndIgnoresSchema);
const CONFIG_WITH_STATUS_EXTERNAL = Object.freeze({ status: "external" });
const CONFIG_WITH_STATUS_IGNORED = Object.freeze({ status: "ignored" });
const CONFIG_WITH_STATUS_UNCONFIGURED = Object.freeze({ status: "unconfigured" });
const EXTERNAL_PATH_REGEX = /^\.\.(?:\/|$)/u;
/**
* Wrapper error for config validation errors that adds a name to the front of the
* error message.
*/
var ConfigError = class extends Error {
	/**
	* Creates a new instance.
	* @param {string} name The config object name causing the error.
	* @param {number} index The index of the config object in the array.
	* @param {Object} options The options for the error.
	* @param {Error} [options.cause] The error that caused this error.
	* @param {string} [options.message] The message to use for the error.
	*/
	constructor(name, index, { cause, message }) {
		const finalMessage = message || cause.message;
		super(`Config ${name}: ${finalMessage}`, { cause });
		if (cause) {
			for (const key of Object.keys(cause)) if (!(key in this)) this[key] = cause[key];
		}
		/**
		* The name of the error.
		* @type {string}
		* @readonly
		*/
		this.name = "ConfigError";
		/**
		* The index of the config object in the array.
		* @type {number}
		* @readonly
		*/
		this.index = index;
	}
};
/**
* Gets the name of a config object.
* @param {ConfigObject} config The config object to get the name of.
* @returns {string} The name of the config object.
*/
function getConfigName(config) {
	if (config && typeof config.name === "string" && config.name) return `"${config.name}"`;
	return "(unnamed)";
}
/**
* Rethrows a config error with additional information about the config object.
* @param {object} config The config object to get the name of.
* @param {number} index The index of the config object in the array.
* @param {Error} error The error to rethrow.
* @throws {ConfigError} When the error is rethrown for a config.
*/
function rethrowConfigError(config, index, error) {
	throw new ConfigError(getConfigName(config), index, { cause: error });
}
/**
* Shorthand for checking if a value is a string.
* @param {any} value The value to check.
* @returns {boolean} True if a string, false if not.
*/
function isString(value) {
	return typeof value === "string";
}
/**
* Creates a function that asserts that the config is valid
* during normalization. This checks that the config is not nullish
* and that files and ignores keys  of a config object are valid as per base schema.
* @param {Object} config The config object to check.
* @param {number} index The index of the config object in the array.
* @returns {void}
* @throws {ConfigError} If the files and ignores keys of a config object are not valid.
*/
function assertValidBaseConfig(config, index) {
	if (config === null) throw new ConfigError(getConfigName(config), index, { message: "Unexpected null config." });
	if (config === void 0) throw new ConfigError(getConfigName(config), index, { message: "Unexpected undefined config." });
	if (typeof config !== "object") throw new ConfigError(getConfigName(config), index, { message: "Unexpected non-object config." });
	const validateConfig = {};
	if ("basePath" in config) validateConfig.basePath = config.basePath;
	if ("files" in config) validateConfig.files = config.files;
	if ("ignores" in config) validateConfig.ignores = config.ignores;
	try {
		FILES_AND_IGNORES_SCHEMA.validate(validateConfig);
	} catch (validationError) {
		rethrowConfigError(config, index, validationError);
	}
}
/**
* Wrapper around minimatch that caches minimatch patterns for
* faster matching speed over multiple file path evaluations.
* @param {string} filepath The file path to match.
* @param {string} pattern The glob pattern to match against.
* @param {object} options The minimatch options to use.
* @returns
*/
function doMatch(filepath, pattern, options = {}) {
	let cache = minimatchCache;
	if (options.flipNegate) cache = negatedMinimatchCache;
	let matcher = cache.get(pattern);
	if (!matcher) {
		matcher = new Minimatch(pattern, Object.assign({}, MINIMATCH_OPTIONS, options));
		cache.set(pattern, matcher);
	}
	return matcher.match(filepath);
}
/**
* Normalizes a pattern by removing the leading "./" if present.
* @param {string} pattern The pattern to normalize.
* @returns {string} The normalized pattern.
*/
function normalizePattern(pattern) {
	if (isString(pattern)) {
		if (pattern.startsWith("./")) return pattern.slice(2);
		if (pattern.startsWith("!./")) return `!${pattern.slice(3)}`;
	}
	return pattern;
}
/**
* Checks if a given pattern requires normalization.
* @param {any} pattern The pattern to check.
* @returns {boolean} True if the pattern needs normalization, false otherwise.
*
*/
function needsPatternNormalization(pattern) {
	return isString(pattern) && (pattern.startsWith("./") || pattern.startsWith("!./"));
}
/**
* Normalizes `files` and `ignores` patterns in a config by removing "./" prefixes.
* @param {Object} config The config object to normalize patterns in.
* @param {string} namespacedBasePath The namespaced base path of the directory to which config base path is relative.
* @param {PathImpl} path Path-handling implementation.
* @returns {Object} The normalized config object.
*/
function normalizeConfigPatterns(config, namespacedBasePath, path) {
	if (!config) return config;
	const hasBasePath = typeof config.basePath === "string";
	let needsNormalization = false;
	if (hasBasePath) needsNormalization = true;
	if (!needsNormalization && Array.isArray(config.files)) needsNormalization = config.files.some((pattern) => {
		if (Array.isArray(pattern)) return pattern.some(needsPatternNormalization);
		return needsPatternNormalization(pattern);
	});
	if (!needsNormalization && Array.isArray(config.ignores)) needsNormalization = config.ignores.some(needsPatternNormalization);
	if (!needsNormalization) return config;
	const newConfig = { ...config };
	if (hasBasePath) if (path.isAbsolute(config.basePath)) newConfig.basePath = path.toNamespacedPath(config.basePath);
	else newConfig.basePath = path.resolve(namespacedBasePath, config.basePath);
	if (Array.isArray(newConfig.files)) newConfig.files = newConfig.files.map((pattern) => {
		if (Array.isArray(pattern)) return pattern.map(normalizePattern);
		return normalizePattern(pattern);
	});
	if (Array.isArray(newConfig.ignores)) newConfig.ignores = newConfig.ignores.map(normalizePattern);
	return newConfig;
}
/**
* Normalizes a `ConfigArray` by flattening it and executing any functions
* that are found inside.
* @param {Array} items The items in a `ConfigArray`.
* @param {Object} context The context object to pass into any function
*      found.
* @param {Array<string>} extraConfigTypes The config types to check.
* @param {string} namespacedBasePath The namespaced base path of the directory to which config base paths are relative.
* @param {PathImpl} path Path-handling implementation.
* @returns {Promise<Array>} A flattened array containing only config objects.
* @throws {TypeError} When a config function returns a function.
*/
async function normalize(items, context, extraConfigTypes, namespacedBasePath, path) {
	const allowFunctions = extraConfigTypes.includes("function");
	const allowArrays = extraConfigTypes.includes("array");
	async function* flatTraverse(array) {
		for (let item of array) {
			if (typeof item === "function") {
				if (!allowFunctions) throw new TypeError("Unexpected function.");
				item = item(context);
				if (item.then) item = await item;
			}
			if (Array.isArray(item)) {
				if (!allowArrays) throw new TypeError("Unexpected array.");
				yield* flatTraverse(item);
			} else if (typeof item === "function") throw new TypeError("A config function can only return an object or array.");
			else yield item;
		}
	}
	const asyncIterable = await flatTraverse(items);
	const configs = [];
	for await (const config of asyncIterable) configs.push(normalizeConfigPatterns(config, namespacedBasePath, path));
	return configs;
}
/**
* Normalizes a `ConfigArray` by flattening it and executing any functions
* that are found inside.
* @param {Array} items The items in a `ConfigArray`.
* @param {Object} context The context object to pass into any function
*      found.
* @param {Array<string>} extraConfigTypes The config types to check.
* @param {string} namespacedBasePath The namespaced base path of the directory to which config base paths are relative.
* @param {PathImpl} path Path-handling implementation
* @returns {Array} A flattened array containing only config objects.
* @throws {TypeError} When a config function returns a function.
*/
function normalizeSync(items, context, extraConfigTypes, namespacedBasePath, path) {
	const allowFunctions = extraConfigTypes.includes("function");
	const allowArrays = extraConfigTypes.includes("array");
	function* flatTraverse(array) {
		for (let item of array) {
			if (typeof item === "function") {
				if (!allowFunctions) throw new TypeError("Unexpected function.");
				item = item(context);
				if (item.then) throw new TypeError("Async config functions are not supported.");
			}
			if (Array.isArray(item)) {
				if (!allowArrays) throw new TypeError("Unexpected array.");
				yield* flatTraverse(item);
			} else if (typeof item === "function") throw new TypeError("A config function can only return an object or array.");
			else yield item;
		}
	}
	const configs = [];
	for (const config of flatTraverse(items)) configs.push(normalizeConfigPatterns(config, namespacedBasePath, path));
	return configs;
}
/**
* Converts a given path to a relative path with all separator characters replaced by forward slashes (`"/"`).
* @param {string} fileOrDirPath The unprocessed path to convert.
* @param {string} namespacedBasePath The namespaced base path of the directory to which the calculated path shall be relative.
* @param {PathImpl} path Path-handling implementations.
* @returns {string} A relative path with all separator characters replaced by forward slashes.
*/
function toRelativePath(fileOrDirPath, namespacedBasePath, path) {
	const fullPath = path.resolve(namespacedBasePath, fileOrDirPath);
	const namespacedFullPath = path.toNamespacedPath(fullPath);
	return path.relative(namespacedBasePath, namespacedFullPath).replaceAll(path.SEPARATOR, "/");
}
/**
* Determines if a given file path should be ignored based on the given
* matcher.
* @param {Array<{ basePath?: string, ignores: Array<string|((string) => boolean)>}>} configs Configuration objects containing `ignores`.
* @param {string} filePath The unprocessed file path to check.
* @param {string} relativeFilePath The path of the file to check relative to the base path,
* 		using forward slash (`"/"`) as a separator.
* @param {Object} [basePathData] Additional data needed to recalculate paths for configuration objects
*  	that have `basePath` property.
* @param {string} [basePathData.basePath] Namespaced path to witch `relativeFilePath` is relative.
* @param {PathImpl} [basePathData.path] Path-handling implementation.
* @returns {boolean} True if the path should be ignored and false if not.
*/
function shouldIgnorePath(configs, filePath, relativeFilePath, { basePath, path } = {}) {
	let shouldIgnore = false;
	for (const config of configs) {
		let relativeFilePathToCheck = relativeFilePath;
		if (config.basePath) {
			relativeFilePathToCheck = toRelativePath(path.resolve(basePath, relativeFilePath), config.basePath, path);
			if (relativeFilePathToCheck === "" || EXTERNAL_PATH_REGEX.test(relativeFilePathToCheck)) continue;
			if (relativeFilePath.endsWith("/")) relativeFilePathToCheck += "/";
		}
		shouldIgnore = config.ignores.reduce((ignored, matcher) => {
			if (!ignored) {
				if (typeof matcher === "function") return matcher(filePath);
				if (!matcher.startsWith("!")) return doMatch(relativeFilePathToCheck, matcher);
				return false;
			}
			if (typeof matcher === "string" && matcher.startsWith("!")) return !doMatch(relativeFilePathToCheck, matcher, { flipNegate: true });
			return ignored;
		}, shouldIgnore);
	}
	return shouldIgnore;
}
/**
* Determines if a given file path is matched by a config. If the config
* has no `files` field, then it matches; otherwise, if a `files` field
* is present then we match the globs in `files` and exclude any globs in
* `ignores`.
* @param {string} filePath The unprocessed file path to check.
* @param {string} relativeFilePath The path of the file to check relative to the base path,
* 		using forward slash (`"/"`) as a separator.
* @param {Object} config The config object to check.
* @returns {boolean} True if the file path is matched by the config,
*      false if not.
*/
function pathMatches(filePath, relativeFilePath, config) {
	function match(pattern) {
		if (isString(pattern)) return doMatch(relativeFilePath, pattern);
		if (typeof pattern === "function") return pattern(filePath);
		throw new TypeError(`Unexpected matcher type ${pattern}.`);
	}
	let filePathMatchesPattern = config.files.some((pattern) => {
		if (Array.isArray(pattern)) return pattern.every(match);
		return match(pattern);
	});
	if (filePathMatchesPattern && config.ignores) filePathMatchesPattern = !shouldIgnorePath([{ ignores: config.ignores }], filePath, relativeFilePath);
	return filePathMatchesPattern;
}
/**
* Ensures that a ConfigArray has been normalized.
* @param {ConfigArray} configArray The ConfigArray to check.
* @returns {void}
* @throws {Error} When the `ConfigArray` is not normalized.
*/
function assertNormalized(configArray) {
	if (!configArray.isNormalized()) throw new Error("ConfigArray must be normalized to perform this operation.");
}
/**
* Ensures that config types are valid.
* @param {Array<string>} extraConfigTypes The config types to check.
* @returns {void}
* @throws {TypeError} When the config types array is invalid.
*/
function assertExtraConfigTypes(extraConfigTypes) {
	if (extraConfigTypes.length > 2) throw new TypeError("configTypes must be an array with at most two items.");
	for (const configType of extraConfigTypes) if (!CONFIG_TYPES.has(configType)) throw new TypeError(`Unexpected config type "${configType}" found. Expected one of: "object", "array", "function".`);
}
/**
* Returns path-handling implementations for Unix or Windows, depending on a given absolute path.
* @param {string} fileOrDirPath The absolute path to check.
* @returns {PathImpl} Path-handling implementations for the specified path.
* @throws {Error} An error is thrown if the specified argument is not an absolute path.
*/
function getPathImpl(fileOrDirPath) {
	if (fileOrDirPath.startsWith("/")) return posix_exports;
	if (/^(?:[A-Za-z]:[/\\]|[/\\]{2})/u.test(fileOrDirPath)) return windows_exports;
	throw new Error(`Expected an absolute path but received "${fileOrDirPath}"`);
}
const ConfigArraySymbol = {
	isNormalized: Symbol("isNormalized"),
	configCache: Symbol("configCache"),
	schema: Symbol("schema"),
	finalizeConfig: Symbol("finalizeConfig"),
	preprocessConfig: Symbol("preprocessConfig")
};
const dataCache = /* @__PURE__ */ new WeakMap();
/**
* Represents an array of config objects and provides method for working with
* those config objects.
*/
var ConfigArray = class extends Array {
	/**
	* The namespaced path of the config file directory.
	* @type {string}
	*/
	#namespacedBasePath;
	/**
	* Path-handling implementations.
	* @type {PathImpl}
	*/
	#path;
	/**
	* Creates a new instance of ConfigArray.
	* @param {Iterable|Function|Object} configs An iterable yielding config
	*      objects, or a config function, or a config object.
	* @param {Object} options The options for the ConfigArray.
	* @param {string} [options.basePath="/"] The absolute path of the config file directory.
	* 		Defaults to `"/"`.
	* @param {boolean} [options.normalized=false] Flag indicating if the
	*      configs have already been normalized.
	* @param {Object} [options.schema] The additional schema
	*      definitions to use for the ConfigArray schema.
	* @param {Array<string>} [options.extraConfigTypes] List of config types supported.
	* @throws {TypeError} When the `basePath` is not a non-empty string,
	*/
	constructor(configs, { basePath = "/", normalized = false, schema: customSchema, extraConfigTypes = [] } = {}) {
		super();
		/**
		* Tracks if the array has been normalized.
		* @property isNormalized
		* @type {boolean}
		* @private
		*/
		this[ConfigArraySymbol.isNormalized] = normalized;
		/**
		* The schema used for validating and merging configs.
		* @property schema
		* @type {ObjectSchemaInstance}
		* @private
		*/
		this[ConfigArraySymbol.schema] = new ObjectSchema(Object.assign({}, customSchema, baseSchema));
		if (!isString(basePath) || !basePath) throw new TypeError("basePath must be a non-empty string");
		/**
		* The path of the config file that this array was loaded from.
		* This is used to calculate filename matches.
		* @property basePath
		* @type {string}
		*/
		this.basePath = basePath;
		assertExtraConfigTypes(extraConfigTypes);
		/**
		* The supported config types.
		* @type {Array<string>}
		*/
		this.extraConfigTypes = [...extraConfigTypes];
		Object.freeze(this.extraConfigTypes);
		/**
		* A cache to store calculated configs for faster repeat lookup.
		* @property configCache
		* @type {Map<string, Object>}
		* @private
		*/
		this[ConfigArraySymbol.configCache] = /* @__PURE__ */ new Map();
		dataCache.set(this, {
			explicitMatches: /* @__PURE__ */ new Map(),
			directoryMatches: /* @__PURE__ */ new Map(),
			files: void 0,
			ignores: void 0
		});
		if (Array.isArray(configs)) this.push(...configs);
		else this.push(configs);
		this.#path = getPathImpl(basePath);
		this.#namespacedBasePath = this.#path.toNamespacedPath(basePath);
	}
	/**
	* Prevent normal array methods from creating a new `ConfigArray` instance.
	* This is to ensure that methods such as `slice()` won't try to create a
	* new instance of `ConfigArray` behind the scenes as doing so may throw
	* an error due to the different constructor signature.
	* @type {ArrayConstructor} The `Array` constructor.
	*/
	static get [Symbol.species]() {
		return Array;
	}
	/**
	* Returns the `files` globs from every config object in the array.
	* This can be used to determine which files will be matched by a
	* config array or to use as a glob pattern when no patterns are provided
	* for a command line interface.
	* @returns {Array<string|Function>} An array of matchers.
	*/
	get files() {
		assertNormalized(this);
		const cache = dataCache.get(this);
		if (cache.files) return cache.files;
		const result = [];
		for (const config of this) if (config.files) config.files.forEach((filePattern) => {
			result.push(filePattern);
		});
		cache.files = result;
		dataCache.set(this, cache);
		return result;
	}
	/**
	* Returns ignore matchers that should always be ignored regardless of
	* the matching `files` fields in any configs. This is necessary to mimic
	* the behavior of things like .gitignore and .eslintignore, allowing a
	* globbing operation to be faster.
	* @returns {Object[]} An array of config objects representing global ignores.
	*/
	get ignores() {
		assertNormalized(this);
		const cache = dataCache.get(this);
		if (cache.ignores) return cache.ignores;
		const result = [];
		for (const config of this) if (config.ignores && Object.keys(config).filter((key) => !META_FIELDS.has(key)).length === 1) result.push(config);
		cache.ignores = result;
		dataCache.set(this, cache);
		return result;
	}
	/**
	* Indicates if the config array has been normalized.
	* @returns {boolean} True if the config array is normalized, false if not.
	*/
	isNormalized() {
		return this[ConfigArraySymbol.isNormalized];
	}
	/**
	* Normalizes a config array by flattening embedded arrays and executing
	* config functions.
	* @param {Object} [context] The context object for config functions.
	* @returns {Promise<ConfigArray>} The current ConfigArray instance.
	*/
	async normalize(context = {}) {
		if (!this.isNormalized()) {
			const normalizedConfigs = await normalize(this, context, this.extraConfigTypes, this.#namespacedBasePath, this.#path);
			this.length = 0;
			this.push(...normalizedConfigs.map(this[ConfigArraySymbol.preprocessConfig].bind(this)));
			this.forEach(assertValidBaseConfig);
			this[ConfigArraySymbol.isNormalized] = true;
			Object.freeze(this);
		}
		return this;
	}
	/**
	* Normalizes a config array by flattening embedded arrays and executing
	* config functions.
	* @param {Object} [context] The context object for config functions.
	* @returns {ConfigArray} The current ConfigArray instance.
	*/
	normalizeSync(context = {}) {
		if (!this.isNormalized()) {
			const normalizedConfigs = normalizeSync(this, context, this.extraConfigTypes, this.#namespacedBasePath, this.#path);
			this.length = 0;
			this.push(...normalizedConfigs.map(this[ConfigArraySymbol.preprocessConfig].bind(this)));
			this.forEach(assertValidBaseConfig);
			this[ConfigArraySymbol.isNormalized] = true;
			Object.freeze(this);
		}
		return this;
	}
	/**
	* Finalizes the state of a config before being cached and returned by
	* `getConfig()`. Does nothing by default but is provided to be
	* overridden by subclasses as necessary.
	* @param {Object} config The config to finalize.
	* @returns {Object} The finalized config.
	*/
	[ConfigArraySymbol.finalizeConfig](config) {
		return config;
	}
	/**
	* Preprocesses a config during the normalization process. This is the
	* method to override if you want to convert an array item before it is
	* validated for the first time. For example, if you want to replace a
	* string with an object, this is the method to override.
	* @param {Object} config The config to preprocess.
	* @returns {Object} The config to use in place of the argument.
	*/
	[ConfigArraySymbol.preprocessConfig](config) {
		return config;
	}
	/**
	* Returns the config object for a given file path and a status that can be used to determine why a file has no config.
	* @param {string} filePath The path of a file to get a config for.
	* @returns {{ config?: Object, status: "ignored"|"external"|"unconfigured"|"matched" }}
	* An object with an optional property `config` and property `status`.
	* `config` is the config object for the specified file as returned by {@linkcode ConfigArray.getConfig},
	* `status` a is one of the constants returned by {@linkcode ConfigArray.getConfigStatus}.
	*/
	getConfigWithStatus(filePath) {
		assertNormalized(this);
		const cache = this[ConfigArraySymbol.configCache];
		if (cache.has(filePath)) return cache.get(filePath);
		const relativeToBaseFilePath = toRelativePath(filePath, this.#namespacedBasePath, this.#path);
		if (EXTERNAL_PATH_REGEX.test(relativeToBaseFilePath)) {
			debug(`No config for file ${filePath} outside of base path`);
			cache.set(filePath, CONFIG_WITH_STATUS_EXTERNAL);
			return CONFIG_WITH_STATUS_EXTERNAL;
		}
		if (this.isDirectoryIgnored(this.#path.dirname(filePath))) {
			debug(`Ignoring ${filePath} based on directory pattern`);
			cache.set(filePath, CONFIG_WITH_STATUS_IGNORED);
			return CONFIG_WITH_STATUS_IGNORED;
		}
		if (shouldIgnorePath(this.ignores, filePath, relativeToBaseFilePath, {
			basePath: this.#namespacedBasePath,
			path: this.#path
		})) {
			debug(`Ignoring ${filePath} based on file pattern`);
			cache.set(filePath, CONFIG_WITH_STATUS_IGNORED);
			return CONFIG_WITH_STATUS_IGNORED;
		}
		const matchingConfigIndices = [];
		let matchFound = false;
		const universalPattern = /^\*$|^!|\/\*{1,2}$/u;
		this.forEach((config, index) => {
			const relativeFilePath = config.basePath ? toRelativePath(this.#path.resolve(this.#namespacedBasePath, filePath), config.basePath, this.#path) : relativeToBaseFilePath;
			if (config.basePath && EXTERNAL_PATH_REGEX.test(relativeFilePath)) {
				debug(`Skipped config found for ${filePath} (based on config's base path: ${config.basePath}`);
				return;
			}
			if (!config.files) {
				if (!config.ignores) {
					debug(`Universal config found for ${filePath}`);
					matchingConfigIndices.push(index);
					return;
				}
				if (Object.keys(config).filter((key) => !META_FIELDS.has(key)).length === 1) {
					debug(`Skipped config found for ${filePath} (global ignores)`);
					return;
				}
				if (shouldIgnorePath([{ ignores: config.ignores }], filePath, relativeFilePath)) {
					debug(`Skipped config found for ${filePath} (based on ignores: ${config.ignores})`);
					return;
				}
				debug(`Matching config found for ${filePath} (based on ignores: ${config.ignores})`);
				matchingConfigIndices.push(index);
				return;
			}
			const nonUniversalFiles = [];
			const universalFiles = config.files.filter((element) => {
				if (Array.isArray(element)) {
					if (element.every((pattern) => universalPattern.test(pattern))) return true;
					nonUniversalFiles.push(element);
					return false;
				}
				if (universalPattern.test(element)) return true;
				nonUniversalFiles.push(element);
				return false;
			});
			if (universalFiles.length) {
				debug("Universal files patterns found. Checking carefully.");
				if (nonUniversalFiles.length && pathMatches(filePath, relativeFilePath, {
					files: nonUniversalFiles,
					ignores: config.ignores
				})) {
					debug(`Matching config found for ${filePath}`);
					matchingConfigIndices.push(index);
					matchFound = true;
					return;
				}
				if (universalFiles.length && pathMatches(filePath, relativeFilePath, {
					files: universalFiles,
					ignores: config.ignores
				})) {
					debug(`Matching config found for ${filePath}`);
					matchingConfigIndices.push(index);
					return;
				}
				return;
			}
			if (pathMatches(filePath, relativeFilePath, config)) {
				debug(`Matching config found for ${filePath}`);
				matchingConfigIndices.push(index);
				matchFound = true;
			}
		});
		if (!matchFound) {
			debug(`No matching configs found for ${filePath}`);
			cache.set(filePath, CONFIG_WITH_STATUS_UNCONFIGURED);
			return CONFIG_WITH_STATUS_UNCONFIGURED;
		}
		const indicesKey = matchingConfigIndices.toString();
		let configWithStatus = cache.get(indicesKey);
		if (configWithStatus) {
			cache.set(filePath, configWithStatus);
			return configWithStatus;
		}
		let finalConfig = matchingConfigIndices.reduce((result, index) => {
			try {
				return this[ConfigArraySymbol.schema].merge(result, this[index]);
			} catch (validationError) {
				rethrowConfigError(this[index], index, validationError);
			}
		}, {});
		finalConfig = this[ConfigArraySymbol.finalizeConfig](finalConfig);
		configWithStatus = Object.freeze({
			config: finalConfig,
			status: "matched"
		});
		cache.set(filePath, configWithStatus);
		cache.set(indicesKey, configWithStatus);
		return configWithStatus;
	}
	/**
	* Returns the config object for a given file path.
	* @param {string} filePath The path of a file to get a config for.
	* @returns {Object|undefined} The config object for this file or `undefined`.
	*/
	getConfig(filePath) {
		return this.getConfigWithStatus(filePath).config;
	}
	/**
	* Determines whether a file has a config or why it doesn't.
	* @param {string} filePath The path of the file to check.
	* @returns {"ignored"|"external"|"unconfigured"|"matched"} One of the following values:
	* * `"ignored"`: the file is ignored
	* * `"external"`: the file is outside the base path
	* * `"unconfigured"`: the file is not matched by any config
	* * `"matched"`: the file has a matching config
	*/
	getConfigStatus(filePath) {
		return this.getConfigWithStatus(filePath).status;
	}
	/**
	* Determines if the given filepath is ignored based on the configs.
	* @param {string} filePath The path of a file to check.
	* @returns {boolean} True if the path is ignored, false if not.
	* @deprecated Use `isFileIgnored` instead.
	*/
	isIgnored(filePath) {
		return this.isFileIgnored(filePath);
	}
	/**
	* Determines if the given filepath is ignored based on the configs.
	* @param {string} filePath The path of a file to check.
	* @returns {boolean} True if the path is ignored, false if not.
	*/
	isFileIgnored(filePath) {
		return this.getConfigStatus(filePath) === "ignored";
	}
	/**
	* Determines if the given directory is ignored based on the configs.
	* This checks only default `ignores` that don't have `files` in the
	* same config. A pattern such as `/foo` be considered to ignore the directory
	* while a pattern such as `/foo/**` is not considered to ignore the
	* directory because it is matching files.
	* @param {string} directoryPath The path of a directory to check.
	* @returns {boolean} True if the directory is ignored, false if not. Will
	* 		return true for any directory that is not inside of `basePath`.
	* @throws {Error} When the `ConfigArray` is not normalized.
	*/
	isDirectoryIgnored(directoryPath) {
		assertNormalized(this);
		const relativeDirectoryPath = toRelativePath(directoryPath, this.#namespacedBasePath, this.#path);
		if (relativeDirectoryPath === "") return false;
		if (EXTERNAL_PATH_REGEX.test(relativeDirectoryPath)) return true;
		const cache = dataCache.get(this).directoryMatches;
		if (cache.has(relativeDirectoryPath)) return cache.get(relativeDirectoryPath);
		const directoryParts = relativeDirectoryPath.split("/");
		let relativeDirectoryToCheck = "";
		let result;
		do {
			relativeDirectoryToCheck += `${directoryParts.shift()}/`;
			result = shouldIgnorePath(this.ignores, this.#path.join(this.basePath, relativeDirectoryToCheck), relativeDirectoryToCheck, {
				basePath: this.#namespacedBasePath,
				path: this.#path
			});
			cache.set(relativeDirectoryToCheck, result);
		} while (!result && directoryParts.length);
		cache.set(relativeDirectoryPath, result);
		return result;
	}
};

//#endregion
//#region shared/configs.ts
const minimatchOpts = {
	dot: true,
	flipNegate: true
};
const _matchInstances = /* @__PURE__ */ new Map();
function minimatch(file, pattern) {
	let m = _matchInstances.get(pattern);
	if (!m) {
		m = new Minimatch(pattern, minimatchOpts);
		_matchInstances.set(pattern, m);
	}
	return m.match(file);
}
function getMatchedGlobs(file, glob) {
	return (Array.isArray(glob) ? glob : [glob]).flat().filter((glob) => minimatch(file, glob)).flat();
}
function matchFile(filepath, configs, basePath) {
	const result = {
		filepath,
		globs: [],
		configs: []
	};
	const { config: globalMatchedConfig = {}, status: globalMatchStatus } = buildConfigArray(configs, basePath).getConfigWithStatus(filepath);
	configs.forEach((config) => {
		const positive = getMatchedGlobs(filepath, config.files || []);
		const negative = getMatchedGlobs(filepath, config.ignores || []);
		if (globalMatchStatus === "matched" && globalMatchedConfig.index?.includes(config.index) && positive.length > 0) {
			result.configs.push(config.index);
			result.globs.push(...positive);
		}
		result.globs.push(...negative);
	});
	result.globs = [...new Set(result.globs)];
	return result;
}
const NOOP_SCHEMA = {
	merge: "replace",
	validate() {}
};
const FLAT_CONFIG_NOOP_SCHEMA = {
	settings: NOOP_SCHEMA,
	linterOptions: NOOP_SCHEMA,
	language: NOOP_SCHEMA,
	languageOptions: NOOP_SCHEMA,
	processor: NOOP_SCHEMA,
	plugins: NOOP_SCHEMA,
	index: {
		...NOOP_SCHEMA,
		merge(v1, v2) {
			return [v1].concat(v2).flat();
		}
	},
	rules: NOOP_SCHEMA
};
function buildConfigArray(configs, basePath) {
	return new ConfigArray(configs, {
		basePath,
		schema: FLAT_CONFIG_NOOP_SCHEMA
	}).normalizeSync();
}

//#endregion
//#region src/constants.ts
const configFilenames = [
	"eslint.config.js",
	"eslint.config.mjs",
	"eslint.config.cjs",
	"eslint.config.ts",
	"eslint.config.mts",
	"eslint.config.cts"
];
const legacyConfigFilenames = [
	".eslintrc.js",
	".eslintrc.cjs",
	".eslintrc.yaml",
	".eslintrc.yml",
	".eslintrc.json"
];
const MARK_CHECK = c.green("✔");
const MARK_INFO = c.blue("ℹ");
const MARK_ERROR = c.red("✖");

//#endregion
//#region src/errors.ts
var ConfigInspectorError = class extends Error {
	prettyPrint() {
		console.error(MARK_ERROR, this.message);
	}
};
var ConfigPathError = class extends ConfigInspectorError {
	name = "ConfigPathError";
	constructor(basePath, configFilenames) {
		super("Cannot find ESLint config file");
		this.basePath = basePath;
		this.configFilenames = configFilenames;
	}
	prettyPrint() {
		console.error(MARK_ERROR, this.message, c.dim(`

Looked in ${c.underline(this.basePath)} and parent folders for:

 * ${this.configFilenames.join("\n * ")}`));
	}
};
var ConfigPathLegacyError = class extends ConfigInspectorError {
	name = "ConfigPathLegacyError";
	constructor(basePath, configFilename) {
		super("Found ESLint legacy config file");
		this.basePath = basePath;
		this.configFilename = configFilename;
	}
	prettyPrint() {
		console.error(MARK_ERROR, this.message, c.dim(`

Encountered unsupported legacy config ${c.underline(this.configFilename)} in ${c.underline(this.basePath)}

\`@eslint/config-inspector\` only works with the new flat config format:
https://eslint.org/docs/latest/use/configure/configuration-files-new`));
	}
};

//#endregion
//#region src/configs.ts
/**
* Search and read the ESLint config file.
*
* Accept an options object to specify the working directory path and overrides.
*/
async function resolveConfigPath(options) {
	let { cwd, userConfigPath, userBasePath } = options;
	if (userBasePath) userBasePath = resolve$3(cwd, userBasePath);
	const lookupBasePath = userBasePath || cwd;
	let configPath = userConfigPath && resolve$3(cwd, userConfigPath);
	if (!configPath) configPath = await findUp(configFilenames, { cwd: lookupBasePath });
	if (!configPath) {
		const legacyConfigPath = await findUp(legacyConfigFilenames, { cwd: lookupBasePath });
		throw legacyConfigPath ? new ConfigPathLegacyError(`${relative$2(cwd, dirname$2(legacyConfigPath))}/`, basename$2(legacyConfigPath)) : new ConfigPathError(`${relative$2(cwd, lookupBasePath)}/`, configFilenames);
	}
	const basePath = normalize$3(userBasePath || (userConfigPath ? cwd : dirname$2(configPath)));
	configPath = normalize$3(configPath);
	return {
		basePath,
		configPath
	};
}
/**
* Search and read the ESLint config file, processed into inspector payload with module dependencies
*
* Accept an options object to specify the working directory path and overrides.
*
* It uses `bundle-requires` load the config file and find it's dependencies.
* It always get the latest version of the config file (no ESM cache).
*/
async function readConfig(options) {
	const { chdir = true, globMatchedFiles: globFiles = true } = options;
	const { basePath, configPath } = await resolveConfigPath(options);
	if (chdir && basePath !== process$1.cwd()) process$1.chdir(basePath);
	console.log(MARK_INFO, `Reading ESLint config from`, c.blue(configPath));
	const { mod, dependencies } = await bundleRequire({
		filepath: configPath,
		cwd: basePath,
		tsconfig: false
	});
	let rawConfigs = await (mod.default ?? mod);
	if (!Array.isArray(rawConfigs)) rawConfigs = [rawConfigs];
	rawConfigs.unshift({
		index: 1,
		name: "eslint/defaults/languages",
		languageOptions: {
			sourceType: "module",
			ecmaVersion: "latest",
			parserOptions: {}
		},
		linterOptions: { reportUnusedDisableDirectives: 1 }
	}, {
		index: 2,
		name: "eslint/defaults/ignores",
		ignores: ["**/node_modules/", ".git/"]
	}, {
		index: 3,
		name: "eslint/defaults/files",
		files: ["**/*.js", "**/*.mjs"]
	}, {
		index: 4,
		name: "eslint/defaults/files-cjs",
		files: ["**/*.cjs"],
		languageOptions: {
			sourceType: "commonjs",
			ecmaVersion: "latest"
		}
	});
	const rulesMap = /* @__PURE__ */ new Map();
	const eslintRules = await import(await resolve$2("eslint/use-at-your-own-risk", { url: basePath }).catch(() => null) || "eslint/use-at-your-own-risk").then((r) => r.default.builtinRules);
	for (const [name, rule] of eslintRules.entries()) rulesMap.set(name, {
		...rule.meta,
		name,
		plugin: "eslint",
		schema: void 0,
		messages: void 0
	});
	for (const item of rawConfigs) for (const [prefix, plugin] of Object.entries(item.plugins ?? {})) for (const [name, rule] of Object.entries(plugin.rules ?? {})) rulesMap.set(`${prefix}/${name}`, {
		...rule.meta,
		name: `${prefix}/${name}`,
		plugin: prefix,
		schema: void 0,
		messages: void 0
	});
	const rules = Object.fromEntries(rulesMap.entries());
	const configs = rawConfigs.map((c, idx) => {
		return {
			...c,
			index: idx,
			plugins: c.plugins ? Object.fromEntries(Object.entries(c.plugins ?? {}).map(([prefix]) => [prefix, {}]).filter((i) => i[0])) : void 0,
			languageOptions: c.languageOptions ? {
				...c.languageOptions,
				parser: c.languageOptions.parser?.meta?.name
			} : void 0,
			processor: c.processor?.meta?.name
		};
	});
	console.log(MARK_CHECK, "Loaded with", configs.length, "config items and", Object.keys(rules).length, "rules");
	const payload = {
		configs,
		rules,
		files: globFiles ? await globMatchedFiles(basePath, configs, rawConfigs) : void 0,
		meta: {
			lastUpdate: Date.now(),
			basePath,
			configPath
		}
	};
	return {
		configs: rawConfigs,
		dependencies,
		payload
	};
}
async function globMatchedFiles(basePath, configs, rawConfigs) {
	console.log(MARK_INFO, "Globbing matched files");
	return [...await configArrayFindFiles({
		basePath,
		configs: buildConfigArray(rawConfigs, basePath)
	})].sort().map((filepath) => {
		filepath = relative$2(basePath, filepath).replaceAll("\\", "/");
		const result = matchFile(filepath, configs, basePath);
		if (!result.configs.length) return void 0;
		return result;
	}).filter((i) => i);
}

//#endregion
//#region src/dirs.ts
const distDir = fileURLToPath(new URL("../dist/public", import.meta.url));

//#endregion
//#region node_modules/.pnpm/mrmime@2.0.1/node_modules/mrmime/index.mjs
const mimes = {
	"3g2": "video/3gpp2",
	"3gp": "video/3gpp",
	"3gpp": "video/3gpp",
	"3mf": "model/3mf",
	"aac": "audio/aac",
	"ac": "application/pkix-attr-cert",
	"adp": "audio/adpcm",
	"adts": "audio/aac",
	"ai": "application/postscript",
	"aml": "application/automationml-aml+xml",
	"amlx": "application/automationml-amlx+zip",
	"amr": "audio/amr",
	"apng": "image/apng",
	"appcache": "text/cache-manifest",
	"appinstaller": "application/appinstaller",
	"appx": "application/appx",
	"appxbundle": "application/appxbundle",
	"asc": "application/pgp-keys",
	"atom": "application/atom+xml",
	"atomcat": "application/atomcat+xml",
	"atomdeleted": "application/atomdeleted+xml",
	"atomsvc": "application/atomsvc+xml",
	"au": "audio/basic",
	"avci": "image/avci",
	"avcs": "image/avcs",
	"avif": "image/avif",
	"aw": "application/applixware",
	"bdoc": "application/bdoc",
	"bin": "application/octet-stream",
	"bmp": "image/bmp",
	"bpk": "application/octet-stream",
	"btf": "image/prs.btif",
	"btif": "image/prs.btif",
	"buffer": "application/octet-stream",
	"ccxml": "application/ccxml+xml",
	"cdfx": "application/cdfx+xml",
	"cdmia": "application/cdmi-capability",
	"cdmic": "application/cdmi-container",
	"cdmid": "application/cdmi-domain",
	"cdmio": "application/cdmi-object",
	"cdmiq": "application/cdmi-queue",
	"cer": "application/pkix-cert",
	"cgm": "image/cgm",
	"cjs": "application/node",
	"class": "application/java-vm",
	"coffee": "text/coffeescript",
	"conf": "text/plain",
	"cpl": "application/cpl+xml",
	"cpt": "application/mac-compactpro",
	"crl": "application/pkix-crl",
	"css": "text/css",
	"csv": "text/csv",
	"cu": "application/cu-seeme",
	"cwl": "application/cwl",
	"cww": "application/prs.cww",
	"davmount": "application/davmount+xml",
	"dbk": "application/docbook+xml",
	"deb": "application/octet-stream",
	"def": "text/plain",
	"deploy": "application/octet-stream",
	"dib": "image/bmp",
	"disposition-notification": "message/disposition-notification",
	"dist": "application/octet-stream",
	"distz": "application/octet-stream",
	"dll": "application/octet-stream",
	"dmg": "application/octet-stream",
	"dms": "application/octet-stream",
	"doc": "application/msword",
	"dot": "application/msword",
	"dpx": "image/dpx",
	"drle": "image/dicom-rle",
	"dsc": "text/prs.lines.tag",
	"dssc": "application/dssc+der",
	"dtd": "application/xml-dtd",
	"dump": "application/octet-stream",
	"dwd": "application/atsc-dwd+xml",
	"ear": "application/java-archive",
	"ecma": "application/ecmascript",
	"elc": "application/octet-stream",
	"emf": "image/emf",
	"eml": "message/rfc822",
	"emma": "application/emma+xml",
	"emotionml": "application/emotionml+xml",
	"eps": "application/postscript",
	"epub": "application/epub+zip",
	"exe": "application/octet-stream",
	"exi": "application/exi",
	"exp": "application/express",
	"exr": "image/aces",
	"ez": "application/andrew-inset",
	"fdf": "application/fdf",
	"fdt": "application/fdt+xml",
	"fits": "image/fits",
	"g3": "image/g3fax",
	"gbr": "application/rpki-ghostbusters",
	"geojson": "application/geo+json",
	"gif": "image/gif",
	"glb": "model/gltf-binary",
	"gltf": "model/gltf+json",
	"gml": "application/gml+xml",
	"gpx": "application/gpx+xml",
	"gram": "application/srgs",
	"grxml": "application/srgs+xml",
	"gxf": "application/gxf",
	"gz": "application/gzip",
	"h261": "video/h261",
	"h263": "video/h263",
	"h264": "video/h264",
	"heic": "image/heic",
	"heics": "image/heic-sequence",
	"heif": "image/heif",
	"heifs": "image/heif-sequence",
	"hej2": "image/hej2k",
	"held": "application/atsc-held+xml",
	"hjson": "application/hjson",
	"hlp": "application/winhlp",
	"hqx": "application/mac-binhex40",
	"hsj2": "image/hsj2",
	"htm": "text/html",
	"html": "text/html",
	"ics": "text/calendar",
	"ief": "image/ief",
	"ifb": "text/calendar",
	"iges": "model/iges",
	"igs": "model/iges",
	"img": "application/octet-stream",
	"in": "text/plain",
	"ini": "text/plain",
	"ink": "application/inkml+xml",
	"inkml": "application/inkml+xml",
	"ipfix": "application/ipfix",
	"iso": "application/octet-stream",
	"its": "application/its+xml",
	"jade": "text/jade",
	"jar": "application/java-archive",
	"jhc": "image/jphc",
	"jls": "image/jls",
	"jp2": "image/jp2",
	"jpe": "image/jpeg",
	"jpeg": "image/jpeg",
	"jpf": "image/jpx",
	"jpg": "image/jpeg",
	"jpg2": "image/jp2",
	"jpgm": "image/jpm",
	"jpgv": "video/jpeg",
	"jph": "image/jph",
	"jpm": "image/jpm",
	"jpx": "image/jpx",
	"js": "text/javascript",
	"json": "application/json",
	"json5": "application/json5",
	"jsonld": "application/ld+json",
	"jsonml": "application/jsonml+json",
	"jsx": "text/jsx",
	"jt": "model/jt",
	"jxl": "image/jxl",
	"jxr": "image/jxr",
	"jxra": "image/jxra",
	"jxrs": "image/jxrs",
	"jxs": "image/jxs",
	"jxsc": "image/jxsc",
	"jxsi": "image/jxsi",
	"jxss": "image/jxss",
	"kar": "audio/midi",
	"ktx": "image/ktx",
	"ktx2": "image/ktx2",
	"less": "text/less",
	"lgr": "application/lgr+xml",
	"list": "text/plain",
	"litcoffee": "text/coffeescript",
	"log": "text/plain",
	"lostxml": "application/lost+xml",
	"lrf": "application/octet-stream",
	"m1v": "video/mpeg",
	"m21": "application/mp21",
	"m2a": "audio/mpeg",
	"m2t": "video/mp2t",
	"m2ts": "video/mp2t",
	"m2v": "video/mpeg",
	"m3a": "audio/mpeg",
	"m4a": "audio/mp4",
	"m4p": "application/mp4",
	"m4s": "video/iso.segment",
	"ma": "application/mathematica",
	"mads": "application/mads+xml",
	"maei": "application/mmt-aei+xml",
	"man": "text/troff",
	"manifest": "text/cache-manifest",
	"map": "application/json",
	"mar": "application/octet-stream",
	"markdown": "text/markdown",
	"mathml": "application/mathml+xml",
	"mb": "application/mathematica",
	"mbox": "application/mbox",
	"md": "text/markdown",
	"mdx": "text/mdx",
	"me": "text/troff",
	"mesh": "model/mesh",
	"meta4": "application/metalink4+xml",
	"metalink": "application/metalink+xml",
	"mets": "application/mets+xml",
	"mft": "application/rpki-manifest",
	"mid": "audio/midi",
	"midi": "audio/midi",
	"mime": "message/rfc822",
	"mj2": "video/mj2",
	"mjp2": "video/mj2",
	"mjs": "text/javascript",
	"mml": "text/mathml",
	"mods": "application/mods+xml",
	"mov": "video/quicktime",
	"mp2": "audio/mpeg",
	"mp21": "application/mp21",
	"mp2a": "audio/mpeg",
	"mp3": "audio/mpeg",
	"mp4": "video/mp4",
	"mp4a": "audio/mp4",
	"mp4s": "application/mp4",
	"mp4v": "video/mp4",
	"mpd": "application/dash+xml",
	"mpe": "video/mpeg",
	"mpeg": "video/mpeg",
	"mpf": "application/media-policy-dataset+xml",
	"mpg": "video/mpeg",
	"mpg4": "video/mp4",
	"mpga": "audio/mpeg",
	"mpp": "application/dash-patch+xml",
	"mrc": "application/marc",
	"mrcx": "application/marcxml+xml",
	"ms": "text/troff",
	"mscml": "application/mediaservercontrol+xml",
	"msh": "model/mesh",
	"msi": "application/octet-stream",
	"msix": "application/msix",
	"msixbundle": "application/msixbundle",
	"msm": "application/octet-stream",
	"msp": "application/octet-stream",
	"mtl": "model/mtl",
	"mts": "video/mp2t",
	"musd": "application/mmt-usd+xml",
	"mxf": "application/mxf",
	"mxmf": "audio/mobile-xmf",
	"mxml": "application/xv+xml",
	"n3": "text/n3",
	"nb": "application/mathematica",
	"nq": "application/n-quads",
	"nt": "application/n-triples",
	"obj": "model/obj",
	"oda": "application/oda",
	"oga": "audio/ogg",
	"ogg": "audio/ogg",
	"ogv": "video/ogg",
	"ogx": "application/ogg",
	"omdoc": "application/omdoc+xml",
	"onepkg": "application/onenote",
	"onetmp": "application/onenote",
	"onetoc": "application/onenote",
	"onetoc2": "application/onenote",
	"opf": "application/oebps-package+xml",
	"opus": "audio/ogg",
	"otf": "font/otf",
	"owl": "application/rdf+xml",
	"oxps": "application/oxps",
	"p10": "application/pkcs10",
	"p7c": "application/pkcs7-mime",
	"p7m": "application/pkcs7-mime",
	"p7s": "application/pkcs7-signature",
	"p8": "application/pkcs8",
	"pdf": "application/pdf",
	"pfr": "application/font-tdpfr",
	"pgp": "application/pgp-encrypted",
	"pkg": "application/octet-stream",
	"pki": "application/pkixcmp",
	"pkipath": "application/pkix-pkipath",
	"pls": "application/pls+xml",
	"png": "image/png",
	"prc": "model/prc",
	"prf": "application/pics-rules",
	"provx": "application/provenance+xml",
	"ps": "application/postscript",
	"pskcxml": "application/pskc+xml",
	"pti": "image/prs.pti",
	"qt": "video/quicktime",
	"raml": "application/raml+yaml",
	"rapd": "application/route-apd+xml",
	"rdf": "application/rdf+xml",
	"relo": "application/p2p-overlay+xml",
	"rif": "application/reginfo+xml",
	"rl": "application/resource-lists+xml",
	"rld": "application/resource-lists-diff+xml",
	"rmi": "audio/midi",
	"rnc": "application/relax-ng-compact-syntax",
	"rng": "application/xml",
	"roa": "application/rpki-roa",
	"roff": "text/troff",
	"rq": "application/sparql-query",
	"rs": "application/rls-services+xml",
	"rsat": "application/atsc-rsat+xml",
	"rsd": "application/rsd+xml",
	"rsheet": "application/urc-ressheet+xml",
	"rss": "application/rss+xml",
	"rtf": "text/rtf",
	"rtx": "text/richtext",
	"rusd": "application/route-usd+xml",
	"s3m": "audio/s3m",
	"sbml": "application/sbml+xml",
	"scq": "application/scvp-cv-request",
	"scs": "application/scvp-cv-response",
	"sdp": "application/sdp",
	"senmlx": "application/senml+xml",
	"sensmlx": "application/sensml+xml",
	"ser": "application/java-serialized-object",
	"setpay": "application/set-payment-initiation",
	"setreg": "application/set-registration-initiation",
	"sgi": "image/sgi",
	"sgm": "text/sgml",
	"sgml": "text/sgml",
	"shex": "text/shex",
	"shf": "application/shf+xml",
	"shtml": "text/html",
	"sieve": "application/sieve",
	"sig": "application/pgp-signature",
	"sil": "audio/silk",
	"silo": "model/mesh",
	"siv": "application/sieve",
	"slim": "text/slim",
	"slm": "text/slim",
	"sls": "application/route-s-tsid+xml",
	"smi": "application/smil+xml",
	"smil": "application/smil+xml",
	"snd": "audio/basic",
	"so": "application/octet-stream",
	"spdx": "text/spdx",
	"spp": "application/scvp-vp-response",
	"spq": "application/scvp-vp-request",
	"spx": "audio/ogg",
	"sql": "application/sql",
	"sru": "application/sru+xml",
	"srx": "application/sparql-results+xml",
	"ssdl": "application/ssdl+xml",
	"ssml": "application/ssml+xml",
	"stk": "application/hyperstudio",
	"stl": "model/stl",
	"stpx": "model/step+xml",
	"stpxz": "model/step-xml+zip",
	"stpz": "model/step+zip",
	"styl": "text/stylus",
	"stylus": "text/stylus",
	"svg": "image/svg+xml",
	"svgz": "image/svg+xml",
	"swidtag": "application/swid+xml",
	"t": "text/troff",
	"t38": "image/t38",
	"td": "application/urc-targetdesc+xml",
	"tei": "application/tei+xml",
	"teicorpus": "application/tei+xml",
	"text": "text/plain",
	"tfi": "application/thraud+xml",
	"tfx": "image/tiff-fx",
	"tif": "image/tiff",
	"tiff": "image/tiff",
	"toml": "application/toml",
	"tr": "text/troff",
	"trig": "application/trig",
	"ts": "video/mp2t",
	"tsd": "application/timestamped-data",
	"tsv": "text/tab-separated-values",
	"ttc": "font/collection",
	"ttf": "font/ttf",
	"ttl": "text/turtle",
	"ttml": "application/ttml+xml",
	"txt": "text/plain",
	"u3d": "model/u3d",
	"u8dsn": "message/global-delivery-status",
	"u8hdr": "message/global-headers",
	"u8mdn": "message/global-disposition-notification",
	"u8msg": "message/global",
	"ubj": "application/ubjson",
	"uri": "text/uri-list",
	"uris": "text/uri-list",
	"urls": "text/uri-list",
	"vcard": "text/vcard",
	"vrml": "model/vrml",
	"vtt": "text/vtt",
	"vxml": "application/voicexml+xml",
	"war": "application/java-archive",
	"wasm": "application/wasm",
	"wav": "audio/wav",
	"weba": "audio/webm",
	"webm": "video/webm",
	"webmanifest": "application/manifest+json",
	"webp": "image/webp",
	"wgsl": "text/wgsl",
	"wgt": "application/widget",
	"wif": "application/watcherinfo+xml",
	"wmf": "image/wmf",
	"woff": "font/woff",
	"woff2": "font/woff2",
	"wrl": "model/vrml",
	"wsdl": "application/wsdl+xml",
	"wspolicy": "application/wspolicy+xml",
	"x3d": "model/x3d+xml",
	"x3db": "model/x3d+fastinfoset",
	"x3dbz": "model/x3d+binary",
	"x3dv": "model/x3d-vrml",
	"x3dvz": "model/x3d+vrml",
	"x3dz": "model/x3d+xml",
	"xaml": "application/xaml+xml",
	"xav": "application/xcap-att+xml",
	"xca": "application/xcap-caps+xml",
	"xcs": "application/calendar+xml",
	"xdf": "application/xcap-diff+xml",
	"xdssc": "application/dssc+xml",
	"xel": "application/xcap-el+xml",
	"xenc": "application/xenc+xml",
	"xer": "application/patch-ops-error+xml",
	"xfdf": "application/xfdf",
	"xht": "application/xhtml+xml",
	"xhtml": "application/xhtml+xml",
	"xhvml": "application/xv+xml",
	"xlf": "application/xliff+xml",
	"xm": "audio/xm",
	"xml": "text/xml",
	"xns": "application/xcap-ns+xml",
	"xop": "application/xop+xml",
	"xpl": "application/xproc+xml",
	"xsd": "application/xml",
	"xsf": "application/prs.xsf+xml",
	"xsl": "application/xml",
	"xslt": "application/xml",
	"xspf": "application/xspf+xml",
	"xvm": "application/xv+xml",
	"xvml": "application/xv+xml",
	"yaml": "text/yaml",
	"yang": "application/yang",
	"yin": "application/yin+xml",
	"yml": "text/yaml",
	"zip": "application/zip"
};
function lookup(extn) {
	let tmp = ("" + extn).trim().toLowerCase();
	let idx = tmp.lastIndexOf(".");
	return mimes[!~idx ? tmp : tmp.substring(++idx)];
}

//#endregion
//#region src/ws.ts
const readErrorWarning = `Failed to load \`eslint.config.js\`.
Note that \`@eslint/config-inspector\` only works with the flat config format:
https://eslint.org/docs/latest/use/configure/configuration-files-new`;
async function createWsServer(options) {
	let payload;
	const port = await getPort({
		port: 7811,
		random: true
	});
	const wss = new WebSocketServer({ port });
	const wsClients = /* @__PURE__ */ new Set();
	wss.on("connection", (ws) => {
		wsClients.add(ws);
		console.log(MARK_CHECK, "Websocket client connected");
		ws.on("close", () => wsClients.delete(ws));
	});
	let resolvedConfigPath;
	try {
		resolvedConfigPath = await resolveConfigPath(options);
	} catch (e) {
		if (e instanceof ConfigInspectorError) {
			e.prettyPrint();
			process$1.exit(1);
		} else throw e;
	}
	const { basePath } = resolvedConfigPath;
	const watcher = chokidar.watch([], {
		ignoreInitial: true,
		cwd: basePath
	});
	watcher.on("change", (path) => {
		payload = void 0;
		console.log();
		console.log(MARK_CHECK, "Config change detected", path);
		wsClients.forEach((ws) => {
			ws.send(JSON.stringify({
				type: "config-change",
				path
			}));
		});
	});
	async function getData() {
		try {
			if (!payload) return await readConfig(options).then((res) => {
				const _payload = payload = res.payload;
				_payload.meta.wsPort = port;
				watcher.add(res.dependencies);
				return payload;
			});
			return payload;
		} catch (e) {
			console.error(readErrorWarning);
			if (e instanceof ConfigInspectorError) e.prettyPrint();
			else console.error(e);
			return {
				message: readErrorWarning,
				error: String(e)
			};
		}
	}
	return {
		port,
		wss,
		watcher,
		getData
	};
}

//#endregion
//#region src/server.ts
async function createHostServer(options) {
	const app = createApp();
	const ws = await createWsServer(options);
	const fileMap = /* @__PURE__ */ new Map();
	const readCachedFile = (id) => {
		if (!fileMap.has(id)) fileMap.set(id, readFile(id, "utf-8").catch(() => void 0));
		return fileMap.get(id);
	};
	app.use("/api/payload.json", eventHandler(async (event) => {
		event.node.res.setHeader("Content-Type", "application/json");
		return event.node.res.end(JSON.stringify(await ws.getData()));
	}));
	app.use("/", eventHandler(async (event) => {
		if (await serveStatic(event, {
			fallthrough: true,
			getContents: (id) => readCachedFile(join$2(distDir, id)),
			getMeta: async (id) => {
				const stats = await stat(join$2(distDir, id)).catch(() => {});
				if (!stats || !stats.isFile()) return;
				return {
					type: lookup(id),
					size: stats.size,
					mtime: stats.mtimeMs
				};
			}
		}) === false) return readCachedFile(join$2(distDir, "index.html"));
	}));
	return createServer$1(toNodeListener(app));
}

//#endregion
//#region src/cli.ts
const cli = cac("eslint-config-inspector");
cli.command("build", "Build inspector with current config file for static hosting").option("--config <configFile>", "Config file path").option("--files", "Include matched file paths in payload", { default: true }).option("--basePath <basePath>", "Base directory for globs to resolve. Default to directory of config file if not provided").option("--base <baseURL>", "Base URL for deployment", { default: "/" }).option("--outDir <dir>", "Output directory", { default: ".eslint-config-inspector" }).action(async (options) => {
	console.log(MARK_INFO, "Building static ESLint config inspector...");
	if (process$1.env.ESLINT_CONFIG) options.config ||= process$1.env.ESLINT_CONFIG;
	const cwd = process$1.cwd();
	const outDir = resolve$3(cwd, options.outDir);
	let configs;
	try {
		configs = await readConfig({
			cwd,
			userConfigPath: options.config,
			userBasePath: options.basePath,
			globMatchedFiles: options.files
		});
	} catch (error) {
		if (error instanceof ConfigInspectorError) {
			error.prettyPrint();
			process$1.exit(1);
		}
		throw error;
	}
	let baseURL = options.base;
	if (!baseURL.endsWith("/")) baseURL += "/";
	if (!baseURL.startsWith("/")) baseURL = `/${baseURL}`;
	baseURL = baseURL.replace(/\/+/g, "/");
	if (existsSync(outDir)) await fs$1.rm(outDir, { recursive: true });
	await fs$1.mkdir(outDir, { recursive: true });
	await fs$1.cp(distDir, outDir, { recursive: true });
	const htmlFiles = await glob("**/*.html", {
		cwd: distDir,
		onlyFiles: true,
		expandDirectories: false
	});
	if (baseURL !== "/") for (const file of htmlFiles) {
		const newContent = (await fs$1.readFile(resolve$3(distDir, file), "utf-8")).replaceAll(/\s(href|src)="\//g, ` $1="${baseURL}`).replaceAll("baseURL:\"/\"", `baseURL:"${baseURL}"`);
		await fs$1.writeFile(resolve$3(outDir, file), newContent, "utf-8");
	}
	await fs$1.mkdir(resolve$3(outDir, "api"), { recursive: true });
	configs.payload.meta.configPath = "";
	configs.payload.meta.basePath = "";
	await fs$1.writeFile(resolve$3(outDir, "api/payload.json"), JSON.stringify(configs.payload, null, 2), "utf-8");
	console.log(MARK_CHECK, `Built to ${relative$2(cwd, outDir)}`);
	console.log(MARK_INFO, `You can use static server like \`npx serve ${relative$2(cwd, outDir)}\` to serve the inspector`);
});
cli.command("", "Start dev inspector").option("--config <configFile>", "Config file path").option("--files", "Include matched file paths in payload", { default: true }).option("--basePath <basePath>", "Base directory for globs to resolve. Default to directory of config file if not provided").option("--host <host>", "Host", { default: process$1.env.HOST || "127.0.0.1" }).option("--port <port>", "Port", { default: process$1.env.PORT || 7777 }).option("--open", "Open browser", { default: true }).action(async (options) => {
	const host = options.host;
	const port = await getPort({
		port: options.port,
		portRange: [7777, 9e3],
		host
	});
	if (process$1.env.ESLINT_CONFIG) options.config ||= process$1.env.ESLINT_CONFIG;
	console.log(MARK_INFO, `Starting ESLint config inspector at`, c.green`http://${host === "127.0.0.1" ? "localhost" : host}:${port}`, "\n");
	(await createHostServer({
		cwd: process$1.cwd(),
		userConfigPath: options.config,
		userBasePath: options.basePath,
		globMatchedFiles: options.files
	})).listen(port, host, async () => {
		if (options.open) await open(`http://${host === "127.0.0.1" ? "localhost" : host}:${port}`);
	});
});
cli.help();
cli.parse();

//#endregion
export {  };
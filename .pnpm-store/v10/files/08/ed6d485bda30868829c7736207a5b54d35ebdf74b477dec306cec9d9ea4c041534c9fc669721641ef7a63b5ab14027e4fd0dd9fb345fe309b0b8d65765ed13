import { t as overrideEnv } from "./env-BRiVSJMz.mjs";
import { n as stopCpuProfile, t as startCpuProfile } from "./profile-q-JV7Qxl.mjs";
import { i as withNodePath, t as loadKit } from "./kit-DUlGqV3Z.mjs";
import { r as showVersionsFromConfig } from "./banner-C2vxTb-6.mjs";
import { t as clearBuildDir } from "./fs-B8DrLsZ2.mjs";
import { a as writeNuxtManifest, i as resolveNuxtManifest, n as loadNuxtManifest } from "./nuxt-CsZm8Jhw.mjs";
import process from "node:process";
import { provider } from "std-env";
import { join, resolve } from "pathe";
import { pathToFileURL } from "node:url";
import defu, { defu as defu$1 } from "defu";
import { existsSync, readdirSync, statSync, watch } from "node:fs";
import EventEmitter from "node:events";
import { mkdir } from "node:fs/promises";
import { resolveModulePath } from "exsolve";
import { joinURL } from "ufo";
import { listen } from "listhen";
import { debounce } from "perfect-debounce";
import { toNodeHandler } from "srvx/node";
import { Youch } from "youch";

//#region ../../node_modules/.pnpm/h3@1.15.6/node_modules/h3/dist/index.mjs
function hasProp(obj, prop) {
	try {
		return prop in obj;
	} catch {
		return false;
	}
}
var H3Error = class extends Error {
	static __h3_error__ = true;
	statusCode = 500;
	fatal = false;
	unhandled = false;
	statusMessage;
	data;
	cause;
	constructor(message, opts = {}) {
		super(message, opts);
		if (opts.cause && !this.cause) this.cause = opts.cause;
	}
	toJSON() {
		const obj = {
			message: this.message,
			statusCode: sanitizeStatusCode(this.statusCode, 500)
		};
		if (this.statusMessage) obj.statusMessage = sanitizeStatusMessage(this.statusMessage);
		if (this.data !== void 0) obj.data = this.data;
		return obj;
	}
};
function createError(input) {
	if (typeof input === "string") return new H3Error(input);
	if (isError(input)) return input;
	const err = new H3Error(input.message ?? input.statusMessage ?? "", { cause: input.cause || input });
	if (hasProp(input, "stack")) try {
		Object.defineProperty(err, "stack", { get() {
			return input.stack;
		} });
	} catch {
		try {
			err.stack = input.stack;
		} catch {}
	}
	if (input.data) err.data = input.data;
	if (input.statusCode) err.statusCode = sanitizeStatusCode(input.statusCode, err.statusCode);
	else if (input.status) err.statusCode = sanitizeStatusCode(input.status, err.statusCode);
	if (input.statusMessage) err.statusMessage = input.statusMessage;
	else if (input.statusText) err.statusMessage = input.statusText;
	if (err.statusMessage) {
		const originalMessage = err.statusMessage;
		if (sanitizeStatusMessage(err.statusMessage) !== originalMessage) console.warn("[h3] Please prefer using `message` for longer error messages instead of `statusMessage`. In the future, `statusMessage` will be sanitized by default.");
	}
	if (input.fatal !== void 0) err.fatal = input.fatal;
	if (input.unhandled !== void 0) err.unhandled = input.unhandled;
	return err;
}
function sendError(event, error, debug) {
	if (event.handled) return;
	const h3Error = isError(error) ? error : createError(error);
	const responseBody = {
		statusCode: h3Error.statusCode,
		statusMessage: h3Error.statusMessage,
		stack: [],
		data: h3Error.data
	};
	if (debug) responseBody.stack = (h3Error.stack || "").split("\n").map((l) => l.trim());
	if (event.handled) return;
	setResponseStatus(event, Number.parseInt(h3Error.statusCode), h3Error.statusMessage);
	event.node.res.setHeader("content-type", MIMES.json);
	event.node.res.end(JSON.stringify(responseBody, void 0, 2));
}
function isError(input) {
	return input?.constructor?.__h3_error__ === true;
}
const RawBodySymbol = Symbol.for("h3RawBody");
const ParsedBodySymbol = Symbol.for("h3ParsedBody");
const MIMES = {
	html: "text/html",
	json: "application/json"
};
const DISALLOWED_STATUS_CHARS = /[^\u0009\u0020-\u007E]/g;
function sanitizeStatusMessage(statusMessage = "") {
	return statusMessage.replace(DISALLOWED_STATUS_CHARS, "");
}
function sanitizeStatusCode(statusCode, defaultStatusCode = 200) {
	if (!statusCode) return defaultStatusCode;
	if (typeof statusCode === "string") statusCode = Number.parseInt(statusCode, 10);
	if (statusCode < 100 || statusCode > 999) return defaultStatusCode;
	return statusCode;
}
function splitCookiesString(cookiesString) {
	if (Array.isArray(cookiesString)) return cookiesString.flatMap((c) => splitCookiesString(c));
	if (typeof cookiesString !== "string") return [];
	const cookiesStrings = [];
	let pos = 0;
	let start;
	let ch;
	let lastComma;
	let nextStart;
	let cookiesSeparatorFound;
	const skipWhitespace = () => {
		while (pos < cookiesString.length && /\s/.test(cookiesString.charAt(pos))) pos += 1;
		return pos < cookiesString.length;
	};
	const notSpecialChar = () => {
		ch = cookiesString.charAt(pos);
		return ch !== "=" && ch !== ";" && ch !== ",";
	};
	while (pos < cookiesString.length) {
		start = pos;
		cookiesSeparatorFound = false;
		while (skipWhitespace()) {
			ch = cookiesString.charAt(pos);
			if (ch === ",") {
				lastComma = pos;
				pos += 1;
				skipWhitespace();
				nextStart = pos;
				while (pos < cookiesString.length && notSpecialChar()) pos += 1;
				if (pos < cookiesString.length && cookiesString.charAt(pos) === "=") {
					cookiesSeparatorFound = true;
					pos = nextStart;
					cookiesStrings.push(cookiesString.slice(start, lastComma));
					start = pos;
				} else pos = lastComma + 1;
			} else pos += 1;
		}
		if (!cookiesSeparatorFound || pos >= cookiesString.length) cookiesStrings.push(cookiesString.slice(start));
	}
	return cookiesStrings;
}
function setResponseStatus(event, code, text) {
	if (code) event.node.res.statusCode = sanitizeStatusCode(code, event.node.res.statusCode);
	if (text) event.node.res.statusMessage = sanitizeStatusMessage(text);
}
function sendStream(event, stream) {
	if (!stream || typeof stream !== "object") throw new Error("[h3] Invalid stream provided.");
	event.node.res._data = stream;
	if (!event.node.res.socket) {
		event._handled = true;
		return Promise.resolve();
	}
	if (hasProp(stream, "pipeTo") && typeof stream.pipeTo === "function") return stream.pipeTo(new WritableStream({ write(chunk) {
		event.node.res.write(chunk);
	} })).then(() => {
		event.node.res.end();
	});
	if (hasProp(stream, "pipe") && typeof stream.pipe === "function") return new Promise((resolve, reject) => {
		stream.pipe(event.node.res);
		if (stream.on) {
			stream.on("end", () => {
				event.node.res.end();
				resolve();
			});
			stream.on("error", (error) => {
				reject(error);
			});
		}
		event.node.res.on("close", () => {
			if (stream.abort) stream.abort();
		});
	});
	throw new Error("[h3] Invalid or incompatible stream provided.");
}
function sendWebResponse(event, response) {
	for (const [key, value] of response.headers) if (key === "set-cookie") event.node.res.appendHeader(key, splitCookiesString(value));
	else event.node.res.setHeader(key, value);
	if (response.status) event.node.res.statusCode = sanitizeStatusCode(response.status, event.node.res.statusCode);
	if (response.statusText) event.node.res.statusMessage = sanitizeStatusMessage(response.statusText);
	if (response.redirected) event.node.res.setHeader("location", response.url);
	if (!response.body) {
		event.node.res.end();
		return;
	}
	return sendStream(event, response.body);
}
var H3Event = class {
	"__is_event__" = true;
	node;
	web;
	context = {};
	_method;
	_path;
	_headers;
	_requestBody;
	_handled = false;
	_onBeforeResponseCalled;
	_onAfterResponseCalled;
	constructor(req, res) {
		this.node = {
			req,
			res
		};
	}
	get method() {
		if (!this._method) this._method = (this.node.req.method || "GET").toUpperCase();
		return this._method;
	}
	get path() {
		return this._path || this.node.req.url || "/";
	}
	get headers() {
		if (!this._headers) this._headers = _normalizeNodeHeaders(this.node.req.headers);
		return this._headers;
	}
	get handled() {
		return this._handled || this.node.res.writableEnded || this.node.res.headersSent;
	}
	respondWith(response) {
		return Promise.resolve(response).then((_response) => sendWebResponse(this, _response));
	}
	toString() {
		return `[${this.method}] ${this.path}`;
	}
	toJSON() {
		return this.toString();
	}
	/** @deprecated Please use `event.node.req` instead. */
	get req() {
		return this.node.req;
	}
	/** @deprecated Please use `event.node.res` instead. */
	get res() {
		return this.node.res;
	}
};
function createEvent(req, res) {
	return new H3Event(req, res);
}
function _normalizeNodeHeaders(nodeHeaders) {
	const headers = new Headers();
	for (const [name, value] of Object.entries(nodeHeaders)) if (Array.isArray(value)) for (const item of value) headers.append(name, item);
	else if (value) headers.set(name, value);
	return headers;
}
const H3Headers = globalThis.Headers;
const H3Response = globalThis.Response;
function toNodeListener(app) {
	const toNodeHandle = async function(req, res) {
		const event = createEvent(req, res);
		try {
			await app.handler(event);
		} catch (_error) {
			const error = createError(_error);
			if (!isError(_error)) error.unhandled = true;
			setResponseStatus(event, error.statusCode, error.statusMessage);
			if (app.options.onError) await app.options.onError(error, event);
			if (event.handled) return;
			if (error.unhandled || error.fatal) console.error("[h3]", error.fatal ? "[fatal]" : "[unhandled]", error);
			if (app.options.onBeforeResponse && !event._onBeforeResponseCalled) await app.options.onBeforeResponse(event, { body: error });
			await sendError(event, error, !!app.options.debug);
			if (app.options.onAfterResponse && !event._onAfterResponseCalled) await app.options.onAfterResponse(event, { body: error });
		}
	};
	return toNodeHandle;
}

//#endregion
//#region ../nuxi/src/dev/error.ts
async function renderError(req, res, error) {
	if (res.headersSent) {
		if (!res.writableEnded) res.end();
		return;
	}
	const youch = new Youch();
	res.statusCode = 500;
	res.setHeader("Content-Type", "text/html");
	res.setHeader("Cache-Control", "no-store");
	res.setHeader("Refresh", "3");
	const html = await youch.toHTML(error, { request: {
		url: req.url,
		method: req.method,
		headers: req.headers
	} });
	res.end(html);
}

//#endregion
//#region ../nuxi/src/dev/utils.ts
const RESTART_RE = /^(?:nuxt\.config\.[a-z0-9]+|\.nuxtignore|\.nuxtrc|\.config\/nuxt(?:\.config)?\.[a-z0-9]+)$/;
var FileChangeTracker = class {
	mtimes = /* @__PURE__ */ new Map();
	shouldEmitChange(filePath) {
		const resolved = resolve(filePath);
		try {
			const currentMtime = statSync(resolved).mtimeMs;
			const lastMtime = this.mtimes.get(resolved);
			this.mtimes.set(resolved, currentMtime);
			return lastMtime === void 0 || currentMtime !== lastMtime;
		} catch {
			this.mtimes.delete(resolved);
			return true;
		}
	}
	prime(filePath, recursive = false) {
		const resolved = resolve(filePath);
		const stat = statSync(resolved);
		this.mtimes.set(resolved, stat.mtimeMs);
		if (stat.isDirectory()) {
			const entries = readdirSync(resolved);
			for (const entry of entries) {
				const fullPath = resolve(resolved, entry);
				try {
					const stats = statSync(fullPath);
					this.mtimes.set(fullPath, stats.mtimeMs);
					if (recursive && stats.isDirectory()) this.prime(fullPath, recursive);
				} catch {}
			}
		}
	}
};
var NuxtDevServer = class extends EventEmitter {
	#handler;
	#distWatcher;
	#configWatcher;
	#currentNuxt;
	#loadingMessage;
	#loadingError;
	#fileChangeTracker = new FileChangeTracker();
	#cwd;
	#websocketConnections = /* @__PURE__ */ new Set();
	loadDebounced;
	handler;
	listener;
	constructor(options) {
		super();
		this.options = options;
		this.loadDebounced = debounce(this.load);
		let _initResolve;
		const _initPromise = new Promise((resolve) => {
			_initResolve = resolve;
		});
		this.once("ready", () => {
			_initResolve();
		});
		this.#cwd = options.cwd;
		this.handler = async (req, res) => {
			if (this.#loadingError) {
				renderError(req, res, this.#loadingError);
				return;
			}
			await _initPromise;
			if (this.#handler) this.#handler(req, res);
			else this.#renderLoadingScreen(req, res);
		};
	}
	async #renderLoadingScreen(req, res) {
		if (res.headersSent) {
			if (!res.writableEnded) res.end();
			return;
		}
		res.statusCode = 503;
		res.setHeader("Content-Type", "text/html");
		const loadingTemplate = this.options.loadingTemplate || this.#currentNuxt?.options.devServer.loadingTemplate || await resolveLoadingTemplate(this.#cwd);
		res.end(loadingTemplate({ loading: this.#loadingMessage || "Loading..." }));
	}
	async init() {
		this.#loadingMessage = `Starting Nuxt...`;
		this.#handler = void 0;
		this.emit("loading", this.#loadingMessage);
		await this.#loadNuxtInstance();
		if (this.options.showBanner) showVersionsFromConfig(this.options.cwd, this.#currentNuxt.options);
		await this.#createListener();
		await this.#initializeNuxt(false);
		this.#watchConfig();
	}
	closeWatchers() {
		this.#distWatcher?.close();
		this.#configWatcher?.();
	}
	async load(reload, reason) {
		try {
			this.closeWatchers();
			await this.#load(reload, reason);
			this.#loadingError = void 0;
		} catch (error) {
			console.error(`Cannot ${reload ? "restart" : "start"} nuxt: `, error);
			this.#handler = void 0;
			this.#loadingError = error;
			this.#loadingMessage = "Error while loading Nuxt. Please check console and fix errors.";
			this.emit("loading:error", error);
		}
		this.#watchConfig();
	}
	async #loadNuxtInstance(urls) {
		const kit = await loadKit(this.options.cwd);
		const loadOptions = {
			cwd: this.options.cwd,
			dev: true,
			ready: false,
			envName: this.options.envName,
			dotenv: {
				cwd: this.options.cwd,
				fileName: this.options.dotenv.fileName
			},
			overrides: {
				logLevel: this.options.logLevel,
				...this.options.overrides,
				vite: {
					clearScreen: this.options.clear,
					...this.options.overrides.vite
				}
			}
		};
		if (urls) {
			const overrides = this.options.listenOverrides || {};
			const hostname = overrides.hostname;
			const https = overrides.https;
			loadOptions.defaults = resolveDevServerDefaults({
				hostname,
				https
			}, urls);
		}
		this.#currentNuxt = await kit.loadNuxt(loadOptions);
	}
	async #createListener() {
		if (!this.#currentNuxt) throw new Error("Nuxt must be loaded before creating listener");
		const listenOptions = this.#resolveListenOptions();
		this.listener = await listen(this.handler, listenOptions);
		if (listenOptions.public) {
			this.#currentNuxt.options.devServer.cors = { origin: "*" };
			if (this.#currentNuxt.options.vite?.server) this.#currentNuxt.options.vite.server.allowedHosts = true;
			return;
		}
		const urls = await this.listener.getURLs().then((r) => r.map((r) => r.url));
		if (urls && urls.length > 0) this.#currentNuxt.options.vite = defu(this.#currentNuxt.options.vite, { server: { allowedHosts: urls.map((u) => new URL(u).hostname) } });
	}
	#resolveListenOptions() {
		if (!this.#currentNuxt) throw new Error("Nuxt must be loaded before resolving listen options");
		const nuxtConfig = this.#currentNuxt.options;
		const overrides = this.options.listenOverrides || {};
		const port = overrides.port ?? nuxtConfig.devServer?.port;
		const hostname = overrides.hostname ?? nuxtConfig.devServer?.host;
		const isPublic = provider === "codesandbox" || (overrides.public ?? (isPublicHostname(hostname) ? true : void 0));
		const httpsFromConfig = typeof nuxtConfig.devServer?.https !== "boolean" && nuxtConfig.devServer?.https ? nuxtConfig.devServer.https : {};
		overrides._https ??= !!nuxtConfig.devServer?.https;
		const httpsOptions = overrides.https && defu(typeof overrides.https === "object" ? overrides.https : {}, httpsFromConfig);
		const baseURL = nuxtConfig.app?.baseURL?.startsWith?.("./") ? nuxtConfig.app.baseURL.slice(1) : nuxtConfig.app?.baseURL;
		return {
			...overrides,
			port,
			hostname,
			public: isPublic,
			https: httpsOptions || void 0,
			baseURL
		};
	}
	async #initializeNuxt(reload) {
		if (!this.#currentNuxt) throw new Error("Nuxt must be loaded before configuration");
		if (!process.env.NUXI_DISABLE_VITE_HMR) this.#currentNuxt.hooks.hook("vite:extend", ({ config }) => {
			if (config.server) config.server.hmr = {
				protocol: void 0,
				...config.server.hmr,
				port: void 0,
				host: void 0,
				server: this.listener.server
			};
		});
		this.#currentNuxt.hooks.hookOnce("close", () => {
			this.#closeWebSocketConnections();
			this.listener.server.removeAllListeners("upgrade");
		});
		if (!reload) {
			const previousManifest = await loadNuxtManifest(this.#currentNuxt.options.buildDir);
			const newManifest = resolveNuxtManifest(this.#currentNuxt);
			const promise = writeNuxtManifest(this.#currentNuxt, newManifest);
			this.#currentNuxt.hooks.hookOnce("ready", async () => {
				await promise;
			});
			if (previousManifest && newManifest && previousManifest._hash !== newManifest._hash) await clearBuildDir(this.#currentNuxt.options.buildDir);
		}
		await this.#currentNuxt.ready();
		const unsub = this.#currentNuxt.hooks.hook("restart", async (options) => {
			unsub();
			if (options?.hard) {
				this.emit("restart");
				return;
			}
			await this.load(true);
		});
		if (this.#currentNuxt.server && "upgrade" in this.#currentNuxt.server) this.listener.server.on("upgrade", (req, socket, head) => {
			const nuxt = this.#currentNuxt;
			if (!nuxt || !nuxt.server) return;
			const viteHmrPath = joinURL(nuxt.options.app.baseURL.startsWith("./") ? nuxt.options.app.baseURL.slice(1) : nuxt.options.app.baseURL, nuxt.options.app.buildAssetsDir);
			if (req.url?.startsWith(viteHmrPath)) return;
			nuxt.server.upgrade(req, socket, head);
			this.#websocketConnections.add(socket);
			socket.on("close", () => {
				this.#websocketConnections.delete(socket);
			});
		});
		await this.#currentNuxt.hooks.callHook("listen", this.listener.server, this.listener);
		const addr = this.listener.address;
		this.#currentNuxt.options.devServer.host = addr.address;
		this.#currentNuxt.options.devServer.port = addr.port;
		this.#currentNuxt.options.devServer.url = getAddressURL(addr, !!this.listener.https);
		this.#currentNuxt.options.devServer.https = this.listener.https;
		if (this.listener.https && !process.env.NODE_TLS_REJECT_UNAUTHORIZED) console.warn("You might need `NODE_TLS_REJECT_UNAUTHORIZED=0` environment variable to make https work.");
		const kit = await loadKit(this.options.cwd);
		const typesPromise = existsSync(join(this.#currentNuxt.options.buildDir, "tsconfig.json")) ? kit.writeTypes(this.#currentNuxt).catch(console.error) : await kit.writeTypes(this.#currentNuxt).catch(console.error);
		await Promise.all([typesPromise, kit.buildNuxt(this.#currentNuxt)]);
		if (!this.#currentNuxt.server) throw new Error("Nitro server has not been initialized.");
		const distDir = join(this.#currentNuxt.options.buildDir, "dist");
		await mkdir(distDir, { recursive: true });
		this.#fileChangeTracker.prime(distDir);
		this.#distWatcher = watch(distDir);
		this.#distWatcher.on("change", (_event, file) => {
			if (!this.#fileChangeTracker.shouldEmitChange(resolve(distDir, file || ""))) return;
			this.loadDebounced(true, ".nuxt/dist directory has been removed");
		});
		if ("fetch" in this.#currentNuxt.server) this.#handler = toNodeHandler(this.#currentNuxt.server.fetch);
		else this.#handler = toNodeListener(this.#currentNuxt.server.app);
		const proto = this.listener.https ? "https" : "http";
		this.emit("ready", `${proto}://127.0.0.1:${addr.port}`);
	}
	async close() {
		if (this.#currentNuxt) await this.#currentNuxt.close();
	}
	#closeWebSocketConnections() {
		for (const socket of this.#websocketConnections) socket.destroy();
		this.#websocketConnections.clear();
	}
	async #load(reload, reason) {
		const action = reload ? "Restarting" : "Starting";
		this.#loadingMessage = `${reason ? `${reason}. ` : ""}${action} Nuxt...`;
		this.#handler = void 0;
		this.emit("loading", this.#loadingMessage);
		if (reload) console.info(this.#loadingMessage);
		await this.close();
		const urls = await this.listener.getURLs().then((r) => r.map((r) => r.url));
		await this.#loadNuxtInstance(urls);
		await this.#initializeNuxt(!!reload);
	}
	#watchConfig() {
		this.#configWatcher = createConfigWatcher(this.#cwd, this.options.dotenv.fileName, () => this.emit("restart"), (file) => this.loadDebounced(true, `${file} updated`));
	}
};
function getAddressURL(addr, https) {
	const proto = https ? "https" : "http";
	let host = addr.address.includes(":") ? `[${addr.address}]` : addr.address;
	if (host === "[::]") host = "localhost";
	const port = addr.port || 3e3;
	return `${proto}://${host}:${port}/`;
}
function resolveDevServerDefaults(listenOptions, urls = []) {
	const defaultConfig = {};
	if (urls && urls.length > 0) defaultConfig.vite = { server: { allowedHosts: urls.map((u) => new URL(u).hostname) } };
	if (listenOptions.hostname) {
		defaultConfig.devServer = { cors: { origin: [`${listenOptions.https ? "https" : "http"}://${listenOptions.hostname}`, ...urls] } };
		defaultConfig.vite = defu(defaultConfig.vite, { server: { allowedHosts: [listenOptions.hostname] } });
	}
	return defaultConfig;
}
function createConfigWatcher(cwd, dotenvFileName = ".env", onRestart, onReload) {
	const fileWatcher = new FileChangeTracker();
	fileWatcher.prime(cwd);
	const configWatcher = watch(cwd);
	let configDirWatcher = existsSync(join(cwd, ".config")) ? createConfigDirWatcher(cwd, onReload) : void 0;
	const dotenvFileNames = new Set(Array.isArray(dotenvFileName) ? dotenvFileName : [dotenvFileName]);
	configWatcher.on("change", (_event, file) => {
		if (!fileWatcher.shouldEmitChange(resolve(cwd, file))) return;
		if (dotenvFileNames.has(file)) onRestart();
		if (RESTART_RE.test(file)) onReload(file);
		if (file === ".config") configDirWatcher ||= createConfigDirWatcher(cwd, onReload);
	});
	return () => {
		configWatcher.close();
		configDirWatcher?.();
	};
}
function createConfigDirWatcher(cwd, onReload) {
	const configDir = join(cwd, ".config");
	const fileWatcher = new FileChangeTracker();
	fileWatcher.prime(configDir);
	const configDirWatcher = watch(configDir);
	configDirWatcher.on("change", (_event, file) => {
		if (!fileWatcher.shouldEmitChange(resolve(configDir, file))) return;
		if (RESTART_RE.test(file)) onReload(file);
	});
	return () => configDirWatcher.close();
}
async function resolveLoadingTemplate(cwd) {
	return (await import(pathToFileURL(resolveModulePath("@nuxt/ui-templates", { from: withNodePath(resolveModulePath("nuxt", {
		from: withNodePath(cwd),
		try: true
	}) || cwd) })).href)).loading || ((params) => `<h2>${params.loading}</h2>`);
}
function isPublicHostname(hostname) {
	return !!hostname && ![
		"localhost",
		"127.0.0.1",
		"::1"
	].includes(hostname);
}

//#endregion
//#region ../nuxi/src/dev/index.ts
const start = Date.now();
var IPC = class {
	enabled = !!process.send && !process.title?.includes("vitest") && process.env.__NUXT__FORK;
	constructor() {
		if (this.enabled) process.once("unhandledRejection", (reason) => {
			this.send({
				type: "nuxt:internal:dev:rejection",
				message: reason instanceof Error ? reason.toString() : "Unhandled Rejection"
			});
			process.exit();
		});
		process.on("message", (message) => {
			if (message.type === "nuxt:internal:dev:context") initialize(message.context, { listenOverrides: message.listenOverrides });
		});
		this.send({ type: "nuxt:internal:dev:fork-ready" });
	}
	send(message) {
		if (this.enabled) process.send?.(message);
	}
};
const ipc = new IPC();
async function initialize(devContext, ctx = {}) {
	overrideEnv("development");
	const profileArg = devContext.args.profile;
	const perfValue = profileArg === "verbose" ? true : profileArg ? "quiet" : void 0;
	const perfOverrides = perfValue ? { debug: { perf: perfValue } } : {};
	if (profileArg) await startCpuProfile();
	const devServer = new NuxtDevServer({
		cwd: devContext.cwd,
		overrides: defu(ctx.data?.overrides, { extends: devContext.args.extends }, perfOverrides),
		logLevel: devContext.args.logLevel,
		clear: devContext.args.clear,
		dotenv: {
			cwd: devContext.cwd,
			fileName: devContext.args.dotenv
		},
		envName: devContext.args.envName,
		showBanner: ctx.showBanner !== false && !ipc.enabled,
		listenOverrides: ctx.listenOverrides
	});
	let address;
	if (ipc.enabled) {
		devServer.on("loading:error", (_error) => {
			ipc.send({
				type: "nuxt:internal:dev:loading:error",
				error: {
					message: _error.message,
					stack: _error.stack,
					name: _error.name,
					code: "code" in _error ? _error.code : void 0
				}
			});
		});
		devServer.on("loading", (message) => {
			ipc.send({
				type: "nuxt:internal:dev:loading",
				message
			});
		});
		devServer.on("restart", () => {
			ipc.send({ type: "nuxt:internal:dev:restart" });
		});
		devServer.on("ready", (payload) => {
			ipc.send({
				type: "nuxt:internal:dev:ready",
				address: payload
			});
		});
	} else devServer.on("ready", (payload) => {
		address = payload;
	});
	await devServer.init();
	if (process.env.DEBUG) console.debug(`Dev server (internal) initialized in ${Date.now() - start}ms`);
	if (profileArg) for (const signal of [
		"exit",
		"SIGTERM",
		"SIGINT",
		"SIGQUIT"
	]) process.once(signal, () => stopCpuProfile(devContext.cwd, "dev"));
	return {
		listener: devServer.listener,
		close: async () => {
			devServer.closeWatchers();
			await Promise.all([devServer.listener.close(), devServer.close()]);
		},
		onReady: (callback) => {
			if (address) callback(address);
			else devServer.once("ready", (payload) => callback(payload));
		},
		onRestart: (callback) => {
			let restarted = false;
			function restart() {
				if (!restarted) {
					restarted = true;
					callback(devServer);
				}
			}
			devServer.once("restart", restart);
			process.once("uncaughtException", restart);
			process.once("unhandledRejection", restart);
		}
	};
}

//#endregion
export { initialize as t };
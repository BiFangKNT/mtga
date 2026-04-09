import { o as __toESM } from "./_chunks/rolldown-runtime.mjs";
import { isBuiltin } from "node:module";
import fs, { existsSync, readFileSync } from "node:fs";
import { performance } from "node:perf_hooks";
import * as vite from "vite";
import { createBuilder, createLogger, createServer, isCSSRequest, mergeConfig, transformWithEsbuild } from "vite";
import { basename, dirname, isAbsolute, join, normalize, relative, resolve } from "pathe";
import { createIsIgnored, directoryToURL, getLayerDirectories, logger, resolveAlias, resolvePath, tryUseNuxt, useNitro, useNuxt } from "@nuxt/kit";
import { findStaticImports, parseNodeModulePath, sanitizeFilePath } from "mlly";
import viteJsxPlugin from "@vitejs/plugin-vue-jsx";
import vuePlugin from "@vitejs/plugin-vue";
import { getQuery, joinURL, withLeadingSlash, withTrailingSlash, withoutBase, withoutLeadingSlash } from "ufo";
import { filename } from "pathe/utils";
import { resolveModulePath } from "exsolve";
import MagicString from "magic-string";
import process from "node:process";
import { mkdir, readFile, rm, unlink, writeFile } from "node:fs/promises";
import net from "node:net";
import os from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";
import { Buffer } from "node:buffer";
import { ViteNodeServer } from "vite-node/server";
import { normalizeViteManifest, precomputeDependencies } from "vue-bundle-renderer";
import { hasTTY, isCI, provider } from "std-env";
import { colorize, stripAnsi } from "consola/utils";
import escapeStringRegexp from "escape-string-regexp";
import { defu } from "defu";
import { addDependency } from "nypm";
import { getPort } from "get-port-please";
import { readTSConfig, resolveTSConfig } from "pkg-types";
import { serialize } from "seroval";
import { createJiti } from "jiti";
import { genArrayFromRaw, genImport, genObjectFromRawEntries } from "knitwork";
import replacePlugin from "@rollup/plugin-replace";
import { defineEnv } from "unenv";
//#region ../nuxt/src/core/utils/plugins.ts
/**
* Split a bundler module ID into its pathname and search (query) parts.
*
* Module IDs from Vite/webpack are already-normalized filesystem paths
* that may carry query strings (e.g. `?vue&type=style&lang=css`).
*/
function parseModuleId(id) {
	const qIndex = id.indexOf("?");
	if (qIndex === -1) return {
		pathname: id,
		search: ""
	};
	return {
		pathname: id.slice(0, qIndex),
		search: id.slice(qIndex)
	};
}
const NUXT_COMPONENT_RE = /[?&]nuxt_component=/;
const MACRO_RE = /[?&]macro=/;
const VUE_QUERY_RE = /[?&]vue(?:&|$)/;
const SETUP_QUERY_RE = /[?&]setup(?:=|&|$)/;
const TYPE_QUERY_RE = /[?&]type=([^&]*)/;
function isVue(id, opts = {}) {
	const { search } = parseModuleId(id);
	if (id.endsWith(".vue") && !search) return true;
	if (!search) return false;
	if (NUXT_COMPONENT_RE.test(search)) return false;
	if (MACRO_RE.test(search) && (search === "?macro=true" || !opts.type || opts.type.includes("script"))) return true;
	if (!VUE_QUERY_RE.test(search)) return false;
	if (opts.type) {
		const type = SETUP_QUERY_RE.test(search) ? "script" : TYPE_QUERY_RE.exec(search)?.[1];
		if (!type || !opts.type.includes(type)) return false;
	}
	return true;
}
//#endregion
//#region src/utils/index.ts
const IS_CSS_RE = /\.(?:css|scss|sass|postcss|pcss|less|stylus|styl)(?:\?[^.]+)?$/;
function isCSS(file) {
	return IS_CSS_RE.test(file);
}
/** @since 3.9.0 */
function toArray(value) {
	return Array.isArray(value) ? value : [value];
}
//#endregion
//#region src/plugins/dev-style-ssr.ts
function DevStyleSSRPlugin(options) {
	return {
		name: "nuxt:dev-style-ssr",
		apply: "serve",
		enforce: "post",
		applyToEnvironment: (environment) => environment.name === "client",
		transform(code, id) {
			if (!isCSS(id) || !code.includes("import.meta.hot")) return;
			let moduleId = id;
			if (moduleId.startsWith(options.srcDir)) moduleId = moduleId.slice(options.srcDir.length);
			return code + [joinURL(options.buildAssetsURL, moduleId), joinURL(options.buildAssetsURL, "@fs", moduleId)].map((selector) => `\ndocument.querySelectorAll(\`link[href="${selector}"]\`).forEach(i=>i.remove())`).join("");
		}
	};
}
//#endregion
//#region src/plugins/runtime-paths.ts
const VITE_ASSET_RE = /__VITE_ASSET__|__VITE_PUBLIC_ASSET__/;
const STYLE_QUERY_RE$1 = /[?&]type=style/;
function RuntimePathsPlugin() {
	let sourcemap;
	return {
		name: "nuxt:runtime-paths-dep",
		enforce: "post",
		applyToEnvironment: (environment) => environment.name === "client",
		configResolved(config) {
			sourcemap = !!config.build.sourcemap;
		},
		transform(code, id) {
			const { pathname, search } = parseModuleId(id);
			if (isCSS(pathname)) return;
			if (pathname.endsWith(".vue")) {
				if (STYLE_QUERY_RE$1.test(search)) return;
			}
			if (VITE_ASSET_RE.test(code)) {
				const s = new MagicString(code);
				s.prepend("import \"#internal/nuxt/paths\";");
				return {
					code: s.toString(),
					map: sourcemap ? s.generateMap({ hires: true }) : void 0
				};
			}
		}
	};
}
//#endregion
//#region src/utils/config.ts
function resolveClientEntry(config) {
	const input = config.environments.client?.build.rollupOptions.input ?? config.build.rollupOptions.input;
	if (input) {
		if (typeof input === "string") return input;
		if (!Array.isArray(input) && input.entry) return input.entry;
	}
	throw new Error("No entry found in rollupOptions.input");
}
function resolveServerEntry(config) {
	const input = config.environments.ssr?.build.rollupOptions.input ?? config.build.rollupOptions.input;
	if (input) {
		if (typeof input === "string") return input;
		if (!Array.isArray(input) && input.server) return input.server;
	}
	throw new Error("No entry found in rollupOptions.input");
}
//#endregion
//#region src/plugins/type-check.ts
const QUERY_RE$2 = /\?.+$/;
function TypeCheckPlugin(nuxt) {
	let entry;
	let sourcemap;
	return {
		name: "nuxt:type-check",
		applyToEnvironment: (environment) => environment.name === "client" && !environment.config.isProduction,
		apply: () => {
			return !nuxt.options.test && nuxt.options.typescript.typeCheck === true;
		},
		configResolved(config) {
			try {
				entry = resolveClientEntry(config);
				sourcemap = !!config.build.sourcemap;
			} catch {
				console.debug("[nuxt:type-check] Could not resolve client entry, type checking will not be applied.");
			}
		},
		transform(code, id) {
			if (id.replace(QUERY_RE$2, "") !== entry) return;
			const s = new MagicString(code);
			s.prepend("import \"/@vite-plugin-checker-runtime-entry\";\n");
			return {
				code: s.toString(),
				map: sourcemap ? s.generateMap({ hires: true }) : void 0
			};
		}
	};
}
//#endregion
//#region src/plugins/module-preload-polyfill.ts
const QUERY_RE$1 = /\?.+$/;
function ModulePreloadPolyfillPlugin() {
	let isDisabled = false;
	let entry;
	let sourcemap;
	return {
		name: "nuxt:module-preload-polyfill",
		applyToEnvironment: (environment) => environment.name === "client",
		configResolved(config) {
			try {
				isDisabled = config.build.modulePreload === false || config.build.modulePreload.polyfill === false;
				sourcemap = !!config.build.sourcemap;
				entry = resolveClientEntry(config);
			} catch {
				console.debug("[nuxt:module-preload-polyfill] Could not resolve client entry, module preload polyfill will not be injected.");
			}
		},
		transform(code, id) {
			if (isDisabled || id.replace(QUERY_RE$1, "") !== entry) return;
			const s = new MagicString(code);
			s.prepend("import \"vite/modulepreload-polyfill\";\n");
			return {
				code: s.toString(),
				map: sourcemap ? s.generateMap({ hires: true }) : void 0
			};
		}
	};
}
//#endregion
//#region src/plugins/vite-node.ts
function getManifest(nuxt, viteServer, clientEntry) {
	const css = /* @__PURE__ */ new Set();
	const ssrServer = nuxt.options.experimental.viteEnvironmentApi ? viteServer.environments.ssr : viteServer;
	for (const key of ssrServer.moduleGraph.urlToModuleMap.keys()) if (isCSS(key)) {
		if ("raw" in getQuery(key)) continue;
		const importers = ssrServer.moduleGraph.urlToModuleMap.get(key)?.importers;
		if (importers && [...importers].every((i) => i.id && "raw" in getQuery(i.id))) continue;
		css.add(key);
	}
	for (const globalCss of nuxt.options.css) if (typeof globalCss === "string") {
		let resolved = resolveAlias(globalCss, nuxt.options.alias);
		if (!isAbsolute(resolved)) {
			resolved = resolveModulePath(resolved, {
				try: true,
				from: nuxt.options.modulesDir.map((d) => directoryToURL(d))
			});
			if (!resolved) continue;
			css.add("/@fs" + resolved);
		} else css.add(resolved);
	}
	return normalizeViteManifest({
		"@vite/client": {
			file: "@vite/client",
			css: [...css],
			module: true,
			isEntry: true
		},
		...nuxt.options.features.noScripts === "all" ? {} : { [clientEntry]: {
			file: clientEntry,
			isEntry: true,
			module: true,
			resourceType: "script"
		} }
	});
}
function generateSocketPath() {
	const socketName = `nuxt-vite-node-${`${process.pid}-${Date.now()}`}`;
	if (process.platform === "win32") return join(String.raw`\\.\pipe`, socketName);
	if (process.platform === "linux") {
		if (Number.parseInt(process.versions.node.split(".")[0], 10) >= 20 && provider !== "stackblitz") {
			let isDocker = false;
			try {
				isDocker = fs.existsSync("/.dockerenv") || fs.existsSync("/proc/1/cgroup") && fs.readFileSync("/proc/1/cgroup", "utf8").includes("docker");
			} catch {}
			if (!isDocker) return `\0${socketName}.sock`;
		}
	}
	return join(os.tmpdir(), `${socketName}.sock`);
}
function useInvalidates() {
	const invalidates = /* @__PURE__ */ new Set();
	function markInvalidate(mod) {
		if (!mod.id) return;
		if (invalidates.has(mod.id)) return;
		invalidates.add(mod.id);
		markInvalidates(mod.importers);
	}
	function markInvalidates(mods) {
		if (!mods) return;
		for (const mod of mods) markInvalidate(mod);
	}
	return {
		invalidates,
		markInvalidate,
		markInvalidates
	};
}
function ViteNodePlugin(nuxt) {
	let socketServer;
	const socketPath = generateSocketPath();
	const { invalidates, markInvalidate, markInvalidates } = useInvalidates();
	async function cleanupSocket() {
		if (socketServer && socketServer.listening) await new Promise((resolveClose) => socketServer.close(() => resolveClose()));
		if (socketPath && !socketPath.startsWith("\\\\.\\pipe\\")) try {
			await unlink(socketPath);
		} catch {}
	}
	return {
		name: "nuxt:vite-node-server",
		enforce: "post",
		configureServer(clientServer) {
			if (!tryUseNuxt()) return;
			function resolveServer(ssrServer) {
				const viteNodeServerOptions = {
					socketPath,
					root: nuxt.options.srcDir,
					entryPath: resolveServerEntry(ssrServer.config),
					base: ssrServer.config.base || "/_nuxt/",
					maxRetryAttempts: nuxt.options.vite.viteNode?.maxRetryAttempts,
					baseRetryDelay: nuxt.options.vite.viteNode?.baseRetryDelay,
					maxRetryDelay: nuxt.options.vite.viteNode?.maxRetryDelay,
					requestTimeout: nuxt.options.vite.viteNode?.requestTimeout,
					baseURL: nuxt.options.devServer.url
				};
				process.env.NUXT_VITE_NODE_OPTIONS = JSON.stringify(viteNodeServerOptions);
				socketServer = createViteNodeSocketServer(nuxt, ssrServer, clientServer, invalidates, viteNodeServerOptions);
			}
			if (nuxt.options.experimental.viteEnvironmentApi) resolveServer(clientServer);
			else nuxt.hook("vite:serverCreated", (ssrServer, ctx) => ctx.isServer ? resolveServer(ssrServer) : void 0);
			nuxt.hook("close", cleanupSocket);
			const client = nuxt.options.experimental.viteEnvironmentApi ? clientServer.environments.client : clientServer;
			nuxt.hook("app:templatesGenerated", (_app, changedTemplates) => {
				for (const template of changedTemplates) {
					const mods = client.moduleGraph.getModulesByFile(`virtual:nuxt:${encodeURIComponent(template.dst)}`);
					for (const mod of mods || []) markInvalidate(mod);
				}
			});
			clientServer.watcher.on("all", (_event, file) => {
				invalidates.add(file);
				markInvalidates(clientServer.moduleGraph.getModulesByFile(normalize(file)));
			});
		},
		async buildEnd() {
			await cleanupSocket();
		}
	};
}
let _node;
let _nodeServer;
function getNode(server) {
	if (!_node || _nodeServer !== server) {
		_node = new ViteNodeServer(server, { transformMode: {
			ssr: [/.*/],
			web: []
		} });
		_nodeServer = server;
	}
	return _node;
}
function createViteNodeSocketServer(nuxt, ssrServer, clientServer, invalidates, config) {
	const server = net.createServer((socket) => {
		const INITIAL_BUFFER_SIZE = 64 * 1024;
		const MAX_BUFFER_SIZE = 1024 * 1024 * 1024;
		let buffer = Buffer.alloc(INITIAL_BUFFER_SIZE);
		let writeOffset = 0;
		let readOffset = 0;
		socket.setNoDelay(true);
		socket.setKeepAlive(true, 0);
		async function processMessage(request) {
			try {
				switch (request.type) {
					case "manifest": {
						const manifestData = getManifest(nuxt, ssrServer, resolveClientEntry(clientServer.config));
						sendResponse(socket, request.id, manifestData);
						return;
					}
					case "invalidates": {
						const responsePayload = Array.from(invalidates);
						invalidates.clear();
						sendResponse(socket, request.id, responsePayload);
						return;
					}
					case "resolve": {
						const { id: resolveId, importer } = request.payload;
						if (!resolveId) throw {
							status: 400,
							message: "Missing id for resolve"
						};
						const resolvedResult = await (nuxt.options.experimental.viteEnvironmentApi ? ssrServer.environments.ssr.pluginContainer : getNode(ssrServer)).resolveId(resolveId, importer).catch(() => null);
						sendResponse(socket, request.id, resolvedResult);
						return;
					}
					case "module": {
						if (request.payload.moduleId === "/") throw {
							status: 400,
							message: "Invalid moduleId"
						};
						const response = await (nuxt.options.experimental.viteEnvironmentApi ? ssrServer.environments.ssr : getNode(ssrServer)).fetchModule(request.payload.moduleId).catch(async (err) => {
							const errorData = {
								code: "VITE_ERROR",
								id: request.payload.moduleId,
								stack: err.stack || "",
								message: err.message || ""
							};
							if (err.frame) errorData.frame = err.frame;
							if (!errorData.frame && err.code === "PARSE_ERROR") try {
								errorData.frame = await (nuxt.options.experimental.viteEnvironmentApi ? ssrServer.environments.client : getNode(ssrServer)).transformRequest(request.payload.moduleId).then((res) => `${err.message || ""}\n${res?.code}`).catch(() => void 0);
							} catch {}
							throw {
								data: errorData,
								message: err.message || "Error fetching module"
							};
						});
						sendResponse(socket, request.id, response);
						return;
					}
					default: throw {
						status: 400,
						message: `Unknown request type: ${request.type}`
					};
				}
			} catch (error) {
				sendError(socket, request.id, error);
			}
		}
		const resetBuffer = () => {
			writeOffset = 0;
			readOffset = 0;
		};
		const compactBuffer = () => {
			if (readOffset > 0) {
				const remainingData = writeOffset - readOffset;
				if (remainingData > 0) buffer.copy(buffer, 0, readOffset, writeOffset);
				writeOffset = remainingData;
				readOffset = 0;
			}
		};
		const ensureBufferCapacity = (additionalBytes) => {
			const requiredSize = writeOffset + additionalBytes;
			if (requiredSize > MAX_BUFFER_SIZE) throw new Error(`Buffer size limit exceeded: ${requiredSize} > ${MAX_BUFFER_SIZE}`);
			if (requiredSize > buffer.length) {
				compactBuffer();
				if (writeOffset + additionalBytes > buffer.length) {
					const newSize = Math.min(Math.max(buffer.length * 2, requiredSize), MAX_BUFFER_SIZE);
					const newBuffer = Buffer.alloc(newSize);
					buffer.copy(newBuffer, 0, 0, writeOffset);
					buffer = newBuffer;
				}
			}
		};
		socket.on("data", (data) => {
			try {
				ensureBufferCapacity(data.length);
				data.copy(buffer, writeOffset);
				writeOffset += data.length;
				while (writeOffset - readOffset >= 4) {
					const totalLength = 4 + buffer.readUInt32BE(readOffset);
					if (writeOffset - readOffset < totalLength) break;
					const messageJSON = buffer.subarray(readOffset + 4, readOffset + totalLength).toString("utf-8");
					readOffset += totalLength;
					try {
						const request = JSON.parse(messageJSON);
						processMessage(request).catch((error) => {
							sendError(socket, request?.id || "unknown", error);
						});
					} catch (parseError) {
						const errorMessage = parseError instanceof Error ? parseError.message : "Unknown parse error";
						socket.destroy(/* @__PURE__ */ new Error(`Invalid JSON in message: ${errorMessage}`));
						return;
					}
				}
				if (readOffset > buffer.length / 2) compactBuffer();
			} catch (error) {
				socket.destroy(error instanceof Error ? error : /* @__PURE__ */ new Error("Buffer management error"));
			}
		});
		socket.on("error", () => {
			resetBuffer();
		});
		socket.on("close", () => {
			resetBuffer();
		});
	});
	const currentSocketPath = config.socketPath;
	if (!currentSocketPath) throw new Error("Socket path not configured for ViteNodeSocketServer.");
	if (!currentSocketPath.startsWith("\\\\.\\pipe\\")) try {
		fs.unlinkSync(currentSocketPath);
	} catch (unlinkError) {
		if (unlinkError.code !== "ENOENT") {}
	}
	server.listen(currentSocketPath);
	server.on("error", () => {});
	return server;
}
function sendResponse(socket, id, data) {
	try {
		const response = {
			id,
			type: "response",
			data
		};
		const responseJSON = JSON.stringify(response);
		const messageBuffer = Buffer.from(responseJSON, "utf-8");
		const messageLength = messageBuffer.length;
		const fullMessage = Buffer.alloc(4 + messageLength);
		fullMessage.writeUInt32BE(messageLength, 0);
		messageBuffer.copy(fullMessage, 4);
		socket.write(fullMessage, (err) => {
			if (err) {}
		});
	} catch (error) {
		sendError(socket, id, error);
	}
}
function sendError(socket, id, error) {
	const errorResponse = {
		id,
		type: "error",
		error: {
			message: error.message,
			stack: error.stack,
			status: error.status,
			statusText: error.statusText,
			data: error.data
		}
	};
	const responseJSON = JSON.stringify(errorResponse);
	const messageBuffer = Buffer.from(responseJSON, "utf-8");
	const messageLength = messageBuffer.length;
	const fullMessage = Buffer.alloc(4 + messageLength);
	fullMessage.writeUInt32BE(messageLength, 0);
	messageBuffer.copy(fullMessage, 4);
	socket.write(fullMessage, (err) => {
		if (err) {}
	});
}
async function writeDevServer(nuxt) {
	const runnerResolvedPath = resolveModulePath("#vite-node-runner", { from: import.meta.url });
	const serverResolvedPath = resolveModulePath("#vite-node-entry", { from: import.meta.url });
	const fetchResolvedPath = resolveModulePath("#vite-node", { from: import.meta.url });
	const serverDist = join(nuxt.options.buildDir, "dist/server");
	await mkdir(serverDist, { recursive: true });
	await Promise.all([
		writeFile(join(serverDist, "server.mjs"), `export { default } from ${JSON.stringify(pathToFileURL(serverResolvedPath).href)}`),
		writeFile(join(serverDist, "runner.mjs"), `export { default } from ${JSON.stringify(pathToFileURL(runnerResolvedPath).href)}`),
		writeFile(join(serverDist, "client.precomputed.mjs"), `export default undefined`),
		writeFile(join(serverDist, "client.manifest.mjs"), `
import { viteNodeFetch } from ${JSON.stringify(pathToFileURL(fetchResolvedPath))}
export default () => viteNodeFetch.getManifest()
    `)
	]);
}
//#endregion
//#region src/plugins/public-dirs.ts
const PREFIX = "virtual:public?";
const PREFIX_RE = /^virtual:public\?/;
const CSS_URL_RE = /url\((\/[^)]+)\)/g;
const CSS_URL_SINGLE_RE = /url\(\/[^)]+\)/;
const RENDER_CHUNK_RE = /(?<= = )['"`]/;
const PublicDirsPlugin = (options) => {
	const { resolveFromPublicAssets } = useResolveFromPublicAssets();
	let sourcemap;
	return [{
		name: "nuxt:vite-public-dir-resolution-dev",
		apply() {
			return !!options.dev && !!options.baseURL && options.baseURL !== "/";
		},
		transform(code, id) {
			if (!isCSSRequest(id) || !CSS_URL_SINGLE_RE.test(code)) return;
			const s = new MagicString(code);
			for (const [full, url] of code.matchAll(CSS_URL_RE)) if (url && resolveFromPublicAssets(url)) s.replace(full, `url(${options.baseURL}${url})`);
			if (s.hasChanged()) return {
				code: s.toString(),
				map: sourcemap ? s.generateMap({ hires: true }) : void 0
			};
		}
	}, {
		name: "nuxt:vite-public-dir-resolution",
		configResolved(config) {
			sourcemap = !!config.build.sourcemap;
		},
		load: {
			order: "pre",
			filter: { id: PREFIX_RE },
			handler(id) {
				return `import { publicAssetsURL } from '#internal/nuxt/paths';export default publicAssetsURL(${JSON.stringify(decodeURIComponent(id.slice(15)))})`;
			}
		},
		resolveId: {
			order: "post",
			filter: { id: { exclude: [
				/^\/__skip_vite$/,
				/^[^/]/,
				/^\/@fs/
			] } },
			handler(id) {
				if (resolveFromPublicAssets(id)) return PREFIX + encodeURIComponent(id);
			}
		},
		renderChunk(code, chunk) {
			if (!chunk.facadeModuleId?.includes("?inline&used")) return;
			const s = new MagicString(code);
			const q = code.match(RENDER_CHUNK_RE)?.[0] || "\"";
			for (const [full, url] of code.matchAll(CSS_URL_RE)) if (url && resolveFromPublicAssets(url)) s.replace(full, `url(${q} + publicAssetsURL(${q}${url}${q}) + ${q})`);
			if (s.hasChanged()) {
				s.prepend(`import { publicAssetsURL } from '#internal/nuxt/paths';`);
				return {
					code: s.toString(),
					map: sourcemap ? s.generateMap({ hires: true }) : void 0
				};
			}
		},
		generateBundle(_outputOptions, bundle) {
			for (const [file, chunk] of Object.entries(bundle)) {
				if (!file.endsWith(".css") || chunk.type !== "asset") continue;
				let css = chunk.source.toString();
				let wasReplaced = false;
				for (const [full, url] of css.matchAll(CSS_URL_RE)) if (url && resolveFromPublicAssets(url)) {
					const relativeURL = relative(withLeadingSlash(dirname(file)), url);
					css = css.replace(full, `url(${relativeURL})`);
					wasReplaced = true;
				}
				if (wasReplaced) chunk.source = css;
			}
		}
	}];
};
const PUBLIC_ASSETS_RE = /[?#].*$/;
function useResolveFromPublicAssets() {
	const nitro = useNitro();
	function resolveFromPublicAssets(id) {
		for (const dir of nitro.options.publicAssets) {
			if (!id.startsWith(withTrailingSlash(dir.baseURL || "/"))) continue;
			if (existsSync(id.replace(PUBLIC_ASSETS_RE, "").replace(withTrailingSlash(dir.baseURL || "/"), withTrailingSlash(dir.dir)))) return id;
		}
	}
	return { resolveFromPublicAssets };
}
//#endregion
//#region src/utils/logger.ts
let duplicateCount = 0;
let lastType = null;
let lastMsg = null;
const logLevelMap = {
	silent: "silent",
	info: "info",
	verbose: "info"
};
const logLevelMapReverse = {
	silent: 0,
	error: 1,
	warn: 2,
	info: 3
};
const RUNTIME_RESOLVE_REF_RE = /^([^ ]+) referenced in/m;
function createViteLogger(config, ctx = {}) {
	const loggedErrors = /* @__PURE__ */ new WeakSet();
	const canClearScreen = hasTTY && !isCI && config.clearScreen;
	const _logger = createLogger();
	const relativeOutDir = relative(config.root, config.build.outDir || "");
	const clear = () => {
		_logger.clearScreen("silent");
	};
	const clearScreen = canClearScreen ? clear : () => {};
	const { resolveFromPublicAssets } = useResolveFromPublicAssets();
	function output(type, msg, options = {}) {
		if (typeof msg === "string" && !process.env.DEBUG) {
			if (msg.startsWith("Sourcemap") && msg.includes("node_modules")) return;
			if (msg.includes("didn't resolve at build time, it will remain unchanged to be resolved at runtime")) {
				const id = msg.trim().match(RUNTIME_RESOLVE_REF_RE)?.[1];
				if (id && resolveFromPublicAssets(id)) return;
			}
			if (type === "info" && ctx.hideOutput && msg.includes(relativeOutDir)) return;
			if (ctx.onStaleDep && type === "warn" && (msg.includes("Failed to resolve dependency") || msg.includes("Cannot optimize dependency"))) {
				const match = stripAnsi(msg).match(/(?:Failed to resolve|Cannot optimize) dependency:\s*([^,]+)/);
				if (match) {
					ctx.onStaleDep(match[1].trim());
					return;
				}
			}
			if (ctx.onNewDeps && type === "info" && msg.includes("new dependencies optimized:")) {
				const match = stripAnsi(msg).match(/new dependencies optimized:\s*(.+)/);
				if (match) {
					ctx.onNewDeps(match[1].split(",").map((d) => d.trim()).filter(Boolean));
					return;
				}
			}
			if (ctx.onNewDeps && type === "info" && (msg.includes("optimized dependencies changed. reloading") || msg.includes("add these dependencies to optimizeDeps.include"))) return;
		}
		const sameAsLast = lastType === type && lastMsg === msg;
		if (sameAsLast) {
			duplicateCount += 1;
			clearScreen();
		} else {
			duplicateCount = 0;
			lastType = type;
			lastMsg = msg;
			if (options.clear) clearScreen();
		}
		if (options.error) loggedErrors.add(options.error);
		const prevLevel = logger.level;
		logger.level = logLevelMapReverse[config.logLevel || "info"];
		logger[type](msg + (sameAsLast ? colorize("dim", ` (x${duplicateCount + 1})`) : ""));
		logger.level = prevLevel;
	}
	const warnedMessages = /* @__PURE__ */ new Set();
	const viteLogger = {
		hasWarned: false,
		info(msg, opts) {
			output("info", msg, opts);
		},
		warn(msg, opts) {
			viteLogger.hasWarned = true;
			output("warn", msg, opts);
		},
		warnOnce(msg, opts) {
			if (warnedMessages.has(msg)) return;
			viteLogger.hasWarned = true;
			output("warn", msg, opts);
			warnedMessages.add(msg);
		},
		error(msg, opts) {
			viteLogger.hasWarned = true;
			output("error", msg, opts);
		},
		clearScreen() {
			clear();
		},
		hasErrorLogged(error) {
			return loggedErrors.has(error);
		}
	};
	return viteLogger;
}
//#endregion
//#region src/plugins/optimize-deps-hint.ts
function formatIncludeSnippet(deps, cjsDeps) {
	if (!deps.length) return "[]";
	return `[\n${deps.map((d) => {
		return `        '${d}',${cjsDeps?.has(d) ? " // CJS" : ""}`;
	}).join("\n")}\n      ]`;
}
function configBlock(deps, cjsDeps) {
	return colorize("gray", `export default defineNuxtConfig({\n  vite: {\n    optimizeDeps: {\n      include: ${formatIncludeSnippet(deps, cjsDeps)}\n    }\n  }\n})\n\n`) + `Learn more: https://vite.dev/guide/dep-pre-bundling.html`;
}
function formatDepLines(deps, importers, cjsDeps) {
	const ungrouped = [];
	const grouped = /* @__PURE__ */ new Map();
	for (const d of deps) {
		const importer = importers?.get(d);
		const label = colorize("cyan", d) + (cjsDeps?.has(d) ? " " + colorize("yellow", "(CJS)") : "");
		if (importer) {
			const list = grouped.get(importer) || [];
			list.push(label);
			grouped.set(importer, list);
		} else ungrouped.push(`  ${label}`);
	}
	const lines = [...ungrouped];
	for (const [file, labels] of grouped) if (labels.length === 1) lines.push(`  ${labels[0]} ${colorize("gray", `← ${file}`)}`);
	else {
		lines.push(`  ${colorize("gray", file)}`);
		for (const label of labels) lines.push(`    ${label}`);
	}
	return lines.join("\n");
}
function formatStaleDepsHint(userStale, moduleStale) {
	const lines = [];
	for (const d of userStale) lines.push(`  ${colorize("cyan", d)}`);
	for (const d of moduleStale) lines.push(`  ${colorize("cyan", d)} ${colorize("gray", "(from a Nuxt module)")}`);
	return `Unresolvable \`optimizeDeps.include\` entries:\n${lines.join("\n")}`;
}
const userOptimizeDepsInclude = /* @__PURE__ */ new WeakMap();
const optimizerCallbacks = /* @__PURE__ */ new WeakMap();
function OptimizeDepsHintPlugin(nuxt) {
	const rootDir = nuxt.options.rootDir;
	const getUserInclude = () => userOptimizeDepsInclude.get(nuxt) || [];
	const discovered = /* @__PURE__ */ new Set();
	const userStale = /* @__PURE__ */ new Set();
	const moduleStale = /* @__PURE__ */ new Set();
	let pending = /* @__PURE__ */ new Set();
	let hintTimer = null;
	let hasShownStaleHint = false;
	let hasShownFullHint = false;
	const getSnippetDeps = () => [...new Set([...getUserInclude().filter((d) => !userStale.has(d)), ...discovered])];
	let getCjsDeps = () => /* @__PURE__ */ new Set();
	const importerOf = /* @__PURE__ */ new Map();
	function scheduleHint() {
		if (hintTimer) clearTimeout(hintTimer);
		hintTimer = setTimeout(() => {
			const hasNew = pending.size > 0;
			const hasStale = !hasShownStaleHint && (userStale.size > 0 || moduleStale.size > 0);
			if (hasNew) {
				const newDeps = [...pending];
				pending = /* @__PURE__ */ new Set();
				const cjsDeps = getCjsDeps();
				const relativeImporters = /* @__PURE__ */ new Map();
				for (const dep of newDeps) {
					const imp = importerOf.get(dep);
					if (imp) relativeImporters.set(dep, "./" + relative(rootDir, imp));
					importerOf.delete(dep);
				}
				if (hasShownFullHint) {
					const depList = newDeps.map((d) => colorize("cyan", d) + (cjsDeps.has(d) ? " " + colorize("yellow", "(CJS)") : "")).join(", ");
					logger.info(`New dependencies found: ${depList}`);
				} else {
					hasShownFullHint = true;
					const snippetDeps = getSnippetDeps();
					const parts = [];
					parts.push(`Vite discovered new dependencies at runtime:\n${formatDepLines(newDeps, relativeImporters, cjsDeps)}`);
					if (hasStale) {
						hasShownStaleHint = true;
						parts.push(formatStaleDepsHint([...userStale], [...moduleStale]));
					}
					parts.push(`Pre-bundle them in your \`nuxt.config.ts\` to avoid page reloads:\n\n` + configBlock(snippetDeps, cjsDeps));
					logger.info(parts.join("\n\n"));
				}
			} else if (hasStale) {
				hasShownStaleHint = true;
				const parts = [];
				parts.push(formatStaleDepsHint([...userStale], [...moduleStale]));
				parts.push(`Update your \`nuxt.config.ts\`:\n\n` + configBlock(getSnippetDeps()));
				logger.warn(parts.join("\n\n"));
			}
		}, 3e3);
	}
	optimizerCallbacks.set(nuxt, {
		onNewDeps(deps) {
			for (const dep of deps) {
				if (getUserInclude().includes(dep)) continue;
				discovered.add(dep);
				pending.add(dep);
			}
			if (pending.size > 0) scheduleHint();
		},
		onStaleDep(dep) {
			if (getUserInclude().includes(dep)) userStale.add(dep);
			else moduleStale.add(dep);
			scheduleHint();
		}
	});
	return {
		name: "nuxt:optimize-deps-hint",
		apply: "serve",
		applyToEnvironment: (environment) => environment.name === "client",
		resolveId: {
			order: "pre",
			handler(source, importer) {
				if (importer && !importer.includes("/node_modules/") && !source.startsWith(".") && !source.startsWith("/") && !source.startsWith("\0")) {
					if (!importerOf.has(source)) importerOf.set(source, importer);
				}
			}
		},
		configureServer(server) {
			const optimizer = server.environments.client?.depsOptimizer;
			if (!optimizer) return;
			getCjsDeps = () => {
				const cjs = /* @__PURE__ */ new Set();
				for (const [id, info] of Object.entries({
					...optimizer.metadata.optimized,
					...optimizer.metadata.discovered
				})) if (info.needsInterop) cjs.add(id);
				return cjs;
			};
			server.httpServer?.on("close", () => {
				if (hintTimer) clearTimeout(hintTimer);
			});
		}
	};
}
//#endregion
//#region src/plugins/stable-entry.ts
function StableEntryPlugin(nuxt) {
	let sourcemap;
	let entryFileName;
	const nitro = useNitro();
	nitro.options.virtual ||= {};
	nitro.options._config.virtual ||= {};
	nitro.options._config.virtual["#internal/entry-chunk.mjs"] = nitro.options.virtual["#internal/entry-chunk.mjs"] = () => `export const entryFileName = ${JSON.stringify(entryFileName)}`;
	return {
		name: "nuxt:stable-entry",
		configResolved(config) {
			sourcemap = !!config.build.sourcemap;
		},
		apply: () => !nuxt.options.dev && nuxt.options.experimental.entryImportMap,
		applyToEnvironment(environment) {
			if (environment.name !== "client") return false;
			if (environment.config.build.target) {
				if (!toArray(environment.config.build.target).every(isSupported)) return false;
			}
			return toArray(environment.config.build.rollupOptions?.output).some((output) => typeof output?.entryFileNames === "string" && output?.entryFileNames.includes("[hash]"));
		},
		renderChunk(code, chunk, _options, meta) {
			const entry = Object.values(meta.chunks).find((chunk) => chunk.isEntry && chunk.name === "entry")?.fileName;
			if (!entry || !chunk.imports.includes(entry)) return;
			const filename = new RegExp(`(?<=['"])[\\./]*${escapeStringRegexp(basename(entry))}`, "g");
			const s = new MagicString(code);
			s.replaceAll(filename, "#entry");
			if (s.hasChanged()) return {
				code: s.toString(),
				map: sourcemap ? s.generateMap({ hires: true }) : void 0
			};
		},
		writeBundle(_options, bundle) {
			let entry = Object.values(bundle).find((chunk) => chunk.type === "chunk" && chunk.isEntry && chunk.name === "entry")?.fileName;
			const prefix = withoutLeadingSlash(nuxt.options.app.buildAssetsDir);
			if (entry?.startsWith(prefix)) entry = entry.slice(prefix.length);
			entryFileName = entry;
		}
	};
}
const supportedEnvironments = {
	chrome: 89,
	edge: 89,
	firefox: 108,
	ie: Infinity,
	ios: 16.4,
	opera: 75,
	safari: 16.4
};
function isSupported(target) {
	const [engine, _version] = target.split(/(?<=[a-z])(?=\d)/);
	const constraint = supportedEnvironments[engine];
	if (!constraint) return true;
	const version = Number(_version);
	return Number.isNaN(version) || Number(version) >= constraint;
}
//#endregion
//#region src/plugins/analyze.ts
async function AnalyzePlugin(nuxt) {
	if (nuxt.options.test) return;
	const analyzeOptions = defu({}, nuxt.options.build.analyze);
	if (!analyzeOptions.enabled) return;
	let visualizer;
	try {
		visualizer = await import("rollup-plugin-visualizer").then((r) => r.visualizer);
	} catch (_err) {
		const err = _err;
		if (err.code !== "ERR_MODULE_NOT_FOUND" && err.code !== "MODULE_NOT_FOUND") throw err;
		if (!isCI && hasTTY) {
			logger.info("Analyzing bundles requires an additional dependency.");
			if (await logger.prompt("Install `rollup-plugin-visualizer`?", {
				type: "confirm",
				choices: [{
					name: "Yes",
					value: true
				}, {
					name: "No",
					value: false
				}]
			})) {
				logger.start("Installing `rollup-plugin-visualizer`...");
				await addDependency("rollup-plugin-visualizer", {
					dev: true,
					cwd: nuxt.options.rootDir,
					silent: true
				});
				logger.info("Rerun Nuxt to analyze your bundle.");
				process.exit(1);
			}
		}
		logger.info("Cannot find `rollup-plugin-visualizer`.");
		process.exit(1);
	}
	return {
		name: "nuxt:analyze",
		applyToEnvironment(environment) {
			if (environment.name !== "client") return false;
			return [{
				name: "nuxt:analyze-minify",
				async generateBundle(_opts, outputBundle) {
					for (const _bundleId in outputBundle) {
						const bundle = outputBundle[_bundleId];
						if (!bundle || bundle.type !== "chunk") continue;
						const minifiedModuleEntryPromises = [];
						for (const [moduleId, module] of Object.entries(bundle.modules)) minifiedModuleEntryPromises.push(transformWithEsbuild(module.code || "", "index.js", { minify: true }).then((result) => [moduleId, {
							...module,
							code: result.code
						}]));
						bundle.modules = Object.fromEntries(await Promise.all(minifiedModuleEntryPromises));
					}
				}
			}, visualizer({
				...analyzeOptions,
				filename: "filename" in analyzeOptions && analyzeOptions.filename ? analyzeOptions.filename.replace("{name}", "client") : void 0,
				title: "Client bundle stats",
				gzipSize: true,
				brotliSize: true
			})];
		}
	};
}
//#endregion
//#region src/plugins/dev-server.ts
function DevServerPlugin(nuxt) {
	let useViteCors = false;
	const nitro = useNitro();
	return {
		name: "nuxt:dev-server",
		async config(config) {
			for (const item of [
				config.optimizeDeps,
				config.environments?.client?.optimizeDeps,
				config.environments?.ssr?.optimizeDeps
			]) {
				if (!item) continue;
				const exclude = new Set(item.exclude ?? []);
				item.include = item.include?.filter((dep) => !exclude.has(dep));
			}
			if (!nuxt.options.dev && config.server) config.server.hmr = false;
			useViteCors = config.server?.cors !== void 0;
			if (!useViteCors) {
				config.server ??= {};
				config.server.cors = false;
			}
			if (config.server && config.server.hmr !== false) {
				const serverDefaults = { hmr: { protocol: nuxt.options.devServer.https ? "wss" : void 0 } };
				if (typeof config.server.hmr !== "object" || !config.server.hmr.server) {
					serverDefaults.hmr ??= {};
					const hmrPortDefault = 24678;
					serverDefaults.hmr.port = await getPort({
						verbose: false,
						portRange: [hmrPortDefault, hmrPortDefault + 20]
					});
				}
				if (nuxt.options.devServer.https) serverDefaults.https = nuxt.options.devServer.https === true ? {} : nuxt.options.devServer.https;
				config.server = defu(config.server, serverDefaults);
			}
		},
		async configureServer(viteServer) {
			nuxt.hook("app:templatesGenerated", async (_app, changedTemplates) => {
				await Promise.all(changedTemplates.map(async (template) => {
					for (const mod of viteServer.moduleGraph.getModulesByFile(`virtual:nuxt:${encodeURIComponent(template.dst)}`) || []) {
						viteServer.moduleGraph.invalidateModule(mod);
						await viteServer.reloadModule(mod);
					}
				}));
			});
			if (nuxt.options.experimental.viteEnvironmentApi) await nuxt.callHook("vite:serverCreated", viteServer, {
				isClient: true,
				isServer: true
			});
			const staticBases = [];
			for (const folder of nitro.options.publicAssets) if (folder.baseURL && folder.baseURL !== "/" && folder.baseURL.startsWith(nuxt.options.app.buildAssetsDir)) staticBases.push(folder.baseURL.replace(/\/?$/, "/"));
			const devHandlerRegexes = [];
			for (const handler of nuxt.options.devServerHandlers) if (handler.route && handler.route !== "/" && handler.route.startsWith(nuxt.options.app.buildAssetsDir)) devHandlerRegexes.push(new RegExp(`^${handler.route.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/:[^/]+/g, "[^/]+").replace(/\*\*/g, ".*").replace(/\*/g, "[^/]*")}$`));
			let _isProxyPath;
			function isProxyPath(url) {
				if (_isProxyPath) return _isProxyPath(url);
				const proxyConfig = viteServer.config.server.proxy;
				const proxyPatterns = [];
				if (proxyConfig) for (const key in proxyConfig) if (key.startsWith("^")) try {
					proxyPatterns.push({
						type: "regex",
						value: new RegExp(key)
					});
				} catch {}
				else proxyPatterns.push({
					type: "string",
					value: key
				});
				_isProxyPath = function isProxyPath(path) {
					for (const pattern of proxyPatterns) if (pattern.type === "regex" && pattern.value.test(path)) return true;
					else if (pattern.type === "string" && path.startsWith(pattern.value)) return true;
					return false;
				};
				return _isProxyPath(url);
			}
			const viteMiddleware = defineEventHandler(async (event) => {
				const url = "url" in event ? event.url.pathname + event.url.search + event.url.hash : event.path;
				let isViteRoute = url.startsWith(viteServer.config.base);
				if (!isViteRoute) {
					for (const viteRoute of viteServer.middlewares.stack) if (viteRoute.route.length > 1 && url.startsWith(viteRoute.route)) {
						isViteRoute = true;
						break;
					}
					isViteRoute ||= isProxyPath(url);
				}
				const { req, res } = "runtime" in event ? event.runtime.node : event.node;
				if (!isViteRoute) req._skip_transform = true;
				const _originalPath = req.url;
				await new Promise((resolve, reject) => {
					viteServer.middlewares.handle(req, res, (err) => {
						req.url = _originalPath;
						return err ? reject(err) : resolve(null);
					});
				});
				if (url.startsWith(nuxt.options.app.buildAssetsDir) && !staticBases.some((baseURL) => url.startsWith(baseURL)) && !devHandlerRegexes.some((regex) => regex.test(url))) {
					res.statusCode = 404;
					res.end("Not Found");
					return;
				}
			});
			await nuxt.callHook("server:devHandler", viteMiddleware, { cors: (url) => {
				if (useViteCors) return false;
				if (url.startsWith(viteServer.config.base)) return true;
				for (const viteRoute of viteServer.middlewares.stack) if (viteRoute.route.length > 1 && url.startsWith(viteRoute.route)) return true;
				return isProxyPath(url);
			} });
			return () => {
				const mw = {
					route: "",
					handle: (req, res, next) => {
						if (req._skip_transform && req.url) req.url = joinURL("/__skip_vite", req.url.replace(/\?.*/, ""));
						next();
					}
				};
				const transformHandler = viteServer.middlewares.stack.findIndex((m) => m.handle instanceof Function && m.handle.name === "viteTransformMiddleware");
				if (transformHandler === -1) viteServer.middlewares.stack.push(mw);
				else viteServer.middlewares.stack.splice(transformHandler, 0, mw);
			};
		}
	};
}
function defineEventHandler(handler) {
	return Object.assign(handler, { __is_handler__: true });
}
//#endregion
//#region src/plugins/vite-plugin-checker.ts
async function VitePluginCheckerPlugin(nuxt, environment) {
	if (!nuxt.options.test && (nuxt.options.typescript.typeCheck === true || nuxt.options.typescript.typeCheck === "build" && !nuxt.options.dev)) {
		const [checker, tsconfigPath] = await Promise.all([import("vite-plugin-checker").then((r) => r.default), resolveTSConfig(nuxt.options.rootDir)]);
		const supportsProjects = await readTSConfig(tsconfigPath).then((r) => !!r.references?.length);
		return ["client", nuxt.options.ssr ? "ssr" : void 0].filter((name) => environment ? name === environment : !!name).map((envName) => ({
			applyToEnvironment: (environment) => environment.name === envName,
			...checker({ vueTsc: {
				tsconfigPath,
				buildMode: supportsProjects
			} })
		}));
	}
}
//#endregion
//#region src/utils/transpile.ts
function getTranspilePatterns(envs) {
	const nuxt = useNuxt();
	const transpile = [];
	for (let pattern of nuxt.options.build.transpile) {
		if (typeof pattern === "function") {
			const result = pattern(envs);
			if (result) pattern = result;
		}
		if (typeof pattern === "string") transpile.push(new RegExp(escapeStringRegexp(normalize(pattern))));
		else if (pattern instanceof RegExp) transpile.push(pattern);
	}
	return transpile;
}
/**
* Get transpile patterns as strings for use with Vite's optimizeDeps.exclude
* This resolves functions and filters to only string patterns
*/
function getTranspileStrings(envs) {
	const nuxt = useNuxt();
	const patterns = [];
	for (let pattern of nuxt.options.build.transpile) {
		if (typeof pattern === "function") {
			const result = pattern(envs);
			if (result) pattern = result;
		}
		if (typeof pattern === "string") patterns.push(normalize(pattern));
	}
	return patterns;
}
//#endregion
//#region src/shared/client.ts
const clientEnvironment = (nuxt, entry) => {
	return {
		optimizeDeps: {
			entries: [entry],
			include: [],
			exclude: [
				"vue",
				"@vue/runtime-core",
				"@vue/runtime-dom",
				"@vue/reactivity",
				"@vue/shared",
				"@vue/devtools-api",
				"@vue/test-utils",
				"vue-router",
				"vue-demi",
				"nuxt",
				"nuxt/app",
				"@nuxt/test-utils",
				"@unhead/vue",
				"consola",
				"defu",
				"devalue",
				"get-port-please",
				"h3",
				"hookable",
				"klona",
				"ofetch",
				"pathe",
				"ufo",
				"unctx",
				"unenv",
				"#app-manifest",
				"#imports",
				"#app",
				"#build",
				"#build/*",
				"#components",
				"#head",
				"virtual:nuxt:",
				"virtual:nuxt:*",
				...getTranspileStrings({
					isDev: nuxt.options.dev,
					isClient: true
				})
			]
		},
		define: {
			"process.env.NODE_ENV": JSON.stringify(nuxt.options.vite.mode),
			"process.server": false,
			"process.client": true,
			"process.browser": true,
			"process.nitro": false,
			"process.prerender": false,
			"import.meta.server": false,
			"import.meta.client": true,
			"import.meta.browser": true,
			"import.meta.nitro": false,
			"import.meta.prerender": false,
			"module.hot": false,
			...nuxt.options.experimental.clientNodeCompat ? { global: "globalThis" } : {}
		},
		build: {
			sourcemap: nuxt.options.sourcemap.client ? nuxt.options.vite.build?.sourcemap ?? nuxt.options.sourcemap.client : false,
			manifest: "manifest.json",
			outDir: resolve(nuxt.options.buildDir, "dist/client"),
			rollupOptions: { input: { entry } }
		}
	};
};
//#endregion
//#region src/client.ts
async function buildClient(nuxt, ctx) {
	const clientConfig = vite.mergeConfig(ctx.config, vite.mergeConfig({
		configFile: false,
		base: nuxt.options.dev ? joinURL(nuxt.options.app.baseURL.replace(/^\.\//, "/") || "/", nuxt.options.app.buildAssetsDir) : "./",
		css: { devSourcemap: !!nuxt.options.sourcemap.client },
		cacheDir: resolve(nuxt.options.rootDir, ctx.config.cacheDir ?? "node_modules/.cache/vite", "client"),
		plugins: [
			DevStyleSSRPlugin({
				srcDir: nuxt.options.srcDir,
				buildAssetsURL: joinURL(nuxt.options.app.baseURL, nuxt.options.app.buildAssetsDir)
			}),
			RuntimePathsPlugin(),
			ViteNodePlugin(nuxt),
			TypeCheckPlugin(nuxt),
			ModulePreloadPolyfillPlugin(),
			StableEntryPlugin(nuxt),
			AnalyzePlugin(nuxt),
			DevServerPlugin(nuxt),
			VitePluginCheckerPlugin(nuxt, "client"),
			OptimizeDepsHintPlugin(nuxt)
		],
		appType: "custom",
		server: {
			warmup: { clientFiles: [ctx.entry] },
			middlewareMode: true
		},
		...clientEnvironment(nuxt, ctx.entry)
	}, nuxt.options.vite.$client || {}));
	const callbacks = optimizerCallbacks.get(nuxt);
	clientConfig.customLogger = createViteLogger(clientConfig, {
		onNewDeps: callbacks?.onNewDeps,
		onStaleDep: callbacks?.onStaleDep
	});
	await nuxt.callHook("vite:extendConfig", clientConfig, {
		isClient: true,
		isServer: false
	});
	clientConfig.plugins.unshift(vuePlugin(clientConfig.vue), viteJsxPlugin(clientConfig.vueJsx));
	await nuxt.callHook("vite:configResolved", clientConfig, {
		isClient: true,
		isServer: false
	});
	if (nuxt.options.dev) {
		const viteServer = await vite.createServer(clientConfig);
		ctx.clientServer = viteServer;
		nuxt.hook("close", () => viteServer.close());
		await nuxt.callHook("vite:serverCreated", viteServer, {
			isClient: true,
			isServer: false
		});
	} else {
		logger.info("Building client...");
		const start = Date.now();
		logger.restoreAll();
		await vite.build(clientConfig);
		logger.wrapAll();
		await nuxt.callHook("vite:compiled");
		logger.success(`Client built in ${Date.now() - start}ms`);
	}
}
//#endregion
//#region src/manifest.ts
async function writeManifest(ctx) {
	const { nuxt } = ctx;
	const devClientManifest = {
		"@vite/client": {
			isEntry: true,
			file: "@vite/client",
			css: [],
			module: true,
			resourceType: "script"
		},
		...nuxt.options.features.noScripts === "all" ? {} : { [ctx.entry]: {
			isEntry: true,
			file: ctx.entry,
			module: true,
			resourceType: "script"
		} }
	};
	const clientDist = resolve(nuxt.options.buildDir, "dist/client");
	const serverDist = resolve(nuxt.options.buildDir, "dist/server");
	const manifestFile = resolve(clientDist, "manifest.json");
	const clientManifest = nuxt.options.dev ? devClientManifest : JSON.parse(readFileSync(manifestFile, "utf-8"));
	const manifestEntries = Object.values(clientManifest);
	const buildAssetsDir = withTrailingSlash(withoutLeadingSlash(nuxt.options.app.buildAssetsDir));
	const BASE_RE = new RegExp(`^${escapeStringRegexp(buildAssetsDir)}`);
	for (const entry of manifestEntries) {
		entry.file &&= entry.file.replace(BASE_RE, "");
		for (const item of ["css", "assets"]) entry[item] &&= entry[item].map((i) => i.replace(BASE_RE, ""));
	}
	await mkdir(serverDist, { recursive: true });
	if (ctx.config.build?.cssCodeSplit === false) {
		for (const entry of manifestEntries) if (entry.file?.endsWith(".css")) {
			const key = relative(ctx.config.root, ctx.entry);
			clientManifest[key].css ||= [];
			clientManifest[key].css.push(entry.file);
			break;
		}
	}
	const manifest = normalizeViteManifest(clientManifest);
	await nuxt.callHook("build:manifest", manifest);
	const precomputed = precomputeDependencies(manifest);
	await writeFile(resolve(serverDist, "client.manifest.mjs"), "export default " + serialize(manifest), "utf8");
	await writeFile(resolve(serverDist, "client.precomputed.mjs"), "export default " + serialize(precomputed), "utf8");
	if (!nuxt.options.dev) await rm(manifestFile, { force: true });
}
//#endregion
//#region src/plugins/sourcemap-preserver.ts
const SourcemapPreserverPlugin = (nuxt) => {
	let outputDir;
	const ids = /* @__PURE__ */ new Set();
	if (!nuxt.options.sourcemap.server || nuxt.options.dev) return [];
	const nitroPlugin = () => ({
		name: "nuxt:sourcemap-import",
		load: {
			filter: { id: new RegExp("^(\\w:)?" + escapeStringRegexp(outputDir.replace(/\/?$/, "/")).replace(/\//g, "[\\\\/]")) },
			async handler(id) {
				id = resolve(id);
				if (!ids.has(id)) return;
				const [code, map] = await Promise.all([readFile(id, "utf-8").catch(() => void 0), readFile(id + ".map.json", "utf-8").catch(() => void 0)]);
				if (!code) {
					this.warn("Failed loading file");
					return null;
				}
				return {
					code,
					map
				};
			}
		}
	});
	nuxt.hook("nitro:build:before", (nitro) => {
		nitro.options.rollupConfig = defu(nitro.options.rollupConfig, { plugins: [nitroPlugin] });
	});
	return {
		name: "nuxt:sourcemap-export",
		applyToEnvironment: (environment) => {
			return environment.name === "ssr" && environment.config.isProduction;
		},
		apply(config) {
			return !!config.build?.sourcemap;
		},
		configResolved(config) {
			outputDir = config.build.outDir;
		},
		async writeBundle(_options, bundle) {
			for (const chunk of Object.values(bundle)) {
				if (chunk.type !== "chunk" || !chunk.map) continue;
				const id = resolve(outputDir, chunk.fileName);
				ids.add(id);
				const dest = id + ".map.json";
				await mkdir(dirname(dest), { recursive: true });
				await writeFile(dest, JSON.stringify({
					file: chunk.map.file,
					mappings: chunk.map.mappings,
					names: chunk.map.names,
					sources: chunk.map.sources,
					sourcesContent: chunk.map.sourcesContent,
					version: chunk.map.version
				}));
			}
		}
	};
};
//#endregion
//#region src/shared/server.ts
function ssr(nuxt) {
	return {
		external: [
			"nitro/runtime",
			"#internal/nitro",
			"#internal/nitro/utils"
		],
		noExternal: [
			...getTranspilePatterns({
				isServer: true,
				isDev: nuxt.options.dev
			}),
			"/__vue-jsx",
			"#app",
			/^nuxt(\/|$)/,
			/(nuxt|nuxt3|nuxt-nightly)\/(dist|src|app)/
		]
	};
}
function ssrEnvironment(nuxt, serverEntry) {
	return {
		build: {
			reportCompressedSize: false,
			sourcemap: nuxt.options.sourcemap.server ? nuxt.options.vite.build?.sourcemap ?? nuxt.options.sourcemap.server : false,
			outDir: resolve(nuxt.options.buildDir, "dist/server"),
			ssr: true,
			rollupOptions: {
				input: { server: serverEntry },
				external: [
					"nitro/runtime",
					"#internal/nitro",
					"nitropack/runtime",
					"#internal/nuxt/paths",
					"#internal/nuxt/app-config",
					"#app-manifest",
					"#shared",
					new RegExp("^" + escapeStringRegexp(withTrailingSlash(resolve(nuxt.options.rootDir, nuxt.options.dir.shared))))
				],
				output: {
					entryFileNames: "[name].mjs",
					format: "module",
					...vite.rolldownVersion ? {} : { generatedCode: {
						symbols: true,
						constBindings: true,
						arrowFunctions: true
					} }
				},
				onwarn(warning, rollupWarn) {
					if (warning.code && "UNUSED_EXTERNAL_IMPORT" === warning.code) return;
					rollupWarn(warning);
				}
			}
		},
		define: {
			"process.server": true,
			"process.client": false,
			"process.browser": false,
			"import.meta.server": true,
			"import.meta.client": false,
			"import.meta.browser": false,
			"window": "undefined",
			"document": "undefined",
			"navigator": "undefined",
			"location": "undefined",
			"XMLHttpRequest": "undefined"
		},
		optimizeDeps: {
			noDiscovery: true,
			include: void 0,
			exclude: getTranspileStrings({
				isDev: nuxt.options.dev,
				isClient: false
			})
		}
	};
}
//#endregion
//#region src/server.ts
async function buildServer(nuxt, ctx) {
	const serverEntry = nuxt.options.ssr ? ctx.entry : await resolvePath(resolve(nuxt.options.appDir, "entry-spa"));
	const serverConfig = vite.mergeConfig(ctx.config, vite.mergeConfig({
		configFile: false,
		base: nuxt.options.dev ? joinURL(nuxt.options.app.baseURL.replace(/^\.\//, "/") || "/", nuxt.options.app.buildAssetsDir) : void 0,
		css: { devSourcemap: !!nuxt.options.sourcemap.server },
		plugins: [
			SourcemapPreserverPlugin(nuxt),
			VitePluginCheckerPlugin(nuxt, "ssr"),
			{
				name: "nuxt:server-hmr-port",
				async config(serverConfig) {
					serverConfig.server ||= {};
					serverConfig.server.hmr ||= {};
					if (nuxt.options.dev && typeof serverConfig.server.hmr !== "boolean") {
						const hmrPortDefault = 24678;
						serverConfig.server.hmr.port ||= await getPort({
							verbose: false,
							portRange: [hmrPortDefault, hmrPortDefault + 20]
						});
					}
				}
			}
		],
		ssr: ssr(nuxt),
		cacheDir: resolve(nuxt.options.rootDir, ctx.config.cacheDir ?? "node_modules/.cache/vite", "server"),
		server: {
			warmup: { ssrFiles: [serverEntry] },
			preTransformRequests: false,
			hmr: false
		},
		...ssrEnvironment(nuxt, serverEntry)
	}, nuxt.options.vite.$server || {}));
	serverConfig.customLogger = createViteLogger(serverConfig, { hideOutput: !nuxt.options.dev });
	await nuxt.callHook("vite:extendConfig", serverConfig, {
		isClient: false,
		isServer: true
	});
	serverConfig.plugins.unshift(vuePlugin(serverConfig.vue), viteJsxPlugin(serverConfig.vueJsx));
	await nuxt.callHook("vite:configResolved", serverConfig, {
		isClient: false,
		isServer: true
	});
	if (!nuxt.options.dev) {
		const start = Date.now();
		logger.info("Building server...");
		logger.restoreAll();
		await vite.build(serverConfig);
		logger.wrapAll();
		await writeManifest(ctx);
		await nuxt.callHook("vite:compiled");
		logger.success(`Server built in ${Date.now() - start}ms`);
		return;
	}
	if (!nuxt.options.ssr) {
		await writeManifest(ctx);
		await nuxt.callHook("vite:compiled");
		return;
	}
	const ssrServer = await vite.createServer(serverConfig);
	ctx.ssrServer = ssrServer;
	nuxt.hook("close", () => ssrServer.close());
	await nuxt.callHook("vite:serverCreated", ssrServer, {
		isClient: false,
		isServer: true
	});
	nuxt.hook("app:templatesGenerated", async (_app, changedTemplates) => {
		await Promise.all(changedTemplates.map(async (template) => {
			for (const mod of ssrServer.moduleGraph.getModulesByFile(`virtual:nuxt:${encodeURIComponent(template.dst)}`) || []) {
				ssrServer.moduleGraph.invalidateModule(mod);
				await ssrServer.reloadModule(mod);
			}
		}));
	});
	await ssrServer.pluginContainer.buildStart({});
	await writeDevServer(nuxt);
}
//#endregion
//#region src/utils/warmup.ts
function fileToUrl(file, root) {
	const url = relative(root, file);
	if (url[0] === ".") return join("/@fs/", normalize(file));
	return "/" + normalize(url);
}
function normaliseURL(url, base) {
	url = withoutBase(url, base);
	if (url.startsWith("/@id/")) url = url.slice(5).replace("__x00__", "\0");
	url = url.replace(/[?&]import=?(?:&|$)/, "").replace(/[?&]$/, "");
	return url;
}
async function warmupViteServer(server, entries, isServer) {
	const warmedUrls = /* @__PURE__ */ new Set();
	const warmup = async (url) => {
		try {
			url = normaliseURL(url, server.config.base);
			if (warmedUrls.has(url) || isBuiltin(url)) return;
			const m = await server.moduleGraph.getModuleByUrl(url, isServer);
			if (m?.transformResult?.code || m?.ssrTransformResult?.code) return;
			warmedUrls.add(url);
			await server.transformRequest(url, { ssr: isServer });
		} catch (e) {
			logger.debug("[nuxt] warmup for %s failed with: %s", url, e);
		}
		if (isCSSRequest(url)) return;
		try {
			const mod = await server.moduleGraph.getModuleByUrl(url, isServer);
			const deps = mod?.ssrTransformResult?.deps || (mod?.importedModules.size ? Array.from(mod?.importedModules).map((m) => m.url) : []);
			await Promise.all(deps.map((m) => warmup(m)));
		} catch (e) {
			logger.debug("[warmup] tracking dependencies for %s failed with: %s", url, e);
		}
	};
	await Promise.all(entries.map((entry) => warmup(fileToUrl(entry, server.config.root))));
}
//#endregion
//#region src/css.ts
function sortPlugins({ plugins, order }) {
	const names = Object.keys(plugins);
	return typeof order === "function" ? order(names) : order || names;
}
async function resolveCSSOptions(nuxt) {
	const css = { postcss: { plugins: [] } };
	const postcssOptions = nuxt.options.postcss;
	const jiti = createJiti(nuxt.options.rootDir, { alias: nuxt.options.alias });
	for (const pluginName of sortPlugins(postcssOptions)) {
		const pluginOptions = postcssOptions.plugins[pluginName];
		if (!pluginOptions) continue;
		let pluginFn;
		for (const parentURL of nuxt.options.modulesDir) {
			pluginFn = await jiti.import(pluginName, {
				parentURL: parentURL.replace(/\/node_modules\/?$/, ""),
				try: true,
				default: true
			});
			if (typeof pluginFn === "function") {
				css.postcss.plugins.push(pluginFn(pluginOptions));
				break;
			}
		}
		if (typeof pluginFn !== "function") console.warn(`[nuxt] could not import postcss plugin \`${pluginName}\`. Please report this as a bug.`);
	}
	return css;
}
//#endregion
//#region src/plugins/ssr-styles.ts
const SUPPORTED_FILES_RE = /\.(?:vue|(?:[cm]?j|t)sx?)$/;
const QUERY_RE = /\?.+$/;
const MACRO_QUERY_RE = /[?&]macro(?:=|&|$)/;
const NUXT_COMPONENT_QUERY_RE = /[?&]nuxt_component=/;
const STYLE_QUERY_RE = /[?&]type=style/;
function SSRStylesPlugin(nuxt) {
	if (nuxt.options.dev) return;
	const chunksWithInlinedCSS = /* @__PURE__ */ new Set();
	const clientCSSMap = {};
	const nitro = useNitro();
	nuxt.hook("build:manifest", (manifest) => {
		const entryIds = /* @__PURE__ */ new Set();
		for (const id of chunksWithInlinedCSS) {
			const chunk = manifest[id];
			if (!chunk) continue;
			if (chunk.isEntry && chunk.src) entryIds.add(chunk.src);
			else chunk.css &&= [];
			if (chunk.imports && chunk.src) {
				const componentBaseName = filename(chunk.src);
				for (const imp of chunk.imports) {
					const imported = manifest[imp];
					if (imported?.css?.length && !imported.isEntry && !imported.src) {
						if (imported.css.every((css) => css.startsWith(componentBaseName + "."))) imported.css = [];
					}
				}
			}
		}
		nitro.options.virtual["#internal/nuxt/entry-ids.mjs"] = () => `export default ${JSON.stringify(Array.from(entryIds))}`;
		nitro.options._config.virtual ||= {};
		nitro.options._config.virtual["#internal/nuxt/entry-ids.mjs"] = nitro.options.virtual["#internal/nuxt/entry-ids.mjs"];
	});
	const cssMap = {};
	const emittedFileRefs = {};
	const options = {
		shouldInline: nuxt.options.features.inlineStyles,
		globalCSS: nuxt.options.css
	};
	const relativeCache = /* @__PURE__ */ new Map();
	const relativeToSrcDir = (path) => {
		let cached = relativeCache.get(path);
		if (cached === void 0) {
			cached = relative(nuxt.options.srcDir, path);
			relativeCache.set(path, cached);
		}
		return cached;
	};
	const warnCache = /* @__PURE__ */ new Set();
	const components = nuxt.apps.default.components || [];
	const islands = components.filter((component) => component.island || component.mode === "server" && !components.some((c) => c.pascalName === component.pascalName && c.mode === "client"));
	const islandPaths = new Set(islands.map((c) => c.filePath));
	let entry;
	return {
		name: "ssr-styles",
		configResolved(config) {
			if (!config.build.ssr || nuxt.options.experimental.viteEnvironmentApi) entry = resolveClientEntry(config);
		},
		applyToEnvironment(environment) {
			return {
				name: `nuxt:ssr-styles:${environment.name}`,
				enforce: "pre",
				resolveId: {
					order: "pre",
					filter: { id: { include: [
						/^#build\/css$/,
						/\.vue$/,
						IS_CSS_RE
					] } },
					async handler(id, importer, _options) {
						if (options.shouldInline === false || typeof options.shouldInline === "function" && !options.shouldInline(importer)) return;
						const res = await this.resolve(id, importer, {
							..._options,
							skipSelf: true
						});
						if (res) return {
							...res,
							moduleSideEffects: false
						};
					}
				},
				generateBundle(outputOptions) {
					if (environment.name === "client") return;
					const emitted = {};
					for (const [file, { files, inBundle }] of Object.entries(cssMap)) {
						if (!files.length || !inBundle) continue;
						const fileName = filename$1(file);
						const baseDir = dirname(typeof outputOptions.assetFileNames === "string" ? outputOptions.assetFileNames : outputOptions.assetFileNames({
							type: "asset",
							name: `${fileName}-styles.mjs`,
							names: [`${fileName}-styles.mjs`],
							originalFileName: `${fileName}-styles.mjs`,
							originalFileNames: [`${fileName}-styles.mjs`],
							source: ""
						}));
						const cssImports = /* @__PURE__ */ new Set();
						const exportNames = /* @__PURE__ */ new Set();
						const importStatements = /* @__PURE__ */ new Set();
						let i = 0;
						for (const css of files) {
							const file = this.getFileName(css);
							if (cssImports.has(file)) continue;
							cssImports.add(file);
							const name = `style_${i++}`;
							importStatements.add(genImport(`./${relative(baseDir, file)}`, name));
							exportNames.add(name);
						}
						emitted[file] = this.emitFile({
							type: "asset",
							name: `${fileName}-styles.mjs`,
							source: [...importStatements, `export default ${genArrayFromRaw([...exportNames])}`].join("\n")
						});
					}
					for (const key in emitted) chunksWithInlinedCSS.add(key);
					this.emitFile({
						type: "asset",
						fileName: "styles.mjs",
						originalFileName: "styles.mjs",
						source: ["const interopDefault = r => r.default || r || []", `export default ${genObjectFromRawEntries(Object.entries(emitted).map(([key, value]) => [key, `() => import('./${this.getFileName(value)}').then(interopDefault)`]))}`].join("\n")
					});
				},
				renderChunk(_code, chunk) {
					const isEntry = chunk.facadeModuleId === entry;
					if (isEntry) clientCSSMap[chunk.facadeModuleId] ||= /* @__PURE__ */ new Set();
					for (const moduleId of [chunk.facadeModuleId, ...chunk.moduleIds].filter(Boolean)) {
						if (environment.name === "client") {
							const moduleMap = clientCSSMap[moduleId] ||= /* @__PURE__ */ new Set();
							if (isCSS(moduleId)) {
								if (isVue(moduleId)) {
									moduleMap.add(moduleId);
									const parent = moduleId.replace(/\?.+$/, "");
									(clientCSSMap[parent] ||= /* @__PURE__ */ new Set()).add(moduleId);
								}
								if (isEntry && chunk.facadeModuleId) (clientCSSMap[chunk.facadeModuleId] ||= /* @__PURE__ */ new Set()).add(moduleId);
							}
							continue;
						}
						const relativePath = relativeToSrcDir(moduleId);
						if (relativePath in cssMap) cssMap[relativePath].inBundle = cssMap[relativePath].inBundle ?? (isVue(moduleId) && !!relativePath || isEntry);
					}
					return null;
				},
				transform: {
					filter: { id: {
						include: environment.name === "client" ? new RegExp("^" + escapeStringRegexp(entry) + "$") : void 0,
						exclude: environment.name === "client" ? [] : [/\?.*macro=/, /\?.*nuxt_component=/]
					} },
					async handler(code, id) {
						if (environment.name === "client") {
							if (id === entry && (options.shouldInline === true || typeof options.shouldInline === "function" && options.shouldInline(id))) {
								const idClientCSSMap = clientCSSMap[id] ||= /* @__PURE__ */ new Set();
								if (!options.globalCSS.length) return;
								const s = new MagicString(code);
								for (const file of options.globalCSS) {
									const resolved = await this.resolve(file) ?? await this.resolve(file, id);
									const res = await this.resolve(file + "?inline&used") ?? await this.resolve(file + "?inline&used", id);
									if (!resolved || !res) {
										if (!warnCache.has(file)) {
											warnCache.add(file);
											this.warn(`[nuxt] Cannot extract styles for \`${file}\`. Its styles will not be inlined when server-rendering.`);
										}
										s.prepend(`${genImport(file)}\n`);
										continue;
									}
									idClientCSSMap.add(resolved.id);
								}
								if (s.hasChanged()) return {
									code: s.toString(),
									map: s.generateMap({ hires: true })
								};
							}
							return;
						}
						const { pathname, search } = parseModuleId(id);
						if (!(id in clientCSSMap) && !islandPaths.has(pathname)) return;
						if (MACRO_QUERY_RE.test(search) || NUXT_COMPONENT_QUERY_RE.test(search)) return;
						if (!islandPaths.has(pathname)) {
							if (options.shouldInline === false || typeof options.shouldInline === "function" && !options.shouldInline(id)) return;
						}
						const relativeId = relativeToSrcDir(id);
						const idMap = cssMap[relativeId] ||= { files: [] };
						const emittedIds = /* @__PURE__ */ new Set();
						const idFilename = filename$1(id);
						let styleCtr = 0;
						const ids = clientCSSMap[id] || [];
						for (const file of ids) {
							if (emittedIds.has(file)) continue;
							const fileInline = file + "?inline&used";
							const resolved = await this.resolve(file) ?? await this.resolve(file, id);
							const res = await this.resolve(fileInline) ?? await this.resolve(fileInline, id);
							if (!resolved || !res) {
								if (!warnCache.has(file)) {
									warnCache.add(file);
									this.warn(`[nuxt] Cannot extract styles for \`${file}\`. Its styles will not be inlined when server-rendering.`);
								}
								continue;
							}
							emittedIds.add(file);
							const resolvedInlineId = res.id;
							let ref = emittedFileRefs[resolvedInlineId];
							if (!ref) {
								ref = this.emitFile({
									type: "chunk",
									name: `${idFilename}-styles-${++styleCtr}.mjs`,
									id: fileInline
								});
								emittedFileRefs[resolvedInlineId] = ref;
							}
							idMap.files.push(ref);
						}
						if (!SUPPORTED_FILES_RE.test(pathname)) return;
						for (const i of findStaticImports(code)) {
							if (!i.specifier.endsWith(".css") && !STYLE_QUERY_RE.test(i.specifier)) continue;
							const resolved = await this.resolve(i.specifier, id);
							if (!resolved) continue;
							const resolvedIdInline = resolved.id + "?inline&used";
							const res = await this.resolve(resolvedIdInline);
							if (!res) {
								if (!warnCache.has(resolved.id)) {
									warnCache.add(resolved.id);
									this.warn(`[nuxt] Cannot extract styles for \`${i.specifier}\`. Its styles will not be inlined when server-rendering.`);
								}
								continue;
							}
							if (emittedIds.has(resolved.id)) continue;
							const resolvedInlineId = res.id;
							let ref = emittedFileRefs[resolvedInlineId];
							if (!ref) {
								ref = this.emitFile({
									type: "chunk",
									name: `${idFilename}-styles-${++styleCtr}.mjs`,
									id: resolvedIdInline
								});
								emittedFileRefs[resolvedInlineId] = ref;
							}
							idMap.files.push(ref);
						}
					}
				}
			};
		}
	};
}
function filename$1(name) {
	return filename(name.replace(QUERY_RE, ""));
}
//#endregion
//#region src/plugins/replace.ts
function ReplacePlugin() {
	return {
		name: "nuxt:replace",
		enforce: "post",
		async applyToEnvironment(environment) {
			const config = environment.getTopLevelConfig();
			const replaceOptions = Object.create(null);
			for (const define of [config.define || {}, environment.config.define || {}]) for (const key in define) if (key.startsWith("import.meta.")) replaceOptions[key] = define[key];
			if (config.isProduction && vite.rolldownVersion) {
				const { replacePlugin } = await import("rolldown/plugins");
				return replacePlugin(replaceOptions, { preventAssignment: true });
			} else return replacePlugin({
				...replaceOptions,
				preventAssignment: true
			});
		}
	};
}
//#endregion
//#region src/plugins/layer-dep-optimize.ts
function LayerDepOptimizePlugin(nuxt) {
	if (!nuxt.options.dev) return;
	const layerDirs = [];
	const delimitedRootDir = nuxt.options.rootDir + "/";
	for (const dirs of getLayerDirectories(nuxt)) if (dirs.app !== nuxt.options.srcDir && !dirs.app.startsWith(delimitedRootDir)) layerDirs.push(dirs.app);
	if (layerDirs.length > 0) {
		layerDirs.sort().reverse();
		const dirs = [...layerDirs];
		return {
			name: "nuxt:optimize-layer-deps",
			enforce: "pre",
			resolveId: { async handler(source, _importer) {
				if (!_importer) return;
				const importer = normalize(_importer);
				const layerIndex = dirs.findIndex((dir) => importer.startsWith(dir));
				if (layerIndex !== -1) {
					dirs.splice(layerIndex, 1);
					await this.resolve(source, join(nuxt.options.srcDir, "index.html"), { skipSelf: true }).catch(() => null);
				}
			} }
		};
	}
}
//#endregion
//#region src/dirs.ts
let _distDir = dirname(fileURLToPath(import.meta.url));
if (/(?:chunks|shared)$/.test(_distDir)) _distDir = dirname(_distDir);
const distDir = _distDir;
//#endregion
//#region src/plugins/decorators.ts
const BABEL_DECORATOR_DEPS = ["@babel/plugin-proposal-decorators", "@babel/plugin-syntax-jsx"];
async function ensureBabelDecoratorDeps(nuxt) {
	for (const pkg of BABEL_DECORATOR_DEPS) try {
		await import(pkg);
	} catch (_err) {
		const err = _err;
		if (err.code !== "ERR_MODULE_NOT_FOUND" && err.code !== "MODULE_NOT_FOUND") throw err;
		if (!isCI && hasTTY) {
			logger.info("Decorator support requires additional dependencies.");
			if (await logger.prompt(`Install \`${BABEL_DECORATOR_DEPS.join("` and `")}\`?`, {
				type: "confirm",
				initial: true
			})) {
				logger.start(`Installing ${BABEL_DECORATOR_DEPS.map((d) => `\`${d}\``).join(" and ")}...`);
				await addDependency(BABEL_DECORATOR_DEPS, {
					dev: true,
					cwd: nuxt.options.rootDir,
					silent: true
				});
				logger.info("Rerun Nuxt to enable decorator support.");
				process.exit(1);
			}
		}
		logger.warn(`Cannot find \`${pkg}\`. Install \`${BABEL_DECORATOR_DEPS.join("` and `")}\` to enable decorator support.`);
		return false;
	}
	return true;
}
function DecoratorsPlugin(nuxt) {
	let transformSync;
	return {
		name: "nuxt:decorators",
		apply: () => !!nuxt.options.experimental.decorators,
		async applyToEnvironment() {
			if (!await ensureBabelDecoratorDeps(nuxt)) return false;
			transformSync = await import("./_chunks/lib.mjs").then((m) => /* @__PURE__ */ __toESM(m.default, 1)).then((r) => r.transformSync);
			return true;
		},
		transform: {
			filter: {
				code: "@",
				id: { exclude: [/\.vue\?.*\btype=(?:style|template)\b/] }
			},
			handler(code, id) {
				if (id.includes(".vue") && code.trimStart().startsWith("<")) return;
				const result = transformSync(code, {
					filename: id,
					configFile: false,
					plugins: ["@babel/plugin-syntax-jsx", ["@babel/plugin-proposal-decorators", { version: "2023-11" }]],
					sourceMaps: true
				});
				if (result?.code != null) return {
					code: result.code,
					map: result.map
				};
			}
		}
	};
}
//#endregion
//#region src/plugins/environments.ts
function EnvironmentsPlugin(nuxt) {
	const fileNames = withoutLeadingSlash(join(nuxt.options.app.buildAssetsDir, "[hash].js"));
	const clientOutputDir = join(useNitro().options.output.publicDir, nuxt.options.app.buildAssetsDir);
	const clientAliases = {
		"nitro/runtime": join(nuxt.options.buildDir, "nitro.client.mjs"),
		"#internal/nitro": join(nuxt.options.buildDir, "nitro.client.mjs"),
		"nitropack/runtime": join(nuxt.options.buildDir, "nitro.client.mjs"),
		"#app-manifest": resolveModulePath("mocked-exports/empty", { from: import.meta.url })
	};
	let viteConfig;
	return {
		name: "nuxt:environments",
		enforce: "pre",
		config(config) {
			viteConfig = config;
			if (!nuxt.options.dev) return { base: "./" };
		},
		configEnvironment(name, config) {
			if (!nuxt.options.experimental.viteEnvironmentApi && viteConfig.ssr) {
				config.optimizeDeps ||= {};
				config.optimizeDeps.include = void 0;
			}
			if (name === "client") {
				const outputConfig = config.build?.rollupOptions?.output;
				return { build: { rollupOptions: { output: {
					chunkFileNames: outputConfig?.chunkFileNames ?? (nuxt.options.dev ? void 0 : fileNames),
					entryFileNames: outputConfig?.entryFileNames ?? (nuxt.options.dev ? "entry.js" : fileNames),
					sourcemapPathTransform: outputConfig?.sourcemapPathTransform ?? ((relativeSourcePath, sourcemapPath) => {
						if (!isAbsolute(relativeSourcePath)) return relative(clientOutputDir, resolve(dirname(sourcemapPath), relativeSourcePath));
						return relativeSourcePath;
					})
				} } } };
			}
			if (name === "ssr") {
				if (config.build?.rollupOptions?.output && !Array.isArray(config.build.rollupOptions.output)) {
					config.build.rollupOptions.output.manualChunks = void 0;
					if (vite.rolldownVersion) config.build.rollupOptions.output.advancedChunks = void 0;
				}
			}
		},
		applyToEnvironment(environment) {
			if (environment.name === "client") return [...nuxt.options.experimental.clientNodeCompat ? [NodeCompatAliasPlugin()] : [], {
				name: "nuxt:client:aliases",
				enforce: "post",
				resolveId: {
					filter: { id: Object.keys(clientAliases).map((id) => new RegExp("^" + escapeStringRegexp(id) + "$")) },
					handler: (source) => clientAliases[source]
				}
			}];
			else if (environment.name === "ssr") {}
			return false;
		}
	};
}
function NodeCompatAliasPlugin() {
	const nodeCompatAlias = defineEnv({
		nodeCompat: true,
		resolve: true
	}).env.alias;
	return {
		name: "nuxt:client:node-compat-aliases",
		resolveId: {
			order: "pre",
			handler(source) {
				if (source in nodeCompatAlias) return nodeCompatAlias[source];
			}
		}
	};
}
//#endregion
//#region src/plugins/client-manifest.ts
function ClientManifestPlugin(nuxt) {
	let clientEntry;
	let key;
	let disableCssCodeSplit;
	return {
		name: "nuxt:client-manifest",
		applyToEnvironment: (environment) => environment.name === "ssr",
		configResolved(config) {
			clientEntry = resolveClientEntry(config);
			key = relative(config.root, clientEntry);
			disableCssCodeSplit = config.build?.cssCodeSplit === false;
		},
		async closeBundle() {
			const devClientManifest = {
				"@vite/client": {
					isEntry: true,
					file: "@vite/client",
					css: [],
					module: true,
					resourceType: "script"
				},
				...nuxt.options.features.noScripts === "all" ? {} : { [clientEntry]: {
					isEntry: true,
					file: clientEntry,
					module: true,
					resourceType: "script"
				} }
			};
			const clientDist = resolve(nuxt.options.buildDir, "dist/client");
			const serverDist = resolve(nuxt.options.buildDir, "dist/server");
			const manifestFile = resolve(clientDist, "manifest.json");
			const clientManifest = nuxt.options.dev ? devClientManifest : JSON.parse(readFileSync(manifestFile, "utf-8"));
			const manifestEntries = Object.values(clientManifest);
			const buildAssetsDir = withTrailingSlash(withoutLeadingSlash(nuxt.options.app.buildAssetsDir));
			const BASE_RE = new RegExp(`^${escapeStringRegexp(buildAssetsDir)}`);
			for (const entry of manifestEntries) {
				entry.file &&= entry.file.replace(BASE_RE, "");
				for (const item of ["css", "assets"]) entry[item] &&= entry[item].map((i) => i.replace(BASE_RE, ""));
			}
			await mkdir(serverDist, { recursive: true });
			if (disableCssCodeSplit) {
				for (const entry of manifestEntries) if (entry.file?.endsWith(".css")) {
					clientManifest[key].css ||= [];
					clientManifest[key].css.push(entry.file);
					break;
				}
			}
			const manifest = normalizeViteManifest(clientManifest);
			await nuxt.callHook("build:manifest", manifest);
			const precomputed = precomputeDependencies(manifest);
			await writeFile(resolve(serverDist, "client.manifest.mjs"), "export default " + serialize(manifest), "utf8");
			await writeFile(resolve(serverDist, "client.precomputed.mjs"), "export default " + serialize(precomputed), "utf8");
			if (!nuxt.options.dev) await rm(manifestFile, { force: true });
		}
	};
}
//#endregion
//#region src/plugins/resolve-deep-imports.ts
const VIRTUAL_RE = /^\0?virtual:(?:nuxt:)?/;
function ResolveDeepImportsPlugin(nuxt) {
	const exclude = [
		"virtual:",
		"\0virtual:",
		"/__skip_vite",
		"@vitest/"
	];
	const conditions = {};
	function resolveConditions(environment) {
		const resolvedConditions = new Set([nuxt.options.dev ? "development" : "production", ...environment.config.resolve.conditions]);
		if (resolvedConditions.has("browser")) {
			resolvedConditions.add("web");
			resolvedConditions.add("import");
			resolvedConditions.add("module");
			resolvedConditions.add("default");
		}
		if (environment.config.mode === "test") {
			resolvedConditions.add("import");
			resolvedConditions.add("require");
		}
		return [...resolvedConditions];
	}
	return {
		name: "nuxt:resolve-bare-imports",
		enforce: "post",
		resolveId: {
			filter: { id: { exclude: [/^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[A-Z]:[/\\]/i, ...exclude.map((e) => new RegExp("^" + escapeStringRegexp(e)))] } },
			async handler(id, importer) {
				if (!importer || !isAbsolute(importer) && !VIRTUAL_RE.test(importer)) return;
				const normalisedId = resolveAlias(normalize(id), nuxt.options.alias);
				const isNuxtTemplate = importer.startsWith("virtual:nuxt");
				const normalisedImporter = (isNuxtTemplate ? decodeURIComponent(importer) : importer).replace(VIRTUAL_RE, "");
				if (nuxt.options.experimental.templateImportResolution !== false && isNuxtTemplate) {
					const template = nuxt.options.build.templates.find((t) => resolve(nuxt.options.buildDir, t.filename) === normalisedImporter);
					if (template?._path) {
						const res = await this.resolve?.(normalisedId, template._path, { skipSelf: true });
						if (res !== void 0 && res !== null) return res;
					}
				}
				const dir = parseNodeModulePath(normalisedImporter).dir || nuxt.options.appDir;
				const res = await this.resolve?.(normalisedId, dir, { skipSelf: true });
				if (res !== void 0 && res !== null) return res;
				const environmentConditions = conditions[this.environment.name] ||= resolveConditions(this.environment);
				const path = resolveModulePath(id, {
					from: [dir, ...nuxt.options.modulesDir].map((d) => directoryToURL(d)),
					suffixes: ["", "index"],
					conditions: environmentConditions,
					try: true
				});
				if (!path) {
					logger.debug("Could not resolve id", id, importer);
					return null;
				}
				return normalize(path);
			}
		}
	};
}
//#endregion
//#region src/plugins/resolved-externals.ts
function ResolveExternalsPlugin(nuxt) {
	let external = /* @__PURE__ */ new Set();
	return {
		name: "nuxt:resolve-externals",
		enforce: "pre",
		config() {
			external = new Set(nuxt["~runtimeDependencies"]);
			return { optimizeDeps: { exclude: Array.from(external) } };
		},
		applyToEnvironment(environment) {
			if (nuxt.options.dev || environment.name !== "ssr") return false;
			return {
				name: "nuxt:resolve-externals:external",
				resolveId: {
					filter: { id: [...external].map((dep) => new RegExp("^" + escapeStringRegexp(dep) + "$")) },
					async handler(id, importer) {
						const res = await this.resolve?.(id, importer, { skipSelf: true });
						if (res !== void 0 && res !== null) {
							if (res.id === id) res.id = resolveModulePath(res.id, {
								try: true,
								from: importer,
								extensions: nuxt.options.extensions
							}) || res.id;
							return {
								...res,
								external: "absolute"
							};
						}
					}
				}
			};
		}
	};
}
//#endregion
//#region src/plugins/perf.ts
const HOOKS_TO_TRACK = [
	"transform",
	"resolveId",
	"load"
];
function PerfPlugin(nuxt) {
	return {
		name: "nuxt:perf",
		enforce: "pre",
		apply: () => !!nuxt?._perf,
		configResolved(config) {
			for (const plugin of config.plugins) {
				if (plugin.name === "nuxt:perf") continue;
				const pluginName = plugin.name;
				for (const hookName of HOOKS_TO_TRACK) wrapPluginHook(plugin, pluginName, hookName, nuxt);
			}
		}
	};
}
function wrapPluginHook(plugin, pluginName, hookName, nuxt) {
	const original = plugin[hookName];
	if (!original) return;
	if (typeof original === "function") plugin[hookName] = function(...args) {
		return timedCall(original, this, args, pluginName, hookName, nuxt);
	};
	else if (typeof original === "object" && "handler" in original) {
		const originalHandler = original.handler;
		original.handler = function(...args) {
			return timedCall(originalHandler, this, args, pluginName, hookName, nuxt);
		};
	}
}
function timedCall(fn, ctx, args, pluginName, hookName, nuxt) {
	const start = performance.now();
	const record = () => nuxt._perf?.recordBundlerPluginHook(pluginName, hookName, performance.now() - start, start);
	try {
		const result = fn.apply(ctx, args);
		if (result && typeof result === "object" && "then" in result) return result.finally(record);
		record();
		return result;
	} catch (err) {
		record();
		throw err;
	}
}
//#endregion
//#region src/vite.ts
const bundle = async (nuxt) => {
	const useAsyncEntry = nuxt.options.experimental.asyncEntry || nuxt.options.dev;
	const entry = await resolvePath(resolve(nuxt.options.appDir, useAsyncEntry ? "entry.async" : "entry"));
	nuxt.options.modulesDir.push(distDir);
	if (nuxt.options.dev) {
		const nitro = useNitro();
		nitro.options.virtual["#internal/nitro/ssr-stacktrace"] = `export { default } from ${JSON.stringify(resolve(distDir, "fix-stacktrace"))}`;
		nitro.options.plugins.push("#internal/nitro/ssr-stacktrace");
		nitro.options.alias["#vite-node"] = resolve(distDir, "vite-node");
		nitro.options.virtual["#internal/nuxt/vite-node-runner"] = () => `export { default } from ${JSON.stringify(resolve(distDir, "vite-node-runner"))}`;
	}
	let allowDirs = [
		nuxt.options.appDir,
		nuxt.options.workspaceDir,
		...nuxt.options.modulesDir,
		...getLayerDirectories(nuxt).map((d) => d.root),
		...Object.values(nuxt.apps).flatMap((app) => [
			...app.components.map((c) => dirname(c.filePath)),
			...app.plugins.map((p) => dirname(p.src)),
			...app.middleware.map((m) => dirname(m.path)),
			...Object.values(app.layouts || {}).map((l) => dirname(l.file)),
			dirname(nuxt.apps.default.rootComponent),
			dirname(nuxt.apps.default.errorComponent)
		])
	].filter((d) => d && existsSync(d));
	for (const dir of allowDirs) allowDirs = allowDirs.filter((d) => !d.startsWith(dir) || d === dir);
	const { $client, $server, ...viteConfig } = nuxt.options.vite;
	if (vite.rolldownVersion) {
		if (viteConfig.esbuild) delete viteConfig.esbuild;
		if (viteConfig.optimizeDeps?.esbuildOptions) delete viteConfig.optimizeDeps.esbuildOptions;
	}
	const mockEmpty = resolveModulePath("mocked-exports/empty", { from: import.meta.url });
	const helper = nuxt.options.nitro.imports !== false ? "" : "globalThis.";
	const isIgnored = createIsIgnored(nuxt);
	const serverEntry = nuxt.options.ssr ? entry : await resolvePath(resolve(nuxt.options.appDir, "entry-spa"));
	const config = mergeConfig({
		base: nuxt.options.dev ? joinURL(nuxt.options.app.baseURL.replace(/^\.\//, "/") || "/", nuxt.options.app.buildAssetsDir) : void 0,
		logLevel: logLevelMap[nuxt.options.logLevel] ?? logLevelMap.info,
		experimental: { renderBuiltUrl: (filename, { type, hostType, ssr }) => {
			if (hostType !== "js") return { relative: true };
			if (!ssr) {
				if (type === "asset") return { relative: true };
				return { runtime: `globalThis.__publicAssetsURL(${JSON.stringify(filename)})` };
			}
			if (type === "public") return { runtime: `${helper}__publicAssetsURL(${JSON.stringify(filename)})` };
			if (type === "asset") {
				const relativeFilename = filename.replace(withTrailingSlash(withoutLeadingSlash(nuxt.options.app.buildAssetsDir)), "");
				return { runtime: `${helper}__buildAssetsURL(${JSON.stringify(relativeFilename)})` };
			}
		} },
		...nuxt.options.experimental.viteEnvironmentApi ? {
			builder: { async buildApp(builder) {
				const environments = Object.values(builder.environments);
				for (const environment of environments) {
					logger.restoreAll();
					nuxt._perf?.startPhase(`vite:${environment.name}`);
					await builder.build(environment);
					nuxt._perf?.endPhase(`vite:${environment.name}`);
					logger.wrapAll();
					await nuxt.callHook("vite:compiled");
				}
			} },
			environments: {
				client: {
					consumer: "client",
					keepProcessEnv: false,
					dev: { warmup: [entry] },
					...clientEnvironment(nuxt, entry)
				},
				ssr: {
					consumer: "server",
					dev: { warmup: [serverEntry] },
					...ssrEnvironment(nuxt, serverEntry)
				}
			},
			ssr: ssr(nuxt)
		} : {},
		resolve: {
			alias: {
				[basename(nuxt.options.dir.assets)]: resolve(nuxt.options.srcDir, nuxt.options.dir.assets),
				...nuxt.options.alias,
				"#app": nuxt.options.appDir,
				"web-streams-polyfill/ponyfill/es2018": mockEmpty,
				"abort-controller": mockEmpty
			},
			dedupe: ["vue"]
		},
		css: await resolveCSSOptions(nuxt),
		define: {
			__NUXT_VERSION__: JSON.stringify(nuxt._version),
			__NUXT_ASYNC_CONTEXT__: nuxt.options.experimental.asyncContext
		},
		build: {
			copyPublicDir: false,
			rollupOptions: { output: {
				sourcemapIgnoreList: (relativeSourcePath) => {
					return relativeSourcePath.includes("node_modules") || relativeSourcePath.includes(nuxt.options.buildDir);
				},
				sanitizeFileName: sanitizeFilePath,
				assetFileNames: nuxt.options.dev ? void 0 : (chunk) => withoutLeadingSlash(join(nuxt.options.app.buildAssetsDir, `${sanitizeFilePath(filename(chunk.names[0]))}.[hash].[ext]`))
			} },
			watch: vite.rolldownVersion ? { exclude: [...nuxt.options.ignore, /[\\/]node_modules[\\/]/] } : {
				chokidar: {
					...nuxt.options.watchers.chokidar,
					ignored: [isIgnored, /[\\/]node_modules[\\/]/]
				},
				exclude: nuxt.options.ignore
			}
		},
		plugins: [
			PerfPlugin(nuxt),
			ResolveDeepImportsPlugin(nuxt),
			ResolveExternalsPlugin(nuxt),
			...nuxt.options.experimental.viteEnvironmentApi ? [
				vuePlugin(viteConfig.vue),
				viteJsxPlugin(viteConfig.vueJsx),
				ViteNodePlugin(nuxt),
				ClientManifestPlugin(nuxt),
				DevServerPlugin(nuxt)
			] : [],
			DecoratorsPlugin(nuxt),
			PublicDirsPlugin({
				dev: nuxt.options.dev,
				baseURL: nuxt.options.app.baseURL
			}),
			ReplacePlugin(),
			LayerDepOptimizePlugin(nuxt),
			SSRStylesPlugin(nuxt),
			EnvironmentsPlugin(nuxt),
			...nuxt.options.experimental.viteEnvironmentApi ? [
				VitePluginCheckerPlugin(nuxt),
				SourcemapPreserverPlugin(nuxt),
				DevStyleSSRPlugin({
					srcDir: nuxt.options.srcDir,
					buildAssetsURL: joinURL(nuxt.options.app.baseURL, nuxt.options.app.buildAssetsDir)
				}),
				RuntimePathsPlugin(),
				TypeCheckPlugin(nuxt),
				ModulePreloadPolyfillPlugin(),
				StableEntryPlugin(nuxt),
				AnalyzePlugin(nuxt),
				OptimizeDepsHintPlugin(nuxt)
			] : []
		],
		appType: "custom",
		server: {
			middlewareMode: true,
			watch: {
				...nuxt.options.watchers.chokidar,
				ignored: [isIgnored, /[\\/]node_modules[\\/]/]
			},
			fs: { allow: [...new Set(allowDirs)] }
		}
	}, nuxt.options.experimental.viteEnvironmentApi ? {
		...viteConfig,
		environments: {
			ssr: $server,
			client: $client
		}
	} : viteConfig);
	if (!nuxt.options.dev) {
		config.server.watch = void 0;
		config.build.watch = void 0;
	}
	userOptimizeDepsInclude.set(nuxt, [...config.optimizeDeps?.include || []]);
	const ctx = {
		nuxt,
		entry,
		config
	};
	await nuxt.callHook("vite:extend", ctx);
	if (nuxt.options.experimental.viteEnvironmentApi) await handleEnvironments(nuxt, config);
	else await handleSerialBuilds(nuxt, ctx);
};
async function handleEnvironments(nuxt, config) {
	const callbacks = optimizerCallbacks.get(nuxt);
	config.customLogger = createViteLogger(config, {
		onNewDeps: callbacks?.onNewDeps,
		onStaleDep: callbacks?.onStaleDep
	});
	config.configFile = false;
	for (const environment of ["client", "ssr"]) {
		const environments = { [environment]: config.environments[environment] };
		const strippedConfig = {
			...config,
			environments
		};
		const ctx = {
			isServer: environment === "ssr",
			isClient: environment === "client"
		};
		await nuxt.hooks.callHook("vite:extendConfig", strippedConfig, ctx);
		await nuxt.hooks.callHook("vite:configResolved", strippedConfig, ctx);
	}
	if (!nuxt.options.dev) {
		await (await createBuilder(config)).buildApp();
		return;
	}
	nuxt._perf?.startPhase("vite:dev-server");
	await withLogs(async () => {
		await (await createServer(config)).environments.ssr.pluginContainer.buildStart({});
	}, "Vite dev server built");
	nuxt._perf?.endPhase("vite:dev-server");
	await writeDevServer(nuxt);
}
async function handleSerialBuilds(nuxt, ctx) {
	nuxt.hook("vite:serverCreated", (server, env) => {
		if (nuxt.options.vite.warmupEntry !== false) useNitro().hooks.hookOnce("compiled", () => {
			const start = Date.now();
			warmupViteServer(server, [ctx.entry], env.isServer).then(() => logger.info(`Vite ${env.isClient ? "client" : "server"} warmed up in ${Date.now() - start}ms`)).catch(logger.error);
		});
	});
	nuxt._perf?.startPhase(`vite:client`);
	await withLogs(() => buildClient(nuxt, ctx), "Vite client built", nuxt.options.dev);
	nuxt._perf?.endPhase(`vite:client`);
	nuxt._perf?.startPhase(`vite:server`);
	await withLogs(() => buildServer(nuxt, ctx), "Vite server built", nuxt.options.dev);
	nuxt._perf?.endPhase(`vite:server`);
}
async function withLogs(fn, message, enabled = true) {
	if (!enabled) return fn();
	const start = performance.now();
	await fn();
	const duration = performance.now() - start;
	logger.success(`${message} in ${Math.round(duration)}ms`);
}
//#endregion
export { bundle };

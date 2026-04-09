import { pathToFileURL } from "node:url";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import * as nodeHTTP$1 from "node:http";
import { EventEmitter } from "node:events";
//#region src/loader.ts
const defaultExts = [
	".mjs",
	".js",
	".mts",
	".ts"
];
const defaultEntries = [
	"server",
	"server/index",
	"src/server",
	"server/server"
];
async function loadServerEntry(opts) {
	let entry = opts.entry;
	if (entry) {
		entry = resolve(opts.dir || ".", entry);
		if (!existsSync(entry)) return { notFound: true };
	} else {
		for (const defEntry of defaultEntries) {
			for (const defExt of defaultExts) {
				const entryPath = resolve(opts.dir || ".", `${defEntry}${defExt}`);
				if (existsSync(entryPath)) {
					entry = entryPath;
					break;
				}
			}
			if (entry) break;
		}
		if (!entry) return { notFound: true };
	}
	const url = entry.startsWith("file://") ? entry : pathToFileURL(resolve(entry)).href;
	let mod;
	let interceptedNodeHandler;
	let interceptedServer;
	try {
		if (opts.interceptHttpListen !== false) {
			const loaded = await interceptListen(() => import(url), opts);
			mod = loaded.res;
			interceptedNodeHandler = loaded.listenHandler;
			interceptedServer = loaded.server;
		} else mod = await import(url);
	} catch (error) {
		if (error?.code === "ERR_UNKNOWN_FILE_EXTENSION") {
			const message = String(error);
			if (/"\.(m|c)?ts"/g.test(message)) throw new Error(`Make sure you're using Node.js v22.18+ or v24+ for TypeScript support (current version: ${process.versions.node})`, { cause: error });
			else if (/"\.(m|c)?tsx"/g.test(message)) throw new Error(`You need a compatible loader for JSX support (Deno, Bun or srvx --register jiti/register)`, { cause: error });
		}
		throw error;
	}
	mod = await opts?.onLoad?.(mod) || mod;
	let fetchHandler = mod?.fetch || mod?.default?.fetch || mod?.default?.default?.fetch || interceptedServer?.fetch;
	if (!fetchHandler && typeof mod?.default === "function" && mod.default.length < 2) fetchHandler = mod.default;
	let nodeCompat = false;
	if (!fetchHandler && opts.nodeCompat !== false) {
		const nodeHandler = interceptedNodeHandler || (typeof mod?.default === "function" ? mod.default : void 0);
		if (nodeHandler) {
			nodeCompat = true;
			const { fetchNodeHandler } = await import("srvx/node");
			fetchHandler = (webReq) => fetchNodeHandler(nodeHandler, webReq);
		}
	}
	return {
		module: mod,
		nodeCompat,
		url,
		fetch: fetchHandler,
		srvxServer: interceptedServer
	};
}
let _interceptQueue = Promise.resolve();
async function interceptListen(cb, opts = {}) {
	const result = _interceptQueue.then(async () => {
		const originalListen = nodeHTTP$1.Server.prototype.listen;
		let res;
		let listenHandler;
		let server;
		const nodeServerStub = opts.nodeServer || opts.srvxServer?.node?.server || new StubNodeServer(() => opts.srvxServer?.node?.server);
		globalThis.__srvxLoader__ = (obj) => {
			server = obj.server;
			if (server && server.node) server.node.server ||= nodeServerStub;
		};
		try {
			nodeHTTP$1.Server.prototype.listen = function(arg1, arg2) {
				listenHandler = this._events.request;
				if (Array.isArray(listenHandler)) listenHandler = listenHandler[0];
				nodeHTTP$1.Server.prototype.listen = originalListen;
				const listenCallback = [arg1, arg2].find((arg) => typeof arg === "function");
				setImmediate(() => {
					listenCallback?.();
				});
				return nodeServerStub;
			};
			res = await cb();
		} finally {
			nodeHTTP$1.Server.prototype.listen = originalListen;
			delete globalThis.__srvxLoader__;
		}
		return {
			res,
			listenHandler,
			server
		};
	});
	_interceptQueue = result.catch(() => {});
	return result;
}
var StubNodeServer = class extends EventEmitter {
	constructor(getServer) {
		super();
		return new Proxy(this, { get(target, prop, receiver) {
			const server = getServer();
			if (!server) return Reflect.get(target, prop, receiver);
			const value = server[prop];
			if (typeof value === "function") return value.bind(server);
			return value;
		} });
	}
	address() {
		return {
			address: "",
			family: "",
			port: 0
		};
	}
	listen() {
		return this;
	}
	close(callback) {
		callback?.();
		return this;
	}
};
//#endregion
export { defaultEntries, defaultExts, loadServerEntry };

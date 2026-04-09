import "../_chunks/_utils.mjs";
import { n as lazyInherit, t as FastURL } from "../_chunks/_url.mjs";
import { a as resolveTLSOptions, i as resolvePortAndHost, n as fmtURL, r as printListening, t as createWaitUntil } from "../_chunks/_utils2.mjs";
import { n as gracefulShutdownPlugin, r as wrapFetch, t as errorPlugin } from "../_chunks/_plugins.mjs";
import nodeHTTP, { IncomingMessage, ServerResponse } from "node:http";
import { Duplex, PassThrough, Readable } from "node:stream";
import { pipeline } from "node:stream/promises";
import nodeHTTPS from "node:https";
import nodeHTTP2 from "node:http2";
//#region src/adapters/_node/send.ts
async function sendNodeResponse(nodeRes, webRes) {
	if (!webRes) {
		nodeRes.statusCode = 500;
		return endNodeResponse(nodeRes);
	}
	if (webRes._toNodeResponse) {
		const res = webRes._toNodeResponse();
		if (res.body) {
			if (res.body instanceof ReadableStream) {
				writeHead(nodeRes, res.status, res.statusText, res.headers);
				return streamBody(res.body, nodeRes);
			} else if (typeof res.body?.pipe === "function") return pipeBody(res.body, nodeRes, res.status, res.statusText, res.headers);
			writeHead(nodeRes, res.status, res.statusText, res.headers);
			nodeRes.write(res.body);
		} else writeHead(nodeRes, res.status, res.statusText, res.headers);
		return endNodeResponse(nodeRes);
	}
	const rawHeaders = [...webRes.headers];
	writeHead(nodeRes, webRes.status, webRes.statusText, rawHeaders);
	return webRes.body ? streamBody(webRes.body, nodeRes) : endNodeResponse(nodeRes);
}
function writeHead(nodeRes, status, statusText, rawHeaders) {
	const writeHeaders = globalThis.Deno ? rawHeaders : rawHeaders.flat();
	if (!nodeRes.headersSent) if (nodeRes.req?.httpVersion === "2.0") nodeRes.writeHead(status, writeHeaders);
	else nodeRes.writeHead(status, statusText, writeHeaders);
}
function endNodeResponse(nodeRes) {
	return new Promise((resolve) => nodeRes.end(resolve));
}
function pipeBody(stream, nodeRes, status, statusText, headers) {
	if (nodeRes.destroyed) {
		stream.destroy?.();
		return;
	}
	if (typeof stream.on !== "function" || typeof stream.destroy !== "function") {
		writeHead(nodeRes, status, statusText, headers);
		stream.pipe(nodeRes);
		return new Promise((resolve) => nodeRes.on("close", resolve));
	}
	if (stream.destroyed) {
		writeHead(nodeRes, 500, "Internal Server Error", []);
		return endNodeResponse(nodeRes);
	}
	return new Promise((resolve) => {
		function onEarlyError() {
			stream.off("readable", onReadable);
			stream.destroy();
			writeHead(nodeRes, 500, "Internal Server Error", []);
			endNodeResponse(nodeRes).then(resolve);
		}
		function onReadable() {
			stream.off("error", onEarlyError);
			if (nodeRes.destroyed) {
				stream.destroy();
				return resolve();
			}
			writeHead(nodeRes, status, statusText, headers);
			pipeline(stream, nodeRes).catch(() => {}).then(() => resolve());
		}
		stream.once("error", onEarlyError);
		stream.once("readable", onReadable);
	});
}
function streamBody(stream, nodeRes) {
	if (nodeRes.destroyed) {
		stream.cancel();
		return;
	}
	const reader = stream.getReader();
	function streamCancel(error) {
		reader.cancel(error).catch(() => {});
		if (error) nodeRes.destroy(error);
	}
	function streamHandle({ done, value }) {
		try {
			if (done) nodeRes.end();
			else if (nodeRes.write(value)) reader.read().then(streamHandle, streamCancel);
			else nodeRes.once("drain", () => reader.read().then(streamHandle, streamCancel));
		} catch (error) {
			streamCancel(error instanceof Error ? error : void 0);
		}
	}
	nodeRes.on("close", streamCancel);
	nodeRes.on("error", streamCancel);
	reader.read().then(streamHandle, streamCancel);
	return reader.closed.catch(streamCancel).finally(() => {
		nodeRes.off("close", streamCancel);
		nodeRes.off("error", streamCancel);
	});
}
//#endregion
//#region src/adapters/_node/url.ts
/**
* Validates an HTTP Host header value (domain, IPv4, or bracketed IPv6) with optional port.
* Intended for preliminary filtering invalid values like "localhost:3000/foobar?"
*/
const HOST_RE = /^(\[(?:[A-Fa-f0-9:.]+)\]|(?:[A-Za-z0-9_-]+\.)*[A-Za-z0-9_-]+|(?:\d{1,3}\.){3}\d{1,3})(:\d{1,5})?$/;
var NodeRequestURL = class extends FastURL {
	#req;
	constructor({ req }) {
		const path = req.url || "/";
		if (path[0] === "/") {
			const qIndex = path.indexOf("?");
			const pathname = qIndex === -1 ? path : path?.slice(0, qIndex) || "/";
			const search = qIndex === -1 ? "" : path?.slice(qIndex) || "";
			let host = req.headers.host || req.headers[":authority"];
			if (host && !HOST_RE.test(host)) host = "_invalid_";
			else if (!host) if (req.socket) host = `${req.socket.localFamily === "IPv6" ? "[" + req.socket.localAddress + "]" : req.socket.localAddress}:${req.socket?.localPort || "80"}`;
			else host = "localhost";
			const protocol = req.socket?.encrypted || req.headers["x-forwarded-proto"] === "https" || req.headers[":scheme"] === "https" ? "https:" : "http:";
			super({
				protocol,
				host,
				pathname,
				search
			});
		} else super(path);
		this.#req = req;
	}
	get pathname() {
		return super.pathname;
	}
	set pathname(value) {
		this._url.pathname = value;
		this.#req.url = this._url.pathname + this._url.search;
	}
};
//#endregion
//#region src/adapters/_node/headers.ts
const NodeRequestHeaders = /* @__PURE__ */ (() => {
	const NativeHeaders = globalThis.Headers;
	class Headers {
		#req;
		#headers;
		constructor(req) {
			this.#req = req;
		}
		static [Symbol.hasInstance](val) {
			return val instanceof NativeHeaders;
		}
		get _headers() {
			if (!this.#headers) {
				const headers = new NativeHeaders();
				const rawHeaders = this.#req.rawHeaders;
				const len = rawHeaders.length;
				for (let i = 0; i < len; i += 2) {
					const key = rawHeaders[i];
					if (key.charCodeAt(0) === 58) continue;
					const value = rawHeaders[i + 1];
					headers.append(key, value);
				}
				this.#headers = headers;
			}
			return this.#headers;
		}
		get(name) {
			if (this.#headers) return this.#headers.get(name);
			const value = this.#req.headers[name.toLowerCase()];
			return Array.isArray(value) ? value.join(", ") : value || null;
		}
		has(name) {
			if (this.#headers) return this.#headers.has(name);
			return name.toLowerCase() in this.#req.headers;
		}
		getSetCookie() {
			if (this.#headers) return this.#headers.getSetCookie();
			const value = this.#req.headers["set-cookie"];
			return Array.isArray(value) ? value : value ? [value] : [];
		}
		entries() {
			return this._headers.entries();
		}
		[Symbol.iterator]() {
			return this.entries();
		}
	}
	lazyInherit(Headers.prototype, NativeHeaders.prototype, "_headers");
	Object.setPrototypeOf(Headers, NativeHeaders);
	Object.setPrototypeOf(Headers.prototype, NativeHeaders.prototype);
	return Headers;
})();
//#endregion
//#region src/adapters/_node/request.ts
const NodeRequest = /* @__PURE__ */ (() => {
	const NativeRequest = globalThis.Request;
	class Request {
		runtime;
		#req;
		#url;
		#bodyStream;
		#request;
		#headers;
		#abortController;
		constructor(ctx) {
			this.#req = ctx.req;
			this.runtime = {
				name: "node",
				node: ctx
			};
		}
		static [Symbol.hasInstance](val) {
			return val instanceof NativeRequest;
		}
		get ip() {
			return this.#req.socket?.remoteAddress;
		}
		get method() {
			if (this.#request) return this.#request.method;
			return this.#req.method || "GET";
		}
		get _url() {
			return this.#url ||= new NodeRequestURL({ req: this.#req });
		}
		set _url(url) {
			this.#url = url;
		}
		get url() {
			if (this.#request) return this.#request.url;
			return this._url.href;
		}
		get headers() {
			if (this.#request) return this.#request.headers;
			return this.#headers ||= new NodeRequestHeaders(this.#req);
		}
		get _abortController() {
			if (!this.#abortController) {
				this.#abortController = new AbortController();
				const { req, res } = this.runtime.node;
				const abortController = this.#abortController;
				const abort = (err) => abortController.abort?.(err);
				if (res) res.once("close", () => {
					const reqError = req.errored;
					if (reqError) abort(reqError);
					else if (!res.writableEnded) abort();
				});
				else req.once("close", () => {
					if (!req.complete) abort();
				});
			}
			return this.#abortController;
		}
		get signal() {
			return this.#request ? this.#request.signal : this._abortController.signal;
		}
		get body() {
			if (this.#request) return this.#request.body;
			if (this.#bodyStream === void 0) {
				const method = this.method;
				this.#bodyStream = !(method === "GET" || method === "HEAD") ? Readable.toWeb(this.#req) : null;
			}
			return this.#bodyStream;
		}
		text() {
			if (this.#request) return this.#request.text();
			if (this.#bodyStream !== void 0) return this.#bodyStream ? new Response(this.#bodyStream).text() : Promise.resolve("");
			return readBody(this.#req).then((buf) => buf.toString());
		}
		json() {
			if (this.#request) return this.#request.json();
			return this.text().then((text) => JSON.parse(text));
		}
		get _request() {
			if (!this.#request) {
				const body = this.body;
				this.#request = new NativeRequest(this.url, {
					method: this.method,
					headers: this.headers,
					signal: this._abortController.signal,
					body,
					duplex: body ? "half" : void 0
				});
				this.#headers = void 0;
				this.#bodyStream = void 0;
			}
			return this.#request;
		}
	}
	lazyInherit(Request.prototype, NativeRequest.prototype, "_request");
	Object.setPrototypeOf(Request.prototype, NativeRequest.prototype);
	return Request;
})();
/**
* Undici uses an incompatible Request constructor depending on private property accessors.
*
* This utility, patches global Request to support `new Request(req)` in Node.js.
*
* Alternatively you can use `new Request(req._request || req)` instead of patching global Request.
*/
function patchGlobalRequest() {
	const NativeRequest = globalThis[Symbol.for("srvx.nativeRequest")] ??= globalThis.Request;
	const PatchedRequest = class Request extends NativeRequest {
		static _srvx = true;
		static [Symbol.hasInstance](instance) {
			if (this === PatchedRequest) return instance instanceof NativeRequest;
			else return Object.prototype.isPrototypeOf.call(this.prototype, instance);
		}
		constructor(input, options) {
			if (typeof input === "object" && "_request" in input) input = input._request;
			super(input, options);
		}
	};
	if (!globalThis.Request._srvx) globalThis.Request = PatchedRequest;
	return PatchedRequest;
}
function readBody(req) {
	if ("rawBody" in req && Buffer.isBuffer(req.rawBody)) return Promise.resolve(req.rawBody);
	return new Promise((resolve, reject) => {
		const chunks = [];
		const onData = (chunk) => {
			chunks.push(chunk);
		};
		const onError = (err) => {
			reject(err);
		};
		const onEnd = () => {
			req.off("error", onError);
			req.off("data", onData);
			resolve(Buffer.concat(chunks));
		};
		req.on("data", onData).once("end", onEnd).once("error", onError);
	});
}
//#endregion
//#region src/adapters/_node/response.ts
/**
* Fast Response for Node.js runtime
*
* It is faster because in most cases it doesn't create a full Response instance.
*/
const NodeResponse = /* @__PURE__ */ (() => {
	const NativeResponse = globalThis.Response;
	const STATUS_CODES = globalThis.process?.getBuiltinModule?.("node:http")?.STATUS_CODES || {};
	class NodeResponse {
		#body;
		#init;
		#headers;
		#response;
		constructor(body, init) {
			this.#body = body;
			this.#init = init;
		}
		static [Symbol.hasInstance](val) {
			return val instanceof NativeResponse;
		}
		get status() {
			return this.#response?.status || this.#init?.status || 200;
		}
		get statusText() {
			return this.#response?.statusText || this.#init?.statusText || STATUS_CODES[this.status] || "";
		}
		get headers() {
			if (this.#response) return this.#response.headers;
			if (this.#headers) return this.#headers;
			const initHeaders = this.#init?.headers;
			return this.#headers = initHeaders instanceof Headers ? initHeaders : new Headers(initHeaders);
		}
		get ok() {
			if (this.#response) return this.#response.ok;
			const status = this.status;
			return status >= 200 && status < 300;
		}
		get _response() {
			if (this.#response) return this.#response;
			let body = this.#body;
			if (body && typeof body.pipe === "function" && !(body instanceof Readable)) {
				const stream = new PassThrough();
				body.pipe(stream);
				const abort = body.abort;
				if (abort) stream.once("close", () => abort());
				body = stream;
			}
			this.#response = new NativeResponse(body, this.#headers ? {
				...this.#init,
				headers: this.#headers
			} : this.#init);
			this.#init = void 0;
			this.#headers = void 0;
			this.#body = void 0;
			return this.#response;
		}
		_toNodeResponse() {
			const status = this.status;
			const statusText = this.statusText;
			let body;
			let contentType;
			let contentLength;
			if (this.#response) body = this.#response.body;
			else if (this.#body) if (this.#body instanceof ReadableStream) body = this.#body;
			else if (typeof this.#body === "string") {
				body = this.#body;
				contentType = "text/plain; charset=UTF-8";
				contentLength = Buffer.byteLength(this.#body);
			} else if (this.#body instanceof ArrayBuffer) {
				body = Buffer.from(this.#body);
				contentLength = this.#body.byteLength;
			} else if (this.#body instanceof Uint8Array) {
				body = this.#body;
				contentLength = this.#body.byteLength;
			} else if (this.#body instanceof DataView) {
				body = Buffer.from(this.#body.buffer);
				contentLength = this.#body.byteLength;
			} else if (this.#body instanceof Blob) {
				body = this.#body.stream();
				contentType = this.#body.type;
				contentLength = this.#body.size;
			} else if (typeof this.#body.pipe === "function") body = this.#body;
			else body = this._response.body;
			const headers = [];
			const initHeaders = this.#init?.headers;
			const headerEntries = this.#response?.headers || this.#headers || (initHeaders ? Array.isArray(initHeaders) ? initHeaders : initHeaders?.entries ? initHeaders.entries() : Object.entries(initHeaders).map(([k, v]) => [k.toLowerCase(), v]) : void 0);
			let hasContentTypeHeader;
			let hasContentLength;
			if (headerEntries) for (const [key, value] of headerEntries) {
				if (Array.isArray(value)) for (const v of value) headers.push([key, v]);
				else headers.push([key, value]);
				if (key === "content-type") hasContentTypeHeader = true;
				else if (key === "content-length") hasContentLength = true;
			}
			if (contentType && !hasContentTypeHeader) headers.push(["content-type", contentType]);
			if (contentLength && !hasContentLength) headers.push(["content-length", String(contentLength)]);
			this.#init = void 0;
			this.#headers = void 0;
			this.#response = void 0;
			this.#body = void 0;
			return {
				status,
				statusText,
				headers,
				body
			};
		}
	}
	lazyInherit(NodeResponse.prototype, NativeResponse.prototype, "_response");
	Object.setPrototypeOf(NodeResponse, NativeResponse);
	Object.setPrototypeOf(NodeResponse.prototype, NativeResponse.prototype);
	return NodeResponse;
})();
//#endregion
//#region src/adapters/_node/web/socket.ts
/**
* Events:
* - Readable (req from client): readable => data => end (push(null)) => error => close
* - Writable (res to client): pipe => unpipe => drain => finish (end called) => error => close
*/
var WebRequestSocket = class extends Duplex {
	_httpMessage;
	autoSelectFamilyAttemptedAddresses = [];
	bufferSize = 0;
	bytesRead = 0;
	bytesWritten = 0;
	connecting = false;
	pending = false;
	readyState = "open";
	remoteAddress = "";
	remoteFamily = "";
	remotePort = 0;
	#request;
	#timeoutTimer;
	#reqReader;
	#headersWritten;
	#_writeBody;
	_webResBody;
	constructor(request) {
		super({
			signal: request.signal,
			allowHalfOpen: true
		});
		this.#request = request;
		this._webResBody = new ReadableStream({ start: (controller) => {
			this.#_writeBody = controller.enqueue.bind(controller);
			this.once("finish", () => {
				this.readyState = "closed";
				controller.close();
			});
		} });
	}
	setTimeout(ms, cb) {
		if (typeof ms !== "number" || !Number.isFinite(ms) || ms < 0) return this;
		if (cb) this.on("timeout", cb);
		if (this.#timeoutTimer) clearTimeout(this.#timeoutTimer);
		if (ms > 0) this.#timeoutTimer = setTimeout(() => this.emit("timeout"), ms);
		return this;
	}
	setNoDelay() {
		return this;
	}
	setKeepAlive() {
		return this;
	}
	ref() {
		return this;
	}
	unref() {
		return this;
	}
	destroySoon() {
		this.destroy();
	}
	connect() {
		return this;
	}
	resetAndDestroy() {
		this.destroy();
		return this;
	}
	address() {
		return {
			address: "",
			family: "",
			port: 0
		};
	}
	_read(_size) {
		const reader = this.#reqReader ??= this.#request.body?.getReader();
		if (!reader) {
			this.push(null);
			return;
		}
		reader.read().then((res) => this._onRead(res)).catch((error) => {
			this.emit("error", error);
		});
	}
	_onRead(res) {
		if (res.done) {
			this.push(null);
			return;
		}
		if (res.value) {
			this.bytesRead += res.value.byteLength;
			this.push(res.value);
		}
	}
	_write(chunk, encoding, callback) {
		if (this.#headersWritten) this.#_writeBody(typeof chunk === "string" ? Buffer.from(chunk, encoding) : chunk);
		else if (chunk?.length > 0) {
			this.#headersWritten = true;
			const headerEnd = chunk.lastIndexOf("\r\n\r\n");
			if (headerEnd === -1) throw new Error("Invalid HTTP headers chunk!");
			if (headerEnd < chunk.length - 4) {
				this._write(chunk.slice(headerEnd + 4), encoding, () => {
					callback(null);
				});
				return;
			}
		}
		callback(null);
	}
	_final(callback) {
		callback(null);
	}
	_destroy(err, cb) {
		if (this.#timeoutTimer) clearTimeout(this.#timeoutTimer);
		if (this.#reqReader) this.#reqReader.cancel().catch((error) => {
			console.error(error);
		});
		this.readyState = "closed";
		cb(err ?? void 0);
	}
};
//#endregion
//#region src/adapters/_node/web/incoming.ts
var WebIncomingMessage = class extends IncomingMessage {
	constructor(req, socket) {
		super(socket);
		this.method = req.method;
		const url = req._url ??= new FastURL(req.url);
		this.url = url.pathname + url.search;
		for (const [key, value] of req.headers.entries()) this.headers[key.toLowerCase()] = value;
		if (req.method !== "GET" && req.method !== "HEAD" && !this.headers["content-length"] && !this.headers["transfer-encoding"]) this.headers["transfer-encoding"] = "chunked";
		const onData = (chunk) => {
			this.push(chunk);
		};
		socket.on("data", onData);
		socket.once("end", () => {
			this.emit("end");
			this.off("data", onData);
		});
	}
};
//#endregion
//#region src/adapters/_node/call.ts
function callNodeHandler(handler, req) {
	const isMiddleware = handler.length > 2;
	const nodeCtx = req.runtime?.node;
	if (!nodeCtx || !nodeCtx.req || !nodeCtx.res) throw new Error("Node.js runtime context is not available.");
	const { req: nodeReq, res: nodeRes } = nodeCtx;
	let _headers;
	const webRes = new NodeResponse(void 0, {
		get status() {
			return nodeRes.statusCode;
		},
		get statusText() {
			return nodeRes.statusMessage;
		},
		get headers() {
			if (!_headers) {
				const headerEntries = [];
				const rawHeaders = nodeRes.getHeaders();
				for (const [name, value] of Object.entries(rawHeaders)) if (Array.isArray(value)) for (const v of value) headerEntries.push([name, v]);
				else if (value) headerEntries.push([name, String(value)]);
				_headers = new Headers(headerEntries);
			}
			return _headers;
		}
	});
	return new Promise((resolve, reject) => {
		nodeRes.once("close", () => resolve(webRes));
		nodeRes.once("finish", () => resolve(webRes));
		nodeRes.once("error", (error) => reject(error));
		let streamPromise;
		nodeRes.once("pipe", (stream) => {
			streamPromise = new Promise((resolve) => {
				stream.once("end", () => resolve(webRes));
				stream.once("error", (error) => reject(error));
			});
		});
		try {
			if (isMiddleware) Promise.resolve(handler(nodeReq, nodeRes, (error) => error ? reject(error) : streamPromise || resolve(webRes))).catch((error) => reject(error));
			else Promise.resolve(handler(nodeReq, nodeRes)).then(() => streamPromise || webRes);
		} catch (error) {
			reject(error);
		}
	});
}
//#endregion
//#region src/adapters/_node/web/response.ts
var WebServerResponse = class extends ServerResponse {
	#socket;
	constructor(req, socket) {
		super(req);
		this.assignSocket(socket);
		this.once("finish", () => {
			socket.end();
		});
		this.#socket = socket;
		this.waitToFinish = this.waitToFinish.bind(this);
		this.toWebResponse = this.toWebResponse.bind(this);
	}
	waitToFinish() {
		if (this.writableEnded) return Promise.resolve();
		return new Promise((resolve, reject) => {
			this.on("finish", () => resolve());
			this.on("error", (err) => reject(err));
		});
	}
	async toWebResponse() {
		await this.waitToFinish();
		const headers = [];
		const httpHeader = this._header?.split("\r\n");
		for (let i = 1; httpHeader && i < httpHeader.length; i++) {
			const sepIndex = httpHeader[i].indexOf(": ");
			if (sepIndex === -1) continue;
			const key = httpHeader[i].slice(0, Math.max(0, sepIndex));
			const value = httpHeader[i].slice(Math.max(0, sepIndex + 2));
			if (!key) continue;
			headers.push([key, value]);
		}
		return new Response(this.#socket._webResBody, {
			status: this.statusCode,
			statusText: this.statusMessage,
			headers
		});
	}
};
//#endregion
//#region src/adapters/_node/web/fetch.ts
/**
* Calls a Node.js HTTP Request handler with a Fetch API Request object and returns a Response object.
*
* If the web Request contains an existing Node.js req/res pair (indicating it originated from a Node.js server from srvx/node), it will be called directly.
*
* Otherwise, new Node.js IncomingMessage and ServerResponse objects are created and linked to a custom Duplex stream that bridges the Fetch API streams with Node.js streams.
*
* The handler is invoked with these objects, and the response is constructed from the ServerResponse once it is finished.
*
* @experimental Behavior might be unstable.
*/
async function fetchNodeHandler(handler, req) {
	const nodeRuntime = req.runtime?.node;
	if (nodeRuntime && nodeRuntime.req && nodeRuntime.res) return await callNodeHandler(handler, req);
	const socket = new WebRequestSocket(req);
	const nodeReq = new WebIncomingMessage(req, socket);
	const nodeRes = new WebServerResponse(nodeReq, socket);
	try {
		await handler(nodeReq, nodeRes);
		return await nodeRes.toWebResponse();
	} catch (error) {
		console.error(error, { cause: {
			req,
			handler
		} });
		return new Response(null, {
			status: 500,
			statusText: "Internal Server Error"
		});
	}
}
//#endregion
//#region src/adapters/_node/adapter.ts
/**
* Converts a Fetch API handler to a Node.js HTTP handler.
*/
function toNodeHandler(handler) {
	if (handler.__nodeHandler) return handler.__nodeHandler;
	function convertedNodeHandler(nodeReq, nodeRes) {
		const res = handler(new NodeRequest({
			req: nodeReq,
			res: nodeRes
		}));
		return res instanceof Promise ? res.then((resolvedRes) => sendNodeResponse(nodeRes, resolvedRes)) : sendNodeResponse(nodeRes, res);
	}
	convertedNodeHandler.__fetchHandler = handler;
	assignFnName(convertedNodeHandler, handler, " (converted to Node handler)");
	return convertedNodeHandler;
}
/**
* Converts a Node.js HTTP handler into a Fetch API handler.
*
* @experimental Behavior might be unstable and won't work in Bun and Deno currently (tracker: https://github.com/h3js/srvx/issues/132)
*/
function toFetchHandler(handler) {
	if (handler.__fetchHandler) return handler.__fetchHandler;
	function convertedNodeHandler(req) {
		return fetchNodeHandler(handler, req);
	}
	convertedNodeHandler.__nodeHandler = handler;
	assignFnName(convertedNodeHandler, handler, " (converted to Web handler)");
	return convertedNodeHandler;
}
function assignFnName(target, source, suffix) {
	if (source.name) try {
		Object.defineProperty(target, "name", { value: `${source.name}${suffix}` });
	} catch {}
}
//#endregion
//#region src/adapters/node.ts
function serve(options) {
	return new NodeServer(options);
}
var NodeServer = class {
	runtime = "node";
	options;
	node;
	serveOptions;
	fetch;
	waitUntil;
	#isSecure;
	#listeningPromise;
	#wait;
	constructor(options) {
		this.options = {
			...options,
			middleware: [...options.middleware || []]
		};
		for (const plugin of options.plugins || []) plugin(this);
		errorPlugin(this);
		const fetchHandler = this.fetch = wrapFetch(this);
		const handler = (nodeReq, nodeRes) => {
			const request = new NodeRequest({
				req: nodeReq,
				res: nodeRes
			});
			request.waitUntil = this.#wait?.waitUntil;
			const res = fetchHandler(request);
			return res instanceof Promise ? res.then((resolvedRes) => sendNodeResponse(nodeRes, resolvedRes)) : sendNodeResponse(nodeRes, res);
		};
		this.node = {
			handler,
			server: void 0
		};
		const loader = globalThis.__srvxLoader__;
		if (loader) {
			loader({ server: this });
			return;
		}
		gracefulShutdownPlugin(this);
		this.#wait = createWaitUntil();
		this.waitUntil = this.#wait.waitUntil;
		const tls = resolveTLSOptions(this.options);
		const { port, hostname: host } = resolvePortAndHost(this.options);
		this.serveOptions = {
			port,
			host,
			exclusive: !this.options.reusePort,
			...tls ? {
				cert: tls.cert,
				key: tls.key,
				passphrase: tls.passphrase
			} : {},
			...this.options.node
		};
		let server;
		this.#isSecure = !!this.serveOptions.cert && this.options.protocol !== "http";
		if (this.options.node?.http2 ?? this.#isSecure) if (this.#isSecure) server = nodeHTTP2.createSecureServer({
			allowHTTP1: true,
			...this.serveOptions
		}, handler);
		else throw new Error("node.http2 option requires tls certificate!");
		else if (this.#isSecure) server = nodeHTTPS.createServer(this.serveOptions, handler);
		else server = nodeHTTP.createServer(this.serveOptions, handler);
		this.node.server = server;
		if (!options.manual) this.serve();
	}
	serve() {
		if (this.#listeningPromise) return Promise.resolve(this.#listeningPromise).then(() => this);
		this.#listeningPromise = new Promise((resolve) => {
			this.node.server.listen(this.serveOptions, () => {
				printListening(this.options, this.url);
				resolve();
			});
		});
	}
	get url() {
		const addr = this.node?.server?.address();
		if (!addr) return;
		return typeof addr === "string" ? addr : fmtURL(addr.address, addr.port, this.#isSecure);
	}
	ready() {
		return Promise.resolve(this.#listeningPromise).then(() => this);
	}
	async close(closeAll) {
		await Promise.all([this.#wait?.wait(), new Promise((resolve, reject) => {
			const server = this.node?.server;
			if (server && closeAll && "closeAllConnections" in server) server.closeAllConnections();
			if (!server || !server.listening) return resolve();
			server.close((error) => error ? reject(error) : resolve());
		})]);
	}
};
//#endregion
export { NodeResponse as FastResponse, NodeResponse, FastURL, NodeRequest, fetchNodeHandler, patchGlobalRequest, sendNodeResponse, serve, toFetchHandler, toNodeHandler };

import "../_chunks/_utils.mjs";
import { t as FastURL } from "../_chunks/_url.mjs";
import { a as resolveTLSOptions, i as resolvePortAndHost, n as fmtURL, r as printListening, t as createWaitUntil } from "../_chunks/_utils2.mjs";
import { n as gracefulShutdownPlugin, r as wrapFetch } from "../_chunks/_plugins.mjs";
//#region src/adapters/deno.ts
const FastResponse = Response;
function serve(options) {
	return new DenoServer(options);
}
var DenoServer = class {
	runtime = "deno";
	options;
	deno = {};
	serveOptions;
	fetch;
	waitUntil;
	#listeningPromise;
	#listeningInfo;
	#wait;
	constructor(options) {
		this.options = {
			...options,
			middleware: [...options.middleware || []]
		};
		for (const plugin of options.plugins || []) plugin(this);
		gracefulShutdownPlugin(this);
		const fetchHandler = wrapFetch(this);
		const loader = globalThis.__srvxLoader__;
		if (loader) {
			this.fetch = fetchHandler;
			loader({ server: this });
			return;
		}
		this.#wait = createWaitUntil();
		this.waitUntil = this.#wait.waitUntil;
		this.fetch = (request, info) => {
			Object.defineProperties(request, {
				waitUntil: { value: this.#wait?.waitUntil },
				runtime: {
					enumerable: true,
					value: {
						name: "deno",
						deno: {
							info,
							server: this.deno?.server
						}
					}
				},
				ip: {
					enumerable: true,
					get() {
						return (info?.remoteAddr)?.hostname;
					}
				}
			});
			return fetchHandler(request);
		};
		const tls = resolveTLSOptions(this.options);
		this.serveOptions = {
			...resolvePortAndHost(this.options),
			reusePort: this.options.reusePort,
			onError: this.options.error,
			...tls ? {
				key: tls.key,
				cert: tls.cert,
				passphrase: tls.passphrase
			} : {},
			...this.options.deno
		};
		if (!options.manual) this.serve();
	}
	serve() {
		if (this.deno?.server) return Promise.resolve(this.#listeningPromise).then(() => this);
		const onListenPromise = Promise.withResolvers();
		this.#listeningPromise = onListenPromise.promise;
		this.deno.server = Deno.serve({
			...this.serveOptions,
			onListen: (info) => {
				this.#listeningInfo = info;
				if (this.options.deno?.onListen) this.options.deno.onListen(info);
				printListening(this.options, this.url);
				onListenPromise.resolve();
			}
		}, this.fetch);
		return Promise.resolve(this.#listeningPromise).then(() => this);
	}
	get url() {
		return this.#listeningInfo ? fmtURL(this.#listeningInfo.hostname, this.#listeningInfo.port, !!this.serveOptions.cert) : void 0;
	}
	ready() {
		return Promise.resolve(this.#listeningPromise).then(() => this);
	}
	async close() {
		await Promise.all([this.#wait?.wait(), Promise.resolve(this.deno?.server?.shutdown())]);
	}
};
//#endregion
export { FastResponse, FastURL, serve };

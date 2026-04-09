import "../_chunks/_utils.mjs";
import { r as wrapFetch, t as errorPlugin } from "../_chunks/_plugins.mjs";
//#region src/adapters/bunny.ts
const FastURL = URL;
const FastResponse = Response;
function serve(options) {
	return new BunnyServer(options);
}
var BunnyServer = class {
	runtime = "bunny";
	options;
	fetch;
	_started = false;
	waitUntil;
	constructor(options) {
		this.options = {
			...options,
			middleware: [...options.middleware || []]
		};
		for (const plugin of options.plugins || []) plugin(this);
		errorPlugin(this);
		const fetchHandler = wrapFetch(this);
		const waitUntil = this.waitUntil = (p) => Bunny.unstable?.waitUntil?.(p);
		this.fetch = (request) => {
			Object.defineProperties(request, {
				runtime: {
					enumerable: true,
					value: { name: "bunny" }
				},
				waitUntil: { value: waitUntil },
				ip: {
					enumerable: true,
					get() {
						return request.headers.get("x-real-ip");
					}
				}
			});
			return fetchHandler(request);
		};
		if (!options.manual) this.serve();
	}
	serve() {
		if (typeof Bunny !== "undefined" && Bunny.v1?.serve) {
			if (this._started) return;
			this._started = true;
			Bunny.v1.serve(this.fetch);
		} else throw new Error("[srvx] Bunny runtime not detected.");
	}
	ready() {
		return Promise.resolve(this);
	}
	close() {
		return Promise.resolve();
	}
};
//#endregion
export { FastResponse, FastURL, serve };

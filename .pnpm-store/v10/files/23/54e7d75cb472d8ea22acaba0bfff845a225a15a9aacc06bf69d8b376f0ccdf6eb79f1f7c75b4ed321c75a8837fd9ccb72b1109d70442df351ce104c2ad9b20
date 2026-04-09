//#region src/tracing.ts
/**
*
* @experimental Channel names, event types and config options may change in future releases.
*
* Tracing plugin that adds diagnostics channel tracing to middleware and fetch handlers.
*
* This plugin wraps all middleware and the fetch handler with tracing instrumentation,
* allowing you to subscribe to `srvx.request` and `srvx.middleware` tracing channels.
*
* @example
* ```ts
* import { serve } from "srvx";
* import { tracingPlugin } from "srvx/tracing";
*
* const server = serve({
*   fetch: (req) => new Response("OK"),
*   middleware: [myMiddleware],
*   plugins: [tracingPlugin()],
* });
* ```
*/
function tracingPlugin(opts = {}) {
	return (server) => {
		const { tracingChannel } = globalThis.process?.getBuiltinModule?.("node:diagnostics_channel") || {};
		if (!tracingChannel) return;
		if (opts.fetch !== false) {
			const fetchChannel = tracingChannel("srvx.request");
			const originalFetch = server.options.fetch;
			server.options.fetch = (request) => {
				return fetchChannel.tracePromise(async () => await originalFetch(request), {
					request,
					server
				});
			};
		}
		if (opts.middleware !== false) {
			const middlewareChannel = tracingChannel("srvx.middleware");
			const wrappedMiddleware = server.options.middleware.map((handler, index) => {
				const middleware = Object.freeze({
					index,
					handler
				});
				return (request, next) => {
					return middlewareChannel.tracePromise(async () => await handler(request, next), {
						request,
						server,
						middleware
					});
				};
			});
			server.options.middleware.splice(0, server.options.middleware.length, ...wrappedMiddleware);
		}
	};
}
//#endregion
export { tracingPlugin };

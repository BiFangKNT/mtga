import { Server, ServerMiddleware, ServerPlugin, ServerRequest } from "./types.mjs";

//#region src/tracing.d.ts
/**
* @experimental Channel names, event types and config options may change in future releases.
*/
type RequestEvent = {
  server: Server;
  request: ServerRequest;
  middleware?: {
    index: number;
    handler: ServerMiddleware;
  };
};
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
declare function tracingPlugin(opts?: {
  middleware?: boolean;
  fetch?: boolean;
}): ServerPlugin;
//#endregion
export { RequestEvent, tracingPlugin };
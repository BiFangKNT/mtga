import { FetchHandler, NodeHttpHandler, NodeServerRequest, NodeServerResponse, Server, ServerOptions, ServerRequest } from "../types.mjs";
import { t as FastURL } from "../_chunks/_url.mjs";
import { Readable } from "node:stream";

//#region src/adapters/_node/request.d.ts
type NodeRequestContext = {
  req: NodeServerRequest;
  res?: NodeServerResponse;
};
declare const NodeRequest: {
  new (nodeCtx: NodeRequestContext): ServerRequest;
};
/**
* Undici uses an incompatible Request constructor depending on private property accessors.
*
* This utility, patches global Request to support `new Request(req)` in Node.js.
*
* Alternatively you can use `new Request(req._request || req)` instead of patching global Request.
*/
declare function patchGlobalRequest(): typeof Request;
//#endregion
//#region src/adapters/_node/response.d.ts
type PreparedNodeResponseBody = string | Buffer | Uint8Array | DataView | ReadableStream | Readable | undefined | null;
interface PreparedNodeResponse {
  status: number;
  statusText: string;
  headers: [string, string][];
  body: PreparedNodeResponseBody;
}
/**
* Fast Response for Node.js runtime
*
* It is faster because in most cases it doesn't create a full Response instance.
*/
declare const NodeResponse: {
  new (body?: BodyInit | null, init?: ResponseInit): globalThis.Response & {
    _toNodeResponse: () => PreparedNodeResponse;
  };
};
type NodeResponse = InstanceType<typeof NodeResponse>;
//#endregion
//#region src/adapters/_node/send.d.ts
declare function sendNodeResponse(nodeRes: NodeServerResponse, webRes: Response | NodeResponse): Promise<void>;
//#endregion
//#region src/adapters/_node/web/fetch.d.ts
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
declare function fetchNodeHandler(handler: NodeHttpHandler, req: ServerRequest): Promise<Response>;
//#endregion
//#region src/adapters/_node/adapter.d.ts
type AdapterMeta = {
  __nodeHandler?: NodeHttpHandler;
  __fetchHandler?: FetchHandler;
};
/**
* Converts a Fetch API handler to a Node.js HTTP handler.
*/
declare function toNodeHandler(handler: FetchHandler & AdapterMeta): NodeHttpHandler & AdapterMeta;
/**
* Converts a Node.js HTTP handler into a Fetch API handler.
*
* @experimental Behavior might be unstable and won't work in Bun and Deno currently (tracker: https://github.com/h3js/srvx/issues/132)
*/
declare function toFetchHandler(handler: NodeHttpHandler & AdapterMeta): FetchHandler & AdapterMeta;
//#endregion
//#region src/adapters/node.d.ts
declare function serve(options: ServerOptions): Server;
//#endregion
export { type AdapterMeta, NodeResponse as FastResponse, NodeResponse, FastURL, NodeRequest, fetchNodeHandler, patchGlobalRequest, sendNodeResponse, serve, toFetchHandler, toNodeHandler };
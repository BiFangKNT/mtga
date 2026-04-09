import { Server, ServerHandler } from "srvx";

//#region src/loader.d.ts
declare const defaultExts: string[];
declare const defaultEntries: string[];
/**
* Options for loading a server entry module.
*/
type LoadOptions = {
  /**
  * Path or URL to the server entry file.
  *
  * If not provided, common entry points will be searched automatically.
  */
  entry?: string;
  /**
  * Base directory for resolving relative paths.
  *
  * @default "."
  */
  dir?: string;
  /**
  * Set to `false` to disable interception of `http.Server.listen` to detect legacy handlers.
  *
  * @default true
  */
  interceptHttpListen?: boolean;
  /**
  * Set to `false` to disable Node.js handler (req, res) compatibility.
  */
  nodeCompat?: boolean;
  /**
  * Node.js server instance to return when intercepting `http.Server.listen`.
  */
  nodeServer?: NodeServer;
  /**
  * srvx server instance to return when intercepting `http.Server.listen`.
  */
  srvxServer?: Server;
  /**
  * Hook called after the module is loaded to allow for custom processing.
  *
  * You can return a modified version of the module if needed.
  */
  onLoad?: (module: unknown) => any;
};
/**
* Result of loading a server entry module.
*/
type LoadedServerEntry = {
  /**
  * The web fetch handler extracted from the loaded module.
  *
  * This is resolved from `module.fetch`, `module.default.fetch`,
  * or upgraded from a legacy Node.js handler.
  */
  fetch?: ServerHandler;
  /**
  * The raw loaded module.
  */
  module?: any;
  /**
  * Whether the handler was upgraded from a legacy Node.js HTTP handler.
  *
  * When `true`, the original module exported a Node.js-style `(req, res)` handler
  * that has been wrapped for web fetch compatibility.
  */
  nodeCompat?: boolean;
  /**
  * The resolved `file://` URL of the loaded entry module.
  */
  url?: string;
  /**
  * Whether the specified entry file was not found.
  *
  * When `true`, no valid entry point could be located.
  */
  notFound?: boolean;
  /**
  * The original srvx server instance if the module used the loader API to export a server directly.
  */
  srvxServer?: Server;
};
declare function loadServerEntry(opts: LoadOptions): Promise<LoadedServerEntry>;
type NodeServer = NonNullable<Server["node"]>["server"];
//#endregion
export { loadServerEntry as a, defaultExts as i, LoadedServerEntry as n, defaultEntries as r, LoadOptions as t };
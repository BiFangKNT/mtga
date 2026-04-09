import { PluginContainer } from "vite";
import { Socket } from "node:net";
import { Manifest } from "vue-bundle-renderer";
import { FetchResult } from "vite-node";

//#region src/plugins/vite-node.d.ts
type ResolveIdResponse = Awaited<ReturnType<PluginContainer["resolveId"]>>;
interface ViteNodeFetch {
  /**  Gets the client manifest. */
  getManifest(): Promise<Manifest>;
  /** Gets the list of invalidated files. */
  getInvalidates(): Promise<string[]>;
  /** Resolves a module ID. */
  resolveId(id: string, importer?: string): Promise<ResolveIdResponse | null>;
  /** Fetches a module. */
  fetchModule(moduleId: string): Promise<FetchResult>;
  /** Ensures the IPC socket is connected. */
  ensureConnected(): Promise<Socket>;
}
type ViteNodeServerOptions = {
  baseURL: string;
  socketPath: string;
  root: string;
  entryPath: string;
  base: string;
  maxRetryAttempts?: number;
  baseRetryDelay?: number;
  maxRetryDelay?: number;
  requestTimeout?: number;
};
//#endregion
//#region src/vite-node.d.ts
declare const viteNodeOptions: ViteNodeServerOptions;
declare const viteNodeFetch: ViteNodeFetch;
//#endregion
export { viteNodeFetch, viteNodeOptions };
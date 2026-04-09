import EventEmitter from "node:events";
import { ListenOptions, Listener } from "listhen";
import { DotenvOptions } from "c12";
import { NuxtConfig } from "@nuxt/schema";
import { RequestListener } from "node:http";

//#region ../nuxi/src/dev/utils.d.ts
interface NuxtDevContext {
  cwd: string;
  args: {
    clear?: boolean;
    logLevel?: string;
    dotenv?: string;
    envName?: string;
    extends?: string;
    profile?: string | boolean;
  };
}
interface NuxtDevServerOptions {
  cwd: string;
  logLevel?: "silent" | "info" | "verbose";
  dotenv: DotenvOptions;
  envName?: string;
  clear?: boolean;
  overrides: NuxtConfig;
  loadingTemplate?: ({
    loading
  }: {
    loading: string;
  }) => string;
  showBanner?: boolean;
  listenOverrides?: Partial<ListenOptions>;
}
interface DevServerEventMap {
  "loading:error": [error: Error];
  "loading": [loadingMessage: string];
  "ready": [address: string];
  "restart": [];
}
declare class NuxtDevServer extends EventEmitter<DevServerEventMap> {
  #private;
  private options;
  loadDebounced: (reload?: boolean, reason?: string) => void;
  handler: RequestListener;
  listener: Listener;
  constructor(options: NuxtDevServerOptions);
  init(): Promise<void>;
  closeWatchers(): void;
  load(reload?: boolean, reason?: string): Promise<void>;
  close(): Promise<void>;
}
//#endregion
//#region ../nuxi/src/dev/index.d.ts
interface InitializeOptions {
  data?: {
    overrides?: NuxtConfig;
  };
  listenOverrides?: Partial<ListenOptions>;
  showBanner?: boolean;
}
interface InitializeReturn {
  listener: Listener;
  close: () => Promise<void>;
  onReady: (callback: (address: string) => void) => void;
  onRestart: (callback: (devServer: NuxtDevServer) => void) => void;
}
declare function initialize(devContext: NuxtDevContext, ctx?: InitializeOptions): Promise<InitializeReturn>;
//#endregion
export { initialize };
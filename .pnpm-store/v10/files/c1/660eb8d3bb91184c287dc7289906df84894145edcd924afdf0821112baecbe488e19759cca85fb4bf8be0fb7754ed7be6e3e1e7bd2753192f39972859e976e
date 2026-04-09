import * as _jridgewell_trace_mapping0 from "@jridgewell/trace-mapping";
import { DecodedSourceMap, EncodedSourceMap, EncodedSourceMap as EncodedSourceMap$1, SourceMapInput } from "@jridgewell/trace-mapping";
import { ViteHotContext } from "vite/types/hot.js";

//#region src/client.d.ts
declare const DEFAULT_REQUEST_STUBS: Record<string, Record<string, unknown>>;
declare class ModuleCacheMap extends Map<string, ModuleCache> {
  normalizePath(fsPath: string): string;
  /**
  * Assign partial data to the map
  */
  update(fsPath: string, mod: ModuleCache): this;
  setByModuleId(modulePath: string, mod: ModuleCache): this;
  set(fsPath: string, mod: ModuleCache): this;
  getByModuleId(modulePath: string): ModuleCache & Required<Pick<ModuleCache, "imports" | "importers">>;
  get(fsPath: string): ModuleCache & Required<Pick<ModuleCache, "importers" | "imports">>;
  deleteByModuleId(modulePath: string): boolean;
  delete(fsPath: string): boolean;
  invalidateModule(mod: ModuleCache): boolean;
  /**
  * Invalidate modules that dependent on the given modules, up to the main entry
  */
  invalidateDepTree(ids: string[] | Set<string>, invalidated?: Set<string>): Set<string>;
  /**
  * Invalidate dependency modules of the given modules, down to the bottom-level dependencies
  */
  invalidateSubDepTree(ids: string[] | Set<string>, invalidated?: Set<string>): Set<string>;
  /**
  * Return parsed source map based on inlined source map of the module
  */
  getSourceMap(id: string): _jridgewell_trace_mapping0.EncodedSourceMap | null;
}
type ModuleExecutionInfo = Map<string, ModuleExecutionInfoEntry>;
interface ModuleExecutionInfoEntry {
  startOffset: number;
  /** The duration that was spent executing the module. */
  duration: number;
  /** The time that was spent executing the module itself and externalized imports. */
  selfTime: number;
}
declare class ViteNodeRunner {
  options: ViteNodeRunnerOptions;
  root: string;
  debug: boolean;
  /**
  * Holds the cache of modules
  * Keys of the map are filepaths, or plain package names
  */
  moduleCache: ModuleCacheMap;
  /**
  * Tracks the stack of modules being executed for the purpose of calculating import self-time.
  *
  * Note that while in most cases, imports are a linear stack of modules,
  * this is occasionally not the case, for example when you have parallel top-level dynamic imports like so:
  *
  * ```ts
  * await Promise.all([
  *  import('./module1'),
  *  import('./module2'),
  * ]);
  * ```
  *
  * In this case, the self time will be reported incorrectly for one of the modules (could go negative).
  * As top-level awaits with dynamic imports like this are uncommon, we don't handle this case specifically.
  */
  private executionStack;
  private performanceNow;
  constructor(options: ViteNodeRunnerOptions);
  executeFile(file: string): Promise<any>;
  executeId(rawId: string): Promise<any>;
  shouldResolveId(id: string, _importee?: string): boolean;
  private _resolveUrl;
  resolveUrl(id: string, importee?: string): Promise<[url: string, fsPath: string]>;
  private _fetchModule;
  protected getContextPrimitives(): {
    Object: ObjectConstructor;
    Reflect: typeof Reflect;
    Symbol: SymbolConstructor;
  };
  protected runModule(context: Record<string, any>, transformed: string): Promise<void>;
  /**
  * mutate the given error to have fixed stacktraces based on source maps
  * Does the same thing as Vite's ssrFixStacktrace
  */
  ssrFixStacktrace(error: Error): Promise<Error>;
  /**
  * Starts calculating the module execution info such as the total duration and self time spent on executing the module.
  * Returns a function to call once the module has finished executing.
  */
  protected startCalculateModuleExecutionInfo(filename: string, startOffset: number): () => ModuleExecutionInfoEntry;
  prepareContext(context: Record<string, any>): Record<string, any>;
  /**
  * Define if a module should be interop-ed
  * This function mostly for the ability to override by subclass
  */
  shouldInterop(path: string, mod: any): boolean;
  protected importExternalModule(path: string): Promise<any>;
  /**
  * Import a module and interop it
  */
  interopedImport(path: string): Promise<any>;
}
//#endregion
//#region src/types.d.ts
type Nullable<T> = T | null | undefined;
type Arrayable<T> = T | Array<T>;
type Awaitable<T> = T | PromiseLike<T>;
interface DepsHandlingOptions {
  external?: (string | RegExp)[];
  inline?: (string | RegExp)[] | true;
  inlineFiles?: string[];
  /**
  * A list of directories that are considered to hold Node.js modules
  * Have to include "/" at the start and end of the path
  *
  * Vite-Node checks the whole absolute path of the import, so make sure you don't include
  * unwanted files accidentally
  * @default ['/node_modules/']
  */
  moduleDirectories?: string[];
  cacheDir?: string;
  /**
  * Try to guess the CJS version of a package when it's invalid ESM
  * @default false
  */
  fallbackCJS?: boolean;
}
interface StartOfSourceMap {
  file?: string;
  sourceRoot?: string;
}
interface RawSourceMap extends StartOfSourceMap {
  version: number;
  sources: string[];
  names: string[];
  sourcesContent?: (string | null)[];
  mappings: string;
}
interface FetchResult {
  code?: string;
  externalize?: string;
  map?: EncodedSourceMap | null;
}
type HotContext = Omit<ViteHotContext, "acceptDeps" | "decline">;
type FetchFunction = (id: string) => Promise<FetchResult>;
type ResolveIdFunction = (id: string, importer?: string) => Awaitable<ViteNodeResolveId | null | undefined | void>;
type CreateHotContextFunction = (runner: ViteNodeRunner, url: string) => HotContext;
interface ModuleCache {
  promise?: Promise<any>;
  exports?: any;
  evaluated?: boolean;
  resolving?: boolean;
  code?: string;
  map?: EncodedSourceMap;
  /**
  * Module ids that imports this module
  */
  importers?: Set<string>;
  imports?: Set<string>;
}
interface ViteNodeRunnerOptions {
  root: string;
  fetchModule: FetchFunction;
  resolveId?: ResolveIdFunction;
  createHotContext?: CreateHotContextFunction;
  base?: string;
  moduleCache?: ModuleCacheMap;
  moduleExecutionInfo?: ModuleExecutionInfo;
  interopDefault?: boolean;
  requestStubs?: Record<string, any>;
  debug?: boolean;
}
interface ViteNodeResolveId {
  external?: boolean | "absolute" | "relative";
  id: string;
  meta?: Record<string, any> | null;
  moduleSideEffects?: boolean | "no-treeshake" | null;
  syntheticNamedExports?: boolean | string | null;
}
interface ViteNodeResolveModule {
  external: string | null;
  id: string;
  fsPath: string;
}
interface ViteNodeServerOptions {
  /**
  * Inject inline sourcemap to modules
  * @default 'inline'
  */
  sourcemap?: "inline" | boolean;
  /**
  * Deps handling
  */
  deps?: DepsHandlingOptions;
  /**
  * Transform method for modules
  */
  transformMode?: {
    ssr?: RegExp[];
    web?: RegExp[];
  };
  debug?: DebuggerOptions;
}
interface DebuggerOptions {
  /**
  * Dump the transformed module to filesystem
  * Passing a string will dump to the specified path
  */
  dumpModules?: boolean | string;
  /**
  * Read dumpped module from filesystem whenever exists.
  * Useful for debugging by modifying the dump result from the filesystem.
  */
  loadDumppedModules?: boolean;
}
//#endregion
export { ModuleExecutionInfo as C, ModuleCacheMap as S, ViteNodeRunner as T, ViteNodeResolveId as _, DecodedSourceMap as a, ViteNodeServerOptions as b, FetchFunction as c, ModuleCache as d, Nullable as f, StartOfSourceMap as g, SourceMapInput as h, DebuggerOptions as i, FetchResult as l, ResolveIdFunction as m, Awaitable as n, DepsHandlingOptions as o, RawSourceMap as p, CreateHotContextFunction as r, EncodedSourceMap$1 as s, Arrayable as t, HotContext as u, ViteNodeResolveModule as v, ModuleExecutionInfoEntry as w, DEFAULT_REQUEST_STUBS as x, ViteNodeRunnerOptions as y };
import { ConsolaInstance, ConsolaOptions } from "consola";
import { UseContext } from "unctx";
import { GlobOptions } from "tinyglobby";
import { LoadConfigOptions } from "c12";
import { Component, ComponentsDir, ModuleDefinition, ModuleMeta, ModuleOptions, Nuxt, NuxtAppConfig, NuxtCompatibility, NuxtCompatibilityIssues, NuxtConfig, NuxtHooks, NuxtMiddleware, NuxtModule, NuxtOptions, NuxtPlugin, NuxtPluginTemplate, NuxtServerTemplate, NuxtTemplate, NuxtTypeTemplate, ResolvedNuxtTemplate, SchemaDefinition } from "@nuxt/schema";
import { Import, InlinePreset } from "unimport";
import { Configuration, WebpackPluginInstance } from "webpack";
import { RspackPluginInstance } from "@rspack/core";
import { Plugin, UserConfig } from "vite";
import * as NitroV2 from "nitropack/types";
import * as NitroV3 from "nitro/types";

//#region src/module/define.d.ts
/**
* Define a Nuxt module, automatically merging defaults with user provided options, installing
* any hooks that are provided, and calling an optional setup function for full control.
*/
declare function defineNuxtModule<TOptions extends ModuleOptions>(definition: ModuleDefinition<TOptions, Partial<TOptions>, false> | NuxtModule<TOptions, Partial<TOptions>, false>): NuxtModule<TOptions, TOptions, false>;
declare function defineNuxtModule<TOptions extends ModuleOptions>(): {
  with: <TOptionsDefaults extends Partial<TOptions>>(definition: ModuleDefinition<TOptions, TOptionsDefaults, true> | NuxtModule<TOptions, TOptionsDefaults, true>) => NuxtModule<TOptions, TOptionsDefaults, true>;
};
//#endregion
//#region src/module/install.d.ts
type ModuleToInstall = string | NuxtModule<ModuleOptions, Partial<ModuleOptions>, false>;
/**
* Installs a set of modules on a Nuxt instance.
* @internal
*/
declare function installModules(modulesToInstall: Map<ModuleToInstall, Record<string, any>>, resolvedModulePaths: Set<string>, nuxt?: Nuxt): Promise<void>;
/**
* Installs a module on a Nuxt instance.
* @deprecated Use module dependencies.
*/
declare function installModule<T extends string | NuxtModule, Config extends Extract<NonNullable<NuxtConfig["modules"]>[number], [T, any]>>(moduleToInstall: T, inlineOptions?: [Config] extends [never] ? any : Config[1], nuxt?: Nuxt): Promise<void>;
declare function resolveModuleWithOptions(definition: NuxtModule<any> | string | false | undefined | null | [(NuxtModule | string)?, Record<string, any>?], nuxt: Nuxt): {
  resolvedPath?: string;
  module: string | NuxtModule<any>;
  options: Record<string, any>;
} | undefined;
declare function loadNuxtModuleInstance(nuxtModule: string | NuxtModule, nuxt?: Nuxt): Promise<{
  nuxtModule: NuxtModule<any>;
  buildTimeModuleMeta: ModuleMeta;
  resolvedModulePath?: string;
}>;
declare function getDirectory(p: string): string;
declare const normalizeModuleTranspilePath: (p: string) => string;
//#endregion
//#region src/module/compatibility.d.ts
/**
* Check if a Nuxt module is installed by name.
*
* This will check both the installed modules and the modules to be installed. Note
* that it cannot detect if a module is _going to be_ installed programmatically by another module.
*/
declare function hasNuxtModule(moduleName: string, nuxt?: Nuxt): boolean;
/**
* Checks if a Nuxt module is compatible with a given semver version.
*/
declare function hasNuxtModuleCompatibility(module: string | NuxtModule, semverVersion: string, nuxt?: Nuxt): Promise<boolean>;
/**
* Get the version of a Nuxt module.
*
* Scans installed modules for the version, if it's not found it will attempt to load the module instance and get the version from there.
*/
declare function getNuxtModuleVersion(module: string | NuxtModule, nuxt?: Nuxt | any): Promise<string | false>;
//#endregion
//#region src/loader/config.d.ts
interface LoadNuxtConfigOptions extends Omit<LoadConfigOptions<NuxtConfig>, "overrides"> {
  overrides?: Exclude<LoadConfigOptions<NuxtConfig>["overrides"], Promise<any> | Function>;
}
declare function loadNuxtConfig(opts: LoadNuxtConfigOptions): Promise<NuxtOptions>;
//#endregion
//#region src/loader/schema.d.ts
declare function extendNuxtSchema(def: SchemaDefinition | (() => SchemaDefinition)): void;
//#endregion
//#region src/loader/nuxt.d.ts
interface LoadNuxtOptions extends LoadNuxtConfigOptions {
  /** Load nuxt with development mode */
  dev?: boolean;
  /** Use lazy initialization of nuxt if set to false */
  ready?: boolean;
}
declare function loadNuxt(opts: LoadNuxtOptions): Promise<Nuxt>;
declare function buildNuxt(nuxt: Nuxt): Promise<any>;
//#endregion
//#region src/layers.d.ts
interface LayerDirectories {
  /** Nuxt rootDir (`/` by default) */
  readonly root: string;
  /** Nitro source directory (`/server` by default) */
  readonly server: string;
  /** Local modules directory (`/modules` by default) */
  readonly modules: string;
  /** Shared directory (`/shared` by default) */
  readonly shared: string;
  /** Public directory (`/public` by default) */
  readonly public: string;
  /** Nuxt srcDir (`/app/` by default) */
  readonly app: string;
  /** Layouts directory (`/app/layouts` by default) */
  readonly appLayouts: string;
  /** Middleware directory (`/app/middleware` by default) */
  readonly appMiddleware: string;
  /** Pages directory (`/app/pages` by default) */
  readonly appPages: string;
  /** Plugins directory (`/app/plugins` by default) */
  readonly appPlugins: string;
}
/**
* Get the resolved directory paths for all layers in a Nuxt application.
*
* Returns an array of LayerDirectories objects, ordered by layer priority:
* - The first layer is the user/project layer (highest priority)
* - Earlier layers override later layers in the array
* - Base layers appear last in the array (lowest priority)
*
* @param nuxt - The Nuxt instance to get layers from. Defaults to the current Nuxt context.
* @returns Array of LayerDirectories objects, ordered by priority (user layer first)
*/
declare function getLayerDirectories(nuxt?: Nuxt): LayerDirectories[];
//#endregion
//#region src/head.d.ts
declare function setGlobalHead(head: NuxtAppConfig["head"]): void;
//#endregion
//#region src/imports.d.ts
declare function addImports(imports: Import | Import[]): void;
declare function addImportsDir(dirs: string | string[], opts?: {
  prepend?: boolean;
}): void;
declare function addImportsSources(presets: InlinePreset | InlinePreset[]): void;
//#endregion
//#region src/runtime-config.d.ts
/**
* Access 'resolved' Nuxt runtime configuration, with values updated from environment.
*
* This mirrors the runtime behavior of Nitro.
*/
declare function useRuntimeConfig(): Record<string, any>;
/**
* Update Nuxt runtime configuration.
*/
declare function updateRuntimeConfig(runtimeConfig: Record<string, unknown>): void | Promise<void>;
//#endregion
//#region src/build.d.ts
type Arrayable<T> = T | T[];
type Thenable<T> = T | Promise<T>;
interface ExtendConfigOptions {
  /**
  * Install plugin on dev
  * @default true
  */
  dev?: boolean;
  /**
  * Install plugin on build
  * @default true
  */
  build?: boolean;
  /**
  * Install plugin on server side
  * @default true
  */
  server?: boolean;
  /**
  * Install plugin on client side
  * @default true
  */
  client?: boolean;
  /**
  * Prepends the plugin to the array with `unshift()` instead of `push()`.
  */
  prepend?: boolean;
}
interface ExtendWebpackConfigOptions extends ExtendConfigOptions {}
interface ExtendViteConfigOptions extends Omit<ExtendConfigOptions, "server" | "client"> {
  /**
  * Extend server Vite configuration
  * @default true
  * @deprecated calling \`extendViteConfig\` with only server/client environment is deprecated.
  * Nuxt 5+ uses the Vite Environment API which shares a configuration between environments.
  * You can likely use a Vite plugin to achieve the same result.
  */
  server?: boolean;
  /**
  * Extend client Vite configuration
  * @default true
  * @deprecated calling \`extendViteConfig\` with only server/client environment is deprecated.
  * Nuxt 5+ uses the Vite Environment API which shares a configuration between environments.
  * You can likely use a Vite plugin to achieve the same result.
  */
  client?: boolean;
}
type ExtendWebpacklikeConfig = (fn: (config: Configuration) => void, options?: ExtendWebpackConfigOptions) => void;
/**
* Extend webpack config
*
* The fallback function might be called multiple times
* when applying to both client and server builds.
*/
declare const extendWebpackConfig: ExtendWebpacklikeConfig;
/**
* Extend rspack config
*
* The fallback function might be called multiple times
* when applying to both client and server builds.
*/
declare const extendRspackConfig: ExtendWebpacklikeConfig;
/**
* Extend Vite config
*/
declare function extendViteConfig(fn: ((config: UserConfig) => Thenable<void>), options?: ExtendViteConfigOptions): (() => void) | undefined;
/**
* Append webpack plugin to the config.
*/
declare function addWebpackPlugin(pluginOrGetter: Arrayable<WebpackPluginInstance> | (() => Thenable<Arrayable<WebpackPluginInstance>>), options?: ExtendWebpackConfigOptions): void;
/**
* Append rspack plugin to the config.
*/
declare function addRspackPlugin(pluginOrGetter: Arrayable<RspackPluginInstance> | (() => Thenable<Arrayable<RspackPluginInstance>>), options?: ExtendWebpackConfigOptions): void;
/**
* Append Vite plugin to the config.
*/
declare function addVitePlugin(pluginOrGetter: Arrayable<Plugin> | (() => Thenable<Arrayable<Plugin>>), options?: ExtendConfigOptions): void;
interface AddBuildPluginFactory {
  vite?: () => Thenable<Arrayable<Plugin>>;
  webpack?: () => Thenable<Arrayable<WebpackPluginInstance>>;
  rspack?: () => Thenable<Arrayable<RspackPluginInstance>>;
}
declare function addBuildPlugin(pluginFactory: AddBuildPluginFactory, options?: ExtendConfigOptions): void;
//#endregion
//#region src/compatibility.d.ts
declare function normalizeSemanticVersion(version: string): string;
/**
* Check version constraints and return incompatibility issues as an array
*/
declare function checkNuxtCompatibility(constraints: NuxtCompatibility, nuxt?: Nuxt): Promise<NuxtCompatibilityIssues>;
/**
* Check version constraints and throw a detailed error if has any, otherwise returns true
*/
declare function assertNuxtCompatibility(constraints: NuxtCompatibility, nuxt?: Nuxt): Promise<true>;
/**
* Check version constraints and return true if passed, otherwise returns false
*/
declare function hasNuxtCompatibility(constraints: NuxtCompatibility, nuxt?: Nuxt): Promise<boolean>;
type NuxtMajorVersion = 2 | 3 | 4;
/**
* Check if current Nuxt instance is of specified major version
*/
declare function isNuxtMajorVersion(majorVersion: NuxtMajorVersion, nuxt?: Nuxt): boolean;
/**
* @deprecated Use `isNuxtMajorVersion(2, nuxt)` instead. This may be removed in \@nuxt/kit v5 or a future major version.
*/
declare function isNuxt2(nuxt?: Nuxt): boolean;
/**
* @deprecated Use `isNuxtMajorVersion(3, nuxt)` instead. This may be removed in \@nuxt/kit v5 or a future major version.
*/
declare function isNuxt3(nuxt?: Nuxt): boolean;
/**
* Get nuxt version
*/
declare function getNuxtVersion(nuxt?: Nuxt | any): string;
//#endregion
//#region src/components.d.ts
/**
* Register a directory to be scanned for components and imported only when used.
*/
declare function addComponentsDir(dir: ComponentsDir, opts?: {
  prepend?: boolean;
}): void;
type AddComponentOptions = {
  name: string;
  filePath: string;
} & Partial<Exclude<Component, "shortPath" | "async" | "level" | "import" | "asyncImport">>;
/**
* This utility takes a file path or npm package that is scanned for named exports, which are get added automatically
*/
declare function addComponentExports(opts: Omit<AddComponentOptions, "name"> & {
  prefix?: string;
}): void;
/**
* Register a component by its name and filePath.
*/
declare function addComponent(opts: AddComponentOptions): void;
//#endregion
//#region src/context.d.ts
/**
* Direct access to the Nuxt global context - see https://github.com/unjs/unctx.
* @deprecated Use `getNuxtCtx` instead
*/
declare const nuxtCtx: UseContext<Nuxt>;
/** Direct access to the Nuxt context with asyncLocalStorage - see https://github.com/unjs/unctx. */
declare const getNuxtCtx: () => Nuxt | null;
/**
* Get access to Nuxt instance.
*
* Throws an error if Nuxt instance is unavailable.
* @example
* ```js
* const nuxt = useNuxt()
* ```
*/
declare function useNuxt(): Nuxt;
/**
* Get access to Nuxt instance.
*
* Returns null if Nuxt instance is unavailable.
* @example
* ```js
* const nuxt = tryUseNuxt()
* if (nuxt) {
*  // Do something
* }
* ```
*/
declare function tryUseNuxt(): Nuxt | null;
declare function runWithNuxtContext<T extends (...args: any[]) => any>(nuxt: Nuxt, fn: T): ReturnType<T>;
//#endregion
//#region src/ignore.d.ts
declare function createIsIgnored(nuxt?: Nuxt | null | undefined): (pathname: string, stats?: unknown) => boolean;
/**
* Return a filter function to filter an array of paths
*/
declare function isIgnored(pathname: string, _stats?: unknown, nuxt?: Nuxt | null | undefined): boolean;
declare function resolveIgnorePatterns(relativePath?: string): string[];
//#endregion
//#region src/layout.d.ts
declare function addLayout(template: NuxtTemplate | string, name?: string): void;
//#endregion
//#region src/nitro-types.d.ts
type isNitroV2 = "options" extends keyof NitroV2.Nitro ? "___INVALID" extends keyof NitroV2.Nitro ? false : true : false;
type isNitroV3 = "options" extends keyof NitroV3.Nitro ? "___INVALID" extends keyof NitroV3.Nitro ? false : true : false;
type Nitro = isNitroV2 extends true ? isNitroV3 extends true ? NitroV2.Nitro | NitroV3.Nitro : NitroV2.Nitro : NitroV3.Nitro;
type NitroDevEventHandler = isNitroV2 extends true ? isNitroV3 extends true ? NitroV2.NitroDevEventHandler | NitroV3.NitroDevEventHandler : NitroV2.NitroDevEventHandler : NitroV3.NitroDevEventHandler;
type NitroEventHandler = isNitroV2 extends true ? isNitroV3 extends true ? NitroV2.NitroEventHandler | NitroV3.NitroEventHandler : NitroV2.NitroEventHandler : NitroV3.NitroEventHandler;
type NitroRouteConfig = isNitroV2 extends true ? isNitroV3 extends true ? NitroV2.NitroRouteConfig | NitroV3.NitroRouteConfig : NitroV2.NitroRouteConfig : NitroV3.NitroRouteConfig;
//#endregion
//#region src/pages.d.ts
declare function extendPages(cb: NuxtHooks["pages:extend"]): void;
interface ExtendRouteRulesOptions {
  /**
  * Override route rule config
  * @default false
  */
  override?: boolean;
}
declare function extendRouteRules(route: string, rule: NitroRouteConfig, options?: ExtendRouteRulesOptions): void;
interface AddRouteMiddlewareOptions {
  /**
  * Override existing middleware with the same name, if it exists
  * @default false
  */
  override?: boolean;
  /**
  * Prepend middleware to the list
  * @default false
  */
  prepend?: boolean;
}
declare function addRouteMiddleware(input: NuxtMiddleware | NuxtMiddleware[], options?: AddRouteMiddlewareOptions): void;
//#endregion
//#region src/plugin.d.ts
declare function normalizePlugin(plugin: NuxtPlugin | string): NuxtPlugin;
/**
* Registers a nuxt plugin and to the plugins array.
*
* Note: You can use mode or .client and .server modifiers with fileName option
* to use plugin only in client or server side.
*
* Note: By default plugin is prepended to the plugins array. You can use second argument to append (push) instead.
* @example
* ```js
* import { createResolver } from '@nuxt/kit'
* const resolver = createResolver(import.meta.url)
*
* addPlugin({
*   src: resolver.resolve('templates/foo.js'),
*   filename: 'foo.server.js' // [optional] only include in server bundle
* })
* ```
*/
interface AddPluginOptions {
  append?: boolean;
}
declare function addPlugin(_plugin: NuxtPlugin | string, opts?: AddPluginOptions): NuxtPlugin;
/**
* Adds a template and registers as a nuxt plugin.
*/
declare function addPluginTemplate(plugin: NuxtPluginTemplate | string, opts?: AddPluginOptions): NuxtPlugin;
//#endregion
//#region src/resolve.d.ts
interface ResolvePathOptions {
  /** Base for resolving paths from. Default is Nuxt rootDir. */
  cwd?: string;
  /** An object of aliases. Default is Nuxt configured aliases. */
  alias?: Record<string, string>;
  /**
  * The file extensions to try.
  * Default is Nuxt configured extensions.
  *
  * Isn't considered when `type` is set to `'dir'`.
  */
  extensions?: string[];
  /**
  * Whether to resolve files that exist in the Nuxt VFS (for example, as a Nuxt template).
  * @default false
  */
  virtual?: boolean;
  /**
  * Whether to fallback to the original path if the resolved path does not exist instead of returning the normalized input path.
  * @default false
  */
  fallbackToOriginal?: boolean;
  /**
  * The type of the path to be resolved.
  * @default 'file'
  */
  type?: PathType;
}
/**
* Resolve the full path to a file or a directory (based on the provided type), respecting Nuxt alias and extensions options.
*
* If a path cannot be resolved, normalized input will be returned unless the `fallbackToOriginal` option is set to `true`,
* in which case the original input path will be returned.
*/
declare function resolvePath(path: string, opts?: ResolvePathOptions): Promise<string>;
/**
* Try to resolve first existing file in paths
*/
declare function findPath(paths: string | string[], opts?: ResolvePathOptions, pathType?: PathType): Promise<string | null>;
/**
* Resolve path aliases respecting Nuxt alias options
*/
declare function resolveAlias(path: string, alias?: Record<string, string>): string;
interface Resolver {
  resolve(...path: string[]): string;
  resolvePath(path: string, opts?: ResolvePathOptions): Promise<string>;
}
/**
* Create a relative resolver
*/
declare function createResolver(base: string | URL): Resolver;
declare function resolveNuxtModule(base: string, paths: string[]): Promise<string[]>;
type PathType = "file" | "dir";
/**
* Resolve absolute file paths in the provided directory with respect to `.nuxtignore` and return them sorted.
* @param path path to the directory to resolve files in
* @param pattern glob pattern or an array of glob patterns to match files
* @param opts options for globbing
* @param opts.followSymbolicLinks whether to follow symbolic links, default is `true`
* @param opts.ignore additional glob patterns to ignore
* @returns sorted array of absolute file paths
*/
declare function resolveFiles(path: string, pattern: string | string[], opts?: {
  followSymbolicLinks?: boolean;
  ignore?: GlobOptions["ignore"];
}): Promise<string[]>;
//#endregion
//#region src/nitro.d.ts
/**
* Adds a nitro server handler
*
*/
declare function addServerHandler(handler: NitroEventHandler): void;
/**
* Adds a nitro server handler for development-only
*
*/
declare function addDevServerHandler(handler: NitroDevEventHandler): void;
/**
* Adds a Nitro plugin
*/
declare function addServerPlugin(plugin: string): void;
/**
* Adds routes to be prerendered
*/
declare function addPrerenderRoutes(routes: string | string[]): void;
/**
* Access to the Nitro instance
*
* **Note:** You can call `useNitro()` only after `ready` hook.
*
* **Note:** Changes to the Nitro instance configuration are not applied.
* @example
*
* ```ts
* nuxt.hook('ready', () => {
*   console.log(useNitro())
* })
* ```
*/
declare function useNitro(): Nitro;
/**
* Add server imports to be auto-imported by Nitro
*/
declare function addServerImports(imports: Import | Import[]): void;
/**
* Add directories to be scanned for auto-imports by Nitro
*/
declare function addServerImportsDir(dirs: string | string[], opts?: {
  prepend?: boolean;
}): void;
/**
* Add directories to be scanned by Nitro. It will check for subdirectories,
* which will be registered just like the `~~/server` folder is.
*/
declare function addServerScanDir(dirs: string | string[], opts?: {
  prepend?: boolean;
}): void;
//#endregion
//#region src/template.d.ts
/**
* Renders given template during build into the virtual file system (and optionally to disk in the project `buildDir`)
*/
declare function addTemplate<T>(_template: NuxtTemplate<T> | string): ResolvedNuxtTemplate<T>;
/**
* Adds a virtual file that can be used within the Nuxt Nitro server build.
*/
declare function addServerTemplate(template: NuxtServerTemplate): NuxtServerTemplate;
/**
* Renders given types during build to disk in the project `buildDir`
* and register them as types.
*
* You can pass a second context object to specify in which context the type should be added.
*
* If no context object is passed, then it will only be added to the nuxt context.
*/
declare function addTypeTemplate<T>(_template: NuxtTypeTemplate<T>, context?: {
  nitro?: boolean;
  nuxt?: boolean;
  node?: boolean;
  shared?: boolean;
}): ResolvedNuxtTemplate<T>;
/**
* Normalize a nuxt template object
*/
declare function normalizeTemplate<T>(template: NuxtTemplate<T> | string, buildDir?: string): ResolvedNuxtTemplate<T>;
/**
* Trigger rebuilding Nuxt templates
*
* You can pass a filter within the options to selectively regenerate a subset of templates.
*/
declare function updateTemplates(options?: {
  filter?: (template: ResolvedNuxtTemplate<any>) => boolean;
}): Promise<void>;
declare function writeTypes(nuxt: Nuxt): Promise<void>;
//#endregion
//#region src/logger.d.ts
declare const logger: ConsolaInstance;
declare function useLogger(tag?: string, options?: Partial<ConsolaOptions>): ConsolaInstance;
//#endregion
//#region src/internal/esm.d.ts
interface ResolveModuleOptions {
  /** @deprecated use `url` with URLs pointing at a file - never a directory */
  paths?: string | string[];
  url?: URL | URL[];
  /** @default ['.js', '.mjs', '.cjs', '.ts', '.mts', '.cts'] */
  extensions?: string[];
}
declare function directoryToURL(dir: string): URL;
/**
* Resolve a module from a given root path using an algorithm patterned on
* the upcoming `import.meta.resolve`. It returns a file URL
*
* @internal
*/
declare function tryResolveModule(id: string, url: URL | URL[]): Promise<string | undefined>;
/** @deprecated pass URLs pointing at files */
declare function tryResolveModule(id: string, url: string | string[]): Promise<string | undefined>;
declare function resolveModule(id: string, options?: ResolveModuleOptions): string;
interface ImportModuleOptions extends ResolveModuleOptions {
  /** Automatically de-default the result of requiring the module. */
  interopDefault?: boolean;
}
declare function importModule<T = unknown>(id: string, opts?: ImportModuleOptions): Promise<T>;
declare function tryImportModule<T = unknown>(id: string, opts?: ImportModuleOptions): Promise<T | undefined> | undefined;
/**
* @deprecated Please use `importModule` instead.
*/
declare function requireModule<T = unknown>(id: string, opts?: ImportModuleOptions): T;
/**
* @deprecated Please use `tryImportModule` instead.
*/
declare function tryRequireModule<T = unknown>(id: string, opts?: ImportModuleOptions): T | undefined;
//#endregion
export { type AddComponentOptions, type AddPluginOptions, type AddRouteMiddlewareOptions, type ExtendConfigOptions, type ExtendRouteRulesOptions, type ExtendViteConfigOptions, type ExtendWebpackConfigOptions, type ImportModuleOptions, type LayerDirectories, type LoadNuxtConfigOptions, type LoadNuxtOptions, type NuxtMajorVersion, type ResolveModuleOptions, type ResolvePathOptions, type Resolver, addBuildPlugin, addComponent, addComponentExports, addComponentsDir, addDevServerHandler, addImports, addImportsDir, addImportsSources, addLayout, addPlugin, addPluginTemplate, addPrerenderRoutes, addRouteMiddleware, addRspackPlugin, addServerHandler, addServerImports, addServerImportsDir, addServerPlugin, addServerScanDir, addServerTemplate, addTemplate, addTypeTemplate, addVitePlugin, addWebpackPlugin, assertNuxtCompatibility, buildNuxt, checkNuxtCompatibility, createIsIgnored, createResolver, defineNuxtModule, directoryToURL, extendNuxtSchema, extendPages, extendRouteRules, extendRspackConfig, extendViteConfig, extendWebpackConfig, findPath, getDirectory, getLayerDirectories, getNuxtCtx, getNuxtModuleVersion, getNuxtVersion, hasNuxtCompatibility, hasNuxtModule, hasNuxtModuleCompatibility, importModule, installModule, installModules, isIgnored, isNuxt2, isNuxt3, isNuxtMajorVersion, loadNuxt, loadNuxtConfig, loadNuxtModuleInstance, logger, normalizeModuleTranspilePath, normalizePlugin, normalizeSemanticVersion, normalizeTemplate, nuxtCtx, requireModule, resolveAlias, resolveFiles, resolveIgnorePatterns, resolveModule, resolveModuleWithOptions, resolveNuxtModule, resolvePath, runWithNuxtContext, setGlobalHead, tryImportModule, tryRequireModule, tryResolveModule, tryUseNuxt, updateRuntimeConfig, updateTemplates, useLogger, useNitro, useNuxt, useRuntimeConfig, writeTypes };
import { VNode, MaybeRefOrGetter } from 'vue';
import { BirpcGroup } from 'birpc';
import { Component, NuxtOptions, NuxtPage, NuxtLayout, NuxtApp, NuxtDebugModuleMutationRecord, Nuxt } from 'nuxt/schema';
import { Import, UnimportMeta } from 'unimport';
import { RouteRecordNormalized } from 'vue-router';
import { Nitro, StorageMounts } from 'nitropack';
import { StorageValue } from 'unstorage';
import { ResolvedConfig } from 'vite';
import { NuxtAnalyzeMeta } from '@nuxt/schema';
import { Options } from 'execa';

type TabCategory = 'pinned' | 'app' | 'vue-devtools' | 'analyze' | 'server' | 'modules' | 'documentation' | 'advanced';

interface ModuleCustomTab {
    /**
     * The name of the tab, must be unique
     */
    name: string;
    /**
     * Icon of the tab, support any Iconify icons, or a url to an image
     */
    icon?: string;
    /**
     * Title of the tab
     */
    title: string;
    /**
     * Main view of the tab
     */
    view: ModuleView;
    /**
     * Category of the tab
     * @default 'app'
     */
    category?: TabCategory;
    /**
     * Insert static vnode to the tab entry
     *
     * Advanced options. You don't usually need this.
     */
    extraTabVNode?: VNode;
    /**
     * Require local authentication to access the tab
     * It's highly recommended to enable this if the tab have sensitive information or have access to the OS
     *
     * @default false
     */
    requireAuth?: boolean;
}
interface ModuleLaunchView {
    /**
     * A view for module to lazy launch some actions
     */
    type: 'launch';
    title?: string;
    icon?: string;
    description: string;
    /**
     * Action buttons
     */
    actions: ModuleLaunchAction[];
}
interface ModuleIframeView {
    /**
     * Iframe view
     */
    type: 'iframe';
    /**
     * Url of the iframe
     */
    src: string;
    /**
     * Persist the iframe instance even if the tab is not active
     *
     * @default true
     */
    persistent?: boolean;
    /**
     * Additional permissions to allow in the iframe
     * These will be merged with the default permissions (clipboard-write, clipboard-read)
     *
     * @example ['camera', 'microphone', 'geolocation']
     */
    permissions?: string[];
}
interface ModuleVNodeView {
    /**
     * Vue's VNode view
     */
    type: 'vnode';
    /**
     * Send vnode to the client, they must be static and serializable
     *
     * Call `nuxt.hook('devtools:customTabs:refresh')` to trigger manual refresh
     */
    vnode: VNode;
}
interface ModuleLaunchAction {
    /**
     * Label of the action button
     */
    label: string;
    /**
     * Additional HTML attributes to the action button
     */
    attrs?: Record<string, string>;
    /**
     * Indicate if the action is pending, will show a loading indicator and disable the button
     */
    pending?: boolean;
    /**
     * Function to handle the action, this is executed on the server side.
     * Will automatically refresh the tabs after the action is resolved.
     */
    handle?: () => void | Promise<void>;
    /**
     * Treat the action as a link, will open the link in a new tab
     */
    src?: string;
}
type ModuleView = ModuleIframeView | ModuleLaunchView | ModuleVNodeView;
interface ModuleIframeTabLazyOptions {
    description?: string;
    onLoad?: () => Promise<void>;
}
interface ModuleBuiltinTab {
    name: string;
    icon?: string;
    title?: string;
    path?: string;
    category?: TabCategory;
    show?: () => MaybeRefOrGetter<any>;
    badge?: () => MaybeRefOrGetter<number | string | undefined>;
    onClick?: () => void;
}
type ModuleTabInfo = ModuleCustomTab | ModuleBuiltinTab;
type CategorizedTabs = [TabCategory, (ModuleCustomTab | ModuleBuiltinTab)[]][];

interface HookInfo {
    name: string;
    start: number;
    end?: number;
    duration?: number;
    listeners: number;
    executions: number[];
}
interface ImageMeta {
    width: number;
    height: number;
    orientation?: number;
    type?: string;
    mimeType?: string;
}
interface PackageUpdateInfo {
    name: string;
    current: string;
    latest: string;
    needsUpdate: boolean;
}
type PackageManagerName = 'npm' | 'yarn' | 'pnpm' | 'bun';
type NpmCommandType = 'install' | 'uninstall' | 'update';
interface NpmCommandOptions {
    dev?: boolean;
    global?: boolean;
}
interface AutoImportsWithMetadata {
    imports: Import[];
    metadata?: UnimportMeta;
    dirs: string[];
}
interface RouteInfo extends Pick<RouteRecordNormalized, 'name' | 'path' | 'meta' | 'props' | 'children'> {
    file?: string;
}
interface ServerRouteInfo {
    route: string;
    filepath: string;
    method?: string;
    type: 'api' | 'route' | 'runtime' | 'collection';
    routes?: ServerRouteInfo[];
}
type ServerRouteInputType = 'string' | 'number' | 'boolean' | 'file' | 'date' | 'time' | 'datetime-local';
interface ServerRouteInput {
    active: boolean;
    key: string;
    value: any;
    type?: ServerRouteInputType;
}
interface Payload {
    url: string;
    time: number;
    data?: Record<string, any>;
    state?: Record<string, any>;
    functions?: Record<string, any>;
}
interface ServerTaskInfo {
    name: string;
    handler: string;
    description: string;
    type: 'collection' | 'task';
    tasks?: ServerTaskInfo[];
}
interface ScannedNitroTasks {
    tasks: {
        [name: string]: {
            handler: string;
            description: string;
        };
    };
    scheduledTasks: {
        [cron: string]: string[];
    };
}
interface PluginInfoWithMetic {
    src: string;
    mode?: 'client' | 'server' | 'all';
    ssr?: boolean;
    metric?: PluginMetric;
}
interface PluginMetric {
    src: string;
    start: number;
    end: number;
    duration: number;
}
interface LoadingTimeMetric {
    ssrStart?: number;
    appInit?: number;
    appLoad?: number;
    pageStart?: number;
    pageEnd?: number;
    pluginInit?: number;
    hmrStart?: number;
    hmrEnd?: number;
}
interface BasicModuleInfo {
    entryPath?: string;
    meta?: {
        name?: string;
    };
}
interface InstalledModuleInfo {
    name?: string;
    isPackageModule: boolean;
    isUninstallable: boolean;
    info?: ModuleStaticInfo;
    entryPath?: string;
    timings?: Record<string, number | undefined>;
    meta?: {
        name?: string;
    };
}
interface ModuleStaticInfo {
    name: string;
    description: string;
    repo: string;
    npm: string;
    icon?: string;
    github: string;
    website: string;
    learn_more: string;
    category: string;
    type: ModuleType;
    stats: ModuleStats;
    maintainers: MaintainerInfo[];
    contributors: GitHubContributor[];
    compatibility: ModuleCompatibility;
}
interface ModuleCompatibility {
    nuxt: string;
    requires: {
        bridge?: boolean | 'optional';
    };
}
interface ModuleStats {
    downloads: number;
    stars: number;
    publishedAt: number;
    createdAt: number;
}
type CompatibilityStatus = 'working' | 'wip' | 'unknown' | 'not-working';
type ModuleType = 'community' | 'official' | '3rd-party';
interface MaintainerInfo {
    name: string;
    github: string;
    twitter?: string;
}
interface GitHubContributor {
    login: string;
    name?: string;
    avatar_url?: string;
}
interface VueInspectorClient {
    enabled: boolean;
    position: {
        x: number;
        y: number;
    };
    linkParams: {
        file: string;
        line: number;
        column: number;
    };
    enable: () => void;
    disable: () => void;
    toggleEnabled: () => void;
    openInEditor: (url: URL) => void;
    onUpdated: () => void;
}
type VueInspectorData = VueInspectorClient['linkParams'] & Partial<VueInspectorClient['position']>;
type AssetType = 'image' | 'font' | 'video' | 'audio' | 'text' | 'json' | 'other';
interface AssetInfo {
    path: string;
    type: AssetType;
    publicPath: string;
    filePath: string;
    size: number;
    mtime: number;
    layer?: string;
}
interface AssetEntry {
    path: string;
    content: string;
    encoding?: BufferEncoding;
    override?: boolean;
}
interface CodeSnippet {
    code: string;
    lang: string;
    name: string;
    docs?: string;
}
interface ComponentRelationship {
    id: string;
    deps: string[];
}
interface ComponentWithRelationships {
    component: Component;
    dependencies?: string[];
    dependents?: string[];
}
interface CodeServerOptions {
    codeBinary: string;
    launchArg: string;
    licenseTermsArg: string;
    connectionTokenArg: string;
}

type CodeServerType = 'ms-code-cli' | 'ms-code-server' | 'coder-code-server';
interface ModuleOptions {
    /**
     * Enable DevTools
     *
     * @default true
     */
    enabled?: boolean;
    /**
     * Custom tabs
     *
     * This is in static format, for dynamic injection, call `nuxt.hook('devtools:customTabs')` instead
     */
    customTabs?: ModuleCustomTab[];
    /**
     * VS Code Server integration options.
     */
    vscode?: VSCodeIntegrationOptions;
    /**
     * Enable Vue Component Inspector
     *
     * @default true
     */
    componentInspector?: boolean;
    /**
     * Enable Vue DevTools integration
     */
    vueDevTools?: boolean;
    /**
     * Enable vite-plugin-inspect
     *
     * @default true
     */
    viteInspect?: boolean;
    /**
     * Enable Vite DevTools integration
     *
     * @experimental
     * @default false
     */
    viteDevTools?: boolean;
    /**
     * Disable dev time authorization check.
     *
     * **NOT RECOMMENDED**, only use this if you know what you are doing.
     *
     * @see https://github.com/nuxt/devtools/pull/257
     * @default false
     */
    disableAuthorization?: boolean;
    /**
     * Props for the iframe element, useful for environment with stricter CSP
     */
    iframeProps?: Record<string, string | boolean>;
    /**
     * Experimental features
     */
    experimental?: {
        /**
         * Timeline tab
         * @deprecated Use `timeline.enable` instead
         */
        timeline?: boolean;
    };
    /**
     * Options for the timeline tab
     */
    timeline?: {
        /**
         * Enable timeline tab
         *
         * @default false
         */
        enabled?: boolean;
        /**
         * Track on function calls
         */
        functions?: {
            include?: (string | RegExp | ((item: Import) => boolean))[];
            /**
             * Include from specific modules
             *
             * @default ['#app', '@unhead/vue']
             */
            includeFrom?: string[];
            exclude?: (string | RegExp | ((item: Import) => boolean))[];
        };
    };
    /**
     * Options for assets tab
     */
    assets?: {
        /**
         * Allowed file extensions for assets tab to upload.
         * To security concern.
         *
         * Set to '*' to disbale this limitation entirely
         *
         * @default Common media and txt files
         */
        uploadExtensions?: '*' | string[];
    };
    /**
     * Enable anonymous telemetry, helping us improve Nuxt DevTools.
     *
     * By default it will respect global Nuxt telemetry settings.
     */
    telemetry?: boolean;
}
interface ModuleGlobalOptions {
    /**
     * List of projects to enable devtools for. Only works when devtools is installed globally.
     */
    projects?: string[];
}
interface VSCodeIntegrationOptions {
    /**
     * Enable VS Code Server integration
     */
    enabled?: boolean;
    /**
     * Start VS Code Server on boot
     *
     * @default false
     */
    startOnBoot?: boolean;
    /**
     * Port to start VS Code Server
     *
     * @default 3080
     */
    port?: number;
    /**
     * Reuse existing server if available (same port)
     */
    reuseExistingServer?: boolean;
    /**
     * Determine whether to use code-server or vs code tunnel
     *
     * @default 'local-serve'
     */
    mode?: 'local-serve' | 'tunnel';
    /**
     * Options for VS Code tunnel
     */
    tunnel?: VSCodeTunnelOptions;
    /**
     * Determines which binary and arguments to use for VS Code.
     *
     * By default, uses the MS Code Server (ms-code-server).
     * Can alternatively use the open source Coder code-server (coder-code-server),
     * or the MS VS Code CLI (ms-code-cli)
     *  @default 'ms-code-server'
     */
    codeServer?: CodeServerType;
    /**
     * Host address to listen on. Unspecified by default.
     */
    host?: string;
}
interface VSCodeTunnelOptions {
    /**
     * the machine name for port forwarding service
     *
     * default: device hostname
     */
    name?: string;
}
interface NuxtDevToolsOptions {
    behavior: {
        telemetry: boolean | null;
        openInEditor: string | undefined;
    };
    ui: {
        componentsGraphShowGlobalComponents: boolean;
        componentsGraphShowLayouts: boolean;
        componentsGraphShowNodeModules: boolean;
        componentsGraphShowPages: boolean;
        componentsGraphShowWorkspace: boolean;
        componentsView: 'list' | 'graph';
        hiddenTabCategories: string[];
        hiddenTabs: string[];
        interactionCloseOnOutsideClick: boolean;
        minimizePanelInactive: number;
        pinnedTabs: string[];
        scale: number;
        showExperimentalFeatures: boolean;
        showHelpButtons: boolean;
        showPanel: boolean | null;
        sidebarExpanded: boolean;
        sidebarScrollable: boolean;
    };
    serverRoutes: {
        selectedRoute: ServerRouteInfo | null;
        view: 'tree' | 'list';
        inputDefaults: Record<string, ServerRouteInput[]>;
        sendFrom: 'app' | 'devtools';
    };
    serverTasks: {
        enabled: boolean;
        selectedTask: ServerTaskInfo | null;
        view: 'tree' | 'list';
        inputDefaults: Record<string, ServerRouteInput[]>;
    };
    assets: {
        view: 'grid' | 'list';
    };
}

interface AnalyzeBuildMeta extends NuxtAnalyzeMeta {
    features: {
        bundleClient: boolean;
        bundleNitro: boolean;
        viteInspect: boolean;
    };
    size: {
        clientBundle?: number;
        nitroBundle?: number;
    };
}
interface AnalyzeBuildsInfo {
    isBuilding: boolean;
    builds: AnalyzeBuildMeta[];
}

interface TerminalBase {
    id: string;
    name: string;
    description?: string;
    icon?: string;
}
type TerminalAction = 'restart' | 'terminate' | 'clear' | 'remove';
interface SubprocessOptions extends Options {
    command: string;
    args?: string[];
}
interface TerminalInfo extends TerminalBase {
    /**
     * Whether the terminal can be restarted
     */
    restartable?: boolean;
    /**
     * Whether the terminal can be terminated
     */
    terminatable?: boolean;
    /**
     * Whether the terminal is terminated
     */
    isTerminated?: boolean;
    /**
     * Content buffer
     */
    buffer?: string;
}
interface TerminalState extends TerminalInfo {
    /**
     * User action to restart the terminal, when not provided, this action will be disabled
     */
    onActionRestart?: () => Promise<void> | void;
    /**
     * User action to terminate the terminal, when not provided, this action will be disabled
     */
    onActionTerminate?: () => Promise<void> | void;
}

interface WizardFunctions {
    enablePages: (nuxt: any) => Promise<void>;
}
type WizardActions = keyof WizardFunctions;
type GetWizardArgs<T extends WizardActions> = WizardFunctions[T] extends (nuxt: any, ...args: infer A) => any ? A : never;

interface ServerFunctions {
    getServerConfig: () => NuxtOptions;
    getServerDebugContext: () => Promise<ServerDebugContext | undefined>;
    getServerData: (token: string) => Promise<NuxtServerData>;
    getServerRuntimeConfig: () => Record<string, any>;
    getModuleOptions: () => ModuleOptions;
    getComponents: () => Component[];
    getComponentsRelationships: () => Promise<ComponentRelationship[]>;
    getAutoImports: () => AutoImportsWithMetadata;
    getServerPages: () => NuxtPage[];
    getCustomTabs: () => ModuleCustomTab[];
    getServerHooks: () => HookInfo[];
    getServerLayouts: () => NuxtLayout[];
    getStaticAssets: () => Promise<AssetInfo[]>;
    getServerRoutes: () => ServerRouteInfo[];
    getServerTasks: () => ScannedNitroTasks | null;
    getServerApp: () => NuxtApp | undefined;
    getOptions: <T extends keyof NuxtDevToolsOptions>(tab: T) => Promise<NuxtDevToolsOptions[T]>;
    updateOptions: <T extends keyof NuxtDevToolsOptions>(tab: T, settings: Partial<NuxtDevToolsOptions[T]>) => Promise<void>;
    clearOptions: () => Promise<void>;
    checkForUpdateFor: (name: string) => Promise<PackageUpdateInfo | undefined>;
    getNpmCommand: (command: NpmCommandType, packageName: string, options?: NpmCommandOptions) => Promise<string[] | undefined>;
    runNpmCommand: (token: string, command: NpmCommandType, packageName: string, options?: NpmCommandOptions) => Promise<{
        processId: string;
    } | undefined>;
    getTerminals: () => TerminalInfo[];
    getTerminalDetail: (token: string, id: string) => Promise<TerminalInfo | undefined>;
    runTerminalAction: (token: string, id: string, action: TerminalAction) => Promise<boolean>;
    getStorageMounts: () => Promise<StorageMounts>;
    getStorageKeys: (base?: string) => Promise<string[]>;
    getStorageItem: (token: string, key: string) => Promise<StorageValue>;
    setStorageItem: (token: string, key: string, value: StorageValue) => Promise<void>;
    removeStorageItem: (token: string, key: string) => Promise<void>;
    getAnalyzeBuildInfo: () => Promise<AnalyzeBuildsInfo>;
    generateAnalyzeBuildName: () => Promise<string>;
    startAnalyzeBuild: (token: string, name: string) => Promise<string>;
    clearAnalyzeBuilds: (token: string, names?: string[]) => Promise<void>;
    getImageMeta: (token: string, filepath: string) => Promise<ImageMeta | undefined>;
    getTextAssetContent: (token: string, filepath: string, limit?: number) => Promise<string | undefined>;
    writeStaticAssets: (token: string, file: AssetEntry[], folder: string) => Promise<string[]>;
    deleteStaticAsset: (token: string, filepath: string) => Promise<void>;
    renameStaticAsset: (token: string, oldPath: string, newPath: string) => Promise<void>;
    telemetryEvent: (payload: object, immediate?: boolean) => void;
    customTabAction: (name: string, action: number) => Promise<boolean>;
    runWizard: <T extends WizardActions>(token: string, name: T, ...args: GetWizardArgs<T>) => Promise<void>;
    openInEditor: (filepath: string) => Promise<boolean>;
    restartNuxt: (token: string, hard?: boolean) => Promise<void>;
    installNuxtModule: (token: string, name: string, dry?: boolean) => Promise<InstallModuleReturn>;
    uninstallNuxtModule: (token: string, name: string, dry?: boolean) => Promise<InstallModuleReturn>;
    enableTimeline: (dry: boolean) => Promise<[string, string]>;
    requestForAuth: (info?: string, origin?: string) => Promise<void>;
    verifyAuthToken: (token: string) => Promise<boolean>;
}
interface ClientFunctions {
    refresh: (event: ClientUpdateEvent) => void;
    callHook: (hook: string, ...args: any[]) => Promise<void>;
    navigateTo: (path: string) => void;
    onTerminalData: (_: {
        id: string;
        data: string;
    }) => void;
    onTerminalExit: (_: {
        id: string;
        code?: number;
    }) => void;
}
interface NuxtServerData {
    nuxt: NuxtOptions;
    nitro?: Nitro['options'];
    vite: {
        server?: ResolvedConfig;
        client?: ResolvedConfig;
    };
}
type ClientUpdateEvent = keyof ServerFunctions;

/**
 * @internal
 */
interface NuxtDevtoolsServerContext {
    nuxt: Nuxt;
    options: ModuleOptions;
    rpc: BirpcGroup<ClientFunctions, ServerFunctions>;
    /**
     * Hook to open file in editor
     */
    openInEditorHooks: ((filepath: string) => boolean | void | Promise<boolean | void>)[];
    /**
     * Invalidate client cache for a function and ask for re-fetching
     */
    refresh: (event: keyof ServerFunctions) => void;
    /**
     * Ensure dev auth token is valid, throw if not
     */
    ensureDevAuthToken: (token: string) => Promise<void>;
    extendServerRpc: <ClientFunctions extends object = Record<string, unknown>, ServerFunctions extends object = Record<string, unknown>>(name: string, functions: ServerFunctions) => BirpcGroup<ClientFunctions, ServerFunctions>;
}
interface NuxtDevtoolsInfo {
    version: string;
    packagePath: string;
    isGlobalInstall: boolean;
}
interface InstallModuleReturn {
    configOriginal: string;
    configGenerated: string;
    commands: string[];
    processId: string;
}
type ServerDebugModuleMutationRecord = (Omit<NuxtDebugModuleMutationRecord, 'module'> & {
    name: string;
});
interface ServerDebugContext {
    moduleMutationRecords: ServerDebugModuleMutationRecord[];
}

declare module '@nuxt/schema' {
    interface NuxtHooks {
        /**
         * Called before devtools starts. Useful to detect if devtools is enabled.
         */
        'devtools:before': () => void;
        /**
         * Called after devtools is initialized.
         */
        'devtools:initialized': (info: NuxtDevtoolsInfo) => void;
        /**
         * Hooks to extend devtools tabs.
         */
        'devtools:customTabs': (tabs: ModuleCustomTab[]) => void;
        /**
         * Retrigger update for custom tabs, `devtools:customTabs` will be called again.
         */
        'devtools:customTabs:refresh': () => void;
        /**
         * Register a terminal.
         */
        'devtools:terminal:register': (terminal: TerminalState) => void;
        /**
         * Write to a terminal.
         *
         * Returns true if terminal is found.
         */
        'devtools:terminal:write': (_: {
            id: string;
            data: string;
        }) => void;
        /**
         * Remove a terminal from devtools.
         *
         * Returns true if terminal is found and deleted.
         */
        'devtools:terminal:remove': (_: {
            id: string;
        }) => void;
        /**
         * Mark a terminal as terminated.
         */
        'devtools:terminal:exit': (_: {
            id: string;
            code?: number;
        }) => void;
    }
}
declare module '@nuxt/schema' {
    /**
     * Runtime Hooks
     */
    interface RuntimeNuxtHooks {
        /**
         * On terminal data.
         */
        'devtools:terminal:data': (payload: {
            id: string;
            data: string;
        }) => void;
    }
}

export type { RouteInfo as $, AnalyzeBuildMeta as A, BasicModuleInfo as B, ClientFunctions as C, ModuleStaticInfo as D, ModuleStats as E, ModuleTabInfo as F, GetWizardArgs as G, HookInfo as H, ImageMeta as I, ModuleType as J, ModuleVNodeView as K, LoadingTimeMetric as L, ModuleCustomTab as M, NuxtDevtoolsInfo as N, ModuleView as O, PluginMetric as P, NpmCommandOptions as Q, NpmCommandType as R, SubprocessOptions as S, TerminalState as T, NuxtDevToolsOptions as U, NuxtDevtoolsServerContext as V, NuxtServerData as W, PackageManagerName as X, PackageUpdateInfo as Y, Payload as Z, PluginInfoWithMetic as _, ServerFunctions as a, ScannedNitroTasks as a0, ServerDebugContext as a1, ServerDebugModuleMutationRecord as a2, ServerRouteInfo as a3, ServerRouteInput as a4, ServerRouteInputType as a5, ServerTaskInfo as a6, TabCategory as a7, TerminalAction as a8, TerminalBase as a9, TerminalInfo as aa, VSCodeIntegrationOptions as ab, VSCodeTunnelOptions as ac, VueInspectorClient as ad, VueInspectorData as ae, WizardActions as af, WizardFunctions as ag, AnalyzeBuildsInfo as b, AssetEntry as c, AssetInfo as d, AssetType as e, AutoImportsWithMetadata as f, CategorizedTabs as g, ClientUpdateEvent as h, CodeServerOptions as i, CodeServerType as j, CodeSnippet as k, CompatibilityStatus as l, ComponentRelationship as m, ComponentWithRelationships as n, GitHubContributor as o, InstallModuleReturn as p, InstalledModuleInfo as q, MaintainerInfo as r, ModuleBuiltinTab as s, ModuleCompatibility as t, ModuleGlobalOptions as u, ModuleIframeTabLazyOptions as v, ModuleIframeView as w, ModuleLaunchAction as x, ModuleLaunchView as y, ModuleOptions as z };

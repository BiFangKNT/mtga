import { a as ServerFunctions, C as ClientFunctions, H as HookInfo, P as PluginMetric, L as LoadingTimeMetric } from './shared/devtools-kit.BE8MVpwl.js';
export { A as AnalyzeBuildMeta, b as AnalyzeBuildsInfo, c as AssetEntry, d as AssetInfo, e as AssetType, f as AutoImportsWithMetadata, B as BasicModuleInfo, g as CategorizedTabs, h as ClientUpdateEvent, i as CodeServerOptions, j as CodeServerType, k as CodeSnippet, l as CompatibilityStatus, m as ComponentRelationship, n as ComponentWithRelationships, G as GetWizardArgs, o as GitHubContributor, I as ImageMeta, p as InstallModuleReturn, q as InstalledModuleInfo, r as MaintainerInfo, s as ModuleBuiltinTab, t as ModuleCompatibility, M as ModuleCustomTab, u as ModuleGlobalOptions, v as ModuleIframeTabLazyOptions, w as ModuleIframeView, x as ModuleLaunchAction, y as ModuleLaunchView, z as ModuleOptions, D as ModuleStaticInfo, E as ModuleStats, F as ModuleTabInfo, J as ModuleType, K as ModuleVNodeView, O as ModuleView, Q as NpmCommandOptions, R as NpmCommandType, U as NuxtDevToolsOptions, N as NuxtDevtoolsInfo, V as NuxtDevtoolsServerContext, W as NuxtServerData, X as PackageManagerName, Y as PackageUpdateInfo, Z as Payload, _ as PluginInfoWithMetic, $ as RouteInfo, a0 as ScannedNitroTasks, a1 as ServerDebugContext, a2 as ServerDebugModuleMutationRecord, a3 as ServerRouteInfo, a4 as ServerRouteInput, a5 as ServerRouteInputType, a6 as ServerTaskInfo, S as SubprocessOptions, a7 as TabCategory, a8 as TerminalAction, a9 as TerminalBase, aa as TerminalInfo, T as TerminalState, ab as VSCodeIntegrationOptions, ac as VSCodeTunnelOptions, ad as VueInspectorClient, ae as VueInspectorData, af as WizardActions, ag as WizardFunctions } from './shared/devtools-kit.BE8MVpwl.js';
import { BirpcReturn } from 'birpc';
import { Hookable } from 'hookable';
import { NuxtApp } from 'nuxt/app';
import { AppConfig } from 'nuxt/schema';
import { $Fetch } from 'ofetch';
import { BuiltinLanguage } from 'shiki';
import { Ref } from 'vue';
import { StackFrame } from 'error-stack-parser-es';
import 'unimport';
import 'vue-router';
import 'nitropack';
import 'unstorage';
import 'vite';
import '@nuxt/schema';
import 'execa';

interface TimelineEventFunction {
    type: 'function';
    start: number;
    end?: number;
    name: string;
    args?: any[];
    result?: any;
    stacktrace?: StackFrame[];
    isPromise?: boolean;
}
interface TimelineServerState {
    timeSsrStart?: number;
}
interface TimelineEventRoute {
    type: 'route';
    start: number;
    end?: number;
    from: string;
    to: string;
}
interface TimelineOptions {
    enabled: boolean;
    stacktrace: boolean;
    arguments: boolean;
}
type TimelineEvent = TimelineEventFunction | TimelineEventRoute;
interface TimelineMetrics {
    events: TimelineEvent[];
    nonLiteralSymbol: symbol;
    options: TimelineOptions;
}
interface TimelineEventNormalized<T> {
    event: T;
    segment: TimelineEventsSegment;
    relativeStart: number;
    relativeWidth: number;
    layer: number;
}
interface TimelineEventsSegment {
    start: number;
    end: number;
    events: TimelineEvent[];
    functions: TimelineEventNormalized<TimelineEventFunction>[];
    route?: TimelineEventNormalized<TimelineEventRoute>;
    duration: number;
    previousGap?: number;
}

interface DevToolsFrameState {
    width: number;
    height: number;
    top: number;
    left: number;
    open: boolean;
    route: string;
    position: 'left' | 'right' | 'bottom' | 'top';
    closeOnOutsideClick: boolean;
    minimizePanelInactive: number;
}
interface NuxtDevtoolsClientHooks {
    /**
     * When the DevTools navigates, used for persisting the current tab
     */
    'devtools:navigate': (path: string) => void;
    /**
     * Event emitted when the component inspector is clicked
     */
    'host:inspector:click': (path: string) => void;
    /**
     * Event to close the component inspector
     */
    'host:inspector:close': () => void;
    /**
     * Triggers reactivity manually, since Vue won't be reactive across frames)
     */
    'host:update:reactivity': () => void;
    /**
     * Host action to control the DevTools navigation
     */
    'host:action:navigate': (path: string) => void;
    /**
     * Host action to reload the DevTools
     */
    'host:action:reload': () => void;
}
/**
 * Host client from the App
 */
interface NuxtDevtoolsHostClient {
    nuxt: NuxtApp;
    hooks: Hookable<NuxtDevtoolsClientHooks>;
    getIframe: () => HTMLIFrameElement | undefined;
    inspector?: {
        enable: () => void;
        disable: () => void;
        toggle: () => void;
        isEnabled: Ref<boolean>;
        isAvailable: Ref<boolean>;
    };
    devtools: {
        close: () => void;
        open: () => void;
        toggle: () => void;
        reload: () => void;
        navigate: (path: string) => void;
        /**
         * Popup the DevTools frame into Picture-in-Picture mode
         *
         * Requires Chrome 111 with experimental flag enabled.
         *
         * Function is undefined when not supported.
         *
         * @see https://developer.chrome.com/docs/web-platform/document-picture-in-picture/
         */
        popup?: () => any;
    };
    app: {
        reload: () => void;
        navigate: (path: string, hard?: boolean) => void;
        appConfig: AppConfig;
        colorMode: Ref<'dark' | 'light'>;
        frameState: Ref<DevToolsFrameState>;
        $fetch: $Fetch;
    };
    metrics: {
        clientHooks: () => HookInfo[];
        clientPlugins: () => PluginMetric[] | undefined;
        clientTimeline: () => TimelineMetrics | undefined;
        loading: () => LoadingTimeMetric;
    };
    /**
     * A counter to trigger reactivity updates
     */
    revision: Ref<number>;
    /**
     * Update client
     * @internal
     */
    syncClient: () => NuxtDevtoolsHostClient;
}
interface CodeHighlightOptions {
    grammarContextCode?: string;
}
interface NuxtDevtoolsClient {
    rpc: BirpcReturn<ServerFunctions, ClientFunctions>;
    renderCodeHighlight: (code: string, lang?: BuiltinLanguage, options?: CodeHighlightOptions) => {
        code: string;
        supported: boolean;
    };
    renderMarkdown: (markdown: string) => string;
    colorMode: string;
    extendClientRpc: <ServerFunctions extends object = Record<string, unknown>, ClientFunctions extends object = Record<string, unknown>>(name: string, functions: ClientFunctions) => BirpcReturn<ServerFunctions, ClientFunctions>;
}
interface NuxtDevtoolsIframeClient {
    host: NuxtDevtoolsHostClient;
    devtools: NuxtDevtoolsClient;
}
interface NuxtDevtoolsGlobal {
    setClient: (client: NuxtDevtoolsHostClient) => void;
}

export { ClientFunctions, HookInfo, LoadingTimeMetric, PluginMetric, ServerFunctions };
export type { CodeHighlightOptions, DevToolsFrameState, NuxtDevtoolsClient, NuxtDevtoolsClientHooks, NuxtDevtoolsGlobal, NuxtDevtoolsHostClient, NuxtDevtoolsIframeClient, TimelineEvent, TimelineEventFunction, TimelineEventNormalized, TimelineEventRoute, TimelineEventsSegment, TimelineMetrics, TimelineOptions, TimelineServerState };

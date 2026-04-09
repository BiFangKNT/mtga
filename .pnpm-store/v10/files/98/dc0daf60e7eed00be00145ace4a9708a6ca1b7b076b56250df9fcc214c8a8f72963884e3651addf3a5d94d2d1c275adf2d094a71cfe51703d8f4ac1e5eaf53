import type { App, EffectScope, Ref, VNode, onErrorCaptured } from 'vue';
import type { RouteLocationNormalizedLoaded } from 'vue-router';
import type { Hookable } from 'hookable';
import type { UseContext } from 'unctx';
import type { SSRContext, createRenderer } from 'vue-bundle-renderer/runtime';
import type { EventHandlerRequest, H3Event } from '@nuxt/nitro-server/h3';
import type { RenderResponse } from 'nitropack/types';
import type { LogObject } from 'consola';
import type { VueHeadClient } from '@unhead/vue/types';
import type { NuxtAppLiterals } from 'nuxt/app';
import type { NuxtIslandContext } from './types.js';
import type { RouteMiddleware } from './composables/router.js';
import type { NuxtError } from './composables/error.js';
import type { AsyncDataExecuteOptions, AsyncDataRequestStatus, DebouncedReturn } from './composables/asyncData.js';
import type { NuxtAppManifestMeta } from './composables/manifest.js';
import type { LoadingIndicator } from './composables/loading-indicator.js';
import type { RouteAnnouncer } from './composables/route-announcer.js';
import type { NuxtAnnouncer } from './composables/announcer.js';
import type { AppConfig, AppConfigInput, RuntimeConfig } from 'nuxt/schema';
export declare function getNuxtAppCtx(id?: string): UseContext<NuxtApp>;
type HookResult = Promise<void> | void;
type AppRenderedContext = {
    ssrContext: NuxtApp['ssrContext'];
    renderResult: null | Awaited<ReturnType<ReturnType<typeof createRenderer>['renderToString']>>;
};
export interface RuntimeNuxtHooks {
    'app:created': (app: App<Element>) => HookResult;
    'app:beforeMount': (app: App<Element>) => HookResult;
    'app:mounted': (app: App<Element>) => HookResult;
    'app:rendered': (ctx: AppRenderedContext) => HookResult;
    'app:redirected': () => HookResult;
    'app:suspense:resolve': (Component?: VNode) => HookResult;
    'app:error': (err: any) => HookResult;
    'app:error:cleared': (options: {
        redirect?: string;
    }) => HookResult;
    'app:chunkError': (options: {
        error: any;
    }) => HookResult;
    'app:data:refresh': (keys?: string[]) => HookResult;
    'app:manifest:update': (meta?: NuxtAppManifestMeta) => HookResult;
    'dev:ssr-logs': (logs: LogObject[]) => HookResult;
    'link:prefetch': (link: string) => HookResult;
    'page:start': (Component?: VNode) => HookResult;
    'page:finish': (Component?: VNode) => HookResult;
    'page:transition:finish': (Component?: VNode) => HookResult;
    'page:view-transition:start': (transition: ViewTransition) => HookResult;
    'page:loading:start': () => HookResult;
    'page:loading:end': () => HookResult;
    'vue:setup': () => void;
    'vue:error': (...args: Parameters<Parameters<typeof onErrorCaptured>[0]>) => HookResult;
}
export interface NuxtSSRContext extends SSRContext {
    url: string;
    event: H3Event;
    runtimeConfig: RuntimeConfig;
    noSSR: boolean;
    /** whether we are rendering an SSR error */
    error?: boolean;
    nuxt: _NuxtApp;
    payload: Partial<NuxtPayload>;
    head: VueHeadClient;
    /** This is used solely to render runtime config with SPA renderer. */
    config?: Pick<RuntimeConfig, 'public' | 'app'>;
    teleports?: Record<string, string>;
    islandContext?: NuxtIslandContext;
    /** @internal */
    ['~renderResponse']?: Partial<RenderResponse>;
    /** @internal */
    ['~payloadReducers']: Record<string, (data: any) => any>;
    /** @internal */
    ['~sharedPrerenderCache']?: {
        get<T = unknown>(key: string): Promise<T> | undefined;
        set<T>(key: string, value: Promise<T>): Promise<void>;
    };
    /** @internal */
    ['~preloadManifest']?: boolean;
    /** @internal */
    ['~lazyHydratedModules']?: Set<string>;
}
export interface NuxtPayload {
    path?: string;
    serverRendered?: boolean;
    prerenderedAt?: number;
    data: Record<string, any>;
    state: Record<string, any>;
    once: Set<string>;
    config?: Pick<RuntimeConfig, 'public' | 'app'>;
    error?: NuxtError | undefined;
    _errors: Record<string, NuxtError | undefined>;
    [key: string]: unknown;
}
interface _NuxtApp {
    'vueApp': App<Element>;
    'versions': Record<string, string>;
    'hooks': Hookable<RuntimeNuxtHooks>;
    'hook': _NuxtApp['hooks']['hook'];
    'callHook': _NuxtApp['hooks']['callHook'];
    'runWithContext': <T extends () => any>(fn: T) => ReturnType<T> | Promise<Awaited<ReturnType<T>>>;
    [key: string]: unknown;
    /** @internal */
    '_cookies'?: Record<string, unknown>;
    '_cookiesChanged'?: Record<string, boolean>;
    /**
     * The id of the Nuxt application.
     * @internal */
    '_id': string;
    /** @internal */
    '_scope': EffectScope;
    /** @internal */
    '_asyncDataPromises': Record<string, Promise<any> | undefined>;
    /** @internal */
    '_asyncData': Record<string, {
        data: Ref<unknown>;
        pending: Ref<boolean>;
        error: Ref<Error | undefined>;
        status: Ref<AsyncDataRequestStatus>;
        execute: (opts?: AsyncDataExecuteOptions) => Promise<void>;
        /** @internal */
        _default: () => unknown;
        /** @internal */
        _deps: number;
        /** @internal */
        _off: () => void;
        /** @internal */
        _init: boolean;
        /** @internal */
        _execute: DebouncedReturn<[opts?: AsyncDataExecuteOptions | undefined], void>;
        /** @internal */
        _hash?: Record<string, string | undefined>;
        /** @internal */
        _abortController?: AbortController;
    } | undefined>;
    /** @internal */
    '_state': Record<string, {
        /** @internal */
        _default: () => unknown;
    } | undefined>;
    /** @internal */
    '_loadingIndicator'?: LoadingIndicator;
    /** @internal */
    '_loadingIndicatorDeps'?: number;
    /** @internal */
    '_middleware': {
        global: RouteMiddleware[];
        named: Record<string, RouteMiddleware>;
    };
    /** @internal */
    '_processingMiddleware'?: string | boolean;
    /** @internal */
    '_once': {
        [key: string]: Promise<any>;
    };
    /** @internal */
    '_observer'?: {
        observe: (element: Element, callback: () => void) => () => void;
    };
    /** @internal */
    '_appConfig': AppConfig;
    /** @internal */
    '_route': RouteLocationNormalizedLoaded & {
        sync?: () => void;
    };
    /** @internal */
    '_islandPromises'?: Record<string, Promise<any>>;
    /** @internal */
    '_payloadRevivers': Record<string, (data: any) => any>;
    /** @internal */
    '_routeAnnouncer'?: RouteAnnouncer;
    /** @internal */
    '_routeAnnouncerDeps'?: number;
    /** @internal */
    '~transitionPromise'?: Promise<void>;
    /** @internal */
    '~transitionFinish'?: () => void;
    /** @internal */
    '_announcer'?: NuxtAnnouncer;
    /** @internal */
    '_announcerDeps'?: number;
    '$config': RuntimeConfig;
    'isHydrating'?: boolean;
    'deferHydration': () => () => void | Promise<void>;
    'ssrContext'?: NuxtSSRContext;
    'payload': NuxtPayload;
    'static': {
        data: Record<string, any>;
    };
    'provide': (name: string, value: any) => void;
}
export interface NuxtApp extends _NuxtApp {
}
export declare const NuxtPluginIndicator = "__nuxt_plugin";
export interface PluginMeta {
    name?: string;
    enforce?: 'pre' | 'default' | 'post';
    /**
     * Await for other named plugins to finish before running this plugin.
     */
    dependsOn?: NuxtAppLiterals['pluginName'][];
    /**
     * This allows more granular control over plugin order and should only be used by advanced users.
     * It overrides the value of `enforce` and is used to sort plugins.
     */
    order?: number;
}
export interface PluginEnvContext {
    /**
     * This enable the plugin for islands components.
     * Require `experimental.componentsIslands`.
     * @default true
     */
    islands?: boolean;
}
export interface ResolvedPluginMeta {
    name?: string;
    parallel?: boolean;
}
export interface Plugin<Injections extends Record<string, unknown> = Record<string, unknown>> {
    (nuxt: _NuxtApp): Promise<void> | Promise<{
        provide?: Injections;
    }> | void | {
        provide?: Injections;
    };
    [NuxtPluginIndicator]?: true;
    meta?: ResolvedPluginMeta;
}
export interface ObjectPlugin<Injections extends Record<string, unknown> = Record<string, unknown>> extends PluginMeta {
    hooks?: Partial<RuntimeNuxtHooks>;
    setup?: Plugin<Injections>;
    env?: PluginEnvContext;
    /**
     * Execute plugin in parallel with other parallel plugins.
     * @default false
     */
    parallel?: boolean;
    /**
     * @internal
     */
    _name?: string;
}
/** @deprecated Use `ObjectPlugin` */
export type ObjectPluginInput<Injections extends Record<string, unknown> = Record<string, unknown>> = ObjectPlugin<Injections>;
export interface CreateOptions {
    vueApp: NuxtApp['vueApp'];
    ssrContext?: NuxtApp['ssrContext'];
    /**
     * The id of the Nuxt application, overrides the default id specified in the Nuxt config (default: `nuxt-app`).
     */
    id?: NuxtApp['_id'];
}
/** @since 3.0.0 */
export declare function createNuxtApp(options: CreateOptions): NuxtApp;
/** @since 3.12.0 */
export declare function registerPluginHooks(nuxtApp: NuxtApp, plugin: Plugin & ObjectPlugin<any>): void;
/** @since 3.0.0 */
export declare function applyPlugin(nuxtApp: NuxtApp, plugin: Plugin & ObjectPlugin<any>): Promise<void>;
/** @since 3.0.0 */
export declare function applyPlugins(nuxtApp: NuxtApp, plugins: Array<Plugin & ObjectPlugin<any>>): Promise<void>;
/** @since 3.0.0 */
export declare function defineNuxtPlugin<T extends Record<string, unknown>>(plugin: Plugin<T> | ObjectPlugin<T>): Plugin<T> & ObjectPlugin<T>;
export declare const definePayloadPlugin: typeof defineNuxtPlugin;
/** @since 3.0.0 */
export declare function isNuxtPlugin(plugin: unknown): plugin is Plugin;
/**
 * Ensures that the setup function passed in has access to the Nuxt instance via `useNuxtApp`.
 * @param nuxt A Nuxt instance
 * @param setup The function to call
 * @since 3.0.0
 */
export declare function callWithNuxt<T extends (...args: any[]) => any>(nuxt: NuxtApp | _NuxtApp, setup: T, args?: Parameters<T>): Promise<ReturnType<T>>;
/**
 * Returns the current Nuxt instance.
 *
 * Returns `null` if Nuxt instance is unavailable.
 * @since 3.10.0
 */
export declare function tryUseNuxtApp(): NuxtApp | null;
/**
 * Returns the current Nuxt instance.
 *
 * Throws an error if Nuxt instance is unavailable.
 * @since 3.0.0
 */
export declare function useNuxtApp(): NuxtApp;
/** @since 3.0.0 */
export declare function useRuntimeConfig(_event?: H3Event<EventHandlerRequest>): RuntimeConfig;
/** @since 3.0.0 */
export declare function defineAppConfig<C extends AppConfigInput>(config: C): C;
export {};

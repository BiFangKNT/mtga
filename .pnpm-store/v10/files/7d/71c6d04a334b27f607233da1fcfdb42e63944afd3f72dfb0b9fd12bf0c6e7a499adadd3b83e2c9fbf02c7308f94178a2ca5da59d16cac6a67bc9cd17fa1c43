import type { MaybeRefOrGetter, MultiWatchSources, Ref } from 'vue';
import type { NuxtApp } from '../nuxt.js';
import type { NuxtError } from './error.js';
export type AsyncDataRequestStatus = 'idle' | 'pending' | 'success' | 'error';
export type _Transform<Input = any, Output = any> = (input: Input) => Output | Promise<Output>;
export type AsyncDataHandler<ResT> = (nuxtApp: NuxtApp, options: {
    signal: AbortSignal;
}) => Promise<ResT>;
export type PickFrom<T, K extends Array<string>> = T extends Array<any> ? T : T extends Record<string, any> ? keyof T extends K[number] ? T : K[number] extends never ? T : Pick<T, K[number]> : T;
export type KeysOf<T> = Array<T extends T ? keyof T extends string ? keyof T : never : never>;
export type KeyOfRes<Transform extends _Transform> = KeysOf<ReturnType<Transform>>;
export type { MultiWatchSources };
export type NoInfer<T> = [T][T extends any ? 0 : never];
export type AsyncDataRefreshCause = 'initial' | 'refresh:hook' | 'refresh:manual' | 'watch';
export interface AsyncDataOptions<ResT, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined> {
    /**
     * Whether to fetch on the server side.
     * @default true
     */
    server?: boolean;
    /**
     * Whether to resolve the async function after loading the route, instead of blocking client-side navigation
     * @default false
     */
    lazy?: boolean;
    /**
     * a factory function to set the default value of the data, before the async function resolves - useful with the `lazy: true` or `immediate: false` options
     */
    default?: () => DefaultT | Ref<DefaultT>;
    /**
     * Provide a function which returns cached data.
     * An `undefined` return value will trigger a fetch.
     * Default is `key => nuxt.isHydrating ? nuxt.payload.data[key] : nuxt.static.data[key]` which only caches data when payloadExtraction is enabled.
     */
    getCachedData?: (key: string, nuxtApp: NuxtApp, context: {
        cause: AsyncDataRefreshCause;
    }) => NoInfer<DataT> | undefined;
    /**
     * A function that can be used to alter handler function result after resolving.
     * Do not use it along with the `pick` option.
     */
    transform?: _Transform<ResT, DataT>;
    /**
     * Only pick specified keys in this array from the handler function result.
     * Do not use it along with the `transform` option.
     */
    pick?: PickKeys;
    /**
     * Watch reactive sources to auto-refresh when changed
     */
    watch?: MultiWatchSources;
    /**
     * When set to false, will prevent the request from firing immediately
     * @default true
     */
    immediate?: boolean;
    /**
     * Return data in a deep ref object (it is false by default). It can be set to false to return data in a shallow ref object, which can improve performance if your data does not need to be deeply reactive.
     */
    deep?: boolean;
    /**
     * Avoid fetching the same key more than once at a time
     * @default 'cancel'
     */
    dedupe?: 'cancel' | 'defer';
    /**
     * A timeout in milliseconds after which the request will be aborted if it has not resolved yet.
     */
    timeout?: number;
}
export interface AsyncDataExecuteOptions {
    /**
     * Force a refresh, even if there is already a pending request. Previous requests will
     * not be cancelled, but their result will not affect the data/pending state - and any
     * previously awaited promises will not resolve until this new request resolves.
     */
    dedupe?: 'cancel' | 'defer';
    cause?: AsyncDataRefreshCause;
    /** @internal */
    cachedData?: any;
    signal?: AbortSignal;
    timeout?: number;
}
export interface _AsyncData<DataT, ErrorT> {
    data: Ref<DataT>;
    pending: Ref<boolean>;
    refresh: (opts?: AsyncDataExecuteOptions) => Promise<void>;
    execute: (opts?: AsyncDataExecuteOptions) => Promise<void>;
    clear: () => void;
    error: Ref<ErrorT | undefined>;
    status: Ref<AsyncDataRequestStatus>;
}
export type AsyncData<Data, Error> = _AsyncData<Data, Error> & Promise<_AsyncData<Data, Error>>;
export declare const createUseAsyncData: <FResT, FDataT = FResT, FPickKeys extends KeysOf<FDataT> = KeysOf<FDataT>, FDefaultT = undefined>(options?: Partial<AsyncDataOptions<FResT, FDataT, FPickKeys, FDefaultT>> | ((currentOptions: AsyncDataOptions<unknown>) => Partial<AsyncDataOptions<FResT, FDataT, FPickKeys, FDefaultT>>)) => {
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT>): AsyncData<PickFrom<DataT, PickKeys> | DefaultT, (NuxtErrorDataT extends Error | NuxtError ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT_1 = unknown, DataT_1 = ResT, PickKeys_1 extends KeysOf<DataT_1> = KeysOf<DataT_1>, DefaultT_1 = DataT_1>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT_1, PickKeys_1, DefaultT_1>): AsyncData<PickFrom<DataT_1, PickKeys_1> | DefaultT_1, (NuxtErrorDataT_1 extends Error | NuxtError ? NuxtErrorDataT_1 : NuxtError<NuxtErrorDataT_1>) | undefined>;
    <ResT, NuxtErrorDataT_2 = unknown, DataT_2 = ResT, PickKeys_2 extends KeysOf<DataT_2> = KeysOf<DataT_2>, DefaultT_2 = undefined>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT_2, PickKeys_2, DefaultT_2>): AsyncData<PickFrom<DataT_2, PickKeys_2> | DefaultT_2, (NuxtErrorDataT_2 extends Error | NuxtError ? NuxtErrorDataT_2 : NuxtError<NuxtErrorDataT_2>) | undefined>;
    <ResT, NuxtErrorDataT_3 = unknown, DataT_3 = ResT, PickKeys_3 extends KeysOf<DataT_3> = KeysOf<DataT_3>, DefaultT_3 = DataT_3>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT_3, PickKeys_3, DefaultT_3>): AsyncData<PickFrom<DataT_3, PickKeys_3> | DefaultT_3, (NuxtErrorDataT_3 extends Error | NuxtError ? NuxtErrorDataT_3 : NuxtError<NuxtErrorDataT_3>) | undefined>;
};
export declare const useAsyncData: {
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = DataT>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = DataT>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
};
export declare const useLazyAsyncData: {
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = DataT>(handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = undefined>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
    <ResT, NuxtErrorDataT = unknown, DataT = ResT, PickKeys extends KeysOf<DataT> = KeysOf<DataT>, DefaultT = DataT>(key: MaybeRefOrGetter<string>, handler: AsyncDataHandler<ResT>, opts?: AsyncDataOptions<ResT, DataT, PickKeys, DefaultT> | undefined): AsyncData<DefaultT | PickFrom<DataT, PickKeys>, (NuxtErrorDataT extends Error | NuxtError<unknown> ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>) | undefined>;
};
/** @since 3.1.0 */
export declare function useNuxtData<DataT = any>(key: string): {
    data: Ref<DataT | undefined>;
};
/** @since 3.0.0 */
export declare function refreshNuxtData(keys?: string | string[]): Promise<void>;
/** @since 3.0.0 */
export declare function clearNuxtData(keys?: string | string[] | ((key: string) => boolean)): void;
export type DebouncedReturn<ArgumentsT extends unknown[], ReturnT> = ((...args: ArgumentsT) => Promise<ReturnT>) & {
    cancel: () => void;
    flush: () => Promise<ReturnT> | undefined;
    isPending: () => boolean;
};
export type CreatedAsyncData<ResT, NuxtErrorDataT = unknown, DataT = ResT, DefaultT = undefined> = Omit<_AsyncData<DataT | DefaultT, (NuxtErrorDataT extends Error | NuxtError ? NuxtErrorDataT : NuxtError<NuxtErrorDataT>)>, 'clear' | 'refresh'> & {
    _off: () => void;
    _hash?: Record<string, string | undefined>;
    _default: () => unknown;
    _init: boolean;
    _deps: number;
    _execute: DebouncedReturn<[opts?: AsyncDataExecuteOptions | undefined], void>;
    _abortController?: AbortController;
};

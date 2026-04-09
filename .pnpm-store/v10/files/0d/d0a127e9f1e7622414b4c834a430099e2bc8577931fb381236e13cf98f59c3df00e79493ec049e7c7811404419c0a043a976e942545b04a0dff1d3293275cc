import type { Ref } from 'vue';
/**
 * Create a global reactive ref that will be hydrated but not shared across ssr requests
 * @since 3.0.0
 * @param key a unique key ensuring that data fetching can be properly de-duplicated across requests
 * @param init a function that provides initial value for the state when it's not initiated
 */
export declare function useState<T>(key?: string, init?: (() => T | Ref<T>)): Ref<T>;
export declare function useState<T>(init?: (() => T | Ref<T>)): Ref<T>;
export interface ClearNuxtStateOptions {
    /**
     * Reset the state to the initial value provided by the `init` function of `useState`
     * instead of setting it to `undefined`.
     *
     * When not specified, this defaults to the value of `experimental.defaults.useState.resetOnClear`
     * in your Nuxt config (which defaults to `true` with `compatibilityVersion: 5`).
     */
    reset?: boolean;
}
/** @since 3.6.0 */
export declare function clearNuxtState(keys?: string | string[] | ((key: string) => boolean), opts?: ClearNuxtStateOptions): void;

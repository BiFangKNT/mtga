export interface ReloadNuxtAppOptions {
    /**
     * Number of milliseconds in which to ignore future reload requests
     * @default {10000}
     */
    ttl?: number;
    /**
     * Force a reload even if one has occurred within the previously specified TTL.
     * @default {false}
     */
    force?: boolean;
    /**
     * Whether to dump the current Nuxt state to sessionStorage (as `nuxt:reload:state`).
     * @default {false}
     */
    persistState?: boolean;
    /**
     * The path to reload. If this is different from the current window location it will
     * trigger a navigation and add an entry in the browser history.
     * @default {window.location.pathname}
     */
    path?: string;
}
/** @since 3.3.0 */
export declare function reloadNuxtApp(options?: ReloadNuxtAppOptions): void;

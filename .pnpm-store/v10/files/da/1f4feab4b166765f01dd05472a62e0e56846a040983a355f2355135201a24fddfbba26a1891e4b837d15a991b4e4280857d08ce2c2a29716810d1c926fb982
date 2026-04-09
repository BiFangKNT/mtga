type CallOnceOptions = {
    mode?: 'navigation' | 'render';
};
/**
 * An SSR-friendly utility to call a method once
 * @param key a unique key ensuring the function can be properly de-duplicated across requests
 * @param fn a function to call
 * @param options Setup the mode, e.g. to re-execute on navigation
 * @see https://nuxt.com/docs/4.x/api/utils/call-once
 * @since 3.9.0
 */
export declare function callOnce(key?: string, fn?: (() => any | Promise<any>), options?: CallOnceOptions): Promise<void>;
export declare function callOnce(fn?: (() => any | Promise<any>), options?: CallOnceOptions): Promise<void>;
export {};

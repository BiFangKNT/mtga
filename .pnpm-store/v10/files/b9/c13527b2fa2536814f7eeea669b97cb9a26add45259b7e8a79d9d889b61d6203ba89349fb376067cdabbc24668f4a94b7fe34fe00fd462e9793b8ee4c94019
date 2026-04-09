import type { Ref } from 'vue';
import type { CookieParseOptions, CookieSerializeOptions } from 'cookie-es';
type _CookieOptions = Omit<CookieSerializeOptions & CookieParseOptions, 'decode' | 'encode'>;
export interface CookieOptions<T = any> extends _CookieOptions {
    decode?(value: string): T;
    encode?(value: T): string;
    default?: () => T | Ref<T>;
    watch?: boolean | 'shallow';
    readonly?: boolean;
    /**
     * Refresh cookie expiration even when the value remains unchanged.
     *
     * By default, a cookie is only rewritten when its value changes.
     * When `refresh` is set to `true`, the cookie will be re-written
     * on every explicit assignment (e.g. `cookie.value = cookie.value`),
     * extending its expiration even if the value is the same.
     *
     * Note: the expiration is not refreshed automatically — you must
     * assign to `cookie.value` to trigger the refresh.
     *
     * @default false
     */
    refresh?: boolean;
}
export interface CookieRef<T> extends Ref<T> {
}
/** @since 3.0.0 */
export declare function useCookie<T = string | null | undefined>(name: string, _opts?: CookieOptions<T> & {
    readonly?: false;
}): CookieRef<T>;
export declare function useCookie<T = string | null | undefined>(name: string, _opts: CookieOptions<T> & {
    readonly: true;
}): Readonly<CookieRef<T>>;
/** @since 3.10.0 */
export declare function refreshCookie(name: string): void;
export {};

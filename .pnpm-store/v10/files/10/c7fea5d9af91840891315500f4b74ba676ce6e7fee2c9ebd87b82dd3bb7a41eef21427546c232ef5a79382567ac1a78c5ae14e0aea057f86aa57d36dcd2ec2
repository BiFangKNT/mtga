import type { H3Error } from '@nuxt/nitro-server/h3';
import type { Ref } from 'vue';
import type { NuxtPayload } from '../nuxt.js';
export declare const NUXT_ERROR_SIGNATURE = "__nuxt_error";
/** @since 3.0.0 */
export declare const useError: () => Ref<NuxtPayload["error"]>;
export interface NuxtError<DataT = unknown> extends Omit<H3Error<DataT>, 'statusCode' | 'statusMessage'>, Error {
    error?: true;
    status?: number;
    statusText?: string;
    /** @deprecated Use `status` */
    statusCode?: H3Error<DataT>['statusCode'];
    /** @deprecated Use `statusText` */
    statusMessage?: H3Error<DataT>['statusMessage'];
}
/** @since 3.0.0 */
export declare const showError: <DataT = unknown>(error: string | Error | (Partial<NuxtError<DataT>> & {
    status?: number;
    statusText?: string;
})) => NuxtError<DataT>;
/** @since 3.0.0 */
export declare const clearError: (options?: {
    redirect?: string;
}) => Promise<void>;
/** @since 3.0.0 */
export declare const isNuxtError: <DataT = unknown>(error: unknown) => error is NuxtError<DataT>;
/** @since 3.0.0 */
export declare const createError: <DataT = unknown>(error: string | Error | Partial<NuxtError<DataT>>) => NuxtError<DataT>;

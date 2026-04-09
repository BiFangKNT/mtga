import type { AppConfig } from 'nuxt/schema';
export type DeepPartial<T> = T extends Function ? T : T extends Record<string, any> ? {
    [P in keyof T]?: DeepPartial<T[P]>;
} : T;
export declare const _getAppConfig: () => AppConfig;
export declare function useAppConfig(): AppConfig;
export declare function _replaceAppConfig(newConfig: AppConfig): void;
/**
 * Deep assign the current appConfig with the new one.
 *
 * Will preserve existing properties.
 */
export declare function updateAppConfig(appConfig: DeepPartial<AppConfig>): void;

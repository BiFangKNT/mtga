import type { H3Event } from '@nuxt/nitro-server/h3';
import type { NitroRouteRules } from 'nitropack/types';
export interface NuxtAppManifestMeta {
    id: string;
    timestamp: number;
}
export interface NuxtAppManifest extends NuxtAppManifestMeta {
    prerendered: string[];
}
/** @since 3.7.4 */
export declare function getAppManifest(): Promise<NuxtAppManifest>;
/** @since 3.7.4 */
export declare function getRouteRules(event: H3Event): NitroRouteRules;
export declare function getRouteRules(options: {
    path: string;
}): Record<string, any>;
/** @deprecated use `getRouteRules({ path })` instead */
export declare function getRouteRules(url: string): Record<string, any>;

import type { NuxtIslandResponse, NuxtSSRContext } from "nuxt/app";
/**
* remove the root node from the html body
*/
export declare function getServerComponentHTML(body: string): string;
export declare function getSlotIslandResponse(ssrContext: NuxtSSRContext): NuxtIslandResponse["slots"];
export declare function getClientIslandResponse(ssrContext: NuxtSSRContext): NuxtIslandResponse["components"];
export declare function getComponentSlotTeleport(clientUid: string, teleports: Record<string, string>): Record<string, string>;
export declare function replaceIslandTeleports(ssrContext: NuxtSSRContext, html: string): string;

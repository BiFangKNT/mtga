import type { NitroRouteRules, RenderResponse } from "nitropack/types";
import type { Script } from "@unhead/vue";
import type { NuxtPayload, NuxtSSRContext } from "nuxt/app";
export declare function renderPayloadResponse(ssrContext: NuxtSSRContext): RenderResponse;
export declare function renderPayloadJsonScript(opts: {
	ssrContext: NuxtSSRContext;
	data?: any;
	src?: string;
}): Script[];
export declare function renderPayloadScript(opts: {
	ssrContext: NuxtSSRContext;
	routeOptions: NitroRouteRules;
	data?: any;
	src?: string;
}): Script[];
interface SplitPayload {
	initial: Omit<NuxtPayload, "data">;
	payload: {
		data?: NuxtPayload["data"];
		prerenderedAt?: NuxtPayload["prerenderedAt"];
	};
}
export declare function splitPayload(ssrContext: NuxtSSRContext): SplitPayload;
export {};

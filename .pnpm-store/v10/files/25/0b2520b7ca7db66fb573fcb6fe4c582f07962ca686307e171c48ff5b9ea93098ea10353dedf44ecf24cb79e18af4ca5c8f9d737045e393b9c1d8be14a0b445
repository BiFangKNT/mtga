import { useStorage } from "nitropack/runtime";
// @ts-expect-error virtual file
import { NUXT_RUNTIME_PAYLOAD_EXTRACTION, NUXT_SHARED_DATA } from "#internal/nuxt/nitro-config.mjs";
export const payloadCache = import.meta.prerender ? useStorage("internal:nuxt:prerender:payload") : NUXT_RUNTIME_PAYLOAD_EXTRACTION ? useStorage("cache:nuxt:payload") : null;
export const islandCache = import.meta.prerender ? useStorage("internal:nuxt:prerender:island") : null;
export const islandPropCache = import.meta.prerender ? useStorage("internal:nuxt:prerender:island-props") : null;
export const sharedPrerenderPromises = import.meta.prerender && NUXT_SHARED_DATA ? new Map() : null;
const sharedPrerenderKeys = new Set();
export const sharedPrerenderCache = import.meta.prerender && NUXT_SHARED_DATA ? {
	get(key) {
		if (sharedPrerenderKeys.has(key)) {
			return sharedPrerenderPromises.get(key) ?? useStorage("internal:nuxt:prerender:shared").getItem(key);
		}
	},
	async set(key, value) {
		sharedPrerenderKeys.add(key);
		sharedPrerenderPromises.set(key, value);
		useStorage("internal:nuxt:prerender:shared").setItem(key, await value).finally(() => sharedPrerenderPromises.delete(key));
	}
} : null;

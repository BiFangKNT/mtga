import { joinRelativeURL } from "ufo";
import { useRuntimeConfig } from "nitropack/runtime";
export function baseURL() {
	// TODO: support passing event to `useRuntimeConfig`
	return useRuntimeConfig().app.baseURL;
}
export function buildAssetsDir() {
	// TODO: support passing event to `useRuntimeConfig`
	return useRuntimeConfig().app.buildAssetsDir;
}
export function buildAssetsURL(...path) {
	return joinRelativeURL(publicAssetsURL(), buildAssetsDir(), ...path);
}
export function publicAssetsURL(...path) {
	// TODO: support passing event to `useRuntimeConfig`
	const app = useRuntimeConfig().app;
	const publicBase = app.cdnURL || app.baseURL;
	return path.length ? joinRelativeURL(publicBase, ...path) : publicBase;
}

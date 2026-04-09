import type { RendererContext } from "vue-bundle-renderer/runtime";
import type { NuxtSSRContext } from "nuxt/app";
interface Renderer {
	rendererContext: RendererContext;
	renderToString(ssrContext: NuxtSSRContext): Promise<{
		html: string;
		renderResourceHeaders: () => Record<string, string>;
		renderResourceHints: () => string;
		renderStyles: () => string;
		renderScripts: () => string;
	}>;
}
export declare const getSSRRenderer: () => Promise<Renderer>;
export declare function getRenderer(ssrContext: NuxtSSRContext): Promise<Renderer>;
export declare const getSSRStyles: () => Promise<Record<string, () => Promise<string[]>>>;
export {};

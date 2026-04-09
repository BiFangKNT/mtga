interface ResourceMeta {
    src?: string;
    file: string;
    css?: string[];
    assets?: string[];
    isEntry?: boolean;
    name?: string;
    names?: string[];
    isDynamicEntry?: boolean;
    sideEffects?: boolean;
    imports?: string[];
    dynamicImports?: string[];
    module?: boolean;
    prefetch?: boolean;
    preload?: boolean;
    resourceType?: 'audio' | 'document' | 'embed' | 'fetch' | 'font' | 'image' | 'object' | 'script' | 'style' | 'track' | 'worker' | 'video';
    mimeType?: string;
}
interface Manifest {
    [key: string]: ResourceMeta;
}
declare function defineManifest(manifest: Manifest): Manifest;

interface ModuleDependencies {
    scripts: Record<string, ResourceMeta>;
    styles: Record<string, ResourceMeta>;
    preload: Record<string, ResourceMeta>;
    prefetch: Record<string, ResourceMeta>;
}
interface SSRContext {
    renderResourceHints?: (...args: unknown[]) => unknown;
    renderScripts?: (...args: unknown[]) => unknown;
    renderStyles?: (...args: unknown[]) => unknown;
    modules?: Set<string>;
    _registeredComponents?: Set<string>;
    _requestDependencies?: ModuleDependencies;
    [key: string]: unknown;
}
interface RenderOptions {
    buildAssetsURL?: (id: string) => string;
    /** @deprecated Use `precomputed` instead for better performance */
    manifest?: Manifest;
    /** Precomputed dependency data */
    precomputed?: PrecomputedData;
}
interface RendererContext {
    buildAssetsURL: (id: string) => string;
    manifest?: Manifest;
    precomputed?: PrecomputedData;
    _dependencies: Record<string, ModuleDependencies>;
    _dependencySets: Record<string, ModuleDependencies>;
    _entrypoints: string[];
    updateManifest: (manifest: Manifest) => void;
}
interface LinkAttributes {
    rel: string | null;
    href: string;
    as?: string | null;
    type?: string | null;
    crossorigin?: '' | null;
}
declare function createRendererContext({ manifest, precomputed, buildAssetsURL }: RenderOptions): RendererContext;
declare function getModuleDependencies(id: string, rendererContext: RendererContext): ModuleDependencies;
declare function getAllDependencies(ids: Set<string>, rendererContext: RendererContext): ModuleDependencies;
declare function getRequestDependencies(ssrContext: SSRContext, rendererContext: RendererContext): ModuleDependencies;
declare function renderStyles(ssrContext: SSRContext, rendererContext: RendererContext): string;
declare function getResources(ssrContext: SSRContext, rendererContext: RendererContext): LinkAttributes[];
declare function renderResourceHints(ssrContext: SSRContext, rendererContext: RendererContext): string;
declare function renderResourceHeaders(ssrContext: SSRContext, rendererContext: RendererContext): Record<string, string>;
declare function getPreloadLinks(ssrContext: SSRContext, rendererContext: RendererContext): LinkAttributes[];
declare function getPrefetchLinks(ssrContext: SSRContext, rendererContext: RendererContext): LinkAttributes[];
declare function renderScripts(ssrContext: SSRContext, rendererContext: RendererContext): string;
type RenderFunction = (ssrContext: SSRContext, rendererContext: RendererContext) => unknown;
type CreateApp<App> = (ssrContext: SSRContext) => App | Promise<App>;
type ImportOf<T> = T | {
    default: T;
} | Promise<T> | Promise<{
    default: T;
}>;
type RenderToString<App> = (app: App, ssrContext: SSRContext) => string | Promise<string>;
declare function createRenderer<App>(createApp: ImportOf<CreateApp<App>>, renderOptions: RenderOptions & {
    renderToString: RenderToString<App>;
}): {
    rendererContext: RendererContext;
    renderToString(ssrContext: SSRContext): Promise<{
        html: string;
        renderResourceHeaders: () => Record<string, string>;
        renderResourceHints: () => string;
        renderStyles: () => string;
        renderScripts: () => string;
    }>;
};

interface PrecomputedData {
    /** Pre-resolved dependencies for each module */
    dependencies: Record<string, ModuleDependencies>;
    /** List of entry point module IDs */
    entrypoints: string[];
    /** Module metadata needed at runtime (file paths, etc.) */
    modules: Record<string, Pick<ResourceMeta, 'file' | 'resourceType' | 'mimeType' | 'module'>>;
}
/**
 * Build-time utility to precompute all module dependencies from a manifest.
 * This eliminates recursive dependency resolution at runtime.
 *
 * @param manifest The build manifest
 * @returns Serializable precomputed data for runtime use
 */
declare function precomputeDependencies(manifest: Manifest): PrecomputedData;

export { defineManifest as d, createRendererContext as e, getAllDependencies as f, getModuleDependencies as g, getRequestDependencies as h, getResources as i, renderResourceHints as j, renderResourceHeaders as k, getPreloadLinks as l, getPrefetchLinks as m, renderScripts as n, precomputeDependencies as p, createRenderer as q, renderStyles as r };
export type { Manifest as M, PrecomputedData as P, ResourceMeta as R, SSRContext as S, ModuleDependencies as a, RenderOptions as b, RendererContext as c, RenderFunction as o };

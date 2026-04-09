declare global {
    const __STATIC_CONTENT: KVNamespace | undefined;
    const __STATIC_CONTENT_MANIFEST: Record<string, string> | undefined;
}
type CacheControl = {
    browserTTL: number;
    edgeTTL: number;
    bypassCache: boolean;
};
type AssetManifestType = Record<string, string>;
type Options = {
    cacheControl: ((req: Request) => Partial<CacheControl>) | Partial<CacheControl>;
    ASSET_NAMESPACE: KVNamespace;
    ASSET_MANIFEST: AssetManifestType | string;
    mapRequestToAsset?: (req: Request, options?: Partial<Options>) => Request;
    defaultMimeType: string;
    defaultDocument: string;
    pathIsEncoded: boolean;
    defaultETag: "strong" | "weak";
};
declare class KVError extends Error {
    constructor(message?: string, status?: number);
    status: number;
}
declare class MethodNotAllowedError extends KVError {
    constructor(message?: string, status?: number);
}
declare class NotFoundError extends KVError {
    constructor(message?: string, status?: number);
}
declare class InternalError extends KVError {
    constructor(message?: string, status?: number);
}

/**
 * maps the path of incoming request to the request pathKey to look up
 * in bucket and in cache
 * e.g.  for a path '/' returns '/index.html' which serves
 * the content of bucket/index.html
 * @param {Request} request incoming request
 */
declare const mapRequestToAsset: (request: Request, options?: Partial<Options>) => Request<unknown, CfProperties<unknown>>;
/**
 * maps the path of incoming request to /index.html if it evaluates to
 * any HTML file.
 * @param {Request} request incoming request
 */
declare function serveSinglePageApp(request: Request, options?: Partial<Options>): Request;
/**
 * takes the path of the incoming request, gathers the appropriate content from KV, and returns
 * the response
 *
 * @param {FetchEvent} event the fetch event of the triggered request
 * @param {{mapRequestToAsset: (string: Request) => Request, cacheControl: {bypassCache:boolean, edgeTTL: number, browserTTL:number}, ASSET_NAMESPACE: any, ASSET_MANIFEST:any}} [options] configurable options
 * @param {CacheControl} [options.cacheControl] determine how to cache on Cloudflare and the browser
 * @param {typeof(options.mapRequestToAsset)} [options.mapRequestToAsset]  maps the path of incoming request to the request pathKey to look up
 * @param {Object | string} [options.ASSET_NAMESPACE] the binding to the namespace that script references
 * @param {any} [options.ASSET_MANIFEST] the map of the key to cache and store in KV
 * */
type Evt = {
    request: Request;
    waitUntil: (promise: Promise<unknown>) => void;
};
declare const getAssetFromKV: (event: Evt, options?: Partial<Options>) => Promise<Response>;

export { type CacheControl, InternalError, MethodNotAllowedError, NotFoundError, type Options, getAssetFromKV, mapRequestToAsset, serveSinglePageApp };

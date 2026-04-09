import * as stream from 'node:stream';
import { Duplex } from 'node:stream';
import http, { ServerResponse, IncomingMessage } from 'node:http';
import { EventEmitter } from 'node:events';
import net, { Socket } from 'node:net';

interface ProxyTargetDetailed {
    host?: string;
    port?: number | string;
    protocol?: string;
    hostname?: string;
    socketPath?: string;
    key?: string;
    passphrase?: string;
    pfx?: Buffer | string;
    cert?: string;
    ca?: string;
    ciphers?: string;
    secureProtocol?: string;
}
type ProxyTarget = string | URL | ProxyTargetDetailed;
/** Resolved proxy address — either TCP (host + port) or Unix socket. */
type ProxyAddr = {
    host?: string;
    port: number;
    socketPath?: undefined;
} | {
    host?: undefined;
    port?: undefined;
    socketPath: string;
};
interface ProxyServerOptions {
    /** URL string to be parsed. */
    target?: ProxyTarget;
    /** URL string to be parsed. */
    forward?: ProxyTarget;
    /** Object to be passed to http(s).request. */
    agent?: any;
    /** Object to be passed to https.createServer(). */
    ssl?: any;
    /** If you want to proxy websockets. */
    ws?: boolean;
    /** Adds x- forward headers. */
    xfwd?: boolean;
    /** Verify SSL certificate. */
    secure?: boolean;
    /** Explicitly specify if we are proxying to another proxy. */
    toProxy?: boolean;
    /** Specify whether you want to prepend the target's path to the proxy path. */
    prependPath?: boolean;
    /** Specify whether you want to ignore the proxy path of the incoming request. */
    ignorePath?: boolean;
    /** Local interface string to bind for outgoing connections. */
    localAddress?: string;
    /** Changes the origin of the host header to the target URL. */
    changeOrigin?: boolean;
    /** specify whether you want to keep letter case of response header key */
    preserveHeaderKeyCase?: boolean;
    /** Basic authentication i.e. 'user:password' to compute an Authorization header. */
    auth?: string;
    /** Rewrites the location hostname on (301 / 302 / 307 / 308) redirects, Default: null. */
    hostRewrite?: string;
    /** Rewrites the location host/ port on (301 / 302 / 307 / 308) redirects based on requested host/ port.Default: false. */
    autoRewrite?: boolean;
    /** Rewrites the location protocol on (301 / 302 / 307 / 308) redirects to 'http' or 'https'.Default: null. */
    protocolRewrite?: string;
    /** Rewrites domain of set-cookie headers. */
    cookieDomainRewrite?: false | string | {
        [oldDomain: string]: string;
    };
    /** Rewrites path of set-cookie headers. Default: false */
    cookiePathRewrite?: false | string | {
        [oldPath: string]: string;
    };
    /** Object with extra headers to be added to target requests. */
    headers?: {
        [header: string]: string;
    };
    /** Timeout (in milliseconds) when proxy receives no response from target. Default: 120000 (2 minutes) */
    proxyTimeout?: number;
    /** Timeout (in milliseconds) for incoming requests */
    timeout?: number;
    /** If set to true, none of the webOutgoing passes are called and it's your responsibility to appropriately return the response by listening and acting on the proxyRes event */
    selfHandleResponse?: boolean;
    /** Follow HTTP redirects from target. `true` = max 5 hops; number = custom max. */
    followRedirects?: boolean | number;
    /** Buffer */
    buffer?: stream.Stream;
}

type ResOfType<T extends "web" | "ws"> = T extends "ws" ? T extends "web" ? ServerResponse | Socket : Socket : T extends "web" ? ServerResponse : never;
type ProxyMiddleware<T extends ServerResponse | Socket> = (req: IncomingMessage, res: T, opts: ProxyServerOptions & {
    target: URL | ProxyTargetDetailed;
    forward: URL;
}, server: ProxyServer, head?: Buffer, callback?: (err: any, req: IncomingMessage, socket: T, url?: any) => void) => void | true;

interface ProxyServerEventMap<Req extends http.IncomingMessage = http.IncomingMessage, Res extends http.ServerResponse = http.ServerResponse> {
    error: [err: Error, req?: Req, res?: Res | net.Socket, target?: URL | ProxyTarget];
    start: [req: Req, res: Res, target: URL | ProxyTarget];
    econnreset: [err: Error, req: Req, res: Res, target: URL | ProxyTarget];
    proxyReq: [proxyReq: http.ClientRequest, req: Req, res: Res, options: ProxyServerOptions];
    proxyReqWs: [
        proxyReq: http.ClientRequest,
        req: Req,
        socket: net.Socket,
        options: ProxyServerOptions,
        head: any
    ];
    proxyRes: [proxyRes: http.IncomingMessage, req: Req, res: Res];
    end: [req: Req, res: Res, proxyRes: http.IncomingMessage];
    open: [proxySocket: net.Socket];
    /** @deprecated */
    proxySocket: [proxySocket: net.Socket];
    close: [proxyRes: Req, proxySocket: net.Socket, proxyHead: any];
}
declare class ProxyServer<Req extends http.IncomingMessage = http.IncomingMessage, Res extends http.ServerResponse = http.ServerResponse> extends EventEmitter<ProxyServerEventMap<Req, Res>> {
    private _server?;
    _webPasses: ProxyMiddleware<http.ServerResponse>[];
    _wsPasses: ProxyMiddleware<net.Socket>[];
    options: ProxyServerOptions;
    web: (req: http.IncomingMessage, res: http.ServerResponse, opts?: ProxyServerOptions, head?: any) => Promise<void>;
    ws: (req: http.IncomingMessage, socket: net.Socket, opts: ProxyServerOptions, head?: any) => Promise<void>;
    /**
     * Creates the proxy server with specified options.
     * @param options - Config object passed to the proxy
     */
    constructor(options?: ProxyServerOptions);
    /**
     * A function that wraps the object in a webserver, for your convenience
     * @param port - Port to listen on
     * @param hostname - The hostname to listen on
     */
    listen(port: number, hostname?: string): this;
    /**
     * A function that closes the inner webserver and stops listening on given port
     */
    close(callback?: () => void): void;
    before<Type extends "ws" | "web">(type: Type, passName: string, pass: ProxyMiddleware<ResOfType<Type>>): void;
    after<Type extends "ws" | "web">(type: Type, passName: string, pass: ProxyMiddleware<ResOfType<Type>>): void;
    /** @internal */
    _getPasses<Type extends "ws" | "web">(type: Type): ProxyMiddleware<ResOfType<Type>>[];
}
/**
 * Creates the proxy server.
 *
 * Examples:
 *
 *    httpProxy.createProxyServer({ .. }, 8000)
 *    // => '{ web: [Function], ws: [Function] ... }'
 *
 * @param {Object} Options Config object passed to the proxy
 *
 * @return {Object} Proxy Proxy object with handlers for `ws` and `web` requests
 *
 * @api public
 */
declare function createProxyServer(options?: ProxyServerOptions): ProxyServer<http.IncomingMessage, http.ServerResponse<http.IncomingMessage>>;

/**
 * Proxy a request to a specific server address (TCP host/port or Unix socket)
 * using web standard {@link Request}/{@link Response} interfaces.
 *
 * Note: Only plain HTTP is supported. HTTPS targets are not supported.
 *
 * @param addr - The target server address. Can be a URL string (`http://host:port`, `unix:/path`), or an object with `host`/`port` for TCP or `socketPath` for Unix sockets.
 * @param input - The request URL (string or URL) or a {@link Request} object.
 * @param inputInit - Optional {@link RequestInit} or {@link Request} to override method, headers, and body.
 */
declare function proxyFetch(addr: string | ProxyAddr, input: string | URL | Request, inputInit?: RequestInit | Request): Promise<Response>;

/**
 * Options for {@link proxyUpgrade}.
 */
interface ProxyUpgradeOptions {
    /**
     * Add `x-forwarded-for`, `x-forwarded-port`, and `x-forwarded-proto` headers.
     * Default: `true`.
     */
    xfwd?: boolean;
    /**
     * Rewrite the `Host` header to match the target.
     * Default: `false` (original host is kept).
     */
    changeOrigin?: boolean;
    /**
     * Extra headers to include in the upstream upgrade request.
     * Default: none.
     */
    headers?: Record<string, string>;
    /**
     * TLS options forwarded to `https.request`.
     * Default: none.
     */
    ssl?: Record<string, unknown>;
    /**
     * Whether to verify upstream TLS certificates.
     * Default: `true`.
     */
    secure?: boolean;
    /**
     * HTTP/HTTPS agent used for the upstream request.
     * Default: `false` (no keep-alive agent is used).
     */
    agent?: any;
    /**
     * Local interface address to bind for upstream connections.
     * Default: OS-selected local address.
     */
    localAddress?: string;
    /**
     * Basic auth credentials in `username:password` format.
     * Default: none.
     */
    auth?: string;
    /**
     * Prepend the target path to the proxied request path.
     * Default: `true`.
     */
    prependPath?: boolean;
    /**
     * Ignore the incoming request path when building the upstream path.
     * Default: `false` (incoming path is used).
     */
    ignorePath?: boolean;
    /**
     * Send absolute URL in request path when proxying to another proxy.
     * Default: `false` (path-only request target is used).
     */
    toProxy?: boolean;
}
/**
 * Proxy a WebSocket upgrade request to a target address without creating a
 * {@link ProxyServer} instance. Similar to {@link proxyFetch} but for
 * WebSocket upgrades.
 *
 * @param addr - Target server address. Can be a URL string (`http://host:port`, `ws://host:port`, `unix:/path`), or an object with `host`/`port` for TCP or `socketPath` for Unix sockets.
 * @param req - The incoming HTTP upgrade request.
 * @param socket - The network socket between the server and client.
 * @param head - The first packet of the upgraded stream (may be empty).
 * @param opts - Optional proxy options.
 * @returns A promise that resolves with the upstream proxy socket once the
 * WebSocket connection is established, or rejects on error.
 */
declare function proxyUpgrade(addr: string | ProxyAddr, req: IncomingMessage, socket: Duplex, head?: Buffer, opts?: ProxyUpgradeOptions): Promise<Socket>;

export { ProxyServer, createProxyServer, proxyFetch, proxyUpgrade };
export type { ProxyAddr, ProxyServerEventMap, ProxyServerOptions, ProxyTarget, ProxyTargetDetailed, ProxyUpgradeOptions };

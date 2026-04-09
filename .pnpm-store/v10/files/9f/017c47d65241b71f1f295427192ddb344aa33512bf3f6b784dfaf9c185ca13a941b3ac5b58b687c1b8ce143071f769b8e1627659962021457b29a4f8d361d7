import nodeHTTP, { request } from 'node:http';
import nodeHTTPS, { request as request$1 } from 'node:https';
import { EventEmitter } from 'node:events';
import { Readable } from 'node:stream';

const upgradeHeader = /(^|,)\s*upgrade\s*($|,)/i;
const isSSL = /^https|wss/;
function setupOutgoing(outgoing, options, req, forward) {
  outgoing.port = options[forward || "target"].port || (isSSL.test(options[forward || "target"].protocol ?? "http") ? 443 : 80);
  for (const e of [
    "host",
    "hostname",
    "socketPath",
    "pfx",
    "key",
    "passphrase",
    "cert",
    "ca",
    "ciphers",
    "secureProtocol"
  ]) {
    const value = options[forward || "target"][e];
    outgoing[e] = value;
  }
  outgoing.method = options.method || req.method;
  outgoing.headers = { ...req.headers };
  if (options.headers) {
    outgoing.headers = { ...outgoing.headers, ...options.headers };
  }
  if (options.auth) {
    outgoing.auth = options.auth;
  }
  if (options.ca) {
    outgoing.ca = options.ca;
  }
  if (isSSL.test(options[forward || "target"].protocol ?? "http")) {
    outgoing.rejectUnauthorized = options.secure === void 0 ? true : options.secure;
  }
  outgoing.agent = options.agent || false;
  outgoing.localAddress = options.localAddress;
  if (!outgoing.agent) {
    outgoing.headers = outgoing.headers || {};
    if (typeof outgoing.headers.connection !== "string" || !upgradeHeader.test(outgoing.headers.connection)) {
      outgoing.headers.connection = "close";
    }
  }
  const target = options[forward || "target"];
  const targetPath = target && options.prependPath !== false ? target.pathname || "" : "";
  const reqUrl = req.url || "";
  const qIdx = reqUrl.indexOf("?");
  const reqPath = qIdx === -1 ? reqUrl : reqUrl.slice(0, qIdx);
  const reqSearch = qIdx === -1 ? "" : reqUrl.slice(qIdx);
  const normalizedPath = reqPath ? reqPath[0] === "/" ? reqPath : "/" + reqPath : "/";
  let outgoingPath = options.toProxy ? "/" + reqUrl : normalizedPath + reqSearch;
  outgoingPath = options.ignorePath ? "" : outgoingPath;
  outgoing.path = joinURL(targetPath, outgoingPath);
  if (options.changeOrigin) {
    outgoing.headers.host = requiresPort(outgoing.port, options[forward || "target"].protocol) && !hasPort(outgoing.host) ? outgoing.host + ":" + outgoing.port : outgoing.host ?? void 0;
  }
  return outgoing;
}
function joinURL(base, path) {
  if (!base || base === "/") {
    return path || "/";
  }
  if (!path || path === "/") {
    return base || "/";
  }
  const baseHasTrailing = base[base.length - 1] === "/";
  const pathHasLeading = path[0] === "/";
  if (baseHasTrailing && pathHasLeading) {
    return base + path.slice(1);
  }
  if (!baseHasTrailing && !pathHasLeading) {
    return base + "/" + path;
  }
  return base + path;
}
function setupSocket(socket) {
  socket.setTimeout(0);
  socket.setNoDelay(true);
  socket.setKeepAlive(true, 0);
  return socket;
}
function getPort(req) {
  const res = req.headers.host ? req.headers.host.match(/:(\d+)/) : "";
  if (res) {
    return res[1];
  }
  return hasEncryptedConnection(req) ? "443" : "80";
}
function hasEncryptedConnection(req) {
  return Boolean(
    // req.connection.pair probably does not exist anymore
    req.connection.encrypted || req.connection.pair
  );
}
function rewriteCookieProperty(header, config, property) {
  if (Array.isArray(header)) {
    return header.map(function(headerElement) {
      return rewriteCookieProperty(headerElement, config, property);
    });
  }
  return header.replace(
    new RegExp(String.raw`(;\s*` + property + "=)([^;]+)", "i"),
    function(match, prefix, previousValue) {
      let newValue;
      if (previousValue in config) {
        newValue = config[previousValue];
      } else if ("*" in config) {
        newValue = config["*"];
      } else {
        return match;
      }
      return newValue ? prefix + newValue : "";
    }
  );
}
function parseAddr(addr) {
  if (typeof addr === "string") {
    if (addr.startsWith("unix:")) {
      return { socketPath: addr.slice(5) };
    }
    const url = new URL(addr);
    return {
      host: url.hostname,
      port: Number(url.port) || (isSSL.test(url.protocol) ? 443 : 80)
    };
  }
  if (!addr.socketPath && !addr.port) {
    throw new Error("ProxyAddr must have either `port` or `socketPath`");
  }
  return addr;
}
function hasPort(host) {
  return host ? !!~host.indexOf(":") : false;
}
function requiresPort(_port, _protocol) {
  const protocol = _protocol?.split(":")[0];
  const port = +_port;
  if (!port) return false;
  switch (protocol) {
    case "http":
    case "ws": {
      return port !== 80;
    }
    case "https":
    case "wss": {
      return port !== 443;
    }
    case "ftp": {
      return port !== 21;
    }
    case "gopher": {
      return port !== 70;
    }
    case "file": {
      return false;
    }
  }
  return port !== 0;
}

function defineProxyMiddleware(m) {
  return m;
}
function defineProxyOutgoingMiddleware(m) {
  return m;
}

const redirectRegex = /^201|30([1278])$/;
const removeChunked = defineProxyOutgoingMiddleware((req, res, proxyRes) => {
  if (req.httpVersion === "1.0") {
    delete proxyRes.headers["transfer-encoding"];
  }
});
const setConnection = defineProxyOutgoingMiddleware((req, res, proxyRes) => {
  if (req.httpVersion === "1.0") {
    proxyRes.headers.connection = req.headers.connection || "close";
  } else if (req.httpVersion !== "2.0" && !proxyRes.headers.connection) {
    proxyRes.headers.connection = req.headers.connection || "keep-alive";
  }
});
const setRedirectHostRewrite = defineProxyOutgoingMiddleware(
  (req, res, proxyRes, options) => {
    if ((options.hostRewrite || options.autoRewrite || options.protocolRewrite) && proxyRes.headers.location && redirectRegex.test(String(proxyRes.statusCode))) {
      const target = options.target instanceof URL ? options.target : new URL(options.target);
      const u = new URL(proxyRes.headers.location);
      if (target.host !== u.host) {
        return;
      }
      if (options.hostRewrite) {
        u.host = options.hostRewrite;
      } else if (options.autoRewrite && req.headers.host) {
        u.host = req.headers.host;
      }
      if (options.protocolRewrite) {
        u.protocol = options.protocolRewrite;
      }
      proxyRes.headers.location = u.toString();
    }
  }
);
const writeHeaders = defineProxyOutgoingMiddleware((req, res, proxyRes, options) => {
  const rewriteCookieDomainConfig = typeof options.cookieDomainRewrite === "string" ? (
    // also test for ''
    { "*": options.cookieDomainRewrite }
  ) : options.cookieDomainRewrite;
  const rewriteCookiePathConfig = typeof options.cookiePathRewrite === "string" ? (
    // also test for ''
    { "*": options.cookiePathRewrite }
  ) : options.cookiePathRewrite;
  const preserveHeaderKeyCase = options.preserveHeaderKeyCase;
  let rawHeaderKeyMap;
  const setHeader = function(key, header) {
    if (header === void 0) {
      return;
    }
    if (rewriteCookieDomainConfig && key.toLowerCase() === "set-cookie") {
      header = rewriteCookieProperty(header, rewriteCookieDomainConfig, "domain");
    }
    if (rewriteCookiePathConfig && key.toLowerCase() === "set-cookie") {
      header = rewriteCookieProperty(header, rewriteCookiePathConfig, "path");
    }
    res.setHeader(String(key).trim(), header);
  };
  if (preserveHeaderKeyCase && proxyRes.rawHeaders !== void 0) {
    rawHeaderKeyMap = {};
    for (let i = 0; i < proxyRes.rawHeaders.length; i += 2) {
      const key = proxyRes.rawHeaders[i];
      rawHeaderKeyMap[key.toLowerCase()] = key;
    }
  }
  for (let key of Object.keys(proxyRes.headers)) {
    const header = proxyRes.headers[key];
    if (preserveHeaderKeyCase && rawHeaderKeyMap) {
      key = rawHeaderKeyMap[key] || key;
    }
    setHeader(key, header);
  }
});
const writeStatusCode = defineProxyOutgoingMiddleware((req, res, proxyRes) => {
  if (proxyRes.statusMessage) {
    res.statusCode = proxyRes.statusCode;
    res.statusMessage = proxyRes.statusMessage;
  } else {
    res.statusCode = proxyRes.statusCode;
  }
});
const webOutgoingMiddleware = [
  removeChunked,
  setConnection,
  setRedirectHostRewrite,
  writeHeaders,
  writeStatusCode
];

const nativeAgents = { http: nodeHTTP, https: nodeHTTPS };
const redirectStatuses = /* @__PURE__ */ new Set([301, 302, 303, 307, 308]);
const deleteLength = defineProxyMiddleware((req) => {
  if ((req.method === "DELETE" || req.method === "OPTIONS") && !req.headers["content-length"]) {
    req.headers["content-length"] = "0";
    delete req.headers["transfer-encoding"];
  }
});
const timeout = defineProxyMiddleware((req, res, options) => {
  if (options.timeout) {
    req.socket.setTimeout(options.timeout, () => {
      req.socket.destroy();
    });
  }
});
const XHeaders$1 = defineProxyMiddleware((req, res, options) => {
  if (!options.xfwd) {
    return;
  }
  const encrypted = req.isSpdy || hasEncryptedConnection(req);
  const values = {
    for: req.connection.remoteAddress || req.socket.remoteAddress,
    port: getPort(req),
    proto: encrypted ? "https" : "http"
  };
  for (const header of ["for", "port", "proto"]) {
    req.headers["x-forwarded-" + header] = (req.headers["x-forwarded-" + header] || "") + (req.headers["x-forwarded-" + header] ? "," : "") + values[header];
  }
  req.headers["x-forwarded-host"] = req.headers["x-forwarded-host"] || req.headers.host || "";
});
const stream$1 = defineProxyMiddleware((req, res, options, server, head, callback) => {
  server.emit("start", req, res, options.target || options.forward);
  const http = nativeAgents.http;
  const https = nativeAgents.https;
  const maxRedirects = typeof options.followRedirects === "number" ? options.followRedirects : options.followRedirects ? 5 : 0;
  if (options.forward) {
    const forwardReq = (options.forward.protocol === "https:" ? https : http).request(
      setupOutgoing(options.ssl || {}, options, req, "forward")
    );
    const forwardError = createErrorHandler(forwardReq, options.forward);
    req.on("error", forwardError);
    forwardReq.on("error", forwardError);
    (options.buffer || req).pipe(forwardReq);
    if (!options.target) {
      res.end();
      return;
    }
  }
  const proxyReq = (options.target.protocol === "https:" ? https : http).request(
    setupOutgoing(options.ssl || {}, options, req)
  );
  proxyReq.on("socket", (_socket) => {
    if (server && !proxyReq.getHeader("expect")) {
      server.emit("proxyReq", proxyReq, req, res, options);
    }
  });
  if (options.proxyTimeout) {
    proxyReq.setTimeout(options.proxyTimeout, function() {
      proxyReq.abort();
    });
  }
  req.on("aborted", function() {
    proxyReq.abort();
  });
  res.on("close", function() {
    if (!res.writableFinished) {
      proxyReq.destroy();
    }
  });
  const proxyError = createErrorHandler(proxyReq, options.target);
  req.on("error", proxyError);
  proxyReq.on("error", proxyError);
  function createErrorHandler(proxyReq2, url) {
    return function proxyError2(err) {
      if (req.socket.destroyed && err.code === "ECONNRESET") {
        server.emit("econnreset", err, req, res, url);
        return proxyReq2.abort();
      }
      if (callback) {
        callback(err, req, res, url);
      } else {
        server.emit("error", err, req, res, url);
      }
    };
  }
  let bodyBuffer;
  if (maxRedirects > 0) {
    const chunks = [];
    const source = options.buffer || req;
    source.on("data", (chunk) => {
      chunks.push(typeof chunk === "string" ? Buffer.from(chunk) : chunk);
      proxyReq.write(chunk);
    });
    source.on("end", () => {
      bodyBuffer = Buffer.concat(chunks);
      proxyReq.end();
    });
    source.on("error", (err) => {
      proxyReq.destroy(err);
    });
  } else {
    (options.buffer || req).pipe(proxyReq);
  }
  function handleResponse(proxyRes, redirectCount, currentUrl) {
    const statusCode = proxyRes.statusCode;
    if (maxRedirects > 0 && redirectStatuses.has(statusCode) && redirectCount < maxRedirects && proxyRes.headers.location) {
      proxyRes.resume();
      const location = new URL(proxyRes.headers.location, currentUrl);
      const preserveMethod = statusCode === 307 || statusCode === 308;
      const redirectMethod = preserveMethod ? req.method || "GET" : "GET";
      const isHTTPS = location.protocol === "https:";
      const agent = isHTTPS ? https : http;
      const redirectHeaders = { ...req.headers };
      if (options.headers) {
        Object.assign(redirectHeaders, options.headers);
      }
      redirectHeaders.host = location.host;
      if (location.host !== currentUrl.host) {
        delete redirectHeaders.authorization;
        delete redirectHeaders.cookie;
      }
      if (!preserveMethod) {
        delete redirectHeaders["content-length"];
        delete redirectHeaders["content-type"];
        delete redirectHeaders["transfer-encoding"];
      }
      const redirectOpts = {
        hostname: location.hostname,
        port: location.port || (isHTTPS ? 443 : 80),
        path: location.pathname + location.search,
        method: redirectMethod,
        headers: redirectHeaders,
        agent: options.agent || false
      };
      if (isHTTPS) {
        redirectOpts.rejectUnauthorized = options.secure === void 0 ? true : options.secure;
      }
      const redirectReq = agent.request(redirectOpts);
      if (server && !redirectReq.getHeader("expect")) {
        server.emit("proxyReq", redirectReq, req, res, options);
      }
      if (options.proxyTimeout) {
        redirectReq.setTimeout(options.proxyTimeout, () => {
          redirectReq.abort();
        });
      }
      const redirectError = createErrorHandler(redirectReq, location);
      redirectReq.on("error", redirectError);
      redirectReq.on("response", (nextRes) => {
        handleResponse(nextRes, redirectCount + 1, location);
      });
      if (preserveMethod && bodyBuffer && bodyBuffer.length > 0) {
        redirectReq.end(bodyBuffer);
      } else {
        redirectReq.end();
      }
      return;
    }
    if (server) {
      server.emit("proxyRes", proxyRes, req, res);
    }
    if (!res.headersSent && !options.selfHandleResponse) {
      for (const pass of webOutgoingMiddleware) {
        if (pass(req, res, proxyRes, options)) {
          break;
        }
      }
    }
    if (res.finished) {
      if (server) {
        server.emit("end", req, res, proxyRes);
      }
    } else {
      res.on("close", function() {
        proxyRes.destroy();
      });
      proxyRes.on("end", function() {
        if (server) {
          server.emit("end", req, res, proxyRes);
        }
      });
      if (!options.selfHandleResponse) {
        proxyRes.pipe(res);
      }
    }
  }
  proxyReq.on("response", function(proxyRes) {
    handleResponse(proxyRes, 0, options.target);
  });
});
const webIncomingMiddleware = [
  deleteLength,
  timeout,
  XHeaders$1,
  stream$1
];

const checkMethodAndHeader = defineProxyMiddleware((req, socket) => {
  if (req.method !== "GET" || !req.headers.upgrade) {
    socket.destroy();
    return true;
  }
  if (req.headers.upgrade.toLowerCase() !== "websocket") {
    socket.destroy();
    return true;
  }
});
const XHeaders = defineProxyMiddleware((req, socket, options) => {
  if (!options.xfwd) {
    return;
  }
  const values = {
    for: req.connection.remoteAddress || req.socket.remoteAddress,
    port: getPort(req),
    proto: hasEncryptedConnection(req) ? "wss" : "ws"
  };
  for (const header of ["for", "port", "proto"]) {
    req.headers["x-forwarded-" + header] = (req.headers["x-forwarded-" + header] || "") + (req.headers["x-forwarded-" + header] ? "," : "") + values[header];
  }
});
const stream = defineProxyMiddleware(
  (req, socket, options, server, head, callback) => {
    const createHttpHeader = function(line, headers) {
      return Object.keys(headers).reduce(
        function(head2, key) {
          const value = headers[key];
          if (!Array.isArray(value)) {
            head2.push(key + ": " + value);
            return head2;
          }
          for (const element of value) {
            head2.push(key + ": " + element);
          }
          return head2;
        },
        [line]
      ).join("\r\n") + "\r\n\r\n";
    };
    setupSocket(socket);
    if (head && head.length > 0) {
      socket.unshift(head);
    }
    socket.on("error", onSocketError);
    const proxyReq = (isSSL.test(options.target.protocol || "http") ? nodeHTTPS : nodeHTTP).request(
      setupOutgoing(options.ssl || {}, options, req)
    );
    if (server) {
      server.emit("proxyReqWs", proxyReq, req, socket, options, head);
    }
    proxyReq.on("error", onOutgoingError);
    proxyReq.on("response", function(res) {
      if (!res.upgrade) {
        socket.write(
          createHttpHeader(
            "HTTP/" + res.httpVersion + " " + res.statusCode + " " + res.statusMessage,
            res.headers
          )
        );
        res.pipe(socket);
      }
    });
    proxyReq.on("upgrade", function(proxyRes, proxySocket, proxyHead) {
      proxySocket.on("error", onOutgoingError);
      proxySocket.on("end", function() {
        server.emit("close", proxyRes, proxySocket, proxyHead);
      });
      socket.on("error", function() {
        proxySocket.end();
      });
      setupSocket(proxySocket);
      if (proxyHead && proxyHead.length > 0) {
        proxySocket.unshift(proxyHead);
      }
      socket.write(createHttpHeader("HTTP/1.1 101 Switching Protocols", proxyRes.headers));
      proxySocket.pipe(socket).pipe(proxySocket);
      server.emit("open", proxySocket);
      server.emit("proxySocket", proxySocket);
    });
    proxyReq.end();
    function onSocketError(err) {
      if (callback) {
        callback(err, req, socket);
      } else {
        server.emit("error", err, req, socket);
      }
      proxyReq.destroy();
    }
    function onOutgoingError(err) {
      if (callback) {
        callback(err, req, socket);
      } else {
        server.emit("error", err, req, socket);
      }
      socket.end();
    }
  }
);
const websocketIncomingMiddleware = [
  checkMethodAndHeader,
  XHeaders,
  stream
];

class ProxyServer extends EventEmitter {
  _server;
  _webPasses = [...webIncomingMiddleware];
  _wsPasses = [...websocketIncomingMiddleware];
  options;
  web;
  ws;
  /**
   * Creates the proxy server with specified options.
   * @param options - Config object passed to the proxy
   */
  constructor(options = {}) {
    super();
    this.options = options || {};
    this.options.prependPath = options.prependPath !== false;
    this.web = _createProxyFn("web", this);
    this.ws = _createProxyFn("ws", this);
  }
  /**
   * A function that wraps the object in a webserver, for your convenience
   * @param port - Port to listen on
   * @param hostname - The hostname to listen on
   */
  listen(port, hostname) {
    const closure = (req, res) => {
      this.web(req, res);
    };
    this._server = this.options.ssl ? nodeHTTPS.createServer(this.options.ssl, closure) : nodeHTTP.createServer(closure);
    if (this.options.ws) {
      this._server.on("upgrade", (req, socket, head) => {
        this.ws(req, socket, head).catch(() => {
        });
      });
    }
    this._server.listen(port, hostname);
    return this;
  }
  /**
   * A function that closes the inner webserver and stops listening on given port
   */
  close(callback) {
    if (this._server) {
      this._server.close((...args) => {
        this._server = void 0;
        if (callback) {
          Reflect.apply(callback, void 0, args);
        }
      });
    }
  }
  before(type, passName, pass) {
    if (type !== "ws" && type !== "web") {
      throw new Error("type must be `web` or `ws`");
    }
    const passes = this._getPasses(type);
    let i = false;
    for (const [idx, v] of passes.entries()) {
      if (v.name === passName) {
        i = idx;
      }
    }
    if (i === false) {
      throw new Error("No such pass");
    }
    passes.splice(i, 0, pass);
  }
  after(type, passName, pass) {
    if (type !== "ws" && type !== "web") {
      throw new Error("type must be `web` or `ws`");
    }
    const passes = this._getPasses(type);
    let i = false;
    for (const [idx, v] of passes.entries()) {
      if (v.name === passName) {
        i = idx;
      }
    }
    if (i === false) {
      throw new Error("No such pass");
    }
    passes.splice(i++, 0, pass);
  }
  /** @internal */
  _getPasses(type) {
    return type === "ws" ? this._wsPasses : this._webPasses;
  }
}
function createProxyServer(options = {}) {
  return new ProxyServer(options);
}
function _createProxyFn(type, server) {
  return function(req, res, opts, head) {
    const requestOptions = { ...opts, ...server.options };
    for (const key of ["target", "forward"]) {
      if (typeof requestOptions[key] === "string") {
        requestOptions[key] = new URL(requestOptions[key]);
      }
    }
    if (!requestOptions.target && !requestOptions.forward) {
      this.emit("error", new Error("Must provide a proper URL as target"));
      return Promise.resolve();
    }
    let _resolve;
    let _reject;
    const callbackPromise = new Promise((resolve, reject) => {
      _resolve = resolve;
      _reject = reject;
    });
    res.on("close", () => {
      _resolve();
    });
    res.on("error", (error) => {
      _reject(error);
    });
    for (const pass of server._getPasses(type)) {
      const stop = pass(
        req,
        res,
        requestOptions,
        server,
        head,
        (error) => {
          if (server.listenerCount("error") > 0) {
            server.emit("error", error, req, res);
            _resolve();
          } else {
            _reject(error);
          }
        }
      );
      if (stop) {
        _resolve();
        break;
      }
    }
    return callbackPromise;
  };
}

async function proxyFetch(addr, input, inputInit) {
  const resolvedAddr = parseAddr(addr);
  let url;
  let init;
  if (input instanceof Request) {
    url = new URL(input.url);
    init = {
      ...toInit(input),
      ...toInit(inputInit)
    };
  } else {
    url = new URL(input);
    init = toInit(inputInit);
  }
  init = {
    redirect: "manual",
    ...init
  };
  if (init.body) {
    init.duplex = "half";
  }
  const path = url.pathname + url.search;
  const reqHeaders = {};
  if (init.headers) {
    const h = init.headers instanceof Headers ? init.headers : new Headers(init.headers);
    for (const [key, value] of h) {
      reqHeaders[key] = value;
    }
  }
  const res = await new Promise((resolve, reject) => {
    const reqOpts = {
      method: init.method || "GET",
      path,
      headers: reqHeaders
    };
    if (resolvedAddr.socketPath) {
      reqOpts.socketPath = resolvedAddr.socketPath;
    } else {
      reqOpts.hostname = resolvedAddr.host || "localhost";
      reqOpts.port = resolvedAddr.port;
    }
    const req = request(reqOpts, resolve);
    req.on("error", reject);
    if (init.body instanceof ReadableStream) {
      const readable = Readable.fromWeb(init.body);
      readable.on("error", reject);
      readable.pipe(req);
    } else if (init.body) {
      req.end(init.body);
    } else {
      req.end();
    }
  });
  const headers = new Headers();
  for (const [key, value] of Object.entries(res.headers)) {
    if (key === "transfer-encoding" || key === "keep-alive" || key === "connection") {
      continue;
    }
    if (Array.isArray(value)) {
      for (const v of value) {
        headers.append(key, v);
      }
    } else if (value) {
      headers.set(key, value);
    }
  }
  const hasBody = res.statusCode !== 204 && res.statusCode !== 304;
  return new Response(hasBody ? Readable.toWeb(res) : null, {
    status: res.statusCode,
    statusText: res.statusMessage,
    headers
  });
}
function toInit(init) {
  if (!init) {
    return void 0;
  }
  if (init instanceof Request) {
    return {
      method: init.method,
      headers: init.headers,
      body: init.body,
      duplex: init.body ? "half" : void 0
    };
  }
  return init;
}

function proxyUpgrade(addr, req, socket, head, opts) {
  const resolvedAddr = parseAddr(addr);
  if (req.method !== "GET" || req.headers.upgrade?.toLowerCase() !== "websocket") {
    socket.destroy();
    return Promise.reject(new Error("Not a valid WebSocket upgrade request"));
  }
  if (opts?.xfwd !== false) {
    const xfFor = req.headers["x-forwarded-for"];
    const xfPort = req.headers["x-forwarded-port"];
    const xfProto = req.headers["x-forwarded-proto"];
    req.headers["x-forwarded-for"] = `${xfFor ? `${xfFor},` : ""}${req.socket?.remoteAddress}`;
    req.headers["x-forwarded-port"] = `${xfPort ? `${xfPort},` : ""}${getPort(req)}`;
    req.headers["x-forwarded-proto"] = `${xfProto ? `${xfProto},` : ""}${hasEncryptedConnection(req) ? "wss" : "ws"}`;
  }
  const target = _buildTargetURL(resolvedAddr);
  const requestOptions = {
    ...opts,
    target,
    prependPath: opts?.prependPath !== false
  };
  const outgoing = setupOutgoing(
    requestOptions.ssl || {},
    requestOptions,
    req
  );
  const sock = socket;
  return new Promise((resolve, reject) => {
    let settled = false;
    setupSocket(sock);
    if (head && head.length > 0) {
      sock.unshift(head);
    }
    sock.once("error", onSocketError);
    const doRequest = isSSL.test(target.protocol) ? request$1 : request;
    const proxyReq = doRequest(outgoing);
    proxyReq.once("error", onOutgoingError);
    proxyReq.once("response", (res) => {
      if (!res.upgrade) {
        sock.write(
          _createHttpHeader(
            `HTTP/${res.httpVersion} ${res.statusCode} ${res.statusMessage}`,
            res.headers
          )
        );
        res.pipe(sock);
        if (!settled) {
          settled = true;
          reject(new Error("Upstream server did not upgrade the connection"));
        }
      }
    });
    proxyReq.once("upgrade", (proxyRes, proxySocket, proxyHead) => {
      proxySocket.once("error", onOutgoingError);
      sock.removeListener("error", onSocketError);
      sock.once("error", () => {
        proxySocket.end();
      });
      setupSocket(proxySocket);
      if (proxyHead && proxyHead.length > 0) {
        proxySocket.unshift(proxyHead);
      }
      sock.write(_createHttpHeader("HTTP/1.1 101 Switching Protocols", proxyRes.headers));
      proxySocket.pipe(sock).pipe(proxySocket);
      settled = true;
      resolve(proxySocket);
    });
    proxyReq.end();
    function onSocketError(err) {
      proxyReq.destroy();
      if (!settled) {
        settled = true;
        reject(err);
      }
    }
    function onOutgoingError(err) {
      sock.end();
      if (!settled) {
        settled = true;
        reject(err);
      }
    }
  });
}
function _buildTargetURL(addr) {
  if (addr.socketPath) {
    const url = new URL("http://unix");
    url.socketPath = addr.socketPath;
    return url;
  }
  return new URL(`http://${addr.host || "localhost"}${addr.port ? `:${addr.port}` : ""}`);
}
function _createHttpHeader(line, headers) {
  let result = line;
  for (const key of Object.keys(headers)) {
    const value = headers[key];
    if (value === void 0) {
      continue;
    }
    if (Array.isArray(value)) {
      for (const element of value) {
        result += `\r
${key}: ${element}`;
      }
    } else {
      result += `\r
${key}: ${value}`;
    }
  }
  return `${result}\r
\r
`;
}

export { ProxyServer, createProxyServer, proxyFetch, proxyUpgrade };

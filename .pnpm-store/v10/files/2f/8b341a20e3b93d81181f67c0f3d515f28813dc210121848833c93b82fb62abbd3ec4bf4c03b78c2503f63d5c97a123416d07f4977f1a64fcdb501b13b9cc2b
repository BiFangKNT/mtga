import { b as ScriptNetworkEvents } from './unhead.yem5I2v_.mjs';

function createNoopedRecordingProxy(instance = {}) {
  const stack = [];
  let stackIdx = -1;
  const handler = (reuseStack = false) => ({
    get(_, prop, receiver) {
      if (!reuseStack) {
        const v = Reflect.get(_, prop, receiver);
        if (typeof v !== "undefined") {
          return v;
        }
        stackIdx++;
        stack[stackIdx] = [];
      }
      stack[stackIdx].push({ type: "get", key: prop });
      return new Proxy(() => {
      }, handler(true));
    },
    apply(_, __, args) {
      stack[stackIdx].push({ type: "apply", key: "", args });
      return void 0;
    }
  });
  return {
    proxy: new Proxy(instance || {}, handler()),
    stack
  };
}
function createForwardingProxy(target) {
  const handler = {
    get(_, prop, receiver) {
      const v = Reflect.get(_, prop, receiver);
      if (typeof v === "object") {
        return new Proxy(v, handler);
      }
      return v;
    },
    apply(_, __, args) {
      Reflect.apply(_, __, args);
      return void 0;
    }
  };
  return new Proxy(target, handler);
}
function replayProxyRecordings(target, stack) {
  stack.forEach((recordings) => {
    let context = target;
    let prevContext = target;
    recordings.forEach(({ type, key, args }) => {
      if (type === "get") {
        prevContext = context;
        context = context[key];
      } else if (type === "apply") {
        context = context.call(prevContext, ...args);
      }
    });
  });
}

function resolveScriptKey(input) {
  return input.key || input.src || (typeof input.innerHTML === "string" ? input.innerHTML : "");
}
const PreconnectServerModes = ["preconnect", "dns-prefetch"];
function useScript(head, _input, _options) {
  const input = typeof _input === "string" ? { src: _input } : _input;
  const options = _options || {};
  const id = resolveScriptKey(input);
  const prevScript = head._scripts?.[id];
  if (prevScript) {
    prevScript.setupTriggerHandler(options.trigger);
    return prevScript;
  }
  options.beforeInit?.();
  const syncStatus = (s) => {
    script.status = s;
    head.hooks.callHook(`script:updated`, hookCtx);
  };
  ScriptNetworkEvents.forEach((fn) => {
    const k = fn;
    const _fn = typeof input[k] === "function" ? input[k].bind(options.eventContext) : null;
    input[k] = (e) => {
      syncStatus(fn === "onload" ? "loaded" : fn === "onerror" ? "error" : "loading");
      _fn?.(e);
    };
  });
  const _cbs = { loaded: [], error: [] };
  const _uniqueCbs = /* @__PURE__ */ new Set();
  const _registerCb = (key, cb, options2) => {
    if (head.ssr) {
      return;
    }
    if (options2?.key) {
      const key2 = `${options2?.key}:${options2.key}`;
      if (_uniqueCbs.has(key2)) {
        return;
      }
      _uniqueCbs.add(key2);
    }
    if (_cbs[key]) {
      const i = _cbs[key].push(cb);
      return () => _cbs[key]?.splice(i - 1, 1);
    }
    cb(script.instance);
    return () => {
    };
  };
  const loadPromise = new Promise((resolve) => {
    if (head.ssr)
      return;
    const emit = (api) => requestAnimationFrame(() => resolve(api));
    const _ = head.hooks.hook("script:updated", ({ script: script2 }) => {
      const status = script2.status;
      if (script2.id === id && (status === "loaded" || status === "error")) {
        if (status === "loaded") {
          if (typeof options.use === "function") {
            const api = options.use();
            if (api) {
              emit(api);
            }
          } else {
            emit({});
          }
        } else if (status === "error") {
          resolve(false);
        }
        _();
      }
    });
  });
  const script = {
    _loadPromise: loadPromise,
    instance: !head.ssr && options?.use?.() || null,
    proxy: null,
    id,
    status: "awaitingLoad",
    remove() {
      script._triggerAbortControllers?.forEach((ac) => ac.abort());
      script._triggerAbortControllers?.clear();
      script._triggerPromises = [];
      script._warmupEl?.dispose();
      if (script.entry) {
        script.entry.dispose();
        script.entry = void 0;
        syncStatus("removed");
        delete head._scripts?.[id];
        return true;
      }
      return false;
    },
    warmup(rel) {
      const { src } = input;
      const isCrossOrigin = !src.startsWith("/") || src.startsWith("//");
      const isPreconnect = rel && PreconnectServerModes.includes(rel);
      let href = src;
      if (!rel || isPreconnect && !isCrossOrigin) {
        return;
      }
      if (isPreconnect) {
        const $url = new URL(src);
        href = `${$url.protocol}//${$url.host}`;
      }
      const link = {
        href,
        rel,
        crossorigin: typeof input.crossorigin !== "undefined" ? input.crossorigin : isCrossOrigin ? "anonymous" : void 0,
        referrerpolicy: typeof input.referrerpolicy !== "undefined" ? input.referrerpolicy : isCrossOrigin ? "no-referrer" : void 0,
        fetchpriority: typeof input.fetchpriority !== "undefined" ? input.fetchpriority : "low",
        integrity: input.integrity,
        as: rel === "preload" ? "script" : void 0
      };
      script._warmupEl = head.push({ link: [link] }, { head, tagPriority: "high" });
      return script._warmupEl;
    },
    load(cb) {
      script._triggerAbortControllers?.forEach((ac) => ac.abort());
      script._triggerAbortControllers?.clear();
      script._triggerPromises = [];
      if (!script.entry) {
        syncStatus("loading");
        const defaults = {
          defer: true,
          fetchpriority: "low"
        };
        if (input.src && (input.src.startsWith("http") || input.src.startsWith("//"))) {
          defaults.crossorigin = "anonymous";
          defaults.referrerpolicy = "no-referrer";
        }
        script.entry = head.push({
          script: [{ ...defaults, ...input }]
        }, options);
      }
      if (cb)
        _registerCb("loaded", cb);
      return loadPromise;
    },
    onLoaded(cb, options2) {
      return _registerCb("loaded", cb, options2);
    },
    onError(cb, options2) {
      return _registerCb("error", cb, options2);
    },
    setupTriggerHandler(trigger) {
      if (script.status !== "awaitingLoad") {
        return;
      }
      if ((typeof trigger === "undefined" || trigger === "client") && !head.ssr || trigger === "server") {
        script.load();
      } else if (trigger instanceof Promise) {
        if (head.ssr) {
          return;
        }
        const abortController = new AbortController();
        script._triggerAbortControllers = script._triggerAbortControllers || /* @__PURE__ */ new Set();
        script._triggerAbortControllers.add(abortController);
        const abortPromise = new Promise((resolve) => {
          abortController.signal.addEventListener("abort", () => {
            script._triggerAbortControllers?.delete(abortController);
            resolve();
          });
        });
        script._triggerAbortController = abortController;
        script._triggerPromises = script._triggerPromises || [];
        const idx = script._triggerPromises.push(Promise.race([
          trigger.then((v) => typeof v === "undefined" || v ? script.load : void 0),
          abortPromise
        ]).catch(() => {
        }).then((res) => {
          res?.();
        }).finally(() => {
          script._triggerPromises?.splice(idx, 1);
        }));
      } else if (typeof trigger === "function") {
        trigger(script.load);
      }
    },
    _cbs
  };
  loadPromise.then((api) => {
    if (api !== false) {
      script.instance = api;
      _cbs.loaded?.forEach((cb) => cb(api));
      _cbs.loaded = null;
    } else {
      _cbs.error?.forEach((cb) => cb());
      _cbs.error = null;
    }
  });
  const hookCtx = { script };
  script.setupTriggerHandler(options.trigger);
  if (options.use) {
    const { proxy, stack } = createNoopedRecordingProxy(head.ssr ? {} : options.use() || {});
    script.proxy = proxy;
    script.onLoaded((instance) => {
      replayProxyRecordings(instance, stack);
      script.proxy = createForwardingProxy(instance);
    });
  }
  if (!options.warmupStrategy && (typeof options.trigger === "undefined" || options.trigger === "client")) {
    options.warmupStrategy = "preload";
  }
  if (options.warmupStrategy) {
    script.warmup(options.warmupStrategy);
  }
  head._scripts = Object.assign(head._scripts || {}, { [id]: script });
  return script;
}

export { resolveScriptKey as r, useScript as u };

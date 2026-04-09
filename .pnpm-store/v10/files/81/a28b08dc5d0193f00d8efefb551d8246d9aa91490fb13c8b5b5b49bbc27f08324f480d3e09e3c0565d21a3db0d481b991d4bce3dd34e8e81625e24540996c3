import { computed, getCurrentInstance, getCurrentScope, inject, isShallow, nextTick, onBeforeMount, onScopeDispose, onServerPrefetch, onUnmounted, queuePostFlushCb, ref, shallowRef, toRef, toValue, unref, watch } from "vue";
import { debounce } from "perfect-debounce";
import { hash } from "ohash";
import { useNuxtApp } from "../nuxt.js";
import { getUserCaller, toArray } from "../utils.js";
import { clientOnlySymbol } from "../components/client-only.js";
import { createError } from "./error.js";
import { onNuxtReady } from "./ready.js";
import { defineKeyedFunctionFactory } from "../../compiler/runtime";
import { asyncDataDefaults, granularCachedData, pendingWhenIdle, purgeCachedData } from "#build/nuxt.config.mjs";
export const createUseAsyncData = defineKeyedFunctionFactory({
  name: "createUseAsyncData",
  factory(options = {}) {
    function useAsyncData2(...args) {
      const autoKey = typeof args[args.length - 1] === "string" ? args.pop() : void 0;
      if (_isAutoKeyNeeded(args[0], args[1])) {
        args.unshift(autoKey);
      }
      let [_key, _handler, opts = {}] = args;
      let keyChanging = false;
      const key = computed(() => toValue(_key));
      if (typeof key.value !== "string") {
        throw new TypeError("[nuxt] [useAsyncData] key must be a string.");
      }
      if (typeof _handler !== "function") {
        throw new TypeError("[nuxt] [useAsyncData] handler must be a function.");
      }
      const shouldFactoryOptionsOverride = typeof options === "function";
      const nuxtApp = useNuxtApp();
      const factoryOptions = shouldFactoryOptionsOverride ? options(opts) : options;
      if (!shouldFactoryOptionsOverride) {
        for (const key2 in factoryOptions) {
          if (factoryOptions[key2] === void 0) {
            continue;
          }
          if (opts[key2] !== void 0) {
            continue;
          }
          opts[key2] = factoryOptions[key2];
        }
      }
      opts.server ??= true;
      opts.default ??= getDefault;
      opts.getCachedData ??= getDefaultCachedData;
      opts.lazy ??= false;
      opts.immediate ??= true;
      opts.deep ??= asyncDataDefaults.deep;
      opts.dedupe ??= "cancel";
      if (shouldFactoryOptionsOverride) {
        for (const key2 in factoryOptions) {
          if (factoryOptions[key2] === void 0) {
            continue;
          }
          opts[key2] = factoryOptions[key2];
        }
      }
      const functionName = import.meta.dev ? factoryOptions._functionName || "useAsyncData" : "";
      const currentData = nuxtApp._asyncData[key.value];
      if (import.meta.dev && currentData) {
        const warnings = [];
        const values = createHash(_handler, opts);
        if (values.handler !== currentData._hash?.handler) {
          warnings.push(`different handler`);
        }
        for (const opt of ["transform", "pick", "getCachedData"]) {
          if (values[opt] !== currentData._hash[opt]) {
            warnings.push(`different \`${opt}\` option`);
          }
        }
        if (currentData._default.toString() !== opts.default.toString()) {
          warnings.push(`different \`default\` value`);
        }
        if (opts.deep && isShallow(currentData.data)) {
          warnings.push(`mismatching \`deep\` option`);
        }
        if (warnings.length) {
          const caller = getUserCaller();
          const explanation = caller ? ` (used at ${caller.source}:${caller.line}:${caller.column})` : "";
          console.warn(`[nuxt] [${functionName}] Incompatible options detected for "${key.value}"${explanation}:
${warnings.map((w) => `- ${w}`).join("\n")}
You can use a different key or move the call to a composable to ensure the options are shared across calls.`);
        }
      }
      function createInitialFetch() {
        const initialFetchOptions = { cause: "initial", dedupe: opts.dedupe };
        if (!nuxtApp._asyncData[key.value]?._init) {
          initialFetchOptions.cachedData = opts.getCachedData(key.value, nuxtApp, { cause: "initial" });
          nuxtApp._asyncData[key.value] = buildAsyncData(nuxtApp, key.value, _handler, opts, initialFetchOptions.cachedData);
        }
        return () => nuxtApp._asyncData[key.value].execute(initialFetchOptions);
      }
      const initialFetch = createInitialFetch();
      const asyncData = nuxtApp._asyncData[key.value];
      asyncData._deps++;
      const fetchOnServer = opts.server !== false && nuxtApp.payload.serverRendered;
      if (import.meta.server && fetchOnServer && opts.immediate) {
        const promise = initialFetch();
        if (getCurrentInstance()) {
          onServerPrefetch(() => promise);
        } else {
          nuxtApp.hook("app:created", async () => {
            await promise;
          });
        }
      }
      if (import.meta.client) {
        let unregister = function(key2) {
          const data = nuxtApp._asyncData[key2];
          if (data?._deps) {
            data._deps--;
            if (data._deps === 0) {
              data?._off();
            }
          }
        };
        const instance = getCurrentInstance();
        if (instance && fetchOnServer && opts.immediate && !instance.sp) {
          instance.sp = [];
        }
        if (import.meta.dev && !nuxtApp.isHydrating && !nuxtApp._processingMiddleware && (!instance || instance?.isMounted)) {
          console.warn(`[nuxt] [${functionName}] Component is already mounted, please use $fetch instead. See https://nuxt.com/docs/4.x/getting-started/data-fetching`);
        }
        if (instance && !instance._nuxtOnBeforeMountCbs) {
          instance._nuxtOnBeforeMountCbs = [];
          const cbs = instance._nuxtOnBeforeMountCbs;
          onBeforeMount(() => {
            cbs.forEach((cb) => {
              cb();
            });
            cbs.splice(0, cbs.length);
          });
          onUnmounted(() => cbs.splice(0, cbs.length));
        }
        const isWithinClientOnly = instance && (instance._nuxtClientOnly || inject(clientOnlySymbol, false));
        if (fetchOnServer && nuxtApp.isHydrating && (asyncData.error.value || asyncData.data.value !== void 0)) {
          if (pendingWhenIdle) {
            asyncData.pending.value = false;
          }
          asyncData.status.value = asyncData.error.value ? "error" : "success";
        } else if (instance && (!isWithinClientOnly && nuxtApp.payload.serverRendered && nuxtApp.isHydrating || opts.lazy) && opts.immediate) {
          instance._nuxtOnBeforeMountCbs.push(initialFetch);
        } else if (opts.immediate && asyncData.status.value !== "success") {
          initialFetch();
        }
        const hasScope = getCurrentScope();
        const unsubKeyWatcher = watch(key, (newKey, oldKey) => {
          if ((newKey || oldKey) && newKey !== oldKey) {
            keyChanging = true;
            const hadData = nuxtApp._asyncData[oldKey]?.data.value !== void 0;
            const wasRunning = nuxtApp._asyncDataPromises[oldKey] !== void 0;
            const initialFetchOptions = { cause: "initial", dedupe: opts.dedupe };
            if (!nuxtApp._asyncData[newKey]?._init) {
              let initialValue;
              if (oldKey && hadData) {
                initialValue = nuxtApp._asyncData[oldKey].data.value;
              } else {
                initialValue = opts.getCachedData(newKey, nuxtApp, { cause: "initial" });
                initialFetchOptions.cachedData = initialValue;
              }
              nuxtApp._asyncData[newKey] = buildAsyncData(nuxtApp, newKey, _handler, opts, initialValue);
            }
            nuxtApp._asyncData[newKey]._deps++;
            if (oldKey) {
              unregister(oldKey);
            }
            if (opts.immediate || hadData || wasRunning) {
              nuxtApp._asyncData[newKey].execute(initialFetchOptions);
            }
            queuePostFlushCb(() => {
              keyChanging = false;
            });
          }
        }, { flush: "sync" });
        const unsubParamsWatcher = opts.watch ? watch(opts.watch, () => {
          if (keyChanging) {
            return;
          }
          if (nuxtApp._asyncData[key.value]?._execute.isPending()) {
            queuePostFlushCb(() => {
              nuxtApp._asyncData[key.value]?._execute.flush();
            });
          }
          nuxtApp._asyncData[key.value]?._execute({ cause: "watch", dedupe: opts.dedupe });
        }) : () => {
        };
        if (hasScope) {
          onScopeDispose(() => {
            unsubKeyWatcher();
            unsubParamsWatcher();
            unregister(key.value);
          });
        }
      }
      const asyncReturn = {
        data: writableComputedRef(() => nuxtApp._asyncData[key.value]?.data),
        pending: writableComputedRef(() => nuxtApp._asyncData[key.value]?.pending),
        status: writableComputedRef(() => nuxtApp._asyncData[key.value]?.status),
        error: writableComputedRef(() => nuxtApp._asyncData[key.value]?.error),
        refresh: (...args2) => {
          if (!nuxtApp._asyncData[key.value]?._init) {
            const initialFetch2 = createInitialFetch();
            return initialFetch2();
          }
          return nuxtApp._asyncData[key.value].execute(...args2);
        },
        execute: (...args2) => asyncReturn.refresh(...args2),
        clear: () => {
          const entry = nuxtApp._asyncData[key.value];
          if (entry?._abortController) {
            try {
              entry._abortController.abort(new DOMException("AsyncData aborted by user.", "AbortError"));
            } finally {
              entry._abortController = void 0;
            }
          }
          clearNuxtDataByKey(nuxtApp, key.value);
        }
      };
      const asyncDataPromise = Promise.resolve(nuxtApp._asyncDataPromises[key.value]).then(() => asyncReturn);
      Object.assign(asyncDataPromise, asyncReturn);
      Object.defineProperties(asyncDataPromise, {
        then: { enumerable: true, value: asyncDataPromise.then.bind(asyncDataPromise) },
        catch: { enumerable: true, value: asyncDataPromise.catch.bind(asyncDataPromise) },
        finally: { enumerable: true, value: asyncDataPromise.finally.bind(asyncDataPromise) }
      });
      return asyncDataPromise;
    }
    return useAsyncData2;
  }
});
export const useAsyncData = createUseAsyncData.__nuxt_factory();
export const useLazyAsyncData = createUseAsyncData.__nuxt_factory({
  lazy: true,
  // @ts-expect-error private property
  _functionName: "useLazyAsyncData"
});
function writableComputedRef(getter) {
  return computed({
    get() {
      return getter()?.value;
    },
    set(value) {
      const ref2 = getter();
      if (ref2) {
        ref2.value = value;
      }
    }
  });
}
function _isAutoKeyNeeded(keyOrFetcher, fetcher) {
  if (typeof keyOrFetcher === "string") {
    return false;
  }
  if (typeof keyOrFetcher === "object" && keyOrFetcher !== null) {
    return false;
  }
  if (typeof keyOrFetcher === "function" && typeof fetcher === "function") {
    return false;
  }
  return true;
}
export function useNuxtData(key) {
  const nuxtApp = useNuxtApp();
  if (!(key in nuxtApp.payload.data)) {
    nuxtApp.payload.data[key] = void 0;
  }
  if (nuxtApp._asyncData[key]) {
    const data = nuxtApp._asyncData[key];
    data._deps++;
    if (getCurrentScope()) {
      onScopeDispose(() => {
        data._deps--;
        if (data._deps === 0) {
          data?._off();
        }
      });
    }
  }
  return {
    data: computed({
      get() {
        return nuxtApp._asyncData[key]?.data.value ?? nuxtApp.payload.data[key];
      },
      set(value) {
        if (nuxtApp._asyncData[key]) {
          nuxtApp._asyncData[key].data.value = value;
        } else {
          nuxtApp.payload.data[key] = value;
        }
      }
    })
  };
}
export async function refreshNuxtData(keys) {
  if (import.meta.server) {
    return Promise.resolve();
  }
  await new Promise((resolve) => onNuxtReady(resolve));
  const _keys = keys ? toArray(keys) : void 0;
  await useNuxtApp().hooks.callHookParallel("app:data:refresh", _keys);
}
export function clearNuxtData(keys) {
  const nuxtApp = useNuxtApp();
  const _allKeys = Object.keys(nuxtApp.payload.data);
  const _keys = !keys ? _allKeys : typeof keys === "function" ? _allKeys.filter(keys) : toArray(keys);
  for (const key of _keys) {
    clearNuxtDataByKey(nuxtApp, key);
  }
}
function clearNuxtDataByKey(nuxtApp, key) {
  if (key in nuxtApp.payload.data) {
    nuxtApp.payload.data[key] = void 0;
  }
  if (key in nuxtApp.payload._errors) {
    nuxtApp.payload._errors[key] = void 0;
  }
  if (nuxtApp._asyncData[key]) {
    nuxtApp._asyncData[key].data.value = unref(nuxtApp._asyncData[key]._default());
    nuxtApp._asyncData[key].error.value = void 0;
    if (pendingWhenIdle) {
      nuxtApp._asyncData[key].pending.value = false;
    }
    nuxtApp._asyncData[key].status.value = "idle";
  }
  if (key in nuxtApp._asyncDataPromises) {
    nuxtApp._asyncDataPromises[key] = void 0;
  }
}
function pick(obj, keys) {
  const newObj = {};
  for (const key of keys) {
    newObj[key] = obj[key];
  }
  return newObj;
}
function buildAsyncData(nuxtApp, key, _handler, options, initialCachedData) {
  nuxtApp.payload._errors[key] ??= void 0;
  const hasCustomGetCachedData = options.getCachedData !== getDefaultCachedData;
  const handler = import.meta.client || !import.meta.prerender || !nuxtApp.ssrContext?.["~sharedPrerenderCache"] ? _handler : (nuxtApp2, options2) => {
    const value = nuxtApp2.ssrContext["~sharedPrerenderCache"].get(key);
    if (value) {
      return value;
    }
    const promise = Promise.resolve().then(() => nuxtApp2.runWithContext(() => _handler(nuxtApp2, options2)));
    nuxtApp2.ssrContext["~sharedPrerenderCache"].set(key, promise);
    return promise;
  };
  const _ref = options.deep ? ref : shallowRef;
  const hasCachedData = initialCachedData !== void 0;
  const unsubRefreshAsyncData = nuxtApp.hook("app:data:refresh", async (keys) => {
    if (!keys || keys.includes(key)) {
      await asyncData.execute({ cause: "refresh:hook" });
    }
  });
  const asyncData = {
    data: _ref(hasCachedData ? initialCachedData : options.default()),
    pending: pendingWhenIdle ? shallowRef(!hasCachedData) : computed(() => asyncData.status.value === "pending"),
    error: toRef(nuxtApp.payload._errors, key),
    status: shallowRef("idle"),
    execute: (...args) => {
      const [_opts, newValue = void 0] = args;
      const opts = _opts && newValue === void 0 && typeof _opts === "object" ? _opts : {};
      if (import.meta.dev && newValue !== void 0 && (!_opts || typeof _opts !== "object")) {
        console.warn(`[nuxt] [${options._functionName}] Do not pass \`execute\` directly to \`watch\`. Instead, use an inline function, such as \`watch(q, () => execute())\`.`);
      }
      if (nuxtApp._asyncDataPromises[key]) {
        if ((opts.dedupe ?? options.dedupe) === "defer") {
          return nuxtApp._asyncDataPromises[key];
        }
      }
      if (granularCachedData || opts.cause === "initial" || nuxtApp.isHydrating) {
        const cachedData = "cachedData" in opts ? opts.cachedData : options.getCachedData(key, nuxtApp, { cause: opts.cause ?? "refresh:manual" });
        if (cachedData !== void 0) {
          nuxtApp.payload.data[key] = asyncData.data.value = cachedData;
          asyncData.error.value = void 0;
          asyncData.status.value = "success";
          return Promise.resolve(cachedData);
        }
      }
      if (pendingWhenIdle) {
        asyncData.pending.value = true;
      }
      if (asyncData._abortController) {
        asyncData._abortController.abort(new DOMException("AsyncData request cancelled by deduplication", "AbortError"));
      }
      asyncData._abortController = new AbortController();
      asyncData.status.value = "pending";
      const cleanupController = new AbortController();
      const promise = new Promise(
        (resolve, reject) => {
          try {
            const timeout = opts.timeout ?? options.timeout;
            const mergedSignal = mergeAbortSignals([asyncData._abortController?.signal, opts?.signal], cleanupController.signal, timeout);
            if (mergedSignal.aborted) {
              const reason = mergedSignal.reason;
              reject(reason instanceof Error ? reason : new DOMException(String(reason ?? "Aborted"), "AbortError"));
              return;
            }
            mergedSignal.addEventListener("abort", () => {
              const reason = mergedSignal.reason;
              reject(reason instanceof Error ? reason : new DOMException(String(reason ?? "Aborted"), "AbortError"));
            }, { once: true, signal: cleanupController.signal });
            return Promise.resolve(handler(nuxtApp, { signal: mergedSignal })).then(resolve, reject);
          } catch (err) {
            reject(err);
          }
        }
      ).then(async (_result) => {
        let result = _result;
        if (options.transform) {
          result = await options.transform(_result);
        }
        if (options.pick) {
          result = pick(result, options.pick);
        }
        if (import.meta.dev && import.meta.server && typeof result === "undefined") {
          const caller = getUserCaller();
          const explanation = caller ? ` (used at ${caller.source}:${caller.line}:${caller.column})` : "";
          console.warn(`[nuxt] \`${options._functionName || "useAsyncData"}${explanation}\` must return a value (it should not be \`undefined\`) or the request may be duplicated on the client side.`);
        }
        nuxtApp.payload.data[key] = result;
        asyncData.data.value = result;
        asyncData.error.value = void 0;
        asyncData.status.value = "success";
      }).catch((error) => {
        if (nuxtApp._asyncDataPromises[key] && nuxtApp._asyncDataPromises[key] !== promise) {
          return nuxtApp._asyncDataPromises[key];
        }
        if (asyncData._abortController?.signal.aborted) {
          return nuxtApp._asyncDataPromises[key];
        }
        if (typeof DOMException !== "undefined" && error instanceof DOMException && error.name === "AbortError") {
          asyncData.status.value = "idle";
          return nuxtApp._asyncDataPromises[key];
        }
        asyncData.error.value = createError(error);
        asyncData.data.value = unref(options.default());
        asyncData.status.value = "error";
      }).finally(() => {
        if (pendingWhenIdle) {
          asyncData.pending.value = false;
        }
        cleanupController.abort();
        delete nuxtApp._asyncDataPromises[key];
      });
      nuxtApp._asyncDataPromises[key] = promise;
      return nuxtApp._asyncDataPromises[key];
    },
    _execute: debounce((...args) => asyncData.execute(...args), 0, { leading: true }),
    _default: options.default,
    _deps: 0,
    _init: true,
    _hash: import.meta.dev ? createHash(_handler, options) : void 0,
    _off: () => {
      unsubRefreshAsyncData();
      if (nuxtApp._asyncData[key]?._init) {
        nuxtApp._asyncData[key]._init = false;
      }
      if (purgeCachedData && !hasCustomGetCachedData) {
        nextTick(() => {
          if (!nuxtApp._asyncData[key]?._init) {
            clearNuxtDataByKey(nuxtApp, key);
            asyncData.execute = () => Promise.resolve();
          }
        });
      }
    }
  };
  return asyncData;
}
const getDefault = () => void 0;
const getDefaultCachedData = (key, nuxtApp, ctx) => {
  if (nuxtApp.isHydrating) {
    return nuxtApp.payload.data[key];
  }
  if (ctx.cause !== "refresh:manual" && ctx.cause !== "refresh:hook") {
    return nuxtApp.static.data[key];
  }
};
function createHash(_handler, options) {
  return {
    handler: hash(_handler),
    transform: options.transform ? hash(options.transform) : void 0,
    pick: options.pick ? hash(options.pick) : void 0,
    getCachedData: options.getCachedData ? hash(options.getCachedData) : void 0
  };
}
function mergeAbortSignals(signals, cleanupSignal, timeout) {
  const list = signals.filter((s) => !!s);
  if (typeof timeout === "number" && timeout >= 0) {
    const timeoutSignal = AbortSignal.timeout?.(timeout);
    if (timeoutSignal) {
      list.push(timeoutSignal);
    }
  }
  if (AbortSignal.any) {
    return AbortSignal.any(list);
  }
  const controller = new AbortController();
  for (const sig of list) {
    if (sig.aborted) {
      const reason = sig.reason ?? new DOMException("Aborted", "AbortError");
      try {
        controller.abort(reason);
      } catch {
        controller.abort();
      }
      return controller.signal;
    }
  }
  const onAbort = () => {
    const abortedSignal = list.find((s) => s.aborted);
    const reason = abortedSignal?.reason ?? new DOMException("Aborted", "AbortError");
    try {
      controller.abort(reason);
    } catch {
      controller.abort();
    }
  };
  for (const sig of list) {
    sig.addEventListener?.("abort", onAbort, { once: true, signal: cleanupSignal });
  }
  return controller.signal;
}

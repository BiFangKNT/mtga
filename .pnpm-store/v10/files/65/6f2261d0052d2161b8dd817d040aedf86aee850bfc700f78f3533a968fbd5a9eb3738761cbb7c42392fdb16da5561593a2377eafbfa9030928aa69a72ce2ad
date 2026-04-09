import { parse as parseStrackTrace } from "error-stack-parser-es";
import { markRaw, reactive } from "vue";
import { useObjectStorage } from "./plugins/view/utils.js";
const nonLiteralSymbol = /* @__PURE__ */ Symbol("nuxt-devtools-fn-metrics-non-literal");
function getStacktrace() {
  return parseStrackTrace(new Error());
}
export function initTimelineMetrics() {
  if (import.meta.server)
    return void 0;
  if (window.__NUXT_DEVTOOLS_TIMELINE_METRICS__)
    return window.__NUXT_DEVTOOLS_TIMELINE_METRICS__;
  Object.defineProperty(window, "__NUXT_DEVTOOLS_TIMELINE_METRICS__", {
    value: reactive(
      window.__NUXT_DEVTOOLS_TIMELINE_METRICS__ || {
        events: [],
        nonLiteralSymbol,
        // TODO: sync with server config
        options: useObjectStorage("nuxt-devtools-timeline-metrics-options", {
          enabled: false,
          stacktrace: true,
          arguments: true
        })
      }
    ),
    enumerable: false,
    configurable: true
  });
  return window.__NUXT_DEVTOOLS_TIMELINE_METRICS__;
}
const wrapperFunctions = /* @__PURE__ */ new WeakMap();
export function __nuxtTimelineWrap(name, fn) {
  if (import.meta.server)
    return fn;
  if (typeof fn !== "function")
    return fn;
  const metrics = initTimelineMetrics();
  if (wrapperFunctions.has(fn))
    return wrapperFunctions.get(fn);
  const wrappred = function(...args) {
    if (!metrics.options.enabled)
      return fn.apply(this, args);
    const event = {
      type: "function",
      name,
      start: Date.now(),
      args: metrics.options.arguments ? markRaw(args) : void 0,
      stacktrace: metrics.options.stacktrace ? getStacktrace().slice(2) : void 0
    };
    metrics.events.push(event);
    const result = fn.apply(this, args);
    try {
      if (result && typeof result.then === "function") {
        event.isPromise = true;
        result.then((i) => i).finally(() => {
          event.end = Date.now();
          return result;
        });
        return result;
      }
    } catch {
    }
    event.end = Date.now();
    return result;
  };
  Object.defineProperty(wrappred, "length", { value: fn.name || name });
  wrapperFunctions.set(fn, wrappred);
  return wrappred;
}

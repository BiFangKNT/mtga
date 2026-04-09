import { setResponseStatus as _setResponseStatus, appendHeader, getRequestHeader, getRequestHeaders, getResponseHeader, removeResponseHeader, setResponseHeader } from "@nuxt/nitro-server/h3";
import { computed, getCurrentInstance, ref } from "vue";
import { useNuxtApp } from "../nuxt.js";
import { toArray } from "../utils.js";
import { useHead } from "./head.js";
export function useRequestEvent(nuxtApp) {
  if (import.meta.client) {
    return;
  }
  nuxtApp ||= useNuxtApp();
  return nuxtApp.ssrContext?.event;
}
export function useRequestHeaders(include) {
  if (import.meta.client) {
    return {};
  }
  const event = useRequestEvent();
  const _headers = event ? getRequestHeaders(event) : {};
  if (!include || !event) {
    return _headers;
  }
  const headers = /* @__PURE__ */ Object.create(null);
  for (const _key of include) {
    const key = _key.toLowerCase();
    const header = _headers[key];
    if (header) {
      headers[key] = header;
    }
  }
  return headers;
}
export function useRequestHeader(header) {
  if (import.meta.client) {
    return void 0;
  }
  const event = useRequestEvent();
  return event ? getRequestHeader(event, header) : void 0;
}
export function useRequestFetch() {
  if (import.meta.client) {
    return globalThis.$fetch;
  }
  return useRequestEvent()?.$fetch || globalThis.$fetch;
}
export function setResponseStatus(arg1, arg2, arg3) {
  if (import.meta.client) {
    return;
  }
  if (arg1 && typeof arg1 !== "number") {
    return _setResponseStatus(arg1, arg2, arg3);
  }
  const event = useRequestEvent();
  if (event) {
    return _setResponseStatus(event, arg1, arg2);
  }
}
export function useResponseHeader(header) {
  if (import.meta.client) {
    if (import.meta.dev) {
      return computed({
        get: () => void 0,
        set: () => console.warn("[nuxt] Setting response headers is not supported in the browser.")
      });
    }
    return ref();
  }
  const event = useRequestEvent();
  return computed({
    get() {
      return getResponseHeader(event, header);
    },
    set(newValue) {
      if (!newValue) {
        return removeResponseHeader(event, header);
      }
      return setResponseHeader(event, header, newValue);
    }
  });
}
export function prerenderRoutes(path) {
  if (!import.meta.server || !import.meta.prerender) {
    return;
  }
  const paths = toArray(path);
  appendHeader(useRequestEvent(), "x-nitro-prerender", paths.map((p) => encodeURIComponent(p)).join(", "));
}
const PREHYDRATE_ATTR_KEY = "data-prehydrate-id";
export function onPrehydrate(callback, key) {
  if (import.meta.client) {
    return;
  }
  if (typeof callback !== "string") {
    throw new TypeError("[nuxt] To transform a callback into a string, `onPrehydrate` must be processed by the Nuxt build pipeline. If it is called in a third-party library, make sure to add the library to `build.transpile`.");
  }
  const vm = getCurrentInstance();
  if (vm && key) {
    vm.attrs[PREHYDRATE_ATTR_KEY] ||= "";
    key = ":" + key + ":";
    if (!vm.attrs[PREHYDRATE_ATTR_KEY].includes(key)) {
      vm.attrs[PREHYDRATE_ATTR_KEY] += key;
    }
  }
  const code = vm && key ? `document.querySelectorAll('[${PREHYDRATE_ATTR_KEY}*=${JSON.stringify(key)}]').forEach` + callback : callback + "()";
  useHead({
    script: [{
      key: vm && key ? key : void 0,
      tagPosition: "bodyClose",
      tagPriority: "critical",
      innerHTML: code
    }]
  });
  return vm && key ? vm.attrs[PREHYDRATE_ATTR_KEY] : void 0;
}

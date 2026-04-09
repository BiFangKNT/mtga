import { shallowRef } from "vue";
export function useNuxtDevTools() {
  const r = shallowRef();
  if (!import.meta.dev)
    return r;
  if (import.meta.server)
    return r;
  if (window.__NUXT_DEVTOOLS_HOST__) {
    r.value = window.__NUXT_DEVTOOLS_HOST__;
  } else {
    Object.defineProperty(window, "__NUXT_DEVTOOLS_HOST__", {
      set(value) {
        r.value = value;
      },
      get() {
        return r.value;
      },
      enumerable: false,
      configurable: true
    });
  }
  return r;
}

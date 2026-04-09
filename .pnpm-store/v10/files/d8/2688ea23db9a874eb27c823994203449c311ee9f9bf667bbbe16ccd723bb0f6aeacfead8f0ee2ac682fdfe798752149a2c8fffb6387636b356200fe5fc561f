import { shallowRef } from "vue";
let clientRef;
const fns = [];
export function onDevtoolsHostClientConnected(fn) {
  fns.push(fn);
  if (typeof window === "undefined")
    return;
  if (window.__NUXT_DEVTOOLS_HOST__) {
    fns.forEach((fn2) => fn2(window.__NUXT_DEVTOOLS_HOST__));
  }
  Object.defineProperty(window, "__NUXT_DEVTOOLS_HOST__", {
    set(value) {
      if (value)
        fns.forEach((fn2) => fn2(value));
    },
    get() {
      return clientRef.value;
    },
    configurable: true
  });
  return () => {
    fns.splice(fns.indexOf(fn), 1);
  };
}
export function useDevtoolsHostClient() {
  if (!clientRef) {
    clientRef = shallowRef();
    onDevtoolsHostClientConnected(setup);
  }
  function setup(client) {
    clientRef.value = client;
  }
  return clientRef;
}

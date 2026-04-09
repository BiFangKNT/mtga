import { shallowRef, triggerRef } from "vue";
let clientRef;
const hasSetup = false;
const fns = [];
export function onDevtoolsClientConnected(fn) {
  fns.push(fn);
  if (hasSetup)
    return;
  if (typeof window === "undefined")
    return;
  if (window.__NUXT_DEVTOOLS__) {
    fns.forEach((fn2) => fn2(window.__NUXT_DEVTOOLS__));
  }
  Object.defineProperty(window, "__NUXT_DEVTOOLS__", {
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
export function useDevtoolsClient() {
  if (!clientRef) {
    clientRef = shallowRef();
    onDevtoolsClientConnected(setup);
  }
  function onUpdateReactivity() {
    if (clientRef) {
      triggerRef(clientRef);
    }
  }
  function setup(client) {
    clientRef.value = client;
    if (client.host)
      client.host.hooks.hook("host:update:reactivity", onUpdateReactivity);
  }
  return clientRef;
}

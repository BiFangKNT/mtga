import { useNuxtApp } from "../nuxt.js";
import { requestIdleCallback } from "../compat/idle-callback.js";
export const onNuxtReady = (callback) => {
  if (import.meta.server) {
    return;
  }
  const nuxtApp = useNuxtApp();
  if (nuxtApp.isHydrating) {
    nuxtApp.hooks.hookOnce("app:suspense:resolve", () => {
      requestIdleCallback(() => callback());
    });
  } else {
    requestIdleCallback(() => callback());
  }
};

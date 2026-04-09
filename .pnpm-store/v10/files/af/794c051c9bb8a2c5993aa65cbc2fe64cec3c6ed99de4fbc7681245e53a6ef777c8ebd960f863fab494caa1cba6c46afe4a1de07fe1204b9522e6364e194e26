import { useNuxtApp } from "../nuxt.js";
export const useHydration = (key, get, set) => {
  const nuxtApp = useNuxtApp();
  if (import.meta.server) {
    nuxtApp.hooks.hook("app:rendered", () => {
      nuxtApp.payload[key] = get();
    });
  }
  if (import.meta.client) {
    nuxtApp.hooks.hook("app:created", () => {
      set(nuxtApp.payload[key]);
    });
  }
};

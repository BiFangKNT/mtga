import { joinURL } from "ufo";
import { defineNuxtPlugin, useRuntimeConfig } from "../nuxt.js";
import { reloadNuxtApp } from "../composables/chunk.js";
import { addRouteMiddleware } from "../composables/router.js";
export default defineNuxtPlugin({
  name: "nuxt:chunk-reload-immediate",
  setup(nuxtApp) {
    let currentlyNavigationTo = null;
    addRouteMiddleware((to) => {
      currentlyNavigationTo = to;
    });
    const config = useRuntimeConfig();
    function reloadAppAtPath(to) {
      const path = joinURL(config.app.baseURL, to.fullPath);
      reloadNuxtApp({ path, persistState: true });
    }
    nuxtApp.hook("app:chunkError", () => reloadAppAtPath(currentlyNavigationTo ?? nuxtApp._route));
    nuxtApp.hook("app:manifest:update", () => reloadAppAtPath(nuxtApp._route));
  }
});

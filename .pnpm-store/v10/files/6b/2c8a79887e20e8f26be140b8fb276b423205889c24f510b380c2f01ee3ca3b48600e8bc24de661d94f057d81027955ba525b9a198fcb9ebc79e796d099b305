import { joinURL } from "ufo";
import { defineNuxtPlugin, useRuntimeConfig } from "../nuxt.js";
import { useRouter } from "../composables/router.js";
import { reloadNuxtApp } from "../composables/chunk.js";
export default defineNuxtPlugin({
  name: "nuxt:chunk-reload",
  setup(nuxtApp) {
    const router = useRouter();
    const config = useRuntimeConfig();
    const chunkErrors = /* @__PURE__ */ new Set();
    router.beforeEach(() => {
      chunkErrors.clear();
    });
    nuxtApp.hook("app:chunkError", ({ error }) => {
      chunkErrors.add(error);
    });
    function reloadAppAtPath(to) {
      const path = joinURL(config.app.baseURL, to.fullPath);
      reloadNuxtApp({ path, persistState: true });
    }
    nuxtApp.hook("app:manifest:update", () => {
      router.beforeResolve(reloadAppAtPath);
    });
    router.onError((error, to) => {
      if (chunkErrors.has(error)) {
        reloadAppAtPath(to);
      }
    });
  }
});

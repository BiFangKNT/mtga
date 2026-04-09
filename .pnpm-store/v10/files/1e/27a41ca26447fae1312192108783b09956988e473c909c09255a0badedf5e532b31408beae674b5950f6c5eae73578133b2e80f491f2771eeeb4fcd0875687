import { defineNuxtPlugin } from "../nuxt.js";
import { loadPayload } from "../composables/payload.js";
import { onNuxtReady } from "../composables/ready.js";
import { useRouter } from "../composables/router.js";
import { getAppManifest } from "../composables/manifest.js";
import { appManifest as isAppManifestEnabled, purgeCachedData } from "#build/nuxt.config.mjs";
export default defineNuxtPlugin({
  name: "nuxt:payload",
  setup(nuxtApp) {
    const staticKeysToRemove = /* @__PURE__ */ new Set();
    useRouter().beforeResolve(async (to, from) => {
      if (to.path === from.path) {
        return;
      }
      const payload = await loadPayload(to.path);
      if (!payload) {
        return;
      }
      if (purgeCachedData) {
        for (const key of staticKeysToRemove) {
          delete nuxtApp.static.data[key];
        }
      }
      for (const key in payload.data) {
        if (purgeCachedData) {
          if (!(key in nuxtApp.static.data)) {
            staticKeysToRemove.add(key);
          }
        }
        nuxtApp.static.data[key] = payload.data[key];
      }
    });
    onNuxtReady(() => {
      nuxtApp.hooks.hook("link:prefetch", async (url) => {
        const { hostname } = new URL(url, window.location.href);
        if (hostname === window.location.hostname) {
          await loadPayload(url).catch(() => {
            console.warn("[nuxt] Error preloading payload for", url);
          });
        }
      });
      if (isAppManifestEnabled && navigator.connection?.effectiveType !== "slow-2g") {
        setTimeout(getAppManifest, 1e3);
      }
    });
  }
});

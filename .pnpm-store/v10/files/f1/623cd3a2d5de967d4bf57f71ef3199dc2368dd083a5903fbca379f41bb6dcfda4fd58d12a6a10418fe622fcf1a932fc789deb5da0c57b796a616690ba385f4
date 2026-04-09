import { hasProtocol } from "ufo";
import { toArray } from "../utils.js";
import { defineNuxtPlugin } from "#app/nuxt";
import { useRouter } from "#app/composables/router";
import layouts from "#build/layouts";
import { namedMiddleware } from "#build/middleware";
import { _loadAsyncComponent } from "#app/composables/preload";
export default defineNuxtPlugin({
  name: "nuxt:prefetch",
  setup(nuxtApp) {
    const router = useRouter();
    nuxtApp.hooks.hook("app:mounted", () => {
      router.beforeEach(async (to) => {
        const layout = to?.meta?.layout;
        if (layout && typeof layouts[layout] === "function") {
          await layouts[layout]();
        }
      });
    });
    nuxtApp.hooks.hook("link:prefetch", (url) => {
      if (hasProtocol(url)) {
        return;
      }
      const route = router.resolve(url);
      if (!route) {
        return;
      }
      const layout = route.meta.layout;
      let middleware = toArray(route.meta.middleware);
      middleware = middleware.filter((m) => typeof m === "string");
      for (const name of middleware) {
        if (typeof namedMiddleware[name] === "function") {
          namedMiddleware[name]();
        }
      }
      if (typeof layout === "string" && layout in layouts) {
        _loadAsyncComponent(layouts[layout]);
      }
    });
  }
});

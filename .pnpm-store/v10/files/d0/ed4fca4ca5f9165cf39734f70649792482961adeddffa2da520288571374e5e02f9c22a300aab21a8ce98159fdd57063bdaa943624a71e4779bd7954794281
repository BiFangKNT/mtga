import { getCurrentInstance } from "vue";
import { useRoute } from "vue-router";
import { useNuxtApp } from "#app/nuxt";
const warnRuntimeUsage = (method) => {
  console.warn(
    `${method}() is a compiler-hint helper that is only usable inside the script block of a single file component which is also a page. Its arguments should be compiled away and passing it at runtime has no effect.`
  );
};
export const definePageMeta = (meta) => {
  if (import.meta.dev) {
    const component = getCurrentInstance()?.type;
    try {
      const isRouteComponent = component && useRoute().matched.some((p) => Object.values(p.components || {}).includes(component));
      const isRenderingServerPage = import.meta.server && useNuxtApp().ssrContext?.islandContext;
      if (isRouteComponent || isRenderingServerPage || component?.__clientOnlyPage) {
        return;
      }
    } catch {
    }
    warnRuntimeUsage("definePageMeta");
  }
};
export const defineRouteRules = /* @__NO_SIDE_EFFECTS__ */ (rules) => {
};

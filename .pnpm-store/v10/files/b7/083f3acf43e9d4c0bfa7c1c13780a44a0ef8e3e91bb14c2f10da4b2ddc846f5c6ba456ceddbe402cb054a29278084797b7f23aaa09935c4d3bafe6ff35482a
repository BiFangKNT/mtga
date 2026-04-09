import { useNuxtApp } from "../nuxt.js";
import { toArray } from "../utils.js";
import { useRouter } from "./router.js";
export const preloadComponents = async (components) => {
  if (import.meta.server) {
    return;
  }
  const nuxtApp = useNuxtApp();
  components = toArray(components);
  await Promise.all(components.map((name) => {
    const component = nuxtApp.vueApp._context.components[name];
    if (component) {
      return _loadAsyncComponent(component);
    }
  }));
};
export const prefetchComponents = (components) => {
  if (import.meta.server) {
    return;
  }
  return preloadComponents(components);
};
export function _loadAsyncComponent(component) {
  if (component?.__asyncLoader && !component.__asyncResolved) {
    return component.__asyncLoader();
  }
}
export async function preloadRouteComponents(to, router = useRouter()) {
  if (import.meta.server) {
    return;
  }
  const { path, matched } = router.resolve(to);
  if (!matched.length) {
    return;
  }
  router._routePreloaded ||= /* @__PURE__ */ new Set();
  if (router._routePreloaded.has(path)) {
    return;
  }
  const promises = router._preloadPromises ||= [];
  if (promises.length > 4) {
    return Promise.all(promises).then(() => preloadRouteComponents(to, router));
  }
  router._routePreloaded.add(path);
  for (const route of matched) {
    const component = route.components?.default;
    if (typeof component !== "function") {
      continue;
    }
    const promise = Promise.resolve(component()).catch(() => {
    }).finally(() => promises.splice(promises.indexOf(promise), 1));
    promises.push(promise);
  }
  await Promise.all(promises);
}

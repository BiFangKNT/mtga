import { joinURL } from "ufo";
import { defineNuxtPlugin } from "#app/nuxt";
import { prerenderRoutes } from "#app/composables/ssr";
import _routes from "#build/routes";
import routerOptions, { hashMode } from "#build/router.options.mjs";
import { crawlLinks } from "#build/nuxt.config.mjs";
import _routeRulesMatcher from "#build/route-rules.mjs";
const routeRulesMatcher = _routeRulesMatcher;
let routes;
export default defineNuxtPlugin(async () => {
  if (!import.meta.server || !import.meta.prerender || hashMode) {
    return;
  }
  if (routes && !routes.length) {
    return;
  }
  routes ||= Array.from(processRoutes(await routerOptions.routes?.(_routes) ?? _routes));
  const batch = routes.splice(0, 10);
  prerenderRoutes(batch);
});
const OPTIONAL_PARAM_RE = /^\/?:.*(?:\?|\(\.\*\)\*)$/;
function shouldPrerender(path) {
  return crawlLinks || !!routeRulesMatcher(path).prerender;
}
function processRoutes(routes2, currentPath = "/", routesToPrerender = /* @__PURE__ */ new Set()) {
  for (const route of routes2) {
    if (OPTIONAL_PARAM_RE.test(route.path) && !route.children?.length && shouldPrerender(currentPath)) {
      routesToPrerender.add(currentPath);
    }
    if (route.path.includes(":")) {
      continue;
    }
    const fullPath = joinURL(currentPath, route.path);
    if (shouldPrerender(fullPath)) {
      routesToPrerender.add(fullPath);
    }
    if (route.children) {
      processRoutes(route.children, fullPath, routesToPrerender);
    }
  }
  return routesToPrerender;
}

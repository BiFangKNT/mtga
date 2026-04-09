import { isReadonly, reactive, shallowReactive, shallowRef } from "vue";
import { START_LOCATION, createMemoryHistory, createRouter, createWebHashHistory, createWebHistory } from "vue-router";
import { isSamePath, withoutBase } from "ufo";
import { toArray } from "../utils.js";
import { getRouteRules } from "#app/composables/manifest";
import { defineNuxtPlugin, useRuntimeConfig } from "#app/nuxt";
import { clearError, createError, isNuxtError, showError, useError } from "#app/composables/error";
import { navigateTo } from "#app/composables/router";
import _routes, { handleHotUpdate } from "#build/routes";
import routerOptions, { hashMode } from "#build/router.options.mjs";
import { globalMiddleware, namedMiddleware } from "#build/middleware";
function createCurrentLocation(base, location, renderedPath) {
  const { pathname, search, hash } = location;
  const hashPos = base.indexOf("#");
  if (hashPos > -1) {
    const slicePos = hash.includes(base.slice(hashPos)) ? base.slice(hashPos).length : 1;
    let pathFromHash = hash.slice(slicePos);
    if (pathFromHash[0] !== "/") {
      pathFromHash = "/" + pathFromHash;
    }
    return withoutBase(pathFromHash, "");
  }
  const displayedPath = withoutBase(pathname, base);
  const path = !renderedPath || isSamePath(displayedPath, renderedPath) ? displayedPath : renderedPath;
  return path + (path.includes("?") ? "" : search) + hash;
}
const plugin = defineNuxtPlugin({
  name: "nuxt:router",
  enforce: "pre",
  async setup(nuxtApp) {
    let routerBase = useRuntimeConfig().app.baseURL;
    if (hashMode && !routerBase.includes("#")) {
      routerBase += "#";
    }
    const history = routerOptions.history?.(routerBase) ?? (import.meta.client ? hashMode ? createWebHashHistory(routerBase) : createWebHistory(routerBase) : createMemoryHistory(routerBase));
    const routes = routerOptions.routes ? await routerOptions.routes(_routes) ?? _routes : _routes;
    let startPosition;
    const router = createRouter({
      ...routerOptions,
      scrollBehavior: (to, from, savedPosition) => {
        if (from === START_LOCATION) {
          startPosition = savedPosition;
          return;
        }
        if (routerOptions.scrollBehavior) {
          router.options.scrollBehavior = routerOptions.scrollBehavior;
          if ("scrollRestoration" in window.history) {
            const unsub = router.beforeEach(() => {
              unsub();
              window.history.scrollRestoration = "manual";
            });
          }
          return routerOptions.scrollBehavior(to, START_LOCATION, startPosition || savedPosition);
        }
      },
      history,
      routes
    });
    if (import.meta.hot) {
      handleHotUpdate(router, routerOptions.routes ? routerOptions.routes : (routes2) => routes2);
    }
    if (import.meta.client && "scrollRestoration" in window.history) {
      window.history.scrollRestoration = "auto";
    }
    nuxtApp.vueApp.use(router);
    const previousRoute = shallowRef(router.currentRoute.value);
    router.afterEach((_to, from) => {
      previousRoute.value = from;
    });
    Object.defineProperty(nuxtApp.vueApp.config.globalProperties, "previousRoute", {
      get: () => previousRoute.value
    });
    const initialURL = import.meta.server ? nuxtApp.ssrContext.url : createCurrentLocation(routerBase, window.location, nuxtApp.payload.path);
    const _route = shallowRef(router.currentRoute.value);
    const syncCurrentRoute = () => {
      _route.value = router.currentRoute.value;
    };
    router.afterEach((to, from) => {
      if (to.matched.at(-1)?.components?.default === from.matched.at(-1)?.components?.default) {
        syncCurrentRoute();
      }
    });
    const route = { sync: syncCurrentRoute };
    for (const key in _route.value) {
      Object.defineProperty(route, key, {
        get: () => _route.value[key],
        enumerable: true
      });
    }
    nuxtApp._route = shallowReactive(route);
    nuxtApp._middleware ||= {
      global: [],
      named: {}
    };
    const error = useError();
    if (import.meta.client || !nuxtApp.ssrContext?.islandContext) {
      router.afterEach(async (to, _from, failure) => {
        delete nuxtApp._processingMiddleware;
        if (import.meta.client && !nuxtApp.isHydrating && error.value) {
          await nuxtApp.runWithContext(clearError);
        }
        if (failure) {
          await nuxtApp.callHook("page:loading:end");
        }
        if (import.meta.server && failure?.type === 4) {
          return;
        }
        if (import.meta.server && to.redirectedFrom && to.fullPath !== initialURL) {
          await nuxtApp.runWithContext(() => navigateTo(to.fullPath || "/"));
        }
      });
    }
    try {
      if (import.meta.server) {
        await router.push(initialURL);
      }
      await router.isReady();
    } catch (error2) {
      await nuxtApp.runWithContext(() => showError(error2));
    }
    const resolvedInitialRoute = import.meta.client && initialURL !== router.currentRoute.value.fullPath ? router.resolve(initialURL) : router.currentRoute.value;
    const hasDeferredRoute = import.meta.client && nuxtApp.isHydrating && nuxtApp.payload.prerenderedAt && nuxtApp.payload.path && initialURL !== nuxtApp.payload.path && isSamePath(router.currentRoute.value.path, nuxtApp.payload.path);
    syncCurrentRoute();
    if (import.meta.server && nuxtApp.ssrContext?.islandContext) {
      return { provide: { router } };
    }
    const initialLayout = nuxtApp.payload.state._layout;
    router.beforeEach(async (to, from) => {
      await nuxtApp.callHook("page:loading:start");
      to.meta = reactive(to.meta);
      if (nuxtApp.isHydrating && initialLayout && !isReadonly(to.meta.layout)) {
        to.meta.layout = initialLayout;
      }
      nuxtApp._processingMiddleware = true;
      if (import.meta.client || !nuxtApp.ssrContext?.islandContext) {
        const middlewareEntries = /* @__PURE__ */ new Set([...globalMiddleware, ...nuxtApp._middleware.global]);
        for (const component of to.matched) {
          const componentMiddleware = component.meta.middleware;
          if (!componentMiddleware) {
            continue;
          }
          for (const entry of toArray(componentMiddleware)) {
            middlewareEntries.add(entry);
          }
        }
        const routeRules = getRouteRules({ path: to.path });
        if (routeRules.appMiddleware) {
          for (const key in routeRules.appMiddleware) {
            if (routeRules.appMiddleware[key]) {
              middlewareEntries.add(key);
            } else {
              middlewareEntries.delete(key);
            }
          }
        }
        for (const entry of middlewareEntries) {
          const middleware = typeof entry === "string" ? nuxtApp._middleware.named[entry] || await namedMiddleware[entry]?.().then((r) => r.default || r) : entry;
          if (!middleware) {
            if (import.meta.dev) {
              throw new Error(`Unknown route middleware: '${entry}'. Valid middleware: ${Object.keys(namedMiddleware).map((mw) => `'${mw}'`).join(", ")}.`);
            }
            throw new Error(`Unknown route middleware: '${entry}'.`);
          }
          try {
            if (import.meta.dev) {
              nuxtApp._processingMiddleware = middleware._path || (typeof entry === "string" ? entry : true);
            }
            const result = await nuxtApp.runWithContext(() => middleware(to, from));
            if (import.meta.server || !nuxtApp.payload.serverRendered && nuxtApp.isHydrating) {
              if (result === false || result instanceof Error) {
                const error2 = result || createError({
                  status: 404,
                  statusText: `Page Not Found: ${initialURL}`
                });
                await nuxtApp.runWithContext(() => showError(error2));
                return false;
              }
            }
            if (result === true) {
              continue;
            }
            if (result === false) {
              return result;
            }
            if (result) {
              if (isNuxtError(result) && result.fatal) {
                await nuxtApp.runWithContext(() => showError(result));
              }
              return result;
            }
          } catch (err) {
            const error2 = createError(err);
            if (error2.fatal) {
              await nuxtApp.runWithContext(() => showError(error2));
            }
            return error2;
          }
        }
      }
    });
    router.onError(async () => {
      delete nuxtApp._processingMiddleware;
      await nuxtApp.callHook("page:loading:end");
    });
    router.afterEach((to) => {
      if (to.matched.length === 0 && !error.value) {
        return nuxtApp.runWithContext(() => showError(createError({
          status: 404,
          fatal: false,
          statusText: `Page not found: ${to.fullPath}`,
          data: {
            path: to.fullPath
          }
        })));
      }
    });
    nuxtApp.hooks.hookOnce("app:created", async () => {
      try {
        if ("name" in resolvedInitialRoute) {
          resolvedInitialRoute.name = void 0;
        }
        if (hasDeferredRoute) {
          const payloadRoute = router.resolve(nuxtApp.payload.path);
          if ("name" in payloadRoute) {
            payloadRoute.name = void 0;
          }
          await router.replace({ ...payloadRoute, force: true });
          nuxtApp.hooks.hookOnce("app:suspense:resolve", async () => {
            await router.replace({ ...resolvedInitialRoute, force: true });
          });
        } else {
          await router.replace({
            ...resolvedInitialRoute,
            force: true
          });
        }
        router.options.scrollBehavior = routerOptions.scrollBehavior;
      } catch (error2) {
        await nuxtApp.runWithContext(() => showError(error2));
      }
    });
    return { provide: { router } };
  }
});
export default plugin;

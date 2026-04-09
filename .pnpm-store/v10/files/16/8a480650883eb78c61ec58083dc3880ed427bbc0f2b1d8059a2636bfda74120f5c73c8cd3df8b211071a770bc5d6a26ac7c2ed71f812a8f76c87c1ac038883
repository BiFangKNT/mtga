import { Fragment, Suspense, defineComponent, h, inject, nextTick, onBeforeUnmount, ref, watch } from "vue";
import { RouterView } from "vue-router";
import { generateRouteKey, wrapInKeepAlive } from "./utils.js";
import { RouteProvider, defineRouteProvider } from "#app/components/route-provider";
import { useNuxtApp } from "#app/nuxt";
import { useRouter } from "#app/composables/router";
import { _mergeTransitionProps, _wrapInTransition } from "#app/components/utils";
import { LayoutMetaSymbol, PageRouteSymbol } from "#app/components/injections";
import { appKeepalive as defaultKeepaliveConfig, appPageTransition as defaultPageTransition } from "#build/nuxt.config.mjs";
const _routeProviders = import.meta.dev ? /* @__PURE__ */ new Map() : /* @__PURE__ */ new WeakMap();
export default defineComponent({
  name: "NuxtPage",
  inheritAttrs: false,
  props: {
    name: {
      type: String
    },
    transition: {
      type: [Boolean, Object],
      default: void 0
    },
    keepalive: {
      type: [Boolean, Object],
      default: void 0
    },
    route: {
      type: Object
    },
    pageKey: {
      type: [Function, String],
      default: null
    }
  },
  setup(props, { attrs, slots, expose }) {
    const nuxtApp = useNuxtApp();
    const pageRef = ref();
    const forkRoute = inject(PageRouteSymbol, null);
    let previousPageKey;
    expose({ pageRef });
    const _layoutMeta = inject(LayoutMetaSymbol, null);
    let vnode;
    const done = nuxtApp.deferHydration();
    let isSuspensePending = false;
    let suspenseKey = 0;
    if (import.meta.client && nuxtApp.isHydrating) {
      const removeErrorHook = nuxtApp.hooks.hookOnce("app:error", done);
      useRouter().beforeEach(removeErrorHook);
    }
    if (import.meta.client && props.pageKey) {
      watch(() => props.pageKey, (next, prev) => {
        if (next !== prev) {
          nuxtApp.callHook("page:loading:start");
        }
      });
    }
    if (import.meta.dev) {
      nuxtApp._isNuxtPageUsed = true;
    }
    let pageLoadingEndHookAlreadyCalled = false;
    if (import.meta.client) {
      const unsub = useRouter().beforeResolve(() => {
        pageLoadingEndHookAlreadyCalled = false;
      });
      onBeforeUnmount(() => {
        unsub();
        done();
      });
    }
    return () => {
      return h(RouterView, { name: props.name, route: props.route, ...attrs }, {
        default: import.meta.server ? (routeProps) => {
          return h(Suspense, { suspensible: true }, {
            default() {
              return h(RouteProvider, {
                vnode: slots.default ? normalizeSlot(slots.default, routeProps) : routeProps.Component,
                route: routeProps.route,
                vnodeRef: pageRef
              });
            }
          });
        } : (routeProps) => {
          const isRenderingNewRouteInOldFork = haveParentRoutesRendered(forkRoute, routeProps.route, routeProps.Component);
          const hasSameChildren = forkRoute && forkRoute.matched.length === routeProps.route.matched.length;
          if (!routeProps.Component) {
            if (vnode && !hasSameChildren) {
              return vnode;
            }
            done();
            return;
          }
          if (vnode && _layoutMeta && !_layoutMeta.isCurrent(routeProps.route)) {
            return vnode;
          }
          if (isRenderingNewRouteInOldFork && forkRoute && (!_layoutMeta || _layoutMeta?.isCurrent(forkRoute))) {
            if (hasSameChildren || vnode) {
              return vnode;
            }
            return null;
          }
          const key = generateRouteKey(routeProps, props.pageKey);
          const willRenderAnotherChild = hasChildrenRoutes(forkRoute, routeProps.route, routeProps.Component);
          if (!nuxtApp.isHydrating && previousPageKey === key && !willRenderAnotherChild) {
            nextTick(() => {
              if (!pageLoadingEndHookAlreadyCalled) {
                pageLoadingEndHookAlreadyCalled = true;
                nuxtApp.callHook("page:loading:end");
              }
            });
          }
          if (isSuspensePending && previousPageKey !== key) {
            suspenseKey++;
          }
          previousPageKey = key;
          const hasTransition = !!(props.transition ?? routeProps.route.meta.pageTransition ?? defaultPageTransition);
          const transitionProps = hasTransition && _mergeTransitionProps([
            props.transition,
            routeProps.route.meta.pageTransition,
            defaultPageTransition,
            {
              onAfterLeave() {
                nuxtApp["~transitionFinish"]?.();
                delete nuxtApp["~transitionFinish"];
                delete nuxtApp["~transitionPromise"];
                nuxtApp.callHook("page:transition:finish", routeProps.Component);
              }
            }
          ]);
          const keepaliveConfig = props.keepalive ?? routeProps.route.meta.keepalive ?? defaultKeepaliveConfig;
          vnode = _wrapInTransition(
            hasTransition && transitionProps,
            wrapInKeepAlive(
              keepaliveConfig,
              h(Suspense, {
                key: suspenseKey,
                suspensible: true,
                onPending: () => {
                  isSuspensePending = true;
                  if (hasTransition && !nuxtApp["~transitionPromise"]) {
                    nuxtApp["~transitionPromise"] = new Promise((resolve) => {
                      nuxtApp["~transitionFinish"] = resolve;
                    });
                  }
                  nuxtApp.callHook("page:start", routeProps.Component);
                },
                onResolve: async () => {
                  isSuspensePending = false;
                  try {
                    await nextTick();
                    nuxtApp._route.sync?.();
                    await nuxtApp.callHook("page:finish", routeProps.Component);
                    if (!pageLoadingEndHookAlreadyCalled && !willRenderAnotherChild) {
                      pageLoadingEndHookAlreadyCalled = true;
                      await nuxtApp.callHook("page:loading:end");
                    }
                  } finally {
                    done();
                  }
                }
              }, {
                default: () => {
                  const routeProviderProps = {
                    key: key || void 0,
                    vnode: slots.default ? normalizeSlot(slots.default, routeProps) : routeProps.Component,
                    route: routeProps.route,
                    renderKey: key || void 0,
                    trackRootNodes: hasTransition,
                    vnodeRef: pageRef
                  };
                  if (!keepaliveConfig) {
                    return h(RouteProvider, routeProviderProps);
                  }
                  const routerComponentType = routeProps.Component.type;
                  const routeProviderKey = import.meta.dev ? routerComponentType.name || routerComponentType.__name : routerComponentType;
                  let PageRouteProvider = _routeProviders.get(routeProviderKey);
                  if (!PageRouteProvider) {
                    PageRouteProvider = defineRouteProvider(routerComponentType.name || routerComponentType.__name);
                    _routeProviders.set(routeProviderKey, PageRouteProvider);
                  }
                  return h(PageRouteProvider, routeProviderProps);
                }
              })
            )
          ).default();
          return vnode;
        }
      });
    };
  }
});
function haveParentRoutesRendered(fork, newRoute, Component) {
  if (!fork) {
    return false;
  }
  const index = newRoute.matched.findIndex((m) => m.components?.default === Component?.type);
  if (!index || index === -1) {
    return false;
  }
  return newRoute.matched.slice(0, index).some(
    (c, i) => c.components?.default !== fork.matched[i]?.components?.default
  ) || Component && generateRouteKey({ route: newRoute, Component }) !== generateRouteKey({ route: fork, Component });
}
function hasChildrenRoutes(fork, newRoute, Component) {
  if (!fork) {
    return false;
  }
  const index = newRoute.matched.findIndex((m) => m.components?.default === Component?.type);
  return index < newRoute.matched.length - 1;
}
function normalizeSlot(slot, data) {
  const slotContent = slot(data);
  return slotContent.length === 1 ? h(slotContent[0]) : h(Fragment, void 0, slotContent);
}

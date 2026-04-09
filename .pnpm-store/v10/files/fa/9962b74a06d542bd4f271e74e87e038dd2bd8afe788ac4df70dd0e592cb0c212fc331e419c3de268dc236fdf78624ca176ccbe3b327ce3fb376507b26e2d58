import { Suspense, computed, defineComponent, h, inject, mergeProps, nextTick, onMounted, provide, shallowReactive, shallowRef, unref } from "vue";
import { useRoute, useRouter } from "../composables/router.js";
import { useNuxtApp } from "../nuxt.js";
import { _mergeTransitionProps, _wrapInTransition } from "./utils.js";
import { LayoutMetaSymbol, PageRouteSymbol } from "./injections.js";
import { useRoute as useVueRouterRoute } from "#build/pages";
import layouts from "#build/layouts";
import { appLayoutTransition as defaultLayoutTransition } from "#build/nuxt.config.mjs";
import _routeRulesMatcher from "#build/route-rules.mjs";
const routeRulesMatcher = _routeRulesMatcher;
const LayoutLoader = defineComponent({
  name: "LayoutLoader",
  inheritAttrs: false,
  props: {
    name: String,
    layoutProps: Object
  },
  setup(props, context) {
    return () => h(layouts[props.name], props.layoutProps, context.slots);
  }
});
const nuxtLayoutProps = {
  name: {
    type: [String, Boolean, Object],
    default: null
  },
  fallback: {
    type: [String, Object],
    default: null
  }
};
export default defineComponent({
  name: "NuxtLayout",
  inheritAttrs: false,
  props: nuxtLayoutProps,
  setup(props, context) {
    const nuxtApp = useNuxtApp();
    const injectedRoute = inject(PageRouteSymbol);
    const shouldUseEagerRoute = !injectedRoute || injectedRoute === useRoute();
    const route = shouldUseEagerRoute ? useVueRouterRoute() : injectedRoute;
    const layout = computed(() => {
      let layout2 = unref(props.name) ?? route?.meta.layout ?? routeRulesMatcher(route?.path).appLayout ?? "default";
      if (layout2 && !(layout2 in layouts)) {
        if (import.meta.dev && layout2 !== "default") {
          console.warn(`Invalid layout \`${layout2}\` selected.`);
        }
        if (props.fallback) {
          layout2 = unref(props.fallback);
        }
      }
      return layout2;
    });
    const layoutRef = shallowRef();
    context.expose({ layoutRef });
    const done = nuxtApp.deferHydration();
    if (import.meta.client && nuxtApp.isHydrating) {
      const removeErrorHook = nuxtApp.hooks.hookOnce("app:error", done);
      useRouter().beforeEach(removeErrorHook);
    }
    if (import.meta.dev) {
      nuxtApp._isNuxtLayoutUsed = true;
    }
    let lastLayout;
    return () => {
      const hasLayout = !!layout.value && layout.value in layouts;
      const hasTransition = hasLayout && !!(route?.meta.layoutTransition ?? defaultLayoutTransition);
      const transitionProps = hasTransition && _mergeTransitionProps([
        route?.meta.layoutTransition,
        defaultLayoutTransition,
        {
          onBeforeLeave() {
            nuxtApp["~transitionPromise"] = new Promise((resolve) => {
              nuxtApp["~transitionFinish"] = resolve;
            });
          },
          onAfterLeave() {
            nuxtApp["~transitionFinish"]?.();
            delete nuxtApp["~transitionFinish"];
            delete nuxtApp["~transitionPromise"];
          }
        }
      ]);
      const previouslyRenderedLayout = lastLayout;
      lastLayout = layout.value;
      return _wrapInTransition(transitionProps, {
        default: () => h(
          Suspense,
          {
            suspensible: true,
            onResolve: async () => {
              await nextTick(done);
            }
          },
          {
            default: () => h(
              LayoutProvider,
              {
                layoutProps: mergeProps(context.attrs, route.meta.layoutProps ?? {}, { ref: layoutRef }),
                key: layout.value || void 0,
                name: layout.value,
                shouldProvide: !props.name,
                isRenderingNewLayout: (name) => {
                  return name !== previouslyRenderedLayout && name === layout.value;
                },
                hasTransition
              },
              context.slots
            )
          }
        )
      }).default();
    };
  }
});
const LayoutProvider = defineComponent({
  name: "NuxtLayoutProvider",
  inheritAttrs: false,
  props: {
    name: {
      type: [String, Boolean]
    },
    layoutProps: {
      type: Object
    },
    hasTransition: {
      type: Boolean
    },
    shouldProvide: {
      type: Boolean
    },
    isRenderingNewLayout: {
      type: Function,
      required: true
    }
  },
  setup(props, context) {
    const name = props.name;
    if (props.shouldProvide) {
      provide(LayoutMetaSymbol, {
        // When name=false, always return true so NuxtPage doesn't skip rendering
        isCurrent: (route) => name === false || name === (route.meta.layout ?? routeRulesMatcher(route.path).appLayout ?? "default")
      });
    }
    const injectedRoute = inject(PageRouteSymbol);
    const isNotWithinNuxtPage = injectedRoute && injectedRoute === useRoute();
    if (isNotWithinNuxtPage) {
      const vueRouterRoute = useVueRouterRoute();
      const reactiveChildRoute = {};
      for (const _key in vueRouterRoute) {
        const key = _key;
        Object.defineProperty(reactiveChildRoute, key, {
          enumerable: true,
          get: () => {
            return props.isRenderingNewLayout(props.name) ? vueRouterRoute[key] : injectedRoute[key];
          }
        });
      }
      provide(PageRouteSymbol, shallowReactive(reactiveChildRoute));
    }
    let vnode;
    if (import.meta.dev && import.meta.client) {
      onMounted(() => {
        nextTick(() => {
          if (["#comment", "#text"].includes(vnode?.el?.nodeName)) {
            if (name) {
              console.warn(`[nuxt] \`${name}\` layout does not have a single root node and will cause errors when navigating between routes.`);
            } else {
              console.warn("[nuxt] `<NuxtLayout>` needs to be passed a single root node in its default slot.");
            }
          }
        });
      });
    }
    return () => {
      if (!name || typeof name === "string" && !(name in layouts)) {
        if (import.meta.dev && import.meta.client && props.hasTransition) {
          vnode = context.slots.default?.();
          return vnode;
        }
        return context.slots.default?.();
      }
      if (import.meta.dev && import.meta.client && props.hasTransition) {
        vnode = h(
          LayoutLoader,
          { key: name, layoutProps: props.layoutProps, name },
          context.slots
        );
        return vnode;
      }
      return h(
        LayoutLoader,
        { key: name, layoutProps: props.layoutProps, name },
        context.slots
      );
    };
  }
});

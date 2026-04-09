import { computed, defineComponent, h, inject, onBeforeUnmount, onMounted, provide, ref, resolveComponent, shallowRef, unref } from "vue";
import { hasProtocol, joinURL, parseQuery, withTrailingSlash, withoutTrailingSlash } from "ufo";
import { preloadRouteComponents } from "../composables/preload.js";
import { onNuxtReady } from "../composables/ready.js";
import { encodeRoutePath, navigateTo, resolveRouteObject, useRouter } from "../composables/router.js";
import { useNuxtApp, useRuntimeConfig } from "../nuxt.js";
import { cancelIdleCallback, requestIdleCallback } from "../compat/idle-callback.js";
import { nuxtLinkDefaults } from "#build/nuxt.config.mjs";
import { hashMode } from "#build/router.options.mjs";
const firstNonUndefined = (...args) => args.find((arg) => arg !== void 0);
const NuxtLinkDevKeySymbol = Symbol("nuxt-link-dev-key");
// @__NO_SIDE_EFFECTS__
export function defineNuxtLink(options) {
  const componentName = options.componentName || "NuxtLink";
  function checkPropConflicts(props, main, sub) {
    if (import.meta.dev && props[main] !== void 0 && props[sub] !== void 0) {
      console.warn(`[${componentName}] \`${main}\` and \`${sub}\` cannot be used together. \`${sub}\` will be ignored.`);
    }
  }
  function isHashLinkWithoutHashMode(link) {
    return !hashMode && typeof link === "string" && link.startsWith("#");
  }
  function resolveTrailingSlashBehavior(to, resolve, trailingSlash) {
    const effectiveTrailingSlash = trailingSlash ?? options.trailingSlash;
    if (!to || effectiveTrailingSlash !== "append" && effectiveTrailingSlash !== "remove") {
      return to;
    }
    if (typeof to === "string") {
      return applyTrailingSlashBehavior(to, effectiveTrailingSlash);
    }
    const path = "path" in to && to.path !== void 0 ? to.path : resolve(to).path;
    const resolvedPath = {
      ...to,
      name: void 0,
      // named routes would otherwise always override trailing slash behavior
      path: applyTrailingSlashBehavior(path, effectiveTrailingSlash)
    };
    return resolvedPath;
  }
  function useNuxtLink(props) {
    const router = useRouter();
    const config = useRuntimeConfig();
    const hasTarget = computed(() => !!unref(props.target) && unref(props.target) !== "_self");
    const isAbsoluteUrl = computed(() => {
      const path = unref(props.to) || unref(props.href) || "";
      return typeof path === "string" && hasProtocol(path, { acceptRelative: true });
    });
    const builtinRouterLink = resolveComponent("RouterLink");
    const useBuiltinLink = builtinRouterLink && typeof builtinRouterLink !== "string" ? builtinRouterLink.useLink : void 0;
    const isExternal = computed(() => {
      if (unref(props.external)) {
        return true;
      }
      const path = unref(props.to) || unref(props.href) || "";
      if (typeof path === "object") {
        return false;
      }
      return path === "" || isAbsoluteUrl.value;
    });
    const to = computed(() => {
      checkPropConflicts(props, "to", "href");
      const path = unref(props.to) || unref(props.href) || "";
      if (isExternal.value) {
        return path;
      }
      return resolveTrailingSlashBehavior(path, router.resolve, unref(props.trailingSlash));
    });
    const link = isExternal.value ? void 0 : useBuiltinLink?.({ ...props, to, viewTransition: unref(props.viewTransition) });
    const href = computed(() => {
      const effectiveTrailingSlash = unref(props.trailingSlash) ?? options.trailingSlash;
      if (!to.value || isAbsoluteUrl.value || isHashLinkWithoutHashMode(to.value)) {
        return to.value;
      }
      if (isExternal.value) {
        const path = typeof to.value === "object" && "path" in to.value ? resolveRouteObject(to.value) : to.value;
        const href2 = typeof path === "object" ? router.resolve(path).href : path;
        return applyTrailingSlashBehavior(href2, effectiveTrailingSlash);
      }
      if (typeof to.value === "object") {
        return router.resolve(to.value)?.href ?? null;
      }
      return applyTrailingSlashBehavior(joinURL(config.app.baseURL, to.value), effectiveTrailingSlash);
    });
    return {
      to,
      hasTarget,
      isAbsoluteUrl,
      isExternal,
      //
      href,
      isActive: link?.isActive ?? computed(() => to.value === router.currentRoute.value.path),
      isExactActive: link?.isExactActive ?? computed(() => to.value === router.currentRoute.value.path),
      route: link?.route ?? computed(() => router.resolve(to.value)),
      async navigate(_e) {
        await navigateTo(href.value, { replace: unref(props.replace), external: isExternal.value || hasTarget.value });
      }
    };
  }
  return defineComponent({
    name: componentName,
    props: {
      // Routing
      to: {
        type: [String, Object],
        default: void 0,
        required: false
      },
      href: {
        type: [String, Object],
        default: void 0,
        required: false
      },
      // Attributes
      target: {
        type: String,
        default: void 0,
        required: false
      },
      rel: {
        type: String,
        default: void 0,
        required: false
      },
      noRel: {
        type: Boolean,
        default: void 0,
        required: false
      },
      // Prefetching
      prefetch: {
        type: Boolean,
        default: void 0,
        required: false
      },
      prefetchOn: {
        type: [String, Object],
        default: void 0,
        required: false
      },
      noPrefetch: {
        type: Boolean,
        default: void 0,
        required: false
      },
      // Styling
      activeClass: {
        type: String,
        default: void 0,
        required: false
      },
      exactActiveClass: {
        type: String,
        default: void 0,
        required: false
      },
      prefetchedClass: {
        type: String,
        default: void 0,
        required: false
      },
      // Vue Router's `<RouterLink>` additional props
      replace: {
        type: Boolean,
        default: void 0,
        required: false
      },
      ariaCurrentValue: {
        type: String,
        default: void 0,
        required: false
      },
      // Edge cases handling
      external: {
        type: Boolean,
        default: void 0,
        required: false
      },
      // Slot API
      custom: {
        type: Boolean,
        default: void 0,
        required: false
      },
      // Behavior
      trailingSlash: {
        type: String,
        default: void 0,
        required: false
      }
    },
    useLink: useNuxtLink,
    setup(props, { slots }) {
      const router = useRouter();
      const { to, href, navigate, isExternal, hasTarget, isAbsoluteUrl } = useNuxtLink(props);
      const prefetched = shallowRef(false);
      const el = import.meta.server ? void 0 : ref(null);
      const elRef = import.meta.server ? void 0 : (ref2) => {
        el.value = props.custom ? ref2?.$el?.nextElementSibling : ref2?.$el;
      };
      function shouldPrefetch(mode) {
        if (import.meta.server) {
          return;
        }
        return !prefetched.value && (typeof props.prefetchOn === "string" ? props.prefetchOn === mode : props.prefetchOn?.[mode] ?? options.prefetchOn?.[mode]) && (props.prefetch ?? options.prefetch) !== false && props.noPrefetch !== true && props.target !== "_blank" && !isSlowConnection();
      }
      async function prefetch(nuxtApp = useNuxtApp()) {
        if (import.meta.server) {
          return;
        }
        if (prefetched.value) {
          return;
        }
        prefetched.value = true;
        const path = typeof to.value === "string" ? to.value : isExternal.value ? resolveRouteObject(to.value) : router.resolve(to.value).fullPath;
        const normalizedPath = isExternal.value ? new URL(path, window.location.href).href : path;
        await Promise.all([
          nuxtApp.hooks.callHook("link:prefetch", normalizedPath)?.catch(() => {
          }),
          !import.meta.dev && !isExternal.value && !hasTarget.value && preloadRouteComponents(to.value, router).catch(() => {
          })
        ]);
      }
      if (import.meta.client) {
        checkPropConflicts(props, "noPrefetch", "prefetch");
        if (shouldPrefetch("visibility")) {
          const nuxtApp = useNuxtApp();
          let idleId;
          let unobserve = null;
          onMounted(() => {
            const observer = useObserver();
            onNuxtReady(() => {
              idleId = requestIdleCallback(() => {
                if (el?.value?.tagName) {
                  unobserve = observer.observe(el.value, async () => {
                    unobserve?.();
                    unobserve = null;
                    await prefetch(nuxtApp);
                  });
                }
              });
            });
          });
          onBeforeUnmount(() => {
            if (idleId) {
              cancelIdleCallback(idleId);
            }
            unobserve?.();
            unobserve = null;
          });
        }
      }
      if (import.meta.dev && import.meta.server && !props.custom) {
        const isNuxtLinkChild = inject(NuxtLinkDevKeySymbol, false);
        if (isNuxtLinkChild) {
          console.log("[nuxt] [NuxtLink] You can't nest one <a> inside another <a>. This will cause a hydration error on client-side. You can pass the `custom` prop to take full control of the markup.");
        } else {
          provide(NuxtLinkDevKeySymbol, true);
        }
      }
      return () => {
        if (!isExternal.value && !hasTarget.value && !isHashLinkWithoutHashMode(to.value)) {
          const routerLinkProps = {
            ref: elRef,
            to: to.value,
            activeClass: props.activeClass || options.activeClass,
            exactActiveClass: props.exactActiveClass || options.exactActiveClass,
            replace: props.replace,
            ariaCurrentValue: props.ariaCurrentValue,
            custom: props.custom
          };
          if (!props.custom) {
            if (import.meta.client) {
              if (shouldPrefetch("interaction")) {
                routerLinkProps.onPointerenter = prefetch.bind(null, void 0);
                routerLinkProps.onFocus = prefetch.bind(null, void 0);
              }
              if (prefetched.value) {
                routerLinkProps.class = props.prefetchedClass || options.prefetchedClass;
              }
            }
            routerLinkProps.rel = props.rel || void 0;
          }
          return h(
            resolveComponent("RouterLink"),
            routerLinkProps,
            slots.default
          );
        }
        const target = props.target || null;
        checkPropConflicts(props, "noRel", "rel");
        const rel = firstNonUndefined(
          // converts `""` to `null` to prevent the attribute from being added as empty (`rel=""`)
          props.noRel ? "" : props.rel,
          options.externalRelAttribute,
          /*
          * A fallback rel of `noopener noreferrer` is applied for external links or links that open in a new tab.
          * This solves a reverse tabnapping security flaw in browsers pre-2021 as well as improving privacy.
          */
          isAbsoluteUrl.value || hasTarget.value ? "noopener noreferrer" : ""
        ) || null;
        if (props.custom) {
          if (!slots.default) {
            return null;
          }
          return slots.default({
            href: href.value,
            navigate,
            prefetch,
            get route() {
              if (!href.value) {
                return void 0;
              }
              const url = new URL(href.value, import.meta.client ? window.location.href : "http://localhost");
              return {
                path: url.pathname,
                fullPath: url.pathname,
                get query() {
                  return parseQuery(url.search);
                },
                hash: url.hash,
                params: {},
                name: void 0,
                matched: [],
                redirectedFrom: void 0,
                meta: {},
                href: href.value
              };
            },
            rel,
            target,
            isExternal: isExternal.value || hasTarget.value,
            isActive: false,
            isExactActive: false
          });
        }
        return h("a", {
          ref: el,
          href: href.value || null,
          // converts `""` to `null` to prevent the attribute from being added as empty (`href=""`)
          rel,
          target,
          onClick: async (event) => {
            if (isExternal.value || hasTarget.value) {
              return;
            }
            event.preventDefault();
            try {
              const encodedHref = encodeRoutePath(href.value);
              return await (props.replace ? router.replace(encodedHref) : router.push(encodedHref));
            } finally {
              if (import.meta.client && isHashLinkWithoutHashMode(to.value)) {
                const rawHash = to.value.slice(1);
                let hash = rawHash;
                try {
                  hash = decodeURIComponent(rawHash);
                } catch {
                }
                const el2 = document.getElementById(hash);
                el2?.focus();
              }
            }
          }
        }, slots.default?.());
      };
    }
  });
}
export default /* @__PURE__ */ defineNuxtLink(nuxtLinkDefaults);
function applyTrailingSlashBehavior(to, trailingSlash) {
  const normalizeFn = trailingSlash === "append" ? withTrailingSlash : withoutTrailingSlash;
  const hasProtocolDifferentFromHttp = hasProtocol(to) && !to.startsWith("http");
  if (hasProtocolDifferentFromHttp) {
    return to;
  }
  return normalizeFn(to, true);
}
function useObserver() {
  if (import.meta.server) {
    return;
  }
  const nuxtApp = useNuxtApp();
  if (nuxtApp._observer) {
    return nuxtApp._observer;
  }
  let observer = null;
  const callbacks = /* @__PURE__ */ new Map();
  const observe = (element, callback) => {
    observer ||= new IntersectionObserver((entries) => {
      for (const entry of entries) {
        const callback2 = callbacks.get(entry.target);
        const isVisible = entry.isIntersecting || entry.intersectionRatio > 0;
        if (isVisible && callback2) {
          callback2();
        }
      }
    });
    callbacks.set(element, callback);
    observer.observe(element);
    return () => {
      callbacks.delete(element);
      observer?.unobserve(element);
      if (callbacks.size === 0) {
        observer?.disconnect();
        observer = null;
      }
    };
  };
  const _observer = nuxtApp._observer = {
    observe
  };
  return _observer;
}
const IS_2G_RE = /2g/;
function isSlowConnection() {
  if (import.meta.server) {
    return;
  }
  const cn = navigator.connection;
  if (cn && (cn.saveData || IS_2G_RE.test(cn.effectiveType))) {
    return true;
  }
  return false;
}

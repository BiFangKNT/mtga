import { isChangingPage } from "../components/utils.js";
import { useRouter } from "../composables/router.js";
import { defineNuxtPlugin } from "../nuxt.js";
import { appViewTransition as defaultViewTransition } from "#build/nuxt.config.mjs";
export default defineNuxtPlugin((nuxtApp) => {
  if (!document.startViewTransition) {
    return;
  }
  let transition;
  let hasUAVisualTransition = false;
  let finishTransition;
  let abortTransition;
  const resetTransitionState = () => {
    transition = void 0;
    hasUAVisualTransition = false;
    abortTransition = void 0;
    finishTransition = void 0;
  };
  window.addEventListener("popstate", (event) => {
    hasUAVisualTransition = event.hasUAVisualTransition;
    if (hasUAVisualTransition) {
      transition?.skipTransition();
    }
  });
  const router = useRouter();
  const normalizeViewTransitionOptions = (value) => {
    if (typeof value === "boolean" || value === "always") {
      return { enabled: value };
    }
    if (value && typeof value === "object") {
      return value;
    }
    return {};
  };
  router.beforeResolve(async (to, from) => {
    if (to.matched.length === 0) {
      return;
    }
    const toViewTransitionOptions = normalizeViewTransitionOptions(to.meta.viewTransition);
    const fromViewTransitionOptions = normalizeViewTransitionOptions(from.meta.viewTransition);
    const viewTransitionMode = toViewTransitionOptions.enabled ?? defaultViewTransition.enabled;
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const prefersNoTransition = prefersReducedMotion && viewTransitionMode !== "always";
    if (viewTransitionMode === false || prefersNoTransition || hasUAVisualTransition || !isChangingPage(to, from)) {
      return;
    }
    const resolveViewTransitionTypes = (types) => {
      return types ? typeof types === "function" ? types(to, from) : types : void 0;
    };
    const viewTransitionBaseTypes = resolveViewTransitionTypes(toViewTransitionOptions.types) ?? resolveViewTransitionTypes(defaultViewTransition.types) ?? [];
    const viewTransitionFromTypes = resolveViewTransitionTypes(fromViewTransitionOptions.fromTypes) ?? [];
    const viewTransitionToTypes = resolveViewTransitionTypes(toViewTransitionOptions.toTypes) ?? [];
    const allTypes = [
      ...viewTransitionBaseTypes,
      ...viewTransitionFromTypes,
      ...viewTransitionToTypes
    ];
    const promise = new Promise((resolve, reject) => {
      finishTransition = resolve;
      abortTransition = reject;
    });
    let changeRoute;
    const ready = new Promise((resolve) => changeRoute = resolve);
    const update = () => {
      changeRoute();
      return promise;
    };
    transition = allTypes.length > 0 ? document.startViewTransition({ update, types: allTypes }) : document.startViewTransition(update);
    transition.finished.catch(() => {
    }).finally(resetTransitionState);
    await nuxtApp.callHook("page:view-transition:start", transition);
    return ready;
  });
  router.onError(() => {
    abortTransition?.();
    resetTransitionState();
  });
  nuxtApp.hook("app:error", () => {
    abortTransition?.();
    resetTransitionState();
  });
  nuxtApp.hook("vue:error", () => {
    abortTransition?.();
    resetTransitionState();
  });
  nuxtApp.hook("page:finish", () => {
    finishTransition?.();
    resetTransitionState();
  });
});

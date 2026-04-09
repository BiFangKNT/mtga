import { getCurrentInstance, h, onMounted, provide, shallowRef } from "vue";
import { isPromise } from "@vue/shared";
import { useNuxtApp } from "#app/nuxt";
import ServerPlaceholder from "#app/components/server-placeholder";
import { clientOnlySymbol } from "#app/components/client-only";
// @__NO_SIDE_EFFECTS__
export async function createClientPage(loader) {
  const m = await loader();
  const c = m.default || m;
  if (import.meta.dev) {
    c.__clientOnlyPage = true;
  }
  return pageToClientOnly(c);
}
const cache = /* @__PURE__ */ new WeakMap();
function pageToClientOnly(component) {
  if (import.meta.server) {
    return ServerPlaceholder;
  }
  if (cache.has(component)) {
    return cache.get(component);
  }
  const clone = { ...component };
  if (clone.render) {
    clone.render = (ctx, cache2, $props, $setup, $data, $options) => $setup.mounted$ ?? ctx.mounted$ ? h(component.render?.bind(ctx)(ctx, cache2, $props, $setup, $data, $options)) : h("div");
  } else {
    clone.template &&= `
      <template v-if="mounted$">${component.template}</template>
      <template v-else><div></div></template>
    `;
  }
  clone.setup = (props, ctx) => {
    const nuxtApp = useNuxtApp();
    const mounted$ = shallowRef(nuxtApp.isHydrating === false);
    provide(clientOnlySymbol, true);
    const vm = getCurrentInstance();
    if (vm) {
      vm._nuxtClientOnly = true;
    }
    onMounted(() => {
      mounted$.value = true;
    });
    const setupState = component.setup?.(props, ctx) || {};
    if (isPromise(setupState)) {
      return Promise.resolve(setupState).then((setupState2) => {
        if (typeof setupState2 !== "function") {
          setupState2 ||= {};
          setupState2.mounted$ = mounted$;
          return setupState2;
        }
        return (...args) => mounted$.value || !nuxtApp.isHydrating ? h(setupState2(...args)) : h("div");
      });
    } else {
      return typeof setupState === "function" ? (...args) => mounted$.value || !nuxtApp.isHydrating ? h(setupState(...args)) : h("div") : Object.assign(setupState, { mounted$ });
    }
  };
  cache.set(component, clone);
  return clone;
}

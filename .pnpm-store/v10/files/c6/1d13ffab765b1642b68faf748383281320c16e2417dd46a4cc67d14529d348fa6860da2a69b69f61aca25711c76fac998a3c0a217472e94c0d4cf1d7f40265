import { computed, getCurrentInstance } from "vue";
import { hash } from "ohash";
import { getNuxtAppCtx, useNuxtApp } from "../nuxt.js";
import { useHead } from "./head.js";
import { useAsyncData } from "./asyncData.js";
import { useRoute } from "./router.js";
import { createError } from "./error.js";
export const NuxtComponentIndicator = "__nuxt_component";
// @__NO_SIDE_EFFECTS__
function getFetchKey() {
  const vm = getCurrentInstance();
  const route = useRoute();
  const { _fetchKeyBase } = vm.proxy.$options;
  return hash([
    _fetchKeyBase,
    route.path,
    route.query,
    route.matched.findIndex((r) => Object.values(r.components || {}).includes(vm.type))
  ]);
}
async function runLegacyAsyncData(res, fn) {
  const nuxtApp = useNuxtApp();
  const { fetchKey } = getCurrentInstance().proxy.$options;
  const key = (typeof fetchKey === "function" ? fetchKey(() => "") : fetchKey) || /* @__PURE__ */ getFetchKey();
  const { data, error } = await useAsyncData(`options:asyncdata:${key}`, () => import.meta.server ? nuxtApp.runWithContext(() => fn(nuxtApp)) : fn(nuxtApp));
  if (error.value) {
    throw createError(error.value);
  }
  if (data.value && typeof data.value === "object") {
    const _res = await res;
    for (const key2 in data.value) {
      _res[key2] = computed({
        get: () => data.value?.[key2],
        set(v) {
          data.value = data.value ? { ...data.value, [key2]: v } : { [key2]: v };
        }
      });
    }
  } else if (import.meta.dev) {
    console.warn("[nuxt] asyncData should return an object", data);
  }
}
export const defineNuxtComponent = /* @__NO_SIDE_EFFECTS__ */ function defineNuxtComponent2(...args) {
  const [options, key] = args;
  const { setup } = options;
  if (!setup && !options.asyncData && !options.head) {
    return {
      [NuxtComponentIndicator]: true,
      ...options
    };
  }
  return {
    [NuxtComponentIndicator]: true,
    _fetchKeyBase: key,
    ...options,
    setup(props, ctx) {
      const nuxtApp = useNuxtApp();
      let res = {};
      if (setup) {
        const fn = () => Promise.resolve(setup(props, ctx)).then((r) => r || {});
        const nuxtAppCtx = getNuxtAppCtx(nuxtApp._id);
        if (import.meta.server) {
          res = nuxtAppCtx.callAsync(nuxtApp, fn);
        } else {
          nuxtAppCtx.set(nuxtApp);
          res = fn();
        }
      }
      const promises = [];
      if (options.asyncData) {
        promises.push(runLegacyAsyncData(res, options.asyncData));
      }
      if (options.head) {
        useHead(typeof options.head === "function" ? () => options.head(nuxtApp) : options.head);
      }
      return Promise.resolve(res).then(() => Promise.all(promises)).then(() => res).finally(() => {
        promises.length = 0;
      });
    }
  };
};

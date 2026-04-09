import { SafeInputPlugin, FlatMetaPlugin } from 'unhead/plugins';
import { walkResolver } from 'unhead/utils';
import { hasInjectionContext, inject, ref, watchEffect, getCurrentInstance, onBeforeUnmount, onDeactivated, onActivated } from 'vue';
import { V as VueResolver } from './vue.N9zWjxoK.mjs';

const headSymbol = "usehead";
// @__NO_SIDE_EFFECTS__
function vueInstall(head) {
  const plugin = {
    install(app) {
      app.config.globalProperties.$unhead = head;
      app.config.globalProperties.$head = head;
      app.provide(headSymbol, head);
    }
  };
  return plugin.install;
}

// @__NO_SIDE_EFFECTS__
function injectHead() {
  if (hasInjectionContext()) {
    const instance = inject(headSymbol);
    if (instance) {
      return instance;
    }
  }
  throw new Error("useHead() was called without provide context, ensure you call it through the setup() function.");
}
function useHead(input, options = {}) {
  const head = options.head || /* @__PURE__ */ injectHead();
  return head.ssr ? head.push(input || {}, options) : clientUseHead(head, input, options);
}
function clientUseHead(head, input, options = {}) {
  const deactivated = ref(false);
  let entry;
  watchEffect(() => {
    const i = deactivated.value ? {} : walkResolver(input, VueResolver);
    if (entry) {
      entry.patch(i);
    } else {
      entry = head.push(i, options);
    }
  });
  const vm = getCurrentInstance();
  if (vm) {
    onBeforeUnmount(() => {
      entry.dispose();
    });
    onDeactivated(() => {
      deactivated.value = true;
    });
    onActivated(() => {
      deactivated.value = false;
    });
  }
  return entry;
}
function useHeadSafe(input = {}, options = {}) {
  const head = options.head || /* @__PURE__ */ injectHead();
  head.use(SafeInputPlugin);
  options._safe = true;
  return useHead(input, options);
}
function useSeoMeta(input = {}, options = {}) {
  const head = options.head || /* @__PURE__ */ injectHead();
  head.use(FlatMetaPlugin);
  const { title, titleTemplate, ...meta } = input;
  return useHead({
    title,
    titleTemplate,
    _flatMeta: meta
  }, options);
}
function useServerHead(input, options = {}) {
  return useHead(input, { ...options, mode: "server" });
}
function useServerHeadSafe(input, options = {}) {
  return useHeadSafe(input, { ...options, mode: "server" });
}
function useServerSeoMeta(input, options = {}) {
  return useSeoMeta(input, { ...options, mode: "server" });
}

export { useHeadSafe as a, useSeoMeta as b, useServerHead as c, useServerHeadSafe as d, useServerSeoMeta as e, headSymbol as h, injectHead as i, useHead as u, vueInstall as v };

import { createUnhead } from 'unhead';
import { inject, ref, watchEffect, unref, watch, getCurrentInstance, onBeforeUnmount, onDeactivated, onActivated } from 'vue';
import { createHead as createHead$1 } from './client.mjs';
import { h as headSymbol } from './shared/vue.Cr7xSEtD.mjs';
import { V as VueResolver } from './shared/vue.N9zWjxoK.mjs';
import { createHead as createHead$2 } from './server.mjs';
import { walkResolver } from 'unhead/utils';
import { defineHeadPlugin, DeprecationsPlugin, PromisesPlugin, TemplateParamsPlugin, AliasSortingPlugin, SafeInputPlugin, FlatMetaPlugin } from 'unhead/plugins';
import 'unhead/client';
import './shared/vue.BM998iwd.mjs';
import 'unhead/server';

const createHeadCore = createUnhead;
function resolveUnrefHeadInput(input) {
  return walkResolver(input, VueResolver);
}
function CapoPlugin() {
  return defineHeadPlugin({
    key: "capo"
  });
}
function createHead(options = {}) {
  return createHead$1({
    disableCapoSorting: true,
    ...options,
    plugins: [
      DeprecationsPlugin,
      PromisesPlugin,
      TemplateParamsPlugin,
      AliasSortingPlugin,
      ...options.plugins || []
    ]
  });
}
function createServerHead(options = {}) {
  return createHead$2({
    disableCapoSorting: true,
    ...options,
    plugins: [
      DeprecationsPlugin,
      PromisesPlugin,
      TemplateParamsPlugin,
      AliasSortingPlugin,
      ...options.plugins || []
    ]
  });
}
function setHeadInjectionHandler(handler) {
}
function injectHead() {
  return inject(headSymbol);
}
function useHead(input, options = {}) {
  const head = options.head || injectHead();
  if (head) {
    return head.ssr ? head.push(input, options) : clientUseHead(head, input, options);
  }
}
function clientUseHead(head, input, options = {}) {
  const deactivated = ref(false);
  const resolvedInput = ref({});
  watchEffect(() => {
    resolvedInput.value = deactivated.value ? {} : walkResolver(input, (v) => unref(v));
  });
  const entry = head.push(resolvedInput.value, options);
  watch(resolvedInput, (e) => {
    entry.patch(e);
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
function useHeadSafe(input, options = {}) {
  const head = options.head || injectHead();
  if (head) {
    head.use(SafeInputPlugin);
    options._safe = true;
    return useHead(input, options);
  }
}
function useSeoMeta(input, options) {
  const head = options?.head || injectHead();
  if (head) {
    head.use(FlatMetaPlugin);
    const { title, titleTemplate, ...meta } = input;
    return useHead({
      title,
      titleTemplate,
      // @ts-expect-error runtime type
      _flatMeta: meta
    }, options);
  }
}
function useServerHead(input, options = {}) {
  return useHead(input, { ...options, mode: "server" });
}
function useServerHeadSafe(input, options = {}) {
  return useHeadSafe(input, { ...options, mode: "server" });
}
function useServerSeoMeta(input, options) {
  return useSeoMeta(input, { ...options, mode: "server" });
}

export { CapoPlugin, createHead, createHeadCore, createServerHead, injectHead, resolveUnrefHeadInput, setHeadInjectionHandler, useHead, useHeadSafe, useSeoMeta, useServerHead, useServerHeadSafe, useServerSeoMeta };

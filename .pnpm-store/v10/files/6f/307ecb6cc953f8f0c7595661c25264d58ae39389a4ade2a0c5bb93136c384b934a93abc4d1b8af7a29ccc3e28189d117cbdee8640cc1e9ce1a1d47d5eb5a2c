import { hasInjectionContext, inject } from "vue";
import {
  useHead as headCore,
  useHeadSafe as headSafe,
  headSymbol,
  useSeoMeta as seoMeta,
  useServerHead as serverHead,
  useServerHeadSafe as serverHeadSafe,
  useServerSeoMeta as serverSeoMeta
} from "@unhead/vue";
import { useNuxtApp } from "#app/nuxt";
export function injectHead(nuxtApp) {
  const nuxt = nuxtApp || useNuxtApp();
  return nuxt.ssrContext?.head || nuxt.runWithContext(() => {
    if (hasInjectionContext()) {
      const head = inject(headSymbol);
      if (!head) {
        throw new Error("[nuxt] [unhead] Missing Unhead instance.");
      }
      return head;
    }
  });
}
export function useHead(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return headCore(input, { head, ...options });
}
export function useHeadSafe(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return headSafe(input, { head, ...options });
}
export function useSeoMeta(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return seoMeta(input, { head, ...options });
}
export function useServerHead(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return serverHead(input, { head, ...options });
}
export function useServerHeadSafe(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return serverHeadSafe(input, { head, ...options });
}
export function useServerSeoMeta(input, options = {}) {
  const head = options.head || injectHead(options.nuxt);
  return serverSeoMeta(input, { head, ...options });
}

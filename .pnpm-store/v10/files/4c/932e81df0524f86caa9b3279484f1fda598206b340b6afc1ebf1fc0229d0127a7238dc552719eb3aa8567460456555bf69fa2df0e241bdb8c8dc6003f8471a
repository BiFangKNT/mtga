import { onScopeDispose } from "vue";
import { useNuxtApp } from "../nuxt.js";
export function useRuntimeHook(name, fn) {
  const nuxtApp = useNuxtApp();
  const unregister = nuxtApp.hook(name, fn);
  onScopeDispose(unregister);
}

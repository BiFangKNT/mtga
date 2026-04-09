import { defineNuxtPlugin } from "../nuxt.js";
export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.config.warnHandler ??= (msg, _instance, trace) => {
    console.warn(`[Vue warn]: ${msg}`, trace);
  };
});

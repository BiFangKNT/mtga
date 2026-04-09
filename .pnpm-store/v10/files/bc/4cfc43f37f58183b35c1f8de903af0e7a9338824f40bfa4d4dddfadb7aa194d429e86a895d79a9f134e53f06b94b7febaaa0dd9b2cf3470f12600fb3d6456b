import { createApp, createSSRApp, nextTick } from "vue";
import "#build/fetch.mjs";
import "#build/global-polyfills.mjs";
import { applyPlugins, createNuxtApp } from "./nuxt.js";
import { createError } from "./composables/error.js";
import "#build/css";
import plugins from "#build/plugins";
import RootComponent from "#build/root-component.mjs";
import { appId, appSpaLoaderAttrs, multiApp, spaLoadingTemplateOutside, vueAppRootContainer } from "#build/nuxt.config.mjs";
let entry;
if (import.meta.server) {
  entry = async function createNuxtAppServer(ssrContext) {
    const vueApp = createApp(RootComponent);
    const nuxt = createNuxtApp({ vueApp, ssrContext });
    try {
      await applyPlugins(nuxt, plugins);
      await nuxt.hooks.callHook("app:created", vueApp);
    } catch (error) {
      await nuxt.hooks.callHook("app:error", error);
      nuxt.payload.error ||= createError(error);
    }
    if (ssrContext && (ssrContext["~renderResponse"] || ssrContext._renderResponse)) {
      throw new Error("skipping render");
    }
    return vueApp;
  };
}
if (import.meta.client) {
  if (import.meta.dev && import.meta.webpackHot) {
    import.meta.webpackHot.accept();
  }
  let vueAppPromise;
  entry = async function initApp() {
    if (vueAppPromise) {
      return vueAppPromise;
    }
    const isSSR = Boolean(
      (multiApp ? window.__NUXT__?.[appId] : window.__NUXT__)?.serverRendered ?? (multiApp ? document.querySelector(`[data-nuxt-data="${appId}"]`) : document.getElementById("__NUXT_DATA__"))?.dataset.ssr === "true"
    );
    const vueApp = isSSR ? createSSRApp(RootComponent) : createApp(RootComponent);
    const nuxt = createNuxtApp({ vueApp });
    async function handleVueError(error) {
      await nuxt.callHook("app:error", error);
      nuxt.payload.error ||= createError(error);
    }
    vueApp.config.errorHandler = handleVueError;
    nuxt.hook("app:suspense:resolve", () => {
      if (vueApp.config.errorHandler === handleVueError) {
        vueApp.config.errorHandler = void 0;
      }
    });
    if (spaLoadingTemplateOutside && !isSSR && appSpaLoaderAttrs.id) {
      nuxt.hook("app:suspense:resolve", () => {
        document.getElementById(appSpaLoaderAttrs.id)?.remove();
      });
    }
    try {
      await applyPlugins(nuxt, plugins);
    } catch (err) {
      handleVueError(err);
    }
    try {
      await nuxt.hooks.callHook("app:created", vueApp);
      await nuxt.hooks.callHook("app:beforeMount", vueApp);
      vueApp.mount(vueAppRootContainer);
      await nuxt.hooks.callHook("app:mounted", vueApp);
      await nextTick();
    } catch (err) {
      handleVueError(err);
    }
    return vueApp;
  };
  vueAppPromise = entry().catch((error) => {
    console.error("Error while mounting app:", error);
    throw error;
  });
}
export default ((ssrContext) => entry(ssrContext));

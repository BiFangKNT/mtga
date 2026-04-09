import { createHead as createClientHead, renderDOMHead } from "@unhead/vue/client";
import { defineNuxtPlugin } from "#app/nuxt";
import unheadOptions from "#build/unhead-options.mjs";
export default defineNuxtPlugin({
  name: "nuxt:head",
  enforce: "pre",
  setup(nuxtApp) {
    const head = import.meta.server ? nuxtApp.ssrContext.head : createClientHead(unheadOptions);
    nuxtApp.vueApp.use(head);
    if (import.meta.client) {
      let pauseDOMUpdates = true;
      const syncHead = async () => {
        pauseDOMUpdates = false;
        await renderDOMHead(head);
      };
      head.hooks.hook("dom:beforeRender", (context) => {
        context.shouldRender = !pauseDOMUpdates;
      });
      nuxtApp.hooks.hook("page:start", () => {
        pauseDOMUpdates = true;
      });
      nuxtApp.hooks.hook("page:finish", () => {
        if (!nuxtApp.isHydrating) {
          syncHead();
        }
      });
      nuxtApp.hooks.hook("app:error", syncHead);
      nuxtApp.hooks.hook("app:suspense:resolve", syncHead);
    }
  }
});

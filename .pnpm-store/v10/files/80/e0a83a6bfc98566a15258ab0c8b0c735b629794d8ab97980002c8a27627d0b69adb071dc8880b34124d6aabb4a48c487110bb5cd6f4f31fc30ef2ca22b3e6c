import { defineNuxtPlugin } from "../nuxt.js";
export default defineNuxtPlugin({
  name: "nuxt:browser-devtools-timing",
  enforce: "pre",
  setup(nuxtApp) {
    nuxtApp.hooks.beforeEach((event) => {
      event.__startTime = performance.now();
    });
    nuxtApp.hooks.afterEach((event) => {
      performance.measure(event.name, {
        // @ts-expect-error __startTime is not a public API
        start: event.__startTime,
        detail: {
          devtools: {
            dataType: "track-entry",
            track: "nuxt",
            color: "tertiary-dark"
          }
        }
      });
    });
  }
});

import { defineNuxtPlugin, useState } from "#imports";
export default defineNuxtPlugin(() => {
  const state = useState("__nuxt_devtools__", () => ({}));
  state.value = {
    timeSsrStart: Date.now()
  };
});

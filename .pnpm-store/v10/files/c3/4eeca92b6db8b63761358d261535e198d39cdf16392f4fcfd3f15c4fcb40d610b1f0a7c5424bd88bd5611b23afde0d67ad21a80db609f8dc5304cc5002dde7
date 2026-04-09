import { reactive, ref, shallowReactive, shallowRef } from "vue";
import { definePayloadReviver, getNuxtClientPayload } from "../composables/payload.js";
import { createError } from "../composables/error.js";
import { defineNuxtPlugin, useNuxtApp } from "../nuxt.js";
import { componentIslands } from "#build/nuxt.config.mjs";
function parseRevivedData(data) {
  try {
    return JSON.parse(data);
  } catch {
    return data;
  }
}
const revivers = [
  ["NuxtError", (data) => createError(data)],
  ["EmptyShallowRef", (data) => shallowRef(data === "_" ? void 0 : data === "0n" ? BigInt(0) : parseRevivedData(data))],
  ["EmptyRef", (data) => ref(data === "_" ? void 0 : data === "0n" ? BigInt(0) : parseRevivedData(data))],
  ["ShallowRef", (data) => shallowRef(data)],
  ["ShallowReactive", (data) => shallowReactive(data)],
  ["Ref", (data) => ref(data)],
  ["Reactive", (data) => reactive(data)]
];
if (componentIslands) {
  revivers.push(["Island", ({ key, params, result }) => {
    const nuxtApp = useNuxtApp();
    if (!nuxtApp.isHydrating) {
      nuxtApp.payload.data[key] ||= $fetch(`/__nuxt_island/${key}.json`, {
        responseType: "json",
        ...params ? { params } : {}
      }).then((r) => {
        nuxtApp.payload.data[key] = r;
        return r;
      });
    }
    return {
      html: "",
      ...result
    };
  }]);
}
export default defineNuxtPlugin({
  name: "nuxt:revive-payload:client",
  order: -30,
  async setup(nuxtApp) {
    for (const [reviver, fn] of revivers) {
      definePayloadReviver(reviver, fn);
    }
    Object.assign(nuxtApp.payload, await nuxtApp.runWithContext(getNuxtClientPayload));
    delete window.__NUXT__;
  }
});

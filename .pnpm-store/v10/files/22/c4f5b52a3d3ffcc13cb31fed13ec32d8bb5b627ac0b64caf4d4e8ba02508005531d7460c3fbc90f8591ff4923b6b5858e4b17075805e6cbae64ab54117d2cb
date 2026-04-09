import { isRef, toRef } from "vue";
import { useNuxtApp } from "../nuxt.js";
import { toArray } from "../utils.js";
import { useStateDefaults } from "#build/nuxt.config.mjs";
const useStateKeyPrefix = "$s";
export function useState(...args) {
  const autoKey = typeof args[args.length - 1] === "string" ? args.pop() : void 0;
  if (typeof args[0] !== "string") {
    args.unshift(autoKey);
  }
  const [_key, init] = args;
  if (!_key || typeof _key !== "string") {
    throw new TypeError("[nuxt] [useState] key must be a string: " + _key);
  }
  if (init !== void 0 && typeof init !== "function") {
    throw new Error("[nuxt] [useState] init must be a function: " + init);
  }
  const key = useStateKeyPrefix + _key;
  const nuxtApp = useNuxtApp();
  const state = toRef(nuxtApp.payload.state, key);
  if (init) {
    nuxtApp._state[key] ??= { _default: init };
  }
  if (state.value === void 0 && init) {
    const initialValue = init();
    if (isRef(initialValue)) {
      nuxtApp.payload.state[key] = initialValue;
      return initialValue;
    }
    state.value = initialValue;
  }
  return state;
}
export function clearNuxtState(keys, opts) {
  const reset = opts?.reset ?? useStateDefaults.resetOnClear;
  const nuxtApp = useNuxtApp();
  const _allKeys = Object.keys(nuxtApp.payload.state).map((key) => key.substring(useStateKeyPrefix.length));
  const _keys = !keys ? _allKeys : typeof keys === "function" ? _allKeys.filter(keys) : toArray(keys);
  for (const _key of _keys) {
    const key = useStateKeyPrefix + _key;
    if (key in nuxtApp.payload.state) {
      if (reset && nuxtApp._state[key]) {
        nuxtApp.payload.state[key] = nuxtApp._state[key]._default();
      } else {
        nuxtApp.payload.state[key] = void 0;
      }
    }
  }
}

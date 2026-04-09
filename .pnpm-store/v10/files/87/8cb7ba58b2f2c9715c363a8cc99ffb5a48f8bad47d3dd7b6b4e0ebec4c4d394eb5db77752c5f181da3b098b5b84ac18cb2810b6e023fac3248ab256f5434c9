import { useRouter } from "./router.js";
import { useNuxtApp } from "../nuxt.js";
let _isHmrUpdating = false;
export async function callOnce(...args) {
  const autoKey = typeof args[args.length - 1] === "string" ? args.pop() : void 0;
  if (typeof args[0] !== "string") {
    args.unshift(autoKey);
  }
  const [_key, fn, options] = args;
  if (!_key || typeof _key !== "string") {
    throw new TypeError("[nuxt] [callOnce] key must be a string: " + _key);
  }
  if (fn !== void 0 && typeof fn !== "function") {
    throw new Error("[nuxt] [callOnce] fn must be a function: " + fn);
  }
  const nuxtApp = useNuxtApp();
  if (options?.mode === "navigation") {
    let callback = function() {
      nuxtApp.payload.once.delete(_key);
      for (const cleanup of cleanups) {
        cleanup();
      }
    };
    const cleanups = [];
    cleanups.push(nuxtApp.hooks.hook("page:start", callback), useRouter().beforeResolve(callback));
  }
  if (nuxtApp.payload.once.has(_key)) {
    if (!import.meta.dev || !_isHmrUpdating) {
      return;
    }
  }
  nuxtApp._once ||= {};
  nuxtApp._once[_key] ||= fn() || true;
  await nuxtApp._once[_key];
  nuxtApp.payload.once.add(_key);
  delete nuxtApp._once[_key];
}
if (import.meta.hot) {
  import.meta.hot.on("vite:beforeUpdate", (payload) => {
    if (payload.updates.some((u) => u.type === "js-update")) {
      _isHmrUpdating = true;
    }
  });
  import.meta.hot.on("vite:afterUpdate", (payload) => {
    if (payload.updates.some((u) => u.type === "js-update")) {
      _isHmrUpdating = false;
    }
  });
}

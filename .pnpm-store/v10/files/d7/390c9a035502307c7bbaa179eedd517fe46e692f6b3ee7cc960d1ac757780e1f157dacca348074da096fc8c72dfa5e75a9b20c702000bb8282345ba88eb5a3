import { toRef, watch } from "vue";
import { useState } from "./state.js";
import { refreshNuxtData } from "./asyncData.js";
import { useRoute, useRouter } from "./router.js";
let unregisterRefreshHook;
export function usePreviewMode(options = {}) {
  const preview = useState("_preview-state", () => ({
    enabled: false,
    state: {}
  }));
  if (preview.value._initialized) {
    return {
      enabled: toRef(preview.value, "enabled"),
      state: preview.value.state
    };
  }
  if (import.meta.client) {
    preview.value._initialized = true;
  }
  if (!preview.value.enabled) {
    const shouldEnable = options.shouldEnable ?? defaultShouldEnable;
    const result = shouldEnable(preview.value.state);
    if (typeof result === "boolean") {
      preview.value.enabled = result;
    }
  }
  watch(() => preview.value.enabled, (value) => {
    if (value) {
      const getState = options.getState ?? getDefaultState;
      const newState = getState(preview.value.state);
      if (newState !== preview.value.state) {
        Object.assign(preview.value.state, newState);
      }
      if (import.meta.client && !unregisterRefreshHook) {
        const onEnable = options.onEnable ?? refreshNuxtData;
        onEnable();
        unregisterRefreshHook = options.onDisable ?? useRouter().afterEach(() => refreshNuxtData());
      }
    } else if (unregisterRefreshHook) {
      unregisterRefreshHook();
      unregisterRefreshHook = void 0;
    }
  }, { immediate: true, flush: "sync" });
  return {
    enabled: toRef(preview.value, "enabled"),
    state: preview.value.state
  };
}
function defaultShouldEnable() {
  const route = useRoute();
  const previewQueryName = "preview";
  return route.query[previewQueryName] === "true";
}
function getDefaultState(state) {
  if (state.token !== void 0) {
    return state;
  }
  const route = useRoute();
  state.token = Array.isArray(route.query.token) ? route.query.token[0] : route.query.token;
  return state;
}

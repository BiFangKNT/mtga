<template>
  <slot
    v-if="error"
    v-bind="{ error, clearError }"
    name="error"
  />

  <slot
    v-else
    name="default"
  />
</template>

<script setup>
import { onErrorCaptured, shallowRef } from "vue";
import { useNuxtApp } from "../nuxt";
import { onNuxtReady } from "../composables/ready";
defineOptions({
  name: "NuxtErrorBoundary",
  inheritAttrs: false
});
const emit = defineEmits(["error"]);
defineSlots();
const error = shallowRef(null);
function clearError() {
  error.value = null;
}
if (import.meta.client) {
  let handleError = function(...args) {
    const [err, instance, info] = args;
    emit("error", err);
    nuxtApp.hooks.callHook("vue:error", err, instance, info);
    error.value = err;
  };
  const nuxtApp = useNuxtApp();
  onErrorCaptured((err, instance, info) => {
    if (!nuxtApp.isHydrating) {
      handleError(err, instance, info);
    } else {
      onNuxtReady(() => handleError(err, instance, info));
    }
    return false;
  });
}
defineExpose({ error, clearError });
</script>

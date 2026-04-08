<script setup lang="ts">
defineOptions({
  inheritAttrs: false,
});

const props = withDefaults(
  defineProps<{
    loading?: boolean;
    disabled?: boolean;
    type?: "button" | "submit" | "reset";
  }>(),
  {
    loading: false,
    disabled: false,
    type: "button",
  },
);

const attrs = useAttrs();

const isDisabled = computed(() => props.disabled || props.loading);
</script>

<template>
  <button v-bind="attrs" :type="props.type" :disabled="isDisabled" :aria-busy="props.loading">
    <span v-if="props.loading" class="loading loading-spinner loading-sm" aria-hidden="true" />
    <slot />
  </button>
</template>

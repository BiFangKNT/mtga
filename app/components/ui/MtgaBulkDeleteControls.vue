<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: "button" | "selection";
    active?: boolean;
    totalCount?: number;
    selectedCount?: number;
    allSelected?: boolean;
    busy?: boolean;
    size?: "xs" | "sm";
    itemLabel?: string;
    deleteText?: string;
    exitText?: string;
    batchDeleteText?: string;
    buttonWidthClass?: string;
  }>(),
  {
    variant: "button",
    active: false,
    totalCount: 0,
    selectedCount: 0,
    allSelected: false,
    busy: false,
    size: "sm",
    itemLabel: "条记录",
    deleteText: "删除",
    exitText: "退出删除",
    batchDeleteText: "批量删除",
    buttonWidthClass: "",
  },
);

const emit = defineEmits<{
  (event: "update:active", value: boolean): void;
  (event: "select-all-change", value: boolean): void;
  (event: "delete-selected"): void;
}>();

const hasItems = computed(() => props.totalCount > 0);
const hasSelection = computed(() => props.selectedCount > 0);
const toggleDisabled = computed(() => props.busy || (!props.active && !hasItems.value));
const buttonClass = computed(() => [
  "btn btn-outline border-rose-200 text-rose-600 hover:border-rose-300 hover:bg-rose-50",
  props.size === "xs" ? "btn-xs rounded-lg" : "btn-sm rounded-xl",
  props.buttonWidthClass,
]);
const selectedLabel = computed(() => `已选择 ${props.selectedCount} ${props.itemLabel}`);

const toggleDeleteMode = () => {
  if (toggleDisabled.value) {
    return;
  }
  emit("update:active", !props.active);
};

const handleSelectAllChange = (event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  emit("select-all-change", target.checked);
};
</script>

<template>
  <button
    v-if="props.variant === 'button'"
    type="button"
    :class="buttonClass"
    :disabled="toggleDisabled"
    @click="toggleDeleteMode"
  >
    {{ props.active ? props.exitText : props.deleteText }}
  </button>

  <div
    v-else-if="props.active && props.totalCount > 0"
    class="sticky top-0 z-10 flex items-center gap-3 rounded-xl border border-slate-200/60 bg-slate-50/80 px-4 py-2"
  >
    <div class="flex items-center">
      <input
        type="checkbox"
        class="checkbox checkbox-xs rounded border-slate-300 [--chkbg:var(--color-amber-500)] [--chkfg:white]"
        :checked="props.allSelected"
        :disabled="props.busy"
        @change="handleSelectAllChange"
      />
    </div>
    <span class="flex-1 text-xs font-medium text-slate-500">{{ selectedLabel }}</span>
    <button
      type="button"
      class="btn btn-ghost btn-xs h-7 min-h-7 rounded-lg px-2 font-medium text-rose-600 hover:bg-rose-50"
      :disabled="props.busy || !hasSelection"
      @click="emit('delete-selected')"
    >
      {{ props.batchDeleteText }}
    </button>
  </div>
</template>

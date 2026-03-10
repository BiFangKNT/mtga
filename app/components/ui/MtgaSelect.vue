<script setup lang="ts">
/**
 * MTGA 标准选择框组件 (升级版)
 * 采用自定义下拉面板实现，以确保在所有平台上拥有统一的圆角、阴影和交互体验
 * 视觉规范严格对齐 MtgaInput
 */

interface Option {
  label: string;
  value: string | number;
}

interface Props {
  modelValue: string | number;
  options: (Option | string)[];
  label?: string;
  description?: string;
  required?: boolean;
  disabled?: boolean;
  /** 尺寸: 'xs' | 'sm' | 'md' | 'lg' */
  size?: "xs" | "sm" | "md" | "lg";
  /** 错误信息 */
  error?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: "md",
  label: "",
  description: "",
  error: "",
});

const emit = defineEmits<{
  (e: "update:modelValue", value: string | number): void;
  (e: "change", value: string | number): void;
}>();

const isOpen = ref(false);
const containerRef = ref<HTMLElement | null>(null);
const triggerRef = ref<HTMLElement | null>(null);
const dropdownPanelRef = ref<HTMLElement | null>(null);
const isPositioned = ref(false);
const dropdownPlacement = ref<"top" | "bottom">("bottom");
const dropdownStyle = ref<Record<string, string>>({});
let globalListenersAttached = false;
let unmounted = false;

// 归一化选项格式
const normalizedOptions = computed(() => {
  return props.options.map((opt) => {
    if (typeof opt === "string") {
      return { label: opt, value: opt };
    }
    return opt;
  });
});

// 获取当前选中项的 Label
const selectedLabel = computed(() => {
  const found = normalizedOptions.value.find((opt) => opt.value === props.modelValue);
  return found ? found.label : "";
});

const toggleDropdown = () => {
  if (props.disabled) return;
  isOpen.value = !isOpen.value;
};

const handleSelect = (val: string | number) => {
  emit("update:modelValue", val);
  emit("change", val);
  isOpen.value = false;
};

// 点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target;
  if (!(target instanceof Node)) {
    return;
  }
  const insideTrigger = containerRef.value?.contains(target) ?? false;
  const insidePanel = dropdownPanelRef.value?.contains(target) ?? false;
  if (!insideTrigger && !insidePanel) {
    isOpen.value = false;
  }
};

const updateDropdownPosition = () => {
  if (!isOpen.value || !triggerRef.value) {
    return;
  }

  const rect = triggerRef.value.getBoundingClientRect();
  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;
  const viewportPadding = 8;
  const gap = 6;
  const maxPanelHeight = 240;

  const availableBottom = viewportHeight - rect.bottom - viewportPadding;
  const availableTop = rect.top - viewportPadding;
  const renderOnTop = availableBottom < maxPanelHeight && availableTop > availableBottom;
  dropdownPlacement.value = renderOnTop ? "top" : "bottom";

  const width = Math.min(rect.width, viewportWidth - viewportPadding * 2);
  const maxLeft = Math.max(viewportPadding, viewportWidth - width - viewportPadding);
  const left = Math.min(Math.max(rect.left, viewportPadding), maxLeft);
  const maxHeight = Math.max(
    120,
    Math.min(maxPanelHeight, renderOnTop ? availableTop - gap : availableBottom - gap),
  );

  dropdownStyle.value = {
    position: "fixed",
    left: `${left}px`,
    width: `${width}px`,
    zIndex: "1000",
    maxHeight: `${maxHeight}px`,
    top: renderOnTop ? "auto" : `${rect.bottom + gap}px`,
    bottom: renderOnTop ? `${viewportHeight - rect.top + gap}px` : "auto",
  };
  isPositioned.value = true;
};

const attachGlobalListeners = () => {
  if (globalListenersAttached) {
    return;
  }
  window.addEventListener("scroll", updateDropdownPosition, true);
  window.addEventListener("resize", updateDropdownPosition);
  globalListenersAttached = true;
};

const detachGlobalListeners = () => {
  if (!globalListenersAttached) {
    return;
  }
  window.removeEventListener("scroll", updateDropdownPosition, true);
  window.removeEventListener("resize", updateDropdownPosition);
  globalListenersAttached = false;
};

watch(
  isOpen,
  async (open) => {
    if (open) {
      isPositioned.value = false;
      await nextTick();
      if (unmounted || !isOpen.value) {
        return;
      }
      updateDropdownPosition();
      attachGlobalListeners();
    } else {
      detachGlobalListeners();
      isPositioned.value = false;
    }
  },
  { flush: "post" },
);

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  unmounted = true;
  document.removeEventListener("click", handleClickOutside);
  detachGlobalListeners();
});

// 尺寸样式映射
const sizeClasses = computed(() => {
  const sizes = {
    xs: {
      trigger: "h-7 px-2 text-xs",
      panel: "mt-1",
      item: "py-1 px-2 text-xs",
      icon: "h-3.5 w-3.5",
    },
    sm: {
      trigger: "h-8 px-3 text-sm",
      panel: "mt-1",
      item: "py-1.5 px-3 text-sm",
      icon: "h-4 w-4",
    },
    md: {
      trigger: "h-10 px-3.5 text-sm",
      panel: "mt-1.5",
      item: "py-2 px-3.5 text-sm",
      icon: "h-4 w-4",
    },
    lg: {
      trigger: "h-12 px-4 text-base",
      panel: "mt-2",
      item: "py-2.5 px-4 text-base",
      icon: "h-5 w-5",
    },
  };
  return sizes[props.size];
});
</script>

<template>
  <div ref="containerRef" class="form-control inline-block relative">
    <!-- 顶部标签区域 -->
    <div v-if="label" class="label py-1">
      <span
        class="label-text font-medium flex items-center gap-0.5"
        :class="[size === 'xs' ? 'text-xs' : 'text-sm', error ? 'text-error' : 'text-slate-600']"
      >
        {{ label }}
        <span v-if="required" class="text-error ml-0.5">*</span>
      </span>
    </div>

    <!-- 选择框 Trigger -->
    <div
      ref="triggerRef"
      class="relative flex items-center group transition-all duration-200 ease-out border rounded-xl shadow-sm cursor-pointer select-none"
      :class="[
        sizeClasses.trigger,
        error ? 'border-error/50 bg-error/5' : 'border-slate-200 bg-white/50',
        isOpen
          ? 'border-primary ring-4 ring-primary/20 bg-white'
          : 'hover:border-primary/40 hover:bg-white',
        disabled ? 'opacity-60 cursor-not-allowed pointer-events-none' : '',
      ]"
      @click="toggleDropdown"
    >
      <!-- 当前选中值 -->
      <span
        class="truncate flex-1 font-medium"
        :class="[selectedLabel ? 'text-slate-700' : 'text-slate-400']"
      >
        {{ selectedLabel || "请选择" }}
      </span>

      <!-- 下拉箭头 -->
      <div
        class="ml-2 text-slate-400 transition-transform duration-300 ease-in-out"
        :class="[
          isOpen ? 'rotate-180 text-primary' : 'group-hover:text-primary/60',
          sizeClasses.icon,
        ]"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          class="w-full h-full"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </div>
    </div>

    <!-- 下拉面板 (Popover) -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-100 ease-out"
        :enter-from-class="
          dropdownPlacement === 'top'
            ? 'transform scale-98 opacity-0 translate-y-1'
            : 'transform scale-98 opacity-0 -translate-y-1'
        "
        enter-to-class="transform scale-100 opacity-100 translate-y-0"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100 translate-y-0"
        :leave-to-class="
          dropdownPlacement === 'top'
            ? 'transform scale-98 opacity-0 translate-y-1'
            : 'transform scale-98 opacity-0 -translate-y-1'
        "
      >
        <div
          v-if="isOpen && isPositioned"
          ref="dropdownPanelRef"
          class="bg-white border border-slate-200 rounded-xl shadow-xl overflow-hidden py-1"
          :style="dropdownStyle"
        >
          <div
            v-if="normalizedOptions.length === 0"
            class="px-4 py-3 text-center text-slate-400 text-xs"
          >
            暂无选项
          </div>
          <ul v-else class="overflow-y-auto custom-scrollbar" :style="{ maxHeight: 'inherit' }">
            <li v-for="opt in normalizedOptions" :key="opt.value">
              <div
                class="cursor-pointer transition-colors duration-150 flex items-center justify-between antialiased"
                :class="[
                  sizeClasses.item,
                  modelValue === opt.value
                    ? 'bg-primary/10 text-slate-900 font-bold'
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
                ]"
                @click="handleSelect(opt.value)"
              >
                <span class="truncate">{{ opt.label }}</span>
                <!-- 选中标记 -->
                <svg
                  v-if="modelValue === opt.value"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 text-primary"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
            </li>
          </ul>
        </div>
      </Transition>
    </Teleport>

    <!-- 底部描述/错误信息 -->
    <div v-if="description || error" class="label py-1 min-h-[24px]">
      <span
        class="label-text-alt transition-all duration-300 ease-out"
        :class="[error ? 'text-error font-medium' : 'text-slate-400']"
      >
        {{ error || description }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>

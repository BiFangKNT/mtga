<script setup lang="ts">
/**
 * MTGA 标准输入框组件
 * 采用 daisyUI 5 和 Tailwind CSS 4 规范实现
 * 支持尺寸、颜色状态、加载中、图标、清空及下拉功能
 */

interface Props {
  modelValue: string | number;
  label?: string;
  description?: string;
  descriptionClass?: string;
  placeholder?: string;
  type?: string;
  required?: boolean;
  disabled?: boolean;
  loading?: boolean;
  readonly?: boolean;
  /** 尺寸: 'xs' | 'sm' | 'md' | 'lg' */
  size?: "xs" | "sm" | "md" | "lg";
  /** 颜色状态: 'primary' | 'success' | 'warning' | 'error' | 'neutral' */
  color?: "primary" | "success" | "warning" | "error" | "neutral";
  /** 左侧图标路径 (SVG path d) */
  icon?: string;
  /** 右侧图标路径 (SVG path d) */
  trailingIcon?: string;
  /** 是否显示下拉按钮 (模拟 Select) */
  showDropdown?: boolean;
  /** 下拉选项 */
  options?: string[];
  /** 下拉选项是否按多选模式处理 */
  multiSelect?: boolean;
  /** 多选模式下的已选中选项 */
  selectedOptions?: string[];
  /** 是否可清空 */
  clearable?: boolean;
  /** 错误信息，存在时 color 强制为 error */
  error?: string;
  /** 传递给 input 元素的类名 */
  inputClass?: string;
}

const props = withDefaults(defineProps<Props>(), {
  type: "text",
  size: "md",
  clearable: true,
  label: "",
  description: "",
  descriptionClass: "",
  placeholder: "",
  color: "neutral",
  icon: "",
  trailingIcon: "",
  options: () => [],
  multiSelect: false,
  selectedOptions: () => [],
  error: "",
  inputClass: "",
});

const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "dropdown"): void;
  (e: "select", value: string): void;
  (e: "focus"): void;
  (e: "blur"): void;
}>();

const dropdownOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);
const isPositioned = ref(false);
const isFiltering = ref(false); // 标记是否正在过滤（仅在展开后有输入才为 true）
const slots = useSlots();

// 下拉菜单定位样式
const dropdownStyle = ref<Record<string, string | number>>({});

/**
 * 更新下拉菜单的定位
 * 通过 getBoundingClientRect 实时计算输入框位置
 */
const updateDropdownPosition = () => {
  if (!dropdownRef.value || !dropdownOpen.value) return;

  const rect = dropdownRef.value.getBoundingClientRect();
  // 检查下方是否有足够空间，否则向上弹出 (简单实现)
  const spaceBelow = window.innerHeight - rect.bottom;
  const hasSpaceBelow = spaceBelow > 250; // 下拉框最大高度约 240px

  dropdownStyle.value = {
    position: "fixed",
    top: hasSpaceBelow ? `${rect.bottom + 6}px` : "auto",
    bottom: !hasSpaceBelow ? `${window.innerHeight - rect.top + 6}px` : "auto",
    left: `${rect.left}px`,
    width: `${rect.width}px`,
    zIndex: 9999,
  };

  // 延迟一帧设置定位完成状态，确保样式已应用到 DOM
  requestAnimationFrame(() => {
    isPositioned.value = true;
  });
};

// 监听窗口事件以同步位置
watch(dropdownOpen, async (val) => {
  if (val) {
    isPositioned.value = false;
    isFiltering.value = false; // 展开时重置过滤状态，显示完整列表
    dropdownStyle.value = {}; // 重置样式
    await nextTick();
    updateDropdownPosition();
    window.addEventListener("scroll", updateDropdownPosition, true);
    window.addEventListener("resize", updateDropdownPosition);
  } else {
    window.removeEventListener("scroll", updateDropdownPosition, true);
    window.removeEventListener("resize", updateDropdownPosition);
    isPositioned.value = false;
    isFiltering.value = false;
  }
});

// 样式映射
const inputSizeClass = computed(() => {
  const sizes = {
    xs: "px-2 py-1",
    sm: "px-3 py-1.5",
    md: "px-3.5 py-2",
    lg: "px-4 py-2.5",
  };
  return sizes[props.size];
});

const hasActionArea = computed(() => {
  return props.loading || props.showDropdown || slots.trailing || props.trailingIcon;
});

const selectedOptionSet = computed(() => new Set(props.selectedOptions));
const isOptionSelected = (option: string) => {
  if (props.multiSelect) {
    return selectedOptionSet.value.has(option);
  }
  return props.modelValue === option;
};

// 计算后缀区宽度以动态调整输入框内边距
const suffixPaddingClass = computed(() => {
  let actionCount = 0;
  if (props.loading) actionCount++;
  if (props.showDropdown) actionCount++;
  if (props.trailingIcon || slots.trailing) actionCount++;

  const hasClear = props.clearable && props.modelValue && !props.disabled && !props.readonly;

  // 只有 actionCount > 0 时才会有分割线和后缀按钮区
  if (actionCount > 0) {
    if (hasClear) return "pr-24"; // 清空按钮 + 分割线 + 后缀按钮
    return "pr-16"; // 分割线 + 后缀按钮
  }

  if (hasClear) return "pr-10"; // 仅清空按钮
  return "pr-3.5"; // 默认
});

// 点击外部关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target;
  if (dropdownRef.value && target instanceof Node && !dropdownRef.value.contains(target)) {
    dropdownOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});

const toggleDropdown = (e: Event) => {
  e.stopPropagation();
  if (props.disabled || props.loading) return;
  if (!dropdownOpen.value) {
    emit("dropdown");
  }
  dropdownOpen.value = !dropdownOpen.value;
};

const handleSelect = (val: string) => {
  if (props.multiSelect) {
    emit("select", val);
    isFiltering.value = false;
    dropdownOpen.value = true;
    return;
  }
  emit("update:modelValue", val);
  emit("select", val);
  dropdownOpen.value = false;
};

const handleInput = (e: Event) => {
  if (e.target instanceof HTMLInputElement) {
    const val = e.target.value;
    emit("update:modelValue", val);

    // 如果 Popover 已经打开，且有选项，则在输入时保持打开并允许过滤
    if (props.showDropdown && props.options.length > 0) {
      dropdownOpen.value = true;
      isFiltering.value = true; // 标记开始过滤
    }
  }
};

// 过滤后的选项
const filteredOptions = computed(() => {
  if (!props.options || props.options.length === 0) return [];
  // 如果当前不是过滤模式（即刚打开），显示完整列表
  if (!isFiltering.value) return props.options;

  const search = String(props.modelValue).toLowerCase().trim();
  if (!search) return props.options;
  return props.options.filter((opt) => opt.toLowerCase().includes(search));
});

const handleClear = (e: MouseEvent) => {
  e.stopPropagation(); // 阻止冒泡，防止触发父级的点击事件导致下拉收起
  emit("update:modelValue", "");
  isFiltering.value = true; // 清空也视为一种过滤操作，显示全部
  // 点击清空时不收起下拉菜单
};
</script>

<template>
  <div class="form-control w-full">
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

    <!-- 输入框包装器 -->
    <div
      ref="dropdownRef"
      class="relative flex items-center group transition-all duration-150 ease-out border rounded-xl shadow-sm"
      :class="[
        error
          ? 'border-error/50 bg-error/5'
          : 'border-slate-200 bg-slate-100/70 focus-within:bg-white focus-within:border-primary focus-within:ring-4 focus-within:ring-primary/20',
        disabled || loading
          ? 'opacity-60 cursor-not-allowed'
          : 'hover:border-primary/40 hover:bg-white',
      ]"
    >
      <!-- 前缀插槽 / 图标 -->
      <div
        v-if="$slots.leading || icon"
        class="absolute left-3 flex items-center justify-center pointer-events-none transition-colors duration-150"
        :class="[
          size === 'xs' ? 'w-4' : 'w-5',
          error
            ? 'text-error/70'
            : 'text-slate-400 group-hover:text-primary/60 group-focus-within:text-primary',
        ]"
      >
        <slot name="leading">
          <svg
            v-if="icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="w-full h-full"
          >
            <path :d="icon" />
          </svg>
        </slot>
      </div>

      <!-- 输入框主体 -->
      <input
        :value="modelValue"
        :type="type"
        :placeholder="placeholder"
        :disabled="disabled || loading"
        :readonly="readonly"
        class="w-full bg-transparent outline-none transition-all duration-150 border-none focus:ring-0"
        :class="[
          inputSizeClass,
          suffixPaddingClass,
          $slots.leading || icon ? 'pl-10' : 'pl-3.5',
          size === 'xs' ? 'h-7 text-xs' : size === 'sm' ? 'h-8 text-sm' : 'h-10 text-sm',
          inputClass,
        ]"
        @input="handleInput"
        @focus="emit('focus')"
        @blur="emit('blur')"
      />

      <!-- 清空按钮 (独立于操作区，在分割线左侧) -->
      <button
        v-if="clearable && modelValue && !disabled && !readonly"
        type="button"
        class="absolute btn btn-ghost btn-circle btn-xs text-slate-400 hover:text-error hover:bg-error/10 transition-all duration-200 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100"
        :class="[hasActionArea ? 'right-11' : 'right-2.5']"
        title="清空"
        @click="handleClear"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-3.5 w-3.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      <!-- 后缀功能区 (带分割线) -->
      <div v-if="hasActionArea" class="absolute right-0 top-0 bottom-0 flex items-center pr-2">
        <!-- 分割线 -->
        <div
          class="h-1/2 w-px bg-slate-200 mx-1 group-hover:bg-primary/20 group-focus-within:bg-primary/30 transition-colors"
        ></div>

        <div class="flex items-center gap-1">
          <!-- 下拉按钮 (模拟 Select) -->
          <button
            v-if="showDropdown"
            type="button"
            class="btn btn-ghost btn-circle btn-xs text-slate-400 hover:text-primary transition-all duration-200"
            :class="{ 'rotate-180 text-primary bg-primary/10': dropdownOpen }"
            @click="toggleDropdown"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          <!-- 自定义后缀插槽 / 图标 -->
          <div
            v-if="$slots.trailing || trailingIcon"
            class="flex items-center justify-center transition-colors px-1"
            :class="[
              size === 'xs' ? 'w-4' : 'w-5',
              error ? 'text-error/70' : 'text-slate-400 group-focus-within:text-primary/70',
            ]"
          >
            <slot name="trailing">
              <svg
                v-if="trailingIcon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="w-full h-full"
              >
                <path :d="trailingIcon" />
              </svg>
            </slot>
          </div>
        </div>
      </div>

      <!-- 下拉面板 (使用 Teleport 实现 Portal 功能，解决父级 overflow 遮挡问题) -->
      <Teleport to="body">
        <div
          v-if="showDropdown && dropdownOpen && isPositioned"
          :style="dropdownStyle"
          class="bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden animate-in fade-in zoom-in duration-300 origin-top"
          @click.stop
        >
          <!-- Loading 遮罩层 (居中动画 + 毛玻璃) -->
          <div
            v-if="loading"
            class="absolute inset-0 z-10 flex items-center justify-center bg-white/40 backdrop-blur-[2px] transition-all duration-300"
          >
            <div class="flex flex-col items-center gap-2">
              <span class="loading loading-spinner loading-md text-primary"></span>
              <span class="text-[10px] text-slate-500 font-medium">加载中...</span>
            </div>
          </div>

          <div
            v-if="!filteredOptions || filteredOptions.length === 0"
            class="px-4 py-6 text-center"
          >
            <p class="text-slate-400 text-xs">暂无匹配数据</p>
          </div>
          <!-- 明确为单列布局 (flex-col) 且占满宽度 (w-full) -->
          <ul
            v-else
            class="menu flex-col flex-nowrap p-1 max-h-[240px] overflow-auto custom-scrollbar w-full"
          >
            <li v-for="opt in filteredOptions" :key="opt">
              <button
                type="button"
                class="flex items-center gap-2 py-2 px-3 rounded-lg hover:bg-primary/5 hover:text-primary transition-all duration-200 text-sm w-full"
                :class="{ 'bg-primary/10 text-primary font-medium': isOptionSelected(opt) }"
                @click="handleSelect(opt)"
              >
                <span class="truncate flex-1 text-left">{{ opt }}</span>
                <svg
                  v-if="isOptionSelected(opt)"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4"
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
              </button>
            </li>
          </ul>
        </div>
      </Teleport>
    </div>

    <!-- 底部描述/错误信息 -->
    <div v-if="description || error" class="label py-1 min-h-[24px]">
      <span
        class="label-text-alt transition-all duration-300 ease-out flex items-center gap-1"
        :class="[
          error ? 'text-error font-medium text-[11px]' : ['text-slate-400', descriptionClass],
        ]"
      >
        <template v-if="error">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-3.5 h-3.5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          {{ error }}
        </template>
        <template v-else>
          {{ description }}
        </template>
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
  background: var(--color-primary, #f0bb32);
}
</style>

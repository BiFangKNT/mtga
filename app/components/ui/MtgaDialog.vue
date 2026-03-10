<script setup lang="ts">
/**
 * MTGA 通用对话框基础组件
 * 仅负责容器层行为：展示、关闭和结构插槽
 */
const props = withDefaults(
  defineProps<{
    /** 是否显示对话框 */
    open?: boolean;
    /** 对话框最大宽度，默认为 max-w-sm */
    maxWidth?: string;
    /** 是否点击背景自动关闭，默认为 true */
    closeOnBackdrop?: boolean;
    /** 是否按 ESC 自动关闭，默认为 true */
    closeOnEsc?: boolean;
  }>(),
  {
    open: false,
    maxWidth: "max-w-sm",
    closeOnBackdrop: true,
    closeOnEsc: true,
  },
);

const emit = defineEmits<{
  (event: "update:open", value: boolean): void;
  (event: "close"): void;
}>();

/**
 * 统一关闭出口：同步 open 状态并发出 close 语义事件
 */
const requestClose = () => {
  if (!props.open) {
    return;
  }
  emit("update:open", false);
  emit("close");
};

const handleBackdropClick = () => {
  if (!props.closeOnBackdrop) {
    return;
  }
  requestClose();
};

const handleEscape = () => {
  if (!props.closeOnEsc) {
    return;
  }
  requestClose();
};
</script>

<template>
  <dialog class="modal" :class="{ 'modal-open': props.open }" @keydown.esc.prevent="handleEscape">
    <div
      class="modal-box mtga-card p-0 overflow-hidden border-slate-200/60 shadow-2xl transition-all duration-200"
      :class="[props.maxWidth, props.open ? 'scale-100 opacity-100' : 'scale-95 opacity-0']"
    >
      <div class="mtga-card-body p-0 flex flex-col">
        <!-- 头部插槽：统一由基础组件提供底部分割线 -->
        <div v-if="$slots.header" class="px-6 py-5 border-b border-slate-100/50">
          <slot name="header"></slot>
        </div>

        <!-- 默认插槽：主要内容区 -->
        <div class="flex-1 min-h-0 overflow-y-auto">
          <slot></slot>
        </div>

        <!-- 底部插槽：操作按钮区 -->
        <div
          v-if="$slots.footer"
          class="px-6 py-3 bg-slate-50/50 border-t border-slate-100 flex items-center gap-3"
        >
          <slot name="footer"></slot>
        </div>
      </div>
    </div>

    <!-- 背景遮罩 -->
    <form
      v-if="props.closeOnBackdrop"
      method="dialog"
      class="modal-backdrop bg-slate-900/20 backdrop-blur-[2px] transition-opacity duration-200"
      :class="props.open ? 'opacity-100' : 'opacity-0'"
      @click.prevent="handleBackdropClick"
    >
      <button type="button" aria-label="关闭对话框">close</button>
    </form>
    <div
      v-else
      class="modal-backdrop bg-slate-900/20 backdrop-blur-[2px] transition-opacity duration-200"
      :class="props.open ? 'opacity-100' : 'opacity-0'"
    ></div>
  </dialog>
</template>

<style scoped>
.modal-open {
  pointer-events: auto;
  visibility: visible;
  opacity: 1;
}
</style>

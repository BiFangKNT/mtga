<script setup lang="ts">
/**
 * WarmupHud 组件
 * 用于在后台预热或加载资源时向用户展示进度
 */

const {
  lazyWarmupVisible,
  lazyWarmupStatus,
  lazyWarmupLabel,
  lazyWarmupDetail,
  lazyWarmupCompleted,
  lazyWarmupTotal,
} = useMtgaStore();

/**
 * 计算进度条数值 (0 到 1)
 */
const progressValue = computed(() => {
  const total = Math.max(lazyWarmupTotal.value, 0);
  const completed = Math.max(lazyWarmupCompleted.value, 0);
  if (total <= 0) {
    return lazyWarmupStatus.value === "done" ? 1 : 0.05;
  }
  if (lazyWarmupStatus.value === "done") {
    return 1;
  }
  if (lazyWarmupStatus.value === "error") {
    return Math.min(completed / total, 1);
  }
  // 运行中时，稍微超前一点进度以获得更好的视觉反馈
  return Math.min((completed + 0.4) / total, 0.98);
});

/**
 * 计算进度条右侧的文本描述
 */
const progressText = computed(() => {
  const total = Math.max(lazyWarmupTotal.value, 0);
  if (lazyWarmupStatus.value === "done") {
    return "已完成";
  }
  if (lazyWarmupStatus.value === "error") {
    return "已暂停";
  }
  if (total <= 0) {
    return "初始化";
  }
  return `${Math.min(lazyWarmupCompleted.value + 1, total)} / ${total}`;
});

/**
 * 计算进度条宽度百分比
 */
const progressWidth = computed(() => `${Math.max(progressValue.value, 0) * 100}%`);

/**
 * 状态对应的文字颜色类
 */
const accentClass = computed(() => {
  if (lazyWarmupStatus.value === "done") {
    return "text-emerald-500";
  }
  if (lazyWarmupStatus.value === "error") {
    return "text-rose-500";
  }
  return "text-blue-500";
});

/**
 * 进度条颜色类
 */
const progressBarClass = computed(() => {
  if (lazyWarmupStatus.value === "done") {
    return "bg-gradient-to-r from-emerald-500 to-teal-400 shadow-[inset_0_0_8px_rgba(255,255,255,0.2)]";
  }
  if (lazyWarmupStatus.value === "error") {
    return "bg-gradient-to-r from-rose-500 to-orange-400 shadow-[inset_0_0_8px_rgba(255,255,255,0.2)]";
  }
  return "bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-400 shadow-[inset_0_0_10px_rgba(255,255,255,0.25)]";
});
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-400 ease-[cubic-bezier(0.23,1,0.32,1)]"
      enter-from-class="-translate-y-4 opacity-0 scale-95"
      enter-to-class="translate-y-0 opacity-100 scale-100"
      leave-active-class="transition duration-300 ease-[cubic-bezier(0.4,0,1,1)]"
      leave-from-class="translate-y-0 opacity-100 scale-100"
      leave-to-class="-translate-y-2 opacity-0 scale-98"
    >
      <div
        v-if="lazyWarmupVisible"
        data-mtga-warmup-hud="true"
        class="pointer-events-none fixed left-1/2 top-6 z-2147483647 w-[min(340px,calc(100vw-2rem))] -translate-x-1/2"
      >
        <div
          class="warmup-hud-shell relative overflow-hidden rounded-2xl"
          role="status"
          aria-live="polite"
        >
          <div class="relative flex items-center gap-3.5 px-4 py-3.5">
            <!-- 状态指示器 -->
            <div class="relative flex size-9 shrink-0 items-center justify-center">
              <div class="warmup-spinner" :class="lazyWarmupStatus" />
              <div
                class="absolute size-1.5 rounded-full transition-colors duration-300"
                :class="accentClass"
              />
            </div>

            <!-- 文本信息 -->
            <div class="min-w-0 flex-1">
              <div class="flex items-center justify-between gap-2">
                <p class="truncate text-[13.5px] font-medium tracking-tight text-slate-900">
                  {{ lazyWarmupLabel || "后台任务处理中" }}
                </p>
                <span
                  class="shrink-0 text-[10.5px] font-semibold tabular-nums tracking-wide text-slate-500/80"
                >
                  {{ progressText }}
                </span>
              </div>

              <p class="mt-0.5 truncate text-[11px] leading-relaxed text-slate-500/70">
                {{ lazyWarmupDetail || "正在为您优化使用体验" }}
              </p>
            </div>
          </div>

          <!-- 进度条 -->
          <div class="px-4 pb-4">
            <div class="warmup-track h-[7px] overflow-hidden rounded-full">
              <div
                class="warmup-progress relative h-full rounded-full transition-[width] duration-700 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
                :class="[progressBarClass, { 'is-running': lazyWarmupStatus === 'running' }]"
                :style="{ width: progressWidth }"
              />
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.warmup-hud-shell {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px) saturate(190%);
  -webkit-backdrop-filter: blur(20px) saturate(190%);
  border: 0.5px solid rgba(255, 255, 255, 0.4);
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.05),
    0 10px 25px -5px rgba(0, 0, 0, 0.1),
    0 20px 48px -12px rgba(0, 0, 0, 0.12),
    inset 0 0 0 1px rgba(255, 255, 255, 0.2);
}

.warmup-spinner {
  width: 100%;
  height: 100%;
  border-radius: 9999px;
  border: 2px solid rgba(0, 0, 0, 0.04);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.warmup-spinner.running {
  border-top-color: currentColor;
  color: #3b82f6;
  animation: warmup-rotate 0.8s linear infinite;
}

.warmup-spinner.done {
  border-color: rgba(16, 185, 129, 0.15);
  background: rgba(16, 185, 129, 0.03);
}

.warmup-spinner.error {
  border-color: rgba(244, 63, 94, 0.15);
  background: rgba(244, 63, 94, 0.03);
}

.warmup-track {
  background: rgba(0, 0, 0, 0.04);
  box-shadow:
    inset 0 1px 2px rgba(0, 0, 0, 0.05),
    0 1px 1px rgba(255, 255, 255, 0.5);
}

.warmup-progress.is-running {
  animation: warmup-pulse 2s infinite ease-in-out;
}

.warmup-progress.is-running::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.1) 30%,
    rgba(255, 255, 255, 0.55) 50%,
    rgba(255, 255, 255, 0.1) 70%,
    rgba(255, 255, 255, 0) 100%
  );
  background-size: 200% 100%;
  animation: warmup-shimmer 1.4s infinite ease-out;
}

@keyframes warmup-rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes warmup-shimmer {
  from {
    background-position: 200% 0;
  }
  to {
    background-position: -200% 0;
  }
}

@keyframes warmup-pulse {
  0%,
  100% {
    filter: brightness(1) saturate(100%);
  }
  50% {
    filter: brightness(1.15) saturate(110%);
  }
}

/* 适配深色背景下的对比度 */
:root[data-theme="dark"] .warmup-hud-shell {
  background: rgba(28, 28, 30, 0.82);
  border: 0.5px solid rgba(255, 255, 255, 0.12);
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.3),
    inset 0 0 0 1px rgba(255, 255, 255, 0.05);
}

:root[data-theme="dark"] .warmup-spinner {
  border-color: rgba(255, 255, 255, 0.08);
}

:root[data-theme="dark"] .warmup-track {
  background: rgba(255, 255, 255, 0.08);
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.2);
}

:root[data-theme="dark"] .text-slate-900 {
  color: rgba(255, 255, 255, 0.94);
}

:root[data-theme="dark"] .text-slate-500\/80 {
  color: rgba(255, 255, 255, 0.5);
}

:root[data-theme="dark"] .text-slate-500\/70 {
  color: rgba(255, 255, 255, 0.4);
}

@media (prefers-reduced-motion: reduce) {
  .warmup-spinner.running,
  .warmup-progress.is-running::after {
    animation: none;
  }
}
</style>

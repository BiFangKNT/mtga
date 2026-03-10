<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    logs?: string[];
    emptyText?: string;
  }>(),
  {
    logs: () => [],
    emptyText: "日志输出占位",
  },
);

const logBox = ref<HTMLDivElement | null>(null);

const logCount = computed(() => props.logs?.length ?? 0);

const formattedLogs = computed(() =>
  props.logs && props.logs.length ? props.logs.join("\n") : props.emptyText,
);

watch(
  () => props.logs,
  async () => {
    await nextTick();
    if (logBox.value) {
      logBox.value.scrollTop = logBox.value.scrollHeight;
    }
  },
  { deep: true },
);
</script>

<template>
  <div class="flex items-center justify-between gap-3 shrink-0">
    <div>
      <h2 class="mtga-card-title">运行日志</h2>
      <p class="mtga-card-subtitle">实时记录后端与操作状态</p>
    </div>
    <div class="flex items-center gap-2">
      <span class="mtga-chip">实时输出</span>
      <span class="text-xs text-slate-500">共 {{ logCount }} 条</span>
    </div>
  </div>
  <div
    ref="logBox"
    class="mtga-log-scroll mt-4 flex-1 overflow-auto rounded-xl border border-slate-200/50 bg-slate-500/10 backdrop-blur-md p-4 text-sm font-mono text-slate-700"
  >
    <pre class="whitespace-pre-wrap leading-relaxed">{{ formattedLogs }}</pre>
  </div>
</template>

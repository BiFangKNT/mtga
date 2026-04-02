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

const emit = defineEmits<{
  (event: "clear"): void;
}>();

const logBox = ref<HTMLDivElement | null>(null);
const clearConfirmOpen = ref(false);

const logCount = computed(() => props.logs?.length ?? 0);

const tryFormatJsonText = (text: string) => {
  const trimmed = text.trim();
  if (!trimmed) {
    return null;
  }
  try {
    const parsed = JSON.parse(trimmed) as unknown;
    if (parsed === null || typeof parsed !== "object") {
      return null;
    }
    return JSON.stringify(parsed, null, 2);
  } catch {
    return null;
  }
};

const formatLogEntry = (entry: string) => {
  const directJson = tryFormatJsonText(entry);
  if (directJson) {
    return directJson;
  }

  const jsonStartMatches = Array.from(entry.matchAll(/{/g));
  for (const match of jsonStartMatches) {
    const startIndex = match.index;
    if (typeof startIndex !== "number") {
      continue;
    }
    const prefix = entry.slice(0, startIndex).trimEnd();
    const suffix = entry.slice(startIndex);
    const formattedJson = tryFormatJsonText(suffix);
    if (!formattedJson) {
      continue;
    }
    return prefix ? `${prefix}\n${formattedJson}` : formattedJson;
  }

  return entry;
};

const formattedLogs = computed(() =>
  props.logs && props.logs.length
    ? props.logs.map((entry) => formatLogEntry(entry)).join("\n")
    : props.emptyText,
);

const requestClearLogs = () => {
  if (!logCount.value) {
    return;
  }
  clearConfirmOpen.value = true;
};

const cancelClearLogs = () => {
  clearConfirmOpen.value = false;
};

const confirmClearLogs = () => {
  emit("clear");
  clearConfirmOpen.value = false;
};

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
      <button
        class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
        :disabled="logCount === 0"
        @click="requestClearLogs"
      >
        清空
      </button>
      <span class="text-xs text-slate-500">共 {{ logCount }} 条</span>
    </div>
  </div>
  <div
    ref="logBox"
    class="mtga-log-scroll mt-4 flex-1 overflow-auto rounded-xl border border-slate-200/50 bg-slate-500/10 backdrop-blur-md p-4 text-sm font-mono text-slate-700"
  >
    <pre class="whitespace-pre-wrap leading-relaxed">{{ formattedLogs }}</pre>
  </div>

  <ConfirmDialog
    :open="clearConfirmOpen"
    title="确认清空日志"
    message="确定要清空当前日志吗？"
    type="error"
    confirm-text="清空"
    @cancel="cancelClearLogs"
    @confirm="confirmClearLogs"
  />
</template>

<script setup lang="ts">
import type { ProxyTrace, ProxyTraceBodyCapture, ProxyTraceSummary } from "~/composables/mtgaTypes";

const store = useMtgaStore();
const loading = ref(false);
const clearing = ref(false);
const detailOpen = ref(false);
const autoRefreshTimer = ref<ReturnType<typeof setInterval> | null>(null);

const traces = computed(() => store.proxyTraces.value);
const selectedTrace = computed(() => store.selectedProxyTrace.value);
const selectedTraceId = computed(() => selectedTrace.value?.trace_id || "");
const hasTraces = computed(() => traces.value.length > 0);

const statusMeta: Record<ProxyTrace["status"], { label: string; className: string }> = {
  active: {
    label: "进行中",
    className: "border-sky-200 bg-sky-50 text-sky-700",
  },
  completed: {
    label: "完成",
    className: "border-emerald-200 bg-emerald-50 text-emerald-700",
  },
  failed: {
    label: "失败",
    className: "border-rose-200 bg-rose-50 text-rose-700",
  },
  cancelled: {
    label: "中断",
    className: "border-slate-200 bg-slate-100 text-slate-600",
  },
};

const formatTime = (value?: string) => {
  if (!value) {
    return "-";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString();
};

const formatDuration = (value?: number) => {
  if (typeof value !== "number") {
    return "-";
  }
  if (value < 1000) {
    return `${value} ms`;
  }
  return `${(value / 1000).toFixed(2)} s`;
};

const formatBytes = (value?: number) => {
  if (typeof value !== "number") {
    return "-";
  }
  if (value < 1024) {
    return `${value} B`;
  }
  if (value < 1024 * 1024) {
    return `${(value / 1024).toFixed(1)} KB`;
  }
  return `${(value / 1024 / 1024).toFixed(1)} MB`;
};

const stringifyValue = (value: unknown) => {
  if (typeof value === "undefined") {
    return "";
  }
  if (typeof value === "string") {
    return value;
  }
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
};

const formatBody = (body?: ProxyTraceBodyCapture) => {
  if (!body) {
    return "";
  }
  return stringifyValue(body.value);
};

const traceTitle = (trace: ProxyTraceSummary) => {
  return trace.request_model || trace.upstream_model || trace.request_path;
};

const refresh = async () => {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    await store.loadProxyTraces();
    if (detailOpen.value && selectedTrace.value) {
      await store.loadProxyTraceDetail(selectedTrace.value.trace_id);
    }
  } finally {
    loading.value = false;
  }
};

const selectTrace = async (trace: ProxyTraceSummary) => {
  if (loading.value) {
    return;
  }
  const ok = await store.loadProxyTraceDetail(trace.trace_id);
  if (ok) {
    detailOpen.value = true;
  }
};

const closeDetail = () => {
  detailOpen.value = false;
};

const clearLogs = async () => {
  if (clearing.value || !hasTraces.value) {
    return;
  }
  clearing.value = true;
  try {
    await store.clearProxyTraces();
    if (!selectedTrace.value) {
      detailOpen.value = false;
    }
  } finally {
    clearing.value = false;
  }
};

onMounted(() => {
  void refresh();
  autoRefreshTimer.value = setInterval(() => {
    void store.loadProxyTraces();
    if (detailOpen.value && selectedTrace.value?.status === "active") {
      void store.loadProxyTraceDetail(selectedTrace.value.trace_id);
    }
  }, 2000);
});

onBeforeUnmount(() => {
  if (autoRefreshTimer.value !== null) {
    clearInterval(autoRefreshTimer.value);
    autoRefreshTimer.value = null;
  }
});
</script>

<template>
  <div class="flex h-full min-h-0 flex-col">
    <div class="flex shrink-0 items-center justify-between gap-3">
      <div>
        <h2 class="mtga-card-title">代理日志</h2>
        <p class="mtga-card-subtitle">按请求追踪代理转发、响应与错误</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
          :class="loading ? 'loading' : ''"
          :disabled="loading || clearing"
          @click="refresh"
        >
          刷新
        </button>
        <button
          class="btn btn-sm btn-outline rounded-xl border-rose-200 text-rose-600 hover:border-rose-300 hover:bg-rose-50"
          :class="clearing ? 'loading' : ''"
          :disabled="loading || clearing || !hasTraces"
          @click="clearLogs"
        >
          清空
        </button>
      </div>
    </div>

    <div class="mt-4 min-h-0 flex-1 overflow-y-auto pr-1 custom-scrollbar">
      <div class="grid gap-3 2xl:grid-cols-2">
        <button
          v-for="trace in traces"
          :key="trace.trace_id"
          class="mtga-clickable-row w-full items-start"
          :class="selectedTraceId === trace.trace_id ? 'border-amber-400/70 bg-amber-50/50' : ''"
          @click="selectTrace(trace)"
        >
          <span class="flex w-full min-w-0 flex-col gap-2 text-left">
            <span class="flex items-center justify-between gap-2">
              <span class="truncate text-sm font-bold text-slate-700">{{ traceTitle(trace) }}</span>
              <span
                class="shrink-0 rounded-full border px-2 py-0.5 text-[11px] font-bold"
                :class="statusMeta[trace.status].className"
              >
                {{ statusMeta[trace.status].label }}
              </span>
            </span>
            <span class="flex items-center gap-2 text-[11px] text-slate-500">
              <span class="font-mono">{{ trace.request_id }}</span>
              <span>{{ trace.provider || "unknown" }}</span>
              <span>{{ formatDuration(trace.duration_ms) }}</span>
            </span>
            <span class="truncate text-[11px] text-slate-400">{{
              formatTime(trace.started_at)
            }}</span>
          </span>
        </button>
      </div>

      <div
        v-if="!loading && traces.length === 0"
        class="rounded-xl border border-slate-200/70 bg-white/40 p-6 text-center text-sm text-slate-400"
      >
        暂无代理请求记录
      </div>
    </div>

    <Teleport to="body">
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="detailOpen && selectedTrace" class="fixed inset-0 z-50 bg-slate-950/30">
          <button
            aria-label="关闭代理日志详情"
            class="absolute inset-0 cursor-default"
            tabindex="-1"
            type="button"
            @click="closeDetail"
          />

          <Transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="translate-x-full"
            enter-to-class="translate-x-0"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-x-0"
            leave-to-class="translate-x-full"
          >
            <aside
              v-if="detailOpen && selectedTrace"
              class="absolute right-0 top-0 flex h-full w-full max-w-[860px] min-w-0 flex-col overflow-hidden border-l border-slate-200 bg-[#fff8e8] shadow-2xl sm:w-[min(860px,calc(100vw-40px))]"
            >
              <div class="shrink-0 border-b border-slate-200/70 p-5">
                <div class="flex min-w-0 items-start justify-between gap-4">
                  <div class="min-w-0">
                    <div class="flex flex-wrap items-center gap-2">
                      <span
                        class="rounded-full border px-2 py-0.5 text-[11px] font-bold"
                        :class="statusMeta[selectedTrace.status].className"
                      >
                        {{ statusMeta[selectedTrace.status].label }}
                      </span>
                      <span class="font-mono text-xs text-slate-500">
                        {{ selectedTrace.request_id }}
                      </span>
                    </div>
                    <h3 class="mt-2 truncate text-lg font-bold text-slate-800">
                      {{ traceTitle(selectedTrace) }}
                    </h3>
                    <div class="mt-1 truncate text-xs text-slate-500">
                      {{ selectedTrace.method }} {{ selectedTrace.request_path }}
                    </div>
                  </div>
                  <button
                    class="btn btn-sm btn-ghost shrink-0 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-700"
                    type="button"
                    @click="closeDetail"
                  >
                    关闭
                  </button>
                </div>
              </div>

              <div
                class="min-h-0 min-w-0 flex-1 overflow-x-hidden overflow-y-auto p-5 custom-scrollbar"
              >
                <div class="grid min-w-0 grid-cols-1 gap-3 text-xs md:grid-cols-2 xl:grid-cols-4">
                  <div
                    class="min-w-0 overflow-hidden rounded-lg border border-slate-200/60 bg-white/50 p-3"
                  >
                    <div class="font-bold text-slate-500">上游</div>
                    <div
                      class="mt-1 overflow-x-auto whitespace-nowrap font-mono text-slate-700 custom-scrollbar"
                    >
                      {{ selectedTrace.provider || "-" }} /
                      {{ selectedTrace.upstream_model || "-" }}
                    </div>
                  </div>
                  <div class="min-w-0 rounded-lg border border-slate-200/60 bg-white/50 p-3">
                    <div class="font-bold text-slate-500">响应</div>
                    <div class="mt-1 text-slate-700">
                      {{ selectedTrace.status_code || "-" }} ·
                      {{ selectedTrace.is_stream ? "SSE" : "JSON" }}
                    </div>
                  </div>
                  <div class="min-w-0 rounded-lg border border-slate-200/60 bg-white/50 p-3">
                    <div class="font-bold text-slate-500">请求体</div>
                    <div class="mt-1 text-slate-700">
                      {{ formatBytes(selectedTrace.request_body?.bytes) }}
                      <span v-if="selectedTrace.request_body?.truncated"> · 已截断</span>
                      <span v-if="selectedTrace.request_body?.redacted"> · 已脱敏</span>
                    </div>
                  </div>
                  <div class="min-w-0 rounded-lg border border-slate-200/60 bg-white/50 p-3">
                    <div class="font-bold text-slate-500">响应体</div>
                    <div class="mt-1 text-slate-700">
                      {{ formatBytes(selectedTrace.response_body?.bytes) }}
                      <span v-if="selectedTrace.response_body?.truncated"> · 已截断</span>
                    </div>
                  </div>
                </div>

                <div
                  v-if="selectedTrace.error"
                  class="mt-4 rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700"
                >
                  {{ selectedTrace.error }}
                </div>

                <div class="mt-4 grid min-w-0 gap-4 xl:grid-cols-2">
                  <section class="min-w-0">
                    <h4 class="mb-2 text-xs font-bold uppercase text-slate-400">Request</h4>
                    <pre
                      class="max-h-[360px] w-full max-w-full overflow-x-hidden overflow-y-auto whitespace-pre-wrap rounded-lg bg-slate-950 p-3 text-xs text-slate-100 [overflow-wrap:anywhere] custom-scrollbar"
                      >{{ formatBody(selectedTrace.request_body) || "-" }}</pre
                    >
                  </section>
                  <section class="min-w-0">
                    <h4 class="mb-2 text-xs font-bold uppercase text-slate-400">Response</h4>
                    <pre
                      class="max-h-[360px] w-full max-w-full overflow-x-hidden overflow-y-auto whitespace-pre-wrap rounded-lg bg-slate-950 p-3 text-xs text-slate-100 [overflow-wrap:anywhere] custom-scrollbar"
                      >{{ formatBody(selectedTrace.response_body) || "-" }}</pre
                    >
                  </section>
                  <section class="min-w-0 xl:col-span-2">
                    <h4 class="mb-2 text-xs font-bold uppercase text-slate-400">Events</h4>
                    <div class="space-y-2">
                      <div
                        v-for="event in selectedTrace.events"
                        :key="`${event.at}-${event.kind}-${event.message || ''}`"
                        class="min-w-0 rounded-lg border border-slate-200/60 bg-white/50 p-3 text-xs"
                      >
                        <div class="flex flex-wrap items-center justify-between gap-2">
                          <span class="font-bold text-slate-700">{{ event.kind }}</span>
                          <span class="font-mono text-slate-400">{{ formatTime(event.at) }}</span>
                        </div>
                        <div v-if="event.message" class="mt-1 break-words text-slate-600">
                          {{ event.message }}
                        </div>
                        <pre
                          v-if="event.data"
                          class="mt-2 max-w-full overflow-x-hidden overflow-y-auto whitespace-pre-wrap rounded bg-slate-100 p-2 text-[11px] text-slate-700 [overflow-wrap:anywhere] custom-scrollbar"
                          >{{ stringifyValue(event.data) }}</pre
                        >
                      </div>
                    </div>
                  </section>
                </div>
              </div>
            </aside>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

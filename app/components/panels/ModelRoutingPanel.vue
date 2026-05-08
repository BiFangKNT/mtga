<script setup lang="ts">
import type {
  FailoverPool,
  ModelRoutingTarget,
  ProviderId,
  PublishedModel,
} from "~/composables/mtgaTypes";

const store = useMtgaStore();

const targets = store.routingTargets;
const failoverPools = store.failoverPools;
const publishedModels = store.publishedModels;

const DEFAULT_MIDDLE_ROUTE = "/v1";
const GEMINI_DEFAULT_MIDDLE_ROUTE = "/v1beta";
const PROVIDER_OPTIONS: { label: string; value: ProviderId }[] = [
  { label: "OpenAI Chat Completion", value: "openai_chat_completion" },
  { label: "OpenAI Response", value: "openai_response" },
  { label: "Anthropic", value: "anthropic" },
  { label: "Gemini", value: "gemini" },
];
const PROVIDER_LABELS: Record<ProviderId, string> = {
  openai_chat_completion: "OpenAI Chat Completion",
  openai_response: "OpenAI Response",
  anthropic: "Anthropic",
  gemini: "Gemini",
};

const selectedTargetId = ref("");
const selectedPublishedName = ref("");
const selectedPoolId = ref("");
const editorOpen = ref(false);
const editorKind = ref<"target" | "published" | "pool">("target");
const editorMode = ref<"add" | "edit">("add");
const formError = ref("");
const saving = ref(false);
const refreshing = ref(false);
const targetTesting = ref(false);
const modelLoading = ref(false);
const availableModels = ref<string[]>([]);
const targetDiscoveryStrategy = ref("");
const targetDiscoveryScope = ref("");

const targetForm = reactive({
  id: "",
  display_name: "",
  provider: "openai_chat_completion" as ProviderId,
  api_base: "",
  upstream_model: "",
  api_key: "",
  middle_route: "",
  prompt_cache_enabled: false,
});

const publishedForm = reactive({
  name: "",
  enabled: true,
  primary_target_id: "",
  failover_pool_id: "",
});

const poolForm = reactive({
  id: "",
  trigger_statuses: "429",
  cooldown_seconds: 10,
  member_ids: [] as string[],
});

const selectedTarget = computed(() =>
  targets.value.find((target) => target.id === selectedTargetId.value),
);
const selectedPublishedModel = computed(() =>
  publishedModels.value.find((model) => model.name === selectedPublishedName.value),
);
const selectedPool = computed(() =>
  failoverPools.value.find((pool) => pool.id === selectedPoolId.value),
);

const targetOptions = computed(() =>
  targets.value.map((target) => ({
    label: `${target.display_name || target.id} · ${target.upstream_model}`,
    value: target.id,
  })),
);
const poolOptions = computed(() => [
  { label: "不启用故障转移", value: "" },
  ...failoverPools.value.map((pool) => ({ label: pool.id, value: pool.id })),
]);
const hasEnabledPublishedModel = computed(() =>
  publishedModels.value.some((model) => model.enabled),
);
const hasModelRoute = computed(() => targets.value.length > 0 && hasEnabledPublishedModel.value);
const routeWarnings = computed(() => {
  const messages: string[] = [];
  if (!targets.value.length) {
    messages.push("缺少目标");
  }
  if (!publishedModels.value.length) {
    messages.push("缺少发布模型");
  }
  if (publishedModels.value.length && !hasEnabledPublishedModel.value) {
    messages.push("没有启用的发布模型");
  }
  return messages;
});

const getTargetLabel = (targetId: string) => {
  const target = targets.value.find((item) => item.id === targetId);
  return target ? target.display_name || target.id : targetId || "-";
};
const isProviderId = (value: string | undefined): value is ProviderId =>
  value === "openai_chat_completion" ||
  value === "openai_response" ||
  value === "anthropic" ||
  value === "gemini";
const getProviderLabel = (provider?: string) =>
  isProviderId(provider) ? PROVIDER_LABELS[provider] : "OpenAI Chat Completion";
const getDefaultMiddleRoute = (provider: ProviderId) =>
  provider === "gemini" ? GEMINI_DEFAULT_MIDDLE_ROUTE : DEFAULT_MIDDLE_ROUTE;
const normalizeApiBase = (value: string) => value.trim().replace(/\/+$/, "");
const normalizeMiddleRoute = (value: string, provider: ProviderId) => {
  let route = value.trim() || getDefaultMiddleRoute(provider);
  if (!route.startsWith("/")) {
    route = `/${route}`;
  }
  return route.length > 1 ? route.replace(/\/+$/, "") : route;
};
const makeIdentifier = (prefix: string, used: Set<string>) => {
  let index = used.size + 1;
  let candidate = `${prefix}-${index}`;
  while (used.has(candidate)) {
    index += 1;
    candidate = `${prefix}-${index}`;
  }
  return candidate;
};
const buildDiscoveryScope = () =>
  JSON.stringify([
    targetForm.provider,
    normalizeApiBase(targetForm.api_base),
    targetForm.api_key.trim(),
    normalizeMiddleRoute(targetForm.middle_route, targetForm.provider),
  ]);
const resetTargetDiscovery = () => {
  availableModels.value = [];
  modelLoading.value = false;
  targetDiscoveryStrategy.value = "";
  targetDiscoveryScope.value = "";
};

const openTargetEditor = (mode: "add" | "edit") => {
  editorKind.value = "target";
  editorMode.value = mode;
  formError.value = "";
  resetTargetDiscovery();
  if (mode === "edit" && selectedTarget.value) {
    const target = selectedTarget.value;
    targetForm.id = target.id;
    targetForm.display_name = target.display_name;
    targetForm.provider = target.provider;
    targetForm.api_base = target.api_base;
    targetForm.upstream_model = target.upstream_model;
    targetForm.api_key = target.api_key;
    targetForm.middle_route = target.middle_route || "";
    targetForm.prompt_cache_enabled = target.prompt_cache_enabled === true;
    targetDiscoveryStrategy.value = target.model_discovery_strategy || "";
    targetDiscoveryScope.value = buildDiscoveryScope();
  } else {
    targetForm.id = makeIdentifier("target", new Set(targets.value.map((target) => target.id)));
    targetForm.display_name = "";
    targetForm.provider = "openai_chat_completion";
    targetForm.api_base = "";
    targetForm.upstream_model = "";
    targetForm.api_key = "";
    targetForm.middle_route = "";
    targetForm.prompt_cache_enabled = false;
  }
  editorOpen.value = true;
};

const openPublishedEditor = (mode: "add" | "edit") => {
  editorKind.value = "published";
  editorMode.value = mode;
  formError.value = "";
  if (mode === "edit" && selectedPublishedModel.value) {
    const model = selectedPublishedModel.value;
    publishedForm.name = model.name;
    publishedForm.enabled = model.enabled;
    publishedForm.primary_target_id = model.primary_target_id;
    publishedForm.failover_pool_id = model.failover_pool_id || "";
  } else {
    publishedForm.name = "";
    publishedForm.enabled = true;
    publishedForm.primary_target_id = selectedTargetId.value || targets.value[0]?.id || "";
    publishedForm.failover_pool_id = "";
  }
  editorOpen.value = true;
};

const openPoolEditor = (mode: "add" | "edit") => {
  editorKind.value = "pool";
  editorMode.value = mode;
  formError.value = "";
  if (mode === "edit" && selectedPool.value) {
    const pool = selectedPool.value;
    poolForm.id = pool.id;
    poolForm.trigger_statuses = pool.trigger_statuses.join(", ");
    poolForm.cooldown_seconds = pool.cooldown_seconds;
    poolForm.member_ids = pool.members.map((member) => member.target_id);
  } else {
    poolForm.id = makeIdentifier(
      "failover-pool",
      new Set(failoverPools.value.map((pool) => pool.id)),
    );
    poolForm.trigger_statuses = "429";
    poolForm.cooldown_seconds = 10;
    poolForm.member_ids = selectedTargetId.value ? [selectedTargetId.value] : [];
  }
  editorOpen.value = true;
};

const closeEditor = () => {
  editorOpen.value = false;
};

const persistConfig = async (successMessage: string) => {
  saving.value = true;
  try {
    const ok = await store.saveConfig();
    if (ok) {
      store.appendLog(successMessage);
      return true;
    }
    store.appendLog("保存模型路由失败");
    return false;
  } finally {
    saving.value = false;
  }
};

const saveTarget = async () => {
  const targetId = targetForm.id.trim();
  const apiBase = normalizeApiBase(targetForm.api_base);
  const upstreamModel = targetForm.upstream_model.trim();
  if (!targetId || !apiBase || !upstreamModel) {
    formError.value = "目标ID、API Base 和上游模型都是必填项";
    return;
  }
  if (
    targets.value.some(
      (target) =>
        target.id === targetId &&
        (editorMode.value === "add" || target.id !== selectedTargetId.value),
    )
  ) {
    formError.value = "目标ID已存在";
    return;
  }
  const target: ModelRoutingTarget = {
    id: targetId,
    display_name: targetForm.display_name.trim(),
    provider: targetForm.provider,
    api_base: apiBase,
    upstream_model: upstreamModel,
    api_key: targetForm.api_key.trim(),
    middle_route: normalizeMiddleRoute(targetForm.middle_route, targetForm.provider),
    prompt_cache_enabled: targetForm.prompt_cache_enabled,
  };
  if (targetDiscoveryStrategy.value && targetDiscoveryScope.value === buildDiscoveryScope()) {
    target.model_discovery_strategy = targetDiscoveryStrategy.value;
  }
  if (editorMode.value === "add") {
    targets.value.push(target);
  } else {
    const oldId = selectedTargetId.value;
    const index = targets.value.findIndex((item) => item.id === oldId);
    if (index >= 0) {
      targets.value[index] = target;
      if (oldId !== target.id) {
        publishedModels.value.forEach((model) => {
          if (model.primary_target_id === oldId) {
            model.primary_target_id = target.id;
          }
        });
        failoverPools.value.forEach((pool) => {
          pool.members.forEach((member) => {
            if (member.target_id === oldId) {
              member.target_id = target.id;
            }
          });
        });
      }
    }
  }
  selectedTargetId.value = target.id;
  if (await persistConfig(`已保存目标: ${target.display_name || target.id}`)) {
    closeEditor();
  }
};

const savePublishedModel = async () => {
  const name = publishedForm.name.trim();
  if (!name || !publishedForm.primary_target_id) {
    formError.value = "发布模型名称和主目标都是必填项";
    return;
  }
  if (
    publishedModels.value.some(
      (model) =>
        model.name === name &&
        (editorMode.value === "add" || model.name !== selectedPublishedName.value),
    )
  ) {
    formError.value = "发布模型名称已存在";
    return;
  }
  const model: PublishedModel = {
    name,
    enabled: publishedForm.enabled,
    primary_target_id: publishedForm.primary_target_id,
    failover_pool_id: publishedForm.failover_pool_id || null,
  };
  if (editorMode.value === "add") {
    publishedModels.value.push(model);
  } else {
    const index = publishedModels.value.findIndex(
      (item) => item.name === selectedPublishedName.value,
    );
    if (index >= 0) {
      publishedModels.value[index] = model;
    }
  }
  selectedPublishedName.value = model.name;
  if (await persistConfig(`已保存发布模型: ${model.name}`)) {
    closeEditor();
  }
};

const parseStatuses = (value: string) =>
  Array.from(
    new Set(
      value
        .split(",")
        .map((item) => Number(item.trim()))
        .filter((status) => Number.isInteger(status) && status > 0),
    ),
  );

const savePool = async () => {
  const poolId = poolForm.id.trim();
  const statuses = parseStatuses(poolForm.trigger_statuses);
  if (!poolId || !statuses.length) {
    formError.value = "故障池ID和触发状态码都是必填项";
    return;
  }
  if (
    failoverPools.value.some(
      (pool) =>
        pool.id === poolId && (editorMode.value === "add" || pool.id !== selectedPoolId.value),
    )
  ) {
    formError.value = "故障池ID已存在";
    return;
  }
  const pool: FailoverPool = {
    id: poolId,
    trigger_statuses: statuses,
    cooldown_seconds: Math.max(1, Number(poolForm.cooldown_seconds) || 10),
    members: poolForm.member_ids.map((target_id) => ({ target_id })),
  };
  if (editorMode.value === "add") {
    failoverPools.value.push(pool);
  } else {
    const oldId = selectedPoolId.value;
    const index = failoverPools.value.findIndex((item) => item.id === oldId);
    if (index >= 0) {
      failoverPools.value[index] = pool;
      if (oldId !== pool.id) {
        publishedModels.value.forEach((model) => {
          if (model.failover_pool_id === oldId) {
            model.failover_pool_id = pool.id;
          }
        });
      }
    }
  }
  selectedPoolId.value = pool.id;
  if (await persistConfig(`已保存故障池: ${pool.id}`)) {
    closeEditor();
  }
};

const handleEditorSave = () => {
  if (saving.value) {
    return;
  }
  if (editorKind.value === "target") {
    void saveTarget();
  } else if (editorKind.value === "published") {
    void savePublishedModel();
  } else {
    void savePool();
  }
};

const deleteSelectedTarget = async () => {
  const target = selectedTarget.value;
  if (!target || saving.value) {
    return;
  }
  if (publishedModels.value.some((model) => model.primary_target_id === target.id)) {
    store.appendLog("删除目标失败：仍有发布模型引用该目标");
    return;
  }
  targets.value = targets.value.filter((item) => item.id !== target.id);
  failoverPools.value.forEach((pool) => {
    pool.members = pool.members.filter((member) => member.target_id !== target.id);
  });
  selectedTargetId.value = targets.value[0]?.id || "";
  await persistConfig(`已删除目标: ${target.display_name || target.id}`);
};

const deleteSelectedPublished = async () => {
  const model = selectedPublishedModel.value;
  if (!model || saving.value) {
    return;
  }
  publishedModels.value = publishedModels.value.filter((item) => item.name !== model.name);
  selectedPublishedName.value = publishedModels.value[0]?.name || "";
  await persistConfig(`已删除发布模型: ${model.name}`);
};

const deleteSelectedPool = async () => {
  const pool = selectedPool.value;
  if (!pool || saving.value) {
    return;
  }
  publishedModels.value.forEach((model) => {
    if (model.failover_pool_id === pool.id) {
      model.failover_pool_id = null;
    }
  });
  failoverPools.value = failoverPools.value.filter((item) => item.id !== pool.id);
  selectedPoolId.value = failoverPools.value[0]?.id || "";
  await persistConfig(`已删除故障池: ${pool.id}`);
};

const refreshConfig = async () => {
  if (refreshing.value) {
    return;
  }
  refreshing.value = true;
  try {
    if (await store.loadConfig()) {
      store.appendLog("已刷新模型路由");
    }
  } finally {
    refreshing.value = false;
  }
};

const testSelectedTarget = async () => {
  const target = selectedTarget.value;
  if (!target || targetTesting.value) {
    return;
  }
  targetTesting.value = true;
  try {
    await store.runConfigGroupTest(-1, target.id);
  } finally {
    targetTesting.value = false;
  }
};

const fetchTargetModels = async () => {
  if (modelLoading.value) {
    return;
  }
  const apiBase = normalizeApiBase(targetForm.api_base);
  if (!apiBase) {
    store.appendLog("获取模型列表失败: API Base为空");
    return;
  }
  modelLoading.value = true;
  const requestPayload = {
    provider: targetForm.provider,
    api_url: apiBase,
    api_key: targetForm.api_key.trim(),
    model_id: targetForm.upstream_model.trim(),
    middle_route: normalizeMiddleRoute(targetForm.middle_route, targetForm.provider),
  };
  const result = await store.fetchConfigGroupModels(requestPayload);
  if (result) {
    availableModels.value = result.models;
    targetDiscoveryStrategy.value = result.strategyId || "";
    targetDiscoveryScope.value = buildDiscoveryScope();
  }
  modelLoading.value = false;
};

const togglePoolMember = (targetId: string, checked: boolean) => {
  const current = new Set(poolForm.member_ids);
  if (checked) {
    current.add(targetId);
  } else {
    current.delete(targetId);
  }
  poolForm.member_ids = Array.from(current);
};

watch(
  targets,
  (nextTargets) => {
    if (
      !selectedTargetId.value ||
      !nextTargets.some((target) => target.id === selectedTargetId.value)
    ) {
      selectedTargetId.value = nextTargets[0]?.id || "";
    }
  },
  { immediate: true, deep: true },
);

watch(
  publishedModels,
  (nextModels) => {
    if (
      !selectedPublishedName.value ||
      !nextModels.some((model) => model.name === selectedPublishedName.value)
    ) {
      selectedPublishedName.value = nextModels[0]?.name || "";
    }
  },
  { immediate: true, deep: true },
);

watch(
  failoverPools,
  (nextPools) => {
    if (!selectedPoolId.value || !nextPools.some((pool) => pool.id === selectedPoolId.value)) {
      selectedPoolId.value = nextPools[0]?.id || "";
    }
  },
  { immediate: true, deep: true },
);

watch(
  () => targetForm.provider,
  (provider, previous) => {
    if (!previous || targetForm.middle_route.trim() !== getDefaultMiddleRoute(previous)) {
      return;
    }
    targetForm.middle_route = getDefaultMiddleRoute(provider);
  },
);
</script>

<template>
  <div class="flex h-full min-h-0 flex-col gap-4">
    <div class="flex shrink-0 flex-wrap items-start justify-between gap-3">
      <div>
        <h2 class="mtga-card-title">模型路由</h2>
        <p class="mtga-card-subtitle">维护 MTGA 入站模型、上游目标与故障转移关系</p>
      </div>
      <div class="flex items-center gap-2">
        <span
          class="rounded-full border px-3 py-1 text-xs font-bold"
          :class="
            hasModelRoute
              ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
              : 'border-amber-200 bg-amber-50 text-amber-700'
          "
        >
          {{ hasModelRoute ? "可启动" : routeWarnings.join(" / ") || "待配置" }}
        </span>
        <button
          class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
          :class="refreshing ? 'loading' : ''"
          :disabled="refreshing || saving"
          @click="refreshConfig"
        >
          刷新
        </button>
      </div>
    </div>

    <div class="grid shrink-0 gap-3 lg:grid-cols-[minmax(0,1fr),260px]">
      <div class="mtga-soft-panel bg-white/40">
        <div class="grid gap-3 md:grid-cols-[minmax(0,1fr),260px]">
          <MtgaInput
            v-model="store.mtgaAuthKey.value"
            label="MTGA Auth Key"
            placeholder="为空则不鉴权"
            type="password"
            description="只用于 MTGA 入站鉴权；上游 API Key 在目标中维护"
            :clearable="true"
          />
          <MtgaInput
            v-model="store.promptCacheBucketId.value"
            label="Prompt Cache Bucket"
            placeholder="自动生成或留空"
            description="用于 prompt cache 隔离"
            :clearable="true"
          />
        </div>
      </div>
      <div class="flex items-end">
        <button
          class="btn btn-primary btn-sm w-full rounded-xl"
          :class="saving ? 'loading' : ''"
          :disabled="saving"
          @click="persistConfig('模型路由已保存')"
        >
          保存路由
        </button>
      </div>
    </div>

    <div class="grid min-h-0 flex-1 gap-4 xl:grid-cols-[minmax(0,1.1fr),minmax(0,1fr)]">
      <section class="flex min-h-0 flex-col">
        <div class="mb-2 flex items-center justify-between gap-2">
          <div>
            <h3 class="text-sm font-bold text-slate-800">Targets</h3>
            <p class="text-xs text-slate-500">上游 provider、base URL、模型与 API Key</p>
          </div>
          <div class="flex gap-2">
            <button class="btn btn-xs btn-outline rounded-lg" @click="openTargetEditor('add')">
              新增
            </button>
            <button
              class="btn btn-xs btn-outline rounded-lg"
              :disabled="!selectedTarget"
              @click="openTargetEditor('edit')"
            >
              修改
            </button>
            <button
              class="btn btn-xs btn-outline rounded-lg border-rose-200 text-rose-600 hover:bg-rose-50"
              :disabled="!selectedTarget || saving"
              @click="deleteSelectedTarget"
            >
              删除
            </button>
          </div>
        </div>

        <div
          class="min-h-0 overflow-auto rounded-xl border border-slate-200/70 bg-white/50 custom-scrollbar"
        >
          <table class="table table-sm w-full text-sm">
            <thead class="sticky top-0 z-10 bg-slate-50/90">
              <tr>
                <th>ID</th>
                <th>名称</th>
                <th>Provider</th>
                <th>上游模型</th>
                <th>API Base</th>
              </tr>
            </thead>
            <tbody v-if="targets.length">
              <tr
                v-for="target in targets"
                :key="target.id"
                class="cursor-pointer hover:bg-amber-50/50"
                :class="selectedTargetId === target.id ? 'bg-amber-100/70' : ''"
                @click="selectedTargetId = target.id"
              >
                <td class="max-w-[120px] truncate font-mono text-xs">{{ target.id }}</td>
                <td class="max-w-[150px] truncate">{{ target.display_name || "-" }}</td>
                <td class="max-w-[160px] truncate">{{ getProviderLabel(target.provider) }}</td>
                <td class="max-w-[160px] truncate font-mono text-xs">
                  {{ target.upstream_model }}
                </td>
                <td class="max-w-[220px] truncate font-mono text-xs">{{ target.api_base }}</td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="5" class="py-6 text-center text-sm text-slate-400">暂无目标</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-3 flex justify-end">
          <button
            class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
            :class="targetTesting ? 'loading' : ''"
            :disabled="!selectedTarget || targetTesting"
            @click="testSelectedTarget"
          >
            测活选中目标
          </button>
        </div>
      </section>

      <div class="grid min-h-0 gap-4 lg:grid-rows-[minmax(0,1fr),minmax(0,0.9fr)]">
        <section class="flex min-h-0 flex-col">
          <div class="mb-2 flex items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold text-slate-800">Published Models</h3>
              <p class="text-xs text-slate-500">暴露给下游 `/models` 与请求体 `model` 的名称</p>
            </div>
            <div class="flex gap-2">
              <button
                class="btn btn-xs btn-outline rounded-lg"
                :disabled="!targets.length"
                @click="openPublishedEditor('add')"
              >
                新增
              </button>
              <button
                class="btn btn-xs btn-outline rounded-lg"
                :disabled="!selectedPublishedModel"
                @click="openPublishedEditor('edit')"
              >
                修改
              </button>
              <button
                class="btn btn-xs btn-outline rounded-lg border-rose-200 text-rose-600 hover:bg-rose-50"
                :disabled="!selectedPublishedModel || saving"
                @click="deleteSelectedPublished"
              >
                删除
              </button>
            </div>
          </div>

          <div
            class="min-h-0 overflow-auto rounded-xl border border-slate-200/70 bg-white/50 custom-scrollbar"
          >
            <table class="table table-sm w-full text-sm">
              <thead class="sticky top-0 z-10 bg-slate-50/90">
                <tr>
                  <th>发布名</th>
                  <th>主目标</th>
                  <th>故障池</th>
                  <th>状态</th>
                </tr>
              </thead>
              <tbody v-if="publishedModels.length">
                <tr
                  v-for="model in publishedModels"
                  :key="model.name"
                  class="cursor-pointer hover:bg-amber-50/50"
                  :class="selectedPublishedName === model.name ? 'bg-amber-100/70' : ''"
                  @click="selectedPublishedName = model.name"
                >
                  <td class="max-w-[170px] truncate font-mono text-xs">{{ model.name }}</td>
                  <td class="max-w-[140px] truncate">
                    {{ getTargetLabel(model.primary_target_id) }}
                  </td>
                  <td class="max-w-[120px] truncate font-mono text-xs">
                    {{ model.failover_pool_id || "-" }}
                  </td>
                  <td>
                    <span
                      class="rounded-full border px-2 py-0.5 text-[11px] font-bold"
                      :class="
                        model.enabled
                          ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                          : 'border-slate-200 bg-slate-100 text-slate-500'
                      "
                    >
                      {{ model.enabled ? "启用" : "停用" }}
                    </span>
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="4" class="py-6 text-center text-sm text-slate-400">暂无发布模型</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section class="flex min-h-0 flex-col">
          <div class="mb-2 flex items-center justify-between gap-2">
            <div>
              <h3 class="text-sm font-bold text-slate-800">Failover Pools</h3>
              <p class="text-xs text-slate-500">429 冷却与网络重试耗尽后的候选目标</p>
            </div>
            <div class="flex gap-2">
              <button
                class="btn btn-xs btn-outline rounded-lg"
                :disabled="!targets.length"
                @click="openPoolEditor('add')"
              >
                新增
              </button>
              <button
                class="btn btn-xs btn-outline rounded-lg"
                :disabled="!selectedPool"
                @click="openPoolEditor('edit')"
              >
                修改
              </button>
              <button
                class="btn btn-xs btn-outline rounded-lg border-rose-200 text-rose-600 hover:bg-rose-50"
                :disabled="!selectedPool || saving"
                @click="deleteSelectedPool"
              >
                删除
              </button>
            </div>
          </div>

          <div
            class="min-h-0 overflow-auto rounded-xl border border-slate-200/70 bg-white/50 custom-scrollbar"
          >
            <table class="table table-sm w-full text-sm">
              <thead class="sticky top-0 z-10 bg-slate-50/90">
                <tr>
                  <th>ID</th>
                  <th>状态码</th>
                  <th>冷却</th>
                  <th>成员</th>
                </tr>
              </thead>
              <tbody v-if="failoverPools.length">
                <tr
                  v-for="pool in failoverPools"
                  :key="pool.id"
                  class="cursor-pointer hover:bg-amber-50/50"
                  :class="selectedPoolId === pool.id ? 'bg-amber-100/70' : ''"
                  @click="selectedPoolId = pool.id"
                >
                  <td class="max-w-[140px] truncate font-mono text-xs">{{ pool.id }}</td>
                  <td class="font-mono text-xs">{{ pool.trigger_statuses.join(", ") }}</td>
                  <td>{{ pool.cooldown_seconds }}s</td>
                  <td class="max-w-[180px] truncate">
                    {{
                      pool.members.map((member) => getTargetLabel(member.target_id)).join(", ") ||
                      "-"
                    }}
                  </td>
                </tr>
              </tbody>
              <tbody v-else>
                <tr>
                  <td colspan="4" class="py-6 text-center text-sm text-slate-400">暂无故障池</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>

    <MtgaDialog v-model:open="editorOpen" max-width="max-w-2xl" @close="closeEditor">
      <template #header>
        <div class="flex items-center justify-between gap-3">
          <div>
            <h3 class="text-lg font-semibold text-slate-900">
              {{
                editorKind === "target"
                  ? editorMode === "add"
                    ? "新增目标"
                    : "修改目标"
                  : editorKind === "published"
                    ? editorMode === "add"
                      ? "新增发布模型"
                      : "修改发布模型"
                    : editorMode === "add"
                      ? "新增故障池"
                      : "修改故障池"
              }}
            </h3>
            <p class="text-xs text-slate-500">保存后写入 v2.6.0 模型路由配置</p>
          </div>
          <span class="mtga-chip">v2.6.0</span>
        </div>
      </template>

      <div class="px-6 py-6">
        <div v-if="editorKind === 'target'" class="grid gap-4 md:grid-cols-2">
          <MtgaInput v-model="targetForm.id" label="Target ID" required placeholder="target-1" />
          <MtgaInput
            v-model="targetForm.display_name"
            label="显示名称"
            placeholder="Claude 主线路"
          />
          <MtgaSelect
            v-model="targetForm.provider"
            label="Provider"
            required
            :options="PROVIDER_OPTIONS"
            class="w-full"
          />
          <MtgaInput
            v-model="targetForm.api_base"
            label="API Base"
            required
            placeholder="https://api.openai.com"
          />
          <MtgaInput
            v-model="targetForm.upstream_model"
            label="上游模型"
            required
            show-dropdown
            :options="availableModels"
            :loading="modelLoading"
            placeholder="gpt-5"
            @dropdown="fetchTargetModels"
          />
          <MtgaInput
            v-model="targetForm.api_key"
            label="API Key"
            type="password"
            placeholder="sk-..."
          />
          <MtgaInput
            v-model="targetForm.middle_route"
            label="Middle Route"
            :placeholder="getDefaultMiddleRoute(targetForm.provider)"
          />
          <label class="mt-7 flex cursor-pointer items-center gap-2">
            <input
              v-model="targetForm.prompt_cache_enabled"
              type="checkbox"
              class="checkbox checkbox-primary checkbox-sm"
            />
            <span class="label-text text-sm font-medium text-slate-700">启用提示缓存</span>
          </label>
        </div>

        <div v-else-if="editorKind === 'published'" class="grid gap-4 md:grid-cols-2">
          <MtgaInput
            v-model="publishedForm.name"
            label="发布模型名称"
            required
            placeholder="gpt-5"
          />
          <MtgaSelect
            v-model="publishedForm.primary_target_id"
            label="主目标"
            required
            :options="targetOptions"
            class="w-full"
          />
          <MtgaSelect
            v-model="publishedForm.failover_pool_id"
            label="故障转移池"
            :options="poolOptions"
            class="w-full"
          />
          <label class="mt-7 flex cursor-pointer items-center gap-2">
            <input
              v-model="publishedForm.enabled"
              type="checkbox"
              class="checkbox checkbox-primary checkbox-sm"
            />
            <span class="label-text text-sm font-medium text-slate-700">在 `/models` 中启用</span>
          </label>
        </div>

        <div v-else class="space-y-4">
          <div class="grid gap-4 md:grid-cols-3">
            <MtgaInput
              v-model="poolForm.id"
              label="Pool ID"
              required
              placeholder="failover-pool-1"
            />
            <MtgaInput
              v-model="poolForm.trigger_statuses"
              label="触发状态码"
              required
              placeholder="429"
            />
            <MtgaInput
              v-model="poolForm.cooldown_seconds"
              label="冷却秒数"
              type="number"
              required
              placeholder="10"
            />
          </div>
          <div>
            <div class="mb-2 text-sm font-medium text-slate-600">成员目标</div>
            <div class="grid gap-2 sm:grid-cols-2">
              <label
                v-for="target in targets"
                :key="target.id"
                class="flex cursor-pointer items-center gap-2 rounded-lg border border-slate-200 bg-white/50 px-3 py-2 text-sm"
              >
                <input
                  type="checkbox"
                  class="checkbox checkbox-primary checkbox-sm"
                  :checked="poolForm.member_ids.includes(target.id)"
                  @change="togglePoolMember(target.id, ($event.target as HTMLInputElement).checked)"
                />
                <span class="min-w-0 truncate">{{ target.display_name || target.id }}</span>
              </label>
            </div>
          </div>
        </div>

        <div v-if="formError" class="alert alert-error mt-4 rounded-xl px-3 py-2 text-xs">
          {{ formError }}
        </div>
      </div>

      <template #footer>
        <button class="mtga-btn-dialog-ghost flex-1" @click="closeEditor">取消</button>
        <button
          class="mtga-btn-dialog-primary flex-1"
          :class="saving ? 'loading' : ''"
          :disabled="saving"
          @click="handleEditorSave"
        >
          保存
        </button>
      </template>
    </MtgaDialog>
  </div>
</template>

<script setup lang="ts">
import type { ConfigGroup, ProviderId } from "~/composables/mtgaTypes";

const store = useMtgaStore();
const configGroups = store.configGroups;
const currentIndex = store.currentConfigIndex;

const DEFAULT_MIDDLE_ROUTE = "/v1";
const GEMINI_DEFAULT_MIDDLE_ROUTE = "/v1beta";

const editorOpen = ref(false);
const editorMode = ref<"add" | "edit">("add");
const formError = ref("");
const middleRouteEnabled = ref(false);
const availableModels = ref<string[]>([]);
const modelLoading = ref(false);
const formModelDiscoveryStrategy = ref("");
const formModelDiscoveryScope = ref("");

const confirmOpen = ref(false);
const confirmTitle = ref("确认删除");
const confirmMessage = ref("");
const pendingDeleteIndex = ref<number | null>(null);
const pendingSwitchIndex = ref<number | null>(null);
const switchInProgress = ref(false);
const refreshInProgress = ref(false);
const testInProgress = ref(false);
const saveInProgress = ref(false);
const deleteInProgress = ref(false);
const reorderInProgress = ref(false);

const form = reactive({
  name: "",
  provider: "openai_chat_completion" as ProviderId,
  api_url: "",
  model_id: "",
  api_key: "",
  middle_route: "",
  prompt_cache_enabled: false,
});

const PROVIDER_LABELS: Record<ProviderId, string> = {
  openai_chat_completion: "OpenAI Chat Completion",
  openai_response: "OpenAI Response",
  anthropic: "Anthropic",
  gemini: "Gemini",
};

const normalizeProvider = (provider?: string): ProviderId => {
  if (
    provider === "openai_chat_completion" ||
    provider === "openai_response" ||
    provider === "anthropic" ||
    provider === "gemini"
  ) {
    return provider;
  }
  return "openai_chat_completion";
};

const getProviderLabel = (provider?: string) => PROVIDER_LABELS[normalizeProvider(provider)];

const normalizeApiUrl = (value: string) => value.trim().replace(/\/+$/, "");

const getDefaultMiddleRoute = (provider: ProviderId) =>
  provider === "gemini" ? GEMINI_DEFAULT_MIDDLE_ROUTE : DEFAULT_MIDDLE_ROUTE;

const supportsModelDiscovery = (_provider: ProviderId) => true;

const testTooltip = [
  "测试选中配置组的实际对话功能",
  "会发送最小请求并消耗少量tokens",
  "请确保配置正确后使用",
].join("\n");

const refreshTooltip = ["重新加载配置文件中的配置组", "用于同步外部修改或恢复意外更改"].join("\n");

const selectedIndex = computed({
  get: () => (configGroups.value.length ? currentIndex.value : -1),
  set: (value) => {
    if (value < 0 || value >= configGroups.value.length) {
      return;
    }
    if (value === currentIndex.value && pendingSwitchIndex.value === null) {
      return;
    }
    currentIndex.value = value;
    pendingSwitchIndex.value = value;
    void processConfigSwitch();
  },
});

const processConfigSwitch = async () => {
  if (switchInProgress.value) {
    return;
  }
  switchInProgress.value = true;
  try {
    while (pendingSwitchIndex.value !== null) {
      const targetIndex = pendingSwitchIndex.value;
      pendingSwitchIndex.value = null;
      currentIndex.value = targetIndex;

      const saved = await store.saveConfig();
      if (!saved) {
        store.appendLog("保存配置组失败");
        continue;
      }

      // 若有新的切换请求，跳过当前热应用，直接处理最新选择。
      if (pendingSwitchIndex.value !== null) {
        continue;
      }
      await store.runProxyApplyCurrentConfig();
    }
  } finally {
    switchInProgress.value = false;
  }
};

const hasSelection = computed(
  () =>
    configGroups.value.length > 0 &&
    selectedIndex.value >= 0 &&
    selectedIndex.value < configGroups.value.length,
);

const panelActionBusy = computed(
  () =>
    switchInProgress.value ||
    saveInProgress.value ||
    deleteInProgress.value ||
    reorderInProgress.value,
);

const normalizeMiddleRoute = (value: string, provider: ProviderId = form.provider) => {
  let raw = value.trim();
  if (!raw) {
    raw = getDefaultMiddleRoute(provider);
  }
  if (!raw.startsWith("/")) {
    raw = `/${raw}`;
  }
  if (raw.length > 1) {
    raw = raw.replace(/\/+$/, "");
    if (!raw) {
      raw = "/";
    }
  }
  return raw;
};

const buildModelDiscoveryScope = (payload: {
  provider?: string;
  api_url: string;
  api_key?: string;
  middle_route?: string;
}) => {
  const provider = normalizeProvider(payload.provider);
  return JSON.stringify([
    provider,
    normalizeApiUrl(payload.api_url),
    (payload.api_key || "").trim(),
    normalizeMiddleRoute(payload.middle_route || "", provider),
  ]);
};

const setFormModelDiscoveryState = (
  strategyId: string | null | undefined,
  payload?: {
    provider?: string;
    api_url: string;
    api_key?: string;
    middle_route?: string;
  },
) => {
  const normalizedStrategyId = (strategyId || "").trim();
  if (!normalizedStrategyId || !payload) {
    formModelDiscoveryStrategy.value = "";
    formModelDiscoveryScope.value = "";
    return;
  }
  formModelDiscoveryStrategy.value = normalizedStrategyId;
  formModelDiscoveryScope.value = buildModelDiscoveryScope(payload);
};

const isProviderDefaultMiddleRoute = (value: string, provider: ProviderId) =>
  normalizeMiddleRoute(value, provider) === getDefaultMiddleRoute(provider);

watch(
  () => form.provider,
  (provider, previousProvider) => {
    if (!middleRouteEnabled.value || !previousProvider) {
      return;
    }

    const rawMiddleRoute = form.middle_route.trim();
    if (!rawMiddleRoute) {
      form.middle_route = getDefaultMiddleRoute(provider);
      return;
    }

    if (isProviderDefaultMiddleRoute(rawMiddleRoute, previousProvider)) {
      form.middle_route = getDefaultMiddleRoute(provider);
    }
  },
);

const getDisplayName = (group: ConfigGroup, index: number) =>
  group.name?.trim() || `配置组 ${index + 1}`;

const refreshList = async () => {
  if (refreshInProgress.value) {
    return;
  }
  refreshInProgress.value = true;
  try {
    const ok = await store.loadConfig();
    if (ok) {
      store.appendLog("已刷新配置组列表");
    }
  } finally {
    refreshInProgress.value = false;
  }
};

const requestTest = async () => {
  if (testInProgress.value) {
    return;
  }
  if (!hasSelection.value) {
    store.appendLog("请先选择要测活的配置组");
    return;
  }
  testInProgress.value = true;
  try {
    await store.runConfigGroupTest(selectedIndex.value);
  } finally {
    testInProgress.value = false;
  }
};

const resetForm = () => {
  form.name = "";
  form.provider = "openai_chat_completion";
  form.api_url = "";
  form.model_id = "";
  form.api_key = "";
  form.middle_route = "";
  form.prompt_cache_enabled = false;
  middleRouteEnabled.value = false;
  formError.value = "";
  availableModels.value = [];
  modelLoading.value = false;
  setFormModelDiscoveryState(undefined);
};

const openAdd = () => {
  editorMode.value = "add";
  resetForm();
  editorOpen.value = true;
};

const openEdit = () => {
  if (!hasSelection.value) {
    store.appendLog("请先选择要修改的配置组");
    return;
  }
  editorMode.value = "edit";
  const group = configGroups.value[selectedIndex.value];
  if (!group) {
    return;
  }
  form.name = group.name || "";
  form.provider = normalizeProvider(group.provider);
  form.api_url = group.api_url || "";
  form.model_id = group.model_id || "";
  form.api_key = group.api_key || "";
  form.middle_route = group.middle_route || "";
  form.prompt_cache_enabled = group.prompt_cache_enabled ?? false;
  middleRouteEnabled.value = Boolean(group.middle_route);
  formError.value = "";
  availableModels.value = [];
  setFormModelDiscoveryState(group.model_discovery_strategy, {
    provider: group.provider,
    api_url: group.api_url || "",
    api_key: group.api_key || "",
    middle_route: group.middle_route || "",
  });
  editorOpen.value = true;
};

const closeEditor = () => {
  editorOpen.value = false;
};

const hasDuplicateConfigGroup = (payload: ConfigGroup, ignoredIndex: number | null = null) =>
  // v2.4.0 仍保留“同一 upstream 下允许配置多个不同实际模型”的现有语义。
  configGroups.value.some((group, index) => {
    if (ignoredIndex !== null && index === ignoredIndex) {
      return false;
    }
    return (
      normalizeProvider(group.provider) === normalizeProvider(payload.provider) &&
      normalizeApiUrl(group.api_url || "") === normalizeApiUrl(payload.api_url) &&
      (group.model_id || "").trim() === payload.model_id &&
      (group.api_key || "").trim() === payload.api_key &&
      normalizeMiddleRoute(group.middle_route || "", normalizeProvider(group.provider)) ===
        normalizeMiddleRoute(payload.middle_route || "", normalizeProvider(payload.provider))
    );
  });

const handleSave = async () => {
  if (saveInProgress.value) {
    return;
  }
  const payload: ConfigGroup = {
    name: form.name.trim(),
    provider: form.provider,
    api_url: normalizeApiUrl(form.api_url),
    model_id: form.model_id.trim(),
    api_key: form.api_key.trim(),
    prompt_cache_enabled: form.prompt_cache_enabled,
  };

  if (!payload.api_url || !payload.model_id || !payload.api_key) {
    formError.value = "API URL、实际模型ID 和 API Key 都是必填项";
    store.appendLog("错误: API URL、实际模型ID和API Key都是必填项");
    return;
  }

  if (middleRouteEnabled.value && form.middle_route.trim()) {
    payload.middle_route = normalizeMiddleRoute(form.middle_route, form.provider);
  } else {
    delete payload.middle_route;
  }

  if (
    formModelDiscoveryStrategy.value &&
    formModelDiscoveryScope.value === buildModelDiscoveryScope(payload)
  ) {
    payload.model_discovery_strategy = formModelDiscoveryStrategy.value;
  } else {
    delete payload.model_discovery_strategy;
  }

  const editingIndex =
    editorMode.value === "edit" && hasSelection.value ? selectedIndex.value : null;
  if (hasDuplicateConfigGroup(payload, editingIndex)) {
    formError.value = "相同 provider、API URL、实际模型ID、API Key 和中间路由的配置组已存在";
    store.appendLog("错误: 相同 provider、API URL、实际模型ID、API Key 和中间路由的配置组已存在");
    return;
  }

  if (editorMode.value === "add") {
    configGroups.value.push(payload);
    currentIndex.value = configGroups.value.length - 1;
  } else if (hasSelection.value) {
    configGroups.value.splice(selectedIndex.value, 1, payload);
  }

  saveInProgress.value = true;
  try {
    const ok = await store.saveConfig();
    if (ok) {
      const displayName = getDisplayName(payload, selectedIndex.value);
      store.appendLog(
        editorMode.value === "add"
          ? `已添加配置组: ${displayName}`
          : `已修改配置组: ${displayName}`,
      );
      closeEditor();
    } else {
      store.appendLog("保存配置组失败");
    }
  } finally {
    saveInProgress.value = false;
  }
};

const handleFetchModels = async () => {
  if (modelLoading.value) {
    return;
  }
  const apiUrl = form.api_url.trim();
  if (!apiUrl) {
    store.appendLog("获取模型列表失败: API URL为空");
    return;
  }
  if (!supportsModelDiscovery(form.provider)) {
    store.appendLog("当前提供商不支持通过 /models 自动发现模型，请直接手填实际模型ID");
    return;
  }
  modelLoading.value = true;
  const requestPayload = {
    provider: form.provider,
    api_url: apiUrl,
    api_key: form.api_key.trim(),
    model_id: form.model_id.trim(),
    middle_route: middleRouteEnabled.value
      ? normalizeMiddleRoute(form.middle_route, form.provider)
      : "",
  };
  const result = await store.fetchConfigGroupModels(requestPayload);
  if (result !== null) {
    availableModels.value = result.models;
    setFormModelDiscoveryState(result.strategyId, requestPayload);
  }
  modelLoading.value = false;
};

const requestDelete = () => {
  if (!hasSelection.value) {
    store.appendLog("请先选择要删除的配置组");
    return;
  }
  if (configGroups.value.length <= 1) {
    store.appendLog("至少需要保留一个配置组");
    return;
  }
  const group = configGroups.value[selectedIndex.value];
  if (!group) {
    return;
  }
  pendingDeleteIndex.value = selectedIndex.value;
  confirmTitle.value = "确认删除";
  confirmMessage.value = `确定要删除配置组 “${getDisplayName(group, selectedIndex.value)}” 吗？`;
  confirmOpen.value = true;
};

const cancelDelete = () => {
  confirmOpen.value = false;
  pendingDeleteIndex.value = null;
};

const confirmDelete = async () => {
  if (deleteInProgress.value) {
    return;
  }
  if (pendingDeleteIndex.value == null) {
    return;
  }
  deleteInProgress.value = true;
  try {
    const index = pendingDeleteIndex.value;
    const group = configGroups.value[index];
    if (!group) {
      store.appendLog("配置组不存在，已取消删除");
      confirmOpen.value = false;
      pendingDeleteIndex.value = null;
      return;
    }
    configGroups.value.splice(index, 1);
    if (currentIndex.value >= configGroups.value.length) {
      currentIndex.value = Math.max(configGroups.value.length - 1, 0);
    } else if (currentIndex.value > index) {
      currentIndex.value -= 1;
    }
    const ok = await store.saveConfig();
    if (ok) {
      store.appendLog(`已删除配置组: ${getDisplayName(group, index)}`);
    } else {
      store.appendLog("保存配置组失败");
    }
    confirmOpen.value = false;
    pendingDeleteIndex.value = null;
  } finally {
    deleteInProgress.value = false;
  }
};

const moveUp = async () => {
  if (reorderInProgress.value) {
    return;
  }
  if (!hasSelection.value || selectedIndex.value <= 0) {
    return;
  }
  const index = selectedIndex.value;
  const current = configGroups.value[index];
  const prev = configGroups.value[index - 1];
  if (!current || !prev) {
    return;
  }
  reorderInProgress.value = true;
  try {
    configGroups.value[index - 1] = current;
    configGroups.value[index] = prev;
    currentIndex.value = index - 1;
    await store.saveConfig();
  } finally {
    reorderInProgress.value = false;
  }
};

const moveDown = async () => {
  if (reorderInProgress.value) {
    return;
  }
  if (!hasSelection.value || selectedIndex.value >= configGroups.value.length - 1) {
    return;
  }
  const index = selectedIndex.value;
  const current = configGroups.value[index];
  const next = configGroups.value[index + 1];
  if (!current || !next) {
    return;
  }
  reorderInProgress.value = true;
  try {
    configGroups.value[index + 1] = current;
    configGroups.value[index] = next;
    currentIndex.value = index + 1;
    await store.saveConfig();
  } finally {
    reorderInProgress.value = false;
  }
};
</script>

<template>
  <div class="flex flex-wrap items-start justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">代理服务器配置组</h2>
      <p class="mtga-card-subtitle">管理模型路由与鉴权组合</p>
    </div>
    <div class="flex items-center gap-2">
      <button
        class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600 tooltip mtga-tooltip"
        :class="testInProgress ? 'loading' : ''"
        :disabled="testInProgress || panelActionBusy"
        :data-tip="testTooltip"
        style="--mtga-tooltip-max: 250px"
        @click="requestTest"
      >
        测活
      </button>
      <button
        class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600 tooltip mtga-tooltip"
        :class="refreshInProgress ? 'loading' : ''"
        :disabled="refreshInProgress || panelActionBusy"
        :data-tip="refreshTooltip"
        style="--mtga-tooltip-max: 250px"
        @click="refreshList"
      >
        刷新
      </button>
    </div>
  </div>

  <div class="mt-4 grid gap-4 lg:grid-cols-[1fr,180px]">
    <div
      class="min-w-0 rounded-xl border border-slate-200/70 bg-white/50 backdrop-blur-md overflow-hidden flex flex-col"
      style="--row-h: 36px; --head-h: 38px"
    >
      <div class="overflow-auto custom-scrollbar flex-1 max-h-[260px]">
        <table class="table table-sm w-full text-sm border-separate border-spacing-0">
          <thead class="sticky top-0 z-10 bg-slate-50/70 backdrop-blur-md">
            <tr style="height: var(--head-h)">
              <th class="w-16 text-center border-b border-slate-200/60">序号</th>
              <th class="min-w-[60px] border-b border-slate-200/60">名称</th>
              <th class="min-w-[100px] border-b border-slate-200/60">提供商</th>
              <th class="min-w-[140px] border-b border-slate-200/60">API URL</th>
              <th class="min-w-[120px] border-b border-slate-200/60">实际模型ID</th>
            </tr>
          </thead>
          <tbody v-if="configGroups.length">
            <tr
              v-for="(group, index) in configGroups"
              :key="index"
              class="cursor-pointer transition-colors hover:bg-amber-100/30 group"
              :class="selectedIndex === index ? 'bg-amber-100/70' : ''"
              :style="{ height: 'var(--row-h)' }"
              :title="group.name || ''"
              @click="selectedIndex = index"
            >
              <td
                class="w-16 border-l-4 text-center transition-all"
                :class="
                  selectedIndex === index
                    ? 'border-amber-400 text-slate-900'
                    : 'border-transparent text-slate-600'
                "
              >
                {{ index + 1 }}
              </td>
              <td
                class="truncate max-w-[128px] text-slate-700 transition-all"
                :class="selectedIndex === index ? 'border-amber-400' : 'border-transparent'"
              >
                {{ getDisplayName(group, index) }}
              </td>
              <td
                class="truncate max-w-[170px] text-slate-700 transition-all"
                :class="selectedIndex === index ? 'border-amber-400' : 'border-transparent'"
              >
                {{ getProviderLabel(group.provider) }}
              </td>
              <td
                class="truncate max-w-[200px] text-slate-700 transition-all"
                :class="selectedIndex === index ? 'border-amber-400' : 'border-transparent'"
              >
                {{ group.api_url || "(未填写)" }}
              </td>
              <td
                class="truncate max-w-[150px] text-slate-700 transition-all"
                :class="selectedIndex === index ? 'border-amber-400' : 'border-transparent'"
              >
                {{ group.model_id || "(未填写)" }}
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="5" class="py-6 text-center text-sm text-slate-400">暂无配置组</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="space-y-2">
      <button class="mtga-btn-primary" :disabled="panelActionBusy" @click="openAdd">新增</button>
      <button class="mtga-btn-outline" :disabled="panelActionBusy" @click="openEdit">修改</button>
      <button
        class="mtga-btn-error"
        :class="deleteInProgress ? 'loading' : ''"
        :disabled="panelActionBusy"
        @click="requestDelete"
      >
        删除
      </button>
      <div class="h-px bg-slate-200/70 mx-1"></div>
      <button
        class="mtga-btn-outline"
        :class="reorderInProgress ? 'loading' : ''"
        :disabled="reorderInProgress || !hasSelection || selectedIndex <= 0"
        @click="moveUp"
      >
        上移
      </button>
      <button
        class="mtga-btn-outline"
        :class="reorderInProgress ? 'loading' : ''"
        :disabled="reorderInProgress || !hasSelection || selectedIndex >= configGroups.length - 1"
        @click="moveDown"
      >
        下移
      </button>
    </div>
  </div>

  <ConfigGroupEditorDialog
    v-model:open="editorOpen"
    v-model:name="form.name"
    v-model:provider="form.provider"
    v-model:api-url="form.api_url"
    v-model:model-id="form.model_id"
    v-model:api-key="form.api_key"
    v-model:middle-route="form.middle_route"
    v-model:middle-route-enabled="middleRouteEnabled"
    v-model:prompt-cache-enabled="form.prompt_cache_enabled"
    :mode="editorMode"
    :form-error="formError"
    :default-middle-route="getDefaultMiddleRoute(form.provider)"
    :available-models="availableModels"
    :model-loading="modelLoading"
    :saving="saveInProgress"
    @fetch-models="handleFetchModels"
    @save="handleSave"
    @cancel="closeEditor"
  />

  <ConfirmDialog
    :open="confirmOpen"
    :title="confirmTitle"
    :message="confirmMessage"
    type="error"
    @cancel="cancelDelete"
    @confirm="confirmDelete"
  />
</template>

<script setup lang="ts">
/**
 * 设置面板组件
 * 提供用户数据管理、备份、还原及清理功能
 */
import type { ProxyMode } from "~/composables/mtgaTypes";
import {
  type ThemeConfig,
  DEFAULT_THEME_CONFIG,
  applyThemeConfig,
  copyThemeConfig,
  loadThemeFromStorage,
  sanitizeThemeConfig,
  saveThemeToStorage,
} from "~/composables/themeConfig";

const store = useMtgaStore();
const appInfo = store.appInfo;

const clearConfirmOpen = ref(false);
const clearConfirmTitle = "确认清除数据";
const clearConfirmMessage =
  "确定要清除用户数据吗？该操作将删除配置文件、SSL 证书和 hosts 备份（历史 backups 保留）。";
const proxyModeSwitchConfirmOpen = ref(false);
const currentProxyModeForConfirm = ref<ProxyMode | null>(null);
const themeDialogOpen = ref(false);
const proxySettingsSaving = ref(false);
const traePathBrowsing = ref(false);

const themeConfig = reactive<ThemeConfig>({ ...DEFAULT_THEME_CONFIG });
if (import.meta.client) {
  const savedTheme = loadThemeFromStorage();
  if (savedTheme) {
    copyThemeConfig(themeConfig, savedTheme);
  }
}

const proxyMode = computed({
  get: () => store.proxyMode.value,
  set: (value: ProxyMode) => {
    store.proxyMode.value = value;
  },
});

const traePath = computed({
  get: () => store.traePath.value,
  set: (value: string) => {
    store.traePath.value = value;
  },
});

const traeNativeEnabled = computed(() => proxyMode.value === "trae_native");
const traeOfficialBaseUrlEnabled = computed(() => proxyMode.value === "trae_official_base_url");
const savedProxyMode = computed(() => store.savedProxyMode.value);
const proxyModeDirty = computed(() => proxyMode.value !== savedProxyMode.value);
const proxyRuntimeKnown = computed(() => store.proxyRuntimeKnown.value);
const proxyRuntimeRunning = computed(() => store.proxyRuntimeRunning.value);
const proxyRuntimeActiveMode = computed(() => store.proxyRuntimeActiveMode.value);
const proxyRuntimeLoopbackPort = computed(() => store.proxyRuntimeLoopbackPort.value);

const traePathMissing = computed(() => traeNativeEnabled.value && !traePath.value.trim());
const PREFERRED_TRAE_OFFICIAL_BASE_URL = "http://127.0.0.1:18083/v1";

const buildTraeOfficialBaseUrl = (port: number) => `http://127.0.0.1:${port}/v1`;

const formatProxyModeLabel = (value: ProxyMode | null | undefined) => {
  if (value === "trae_native") {
    return "Trae native";
  }
  if (value === "trae_official_base_url") {
    return "官方 Base URL";
  }
  if (value === "reverse_hosts") {
    return "反代";
  }
  return "未运行";
};

const runtimeStatusBadgeClass = computed(() => {
  if (!proxyRuntimeKnown.value) {
    return "border-slate-200 bg-white/60 text-slate-500";
  }
  if (proxyRuntimeRunning.value) {
    return "border-emerald-500/40 bg-emerald-50 text-emerald-700";
  }
  return "border-slate-200 bg-white/60 text-slate-500";
});

const runtimeStatusDotClass = computed(() => {
  if (!proxyRuntimeKnown.value) {
    return "bg-slate-300";
  }
  return proxyRuntimeRunning.value ? "bg-emerald-500" : "bg-slate-300";
});

const runtimeStatusLabel = computed(() => {
  if (!proxyRuntimeKnown.value) {
    return "运行态同步中";
  }
  if (proxyRuntimeRunning.value) {
    return formatProxyModeLabel(proxyRuntimeActiveMode.value);
  }
  return "未运行";
});

const traePathPlaceholder = computed(() => {
  if (import.meta.client && /Mac/i.test(navigator.platform)) {
    return "/Applications/Trae.app";
  }
  return "%LOCALAPPDATA%\\Programs\\Trae\\Trae.exe";
});

/**
 * 打开目录的工具提示内容
 */
const openDirTooltip = computed(() => {
  const current = appInfo.value.user_data_dir?.trim();
  const fallback = appInfo.value.default_user_data_dir?.trim();
  if (current && fallback && current !== fallback) {
    return `使用系统文件管理器打开用户数据目录\n当前：${current}\n默认：${fallback}`;
  }
  if (current) {
    return `使用系统文件管理器打开用户数据目录\n目录：${current}`;
  }
  if (fallback) {
    return `使用系统文件管理器打开用户数据目录\n默认目录：${fallback}`;
  }
  return "使用系统文件管理器打开用户数据目录";
});

/**
 * 备份数据的工具提示内容
 */
const backupTooltip = [
  "创建带时间戳的完整数据备份",
  "备份内容：配置文件、SSL证书、hosts备份",
  "备份位置：用户数据目录/backups/backup_时间戳/",
].join("\n");

/**
 * 还原数据的工具提示内容
 */
const restoreTooltip = [
  "从最新备份恢复用户数据（覆盖现有数据）",
  "自动选择最新时间戳的备份进行还原",
  "注意：此操作会覆盖当前的配置和证书",
].join("\n");

/**
 * 清除数据的工具提示内容
 */
const clearTooltip = [
  "删除所有用户数据（保留历史备份）",
  "清除内容：配置文件、SSL证书、hosts备份",
  "保留内容：backups文件夹及其历史备份",
].join("\n");

const proxyModeTooltip = [
  "官方 Base URL：走官方接口，只启动本地 loopback",
  "反代：沿用旧的 hosts + HTTPS 路线",
  "Trae native：MTGA 拉起 Trae，并挂载 native rewriter",
  "后续一键启动会按所选模式切分启动流程",
].join("\n");

const traePathTooltip = [
  "用于选择 Trae 可执行文件路径",
  "建议直接通过右侧“浏览”选择，避免手填路径出错",
  "启用该模式后，一键启动会自动拉起 Trae，并挂载 native SSE URL rewriter",
].join("\n");

const officialBaseUrlTooltip = [
  "该模式只启动本地 loopback，不会修改 hosts，也不会安装证书",
  `优先使用：${PREFERRED_TRAE_OFFICIAL_BASE_URL}`,
  "若 18083 被占用，会自动顺延到下一个可用端口",
  "启动后会在此处自动显示实际地址",
].join("\n");

const officialRuntimeLoopbackPort = computed(() => {
  if (!proxyRuntimeRunning.value || proxyRuntimeActiveMode.value !== "trae_official_base_url") {
    return null;
  }
  return proxyRuntimeLoopbackPort.value;
});

const officialBaseUrlDisplay = computed(() => {
  const runtimePort = officialRuntimeLoopbackPort.value;
  if (typeof runtimePort === "number") {
    return buildTraeOfficialBaseUrl(runtimePort);
  }
  return PREFERRED_TRAE_OFFICIAL_BASE_URL;
});

const officialBaseUrlStatusText = computed(() => {
  const runtimePort = officialRuntimeLoopbackPort.value;
  if (runtimePort === null) {
    return "未启动时显示首选地址；启动后会自动更新为实际端口";
  }
  if (runtimePort === 18083) {
    return "当前运行中的实际地址";
  }
  return `当前运行中的实际地址，端口已顺延到 ${runtimePort}`;
});

onMounted(() => {
  void store.startProxyStatusListener().finally(() => {
    void store.fetchProxyRuntimeStatus();
  });
});

/**
 * 处理打开数据目录
 */
const handleOpen = () => {
  store.runUserDataOpenDir();
};

/**
 * 处理备份数据
 */
const handleBackup = () => {
  store.runUserDataBackup();
};

/**
 * 处理还原数据
 */
const handleRestore = () => {
  store.runUserDataRestoreLatest();
};

/**
 * 处理清除数据
 */
const handleClear = () => {
  clearConfirmOpen.value = true;
};

const cancelClear = () => {
  clearConfirmOpen.value = false;
};

const confirmClear = () => {
  clearConfirmOpen.value = false;
  store.runUserDataClear();
};

const handleBrowseTraePath = async () => {
  if (traePathBrowsing.value) {
    return;
  }
  traePathBrowsing.value = true;
  try {
    await store.runBrowseTraePath();
  } finally {
    traePathBrowsing.value = false;
  }
};

const setProxyMode = (value: ProxyMode) => {
  proxyMode.value = value;
};

const saveProxySettings = async (options?: { stopRunningProxy?: boolean }) => {
  const stopRunningProxy = options?.stopRunningProxy === true;
  if (proxySettingsSaving.value) {
    return;
  }

  proxySettingsSaving.value = true;
  proxyModeSwitchConfirmOpen.value = false;
  currentProxyModeForConfirm.value = null;
  try {
    const ok = await store.saveConfig();
    if (!ok) {
      store.appendLog("保存代理模式设置失败");
      return;
    }

    if (!stopRunningProxy) {
      store.appendLog("代理模式设置已保存");
      return;
    }

    store.appendLog("代理模式设置已保存，正在停止当前代理...");
    const stopped = await store.runProxyStop();
    if (stopped) {
      store.appendLog("当前代理已停止；请按新路线重新启动");
      return;
    }
    store.appendLog("代理模式设置已保存，但停止当前代理失败");
  } finally {
    proxySettingsSaving.value = false;
  }
};

const handleProxySettingsSave = async () => {
  if (proxyMode.value === "trae_native" && !traePath.value.trim()) {
    store.appendLog("错误: 启用 Trae native 路线前，请先选择 Trae 路径");
    return;
  }

  if (proxyModeDirty.value) {
    const runtimeStatus = await store.fetchProxyRuntimeStatus();
    if (runtimeStatus?.running) {
      currentProxyModeForConfirm.value = runtimeStatus.active_mode;
      proxyModeSwitchConfirmOpen.value = true;
      return;
    }
  }

  await saveProxySettings();
};

const cancelProxyModeSwitch = () => {
  proxyModeSwitchConfirmOpen.value = false;
  currentProxyModeForConfirm.value = null;
};

const confirmProxyModeSwitch = async () => {
  await saveProxySettings({ stopRunningProxy: true });
};

const openThemeDialog = () => {
  themeDialogOpen.value = true;
};

const handleThemeSave = (value: ThemeConfig) => {
  const normalized = sanitizeThemeConfig(value);
  copyThemeConfig(themeConfig, normalized);
  applyThemeConfig(themeConfig);
  const saveResult = saveThemeToStorage(themeConfig);
  if (saveResult.ok) {
    store.appendLog("主题配置已保存");
    return;
  }
  store.appendLog(`主题配置已应用，但本地保存失败：${saveResult.error}`);
};
</script>

<template>
  <div class="flex items-center justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">应用设置</h2>
      <p class="mtga-card-subtitle">管理数据与系统配置</p>
    </div>
    <span class="mtga-chip">系统</span>
  </div>

  <div class="mt-4 space-y-4">
    <div class="mtga-soft-panel space-y-3">
      <div>
        <div class="text-sm font-semibold text-slate-900">用户数据</div>
        <div class="text-xs text-slate-500">备份与恢复历史数据</div>
      </div>
      <div class="space-y-2">
        <button
          class="mtga-btn-outline tooltip mtga-tooltip"
          :data-tip="openDirTooltip"
          @click="handleOpen"
        >
          打开目录
        </button>
        <button
          class="mtga-btn-primary tooltip mtga-tooltip"
          :data-tip="backupTooltip"
          style="--mtga-tooltip-max: 360px"
          @click="handleBackup"
        >
          备份数据
        </button>
        <button
          class="mtga-btn-outline tooltip mtga-tooltip"
          :data-tip="restoreTooltip"
          style="--mtga-tooltip-max: 360px"
          @click="handleRestore"
        >
          还原数据
        </button>
        <button
          class="mtga-btn-error tooltip mtga-tooltip"
          :data-tip="clearTooltip"
          style="--mtga-tooltip-max: 360px"
          @click="handleClear"
        >
          清除数据
        </button>
      </div>
    </div>

    <div class="mtga-soft-panel space-y-3">
      <div class="flex items-start justify-between gap-3">
        <div>
          <div class="text-sm font-semibold text-slate-900">启动路线</div>
          <div class="text-xs text-slate-500">决定使用哪条接入链路</div>
        </div>
        <span
          class="inline-flex shrink-0 items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-semibold"
          :class="runtimeStatusBadgeClass"
        >
          <span class="h-1.5 w-1.5 rounded-full" :class="runtimeStatusDotClass" />
          实时运行态：{{ runtimeStatusLabel }}
        </span>
      </div>

      <div
        class="tooltip mtga-tooltip grid grid-cols-1 gap-2 md:grid-cols-3"
        :data-tip="proxyModeTooltip"
        style="--mtga-tooltip-max: 360px"
      >
        <button
          type="button"
          class="cursor-pointer rounded-xl border px-3 py-2 text-left transition-all active:scale-[0.99]"
          :class="
            traeOfficialBaseUrlEnabled
              ? 'border-emerald-500/50 bg-emerald-50/80 shadow-sm shadow-emerald-500/10'
              : 'border-slate-200/80 bg-white/40 hover:border-slate-300 hover:bg-white/70'
          "
          @click="setProxyMode('trae_official_base_url')"
        >
          <span class="block text-sm font-semibold text-slate-800">官方 Base URL</span>
          <span class="mt-0.5 block text-[11px] leading-4 text-slate-500"
            >仅 loopback，无 patch</span
          >
        </button>
        <button
          type="button"
          class="cursor-pointer rounded-xl border px-3 py-2 text-left transition-all active:scale-[0.99]"
          :class="
            proxyMode === 'reverse_hosts'
              ? 'border-amber-500/50 bg-amber-50/80 shadow-sm shadow-amber-500/10'
              : 'border-slate-200/80 bg-white/40 hover:border-slate-300 hover:bg-white/70'
          "
          @click="setProxyMode('reverse_hosts')"
        >
          <span class="block text-sm font-semibold text-slate-800">反代</span>
          <span class="mt-0.5 block text-[11px] leading-4 text-slate-500">hosts + HTTPS 代理</span>
        </button>
        <button
          type="button"
          class="cursor-pointer rounded-xl border px-3 py-2 text-left transition-all active:scale-[0.99]"
          :class="
            traeNativeEnabled
              ? 'border-amber-500/50 bg-amber-50/80 shadow-sm shadow-amber-500/10'
              : 'border-slate-200/80 bg-white/40 hover:border-slate-300 hover:bg-white/70'
          "
          @click="setProxyMode('trae_native')"
        >
          <span class="block text-sm font-semibold text-slate-800">Trae native</span>
          <span class="mt-0.5 block text-[11px] leading-4 text-slate-500">patch trae 源码</span>
        </button>
      </div>

      <div
        v-if="traeNativeEnabled"
        class="mtga-tooltip w-full rounded-xl border border-slate-200/80 bg-white/35 p-3"
        :data-tip="traePathTooltip"
        style="--mtga-tooltip-max: 360px"
      >
        <div class="mb-2 flex items-center justify-between gap-3">
          <div>
            <div class="text-xs font-semibold text-slate-700">Trae 可执行文件</div>
            <div class="text-[11px] text-slate-400">用于由 MTGA 拉起干净 Trae 实例</div>
          </div>
        </div>
        <div class="flex items-start gap-2">
          <MtgaInput
            v-model="traePath"
            class="min-w-0 flex-1"
            :placeholder="traePathPlaceholder"
            :error="traePathMissing ? '启用 Trae native 路线前需要先选择 Trae 路径。' : ''"
          />
          <button
            type="button"
            class="btn btn-outline btn-sm h-10 min-w-[76px] shrink-0 cursor-pointer gap-2 rounded-xl border-slate-200 px-3 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
            :disabled="traePathBrowsing"
            :aria-busy="traePathBrowsing"
            @click="handleBrowseTraePath"
          >
            <span
              v-if="traePathBrowsing"
              class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-slate-300 border-t-amber-500"
            />
            <span>{{ traePathBrowsing ? "选择中" : "浏览" }}</span>
          </button>
        </div>
      </div>

      <div
        v-if="traeOfficialBaseUrlEnabled"
        class="mtga-tooltip w-full rounded-xl border border-emerald-200/70 bg-emerald-50/50 p-3"
        :data-tip="officialBaseUrlTooltip"
        style="--mtga-tooltip-max: 360px"
      >
        <div class="mb-2 flex items-center justify-between gap-3">
          <div>
            <div class="text-xs font-semibold text-emerald-800">Trae 自定义模型 Base URL</div>
            <div class="text-[11px] text-emerald-700/80">
              该路线只启动本地 loopback，Trae 需要手动配置 base_url
            </div>
          </div>
        </div>
        <div
          class="rounded-lg border border-emerald-200/70 bg-white/80 px-3 py-2 font-mono text-sm text-emerald-900"
        >
          {{ officialBaseUrlDisplay }}
        </div>
        <div class="mt-2 text-[11px] text-emerald-700/80">
          {{ officialBaseUrlStatusText }}
        </div>
      </div>

      <div class="flex items-center justify-end">
        <button
          class="btn btn-primary btn-sm rounded-xl px-4"
          :class="proxySettingsSaving ? 'loading' : ''"
          :disabled="proxySettingsSaving"
          @click="handleProxySettingsSave"
        >
          保存路线设置
        </button>
      </div>
    </div>

    <button class="mtga-clickable-row" @click="openThemeDialog">
      <span class="flex flex-col items-start gap-0.5 text-left">
        <span class="font-semibold text-slate-800">主题配置</span>
        <span class="text-xs font-normal text-slate-500">自定义颜色、字体与背景</span>
      </span>
    </button>
  </div>

  <ConfirmDialog
    :open="clearConfirmOpen"
    :title="clearConfirmTitle"
    :message="clearConfirmMessage"
    confirm-text="确认清除"
    type="error"
    @cancel="cancelClear"
    @confirm="confirmClear"
  />

  <ConfirmDialog
    :open="proxyModeSwitchConfirmOpen"
    title="确认切换路线"
    message="当前代理正在运行。保存新路线后，MTGA 会立即停止当前代理；下次启动将按新路线生效。"
    confirm-text="保存并停止代理"
    @cancel="cancelProxyModeSwitch"
    @confirm="confirmProxyModeSwitch"
  >
    <div class="space-y-2 text-sm text-slate-600">
      <p>当前运行：{{ formatProxyModeLabel(currentProxyModeForConfirm) }}</p>
      <p>将切换为：{{ formatProxyModeLabel(proxyMode) }}</p>
    </div>
  </ConfirmDialog>

  <ThemeSettingsDialog
    v-model:open="themeDialogOpen"
    :config="themeConfig"
    @save="handleThemeSave"
  />
</template>

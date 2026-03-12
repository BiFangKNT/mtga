<script setup lang="ts">
/**
 * 设置面板组件
 * 提供用户数据管理、备份、还原及清理功能
 */
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
const themeDialogOpen = ref(false);

const themeConfig = reactive<ThemeConfig>({ ...DEFAULT_THEME_CONFIG });
if (import.meta.client) {
  const savedTheme = loadThemeFromStorage();
  if (savedTheme) {
    copyThemeConfig(themeConfig, savedTheme);
  }
}

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

const openThemeDialog = () => {
  themeDialogOpen.value = true;
};

const enable429Failover = computed({
  get: () => store.enable429Failover.value,
  set: (value) => {
    store.enable429Failover.value = value;
  },
});

const failover429CooldownSeconds = computed({
  get: () => store.failover429CooldownSeconds.value,
  set: (value) => {
    store.failover429CooldownSeconds.value = value;
  },
});

const handleFailoverChange = async () => {
  const ok = await store.saveConfig();
  if (ok) {
    store.appendLog(`API 智能调度已${enable429Failover.value ? "启用" : "禁用"}`);
  } else {
    store.appendLog("保存配置失败");
  }
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
        <div class="text-sm font-semibold text-slate-900">高级策略</div>
        <div class="text-xs text-slate-500">API 调度与故障转移</div>
      </div>
      <label class="label cursor-pointer justify-start gap-3 p-0">
        <input
          v-model="enable429Failover"
          type="checkbox"
          class="toggle toggle-primary toggle-sm"
          @change="handleFailoverChange"
        />
        <span class="label-text text-slate-700">启用 API 智能调度（轮询 + 429 切换）</span>
      </label>
      <label class="label justify-start gap-3 p-0 pl-11">
        <span class="label-text text-slate-700">429 冷却（秒）</span>
        <input
          v-model.number="failover429CooldownSeconds"
          type="number"
          min="1"
          class="input input-sm w-24"
          @change="handleFailoverChange"
        />
      </label>
      <div class="text-xs text-slate-500 pl-11">
        开启后，请求会在配置组间轮询分发；当某个节点触发 429 (Too Many Requests) 时，
        将自动切换到下一个节点，并对 429 节点进行短暂冷却以避免重复命中。
      </div>
    </div>

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

  <ThemeSettingsDialog
    v-model:open="themeDialogOpen"
    :config="themeConfig"
    @save="handleThemeSave"
  />
</template>

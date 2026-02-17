<script setup lang="ts">
/**
 * 设置面板组件
 * 提供用户数据管理、备份、还原及清理功能
 */
import { ref, computed, reactive, onMounted } from 'vue'
import {
  type ThemeConfig,
  DEFAULT_THEME_CONFIG,
  applyThemeConfig,
  copyThemeConfig,
  loadThemeFromStorage,
  sanitizeThemeConfig,
  saveThemeToStorage,
} from "~/composables/themeConfig"
import { useAutoStart } from "~/composables/useAutoStart"


const store = useMtgaStore()
const appInfo = store.appInfo
const disableUpdatePopup = computed({
  get: () => store.disableUpdatePopup.value,
  set: async (val) => {
    store.disableUpdatePopup.value = val
    // 立即保存配置到后端
    const ok = await store.saveConfig()
    if (!ok) {
      store.appendLog("保存配置失败：无法持久化禁用更新弹窗设置")
    }
  }
})

// 移除旧的 localStorage watcher，改用 computed setter 触发 saveConfig
// watch(disableUpdatePopup, (val) => { ... }) 

const clearConfirmOpen = ref(false)
const clearConfirmTitle = "确认清除数据"
const clearConfirmMessage = "确定要清除用户数据吗？该操作将删除配置文件、SSL 证书和 hosts 备份（历史 backups 保留）。"
const themeDialogOpen = ref(false)

const themeConfig = reactive<ThemeConfig>({ ...DEFAULT_THEME_CONFIG })
if (import.meta.client) {
  const savedTheme = loadThemeFromStorage()
  if (savedTheme) {
    copyThemeConfig(themeConfig, savedTheme)
  }
}

// 开机自启动相关
const {
  isSupported: isAutoStartSupported,
  isEnabled: autoStartEnabled,
  isLoading: autoStartLoading,
  checkStatus: checkAutoStartStatus,
  setEnabled: setAutoStartEnabled
} = useAutoStart()

// GitHub Token (从 store 获取)
const githubToken = computed({
  get: () => store.githubToken.value,
  set: (value) => {
    store.githubToken.value = value
  },
})

const handleSaveToken = async () => {
  const ok = await store.saveConfig()
  if (ok) {
    store.appendLog("GitHub Token 已保存")
  } else {
    store.appendLog("保存 GitHub Token 失败")
  }
}

/**
 * 打开目录的工具提示内容
 */
const openDirTooltip = computed(() => {
  const current = appInfo.value.user_data_dir?.trim()
  const fallback = appInfo.value.default_user_data_dir?.trim()
  if (current && fallback && current !== fallback) {
    return `使用系统文件管理器打开用户数据目录\n当前：${current}\n默认：${fallback}`
  }
  if (current) {
    return `使用系统文件管理器打开用户数据目录\n目录：${current}`
  }
  if (fallback) {
    return `使用系统文件管理器打开用户数据目录\n默认目录：${fallback}`
  }
  return "使用系统文件管理器打开用户数据目录"
})

/**
 * 备份数据的工具提示内容
 */
const backupTooltip = [
  "创建当前状态的完整快照，包含：",
  "• 配置分组：所有代理服务配置",
  "• 全局参数：映射模型ID与鉴权Key",
  "• 核心服务：SSL证书与hosts备份",
  "• 系统设置：界面主题与应用行为",
  "",
  "备份位置：用户数据目录/backups/"
].join("\n")

/**
 * 还原数据的工具提示内容
 */
const restoreTooltip = [
  "从最新备份恢复所有数据：",
  "• 覆盖所有配置分组与全局参数",
  "• 恢复证书文件与hosts记录",
  "• 应用备份时的系统设置与主题",
  "",
  "注意：操作后界面将自动刷新"
].join("\n")

/**
 * 清除数据的工具提示内容
 */
const clearTooltip = [
  "重置应用为初始安装状态：",
  "• 清空所有配置分组与参数",
  "• 删除证书与hosts备份文件",
  "• 重置系统设置与主题为默认",
  "",
  "注意：保留历史备份文件"
].join("\n")

/**
 * 自启动工具提示
 */
const autoStartTooltip = computed(() => {
  if (!isAutoStartSupported.value) {
    return "当前系统不支持开机自启动功能"
  }
  return autoStartEnabled.value 
    ? "应用将在系统启动时自动运行（最小化启动）"
    : "应用不会在系统启动时自动运行"
})

const cancelClear = () => {
  clearConfirmOpen.value = false
}

const confirmClear = () => {
  clearConfirmOpen.value = false
  store.runUserDataClear()
}

const handleThemeSave = (value: ThemeConfig) => {
  const normalized = sanitizeThemeConfig(value)
  copyThemeConfig(themeConfig, normalized)
  applyThemeConfig(themeConfig)
  const saveResult = saveThemeToStorage(themeConfig)
  if (saveResult.ok) {
    store.appendLog("主题配置已保存")
    return
  }
  store.appendLog(`主题配置已应用，但本地保存失败：${saveResult.error}`)
}

// 组件挂载时检查自启动支持
onMounted(() => {
  if (import.meta.client) {
    checkAutoStartStatus()
  }
})
</script>

<template>
  <div class="flex items-center justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">系统设置</h2>
      <p class="mtga-card-subtitle">管理用户数据、界面外观与应用行为</p>
    </div>
    <span class="mtga-chip">系统设置</span>
  </div>

  <div class="mt-4 space-y-4">
    <!-- 用户数据 -->
    <div class="mtga-soft-panel space-y-3">
      <div>
        <div class="text-sm font-semibold text-slate-900">用户数据</div>
        <div class="text-xs text-slate-500">备份与恢复历史数据</div>
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50 hover:text-amber-600 font-normal mtga-tooltip"
          :data-tip="openDirTooltip"
          @click="store.runUserDataOpenDir"
        >
          打开目录
        </button>
        <button
          class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50 hover:text-amber-600 font-normal mtga-tooltip"
          :data-tip="backupTooltip"
          style="--mtga-tooltip-max: 360px;"
          @click="store.runUserDataBackup"
        >
          备份数据
        </button>
        <button
          class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50 hover:text-amber-600 font-normal mtga-tooltip"
          :data-tip="restoreTooltip"
          style="--mtga-tooltip-max: 360px;"
          @click="store.runUserDataRestoreLatest"
        >
          还原数据
        </button>
        <button
          class="btn btn-sm btn-outline btn-error text-error border-error/20 hover:bg-error/10 hover:border-error font-normal mtga-tooltip ml-auto rounded-xl"
          :data-tip="clearTooltip"
          style="--mtga-tooltip-max: 360px;"
          @click="clearConfirmOpen = true"
        >
          清除数据
        </button>
      </div>
    </div>

    <!-- 系统设置 -->
    <div class="mtga-soft-panel space-y-3">
      <div>
        <div class="text-sm font-semibold text-slate-900">系统设置</div>
        <div class="text-xs text-slate-500">应用行为与外观</div>
      </div>
      
      <!-- 界面主题 -->
      <div class="mtga-settings-row">
        <div class="flex-1">
          <div class="font-medium text-slate-800 text-sm">界面主题</div>
          <div class="text-xs text-slate-500 mt-0.5">
            自定义应用配色方案
          </div>
        </div>
        <button
          class="btn btn-sm btn-ghost text-amber-600 hover:bg-amber-100 font-normal"
          @click="themeDialogOpen = true"
        >
          配置主题
        </button>
      </div>

      <!-- 开机自启动 -->
      <div v-if="!isAutoStartSupported" class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-500">
        当前系统不支持开机自启动功能
      </div>
      <div v-else class="mtga-settings-row">
        <div class="flex-1">
          <div class="font-medium text-slate-800 text-sm">开机自启动</div>
          <div class="text-xs text-slate-500 mt-0.5">
            {{ autoStartTooltip }}
          </div>
        </div>
        <input
          type="checkbox"
          class="toggle toggle-warning toggle-sm"
          :checked="autoStartEnabled"
          :disabled="autoStartLoading"
          @change="async (e) => await setAutoStartEnabled((e.target as HTMLInputElement).checked)"
        />
      </div>

      <!-- GitHub Token -->
      <div class="mtga-settings-row">
        <div class="flex-1 mr-4">
          <div class="font-medium text-slate-800 text-sm">GitHub Token</div>
          <div class="text-xs text-slate-500 mt-0.5">
            解决检查更新时的 403 速率限制
          </div>
        </div>
        <div 
          class="w-[220px] mtga-tooltip"
          data-tip="可选：GitHub Token\n用于解决检查更新时的 403 速率限制问题。\n如果没有遇到更新检查失败，可留空。\n需要 repo 权限的 Classic Token 或 Fine-grained Token。"
          style="--mtga-tooltip-max: 360px;"
        >
          <MtgaInput
            v-model="githubToken"
            type="password"
            placeholder="ghp_..."
            size="sm"
            input-class="text-xs"
          >
            <template #trailing>
              <button
                class="btn btn-xs btn-ghost text-amber-600 hover:bg-amber-100 h-6 min-h-0 px-2 font-normal rounded"
                @click="handleSaveToken"
              >
                保存
              </button>
            </template>
          </MtgaInput>
        </div>
      </div>

      <!-- 禁用自动更新弹窗 -->
      <div class="mtga-settings-row">
        <div class="flex-1">
          <div class="font-medium text-slate-800 text-sm">禁用自动更新弹窗</div>
          <div class="text-xs text-slate-500 mt-0.5">
            启动时发现新版本不再自动弹出提示窗口
          </div>
        </div>
        <input
          v-model="disableUpdatePopup"
          type="checkbox"
          class="toggle toggle-warning toggle-sm"
        />
      </div>
    </div>
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

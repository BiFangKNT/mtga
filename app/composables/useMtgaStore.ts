import { useMtgaApi } from "./useMtgaApi"
import { listen } from "@tauri-apps/api/event"
import { isBundledRuntime, isTauriRuntime } from "./runtime"
import type {
  AppInfo,
  ConfigGroup,
  ConfigPayload,
  InvokeResult,
  LogEventPayload,
  LogPullResult,
  MainTabKey,
  ProxyStartStepEvent,
} from "./mtgaTypes"

type RuntimeOptions = {
  debugMode: boolean
  disableSslStrict: boolean
  forceStream: boolean
  streamMode: "true" | "false"
}

type PanelTarget = "config-group" | "global-config" | "main-tabs" | "settings"

const DEFAULT_APP_INFO: AppInfo = {
  display_name: "MTGA",
  version: "v0.0.0",
  github_repo: "",
  ca_common_name: "MTGA_CA",
  api_key_visible_chars: 4,
  user_data_dir: "",
  default_user_data_dir: "",
}

const DEFAULT_RUNTIME_OPTIONS: RuntimeOptions = {
  debugMode: false,
  disableSslStrict: false,
  forceStream: false,
  streamMode: "true",
}

const FRONTEND_LOG_LIMIT = 2000

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const isMainTabKey = (value: unknown): value is MainTabKey =>
  value === "cert" || value === "hosts" || value === "proxy"

const isProxyStepStatus = (
  value: unknown
): value is ProxyStartStepEvent["status"] =>
  value === "ok" ||
  value === "skipped" ||
  value === "failed" ||
  value === "started"

const isPanelTarget = (value: unknown): value is PanelTarget =>
  value === "config-group" ||
  value === "global-config" ||
  value === "main-tabs" ||
  value === "settings"

const isProxyStartStepEvent = (
  value: unknown
): value is ProxyStartStepEvent => {
  if (!isRecord(value)) {
    return false
  }
  return isMainTabKey(value.step) && isProxyStepStatus(value.status)
}

const normalizeProxyStepPayload = (
  payload: unknown
): ProxyStartStepEvent | null => {
  if (isProxyStartStepEvent(payload)) {
    return payload
  }
  if (typeof payload === "string") {
    try {
      const parsed = JSON.parse(payload)
      if (isProxyStartStepEvent(parsed)) {
        return parsed
      }
    } catch {
      return null
    }
  }
  return null
}

const coerceText = (value: unknown) => {
  if (typeof value === "string") {
    return value
  }
  if (typeof value === "number") {
    return String(value)
  }
  if (isRecord(value)) {
    const candidates = [value["id"], value["value"], value["model_id"]]
    for (const candidate of candidates) {
      if (typeof candidate === "string") {
        return candidate
      }
    }
  }
  return ""
}

const normalizeModelList = (value: unknown) => {
  if (!Array.isArray(value)) {
    return []
  }
  const unique = new Set<string>()
  value.forEach((item) => {
    const text = coerceText(item).trim()
    if (text) {
      unique.add(text)
    }
  })
  return Array.from(unique).sort((a, b) => a.localeCompare(b))
}

const clampIndex = (value: number, max: number) => {
  if (max <= 0) {
    return 0
  }
  return Math.min(Math.max(value, 0), max - 1)
}

export const useMtgaStore = () => {
  const api = useMtgaApi()

  const configGroups = useState<ConfigGroup[]>("mtga-config-groups", () => [])
  const currentConfigIndex = useState<number>("mtga-current-config-index", () => 0)
  const mappedModelId = useState<string>("mtga-mapped-model-id", () => "")
  const mtgaAuthKey = useState<string>("mtga-auth-key", () => "")
  const githubToken = useState<string>("mtga-github-token", () => "")
  const runtimeOptions = useState<RuntimeOptions>(
    "mtga-runtime-options",
    () => ({ ...DEFAULT_RUNTIME_OPTIONS })
  )
  const logs = useState<string[]>("mtga-logs", () => [])
  const logCursor = useState<number>("mtga-log-cursor", () => 0)
  const logStreamActive = useState<boolean>("mtga-log-stream-active", () => false)
  const appInfo = useState<AppInfo>("mtga-app-info", () => ({ ...DEFAULT_APP_INFO }))
  const initialized = useState<boolean>("mtga-initialized", () => false)
  const hasNewVersion = useState<boolean>("mtga-has-new-version", () => false)
  const updateDialogOpen = useState<boolean>("mtga-update-dialog-open", () => false)
  const updateVersionLabel = useState<string>("mtga-update-version-label", () => "")
  const updateNotesHtml = useState<string>("mtga-update-notes-html", () => "")
  const updateReleaseUrl = useState<string>("mtga-update-release-url", () => "")
  const updateAutoChecked = useState<boolean>(
    "mtga-update-auto-checked",
    () => false
  )
  const panelNavTarget = useState<string | null>(
    "mtga-panel-nav-target",
    () => null
  )
  const panelNavSignal = useState<number>("mtga-panel-nav-signal", () => 0)
  const mainTabTarget = useState<MainTabKey | null>(
    "mtga-main-tab-target",
    () => null
  )
  const mainTabSignal = useState<number>("mtga-main-tab-signal", () => 0)
  const proxyStepListenerActive = useState<boolean>(
    "mtga-proxy-step-listener-active",
    () => false
  )
  const proxyStepQueue = useState<MainTabKey[]>(
    "mtga-proxy-step-queue",
    () => []
  )
  const proxyStepProcessing = useState<boolean>(
    "mtga-proxy-step-processing",
    () => false
  )
  const disableUpdatePopup = useState<boolean>(
    "mtga-disable-update-popup",
    () => false
  )

  let logPollTimer: ReturnType<typeof setTimeout> | null = null
  let logEventUnlisten: (() => void) | null = null
  let proxyStepUnlisten: (() => void) | null = null

  const drainProxyStepQueue = async () => {
    if (proxyStepProcessing.value) {
      return
    }
    proxyStepProcessing.value = true
    while (proxyStepQueue.value.length) {
      const step = proxyStepQueue.value.shift()
      if (!step) {
        continue
      }
      panelNavTarget.value = "main-tabs"
      panelNavSignal.value += 1
      mainTabTarget.value = step
      mainTabSignal.value += 1
      await nextTick()
      await new Promise((resolve) => setTimeout(resolve, 240))
    }
    proxyStepProcessing.value = false
  }

  const enqueueProxyStep = (step: MainTabKey) => {
    proxyStepQueue.value.push(step)
    void drainProxyStepQueue()
  }

  const navigateProxyMissingConfigPanel = (message?: string | null) => {
    const normalized = (message || "").trim()
    if (!normalized) {
      return
    }
    if (
      normalized.includes("全局配置缺失") ||
      normalized === "global_config_missing"
    ) {
      panelNavTarget.value = "global-config"
      panelNavSignal.value += 1
      return
    }
    if (
      normalized.includes("没有可用的配置组") ||
      normalized === "config_group_missing"
    ) {
      panelNavTarget.value = "config-group"
      panelNavSignal.value += 1
    }
  }

  const appendLog = (message: string) => {
    logs.value.push(message)
    const overflow = logs.value.length - FRONTEND_LOG_LIMIT
    if (overflow > 0) {
      logs.value.splice(0, overflow)
    }
  }

  const handleProxyStep = (payload: unknown) => {
    const normalized = normalizeProxyStepPayload(payload)
    if (!normalized || !isMainTabKey(normalized.step)) {
      return
    }
    if (isPanelTarget(normalized.panel_target)) {
      panelNavTarget.value = normalized.panel_target
      panelNavSignal.value += 1
    } else {
      navigateProxyMissingConfigPanel(normalized.message)
    }
    if (normalized.status === "started") {
      enqueueProxyStep(normalized.step)
    }
  }

  const appendLogs = (entries?: string[]) => {
    if (!entries || !entries.length) {
      return
    }
    entries.forEach((entry) => appendLog(entry))
  }

  const applyInvokeResult = (
    result: InvokeResult | null,
    fallbackMessage: string
  ) => {
    if (!result) {
      appendLog(`${fallbackMessage}失败：无法连接后端`)
      return false
    }
    if (result.message) {
      appendLog(result.message)
    }
    return result.ok
  }

  const startLogStream = () => {
    if (logStreamActive.value) {
      return
    }
    logStreamActive.value = true
    if (logEventUnlisten) {
      try {
        logEventUnlisten()
      } catch {
        // ignore cleanup errors
      }
      logEventUnlisten = null
    }
    if (logPollTimer !== null) {
      clearTimeout(logPollTimer)
      logPollTimer = null
    }

    const applyLogResult = (result: LogPullResult | null) => {
      if (!result) {
        return
      }
      if (Array.isArray(result.items) && result.items.length) {
        appendLogs(result.items)
      }
      if (typeof result.next_id === "number") {
        logCursor.value = result.next_id
      }
    }

    const startPolling = () => {
      const loop = async () => {
        if (!logStreamActive.value) {
          return
        }
        const result = await api.pullLogs({
          after_id: logCursor.value || null,
          timeout_ms: 0,
          max_items: 200,
        })
        if (!logStreamActive.value) {
          return
        }
        applyLogResult(result)
        logPollTimer = setTimeout(loop, 200)
      }
      void loop()
    }

    const startEventStream = async () => {
      if (!isTauriRuntime()) {
        startPolling()
        return
      }

      const initial = await api.pullLogs({
        after_id: logCursor.value || null,
        timeout_ms: 0,
        max_items: 200,
      })
      applyLogResult(initial)

      try {
        const unlisten = await listen<LogEventPayload>("mtga:logs", (event) => {
          const payload = event.payload
          if (!payload) {
            return
          }
          if (Array.isArray(payload.items) && payload.items.length) {
            appendLogs(payload.items)
          }
          if (typeof payload.next_id === "number") {
            logCursor.value = payload.next_id
          }
        })
        if (!logStreamActive.value) {
          try {
            unlisten()
          } catch {
            // ignore cleanup errors
          }
          return
        }
        logEventUnlisten = () => {
          void unlisten()
        }
      } catch (error) {
        console.warn("[mtga] log event listen failed", error)
        startPolling()
      }
    }

    void startEventStream()
  }

  const stopLogStream = () => {
    logStreamActive.value = false
    if (logPollTimer !== null) {
      clearTimeout(logPollTimer)
      logPollTimer = null
    }
    if (logEventUnlisten) {
      try {
        logEventUnlisten()
      } catch {
        // ignore cleanup errors
      }
      logEventUnlisten = null
    }
  }

  const startProxyStepListener = () => {
    if (proxyStepListenerActive.value) {
      return
    }
    proxyStepListenerActive.value = true
    if (proxyStepUnlisten) {
      try {
        proxyStepUnlisten()
      } catch {
        // ignore cleanup errors
      }
      proxyStepUnlisten = null
    }

    if (isBundledRuntime()) {
      return
    }

    const listenProxySteps = async () => {
      try {
        const unlisten = await listen<ProxyStartStepEvent>("mtga:proxy-step", (event) => {
          handleProxyStep(event.payload)
        })
        if (!proxyStepListenerActive.value) {
          try {
            unlisten()
          } catch {
            // ignore cleanup errors
          }
          return
        }
        proxyStepUnlisten = () => {
          void unlisten()
        }
      } catch (error) {
        console.warn("[mtga] proxy step listen failed", error)
      }
    }

    void listenProxySteps()
  }

  const stopProxyStepListener = () => {
    proxyStepListenerActive.value = false
    if (proxyStepUnlisten) {
      try {
        proxyStepUnlisten()
      } catch {
        // ignore cleanup errors
      }
      proxyStepUnlisten = null
    }
  }

  const loadConfig = async () => {
    const result = await api.loadConfig()
    if (!result) {
      return false
    }
    configGroups.value = result.config_groups || []
    currentConfigIndex.value = clampIndex(
      result.current_config_index ?? 0,
      configGroups.value.length
    )
    mappedModelId.value = coerceText(result.mapped_model_id)
    mtgaAuthKey.value = coerceText(result.mtga_auth_key)
    githubToken.value = coerceText(result.github_token)
    // 优先使用后端配置，如果没有则回退到 localStorage (兼容旧版数据)
    if (typeof result.disable_update_popup === 'boolean') {
      disableUpdatePopup.value = result.disable_update_popup
    }

    // 恢复主题配置
    if (result.theme_config && typeof result.theme_config === 'object') {
      try {
        const { applyThemeConfig, sanitizeThemeConfig } = await import("./themeConfig")
        const normalized = sanitizeThemeConfig(result.theme_config)
        // 应用到全局状态（注意这里需要配合 SettingsPanel 的响应式数据，
        // 但 themeConfig 是在组件中使用的。我们需要一种方式通知或更新全局主题）
        // 目前 themeConfig 模块主要操作 DOM CSS 变量，我们直接调用 applyThemeConfig 即可生效视觉
        // 同时保存到 localStorage 以保持兼容性
        const { saveThemeToStorage } = await import("./themeConfig")
        saveThemeToStorage(normalized)
        applyThemeConfig(normalized)
      } catch {
        console.warn("[mtga] restore theme config failed")
      }
    }
    return true
  }

  const saveConfig = async () => {
    const clampedIndex = clampIndex(
      currentConfigIndex.value,
      configGroups.value.length
    )
    currentConfigIndex.value = clampedIndex

    // 获取当前主题配置
    let currentThemeConfig = null
    try {
      const { loadThemeFromStorage } = await import("./themeConfig")
      currentThemeConfig = loadThemeFromStorage()
    } catch {
      // ignore
    }

    const payload: ConfigPayload = {
      config_groups: configGroups.value,
      current_config_index: clampedIndex,
      mapped_model_id: coerceText(mappedModelId.value),
      mtga_auth_key: coerceText(mtgaAuthKey.value),
      github_token: coerceText(githubToken.value),
      disable_update_popup: disableUpdatePopup.value,
      theme_config: currentThemeConfig || undefined,
    }
    const ok = await api.saveConfig(payload)
    return Boolean(ok)
  }

  const loadAppInfo = async () => {
    const info = await api.getAppInfo()
    if (!info) {
      return false
    }
    appInfo.value = {
      ...DEFAULT_APP_INFO,
      ...info,
    }
    return true
  }

  const buildStartupLogs = (details: Record<string, unknown>) => {
    const envOk = details["env_ok"] === true
    const envMessage = coerceText(details["env_message"])
    if (envMessage) {
      appendLog(`${envOk ? "✅" : "❌"} ${envMessage}`)
    }
    if (envOk) {
      const runtime = coerceText(details["runtime"])
      if (runtime === "tauri" || runtime === "nuitka") {
        appendLog("📦 运行在打包环境中")
      } else {
        appendLog("🔧 运行在开发环境中")
      }
    }

    const allowFlag =
      coerceText(details["allow_unsafe_hosts_flag"]) || "--allow-unsafe-hosts"
    const hostsModifyBlocked = details["hosts_modify_blocked"] === true
    if (hostsModifyBlocked) {
      const status = coerceText(details["hosts_modify_block_status"]) || "unknown"
      appendLog(
        `⚠️ 检测到 hosts 文件写入受限（status=${status}），已启用受限 hosts 模式：添加将回退为追加写入（无法保证原子性增删/去重），自动移除/还原将被禁用。`
      )
      appendLog(
        `⚠️ 你可以点击「打开hosts文件」手动修改；或使用启动参数 ${allowFlag} 覆盖此检查以强制尝试原子写入（风险自负）。`
      )
    } else {
      const preflightOk = details["hosts_preflight_ok"] === true
      const preflightStatus = coerceText(details["hosts_preflight_status"])
      if (preflightStatus && !preflightOk) {
        appendLog(
          `⚠️ hosts 预检未通过（status=${preflightStatus}），但已使用启动参数 ${allowFlag} 覆盖；后续自动修改可能失败。`
        )
      }
    }

    if (details["explicit_proxy_detected"] === true) {
      appendLog(
        "⚠️".repeat(21) +
        "\n检测到显式代理配置：部分应用可能优先走代理，从而绕过 hosts 导流。"
      )
      appendLog("建议：1. 关闭显式代理（如clash的系统代理），或改用 TUN/VPN")
      appendLog("      2. 检查 Trae 的代理设置。\n" + "⚠️".repeat(21))
    }

    appendLog("MTGA 已启动")
    appendLog("请选择操作或直接使用一键启动...")
  }

  const loadStartupStatus = async () => {
    const result = await api.getStartupStatus()
    if (!result) {
      appendLog("启动日志加载失败：无法连接后端")
      return false
    }
    if (isRecord(result.details)) {
      buildStartupLogs(result.details)
    }
    return result.ok
  }

  const init = async () => {
    if (initialized.value) {
      startLogStream()
      startProxyStepListener()
      return
    }

    if (import.meta.client) {
      try {
        const raw = localStorage.getItem("mtga-user-config-v1")
        if (raw) {
          const parsed = JSON.parse(raw)
          disableUpdatePopup.value = !!parsed.disableUpdatePopup
        }
      } catch (e) {
        console.warn("[mtga] load user config failed", e)
      }
    }

    initialized.value = true
    startLogStream()
    startProxyStepListener()
    await Promise.all([loadAppInfo(), loadConfig(), loadStartupStatus()])
  }

  const buildProxyPayload = () => ({
    debug_mode: runtimeOptions.value.debugMode,
    disable_ssl_strict_mode: runtimeOptions.value.disableSslStrict,
    force_stream: runtimeOptions.value.forceStream,
    stream_mode: runtimeOptions.value.streamMode,
  })

  const runGenerateCertificates = async () => {
    const result = await api.generateCertificates()
    return applyInvokeResult(result, "生成证书")
  }

  const runInstallCaCert = async () => {
    const result = await api.installCaCert()
    return applyInvokeResult(result, "安装 CA 证书")
  }

  const runClearCaCert = async (caCommonName?: string) => {
    const normalizedCaCommonName = caCommonName?.trim()
    const result = await api.clearCaCert(
      normalizedCaCommonName
        ? { ca_common_name: normalizedCaCommonName }
        : {}
    )
    return applyInvokeResult(result, "清除 CA 证书")
  }

  const runHostsModify = async (
    mode: "add" | "backup" | "restore" | "remove"
  ) => {
    const result = await api.hostsModify({ mode })
    return applyInvokeResult(result, "hosts 操作")
  }

  const runHostsOpen = async () => {
    const result = await api.hostsOpen()
    return applyInvokeResult(result, "打开 hosts 文件")
  }

  const runProxyStart = async () => {
    const result = await api.proxyStart(buildProxyPayload())
    navigateProxyMissingConfigPanel(result?.message)
    return applyInvokeResult(result, "启动代理服务器")
  }

  const runProxyApplyCurrentConfig = async () => {
    const result = await api.proxyApplyCurrentConfig(buildProxyPayload())
    navigateProxyMissingConfigPanel(result?.message)
    if (!result) {
      appendLog("应用代理配置失败：无法连接后端")
      return false
    }

    const message = coerceText(result.message).trim()
    const applyStatus =
      isRecord(result.details) ? coerceText(result.details["apply_status"]) : ""

    if (result.ok) {
      if (applyStatus === "deferred" || message === "proxy_not_running") {
        appendLog("代理未运行，配置将在下次启动时生效")
      } else {
        appendLog("已应用当前配置组到运行中代理")
      }
      return true
    }

    if (message === "global_config_missing") {
      appendLog("应用代理配置失败：请先完善全局配置")
      return false
    }
    if (message === "config_group_missing") {
      appendLog("应用代理配置失败：没有可用的配置组")
      return false
    }
    if (message === "config_invalid") {
      appendLog("应用代理配置失败：当前配置组无效")
      return false
    }

    appendLog("应用代理配置失败")
    return false
  }

  const runProxyStop = async () => {
    const result = await api.proxyStop()
    return applyInvokeResult(result, "停止代理服务器")
  }

  const runProxyCheckNetwork = async () => {
    const result = await api.proxyCheckNetwork()
    return applyInvokeResult(result, "检查网络环境")
  }

  const runProxyStartAll = async () => {
    if (isBundledRuntime()) {
      const ok = await api.startProxyStepChannel(handleProxyStep, {
        reset: true,
        startFromLatest: true,
      })
      if (!ok) {
        appendLog("⚠️ proxy-step channel 启动失败，自动导航不可用")
      }
    }
    const result = await api.proxyStartAll(buildProxyPayload())
    navigateProxyMissingConfigPanel(result?.message)
    return applyInvokeResult(result, "一键启动全部服务")
  }

  const runConfigGroupTest = async (index: number) => {
    const result = await api.configGroupTest({ index })
    return applyInvokeResult(result, "配置组测活")
  }

  const fetchConfigGroupModels = async (payload: {
    api_url: string
    api_key?: string
    middle_route?: string
    model_id?: string
  }) => {
    const result = await api.configGroupModels(payload)
    const ok = applyInvokeResult(result, "获取模型列表")
    if (!ok || !result) {
      return null
    }
    return normalizeModelList(result.details?.["models"])
  }

  const runUserDataOpenDir = async () => {
    const result = await api.userDataOpenDir()
    return applyInvokeResult(result, "打开用户数据目录")
  }

  const runUserDataBackup = async () => {
    // 备份前先保存当前的前端配置到后端（如果有必要）
    // 但前端配置目前是存储在 localStorage 的，后端备份脚本主要是备份 user_data_dir 下的文件
    // 所以我们需要确保 localStorage 的关键配置也同步到了 user_data_dir 下的某个文件，或者备份脚本能包含它
    // 目前看代码，disableUpdatePopup 是存在 localStorage 的，而后端备份的是 user_data_dir
    // 这是一个架构问题：前端独有的配置没有下沉到后端文件系统

    // 临时方案：在调用备份前，将关键的前端配置写入到 user_data_dir/frontend_config.json
    // 但这需要后端提供一个写入接口，或者我们将配置合并到 mtga_config.yaml

    // 更好的方案：
    // 在 SettingsPanel 中，disableUpdatePopup 的 watcher 已经将其写入 localStorage
    // 我们可以在这里调用后端 API 将其保存到 config.yaml 中（需要后端支持）
    // 或者，由于时间紧迫，我们先尝试修复"还原后状态没变"的问题：
    // 还原操作会覆盖文件，但浏览器 localStorage 不会被后端还原操作修改！
    // 所以还原后，localStorage 里还是旧的配置。
    // 我们需要在还原成功后，清除或重置相关的 localStorage 项，或者从还原回来的文件中读取配置（如果配置被保存到了文件）

    // 鉴于目前 disableUpdatePopup 只存在 localStorage，它实际上没有被备份！
    // 这是一个功能缺失。
    // 修复计划：
    // 1. 修改 disableUpdatePopup 的存储方式，使其持久化到 config.yaml (后端)
    // 2. 或者在备份时，将 localStorage 内容发送给后端保存（复杂）

    // 既然用户提到 "备份还原以GitHub Token为例复原了"，说明后端文件备份是工作的。
    // "禁用自动更新弹窗开机自启动这些按钮的状态没有变化" -> 说明这些状态没有被正确备份/还原。
    // GitHub Token 是存在 config.yaml 的，所以能还原。
    // disableUpdatePopup 是存在 localStorage 的，所以不能还原（因为 localStorage 独立于后端文件系统）。
    // 开机自启动状态是系统注册表/启动项状态，也不是文件，所以还原文件不会改变自启动状态。

    // 针对 "禁用自动更新弹窗"：
    // 我们应该将其迁移到后端配置中，和 GitHub Token 一样存储在 mtga_config.yaml

    // 获取当前主题配置
    let currentThemeConfig = null
    try {
      const { loadThemeFromStorage } = await import("./themeConfig")
      currentThemeConfig = loadThemeFromStorage()
    } catch {
      // ignore
    }

    // 在执行备份前，先强制保存一次当前的所有配置到后端文件
    // 确保内存中的状态（包括主题、禁用弹窗等）都持久化到磁盘，这样备份文件才是最新的
    const clampedIndex = clampIndex(
      currentConfigIndex.value,
      configGroups.value.length
    )
    const payload: ConfigPayload = {
      config_groups: configGroups.value,
      current_config_index: clampedIndex,
      mapped_model_id: coerceText(mappedModelId.value),
      mtga_auth_key: coerceText(mtgaAuthKey.value),
      github_token: coerceText(githubToken.value),
      disable_update_popup: disableUpdatePopup.value,
      theme_config: currentThemeConfig || undefined,
    }
    await api.saveConfig(payload)

    const result = await api.userDataBackup()
    return applyInvokeResult(result, "备份用户数据")
  }

  const runUserDataRestoreLatest = async () => {
    const result = await api.userDataRestoreLatest()
    if (result && result.ok) {
      await loadConfig() // Reload config after restore
      await loadAppInfo() // Reload app info

      // 还原后，前端配置（如 disableUpdatePopup）会通过 loadConfig 从后端同步回来
      // 但自启动状态是系统级的，不会因为文件还原而改变。
      // 如果用户期望还原到备份时的自启动状态（比如备份时开启了自启动），这很难做到，因为备份文件里不包含自启动注册表信息。
      // 我们能做的是：确保还原后，界面状态与系统实际状态一致。

      // 触发一次自启动状态检查（如果在客户端环境）
      if (typeof window !== 'undefined') {
        const { useAutoStart } = await import("./useAutoStart")
        const { checkStatus } = useAutoStart()
        await checkStatus()
      }

      if (isRecord(result.details) && isRecord(result.details.restore_result)) {
        const backupName = coerceText(result.details.restore_result.backup_name)
        if (backupName) {
          applyInvokeResult(result, `已还原备份: ${backupName}`)
          return true
        }
      }
    }
    return applyInvokeResult(result, "还原用户数据")
  }

  const runUserDataClear = async () => {
    const result = await api.userDataClear()
    if (result && result.ok) {
      // 清除后，重新加载配置以重置前端状态（loadConfig 会处理空文件情况，返回默认值）
      await loadConfig()

      // 强制重置主题为默认
      try {
        const { applyThemeConfig, DEFAULT_THEME_CONFIG, saveThemeToStorage } = await import("./themeConfig")
        applyThemeConfig(DEFAULT_THEME_CONFIG)
        saveThemeToStorage(DEFAULT_THEME_CONFIG)
      } catch {
        // ignore
      }

      // 重新加载 AppInfo
      await loadAppInfo()
    }
    return applyInvokeResult(result, "清除用户数据")
  }

  const runCheckUpdates = async () => {
    const result = await api.checkUpdates()
    const ok = applyInvokeResult(result, "检查更新")
    if (!result || !isRecord(result.details)) {
      return ok
    }
    const updateResult = isRecord(result.details["update_result"])
      ? result.details["update_result"]
      : result.details
    const status = coerceText(updateResult["status"])
    if (status === "new_version") {
      hasNewVersion.value = true
      updateVersionLabel.value = coerceText(updateResult["latest_version"])
      updateNotesHtml.value = coerceText(updateResult["release_notes"])
      updateReleaseUrl.value = coerceText(updateResult["release_url"])
      updateDialogOpen.value = true
    } else if (status === "up_to_date") {
      hasNewVersion.value = false
      const latestVersion = coerceText(updateResult["latest_version"])
      if (latestVersion) {
        appendLog(`已是最新版本：${latestVersion}`)
      }
    }
    return ok
  }

  const runCheckUpdatesOnce = async () => {
    if (updateAutoChecked.value) {
      return false
    }
    updateAutoChecked.value = true
    return runCheckUpdates()
  }

  const closeUpdateDialog = () => {
    updateDialogOpen.value = false
  }

  const openUpdateRelease = async () => {
    const url = updateReleaseUrl.value.trim()
    if (!url || typeof window === "undefined") {
      return
    }
    if (isTauriRuntime()) {
      try {
        const { open } = await import("@tauri-apps/plugin-shell")
        await open(url)
        return
      } catch (error) {
        console.warn("[mtga] open release url failed", error)
        appendLog("打开发布页失败，请手动复制链接")
        return
      }
    }
    const opened = window.open(url, "_blank", "noopener,noreferrer")
    if (!opened) {
      window.location.href = url
    }
  }

  const runPlaceholder = (label: string) => {
    appendLog(`${label}（待接入后端）`)
  }

  return {
    configGroups,
    currentConfigIndex,
    mappedModelId,
    mtgaAuthKey,
    githubToken,
    runtimeOptions,
    logs,
    logCursor,
    appInfo,
    hasNewVersion,
    disableUpdatePopup,
    updateDialogOpen,
    updateVersionLabel,
    updateNotesHtml,
    updateReleaseUrl,
    panelNavTarget,
    panelNavSignal,
    mainTabTarget,
    mainTabSignal,
    appendLog,
    startLogStream,
    stopLogStream,
    startProxyStepListener,
    stopProxyStepListener,
    loadConfig,
    saveConfig,
    init,
    runGenerateCertificates,
    runInstallCaCert,
    runClearCaCert,
    runHostsModify,
    runHostsOpen,
    runProxyStart,
    runProxyApplyCurrentConfig,
    runProxyStop,
    runProxyCheckNetwork,
    runProxyStartAll,
    runConfigGroupTest,
    fetchConfigGroupModels,
    runUserDataOpenDir,
    runUserDataBackup,
    runUserDataRestoreLatest,
    runUserDataClear,
    runCheckUpdates,
    runCheckUpdatesOnce,
    closeUpdateDialog,
    openUpdateRelease,
    runPlaceholder,
  }
}

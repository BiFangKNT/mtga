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

type OutboundProxyType = "http" | "https" | "socks4" | "socks5"

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

const OUTBOUND_PROXY_TYPES: OutboundProxyType[] = ["http", "https", "socks4", "socks5"]

const FRONTEND_LOG_LIMIT = 2000

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const coerceBoolean = (value: unknown) => {
  if (typeof value === "boolean") {
    return value
  }
  if (typeof value === "number") {
    return value !== 0
  }
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase()
    return ["1", "true", "yes", "on"].includes(normalized)
  }
  return false
}

const isMainTabKey = (value: unknown): value is MainTabKey =>
  value === "cert" || value === "hosts" || value === "proxy"

const isProxyStepStatus = (
  value: unknown
): value is ProxyStartStepEvent["status"] =>
  value === "ok" ||
  value === "skipped" ||
  value === "failed" ||
  value === "started"

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

const normalizeProxyType = (value: unknown): OutboundProxyType => {
  const normalized = coerceText(value).trim().toLowerCase()
  if (normalized === "http") return "http"
  if (normalized === "https") return "https"
  if (normalized === "socks4") return "socks4"
  if (normalized === "socks5") return "socks5"
  return "http"
}

const normalizeProxyPort = (value: unknown) => {
  if (typeof value === "number" && Number.isFinite(value)) {
    return String(value)
  }
  if (typeof value === "string") {
    return value
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
  const outboundProxyEnabled = useState<boolean>("mtga-outbound-proxy-enabled", () => false)
  const outboundProxyType = useState<OutboundProxyType>("mtga-outbound-proxy-type", () => "http")
  const outboundProxyHost = useState<string>("mtga-outbound-proxy-host", () => "")
  const outboundProxyPort = useState<string>("mtga-outbound-proxy-port", () => "")
  const outboundProxyUsername = useState<string>("mtga-outbound-proxy-username", () => "")
  const outboundProxyPassword = useState<string>("mtga-outbound-proxy-password", () => "")
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
    outboundProxyEnabled.value = coerceBoolean(result.outbound_proxy_enabled)
    outboundProxyType.value = normalizeProxyType(result.outbound_proxy_type)
    outboundProxyHost.value = coerceText(result.outbound_proxy_host)
    outboundProxyPort.value = normalizeProxyPort(result.outbound_proxy_port)
    outboundProxyUsername.value = coerceText(result.outbound_proxy_username)
    outboundProxyPassword.value = coerceText(result.outbound_proxy_password)
    return true
  }

  const saveConfig = async () => {
    const clampedIndex = clampIndex(
      currentConfigIndex.value,
      configGroups.value.length
    )
    currentConfigIndex.value = clampedIndex
    const parsedProxyPort = Number.parseInt(outboundProxyPort.value, 10)
    const proxyPortValue = Number.isFinite(parsedProxyPort) ? parsedProxyPort : 0
    const payload: ConfigPayload = {
      config_groups: configGroups.value,
      current_config_index: clampedIndex,
      mapped_model_id: coerceText(mappedModelId.value),
      mtga_auth_key: coerceText(mtgaAuthKey.value),
      outbound_proxy_enabled: outboundProxyEnabled.value,
      outbound_proxy_type: outboundProxyType.value,
      outbound_proxy_host: coerceText(outboundProxyHost.value),
      outbound_proxy_port: proxyPortValue,
      outbound_proxy_username: coerceText(outboundProxyUsername.value),
      outbound_proxy_password: coerceText(outboundProxyPassword.value),
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
    return applyInvokeResult(result, "启动代理服务器")
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
    const result = await api.userDataBackup()
    return applyInvokeResult(result, "备份用户数据")
  }

  const runUserDataRestoreLatest = async () => {
    const result = await api.userDataRestoreLatest()
    return applyInvokeResult(result, "还原用户数据")
  }

  const runUserDataClear = async () => {
    const result = await api.userDataClear()
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
    outboundProxyEnabled,
    outboundProxyType,
    outboundProxyHost,
    outboundProxyPort,
    outboundProxyUsername,
    outboundProxyPassword,
    outboundProxyTypes: OUTBOUND_PROXY_TYPES,
    runtimeOptions,
    logs,
    logCursor,
    appInfo,
    hasNewVersion,
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

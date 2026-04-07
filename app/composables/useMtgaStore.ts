import { useMtgaApi } from "./useMtgaApi";
import { listen } from "@tauri-apps/api/event";
import { isBundledRuntime, isTauriRuntime } from "./runtime";
import type {
  AppInfo,
  ConfigGroup,
  ConfigGroupModelsResult,
  ConfigPayload,
  InvokeResult,
  LazyWarmupEventPayload,
  LogEventPayload,
  LogPullResult,
  MainTabKey,
  ProxyStartStepEvent,
  SystemPromptItem,
} from "./mtgaTypes";

type RuntimeOptions = {
  debugMode: boolean;
  disableSslStrict: boolean;
  forceStream: boolean;
  streamMode: "true" | "false";
};

type PanelTarget = "config-group" | "global-config" | "main-tabs" | "system-prompts" | "settings";
type LazyWarmupStatus = "idle" | "running" | "done" | "error";

const DEFAULT_APP_INFO: AppInfo = {
  display_name: "MTGA",
  version: "v0.0.0",
  github_repo: "",
  ca_common_name: "MTGA_CA",
  api_key_visible_chars: 4,
  user_data_dir: "",
  default_user_data_dir: "",
};

const DEFAULT_RUNTIME_OPTIONS: RuntimeOptions = {
  debugMode: false,
  disableSslStrict: false,
  forceStream: false,
  streamMode: "true",
};

const FRONTEND_LOG_LIMIT = 2000;
const LAZY_WARMUP_SHOW_DELAY_MS = 120;
const LAZY_WARMUP_DONE_PEEK_MS = 960;
const LAZY_WARMUP_HIDE_MS = 850;
const LAZY_WARMUP_ERROR_HIDE_MS = 2200;
const LAZY_WARMUP_MIN_VISIBLE_MS = 640;
const LAZY_WARMUP_POLL_INTERVAL_MS = 220;
const LAZY_WARMUP_POLL_TIMEOUT_MS = 15000;

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const isMainTabKey = (value: unknown): value is MainTabKey =>
  value === "cert" || value === "hosts" || value === "proxy";

const isProxyStepStatus = (value: unknown): value is ProxyStartStepEvent["status"] =>
  value === "ok" || value === "skipped" || value === "failed" || value === "started";

const isPanelTarget = (value: unknown): value is PanelTarget =>
  value === "config-group" ||
  value === "global-config" ||
  value === "main-tabs" ||
  value === "system-prompts" ||
  value === "settings";

const isProxyStartStepEvent = (value: unknown): value is ProxyStartStepEvent => {
  if (!isRecord(value)) {
    return false;
  }
  return isMainTabKey(value.step) && isProxyStepStatus(value.status);
};

const normalizeProxyStepPayload = (payload: unknown): ProxyStartStepEvent | null => {
  if (isProxyStartStepEvent(payload)) {
    return payload;
  }
  if (typeof payload === "string") {
    try {
      const parsed = JSON.parse(payload);
      if (isProxyStartStepEvent(parsed)) {
        return parsed;
      }
    } catch {
      return null;
    }
  }
  return null;
};

const coerceText = (value: unknown) => {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    return String(value);
  }
  if (isRecord(value)) {
    const candidates = [value["id"], value["value"], value["model_id"]];
    for (const candidate of candidates) {
      if (typeof candidate === "string") {
        return candidate;
      }
    }
  }
  return "";
};

const isLazyWarmupPhase = (value: unknown): value is LazyWarmupEventPayload["phase"] =>
  value === "start" || value === "progress" || value === "done" || value === "error";

const normalizeLazyWarmupPayload = (payload: unknown): LazyWarmupEventPayload | null => {
  if (!isRecord(payload) || !isLazyWarmupPhase(payload.phase)) {
    return null;
  }
  const completed = Number(payload.completed);
  const total = Number(payload.total);
  return {
    phase: payload.phase,
    stage: coerceText(payload.stage) || null,
    label: coerceText(payload.label) || null,
    detail: coerceText(payload.detail) || null,
    completed: Number.isFinite(completed) ? Math.max(0, completed) : 0,
    total: Number.isFinite(total) ? Math.max(0, total) : 0,
    error_message: coerceText(payload.error_message) || null,
  };
};

const normalizeModelList = (value: unknown) => {
  if (!Array.isArray(value)) {
    return [];
  }
  const unique = new Set<string>();
  value.forEach((item) => {
    const text = coerceText(item).trim();
    if (text) {
      unique.add(text);
    }
  });
  return Array.from(unique).sort((a, b) => a.localeCompare(b));
};

const normalizeSystemPromptList = (value: unknown): SystemPromptItem[] => {
  if (!Array.isArray(value)) {
    return [];
  }
  const normalized: SystemPromptItem[] = [];
  value.forEach((item) => {
    if (!isRecord(item)) {
      return;
    }
    const hash = coerceText(item["hash"]).trim();
    const originalText = coerceText(item["original_text"]);
    const createdAt = coerceText(item["created_at"]);
    if (!hash || !createdAt) {
      return;
    }

    const nextItem: SystemPromptItem = {
      hash,
      original_text: originalText,
      created_at: createdAt,
    };

    const latestDeltaRaw = item["latest_delta"];
    if (isRecord(latestDeltaRaw)) {
      const editedAt = coerceText(latestDeltaRaw["edited_at"]);
      const editor = coerceText(latestDeltaRaw["editor"]);
      const nextDelta: SystemPromptDelta = {
        edited_at: editedAt,
        ...(editor ? { editor } : {}),
      };
      const hasEditedText = Object.prototype.hasOwnProperty.call(latestDeltaRaw, "edited_text");
      const editedTextRaw = latestDeltaRaw["edited_text"];
      if (hasEditedText && typeof editedTextRaw === "string") {
        nextDelta.edited_text = editedTextRaw;
      }
      nextItem.latest_delta = nextDelta;
    }
    normalized.push(nextItem);
  });
  return normalized;
};

const clampIndex = (value: number, max: number) => {
  if (max <= 0) {
    return 0;
  }
  return Math.min(Math.max(value, 0), max - 1);
};

export const useMtgaStore = () => {
  const api = useMtgaApi();

  const configGroups = useState<ConfigGroup[]>("mtga-config-groups", () => []);
  const currentConfigIndex = useState<number>("mtga-current-config-index", () => 0);
  const mappedModelId = useState<string>("mtga-mapped-model-id", () => "");
  const mtgaAuthKey = useState<string>("mtga-auth-key", () => "");
  const runtimeOptions = useState<RuntimeOptions>("mtga-runtime-options", () => ({
    ...DEFAULT_RUNTIME_OPTIONS,
  }));
  const logs = useState<string[]>("mtga-logs", () => []);
  const systemPrompts = useState<SystemPromptItem[]>("mtga-system-prompts", () => []);
  const logCursor = useState<number>("mtga-log-cursor", () => 0);
  const logStreamActive = useState<boolean>("mtga-log-stream-active", () => false);
  const appInfo = useState<AppInfo>("mtga-app-info", () => ({ ...DEFAULT_APP_INFO }));
  const initialized = useState<boolean>("mtga-initialized", () => false);
  const hasNewVersion = useState<boolean>("mtga-has-new-version", () => false);
  const updateDialogOpen = useState<boolean>("mtga-update-dialog-open", () => false);
  const updateVersionLabel = useState<string>("mtga-update-version-label", () => "");
  const updateNotesHtml = useState<string>("mtga-update-notes-html", () => "");
  const updateReleaseUrl = useState<string>("mtga-update-release-url", () => "");
  const updateAutoChecked = useState<boolean>("mtga-update-auto-checked", () => false);
  const panelNavTarget = useState<string | null>("mtga-panel-nav-target", () => null);
  const panelNavSignal = useState<number>("mtga-panel-nav-signal", () => 0);
  const mainTabTarget = useState<MainTabKey | null>("mtga-main-tab-target", () => null);
  const mainTabSignal = useState<number>("mtga-main-tab-signal", () => 0);
  const proxyStepListenerActive = useState<boolean>("mtga-proxy-step-listener-active", () => false);
  const proxyStepQueue = useState<MainTabKey[]>("mtga-proxy-step-queue", () => []);
  const proxyStepProcessing = useState<boolean>("mtga-proxy-step-processing", () => false);
  const lazyWarmupStatus = useState<LazyWarmupStatus>("mtga-lazy-warmup-status", () => "idle");
  const lazyWarmupVisible = useState<boolean>("mtga-lazy-warmup-visible", () => false);
  const lazyWarmupLabel = useState<string>("mtga-lazy-warmup-label", () => "");
  const lazyWarmupDetail = useState<string>("mtga-lazy-warmup-detail", () => "");
  const lazyWarmupCompleted = useState<number>("mtga-lazy-warmup-completed", () => 0);
  const lazyWarmupTotal = useState<number>("mtga-lazy-warmup-total", () => 0);
  const lazyWarmupRequested = useState<boolean>("mtga-lazy-warmup-requested", () => false);
  const lazyWarmupListenerActive = useState<boolean>(
    "mtga-lazy-warmup-listener-active",
    () => false,
  );

  let logPollTimer: ReturnType<typeof setTimeout> | null = null;
  let logEventUnlisten: (() => void) | null = null;
  let proxyStepUnlisten: (() => void) | null = null;
  let lazyWarmupShowTimer: ReturnType<typeof setTimeout> | null = null;
  let lazyWarmupHideTimer: ReturnType<typeof setTimeout> | null = null;
  let lazyWarmupPollTimer: ReturnType<typeof setTimeout> | null = null;
  let lazyWarmupUnlisten: (() => void) | null = null;
  let lazyWarmupVisibilityCleanup: (() => void) | null = null;
  let lazyWarmupShownAt = 0;
  let lazyWarmupPollSession = 0;

  const drainProxyStepQueue = async () => {
    if (proxyStepProcessing.value) {
      return;
    }
    proxyStepProcessing.value = true;
    while (proxyStepQueue.value.length) {
      const step = proxyStepQueue.value.shift();
      if (!step) {
        continue;
      }
      panelNavTarget.value = "main-tabs";
      panelNavSignal.value += 1;
      mainTabTarget.value = step;
      mainTabSignal.value += 1;
      await nextTick();
      await new Promise((resolve) => setTimeout(resolve, 240));
    }
    proxyStepProcessing.value = false;
  };

  const enqueueProxyStep = (step: MainTabKey) => {
    proxyStepQueue.value.push(step);
    void drainProxyStepQueue();
  };

  const navigateProxyMissingConfigPanel = (message?: string | null) => {
    const normalized = (message || "").trim();
    if (!normalized) {
      return;
    }
    if (normalized.includes("全局配置缺失") || normalized === "global_config_missing") {
      panelNavTarget.value = "global-config";
      panelNavSignal.value += 1;
      return;
    }
    if (normalized.includes("没有可用的配置组") || normalized === "config_group_missing") {
      panelNavTarget.value = "config-group";
      panelNavSignal.value += 1;
    }
  };

  const appendLog = (message: string) => {
    logs.value.push(message);
    const overflow = logs.value.length - FRONTEND_LOG_LIMIT;
    if (overflow > 0) {
      logs.value.splice(0, overflow);
    }
  };

  const handleProxyStep = (payload: unknown) => {
    const normalized = normalizeProxyStepPayload(payload);
    if (!normalized || !isMainTabKey(normalized.step)) {
      return;
    }
    if (isPanelTarget(normalized.panel_target)) {
      panelNavTarget.value = normalized.panel_target;
      panelNavSignal.value += 1;
    } else {
      navigateProxyMissingConfigPanel(normalized.message);
    }
    if (normalized.status === "started") {
      enqueueProxyStep(normalized.step);
    }
  };

  const appendLogs = (entries?: string[]) => {
    if (!entries || !entries.length) {
      return;
    }
    entries.forEach((entry) => appendLog(entry));
  };

  const applyInvokeResult = (result: InvokeResult | null, fallbackMessage: string) => {
    if (!result) {
      appendLog(`${fallbackMessage}失败：无法连接后端`);
      return false;
    }
    if (result.message) {
      appendLog(result.message);
    }
    return result.ok;
  };

  const startLogStream = () => {
    if (logStreamActive.value) {
      return;
    }
    logStreamActive.value = true;
    if (logEventUnlisten) {
      try {
        logEventUnlisten();
      } catch {
        // ignore cleanup errors
      }
      logEventUnlisten = null;
    }
    if (logPollTimer !== null) {
      clearTimeout(logPollTimer);
      logPollTimer = null;
    }

    const applyLogResult = (result: LogPullResult | null) => {
      if (!result) {
        return;
      }
      if (Array.isArray(result.items) && result.items.length) {
        appendLogs(result.items);
      }
      if (typeof result.next_id === "number") {
        logCursor.value = result.next_id;
      }
    };

    const startPolling = () => {
      const loop = async () => {
        if (!logStreamActive.value) {
          return;
        }
        const result = await api.pullLogs({
          after_id: logCursor.value || null,
          timeout_ms: 0,
          max_items: 200,
        });
        if (!logStreamActive.value) {
          return;
        }
        applyLogResult(result);
        logPollTimer = setTimeout(loop, 200);
      };
      void loop();
    };

    const startEventStream = async () => {
      if (!isTauriRuntime()) {
        startPolling();
        return;
      }

      const initial = await api.pullLogs({
        after_id: logCursor.value || null,
        timeout_ms: 0,
        max_items: 200,
      });
      applyLogResult(initial);

      try {
        const unlisten = await listen<LogEventPayload>("mtga:logs", (event) => {
          const payload = event.payload;
          if (!payload) {
            return;
          }
          if (Array.isArray(payload.items) && payload.items.length) {
            appendLogs(payload.items);
          }
          if (typeof payload.next_id === "number") {
            logCursor.value = payload.next_id;
          }
        });
        if (!logStreamActive.value) {
          try {
            unlisten();
          } catch {
            // ignore cleanup errors
          }
          return;
        }
        logEventUnlisten = () => {
          void unlisten();
        };
      } catch (error) {
        console.warn("[mtga] log event listen failed", error);
        startPolling();
      }
    };

    void startEventStream();
  };

  const stopLogStream = () => {
    logStreamActive.value = false;
    if (logPollTimer !== null) {
      clearTimeout(logPollTimer);
      logPollTimer = null;
    }
    if (logEventUnlisten) {
      try {
        logEventUnlisten();
      } catch {
        // ignore cleanup errors
      }
      logEventUnlisten = null;
    }
  };

  const startProxyStepListener = () => {
    if (proxyStepListenerActive.value) {
      return;
    }
    proxyStepListenerActive.value = true;
    if (proxyStepUnlisten) {
      try {
        proxyStepUnlisten();
      } catch {
        // ignore cleanup errors
      }
      proxyStepUnlisten = null;
    }

    if (isBundledRuntime()) {
      return;
    }

    const listenProxySteps = async () => {
      try {
        const unlisten = await listen<ProxyStartStepEvent>("mtga:proxy-step", (event) => {
          handleProxyStep(event.payload);
        });
        if (!proxyStepListenerActive.value) {
          try {
            unlisten();
          } catch {
            // ignore cleanup errors
          }
          return;
        }
        proxyStepUnlisten = () => {
          void unlisten();
        };
      } catch (error) {
        console.warn("[mtga] proxy step listen failed", error);
      }
    };

    void listenProxySteps();
  };

  const stopProxyStepListener = () => {
    proxyStepListenerActive.value = false;
    if (proxyStepUnlisten) {
      try {
        proxyStepUnlisten();
      } catch {
        // ignore cleanup errors
      }
      proxyStepUnlisten = null;
    }
  };

  const clearLazyWarmupShowTimer = () => {
    if (lazyWarmupShowTimer !== null) {
      clearTimeout(lazyWarmupShowTimer);
      lazyWarmupShowTimer = null;
    }
  };

  const clearLazyWarmupHideTimer = () => {
    if (lazyWarmupHideTimer !== null) {
      clearTimeout(lazyWarmupHideTimer);
      lazyWarmupHideTimer = null;
    }
  };

  const clearLazyWarmupPollTimer = () => {
    if (lazyWarmupPollTimer !== null) {
      clearTimeout(lazyWarmupPollTimer);
      lazyWarmupPollTimer = null;
    }
  };

  const clearLazyWarmupVisibilityCleanup = () => {
    if (lazyWarmupVisibilityCleanup) {
      lazyWarmupVisibilityCleanup();
      lazyWarmupVisibilityCleanup = null;
    }
  };

  const stopLazyWarmupPolling = () => {
    lazyWarmupPollSession += 1;
    clearLazyWarmupPollTimer();
  };

  const scheduleLazyWarmupHudShow = () => {
    clearLazyWarmupHideTimer();
    if (lazyWarmupVisible.value || lazyWarmupShowTimer !== null) {
      return;
    }
    lazyWarmupShowTimer = setTimeout(() => {
      lazyWarmupShowTimer = null;
      if (lazyWarmupStatus.value === "running" || lazyWarmupStatus.value === "done") {
        lazyWarmupShownAt = Date.now();
        lazyWarmupVisible.value = true;
      }
    }, LAZY_WARMUP_SHOW_DELAY_MS);
  };

  const scheduleLazyWarmupHudHide = (delay = LAZY_WARMUP_HIDE_MS) => {
    clearLazyWarmupShowTimer();
    clearLazyWarmupHideTimer();
    const elapsed = lazyWarmupShownAt > 0 ? Date.now() - lazyWarmupShownAt : 0;
    const nextDelay =
      lazyWarmupVisible.value && elapsed < LAZY_WARMUP_MIN_VISIBLE_MS
        ? Math.max(delay, LAZY_WARMUP_MIN_VISIBLE_MS - elapsed)
        : delay;
    lazyWarmupHideTimer = setTimeout(() => {
      lazyWarmupHideTimer = null;
      lazyWarmupVisible.value = false;
      lazyWarmupShownAt = 0;
    }, nextDelay);
  };

  const showLazyWarmupHudNow = () => {
    clearLazyWarmupShowTimer();
    clearLazyWarmupHideTimer();
    lazyWarmupShownAt = Date.now();
    lazyWarmupVisible.value = true;
  };

  const handleLazyWarmupEvent = (payload: unknown) => {
    const normalized = normalizeLazyWarmupPayload(payload);
    if (!normalized) {
      return;
    }

    lazyWarmupCompleted.value = normalized.completed;
    lazyWarmupTotal.value = normalized.total;

    if (normalized.phase === "start" || normalized.phase === "progress") {
      lazyWarmupStatus.value = "running";
      lazyWarmupLabel.value = normalized.label || "正在准备后台能力";
      lazyWarmupDetail.value = normalized.detail || "常用功能将在后台完成预热";
      if (normalized.phase === "progress" && normalized.completed > 0 && !lazyWarmupVisible.value) {
        showLazyWarmupHudNow();
      } else {
        scheduleLazyWarmupHudShow();
      }
      return;
    }

    if (normalized.phase === "done") {
      lazyWarmupStatus.value = "done";
      lazyWarmupCompleted.value = normalized.total;
      lazyWarmupLabel.value = normalized.label || "后台能力已就绪";
      lazyWarmupDetail.value = normalized.detail || "常用功能预热完成";
      stopLazyWarmupPolling();
      if (lazyWarmupVisible.value) {
        scheduleLazyWarmupHudHide();
      } else {
        showLazyWarmupHudNow();
        scheduleLazyWarmupHudHide(LAZY_WARMUP_DONE_PEEK_MS);
      }
      return;
    }

    lazyWarmupStatus.value = "error";
    lazyWarmupLabel.value = normalized.label || "后台预热失败";
    lazyWarmupDetail.value =
      normalized.error_message || normalized.detail || "部分能力仍会在首次使用时按需加载";
    stopLazyWarmupPolling();
    showLazyWarmupHudNow();
    scheduleLazyWarmupHudHide(LAZY_WARMUP_ERROR_HIDE_MS);
  };

  const startLazyWarmupPolling = () => {
    if (!isTauriRuntime()) {
      return;
    }

    stopLazyWarmupPolling();
    const session = lazyWarmupPollSession;
    const deadline = Date.now() + LAZY_WARMUP_POLL_TIMEOUT_MS;

    const loop = async () => {
      if (session !== lazyWarmupPollSession || !lazyWarmupRequested.value) {
        return;
      }

      const payload = await api.getLazyWarmupStatus();
      if (session !== lazyWarmupPollSession) {
        return;
      }

      if (payload) {
        handleLazyWarmupEvent(payload);
      }

      if (
        lazyWarmupStatus.value === "done" ||
        lazyWarmupStatus.value === "error" ||
        Date.now() >= deadline
      ) {
        clearLazyWarmupPollTimer();
        return;
      }

      lazyWarmupPollTimer = setTimeout(loop, LAZY_WARMUP_POLL_INTERVAL_MS);
    };

    void loop();
  };

  const startLazyWarmupListener = () => {
    if (lazyWarmupListenerActive.value) {
      return;
    }
    lazyWarmupListenerActive.value = true;
    if (lazyWarmupUnlisten) {
      try {
        lazyWarmupUnlisten();
      } catch {
        // ignore cleanup errors
      }
      lazyWarmupUnlisten = null;
    }

    if (!isTauriRuntime()) {
      return;
    }

    const listenLazyWarmup = async () => {
      try {
        const unlisten = await listen<LazyWarmupEventPayload>("mtga:lazy-warmup", (event) => {
          handleLazyWarmupEvent(event.payload);
        });
        if (!lazyWarmupListenerActive.value) {
          try {
            unlisten();
          } catch {
            // ignore cleanup errors
          }
          return;
        }
        lazyWarmupUnlisten = () => {
          void unlisten();
        };
      } catch (error) {
        console.warn("[mtga] lazy warmup listen failed", error);
      }
    };

    void listenLazyWarmup();
  };

  const stopLazyWarmupListener = () => {
    lazyWarmupListenerActive.value = false;
    clearLazyWarmupShowTimer();
    clearLazyWarmupHideTimer();
    stopLazyWarmupPolling();
    clearLazyWarmupVisibilityCleanup();
    lazyWarmupShownAt = 0;
    if (lazyWarmupUnlisten) {
      try {
        lazyWarmupUnlisten();
      } catch {
        // ignore cleanup errors
      }
      lazyWarmupUnlisten = null;
    }
  };

  const scheduleLazyWarmup = () => {
    if (!isTauriRuntime() || typeof window === "undefined") {
      return;
    }

    if (lazyWarmupRequested.value) {
      void api.startLazyWarmup();
      startLazyWarmupPolling();
      return;
    }

    const launchWarmup = () => {
      if (lazyWarmupRequested.value) {
        return;
      }
      clearLazyWarmupVisibilityCleanup();
      window.requestAnimationFrame(() => {
        window.setTimeout(() => {
          if (lazyWarmupRequested.value) {
            return;
          }
          lazyWarmupRequested.value = true;
          void api.startLazyWarmup().then((ok) => {
            if (!ok) {
              lazyWarmupRequested.value = false;
              stopLazyWarmupPolling();
              return;
            }
            startLazyWarmupPolling();
          });
        }, 120);
      });
    };

    if (document.visibilityState === "visible") {
      launchWarmup();
      return;
    }

    const handleVisibilityChange = () => {
      if (document.visibilityState !== "visible") {
        return;
      }
      launchWarmup();
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    lazyWarmupVisibilityCleanup = () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  };

  const loadConfig = async () => {
    const result = await api.loadConfig();
    if (!result) {
      return false;
    }
    configGroups.value = result.config_groups || [];
    currentConfigIndex.value = clampIndex(
      result.current_config_index ?? 0,
      configGroups.value.length,
    );
    mappedModelId.value = coerceText(result.mapped_model_id);
    mtgaAuthKey.value = coerceText(result.mtga_auth_key);
    if (Array.isArray(result.warnings)) {
      result.warnings.forEach((warning) => {
        const text = coerceText(warning).trim();
        if (text) {
          appendLog(text);
        }
      });
    }
    return true;
  };

  const saveConfig = async () => {
    const clampedIndex = clampIndex(currentConfigIndex.value, configGroups.value.length);
    currentConfigIndex.value = clampedIndex;
    const payload: ConfigPayload = {
      config_groups: configGroups.value,
      current_config_index: clampedIndex,
      mapped_model_id: coerceText(mappedModelId.value),
      mtga_auth_key: coerceText(mtgaAuthKey.value),
    };
    const ok = await api.saveConfig(payload);
    return Boolean(ok);
  };

  const loadAppInfo = async () => {
    const info = await api.getAppInfo();
    if (!info) {
      return false;
    }
    appInfo.value = {
      ...DEFAULT_APP_INFO,
      ...info,
    };
    return true;
  };

  const buildStartupLogs = (details: Record<string, unknown>) => {
    const envOk = details["env_ok"] === true;
    const envMessage = coerceText(details["env_message"]);
    if (envMessage) {
      appendLog(`${envOk ? "✅" : "❌"} ${envMessage}`);
    }
    if (envOk) {
      const runtime = coerceText(details["runtime"]);
      if (runtime === "tauri" || runtime === "nuitka") {
        appendLog("📦 运行在打包环境中");
      } else {
        appendLog("🔧 运行在开发环境中");
      }
    }

    const allowFlag = coerceText(details["allow_unsafe_hosts_flag"]) || "--allow-unsafe-hosts";
    const hostsModifyBlocked = details["hosts_modify_blocked"] === true;
    if (hostsModifyBlocked) {
      const status = coerceText(details["hosts_modify_block_status"]) || "unknown";
      appendLog(
        `⚠️ 检测到 hosts 文件写入受限（status=${status}），已启用受限 hosts 模式：添加将回退为追加写入（无法保证原子性增删/去重），自动移除/还原将被禁用。`,
      );
      appendLog(
        `⚠️ 你可以点击「打开hosts文件」手动修改；或使用启动参数 ${allowFlag} 覆盖此检查以强制尝试原子写入（风险自负）。`,
      );
    } else {
      const preflightOk = details["hosts_preflight_ok"] === true;
      const preflightStatus = coerceText(details["hosts_preflight_status"]);
      if (preflightStatus && !preflightOk) {
        appendLog(
          `⚠️ hosts 预检未通过（status=${preflightStatus}），但已使用启动参数 ${allowFlag} 覆盖；后续自动修改可能失败。`,
        );
      }
    }

    if (details["explicit_proxy_detected"] === true) {
      appendLog(
        "⚠️".repeat(21) + "\n检测到显式代理配置：部分应用可能优先走代理，从而绕过 hosts 导流。",
      );
      appendLog("建议：1. 关闭显式代理（如clash的系统代理），或改用 TUN/VPN");
      appendLog("      2. 检查 Trae 的代理设置。\n" + "⚠️".repeat(21));
    }

    if (details["legacy_user_data_dir_detected"] === true) {
      const legacyDir = coerceText(details["legacy_user_data_dir"]);
      appendLog(
        `⚠️ 检测到旧版用户数据目录${legacyDir ? `：${legacyDir}` : ""}。当前版本已不再使用该目录，如需保留旧配置、证书或备份，请手动迁移到新的用户数据目录。`,
      );
    }

    appendLog("MTGA 已启动");
    appendLog("请选择操作或直接使用一键启动...");
  };

  const loadStartupStatus = async () => {
    const result = await api.getStartupStatus();
    if (!result) {
      appendLog("启动日志加载失败：无法连接后端");
      return false;
    }
    if (isRecord(result.details)) {
      buildStartupLogs(result.details);
    }
    return result.ok;
  };

  const init = async () => {
    if (initialized.value) {
      startLogStream();
      startProxyStepListener();
      startLazyWarmupListener();
      scheduleLazyWarmup();
      return;
    }
    initialized.value = true;
    startLogStream();
    startProxyStepListener();
    startLazyWarmupListener();
    await Promise.all([loadAppInfo(), loadConfig(), loadStartupStatus()]);
    scheduleLazyWarmup();
  };

  const buildProxyPayload = () => ({
    debug_mode: runtimeOptions.value.debugMode,
    disable_ssl_strict_mode: runtimeOptions.value.disableSslStrict,
    force_stream: runtimeOptions.value.forceStream,
    stream_mode: runtimeOptions.value.streamMode,
  });

  const runGenerateCertificates = async () => {
    const result = await api.generateCertificates();
    return applyInvokeResult(result, "生成证书");
  };

  const runInstallCaCert = async () => {
    const result = await api.installCaCert();
    return applyInvokeResult(result, "安装 CA 证书");
  };

  const runClearCaCert = async (caCommonName?: string) => {
    const normalizedCaCommonName = caCommonName?.trim();
    const result = await api.clearCaCert(
      normalizedCaCommonName ? { ca_common_name: normalizedCaCommonName } : {},
    );
    return applyInvokeResult(result, "清除 CA 证书");
  };

  const runHostsModify = async (mode: "add" | "backup" | "restore" | "remove") => {
    const result = await api.hostsModify({ mode });
    return applyInvokeResult(result, "hosts 操作");
  };

  const runHostsOpen = async () => {
    const result = await api.hostsOpen();
    return applyInvokeResult(result, "打开 hosts 文件");
  };

  const runProxyStart = async () => {
    const result = await api.proxyStart(buildProxyPayload());
    navigateProxyMissingConfigPanel(result?.message);
    return applyInvokeResult(result, "启动代理服务器");
  };

  const runProxyApplyCurrentConfig = async () => {
    const result = await api.proxyApplyCurrentConfig(buildProxyPayload());
    navigateProxyMissingConfigPanel(result?.message);
    if (!result) {
      appendLog("应用代理配置失败：无法连接后端");
      return false;
    }

    const message = coerceText(result.message).trim();
    const applyStatus = isRecord(result.details) ? coerceText(result.details["apply_status"]) : "";

    if (result.ok) {
      if (applyStatus === "deferred" || message === "proxy_not_running") {
        appendLog("代理未运行，配置将在下次启动时生效");
      } else {
        appendLog("已应用当前配置组到运行中代理");
      }
      return true;
    }

    if (message === "global_config_missing") {
      appendLog("应用代理配置失败：请先完善全局配置");
      return false;
    }
    if (message === "config_group_missing") {
      appendLog("应用代理配置失败：没有可用的配置组");
      return false;
    }
    if (message === "config_invalid") {
      appendLog("应用代理配置失败：当前配置组无效");
      return false;
    }

    appendLog("应用代理配置失败");
    return false;
  };

  const runProxyStop = async () => {
    const result = await api.proxyStop();
    return applyInvokeResult(result, "停止代理服务器");
  };

  const runProxyCheckNetwork = async () => {
    const result = await api.proxyCheckNetwork();
    return applyInvokeResult(result, "检查网络环境");
  };

  const runProxyStartAll = async () => {
    if (isBundledRuntime()) {
      const ok = await api.startProxyStepChannel(handleProxyStep, {
        reset: true,
        startFromLatest: true,
      });
      if (!ok) {
        appendLog("⚠️ proxy-step channel 启动失败，自动导航不可用");
      }
    }
    const result = await api.proxyStartAll(buildProxyPayload());
    navigateProxyMissingConfigPanel(result?.message);
    return applyInvokeResult(result, "一键启动全部服务");
  };

  const runConfigGroupTest = async (index: number) => {
    const result = await api.configGroupTest({ index });
    return applyInvokeResult(result, "配置组测活");
  };

  const fetchConfigGroupModels = async (payload: {
    provider?: string;
    api_url: string;
    api_key?: string;
    middle_route?: string;
    model_id?: string;
  }): Promise<ConfigGroupModelsResult | null> => {
    const result = await api.configGroupModels(payload);
    const ok = applyInvokeResult(result, "获取模型列表");
    if (!ok || !result) {
      return null;
    }
    const strategyIdRaw = result.details?.["strategy_id"];
    const strategyId =
      typeof strategyIdRaw === "string" && strategyIdRaw.trim() ? strategyIdRaw.trim() : null;
    return {
      models: normalizeModelList(result.details?.["models"]),
      strategyId,
    };
  };

  const runUserDataOpenDir = async () => {
    const result = await api.userDataOpenDir();
    return applyInvokeResult(result, "打开用户数据目录");
  };

  const runUserDataBackup = async () => {
    const result = await api.userDataBackup();
    return applyInvokeResult(result, "备份用户数据");
  };

  const runUserDataRestoreLatest = async () => {
    const result = await api.userDataRestoreLatest();
    return applyInvokeResult(result, "还原用户数据");
  };

  const runUserDataClear = async () => {
    const result = await api.userDataClear();
    return applyInvokeResult(result, "清除用户数据");
  };

  const runCheckUpdates = async () => {
    const result = await api.checkUpdates();
    const ok = applyInvokeResult(result, "检查更新");
    if (!result || !isRecord(result.details)) {
      return ok;
    }
    const updateResult = isRecord(result.details["update_result"])
      ? result.details["update_result"]
      : result.details;
    const status = coerceText(updateResult["status"]);
    if (status === "new_version") {
      hasNewVersion.value = true;
      updateVersionLabel.value = coerceText(updateResult["latest_version"]);
      updateNotesHtml.value = coerceText(updateResult["release_notes"]);
      updateReleaseUrl.value = coerceText(updateResult["release_url"]);
      updateDialogOpen.value = true;
    } else if (status === "up_to_date") {
      hasNewVersion.value = false;
      const latestVersion = coerceText(updateResult["latest_version"]);
      if (latestVersion) {
        appendLog(`已是最新版本：${latestVersion}`);
      }
    }
    return ok;
  };

  const loadSystemPrompts = async () => {
    const result = await api.systemPromptsList();
    const ok = applyInvokeResult(result, "加载系统提示词");
    if (!ok) {
      return false;
    }
    if (!result || !isRecord(result.details)) {
      systemPrompts.value = [];
      return true;
    }
    systemPrompts.value = normalizeSystemPromptList(result.details["items"]);
    return true;
  };

  const updateSystemPrompt = async (payload: { hash: string; edited_text: string }) => {
    const result = await api.systemPromptsUpdate(payload);
    const ok = applyInvokeResult(result, "更新系统提示词");
    if (!ok) {
      return false;
    }
    await loadSystemPrompts();
    return true;
  };

  const deleteSystemPrompts = async (payload: { hashes: string[] }) => {
    const normalizedHashes = payload.hashes
      .map((hash) => coerceText(hash).trim())
      .filter((hash) => hash.length > 0);
    if (!normalizedHashes.length) {
      appendLog("删除系统提示词失败：未提供有效 hash");
      return false;
    }
    const result = await api.systemPromptsDelete({ hashes: normalizedHashes });
    const ok = applyInvokeResult(result, "删除系统提示词");
    if (!ok) {
      return false;
    }
    await loadSystemPrompts();
    return true;
  };

  const runCheckUpdatesOnce = async () => {
    if (updateAutoChecked.value) {
      return false;
    }
    updateAutoChecked.value = true;
    return runCheckUpdates();
  };

  const closeUpdateDialog = () => {
    updateDialogOpen.value = false;
  };

  const openUpdateRelease = async () => {
    const url = updateReleaseUrl.value.trim();
    if (!url || typeof window === "undefined") {
      return;
    }
    if (isTauriRuntime()) {
      try {
        const { open } = await import("@tauri-apps/plugin-shell");
        await open(url);
        return;
      } catch (error) {
        console.warn("[mtga] open release url failed", error);
        appendLog("打开发布页失败，请手动复制链接");
        return;
      }
    }
    const opened = window.open(url, "_blank", "noopener,noreferrer");
    if (!opened) {
      window.location.href = url;
    }
  };

  const runPlaceholder = (label: string) => {
    appendLog(`${label}（待接入后端）`);
  };

  return {
    configGroups,
    currentConfigIndex,
    mappedModelId,
    mtgaAuthKey,
    runtimeOptions,
    logs,
    systemPrompts,
    logCursor,
    appInfo,
    hasNewVersion,
    updateDialogOpen,
    updateVersionLabel,
    updateNotesHtml,
    updateReleaseUrl,
    lazyWarmupStatus,
    lazyWarmupVisible,
    lazyWarmupLabel,
    lazyWarmupDetail,
    lazyWarmupCompleted,
    lazyWarmupTotal,
    panelNavTarget,
    panelNavSignal,
    mainTabTarget,
    mainTabSignal,
    appendLog,
    startLogStream,
    stopLogStream,
    startProxyStepListener,
    stopProxyStepListener,
    startLazyWarmupListener,
    stopLazyWarmupListener,
    scheduleLazyWarmup,
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
    loadSystemPrompts,
    updateSystemPrompt,
    deleteSystemPrompts,
    runPlaceholder,
  };
};

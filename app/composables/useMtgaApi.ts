import { Channel, invoke } from "@tauri-apps/api/core";
import { pyInvoke } from "tauri-plugin-pytauri-api";

import type {
  AppInfo,
  ConfigPayload,
  InvokeResult,
  LazyWarmupEventPayload,
  LogPullResult,
} from "./mtgaTypes";

type InvokePayload = Record<string, unknown>;

const canInvoke = () => typeof window !== "undefined";

const safeInvoke = async <T>(
  command: string,
  payload?: InvokePayload,
  fallback?: T,
): Promise<T | null> => {
  if (!canInvoke()) {
    return fallback ?? null;
  }
  try {
    return await pyInvoke(command, payload);
  } catch (error) {
    console.warn(`[mtga] invoke ${command} failed`, error);
    return fallback ?? null;
  }
};

export const useMtgaApi = () => {
  let proxyStepChannel: Channel<string> | null = null;
  type ProxyStepChannelOptions = {
    reset?: boolean;
    startFromLatest?: boolean;
  };
  const loadConfig = () => safeInvoke<ConfigPayload>("load_config");
  const saveConfig = (payload: ConfigPayload) => safeInvoke<boolean>("save_config", payload, false);
  const getAppInfo = () => safeInvoke<AppInfo>("get_app_info");
  const getStartupStatus = () => safeInvoke<InvokeResult>("startup_status");
  const startLazyWarmup = () => safeInvoke<boolean>("start_lazy_warmup", undefined, false);
  const getLazyWarmupStatus = () => safeInvoke<LazyWarmupEventPayload>("get_lazy_warmup_status");
  const hostsModify = (payload: {
    mode: "add" | "backup" | "restore" | "remove";
    domain?: string;
    ip?: string[] | string;
  }) => safeInvoke<InvokeResult>("hosts_modify", payload);
  const hostsOpen = () => safeInvoke<InvokeResult>("hosts_open");
  const generateCertificates = () => safeInvoke<InvokeResult>("generate_certificates");
  const installCaCert = () => safeInvoke<InvokeResult>("install_ca_cert");
  const clearCaCert = (payload: { ca_common_name?: string } = {}) =>
    safeInvoke<InvokeResult>("clear_ca_cert", payload);
  const proxyStart = (payload: {
    debug_mode: boolean;
    disable_ssl_strict_mode: boolean;
    force_stream: boolean;
    stream_mode?: string | null;
  }) => safeInvoke<InvokeResult>("proxy_start", payload);
  const proxyApplyCurrentConfig = (payload: {
    debug_mode: boolean;
    disable_ssl_strict_mode: boolean;
    force_stream: boolean;
    stream_mode?: string | null;
  }) => safeInvoke<InvokeResult>("proxy_apply_current_config", payload);
  const proxyStop = () => safeInvoke<InvokeResult>("proxy_stop");
  const proxyCheckNetwork = () => safeInvoke<InvokeResult>("proxy_check_network");
  const proxyStartAll = (payload: {
    debug_mode: boolean;
    disable_ssl_strict_mode: boolean;
    force_stream: boolean;
    stream_mode?: string | null;
  }) => safeInvoke<InvokeResult>("proxy_start_all", payload);
  const configGroupTest = (payload: { index: number; mode?: "chat" | "models" }) =>
    safeInvoke<InvokeResult>("config_group_test", payload);
  const configGroupModels = (payload: {
    provider?: string;
    api_url: string;
    api_key?: string;
    middle_route?: string;
    model_id?: string;
  }) => safeInvoke<InvokeResult>("config_group_models", payload);
  const userDataOpenDir = () => safeInvoke<InvokeResult>("user_data_open_dir");
  const userDataBackup = () => safeInvoke<InvokeResult>("user_data_backup");
  const userDataRestoreLatest = () => safeInvoke<InvokeResult>("user_data_restore_latest");
  const userDataClear = () => safeInvoke<InvokeResult>("user_data_clear");
  const checkUpdates = () => safeInvoke<InvokeResult>("check_updates");
  const systemPromptsList = () => safeInvoke<InvokeResult>("system_prompts_list");
  const systemPromptsUpdate = (payload: { hash: string; edited_text: string }) =>
    safeInvoke<InvokeResult>("system_prompts_update", payload);
  const systemPromptsDelete = (payload: { hashes: string[] }) =>
    safeInvoke<InvokeResult>("system_prompts_delete", payload);
  const pullLogs = (payload: {
    after_id?: number | null;
    timeout_ms?: number;
    max_items?: number;
  }) => safeInvoke<LogPullResult>("pull_logs_command", payload);

  const startProxyStepChannel = async (
    onMessage: (payload: unknown) => void,
    options?: ProxyStepChannelOptions,
  ): Promise<boolean> => {
    if (!canInvoke()) {
      return false;
    }
    try {
      if (proxyStepChannel && options?.reset) {
        proxyStepChannel.onmessage = () => {};
        proxyStepChannel = null;
      }
      if (proxyStepChannel) {
        proxyStepChannel.onmessage = onMessage;
        return true;
      }
      proxyStepChannel = new Channel<string>();
      proxyStepChannel.onmessage = onMessage;
      await invoke("proxy_step_channel", {
        channel: proxyStepChannel,
        start_from_latest: options?.startFromLatest ?? false,
      });
      return true;
    } catch (error) {
      proxyStepChannel = null;
      console.warn("[mtga] proxy step channel failed", error);
      return false;
    }
  };

  return {
    loadConfig,
    saveConfig,
    getAppInfo,
    getStartupStatus,
    startLazyWarmup,
    getLazyWarmupStatus,
    hostsModify,
    hostsOpen,
    generateCertificates,
    installCaCert,
    clearCaCert,
    proxyStart,
    proxyApplyCurrentConfig,
    proxyStop,
    proxyCheckNetwork,
    proxyStartAll,
    configGroupTest,
    configGroupModels,
    userDataOpenDir,
    userDataBackup,
    userDataRestoreLatest,
    userDataClear,
    checkUpdates,
    systemPromptsList,
    systemPromptsUpdate,
    systemPromptsDelete,
    pullLogs,
    startProxyStepChannel,
  };
};

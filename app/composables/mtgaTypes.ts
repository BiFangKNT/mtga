export type ProviderId = "openai_chat_completion" | "openai_response" | "anthropic" | "gemini";
export type ProxyMode = "reverse_hosts" | "trae_native" | "trae_official_base_url";

export type ConfigGroup = {
  name?: string;
  provider?: ProviderId;
  api_url: string;
  model_id: string;
  api_key: string;
  middle_route?: string;
  model_discovery_strategy?: string;
  prompt_cache_enabled?: boolean;
};

export type ConfigPayload = {
  config_groups: ConfigGroup[];
  current_config_index: number;
  mapped_model_id: string;
  mtga_auth_key: string;
  proxy_mode: ProxyMode;
  trae_path: string;
  warnings?: string[];
};

export type ConfigGroupModelsResult = {
  models: string[];
  strategyId: string | null;
};

export type AppInfo = {
  display_name: string;
  version: string;
  github_repo: string;
  ca_common_name: string;
  api_key_visible_chars: number;
  user_data_dir?: string;
  default_user_data_dir?: string;
};

export type InvokeResult = {
  ok: boolean;
  message?: string | null;
  code?: string | null;
  details?: Record<string, unknown>;
  logs?: string[];
};

export type LogPullResult = {
  items?: string[];
  next_id?: number;
};

export type LogEventPayload = {
  items: string[];
  next_id: number;
};

export type ProxyTraceStatus = "active" | "completed" | "failed" | "cancelled";

export type ProxyTraceBodyCapture = {
  value?: unknown;
  bytes?: number;
  truncated?: boolean;
  truncated_reason?: "size_limit" | "stream_limit" | "unsupported_type";
  redacted?: boolean;
};

export type ProxyTraceEvent = {
  at: string;
  kind: string;
  message?: string;
  data?: Record<string, unknown>;
};

export type ProxyTraceSummary = {
  trace_id: string;
  request_id: string;
  status: ProxyTraceStatus;
  method: string;
  request_path: string;
  request_model?: string;
  provider?: string;
  upstream_model?: string;
  is_stream: boolean;
  status_code?: number;
  started_at: string;
  ended_at?: string;
  duration_ms?: number;
  chunk_count?: number;
  error?: string;
  events_count?: number;
  request_body_bytes?: number;
  response_body_bytes?: number;
  request_body_truncated?: boolean;
  response_body_truncated?: boolean;
};

export type ProxyTrace = ProxyTraceSummary & {
  route_mode?: ProxyMode;
  request_api?: "chat_completions" | "responses";
  client_model?: string;
  resolved_target_label?: string;
  target_api_base_url?: string;
  target_model?: string;
  first_chunk_at?: string;
  finish_reason?: string;
  request_body?: ProxyTraceBodyCapture;
  response_body?: ProxyTraceBodyCapture;
  events: ProxyTraceEvent[];
};

export type ProxyTraceListResult = {
  items?: ProxyTraceSummary[];
};

export type ProxyTraceClearResult = {
  deleted_count?: number;
  kept_active_count?: number;
};

export type MainTabKey = "cert" | "hosts" | "proxy";

export type ProxyStartStepEvent = {
  step: MainTabKey;
  status: "ok" | "skipped" | "failed" | "started";
  message?: string | null;
  panel_target?: "config-group" | "global-config" | "settings" | null;
};

export type ProxyRuntimeStatusPayload = {
  running: boolean;
  active_mode: ProxyMode | null;
  loopback_port?: number | null;
};

export type SystemPromptDelta = {
  edited_text?: string;
  edited_at: string;
  editor?: string;
};

export type SystemPromptItem = {
  hash: string;
  original_text: string;
  created_at: string;
  latest_delta?: SystemPromptDelta | null;
};

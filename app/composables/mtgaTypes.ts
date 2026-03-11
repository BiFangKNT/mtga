export type ConfigGroup = {
  name?: string;
  api_url: string;
  model_id: string;
  api_key: string;
  middle_route?: string;
  target_model_id?: string;
  mapped_model_id?: string;
};

export type ConfigPayload = {
  config_groups: ConfigGroup[];
  current_config_index: number;
  mapped_model_id: string;
  mtga_auth_key: string;
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

export type MainTabKey = "cert" | "hosts" | "proxy";

export type ProxyStartStepEvent = {
  step: MainTabKey;
  status: "ok" | "skipped" | "failed" | "started";
  message?: string | null;
  panel_target?: "config-group" | "global-config" | null;
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

<script setup lang="ts">
import type { ProviderId } from "~/composables/mtgaTypes";

const props = withDefaults(
  defineProps<{
    open?: boolean;
    mode?: "add" | "edit";
    name?: string;
    provider?: ProviderId;
    apiUrl?: string;
    modelId?: string;
    apiKey?: string;
    middleRoute?: string;
    middleRouteEnabled?: boolean;
    formError?: string;
    defaultMiddleRoute?: string;
    availableModels?: string[];
    modelLoading?: boolean;
    saving?: boolean;
  }>(),
  {
    open: false,
    mode: "add",
    name: "",
    provider: "openai_chat_completion",
    apiUrl: "",
    modelId: "",
    apiKey: "",
    middleRoute: "",
    middleRouteEnabled: false,
    formError: "",
    defaultMiddleRoute: "/v1",
    availableModels: () => [],
    modelLoading: false,
    saving: false,
  },
);

const emit = defineEmits<{
  (event: "update:open", value: boolean): void;
  (event: "update:name", value: string): void;
  (event: "update:provider", value: ProviderId): void;
  (event: "update:apiUrl", value: string): void;
  (event: "update:modelId", value: string): void;
  (event: "update:apiKey", value: string): void;
  (event: "update:middleRoute", value: string): void;
  (event: "update:middleRouteEnabled", value: boolean): void;
  (event: "save"): void;
  (event: "cancel"): void;
  (event: "fetch-models"): void;
}>();

const openModel = computed({
  get: () => props.open,
  set: (value: boolean) => emit("update:open", value),
});

const nameModel = computed({
  get: () => props.name,
  set: (value: string) => emit("update:name", value),
});

const providerModel = computed({
  get: () => props.provider,
  set: (value: ProviderId) => emit("update:provider", value),
});

const apiUrlModel = computed({
  get: () => props.apiUrl,
  set: (value: string) => emit("update:apiUrl", value),
});

const modelIdModel = computed({
  get: () => props.modelId,
  set: (value: string) => emit("update:modelId", value),
});

const apiKeyModel = computed({
  get: () => props.apiKey,
  set: (value: string) => emit("update:apiKey", value),
});

const middleRouteModel = computed({
  get: () => props.middleRoute,
  set: (value: string) => emit("update:middleRoute", value),
});

const middleRouteEnabledModel = computed({
  get: () => props.middleRouteEnabled,
  set: (value: boolean) => emit("update:middleRouteEnabled", value),
});

const handleDialogClose = () => {
  emit("cancel");
};

const handleCancel = () => {
  openModel.value = false;
  emit("cancel");
};

const handleSave = () => {
  if (props.saving) {
    return;
  }
  emit("save");
};

const handleFetchModels = () => {
  emit("fetch-models");
};

const providerOptions: { label: string; value: ProviderId }[] = [
  { label: "OpenAI Chat Completion", value: "openai_chat_completion" },
  { label: "OpenAI Response", value: "openai_response" },
  { label: "Anthropic", value: "anthropic" },
  { label: "Gemini", value: "gemini" },
];

const getModelPlaceholder = (provider: ProviderId) => {
  if (provider === "anthropic") {
    return "例如：claude-3-7-sonnet-latest";
  }
  if (provider === "gemini") {
    return "例如：gemini-2.5-pro";
  }
  return "例如：gpt-5";
};
</script>

<template>
  <MtgaDialog v-model:open="openModel" max-width="max-w-l" @close="handleDialogClose">
    <template #header>
      <div class="flex items-center justify-between gap-3">
        <div>
          <h3 class="text-lg font-semibold text-slate-900">
            {{ props.mode === "add" ? "新增配置组" : "修改配置组" }}
          </h3>
          <p class="text-xs text-slate-500">配置代理目标与鉴权参数</p>
        </div>
        <span class="mtga-chip">配置编辑</span>
      </div>
    </template>

    <div class="px-6 py-6 space-y-5">
      <MtgaInput
        v-model="nameModel"
        label="配置组名称"
        placeholder="例如：我的常用配置"
        icon="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
      />

      <MtgaSelect v-model="providerModel" label="提供商" required :options="providerOptions" />

      <MtgaInput
        v-model="apiUrlModel"
        label="API URL"
        required
        placeholder="https://api.openai.com"
        icon="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
      />

      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="flex cursor-pointer items-center gap-2">
            <input
              v-model="middleRouteEnabledModel"
              type="checkbox"
              class="checkbox checkbox-primary checkbox-xs"
            />
            <span class="label-text text-xs font-medium text-slate-500">修改中间路由</span>
          </label>
          <span v-if="middleRouteEnabledModel" class="text-[10px] text-slate-400">
            通常为 {{ props.defaultMiddleRoute }}
          </span>
        </div>
        <MtgaInput
          v-if="middleRouteEnabledModel"
          v-model="middleRouteModel"
          :placeholder="props.defaultMiddleRoute"
          size="sm"
        />
      </div>

      <MtgaInput
        v-model="modelIdModel"
        label="实际模型ID"
        required
        show-dropdown
        :loading="props.modelLoading"
        :options="props.availableModels"
        :placeholder="getModelPlaceholder(props.provider)"
        icon="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"
        @dropdown="handleFetchModels"
      />

      <MtgaInput
        v-model="apiKeyModel"
        label="API Key"
        required
        type="password"
        placeholder="sk-..."
        icon="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"
      />

      <div v-if="props.formError" class="alert alert-error py-2 px-3 rounded-xl">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current shrink-0 h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span class="text-xs">{{ props.formError }}</span>
      </div>
    </div>

    <template #footer>
      <button class="mtga-btn-dialog-ghost flex-1" @click="handleCancel">取消</button>
      <button
        class="mtga-btn-dialog-primary flex-1"
        :class="props.saving ? 'loading' : ''"
        :disabled="props.saving"
        @click="handleSave"
      >
        保存
      </button>
    </template>
  </MtgaDialog>
</template>

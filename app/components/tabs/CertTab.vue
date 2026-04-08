<script setup lang="ts">
type CertAction = "generate" | "install" | "clear";

const store = useMtgaStore();
const appInfo = store.appInfo;
const { runningAction, runAction } = usePendingAction<CertAction>();

const isConfirmOpen = ref(false);
const inputCommonName = ref("");
const showInputError = ref(false);

const clearCaTooltip = computed(() => {
  const commonName = appInfo.value.ca_common_name || "MTGA_CA";
  return [
    "macOS: 删除系统钥匙串中匹配的CA证书；",
    "Windows: 删除本地计算机/Root 中匹配的CA证书",
    `Common Name: ${commonName}`,
    "需要管理员权限，建议仅在需要重置证书时使用",
  ].join("\n");
});

const handleGenerate = async () => {
  await runAction("generate", () => store.runGenerateCertificates());
};

const handleInstall = async () => {
  await runAction("install", () => store.runInstallCaCert());
};

/**
 * 触发清除系统 CA 证书流程，先打开确认弹窗
 */
const handleClear = () => {
  inputCommonName.value = appInfo.value.ca_common_name || "MTGA_CA";
  showInputError.value = false;
  isConfirmOpen.value = true;
};

/**
 * 用户确认后的实际清除操作
 */
const confirmClear = async () => {
  if (!inputCommonName.value.trim()) {
    showInputError.value = true;
    return;
  }
  isConfirmOpen.value = false;
  await runAction("clear", () => store.runClearCaCert(inputCommonName.value));
};

watch(inputCommonName, (val) => {
  if (val.trim()) {
    showInputError.value = false;
  }
});
</script>

<template>
  <div class="mtga-soft-panel space-y-3">
    <div>
      <div class="text-sm font-semibold text-slate-900">证书管理</div>
      <div class="text-xs text-slate-500">生成、安装与清理本地证书</div>
    </div>
    <div class="space-y-2">
      <MtgaLoadingButton
        class="mtga-btn-primary"
        :loading="runningAction === 'generate'"
        :disabled="Boolean(runningAction)"
        @click="handleGenerate"
      >
        生成CA和服务器证书
      </MtgaLoadingButton>
      <div class="grid grid-cols-2 gap-2">
        <MtgaLoadingButton
          class="mtga-btn-primary"
          :loading="runningAction === 'install'"
          :disabled="Boolean(runningAction)"
          @click="handleInstall"
        >
          安装CA证书
        </MtgaLoadingButton>
        <MtgaLoadingButton
          class="mtga-btn-error tooltip mtga-tooltip"
          :data-tip="clearCaTooltip"
          :loading="runningAction === 'clear'"
          :disabled="Boolean(runningAction)"
          style="--mtga-tooltip-max: 280px"
          @click="handleClear"
        >
          清除系统CA证书
        </MtgaLoadingButton>
      </div>
    </div>
  </div>

  <!-- 二次确认弹窗 -->
  <ConfirmDialog
    v-model:open="isConfirmOpen"
    v-model="inputCommonName"
    title="确认清除 CA 证书"
    message="将从系统信任存储中删除匹配的 CA 证书，是否继续？"
    show-input
    label="Common Name:"
    placeholder="请输入证书 Common Name"
    :error="showInputError ? '请输入有效的 Common Name' : ''"
    input-class="font-mono"
    confirm-text="确认清除"
    type="error"
    @confirm="confirmClear"
  />
</template>

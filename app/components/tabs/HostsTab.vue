<script setup lang="ts">
type HostsAction = "modify" | "backup" | "restore" | "open";

const store = useMtgaStore();
const { runningAction, runAction } = usePendingAction<HostsAction>();

const handleModify = async () => {
  await runAction("modify", () => store.runHostsModify("add"));
};

const handleBackup = async () => {
  await runAction("backup", () => store.runHostsModify("backup"));
};

const handleRestore = async () => {
  await runAction("restore", () => store.runHostsModify("restore"));
};

const handleOpen = async () => {
  await runAction("open", () => store.runHostsOpen());
};
</script>

<template>
  <div class="mtga-soft-panel space-y-3">
    <div>
      <div class="text-sm font-semibold text-slate-900">hosts 文件</div>
      <div class="text-xs text-slate-500">快速修改与备份恢复</div>
    </div>
    <div class="space-y-2">
      <MtgaLoadingButton
        class="mtga-btn-primary"
        :loading="runningAction === 'modify'"
        :disabled="Boolean(runningAction)"
        @click="handleModify"
      >
        修改hosts文件
      </MtgaLoadingButton>
      <div class="grid grid-cols-2 gap-2">
        <MtgaLoadingButton
          class="mtga-btn-outline"
          :loading="runningAction === 'backup'"
          :disabled="Boolean(runningAction)"
          @click="handleBackup"
        >
          备份hosts
        </MtgaLoadingButton>
        <MtgaLoadingButton
          class="mtga-btn-outline"
          :loading="runningAction === 'restore'"
          :disabled="Boolean(runningAction)"
          @click="handleRestore"
        >
          还原hosts
        </MtgaLoadingButton>
      </div>
      <MtgaLoadingButton
        class="mtga-btn-outline"
        :loading="runningAction === 'open'"
        :disabled="Boolean(runningAction)"
        @click="handleOpen"
      >
        打开hosts文件
      </MtgaLoadingButton>
    </div>
  </div>
</template>

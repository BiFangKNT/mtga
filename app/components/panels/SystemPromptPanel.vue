<script setup lang="ts">
import type { SystemPromptItem } from "~/composables/mtgaTypes";
import {
  formatSystemPromptCreatedAt,
  sortSystemPromptItemsByCreatedAt,
} from "~/composables/systemPromptUi";

const store = useMtgaStore();
const loading = ref(false);
const editorOpen = ref(false);
const editingItem = ref<SystemPromptItem | null>(null);

const sortedItems = computed(() => {
  return sortSystemPromptItemsByCreatedAt(store.systemPrompts.value);
});

const formatTime = (value: string) => {
  return formatSystemPromptCreatedAt(value);
};

const refreshList = async () => {
  if (loading.value) {
    return;
  }
  loading.value = true;
  try {
    await store.loadSystemPrompts();
  } finally {
    loading.value = false;
  }
};

const openEditor = (item: SystemPromptItem) => {
  editingItem.value = item;
  editorOpen.value = true;
};

const handleSaved = async () => {
  const hashValue = editingItem.value?.hash || "";
  await refreshList();
  if (!hashValue) {
    return;
  }
  const latest = store.systemPrompts.value.find((item) => item.hash === hashValue);
  if (latest) {
    editingItem.value = latest;
  }
};

watch(editorOpen, (open) => {
  if (!open) {
    editingItem.value = null;
  }
});

onMounted(() => {
  void refreshList();
});
</script>

<template>
  <div class="flex items-center justify-between gap-3">
    <div>
      <h2 class="mtga-card-title">系统提示词</h2>
      <p class="mtga-card-subtitle">收录系统提示词哈希记录并支持增量编辑</p>
    </div>
    <button
      class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
      :class="loading ? 'loading' : ''"
      :disabled="loading"
      @click="refreshList"
    >
      刷新
    </button>
  </div>

  <div class="mt-4 space-y-2">
    <button
      v-for="item in sortedItems"
      :key="item.hash"
      class="mtga-clickable-row w-full"
      @click="openEditor(item)"
    >
      <span class="flex flex-col items-start gap-1 text-left min-w-0">
        <span class="font-mono text-xs text-slate-700 break-all">{{ item.hash }}</span>
        <span class="text-[11px] text-slate-500">创建时间：{{ formatTime(item.created_at) }}</span>
      </span>
    </button>

    <div
      v-if="!loading && sortedItems.length === 0"
      class="rounded-xl border border-slate-200/70 bg-white/40 p-6 text-center text-sm text-slate-400"
    >
      暂无系统提示词记录
    </div>
  </div>

  <SystemPromptEditorDialog v-model:open="editorOpen" :item="editingItem" @saved="handleSaved" />
</template>

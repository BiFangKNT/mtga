<script setup lang="ts">
import type { SystemPromptItem } from "~/composables/mtgaTypes";
import {
  formatSystemPromptCreatedAt,
  sortSystemPromptItemsByCreatedAt,
} from "~/composables/systemPromptUi";

const store = useMtgaStore();
const loading = ref(false);
const deleting = ref(false);
const editorOpen = ref(false);
const editingItem = ref<SystemPromptItem | null>(null);
const deleteMode = ref(false);
const selectedHashes = ref<string[]>([]);
const deleteConfirmOpen = ref(false);
const pendingDeleteHashes = ref<string[]>([]);
const pendingDeleteIsBatch = ref(false);

const sortedItems = computed(() => {
  return sortSystemPromptItemsByCreatedAt(store.systemPrompts.value);
});
const selectedHashSet = computed(() => new Set(selectedHashes.value));
const busy = computed(() => loading.value || deleting.value);
const hasSelection = computed(() => selectedHashes.value.length > 0);
const allSelected = computed(() => {
  if (!sortedItems.value.length) {
    return false;
  }
  return sortedItems.value.every((item) => selectedHashSet.value.has(item.hash));
});
const deleteConfirmTitle = computed(() =>
  pendingDeleteIsBatch.value ? "批量删除记录" : "删除记录",
);
const deleteConfirmMessage = computed(() => {
  if (!pendingDeleteHashes.value.length) {
    return "请确认是否删除该记录。";
  }
  if (pendingDeleteIsBatch.value) {
    return `确认删除所选 ${pendingDeleteHashes.value.length} 条记录？此操作不可恢复。`;
  }
  const hashValue = pendingDeleteHashes.value[0] || "";
  const hashPrefix = hashValue.slice(0, 12);
  return `确认删除记录 ${hashPrefix}${hashValue.length > 12 ? "..." : ""}？此操作不可恢复。`;
});

const formatTime = (value: string) => {
  return formatSystemPromptCreatedAt(value);
};

const refreshList = async () => {
  if (busy.value) {
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

const clearSelection = () => {
  selectedHashes.value = [];
};

const exitDeleteMode = () => {
  deleteMode.value = false;
  clearSelection();
};

const toggleDeleteMode = () => {
  if (deleteMode.value) {
    exitDeleteMode();
    return;
  }
  deleteMode.value = true;
  clearSelection();
};

const handleRowClick = (item: SystemPromptItem) => {
  if (deleteMode.value || busy.value) {
    return;
  }
  openEditor(item);
};

const setHashSelected = (hashValue: string, checked: boolean) => {
  if (checked) {
    if (!selectedHashSet.value.has(hashValue)) {
      selectedHashes.value = [...selectedHashes.value, hashValue];
    }
    return;
  }
  selectedHashes.value = selectedHashes.value.filter((hash) => hash !== hashValue);
};

const handleItemSelectionChange = (hashValue: string, event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  setHashSelected(hashValue, target.checked);
};

const handleSelectAllChange = (event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  if (target.checked) {
    selectedHashes.value = sortedItems.value.map((item) => item.hash);
    return;
  }
  clearSelection();
};

const closeDeleteConfirm = () => {
  deleteConfirmOpen.value = false;
  pendingDeleteHashes.value = [];
  pendingDeleteIsBatch.value = false;
};

const openDeleteConfirm = (hashes: string[], options?: { batch?: boolean }) => {
  const normalized = Array.from(new Set(hashes.map((hash) => hash.trim()).filter(Boolean)));
  if (!normalized.length || busy.value) {
    return;
  }
  pendingDeleteHashes.value = normalized;
  pendingDeleteIsBatch.value = options?.batch === true || normalized.length > 1;
  deleteConfirmOpen.value = true;
};

const handleDeleteSingle = (item: SystemPromptItem) => {
  openDeleteConfirm([item.hash], { batch: false });
};

const handleDeleteSelected = () => {
  if (!selectedHashes.value.length) {
    return;
  }
  openDeleteConfirm(selectedHashes.value, { batch: true });
};

const handleDeleteCancel = () => {
  if (deleting.value) {
    return;
  }
  closeDeleteConfirm();
};

const handleDeleteConfirm = async () => {
  if (deleting.value || !pendingDeleteHashes.value.length) {
    return;
  }
  deleting.value = true;
  const deletingSet = new Set(pendingDeleteHashes.value);
  try {
    const ok = await store.deleteSystemPrompts({
      hashes: pendingDeleteHashes.value,
    });
    if (!ok) {
      return;
    }
    selectedHashes.value = selectedHashes.value.filter((hash) => !deletingSet.has(hash));
    if (editingItem.value && deletingSet.has(editingItem.value.hash)) {
      editorOpen.value = false;
      editingItem.value = null;
    }
    closeDeleteConfirm();
  } finally {
    deleting.value = false;
  }
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

watch(
  sortedItems,
  (items) => {
    const validHashes = new Set(items.map((item) => item.hash));
    selectedHashes.value = selectedHashes.value.filter((hash) => validHashes.has(hash));
    if (!items.length && deleteMode.value) {
      exitDeleteMode();
    }
  },
  { deep: true },
);

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
    <div class="flex items-center gap-2">
      <button
        class="btn btn-sm btn-outline rounded-xl border-rose-200 text-rose-600 hover:border-rose-300 hover:bg-rose-50"
        :disabled="busy || (!deleteMode && sortedItems.length === 0)"
        @click="toggleDeleteMode"
      >
        {{ deleteMode ? "退出删除" : "删除" }}
      </button>
      <button
        class="btn btn-sm btn-outline rounded-xl border-slate-200 hover:border-amber-500 hover:bg-amber-50/50 hover:text-amber-600"
        :class="loading ? 'loading' : ''"
        :disabled="busy"
        @click="refreshList"
      >
        刷新
      </button>
    </div>
  </div>

  <div class="mt-4 space-y-2">
    <!-- 删除模式：全选栏 -->
    <div
      v-if="deleteMode && sortedItems.length > 0"
      class="flex items-center gap-3 px-4 py-2 bg-slate-50/80 rounded-xl border border-slate-200/60 sticky top-0 z-10"
    >
      <div class="flex items-center">
        <input
          type="checkbox"
          class="checkbox checkbox-xs rounded border-slate-300 [--chkbg:var(--color-amber-500)] [--chkfg:white]"
          :checked="allSelected"
          :disabled="busy"
          @change="handleSelectAllChange"
        />
      </div>
      <span class="text-xs text-slate-500 font-medium flex-1"
        >已选择 {{ selectedHashes.length }} 条记录</span
      >
      <button
        class="btn btn-ghost btn-xs h-7 min-h-7 rounded-lg text-rose-600 hover:bg-rose-50 px-2 font-medium"
        :disabled="busy || !hasSelection"
        @click="handleDeleteSelected"
      >
        批量删除
      </button>
    </div>

    <!-- 列表内容 -->
    <template v-if="deleteMode">
      <label
        v-for="item in sortedItems"
        :key="item.hash"
        class="flex items-center gap-3 px-4 py-2.5 bg-white/20 hover:bg-white/40 rounded-xl border border-slate-200/40 transition-all duration-200 group cursor-pointer"
      >
        <div class="flex items-center">
          <input
            type="checkbox"
            class="checkbox checkbox-xs rounded border-slate-300 [--chkbg:var(--color-amber-500)] [--chkfg:white] cursor-pointer"
            :checked="selectedHashSet.has(item.hash)"
            :disabled="busy"
            @change="handleItemSelectionChange(item.hash, $event)"
          />
        </div>
        <div class="flex-1 min-w-0 flex flex-col gap-0.5">
          <span class="font-mono text-xs text-slate-700 break-all leading-relaxed">{{
            item.hash
          }}</span>
          <span class="text-[10px] text-slate-400"
            >创建时间：{{ formatTime(item.created_at) }}</span
          >
        </div>
        <button
          type="button"
          class="btn btn-ghost btn-xs btn-circle h-7 min-h-7 w-7 text-slate-300 hover:bg-rose-50 hover:text-rose-600 transition-colors"
          :disabled="busy"
          @click.stop.prevent="handleDeleteSingle(item)"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-3.5 w-3.5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </label>
    </template>
    <template v-else>
      <button
        v-for="item in sortedItems"
        :key="item.hash"
        class="mtga-clickable-row w-full"
        :disabled="busy"
        @click="handleRowClick(item)"
      >
        <span class="flex min-w-0 flex-col items-start gap-1 text-left">
          <span class="font-mono text-xs text-slate-700 break-all">{{ item.hash }}</span>
          <span class="text-[11px] text-slate-500"
            >创建时间：{{ formatTime(item.created_at) }}</span
          >
        </span>
      </button>
    </template>

    <div
      v-if="!loading && sortedItems.length === 0"
      class="rounded-xl border border-slate-200/70 bg-white/40 p-6 text-center text-sm text-slate-400"
    >
      暂无系统提示词记录
    </div>
  </div>

  <SystemPromptEditorDialog v-model:open="editorOpen" :item="editingItem" @saved="handleSaved" />
  <ConfirmDialog
    v-model:open="deleteConfirmOpen"
    type="error"
    :title="deleteConfirmTitle"
    :message="deleteConfirmMessage"
    confirm-text="删除"
    cancel-text="取消"
    @confirm="handleDeleteConfirm"
    @cancel="handleDeleteCancel"
  />
</template>

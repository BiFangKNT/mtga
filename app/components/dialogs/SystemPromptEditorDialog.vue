<script setup lang="ts">
import { EditorState } from "@codemirror/state";
import { defaultKeymap, history, historyKeymap } from "@codemirror/commands";
import { openSearchPanel, search, searchKeymap } from "@codemirror/search";
import { EditorView, keymap, lineNumbers } from "@codemirror/view";
import { diffLines } from "diff";

import type { SystemPromptItem } from "~/composables/mtgaTypes";

const props = withDefaults(
  defineProps<{
    open?: boolean;
    item: SystemPromptItem | null;
  }>(),
  {
    open: false,
  },
);

const emit = defineEmits<{
  (event: "update:open", value: boolean): void;
  (event: "saved"): void;
}>();

const store = useMtgaStore();
const editorHost = ref<HTMLDivElement | null>(null);
const draftText = ref("");
const saving = ref(false);
const showDiff = ref(false);
let editorView: EditorView | null = null;

const openModel = computed({
  get: () => props.open,
  set: (value: boolean) => emit("update:open", value),
});

const originalText = computed(() => props.item?.original_text ?? "");
const effectiveText = computed(
  () => props.item?.latest_delta?.edited_text ?? props.item?.original_text ?? "",
);

const createdAtLabel = computed(() => {
  const raw = props.item?.created_at ?? "";
  const date = new Date(raw);
  if (Number.isNaN(date.getTime())) {
    return raw;
  }
  return date.toLocaleString("zh-CN", { hour12: false });
});

const diffParts = computed(() => {
  if (!showDiff.value) {
    return [];
  }
  return diffLines(originalText.value, draftText.value);
});

const destroyEditor = () => {
  if (!editorView) {
    return;
  }
  editorView.destroy();
  editorView = null;
};

const syncEditorDoc = (value: string) => {
  if (!editorView) {
    return;
  }
  const current = editorView.state.doc.toString();
  if (current === value) {
    return;
  }
  editorView.dispatch({
    changes: {
      from: 0,
      to: editorView.state.doc.length,
      insert: value,
    },
  });
};

const createEditor = () => {
  if (!editorHost.value) {
    return;
  }
  destroyEditor();

  const updateListener = EditorView.updateListener.of((update) => {
    if (!update.docChanged) {
      return;
    }
    draftText.value = update.state.doc.toString();
  });

  const state = EditorState.create({
    doc: draftText.value,
    extensions: [
      lineNumbers(),
      history(),
      search({ top: true }),
      keymap.of([...defaultKeymap, ...historyKeymap, ...searchKeymap]),
      EditorView.lineWrapping,
      updateListener,
    ],
  });

  editorView = new EditorView({
    state,
    parent: editorHost.value,
  });
};

const handleSearch = () => {
  if (!editorView) {
    return;
  }
  openSearchPanel(editorView);
  editorView.focus();
};

const handleReplace = () => {
  if (!editorView) {
    return;
  }
  openSearchPanel(editorView);
  editorView.focus();
};

const handleCancel = () => {
  openModel.value = false;
};

const handleSave = async () => {
  if (saving.value || !props.item) {
    return;
  }
  saving.value = true;
  try {
    const ok = await store.updateSystemPrompt({
      hash: props.item.hash,
      edited_text: draftText.value,
    });
    if (!ok) {
      return;
    }
    emit("saved");
    openModel.value = false;
  } finally {
    saving.value = false;
  }
};

watch(
  () => props.open,
  async (open) => {
    if (!open) {
      destroyEditor();
      return;
    }
    draftText.value = effectiveText.value;
    showDiff.value = false;
    await nextTick();
    createEditor();
  },
);

watch(
  () => props.item?.hash,
  async () => {
    if (!props.open) {
      return;
    }
    draftText.value = effectiveText.value;
    await nextTick();
    if (editorView) {
      syncEditorDoc(draftText.value);
    } else {
      createEditor();
    }
  },
);

watch(draftText, (value) => {
  syncEditorDoc(value);
});

onUnmounted(() => {
  destroyEditor();
});
</script>

<template>
  <MtgaDialog v-model:open="openModel" max-width="max-w-4xl">
    <template #header>
      <div class="space-y-1">
        <h3 class="text-lg font-semibold text-slate-900">编辑系统提示词</h3>
        <p class="text-xs text-slate-500 font-mono break-all">{{ props.item?.hash || "-" }}</p>
        <p class="text-[11px] text-slate-400">收录时间：{{ createdAtLabel || "-" }}</p>
      </div>
    </template>

    <div class="px-6 py-5 space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <button class="btn btn-xs rounded-lg border-slate-200" @click="handleSearch">查找</button>
          <button class="btn btn-xs rounded-lg border-slate-200" @click="handleReplace">
            替换
          </button>
        </div>
        <label class="label cursor-pointer gap-2 py-0">
          <span class="label-text text-xs text-slate-500">显示 diff 高亮</span>
          <input v-model="showDiff" type="checkbox" class="toggle toggle-xs toggle-warning" />
        </label>
      </div>

      <div
        ref="editorHost"
        class="rounded-xl border border-slate-200 bg-white min-h-[280px] overflow-hidden"
      ></div>

      <div v-if="showDiff" class="rounded-xl border border-slate-200 bg-slate-50/60 p-3 space-y-2">
        <div class="text-xs text-slate-500">原文 vs 修改版（当前编辑内容）</div>
        <div
          class="max-h-[220px] overflow-auto custom-scrollbar rounded-lg border border-slate-200"
        >
          <pre class="text-xs leading-relaxed p-3 whitespace-pre-wrap">
<template v-for="(part, index) in diffParts" :key="index"
><span
  :class="
    part.added
      ? 'bg-emerald-100/70 text-emerald-700'
      : part.removed
        ? 'bg-rose-100/70 text-rose-700 line-through'
        : 'text-slate-600'
  "
>{{ part.value }}</span></template
></pre>
        </div>
      </div>
    </div>

    <template #footer>
      <button class="mtga-btn-dialog-ghost flex-1" @click="handleCancel">取消</button>
      <button
        class="mtga-btn-dialog-primary flex-1"
        :class="saving ? 'loading' : ''"
        :disabled="saving"
        @click="handleSave"
      >
        保存
      </button>
    </template>
  </MtgaDialog>
</template>

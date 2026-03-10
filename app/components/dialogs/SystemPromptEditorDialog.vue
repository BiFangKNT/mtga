<script setup lang="ts">
import {
  defaultKeymap,
  history,
  historyField,
  historyKeymap,
  redo,
  redoDepth,
  undo,
  undoDepth,
} from "@codemirror/commands";
import { markdown } from "@codemirror/lang-markdown";
import { defaultHighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { MergeView } from "@codemirror/merge";
import { type Extension, EditorState } from "@codemirror/state";
import {
  closeSearchPanel,
  openSearchPanel,
  search,
  searchKeymap,
  searchPanelOpen,
} from "@codemirror/search";
import { EditorView, keymap, lineNumbers } from "@codemirror/view";

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
const mergeHost = ref<HTMLDivElement | null>(null);
const editorSurface = ref<HTMLDivElement | null>(null);
const draftText = ref("");
const saving = ref(false);
const showDiff = ref(false);
const canUndo = ref(false);
const canRedo = ref(false);
const copied = ref(false);
const mergeHeaderTemplate = ref("minmax(0, 1fr) minmax(0, 1fr)");
let singleView: EditorView | null = null;
let diffView: MergeView | null = null;
let editableStateSnapshot: unknown | null = null;
let editableScroll = { top: 0, left: 0 };
let copiedTimer: ReturnType<typeof setTimeout> | null = null;
let mergeLayoutObserver: ResizeObserver | null = null;
let mergeLayoutRaf = 0;
let mountRevision = 0;
let diffSwitching = false;
let pendingDiffMode: boolean | null = null;

const stateFields = {
  history: historyField,
};

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

const isDirty = computed(() => draftText.value !== effectiveText.value);
const charCount = computed(() => draftText.value.length);
const lineCount = computed(() => draftText.value.split("\n").length);

const editorTheme = EditorView.theme({
  "&": {
    height: "100%",
    fontSize: "13px",
    backgroundColor: "#ffffff",
  },
  ".cm-editor": {
    height: "100%",
  },
  ".cm-scroller": {
    height: "100%",
    overflow: "auto",
    lineHeight: "1.65",
    fontFamily:
      "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace",
  },
  ".cm-gutters": {
    backgroundColor: "#f8fafc",
    color: "#64748b",
    borderRight: "1px solid #e2e8f0",
  },
  ".cm-activeLine": {
    backgroundColor: "#f8fafc",
  },
  ".cm-activeLineGutter": {
    backgroundColor: "#f1f5f9",
  },
  ".cm-content": {
    caretColor: "#0f172a",
  },
  ".cm-selectionBackground, ::selection": {
    backgroundColor: "#fcd34d66",
  },
  ".cm-search": {
    borderBottom: "1px solid #e2e8f0",
    backgroundColor: "#fffaf0",
  },
  ".cm-keyword": { color: "#b45309" },
  ".cm-strong": { color: "#0f172a", fontWeight: "700" },
  ".cm-emphasis": { color: "#7c2d12", fontStyle: "italic" },
  ".cm-link": { color: "#0369a1", textDecoration: "underline" },
  ".cm-url": { color: "#0284c7" },
  ".cm-string": { color: "#166534" },
  ".cm-quote": { color: "#475569" },
  ".cm-heading": { color: "#1d4ed8", fontWeight: "700" },
  ".cm-comment": { color: "#64748b" },
});

const getActiveEditableView = () => diffView?.b ?? singleView;

const getActiveScrollElement = () => diffView?.dom ?? singleView?.scrollDOM ?? null;

const serializeEditableState = (state: EditorState) => state.toJSON(stateFields);

const syncDraftFromState = (state: EditorState) => {
  draftText.value = state.doc.toString();
};

const snapshotEditableState = (state: EditorState) => {
  editableStateSnapshot = serializeEditableState(state);
};

const captureActiveEditableState = (options?: { includeSnapshot?: boolean }) => {
  const activeView = getActiveEditableView();
  if (activeView) {
    syncDraftFromState(activeView.state);
    if (options?.includeSnapshot) {
      snapshotEditableState(activeView.state);
    }
  }
  const scrollEl = getActiveScrollElement();
  if (scrollEl) {
    editableScroll = {
      top: scrollEl.scrollTop,
      left: scrollEl.scrollLeft,
    };
  }
};

const refreshHistoryState = (state = getActiveEditableView()?.state ?? null) => {
  if (!state) {
    canUndo.value = false;
    canRedo.value = false;
    return;
  }
  canUndo.value = undoDepth(state) > 0;
  canRedo.value = redoDepth(state) > 0;
};

const editableUpdateListener = EditorView.updateListener.of((update) => {
  draftText.value = update.state.doc.toString();
  const scrollEl = getActiveScrollElement();
  if (scrollEl) {
    editableScroll = {
      top: scrollEl.scrollTop,
      left: scrollEl.scrollLeft,
    };
  }
  refreshHistoryState(update.state);
  if (diffView) {
    scheduleMergeHeaderLayoutUpdate();
  }
});

const createEditableExtensions = () => [
  markdown(),
  syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
  lineNumbers(),
  history(),
  search({ top: true }),
  editorTheme,
  keymap.of([...defaultKeymap, ...historyKeymap, ...searchKeymap]),
  EditorView.lineWrapping,
  editableUpdateListener,
];

const createOriginalExtensions = () => [
  markdown(),
  syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
  lineNumbers(),
  EditorState.readOnly.of(true),
  EditorView.editable.of(false),
  editorTheme,
  EditorView.lineWrapping,
];

const deserializeEditableState = (extensions: readonly Extension[]) => {
  if (!editableStateSnapshot) {
    return EditorState.create({
      doc: draftText.value,
      extensions,
    });
  }
  return EditorState.fromJSON(
    editableStateSnapshot,
    {
      doc: draftText.value,
      extensions,
    },
    stateFields,
  );
};

const getMergeBaseExtensions = (state: EditorState) => {
  const config = (
    state as EditorState & {
      config?: {
        base?: readonly Extension[];
      };
    }
  ).config;
  return config?.base ?? [];
};

const waitForNextFrame = () =>
  new Promise<void>((resolve) => {
    requestAnimationFrame(() => resolve());
  });

const resetMergeHeaderLayout = () => {
  mergeHeaderTemplate.value = "minmax(0, 1fr) minmax(0, 1fr)";
};

const disconnectMergeLayoutObserver = () => {
  if (mergeLayoutObserver) {
    mergeLayoutObserver.disconnect();
    mergeLayoutObserver = null;
  }
  if (mergeLayoutRaf) {
    cancelAnimationFrame(mergeLayoutRaf);
    mergeLayoutRaf = 0;
  }
};

const updateMergeHeaderLayout = () => {
  if (!diffView) {
    resetMergeHeaderLayout();
    return;
  }
  const editors = diffView.dom.querySelectorAll<HTMLElement>(".cm-mergeViewEditor");
  const leftEditor = editors.item(0);
  const rightEditor = editors.item(1);
  if (!(leftEditor && rightEditor)) {
    resetMergeHeaderLayout();
    return;
  }
  const leftWidth = leftEditor.getBoundingClientRect().width;
  const rightWidth = rightEditor.getBoundingClientRect().width;
  if (!(leftWidth > 0 && rightWidth > 0)) {
    resetMergeHeaderLayout();
    return;
  }
  mergeHeaderTemplate.value = `${leftWidth}px ${rightWidth}px`;
};

const scheduleMergeHeaderLayoutUpdate = () => {
  if (!diffView || mergeLayoutRaf) {
    return;
  }
  mergeLayoutRaf = requestAnimationFrame(() => {
    mergeLayoutRaf = 0;
    updateMergeHeaderLayout();
  });
};

const attachMergeLayoutObserver = () => {
  disconnectMergeLayoutObserver();
  if (!diffView || typeof ResizeObserver === "undefined") {
    return;
  }
  mergeLayoutObserver = new ResizeObserver(() => {
    scheduleMergeHeaderLayoutUpdate();
  });
  mergeLayoutObserver.observe(diffView.dom);
};

const flushActiveEditableInput = async () => {
  const activeView = getActiveEditableView();
  if (!activeView) {
    return;
  }
  if (activeView.composing || activeView.hasFocus) {
    activeView.contentDOM.blur();
  }
  await waitForNextFrame();
  await nextTick();
};

const restoreEditableScroll = () => {
  const apply = () => {
    const scrollEl = getActiveScrollElement();
    if (!scrollEl) {
      return;
    }
    scrollEl.scrollTop = editableScroll.top;
    scrollEl.scrollLeft = editableScroll.left;
  };
  requestAnimationFrame(() => {
    requestAnimationFrame(apply);
  });
};

const destroyViews = () => {
  disconnectMergeLayoutObserver();
  diffView?.destroy();
  diffView = null;
  singleView?.destroy();
  singleView = null;
  resetMergeHeaderLayout();
  refreshHistoryState(null);
};

const createSingleView = () => {
  if (!editorHost.value) {
    return;
  }
  singleView = new EditorView({
    state: deserializeEditableState(createEditableExtensions()),
    parent: editorHost.value,
  });
  syncDraftFromState(singleView.state);
  refreshHistoryState(singleView.state);
  restoreEditableScroll();
};

const hydrateMergeEditableState = () => {
  if (!(diffView && editableStateSnapshot)) {
    return;
  }
  const mergeExtensions = getMergeBaseExtensions(diffView.b.state);
  if (!mergeExtensions.length) {
    return;
  }
  const restoredState = EditorState.fromJSON(
    editableStateSnapshot,
    {
      doc: draftText.value,
      extensions: mergeExtensions,
    },
    stateFields,
  );
  diffView.b.setState(restoredState);
  syncDraftFromState(restoredState);
  refreshHistoryState(restoredState);
};

const createDiffView = () => {
  if (!mergeHost.value) {
    return;
  }
  diffView = new MergeView({
    parent: mergeHost.value,
    orientation: "a-b",
    gutter: false,
    highlightChanges: true,
    a: {
      doc: originalText.value,
      extensions: createOriginalExtensions(),
    },
    b: {
      doc: draftText.value,
      extensions: createEditableExtensions(),
    },
  });
  attachMergeLayoutObserver();
  scheduleMergeHeaderLayoutUpdate();
  hydrateMergeEditableState();
  scheduleMergeHeaderLayoutUpdate();
  restoreEditableScroll();
};

const mountCurrentView = async () => {
  const revision = ++mountRevision;
  destroyViews();
  await nextTick();
  if (revision !== mountRevision || !props.open) {
    return;
  }
  if (showDiff.value) {
    createDiffView();
  } else {
    createSingleView();
  }
};

const resetEditorSession = () => {
  draftText.value = effectiveText.value;
  editableStateSnapshot = null;
  editableScroll = { top: 0, left: 0 };
  copied.value = false;
  pendingDiffMode = null;
  diffSwitching = false;
};

const runCommand = (command: (view: EditorView) => boolean) => {
  const activeView = getActiveEditableView();
  if (!activeView) {
    return false;
  }
  const ok = command(activeView);
  captureActiveEditableState();
  refreshHistoryState(activeView.state);
  activeView.focus();
  return ok;
};

const replaceEditableDoc = (value: string) => {
  const activeView = getActiveEditableView();
  if (!activeView) {
    draftText.value = value;
    editableStateSnapshot = null;
    return;
  }
  activeView.dispatch({
    changes: {
      from: 0,
      to: activeView.state.doc.length,
      insert: value,
    },
  });
};

const localizeSearchPanel = () => {
  const panel = editorSurface.value?.querySelector(".cm-search");
  if (!(panel instanceof HTMLElement)) {
    return;
  }
  const textInputs = panel.querySelectorAll("input[type='text']");
  const findInput = textInputs.item(0);
  const replaceInput = textInputs.item(1);
  if (findInput instanceof HTMLInputElement) {
    findInput.placeholder = "查找";
  }
  if (replaceInput instanceof HTMLInputElement) {
    replaceInput.placeholder = "替换";
  }

  const labelMap: Record<string, string> = {
    next: "下一个",
    prev: "上一个",
    select: "全选匹配",
    replace: "替换",
    replaceAll: "全部替换",
    close: "关闭",
  };

  panel.querySelectorAll("button[name]").forEach((button) => {
    if (!(button instanceof HTMLButtonElement)) {
      return;
    }
    const label = labelMap[button.name];
    if (!label) {
      return;
    }
    button.textContent = label;
    button.title = label;
    button.setAttribute("aria-label", label);
  });
};

const handleSearch = () => {
  const activeView = getActiveEditableView();
  if (!activeView) {
    return;
  }
  const opened = searchPanelOpen(activeView.state);
  runCommand(opened ? closeSearchPanel : openSearchPanel);
  if (!opened) {
    nextTick(() => {
      localizeSearchPanel();
    });
  }
};

const handleUndo = async () => {
  await flushActiveEditableInput();
  runCommand(undo);
};

const handleRedo = async () => {
  await flushActiveEditableInput();
  runCommand(redo);
};

const handleRestoreOriginal = () => {
  replaceEditableDoc(originalText.value);
};

const handleClear = () => {
  replaceEditableDoc("");
};

const handleCopyHash = async () => {
  const hashValue = props.item?.hash;
  if (!hashValue) {
    return;
  }
  if (typeof navigator === "undefined" || !navigator.clipboard?.writeText) {
    return;
  }
  try {
    await navigator.clipboard.writeText(hashValue);
    copied.value = true;
    if (copiedTimer) {
      clearTimeout(copiedTimer);
    }
    copiedTimer = setTimeout(() => {
      copied.value = false;
      copiedTimer = null;
    }, 1400);
  } catch {
    // ignore clipboard errors
  }
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
    await flushActiveEditableInput();
    captureActiveEditableState();
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

const handleDiffToggle = async (event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  pendingDiffMode = target.checked;
  if (!props.open || diffSwitching) {
    return;
  }
  diffSwitching = true;
  try {
    while (pendingDiffMode !== null) {
      const nextMode = pendingDiffMode;
      pendingDiffMode = null;
      if (nextMode === showDiff.value) {
        continue;
      }
      await flushActiveEditableInput();
      captureActiveEditableState({ includeSnapshot: true });
      showDiff.value = nextMode;
      await mountCurrentView();
    }
  } finally {
    diffSwitching = false;
  }
};

watch(
  () => props.open,
  async (open) => {
    if (!open) {
      mountRevision += 1;
      pendingDiffMode = null;
      diffSwitching = false;
      destroyViews();
      return;
    }
    resetEditorSession();
    showDiff.value = false;
    await mountCurrentView();
  },
);

watch(
  () => props.item?.hash,
  async () => {
    if (!props.open) {
      return;
    }
    resetEditorSession();
    await mountCurrentView();
  },
);

onUnmounted(() => {
  if (copiedTimer) {
    clearTimeout(copiedTimer);
    copiedTimer = null;
  }
  destroyViews();
});
</script>

<template>
  <MtgaDialog v-model:open="openModel" max-width="max-w-6xl">
    <template #header>
      <div class="space-y-3">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0 space-y-1">
            <h3 class="text-lg font-semibold text-slate-900">系统提示词编辑器</h3>
            <div class="flex min-w-0 items-center gap-2">
              <span class="truncate font-mono text-[11px] text-slate-500">
                {{ props.item?.hash || "-" }}
              </span>
              <button class="btn btn-ghost btn-xs h-6 min-h-6 px-2" @click="handleCopyHash">
                {{ copied ? "已复制" : "复制" }}
              </button>
            </div>
            <p class="text-[11px] text-slate-400">收录时间：{{ createdAtLabel || "-" }}</p>
          </div>
          <div class="flex items-center gap-2">
            <label class="label cursor-pointer gap-2 px-0 py-0">
              <span class="label-text text-xs text-slate-500">Diff</span>
              <input
                :checked="showDiff"
                type="checkbox"
                class="toggle toggle-xs toggle-warning"
                @change="handleDiffToggle"
              />
            </label>
            <span
              class="rounded-md px-2 py-0.5 text-[11px]"
              :class="
                isDirty
                  ? 'border border-amber-200 bg-amber-100 text-amber-700'
                  : 'border border-emerald-200 bg-emerald-100 text-emerald-700'
              "
            >
              {{ isDirty ? "未保存修改" : "已同步" }}
            </span>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-1">
          <button class="btn btn-xs rounded-lg border-slate-200" @click="handleSearch">
            查找/替换面板
          </button>
          <button
            class="btn btn-xs rounded-lg border-slate-200"
            :disabled="!canUndo"
            @click="handleUndo"
          >
            撤销
          </button>
          <button
            class="btn btn-xs rounded-lg border-slate-200"
            :disabled="!canRedo"
            @click="handleRedo"
          >
            重做
          </button>
          <button class="btn btn-xs rounded-lg border-slate-200" @click="handleRestoreOriginal">
            恢复原文
          </button>
          <button class="btn btn-xs rounded-lg border-slate-200" @click="handleClear">清空</button>
        </div>
      </div>
    </template>

    <div ref="editorSurface" class="flex h-[68vh] min-h-[480px] flex-col overflow-hidden px-6 py-5">
      <div
        v-if="!showDiff"
        ref="editorHost"
        class="flex-1 min-h-0 overflow-hidden rounded-xl border border-slate-200 bg-white"
      ></div>

      <div
        v-else
        class="flex flex-1 min-h-0 flex-col overflow-hidden rounded-xl border border-slate-200 bg-slate-50/80"
      >
        <div
          class="grid shrink-0 border-b border-slate-200"
          :style="{ gridTemplateColumns: mergeHeaderTemplate }"
        >
          <div class="bg-slate-100 px-3 py-2 text-xs text-slate-600">原文</div>
          <div class="border-l border-slate-200 bg-amber-50 px-3 py-2 text-xs text-amber-700">
            当前编辑稿
          </div>
        </div>
        <div ref="mergeHost" class="mtga-merge-host flex-1 min-h-0 overflow-hidden"></div>
      </div>
    </div>

    <template #footer>
      <div class="flex w-full items-center justify-between gap-3">
        <div class="text-xs text-slate-500">
          {{ lineCount }} 行 · {{ charCount }} 字符
          <span class="mx-1 text-slate-300">|</span>
          快捷键：Ctrl/Cmd+F 查找，Ctrl/Cmd+Z 撤销
        </div>
        <div class="flex items-center gap-2">
          <button class="mtga-btn-dialog-ghost min-w-24" @click="handleCancel">取消</button>
          <button
            class="mtga-btn-dialog-primary min-w-24"
            :class="saving ? 'loading' : ''"
            :disabled="saving"
            @click="handleSave"
          >
            保存
          </button>
        </div>
      </div>
    </template>
  </MtgaDialog>
</template>

<style scoped>
.mtga-merge-host :deep(.cm-mergeView) {
  height: 100%;
  overflow: auto;
  background: #fff;
}

.mtga-merge-host :deep(.cm-mergeViewEditors) {
  min-height: 100%;
}

.mtga-merge-host :deep(.cm-mergeViewEditor) {
  min-width: 0;
}

.mtga-merge-host :deep(.cm-merge-a .cm-changedLine),
.mtga-merge-host :deep(.cm-deletedChunk) {
  background: #fff1f2;
}

.mtga-merge-host :deep(.cm-merge-b .cm-changedLine),
.mtga-merge-host :deep(.cm-inlineChangedLine) {
  background: #ecfdf5;
}

.mtga-merge-host :deep(.cm-merge-a .cm-changedText),
.mtga-merge-host :deep(.cm-deletedChunk .cm-deletedText) {
  background: linear-gradient(#fb718566, #fb718566) bottom / 100% 2px no-repeat;
}

.mtga-merge-host :deep(.cm-merge-b .cm-changedText) {
  background: linear-gradient(#10b98188, #10b98188) bottom / 100% 2px no-repeat;
}

.mtga-merge-host :deep(.cm-changedLineGutter) {
  width: 4px;
}

.mtga-merge-host :deep(.cm-search) {
  position: sticky;
  top: 0;
  z-index: 2;
}
</style>

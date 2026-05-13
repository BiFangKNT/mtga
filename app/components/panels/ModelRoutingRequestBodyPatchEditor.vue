<script setup lang="ts">
type PatchOperation = "add" | "remove" | "replace" | "copy" | "move" | "test";
type PatchValueMode = "string" | "number" | "boolean" | "object" | "array" | "null";

type PatchRow = {
  id: number;
  op: PatchOperation;
  path: string;
  from: string;
  valueMode: PatchValueMode;
  valueText: string;
  boolValue: boolean;
};

const PATCH_OPERATIONS: {
  label: string;
  value: PatchOperation;
  description: string;
}[] = [
  { label: "新增", value: "add", description: "写入新字段或数组元素" },
  { label: "删除", value: "remove", description: "移除已有字段或数组元素" },
  { label: "替换", value: "replace", description: "替换已有字段的值" },
  { label: "复制", value: "copy", description: "从 from 复制到 path" },
  { label: "移动", value: "move", description: "从 from 移动到 path" },
  { label: "断言", value: "test", description: "保存前校验字段值" },
];

const VALUE_MODES: {
  label: string;
  value: PatchValueMode;
}[] = [
  { label: "文本", value: "string" },
  { label: "数字", value: "number" },
  { label: "布尔", value: "boolean" },
  { label: "对象", value: "object" },
  { label: "数组", value: "array" },
  { label: "Null", value: "null" },
];

const QUICK_PATHS = [
  "/temperature",
  "/top_p",
  "/max_tokens",
  "/thinking",
  "/tools/0",
  "/metadata",
  "/user",
];

const INVALID_PATCH_TEXT = '[{"op":"invalid"';

const props = withDefaults(
  defineProps<{
    modelValue: string;
    open?: boolean;
  }>(),
  {
    open: false,
  },
);

const emit = defineEmits<{
  (event: "update:modelValue", value: string): void;
  (event: "update:open", value: boolean): void;
}>();

const rows = ref<PatchRow[]>([]);
const parseError = ref("");
const lastEmittedValue = ref<string | null>(null);
const rowSeed = ref(0);

const isOpen = computed({
  get: () => props.open,
  set: (value) => {
    emit("update:open", value);
  },
});

const operationCountLabel = computed(() =>
  rows.value.length ? `${rows.value.length} 项编辑` : "未启用",
);

const needsValue = (op: PatchOperation) => op === "add" || op === "replace" || op === "test";
const needsFrom = (op: PatchOperation) => op === "copy" || op === "move";
const isPlainObject = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);
const isPatchOperation = (value: unknown): value is PatchOperation =>
  value === "add" ||
  value === "remove" ||
  value === "replace" ||
  value === "copy" ||
  value === "move" ||
  value === "test";
const isPatchValueMode = (value: unknown): value is PatchValueMode =>
  value === "string" ||
  value === "number" ||
  value === "boolean" ||
  value === "object" ||
  value === "array" ||
  value === "null";
const stringifyValue = (value: unknown) => JSON.stringify(value, null, 2);

const createRow = (overrides: Partial<PatchRow> = {}): PatchRow => {
  rowSeed.value += 1;
  return {
    op: "add",
    path: "/temperature",
    from: "",
    valueMode: "number",
    valueText: "0.2",
    boolValue: false,
    ...overrides,
    id: rowSeed.value,
  };
};

const inferValueMode = (
  value: unknown,
): Pick<PatchRow, "valueMode" | "valueText" | "boolValue"> => {
  if (value === null) {
    return { valueMode: "null", valueText: "", boolValue: false };
  }
  if (typeof value === "boolean") {
    return { valueMode: "boolean", valueText: "", boolValue: value };
  }
  if (typeof value === "number") {
    return { valueMode: "number", valueText: String(value), boolValue: false };
  }
  if (typeof value === "string") {
    return { valueMode: "string", valueText: value, boolValue: false };
  }
  if (Array.isArray(value)) {
    return { valueMode: "array", valueText: stringifyValue(value), boolValue: false };
  }
  if (isPlainObject(value)) {
    return { valueMode: "object", valueText: stringifyValue(value), boolValue: false };
  }
  return { valueMode: "string", valueText: String(value), boolValue: false };
};

const rowFromOperation = (operation: Record<string, unknown>) => {
  const op = isPatchOperation(operation.op) ? operation.op : "add";
  return createRow({
    op,
    path: typeof operation.path === "string" ? operation.path : "",
    from: typeof operation.from === "string" ? operation.from : "",
    ...inferValueMode(operation.value),
  });
};

const hydrateRows = (source: string) => {
  parseError.value = "";
  const text = source.trim();
  if (!text) {
    rows.value = [];
    return;
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch {
    parseError.value = "当前参数编辑不是合法 JSON，无法转换成可视化表单。";
    rows.value = [];
    return;
  }
  if (!Array.isArray(parsed)) {
    parseError.value = "当前参数编辑不是 JSON Patch 数组。";
    rows.value = [];
    return;
  }
  const nextRows: PatchRow[] = [];
  for (const item of parsed) {
    if (!isPlainObject(item)) {
      parseError.value = "JSON Patch 数组里包含非对象项，无法转换成可视化表单。";
      rows.value = [];
      return;
    }
    nextRows.push(rowFromOperation(item));
  }
  rows.value = nextRows;
};

const normalizePointerInput = (value: string) => {
  const pointer = value.trim();
  if (!pointer) {
    return "";
  }
  return pointer.startsWith("/") ? pointer : `/${pointer}`;
};

const decodePointer = (pointer: string) => {
  const tokens: string[] = [];
  for (const token of pointer.split("/").slice(1)) {
    let decoded = "";
    for (let index = 0; index < token.length; index += 1) {
      const char = token[index];
      if (char !== "~") {
        decoded += char;
        continue;
      }
      const escape = token[index + 1];
      if (escape === "0") {
        decoded += "~";
      } else if (escape === "1") {
        decoded += "/";
      } else {
        return null;
      }
      index += 1;
    }
    tokens.push(decoded);
  }
  return tokens;
};

const validatePointer = (value: string, label: string) => {
  const pointer = value.trim();
  if (!pointer) {
    return `${label} 必填`;
  }
  if (!pointer.startsWith("/")) {
    return `${label} 必须以 / 开头`;
  }
  if (pointer === "/stream" || pointer.startsWith("/stream/")) {
    return "不允许修改 stream";
  }
  if (decodePointer(pointer) === null) {
    return `${label} 包含无效 JSON Pointer 转义`;
  }
  return "";
};

const readValue = (row: PatchRow) => {
  if (row.valueMode === "string") {
    return { ok: true as const, value: row.valueText };
  }
  if (row.valueMode === "number") {
    const numberValue = Number(row.valueText.trim());
    if (!Number.isFinite(numberValue)) {
      return { ok: false as const, error: "数字值不合法" };
    }
    return { ok: true as const, value: numberValue };
  }
  if (row.valueMode === "boolean") {
    return { ok: true as const, value: row.boolValue };
  }
  if (row.valueMode === "null") {
    return { ok: true as const, value: null };
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(row.valueText);
  } catch {
    return {
      ok: false as const,
      error: row.valueMode === "array" ? "数组 JSON 不合法" : "对象 JSON 不合法",
    };
  }
  if (row.valueMode === "array" && !Array.isArray(parsed)) {
    return { ok: false as const, error: "value 必须是数组" };
  }
  if (row.valueMode === "object" && !isPlainObject(parsed)) {
    return { ok: false as const, error: "value 必须是对象" };
  }
  return { ok: true as const, value: parsed };
};

const validateRow = (row: PatchRow) => {
  const issues: string[] = [];
  const pathIssue = validatePointer(row.path, "path");
  if (pathIssue) {
    issues.push(pathIssue);
  }
  if (needsFrom(row.op)) {
    const fromIssue = validatePointer(row.from, "from");
    if (fromIssue) {
      issues.push(fromIssue);
    }
    const fromTokens = decodePointer(row.from.trim());
    const pathTokens = decodePointer(row.path.trim());
    if (
      row.op === "move" &&
      fromTokens &&
      pathTokens &&
      pathTokens.length > fromTokens.length &&
      fromTokens.every((token, tokenIndex) => token === pathTokens[tokenIndex])
    ) {
      issues.push("不能移动到自己的子路径");
    }
  }
  if (needsValue(row.op)) {
    const value = readValue(row);
    if (!value.ok) {
      issues.push(value.error);
    }
  }
  return issues;
};

const rowIssues = computed(() => rows.value.map((row) => validateRow(row)));
const hasRowIssue = computed(() => rowIssues.value.some((issues) => issues.length > 0));

const buildOperation = (row: PatchRow) => {
  const operation: Record<string, unknown> = {
    op: row.op,
    path: row.path.trim(),
  };
  if (needsFrom(row.op)) {
    operation.from = row.from.trim();
  }
  if (needsValue(row.op)) {
    const value = readValue(row);
    if (!value.ok) {
      return null;
    }
    operation.value = value.value;
  }
  return operation;
};

const emitRows = () => {
  if (!rows.value.length) {
    lastEmittedValue.value = "";
    emit("update:modelValue", "");
    return;
  }
  if (hasRowIssue.value) {
    lastEmittedValue.value = INVALID_PATCH_TEXT;
    emit("update:modelValue", INVALID_PATCH_TEXT);
    return;
  }
  const operations = rows.value.map(buildOperation);
  if (operations.some((operation) => operation === null)) {
    lastEmittedValue.value = INVALID_PATCH_TEXT;
    emit("update:modelValue", INVALID_PATCH_TEXT);
    return;
  }
  const nextValue = stringifyValue(operations);
  lastEmittedValue.value = nextValue;
  emit("update:modelValue", nextValue);
};

const addRow = (template?: Partial<PatchRow>) => {
  rows.value.push(createRow(template));
  isOpen.value = true;
  emitRows();
};

const addThinkingRow = () => {
  addRow({
    op: "add",
    path: "/thinking",
    valueMode: "object",
    valueText: '{\n  "type": "enabled",\n  "budget_tokens": 1024\n}',
  });
};

const addToolRow = () => {
  addRow({
    op: "add",
    path: "/tools/0",
    valueMode: "object",
    valueText: '{\n  "type": "web_search"\n}',
  });
};

const removeRow = (index: number) => {
  rows.value.splice(index, 1);
  emitRows();
};

const duplicateRow = (row: PatchRow) => {
  rows.value.push(createRow({ ...row }));
  emitRows();
};

const moveRow = (index: number, direction: -1 | 1) => {
  const nextIndex = index + direction;
  if (nextIndex < 0 || nextIndex >= rows.value.length) {
    return;
  }
  const [row] = rows.value.splice(index, 1);
  if (!row) {
    return;
  }
  rows.value.splice(nextIndex, 0, row);
  emitRows();
};

const updateOperation = (row: PatchRow, value: string) => {
  if (!isPatchOperation(value)) {
    return;
  }
  row.op = value;
  if (needsFrom(row.op) && !row.from) {
    row.from = "/metadata/user_id";
  }
  if (needsValue(row.op) && row.valueMode === "null" && row.op !== "test") {
    row.valueMode = "string";
  }
  emitRows();
};

const updateValueMode = (row: PatchRow, value: string) => {
  if (!isPatchValueMode(value)) {
    return;
  }
  row.valueMode = value;
  if (row.valueMode === "number") {
    row.valueText = Number.isFinite(Number(row.valueText)) ? row.valueText : "0";
  } else if (row.valueMode === "object") {
    row.valueText = isPlainObject(readValue(row).value) ? row.valueText : "{\n  \n}";
  } else if (row.valueMode === "array") {
    row.valueText = Array.isArray(readValue(row).value) ? row.valueText : "[\n  \n]";
  } else if (row.valueMode === "boolean") {
    row.boolValue = false;
  } else if (row.valueMode === "null") {
    row.valueText = "";
  }
  emitRows();
};

const normalizeRowPointer = (row: PatchRow, field: "path" | "from") => {
  row[field] = normalizePointerInput(row[field]);
  emitRows();
};

const setQuickPath = (row: PatchRow, path: string) => {
  row.path = path;
  emitRows();
};

const clearRows = () => {
  rows.value = [];
  parseError.value = "";
  isOpen.value = false;
  emitRows();
};

watch(
  () => props.modelValue,
  (value) => {
    if (value === lastEmittedValue.value) {
      return;
    }
    hydrateRows(value);
  },
  { immediate: true },
);
</script>

<template>
  <details
    class="block w-full rounded-xl border border-slate-200/70 bg-slate-50/60 px-4 py-3"
    :open="isOpen"
    @toggle="isOpen = ($event.target as HTMLDetailsElement).open"
  >
    <summary
      class="flex cursor-pointer list-none items-center justify-between gap-3 text-sm font-semibold text-slate-700"
    >
      <span class="flex min-w-0 items-center gap-2">
        <span>参数编辑</span>
        <span class="hidden text-xs font-normal text-slate-500 sm:inline">
          按顺序应用到上游请求体
        </span>
      </span>
      <span
        class="shrink-0 rounded-full border px-2 py-0.5 text-[11px] font-medium"
        :class="
          hasRowIssue || parseError
            ? 'border-rose-200 bg-rose-50 text-rose-600'
            : rows.length
              ? 'border-amber-200 bg-amber-50 text-amber-700'
              : 'border-slate-200 bg-white text-slate-500'
        "
      >
        JSON Patch · {{ operationCountLabel }}
      </span>
    </summary>

    <div class="mt-4 space-y-3">
      <div class="flex flex-wrap items-center gap-2">
        <button type="button" class="btn btn-xs btn-primary rounded-lg" @click="addRow()">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M5 12h14" />
            <path d="M12 5v14" />
          </svg>
          新增一项
        </button>
        <button
          type="button"
          class="btn btn-xs rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-amber-300 hover:bg-amber-50"
          @click="addThinkingRow"
        >
          Thinking
        </button>
        <button
          type="button"
          class="btn btn-xs rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-amber-300 hover:bg-amber-50"
          @click="addToolRow"
        >
          Tool
        </button>
        <button
          v-if="rows.length"
          type="button"
          class="btn btn-xs rounded-lg border border-slate-200 bg-white text-slate-500 hover:border-rose-200 hover:bg-rose-50 hover:text-rose-600"
          @click="clearRows"
        >
          清空
        </button>
      </div>

      <div
        v-if="parseError"
        class="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-700"
      >
        {{ parseError }}
      </div>

      <div
        v-if="!rows.length && !parseError"
        class="rounded-lg border border-dashed border-slate-200 bg-white/60 px-4 py-6 text-center text-sm text-slate-500"
      >
        当前不改写请求参数。需要新增、替换或删除字段时，点上方按钮添加规则。
      </div>

      <div v-else class="space-y-3">
        <div
          v-for="(row, index) in rows"
          :key="row.id"
          class="rounded-xl border bg-white p-3 shadow-sm"
          :class="rowIssues[index]?.length ? 'border-rose-200' : 'border-slate-200/80'"
        >
          <div class="flex flex-wrap items-start justify-between gap-3">
            <div class="grid flex-1 gap-3 md:grid-cols-[116px_minmax(0,1fr)]">
              <div>
                <div class="mb-1 text-xs font-medium text-slate-600">动作</div>
                <select
                  class="select select-sm w-full cursor-pointer rounded-lg border-slate-200 bg-slate-50 text-sm focus:border-amber-300 focus:outline-none"
                  :value="row.op"
                  @change="updateOperation(row, ($event.target as HTMLSelectElement).value)"
                >
                  <option
                    v-for="operation in PATCH_OPERATIONS"
                    :key="operation.value"
                    :value="operation.value"
                  >
                    {{ operation.label }}
                  </option>
                </select>
                <div class="mt-1 text-[11px] leading-4 text-slate-400">
                  {{
                    PATCH_OPERATIONS.find((operation) => operation.value === row.op)?.description
                  }}
                </div>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-600">目标路径</label>
                  <input
                    v-model="row.path"
                    class="input input-sm w-full rounded-lg border-slate-200 bg-slate-50 font-mono text-xs focus:border-amber-300 focus:outline-none"
                    placeholder="/temperature"
                    spellcheck="false"
                    @input="emitRows"
                    @blur="normalizeRowPointer(row, 'path')"
                  />
                  <div class="mt-1 flex flex-wrap gap-1">
                    <button
                      v-for="path in QUICK_PATHS"
                      :key="path"
                      type="button"
                      class="cursor-pointer rounded-md border border-slate-200 bg-white px-1.5 py-0.5 font-mono text-[10px] text-slate-500 hover:border-amber-300 hover:bg-amber-50 hover:text-amber-700"
                      @click="setQuickPath(row, path)"
                    >
                      {{ path }}
                    </button>
                  </div>
                </div>

                <div v-if="needsFrom(row.op)">
                  <label class="mb-1 block text-xs font-medium text-slate-600">来源路径</label>
                  <input
                    v-model="row.from"
                    class="input input-sm w-full rounded-lg border-slate-200 bg-slate-50 font-mono text-xs focus:border-amber-300 focus:outline-none"
                    placeholder="/metadata/user_id"
                    spellcheck="false"
                    @input="emitRows"
                    @blur="normalizeRowPointer(row, 'from')"
                  />
                </div>
              </div>
            </div>

            <div class="flex shrink-0 items-center gap-1">
              <button
                type="button"
                class="btn btn-ghost btn-xs btn-square rounded-lg text-slate-500"
                :disabled="index === 0"
                title="上移"
                @click="moveRow(index, -1)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="m18 15-6-6-6 6" />
                </svg>
              </button>
              <button
                type="button"
                class="btn btn-ghost btn-xs btn-square rounded-lg text-slate-500"
                :disabled="index === rows.length - 1"
                title="下移"
                @click="moveRow(index, 1)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="m6 9 6 6 6-6" />
                </svg>
              </button>
              <button
                type="button"
                class="btn btn-ghost btn-xs btn-square rounded-lg text-slate-500"
                title="复制"
                @click="duplicateRow(row)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
                  <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
                </svg>
              </button>
              <button
                type="button"
                class="btn btn-ghost btn-xs btn-square rounded-lg text-rose-500 hover:bg-rose-50"
                title="删除"
                @click="removeRow(index)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M3 6h18" />
                  <path d="M8 6V4h8v2" />
                  <path d="M19 6l-1 14H6L5 6" />
                </svg>
              </button>
            </div>
          </div>

          <div v-if="needsValue(row.op)" class="mt-3 grid gap-3 md:grid-cols-[120px_minmax(0,1fr)]">
            <div>
              <label class="mb-1 block text-xs font-medium text-slate-600">值类型</label>
              <select
                class="select select-sm w-full cursor-pointer rounded-lg border-slate-200 bg-slate-50 text-sm focus:border-amber-300 focus:outline-none"
                :value="row.valueMode"
                @change="updateValueMode(row, ($event.target as HTMLSelectElement).value)"
              >
                <option v-for="mode in VALUE_MODES" :key="mode.value" :value="mode.value">
                  {{ mode.label }}
                </option>
              </select>
            </div>

            <div v-if="row.valueMode === 'boolean'">
              <label class="mb-1 block text-xs font-medium text-slate-600">值</label>
              <select
                v-model="row.boolValue"
                class="select select-sm w-full cursor-pointer rounded-lg border-slate-200 bg-slate-50 text-sm focus:border-amber-300 focus:outline-none"
                @change="emitRows"
              >
                <option :value="true">true</option>
                <option :value="false">false</option>
              </select>
            </div>

            <div v-else-if="row.valueMode === 'null'">
              <label class="mb-1 block text-xs font-medium text-slate-600">值</label>
              <div
                class="flex h-9 items-center rounded-lg border border-slate-200 bg-slate-50 px-3 font-mono text-xs text-slate-500"
              >
                null
              </div>
            </div>

            <div v-else>
              <label class="mb-1 block text-xs font-medium text-slate-600">值</label>
              <textarea
                v-if="row.valueMode === 'object' || row.valueMode === 'array'"
                v-model="row.valueText"
                class="min-h-24 w-full resize-y rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 font-mono text-xs leading-5 text-slate-800 outline-none transition focus:border-amber-300 focus:ring-4 focus:ring-amber-100"
                spellcheck="false"
                @input="emitRows"
              ></textarea>
              <input
                v-else
                v-model="row.valueText"
                class="input input-sm w-full rounded-lg border-slate-200 bg-slate-50 font-mono text-xs focus:border-amber-300 focus:outline-none"
                :type="row.valueMode === 'number' ? 'number' : 'text'"
                spellcheck="false"
                @input="emitRows"
              />
            </div>
          </div>

          <div
            v-if="rowIssues[index]?.length"
            class="mt-3 rounded-lg border border-rose-100 bg-rose-50 px-3 py-2 text-xs leading-5 text-rose-700"
          >
            {{ rowIssues[index]?.join(" / ") }}
          </div>
        </div>
      </div>

      <div class="text-xs leading-5 text-slate-500">
        参数编辑优先级高于 provider 适配层，请谨慎使用，任何后果自行承担。保存时按 JSON Patch
        校验；stream 字段不可修改。
      </div>
    </div>
  </details>
</template>

<script setup lang="ts">
const REQUEST_BODY_PATCH_TOOLTIP = [
  "格式：JSON Patch 数组，按从上到下的顺序依次应用。",
  "path 使用 JSON Pointer：/thinking 表示根对象字段，/tools/0 表示数组第 1 项;",
  "value 可写字符串、数字、布尔、对象或数组。",
  "add：新增字段或数组元素。",
  "remove：删除已有字段或数组元素。",
  "replace：替换已有字段的值。",
  "copy：把 from 指向的值复制到 path。",
  "move：把 from 指向的值移动到 path，原位置会被移除。",
  "test：断言 path 当前值等于 value；失败时本次参数编辑失败。",
  "限制：不允许修改 stream。",
].join("\n");

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

const isOpen = computed({
  get: () => props.open,
  set: (value) => {
    emit("update:open", value);
  },
});

const updateModelValue = (event: Event) => {
  if (event.target instanceof HTMLTextAreaElement) {
    emit("update:modelValue", event.target.value);
  }
};
</script>

<template>
  <details
    class="tooltip mtga-tooltip block w-full rounded-xl border border-slate-200/70 bg-slate-50/60 px-4 py-3"
    :data-tip="REQUEST_BODY_PATCH_TOOLTIP"
    style="--mtga-tooltip-max: 520px"
    :open="isOpen"
    @toggle="isOpen = ($event.target as HTMLDetailsElement).open"
  >
    <summary
      class="flex cursor-pointer list-none items-center justify-between gap-3 text-sm font-semibold text-slate-700"
    >
      <span class="flex min-w-0 items-center gap-2">
        <span>参数编辑</span>
      </span>
      <span
        class="rounded-full border border-slate-200 bg-white px-2 py-0.5 text-[11px] font-medium text-slate-500"
      >
        JSON Patch
      </span>
    </summary>
    <div class="mt-3">
      <textarea
        :value="modelValue"
        class="min-h-36 w-full resize-y rounded-lg border border-slate-200 bg-white px-3 py-2 font-mono text-xs leading-5 text-slate-800 outline-none transition focus:border-amber-300 focus:ring-4 focus:ring-amber-100"
        spellcheck="false"
        placeholder='[
  {"op":"add","path":"/thinking","value":{"type":"enabled","budget_tokens":1024}},
  {"op":"replace","path":"/temperature","value":0.2},
  {"op":"add","path":"/tools/0","value":{"type":"web_search"}},
  {"op":"copy","from":"/metadata/user_id","path":"/user"},
  {"op":"test","path":"/model","value":"Qwen/Qwen3.5-27B"}
]'
        @input="updateModelValue"
      ></textarea>
      <div class="mt-2 text-xs leading-5 text-slate-500">
        此处优先级高于 provider 适配层，请谨慎使用，任何后果自行承担。
      </div>
    </div>
  </details>
</template>

<script setup lang="ts">
import {
  type ThemeColorKey,
  type ThemeConfig,
  DEFAULT_THEME_CONFIG,
  THEME_COLOR_FIELDS,
  copyThemeConfig,
  normalizeHexColor,
  parseCustomColorInput,
  resolveColorValue,
  resolvePickerColor,
  resolveThemeBasePalette,
  sanitizeThemeConfig,
} from "~/composables/themeConfig";

const props = withDefaults(
  defineProps<{
    open?: boolean;
    config: ThemeConfig;
  }>(),
  {
    open: false,
  },
);

const emit = defineEmits<{
  (event: "update:open", value: boolean): void;
  (event: "save", value: ThemeConfig): void;
}>();

const openModel = computed({
  get: () => props.open,
  set: (value: boolean) => emit("update:open", value),
});

const themeError = ref("");
const backgroundInputRef = ref<HTMLInputElement | null>(null);
const themeDraft = reactive<ThemeConfig>({ ...DEFAULT_THEME_CONFIG });
const MAX_BACKGROUND_SIZE = 2 * 1024 * 1024;
const basePalette = ref<Record<ThemeColorKey, string>>(resolveThemeBasePalette());

type QueryLocalFontData = { family: string };
type QueryLocalFontsWindow = Window & {
  queryLocalFonts?: () => Promise<QueryLocalFontData[]>;
};

const createEmptyColorInput = (): Record<ThemeColorKey, string> => ({
  primaryColor: "",
  secondaryColor: "",
  textPrimaryColor: "",
  textSecondaryColor: "",
  infoColor: "",
  warningColor: "",
  errorColor: "",
  successColor: "",
});

const colorInput = reactive<Record<ThemeColorKey, string>>(createEmptyColorInput());
const fontListLoading = ref(false);
const fontListLoaded = ref(false);
const fontFamilies = ref<string[]>([]);
let fontLoadPromise: Promise<void> | null = null;

const getFieldLabel = (key: ThemeColorKey) =>
  THEME_COLOR_FIELDS.find((field) => field.key === key)?.label ?? key;

const normalizeFontFamily = (value: string) => value.trim().replace(/^["']+|["']+$/g, "");

const dedupeAndSortFontFamilies = (value: string[]) => {
  const unique = new Set<string>();
  for (const item of value) {
    const normalized = normalizeFontFamily(item);
    if (normalized) {
      unique.add(normalized);
    }
  }
  return Array.from(unique).sort((a, b) => a.localeCompare(b, "zh-Hans-CN"));
};

const fontInputDescription = computed(() => {
  if (fontListLoading.value) {
    return "正在读取系统字体列表...";
  }
  if (fontFamilies.value.length === 0) {
    return "未读取到系统字体，可手动输入并保存（不做系统校验）";
  }
  return `共 ${fontFamilies.value.length} 个系统字体，可输入关键字过滤`;
});

const findMatchedSystemFont = (value: string) => {
  const normalized = normalizeFontFamily(value).toLowerCase();
  if (!normalized) {
    return "";
  }
  return fontFamilies.value.find((family) => family.toLowerCase() === normalized) ?? "";
};

const loadSystemFontFamilies = async () => {
  if (typeof window === "undefined") {
    return;
  }
  if (fontListLoaded.value) {
    return;
  }
  if (fontLoadPromise) {
    await fontLoadPromise;
    return;
  }

  fontLoadPromise = (async () => {
    const queryLocalFonts = (window as QueryLocalFontsWindow).queryLocalFonts;
    if (typeof queryLocalFonts === "function") {
      try {
        const localFonts = await queryLocalFonts();
        const families = dedupeAndSortFontFamilies(
          localFonts.map((font) => (typeof font.family === "string" ? font.family : "")),
        );
        if (families.length > 0) {
          fontFamilies.value = families;
          const matched = findMatchedSystemFont(themeDraft.fontFamily);
          if (matched) {
            themeDraft.fontFamily = matched;
          }
          fontListLoaded.value = true;
          return;
        }
      } catch {
        // ignore and leave font list empty
      }
    }
    fontFamilies.value = [];
    fontListLoaded.value = false;
  })();

  fontListLoading.value = true;
  try {
    await fontLoadPromise;
  } finally {
    fontListLoading.value = false;
    fontLoadPromise = null;
  }
};

const syncColorStateFromConfig = (config: ThemeConfig) => {
  for (const field of THEME_COLOR_FIELDS) {
    const key = field.key;
    const configured = normalizeHexColor(config[key]);
    if (/^#([0-9A-F]{6}|[0-9A-F]{8})$/.test(configured)) {
      themeDraft[key] = configured;
      colorInput[key] = configured;
    } else {
      themeDraft[key] = "";
      colorInput[key] = "";
    }
  }
};

const buildThemeConfigForSave = (): { payload: ThemeConfig | null; error: string } => {
  const payload = sanitizeThemeConfig(themeDraft);
  for (const field of THEME_COLOR_FIELDS) {
    const key = field.key;
    const raw = colorInput[key].trim();
    if (!raw) {
      payload[key] = "";
      continue;
    }
    const parsed = parseCustomColorInput(raw);
    if (!parsed) {
      return {
        payload: null,
        error: `${field.label} 必须是 6 位或 8 位十六进制颜色值`,
      };
    }
    payload[key] = parsed;
  }
  return { payload, error: "" };
};

const getPickerColor = (key: ThemeColorKey, value: string) => {
  return resolvePickerColor(key, value, basePalette.value);
};

const getPreviewColor = (key: ThemeColorKey, value: string) => {
  return resolveColorValue(key, value, basePalette.value);
};

const refreshBasePalette = () => {
  basePalette.value = resolveThemeBasePalette();
};

const onThemeColorInputBlur = (key: ThemeColorKey) => {
  const raw = colorInput[key].trim();
  if (!raw) {
    themeDraft[key] = "";
    colorInput[key] = "";
    themeError.value = "";
    return;
  }
  const parsed = parseCustomColorInput(raw);
  if (parsed) {
    themeDraft[key] = parsed;
    colorInput[key] = parsed;
    themeError.value = "";
    return;
  }
  themeError.value = `${getFieldLabel(key)} 必须是 6 位或 8 位十六进制颜色值`;
};

const onThemeColorPickerInput = (key: ThemeColorKey, event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  const normalized = normalizeHexColor(target.value);
  themeDraft[key] = normalized;
  colorInput[key] = normalized;
  themeError.value = "";
};

const resetDraft = () => {
  const normalized = sanitizeThemeConfig(props.config);
  copyThemeConfig(themeDraft, normalized);
  syncColorStateFromConfig(normalized);
  themeError.value = "";
};

watch(
  () => props.open,
  (open) => {
    if (open) {
      refreshBasePalette();
      resetDraft();
      void loadSystemFontFamilies();
    }
  },
);

watch(
  () => props.config,
  () => {
    if (props.open) {
      refreshBasePalette();
      resetDraft();
    }
  },
  { deep: true },
);

const handleClose = () => {
  themeError.value = "";
};

const handleCancel = () => {
  openModel.value = false;
  themeError.value = "";
};

const handleSave = async () => {
  await loadSystemFontFamilies();
  const normalizedFont = normalizeFontFamily(themeDraft.fontFamily);
  if (normalizedFont) {
    if (fontFamilies.value.length > 0) {
      const matched = findMatchedSystemFont(normalizedFont);
      if (!matched) {
        themeError.value = "字体必须从系统字体列表中选择";
        return;
      }
      themeDraft.fontFamily = matched;
    } else {
      themeDraft.fontFamily = normalizedFont;
    }
  }
  const { payload, error } = buildThemeConfigForSave();
  if (!payload) {
    themeError.value = error;
    return;
  }
  emit("save", payload);
  openModel.value = false;
  themeError.value = "";
};

const handleReset = () => {
  refreshBasePalette();
  const normalized = sanitizeThemeConfig({ ...DEFAULT_THEME_CONFIG });
  copyThemeConfig(themeDraft, normalized);
  syncColorStateFromConfig(normalized);
  themeError.value = "";
};

const openBackgroundPicker = () => {
  backgroundInputRef.value?.click();
};

const clearBackground = () => {
  themeDraft.backgroundImage = "";
};

const handleBackgroundFileChange = (event: Event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) {
    return;
  }
  const [file] = target.files ?? [];
  target.value = "";
  if (!file) {
    return;
  }
  if (!file.type.startsWith("image/")) {
    themeError.value = "仅支持图片文件";
    return;
  }
  if (file.size > MAX_BACKGROUND_SIZE) {
    themeError.value = "背景图片不能超过 2MB";
    return;
  }
  const reader = new FileReader();
  reader.onload = () => {
    if (typeof reader.result === "string") {
      themeDraft.backgroundImage = reader.result;
      themeError.value = "";
    }
  };
  reader.onerror = () => {
    themeError.value = "读取背景图片失败，请重试";
  };
  reader.readAsDataURL(file);
};
</script>

<template>
  <MtgaDialog v-model:open="openModel" max-width="max-w-3xl" @close="handleClose">
    <template #header>
      <div class="flex items-start justify-between gap-3">
        <div class="space-y-1">
          <h3 class="text-lg font-semibold text-slate-900">主题配置</h3>
          <p class="text-xs text-slate-500">保存后会立即应用到当前界面，并持久化到本地。</p>
        </div>
        <button
          class="btn btn-xs h-7 rounded-lg border-slate-200 bg-white px-3 font-medium text-slate-600 hover:border-rose-500 hover:bg-rose-50 hover:text-rose-600 transition-all"
          @click="handleReset"
        >
          重置
        </button>
      </div>
    </template>

    <div class="px-6 py-5 space-y-5">
      <div class="grid gap-3 md:grid-cols-2">
        <div
          v-for="field in THEME_COLOR_FIELDS"
          :key="field.key"
          class="group flex items-center gap-3 rounded-xl border border-slate-200/60 bg-white/50 p-2 transition-all hover:border-amber-200 hover:bg-white hover:shadow-sm"
        >
          <!-- 标签 -->
          <span
            class="text-sm font-semibold text-slate-500 min-w-[80px] pl-1 group-hover:text-amber-600 transition-colors"
          >
            {{ field.label }}
          </span>

          <div class="flex flex-1 items-center justify-end gap-2">
            <!-- 颜色预览和选择器 -->
            <div
              class="relative h-7 w-9 shrink-0 overflow-hidden rounded-md border border-slate-200 shadow-sm transition-transform active:scale-95"
            >
              <input
                type="color"
                class="absolute -inset-1 h-[150%] w-[150%] cursor-pointer opacity-0"
                :value="getPickerColor(field.key, colorInput[field.key])"
                @input="onThemeColorPickerInput(field.key, $event)"
              />
              <div
                class="h-full w-full pointer-events-none transition-colors duration-300"
                :style="{ backgroundColor: getPreviewColor(field.key, colorInput[field.key]) }"
              ></div>
            </div>

            <!-- 十六进制输入框 -->
            <MtgaInput
              v-model="colorInput[field.key]"
              class="w-22! shrink-0"
              size="xs"
              :clearable="false"
              input-class="font-mono text-[14px] tracking-tight"
              :placeholder="basePalette[field.key]"
              @blur="onThemeColorInputBlur(field.key)"
            />
          </div>
        </div>
      </div>

      <div
        class="rounded-2xl border border-slate-200/60 bg-white/50 p-4 transition-all hover:border-amber-200 hover:bg-white hover:shadow-sm"
      >
        <label class="mb-2 block text-sm font-semibold text-slate-500">字体</label>
        <MtgaInput
          v-model="themeDraft.fontFamily"
          class="w-full"
          size="sm"
          :options="fontFamilies"
          :show-dropdown="fontFamilies.length > 0"
          :loading="fontListLoading"
          placeholder="输入关键词过滤系统字体；留空跟随系统默认"
          :description="fontInputDescription"
          description-class="text-sm"
          @dropdown="void loadSystemFontFamilies()"
        />
      </div>

      <div
        class="rounded-2xl border border-slate-200/60 bg-white/50 p-4 space-y-3 transition-all hover:border-amber-200 hover:bg-white hover:shadow-sm"
      >
        <div class="flex items-center justify-between gap-3">
          <div>
            <div class="text-sm font-semibold text-slate-500">背景</div>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="btn btn-xs h-7 rounded-lg border-slate-200 bg-white px-3 font-medium text-slate-600 hover:border-amber-500 hover:bg-amber-50 hover:text-amber-600 transition-all"
              @click="openBackgroundPicker"
            >
              上传图片
            </button>
            <button
              class="btn btn-xs h-7 rounded-lg border-slate-200 bg-white px-3 font-medium text-slate-600 hover:border-rose-500 hover:bg-rose-50 hover:text-rose-600 transition-all"
              :disabled="!themeDraft.backgroundImage"
              @click="clearBackground"
            >
              清除
            </button>
          </div>
        </div>

        <input
          ref="backgroundInputRef"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleBackgroundFileChange"
        />

        <div
          class="relative h-28 overflow-hidden rounded-xl border border-dashed border-slate-200 bg-slate-50/70"
        >
          <img
            v-if="themeDraft.backgroundImage"
            :src="themeDraft.backgroundImage"
            alt="背景预览"
            class="h-full w-full object-cover"
          />
          <div v-else class="flex h-full items-center justify-center text-xs text-slate-400">
            未设置背景图片，将使用默认渐变背景
          </div>
        </div>
      </div>

      <div
        v-if="themeError"
        class="rounded-xl border border-error/30 bg-error/10 px-3 py-2 text-xs text-error"
      >
        {{ themeError }}
      </div>
    </div>

    <template #footer>
      <button class="mtga-btn-dialog-ghost flex-1" @click="handleCancel">取消</button>
      <button class="mtga-btn-dialog-primary flex-1" @click="handleSave">保存</button>
    </template>
  </MtgaDialog>
</template>

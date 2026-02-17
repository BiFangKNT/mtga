export type ThemeColorKey =
  | "primaryColor"
  | "secondaryColor"
  | "textPrimaryColor"
  | "textSecondaryColor"
  | "infoColor"
  | "warningColor"
  | "errorColor"
  | "successColor"

export type ThemeConfig = {
  primaryColor: string
  secondaryColor: string
  textPrimaryColor: string
  textSecondaryColor: string
  infoColor: string
  warningColor: string
  errorColor: string
  successColor: string
  fontFamily: string
  backgroundImage: string
}

export const THEME_STORAGE_KEY = "mtga-theme-config-v1"

export const DEFAULT_THEME_CONFIG: ThemeConfig = {
  primaryColor: "",
  secondaryColor: "",
  textPrimaryColor: "",
  textSecondaryColor: "",
  infoColor: "",
  warningColor: "",
  errorColor: "",
  successColor: "",
  fontFamily: "",
  backgroundImage: "",
}

export const THEME_COLOR_FIELDS: Array<{ key: ThemeColorKey; label: string }> = [
  { key: "primaryColor", label: "主要颜色" },
  { key: "secondaryColor", label: "次要颜色" },
  { key: "textPrimaryColor", label: "文本主要颜色" },
  { key: "textSecondaryColor", label: "文本次要颜色" },
  { key: "infoColor", label: "信息颜色" },
  { key: "warningColor", label: "警告颜色" },
  { key: "errorColor", label: "错误颜色" },
  { key: "successColor", label: "成功颜色" },
]

const HEX_COLOR_PATTERN = /^#([0-9A-F]{6}|[0-9A-F]{8})$/
const COLOR_VAR_MAP: Record<ThemeColorKey, string> = {
  primaryColor: "--color-primary",
  secondaryColor: "--mtga-accent-strong",
  textPrimaryColor: "--mtga-text",
  textSecondaryColor: "--mtga-text-muted",
  infoColor: "--color-info",
  warningColor: "--color-warning",
  errorColor: "--color-error",
  successColor: "--color-success",
}

const DAISY_COLOR_CLASS_MAP: Partial<Record<ThemeColorKey, string>> = {
  infoColor: "text-info",
  warningColor: "text-warning",
  errorColor: "text-error",
  successColor: "text-success",
}

const COLOR_HARD_FALLBACK: Record<ThemeColorKey, string> = {
  primaryColor: "#F0BB32",
  secondaryColor: "#D9A307",
  textPrimaryColor: "#0F172A",
  textSecondaryColor: "#64748B",
  infoColor: "#007AFF",
  warningColor: "#F59E0B",
  errorColor: "#FF3B30",
  successColor: "#06943D",
}

const isObjectRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value)

const isHexColor = (value: string) => HEX_COLOR_PATTERN.test(value)

export const normalizeHexColor = (value: string) => {
  const trimmed = value.trim().toUpperCase()
  if (!trimmed) {
    return ""
  }
  return trimmed.startsWith("#") ? trimmed : `#${trimmed}`
}

const parseRgbToHex = (value: string) => {
  const match = value.match(
    /^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*(\d*\.?\d+))?\s*\)$/i
  )
  if (!match) {
    return ""
  }

  const toHex = (channel: number) =>
    Math.max(0, Math.min(255, channel)).toString(16).padStart(2, "0").toUpperCase()

  const r = Number(match[1])
  const g = Number(match[2])
  const b = Number(match[3])
  const a = match[4] == null ? 1 : Number(match[4])
  const rgb = `${toHex(r)}${toHex(g)}${toHex(b)}`

  if (a >= 0.999 || Number.isNaN(a)) {
    return `#${rgb}`
  }
  if (a <= 0.001) {
    return ""
  }
  const alpha = Math.round(Math.max(0, Math.min(1, a)) * 255)
    .toString(16)
    .padStart(2, "0")
    .toUpperCase()
  return `#${rgb}${alpha}`
}

const rgbaBytesToHex = (r: number, g: number, b: number, a: number) => {
  const toHex = (channel: number) =>
    Math.max(0, Math.min(255, channel)).toString(16).padStart(2, "0").toUpperCase()
  const rgb = `${toHex(r)}${toHex(g)}${toHex(b)}`
  if (a >= 254) {
    return `#${rgb}`
  }
  if (a <= 0) {
    return ""
  }
  return `#${rgb}${toHex(a)}`
}

const parseColorWithCanvas = (value: string) => {
  if (typeof document === "undefined") {
    return ""
  }
  const canvas = document.createElement("canvas")
  canvas.width = 1
  canvas.height = 1
  const context = canvas.getContext("2d", { willReadFrequently: true })
  if (!context) {
    return ""
  }
  context.fillStyle = "rgba(1, 2, 3, 0.5)"
  const sentinel = context.fillStyle
  try {
    context.fillStyle = value
  } catch {
    return ""
  }
  if (context.fillStyle === sentinel && value.trim().toLowerCase() !== sentinel.toLowerCase()) {
    return ""
  }
  context.clearRect(0, 0, 1, 1)
  context.fillRect(0, 0, 1, 1)
  const pixel = context.getImageData(0, 0, 1, 1).data
  const r = pixel[0] ?? 0
  const g = pixel[1] ?? 0
  const b = pixel[2] ?? 0
  const a = pixel[3] ?? 255
  return rgbaBytesToHex(r, g, b, a)
}

export const parseCssColorToHex = (value: string) => {
  const normalized = normalizeHexColor(value)
  if (isHexColor(normalized)) {
    return normalized
  }

  const parsedByCanvas = parseColorWithCanvas(value)
  if (isHexColor(parsedByCanvas)) {
    return parsedByCanvas
  }

  const parsedRgb = parseRgbToHex(value)
  if (isHexColor(parsedRgb)) {
    return parsedRgb
  }

  if (typeof document === "undefined") {
    return ""
  }

  const probe = document.createElement("span")
  probe.style.color = ""
  probe.style.color = value
  if (!probe.style.color) {
    return ""
  }

  probe.style.display = "none"
  document.body.appendChild(probe)
  const computed = getComputedStyle(probe).color
  probe.remove()

  const parsedComputed = parseRgbToHex(computed)
  if (isHexColor(parsedComputed)) {
    return parsedComputed
  }

  const computedByCanvas = parseColorWithCanvas(computed)
  if (isHexColor(computedByCanvas)) {
    return computedByCanvas
  }

  return ""
}

export const parseCustomColorInput = (rawValue: string) => {
  const normalized = normalizeHexColor(rawValue)
  if (isHexColor(normalized)) {
    return normalized
  }
  const parsed = parseCssColorToHex(rawValue)
  if (isHexColor(parsed)) {
    return parsed
  }
  return ""
}

export const sanitizeThemeConfig = (input: unknown): ThemeConfig => {
  const theme = isObjectRecord(input) ? input : {}
  const toText = (value: unknown) => (typeof value === "string" ? value : "")

  return {
    primaryColor: normalizeHexColor(toText(theme.primaryColor)),
    secondaryColor: normalizeHexColor(toText(theme.secondaryColor)),
    textPrimaryColor: normalizeHexColor(toText(theme.textPrimaryColor)),
    textSecondaryColor: normalizeHexColor(toText(theme.textSecondaryColor)),
    infoColor: normalizeHexColor(toText(theme.infoColor)),
    warningColor: normalizeHexColor(toText(theme.warningColor)),
    errorColor: normalizeHexColor(toText(theme.errorColor)),
    successColor: normalizeHexColor(toText(theme.successColor)),
    fontFamily: toText(theme.fontFamily).trim(),
    backgroundImage: toText(theme.backgroundImage).trim(),
  }
}

export const copyThemeConfig = (target: ThemeConfig, source: ThemeConfig) => {
  target.primaryColor = source.primaryColor
  target.secondaryColor = source.secondaryColor
  target.textPrimaryColor = source.textPrimaryColor
  target.textSecondaryColor = source.textSecondaryColor
  target.infoColor = source.infoColor
  target.warningColor = source.warningColor
  target.errorColor = source.errorColor
  target.successColor = source.successColor
  target.fontFamily = source.fontFamily
  target.backgroundImage = source.backgroundImage
}

export const saveThemeToStorage = (theme: ThemeConfig) => {
  if (typeof window === "undefined") {
    return { ok: false, error: "当前环境不支持本地存储" } as const
  }
  try {
    window.localStorage.setItem(THEME_STORAGE_KEY, JSON.stringify(theme))
    return { ok: true } as const
  } catch (error) {
    if (error instanceof DOMException && error.name === "QuotaExceededError") {
      return { ok: false, error: "本地存储空间不足，请清理后重试" } as const
    }
    const message = error instanceof Error ? error.message : "未知错误"
    return { ok: false, error: message } as const
  }
}

export const loadThemeFromStorage = (): ThemeConfig | null => {
  if (typeof window === "undefined") {
    return null
  }

  try {
    const raw = window.localStorage.getItem(THEME_STORAGE_KEY)
    if (!raw) {
      return null
    }

    const parsed: unknown = JSON.parse(raw)
    if (!isObjectRecord(parsed)) {
      return null
    }
    const toOptionalText = (value: unknown) =>
      typeof value === "string" ? value : undefined

    return sanitizeThemeConfig({
      ...DEFAULT_THEME_CONFIG,
      primaryColor: toOptionalText(parsed.primaryColor) ?? DEFAULT_THEME_CONFIG.primaryColor,
      secondaryColor: toOptionalText(parsed.secondaryColor) ?? DEFAULT_THEME_CONFIG.secondaryColor,
      textPrimaryColor: toOptionalText(parsed.textPrimaryColor) ?? DEFAULT_THEME_CONFIG.textPrimaryColor,
      textSecondaryColor: toOptionalText(parsed.textSecondaryColor) ?? DEFAULT_THEME_CONFIG.textSecondaryColor,
      infoColor: toOptionalText(parsed.infoColor) ?? DEFAULT_THEME_CONFIG.infoColor,
      warningColor: toOptionalText(parsed.warningColor) ?? DEFAULT_THEME_CONFIG.warningColor,
      errorColor: toOptionalText(parsed.errorColor) ?? DEFAULT_THEME_CONFIG.errorColor,
      successColor: toOptionalText(parsed.successColor) ?? DEFAULT_THEME_CONFIG.successColor,
      fontFamily: toOptionalText(parsed.fontFamily) ?? DEFAULT_THEME_CONFIG.fontFamily,
      backgroundImage: toOptionalText(parsed.backgroundImage) ?? DEFAULT_THEME_CONFIG.backgroundImage,
    })
  } catch {
    return null
  }
}

export const applyThemeConfig = (theme: ThemeConfig) => {
  if (typeof document === "undefined") {
    return
  }

  const root = document.documentElement
  const setOrClearRootColor = (varName: string, value: string) => {
    if (value) {
      root.style.setProperty(varName, value, "important")
    } else {
      root.style.removeProperty(varName)
    }
  }

  setOrClearRootColor("--color-primary", theme.primaryColor)
  setOrClearRootColor("--mtga-accent", theme.primaryColor)
  setOrClearRootColor("--mtga-accent-strong", theme.secondaryColor)
  setOrClearRootColor("--mtga-text", theme.textPrimaryColor)
  setOrClearRootColor("--mtga-text-muted", theme.textSecondaryColor)
  setOrClearRootColor("--color-info", theme.infoColor)
  setOrClearRootColor("--color-warning", theme.warningColor)
  setOrClearRootColor("--color-error", theme.errorColor)
  setOrClearRootColor("--color-success", theme.successColor)

  const body = document.body
  if (!body) {
    return
  }

  if (theme.fontFamily) {
    root.style.setProperty("--mtga-theme-font-family", theme.fontFamily)
    body.style.fontFamily = theme.fontFamily
  } else {
    root.style.removeProperty("--mtga-theme-font-family")
    body.style.removeProperty("font-family")
  }

  if (theme.backgroundImage) {
    const backgroundImage = theme.backgroundImage.replace(/"/g, '\\"')
    body.style.backgroundImage = `url("${backgroundImage}")`
    body.style.backgroundSize = "cover"
    body.style.backgroundPosition = "center"
    body.style.backgroundRepeat = "no-repeat"
  } else {
    body.style.removeProperty("background-image")
    body.style.removeProperty("background-size")
    body.style.removeProperty("background-position")
    body.style.removeProperty("background-repeat")
  }
}

const resolveColorFromClass = (className: string) => {
  if (typeof document === "undefined") {
    return ""
  }
  const probe = document.createElement("span")
  probe.className = className
  probe.style.display = "none"
  probe.textContent = "."
  document.body.appendChild(probe)
  const color = getComputedStyle(probe).color.trim()
  probe.remove()
  return parseCssColorToHex(color)
}

const resolveColorFromCssVar = (varName: string) => {
  if (typeof document === "undefined") {
    return ""
  }
  const raw = getComputedStyle(document.documentElement)
    .getPropertyValue(varName)
    .trim()
  if (!raw) {
    return ""
  }
  return parseCssColorToHex(raw)
}

const withClearedInlineRootVars = <T>(varNames: string[], callback: () => T) => {
  if (typeof document === "undefined") {
    return callback()
  }

  const root = document.documentElement
  const snapshots = varNames.map((name) => ({
    name,
    value: root.style.getPropertyValue(name),
    priority: root.style.getPropertyPriority(name),
  }))

  for (const item of snapshots) {
    root.style.removeProperty(item.name)
  }

  try {
    return callback()
  } finally {
    for (const item of snapshots) {
      if (item.value) {
        root.style.setProperty(item.name, item.value, item.priority || undefined)
      } else {
        root.style.removeProperty(item.name)
      }
    }
  }
}

export const resolveThemeBasePalette = (): Record<ThemeColorKey, string> => {
  const keys = Object.values(COLOR_VAR_MAP)
  return withClearedInlineRootVars([...new Set(keys)], () => {
    const palette: Record<ThemeColorKey, string> = {
      primaryColor: COLOR_HARD_FALLBACK.primaryColor,
      secondaryColor: COLOR_HARD_FALLBACK.secondaryColor,
      textPrimaryColor: COLOR_HARD_FALLBACK.textPrimaryColor,
      textSecondaryColor: COLOR_HARD_FALLBACK.textSecondaryColor,
      infoColor: COLOR_HARD_FALLBACK.infoColor,
      warningColor: COLOR_HARD_FALLBACK.warningColor,
      errorColor: COLOR_HARD_FALLBACK.errorColor,
      successColor: COLOR_HARD_FALLBACK.successColor,
    }
    for (const field of THEME_COLOR_FIELDS) {
      const key = field.key
      const fromVar = resolveColorFromCssVar(COLOR_VAR_MAP[key])
      if (isHexColor(fromVar)) {
        palette[key] = fromVar
        continue
      }
      const className = DAISY_COLOR_CLASS_MAP[key]
      if (className) {
        const fromClass = resolveColorFromClass(className)
        if (isHexColor(fromClass)) {
          palette[key] = fromClass
          continue
        }
      }
      palette[key] = COLOR_HARD_FALLBACK[key]
    }
    return palette
  })
}

export const resolveColorValue = (
  key: ThemeColorKey,
  rawValue: string,
  basePalette: Record<ThemeColorKey, string>
) => {
  const normalized = normalizeHexColor(rawValue)
  if (isHexColor(normalized)) {
    return normalized
  }
  const parsed = parseCssColorToHex(rawValue)
  if (isHexColor(parsed)) {
    return parsed
  }
  const fallback = basePalette[key]
  if (isHexColor(fallback)) {
    return fallback
  }
  return COLOR_HARD_FALLBACK[key]
}

export const resolvePickerColor = (
  key: ThemeColorKey,
  rawValue: string,
  basePalette: Record<ThemeColorKey, string>
) => {
  const resolved = resolveColorValue(key, rawValue, basePalette)
  if (/^#[0-9A-F]{8}$/.test(resolved)) {
    return resolved.slice(0, 7)
  }
  if (/^#[0-9A-F]{6}$/.test(resolved)) {
    return resolved
  }
  return "#000000"
}

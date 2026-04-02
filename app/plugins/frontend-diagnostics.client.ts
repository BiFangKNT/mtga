import { pyInvoke } from "tauri-plugin-pytauri-api";

type DiagnosticExtra = Record<string, string | number | boolean | null>;

type FrontendDiagnosticPayload = {
  kind: string;
  message: string;
  stack?: string | null;
  source?: string | null;
  url?: string | null;
  user_agent?: string | null;
  ready_state?: string | null;
  extra?: DiagnosticExtra;
};

const MAX_REPORTS = 30;
const MAX_TEXT_LENGTH = 4000;
const pendingReports: FrontendDiagnosticPayload[] = [];
const seenReports = new Set<string>();

let installed = false;
let flushInFlight = false;
let reportCount = 0;
let retryTimer: ReturnType<typeof setTimeout> | null = null;

const trimText = (value: unknown, max = MAX_TEXT_LENGTH): string | null => {
  if (value === null || value === undefined) {
    return null;
  }
  const text = String(value).trim();
  if (!text) {
    return null;
  }
  if (text.length <= max) {
    return text;
  }
  return `${text.slice(0, max - 1)}…`;
};

const isTauriRuntimeReady = () =>
  typeof window !== "undefined" && typeof window.__TAURI__?.core?.invoke === "function";

const describeValue = (value: unknown): Pick<FrontendDiagnosticPayload, "message" | "stack"> => {
  if (value instanceof Error) {
    return {
      message: trimText(value.message) || value.name,
      stack: trimText(value.stack, 12000),
    };
  }
  if (typeof value === "string") {
    return { message: trimText(value) || "Unknown error" };
  }
  try {
    return {
      message: trimText(JSON.stringify(value, null, 2)) || "Unknown error",
    };
  } catch {
    return { message: trimText(value) || "Unknown error" };
  }
};

const normalizeExtra = (value: Record<string, unknown>): DiagnosticExtra => {
  const entries = Object.entries(value)
    .map(([key, item]) => {
      if (item === null || item === undefined) {
        return [key, null] as const;
      }
      if (typeof item === "string" || typeof item === "number" || typeof item === "boolean") {
        return [key, item] as const;
      }
      try {
        return [key, trimText(JSON.stringify(item), 1000)] as const;
      } catch {
        return [key, trimText(String(item), 1000)] as const;
      }
    })
    .filter(([, item]) => item !== "");
  return Object.fromEntries(entries);
};

const getContextFields = () => ({
  url: trimText(window.location?.href, 1024),
  user_agent: trimText(window.navigator?.userAgent, 1024),
  ready_state: trimText(document.readyState, 64),
});

const buildFingerprint = (payload: FrontendDiagnosticPayload) =>
  [payload.kind, payload.message, payload.source || "", payload.stack?.slice(0, 512) || ""].join(
    "|",
  );

const scheduleFlush = () => {
  if (!isTauriRuntimeReady()) {
    return;
  }
  if (retryTimer) {
    clearTimeout(retryTimer);
    retryTimer = null;
  }
  queueMicrotask(() => {
    void flushPendingReports();
  });
};

const enqueueReport = (payload: FrontendDiagnosticPayload) => {
  if (reportCount >= MAX_REPORTS) {
    return;
  }
  const normalized: FrontendDiagnosticPayload = {
    ...payload,
    kind: trimText(payload.kind, 80) || "unknown",
    message: trimText(payload.message) || "Unknown error",
    stack: trimText(payload.stack, 12000),
    source: trimText(payload.source, 512),
    ...getContextFields(),
    extra: payload.extra && Object.keys(payload.extra).length ? payload.extra : undefined,
  };

  const fingerprint = buildFingerprint(normalized);
  if (seenReports.has(fingerprint)) {
    return;
  }
  seenReports.add(fingerprint);
  reportCount += 1;
  pendingReports.push(normalized);
  console.error(`[mtga][frontend:${normalized.kind}] ${normalized.message}`, normalized);
  scheduleFlush();
};

const flushPendingReports = async () => {
  if (flushInFlight || !isTauriRuntimeReady()) {
    return;
  }
  flushInFlight = true;
  try {
    while (pendingReports.length) {
      const current = pendingReports[0];
      try {
        await pyInvoke("frontend_report", current);
        pendingReports.shift();
      } catch (error) {
        console.warn("[mtga] frontend diagnostics report failed", error);
        if (!retryTimer) {
          retryTimer = setTimeout(() => {
            retryTimer = null;
            void flushPendingReports();
          }, 1000);
        }
        break;
      }
    }
  } finally {
    flushInFlight = false;
  }
};

const resolveResourceSource = (target: EventTarget | null): string | null => {
  if (!(target instanceof HTMLElement)) {
    return null;
  }
  const tag = target.tagName.toLowerCase();
  if (target instanceof HTMLScriptElement) {
    return trimText(`${tag}:${target.src || target.baseURI}`);
  }
  if (target instanceof HTMLLinkElement) {
    return trimText(`${tag}:${target.href || target.baseURI}`);
  }
  if (target instanceof HTMLImageElement) {
    return trimText(`${tag}:${target.currentSrc || target.src || target.baseURI}`);
  }
  return trimText(tag);
};

const handleWindowError = (event: Event) => {
  if (event instanceof ErrorEvent) {
    const described = describeValue(event.error || event.message);
    enqueueReport({
      kind: "window-error",
      message: described.message,
      stack: described.stack,
      source:
        trimText([event.filename, event.lineno, event.colno].filter(Boolean).join(":"), 512) ||
        null,
      extra: normalizeExtra({
        event_type: event.type,
      }),
    });
    return;
  }

  const source = resolveResourceSource(event.target);
  enqueueReport({
    kind: "resource-error",
    message: "Failed to load frontend resource",
    source,
    extra: normalizeExtra({
      event_type: event.type,
    }),
  });
};

const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
  const described = describeValue(event.reason);
  enqueueReport({
    kind: "unhandledrejection",
    message: described.message,
    stack: described.stack,
    extra: normalizeExtra({
      event_type: event.type,
    }),
  });
};

export default defineNuxtPlugin((nuxtApp) => {
  if (installed) {
    scheduleFlush();
    return;
  }

  installed = true;

  window.addEventListener("error", handleWindowError, true);
  window.addEventListener("unhandledrejection", handleUnhandledRejection);

  const previousErrorHandler = nuxtApp.vueApp.config.errorHandler;
  nuxtApp.vueApp.config.errorHandler = (error, instance, info) => {
    const described = describeValue(error);
    enqueueReport({
      kind: "vue-error",
      message: described.message,
      stack: described.stack,
      source: trimText(info, 512),
      extra: normalizeExtra({
        component:
          (instance as { $options?: { name?: string } } | null)?.$options?.name || "anonymous",
      }),
    });
    previousErrorHandler?.(error, instance, info);
  };

  scheduleFlush();
});

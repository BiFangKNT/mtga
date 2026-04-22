export const getRuntimeTag = (): string => {
  if (typeof window === "undefined") {
    return "";
  }
  const tauriCore = window.__TAURI__?.core;
  if (tauriCore?.invoke) {
    return "tauri";
  }
  const runtime = window.__MTGA_RUNTIME__;
  if (typeof runtime === "string" && runtime.trim()) {
    return runtime.trim().toLowerCase();
  }
  return "";
};

export const isTauriRuntime = (): boolean => getRuntimeTag() === "tauri";

export const isBundledRuntime = (): boolean => {
  if (typeof window === "undefined") {
    return false;
  }
  const runtime = window.__MTGA_RUNTIME__;
  if (runtime === "tauri" || runtime === "nuitka") {
    return true;
  }
  const protocol = window.location?.protocol?.replace(":", "");
  if (protocol === "tauri") {
    return true;
  }
  return window.location?.hostname === "tauri.localhost";
};

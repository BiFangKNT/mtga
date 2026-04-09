import { getCurrentScope, onScopeDispose, ref, watch } from "vue";
export function useObjectStorage(key, initial, listenToStorage = true) {
  const raw = localStorage.getItem(key);
  const data = ref(raw ? JSON.parse(raw) : initial);
  for (const key2 in initial) {
    if (data.value[key2] === void 0)
      data.value[key2] = initial[key2];
  }
  let updating = false;
  let wrote = "";
  watch(data, (value) => {
    if (updating)
      return;
    wrote = JSON.stringify(value);
    localStorage.setItem(key, wrote);
  }, { deep: true, flush: "post" });
  if (listenToStorage) {
    useEventListener(window, "storage", (e) => {
      if (e.key === key && e.newValue && e.newValue !== wrote) {
        updating = true;
        data.value = JSON.parse(e.newValue);
        updating = false;
      }
    });
  }
  return data;
}
export function useEventListener(target, type, listener, options) {
  target.addEventListener(type, listener, options);
  if (getCurrentScope())
    onScopeDispose(() => target.removeEventListener(type, listener, options));
}

import { shallowRef, customRef, ref } from 'vue';
import { getInternalStore, findTraceAtPointer } from './record.mjs';
export { ElementTraceInfo, findTraceFromElement, findTraceFromVNode, hasData, recordPosition } from './record.mjs';

let createNanoEvents = () => ({
  emit(event, ...args) {
    for (
      let callbacks = this.events[event] || [],
        i = 0,
        length = callbacks.length;
      i < length;
      i++
    ) {
      callbacks[i](...args);
    }
  },
  events: {},
  on(event, cb) {
(this.events[event] ||= []).push(cb);
    return () => {
      this.events[event] = this.events[event]?.filter(i => cb !== i);
    }
  }
});

const lastMatchedElement = shallowRef();
const _store = getInternalStore();
const events = _store.events ||= createNanoEvents();
const isEnabled = customRef(() => {
  const value = ref(false);
  return {
    get() {
      return value.value;
    },
    set(newValue) {
      if (newValue === value.value)
        return;
      value.value = newValue;
      if (newValue)
        events.emit("enabled");
      else
        events.emit("disabled");
    }
  };
});
if (typeof document !== "undefined") {
  document.addEventListener("pointermove", (e) => {
    if (!isEnabled.value)
      return;
    const result = findTraceAtPointer({ x: e.clientX, y: e.clientY });
    if (result?.el === lastMatchedElement.value?.el)
      return;
    lastMatchedElement.value = result;
    events.emit("hover", result, e);
  });
  document.addEventListener("click", (e) => {
    if (!isEnabled.value)
      return;
    const result = findTraceAtPointer({ x: e.clientX, y: e.clientY });
    if (result) {
      events.emit("click", result, e);
      e.preventDefault();
      e.stopPropagation();
      e.stopImmediatePropagation();
      return false;
    }
  }, true);
}

export { events, findTraceAtPointer, getInternalStore, isEnabled, lastMatchedElement };

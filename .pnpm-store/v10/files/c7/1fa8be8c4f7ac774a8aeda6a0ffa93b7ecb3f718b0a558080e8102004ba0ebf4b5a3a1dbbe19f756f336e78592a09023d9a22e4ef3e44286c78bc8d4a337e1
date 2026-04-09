import { getCurrentScope, onScopeDispose, shallowRef } from "vue";
import { useNuxtApp } from "../nuxt.js";
function createAnnouncer(opts = {}) {
  const message = shallowRef("");
  const politeness = shallowRef(opts.politeness || "polite");
  function set(messageValue = "", politenessSetting = "polite") {
    message.value = messageValue;
    politeness.value = politenessSetting;
  }
  function polite(msg) {
    set(msg, "polite");
  }
  function assertive(msg) {
    set(msg, "assertive");
  }
  function _cleanup() {
    message.value = "";
    politeness.value = opts.politeness || "polite";
  }
  return {
    message,
    politeness,
    set,
    polite,
    assertive,
    _cleanup
  };
}
export function useAnnouncer(opts = {}) {
  const nuxtApp = useNuxtApp();
  const announcer = nuxtApp._announcer ||= createAnnouncer(opts);
  if (opts.politeness && opts.politeness !== announcer.politeness.value) {
    announcer.politeness.value = opts.politeness;
  }
  if (import.meta.client && getCurrentScope()) {
    nuxtApp._announcerDeps ||= 0;
    nuxtApp._announcerDeps++;
    onScopeDispose(() => {
      nuxtApp._announcerDeps--;
      if (nuxtApp._announcerDeps === 0) {
        announcer._cleanup();
        delete nuxtApp._announcer;
      }
    });
  }
  return announcer;
}

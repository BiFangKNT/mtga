import { computed, getCurrentScope, onScopeDispose, shallowRef } from "vue";
import { useNuxtApp } from "../nuxt.js";
function defaultEstimatedProgress(duration, elapsed) {
  const completionPercentage = elapsed / duration * 100;
  return 2 / Math.PI * 100 * Math.atan(completionPercentage / 50);
}
function createLoadingIndicator(opts = {}) {
  const { duration = 2e3, throttle = 200, hideDelay = 500, resetDelay = 400 } = opts;
  const getProgress = opts.estimatedProgress || defaultEstimatedProgress;
  const nuxtApp = useNuxtApp();
  const progress = shallowRef(0);
  const isLoading = shallowRef(false);
  const error = shallowRef(false);
  let done = false;
  let rafId;
  let throttleTimeout;
  let hideTimeout;
  let resetTimeout;
  const start = (opts2 = {}) => {
    _clearTimeouts();
    error.value = false;
    set(0, opts2);
  };
  function set(at = 0, opts2 = {}) {
    if (nuxtApp.isHydrating) {
      return;
    }
    if (at >= 100) {
      return finish({ force: opts2.force });
    }
    clear();
    progress.value = at < 0 ? 0 : at;
    const throttleTime = opts2.force ? 0 : throttle;
    if (throttleTime && import.meta.client) {
      throttleTimeout = setTimeout(() => {
        isLoading.value = true;
        _startProgress();
      }, throttleTime);
    } else {
      isLoading.value = true;
      _startProgress();
    }
  }
  function _hide() {
    if (import.meta.client) {
      hideTimeout = setTimeout(() => {
        isLoading.value = false;
        resetTimeout = setTimeout(() => {
          progress.value = 0;
        }, resetDelay);
      }, hideDelay);
    }
  }
  function finish(opts2 = {}) {
    progress.value = 100;
    done = true;
    clear();
    _clearTimeouts();
    if (opts2.error) {
      error.value = true;
    }
    if (opts2.force) {
      progress.value = 0;
      isLoading.value = false;
    } else {
      _hide();
    }
  }
  function _clearTimeouts() {
    if (import.meta.client) {
      clearTimeout(hideTimeout);
      clearTimeout(resetTimeout);
    }
  }
  function clear() {
    if (import.meta.client) {
      clearTimeout(throttleTimeout);
      cancelAnimationFrame(rafId);
    }
  }
  function _startProgress() {
    done = false;
    let startTimeStamp;
    function step(timeStamp) {
      if (done) {
        return;
      }
      startTimeStamp ??= timeStamp;
      const elapsed = timeStamp - startTimeStamp;
      progress.value = Math.max(0, Math.min(100, getProgress(duration, elapsed)));
      if (import.meta.client) {
        rafId = requestAnimationFrame(step);
      }
    }
    if (import.meta.client) {
      rafId = requestAnimationFrame(step);
    }
  }
  let _cleanup = () => {
  };
  if (import.meta.client) {
    const unsubLoadingStartHook = nuxtApp.hook("page:loading:start", () => {
      start();
    });
    const unsubLoadingFinishHook = nuxtApp.hook("page:loading:end", () => {
      finish();
    });
    const unsubError = nuxtApp.hook("vue:error", () => finish());
    _cleanup = () => {
      unsubError();
      unsubLoadingStartHook();
      unsubLoadingFinishHook();
      clear();
    };
  }
  return {
    _cleanup,
    progress: computed(() => progress.value),
    isLoading: computed(() => isLoading.value),
    error: computed(() => error.value),
    start,
    set,
    finish,
    clear
  };
}
export function useLoadingIndicator(opts = {}) {
  const nuxtApp = useNuxtApp();
  const indicator = nuxtApp._loadingIndicator ||= createLoadingIndicator(opts);
  if (import.meta.client && getCurrentScope()) {
    nuxtApp._loadingIndicatorDeps ||= 0;
    nuxtApp._loadingIndicatorDeps++;
    onScopeDispose(() => {
      nuxtApp._loadingIndicatorDeps--;
      if (nuxtApp._loadingIndicatorDeps === 0) {
        indicator._cleanup();
        delete nuxtApp._loadingIndicator;
      }
    });
  }
  return indicator;
}

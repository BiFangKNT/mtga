import { getCurrentInstance, withAsyncContext as withVueAsyncContext } from "vue";
export function withAsyncContext(fn) {
  return withVueAsyncContext(() => {
    const nuxtApp = getCurrentInstance()?.appContext.app.$nuxt;
    return nuxtApp ? nuxtApp.runWithContext(fn) : fn();
  });
}

import { reactive } from "vue";
import { klona } from "klona";
import { useNuxtApp } from "./nuxt.js";
import __appConfig from "#build/app.config.mjs";
export const _getAppConfig = () => __appConfig;
function isPojoOrArray(val) {
  return Array.isArray(val) || !!val && typeof val === "object" && val.constructor?.name === "Object";
}
function deepDelete(obj, newObj) {
  if (Array.isArray(obj) && Array.isArray(newObj)) {
    obj.length = 0;
    obj.push(...newObj);
    return;
  }
  for (const key in obj) {
    const val = newObj[key];
    if (!(key in newObj)) {
      delete obj[key];
    }
    if (isPojoOrArray(val)) {
      deepDelete(obj[key], newObj[key]);
    }
  }
}
function deepAssign(obj, newObj) {
  for (const key in newObj) {
    if (key === "__proto__" || key === "constructor") {
      continue;
    }
    const val = newObj[key];
    if (isPojoOrArray(val)) {
      const defaultVal = Array.isArray(val) ? [] : {};
      if (Array.isArray(obj[key]) !== Array.isArray(val)) {
        obj[key] = defaultVal;
      } else {
        obj[key] ??= defaultVal;
      }
      deepAssign(obj[key], val);
    } else {
      obj[key] = val;
    }
  }
}
export function useAppConfig() {
  const nuxtApp = useNuxtApp();
  nuxtApp._appConfig ||= import.meta.server ? klona(__appConfig) : reactive(__appConfig);
  return nuxtApp._appConfig;
}
export function _replaceAppConfig(newConfig) {
  const appConfig = useAppConfig();
  deepAssign(appConfig, newConfig);
  deepDelete(appConfig, newConfig);
}
export function updateAppConfig(appConfig) {
  const _appConfig = useAppConfig();
  deepAssign(_appConfig, appConfig);
}
if (import.meta.dev) {
  if (import.meta.hot) {
    import.meta.hot.accept((newModule) => {
      const newConfig = newModule?._getAppConfig();
      if (newConfig) {
        _replaceAppConfig(newConfig);
      }
    });
  }
  if (import.meta.webpackHot) {
    import.meta.webpackHot.accept("#build/app.config.mjs", () => {
      _replaceAppConfig(__appConfig);
    });
  }
}

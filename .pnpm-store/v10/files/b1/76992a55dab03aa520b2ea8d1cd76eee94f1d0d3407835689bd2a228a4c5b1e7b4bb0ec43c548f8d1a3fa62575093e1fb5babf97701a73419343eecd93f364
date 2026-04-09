import { hasProtocol, joinURL } from "ufo";
import { parse } from "devalue";
import { getCurrentInstance, onServerPrefetch, reactive } from "vue";
import { useNuxtApp, useRuntimeConfig } from "../nuxt.js";
import { useHead } from "./head.js";
import { useRoute } from "./router.js";
import { getAppManifest, getRouteRules } from "./manifest.js";
import { appId, appManifest, multiApp, payloadExtraction, renderJsonPayloads } from "#build/nuxt.config.mjs";
export async function loadPayload(url, opts = {}) {
  if (import.meta.server || !payloadExtraction) {
    return null;
  }
  if (await shouldLoadPayload(url)) {
    const payloadURL = await _getPayloadURL(url, opts);
    return await _importPayload(payloadURL) || null;
  }
  return null;
}
let linkRelType;
function detectLinkRelType() {
  if (import.meta.server) {
    return "preload";
  }
  if (linkRelType) {
    return linkRelType;
  }
  const relList = document.createElement("link").relList;
  linkRelType = relList && relList.supports && relList.supports("prefetch") ? "prefetch" : "preload";
  return linkRelType;
}
export function preloadPayload(url, opts = {}) {
  const nuxtApp = useNuxtApp();
  const promise = shouldLoadPayload(url).then(async (shouldPreload) => {
    if (!shouldPreload) {
      return;
    }
    const payloadURL = await _getPayloadURL(url, opts);
    const link = renderJsonPayloads ? { rel: detectLinkRelType(), as: "fetch", crossorigin: "anonymous", href: payloadURL } : { rel: "modulepreload", crossorigin: "", href: payloadURL };
    if (import.meta.server) {
      nuxtApp.runWithContext(() => useHead({ link: [link] }));
    } else {
      const linkEl = document.createElement("link");
      for (const key of Object.keys(link)) {
        linkEl[key === "crossorigin" ? "crossOrigin" : key] = link[key];
      }
      document.head.appendChild(linkEl);
      return new Promise((resolve, reject) => {
        linkEl.addEventListener("load", () => resolve());
        linkEl.addEventListener("error", () => reject());
      });
    }
  });
  if (import.meta.server) {
    onServerPrefetch(() => promise);
  }
  return promise;
}
const filename = renderJsonPayloads ? "_payload.json" : "_payload.js";
async function _getPayloadURL(url, opts = {}) {
  const u = new URL(url, "http://localhost");
  if (u.host !== "localhost" || hasProtocol(u.pathname, { acceptRelative: true })) {
    throw new Error("Payload URL must not include hostname: " + url);
  }
  const config = useRuntimeConfig();
  const hash = opts.hash || (opts.fresh || import.meta.dev ? Date.now() : config.app.buildId);
  const cdnURL = config.app.cdnURL;
  const baseOrCdnURL = cdnURL && await isPrerendered(url) ? cdnURL : config.app.baseURL;
  return joinURL(baseOrCdnURL, u.pathname, filename + (hash ? `?${hash}` : ""));
}
async function _importPayload(payloadURL) {
  if (import.meta.server || !payloadExtraction) {
    return null;
  }
  const payloadPromise = renderJsonPayloads ? fetch(payloadURL, import.meta.dev ? {} : { cache: "force-cache" }).then((res) => res.text().then(parsePayload)) : import(
    /* webpackIgnore: true */
    /* @vite-ignore */
    payloadURL
  ).then((r) => r.default || r);
  try {
    return await payloadPromise;
  } catch (err) {
    console.warn("[nuxt] Cannot load payload ", payloadURL, err);
  }
  return null;
}
function _shouldLoadPrerenderedPayload(rules) {
  if (rules.redirect) {
    return false;
  }
  if (rules.prerender) {
    return true;
  }
}
async function _isPrerenderedInManifest(url) {
  if (!appManifest) {
    return false;
  }
  url = url === "/" ? url : url.replace(/\/$/, "");
  const manifest = await getAppManifest();
  return manifest.prerendered.includes(url);
}
export async function shouldLoadPayload(url = useRoute().path) {
  const rules = getRouteRules({ path: url });
  if (rules.ssr === false) {
    return false;
  }
  const res = _shouldLoadPrerenderedPayload(rules);
  if (res !== void 0) {
    return res;
  }
  if (rules.payload) {
    return true;
  }
  const prerendered = await _isPrerenderedInManifest(url);
  return prerendered;
}
export async function isPrerendered(url = useRoute().path) {
  const res = _shouldLoadPrerenderedPayload(getRouteRules({ path: url }));
  if (res !== void 0) {
    return res;
  }
  const prerendered = await _isPrerenderedInManifest(url);
  return prerendered;
}
let payloadCache = null;
export async function getNuxtClientPayload() {
  if (import.meta.server) {
    return null;
  }
  if (payloadCache) {
    return payloadCache;
  }
  const el = multiApp ? document.querySelector(`[data-nuxt-data="${appId}"]`) : document.getElementById("__NUXT_DATA__");
  if (!el) {
    return {};
  }
  const inlineData = await parsePayload(el.textContent || "");
  const externalData = el.dataset.src ? await _importPayload(el.dataset.src) : void 0;
  payloadCache = {
    ...inlineData,
    ...externalData,
    ...multiApp ? window.__NUXT__?.[appId] : window.__NUXT__
  };
  if (payloadCache.config?.public) {
    payloadCache.config.public = reactive(payloadCache.config.public);
  }
  return payloadCache;
}
export async function parsePayload(payload) {
  return await parse(payload, useNuxtApp()._payloadRevivers);
}
export function definePayloadReducer(name, reduce) {
  if (import.meta.server) {
    useNuxtApp().ssrContext["~payloadReducers"][name] = reduce;
  }
}
export function definePayloadReviver(name, revive) {
  if (import.meta.dev && getCurrentInstance()) {
    console.warn("[nuxt] [definePayloadReviver] This function must be called in a Nuxt plugin that is `unshift`ed to the beginning of the Nuxt plugins array.");
  }
  if (import.meta.client) {
    useNuxtApp()._payloadRevivers[name] = revive;
  }
}

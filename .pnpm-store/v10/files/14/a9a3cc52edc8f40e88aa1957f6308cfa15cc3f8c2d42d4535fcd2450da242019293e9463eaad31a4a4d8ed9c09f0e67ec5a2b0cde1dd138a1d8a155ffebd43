import { useRuntimeConfig } from "../nuxt.js";
import { appManifest as isAppManifestEnabled } from "#build/nuxt.config.mjs";
import { buildAssetsURL } from "#internal/nuxt/paths";
import _routeRulesMatcher from "#build/route-rules.mjs";
const routeRulesMatcher = _routeRulesMatcher;
let manifest;
function fetchManifest() {
  if (!isAppManifestEnabled) {
    throw new Error("[nuxt] app manifest should be enabled with `experimental.appManifest`");
  }
  if (import.meta.server) {
    manifest = import(
      /* webpackIgnore: true */
      /* @vite-ignore */
      "#app-manifest"
    );
  } else {
    manifest = $fetch(buildAssetsURL(`builds/meta/${useRuntimeConfig().app.buildId}.json`), {
      responseType: "json"
    });
  }
  manifest.catch((e) => {
    console.error("[nuxt] Error fetching app manifest.", e);
  });
  return manifest;
}
export function getAppManifest() {
  if (!isAppManifestEnabled) {
    throw new Error("[nuxt] app manifest should be enabled with `experimental.appManifest`");
  }
  return manifest || fetchManifest();
}
export function getRouteRules(arg) {
  const path = typeof arg === "string" ? arg : arg.path;
  try {
    return routeRulesMatcher(path);
  } catch (e) {
    console.error("[nuxt] Error matching route rules.", e);
    return {};
  }
}

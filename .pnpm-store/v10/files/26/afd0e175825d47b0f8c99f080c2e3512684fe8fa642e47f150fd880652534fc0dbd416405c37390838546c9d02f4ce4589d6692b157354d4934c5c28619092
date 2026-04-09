import { useAppConfig, useRuntimeConfig } from "#imports";
import { NuxtDevtoolsFrame, NuxtDevtoolsInspectPanel } from "@nuxt/devtools/webcomponents";
import { setIframeServerContext } from "@vue/devtools-kit";
import { createHooks } from "hookable";
import { debounce } from "perfect-debounce";
import { events as inspectorEvents, hasData as inspectorHasData, state as inspectorState } from "vite-plugin-vue-tracer/client/overlay";
import { computed, markRaw, nextTick, reactive, ref, shallowReactive, shallowRef, toRef, watch } from "vue";
import { initTimelineMetrics } from "../../function-metrics-helpers.js";
import { settings } from "../../settings.js";
import { popupWindow, state } from "./state.js";
const MULTIPLE_SLASHES_RE = /\/+/g;
const clientRef = shallowRef();
export { clientRef as client };
export async function setupDevToolsClient({
  nuxt,
  clientHooks,
  timeMetric,
  router
}) {
  let iframe;
  let inspector;
  const colorMode = useClientColorMode();
  const timeline = initTimelineMetrics();
  const client = shallowReactive({
    nuxt: markRaw(nuxt),
    hooks: createHooks(),
    inspector: getInspectorInstance(),
    getIframe,
    syncClient,
    devtools: {
      toggle() {
        if (state.value.open)
          client.devtools.close();
        else
          client.devtools.open();
      },
      close() {
        if (!state.value.open)
          return;
        state.value.open = false;
        if (popupWindow.value) {
          try {
            popupWindow.value.close();
          } catch {
          }
          popupWindow.value = null;
        }
      },
      open() {
        if (state.value.open)
          return;
        state.value.open = true;
      },
      async navigate(path) {
        if (!state.value.open)
          await client.devtools.open();
        await client.hooks.callHook("host:action:navigate", path);
      },
      async reload() {
        await client.hooks.callHook("host:action:reload");
      }
    },
    app: {
      appConfig: useAppConfig(),
      reload() {
        location.reload();
      },
      navigate(path, hard = false) {
        if (hard)
          location.href = path;
        else
          router.push(path);
      },
      colorMode,
      frameState: state,
      $fetch: globalThis.$fetch
    },
    metrics: {
      clientPlugins: () => window.__NUXT_DEVTOOLS_PLUGINS_METRIC__,
      clientHooks: () => Object.values(clientHooks),
      clientTimeline: () => timeline,
      loading: () => timeMetric
    },
    revision: ref(0)
  });
  window.__NUXT_DEVTOOLS_HOST__ = client;
  function syncClient() {
    if (!client.inspector)
      client.inspector = getInspectorInstance();
    try {
      iframe?.contentWindow?.__NUXT_DEVTOOLS_VIEW__?.setClient(client);
    } catch (e) {
      console.error("[nuxt-devtools] Failed to connect view", e);
    }
    return client;
  }
  function getIframe() {
    if (!iframe) {
      const runtimeConfig = useRuntimeConfig();
      const CLIENT_BASE = "/__nuxt_devtools__/client";
      const CLIENT_PATH = `${runtimeConfig.app.baseURL.replace(CLIENT_BASE, "/")}${CLIENT_BASE}`.replace(MULTIPLE_SLASHES_RE, "/");
      const initialUrl = CLIENT_PATH + state.value.route;
      iframe = document.createElement("iframe");
      for (const [key, value] of Object.entries(runtimeConfig.app.devtools?.iframeProps || {}))
        iframe.setAttribute(key, String(value));
      iframe.id = "nuxt-devtools-iframe";
      iframe.src = initialUrl;
      iframe.onload = async () => {
        try {
          setIframeServerContext(iframe);
          await waitForClientInjection();
          client.syncClient();
        } catch (e) {
          console.error("Nuxt DevTools client injection failed");
          console.error(e);
        }
      };
    }
    return iframe;
  }
  function waitForClientInjection(retry = 20, timeout = 300) {
    let lastError;
    const test = () => {
      try {
        return !!iframe?.contentWindow?.__NUXT_DEVTOOLS_VIEW__;
      } catch (e) {
        lastError = e;
      }
      return false;
    };
    if (test())
      return;
    return new Promise((resolve, reject) => {
      const interval = setInterval(() => {
        if (test()) {
          clearInterval(interval);
          resolve();
        } else if (retry-- <= 0) {
          clearInterval(interval);
          reject(lastError);
        }
      }, timeout);
    });
  }
  function getInspectorInstance() {
    if (inspector)
      return inspector;
    const props = reactive({
      mouse: { x: 0, y: 0 },
      hasParent: false,
      matched: void 0
    });
    const component = new NuxtDevtoolsInspectPanel(reactive({ props }));
    document.body.appendChild(component);
    Object.assign(component.style, {
      zIndex: 999999,
      position: "fixed",
      left: "0",
      top: "0"
    });
    component.addEventListener("close", () => {
      props.matched = void 0;
      inspectorState.isEnabled = false;
      inspectorState.isVisible = false;
    });
    component.addEventListener("selectParent", () => {
      const parent = inspectorState.main?.getParent();
      if (parent) {
        inspectorState.main = parent;
        props.matched = parent;
        nextTick(() => {
          props.hasParent = !!inspectorState.main?.getParent();
        });
      }
    });
    component.addEventListener("openInEditor", async (e) => {
      const url = e?.detail?.[0];
      if (url)
        await client.hooks.callHook("host:inspector:click", url);
    });
    inspectorEvents.on("hover", () => {
      inspectorState.isFocused = false;
      props.hasParent = !!inspectorState.main?.getParent();
    });
    inspectorEvents.on("disabled", () => {
      inspectorState.isVisible = false;
      client?.hooks.callHook("host:inspector:close");
    });
    inspectorEvents.on("enabled", () => {
      inspectorState.isVisible = true;
      inspectorState.isEnabled = true;
    });
    inspectorEvents.on("click", async (info, e) => {
      inspectorState.isEnabled = false;
      inspectorState.isFocused = true;
      inspectorState.isVisible = true;
      props.matched = info;
      props.mouse = { x: e.clientX, y: e.clientY };
    });
    const isAvailable = ref(inspectorHasData());
    if (!isAvailable.value) {
      inspectorEvents.on("hover", async () => {
        isAvailable.value = inspectorHasData();
      });
    }
    return inspector = markRaw({
      isAvailable,
      isEnabled: toRef(inspectorState, "isVisible"),
      enable: () => {
        inspectorState.isVisible = true;
        inspectorState.isEnabled = true;
      },
      disable: () => {
        inspectorState.isVisible = false;
        inspectorState.isEnabled = false;
      },
      toggle: () => {
        inspectorState.isEnabled = !inspectorState.isEnabled;
        inspectorState.isVisible = inspectorState.isEnabled;
      }
    });
  }
  setupRouteTracking(timeline, router);
  setupReactivity(client, router, timeline);
  clientRef.value = client;
  const documentPictureInPicture = window.documentPictureInPicture;
  if (documentPictureInPicture?.requestWindow) {
    client.devtools.popup = async () => {
      const iframe2 = getIframe();
      if (!iframe2)
        return;
      const pip = popupWindow.value = await documentPictureInPicture.requestWindow({
        width: Math.round(window.innerWidth * state.value.width / 100),
        height: Math.round(window.innerHeight * state.value.height / 100)
      });
      const style = pip.document.createElement("style");
      style.innerHTML = `
        body {
          margin: 0;
          padding: 0;
        }
        iframe {
          width: 100vw;
          height: 100vh;
          border: none;
          outline: none;
        }
      `;
      pip.__NUXT_DEVTOOLS_DISABLE__ = true;
      pip.__NUXT_DEVTOOLS_IS_POPUP__ = true;
      pip.__NUXT__ = window.parent?.__NUXT__ || window.__NUXT__;
      pip.document.title = "Nuxt DevTools";
      pip.document.head.appendChild(style);
      pip.document.body.appendChild(iframe2);
      pip.addEventListener("resize", () => {
        state.value.width = Math.round(pip.innerWidth / window.innerWidth * 100);
        state.value.height = Math.round(pip.innerHeight / window.innerHeight * 100);
      });
      pip.addEventListener("pagehide", () => {
        popupWindow.value = null;
        pip.close();
      });
    };
  }
  const holder = document.createElement("div");
  holder.id = "nuxt-devtools-container";
  holder.setAttribute("data-v-inspector-ignore", "true");
  document.body.appendChild(holder);
  window.addEventListener("keydown", (e) => {
    if (e.code === "KeyD" && e.altKey && e.shiftKey)
      client.devtools.toggle();
  });
  const frame = new NuxtDevtoolsFrame(reactive({
    client,
    settings,
    state,
    popupWindow
  }));
  holder.appendChild(frame);
}
export function useClientColorMode() {
  const explicitColor = ref();
  const systemColor = ref();
  const elements = [
    document.documentElement,
    document.body
  ];
  const ob = new MutationObserver(getExplicitColor);
  elements.forEach((el) => {
    ob.observe(el, {
      attributes: true,
      attributeFilter: ["class"]
    });
  });
  const preferDarkQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const preferLightQuery = window.matchMedia("(prefers-color-scheme: light)");
  preferDarkQuery.addEventListener("change", getSystemColor);
  preferLightQuery.addEventListener("change", getSystemColor);
  function getExplicitColor() {
    let color;
    for (const el of elements) {
      if (el.classList.contains("dark")) {
        color = "dark";
        break;
      }
      if (el.classList.contains("light")) {
        color = "light";
        break;
      }
    }
    explicitColor.value = color;
  }
  function getSystemColor() {
    if (preferDarkQuery.matches)
      systemColor.value = "dark";
    else if (preferLightQuery.matches)
      systemColor.value = "light";
    else
      systemColor.value = void 0;
  }
  getExplicitColor();
  getSystemColor();
  return computed(() => explicitColor.value || systemColor.value || "light");
}
function setupRouteTracking(timeline, router) {
  if (timeline.options.enabled && router?.currentRoute?.value?.path) {
    const start = timeline.events[0]?.start || Date.now();
    timeline.events.unshift({
      type: "route",
      from: router.currentRoute.value.path,
      to: router.currentRoute.value.path,
      start,
      end: start
    });
  }
  let lastRouteEvent;
  router?.afterEach(() => {
    if (lastRouteEvent && !lastRouteEvent?.end)
      lastRouteEvent.end = Date.now();
  });
  router?.beforeEach((to, from) => {
    if (!timeline.options.enabled)
      return;
    lastRouteEvent = {
      type: "route",
      from: from.path,
      to: to.path,
      start: Date.now()
    };
    timeline.events.push(lastRouteEvent);
  });
}
function setupReactivity(client, router, timeMetric) {
  const refreshReactivity = debounce(() => {
    client.hooks.callHook("host:update:reactivity");
  }, 100, { trailing: true });
  watch(() => [
    client.nuxt.payload,
    client.app.colorMode.value,
    client.metrics.loading(),
    timeMetric
  ], () => {
    refreshReactivity();
  }, { deep: true });
  router?.afterEach(() => {
    refreshReactivity();
  });
  client.nuxt.hook("app:mounted", () => {
    refreshReactivity();
  });
  client.hooks.hook("devtools:navigate", (path) => {
    state.value.route = path;
  });
}

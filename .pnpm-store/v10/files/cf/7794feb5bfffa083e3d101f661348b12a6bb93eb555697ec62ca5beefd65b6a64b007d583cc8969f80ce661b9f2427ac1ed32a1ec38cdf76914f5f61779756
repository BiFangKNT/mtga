import { createConsola } from "consola";
import { parse } from "devalue";
import { h } from "vue";
import { defineNuxtPlugin } from "../nuxt.js";
import { devLogs, devRootDir } from "#build/nuxt.config.mjs";
const devRevivers = import.meta.server ? {} : {
  VNode: (data) => h(data.type, data.props),
  URL: (data) => new URL(data)
};
export default defineNuxtPlugin(async (nuxtApp) => {
  if (import.meta.test) {
    return;
  }
  if (import.meta.server) {
    nuxtApp.ssrContext.event.context["~payloadReducers"] = nuxtApp.ssrContext["~payloadReducers"];
    return;
  }
  if (devLogs !== "silent") {
    const logger = createConsola({
      formatOptions: {
        colors: true,
        date: true
      }
    });
    nuxtApp.hook("dev:ssr-logs", (logs) => {
      for (const log of logs) {
        logger.log(normalizeServerLog({ ...log }));
      }
    });
  }
  if (typeof window !== "undefined") {
    const nuxtLogsElement = document.querySelector(`[data-nuxt-logs="${nuxtApp._id}"]`);
    const content = nuxtLogsElement?.textContent;
    const logs = content ? parse(content, { ...devRevivers, ...nuxtApp._payloadRevivers }) : [];
    await nuxtApp.hooks.callHook("dev:ssr-logs", logs);
  }
});
function normalizeFilenames(stack) {
  if (!stack) {
    return "";
  }
  let message = "";
  for (const item of stack) {
    const source = item.source.replace(`${devRootDir}/`, "");
    if (item.function) {
      message += `  at ${item.function} (${source})
`;
    } else {
      message += `  at ${source}
`;
    }
  }
  return message;
}
function normalizeServerLog(log) {
  log.additional = normalizeFilenames(log.stack);
  log.tag = "ssr";
  delete log.stack;
  return log;
}

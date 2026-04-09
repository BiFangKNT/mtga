import { useNuxt } from '@nuxt/kit';
import { execa } from 'execa';

function addCustomTab(tab, nuxt = useNuxt()) {
  nuxt.hook("devtools:customTabs", async (tabs) => {
    if (typeof tab === "function")
      tab = await tab();
    tabs.push(tab);
  });
}
function refreshCustomTabs(nuxt = useNuxt()) {
  return nuxt.callHook("devtools:customTabs:refresh");
}
function startSubprocess(execaOptions, tabOptions, nuxt = useNuxt()) {
  const id = tabOptions.id;
  let restarting = false;
  function start() {
    const process2 = execa(
      execaOptions.command,
      execaOptions.args,
      {
        reject: false,
        ...execaOptions,
        env: {
          COLORS: "true",
          FORCE_COLOR: "true",
          ...execaOptions.env,
          // Force disable Nuxi CLI override
          __CLI_ARGV__: void 0
        }
      }
    );
    nuxt.callHook("devtools:terminal:write", { id, data: `> ${[execaOptions.command, ...execaOptions.args || []].join(" ")}

` });
    process2.stdout.on("data", (data) => {
      nuxt.callHook("devtools:terminal:write", { id, data: data.toString() });
    });
    process2.stderr.on("data", (data) => {
      nuxt.callHook("devtools:terminal:write", { id, data: data.toString() });
    });
    process2.on("exit", (code) => {
      if (!restarting) {
        nuxt.callHook("devtools:terminal:write", { id, data: `
> process terminalated with ${code}
` });
        nuxt.callHook("devtools:terminal:exit", { id, code: code || 0 });
      }
    });
    return process2;
  }
  register();
  nuxt.hook("close", () => {
    terminate();
  });
  let process = start();
  function restart() {
    restarting = true;
    process?.kill();
    clear();
    process = start();
    restarting = false;
  }
  function clear() {
    tabOptions.buffer = "";
    register();
  }
  function terminate() {
    restarting = false;
    try {
      process?.kill();
    } catch {
    }
    nuxt.callHook("devtools:terminal:remove", { id });
  }
  function register() {
    nuxt.callHook("devtools:terminal:register", {
      onActionRestart: tabOptions.restartable === false ? void 0 : restart,
      onActionTerminate: tabOptions.terminatable === false ? void 0 : terminate,
      isTerminated: false,
      ...tabOptions
    });
  }
  return {
    getProcess: () => process,
    terminate,
    restart,
    clear
  };
}
function extendServerRpc(namespace, functions, nuxt = useNuxt()) {
  const ctx = _getContext(nuxt);
  if (!ctx)
    throw new Error("[Nuxt DevTools] Failed to get devtools context.");
  return ctx.extendServerRpc(namespace, functions);
}
function onDevToolsInitialized(fn, nuxt = useNuxt()) {
  nuxt.hook("devtools:initialized", fn);
}
function _getContext(nuxt = useNuxt()) {
  return nuxt?.devtools;
}

export { addCustomTab, extendServerRpc, onDevToolsInitialized, refreshCustomTabs, startSubprocess };

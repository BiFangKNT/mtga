export function setupHooksDebug(hooks) {
  const serverHooks = {};
  const now = typeof globalThis.performance === "undefined" ? () => Date.now() : () => performance.now();
  hooks.beforeEach((event) => {
    if (!serverHooks[event.name]) {
      serverHooks[event.name] = {
        name: event.name,
        start: now(),
        // @ts-expect-error private field
        listeners: hooks._hooks[event.name]?.length || 0,
        executions: []
      };
    } else {
      const hook = serverHooks[event.name];
      if (hook) {
        if (hook.duration != null)
          hook.executions.push(hook.duration);
        hook.start = now();
        hook.end = void 0;
        hook.duration = void 0;
      }
    }
  });
  hooks.afterEach((event) => {
    const hook = serverHooks[event.name];
    if (!hook)
      return;
    hook.end = now();
    hook.duration = hook.end - hook.start;
    const listeners = hooks._hooks[event.name]?.length;
    if (listeners != null)
      hook.listeners = listeners;
  });
  return serverHooks;
}

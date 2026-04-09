import { events, isEnabled } from 'vite-plugin-vue-tracer/client/listeners';
import { state } from 'vite-plugin-vue-tracer/client/overlay';

function clientScriptSetup(ctx) {
  ctx.current.events.on("entry:activated", () => {
    events.on("click", (e) => {
      ctx.rpc.call("vite:core:open-in-editor", `${e.pos[0]}:${e.pos[1]}:${e.pos[2]}`);
      state.isVisible = false;
      state.isEnabled = false;
      ctx.docks.switchEntry(null);
    });
    isEnabled.value = true;
    state.isVisible = true;
  });
  ctx.current.events.on("entry:deactivated", () => {
    isEnabled.value = false;
    state.isVisible = false;
  });
}

export { clientScriptSetup as default };

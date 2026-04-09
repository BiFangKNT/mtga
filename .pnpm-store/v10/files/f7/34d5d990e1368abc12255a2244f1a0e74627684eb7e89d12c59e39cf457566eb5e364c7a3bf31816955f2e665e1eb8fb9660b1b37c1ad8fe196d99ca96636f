import { Teleport, defineComponent, h, inject, provide, useId } from "vue";
import { useNuxtApp } from "../nuxt.js";
import paths from "#build/component-chunk";
import { buildAssetsURL } from "#internal/nuxt/paths";
export const NuxtTeleportIslandSymbol = Symbol("NuxtTeleportIslandComponent");
export default defineComponent({
  name: "NuxtTeleportIslandComponent",
  inheritAttrs: false,
  props: {
    nuxtClient: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { slots }) {
    const nuxtApp = useNuxtApp();
    const to = useId();
    if (!nuxtApp.ssrContext?.islandContext || !props.nuxtClient || inject(NuxtTeleportIslandSymbol, false)) {
      return () => slots.default?.();
    }
    provide(NuxtTeleportIslandSymbol, to);
    const islandContext = nuxtApp.ssrContext.islandContext;
    return () => {
      const slot = slots.default()[0];
      const slotType = slot.type;
      const name = slotType.__name || slotType.name;
      islandContext.components[to] = {
        chunk: import.meta.dev ? buildAssetsURL(paths[name]) : paths[name],
        props: slot.props || {}
      };
      return [h("div", {
        "style": "display: contents;",
        "data-island-uid": "",
        "data-island-component": to
      }, []), h(Teleport, { to }, slot)];
    };
  }
});

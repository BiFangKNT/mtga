import { defineComponent } from "vue";
import { devPagesDir } from "#build/nuxt.config.mjs";
export default defineComponent({
  name: "NuxtPage",
  setup(_, props) {
    if (import.meta.dev) {
      console.warn(`Create a Vue component in the \`${devPagesDir}/\` directory to enable \`<NuxtPage>\``);
    }
    return () => props.slots.default?.();
  }
});

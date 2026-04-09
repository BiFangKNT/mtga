import { createVNode, defineComponent, onErrorCaptured } from "vue";
import { injectHead } from "../composables/head.js";
import { createError } from "../composables/error.js";
import { islandComponents } from "#build/components.islands.mjs";
export default defineComponent({
  name: "IslandRenderer",
  props: {
    context: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const head = injectHead();
    head.entries.clear();
    const component = islandComponents[props.context.name];
    if (!component) {
      throw createError({
        status: 404,
        statusText: `Island component not found: ${props.context.name}`
      });
    }
    onErrorCaptured((e) => {
      console.log(e);
    });
    return () => createVNode(component || "span", { ...props.context.props, "data-island-uid": "" });
  }
});

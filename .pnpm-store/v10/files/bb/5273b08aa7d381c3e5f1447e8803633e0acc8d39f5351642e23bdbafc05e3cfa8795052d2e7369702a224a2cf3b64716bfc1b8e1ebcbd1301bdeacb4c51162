import { computed, defineComponent, h } from "vue";
import { useAnnouncer } from "../composables/announcer.js";
export default defineComponent({
  name: "NuxtAnnouncer",
  props: {
    atomic: {
      type: Boolean,
      default: true
    },
    politeness: {
      type: String,
      default: "polite"
    }
  },
  setup(props, { slots, expose }) {
    const { set, polite, assertive, message, politeness } = useAnnouncer({
      politeness: props.politeness
    });
    const role = computed(() => {
      if (politeness.value === "assertive") {
        return "alert";
      }
      if (politeness.value === "off") {
        return void 0;
      }
      return "status";
    });
    expose({
      set,
      polite,
      assertive,
      message,
      politeness
    });
    return () => h("span", {
      class: "nuxt-announcer",
      style: {
        position: "absolute"
      }
    }, h("span", {
      "role": role.value,
      "aria-live": politeness.value,
      "aria-atomic": props.atomic,
      "style": {
        "border": "0",
        "clip": "rect(0 0 0 0)",
        "clip-path": "inset(50%)",
        "height": "1px",
        "width": "1px",
        "overflow": "hidden",
        "position": "absolute",
        "white-space": "nowrap",
        "word-wrap": "normal",
        "margin": "-1px",
        "padding": "0"
      }
    }, slots.default ? slots.default({ message: message.value }) : message.value));
  }
});

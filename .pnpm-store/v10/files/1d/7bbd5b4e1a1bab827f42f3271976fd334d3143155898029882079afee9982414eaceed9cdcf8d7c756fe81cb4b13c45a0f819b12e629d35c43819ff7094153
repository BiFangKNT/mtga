import { defineComponent, getCurrentInstance, inject, onUnmounted, provide, reactive } from "vue";
import { useHead } from "#app/composables/head";
const HeadComponentCtxSymbol = Symbol("head-component");
const TagPositionProps = {
  /**
   * @deprecated Use tagPosition
   */
  body: { type: Boolean, default: void 0 },
  tagPosition: { type: String }
};
function normalizeProps(_props, key) {
  const props = Object.fromEntries(
    Object.entries(_props).filter(([_, value]) => value !== void 0)
  );
  if (typeof props.body !== "undefined") {
    props.tagPosition = props.body ? "bodyClose" : "head";
  }
  if (typeof props.renderPriority !== "undefined") {
    props.tagPriority = props.renderPriority;
  }
  return {
    ...props,
    key
  };
}
function useVNodeStringKey() {
  const vnodeKey = getCurrentInstance()?.vnode.key;
  return vnodeKey != null && typeof vnodeKey !== "symbol" ? String(vnodeKey) : void 0;
}
function useHeadComponentCtx() {
  return inject(HeadComponentCtxSymbol, createHeadComponentCtx, true);
}
function createHeadComponentCtx() {
  const prev = inject(HeadComponentCtxSymbol, null);
  if (prev) {
    return prev;
  }
  const input = reactive({});
  const entry = useHead(input);
  const ctx = { input, entry, update: () => entry.patch(input) };
  provide(HeadComponentCtxSymbol, ctx);
  return ctx;
}
const globalProps = {
  accesskey: String,
  autocapitalize: String,
  autofocus: {
    type: Boolean,
    default: void 0
  },
  class: { type: [String, Object, Array], default: void 0 },
  contenteditable: {
    type: Boolean,
    default: void 0
  },
  contextmenu: String,
  dir: String,
  draggable: {
    type: Boolean,
    default: void 0
  },
  enterkeyhint: String,
  exportparts: String,
  hidden: {
    type: Boolean,
    default: void 0
  },
  id: String,
  inputmode: String,
  is: String,
  itemid: String,
  itemprop: String,
  itemref: String,
  itemscope: String,
  itemtype: String,
  lang: String,
  nonce: String,
  part: String,
  slot: String,
  spellcheck: {
    type: Boolean,
    default: void 0
  },
  style: { type: [String, Object, Array], default: void 0 },
  tabindex: String,
  title: String,
  translate: String,
  /**
   * @deprecated Use tagPriority
   */
  renderPriority: [String, Number],
  /**
   * Unhead prop to modify the priority of the tag.
   */
  tagPriority: { type: [String, Number] }
};
export const NoScript = defineComponent({
  name: "NoScript",
  inheritAttrs: false,
  props: {
    ...globalProps,
    ...TagPositionProps,
    title: String
  },
  setup(props, { slots }) {
    const { input, update } = useHeadComponentCtx();
    input.noscript ||= [];
    const idx = input.noscript.push({}) - 1;
    onUnmounted(() => {
      input.noscript[idx] = null;
      update();
    });
    const key = useVNodeStringKey();
    return () => {
      const noscript = normalizeProps(props, key);
      const slotVnodes = slots.default?.();
      const textContent = [];
      if (slotVnodes) {
        for (const vnode of slotVnodes) {
          if (vnode.children) {
            textContent.push(vnode.children);
          }
        }
      }
      if (textContent.length > 0) {
        noscript.innerHTML = textContent.join("");
      }
      input.noscript[idx] = noscript;
      update();
      return null;
    };
  }
});
export const Link = defineComponent({
  name: "Link",
  inheritAttrs: false,
  props: {
    ...globalProps,
    ...TagPositionProps,
    as: String,
    crossorigin: String,
    disabled: Boolean,
    fetchpriority: String,
    href: String,
    hreflang: String,
    imagesizes: String,
    imagesrcset: String,
    integrity: String,
    media: String,
    prefetch: {
      type: Boolean,
      default: void 0
    },
    referrerpolicy: String,
    rel: String,
    sizes: String,
    title: String,
    type: String,
    /** @deprecated **/
    methods: String,
    /** @deprecated **/
    target: String
  },
  setup(props) {
    const { input, update } = useHeadComponentCtx();
    input.link ||= [];
    const idx = input.link.push({}) - 1;
    const key = useVNodeStringKey();
    onUnmounted(() => {
      input.link[idx] = null;
      update();
    });
    return () => {
      input.link[idx] = normalizeProps(props, key);
      update();
      return null;
    };
  }
});
export const Base = defineComponent({
  name: "Base",
  inheritAttrs: false,
  props: {
    ...globalProps,
    href: String,
    target: String
  },
  setup(props) {
    const { input, update } = useHeadComponentCtx();
    const key = useVNodeStringKey();
    onUnmounted(() => {
      input.base = null;
      update();
    });
    return () => {
      input.base = normalizeProps(props, key);
      update();
      return null;
    };
  }
});
export const Title = defineComponent({
  name: "Title",
  inheritAttrs: false,
  setup(_, { slots }) {
    const { input, update } = useHeadComponentCtx();
    onUnmounted(() => {
      input.title = null;
      update();
    });
    return () => {
      const defaultSlot = slots.default?.();
      input.title = defaultSlot?.[0]?.children ? String(defaultSlot?.[0]?.children) : void 0;
      if (import.meta.dev) {
        if (defaultSlot && (defaultSlot.length > 1 || defaultSlot[0] && typeof defaultSlot[0].children !== "string")) {
          console.error("<Title> can take only one string in its default slot.");
        }
      }
      update();
      return null;
    };
  }
});
export const Meta = defineComponent({
  name: "Meta",
  inheritAttrs: false,
  props: {
    ...globalProps,
    charset: String,
    content: String,
    httpEquiv: String,
    name: String,
    property: String
  },
  setup(props) {
    const { input, update } = useHeadComponentCtx();
    const key = useVNodeStringKey();
    input.meta ||= [];
    const idx = input.meta.push({}) - 1;
    onUnmounted(() => {
      input.meta[idx] = null;
      update();
    });
    return () => {
      const meta = { "http-equiv": props.httpEquiv, ...normalizeProps(props, key) };
      if ("httpEquiv" in meta) {
        delete meta.httpEquiv;
      }
      input.meta[idx] = meta;
      update();
      return null;
    };
  }
});
export const Style = defineComponent({
  name: "Style",
  inheritAttrs: false,
  props: {
    ...globalProps,
    ...TagPositionProps,
    type: String,
    media: String,
    nonce: String,
    title: String,
    /** @deprecated **/
    scoped: {
      type: Boolean,
      default: void 0
    }
  },
  setup(props, { slots }) {
    const { input, update } = useHeadComponentCtx();
    const key = useVNodeStringKey();
    input.style ||= [];
    const idx = input.style.push({}) - 1;
    onUnmounted(() => {
      input.style[idx] = null;
      update();
    });
    return () => {
      const style = normalizeProps(props, key);
      const textContent = slots.default?.()?.[0]?.children;
      if (textContent) {
        if (import.meta.dev && typeof textContent !== "string") {
          console.error("<Style> can only take a string in its default slot.");
        }
        input.style[idx] = style;
        style.textContent = textContent;
      }
      update();
      return null;
    };
  }
});
export const Head = defineComponent({
  name: "Head",
  inheritAttrs: false,
  setup: (_props, ctx) => {
    createHeadComponentCtx();
    return () => ctx.slots.default?.();
  }
});
export const Html = defineComponent({
  name: "Html",
  inheritAttrs: false,
  props: {
    ...globalProps,
    manifest: String,
    version: String,
    xmlns: String
  },
  setup(_props, ctx) {
    const { input, update } = useHeadComponentCtx();
    onUnmounted(() => {
      input.htmlAttrs = null;
      update();
    });
    return () => {
      input.htmlAttrs = { ..._props, ...ctx.attrs };
      update();
      return ctx.slots.default?.();
    };
  }
});
export const Body = defineComponent({
  name: "Body",
  inheritAttrs: false,
  props: globalProps,
  setup(_props, ctx) {
    const { input, update } = useHeadComponentCtx();
    onUnmounted(() => {
      input.bodyAttrs = null;
      update();
    });
    return () => {
      input.bodyAttrs = { ..._props, ...ctx.attrs };
      update();
      return ctx.slots.default?.();
    };
  }
});

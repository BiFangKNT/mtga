import { defineComponent, ref, onBeforeUnmount, watchEffect } from 'vue';
import { u as useHead } from './shared/vue.Cr7xSEtD.mjs';
import 'unhead/plugins';
import 'unhead/utils';
import './shared/vue.N9zWjxoK.mjs';

function addVNodeToHeadObj(node, obj) {
  const nodeType = node.type;
  const type = nodeType === "html" ? "htmlAttrs" : nodeType === "body" ? "bodyAttrs" : nodeType;
  if (typeof type !== "string" || !(type in obj))
    return;
  const props = node.props || {};
  if (node.children) {
    const childrenAttr = "children";
    props.children = Array.isArray(node.children) ? node.children[0][childrenAttr] : node[childrenAttr];
  }
  if (Array.isArray(obj[type]))
    obj[type].push(props);
  else if (type === "title")
    obj.title = props.children;
  else
    obj[type] = props;
}
function vnodesToHeadObj(nodes) {
  const obj = {
    title: void 0,
    htmlAttrs: void 0,
    bodyAttrs: void 0,
    base: void 0,
    meta: [],
    link: [],
    style: [],
    script: [],
    noscript: []
  };
  for (const node of nodes) {
    if (typeof node.type === "symbol" && Array.isArray(node.children)) {
      for (const childNode of node.children)
        addVNodeToHeadObj(childNode, obj);
    } else {
      addVNodeToHeadObj(node, obj);
    }
  }
  return obj;
}
const Head = /* @__PURE__ */ defineComponent({
  name: "Head",
  setup(_, { slots }) {
    const obj = ref({});
    const entry = useHead(obj);
    onBeforeUnmount(() => {
      entry.dispose();
    });
    return () => {
      watchEffect(() => {
        if (!slots.default)
          return;
        entry.patch(vnodesToHeadObj(slots.default()));
      });
      return null;
    };
  }
});

export { Head };

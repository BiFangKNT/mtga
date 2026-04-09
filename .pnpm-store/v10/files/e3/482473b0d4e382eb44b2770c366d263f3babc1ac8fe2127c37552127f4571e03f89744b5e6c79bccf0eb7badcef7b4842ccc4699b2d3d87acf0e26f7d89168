import { getCurrentInstance } from 'vue';
import { u as useHead } from './vue.Cr7xSEtD.mjs';

const VueHeadMixin = {
  created() {
    let source = false;
    const instance = getCurrentInstance();
    if (!instance)
      return;
    const options = instance.type;
    if (!options || !("head" in options))
      return;
    source = typeof options.head === "function" ? () => options.head.call(instance.proxy) : options.head;
    source && useHead(source);
  }
};

export { VueHeadMixin as V };

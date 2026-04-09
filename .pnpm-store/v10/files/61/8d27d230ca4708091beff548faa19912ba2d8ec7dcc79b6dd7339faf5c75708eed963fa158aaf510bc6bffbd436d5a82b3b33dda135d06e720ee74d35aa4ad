import { createHead as createHead$1, createDebouncedFn, renderDOMHead } from 'unhead/client';
export { renderDOMHead } from 'unhead/client';
import { v as vueInstall } from './shared/vue.Cr7xSEtD.mjs';
export { V as VueHeadMixin } from './shared/vue.BM998iwd.mjs';
import 'unhead/plugins';
import 'unhead/utils';
import 'vue';
import './shared/vue.N9zWjxoK.mjs';

// @__NO_SIDE_EFFECTS__
function createHead(options = {}) {
  const head = createHead$1({
    domOptions: {
      render: createDebouncedFn(() => renderDOMHead(head), (fn) => setTimeout(fn, 0))
    },
    ...options
  });
  head.install = vueInstall(head);
  return head;
}

export { createHead };

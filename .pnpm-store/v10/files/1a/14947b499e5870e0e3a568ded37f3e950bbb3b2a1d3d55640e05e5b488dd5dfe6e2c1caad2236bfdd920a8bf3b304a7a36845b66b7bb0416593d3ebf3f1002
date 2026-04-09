import { a as createUnhead } from './shared/unhead.Ct24BOby.mjs';
import { D as DeprecationsPlugin, P as PromisesPlugin, T as TemplateParamsPlugin, A as AliasSortingPlugin } from './shared/unhead.Chhckluj.mjs';
export { u as useHead, a as useHeadSafe, b as useSeoMeta, c as useServerHead, d as useServerHeadSafe, e as useServerSeoMeta } from './shared/unhead._ybhDo-G.mjs';
export { u as useScript } from './shared/unhead.BnoAbrHA.mjs';
import 'hookable';
import './shared/unhead.B5FWS6X0.mjs';
import './shared/unhead.yem5I2v_.mjs';
import './shared/unhead.CbpEuj3y.mjs';
import './shared/unhead.0eF0fa-Y.mjs';
import './shared/unhead.DQc16pHI.mjs';
import './shared/unhead.BYvz9V1x.mjs';

const activeHead = { value: null };
function getActiveHead() {
  return activeHead?.value;
}
function createServerHead(options = {}) {
  return activeHead.value = createUnhead({
    disableCapoSorting: true,
    ...options,
    // @ts-expect-error untyped
    document: false,
    plugins: [
      ...options.plugins || [],
      DeprecationsPlugin,
      PromisesPlugin,
      TemplateParamsPlugin,
      AliasSortingPlugin
    ]
  });
}
function createHead(options = {}) {
  return activeHead.value = createUnhead({
    disableCapoSorting: true,
    ...options,
    plugins: [
      ...options.plugins || [],
      DeprecationsPlugin,
      PromisesPlugin,
      TemplateParamsPlugin,
      AliasSortingPlugin
    ]
  });
}
const createHeadCore = createUnhead;

export { activeHead, createHead, createHeadCore, createServerHead, createUnhead, getActiveHead };

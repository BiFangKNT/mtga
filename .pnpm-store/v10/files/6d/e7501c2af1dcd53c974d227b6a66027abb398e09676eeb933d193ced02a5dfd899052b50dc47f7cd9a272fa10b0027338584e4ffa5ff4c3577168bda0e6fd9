import { Transition, createStaticVNode, h } from "vue";
import { defu } from "defu";
import { isString, isPromise, isArray, isObject } from "@vue/shared";
import { START_LOCATION } from "#build/pages";
export const _wrapInTransition = (props, children) => {
  return { default: () => import.meta.client && props ? h(Transition, props === true ? {} : props, children) : children.default?.() };
};
const ROUTE_KEY_PARENTHESES_RE = /(:\w+)\([^)]+\)/g;
const ROUTE_KEY_SYMBOLS_RE = /(:\w+)[?+*]/g;
const ROUTE_KEY_NORMAL_RE = /:\w+/g;
function generateRouteKey(route) {
  const source = route?.meta.key ?? route.path.replace(ROUTE_KEY_PARENTHESES_RE, "$1").replace(ROUTE_KEY_SYMBOLS_RE, "$1").replace(ROUTE_KEY_NORMAL_RE, (r) => route.params[r.slice(1)]?.toString() || "");
  return typeof source === "function" ? source(route) : source;
}
export function isChangingPage(to, from) {
  if (to === from || from === START_LOCATION) {
    return false;
  }
  if (generateRouteKey(to) !== generateRouteKey(from)) {
    return true;
  }
  const areComponentsSame = to.matched.every(
    (comp, index) => comp.components && comp.components.default === from.matched[index]?.components?.default
  );
  if (areComponentsSame) {
    return false;
  }
  return true;
}
export function createBuffer() {
  let appendable = false;
  const buffer = [];
  return {
    getBuffer() {
      return buffer;
    },
    push(item) {
      const isStringItem = isString(item);
      if (appendable && isStringItem) {
        buffer[buffer.length - 1] += item;
      } else {
        buffer.push(item);
      }
      appendable = isStringItem;
      if (isPromise(item) || isArray(item) && item.hasAsync) {
        buffer.hasAsync = true;
      }
    }
  };
}
export function vforToArray(source) {
  if (isArray(source)) {
    return source;
  } else if (isString(source)) {
    return source.split("");
  } else if (typeof source === "number") {
    if (import.meta.dev && !Number.isInteger(source)) {
      console.warn(`The v-for range expect an integer value but got ${source}.`);
    }
    const array = [];
    for (let i = 0; i < source; i++) {
      array[i] = i;
    }
    return array;
  } else if (isObject(source)) {
    if (source[Symbol.iterator]) {
      return Array.from(
        source,
        (item) => item
      );
    } else {
      const keys = Object.keys(source);
      const array = new Array(keys.length);
      for (let i = 0, l = keys.length; i < l; i++) {
        const key = keys[i];
        array[i] = source[key];
      }
      return array;
    }
  }
  return [];
}
export function getFragmentHTML(element, withoutSlots = false) {
  if (element) {
    if (element.nodeName === "#comment" && element.nodeValue === "[") {
      return getFragmentChildren(element, [], withoutSlots);
    }
    if (withoutSlots) {
      const clone = element.cloneNode(true);
      clone.querySelectorAll("[data-island-slot]").forEach((n) => {
        n.innerHTML = "";
      });
      return [clone.outerHTML];
    }
    return [element.outerHTML];
  }
}
function getFragmentChildren(element, blocks = [], withoutSlots = false) {
  if (element && element.nodeName) {
    if (isEndFragment(element)) {
      return blocks;
    } else if (!isStartFragment(element)) {
      const clone = element.cloneNode(true);
      if (withoutSlots) {
        clone.querySelectorAll?.("[data-island-slot]").forEach((n) => {
          n.innerHTML = "";
        });
      }
      blocks.push(clone.outerHTML);
    }
    getFragmentChildren(element.nextSibling, blocks, withoutSlots);
  }
  return blocks;
}
export function elToStaticVNode(el, staticNodeFallback) {
  const fragment = el ? getFragmentHTML(el) : staticNodeFallback ? [staticNodeFallback] : void 0;
  if (fragment) {
    return createStaticVNode(fragment.join(""), fragment.length);
  }
  return h("div");
}
export function isStartFragment(element) {
  return element.nodeName === "#comment" && element.nodeValue === "[";
}
export function isEndFragment(element) {
  return element.nodeName === "#comment" && element.nodeValue === "]";
}
export function toArray(value) {
  return Array.isArray(value) ? value : [value];
}
export function _mergeTransitionProps(routeProps) {
  const _props = [];
  for (const prop of routeProps) {
    if (!prop) {
      continue;
    }
    _props.push({
      ...prop,
      onAfterLeave: prop.onAfterLeave ? toArray(prop.onAfterLeave) : void 0,
      onBeforeLeave: prop.onBeforeLeave ? toArray(prop.onBeforeLeave) : void 0
    });
  }
  return defu(..._props);
}

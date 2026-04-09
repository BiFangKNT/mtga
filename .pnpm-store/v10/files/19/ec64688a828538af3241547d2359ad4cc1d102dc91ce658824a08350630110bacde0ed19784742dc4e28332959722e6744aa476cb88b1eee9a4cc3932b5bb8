export { r as resolveScriptKey, u as useScript } from './shared/unhead.BnoAbrHA.mjs';
import './shared/unhead.yem5I2v_.mjs';

function createSpyProxy(target, onApply) {
  const stack = [];
  let stackIdx = -1;
  const handler = (reuseStack = false) => ({
    get(_, prop, receiver) {
      if (!reuseStack) {
        stackIdx++;
        stack[stackIdx] = [];
      }
      const v = Reflect.get(_, prop, receiver);
      if (typeof v === "object" || typeof v === "function") {
        stack[stackIdx].push({ type: "get", key: prop });
        return new Proxy(v, handler(true));
      }
      stack[stackIdx].push({ type: "get", key: prop, value: v });
      return v;
    },
    apply(_, __, args) {
      stack[stackIdx].push({ type: "apply", key: "", args });
      onApply(stack);
      return Reflect.apply(_, __, args);
    }
  });
  return new Proxy(target, handler());
}

export { createSpyProxy };

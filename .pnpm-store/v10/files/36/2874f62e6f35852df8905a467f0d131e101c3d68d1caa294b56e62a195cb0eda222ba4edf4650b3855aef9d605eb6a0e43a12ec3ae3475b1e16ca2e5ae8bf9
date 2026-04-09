import { S as SafeInputPlugin, F as FlatMetaPlugin } from './unhead.0eF0fa-Y.mjs';

function useHead(unhead, input, options = {}) {
  return unhead.push(input || {}, options);
}
function useHeadSafe(unhead, input = {}, options = {}) {
  unhead.use(SafeInputPlugin);
  return useHead(unhead, input, Object.assign(options, { _safe: true }));
}
function useSeoMeta(unhead, input = {}, options) {
  unhead.use(FlatMetaPlugin);
  function normalize(input2) {
    if (input2._flatMeta) {
      return input2;
    }
    const { title, titleTemplate, ...meta } = input2 || {};
    return {
      title,
      titleTemplate,
      _flatMeta: meta
    };
  }
  const entry = unhead.push(normalize(input), options);
  const corePatch = entry.patch;
  if (!entry.__patched) {
    entry.patch = (input2) => corePatch(normalize(input2));
    entry.__patched = true;
  }
  return entry;
}
function useServerHead(unhead, input = {}, options = {}) {
  options.mode = "server";
  return unhead.push(input, options);
}
function useServerHeadSafe(unhead, input = {}, options = {}) {
  options.mode = "server";
  return useHeadSafe(unhead, input, { ...options, mode: "server" });
}
function useServerSeoMeta(unhead, input = {}, options) {
  options.mode = "server";
  return useSeoMeta(unhead, input, { ...options, mode: "server" });
}

export { useHeadSafe as a, useSeoMeta as b, useServerHead as c, useServerHeadSafe as d, useServerSeoMeta as e, useHead as u };

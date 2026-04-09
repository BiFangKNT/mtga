function mergeProcessors(processors) {
  const cache = /* @__PURE__ */ new Map();
  return {
    meta: {
      name: `merged-processor:${processors.map((processor) => processor.meta?.name || "unknown").join("+")}`
    },
    supportsAutofix: true,
    preprocess(text, filename) {
      const counts = [];
      cache.set(filename, counts);
      return processors.flatMap((processor) => {
        const result = processor.preprocess?.(text, filename) || [];
        counts.push(result.length);
        return result;
      });
    },
    postprocess(messages, filename) {
      const counts = cache.get(filename);
      cache.delete(filename);
      let index = 0;
      return processors.flatMap((processor, idx) => {
        const msgs = messages.slice(index, index + counts[idx]);
        index += counts[idx];
        return processor.postprocess?.(msgs, filename) || [];
      });
    }
  };
}
const processorPassThrough = {
  meta: {
    name: "pass-through"
  },
  preprocess(text) {
    return [text];
  },
  postprocess(messages) {
    return messages[0];
  }
};

export { mergeProcessors, processorPassThrough };

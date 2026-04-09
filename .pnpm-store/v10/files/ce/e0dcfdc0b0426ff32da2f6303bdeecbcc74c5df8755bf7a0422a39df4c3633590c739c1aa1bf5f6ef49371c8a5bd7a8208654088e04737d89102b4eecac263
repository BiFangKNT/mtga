async function runParallel(inputs, cb, opts) {
  const errors = [];
  const tasks = /* @__PURE__ */ new Set();
  function queueNext() {
    const route = inputs.values().next().value;
    if (!route) {
      return;
    }
    inputs.delete(route);
    const task = (opts.interval ? new Promise((resolve) => setTimeout(resolve, opts.interval)) : Promise.resolve()).then(() => cb(route)).catch((error) => {
      console.error(error);
      errors.push(error);
    });
    tasks.add(task);
    return task.then(() => {
      tasks.delete(task);
      if (inputs.size > 0) {
        return refillQueue();
      }
    });
  }
  function refillQueue() {
    const workers = Math.min(opts.concurrency - tasks.size, inputs.size);
    return Promise.all(Array.from({ length: workers }, () => queueNext()));
  }
  await refillQueue();
  return { errors };
}

export { runParallel as r };

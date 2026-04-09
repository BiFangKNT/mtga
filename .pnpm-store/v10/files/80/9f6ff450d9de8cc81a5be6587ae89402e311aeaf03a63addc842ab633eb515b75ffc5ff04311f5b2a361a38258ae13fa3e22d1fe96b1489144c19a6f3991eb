import { isMainThread as _isMainThread, threadId } from "node:worker_threads";
const isInVitestEntryThread = threadId === 0 && process.env.VITEST;
const isMainThread = _isMainThread || isInVitestEntryThread;
export {
  isInVitestEntryThread,
  isMainThread
};
//# sourceMappingURL=utils.js.map
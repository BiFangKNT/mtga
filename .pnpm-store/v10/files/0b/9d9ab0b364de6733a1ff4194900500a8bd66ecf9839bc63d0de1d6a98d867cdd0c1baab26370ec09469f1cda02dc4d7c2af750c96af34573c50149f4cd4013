// runner.js
import { resolve } from "node:path";
import { createSyncFn } from "synckit";
import { getWorkerOptions } from "../async-utils/worker.js";
export function createGetCustomComponentClasses() {
    const workerPath = getWorkerPath();
    const workerOptions = getWorkerOptions();
    return createSyncFn(workerPath, workerOptions);
}
function getWorkerPath() {
    return resolve(getCurrentDirectory(), "./custom-component-classes.async.worker.js");
}
function getCurrentDirectory() {
    // eslint-disable-next-line eslint-plugin-typescript/prefer-ts-expect-error
    // @ts-ignore - `import.meta` doesn't exist in CommonJS -> will be transformed in build step
    return import.meta.dirname;
}
//# sourceMappingURL=custom-component-classes.js.map
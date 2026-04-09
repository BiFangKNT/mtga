import { resolve } from "node:path";
import { createSyncFn } from "synckit";
import { getTailwindcssVersion } from "../async-utils/tailwindcss.js";
import { getWorkerOptions } from "../async-utils/worker.js";
export function createGetDissectedClasses() {
    const workerPath = getWorkerPath();
    const workerOptions = getWorkerOptions();
    return createSyncFn(workerPath, workerOptions);
}
function getWorkerPath() {
    const { major } = getTailwindcssVersion();
    return resolve(getCurrentDirectory(), `./dissect-classes.async.worker.v${major}.js`);
}
function getCurrentDirectory() {
    // eslint-disable-next-line eslint-plugin-typescript/prefer-ts-expect-error
    // @ts-ignore - `import.meta` doesn't exist in CommonJS -> will be transformed in build step
    return import.meta.dirname;
}
//# sourceMappingURL=dissect-classes.js.map
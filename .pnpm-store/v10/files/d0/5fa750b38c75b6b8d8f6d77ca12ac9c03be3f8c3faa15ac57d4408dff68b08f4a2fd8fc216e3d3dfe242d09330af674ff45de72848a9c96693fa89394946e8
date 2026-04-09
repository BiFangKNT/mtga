"use strict";
// runner.js
Object.defineProperty(exports, "__esModule", { value: true });
exports.createGetCustomComponentClasses = createGetCustomComponentClasses;
const node_path_1 = require("node:path");
const synckit_1 = require("synckit");
const worker_js_1 = require("../async-utils/worker.js");
function createGetCustomComponentClasses() {
    const workerPath = getWorkerPath();
    const workerOptions = (0, worker_js_1.getWorkerOptions)();
    return (0, synckit_1.createSyncFn)(workerPath, workerOptions);
}
function getWorkerPath() {
    return (0, node_path_1.resolve)(getCurrentDirectory(), "./custom-component-classes.async.worker.js");
}
function getCurrentDirectory() {
    // eslint-disable-next-line eslint-plugin-typescript/prefer-ts-expect-error
    // @ts-ignore - `import.meta` doesn't exist in CommonJS -> will be transformed in build step
    return __dirname;
}
//# sourceMappingURL=custom-component-classes.js.map
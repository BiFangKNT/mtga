"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createGetPrefix = createGetPrefix;
const node_path_1 = require("node:path");
const synckit_1 = require("synckit");
const tailwindcss_js_1 = require("../async-utils/tailwindcss.js");
const worker_js_1 = require("../async-utils/worker.js");
function createGetPrefix() {
    const workerPath = getWorkerPath();
    const workerOptions = (0, worker_js_1.getWorkerOptions)();
    return (0, synckit_1.createSyncFn)(workerPath, workerOptions);
}
function getWorkerPath() {
    const { major } = (0, tailwindcss_js_1.getTailwindcssVersion)();
    return (0, node_path_1.resolve)(getCurrentDirectory(), `./prefix.async.worker.v${major}.js`);
}
function getCurrentDirectory() {
    // eslint-disable-next-line eslint-plugin-typescript/prefer-ts-expect-error
    // @ts-ignore - `import.meta` doesn't exist in CommonJS -> will be transformed in build step
    return __dirname;
}
//# sourceMappingURL=prefix.js.map
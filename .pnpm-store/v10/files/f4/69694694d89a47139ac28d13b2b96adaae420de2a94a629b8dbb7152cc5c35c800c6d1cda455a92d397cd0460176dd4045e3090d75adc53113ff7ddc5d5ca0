"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getWorkerOptions = getWorkerOptions;
const node_process_1 = require("node:process");
const synckit_1 = require("synckit");
function getWorkerOptions() {
    if (node_process_1.env.NODE_ENV === "test") {
        return {
            tsRunner: synckit_1.TsRunner.TsNode
        };
    }
}
//# sourceMappingURL=worker.js.map
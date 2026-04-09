"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getTSConfigPath = void 0;
const node_path_1 = require("node:path");
const cache_js_1 = require("./cache.js");
const fs_js_1 = require("./fs.js");
const getTSConfigPath = ({ configPath, cwd }) => (0, cache_js_1.withCache)("tsconfig-path", configPath, () => {
    const potentialPaths = [
        ...configPath ? [configPath] : [],
        "tsconfig.json",
        "jsconfig.json"
    ];
    const foundConfigPath = (0, fs_js_1.findFileRecursive)(cwd, potentialPaths);
    const warning = getConfigPathWarning(configPath, foundConfigPath);
    return {
        path: foundConfigPath,
        warnings: [warning]
    };
});
exports.getTSConfigPath = getTSConfigPath;
function getConfigPathWarning(configPath, foundConfigPath) {
    if (!configPath) {
        return;
    }
    if (foundConfigPath && (0, node_path_1.resolve)(configPath) === (0, node_path_1.resolve)(foundConfigPath)) {
        return;
    }
    return {
        option: "tsconfig",
        title: `No tsconfig found at \`${configPath}\``
    };
}
//# sourceMappingURL=tsconfig.js.map
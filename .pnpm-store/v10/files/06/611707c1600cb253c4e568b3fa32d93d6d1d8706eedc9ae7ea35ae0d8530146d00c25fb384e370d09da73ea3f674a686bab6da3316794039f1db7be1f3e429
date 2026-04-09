"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.isTailwindcssInstalled = isTailwindcssInstalled;
exports.isSupportedVersion = isSupportedVersion;
exports.isTailwindcssVersion3 = isTailwindcssVersion3;
exports.isTailwindcssVersion4 = isTailwindcssVersion4;
exports.getTailwindcssVersion = getTailwindcssVersion;
const node_fs_1 = require("node:fs");
const node_process_1 = require("node:process");
const cache_js_1 = require("./cache.js");
const resolvers_js_1 = require("./resolvers.js");
function isTailwindcssInstalled() {
    try {
        return (0, node_fs_1.existsSync)((0, resolvers_js_1.resolveJson)("tailwindcss/package.json", (0, node_process_1.cwd)()));
    }
    catch {
        return false;
    }
}
function isSupportedVersion(version) {
    return version === 3 /* TailwindcssVersion.V3 */ || version === 4 /* TailwindcssVersion.V4 */;
}
function isTailwindcssVersion3(version) {
    return version === 3 /* TailwindcssVersion.V3 */;
}
function isTailwindcssVersion4(version) {
    return version === 4 /* TailwindcssVersion.V4 */;
}
function getTailwindcssVersion() {
    const packageJsonPath = (0, resolvers_js_1.resolveJson)("tailwindcss/package.json", (0, node_process_1.cwd)());
    return (0, cache_js_1.withCache)("version", packageJsonPath, () => {
        try {
            const packageJson = JSON.parse((0, node_fs_1.readFileSync)(packageJsonPath, "utf-8"));
            return parseSemanticVersion(packageJson.version);
        }
        catch {
            throw new Error("Error reading Tailwind CSS package.json");
        }
    });
}
function parseSemanticVersion(version) {
    const [major, minor, patchString] = version.split(".");
    const [patch, identifier] = patchString.split("-");
    return { identifier, major: +major, minor: +minor, patch: +patch };
}
//# sourceMappingURL=tailwindcss.js.map
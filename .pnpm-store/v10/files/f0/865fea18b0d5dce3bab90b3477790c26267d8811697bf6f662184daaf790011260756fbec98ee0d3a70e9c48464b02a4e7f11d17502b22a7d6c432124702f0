"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.resolveJs = resolveJs;
exports.resolveCss = resolveCss;
exports.resolveJson = resolveJson;
const node_fs_1 = __importDefault(require("node:fs"));
const enhanced_resolve_1 = __importDefault(require("enhanced-resolve"));
const tsconfig_paths_webpack_plugin_1 = require("tsconfig-paths-webpack-plugin");
const cache_js_1 = require("../async-utils/cache.js");
const fileSystem = new enhanced_resolve_1.default.CachedInputFileSystem(node_fs_1.default, 30000);
const getESMResolver = (ctx) => (0, cache_js_1.withCache)("esm-resolver", ctx?.tsconfigPath, () => enhanced_resolve_1.default.ResolverFactory.createResolver({
    conditionNames: ["node", "import"],
    extensions: [".mjs", ".js"],
    fileSystem,
    mainFields: ["module"],
    plugins: ctx?.tsconfigPath ? [new tsconfig_paths_webpack_plugin_1.TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["module"] })] : [],
    useSyncFileSystemCalls: true
}));
const getCJSResolver = (ctx) => (0, cache_js_1.withCache)("cjs-resolver", ctx?.tsconfigPath, () => enhanced_resolve_1.default.ResolverFactory.createResolver({
    conditionNames: ["node", "require"],
    extensions: [".js", ".cjs"],
    fileSystem,
    mainFields: ["main"],
    plugins: ctx?.tsconfigPath ? [new tsconfig_paths_webpack_plugin_1.TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["main"] })] : [],
    useSyncFileSystemCalls: true
}));
const getCSSResolver = (ctx) => (0, cache_js_1.withCache)("css-resolver", ctx?.tsconfigPath, () => enhanced_resolve_1.default.ResolverFactory.createResolver({
    conditionNames: ["style"],
    extensions: [".css"],
    fileSystem,
    mainFields: ["style"],
    plugins: ctx?.tsconfigPath ? [new tsconfig_paths_webpack_plugin_1.TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["style"] })] : [],
    useSyncFileSystemCalls: true
}));
const jsonResolver = enhanced_resolve_1.default.ResolverFactory.createResolver({
    conditionNames: ["json"],
    extensions: [".json"],
    fileSystem,
    useSyncFileSystemCalls: true
});
function resolveJs(ctxOrPath, pathOrCwd, cwdOrUndefined) {
    const ctx = typeof ctxOrPath === "object" ? ctxOrPath : undefined;
    const path = typeof ctxOrPath === "string" ? ctxOrPath : pathOrCwd;
    const cwd = (typeof ctxOrPath === "object" ? cwdOrUndefined : pathOrCwd);
    try {
        return getESMResolver(ctx).resolveSync({}, cwd, path) || path;
    }
    catch {
        return getCJSResolver(ctx).resolveSync({}, cwd, path) || path;
    }
}
function resolveCss(ctxOrPath, pathOrCwd, cwdOrUndefined) {
    const ctx = typeof ctxOrPath === "object" ? ctxOrPath : undefined;
    const path = typeof ctxOrPath === "string" ? ctxOrPath : pathOrCwd;
    const cwd = (typeof ctxOrPath === "object" ? cwdOrUndefined : pathOrCwd);
    try {
        return getCSSResolver(ctx).resolveSync({}, cwd, path) || path;
    }
    catch {
        return path;
    }
}
function resolveJson(path, cwd) {
    try {
        return jsonResolver.resolveSync({}, cwd, path) || path;
    }
    catch {
        return path;
    }
}
//# sourceMappingURL=resolvers.js.map
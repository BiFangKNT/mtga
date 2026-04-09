import fs from "node:fs";
import enhancedResolve from "enhanced-resolve";
import { TsconfigPathsPlugin } from "tsconfig-paths-webpack-plugin";
import { withCache } from "../async-utils/cache.js";
const fileSystem = new enhancedResolve.CachedInputFileSystem(fs, 30000);
const getESMResolver = (ctx) => withCache("esm-resolver", ctx?.tsconfigPath, () => enhancedResolve.ResolverFactory.createResolver({
    conditionNames: ["node", "import"],
    extensions: [".mjs", ".js"],
    fileSystem,
    mainFields: ["module"],
    plugins: ctx?.tsconfigPath ? [new TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["module"] })] : [],
    useSyncFileSystemCalls: true
}));
const getCJSResolver = (ctx) => withCache("cjs-resolver", ctx?.tsconfigPath, () => enhancedResolve.ResolverFactory.createResolver({
    conditionNames: ["node", "require"],
    extensions: [".js", ".cjs"],
    fileSystem,
    mainFields: ["main"],
    plugins: ctx?.tsconfigPath ? [new TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["main"] })] : [],
    useSyncFileSystemCalls: true
}));
const getCSSResolver = (ctx) => withCache("css-resolver", ctx?.tsconfigPath, () => enhancedResolve.ResolverFactory.createResolver({
    conditionNames: ["style"],
    extensions: [".css"],
    fileSystem,
    mainFields: ["style"],
    plugins: ctx?.tsconfigPath ? [new TsconfigPathsPlugin({ configFile: ctx.tsconfigPath, mainFields: ["style"] })] : [],
    useSyncFileSystemCalls: true
}));
const jsonResolver = enhancedResolve.ResolverFactory.createResolver({
    conditionNames: ["json"],
    extensions: [".json"],
    fileSystem,
    useSyncFileSystemCalls: true
});
export function resolveJs(ctxOrPath, pathOrCwd, cwdOrUndefined) {
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
export function resolveCss(ctxOrPath, pathOrCwd, cwdOrUndefined) {
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
export function resolveJson(path, cwd) {
    try {
        return jsonResolver.resolveSync({}, cwd, path) || path;
    }
    catch {
        return path;
    }
}
//# sourceMappingURL=resolvers.js.map
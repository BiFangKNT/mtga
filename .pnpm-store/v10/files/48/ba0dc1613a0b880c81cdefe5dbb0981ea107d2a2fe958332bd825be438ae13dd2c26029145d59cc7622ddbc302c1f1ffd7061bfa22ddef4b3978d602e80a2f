"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findFileRecursive = findFileRecursive;
exports.getModifiedDate = getModifiedDate;
const node_fs_1 = require("node:fs");
const node_path_1 = require("node:path");
function findFileRecursive(cwd, paths) {
    const resolvedPaths = paths.map(p => (0, node_path_1.resolve)(cwd, p));
    for (let resolvedPath = resolvedPaths.shift(); resolvedPath !== undefined; resolvedPath = resolvedPaths.shift()) {
        if ((0, node_fs_1.existsSync)(resolvedPath)) {
            const stat = (0, node_fs_1.statSync)(resolvedPath);
            if (!stat.isFile()) {
                continue;
            }
            return resolvedPath;
        }
        const fileName = (0, node_path_1.basename)(resolvedPath);
        const directory = (0, node_path_1.dirname)(resolvedPath);
        const parentDirectory = (0, node_path_1.resolve)(directory, "..");
        const parentPath = (0, node_path_1.resolve)(parentDirectory, fileName);
        if (parentDirectory === directory || directory === cwd) {
            continue;
        }
        resolvedPaths.push(parentPath);
    }
}
function getModifiedDate(filePath) {
    try {
        const stats = (0, node_fs_1.statSync)(filePath);
        return stats.mtime;
    }
    catch {
        return new Date();
    }
}
//# sourceMappingURL=fs.js.map
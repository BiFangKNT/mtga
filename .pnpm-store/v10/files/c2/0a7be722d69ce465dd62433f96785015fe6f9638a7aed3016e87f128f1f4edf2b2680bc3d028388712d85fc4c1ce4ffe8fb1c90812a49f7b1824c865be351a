import { existsSync, statSync } from "node:fs";
import { basename, dirname, resolve } from "node:path";
export function findFileRecursive(cwd, paths) {
    const resolvedPaths = paths.map(p => resolve(cwd, p));
    for (let resolvedPath = resolvedPaths.shift(); resolvedPath !== undefined; resolvedPath = resolvedPaths.shift()) {
        if (existsSync(resolvedPath)) {
            const stat = statSync(resolvedPath);
            if (!stat.isFile()) {
                continue;
            }
            return resolvedPath;
        }
        const fileName = basename(resolvedPath);
        const directory = dirname(resolvedPath);
        const parentDirectory = resolve(directory, "..");
        const parentPath = resolve(parentDirectory, fileName);
        if (parentDirectory === directory || directory === cwd) {
            continue;
        }
        resolvedPaths.push(parentPath);
    }
}
export function getModifiedDate(filePath) {
    try {
        const stats = statSync(filePath);
        return stats.mtime;
    }
    catch {
        return new Date();
    }
}
//# sourceMappingURL=fs.js.map
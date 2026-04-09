import { readFile } from "node:fs/promises";
import { dirname } from "node:path";
import { fork } from "@eslint/css-tree";
import { tailwind4 } from "tailwind-csstree";
import { withCache } from "../async-utils/cache.js";
import { resolveCss } from "../async-utils/resolvers.js";
const { findAll, generate, parse, walk } = fork(tailwind4);
export async function getCustomComponentClasses(ctx) {
    const resolvedPath = resolveCss(ctx, ctx.tailwindConfigPath);
    if (!resolvedPath) {
        return [];
    }
    const files = await parseCssFilesDeep(ctx, resolvedPath);
    return getCustomComponentUtilities(files, resolvedPath);
}
async function parseCssFilesDeep(ctx, resolvedPath) {
    const cssFiles = {};
    const cssFile = await parseCssFile(ctx, resolvedPath);
    if (!cssFile) {
        return cssFiles;
    }
    cssFiles[resolvedPath] = cssFile;
    for (const { path } of cssFile.imports) {
        const importedFiles = await parseCssFilesDeep(ctx, path);
        for (const importedFile in importedFiles) {
            cssFiles[importedFile] = importedFiles[importedFile];
        }
    }
    return cssFiles;
}
const parseCssFile = async (ctx, resolvedPath) => withCache("css-file", resolvedPath, async () => {
    try {
        const content = await readFile(resolvedPath, "utf-8");
        const ast = parse(content);
        const importNodes = findAll(ast, node => node.type === "Atrule" &&
            node.name === "import" &&
            node.prelude?.type === "AtrulePrelude");
        const imports = importNodes.reduce((imports, importNode) => {
            if (importNode.type !== "Atrule" || !importNode.prelude) {
                return imports;
            }
            const prelude = generate(importNode.prelude);
            const importStatement = prelude.match(/["'](?<importPath>[^"']+)["'](?<rest>.*)/);
            if (!importStatement) {
                return imports;
            }
            const { importPath, rest } = importStatement.groups || {};
            const layerMatch = rest?.match(/layer(?:\((?<layerName>[^)]+)\))?/);
            const layer = layerMatch ? layerMatch.groups?.layerName || "anonymous" : undefined;
            const cwd = dirname(resolvedPath);
            const resolvedImportPath = resolveCss(ctx, importPath, cwd);
            if (resolvedImportPath) {
                imports.push({ layer, path: resolvedImportPath });
            }
            return imports;
        }, []);
        return {
            ast,
            imports
        };
    }
    catch { }
});
function getCustomComponentUtilities(files, filePath, currentLayer = []) {
    const classes = new Set();
    const file = files[filePath];
    if (!file) {
        return [];
    }
    for (const { layer, path } of file.imports) {
        const nextLayer = [...currentLayer];
        if (layer) {
            nextLayer.push(layer);
        }
        const importedClasses = getCustomComponentUtilities(files, path, nextLayer);
        for (const importedClass of importedClasses) {
            classes.add(importedClass);
        }
    }
    const localLayers = [];
    walk(file.ast, {
        enter: (node) => {
            if (node.type === "Atrule" && node.name === "layer" && node.prelude?.type === "AtrulePrelude" && node.block) {
                const layerName = generate(node.prelude).trim();
                localLayers.push(layerName);
            }
            if (node.type === "ClassSelector") {
                if ([...currentLayer, ...localLayers][0] === "components") {
                    classes.add(node.name);
                }
            }
        },
        leave: (node) => {
            if (node.type === "Atrule" && node.name === "layer" && node.block) {
                localLayers.pop();
            }
        }
    });
    return Array.from(classes);
}
//# sourceMappingURL=custom-component-classes.async.v4.js.map
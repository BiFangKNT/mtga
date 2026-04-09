import { isModuleTree } from "../shared/types.js";
const addToPath = (moduleId, tree, modulePath, node) => {
    if (modulePath.length === 0) {
        throw new Error(`Error adding node to path ${moduleId}`);
    }
    const [head, ...rest] = modulePath;
    if (rest.length === 0) {
        tree.children.push({ ...node, name: head });
        return;
    }
    else {
        let newTree = tree.children.find((folder) => folder.name === head && isModuleTree(folder));
        if (!newTree) {
            newTree = { name: head, children: [] };
            tree.children.push(newTree);
        }
        addToPath(moduleId, newTree, rest, node);
        return;
    }
};
// TODO try to make it without recursion, but still typesafe
const mergeSingleChildTrees = (tree) => {
    if (tree.children.length === 1) {
        const child = tree.children[0];
        const name = `${tree.name}/${child.name}`;
        if (isModuleTree(child)) {
            tree.name = name;
            tree.children = child.children;
            return mergeSingleChildTrees(tree);
        }
        else {
            return {
                name,
                uid: child.uid,
            };
        }
    }
    else {
        tree.children = tree.children.map((node) => {
            if (isModuleTree(node)) {
                return mergeSingleChildTrees(node);
            }
            else {
                return node;
            }
        });
        return tree;
    }
};
export const buildTree = (bundleId, modules, mapper) => {
    const tree = {
        name: bundleId,
        children: [],
    };
    for (const { id, renderedLength, gzipLength, brotliLength } of modules) {
        const bundleModuleUid = mapper.setNodePart(bundleId, id, {
            renderedLength,
            gzipLength,
            brotliLength,
        });
        const trimmedModuleId = mapper.trimProjectRootId(id);
        const pathParts = trimmedModuleId.split(/\\|\//).filter((p) => p !== "");
        addToPath(trimmedModuleId, tree, pathParts, { uid: bundleModuleUid });
    }
    tree.children = tree.children.map((node) => {
        if (isModuleTree(node)) {
            return mergeSingleChildTrees(node);
        }
        else {
            return node;
        }
    });
    return tree;
};
export const mergeTrees = (trees) => {
    const newTree = {
        name: "root",
        children: trees,
        isRoot: true,
    };
    return newTree;
};
export const addLinks = (startModuleId, getModuleInfo, mapper) => {
    const processedNodes = {};
    const moduleIds = [startModuleId];
    while (moduleIds.length > 0) {
        const moduleId = moduleIds.shift();
        if (processedNodes[moduleId]) {
            continue;
        }
        else {
            processedNodes[moduleId] = true;
        }
        const moduleInfo = getModuleInfo(moduleId);
        if (!moduleInfo) {
            return;
        }
        if (moduleInfo.isEntry) {
            mapper.setNodeMeta(moduleId, { isEntry: true });
        }
        if (moduleInfo.isExternal) {
            mapper.setNodeMeta(moduleId, { isExternal: true });
        }
        for (const importedId of moduleInfo.importedIds) {
            mapper.addImportedByLink(importedId, moduleId);
            mapper.addImportedLink(moduleId, importedId);
            moduleIds.push(importedId);
        }
        for (const importedId of moduleInfo.dynamicallyImportedIds || []) {
            mapper.addImportedByLink(importedId, moduleId);
            mapper.addImportedLink(moduleId, importedId, true);
            moduleIds.push(importedId);
        }
    }
};

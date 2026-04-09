import { isESNode } from "../parsers/es.js";
export function getLiteralsByNodeAndRegex(ctx, node, regex, { getLiteralsByMatchingNode, getNodeByRangeStart, getNodeRange, getNodeSourceCode }) {
    const [containerRegexString, stringLiteralRegexString] = regex;
    const sourceCode = getNodeSourceCode(node);
    if (!sourceCode) {
        return [];
    }
    const containerRegex = new RegExp(containerRegexString, "gdm");
    const stringLiteralRegex = new RegExp(stringLiteralRegexString, "gdm");
    const containers = sourceCode.matchAll(containerRegex);
    const matchedLiterals = [];
    for (const container of containers) {
        if (!container.indices || container.indices.length < 2) {
            continue;
        }
        for (const [containerStartIndex] of container.indices.slice(1)) {
            const range = getNodeRange(node);
            const containerNode = getNodeByRangeStart((range?.[0] ?? 0) + containerStartIndex);
            if (!containerNode) {
                continue;
            }
            const literalNodes = getLiteralNodesByRegex(ctx, containerNode, stringLiteralRegex);
            for (const literalNode of literalNodes) {
                const literals = getLiteralsByMatchingNode(literalNode);
                if (!literals) {
                    continue;
                }
                matchedLiterals.push(...literals);
            }
        }
    }
    return matchedLiterals;
}
function getLiteralNodesByRegex(ctx, node, regex, { getNodeByRangeStart, getNodeRange, getNodeSourceCode } = {
    getNodeByRangeStart: (start) => ctx.sourceCode.getNodeByRangeIndex(start),
    getNodeRange: node => isESNode(node) ? [node.range?.[0], node.range?.[1]] : undefined,
    getNodeSourceCode: node => isESNode(node) ? ctx.sourceCode.getText(node) : undefined
}) {
    const sourceCode = getNodeSourceCode(node);
    if (!sourceCode) {
        return [];
    }
    const matchedNodes = [];
    const matches = sourceCode.matchAll(regex);
    for (const groups of matches) {
        if (!groups.indices || groups.indices.length < 2) {
            continue;
        }
        for (const [startIndex] of groups.indices.slice(1)) {
            const range = getNodeRange(node);
            if (!range) {
                continue;
            }
            const literalNode = getNodeByRangeStart((range?.[0] ?? 0) + startIndex);
            if (!literalNode) {
                continue;
            }
            matchedNodes.push(literalNode);
        }
    }
    return matchedNodes;
}
//# sourceMappingURL=regex.js.map
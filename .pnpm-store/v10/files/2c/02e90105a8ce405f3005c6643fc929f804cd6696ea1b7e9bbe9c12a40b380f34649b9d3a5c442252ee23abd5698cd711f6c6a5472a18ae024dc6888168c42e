"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getWhitespace = getWhitespace;
exports.getQuotes = getQuotes;
exports.getContent = getContent;
exports.splitClasses = splitClasses;
exports.display = display;
exports.augmentMessageWithWarnings = augmentMessageWithWarnings;
exports.splitWhitespaces = splitWhitespaces;
exports.getIndentation = getIndentation;
exports.isClassSticky = isClassSticky;
exports.getExactClassLocation = getExactClassLocation;
exports.matchesName = matchesName;
exports.replacePlaceholders = replacePlaceholders;
exports.deduplicateLiterals = deduplicateLiterals;
exports.createObjectPathElement = createObjectPathElement;
exports.isGenericNodeWithParent = isGenericNodeWithParent;
function getWhitespace(classes) {
    const leadingWhitespace = classes.match(/^\s*/)?.[0];
    const trailingWhitespace = classes.match(/\s*$/)?.[0];
    return { leadingWhitespace, trailingWhitespace };
}
function getQuotes(raw) {
    const openingQuote = raw.at(0);
    const closingQuote = raw.at(-1);
    return {
        closingQuote: closingQuote === "'" || closingQuote === '"' || closingQuote === "`" ? closingQuote : undefined,
        openingQuote: openingQuote === "'" || openingQuote === '"' || openingQuote === "`" ? openingQuote : undefined
    };
}
function getContent(raw, quotes, braces) {
    return raw.substring((quotes?.openingQuote?.length ?? 0) + (braces?.closingBraces?.length ?? 0), raw.length - (quotes?.closingQuote?.length ?? 0) - (braces?.openingBraces?.length ?? 0));
}
function splitClasses(classes) {
    if (classes.trim() === "") {
        return [];
    }
    return classes
        .trim()
        .split(/\s+/);
}
function display(classes) {
    return classes
        .replaceAll(" ", "·")
        .replaceAll("\n", "↵\n")
        .replaceAll("\r", "↩\r")
        .replaceAll("\t", "→");
}
function augmentMessageWithWarnings(message, documentationUrl, warnings) {
    const ruleWarnings = warnings
        ?.filter(warning => warning)
        .map(warning => ({ ...warning, url: documentationUrl }));
    if (!ruleWarnings || ruleWarnings.length === 0) {
        return message;
    }
    return [
        ruleWarnings.flatMap(({ option, title, url }) => [
            `⚠️ Warning: ${title}. Option \`${option}\` may be misconfigured.`,
            `Check documentation at ${url}`
        ]).join("\n"),
        message
    ].join("\n\n");
}
function splitWhitespaces(classes) {
    return classes.split(/\S+/);
}
function getIndentation(line) {
    return line.match(/^[\t ]*/)?.[0].length ?? 0;
}
function isClassSticky(literal, classIndex) {
    const classes = literal.content;
    const classChunks = splitClasses(classes);
    const whitespaceChunks = splitWhitespaces(classes);
    const startsWithWhitespace = whitespaceChunks.length > 0 && whitespaceChunks[0] !== "";
    const endsWithWhitespace = whitespaceChunks.length > 0 && whitespaceChunks[whitespaceChunks.length - 1] !== "";
    return (!startsWithWhitespace && classIndex === 0 && !!literal.closingBraces ||
        !endsWithWhitespace && classIndex === classChunks.length - 1 && !!literal.openingBraces);
}
function getExactClassLocation(literal, startIndex, endIndex) {
    const linesUpToStartIndex = literal.content.slice(0, startIndex).split(/\r?\n/);
    const isOnFirstLine = linesUpToStartIndex.length === 1;
    const containingLine = linesUpToStartIndex.at(-1);
    const line = literal.loc.start.line + linesUpToStartIndex.length - 1;
    const column = (isOnFirstLine
        ? literal.loc.start.column + (literal.openingQuote?.length ?? 0) + (literal.closingBraces?.length ?? 0)
        : 0) + (containingLine?.length ?? 0);
    return {
        end: {
            column: column + (endIndex - startIndex),
            line
        },
        start: {
            column,
            line
        }
    };
}
function matchesName(pattern, name) {
    if (!name) {
        return false;
    }
    const match = name.match(pattern);
    return !!match && match[0] === name;
}
function replacePlaceholders(template, match) {
    return template.replace(/\$(\d+)/g, (_, groupIndex) => {
        const index = Number(groupIndex);
        return match[index] ?? "";
    });
}
function deduplicateLiterals(literals) {
    return literals.filter((l1, index) => {
        return literals.findIndex(l2 => {
            return l1.content === l2.content &&
                l1.range[0] === l2.range[0] &&
                l1.range[1] === l2.range[1];
        }) === index;
    });
}
function createObjectPathElement(path) {
    if (!path) {
        return "";
    }
    return path.match(/^[A-Z_a-z]\w*$/)
        ? path
        : `["${path}"]`;
}
function isGenericNodeWithParent(node) {
    return (typeof node === "object" &&
        node !== null &&
        "parent" in node &&
        node.parent !== null &&
        typeof node.parent === "object");
}
//# sourceMappingURL=utils.js.map
export function escapeNestedQuotes(content, surroundingQuotes) {
    const regex = surroundingQuotes === "'"
        ? /(?<!\\)'/g
        : surroundingQuotes === "\""
            ? /(?<!\\)"/g
            : /(?<!\\)`/g;
    return content.replace(regex, `\\${surroundingQuotes}`);
}
//# sourceMappingURL=quotes.js.map
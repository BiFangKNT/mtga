"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.escapeNestedQuotes = escapeNestedQuotes;
function escapeNestedQuotes(content, surroundingQuotes) {
    const regex = surroundingQuotes === "'"
        ? /(?<!\\)'/g
        : surroundingQuotes === "\""
            ? /(?<!\\)"/g
            : /(?<!\\)`/g;
    return content.replace(regex, `\\${surroundingQuotes}`);
}
//# sourceMappingURL=quotes.js.map
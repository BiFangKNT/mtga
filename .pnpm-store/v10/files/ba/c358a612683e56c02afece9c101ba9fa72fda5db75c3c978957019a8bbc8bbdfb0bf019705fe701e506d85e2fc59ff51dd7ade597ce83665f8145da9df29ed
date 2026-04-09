"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.lintClasses = lintClasses;
const utils_js_1 = require("./utils.js");
function lintClasses(ctx, literal, report) {
    const classChunks = (0, utils_js_1.splitClasses)(literal.content);
    const whitespaceChunks = (0, utils_js_1.splitWhitespaces)(literal.content);
    const startsWithWhitespace = whitespaceChunks.length > 0 && whitespaceChunks[0] !== "";
    const after = [...classChunks];
    for (let classIndex = 0, stringIndex = 0; classIndex < classChunks.length; classIndex++) {
        const className = classChunks[classIndex];
        if (startsWithWhitespace) {
            stringIndex += whitespaceChunks[classIndex].length;
        }
        const startIndex = stringIndex;
        const endIndex = stringIndex + className.length;
        stringIndex = endIndex;
        if (!startsWithWhitespace) {
            stringIndex += whitespaceChunks[classIndex + 1].length;
        }
        const result = report(className, classIndex, after);
        if (result === undefined || result === false || result === className) {
            continue;
        }
        const [literalStart] = literal.range;
        if (typeof result === "object" && result.fix !== undefined) {
            after[classIndex] = result.fix;
        }
        ctx.report({
            data: {
                className
            },
            loc: (0, utils_js_1.getExactClassLocation)(literal, startIndex, endIndex),
            message: typeof result === "object" && result.message
                ? result.message
                : "Expected {{ before }} to be {{ after }}.",
            ...typeof result === "object" && result.fix !== undefined &&
                {
                    fix: fixer => fixer.replaceTextRange([
                        literalStart + startIndex + 1,
                        literalStart + endIndex + 1
                    ], result.fix)
                }
        });
    }
}
//# sourceMappingURL=lint.js.map
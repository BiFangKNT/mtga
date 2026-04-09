"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDissectedClasses = getDissectedClasses;
const escape_js_1 = require("../async-utils/escape.js");
const prefix_async_v4_js_1 = require("./prefix.async.v4.js");
function getDissectedClasses(context, classes) {
    const prefix = (0, prefix_async_v4_js_1.getPrefix)(context);
    const separator = ":";
    return classes.map(className => {
        const [parsed] = context.parseCandidate(className);
        const variants = parsed?.variants?.map(variant => context.printVariant(variant)).reverse() ?? [];
        let base = className
            .replace(new RegExp(`^${(0, escape_js_1.escapeForRegex)(prefix + separator)}`), "")
            .replace(new RegExp(`^${(0, escape_js_1.escapeForRegex)(variants.join(separator) + separator)}`), "");
        const isNegative = base.startsWith("-");
        base = base.replace(/^-/, "");
        const isImportantAtStart = base.startsWith("!");
        base = base.replace(/^!/, "");
        const isImportantAtEnd = base.endsWith("!");
        base = base.replace(/!$/, "");
        return {
            base,
            className,
            important: [isImportantAtStart, isImportantAtEnd],
            negative: isNegative,
            prefix,
            separator,
            variants
        };
    });
}
//# sourceMappingURL=dissect-classes.async.v4.js.map
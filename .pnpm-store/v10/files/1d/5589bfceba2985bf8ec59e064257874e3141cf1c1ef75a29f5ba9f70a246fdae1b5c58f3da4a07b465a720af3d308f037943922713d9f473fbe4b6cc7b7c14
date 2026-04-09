import * as utils from "tailwindcss/lib/util/splitAtTopLevelOnly.js";
import { escapeForRegex } from "../async-utils/escape.js";
import { getPrefix } from "./prefix.async.v3.js";
export function getDissectedClasses(context, classes) {
    const prefix = getPrefix(context);
    const separator = context.tailwindConfig.separator ?? ":";
    return classes.map(className => {
        const splitChunks = utils.splitAtTopLevelOnly?.(className, separator) ?? utils.default?.splitAtTopLevelOnly?.(className, separator);
        const variants = splitChunks.slice(0, -1);
        let base = className
            .replace(new RegExp(`^${escapeForRegex(variants.join(separator) + separator)}`), "")
            .replace(new RegExp(`^${escapeForRegex(prefix)}`), "");
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
//# sourceMappingURL=dissect-classes.async.v3.js.map
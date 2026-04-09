import { escapeForRegex } from "../async-utils/escape.js";
import { getPrefix } from "./prefix.async.v4.js";
export function getDissectedClasses(context, classes) {
    const prefix = getPrefix(context);
    const separator = ":";
    return classes.map(className => {
        const [parsed] = context.parseCandidate(className);
        const variants = parsed?.variants?.map(variant => context.printVariant(variant)).reverse() ?? [];
        let base = className
            .replace(new RegExp(`^${escapeForRegex(prefix + separator)}`), "")
            .replace(new RegExp(`^${escapeForRegex(variants.join(separator) + separator)}`), "");
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
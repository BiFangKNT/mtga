import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { isAttributesRegex, isCalleeRegex, isVariableRegex } from "./matchers.js";
import { warnOnce } from "./warn.js";
export function getCommonOptions(ctx) {
    const attributes = getOption(ctx, "attributes") ?? DEFAULT_ATTRIBUTE_NAMES;
    const callees = getOption(ctx, "callees") ?? DEFAULT_CALLEE_NAMES;
    const variables = getOption(ctx, "variables") ?? DEFAULT_VARIABLE_NAMES;
    const tags = getOption(ctx, "tags") ?? DEFAULT_TAG_NAMES;
    const tailwindConfig = getOption(ctx, "entryPoint") ?? getOption(ctx, "tailwindConfig");
    const tsconfig = getOption(ctx, "tsconfig");
    if (Array.isArray(attributes) && attributes.some(attributes => isAttributesRegex(attributes)) ||
        Array.isArray(callees) && callees.some(callees => isCalleeRegex(callees)) ||
        Array.isArray(variables) && variables.some(variables => isVariableRegex(variables))) {
        warnOnce("Regex matching is deprecated and will be removed in the next major version. Please use matchers instead. See: https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/configuration/advanced.md#matchers");
    }
    return {
        attributes,
        callees,
        tags,
        tailwindConfig,
        tsconfig,
        variables
    };
}
function getOption(ctx, key) {
    return ctx.options[0]?.[key] ?? ctx.settings["eslint-plugin-better-tailwindcss"]?.[key] ??
        ctx.settings["better-tailwindcss"]?.[key];
}
//# sourceMappingURL=options.js.map
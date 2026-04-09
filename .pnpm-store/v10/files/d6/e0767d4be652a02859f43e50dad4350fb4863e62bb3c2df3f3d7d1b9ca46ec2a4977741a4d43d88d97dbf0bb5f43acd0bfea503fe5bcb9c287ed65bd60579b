"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCommonOptions = getCommonOptions;
const default_options_js_1 = require("../options/default-options.js");
const matchers_js_1 = require("./matchers.js");
const warn_js_1 = require("./warn.js");
function getCommonOptions(ctx) {
    const attributes = getOption(ctx, "attributes") ?? default_options_js_1.DEFAULT_ATTRIBUTE_NAMES;
    const callees = getOption(ctx, "callees") ?? default_options_js_1.DEFAULT_CALLEE_NAMES;
    const variables = getOption(ctx, "variables") ?? default_options_js_1.DEFAULT_VARIABLE_NAMES;
    const tags = getOption(ctx, "tags") ?? default_options_js_1.DEFAULT_TAG_NAMES;
    const tailwindConfig = getOption(ctx, "entryPoint") ?? getOption(ctx, "tailwindConfig");
    const tsconfig = getOption(ctx, "tsconfig");
    if (Array.isArray(attributes) && attributes.some(attributes => (0, matchers_js_1.isAttributesRegex)(attributes)) ||
        Array.isArray(callees) && callees.some(callees => (0, matchers_js_1.isCalleeRegex)(callees)) ||
        Array.isArray(variables) && variables.some(variables => (0, matchers_js_1.isVariableRegex)(variables))) {
        (0, warn_js_1.warnOnce)("Regex matching is deprecated and will be removed in the next major version. Please use matchers instead. See: https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/configuration/advanced.md#matchers");
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
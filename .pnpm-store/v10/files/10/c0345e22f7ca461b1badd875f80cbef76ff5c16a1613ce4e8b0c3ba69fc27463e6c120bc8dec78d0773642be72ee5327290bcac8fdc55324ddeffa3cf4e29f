"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.noRestrictedClasses = void 0;
exports.getOptions = getOptions;
const default_options_js_1 = require("../options/default-options.js");
const descriptions_js_1 = require("../options/descriptions.js");
const lint_js_1 = require("../utils/lint.js");
const options_js_1 = require("../utils/options.js");
const rule_js_1 = require("../utils/rule.js");
const utils_js_1 = require("../utils/utils.js");
const defaultOptions = {
    attributes: default_options_js_1.DEFAULT_ATTRIBUTE_NAMES,
    callees: default_options_js_1.DEFAULT_CALLEE_NAMES,
    restrict: [],
    tags: default_options_js_1.DEFAULT_TAG_NAMES,
    variables: default_options_js_1.DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-restricted-classes.md";
exports.noRestrictedClasses = {
    name: "no-restricted-classes",
    rule: {
        create: ctx => (0, rule_js_1.createRuleListener)(ctx, initialize, getOptions, lintLiterals),
        meta: {
            docs: {
                description: "Disallow restricted classes.",
                recommended: false,
                url: DOCUMENTATION_URL
            },
            fixable: "code",
            schema: [
                {
                    additionalProperties: false,
                    properties: {
                        ...descriptions_js_1.CALLEE_SCHEMA,
                        ...descriptions_js_1.ATTRIBUTE_SCHEMA,
                        ...descriptions_js_1.VARIABLE_SCHEMA,
                        ...descriptions_js_1.TAG_SCHEMA,
                        restrict: {
                            items: {
                                anyOf: [
                                    {
                                        additionalProperties: false,
                                        properties: {
                                            fix: {
                                                description: "A replacement class",
                                                type: "string"
                                            },
                                            message: {
                                                default: undefined,
                                                description: "The message to report when a class is restricted.",
                                                type: "string"
                                            },
                                            pattern: {
                                                description: "The regex pattern to match restricted classes.",
                                                type: "string"
                                            }
                                        },
                                        required: ["pattern"],
                                        type: "object"
                                    },
                                    {
                                        type: "string"
                                    }
                                ]
                            },
                            type: "array"
                        }
                    },
                    type: "object"
                }
            ],
            type: "problem"
        }
    }
};
function initialize() { }
function lintLiterals(ctx, literals) {
    const { restrict: restrictions } = getOptions(ctx);
    for (const literal of literals) {
        (0, lint_js_1.lintClasses)(ctx, literal, (className, classes) => {
            for (const restriction of restrictions) {
                const pattern = typeof restriction === "string"
                    ? restriction
                    : restriction.pattern;
                const matches = className.match(pattern);
                if (!matches) {
                    continue;
                }
                const message = typeof restriction === "string" || !restriction.message
                    ? `Restricted class: "${className}".`
                    : (0, utils_js_1.replacePlaceholders)(restriction.message, matches);
                if (typeof restriction === "string") {
                    return {
                        message
                    };
                }
                if (restriction.fix !== undefined) {
                    return {
                        fix: (0, utils_js_1.replacePlaceholders)(restriction.fix, matches),
                        message
                    };
                }
                return {
                    message
                };
            }
        });
    }
}
function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = (0, options_js_1.getCommonOptions)(ctx);
    const restrict = options.restrict ?? defaultOptions.restrict;
    return {
        ...common,
        restrict
    };
}
//# sourceMappingURL=no-restricted-classes.js.map
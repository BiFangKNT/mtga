import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { ATTRIBUTE_SCHEMA, CALLEE_SCHEMA, TAG_SCHEMA, VARIABLE_SCHEMA } from "../options/descriptions.js";
import { lintClasses } from "../utils/lint.js";
import { getCommonOptions } from "../utils/options.js";
import { createRuleListener } from "../utils/rule.js";
import { replacePlaceholders } from "../utils/utils.js";
const defaultOptions = {
    attributes: DEFAULT_ATTRIBUTE_NAMES,
    callees: DEFAULT_CALLEE_NAMES,
    restrict: [],
    tags: DEFAULT_TAG_NAMES,
    variables: DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-restricted-classes.md";
export const noRestrictedClasses = {
    name: "no-restricted-classes",
    rule: {
        create: ctx => createRuleListener(ctx, initialize, getOptions, lintLiterals),
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
                        ...CALLEE_SCHEMA,
                        ...ATTRIBUTE_SCHEMA,
                        ...VARIABLE_SCHEMA,
                        ...TAG_SCHEMA,
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
        lintClasses(ctx, literal, (className, classes) => {
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
                    : replacePlaceholders(restriction.message, matches);
                if (typeof restriction === "string") {
                    return {
                        message
                    };
                }
                if (restriction.fix !== undefined) {
                    return {
                        fix: replacePlaceholders(restriction.fix, matches),
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
export function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = getCommonOptions(ctx);
    const restrict = options.restrict ?? defaultOptions.restrict;
    return {
        ...common,
        restrict
    };
}
//# sourceMappingURL=no-restricted-classes.js.map
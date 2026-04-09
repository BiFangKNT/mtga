"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.noConflictingClasses = void 0;
exports.getOptions = getOptions;
const default_options_js_1 = require("../options/default-options.js");
const descriptions_js_1 = require("../options/descriptions.js");
const conflicting_classes_js_1 = require("../tailwindcss/conflicting-classes.js");
const lint_js_1 = require("../utils/lint.js");
const options_js_1 = require("../utils/options.js");
const rule_js_1 = require("../utils/rule.js");
const utils_js_1 = require("../utils/utils.js");
const defaultOptions = {
    attributes: default_options_js_1.DEFAULT_ATTRIBUTE_NAMES,
    callees: default_options_js_1.DEFAULT_CALLEE_NAMES,
    tags: default_options_js_1.DEFAULT_TAG_NAMES,
    variables: default_options_js_1.DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-conflicting-classes.md";
exports.noConflictingClasses = {
    name: "no-conflicting-classes",
    rule: {
        create: ctx => (0, rule_js_1.createRuleListener)(ctx, initialize, getOptions, lintLiterals),
        meta: {
            docs: {
                description: "Disallow classes that produce conflicting styles.",
                recommended: true,
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
                        ...descriptions_js_1.ENTRYPOINT_SCHEMA,
                        ...descriptions_js_1.TAILWIND_CONFIG_SCHEMA,
                        ...descriptions_js_1.TSCONFIG_SCHEMA
                    },
                    type: "object"
                }
            ],
            type: "problem"
        }
    }
};
function initialize() {
    (0, conflicting_classes_js_1.createGetConflictingClasses)();
}
function lintLiterals(ctx, literals) {
    const getConflictingClasses = (0, conflicting_classes_js_1.createGetConflictingClasses)();
    for (const literal of literals) {
        const { tailwindConfig, tsconfig } = getOptions(ctx);
        const classes = (0, utils_js_1.splitClasses)(literal.content);
        const { conflictingClasses, warnings } = getConflictingClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        if (Object.keys(conflictingClasses).length === 0) {
            continue;
        }
        (0, lint_js_1.lintClasses)(ctx, literal, className => {
            if (!conflictingClasses[className]) {
                return;
            }
            const conflicts = Object.entries(conflictingClasses[className]);
            if (conflicts.length === 0) {
                return;
            }
            const conflictingClassNames = conflicts.map(([conflictingClassName]) => conflictingClassName);
            const conflictingProperties = conflicts.reduce((acc, [, properties]) => {
                for (const property of properties) {
                    if (!acc.includes(property.cssPropertyName)) {
                        acc.push(property.cssPropertyName);
                    }
                }
                return acc;
            }, []);
            const conflictingClassString = conflictingClassNames.join(", ");
            const conflictingPropertiesString = conflictingProperties.map(conflictingProperty => `"${conflictingProperty}"`).join(", ");
            return {
                message: (0, utils_js_1.augmentMessageWithWarnings)(`Conflicting class detected: "${className}" and "${conflictingClassString}" apply the same CSS properties: ${conflictingPropertiesString}.`, DOCUMENTATION_URL, warnings)
            };
        });
    }
}
function getOptions(ctx) {
    return (0, options_js_1.getCommonOptions)(ctx);
}
//# sourceMappingURL=no-conflicting-classes.js.map
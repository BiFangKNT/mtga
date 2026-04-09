"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.noDuplicateClasses = void 0;
const default_options_js_1 = require("../options/default-options.js");
const descriptions_js_1 = require("../options/descriptions.js");
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
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-duplicate-classes.md";
exports.noDuplicateClasses = {
    name: "no-duplicate-classes",
    rule: {
        create: ctx => (0, rule_js_1.createRuleListener)(ctx, initialize, getOptions, lintLiterals),
        meta: {
            docs: {
                category: "Stylistic Issues",
                description: "Disallow duplicate class names in tailwind classes.",
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
                        ...descriptions_js_1.TAG_SCHEMA
                    },
                    type: "object"
                }
            ],
            type: "layout"
        }
    }
};
function initialize() { }
function lintLiterals(ctx, literals) {
    for (const literal of literals) {
        const parentClasses = literal.priorLiterals
            ? getClassesFromLiteralNodes(literal.priorLiterals)
            : [];
        (0, lint_js_1.lintClasses)(ctx, literal, (className, index, after) => {
            const duplicateClassIndex = after.findIndex((afterClass, afterIndex) => afterClass === className && afterIndex < index);
            // always keep sticky classes
            if ((0, utils_js_1.isClassSticky)(literal, index) || (0, utils_js_1.isClassSticky)(literal, duplicateClassIndex)) {
                return;
            }
            if (parentClasses.includes(className) || duplicateClassIndex !== -1) {
                return {
                    fix: "",
                    message: `Duplicate classname: "${className}}".`
                };
            }
        });
    }
}
function getClassesFromLiteralNodes(literals) {
    return literals.reduce((combinedClasses, literal) => {
        if (!literal) {
            return combinedClasses;
        }
        const classes = literal.content;
        const split = (0, utils_js_1.splitClasses)(classes);
        for (const className of split) {
            if (!combinedClasses.includes(className)) {
                combinedClasses.push(className);
            }
        }
        return combinedClasses;
    }, []);
}
function getOptions(ctx) {
    return (0, options_js_1.getCommonOptions)(ctx);
}
//# sourceMappingURL=no-duplicate-classes.js.map
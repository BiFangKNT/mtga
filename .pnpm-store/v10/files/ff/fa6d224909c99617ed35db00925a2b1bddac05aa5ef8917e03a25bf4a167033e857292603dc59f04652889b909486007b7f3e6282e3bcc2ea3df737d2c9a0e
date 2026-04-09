import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { ATTRIBUTE_SCHEMA, CALLEE_SCHEMA, TAG_SCHEMA, VARIABLE_SCHEMA } from "../options/descriptions.js";
import { lintClasses } from "../utils/lint.js";
import { getCommonOptions } from "../utils/options.js";
import { createRuleListener } from "../utils/rule.js";
import { isClassSticky, splitClasses } from "../utils/utils.js";
const defaultOptions = {
    attributes: DEFAULT_ATTRIBUTE_NAMES,
    callees: DEFAULT_CALLEE_NAMES,
    tags: DEFAULT_TAG_NAMES,
    variables: DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-duplicate-classes.md";
export const noDuplicateClasses = {
    name: "no-duplicate-classes",
    rule: {
        create: ctx => createRuleListener(ctx, initialize, getOptions, lintLiterals),
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
                        ...CALLEE_SCHEMA,
                        ...ATTRIBUTE_SCHEMA,
                        ...VARIABLE_SCHEMA,
                        ...TAG_SCHEMA
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
        lintClasses(ctx, literal, (className, index, after) => {
            const duplicateClassIndex = after.findIndex((afterClass, afterIndex) => afterClass === className && afterIndex < index);
            // always keep sticky classes
            if (isClassSticky(literal, index) || isClassSticky(literal, duplicateClassIndex)) {
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
        const split = splitClasses(classes);
        for (const className of split) {
            if (!combinedClasses.includes(className)) {
                combinedClasses.push(className);
            }
        }
        return combinedClasses;
    }, []);
}
function getOptions(ctx) {
    return getCommonOptions(ctx);
}
//# sourceMappingURL=no-duplicate-classes.js.map
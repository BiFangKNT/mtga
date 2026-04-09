import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { ATTRIBUTE_SCHEMA, CALLEE_SCHEMA, ENTRYPOINT_SCHEMA, TAG_SCHEMA, TAILWIND_CONFIG_SCHEMA, TSCONFIG_SCHEMA, VARIABLE_SCHEMA } from "../options/descriptions.js";
import { createGetConflictingClasses } from "../tailwindcss/conflicting-classes.js";
import { lintClasses } from "../utils/lint.js";
import { getCommonOptions } from "../utils/options.js";
import { createRuleListener } from "../utils/rule.js";
import { augmentMessageWithWarnings, splitClasses } from "../utils/utils.js";
const defaultOptions = {
    attributes: DEFAULT_ATTRIBUTE_NAMES,
    callees: DEFAULT_CALLEE_NAMES,
    tags: DEFAULT_TAG_NAMES,
    variables: DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/no-conflicting-classes.md";
export const noConflictingClasses = {
    name: "no-conflicting-classes",
    rule: {
        create: ctx => createRuleListener(ctx, initialize, getOptions, lintLiterals),
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
                        ...CALLEE_SCHEMA,
                        ...ATTRIBUTE_SCHEMA,
                        ...VARIABLE_SCHEMA,
                        ...TAG_SCHEMA,
                        ...ENTRYPOINT_SCHEMA,
                        ...TAILWIND_CONFIG_SCHEMA,
                        ...TSCONFIG_SCHEMA
                    },
                    type: "object"
                }
            ],
            type: "problem"
        }
    }
};
function initialize() {
    createGetConflictingClasses();
}
function lintLiterals(ctx, literals) {
    const getConflictingClasses = createGetConflictingClasses();
    for (const literal of literals) {
        const { tailwindConfig, tsconfig } = getOptions(ctx);
        const classes = splitClasses(literal.content);
        const { conflictingClasses, warnings } = getConflictingClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        if (Object.keys(conflictingClasses).length === 0) {
            continue;
        }
        lintClasses(ctx, literal, className => {
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
                message: augmentMessageWithWarnings(`Conflicting class detected: "${className}" and "${conflictingClassString}" apply the same CSS properties: ${conflictingPropertiesString}.`, DOCUMENTATION_URL, warnings)
            };
        });
    }
}
export function getOptions(ctx) {
    return getCommonOptions(ctx);
}
//# sourceMappingURL=no-conflicting-classes.js.map
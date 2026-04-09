import { multiline } from "../rules/deprecated/multiline.js";
import { sortClasses } from "../rules/deprecated/sort-classes.js";
import { enforceConsistentClassOrder } from "../rules/enforce-consistent-class-order.js";
import { enforceConsistentImportantPosition } from "../rules/enforce-consistent-important-position.js";
import { enforceConsistentLineWrapping } from "../rules/enforce-consistent-line-wrapping.js";
import { enforceConsistentVariableSyntax } from "../rules/enforce-consistent-variable-syntax.js";
import { enforceShorthandClasses } from "../rules/enforce-shorthand-classes.js";
import { noConflictingClasses } from "../rules/no-conflicting-classes.js";
import { noDeprecatedClasses } from "../rules/no-deprecated-classes.js";
import { noDuplicateClasses } from "../rules/no-duplicate-classes.js";
import { noRestrictedClasses } from "../rules/no-restricted-classes.js";
import { noUnnecessaryWhitespace } from "../rules/no-unnecessary-whitespace.js";
import { noUnregisteredClasses } from "../rules/no-unregistered-classes.js";
const plugin = {
    meta: {
        name: "better-tailwindcss"
    },
    rules: {
        [multiline.name]: multiline.rule,
        [sortClasses.name]: sortClasses.rule,
        [enforceConsistentClassOrder.name]: enforceConsistentClassOrder.rule,
        [enforceConsistentImportantPosition.name]: enforceConsistentImportantPosition.rule,
        [enforceConsistentLineWrapping.name]: enforceConsistentLineWrapping.rule,
        [enforceConsistentVariableSyntax.name]: enforceConsistentVariableSyntax.rule,
        [enforceShorthandClasses.name]: enforceShorthandClasses.rule,
        [noConflictingClasses.name]: noConflictingClasses.rule,
        [noDeprecatedClasses.name]: noDeprecatedClasses.rule,
        [noDuplicateClasses.name]: noDuplicateClasses.rule,
        [noRestrictedClasses.name]: noRestrictedClasses.rule,
        [noUnnecessaryWhitespace.name]: noUnnecessaryWhitespace.rule,
        [noUnregisteredClasses.name]: noUnregisteredClasses.rule
    }
};
const plugins = [plugin.meta.name];
const getStylisticRules = (severity = "warn") => {
    return {
        [`${plugin.meta.name}/${enforceConsistentClassOrder.name}`]: severity,
        [`${plugin.meta.name}/${enforceConsistentLineWrapping.name}`]: severity,
        [`${plugin.meta.name}/${noDuplicateClasses.name}`]: severity,
        [`${plugin.meta.name}/${noUnnecessaryWhitespace.name}`]: severity
    };
};
const getCorrectnessRules = (severity = "error") => {
    return {
        [`${plugin.meta.name}/${noConflictingClasses.name}`]: severity,
        [`${plugin.meta.name}/${noUnregisteredClasses.name}`]: severity
    };
};
const createConfig = (name, getRulesFunction) => {
    return {
        [`${name}-error`]: {
            plugins,
            rules: getRulesFunction("error")
        },
        [`${name}-warn`]: {
            plugins,
            rules: getRulesFunction("warn")
        },
        [name]: {
            plugins,
            rules: getRulesFunction()
        }
    };
};
export const config = {
    ...plugin,
    configs: {
        ...createConfig("stylistic", getStylisticRules),
        ...createConfig("correctness", getCorrectnessRules),
        ...createConfig("recommended", severity => ({
            ...getStylisticRules(severity),
            ...getCorrectnessRules(severity)
        }))
    }
};
//# sourceMappingURL=config.js.map
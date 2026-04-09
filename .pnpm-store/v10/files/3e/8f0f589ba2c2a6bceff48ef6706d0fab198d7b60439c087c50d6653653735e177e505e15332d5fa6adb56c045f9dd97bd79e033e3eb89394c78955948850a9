"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.config = void 0;
const multiline_js_1 = require("../rules/deprecated/multiline.js");
const sort_classes_js_1 = require("../rules/deprecated/sort-classes.js");
const enforce_consistent_class_order_js_1 = require("../rules/enforce-consistent-class-order.js");
const enforce_consistent_important_position_js_1 = require("../rules/enforce-consistent-important-position.js");
const enforce_consistent_line_wrapping_js_1 = require("../rules/enforce-consistent-line-wrapping.js");
const enforce_consistent_variable_syntax_js_1 = require("../rules/enforce-consistent-variable-syntax.js");
const enforce_shorthand_classes_js_1 = require("../rules/enforce-shorthand-classes.js");
const no_conflicting_classes_js_1 = require("../rules/no-conflicting-classes.js");
const no_deprecated_classes_js_1 = require("../rules/no-deprecated-classes.js");
const no_duplicate_classes_js_1 = require("../rules/no-duplicate-classes.js");
const no_restricted_classes_js_1 = require("../rules/no-restricted-classes.js");
const no_unnecessary_whitespace_js_1 = require("../rules/no-unnecessary-whitespace.js");
const no_unregistered_classes_js_1 = require("../rules/no-unregistered-classes.js");
const plugin = {
    meta: {
        name: "better-tailwindcss"
    },
    rules: {
        [multiline_js_1.multiline.name]: multiline_js_1.multiline.rule,
        [sort_classes_js_1.sortClasses.name]: sort_classes_js_1.sortClasses.rule,
        [enforce_consistent_class_order_js_1.enforceConsistentClassOrder.name]: enforce_consistent_class_order_js_1.enforceConsistentClassOrder.rule,
        [enforce_consistent_important_position_js_1.enforceConsistentImportantPosition.name]: enforce_consistent_important_position_js_1.enforceConsistentImportantPosition.rule,
        [enforce_consistent_line_wrapping_js_1.enforceConsistentLineWrapping.name]: enforce_consistent_line_wrapping_js_1.enforceConsistentLineWrapping.rule,
        [enforce_consistent_variable_syntax_js_1.enforceConsistentVariableSyntax.name]: enforce_consistent_variable_syntax_js_1.enforceConsistentVariableSyntax.rule,
        [enforce_shorthand_classes_js_1.enforceShorthandClasses.name]: enforce_shorthand_classes_js_1.enforceShorthandClasses.rule,
        [no_conflicting_classes_js_1.noConflictingClasses.name]: no_conflicting_classes_js_1.noConflictingClasses.rule,
        [no_deprecated_classes_js_1.noDeprecatedClasses.name]: no_deprecated_classes_js_1.noDeprecatedClasses.rule,
        [no_duplicate_classes_js_1.noDuplicateClasses.name]: no_duplicate_classes_js_1.noDuplicateClasses.rule,
        [no_restricted_classes_js_1.noRestrictedClasses.name]: no_restricted_classes_js_1.noRestrictedClasses.rule,
        [no_unnecessary_whitespace_js_1.noUnnecessaryWhitespace.name]: no_unnecessary_whitespace_js_1.noUnnecessaryWhitespace.rule,
        [no_unregistered_classes_js_1.noUnregisteredClasses.name]: no_unregistered_classes_js_1.noUnregisteredClasses.rule
    }
};
const plugins = [plugin.meta.name];
const getStylisticRules = (severity = "warn") => {
    return {
        [`${plugin.meta.name}/${enforce_consistent_class_order_js_1.enforceConsistentClassOrder.name}`]: severity,
        [`${plugin.meta.name}/${enforce_consistent_line_wrapping_js_1.enforceConsistentLineWrapping.name}`]: severity,
        [`${plugin.meta.name}/${no_duplicate_classes_js_1.noDuplicateClasses.name}`]: severity,
        [`${plugin.meta.name}/${no_unnecessary_whitespace_js_1.noUnnecessaryWhitespace.name}`]: severity
    };
};
const getCorrectnessRules = (severity = "error") => {
    return {
        [`${plugin.meta.name}/${no_conflicting_classes_js_1.noConflictingClasses.name}`]: severity,
        [`${plugin.meta.name}/${no_unregistered_classes_js_1.noUnregisteredClasses.name}`]: severity
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
exports.config = {
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
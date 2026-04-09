"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.enforceConsistentImportantPosition = void 0;
exports.getOptions = getOptions;
const default_options_js_1 = require("../options/default-options.js");
const descriptions_js_1 = require("../options/descriptions.js");
const dissect_classes_js_1 = require("../tailwindcss/dissect-classes.js");
const class_js_1 = require("../utils/class.js");
const lint_js_1 = require("../utils/lint.js");
const options_js_1 = require("../utils/options.js");
const rule_js_1 = require("../utils/rule.js");
const tailwindcss_js_1 = require("../async-utils/tailwindcss.js");
const utils_js_1 = require("../utils/utils.js");
const defaultOptions = {
    attributes: default_options_js_1.DEFAULT_ATTRIBUTE_NAMES,
    callees: default_options_js_1.DEFAULT_CALLEE_NAMES,
    tags: default_options_js_1.DEFAULT_TAG_NAMES,
    variables: default_options_js_1.DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/enforce-consistent-important-position.md";
exports.enforceConsistentImportantPosition = {
    name: "enforce-consistent-important-position",
    rule: {
        create: ctx => (0, rule_js_1.createRuleListener)(ctx, initialize, getOptions, lintLiterals),
        meta: {
            docs: {
                description: "Enforce consistent important position for classes.",
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
                        ...descriptions_js_1.ENTRYPOINT_SCHEMA,
                        ...descriptions_js_1.TAILWIND_CONFIG_SCHEMA,
                        ...descriptions_js_1.TSCONFIG_SCHEMA,
                        position: {
                            description: "Preferred position for important classes. 'legacy' places the important modifier (!) at the start of the class name, 'recommended' places it at the end.",
                            enum: ["legacy", "recommended"],
                            type: "string"
                        }
                    },
                    type: "object"
                }
            ],
            type: "problem"
        }
    }
};
function initialize() {
    (0, dissect_classes_js_1.createGetDissectedClasses)();
}
function lintLiterals(ctx, literals) {
    const getDissectedClasses = (0, dissect_classes_js_1.createGetDissectedClasses)();
    const { position, tailwindConfig, tsconfig } = getOptions(ctx);
    const { major } = (0, tailwindcss_js_1.getTailwindcssVersion)();
    for (const literal of literals) {
        const classes = (0, utils_js_1.splitClasses)(literal.content);
        const { dissectedClasses, warnings } = getDissectedClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        (0, lint_js_1.lintClasses)(ctx, literal, (className, index, after) => {
            const dissectedClass = dissectedClasses.find(dissectedClass => dissectedClass.className === className);
            if (!dissectedClass) {
                return;
            }
            const [importantAtStart, importantAtEnd] = dissectedClass.important;
            if (!importantAtStart && !importantAtEnd ||
                position === "legacy" && importantAtStart ||
                position === "recommended" && importantAtEnd) {
                return;
            }
            if (major <= 3 /* TailwindcssVersion.V3 */ && position === "recommended") {
                warnings.push({
                    option: "position",
                    title: `The "${position}" position is not supported in Tailwind CSS v3`
                });
            }
            const fix = position === "recommended"
                ? (0, class_js_1.buildClass)({ ...dissectedClass, important: [false, true] })
                : (0, class_js_1.buildClass)({ ...dissectedClass, important: [true, false] });
            return {
                fix,
                message: (0, utils_js_1.augmentMessageWithWarnings)(`Incorrect important position. "${className}" should be "${fix}".`, DOCUMENTATION_URL, warnings)
            };
        });
    }
}
function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = (0, options_js_1.getCommonOptions)(ctx);
    const position = options.position ?? ((0, tailwindcss_js_1.getTailwindcssVersion)().major === 3 /* TailwindcssVersion.V3 */ ? "legacy" : "recommended");
    return {
        ...common,
        position
    };
}
//# sourceMappingURL=enforce-consistent-important-position.js.map
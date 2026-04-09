"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.enforceConsistentVariableSyntax = void 0;
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
    syntax: "shorthand",
    tags: default_options_js_1.DEFAULT_TAG_NAMES,
    variables: default_options_js_1.DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/enforce-consistent-variable-syntax.md";
exports.enforceConsistentVariableSyntax = {
    name: "enforce-consistent-variable-syntax",
    rule: {
        create: ctx => (0, rule_js_1.createRuleListener)(ctx, initialize, getOptions, lintLiterals),
        meta: {
            docs: {
                description: "Enforce consistent syntax for css variables.",
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
                        syntax: {
                            default: "shorthand",
                            description: "Preferred syntax for CSS variables. 'variable' uses [var(--foo)], 'shorthand' uses (--foo) in Tailwind CSS v4 or [--foo] in Tailwind CSS v3.",
                            enum: ["arbitrary", "parentheses", "shorthand", "variable"],
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
    const { syntax, tailwindConfig, tsconfig } = getOptions(ctx);
    const { major } = (0, tailwindcss_js_1.getTailwindcssVersion)();
    for (const literal of literals) {
        const classes = (0, utils_js_1.splitClasses)(literal.content);
        const { dissectedClasses } = getDissectedClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        (0, lint_js_1.lintClasses)(ctx, literal, className => {
            const dissectedClass = dissectedClasses.find(dissectedClass => dissectedClass.className === className);
            if (!dissectedClass) {
                return;
            }
            // skip variable definitions
            if (dissectedClass.base.includes(":")) {
                return;
            }
            const { after: afterParentheses, before: beforeParentheses, characters: charactersParentheses } = extractBalanced(dissectedClass.base);
            const { after: afterSquareBrackets, before: beforeSquareBrackets, characters: charactersSquareBrackets } = extractBalanced(dissectedClass.base, "[", "]");
            if (syntax === "parentheses" || syntax === "shorthand") {
                if (!charactersSquareBrackets) {
                    return;
                }
                if (isBeginningOfArbitraryVariable(charactersSquareBrackets)) {
                    const { after, characters } = extractBalanced(charactersSquareBrackets);
                    if (trimTailwindWhitespace(after).length > 0) {
                        return;
                    }
                    const fixedClass = major >= 4 /* TailwindcssVersion.V4 */
                        ? (0, class_js_1.buildClass)({ ...dissectedClass, base: [...beforeSquareBrackets, `(${characters})`, ...afterSquareBrackets].join("") })
                        : (0, class_js_1.buildClass)({ ...dissectedClass, base: [...beforeSquareBrackets, `[${characters}]`, ...afterSquareBrackets].join("") });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
                if (isBeginningOfArbitraryShorthand(charactersSquareBrackets)) {
                    if (major <= 3 /* TailwindcssVersion.V3 */) {
                        return;
                    }
                    const fixedClass = (0, class_js_1.buildClass)({
                        ...dissectedClass,
                        base: [...beforeSquareBrackets, `(${charactersSquareBrackets})`, ...afterSquareBrackets].join("")
                    });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
            }
            if (syntax === "arbitrary" || syntax === "variable") {
                if (charactersSquareBrackets && isBeginningOfArbitraryVariable(charactersSquareBrackets)) {
                    return;
                }
                if (isBeginningOfArbitraryShorthand(charactersSquareBrackets)) {
                    const fixedClass = (0, class_js_1.buildClass)({
                        ...dissectedClass,
                        base: [...beforeSquareBrackets, `[var(${charactersSquareBrackets})]`, ...afterSquareBrackets].join("")
                    });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
                if (isBeginningOfArbitraryShorthand(charactersParentheses)) {
                    const fixedClass = (0, class_js_1.buildClass)({
                        ...dissectedClass,
                        base: [
                            ...beforeParentheses,
                            `[var(${charactersParentheses})]`,
                            ...afterParentheses
                        ].join("")
                    });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
            }
        });
    }
}
function isBeginningOfArbitraryShorthand(base) {
    return !!base.match(/^_*--/);
}
function isBeginningOfArbitraryVariable(base) {
    return !!base.match(/^_*var\(_*--/);
}
function extractBalanced(className, start = "(", end = ")") {
    const before = [];
    const characters = [];
    const after = [];
    for (let i = 0, parenthesesCount = 0, hasStarted = false, hasEnded = false; i < className.length; i++) {
        if (className[i] === start) {
            parenthesesCount++;
            if (!hasStarted) {
                hasStarted = true;
                continue;
            }
        }
        if (!hasStarted && !hasEnded) {
            before.push(className[i]);
            continue;
        }
        if (className[i] === end) {
            parenthesesCount--;
            if (parenthesesCount === 0) {
                hasEnded = true;
                continue;
            }
        }
        if (!hasEnded) {
            characters.push(className[i]);
            continue;
        }
        else {
            after.push(className[i]);
        }
    }
    return {
        after: after.join(""),
        before: before.join(""),
        characters: characters.join("")
    };
}
function trimTailwindWhitespace(className) {
    return className.replace(/^_+|_+$/g, "");
}
function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = (0, options_js_1.getCommonOptions)(ctx);
    const syntax = options.syntax ?? defaultOptions.syntax;
    return {
        ...common,
        syntax
    };
}
//# sourceMappingURL=enforce-consistent-variable-syntax.js.map
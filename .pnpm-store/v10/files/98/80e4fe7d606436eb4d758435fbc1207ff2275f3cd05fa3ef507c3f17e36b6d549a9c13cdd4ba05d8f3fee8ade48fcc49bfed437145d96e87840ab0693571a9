import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { ATTRIBUTE_SCHEMA, CALLEE_SCHEMA, TAG_SCHEMA, VARIABLE_SCHEMA } from "../options/descriptions.js";
import { createGetDissectedClasses } from "../tailwindcss/dissect-classes.js";
import { buildClass } from "../utils/class.js";
import { lintClasses } from "../utils/lint.js";
import { getCommonOptions } from "../utils/options.js";
import { createRuleListener } from "../utils/rule.js";
import { getTailwindcssVersion, TailwindcssVersion } from "../async-utils/tailwindcss.js";
import { splitClasses } from "../utils/utils.js";
const defaultOptions = {
    attributes: DEFAULT_ATTRIBUTE_NAMES,
    callees: DEFAULT_CALLEE_NAMES,
    syntax: "shorthand",
    tags: DEFAULT_TAG_NAMES,
    variables: DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/enforce-consistent-variable-syntax.md";
export const enforceConsistentVariableSyntax = {
    name: "enforce-consistent-variable-syntax",
    rule: {
        create: ctx => createRuleListener(ctx, initialize, getOptions, lintLiterals),
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
                        ...CALLEE_SCHEMA,
                        ...ATTRIBUTE_SCHEMA,
                        ...VARIABLE_SCHEMA,
                        ...TAG_SCHEMA,
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
    createGetDissectedClasses();
}
function lintLiterals(ctx, literals) {
    const getDissectedClasses = createGetDissectedClasses();
    const { syntax, tailwindConfig, tsconfig } = getOptions(ctx);
    const { major } = getTailwindcssVersion();
    for (const literal of literals) {
        const classes = splitClasses(literal.content);
        const { dissectedClasses } = getDissectedClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        lintClasses(ctx, literal, className => {
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
                    const fixedClass = major >= TailwindcssVersion.V4
                        ? buildClass({ ...dissectedClass, base: [...beforeSquareBrackets, `(${characters})`, ...afterSquareBrackets].join("") })
                        : buildClass({ ...dissectedClass, base: [...beforeSquareBrackets, `[${characters}]`, ...afterSquareBrackets].join("") });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
                if (isBeginningOfArbitraryShorthand(charactersSquareBrackets)) {
                    if (major <= TailwindcssVersion.V3) {
                        return;
                    }
                    const fixedClass = buildClass({
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
                    const fixedClass = buildClass({
                        ...dissectedClass,
                        base: [...beforeSquareBrackets, `[var(${charactersSquareBrackets})]`, ...afterSquareBrackets].join("")
                    });
                    return {
                        fix: fixedClass,
                        message: `Incorrect variable syntax: "${className}".`
                    };
                }
                if (isBeginningOfArbitraryShorthand(charactersParentheses)) {
                    const fixedClass = buildClass({
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
export function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = getCommonOptions(ctx);
    const syntax = options.syntax ?? defaultOptions.syntax;
    return {
        ...common,
        syntax
    };
}
//# sourceMappingURL=enforce-consistent-variable-syntax.js.map
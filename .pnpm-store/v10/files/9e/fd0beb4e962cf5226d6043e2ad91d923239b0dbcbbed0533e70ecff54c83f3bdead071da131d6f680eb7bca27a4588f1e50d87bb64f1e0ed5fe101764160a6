import { DEFAULT_ATTRIBUTE_NAMES, DEFAULT_CALLEE_NAMES, DEFAULT_TAG_NAMES, DEFAULT_VARIABLE_NAMES } from "../options/default-options.js";
import { ATTRIBUTE_SCHEMA, CALLEE_SCHEMA, ENTRYPOINT_SCHEMA, TAG_SCHEMA, TAILWIND_CONFIG_SCHEMA, TSCONFIG_SCHEMA, VARIABLE_SCHEMA } from "../options/descriptions.js";
import { createGetDissectedClasses } from "../tailwindcss/dissect-classes.js";
import { buildClass } from "../utils/class.js";
import { lintClasses } from "../utils/lint.js";
import { getCommonOptions } from "../utils/options.js";
import { createRuleListener } from "../utils/rule.js";
import { getTailwindcssVersion, TailwindcssVersion } from "../async-utils/tailwindcss.js";
import { augmentMessageWithWarnings, splitClasses } from "../utils/utils.js";
const defaultOptions = {
    attributes: DEFAULT_ATTRIBUTE_NAMES,
    callees: DEFAULT_CALLEE_NAMES,
    tags: DEFAULT_TAG_NAMES,
    variables: DEFAULT_VARIABLE_NAMES
};
const DOCUMENTATION_URL = "https://github.com/schoero/eslint-plugin-better-tailwindcss/blob/main/docs/rules/enforce-consistent-important-position.md";
export const enforceConsistentImportantPosition = {
    name: "enforce-consistent-important-position",
    rule: {
        create: ctx => createRuleListener(ctx, initialize, getOptions, lintLiterals),
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
                        ...CALLEE_SCHEMA,
                        ...ATTRIBUTE_SCHEMA,
                        ...VARIABLE_SCHEMA,
                        ...TAG_SCHEMA,
                        ...ENTRYPOINT_SCHEMA,
                        ...TAILWIND_CONFIG_SCHEMA,
                        ...TSCONFIG_SCHEMA,
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
    createGetDissectedClasses();
}
function lintLiterals(ctx, literals) {
    const getDissectedClasses = createGetDissectedClasses();
    const { position, tailwindConfig, tsconfig } = getOptions(ctx);
    const { major } = getTailwindcssVersion();
    for (const literal of literals) {
        const classes = splitClasses(literal.content);
        const { dissectedClasses, warnings } = getDissectedClasses({ classes, configPath: tailwindConfig, cwd: ctx.cwd, tsconfigPath: tsconfig });
        lintClasses(ctx, literal, (className, index, after) => {
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
            if (major <= TailwindcssVersion.V3 && position === "recommended") {
                warnings.push({
                    option: "position",
                    title: `The "${position}" position is not supported in Tailwind CSS v3`
                });
            }
            const fix = position === "recommended"
                ? buildClass({ ...dissectedClass, important: [false, true] })
                : buildClass({ ...dissectedClass, important: [true, false] });
            return {
                fix,
                message: augmentMessageWithWarnings(`Incorrect important position. "${className}" should be "${fix}".`, DOCUMENTATION_URL, warnings)
            };
        });
    }
}
export function getOptions(ctx) {
    const options = ctx.options[0] ?? {};
    const common = getCommonOptions(ctx);
    const position = options.position ?? (getTailwindcssVersion().major === TailwindcssVersion.V3 ? "legacy" : "recommended");
    return {
        ...common,
        position
    };
}
//# sourceMappingURL=enforce-consistent-important-position.js.map
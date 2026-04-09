import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Shorthands = [RegExp[], string[]][][];
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        entryPoint?: string;
        tailwindConfig?: string;
        tsconfig?: string;
    }>
];
export declare const enforceShorthandClasses: ESLintRule<Options>;
export declare const shorthands: [RegExp[], string[]][][];
export declare function getOptions(ctx: Rule.RuleContext): {
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=enforce-shorthand-classes.d.ts.map
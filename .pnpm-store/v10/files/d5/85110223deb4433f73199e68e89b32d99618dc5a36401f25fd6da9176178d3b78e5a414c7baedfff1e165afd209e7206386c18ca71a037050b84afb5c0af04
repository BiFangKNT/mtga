import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        syntax?: "arbitrary" | "parentheses" | "shorthand" | "variable";
    }>
];
export declare const enforceConsistentVariableSyntax: ESLintRule<Options>;
export declare function getOptions(ctx: Rule.RuleContext): {
    syntax: "shorthand" | "arbitrary" | "parentheses" | "variable";
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=enforce-consistent-variable-syntax.d.ts.map
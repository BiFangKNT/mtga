import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        entryPoint?: string;
        order?: "asc" | "desc" | "improved" | "official";
        tailwindConfig?: string;
        tsconfig?: string;
    }>
];
export declare const enforceConsistentClassOrder: ESLintRule<Options>;
export declare function getOptions(ctx: Rule.RuleContext): {
    order: "asc" | "desc" | "improved" | "official";
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=enforce-consistent-class-order.d.ts.map
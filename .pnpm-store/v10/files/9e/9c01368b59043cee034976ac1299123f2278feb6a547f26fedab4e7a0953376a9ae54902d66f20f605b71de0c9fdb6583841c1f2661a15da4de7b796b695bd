import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        entryPoint?: string;
        position?: "legacy" | "recommended";
        tailwindConfig?: string;
        tsconfig?: string;
    }>
];
export declare const enforceConsistentImportantPosition: ESLintRule<Options>;
export declare function getOptions(ctx: Rule.RuleContext): {
    position: "legacy" | "recommended";
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=enforce-consistent-important-position.d.ts.map
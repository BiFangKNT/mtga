import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        restrict?: (string | {
            pattern: string;
            fix?: string;
            message?: string;
        })[];
    }>
];
export declare const noRestrictedClasses: ESLintRule<Options>;
export declare function getOptions(ctx: Rule.RuleContext): {
    restrict: (string | {
        pattern: string;
        fix?: string;
        message?: string;
    })[];
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=no-restricted-classes.d.ts.map
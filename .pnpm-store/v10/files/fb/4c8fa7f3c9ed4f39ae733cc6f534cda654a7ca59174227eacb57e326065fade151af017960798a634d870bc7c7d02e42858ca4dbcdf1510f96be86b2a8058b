import type { Rule } from "eslint";
import type { AttributeOption, CalleeOption, ESLintRule, TagOption, VariableOption } from "../types/rule.js";
export type Options = [
    Partial<AttributeOption & CalleeOption & TagOption & VariableOption & {
        detectComponentClasses?: boolean;
        entryPoint?: string;
        ignore?: string[];
        tailwindConfig?: string;
        tsconfig?: string;
    }>
];
export declare const DEFAULT_IGNORED_UNREGISTERED_CLASSES: never[];
export declare const noUnregisteredClasses: ESLintRule<Options>;
export declare function getOptions(ctx: Rule.RuleContext): {
    detectComponentClasses: boolean;
    ignore: string[];
    attributes: any;
    callees: any;
    tags: any;
    tailwindConfig: any;
    tsconfig: any;
    variables: any;
};
//# sourceMappingURL=no-unregistered-classes.d.ts.map
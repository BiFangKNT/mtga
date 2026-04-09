import { MatcherType } from "../../types/rule.js";
export const CVA_STRINGS = [
    "cva",
    [
        {
            match: MatcherType.String
        }
    ]
];
export const CVA_VARIANT_VALUES = [
    "cva",
    [
        {
            match: MatcherType.ObjectValue,
            pathPattern: "^variants.*$"
        }
    ]
];
export const CVA_COMPOUND_VARIANTS_CLASS = [
    "cva",
    [
        {
            match: MatcherType.ObjectValue,
            pathPattern: "^compoundVariants\\[\\d+\\]\\.(?:className|class)$"
        }
    ]
];
/** @see https://github.com/joe-bell/cva */
export const CVA = [
    CVA_STRINGS,
    CVA_VARIANT_VALUES,
    CVA_COMPOUND_VARIANTS_CLASS
];
//# sourceMappingURL=cva.js.map
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CVA = exports.CVA_COMPOUND_VARIANTS_CLASS = exports.CVA_VARIANT_VALUES = exports.CVA_STRINGS = void 0;
const rule_js_1 = require("../../types/rule.js");
exports.CVA_STRINGS = [
    "cva",
    [
        {
            match: rule_js_1.MatcherType.String
        }
    ]
];
exports.CVA_VARIANT_VALUES = [
    "cva",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^variants.*$"
        }
    ]
];
exports.CVA_COMPOUND_VARIANTS_CLASS = [
    "cva",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^compoundVariants\\[\\d+\\]\\.(?:className|class)$"
        }
    ]
];
/** @see https://github.com/joe-bell/cva */
exports.CVA = [
    exports.CVA_STRINGS,
    exports.CVA_VARIANT_VALUES,
    exports.CVA_COMPOUND_VARIANTS_CLASS
];
//# sourceMappingURL=cva.js.map
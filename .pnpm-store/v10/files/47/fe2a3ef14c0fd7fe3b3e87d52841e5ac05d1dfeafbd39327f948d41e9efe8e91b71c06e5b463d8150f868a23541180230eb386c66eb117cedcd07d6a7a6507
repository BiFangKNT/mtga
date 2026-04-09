"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CLB = exports.CLB_COMPOUND_VARIANTS_CLASSES = exports.CLB_VARIANT_VALUES = exports.CLB_BASE_VALUES = void 0;
const rule_js_1 = require("../../types/rule.js");
exports.CLB_BASE_VALUES = [
    "clb",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^base$"
        }
    ]
];
exports.CLB_VARIANT_VALUES = [
    "clb",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^variants.*$"
        }
    ]
];
exports.CLB_COMPOUND_VARIANTS_CLASSES = [
    "clb",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^compoundVariants\\[\\d+\\]\\.classes$"
        }
    ]
];
/** @see https://github.com/crswll/clb */
exports.CLB = [
    exports.CLB_BASE_VALUES,
    exports.CLB_VARIANT_VALUES,
    exports.CLB_COMPOUND_VARIANTS_CLASSES
    // TODO: add object key matcher: classes
];
//# sourceMappingURL=clb.js.map
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TV = exports.TV_COMPOUND_SLOTS_CLASS = exports.TV_COMPOUND_VARIANTS_CLASS = exports.TV_SLOTS_VALUES = exports.TV_BASE_VALUES = exports.TV_VARIANT_VALUES = exports.TV_STRINGS = void 0;
const rule_js_1 = require("../../types/rule.js");
exports.TV_STRINGS = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.String
        }
    ]
];
exports.TV_VARIANT_VALUES = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^variants.*$"
        }
    ]
];
exports.TV_BASE_VALUES = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^base$"
        }
    ]
];
exports.TV_SLOTS_VALUES = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^slots.*$"
        }
    ]
];
exports.TV_COMPOUND_VARIANTS_CLASS = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^compoundVariants\\[\\d+\\]\\.(?:className|class).*$"
        }
    ]
];
exports.TV_COMPOUND_SLOTS_CLASS = [
    "tv",
    [
        {
            match: rule_js_1.MatcherType.ObjectValue,
            pathPattern: "^compoundSlots\\[\\d+\\]\\.(?:className|class).*$"
        }
    ]
];
/** @see https://github.com/nextui-org/tailwind-variants?tab=readme-ov-file */
exports.TV = [
    exports.TV_STRINGS,
    exports.TV_VARIANT_VALUES,
    exports.TV_COMPOUND_VARIANTS_CLASS,
    exports.TV_BASE_VALUES,
    exports.TV_SLOTS_VALUES,
    exports.TV_COMPOUND_SLOTS_CLASS
];
//# sourceMappingURL=tv.js.map
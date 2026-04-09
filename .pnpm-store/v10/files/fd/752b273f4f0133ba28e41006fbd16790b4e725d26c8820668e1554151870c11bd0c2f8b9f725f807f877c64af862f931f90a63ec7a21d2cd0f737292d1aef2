"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEFAULT_TAG_NAMES = exports.DEFAULT_VARIABLE_NAMES = exports.DEFAULT_ATTRIBUTE_NAMES = exports.DEFAULT_CALLEE_NAMES = void 0;
const cc_js_1 = require("./callees/cc.js");
const clb_js_1 = require("./callees/clb.js");
const clsx_js_1 = require("./callees/clsx.js");
const cn_js_1 = require("./callees/cn.js");
const cnb_js_1 = require("./callees/cnb.js");
const ctl_js_1 = require("./callees/ctl.js");
const cva_js_1 = require("./callees/cva.js");
const cx_js_1 = require("./callees/cx.js");
const dcnb_js_1 = require("./callees/dcnb.js");
const objstr_js_1 = require("./callees/objstr.js");
const tv_js_1 = require("./callees/tv.js");
const twJoin_js_1 = require("./callees/twJoin.js");
const twMerge_js_1 = require("./callees/twMerge.js");
const rule_js_1 = require("../types/rule.js");
exports.DEFAULT_CALLEE_NAMES = [
    ...cc_js_1.CC,
    ...clb_js_1.CLB,
    ...clsx_js_1.CLSX,
    ...cn_js_1.CN,
    ...cnb_js_1.CNB,
    ...ctl_js_1.CTL,
    ...cva_js_1.CVA,
    ...cx_js_1.CX,
    ...dcnb_js_1.DCNB,
    ...objstr_js_1.OBJSTR,
    ...tv_js_1.TV,
    ...twJoin_js_1.TW_JOIN,
    ...twMerge_js_1.TW_MERGE
];
exports.DEFAULT_ATTRIBUTE_NAMES = [
    // general
    "^class(?:Name)?$",
    [
        "^class(?:Name)?$", [
            {
                match: rule_js_1.MatcherType.String
            }
        ]
    ],
    // angular
    "(?:^\\[class\\]$)|(?:^\\[ngClass\\]$)",
    [
        "(?:^\\[class\\]$)|(?:^\\[ngClass\\]$)", [
            {
                match: rule_js_1.MatcherType.String
            },
            {
                match: rule_js_1.MatcherType.ObjectKey
            }
        ]
    ],
    // vue
    [
        "^v-bind:class$", [
            {
                match: rule_js_1.MatcherType.String
            },
            {
                match: rule_js_1.MatcherType.ObjectKey
            }
        ]
    ],
    // astro
    [
        "^class:list$", [
            {
                match: rule_js_1.MatcherType.String
            },
            {
                match: rule_js_1.MatcherType.ObjectKey
            }
        ]
    ]
];
exports.DEFAULT_VARIABLE_NAMES = [
    [
        "^classNames?$", [
            {
                match: rule_js_1.MatcherType.String
            }
        ]
    ],
    [
        "^classes$", [
            {
                match: rule_js_1.MatcherType.String
            }
        ]
    ],
    [
        "^styles?$", [
            {
                match: rule_js_1.MatcherType.String
            }
        ]
    ]
];
exports.DEFAULT_TAG_NAMES = [];
//# sourceMappingURL=default-options.js.map
import { CC } from "./callees/cc.js";
import { CLB } from "./callees/clb.js";
import { CLSX } from "./callees/clsx.js";
import { CN } from "./callees/cn.js";
import { CNB } from "./callees/cnb.js";
import { CTL } from "./callees/ctl.js";
import { CVA } from "./callees/cva.js";
import { CX } from "./callees/cx.js";
import { DCNB } from "./callees/dcnb.js";
import { OBJSTR } from "./callees/objstr.js";
import { TV } from "./callees/tv.js";
import { TW_JOIN } from "./callees/twJoin.js";
import { TW_MERGE } from "./callees/twMerge.js";
import { MatcherType } from "../types/rule.js";
export const DEFAULT_CALLEE_NAMES = [
    ...CC,
    ...CLB,
    ...CLSX,
    ...CN,
    ...CNB,
    ...CTL,
    ...CVA,
    ...CX,
    ...DCNB,
    ...OBJSTR,
    ...TV,
    ...TW_JOIN,
    ...TW_MERGE
];
export const DEFAULT_ATTRIBUTE_NAMES = [
    // general
    "^class(?:Name)?$",
    [
        "^class(?:Name)?$", [
            {
                match: MatcherType.String
            }
        ]
    ],
    // angular
    "(?:^\\[class\\]$)|(?:^\\[ngClass\\]$)",
    [
        "(?:^\\[class\\]$)|(?:^\\[ngClass\\]$)", [
            {
                match: MatcherType.String
            },
            {
                match: MatcherType.ObjectKey
            }
        ]
    ],
    // vue
    [
        "^v-bind:class$", [
            {
                match: MatcherType.String
            },
            {
                match: MatcherType.ObjectKey
            }
        ]
    ],
    // astro
    [
        "^class:list$", [
            {
                match: MatcherType.String
            },
            {
                match: MatcherType.ObjectKey
            }
        ]
    ]
];
export const DEFAULT_VARIABLE_NAMES = [
    [
        "^classNames?$", [
            {
                match: MatcherType.String
            }
        ]
    ],
    [
        "^classes$", [
            {
                match: MatcherType.String
            }
        ]
    ],
    [
        "^styles?$", [
            {
                match: MatcherType.String
            }
        ]
    ]
];
export const DEFAULT_TAG_NAMES = [];
//# sourceMappingURL=default-options.js.map
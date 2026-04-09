import { Rune } from "./runes";
import { Casing } from "./types";
export declare enum TermType {
    Fuzzy = 0,
    Exact = 1,
    Prefix = 2,
    Suffix = 3,
    Equal = 4
}
export declare const termTypeMap: {
    0: import("./algo").AlgoFn;
    1: import("./algo").AlgoFn;
    2: import("./algo").AlgoFn;
    3: import("./algo").AlgoFn;
    4: import("./algo").AlgoFn;
};
interface Term {
    typ: TermType;
    inv: boolean;
    text: Rune[];
    caseSensitive: boolean;
    normalize: boolean;
}
type TermSet = Term[];
export declare function buildPatternForExtendedMatch(fuzzy: boolean, caseMode: Casing, normalize: boolean, str: string): {
    str: string;
    termSets: TermSet[];
    sortable: boolean;
    cacheable: boolean;
    fuzzy: boolean;
};
export declare const buildPatternForBasicMatch: (query: string, casing: Casing, normalize: boolean) => {
    queryRunes: number[];
    caseSensitive: boolean;
};
export {};

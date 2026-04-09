import { Slab } from "./slab";
import { Rune } from "./runes";
export interface Result {
    start: number;
    end: number;
    score: number;
}
export declare const SCORE_MATCH = 16, SCORE_GAP_START = -3, SCORE_GAP_EXTENTION = -1, BONUS_BOUNDARY: number, BONUS_NON_WORD: number, BONUS_CAMEL_123: number, BONUS_CONSECUTIVE: number, BONUS_FIRST_CHAR_MULTIPLIER = 2;
export type AlgoFn = (caseSensitive: boolean, normalize: boolean, forward: boolean, input: Rune[], pattern: Rune[], withPos: boolean, slab: Slab | null) => [Result, Set<number> | null];
export declare const fuzzyMatchV2: AlgoFn;
export declare const fuzzyMatchV1: AlgoFn;
export declare const exactMatchNaive: AlgoFn;
export declare const prefixMatch: AlgoFn;
export declare const suffixMatch: AlgoFn;
export declare const equalMatch: AlgoFn;

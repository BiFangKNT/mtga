import type { Result } from "./algo";
import type { SyncFinder, AsyncFinder } from "./finders";
export interface Token {
    cancelled: boolean;
}
export type Casing = "smart-case" | "case-sensitive" | "case-insensitive";
export interface FzfResultItem<U = string> extends Result {
    item: U;
    positions: Set<number>;
}
export type Selector<U> = BaseOptions<U>["selector"];
export type Tiebreaker<U> = (a: FzfResultItem<U>, b: FzfResultItem<U>, selector: Selector<U>) => number;
export interface BaseOptions<U> {
    /**
     * If `limit` is 32, top 32 items that matches your query will be returned.
     * By default all matched items are returned.
     *
     * @defaultValue `Infinity`
     */
    limit: number;
    /**
     * For each item in the list, target a specific property of the item to search for.
     */
    selector: (v: U) => string;
    /**
     * Defines what type of case sensitive search you want.
     *
     * @defaultValue `"smart-case"`
     */
    casing: Casing;
    /**
     * If true, FZF will try to remove diacritics from list items.
     * This is useful if the list contains items with diacritics but
     * you want to query with plain A-Z letters.
     *
     * @example
     * Zoë →  Zoe
     * blessèd →  blessed
     *
     * @defaultValue `true`
     */
    normalize: boolean;
    /**
     * Fuzzy algo to choose. Each algo has their own advantages, see here:
     * https://github.com/junegunn/fzf/blob/4c9cab3f8ae7b55f7124d7c3cf7ac6b4cc3db210/src/algo/algo.go#L5
     * If asssigned `false`, an exact match will be made instead of a fuzzy one.
     *
     * @defaultValue `"v2"`
     */
    fuzzy: "v1" | "v2" | false;
    /**
     * A list of functions that act as fallback and help to
     * sort result entries when the score between two entries is tied.
     *
     * Consider a tiebreaker to be a [JS array sort](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort)
     * compare function with an added third argument which is `options.selector`.
     *
     * If multiple tiebreakers are given, they are evaluated left to right until
     * one breaks the tie.
     *
     * Note that tiebreakers cannot be used if `sort=false`.
     *
     * FZF ships with these tiebreakers:
     * - `byLengthAsc`
     * - `byStartAsc`
     *
     * @defaultValue `[]`
     *
     * @example
     * ```js
     * function byLengthAsc(a, b, selector) {
     *   return selector(a.item).length - selector(b.item).length;
     * }
     *
     * const fzf = new Fzf(list, { tiebreakers: [byLengthAsc] })
     * ```
     * This will result in following result entries having same score sorted like this:
     *    FROM                TO
     * axaa                axaa
     * bxbbbb              bxbbbb
     * cxcccccccccc        dxddddddd
     * dxddddddd           cxcccccccccc
     */
    tiebreakers: Tiebreaker<U>[];
    /**
     * If `true`, result items will be sorted in descending order by their score.
     *
     * If `false`, result items won't be sorted and tiebreakers won't affect the
     * sort order either. In this case, the items are returned in the same order
     * as they are in the input list.
     *
     * @defaultValue `true`
     */
    sort: boolean;
    /**
     * If `false`, matching will be done from backwards.
     *
     * @defaultValue `true`
     *
     * @example
     * /breeds/pyrenees when queried with "re"
     * with forward=true  : /b**re**eds/pyrenees
     * with forward=false : /breeds/py**re**nees
     *
     * Doing forward=false is useful, for example, if one needs to match a file
     * path and they prefer querying for the file name over directory names
     * present in the path.
     */
    forward: boolean;
}
export type SyncOptions<U> = BaseOptions<U> & {
    /**
     * A function that is responsible for matching list items with the query.
     *
     * We ship with two match functions - `basicMatch` and `extendedMatch`.
     *
     * If `extendedMatch` is used, you can add special patterns to narrow down your search.
     * To read about how they can be used, see [this section](https://github.com/junegunn/fzf/tree/7191ebb615f5d6ebbf51d598d8ec853a65e2274d#search-syntax).
     * For a quick glance, see [this piece](https://github.com/junegunn/fzf/blob/764316a53d0eb60b315f0bbcd513de58ed57a876/src/pattern.go#L12-L19).
     *
     * @defaultValue `basicMatch`
     */
    match: (this: SyncFinder<ReadonlyArray<U>>, query: string) => FzfResultItem<U>[];
};
export type AsyncOptions<U> = BaseOptions<U> & {
    /**
     * A function that is responsible for matching list items with the query.
     *
     * We ship with two match functions - `asyncBasicMatch` and `asyncExtendedMatch`.
     *
     * If `asyncExtendedMatch` is used, you can add special patterns to narrow down your search.
     * To read about how they can be used, see [this section](https://github.com/junegunn/fzf/tree/7191ebb615f5d6ebbf51d598d8ec853a65e2274d#search-syntax).
     * For a quick glance, see [this piece](https://github.com/junegunn/fzf/blob/764316a53d0eb60b315f0bbcd513de58ed57a876/src/pattern.go#L12-L19).
     *
     * @defaultValue `asyncBasicMatch`
     */
    match: (this: AsyncFinder<ReadonlyArray<U>>, query: string, token: Token) => Promise<FzfResultItem<U>[]>;
};

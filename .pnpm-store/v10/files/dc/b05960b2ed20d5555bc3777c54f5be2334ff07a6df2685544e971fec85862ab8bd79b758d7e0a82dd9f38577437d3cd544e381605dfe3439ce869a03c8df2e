import { SyncFinder, AsyncFinder } from "./finders";
import type { ArrayElement, SyncOptionsTuple, SyncOptsToUse, AsyncOptionsTuple, AsyncOptsToUse } from "./finders";
import type { SyncOptions, AsyncOptions } from "./types";
export type { FzfResultItem, Selector, Tiebreaker } from "./types";
export * from "./matchers";
export * from "./tiebreakers";
export type FzfOptions<U = string> = U extends string ? SyncOptsToUse<U> : SyncOptsToUse<U> & {
    selector: SyncOptions<U>["selector"];
};
export declare class Fzf<L extends ReadonlyArray<any>> {
    private finder;
    find: SyncFinder<L>["find"];
    constructor(list: L, ...optionsTuple: SyncOptionsTuple<ArrayElement<L>>);
}
export type AsyncFzfOptions<U = string> = U extends string ? AsyncOptsToUse<U> : AsyncOptsToUse<U> & {
    selector: AsyncOptions<U>["selector"];
};
export declare class AsyncFzf<L extends ReadonlyArray<any>> {
    private finder;
    find: AsyncFinder<L>["find"];
    constructor(list: L, ...optionsTuple: AsyncOptionsTuple<ArrayElement<L>>);
}
